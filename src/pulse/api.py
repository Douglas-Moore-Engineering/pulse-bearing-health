"""Authenticated assessment boundary with optional single-node durable receipts."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sqlite3
import threading
import time
from pathlib import Path
from typing import Annotated, Literal
from uuid import UUID

import httpx
import jwt
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ConfigDict, Field, field_validator
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from pulse.core import encode, features
from pulse.assessment_store import AssessmentStore, WindowConflict
from pulse.reference_detector import ReferenceDetector, ReferenceOrderError, ASSET as REFERENCE_ASSET
from pulse.alert_ledger import AlertConflict
from pulse.adjudication import AdjudicationLedger
from pulse.intake import validate_intake


@dataclass(frozen=True)
class Settings:
    tenant: str
    audience: str
    allowed_clients: tuple[str, ...]
    role: str = 'Pulse.Assess'
    asset_grants: dict[str, tuple[str, ...]] | None = None

    @classmethod
    def from_env(cls):
        tenant = str(UUID(os.environ['PULSE_TENANT_ID']))
        audience = str(UUID(os.environ['PULSE_API_CLIENT_ID']))
        clients = tuple(str(UUID(x.strip())) for x in os.environ['PULSE_ALLOWED_CLIENT_IDS'].split(','))
        if not clients:
            raise ValueError('At least one authorized client is required')
        grants = json.loads(os.environ['PULSE_ASSET_GRANTS'])
        if (not isinstance(grants, dict) or set(grants) != set(clients) or
                any(not isinstance(assets, list) or not assets or
                    any(not isinstance(a, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', a)
                        for a in assets) for assets in grants.values())):
            raise ValueError('Explicit asset grants for every allowed client are required')
        return cls(tenant, audience, clients, asset_grants={k: tuple(v) for k, v in grants.items()})

    @property
    def issuer(self):
        return f'https://login.microsoftonline.com/{self.tenant}/v2.0'


class EntraVerifier:
    """RS256 v2 app-token verification with bounded, serialized JWKS refresh."""
    def __init__(self, settings):
        self.settings = settings
        self.keys = {}
        self.last_attempt = -float('inf')
        self.loaded_at = -float('inf')
        self.lock = threading.Lock()

    def key(self, kid):
        with self.lock:
            now = time.monotonic()
            if (kid not in self.keys or now-self.loaded_at > 3600) and now-self.last_attempt >= 60:
                self.last_attempt = now
                try:
                    response = httpx.get(
                        f'https://login.microsoftonline.com/{self.settings.tenant}/discovery/v2.0/keys',
                        timeout=5, follow_redirects=False)
                    response.raise_for_status()
                    self.keys = {k['kid']: jwt.PyJWK.from_dict(k).key for k in response.json()['keys']
                                 if k.get('kty') == 'RSA' and k.get('use', 'sig') == 'sig'}
                    self.loaded_at = now
                except (httpx.HTTPError, ValueError, KeyError, jwt.PyJWTError) as exc:
                    raise HTTPException(503, 'Identity keys unavailable') from exc
            if now-self.loaded_at > 3600:
                raise HTTPException(503, 'Identity keys expired')
            if kid not in self.keys:
                raise HTTPException(401, 'Unknown signing key')
            return self.keys[kid]

    def __call__(self, token):
        try:
            header = jwt.get_unverified_header(token)
            if header.get('alg') != 'RS256' or not isinstance(header.get('kid'), str):
                raise jwt.InvalidTokenError()
            claims = jwt.decode(token, self.key(header['kid']), algorithms=['RS256'],
                                audience=self.settings.audience, issuer=self.settings.issuer,
                                options={'require': ['exp', 'iat', 'nbf', 'iss', 'aud', 'tid', 'oid', 'azp', 'ver']})
            if claims['tid'] != self.settings.tenant or claims['ver'] != '2.0':
                raise jwt.InvalidTokenError()
            if claims['azp'] not in self.settings.allowed_clients or self.settings.role not in claims.get('roles', []):
                raise HTTPException(403, 'Client or application role not authorized')
            return claims
        except jwt.PyJWTError as exc:
            raise HTTPException(401, 'Invalid access token') from exc


Sample = Annotated[float, Field(strict=True, allow_inf_nan=False, ge=-1000, le=1000)]


class Assessment(BaseModel):
    model_config = ConfigDict(extra='forbid')
    schema_version: Literal['1']
    asset_id: Annotated[str, Field(pattern=r'^[A-Za-z0-9_-]{1,64}$')]
    window_id: Annotated[str, Field(pattern=r'^[A-Za-z0-9_-]{1,128}$')]
    observed_at: datetime
    source_sha256: Annotated[str, Field(pattern=r'^[a-f0-9]{64}$')]
    unit: Literal['g', 'm/s2']
    sample_rate_hz: Annotated[float, Field(strict=True, gt=0, le=256000, allow_inf_nan=False)]
    samples: Annotated[list[Sample], Field(min_length=2, max_length=4096)]

    @field_validator('observed_at')
    @classmethod
    def utc_required(cls, value):
        if value.tzinfo is None or value.utcoffset().total_seconds() != 0:
            raise ValueError('UTC timestamp required')
        if (value-datetime.now(timezone.utc)).total_seconds() > 60:
            raise ValueError('Observation is in the future')
        return value


class RequestBoundary:
    """Bound bytes before JSON parsing, including chunked requests, and bound receive time."""
    def __init__(self, app, max_bytes=131072):
        self.app, self.max_bytes = app, max_bytes

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http' or scope['method'] != 'POST':
            return await self.app(scope, receive, send)
        headers = dict(scope['headers'])
        if headers.get(b'content-encoding', b'identity') != b'identity':
            return await JSONResponse({'detail': 'Encoded bodies unsupported'}, 415)(scope, receive, send)
        chunks, size = [], 0
        deadline = asyncio.get_running_loop().time()+10
        while True:
            try:
                message = await asyncio.wait_for(receive(), max(.001, deadline-asyncio.get_running_loop().time()))
            except asyncio.TimeoutError:
                return await JSONResponse({'detail': 'Body timeout'}, 408)(scope, receive, send)
            if message['type'] == 'http.disconnect':
                return
            chunk = message.get('body', b'')
            size += len(chunk)
            if size > self.max_bytes:
                return await JSONResponse({'detail': 'Body too large'}, 413)(scope, receive, send)
            chunks.append(chunk)
            if not message.get('more_body', False):
                break
        body = b''.join(chunks)
        delivered = False

        async def bounded_receive():
            nonlocal delivered
            if delivered:
                return await receive()
            delivered = True
            return {'type': 'http.request', 'body': body, 'more_body': False}
        await self.app(scope, bounded_receive, send)


class ReferenceAssessment(BaseModel):
    model_config = ConfigDict(extra='forbid')
    asset_id: Literal['ims-run2-bearing1-reference']
    window_id: Annotated[str, Field(pattern=r'^[A-Za-z0-9_-]{1,128}$')]
    source_timestamp: Annotated[str, Field(pattern=r'^\d{4}\.\d{2}\.\d{2}\.\d{2}\.\d{2}\.\d{2}$')]
    source_sha256: Annotated[str, Field(pattern=r'^[a-f0-9]{64}$')]
    dataset_id: Literal['DS-IMS']
    source_run: Literal['2nd_test']
    amplitude_unit: Literal['native_unknown']
    sample_count: Literal[20480]
    sample_rate_hz: Literal[20000]
    rms_native: Annotated[float, Field(strict=True, ge=0, le=1000, allow_inf_nan=False)]

    @field_validator('source_timestamp')
    @classmethod
    def valid_source_time(cls, value):
        datetime.strptime(value, '%Y.%m.%d.%H.%M.%S')
        return value


class ClosureRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    rationale: Annotated[str, Field(min_length=1, max_length=4096)]
    evidence: Annotated[list[Annotated[str, Field(min_length=1, max_length=2048)]], Field(min_length=1, max_length=100)]


class ReviewRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    outcome: Literal['confirmed_fault', 'nuisance', 'unresolved']
    rationale: Annotated[str, Field(min_length=1, max_length=4096)]
    evidence: Annotated[list[Annotated[str, Field(min_length=1, max_length=2048)]], Field(max_length=100)]
    supersedes: str | None = None


def create_app(settings=None, verifier=None, store=None, reference=None, review_db=None, intake_schema=None):
    settings = settings or Settings.from_env()  # missing identity configuration fails startup
    verify = verifier or EntraVerifier(settings)
    if os.environ.get('PULSE_PILOT_COMPONENTS') == '1':
        review_db = review_db or os.environ['PULSE_REVIEW_DB']
        if not Path(review_db).is_absolute() or not Path(review_db).parent.is_dir():
            raise ValueError('Existing absolute review storage directory required')
        if intake_schema is None:
            intake_schema = json.loads(Path(os.environ['PULSE_INTAKE_SCHEMA']).read_text(encoding='utf-8'))
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(intake_schema)
    if store is None and os.environ.get('PULSE_ASSESSMENT_DB'):
        store = AssessmentStore(os.environ['PULSE_ASSESSMENT_DB'])
    if reference is None and os.environ.get('PULSE_REFERENCE_DETECTOR') == '1':
        reference = ReferenceDetector(os.environ['PULSE_ASSESSMENT_DB'])
    app = FastAPI(title='Pulse degradation assessment', docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(RequestBoundary)
    registry = CollectorRegistry()
    count = Counter('pulse_assessments_total', 'Completed assessment requests', ['status'], registry=registry)
    duration = Histogram('pulse_assessment_seconds', 'Assessment computation time', registry=registry,
                         buckets=(.005, .01, .025, .05, .1, .25, .5, 1, 5))

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request, exc):
        # Avoid reflecting samples, tokens or nonfinite JSON values in error messages.
        return JSONResponse({'detail': 'Invalid assessment contract'}, status_code=422)

    def authorize(authorization: Annotated[str | None, Header()] = None):
        if not authorization or not authorization.startswith('Bearer ') or len(authorization) > 16384:
            raise HTTPException(401, 'Bearer access token required')
        return verify(authorization[7:])

    def authorize_reference(claims):
        if reference is None:
            raise HTTPException(503, 'Reference detector is disabled')
        if settings.asset_grants is None or REFERENCE_ASSET not in settings.asset_grants.get(claims.get('azp'), ()):
            raise HTTPException(403, 'Client not authorized for the reference asset')

    def review_subject(event_id, claims):
        authorize_reference(claims)
        if 'Pulse.Review' not in claims.get('roles', []):
            raise HTTPException(403, 'Reviewer application role required')
        if review_db is None:
            raise HTTPException(503, 'Review storage is disabled')
        if not re.fullmatch(r'[a-f0-9]{64}', event_id):
            raise HTTPException(422, 'Invalid event ID')
        scope = json.dumps([settings.tenant, claims['oid']], separators=(',', ':'))
        with reference.connection() as db:
            row = db.execute('SELECT 1 FROM alerts WHERE event_id=? AND tenant=? AND asset=?',
                             (event_id, scope, REFERENCE_ASSET)).fetchone()
        if row is None:
            raise HTTPException(404, 'Reference event not found')
        return json.dumps([settings.tenant, claims['oid'], REFERENCE_ASSET, event_id], separators=(',', ':'))

    @app.post('/v1/intake/validate')
    def intake(document: dict, claims=Depends(authorize)):
        metadata = document.get('metadata')
        asset = metadata.get('asset_id') if isinstance(metadata, dict) else None
        if not isinstance(asset,str) or settings.asset_grants is None or asset not in settings.asset_grants.get(claims.get('azp'), ()):
            raise HTTPException(403, 'Client not authorized for this asset')
        if intake_schema is None:
            raise HTTPException(503, 'Intake validation disabled')
        return validate_intake(document, intake_schema)

    @app.post('/v1/reference/alerts/{event_id}/reviews')
    def append_review(event_id: str, request: ReviewRequest, claims=Depends(authorize)):
        ledger = None
        try:
            subject = review_subject(event_id, claims)
            ledger = AdjudicationLedger(review_db)
            reviewer = json.dumps([settings.tenant, claims['oid'], claims['azp']], separators=(',', ':'))
            identifier = ledger.append(subject, reviewer, request.outcome, request.rationale,
                                       request.evidence, request.supersedes)
            return {'review_id': identifier, 'principal_authenticated': True,
                    'human_identity_verified': False, 'evidence_verified': False, 'qualified_detector': False}
        except ValueError as exc:
            raise HTTPException(409, 'Invalid review or correction') from exc
        except sqlite3.Error as exc:
            raise HTTPException(503, 'Review storage unavailable') from exc
        finally:
            if ledger is not None: ledger.close()

    @app.get('/v1/reference/alerts/{event_id}/reviews')
    def review_history(event_id: str, claims=Depends(authorize)):
        ledger = None
        try:
            subject = review_subject(event_id, claims)
            ledger = AdjudicationLedger(review_db)
            return {'reviews': ledger.history(subject), 'qualified_detector': False}
        except sqlite3.Error as exc:
            raise HTTPException(503, 'Review storage unavailable') from exc
        finally:
            if ledger is not None: ledger.close()

    @app.post('/v1/reference/alerts/{event_id}/close')
    def close_incident(event_id: str, request: ClosureRequest, claims=Depends(authorize)):
        try:
            review_subject(event_id, claims)
            if 'Pulse.Close' not in claims.get('roles', []):
                raise HTTPException(403, 'Incident closure role required')
            scope = json.dumps([settings.tenant, claims['oid']], separators=(',', ':'))
            actor = json.dumps([settings.tenant, claims['oid'], claims['azp']], separators=(',', ':'))
            closure = reference.close_incident(scope, REFERENCE_ASSET, event_id,
                                               actor, request.rationale, request.evidence)
            return {'state': 'CLOSED', 'closure': closure, 'principal_authenticated': True,
                    'human_identity_verified': False, 'evidence_verified': False,
                    'qualified_detector': False}
        except KeyError as exc:
            raise HTTPException(404, 'Reference event not found') from exc
        except ValueError as exc:
            raise HTTPException(409, 'Invalid incident closure or conflicting disposition') from exc
        except sqlite3.Error as exc:
            raise HTTPException(503, 'Incident storage unavailable') from exc

    @app.get('/health/live')
    def live():
        return {'status': 'live'}

    @app.get('/health/ready')
    def ready():
        if store is not None:
            try:
                store.healthy()
            except sqlite3.Error as exc:
                raise HTTPException(503, 'Assessment storage unavailable') from exc
        return {'status': 'ready', 'assessment_available': True, 'qualified_alerts_available': False}

    @app.get('/metrics')
    def metrics():
        return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

    @app.post('/v1/reference/assess')
    def reference_assess(window: ReferenceAssessment, claims=Depends(authorize)):
        authorize_reference(claims)
        try:
            return reference.assess(settings.tenant, claims['oid'], window.model_dump())
        except (AlertConflict, ReferenceOrderError) as exc:
            raise HTTPException(409, str(exc)) from exc
        except sqlite3.Error as exc:
            raise HTTPException(503, 'Reference decision could not be persisted') from exc

    @app.get('/v1/reference/alerts')
    def reference_alerts(claims=Depends(authorize)):
        authorize_reference(claims)
        try:
            return {'scope': 'simulated_maintenance_inbox', 'qualified_detector': False,
                    'events': reference.inbox(settings.tenant, claims['oid'], REFERENCE_ASSET)}
        except sqlite3.Error as exc:
            raise HTTPException(503, 'Reference inbox unavailable') from exc

    @app.post('/v1/reference/alerts/{event_id}/acknowledge')
    def reference_acknowledge(event_id: str, claims=Depends(authorize)):
        authorize_reference(claims)
        if not re.fullmatch(r'[a-f0-9]{64}', event_id):
            raise HTTPException(422, 'Invalid event ID')
        try:
            return reference.acknowledge_reference(settings.tenant, claims['oid'], REFERENCE_ASSET, event_id)
        except KeyError as exc:
            raise HTTPException(404, 'Reference event not found') from exc
        except AlertConflict as exc:
            raise HTTPException(409, str(exc)) from exc
        except sqlite3.Error as exc:
            raise HTTPException(503, 'Acknowledgement could not be persisted') from exc

    @app.post('/v1/degradation/assess')
    def assess(window: Assessment, claims=Depends(authorize)):
        if settings.asset_grants is not None and window.asset_id not in settings.asset_grants.get(claims.get('azp'), ()):
            raise HTTPException(403, 'Client not authorized for this asset')
        with duration.time():
            payload = window.model_dump(mode='json')
            request_sha = hashlib.sha256(encode(payload)).hexdigest()
            result = {
                'assessment_id': hashlib.sha256(encode({'tenant': settings.tenant, 'caller': claims['oid'],
                                                       'request': request_sha})).hexdigest(),
                'asset_id': window.asset_id, 'window_id': window.window_id,
                'request_sha256': request_sha,
                'source_sha256': window.source_sha256, 'source_integrity': 'caller_asserted_not_verified',
                'features': features(window.samples, window.unit),
                'alert_status': 'unavailable', 'reason': 'No qualified degradation policy or model',
                'model_version': None, 'threshold_version': None, 'policy_version': 'abstain-unqualified-1',
                'site_validated': False, 'persisted': False, 'notification_sent': False,
            }
            if store is not None:
                try:
                    result = store.save(settings.tenant, claims['oid'], result,
                                        payload['observed_at'])
                except WindowConflict as exc:
                    raise HTTPException(409, 'Window already accepted with different content') from exc
                except sqlite3.Error as exc:
                    raise HTTPException(503, 'Assessment could not be persisted') from exc
            count.labels(result['alert_status']).inc()
            return result
    return app

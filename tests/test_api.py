import json
import time
from datetime import datetime, timezone

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from pulse.api import Settings, EntraVerifier, create_app

TENANT = '00000000-0000-0000-0000-000000000001'
CLIENT = '00000000-0000-0000-0000-000000000002'
AUDIENCE = '00000000-0000-0000-0000-000000000003'


@pytest.fixture
def api():
    settings = Settings(TENANT, AUDIENCE, (CLIENT,))
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    verifier = EntraVerifier(settings)
    verifier.keys = {'fixture': private.public_key()}
    verifier.loaded_at = verifier.last_attempt = time.monotonic()
    client = TestClient(create_app(settings, verifier))

    def token(**overrides):
        now = int(time.time())
        claims = {'iss': settings.issuer, 'aud': AUDIENCE, 'tid': TENANT, 'ver': '2.0',
                  'oid': 'generated-test-caller', 'azp': CLIENT, 'roles': ['Pulse.Assess'],
                  'iat': now, 'nbf': now, 'exp': now+300}
        claims.update(overrides)
        return jwt.encode(claims, private, algorithm='RS256', headers={'kid': 'fixture'})
    return client, token


def payload():
    return {'schema_version': '1', 'asset_id': 'fixture-bearing', 'window_id': 'w1',
            'observed_at': datetime.now(timezone.utc).isoformat(), 'source_sha256': 'a'*64,
            'unit': 'g', 'sample_rate_hz': 12800.0, 'samples': [-1.0, 1.0]*64}


def test_valid_token_features_abstention_and_stable_identity(api):
    client, token = api
    headers = {'Authorization': 'Bearer '+token()}
    data = payload()
    a = client.post('/v1/degradation/assess', json=data, headers=headers)
    b = client.post('/v1/degradation/assess', json=data, headers=headers)
    assert a.status_code == 200
    result = a.json()
    assert result['features']['rms_m_s2'] == pytest.approx(9.80665)
    assert result['alert_status'] == 'unavailable'
    assert not result['persisted'] and not result['notification_sent'] and not result['site_validated']
    assert result['assessment_id'] == b.json()['assessment_id']


@pytest.mark.parametrize('override,expected', [({'aud': 'wrong'}, 401), ({'tid': 'wrong'}, 401),
    ({'exp': 1}, 401), ({'iss': 'https://attacker.invalid'}, 401), ({'roles': []}, 403),
    ({'azp': 'other-client'}, 403), ({'nbf': 9999999999}, 401), ({'ver': '1.0'}, 401)])
def test_token_denials(api, override, expected):
    client, token = api
    assert client.post('/v1/degradation/assess', json=payload(),
                       headers={'Authorization': 'Bearer '+token(**override)}).status_code == expected


def test_anonymous_denied(api):
    client, _ = api
    assert client.post('/v1/degradation/assess', json=payload()).status_code == 401


def test_forged_signature_and_wrong_algorithm_denied(api):
    client, token = api
    valid = token()
    claims = jwt.decode(valid, options={'verify_signature': False})
    forged = jwt.encode(claims, rsa.generate_private_key(public_exponent=65537, key_size=2048),
                        algorithm='RS256', headers={'kid': 'fixture'})
    wrong_algorithm = jwt.encode(claims, b'x'*32, algorithm='HS256', headers={'kid': 'fixture'})
    for candidate in (forged, wrong_algorithm):
        assert client.post('/v1/degradation/assess', json=payload(),
                           headers={'Authorization': 'Bearer '+candidate}).status_code == 401


@pytest.mark.parametrize('change', [{'samples': [True, False]}, {'samples': [1.]},
    {'samples': [1.]*4097}, {'unit': 'V'}, {'observed_at': '2026-01-01T00:00:00'},
    {'samples': [1001., 1.]}, {'sample_rate_hz': 0.}, {'unexpected': 'data'}])
def test_contract_denials(api, change):
    client, token = api
    data = payload(); data.update(change)
    assert client.post('/v1/degradation/assess', json=data,
                       headers={'Authorization': 'Bearer '+token()}).status_code == 422


def test_nonfinite_not_reflected_or_crashed(api):
    client, token = api
    data = payload(); data['samples'] = [float('nan'), 1.]
    response = client.post('/v1/degradation/assess', content=json.dumps(data),
                           headers={'Authorization': 'Bearer '+token(), 'Content-Type': 'application/json'})
    assert response.status_code == 422
    assert 'NaN' not in response.text


def test_oversized_body_before_parsing(api):
    client, token = api
    response = client.post('/v1/degradation/assess', content=b'x'*131073,
                           headers={'Authorization': 'Bearer '+token()})
    assert response.status_code == 413


def test_health_metrics_and_no_public_docs(api):
    client, _ = api
    assert client.get('/health/live').status_code == 200
    assert client.get('/health/ready').json()['qualified_alerts_available'] is False
    assert client.get('/metrics').status_code == 200
    assert client.get('/docs').status_code == 404


def test_startup_requires_identity_configuration(monkeypatch):
    monkeypatch.delenv('PULSE_TENANT_ID', raising=False)
    with pytest.raises(KeyError):
        create_app()


def test_durable_api_retries_conflicts_and_restart(tmp_path):
    from pulse.assessment_store import AssessmentStore
    settings = Settings(TENANT, AUDIENCE, (CLIENT,))
    path = str(tmp_path/'api.db')
    def build():
        return TestClient(create_app(settings, lambda token: {'oid': 'fixture'},
                                    AssessmentStore(path)))
    data = payload()
    headers = {'Authorization': 'Bearer fixture'}
    with build() as client:
        first = client.post('/v1/degradation/assess', json=data, headers=headers)
        assert first.status_code == 200 and first.json()['persisted']
    with build() as restarted:
        assert restarted.post('/v1/degradation/assess', json=data, headers=headers).json() == first.json()
        data['samples'] = [0., 0.]
        assert restarted.post('/v1/degradation/assess', json=data, headers=headers).status_code == 409


def test_storage_failure_never_returns_success():
    import sqlite3
    class UnavailableStore:
        def save(self, *args):
            raise sqlite3.OperationalError('disk full')
        def healthy(self):
            raise sqlite3.OperationalError('disk unavailable')
    client = TestClient(create_app(Settings(TENANT, AUDIENCE, (CLIENT,)),
                                  lambda token: {'oid': 'fixture'}, UnavailableStore()))
    assert client.get('/health/ready').status_code == 503
    response = client.post('/v1/degradation/assess', json=payload(),
                           headers={'Authorization': 'Bearer fixture'})
    assert response.status_code == 503
    assert 'disk full' not in response.text

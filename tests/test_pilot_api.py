import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from pulse.api import create_app, Settings
from pulse.reference_detector import ReferenceDetector, ASSET
from test_reference_detector import payload
from test_intake import fixture


def setup(tmp_path):
    detector=ReferenceDetector(tmp_path/'reference.db')
    for i in range(3): result=detector.assess('tenant','caller',payload(i))
    settings=Settings('tenant','audience',('client',),asset_grants={'client':(ASSET,)})
    claims={'oid':'caller','azp':'client','roles':['Pulse.Assess','Pulse.Review']}
    schema=json.loads((Path(__file__).resolve().parents[1]/'data/contracts/vibration-window.schema.json').read_text())
    def client():return TestClient(create_app(settings,lambda _:dict(claims),reference=detector,review_db=tmp_path/'reviews.db',intake_schema=schema))
    return client,claims,result['event_id']

HEADERS={'Authorization':'Bearer synthetic'}

def test_review_identity_history_restart_and_conflict(tmp_path):
    factory,claims,event=setup(tmp_path);client=factory();url=f'/v1/reference/alerts/{event}/reviews'
    request={'outcome':'unresolved','rationale':'Synthetic review','evidence':[]}
    assert client.post(url,json=request).status_code==401
    assert client.post(url,headers=HEADERS,json=dict(request,reviewer='spoof')).status_code==422
    first=client.post(url,headers=HEADERS,json=request)
    assert first.status_code==200
    correction=dict(request,outcome='nuisance',evidence=['fixture:inspection'],supersedes=first.json()['review_id'])
    assert client.post(url,headers=HEADERS,json=correction).status_code==200
    assert client.post(url,headers=HEADERS,json=correction).status_code==409
    rows=factory().get(url,headers=HEADERS).json()['reviews']
    assert len(rows)==2 and json.loads(rows[0]['reviewer'])==['tenant','caller','client']
    assert not rows[1]['evidence_verified']

def test_review_role_and_caller_scope_enforced(tmp_path):
    factory,claims,event=setup(tmp_path);url=f'/v1/reference/alerts/{event}/reviews'
    claims['roles']=['Pulse.Assess']
    assert factory().get(url,headers=HEADERS).status_code==403
    claims['roles'].append('Pulse.Review');claims['oid']='other'
    assert factory().get(url,headers=HEADERS).status_code==404
    claims['oid']='caller';claims['azp']='ungranted'
    assert factory().get(url,headers=HEADERS).status_code==403

def test_intake_authorization_validation_and_no_permission_claim(tmp_path):
    factory,claims,event=setup(tmp_path);client=factory();document=fixture()
    assert client.post('/v1/intake/validate',json=document).status_code==401
    assert client.post('/v1/intake/validate',headers=HEADERS,json=document).status_code==403
    document['metadata']['asset_id']=ASSET
    r=client.post('/v1/intake/validate',headers=HEADERS,json=document)
    assert r.status_code==200 and r.json()['status']=='STRUCTURALLY_VALID_PENDING_REVIEW'
    assert not r.json()['permission_verified']
    document['window']['unit']='volts'
    assert client.post('/v1/intake/validate',headers=HEADERS,json=document).json()['status']=='REJECTED'

def test_runtime_opt_in_requires_complete_configuration(tmp_path,monkeypatch):
    settings=Settings('tenant','audience',('client',),asset_grants={'client':(ASSET,)})
    monkeypatch.setenv('PULSE_PILOT_COMPONENTS','1')
    monkeypatch.delenv('PULSE_REVIEW_DB',raising=False)
    with pytest.raises(KeyError):create_app(settings,lambda _: {})
    monkeypatch.setenv('PULSE_REVIEW_DB',str(tmp_path/'reviews.db'))
    monkeypatch.setenv('PULSE_INTAKE_SCHEMA',str(Path(__file__).resolve().parents[1]/'data/contracts/vibration-window.schema.json'))
    app=create_app(settings,lambda _: {'oid':'caller','azp':'client'})
    d=fixture();d['metadata']['asset_id']=ASSET
    assert TestClient(app).post('/v1/intake/validate',headers=HEADERS,json=d).json()['status']=='STRUCTURALLY_VALID_PENDING_REVIEW'

def test_closure_role_ownership_acknowledgement_and_retry(tmp_path):
    factory,claims,event=setup(tmp_path);client=factory();url=f'/v1/reference/alerts/{event}/close'
    body={'rationale':'Synthetic disposition','evidence':['fixture:inspection']}
    assert client.post(url,json=body).status_code==401
    assert client.post(url,headers=HEADERS,json=body).status_code==403
    claims['roles'].append('Pulse.Close')
    assert client.post(url,headers=HEADERS,json=dict(body,actor='spoof')).status_code==422
    assert client.post(url,headers=HEADERS,json=body).status_code==409
    assert client.post(f'/v1/reference/alerts/{event}/acknowledge',headers=HEADERS,json={}).status_code==200
    first=client.post(url,headers=HEADERS,json=body)
    assert first.status_code==200 and first.json()['state']=='CLOSED'
    assert not first.json()['human_identity_verified']
    assert factory().post(url,headers=HEADERS,json=body).json()==first.json()
    assert client.post(url,headers=HEADERS,json=dict(body,rationale='changed')).status_code==409
    claims['oid']='other'
    assert client.post(url,headers=HEADERS,json=body).status_code==404

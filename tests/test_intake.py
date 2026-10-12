import json
from pathlib import Path
import pytest
from pulse.intake import validate_intake, REFERENCES

SCHEMA=json.loads((Path(__file__).resolve().parents[1]/'data/contracts/vibration-window.schema.json').read_text())
def fixture():
    return {'metadata':{k:'synthetic-reference' for k in REFERENCES},'window':{
        'schema_version':'0.1','dataset_id':'synthetic','bearing_id':'b','run_id':'r','window_id':'w',
        'source_sha256':'0'*64,'sample_rate_hz':100,'unit':'g','samples':[0,1,-1],
        'time_basis':'utc','timestamp_utc':'2026-10-11T12:00:00Z','split':'test'}}

def test_structural_validity_never_grants_authority():
    r=validate_intake(fixture(),SCHEMA)
    assert r['status']=='STRUCTURALLY_VALID_PENDING_REVIEW'
    assert not r['permission_verified'] and not r['source_hash_verified']

@pytest.mark.parametrize('field,value', [('samples',[float('nan'),0]),('sample_rate_hz',float('inf')),('timestamp_utc','2026-10-11T12:00:00'),('unit','volts'),('bearing_id',' ')])
def test_invalid_window_rejected(field,value):
    d=fixture();d['window'][field]=value
    assert validate_intake(d,SCHEMA)['status']=='REJECTED'

def test_missing_reference_and_unknown_metadata_rejected():
    d=fixture();del d['metadata']['data_use_ref'];d['metadata']['secret']='not-printed'
    r=validate_intake(d,SCHEMA)
    assert r['status']=='REJECTED' and 'not-printed' not in str(r)

def test_non_object_rejected():
    assert validate_intake([],SCHEMA)['status']=='REJECTED'

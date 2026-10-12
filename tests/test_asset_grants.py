from datetime import datetime, timezone
import json
import pytest
from fastapi.testclient import TestClient
from pulse.api import Settings, create_app

TENANT = '00000000-0000-0000-0000-000000000001'
CLIENT = '00000000-0000-0000-0000-000000000002'
AUDIENCE = '00000000-0000-0000-0000-000000000003'


def test_cross_asset_denied_before_storage():
    settings = Settings(TENANT, AUDIENCE, (CLIENT,), asset_grants={CLIENT: ('permitted',)})
    client = TestClient(create_app(settings, verifier=lambda _: {'azp': CLIENT, 'oid': 'caller'}))
    body = {'schema_version': '1', 'asset_id': 'other', 'window_id': 'w1',
            'observed_at': datetime.now(timezone.utc).isoformat(), 'source_sha256': 'a'*64,
            'unit': 'g', 'sample_rate_hz': 20000., 'samples': [-1., 1.]}
    assert client.post('/v1/degradation/assess', json=body,
                       headers={'Authorization': 'Bearer fixture'}).status_code == 403
    body['asset_id'] = 'permitted'
    assert client.post('/v1/degradation/assess', json=body,
                       headers={'Authorization': 'Bearer fixture'}).status_code == 200


@pytest.mark.parametrize('grants', [{}, {CLIENT: ['*']}, {CLIENT: []}, {CLIENT: 'all'}, []])
def test_invalid_environment_grants_fail_startup(monkeypatch, grants):
    monkeypatch.setenv('PULSE_TENANT_ID', TENANT)
    monkeypatch.setenv('PULSE_API_CLIENT_ID', AUDIENCE)
    monkeypatch.setenv('PULSE_ALLOWED_CLIENT_IDS', CLIENT)
    monkeypatch.setenv('PULSE_ASSET_GRANTS', json.dumps(grants))
    with pytest.raises(ValueError): Settings.from_env()

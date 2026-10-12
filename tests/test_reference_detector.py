from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from pulse.api import Settings, create_app
from pulse.reference_detector import ReferenceDetector, ReferenceOrderError, BASELINE_RMS, ASSET
from pulse.alert_ledger import AlertConflict


def payload(index, ratio=4.):
    return {'asset_id': ASSET, 'window_id': f'w{index}',
            'source_timestamp': (datetime(2004, 2, 12)+timedelta(minutes=10*index)).strftime('%Y.%m.%d.%H.%M.%S'),
            'source_sha256': 'a'*64, 'dataset_id': 'DS-IMS', 'source_run': '2nd_test',
            'amplitude_unit': 'native_unknown', 'sample_count': 20480, 'sample_rate_hz': 20000,
            'rms_native': BASELINE_RMS*ratio}


def test_atomic_decisions_episode_dedupe_and_restart(tmp_path):
    path = tmp_path/'reference.db'
    detector = ReferenceDetector(path)
    for i in range(2):
        assert detector.assess('t', 'c', payload(i))['event_id'] is None
    detector = ReferenceDetector(path)
    first = detector.assess('t', 'c', payload(2))
    assert first['reference_status'] == 'reference_anomaly'
    assert not first['qualified_detector'] and not first['external_notification_sent']
    assert detector.assess('t', 'c', payload(2)) == first
    assert detector.assess('t', 'c', payload(3))['event_id'] == first['event_id']
    assert len(detector.inbox('t', 'c', ASSET)) == 1
    assert detector.inbox('t', 'other', ASSET) == []
    with pytest.raises(AlertConflict): detector.assess('t', 'c', payload(2, 5))
    with pytest.raises(ReferenceOrderError): detector.assess('t', 'c', dict(payload(1), window_id='late'))
    detector.assess('t', 'c', payload(4, 1))
    for i in [5, 6, 7]: result = detector.assess('t', 'c', payload(i))
    assert result['event_id'] != first['event_id']
    ack = detector.acknowledge_reference('t', 'c', ASSET, first['event_id'])
    assert detector.acknowledge_reference('t', 'c', ASSET, first['event_id']) == ack
    with pytest.raises(KeyError): detector.acknowledge_reference('t', 'other', ASSET, first['event_id'])


def test_gap_resets_and_exact_threshold_not_flagged(tmp_path):
    detector = ReferenceDetector(tmp_path/'reference.db')
    detector.assess('t', 'c', payload(0))
    detector.assess('t', 'c', payload(1))
    assert detector.assess('t', 'c', payload(10))['consecutive_exceedances'] == 1
    assert detector.assess('t', 'c', payload(11, 3))['consecutive_exceedances'] == 0


def test_api_gates_native_schema_and_inbox(tmp_path):
    settings = Settings('tenant', 'audience', ('client',), asset_grants={'client': (ASSET,)})
    detector = ReferenceDetector(tmp_path/'reference.db')
    verify = lambda _: {'oid': 'caller', 'azp': 'client'}
    client = TestClient(create_app(settings, verify, reference=detector))
    headers = {'Authorization': 'Bearer fixture'}
    assert client.get('/v1/reference/alerts').status_code == 401
    assert client.post('/v1/reference/assess', headers=headers, json=dict(payload(0), amplitude_unit='g')).status_code == 422
    for i in range(3):
        response = client.post('/v1/reference/assess', headers=headers, json=payload(i))
        assert response.status_code == 200
    event = response.json()['event_id']
    assert len(client.get('/v1/reference/alerts', headers=headers).json()['events']) == 1
    assert client.post(f'/v1/reference/alerts/{event}/acknowledge', headers=headers).status_code == 200
    assert client.post('/v1/reference/assess', headers=headers, json=dict(payload(0), window_id='late')).status_code == 409
    denied = TestClient(create_app(Settings('tenant', 'audience', ('client',), asset_grants={'client': ()}), verify, reference=detector))
    assert denied.get('/v1/reference/alerts', headers=headers).status_code == 403
    disabled = TestClient(create_app(settings, verify))
    assert disabled.get('/v1/reference/alerts', headers=headers).status_code == 503

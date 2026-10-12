from concurrent.futures import ThreadPoolExecutor

import pytest

from pulse.assessment_store import AssessmentStore, WindowConflict


def result(sha='a'*64):
    return dict(asset_id='bearing-1', window_id='window-1', request_sha256=sha,
                alert_status='unavailable', persisted=False, notification_sent=False)


def test_receipt_survives_restart_and_retries(tmp_path):
    path = str(tmp_path/'receipts.db')
    first = AssessmentStore(path).save('tenant', 'caller', result())
    restarted = AssessmentStore(path)
    assert first['persisted'] and not first['notification_sent']
    assert restarted.save('tenant', 'caller', result()) == first
    with pytest.raises(WindowConflict):
        restarted.save('tenant', 'caller', result('b'*64))
    assert restarted.save('other-tenant', 'caller', result('b'*64))['persisted']
    assert restarted.save('tenant', 'other-caller', result('b'*64))['persisted']


def test_concurrent_duplicate_writes_create_one_receipt(tmp_path):
    store = AssessmentStore(str(tmp_path/'receipts.db'))
    with ThreadPoolExecutor(max_workers=8) as pool:
        receipts = list(pool.map(lambda _: store.save('tenant', 'caller', result()), range(32)))
    assert all(r == receipts[0] for r in receipts)
    with store.connect() as db:
        assert db.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0] == 1


def test_memory_database_cannot_claim_durable_receipts():
    with pytest.raises(ValueError):
        AssessmentStore(':memory:')


def test_commit_evidence_is_scoped_and_retry_stable(tmp_path):
    from datetime import datetime, timezone
    store = AssessmentStore(str(tmp_path/'receipts.db'))
    before = datetime.now(timezone.utc)
    first = store.save('tenant', 'caller', result(), '2026-01-01T00:00:00Z')
    with store.connect() as db:
        evidence = db.execute('SELECT * FROM assessment_commit_evidence').fetchall()
    assert len(evidence) == 1
    assert datetime.fromisoformat(evidence[0][-1]) >= before
    assert evidence[0][:4] == ('tenant','caller','bearing-1','window-1')
    assert store.save('tenant','caller',result(),'2026-02-01T00:00:00Z') == first
    with store.connect() as db:
        assert db.execute('SELECT * FROM assessment_commit_evidence').fetchall() == evidence


def test_old_receipts_do_not_gain_invented_commit_times(tmp_path):
    path = str(tmp_path/'receipts.db')
    store = AssessmentStore(path)
    store.save('tenant','caller',result())
    store = AssessmentStore(path)
    store.save('tenant','caller',result(),'2026-01-01T00:00:00Z')
    with store.connect() as db:
        assert db.execute('SELECT COUNT(*) FROM assessment_commit_evidence').fetchone()[0] == 0

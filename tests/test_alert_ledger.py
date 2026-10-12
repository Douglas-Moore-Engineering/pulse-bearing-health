from concurrent.futures import ThreadPoolExecutor
import pytest
from pulse.alert_ledger import AlertLedger, AlertConflict


def test_concurrent_episode_deduplication_restart_and_conflict(tmp_path):
    path = tmp_path/'events.db'
    ledger = AlertLedger(path)
    with ThreadPoolExecutor(max_workers=8) as pool:
        ids = list(pool.map(lambda _: ledger.record('t', 'a', 'episode-1', 'policy-1', {'fixture': True}), range(32)))
    assert len(set(ids)) == 1
    assert AlertLedger(path).record('t', 'a', 'episode-1', 'policy-1', {'fixture': True}) == ids[0]
    with pytest.raises(AlertConflict): ledger.record('t', 'a', 'episode-1', 'policy-1', {'fixture': False})
    with ledger.connection() as db:
        assert db.execute('SELECT COUNT(*) FROM alerts').fetchone()[0] == 1


def test_ack_is_scoped_immutable_and_does_not_claim_delivery(tmp_path):
    ledger = AlertLedger(tmp_path/'events.db')
    event = ledger.record('t', 'a', 'e', 'p', {'fixture': True})
    for tenant, asset in [('other', 'a'), ('t', 'other')]:
        with pytest.raises(KeyError): ledger.acknowledge(tenant, asset, event, 'actor')
    first = ledger.acknowledge('t', 'a', event, 'actor')
    assert ledger.acknowledge('t', 'a', event, 'actor') == first
    with pytest.raises(AlertConflict): ledger.acknowledge('t', 'a', event, 'other')
    with ledger.connection() as db:
        assert db.execute('SELECT COUNT(*) FROM alert_delivery_attempts').fetchone()[0] == 0


def test_transport_results_preserve_failure_and_unknown(tmp_path):
    ledger = AlertLedger(tmp_path/'events.db')
    event = ledger.record('t', 'a', 'e', 'p', {'fixture': True})
    for outcome in ['failed', 'unknown', 'delivered']:
        ledger.record_delivery_attempt('t', 'a', event, outcome, 'mock-only', outcome)
        ledger.record_delivery_attempt('t', 'a', event, outcome, 'mock-only', outcome)
    with pytest.raises(AlertConflict): ledger.record_delivery_attempt('t', 'a', event, 'failed', 'mock-only', 'delivered')
    with pytest.raises(KeyError): ledger.record_delivery_attempt('other', 'a', event, 'x', 'mock-only', 'delivered')
    with ledger.connection() as db:
        assert db.execute('SELECT COUNT(*) FROM alert_delivery_attempts').fetchone()[0] == 3

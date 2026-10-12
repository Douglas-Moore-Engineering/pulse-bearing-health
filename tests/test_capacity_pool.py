"""Exercise experimental pooling against real SQLite transaction semantics."""
import runpy
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pytest
from pulse.assessment_store import WindowConflict

Store = runpy.run_path(str(Path(__file__).parents[1]/'scripts/exercise_local_capacity.py'))['ReusedConnectionStore']


def test_pool_preserves_durability_retry_rollback_and_restart(tmp_path):
    path = str(tmp_path/'receipts.db')
    store = Store(path)
    result = dict(asset_id='a', window_id='w', request_sha256='a'*64)
    with ThreadPoolExecutor(max_workers=8) as executor:
        rows = list(executor.map(lambda _: store.save('t','c',result,'2026-01-01T00:00:00Z'),range(32)))
    assert all(row == rows[0] for row in rows)
    with pytest.raises(WindowConflict):
        store.save('t','c',dict(result,request_sha256='b'*64))
    with pytest.raises(RuntimeError, match='injected'):
        with store.connect() as db:
            db.execute('DELETE FROM api_assessments')
            raise RuntimeError('injected')
    with store.connect() as db:
        assert db.execute('PRAGMA synchronous').fetchone()[0] == 2
        assert db.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0] == 1
        assert db.execute('SELECT COUNT(*) FROM assessment_commit_evidence').fetchone()[0] == 1
        evidence = db.execute('SELECT * FROM assessment_commit_evidence').fetchall()
    store.close()
    with pytest.raises(RuntimeError, match='closed'):
        store.healthy()
    restarted = Store(path)
    assert restarted.save('t','c',result,'2026-02-01T00:00:00Z') == rows[0]
    with restarted.connect() as db:
        assert db.execute('SELECT * FROM assessment_commit_evidence').fetchall() == evidence
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    restarted.close()

@pytest.mark.parametrize('failure', ['setup', 'commit'])
def test_failed_connection_is_discarded_and_slot_recovers(tmp_path, failure):
    import sqlite3
    class FaultConnection(sqlite3.Connection):
        armed = False
        closed_count = 0
        def execute(self, sql, *args):
            if self.armed and failure == 'setup' and sql == 'PRAGMA synchronous=FULL':
                raise sqlite3.OperationalError('injected setup')
            return super().execute(sql, *args)
        def __exit__(self, *args):
            if self.armed and failure == 'commit':
                self.rollback()
                raise sqlite3.OperationalError('injected commit')
            return super().__exit__(*args)
        def close(self):
            type(self).closed_count += 1
            return super().close()
    store = Store(str(tmp_path/'failure.db'), factory=FaultConnection)
    # Force the next lease to initialize a fresh connection.
    db = store.pool.get_nowait()
    db.close()
    store.pool.put(None)
    before = FaultConnection.closed_count
    FaultConnection.armed = True
    with pytest.raises(sqlite3.OperationalError, match='injected'):
        store.save('t','c',dict(asset_id='a',window_id='w',request_sha256='a'*64))
    assert FaultConnection.closed_count == before + 1
    assert store.pool.qsize() == 8
    FaultConnection.armed = False
    with store.connect() as db:
        assert db.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0] == 0
        assert db.execute('PRAGMA synchronous').fetchone()[0] == 2
    assert store.save('t','c',dict(asset_id='a',window_id='w',request_sha256='a'*64))['persisted']
    store.close()


def test_evidence_write_failure_keeps_receipt_without_inventing_timing(tmp_path):
    import sqlite3
    class FaultConnection(sqlite3.Connection):
        def execute(self, sql, *args):
            if sql.startswith('INSERT INTO assessment_commit_evidence'):
                raise sqlite3.OperationalError('injected evidence failure')
            return super().execute(sql, *args)
    store = Store(str(tmp_path/'evidence.db'), factory=FaultConnection)
    result = dict(asset_id='a', window_id='w', request_sha256='a'*64)
    with pytest.raises(sqlite3.OperationalError, match='injected evidence'):
        store.save('t','c',result,'2026-01-01T00:00:00Z')
    assert store.save('t','c',result,'2026-02-01T00:00:00Z')['persisted']
    with store.connect() as db:
        assert db.execute('SELECT COUNT(*) FROM api_assessments').fetchone()[0] == 1
        assert db.execute('SELECT COUNT(*) FROM assessment_commit_evidence').fetchone()[0] == 0
    store.close()

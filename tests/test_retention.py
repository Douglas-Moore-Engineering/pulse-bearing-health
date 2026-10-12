import sqlite3
import pytest
from pulse.retention import plan, inventory_sqlite

def record():
    return dict(id='synthetic-1',created_at='2025-01-01T00:00:00Z',hold=False,
                review_resolved=True,dependencies_clear=True,export_verified=True)

def test_old_complete_record_is_only_review_eligible():
    result=plan([record()],'2026-01-01T00:00:00Z',30)
    assert result['records'][0]['disposition']=='ELIGIBLE_FOR_OWNER_REVIEW'
    assert not result['deletion_authorized']

@pytest.mark.parametrize('field',['hold','review_resolved','dependencies_clear','export_verified','created_at'])
def test_unknown_protection_metadata_retains(field):
    r=record();del r[field]
    assert plan([r],'2026-01-01T00:00:00Z',30)['records'][0]['disposition']=='RETAIN'

def test_cutoff_and_future_timestamps_retained():
    for created in ['2025-12-02T00:00:00Z','2027-01-01T00:00:00Z','2025-01-01']:
        r=record();r['created_at']=created
        assert plan([r],'2026-01-01T00:00:00Z',30)['records'][0]['disposition']=='RETAIN'

def test_duplicate_identity_rejected():
    with pytest.raises(ValueError):plan([record(),record()],'2026-01-01T00:00:00Z',30)

def test_read_only_inventory_preserves_database(tmp_path):
    path=tmp_path/'synthetic.db'
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE receipts (payload TEXT)')
        db.execute("INSERT INTO receipts VALUES ('private synthetic payload')")
    before=path.read_bytes();result=inventory_sqlite(path)
    assert result['tables'][0]['rows']==1
    assert 'private synthetic payload' not in str(result)
    assert before==path.read_bytes()

def test_missing_database_is_not_created(tmp_path):
    path=tmp_path/'missing.db'
    with pytest.raises(FileNotFoundError):inventory_sqlite(path)
    assert not path.exists()

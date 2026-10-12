import pytest
from pulse.reconciliation import reconcile


def test_fleet_missing_late_and_future_receipts():
    assets=[f'a{i}' for i in range(12)]
    def row(a,p):return {'asset_id':a,'observed_at':'2026-10-10T16:00:00Z','persisted_at':p}
    r=reconcile('2026-10-10','America/New_York',assets,
        [row('a0','2026-10-11T10:00:00Z'),row('a1','2026-10-11T10:01:00Z'),row('a2','2026-10-12T00:00:00Z')],
        '2026-10-11T12:00:00Z')
    assert len(r['assets'])==12
    assert [a['status'] for a in r['assets'][:3]]==['PRESENT_BY_DEADLINE','LATE','MISSING']
    assert not r['scheduled_execution_verified']


def test_dst_and_pending_boundary():
    r=reconcile('2026-11-01','America/New_York',['a'],[], '2026-11-02T10:59:59Z')
    assert r['deadline_utc']=='2026-11-02T11:00:00+00:00'
    assert r['assets'][0]['status']=='PENDING'


@pytest.mark.parametrize('change', [{'assets':['a','a']},{'as_of':'2026-10-11T12:00:00'},
    {'records':[{'asset_id':'other','observed_at':'2026-10-10T00:00:00Z','persisted_at':'2026-10-11T00:00:00Z'}]}])
def test_invalid_inputs_rejected(change):
    args=dict(day='2026-10-10',plant_timezone='UTC',assets=['a'],records=[],as_of='2026-10-11T12:00:00Z')
    args.update(change)
    with pytest.raises(ValueError):reconcile(**args)

def test_database_scope_and_unknown_legacy_timing(tmp_path):
    from pulse.assessment_store import AssessmentStore
    from pulse.reconciliation import reconcile_database
    store=AssessmentStore(str(tmp_path/'receipts.db'))
    def save(tenant,asset,window):
        store.save(tenant,'caller',dict(asset_id=asset,window_id=window,request_sha256='a'*64))
    save('tenant','a','legacy');save('other','b','foreign')
    r=reconcile_database(store.path,'tenant','caller','2026-10-10','UTC',['a','b'],'2026-10-11T07:00:00Z')
    assert [a['status'] for a in r['assets']]==['TIMING_UNKNOWN','MISSING']


def test_database_upper_bound_does_not_prove_late_commit(tmp_path):
    from pulse.assessment_store import AssessmentStore
    from pulse.reconciliation import reconcile_database
    store=AssessmentStore(str(tmp_path/'receipts.db'))
    store.save('tenant','caller',dict(asset_id='a',window_id='w',request_sha256='a'*64))
    with store.connect() as db:
        db.execute('INSERT INTO assessment_commit_evidence VALUES (?,?,?,?,?,?)',
            ('tenant','caller','a','w','2026-10-10T12:00:00Z','2026-10-11T06:01:00Z'))
    r=reconcile_database(store.path,'tenant','caller','2026-10-10','UTC',['a'],'2026-10-11T07:00:00Z')
    assert r['assets'][0]['status']=='TIMING_UNCERTAIN'

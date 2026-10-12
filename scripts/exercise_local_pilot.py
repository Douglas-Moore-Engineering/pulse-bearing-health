"""Synthetic local component integration and isolated SQLite recovery exercise."""
import hashlib
import json
import sqlite3
import sys
import tempfile
import time
from contextlib import closing
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pulse.intake import validate_intake, REFERENCES
from pulse.adjudication import AdjudicationLedger
from pulse.retention import inventory_sqlite, plan

def main():
    schema=json.loads((ROOT/'data/contracts/vibration-window.schema.json').read_text())
    started=time.perf_counter();latencies=[]
    with tempfile.TemporaryDirectory(prefix='pulse-synthetic-recovery-') as directory:
        root=Path(directory);source=root/'source.db';backup=root/'backup.db';restored=root/'restored.db'
        ledger=AdjudicationLedger(source)
        expected={}
        for i in range(1000):
            tick=time.perf_counter();subject=f'synthetic-{i}'
            document={'metadata':{k:'synthetic-reference' for k in REFERENCES},'window':{
                'schema_version':'0.1','dataset_id':'synthetic','bearing_id':'fixture-bearing','run_id':'fixture-run',
                'window_id':subject,'source_sha256':'0'*64,'sample_rate_hz':100,'unit':'g','samples':[0,1,-1],
                'time_basis':'utc','timestamp_utc':'2026-10-11T12:00:00Z','split':'test'}}
            result=validate_intake(document,schema)
            assert result['status']=='STRUCTURALLY_VALID_PENDING_REVIEW'
            identifier=ledger.append(subject,'synthetic-reviewer','unresolved','Synthetic integration fixture',[])
            if i%10==0:
                ledger.append(subject,'synthetic-reviewer','nuisance','Synthetic correction',['fixture:evidence'],identifier)
            expected[subject]=ledger.history(subject)
            latencies.append((time.perf_counter()-tick)*1000)
        workload_seconds=time.perf_counter()-started
        with closing(sqlite3.connect(backup)) as destination: ledger.db.backup(destination)
        ledger.close()
        recovery_start=time.perf_counter()
        with closing(sqlite3.connect(backup.as_uri()+'?mode=ro',uri=True)) as src,closing(sqlite3.connect(restored)) as dst:
            src.backup(dst)
            assert dst.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        recovered=AdjudicationLedger(restored)
        assert all(recovered.history(k)==v for k,v in expected.items())
        recovered.close();recovery_seconds=time.perf_counter()-recovery_start
        inventory=inventory_sqlite(restored)
        assert next(r['rows'] for r in inventory['tables'] if r['table']=='reviews')==1100
        dryrun=plan([{'id':k,'created_at':v[0]['recorded_at'],'hold':False,
            'review_resolved':v[-1]['outcome']!='unresolved','dependencies_clear':True,'export_verified':True}
            for k,v in expected.items()], '2030-01-01T00:00:00Z',30)
        assert sum(r['disposition']=='ELIGIBLE_FOR_OWNER_REVIEW' for r in dryrun['records'])==100
        assert sum(r['disposition']=='RETAIN' for r in dryrun['records'])==900
        report={'scope':'Synthetic local component exercise; not API, Azure, site, host-loss or capacity qualification',
            'intake_windows':1000,'review_rows':1100,'corrections':100,'restored_histories_identical':True,
            'integrity':'ok','retained_unresolved_subjects':900,'review_eligible_subjects':100,'records_deleted':0,
            'workload_seconds':workload_seconds,'sequential_windows_per_second':1000/workload_seconds,
            'window_processing_ms_p95':sorted(latencies)[949],'isolated_restore_seconds':recovery_seconds,
            'database_bytes':restored.stat().st_size,'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'governance/evidence/local-pilot-integration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

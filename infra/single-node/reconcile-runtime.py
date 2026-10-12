"""Host-local scheduled reconciliation for the fictional reference fleet."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import json
import subprocess

root=Path('/var/lib/pulse-ops/reconciliation')
root.mkdir(mode=0o700,parents=True,exist_ok=True)
config=json.loads(Path('/home/pulseadmin/pulse-release/reconciliation-config.json').read_text())
now=datetime.now(ZoneInfo(config['plant_timezone']))
config.update(day=str(now.date()-timedelta(days=1)),as_of=now.isoformat())
code='''import json,sys
from pulse.reconciliation import reconcile_database
print(json.dumps(reconcile_database('/data/assessments.db',**json.load(sys.stdin))))
'''
result=subprocess.run(['/usr/local/bin/k3s','kubectl','-n','pulse','exec','-i','deployment/pulse-api','--','python','-c',code],input=json.dumps(config),text=True,capture_output=True,timeout=60,check=True)
report=json.loads(result.stdout)
report.update(executed_at=now.isoformat(),execution='host systemd service; fictional reference fleet',scheduled_execution_verified=False)
# One bounded report per local day plus latest snapshot. Never delete receipts.
path=root/(config['day']+'.json')
if not path.exists() and len(list(root.glob('????-??-??.json')))>=366:
    raise RuntimeError('Report retention limit reached; operator disposition required')
for destination in [path,root/'latest.json']:
    temporary=destination.with_suffix('.tmp')
    temporary.write_text(json.dumps(report,indent=2)+'\n')
    temporary.replace(destination)
print(json.dumps({'day':report['day'],'counts':{s:sum(a['status']==s for a in report['assets']) for s in set(a['status'] for a in report['assets'])},'report_persisted':True,'fictional':True}))

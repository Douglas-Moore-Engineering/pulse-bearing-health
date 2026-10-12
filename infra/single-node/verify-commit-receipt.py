"""Exercise new commit evidence through the authenticated reference API."""
import runpy,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone
context=runpy.run_path('/home/pulseadmin/pulse-release/verify-live-api.py')
payload=json.loads(context['body'])
payload['window_id']='reconciliation-commit-fixture-repeatable-20261012'
payload['observed_at']=datetime.now(timezone.utc).isoformat()
fixture=Path('/home/pulseadmin/pulse-release/commit-fixture.json')
if fixture.exists():payload=json.loads(fixture.read_text())
else:fixture.write_text(json.dumps(payload))
request=urllib.request.Request(context['base']+'/v1/degradation/assess',data=json.dumps(payload).encode(),headers=context['headers'])
with urllib.request.urlopen(request,timeout=20) as response:
 result=json.load(response)
assert result['persisted']
print(json.dumps({'new_fixture_persisted':True,'qualified_detector':False}))

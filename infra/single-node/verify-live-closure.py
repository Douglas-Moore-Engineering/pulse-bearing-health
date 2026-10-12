"""Synthetic reference closure check; does not assert human maintenance."""
import runpy,json
from datetime import datetime,timezone
c=runpy.run_path('/home/pulseadmin/pulse-release/verify-live-pilot.py')
call=c['call'];url=c['url'].removesuffix('/reviews')+'/close'
body={'rationale':'Synthetic rollout closure; no physical inspection or real maintenance asserted.',
      'evidence':['fixture:reference-rollout-closure']}
assert call(url,body,False)[0]==401
status,response=call(url,body)
report={'executed_at':datetime.now(timezone.utc).isoformat(),'closure_status':status,
 'fixture_only':True,'qualified_detector':False,'roles_observed':c['claims'].get('roles',[])}
if status==200:
 assert response['state']=='CLOSED' and not response['human_identity_verified']
 assert call(url,body)==(status,response)
 assert call(url,dict(body,rationale='Conflicting synthetic retry'))[0]==409
 report.update(closure_retry_identical=True,conflicting_retry_status=409)
else:
 assert status==403
 report['pending']='Role not available in token; live closure and recovery not verified'
print(json.dumps(report,indent=2))

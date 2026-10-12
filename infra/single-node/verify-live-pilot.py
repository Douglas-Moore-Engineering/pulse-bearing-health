"""Live synthetic pilot checks; run on the VM, never export tokens."""
import base64, json, urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone
q=urllib.parse.urlencode({'api-version':'2018-02-01','resource':'api://a7064e03-b8e9-46d7-bb0d-52f030b2a39a','client_id':'e168e6af-1310-4cbf-9677-54e5ff3f294b'})
with urllib.request.urlopen(urllib.request.Request('http://169.254.169.254/metadata/identity/oauth2/token?'+q,headers={'Metadata':'true'}),timeout=20) as r:
 token=json.load(r)['access_token']
def call(path,body=None,auth=True):
 headers={'Content-Type':'application/json'}
 if auth:headers['Authorization']='Bearer '+token
 try:
  with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:18080'+path,data=None if body is None else json.dumps(body).encode(),headers=headers),timeout=20) as r:return r.status,json.load(r)
 except urllib.error.HTTPError as e:return e.code,None
claims=json.loads(base64.urlsafe_b64decode(token.split('.')[1]+'=='))
report={'token_roles_observed':claims.get('roles',[]),'token_expires_at':claims.get('exp'),'executed_at':datetime.now(timezone.utc).isoformat(),'fixture_only':True,'qualified_detector':False}
d={'metadata':{k:'synthetic-reference' for k in ['asset_id','sensor_id','calibration_ref','data_use_ref','provenance_ref']},'window':{'schema_version':'0.1','dataset_id':'synthetic','bearing_id':'b','run_id':'r','window_id':'w','source_sha256':'0'*64,'sample_rate_hz':100,'unit':'g','samples':[0,1,-1],'time_basis':'utc','timestamp_utc':'2026-10-11T12:00:00Z','split':'test'}}
d['metadata']['asset_id']='ims-run2-bearing1-reference'
p='/v1/intake/validate'
assert call(p,d,False)[0]==401
status,result=call(p,d);assert status==200 and result['status']=='STRUCTURALLY_VALID_PENDING_REVIEW'
d['metadata']['asset_id']='unauthorized';assert call(p,d)[0]==403
report.update(intake_validated=True,anonymous_status=401,cross_asset_status=403)
s,inbox=call('/v1/reference/alerts');assert s==200
url='/v1/reference/alerts/'+inbox['events'][0]['event_id']+'/reviews'
s,history=call(url);report['review_status']=s
if s==200:
 rows=history['reviews']
 body={'outcome':'unresolved','rationale':'Synthetic rollout exercise; no human inspection or detector acceptance.','evidence':[]}
 if rows:body['supersedes']=rows[-1]['id']
 s,first=call(url,body);assert s==200
 body['supersedes']=first['review_id'];s,second=call(url,body);assert s==200
 assert call(url,body)[0]==409
 s,history=call(url);assert s==200 and len(history['reviews'])==len(rows)+2
 report.update(review_history_count=len(history['reviews']),correction_conflict_status=409,principal_authenticated=second['principal_authenticated'],human_identity_verified=False)
else:report['review_check_pending']='Managed identity review access not yet available'
print(json.dumps(report,indent=2))

"""Run on the authorized VM; never print or save managed-identity access tokens."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

root = Path('/home/pulseadmin/pulse-release')
fixture = root/'live-fixture.json'
if not fixture.exists():
    fixture.write_text(json.dumps({
        'schema_version': '1', 'asset_id': 'generated-validation-bearing',
        'window_id': 'azure-deployment-smoke-20261011',
        'observed_at': datetime.now(timezone.utc).isoformat(),
        'source_sha256': hashlib.sha256(b'generated deployment fixture').hexdigest(),
        'unit': 'g', 'sample_rate_hz': 12800.0, 'samples': [-1.0, 1.0]*64}))
body = fixture.read_bytes()
base = 'http://127.0.0.1:18080'
query = urllib.parse.urlencode({
    'api-version': '2018-02-01',
    'resource': 'api://a7064e03-b8e9-46d7-bb0d-52f030b2a39a',
    'client_id': 'e168e6af-1310-4cbf-9677-54e5ff3f294b'})
request = urllib.request.Request('http://169.254.169.254/metadata/identity/oauth2/token?'+query,
                                 headers={'Metadata': 'true'})
with urllib.request.urlopen(request, timeout=20) as response:
    token = json.load(response)['access_token']
headers = {'Authorization': 'Bearer '+token, 'Content-Type': 'application/json'}
request = urllib.request.Request(base+'/v1/degradation/assess', data=body, headers=headers)
with urllib.request.urlopen(request, timeout=20) as response:
    result = json.load(response)
assert result['persisted'] and result['alert_status'] == 'unavailable'
assert not result['notification_sent'] and not result['site_validated']
previous = root/'live-receipt.json'
replayed = previous.exists()
if replayed:
    assert json.loads(previous.read_text()) == result, 'Persisted receipt changed on retry'
else:
    previous.write_text(json.dumps(result))
try:
    urllib.request.urlopen(urllib.request.Request(base+'/v1/degradation/assess', data=body,
                           headers={'Content-Type': 'application/json'}), timeout=10)
    raise AssertionError('Anonymous assessment accepted')
except urllib.error.HTTPError as error:
    assert error.code == 401
unauthorized = dict(json.loads(body), asset_id='unauthorized-bearing')
try:
    urllib.request.urlopen(urllib.request.Request(base+'/v1/degradation/assess',
        data=json.dumps(unauthorized).encode(), headers=headers), timeout=10)
    raise AssertionError('Cross-asset assessment accepted')
except urllib.error.HTTPError as error:
    assert error.code == 403
print(json.dumps({'authenticatedRequest': 'passed', 'managedIdentityTokenVerified': True,
                  'persisted': True, 'replayedSameReceipt': replayed, 'anonymousStatus': 401,
                  'crossAssetStatus': 403,
                  'assessmentId': result['assessment_id'], 'qualifiedAlertsAvailable': False,
                  'fixtureOnly': True}))

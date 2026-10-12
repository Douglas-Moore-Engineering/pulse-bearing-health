"""Replay verified benchmark features into the unqualified Azure reference route."""
import hashlib
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request

root = Path('/home/pulseadmin/pulse-release')
query = urllib.parse.urlencode({'api-version': '2018-02-01',
    'resource': 'api://a7064e03-b8e9-46d7-bb0d-52f030b2a39a',
    'client_id': 'e168e6af-1310-4cbf-9677-54e5ff3f294b'})
with urllib.request.urlopen(urllib.request.Request(
        'http://169.254.169.254/metadata/identity/oauth2/token?'+query,
        headers={'Metadata': 'true'}), timeout=20) as response:
    token = json.load(response)['access_token']
headers = {'Authorization': 'Bearer '+token, 'Content-Type': 'application/json'}


def request(path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:18080'+path,
            data=data, headers=headers), timeout=20) as response:
        return json.load(response)


source = root/'reference-ims-replay.jsonl'
lines = source.read_text().splitlines()
assert len(lines) == 884
flagged = 0
events = set()
started = time.monotonic()
latencies = []
for line in lines:
    payload = json.loads(line)
    before = time.monotonic()
    result = request('/v1/reference/assess', payload)
    latencies.append((time.monotonic()-before)*1000)
    assert result['persisted'] and not result['qualified_detector'] and not result['external_notification_sent']
    if result['reference_status'] == 'reference_anomaly':
        flagged += 1
        events.add(result['event_id'])
assert flagged == 17 and len(events) == 1
assert request('/v1/reference/assess', payload) == result
inbox = request('/v1/reference/alerts')
event = next(item for item in inbox['events'] if item['event_id'] in events)
episode = json.loads(event['payload'])
assert episode['source_timestamp'] == '2004.02.19.03.22.39'
ack = request('/v1/reference/alerts/'+event['event_id']+'/acknowledge', {})
assert ack['acknowledged_by']
assert request('/v1/reference/alerts/'+event['event_id']+'/acknowledge', {}) == ack
latencies.sort()
print(json.dumps({'scope': 'Real benchmark-feature replay; unqualified detector; fictional local inbox',
    'windows': len(lines), 'flagged_windows': flagged, 'unique_episodes': len(events),
    'first_flag_source_timestamp': episode['source_timestamp'], 'source_timezone': 'unknown',
    'receipt_replay_identical': True, 'acknowledgement_replay_identical': True,
    'acknowledgement_actor': 'automated reference client; not a human acceptance',
    'seconds': time.monotonic()-started, 'p95_ms': latencies[int(.95*(len(latencies)-1))],
    'feature_replay_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'qualified_detector': False, 'external_notification_sent': False,
    'daily_capacity_qualified': False}, indent=2))

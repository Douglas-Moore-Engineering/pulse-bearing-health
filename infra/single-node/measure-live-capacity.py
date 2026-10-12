"""Short VM-local authenticated persistence load experiment, not a daily SLA proof."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import time
import urllib.parse
import urllib.request
import uuid

query = urllib.parse.urlencode({'api-version': '2018-02-01',
    'resource': 'api://a7064e03-b8e9-46d7-bb0d-52f030b2a39a',
    'client_id': 'e168e6af-1310-4cbf-9677-54e5ff3f294b'})
request = urllib.request.Request('http://169.254.169.254/metadata/identity/oauth2/token?'+query,
                                 headers={'Metadata': 'true'})
with urllib.request.urlopen(request, timeout=20) as response:
    token = json.load(response)['access_token']
headers = {'Authorization': 'Bearer '+token, 'Content-Type': 'application/json'}
run_id = uuid.uuid4().hex
base = {'schema_version': '1', 'asset_id': 'generated-capacity-bearing',
        'observed_at': datetime.now(timezone.utc).isoformat(), 'source_sha256': 'a'*64,
        'unit': 'g', 'sample_rate_hz': 12800.0, 'samples': [-1.0, 1.0]*2048}


def send(window_id):
    body = json.dumps(dict(base, window_id=window_id)).encode()
    started = time.monotonic()
    try:
        with urllib.request.urlopen(urllib.request.Request(
                'http://127.0.0.1:18080/v1/degradation/assess', data=body, headers=headers), timeout=10) as response:
            result = json.load(response)
            return result['persisted'] and result['alert_status'] == 'unavailable', time.monotonic()-started
    except Exception:
        return False, time.monotonic()-started


stages = []
for rate in (17.4, 70):
    duration = 20
    count = int(rate*duration)
    dropped = 0
    with ThreadPoolExecutor(max_workers=16) as pool:
        pending, submitted = set(), []
        start = time.monotonic()
        for i in range(count):
            delay = start+i/rate-time.monotonic()
            if delay > 0:
                time.sleep(delay)
            pending = {f for f in pending if not f.done()}
            if len(pending) >= 64:
                dropped += 1
                continue
            rate_label = str(rate).replace('.', '_')
            f = pool.submit(send, f'{run_id}-{rate_label}-{i}')
            pending.add(f); submitted.append(f)
        results = [f.result() for f in submitted]
    elapsed = time.monotonic()-start
    latencies = sorted(seconds for ok, seconds in results)
    failures = sum(not ok for ok, seconds in results)
    stages.append({'offeredRps': rate, 'seconds': duration, 'offeredRequests': count,
        'completed': len(results), 'failures': failures, 'dropped': dropped,
        'achievedRps': len(results)/elapsed, 'p95Ms': latencies[int(.95*(len(latencies)-1))]*1000,
        'samplesPerRequest': 4096})
print(json.dumps({'scope': '20-second VM-local tests with real Entra and SQLite persistence; no qualified model or external network',
                  'dailyCapacityQualified': False, 'stages': stages}))

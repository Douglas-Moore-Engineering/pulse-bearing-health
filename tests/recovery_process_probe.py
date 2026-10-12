"""Test-only fresh-interpreter recovery probe; synthetic identity, loopback only."""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import socket
import sys
import threading
import time

import httpx
import uvicorn
from pulse.api import Settings, create_app
from pulse.assessment_store import AssessmentStore
from pulse.reference_detector import ASSET, ReferenceDetector


@contextmanager
def local_http_client(app):
    # Keep the ephemeral port bound throughout startup to avoid a port-selection race.
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('127.0.0.1', 0))
    port = listener.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level='error', access_log=False))
    worker = threading.Thread(target=server.run, kwargs={'sockets': [listener]}, daemon=True)
    try:
        worker.start()
        deadline = time.monotonic() + 10
        while not server.started:
            if not worker.is_alive() or time.monotonic() >= deadline:
                raise RuntimeError('Recovered HTTP application did not start')
            time.sleep(0.02)
        with httpx.Client(base_url=f'http://127.0.0.1:{port}', timeout=5, trust_env=False) as client:
            yield client
    finally:
        server.should_exit = True
        worker.join(timeout=5)
        listener.close()
        if worker.is_alive():
            raise RuntimeError('Recovered HTTP application did not stop')


def main():
    fixture = json.loads(Path(sys.argv[1]).read_text())
    database = Path(sys.argv[2] if len(sys.argv) > 2 else fixture['database'])
    # Prevent an accidentally missing path from silently becoming an empty DB.
    if not database.is_file():
        raise RuntimeError('Restored database is absent')
    claims = {'oid': 'caller', 'azp': 'client',
              'roles': ['Pulse.Assess', 'Pulse.Review', 'Pulse.Close']}
    settings = Settings('tenant', 'audience', ('client',), asset_grants={'client': (ASSET,)})
    app = create_app(settings, lambda _: dict(claims), store=AssessmentStore(database),
                     reference=ReferenceDetector(database), review_db=database)
    headers = {'Authorization': 'Bearer synthetic'}
    with local_http_client(app) as client:
        assert client.get('/health/ready').status_code == 200
        response = client.post('/v1/degradation/assess', headers=headers, json=fixture['data'])
        assert response.status_code == 200 and response.json() == fixture['receipt']
        base = fixture['base']
        assert client.get(base + '/reviews', headers=headers).json() == fixture['history']
        response = client.post(base + '/close', headers=headers, json=fixture['closure'])
        assert response.status_code == 200 and response.json() == fixture['closed']
        assert client.get(base + '/reviews').status_code == 401
        claims['oid'] = 'other'
        assert client.get(base + '/reviews', headers=headers).status_code == 404
        claims['oid'] = 'caller'
        claims['roles'] = ['Pulse.Assess']
        assert client.get(base + '/reviews', headers=headers).status_code == 403
    print(json.dumps({'result': 'PASS', 'pid': os.getpid(),
                      'transport': 'HTTP loopback', 'synthetic_identity': True}))


if __name__ == '__main__':
    main()

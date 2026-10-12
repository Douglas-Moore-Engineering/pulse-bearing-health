"""Synthetic whole-database restore through a fresh ASGI application."""
from contextlib import closing
import json
import os
from pathlib import Path
import runpy
import sqlite3
import subprocess
import sys

from fastapi.testclient import TestClient
from pulse.api import Settings, create_app
from pulse.assessment_store import AssessmentStore
from pulse.reference_detector import ASSET, ReferenceDetector
from test_api import payload as assessment_payload
from test_reference_detector import payload as reference_payload


def test_restored_application_preserves_receipts_reviews_and_closure(tmp_path):
    original = tmp_path / 'original.db'
    restored = tmp_path / 'restored.db'
    claims = {'oid': 'caller', 'azp': 'client',
              'roles': ['Pulse.Assess', 'Pulse.Review', 'Pulse.Close']}
    settings = Settings('tenant', 'audience', ('client',), asset_grants={'client': (ASSET,)})
    headers = {'Authorization': 'Bearer synthetic'}

    def application(path):
        return TestClient(create_app(settings, lambda _: dict(claims),
            store=AssessmentStore(path), reference=ReferenceDetector(path), review_db=path))

    data = assessment_payload()
    data['asset_id'] = ASSET
    closure = {'rationale': 'Synthetic closure', 'evidence': ['fixture:inspection']}
    with application(original) as client:
        receipt = client.post('/v1/degradation/assess', headers=headers, json=data)
        assert receipt.status_code == 200
        for index in range(3):
            event = client.post('/v1/reference/assess', headers=headers, json=reference_payload(index))
            assert event.status_code == 200
        base = '/v1/reference/alerts/' + event.json()['event_id']
        assert client.post(base + '/acknowledge', headers=headers).status_code == 200
        review = client.post(base + '/reviews', headers=headers,
            json={'outcome': 'unresolved', 'rationale': 'Synthetic review', 'evidence': []})
        assert review.status_code == 200
        assert client.post(base + '/reviews', headers=headers,
            json={'outcome': 'nuisance', 'rationale': 'Synthetic correction',
                  'evidence': ['fixture:inspection'], 'supersedes': review.json()['review_id']}).status_code == 200
        history = client.get(base + '/reviews', headers=headers).json()
        closed = client.post(base + '/close', headers=headers, json=closure)
        assert closed.status_code == 200
    with closing(sqlite3.connect(original)) as source, closing(sqlite3.connect(restored)) as target:
        source.backup(target)
        assert target.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert target.execute('PRAGMA foreign_key_check').fetchall() == []
    # Remove access to the source path before constructing the recovered app.
    original.rename(tmp_path / 'unavailable-source.db')
    fixture = tmp_path / 'recovery-expectations.json'
    fixture.write_text(json.dumps({'database': str(restored), 'data': data,
        'receipt': receipt.json(), 'base': base, 'history': history,
        'closure': closure, 'closed': closed.json()}))
    environment = os.environ.copy()
    source_path = str(Path(__file__).resolve().parents[1] / 'src')
    environment['PYTHONPATH'] = os.pathsep.join([source_path, environment.get('PYTHONPATH', '')])
    result = subprocess.run([sys.executable, str(Path(__file__).parent /
        'recovery_process_probe.py'), str(fixture)], env=environment,
        capture_output=True, text=True, timeout=30, check=True)
    report = json.loads(result.stdout)
    assert report['pid'] != os.getpid()
    assert report['result'] == 'PASS'
    assert report['transport'] == 'HTTP loopback'
    if os.environ.get('PULSE_RECOVERY_KUBERNETES') == '1':
        helper = runpy.run_path(str(Path(__file__).resolve().parents[1] /
            'scripts/exercise_kubernetes_application.py'))['exercise']
        result = helper(os.environ['PULSE_RECOVERY_TEST_IMAGE'], restored, fixture,
                        Path(__file__).parent / 'recovery_process_probe.py')
        assert result['namespace_removed'] and result['pod_replaced']
        assert result['default_deployment_recovered']
        assert result['service_dns_and_routing_verified']
        if os.environ.get('PULSE_VERIFY_NETWORK_POLICY') == '1':
            assert result['network_policy']['ingress_denied'], 'Rendered ingress deny policy was not enforced'
            assert result['network_policy']['private_egress_denied'], 'Private egress was not blocked'
            if os.environ.get('PULSE_VERIFY_PUBLIC_HTTPS') == '1':
                assert result['network_policy']['public_https']['status'] == 200
    # Explicit opt-in: ordinary CI and local tests never require a Docker daemon.
    image = os.environ.get('PULSE_RECOVERY_TEST_IMAGE')
    if image:
        probe = Path(__file__).parent / 'recovery_process_probe.py'
        result = subprocess.run(['docker', 'run', '--rm', '--pull=never',
            '--network=none', '--read-only', '--cap-drop=ALL',
            '--security-opt=no-new-privileges', '--memory=512m', '--cpus=1',
            '--tmpfs', '/tmp:rw,noexec,nosuid,size=16m',
            '--mount', f'type=bind,source={tmp_path.resolve()},target=/recovery',
            '--mount', f'type=bind,source={probe.resolve()},target=/probe.py,readonly',
            image, 'python', '/probe.py', '/recovery/recovery-expectations.json',
            '/recovery/restored.db'], capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, result.stderr
        container_report = json.loads(result.stdout)
        assert container_report['result'] == 'PASS'
        assert container_report['transport'] == 'HTTP loopback'
        # Exercise the unmodified image CMD and production identity verifier.
        client_id = '00000000-0000-0000-0000-000000000003'
        render = runpy.run_path(str(Path(__file__).resolve().parents[1] /
            'scripts/render_single_node_manifests.py'))['render']
        manifests = render(image=image,
            tenant='00000000-0000-0000-0000-000000000001',
            audience='00000000-0000-0000-0000-000000000002',
            clients=[client_id], pilot_components=True)
        configuration = next(doc['data'] for doc in manifests if doc['kind'] == 'ConfigMap')
        deployment = next(doc for doc in manifests if doc['kind'] == 'Deployment')
        container_spec = deployment['spec']['template']['spec']['containers'][0]
        mount_path = container_spec['volumeMounts'][0]['mountPath']
        assert configuration['PULSE_REVIEW_DB'] == configuration['PULSE_ASSESSMENT_DB']
        with closing(sqlite3.connect(restored)) as source, closing(sqlite3.connect(tmp_path / 'assessments.db')) as target:
            source.backup(target)
        command = ['docker', 'run', '-d', '--pull=never', '--network=none',
            '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
            '--memory=512m', '--cpus=1', '--tmpfs', '/tmp:rw,noexec,nosuid,size=16m',
            '--mount', f'type=bind,source={tmp_path.resolve()},target={mount_path}']
        for key, value in configuration.items():
            command.extend(['--env', f'{key}={value}'])
        container = subprocess.run(command + [image], capture_output=True, text=True,
                                   timeout=30, check=True).stdout.strip()
        try:
            probe = '''import time,urllib.request,urllib.error
deadline=time.monotonic()+15
while True:
 try:
  with urllib.request.urlopen('http://127.0.0.1:8000/health/ready',timeout=2) as r:
   assert r.status==200
  break
 except OSError:
  if time.monotonic()>deadline: raise
  time.sleep(.1)
for headers in ({},{'Authorization':'Bearer invalid'}):
 try:
  urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8000/v1/reference/alerts',headers=headers),timeout=3)
  raise AssertionError('Unauthorized request accepted')
 except urllib.error.HTTPError as error:
  assert error.code==401,error.code
print('DEFAULT_ENTRYPOINT_PASS')
'''
            response = subprocess.run(['docker', 'exec', container, 'python', '-c', probe],
                capture_output=True, text=True, timeout=25)
            assert response.returncode == 0, response.stderr
            assert 'DEFAULT_ENTRYPOINT_PASS' in response.stdout
        finally:
            subprocess.run(['docker', 'rm', '-f', container], capture_output=True,
                           text=True, timeout=20, check=True)
        for missing in ('PULSE_TENANT_ID', 'PULSE_REVIEW_DB'):
            incomplete = ['docker', 'run', '-d', '--pull=never', '--network=none',
                '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
                '--memory=512m', '--cpus=1']
            for key, value in configuration.items():
                if key != missing:
                    incomplete.extend(['--env', f'{key}={value}'])
            failed_container = subprocess.run(incomplete + [image], capture_output=True,
                text=True, timeout=30, check=True).stdout.strip()
            try:
                exit_status = subprocess.run(['docker', 'wait', failed_container],
                    capture_output=True, text=True, timeout=25, check=True)
                assert int(exit_status.stdout.strip()) != 0
                logs = subprocess.run(['docker', 'logs', failed_container],
                    capture_output=True, text=True, timeout=10, check=True)
                assert f"KeyError: '{missing}'" in logs.stderr
            finally:
                subprocess.run(['docker', 'rm', '-f', failed_container], capture_output=True,
                    text=True, timeout=20, check=True)
    with application(restored) as client:
        assert client.get('/health/ready').status_code == 200
        assert client.post('/v1/degradation/assess', headers=headers, json=data).json() == receipt.json()
        assert client.get(base + '/reviews', headers=headers).json() == history
        assert client.post(base + '/close', headers=headers, json=closure).json() == closed.json()
        assert client.post(base + '/close', headers=headers,
            json=dict(closure, rationale='conflicting disposition')).status_code == 409
        assert client.get(base + '/reviews').status_code == 401
        claims['oid'] = 'other'
        assert client.get(base + '/reviews', headers=headers).status_code == 404
        claims['oid'] = 'caller'
        claims['roles'] = ['Pulse.Assess']
        assert client.get(base + '/reviews', headers=headers).status_code == 403

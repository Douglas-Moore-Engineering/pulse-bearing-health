"""Verify PVC persistence across pod replacement on loopback-only Kubernetes."""
import argparse
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    context = 'docker-desktop'
    namespace = 'pulse-storage-check-' + uuid.uuid4().hex[:10]
    def kubectl(*commands, data=None):
        return subprocess.run(['kubectl', '--context', context, '--request-timeout=15s',
            *commands], input=data, capture_output=True, text=True, timeout=55, check=True).stdout
    config = json.loads(kubectl('config', 'view', '--minify', '-o', 'json'))
    endpoint = config['clusters'][0]['cluster']['server']
    if urlparse(endpoint).hostname not in ('127.0.0.1', 'localhost', '::1'):
        raise RuntimeError('Only a loopback Kubernetes endpoint is permitted')
    marker = 'synthetic-' + uuid.uuid4().hex
    image = 'docker.io/kindest/local-path-helper:v20230510-486859a6'
    def pod(name, command):
        return {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': name, 'namespace': namespace},
            'spec': {'restartPolicy': 'Never', 'automountServiceAccountToken': False,
                'securityContext': {'runAsUser': 10001, 'runAsGroup': 10001, 'fsGroup': 10001,
                    'runAsNonRoot': True, 'seccompProfile': {'type': 'RuntimeDefault'}},
                'containers': [{'name': 'check', 'image': image, 'imagePullPolicy': 'Never',
                    'command': ['sh', '-c', command],
                    'securityContext': {'allowPrivilegeEscalation': False,
                        'readOnlyRootFilesystem': True, 'capabilities': {'drop': ['ALL']}},
                    'resources': {'limits': {'cpu': '100m', 'memory': '32Mi'}},
                    'volumeMounts': [{'name': 'data', 'mountPath': '/data'}]}],
                'volumes': [{'name': 'data', 'persistentVolumeClaim': {'claimName': 'check'}}]}}
    resources = [
        {'apiVersion': 'v1', 'kind': 'Namespace', 'metadata': {'name': namespace,
            'labels': {'pod-security.kubernetes.io/enforce': 'restricted'}}},
        {'apiVersion': 'v1', 'kind': 'PersistentVolumeClaim', 'metadata': {'name': 'check', 'namespace': namespace},
            'spec': {'storageClassName': 'standard', 'accessModes': ['ReadWriteOnce'],
                'resources': {'requests': {'storage': '16Mi'}}}},
        pod('writer', f'printf %s {marker} > /data/marker')]
    try:
        kubectl('apply', '-f', '-', data=yaml.safe_dump_all(resources))
        kubectl('-n', namespace, 'wait', '--for=jsonpath={.status.phase}=Succeeded', 'pod/writer', '--timeout=40s')
        kubectl('-n', namespace, 'delete', 'pod', 'writer', '--wait=true', '--timeout=40s')
        kubectl('apply', '-f', '-', data=yaml.safe_dump(pod('reader', 'IFS= read -r value < /data/marker; printf %s "$value"')))
        kubectl('-n', namespace, 'wait', '--for=jsonpath={.status.phase}=Succeeded', 'pod/reader', '--timeout=40s')
        recovered = kubectl('-n', namespace, 'logs', 'reader').strip()
        if recovered != marker:
            raise RuntimeError('Persistent marker did not survive pod replacement')
        report = {'result': 'PASS', 'observed_at': datetime.now(timezone.utc).isoformat(),
            'context': context, 'endpoint': endpoint, 'namespace': namespace,
            'storage_class': 'standard', 'image': image, 'synthetic_marker_restored': True,
            'scope': 'Local PVC persistence across pod replacement; not application or host-loss recovery'}
    except subprocess.CalledProcessError as error:
        report = {'result': 'FAIL', 'observed_at': datetime.now(timezone.utc).isoformat(),
            'namespace': namespace, 'error': error.stderr,
            'diagnostics': kubectl('-n', namespace, 'get', 'events', '-o', 'json'),
            'scope': 'Local PVC persistence; no success claimed'}
    finally:
        kubectl('delete', 'namespace', namespace, '--ignore-not-found=true', '--wait=true', '--timeout=40s')
    report['temporary_namespace_removed'] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
    if report['result'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()

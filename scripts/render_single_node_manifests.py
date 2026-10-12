"""Render the single-node demo; requires a verified, locally imported image."""
import argparse
import json
from pathlib import Path
import re
from uuid import UUID

import yaml


def render(image, tenant, audience, clients, pilot_components=False):
    # The tag is the verified Docker image ID, not a registry manifest digest.
    # Import tooling must verify the image ID before applying this manifest.
    if not re.fullmatch(r'pulse-api:sha256-[a-f0-9]{64}', image):
        raise ValueError('Use a locally verified Docker image SHA-256 tag')
    if not clients or any(UUID(value).int == 0 for value in (tenant, audience, *clients)):
        raise ValueError('Real identity IDs and at least one caller are required')
    labels = {'app': 'pulse-api'}
    def resource(api, kind, name, **fields):
        return dict(apiVersion=api, kind=kind, metadata={'name': name, 'namespace': 'pulse'}, **fields)
    namespace = {'apiVersion': 'v1', 'kind': 'Namespace', 'metadata': {'name': 'pulse', 'labels': {
        'pod-security.kubernetes.io/enforce': 'restricted'}}}
    container = {
        'name': 'api', 'image': image, 'imagePullPolicy': 'Never',
        'envFrom': [{'configMapRef': {'name': 'pulse-api'}}],
        'ports': [{'name': 'http', 'containerPort': 8000}],
        'resources': {'requests': {'cpu': '250m', 'memory': '256Mi'},
                      'limits': {'cpu': '1', 'memory': '512Mi'}},
        'securityContext': {'runAsNonRoot': True, 'runAsUser': 10001, 'runAsGroup': 10001,
            'readOnlyRootFilesystem': True, 'allowPrivilegeEscalation': False,
            'capabilities': {'drop': ['ALL']}, 'seccompProfile': {'type': 'RuntimeDefault'}},
        'volumeMounts': [{'name': 'receipts', 'mountPath': '/data'}],
        'livenessProbe': {'httpGet': {'path': '/health/live', 'port': 'http'}, 'periodSeconds': 10},
        'readinessProbe': {'httpGet': {'path': '/health/ready', 'port': 'http'}, 'periodSeconds': 5},
        'startupProbe': {'httpGet': {'path': '/health/live', 'port': 'http'},
                         'periodSeconds': 2, 'failureThreshold': 30}}
    return [namespace,
        resource('v1', 'ServiceAccount', 'pulse-api', automountServiceAccountToken=False),
        resource('v1', 'ConfigMap', 'pulse-api', data={
            'PULSE_TENANT_ID': tenant, 'PULSE_API_CLIENT_ID': audience,
            'PULSE_ALLOWED_CLIENT_IDS': ','.join(clients), 'PULSE_ASSESSMENT_DB': '/data/assessments.db',
            'PULSE_ASSET_GRANTS': json.dumps({client: ['generated-validation-bearing',
                'generated-capacity-bearing', 'ims-run2-bearing1-reference'] for client in clients}, sort_keys=True),
            'PULSE_REFERENCE_DETECTOR': '1', **({'PULSE_PILOT_COMPONENTS': '1',
                'PULSE_REVIEW_DB': '/data/assessments.db',
                'PULSE_INTAKE_SCHEMA': '/app/contracts/vibration-window.schema.json'} if pilot_components else {})}),
        resource('v1', 'PersistentVolumeClaim', 'pulse-receipts', spec={
            'accessModes': ['ReadWriteOnce'], 'storageClassName': 'local-path',
            'resources': {'requests': {'storage': '1Gi'}}}),
        resource('apps/v1', 'Deployment', 'pulse-api', spec={
            'replicas': 1, 'strategy': {'type': 'Recreate'}, 'revisionHistoryLimit': 2,
            'selector': {'matchLabels': labels}, 'template': {'metadata': {'labels': labels}, 'spec': {
                'serviceAccountName': 'pulse-api', 'automountServiceAccountToken': False,
                'securityContext': {'fsGroup': 10001, 'fsGroupChangePolicy': 'OnRootMismatch',
                                    'seccompProfile': {'type': 'RuntimeDefault'}},
                'containers': [container], 'volumes': [{'name': 'receipts',
                    'persistentVolumeClaim': {'claimName': 'pulse-receipts'}}]}}}),
        resource('v1', 'Service', 'pulse-api', spec={'type': 'ClusterIP', 'selector': labels,
            'ports': [{'name': 'http', 'port': 80, 'targetPort': 'http'}]}),
        resource('networking.k8s.io/v1', 'NetworkPolicy', 'pulse-isolation', spec={
            'podSelector': {'matchLabels': labels}, 'policyTypes': ['Ingress', 'Egress'],
            'ingress': [], 'egress': [
                {'to': [{'namespaceSelector': {'matchLabels': {'kubernetes.io/metadata.name': 'kube-system'}},
                         'podSelector': {'matchLabels': {'k8s-app': 'kube-dns'}}}],
                 'ports': [{'protocol': 'UDP', 'port': 53}, {'protocol': 'TCP', 'port': 53}]},
                {'to': [{'ipBlock': {'cidr': '0.0.0.0/0', 'except': [
                    '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '169.254.0.0/16']}}],
                 'ports': [{'protocol': 'TCP', 'port': 443}]}]})]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    documents = render(**json.loads(args.config.read_text(encoding='utf-8')))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        yaml.safe_dump_all(documents, stream, sort_keys=False)

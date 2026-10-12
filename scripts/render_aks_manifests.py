"""Render immutable-image AKS manifests; does not apply them or create credentials."""
import argparse
import json
from pathlib import Path
import re
from uuid import UUID

import yaml


def render(image, tenant, audience, clients, hostname, tls_secret):
    if not re.fullmatch(r'[a-z0-9]+\.azurecr\.io/pulse-api@sha256:[a-f0-9]{64}', image):
        raise ValueError('An ACR image pinned by SHA-256 digest is required')
    for value in (tenant, audience, *clients):
        if UUID(value).int == 0:
            raise ValueError('Real nonzero identity identifiers are required')
    if not clients:
        raise ValueError('At least one authorized caller is required')
    if not re.fullmatch(r'(?=.{1,253}$)[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?', hostname) or '.' not in hostname:
        raise ValueError('A TLS hostname is required')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', tls_secret):
        raise ValueError('An existing TLS Secret name is required')
    docs = []

    def add(api, kind, name, spec=None, namespace='pulse', **extra):
        item = {'apiVersion': api, 'kind': kind, 'metadata': {'name': name}}
        if namespace:
            item['metadata']['namespace'] = namespace
        if spec is not None:
            item['spec'] = spec
        item.update(extra); docs.append(item)
        return item

    for name in ('pulse', 'pulse-ingress'):
        ns = add('v1', 'Namespace', name, namespace=None)
        ns['metadata']['labels'] = {'pod-security.kubernetes.io/enforce': 'restricted',
                                    'pod-security.kubernetes.io/enforce-version': 'v1.36'}
    add('v1', 'ServiceAccount', 'pulse-api', automountServiceAccountToken=False)
    add('v1', 'ConfigMap', 'pulse-api', data={'PULSE_TENANT_ID': tenant, 'PULSE_API_CLIENT_ID': audience,
                                          'PULSE_ALLOWED_CLIENT_IDS': ','.join(clients),
                                          'PULSE_ASSET_GRANTS': json.dumps({client: [
                                              'generated-validation-bearing', 'generated-capacity-bearing'
                                          ] for client in clients}, sort_keys=True)})
    labels = {'app': 'pulse-api'}
    container = {'name': 'api', 'image': image, 'imagePullPolicy': 'IfNotPresent',
        'ports': [{'name': 'http', 'containerPort': 8000}], 'envFrom': [{'configMapRef': {'name': 'pulse-api'}}],
        'securityContext': {'runAsNonRoot': True, 'runAsUser': 10001, 'runAsGroup': 10001,
                            'readOnlyRootFilesystem': True, 'allowPrivilegeEscalation': False,
                            'capabilities': {'drop': ['ALL']}, 'seccompProfile': {'type': 'RuntimeDefault'}},
        'resources': {'requests': {'cpu': '500m', 'memory': '256Mi'}, 'limits': {'cpu': '1', 'memory': '512Mi'}},
        'livenessProbe': {'httpGet': {'path': '/health/live', 'port': 'http'}, 'periodSeconds': 10, 'timeoutSeconds': 2},
        'readinessProbe': {'httpGet': {'path': '/health/ready', 'port': 'http'}, 'periodSeconds': 5, 'timeoutSeconds': 2},
        'startupProbe': {'httpGet': {'path': '/health/live', 'port': 'http'}, 'periodSeconds': 2, 'failureThreshold': 30}}
    add('apps/v1', 'Deployment', 'pulse-api', {
        'replicas': 3, 'revisionHistoryLimit': 5, 'progressDeadlineSeconds': 300,
        'strategy': {'type': 'RollingUpdate', 'rollingUpdate': {'maxSurge': 1, 'maxUnavailable': 0}},
        'selector': {'matchLabels': labels},
        'template': {'metadata': {'labels': labels}, 'spec': {
            'serviceAccountName': 'pulse-api', 'automountServiceAccountToken': False,
            'terminationGracePeriodSeconds': 30, 'nodeSelector': {'workload': 'pulse-api'},
            'securityContext': {'runAsNonRoot': True, 'seccompProfile': {'type': 'RuntimeDefault'}},
            'topologySpreadConstraints': [
                {'maxSkew': 1, 'topologyKey': key, 'whenUnsatisfiable': 'ScheduleAnyway', 'labelSelector': {'matchLabels': labels}}
                for key in ('topology.kubernetes.io/zone', 'kubernetes.io/hostname')],
            'containers': [container]}}})
    add('v1', 'Service', 'pulse-api', {'selector': labels, 'type': 'ClusterIP',
                                     'ports': [{'name': 'http', 'port': 80, 'targetPort': 'http'}]})
    add('autoscaling/v2', 'HorizontalPodAutoscaler', 'pulse-api', {
        'scaleTargetRef': {'apiVersion': 'apps/v1', 'kind': 'Deployment', 'name': 'pulse-api'},
        'minReplicas': 3, 'maxReplicas': 12,
        'metrics': [{'type': 'Resource', 'resource': {'name': 'cpu', 'target': {'type': 'Utilization', 'averageUtilization': 60}}}],
        'behavior': {'scaleDown': {'stabilizationWindowSeconds': 300},
                     'scaleUp': {'stabilizationWindowSeconds': 0, 'policies': [{'type': 'Pods', 'value': 3, 'periodSeconds': 30}]}}})
    add('policy/v1', 'PodDisruptionBudget', 'pulse-api', {'minAvailable': 2, 'selector': {'matchLabels': labels}})
    add('v1', 'ResourceQuota', 'pulse-budget', {'hard': {'pods': '16', 'requests.cpu': '8', 'limits.cpu': '16',
                                                      'requests.memory': '4Gi', 'limits.memory': '8Gi'}})
    add('networking.k8s.io/v1', 'NetworkPolicy', 'default-deny', {'podSelector': {}, 'policyTypes': ['Ingress', 'Egress']})
    add('networking.k8s.io/v1', 'NetworkPolicy', 'api-traffic', {
        'podSelector': {'matchLabels': labels}, 'policyTypes': ['Ingress', 'Egress'],
        'ingress': [{'from': [{'namespaceSelector': {'matchLabels': {'kubernetes.io/metadata.name': 'pulse-ingress'}},
                              'podSelector': {'matchLabels': {'gateway.networking.k8s.io/gateway-name': 'pulse'}}}],
                     'ports': [{'protocol': 'TCP', 'port': 8000}]},
                    {'from': [{'namespaceSelector': {'matchLabels': {'kubernetes.io/metadata.name': 'kube-system'}}}],
                     'ports': [{'protocol': 'TCP', 'port': 8000}]}],
        'egress': [{'to': [{'namespaceSelector': {'matchLabels': {'kubernetes.io/metadata.name': 'kube-system'}},
                           'podSelector': {'matchLabels': {'k8s-app': 'kube-dns'}}}],
                    'ports': [{'protocol': 'UDP', 'port': 53}, {'protocol': 'TCP', 'port': 53}]},
                   {'to': [{'ipBlock': {'cidr': '0.0.0.0/0', 'except': ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '169.254.0.0/16']}}],
                    'ports': [{'protocol': 'TCP', 'port': 443}]}]})
    add('gateway.networking.k8s.io/v1', 'Gateway', 'pulse', {
        'gatewayClassName': 'approuting-istio',
        'infrastructure': {'annotations': {'service.beta.kubernetes.io/azure-load-balancer-internal': 'true'}},
        'listeners': [{'name': 'https', 'protocol': 'HTTPS', 'port': 443, 'hostname': hostname,
                       'tls': {'mode': 'Terminate', 'certificateRefs': [{'kind': 'Secret', 'name': tls_secret}]},
                       'allowedRoutes': {'namespaces': {'from': 'Selector', 'selector': {'matchLabels': {'kubernetes.io/metadata.name': 'pulse'}}}}}]},
        namespace='pulse-ingress')
    add('gateway.networking.k8s.io/v1', 'HTTPRoute', 'pulse-api', {
        'parentRefs': [{'name': 'pulse', 'namespace': 'pulse-ingress', 'sectionName': 'https'}], 'hostnames': [hostname],
        'rules': [{'matches': [{'path': {'type': 'Exact', 'value': '/v1/degradation/assess'}, 'method': 'POST'}],
                   'timeouts': {'request': '5s', 'backendRequest': '4s'},
                   'backendRefs': [{'name': 'pulse-api', 'port': 80}]}]})
    return docs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    docs = render(**json.loads(args.config.read_text(encoding='utf-8')))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        yaml.safe_dump_all(docs, stream, sort_keys=False)

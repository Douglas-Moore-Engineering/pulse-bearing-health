import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('render_aks', Path(__file__).parents[1]/'scripts/render_aks_manifests.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


def config():
    return dict(image='fixture.azurecr.io/pulse-api@sha256:'+'a'*64,
                tenant='00000000-0000-0000-0000-000000000001', audience='00000000-0000-0000-0000-000000000002',
                clients=['00000000-0000-0000-0000-000000000003'], hostname='pulse.example.test', tls_secret='fixture-tls')


def test_safeguards_routing_and_scaling():
    docs = module.render(**config())
    deployment = next(d for d in docs if d['kind'] == 'Deployment')
    pod = deployment['spec']['template']['spec']; container = pod['containers'][0]
    assert pod['automountServiceAccountToken'] is False
    assert container['securityContext']['readOnlyRootFilesystem']
    assert container['securityContext']['capabilities']['drop'] == ['ALL']
    assert all(p in container for p in ('startupProbe', 'readinessProbe', 'livenessProbe'))
    hpa = next(d for d in docs if d['kind'] == 'HorizontalPodAutoscaler')['spec']
    assert hpa['minReplicas'] >= 3 and hpa['maxReplicas'] == 12
    gateway = next(d for d in docs if d['kind'] == 'Gateway')['spec']
    assert gateway['listeners'][0]['protocol'] == 'HTTPS'
    assert gateway['infrastructure']['annotations']['service.beta.kubernetes.io/azure-load-balancer-internal'] == 'true'
    route = next(d for d in docs if d['kind'] == 'HTTPRoute')['spec']
    assert route['rules'][0]['matches'][0]['path']['value'] == '/v1/degradation/assess'


@pytest.mark.parametrize('change', [{'image': 'fixture.azurecr.io/pulse-api:latest'}, {'clients': []},
    {'tenant': '00000000-0000-0000-0000-000000000000'}, {'hostname': '*'}, {'tls_secret': '../bad'}])
def test_unresolved_or_unsafe_release_input_denied(change):
    values = config(); values.update(change)
    with pytest.raises(ValueError): module.render(**values)

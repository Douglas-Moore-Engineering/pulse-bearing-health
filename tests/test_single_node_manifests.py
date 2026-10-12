import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('single_node', Path(__file__).parents[1]/'scripts/render_single_node_manifests.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def config():
    return dict(image='pulse-api:sha256-'+'a'*64,
                tenant='00000000-0000-0000-0000-000000000001',
                audience='00000000-0000-0000-0000-000000000002',
                clients=['00000000-0000-0000-0000-000000000003'])


def test_single_writer_persistence_and_no_public_service():
    docs = module.render(**config())
    deployment = next(d['spec'] for d in docs if d['kind'] == 'Deployment')
    assert deployment['replicas'] == 1 and deployment['strategy']['type'] == 'Recreate'
    pod = deployment['template']['spec']
    assert pod['securityContext']['fsGroup'] == 10001
    assert pod['containers'][0]['imagePullPolicy'] == 'Never'
    assert pod['containers'][0]['securityContext']['readOnlyRootFilesystem']
    assert any(d['kind'] == 'PersistentVolumeClaim' for d in docs)
    assert next(d['spec']['type'] for d in docs if d['kind'] == 'Service') == 'ClusterIP'
    assert not any(d['kind'] in ['HorizontalPodAutoscaler', 'Gateway', 'Ingress'] for d in docs)


@pytest.mark.parametrize('change', [{'image': 'pulse-api:latest'}, {'clients': []}])
def test_unverified_release_inputs_rejected(change):
    params = config(); params.update(change)
    with pytest.raises(ValueError):
        module.render(**params)


def test_pilot_opt_in_uses_existing_backup_database():
    baseline = module.render(**config())
    enabled = module.render(**config(), pilot_components=True)
    before = next(d['data'] for d in baseline if d['kind'] == 'ConfigMap')
    after = next(d['data'] for d in enabled if d['kind'] == 'ConfigMap')
    assert 'PULSE_PILOT_COMPONENTS' not in before
    assert after['PULSE_PILOT_COMPONENTS'] == '1'
    assert after['PULSE_REVIEW_DB'] == '/data/assessments.db'
    assert after['PULSE_INTAKE_SCHEMA'] == '/app/contracts/vibration-window.schema.json'
    assert [d for d in enabled if d['kind'] != 'ConfigMap'] == [
        d for d in baseline if d['kind'] != 'ConfigMap']

"""Frozen retrospective RMS snapshot diagnostic; not warning-time validation."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    protocol_path = ROOT/'config/sca-case1-diagnostic-protocol.json'
    protocol = json.loads(protocol_path.read_text())
    freeze = json.loads((ROOT/'governance/evidence/sca-case1-protocol-freeze.json').read_text())
    assert sha(protocol_path) == freeze['protocol_sha256']
    inventory = json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
    case = next(r for r in inventory['files'] if r['case'] == '1')
    inputs, hashes = {}, {}
    for f in case['files']:
        path = ROOT/'outputs/reference-dataset-review/sca'/('case1-'+f['name'])
        assert sha(path) == f['sha256']
        inputs[f['name']] = loadmat(path, simplify_cells=True)
        hashes[f['name']] = sha(path)
    results = []
    for placement in protocol['placements']:
        train, test = (inputs[k][placement] for k in ['train.mat', 'test.mat'])
        for d in [train, test]:
            assert d['unit'] == 'm/s^2'
            assert np.isfinite(d['rawData']).all()
            assert all(len(d[k]) == len(d['rawData']) for k in ['label', 'time', 'RPM', 'samplingRate'])
        train_valid = (train['label'] == 0) & np.isfinite(train['RPM']) & (train['RPM'] > 0)
        reference = float(np.median(np.sqrt(np.mean(train['rawData'][train_valid]**2, axis=1))))
        assert np.isfinite(reference) and reference > 0
        valid = np.isin(test['label'], [0, 1, 2, 3]) & np.isfinite(test['RPM']) & (test['RPM'] > 0)
        positive = np.isin(test['label'], protocol['positive_labels'])
        ratio = np.sqrt(np.mean(test['rawData']**2, axis=1))/reference
        predicted = ratio > protocol['threshold_ratio']
        tp = int(np.sum(valid & positive & predicted))
        fn = int(np.sum(valid & positive & ~predicted))
        fp = int(np.sum(valid & ~positive & predicted))
        tn = int(np.sum(valid & ~positive & ~predicted))
        results.append({'placement': placement, 'reference_rms': reference,
            'reference_records': int(train_valid.sum()), 'excluded_test_records': int((~valid).sum()),
            'tp': tp, 'fn': fn, 'fp': fp, 'tn': tn,
            'fault_snapshot_recall': tp/(tp+fn) if tp+fn else None,
            'normal_snapshot_false_positive_rate': fp/(fp+tn) if fp+tn else None,
            'decisions': [{'time': str(t), 'label': int(l), 'eligible': bool(v), 'ratio': float(r), 'positive': bool(p) if v else None}
                          for t,l,v,r,p in zip(test['time'],test['label'],valid,ratio,predicted)]})
    report = {'scope': protocol['scope'], 'protocol_sha256': sha(protocol_path), 'code_sha256': sha(Path(__file__)),
        'input_sha256': hashes, 'qualified_detector': False, 'release_disposition': 'NOT_PROMOTED', 'results': results}
    (ROOT/'governance/evidence/sca-case1-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
    for r in results: print(json.dumps({k:v for k,v in r.items() if k != 'decisions'}))


if __name__ == '__main__':
    main()

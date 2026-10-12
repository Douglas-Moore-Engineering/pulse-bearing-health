"""Qualify SCA v2 case 1 schema/labels without fitting or testing a detector."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]


def main():
    inventory = json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
    case = next(r for r in inventory['files'] if r['case'] == '1')
    report = {'dataset': 'SCA v2', 'case': 1, 'scope': 'Schema and labels only; no detector performance measured',
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'files': []}
    for file in case['files']:
        path = ROOT/'outputs/reference-dataset-review/sca'/('case1-'+file['name'])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == file['sha256'] and path.stat().st_size == file['bytes']
        data = loadmat(path, simplify_cells=True)
        item = {'file': file['name'], 'sha256': digest, 'fromDate': data['fromDate'], 'toDate': data['toDate'],
                'faultOrigin': data['faultOrigin'], 'placements': []}
        for placement in ['DS', 'FS']:
            d = data[placement]
            raw = np.asarray(d['rawData'])
            labels, counts = np.unique(d['label'], return_counts=True)
            assert raw.ndim == 2
            assert all(len(d[k]) == len(raw) for k in ['samplingRate', 'RPM', 'time', 'label'])
            assert set(labels).issubset({-1, 0, 1, 2, 3})
            item['placements'].append({'placement': placement, 'shape': list(raw.shape), 'unit': d['unit'],
                'finite_raw': bool(np.isfinite(raw).all()),
                'sampling_rates': np.unique(d['samplingRate']).tolist(),
                'label_counts': {str(int(k)): int(v) for k,v in zip(labels,counts)},
                'time_first_native': str(d['time'][0]), 'time_last_native': str(d['time'][-1]),
                'rpm_range': [float(np.min(d['RPM'])), float(np.max(d['RPM']))]})
        report['files'].append(item)
    (ROOT/'governance/evidence/sca-case1-profile.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

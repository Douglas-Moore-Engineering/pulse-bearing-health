"""Prepare checksum-verified IMS run-2 feature replay; no raw signals are exported."""
import hashlib
import json
from pathlib import Path
import numpy as np

source = Path('outputs/reference-dataset-review/IMS-sample/2nd_test')
evidence = json.loads(Path('governance/evidence/ims-run2-baseline.json').read_text())
target = Path('outputs/reference-ims-replay.jsonl')
with target.open('x', encoding='utf-8') as stream:
    for index, member in enumerate(evidence['lineage']):
        if index < 100:
            continue  # Only monitoring windows; baseline was frozen offline.
        path = source/member['member']
        raw = path.read_bytes()
        checksum = hashlib.sha256(raw).hexdigest()
        if checksum != member['sha256']:
            raise ValueError('Native snapshot differs from the evaluated source')
        from io import BytesIO
        data = np.loadtxt(BytesIO(raw))
        if data.shape != (20480, 4) or not np.isfinite(data).all():
            raise ValueError('Unexpected source schema')
        payload = {'asset_id': 'ims-run2-bearing1-reference', 'window_id': f'ims2-{index:06d}',
            'source_timestamp': path.name, 'source_sha256': checksum,
            'dataset_id': 'DS-IMS', 'source_run': '2nd_test', 'amplitude_unit': 'native_unknown',
            'sample_count': 20480, 'sample_rate_hz': 20000,
            'rms_native': float(np.sqrt(np.mean(data[:, 0]*data[:, 0])))}
        stream.write(json.dumps(payload)+'\n')
print(json.dumps({'monitoring_windows': 884, 'raw_signals_exported': False,
                  'feature_replay_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))

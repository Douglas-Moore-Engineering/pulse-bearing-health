"""Frozen IMS experiment-level evaluation; native bytes stay in ignored storage."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from pulse.ims_baseline import evaluate


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('run', choices=['1st_test', '3rd_test'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    plan_path = Path('data/qualification/ims-independent-plan.json')
    plan = json.loads(plan_path.read_text())
    config, rule = plan['runs'][args.run], plan['rule']
    files = sorted(p for p in args.source.rglob('*') if p.is_file())
    if len(files) != config['snapshots']:
        raise ValueError(f"Expected {config['snapshots']} files; observed {len(files)}")
    features, lineage = [], []
    for i, path in enumerate(files):
        raw = path.read_bytes()
        from io import BytesIO
        data = np.loadtxt(BytesIO(raw))
        if data.shape != (20480, config['channels']) or not np.isfinite(data).all():
            raise ValueError(f'Invalid numerical schema: {path.name}')
        features.append(np.sqrt(np.mean(data*data, axis=0)))
        lineage.append({'member': path.relative_to(args.source).as_posix(),
                        'sha256': hashlib.sha256(raw).hexdigest()})
        if (i+1) % 500 == 0:
            print(f'{args.run}: validated {i+1} snapshots', flush=True)
    times = [p.name for p in files]
    array = np.asarray(features)
    summaries = []
    for offset in range(0, config['channels'], 4):
        batch = evaluate(times, array[:, offset:offset+4], rule['baseline_snapshots'],
                         rule['threshold_ratio'], rule['consecutive_snapshots'], rule['maximum_gap_seconds'])
        for channel in batch.pop('channels'):
            number = channel.pop('bearing')+offset
            channel['channel'] = number
            channel['bearing'] = (number+1)//2 if args.run == '1st_test' else number
            summaries.append(channel)
    report = {**batch, 'run': args.run, 'channels': summaries,
              'plan': plan, 'plan_sha256': sha(plan_path),
              'executed_at': datetime.now(timezone.utc).isoformat(),
              'code_sha256': {p.as_posix(): sha(p) for p in [Path('scripts/evaluate_ims_independent.py'), Path('src/pulse/ims_baseline.py')]},
              'environment': {'python': platform.python_version(), 'numpy': np.__version__},
              'lineage': lineage, 'qualified_detector': False,
              'units': 'unknown native amplitude', 'onset_labels_available': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('lineage', 'plan')}, indent=2))


if __name__ == '__main__':
    main()

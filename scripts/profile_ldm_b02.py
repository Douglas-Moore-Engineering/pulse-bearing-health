"""Profile the inspected native B02 sample without training or cloud access."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from pulse.ldm import profile_b02


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT/'data/qualification/ldm-upb-10868257.json').read_text(encoding='utf-8'))
    result = profile_b02(args.source_dir, manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'status': result['status'], 'channel_measurements': len(result['records']),
                      'training_qualified': False, 'timestamp_gap_seconds': result['timestamp_gap_seconds']}))

"""Record a local operator's disposition; no CMMS or equipment action."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from pulse.core import ReferenceStore


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--evidence-id', required=True)
    parser.add_argument('--actor', required=True)
    parser.add_argument('--disposition', choices=['approve', 'modify', 'reject'], required=True)
    parser.add_argument('--rationale', required=True)
    args = parser.parse_args()
    if not args.database.is_file():
        parser.error('An existing reference database is required')
    store = ReferenceStore(args.database, ROOT / 'data/contracts')
    try:
        print(json.dumps(store.decide(args.evidence_id, args.actor, args.disposition, args.rationale), indent=2))
    finally:
        store.close()

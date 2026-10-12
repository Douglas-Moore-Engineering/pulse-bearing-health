"""Reconcile a bounded, operator-supplied persisted-result inventory offline."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pulse.reconciliation import reconcile
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: reconcile_daily_fleet.py INPUT.json')
    with Path(sys.argv[1]).open('rb') as stream:data=stream.read(4*1024*1024+1)
    if len(data)>4*1024*1024:raise SystemExit('Inventory exceeds 4 MiB')
    print(json.dumps(reconcile(**json.loads(data)),indent=2))

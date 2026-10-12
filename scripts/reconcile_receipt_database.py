"""Read-only scoped receipt reconciliation; output may contain asset identifiers."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pulse.reconciliation import reconcile_database

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',required=True)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    with args.config.open('rb') as stream:raw=stream.read(65537)
    if len(raw)>65536:raise ValueError('Configuration exceeds 64 KiB')
    report=reconcile_database(args.database,**json.loads(raw))
    with args.output.open('x',encoding='utf-8') as stream:
        json.dump(report,stream,indent=2);stream.write('\n')
    print('Reconciliation written; no database changes')
if __name__=='__main__':main()

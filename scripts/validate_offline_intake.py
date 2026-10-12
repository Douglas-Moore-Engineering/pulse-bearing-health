"""Read-only validation; prints reason codes, never source samples/identifiers."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pulse.intake import validate_intake

def main():
    if len(sys.argv)!=2: raise SystemExit('Usage: python scripts/validate_offline_intake.py INPUT.json')
    with Path(sys.argv[1]).open('rb') as stream: payload=stream.read(32*1024*1024+1)
    if len(payload)>32*1024*1024:
        result={'status':'REJECTED','reasons':['FILE_TOO_LARGE']}
    else:
        try:
            def unique(pairs):
                d={}
                for k,v in pairs:
                    if k in d: raise ValueError('Duplicate key')
                    d[k]=v
                return d
            document=json.loads(payload,object_pairs_hook=unique)
            schema=json.loads((ROOT/'data/contracts/vibration-window.schema.json').read_text())
            result=validate_intake(document,schema)
        except (ValueError,RecursionError,OverflowError):
            result={'status':'REJECTED','reasons':['INVALID_JSON_OR_NUMERIC_VALUE']}
    print(json.dumps(result))
    return 2 if result['status']=='REJECTED' else 0

if __name__=='__main__':sys.exit(main())

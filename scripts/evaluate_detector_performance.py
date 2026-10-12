"""Evaluate a supplied detector evidence dossier without network or deployment."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pulse.performance_evaluator import evaluate

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('evidence',type=Path);args=p.parse_args()
 with args.evidence.open('rb') as stream:raw=stream.read(4*1024*1024+1)
 if len(raw)>4*1024*1024:raise ValueError('Evidence exceeds 4 MiB')
 def unique(pairs):
  result={}
  for k,v in pairs:
   if k in result:raise ValueError('Duplicate JSON key')
   result[k]=v
  return result
 evidence=json.loads(raw,object_pairs_hook=unique)
 policy=json.loads((ROOT/'config/detector-performance-requirements.json').read_text())
 result=evaluate(evidence,policy);print(json.dumps(result,indent=2))
 return {'PASS':0,'FAIL':1,'INCONCLUSIVE':2}[result['status']]
if __name__=='__main__':sys.exit(main())

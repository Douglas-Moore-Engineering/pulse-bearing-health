"""Audit consumed-case class/position/time confounding without fitting a model."""
import hashlib,json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from evaluate_sca_pairing import parse
ROOT=Path(__file__).resolve().parents[1]

def main():
 inventory=json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
 rows=[];hashes={}
 for case in ['1','2','11']:
  record=next(r for r in inventory['files'] if r['case']==case)
  for name in ['train.mat','test.mat']:
   expected=next(f['sha256'] for f in record['files'] if f['name']==name)
   p=ROOT/'outputs/reference-dataset-review/sca'/f'case{case}-{name}'
   actual=hashlib.sha256(p.read_bytes()).hexdigest()
   if actual!=expected:raise ValueError('Source hash mismatch')
   hashes[f'{case}/{name}']=actual;data=loadmat(p,simplify_cells=True)
   for side in ['DS','FS']:
    d=data[side]
    for label in sorted(set(map(int,d['label']))):
     indexes=[i for i,v in enumerate(d['label']) if int(v)==label]
     times=[parse(d['time'][i]) for i in indexes]
     speeds=[float(d['RPM'][i]) for i in indexes if np.isfinite(d['RPM'][i])]
     rows.append({'case':case,'file':name,'side':side,'label':label,'records':len(indexes),
       'first':min(times).isoformat(),'last':max(times).isoformat(),
       'rpm_min_max':[min(speeds),max(speeds)] if speeds else None})
 comparisons=[]
 for case in ['1','2','11']:
  for side in ['DS','FS']:
   group=[r for r in rows if r['case']==case and r['side']==side]
   normal=[r for r in group if r['label']==0];fault=[r for r in group if r['label']>0]
   comparisons.append({'case':case,'side':side,'both_classes_present':bool(normal and fault),
     'both_classes_in_publisher_test':bool(any(r['file']=='test.mat' for r in normal) and any(r['file']=='test.mat' for r in fault)),
     'all_normal_records_after_fault_records':bool(normal and fault and min(r['first'] for r in normal)>max(r['last'] for r in fault))})
 report={'scope':'Consumed-case label/position/time audit only','source_sha256':hashes,'groups':rows,'comparisons':comparisons,
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'reserved_cases_opened':False,
 'timezone_verified':False,'physical_bearing_identity_verified':False,'model_trained':False}
 (ROOT/'governance/evidence/sca-reference-feasibility.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(comparisons,indent=2))
if __name__=='__main__':main()

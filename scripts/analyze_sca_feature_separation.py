"""Recompute consumed-case scores without future pairing or opposite-side veto."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from evaluate_sca_spectral import feature
from evaluate_sca_pairing import parse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pulse.causal_observations import CausalObservations

def main():
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--feature-votes",type=int,choices=[1,2,3],default=1)
 args=parser.parse_args()
 inventory=json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
 frozen=json.loads((ROOT/'governance/evidence/sca-envelope-validation.json').read_text())
 spectral=json.loads((ROOT/'governance/evidence/sca-case1-spectral.json').read_text())
 paired=json.loads((ROOT/'governance/evidence/sca-paired-development.json').read_text())
 keys=['BPFIMultiple','BPFOMultiple','BPFMultiple'];results=[];sources={};observations=[]
 for case in ['1','2','11']:
  expected=next(f['sha256'] for r in inventory['files'] if r['case']==case for f in r['files'] if f['name']=='test.mat')
  path=ROOT/'outputs/reference-dataset-review/sca'/('case'+case+'-test.mat')
  assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
  sources[case]=expected;data=loadmat(path,simplify_cells=True);stream=[];counts={}
  for side in ['DS','FS']:
   thresholds=([next(r['threshold_train_99percentile'] for r in spectral['results'] if r['frequency_interpretation']=='documented_Hz_multiple' and r['placement']==side and r['feature']==k) for k in keys] if case=='1' else next(r['thresholds'] for r in frozen['results'] if r['case']==case and r['placement']==side))
   counts[side]=dict(tp=0,fn=0,fp=0,tn=0,abstain_fault=0,abstain_normal=0,excluded=0)
   d=data[side]
   for x,rpm,fs,label,t in zip(d['rawData'],d['RPM'],d['samplingRate'],d['label'],d['time']):
    if label==-1:counts[side]['excluded']+=1;continue
    values=[feature(x,fs,rpm/60*d['faultFrequencies'][k]) for k in keys] if rpm>0 else [None]
    score=sorted((v/threshold for v,threshold in zip(values,thresholds)),reverse=True)[args.feature_votes-1] if all(v is not None and np.isfinite(v) for v in values) else None
    stream.append((parse(t),side,score,int(label)))
    if score is not None:observations.append({'case':case,'side':side,'fault':bool(label>0),'rpm':float(rpm),'scores':[float(v/threshold) for v,threshold in zip(values,thresholds)]})
  stream.sort(key=lambda r:(r[0],r[1]));state=CausalObservations();origin=stream[0][0]
  for t,side,score,label in stream:
   decision=state.update(side,(t-origin).total_seconds(),score)['anomaly']
   key=('abstain_fault' if label>0 else 'abstain_normal') if decision is None else (('tp' if decision else 'fn') if label>0 else ('fp' if decision else 'tn'))
   counts[side][key]+=1
  for side,c in counts.items():
   eligible=sum(v for k,v in c.items() if k!='excluded');abstain=c['abstain_fault']+c['abstain_normal']
   row={'case':case,'placement':side,**c,'eligible':eligible,'coverage':(eligible-abstain)/eligible,'paired_comparator':next(r for r in paired['results'] if r['case']==case and r['placement']==side)}
   results.append(row);print(json.dumps(row))

 summaries=[];tradeoffs=[]
 for case in ['1','2','11']:
  records=[r for r in observations if r['case']==case]
  for k,name in enumerate(keys+['OR_max']):
   def score(r):return r['scores'][k] if k<3 else max(r['scores'])
   for side in ['DS','FS']:
    for fault in [False,True]:
     group=[r for r in records if r['side']==side and r['fault']==fault]
     if group:
      summaries.append({'case':case,'side':side,'fault':fault,'feature':name,'count':len(group),
       'score_p10_p50_p90':list(map(float,np.quantile([score(r) for r in group],[.1,.5,.9]))),
       'rpm_min_max':[min(r['rpm'] for r in group),max(r['rpm'] for r in group)]})
   for threshold in [0.5,1,1.5,2,3,5,10]:
    positive=[score(r)>threshold for r in records]
    tp=sum(p and r['fault'] for p,r in zip(positive,records));fp=sum(p and not r['fault'] for p,r in zip(positive,records))
    faults=sum(r['fault'] for r in records);normal=len(records)-faults
    tradeoffs.append({'case':case,'feature':name,'threshold_multiplier':threshold,'tp':tp,'fn':faults-tp,'fp':fp,'tn':normal-fp,
      'snapshot_recall':tp/faults if faults else None,'snapshot_false_positive_rate':fp/normal if normal else None})
 report={'scope':'Consumed-case exploratory feature separation; no selected threshold',
 'limitations':['Fault status is confounded with sensor side in cases 1/2','Existing reference calibration is retrospective','Load metadata not evaluated','No independent events or operating exposure inferred'],
 'source_sha256':sources,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'summaries':summaries,'tradeoffs':tradeoffs,'qualified_detector':False,'reserved_cases_opened':False}
 (ROOT/'governance/evidence/sca-feature-separation.json').write_text(json.dumps(report,indent=2)+'\n')
 for r in tradeoffs:
  if r['feature']=='OR_max' and r['case'] in ['1','2']:print(json.dumps(r))
if __name__=='__main__':main()

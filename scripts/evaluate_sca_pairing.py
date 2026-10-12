"""Consumed-case paired localization experiment; unmatched records abstain."""
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from evaluate_sca_spectral import feature

ROOT=Path(__file__).resolve().parents[1]

def parse(value):
    value=str(value).strip().replace('Z','+00:00')
    return datetime.fromisoformat(re.sub(r'\.(\d+)',lambda m:'.'+m.group(1).ljust(6,'0'),value))

def main():
    inventory=json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
    frozen=json.loads((ROOT/'governance/evidence/sca-envelope-validation.json').read_text())
    spectral=json.loads((ROOT/'governance/evidence/sca-case1-spectral.json').read_text())
    for side in ['DS','FS']:
        thresholds=[next(r['threshold_train_99percentile'] for r in spectral['results'] if r['frequency_interpretation']=='documented_Hz_multiple' and r['placement']==side and r['feature']==key) for key in ['BPFIMultiple','BPFOMultiple','BPFMultiple']]
        frozen['results'].append({'case':'1','placement':side,'thresholds':thresholds})
    report={'scope':'Post-hoc paired development on consumed cases 1/2/11; no independent validation',
      'rule':'Mutual nearest within 60 seconds; positive only when max threshold-normalized feature exceeds 1 and is greater than opposite-side score; ties negative; unmatched abstain',
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':[]}
    for case in ['1','2','11']:
        source=next(r for r in inventory['files'] if r['case']==case)
        f=next(f for f in source['files'] if f['name']=='test.mat')
        p=ROOT/'outputs/reference-dataset-review/sca'/('case'+case+'-test.mat')
        assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
        data=loadmat(p,simplify_cells=True); scores={}; times={}
        for side in ['DS','FS']:
            d=data[side];thresholds=next(r['thresholds'] for r in frozen['results'] if r['case']==case and r['placement']==side)
            times[side]=[parse(t) for t in d['time']];scores[side]=[]
            for x,rpm,fs,label in zip(d['rawData'],d['RPM'],d['samplingRate'],d['label']):
                values=[feature(x,fs,rpm/60*d['faultFrequencies'][key]) for key in ['BPFIMultiple','BPFOMultiple','BPFMultiple']] if label!=-1 and rpm>0 else [None]
                scores[side].append(max(v/t for v,t in zip(values,thresholds)) if all(v is not None and np.isfinite(v) for v in values) else None)
        distance=np.array([[abs((a-b).total_seconds()) for b in times['FS']] for a in times['DS']])
        forward=distance.argmin(axis=1);reverse=distance.argmin(axis=0)
        pairs=[(i,int(j)) for i,j in enumerate(forward) if reverse[j]==i and distance[i,j]<=60 and scores['DS'][i] is not None and scores['FS'][j] is not None]
        for side in ['DS','FS']:
            mapped={i:j for i,j in pairs} if side=='DS' else {j:i for i,j in pairs}
            opposite='FS' if side=='DS' else 'DS';counts=dict(tp=0,fn=0,fp=0,tn=0,abstain_fault=0,abstain_normal=0,excluded=0)
            for i,label in enumerate(data[side]['label']):
                if label==-1:counts['excluded']+=1;continue
                if i not in mapped:counts['abstain_fault' if label>0 else 'abstain_normal']+=1;continue
                positive=scores[side][i]>1 and scores[side][i]>scores[opposite][mapped[i]]
                counts[('tp' if positive else 'fn') if label>0 else ('fp' if positive else 'tn')]+=1
            baseline=next(r for r in frozen['results'] if r['case']==case and r['placement']==side)
            original={str(r['time']).strip():r['positive'] for r in baseline.get('decisions',[])}
            baseline_counts=dict(tp=0,fn=0,fp=0,tn=0)
            for i in mapped:
                label=int(data[side]['label'][i]);positive=original.get(str(data[side]['time'][i]).strip(),scores[side][i]>1)
                baseline_counts[('tp' if positive else 'fn') if label>0 else ('fp' if positive else 'tn')]+=1
            result={'case':case,'placement':side,'total':len(data[side]['label']),'paired':len(mapped),**counts,'original_on_same_pairs':baseline_counts}
            report['results'].append(result);print(json.dumps(result))
    (ROOT/'governance/evidence/sca-paired-development.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()

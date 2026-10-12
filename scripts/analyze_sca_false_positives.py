"""Consumed-case attribution; does not modify the frozen detector."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from evaluate_sca_spectral import feature

ROOT = Path(__file__).resolve().parents[1]

def main():
    prior = json.loads((ROOT/'governance/evidence/sca-envelope-validation.json').read_text())
    inventory = json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
    names = ['BPFIMultiple','BPFOMultiple','BPFMultiple']
    results=[]
    for case in ['2','11']:
        record=next(r for r in inventory['files'] if r['case']==case)
        inputs={}
        for f in record['files']:
            p=ROOT/'outputs/reference-dataset-review/sca'/('case'+case+'-'+f['name'])
            assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
            inputs[f['name']]=loadmat(p,simplify_cells=True)
        for frozen in [r for r in prior['results'] if r['case']==case]:
            placement=frozen['placement']; train=inputs['train.mat'][placement]; test=inputs['test.mat'][placement]
            refspeed=np.asarray(train['RPM'])[(train['label']==0)&(train['RPM']>0)]
            lower,upper=float(refspeed.min()),float(refspeed.max())
            patterns={}; rows=[]
            for x,fs,rpm,label,time in zip(test['rawData'],test['samplingRate'],test['RPM'],test['label'],test['time']):
                if label==-1 or rpm<=0: continue
                scores=[feature(x,fs,rpm/60*test['faultFrequencies'][f]) for f in names]
                if any(s is None for s in scores): continue
                fired=[name for name,s,t in zip(names,scores,frozen['thresholds']) if s>t]
                normal=label==0
                if normal and fired:
                    key='+'.join(fired); patterns[key]=patterns.get(key,0)+1
                rows.append({'normal':bool(normal),'positive':bool(fired),'outside_reference_speed':bool(rpm<lower or rpm>upper),'rpm':float(rpm),'time':str(time),'fired':fired})
            fp=[r for r in rows if r['normal'] and r['positive']]
            tn=[r for r in rows if r['normal'] and not r['positive']]
            assert len(fp)==frozen['fp'] and len(tn)==frozen['tn']
            results.append({'case':case,'placement':placement,'reference_rpm_range':[lower,upper],
                'false_positive_patterns':patterns,'false_positives':len(fp),
                'false_positives_outside_reference_speed':sum(r['outside_reference_speed'] for r in fp),
                'true_negatives_outside_reference_speed':sum(r['outside_reference_speed'] for r in tn),
                'false_positive_rpm_range':[min(r['rpm'] for r in fp),max(r['rpm'] for r in fp)] if fp else None,
                'first_false_positive':fp[0]['time'] if fp else None,'last_false_positive':fp[-1]['time'] if fp else None})
    report={'scope':'Consumed-case diagnostic attribution; no causal or independent validation claim',
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':results}
    (ROOT/'governance/evidence/sca-false-positive-analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()

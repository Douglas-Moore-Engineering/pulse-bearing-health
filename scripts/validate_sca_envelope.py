"""Frozen multi-feature SCA diagnostic validation, including explicit abstention."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from evaluate_sca_spectral import feature

ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    config_path = ROOT/'config/sca-envelope-validation.json'
    policy = json.loads(config_path.read_text())
    freeze = json.loads((ROOT/'governance/evidence/sca-envelope-validation-freeze.json').read_text())
    for name, digest in freeze['hashes'].items():
        if sha(ROOT/name) != digest: raise ValueError('Frozen file changed: '+name)
    inventory = json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
    report = {'scope':policy['scope'],'qualified_detector':False,'frequency_units_physically_verified':False,
              'protocol_sha256':sha(config_path),'results':[]}
    for case in policy['cases']:
        record = next(r for r in inventory['files'] if r['case']==case)
        inputs = {}
        for f in record['files']:
            p = ROOT/'outputs/reference-dataset-review/sca'/('case'+case+'-'+f['name'])
            if sha(p) != f['sha256']: raise ValueError('Input hash mismatch')
            inputs[f['name']] = loadmat(p,simplify_cells=True)
        train, test = inputs['train.mat'],inputs['test.mat']
        for placement,d in test.items():
            if not isinstance(d,dict) or 'rawData' not in d: continue
            def observations(data):
                if not all(len(data[k])==len(data['rawData']) for k in ['RPM','label','samplingRate','time']):
                    raise ValueError('Unaligned records')
                for x,rpm,fs,label,time in zip(data['rawData'],data['RPM'],data['samplingRate'],data['label'],data['time']):
                    if label not in [-1,0,1,2,3]: raise ValueError('Unknown label')
                    valid = label!=-1 and np.isfinite(rpm) and rpm>0 and np.isfinite(fs) and fs>0 and np.isfinite(x).all()
                    scores = [feature(x,fs,rpm/policy['frequency_divisor']*data['faultFrequencies'][f]) for f in policy['features']] if valid else None
                    yield int(label),str(time),scores
            reference = list(observations(train[placement]))
            normal = [s for l,t,s in reference if l==0 and s is not None and all(v is not None and np.isfinite(v) for v in s)]
            thresholds = np.quantile(normal,policy['normal_quantile'],axis=0) if len(normal)>=policy['minimum_reference_records'] else None
            counts = dict(tp=0,fn=0,fp=0,tn=0,excluded=0,abstain_fault=0,abstain_normal=0)
            decisions=[]
            for label,time,scores in observations(d):
                prediction=None
                if scores is None: counts['excluded']+=1
                elif thresholds is None or any(s is None or not np.isfinite(s) for s in scores): counts['abstain_fault' if label>0 else 'abstain_normal']+=1
                else:
                    prediction=bool(np.any(np.array(scores)>thresholds))
                    counts[('tp' if prediction else 'fn') if label>0 else ('fp' if prediction else 'tn')]+=1
                decisions.append({'time':time,'label':label,'positive':prediction})
            result={'case':case,'placement':placement,'unit':d['unit'],'reference_records':len(normal),
                    'thresholds':thresholds.tolist() if thresholds is not None else None,**counts,'decisions':decisions}
            report['results'].append(result)
            print(json.dumps({k:v for k,v in result.items() if k!='decisions'}),flush=True)
    (ROOT/'governance/evidence/sca-envelope-validation.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__': main()

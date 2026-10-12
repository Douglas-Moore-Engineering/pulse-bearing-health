"""Decompose envelope contrast on consumed case 2; no detector modification."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import hilbert

ROOT=Path(__file__).resolve().parents[1]

def summary(values):
    return dict(zip(['p10','median','p90'],map(float,np.quantile(values,[.1,.5,.9])))) if values else None

def main():
    inv=json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
    case=next(r for r in inv['files'] if r['case']=='2')
    frozen=json.loads((ROOT/'governance/evidence/sca-envelope-validation.json').read_text())
    results=[]
    for f in case['files']:
        path=ROOT/'outputs/reference-dataset-review/sca'/('case2-'+f['name'])
        assert hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256']
        data=loadmat(path,simplify_cells=True)
        for side in ['DS','FS']:
            d=data[side]; groups={}
            prior=next(r for r in frozen['results'] if r['case']=='2' and r['placement']==side)
            decisions={r['time']:r['positive'] for r in prior['decisions']}
            for x,rpm,fs,label,time in zip(d['rawData'],d['RPM'],d['samplingRate'],d['label'],d['time']):
                if label==-1 or rpm<=0:continue
                group='reference_normal' if f['name']=='train.mat' else ('fault' if label>0 else 'normal')+('_positive' if decisions[str(time)] else '_negative')
                g=groups.setdefault(group,{'rms':[],'signal':[],'background':[],'contrast':[]})
                g['rms'].append(float(np.sqrt(np.mean(x*x))))
                envelope=np.abs(hilbert(x-x.mean())); window=np.hanning(len(x))
                power=np.abs(np.fft.rfft((envelope-envelope.mean())*window))**2/np.sum(window)**2
                freq=np.fft.rfftfreq(len(x),1/fs); target=rpm/60*d['faultFrequencies']['BPFOMultiple']
                signal=[];background=[];contrast=[]
                for h in [1,2,3]:
                    center=target*h;width=max(2*fs/len(x),center*.02)
                    if center+4*width>=fs/2:continue
                    a=power[np.abs(freq-center)<=width].mean()
                    b=power[(np.abs(freq-center)>2*width)&(np.abs(freq-center)<=4*width)].mean()
                    signal.append(float(a));background.append(float(b));contrast.append(float(a/max(b,np.finfo(float).tiny)))
                g['signal'].append(float(np.mean(signal)));g['background'].append(float(np.mean(background)));g['contrast'].append(float(np.mean(contrast)))
            for group,g in groups.items():results.append({'file':f['name'],'placement':side,'group':group,'records':len(g['rms']),**{k:summary(v) for k,v in g.items()}})
    report={'scope':'Case 2 consumed-data descriptive shift analysis; not causal attribution',
      'feature':'Outer-ring envelope feature; power normalized by squared window sum; mean harmonic contrast retained',
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':results}
    (ROOT/'governance/evidence/sca-spectral-shift.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

"""Timestamp-only feasibility audit; never infer simultaneous vibration."""
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
import numpy as np
from scipy.io import loadmat

ROOT=Path(__file__).resolve().parents[1]

def main():
    results=[]
    inventory=json.loads((ROOT/'data/qualification/sca-source-inventory.json').read_text())
    for case in ['1','2','11']:
        record=next(r for r in inventory['files'] if r['case']==case)
        for f in record['files']:
            p=ROOT/'outputs/reference-dataset-review/sca'/('case'+case+'-'+f['name'])
            assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
            d=loadmat(p,simplify_cells=True)
            def parse(t):
                value=str(t).strip().replace('Z','+00:00')
                value=re.sub(r'\.(\d+)',lambda m: '.'+m.group(1).ljust(6,'0'),value)
                return datetime.fromisoformat(value)
            stamps=[[parse(t) for t in d[side]['time']] for side in ['DS','FS']]
            aware={t.tzinfo is not None for times in stamps for t in times}
            if len(aware)!=1: raise ValueError('Mixed timezone-aware and naive timestamps')
            epoch=stamps[0][0]
            a,b=[np.array([(t-epoch).total_seconds() for t in times]) for times in stamps]
            distance=np.abs(a[:,None]-b[None,:]); nearest=distance.argmin(axis=1)
            reverse=distance.argmin(axis=0)
            mutual=[(i,int(j),float(distance[i,j])) for i,j in enumerate(nearest) if reverse[j]==i]
            results.append({'case':case,'file':f['name'],'native_id':int(d['id']),
                'asset_description':d['assetDescription'],'fault_origin':d['faultOrigin'],
                'bearing_DS':d['DS']['assetName'],'bearing_FS':d['FS']['assetName'],
                'frequency_multiples_DS':d['DS']['faultFrequencies'],'frequency_multiples_FS':d['FS']['faultFrequencies'],
                'records_DS':len(a),'records_FS':len(b),'mutual_nearest_pairs':len(mutual),
                'pairs_within_seconds':{str(t):sum(delta<=t for i,j,delta in mutual) for t in [1,60,300,3600]},
                'median_mutual_separation_seconds':float(np.median([v[2] for v in mutual])),
                'timezone':'Explicit offset parsed' if True in aware else 'Unspecified; same-clock assumption only'})
    report={'scope':'Consumed-case metadata and timing only; no new detector score', 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':results}
    (ROOT/'governance/evidence/sca-pairing-profile.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

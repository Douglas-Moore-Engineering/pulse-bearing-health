"""Replay frozen binary decisions as causal context, not recomputed features."""
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime
from evaluate_sca_pairing import parse

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pulse.causal_observations import CausalObservations

def main():
    source=ROOT/'governance/evidence/sca-envelope-validation.json'
    data=json.loads(source.read_text());results=[]
    for case in ['2','11']:
        state=CausalObservations();stream=[];counts={}
        for row in data['results']:
            if row['case']!=case:continue
            side=row['placement'];counts[side]=dict(total=0,positive=0,partner_available=0,both_anomalous=0)
            for d in row['decisions']:
                stream.append((parse(d['time']),side,d['positive']))
        stream.sort(key=lambda r:(r[0],r[1]))
        origin=stream[0][0]
        for time,side,positive in stream:
            # Binary encoding preserves only the original threshold decision.
            score=None if positive is None else 2.0 if positive else 0.0
            output=state.update(side,(time-origin).total_seconds(),score)
            assert output['anomaly']==positive
            counts[side]['total']+=1
            counts[side]['positive']+=int(output['anomaly'] is True)
            counts[side]['partner_available']+=int(output['partner_available'])
            counts[side]['both_anomalous']+=int(output['both_anomalous'])
        for side,values in counts.items():results.append({'case':case,'placement':side,**values})
    report={'scope':'Causal context replay of frozen binary decisions; no new detector or accuracy improvement',
            'equal_timestamp_order':'DS before FS, deterministic replay convention not acquisition-order evidence',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'component_sha256':hashlib.sha256((ROOT/'src/pulse/causal_observations.py').read_bytes()).hexdigest(),
            'all_decisions_preserved':True,'results':results}
    (ROOT/'governance/evidence/sca-causal-replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

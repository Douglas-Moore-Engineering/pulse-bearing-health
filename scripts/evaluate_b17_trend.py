"""Replay consumed B17 features under prewritten fixed development settings."""
import hashlib,json,sys,statistics
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from pulse.trailing_median import TrailingMedian
p=ROOT/'config/b17-trend-development.json';cfg=json.loads(p.read_text())
src=ROOT/'governance/evidence/ldm-B17-rms-v2-final.json';d=json.loads(src.read_text())
rows=d['native_features'];reference=[r for r in rows if r['eligible']][:cfg['reference_records']]
refs=[statistics.median(r['rms'][i] for r in reference) for i in [0,1]]
assert refs==d['reference_rms']
s=TrailingMedian(refs,cfg['trailing_records'],cfg['threshold_ratio'],cfg['consecutive_records'],cfg['maximum_gap_seconds'])
origin=datetime.fromisoformat(reference[-1]['timestamp']);outputs=[];episodes=0;prior=False
for r in rows:
 if r['timestamp']<=reference[-1]['timestamp']:continue
 if not r['eligible']:raise ValueError('Protocol requires contiguous eligible B17 monitoring')
 o=s.update((datetime.fromisoformat(r['timestamp'])-origin).total_seconds(),r['rms'])
 if o['flagged'] and not prior:episodes+=1
 prior=o['flagged'] is True;outputs.append(dict(identity=r['identity'],timestamp=r['timestamp'],**o))
first=next((r['timestamp'] for r in outputs if r['flagged']),None)
report={'candidate':cfg['candidate'],'config_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'component_sha256':hashlib.sha256((ROOT/'src/pulse/trailing_median.py').read_bytes()).hexdigest(),'monitoring_records':len(outputs),'available_records':sum(r['available'] for r in outputs),'flagged_records':sum(r['flagged'] is True for r in outputs),'episodes':episodes,'first_flag':first,'record_end_lead_minutes':(datetime.fromisoformat(outputs[-1]['timestamp'])-datetime.fromisoformat(first)).total_seconds()/60 if first else None,'baseline':{k:d[k] for k in ['flagged_records','bearing_alert_episodes','descriptive_lead_minutes']},'qualified_detector':False,'decisions':outputs}
(ROOT/'governance/evidence/b17-trend-development.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='decisions'},indent=2))

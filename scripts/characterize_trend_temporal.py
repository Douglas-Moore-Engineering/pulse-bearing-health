"""Synthetic temporal characterization of the unchanged development detector."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from pulse.trailing_median import TrailingMedian
cfgpath=ROOT/'config/b17-trend-development.json';cfg=json.loads(cfgpath.read_text())
def replay(values):
 s=TrailingMedian([1],cfg['trailing_records'],cfg['threshold_ratio'],cfg['consecutive_records'],cfg['maximum_gap_seconds'])
 return [s.update(i,[v]) for i,v in enumerate(values)]
rows=[]
for length in [1,3,7,8,20]:
 values=[1]*20+[2]*length+[1]*30;out=replay(values);flags=[i for i,r in enumerate(out) if r['flagged']]
 rows.append({'high_pulse_records':length,'first_high_index':20,'last_high_index':19+length,
 'first_flag_index':flags[0] if flags else None,'last_flag_index':flags[-1] if flags else None,
 'first_clear_index':flags[-1]+1 if flags else None,
 'alarm_after_pulse_ended':bool(flags and flags[0]>19+length)})
report={'scope':'Synthetic temporal tests; unit-spaced observations, not field warning metrics','results':rows,
 'config_sha256':hashlib.sha256(cfgpath.read_bytes()).hexdigest(),
 'component_sha256':hashlib.sha256((ROOT/'src/pulse/trailing_median.py').read_bytes()).hexdigest(),
 'qualified_detector':False,'parameters_changed':False,
 'limitations':['No automatic clearance of a maintenance incident is authorized by a false detector flag','Unavailable after a gap does not mean healthy','Record delay cannot be converted into minutes without acquisition cadence']}
(ROOT/'governance/evidence/trend-temporal-characterization.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(rows,indent=2))

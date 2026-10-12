"""Audit chronology from consumed recorded feature inventories, without raw access."""
import hashlib,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 results=[]
 for name in ['ldm_b04-rms-v2-validation.json','ldm-B12-rms-v2-final.json','ldm-B17-rms-v2-final.json']:
  p=ROOT/'governance/evidence'/name;d=json.loads(p.read_text());rows=d['native_features']
  assert all(a['timestamp']<b['timestamp'] for a,b in zip(rows,rows[1:]))
  eligible=[r for r in rows if r['eligible']];n=d['reference_records'];reference=eligible[:n];monitor=eligible[n:]
  assert reference[-1]['timestamp']<monitor[0]['timestamp']
  median=[statistics.median(r['rms'][i] for r in reference) for i in [0,1]]
  assert all(abs(a-b)<1e-10 for a,b in zip(median,d['reference_rms']))
  def conditions(r):return (r['set_speed_rpm'],r['set_dynamic_load_N'])
  ref_conditions=set(map(conditions,reference))
  results.append({'source':name,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
   'reference_count':n,'monitoring_count':len(monitor),'reference_start':reference[0]['timestamp'],
   'reference_end':reference[-1]['timestamp'],'monitoring_start':monitor[0]['timestamp'],
   'baseline_median_reproduced':True,'baseline_precedes_monitoring':True,
   'reference_setpoint_ranges':[[min(c[i] for c in ref_conditions),max(c[i] for c in ref_conditions)] for i in [0,1]],
   'exact_reference_setpoint_pair_count':len(ref_conditions),
   'monitoring_unseen_setpoint_records':sum(conditions(r) not in ref_conditions for r in monitor),
   'early_reference_verified_healthy':False,'physical_failure_endpoint_verified':False})
 ims_path=ROOT/'governance/evidence/ims-run1-independent.json';ims=json.loads(ims_path.read_text())
 report={'scope':'Consumed recorded evidence audit; no training or holdout access','ldm':results,
 'ims':{'source_sha256':hashlib.sha256(ims_path.read_bytes()).hexdigest(),'baseline_snapshots':ims['baseline_snapshots'],
 'monitoring_snapshots':ims['monitoring_snapshots'],'gaps_above_limit':ims['gaps_above_limit'],
 'chronology_basis':'Existing executed report and first-100 baseline protocol; native inventory not replayed in this audit',
 'verified_healthy_reference':False,'physical_endpoint_timing_verified':False},
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'production_release_authorized':False}
 (ROOT/'governance/evidence/chronological-reference-audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps([{'source':r['source'],'chronology_passed':r['baseline_precedes_monitoring'],'median_reproduced':r['baseline_median_reproduced']} for r in results]))
if __name__=='__main__':main()

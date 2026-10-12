"""Consolidate recorded results only; never open reserved data or invent labels."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pulse.performance_evaluator import evaluate

def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def main():
 policy_path='config/detector-performance-requirements.json'
 policy=json.loads((ROOT/policy_path).read_text())
 base={'policy_version':policy['version'],'events':[],'healthy_blocks':[], 'regimes':[],
       'evidence_review':{'satisfied':None,'references':[]},
       'limitations':['No verified 720-hour healthy exposure blocks','No sufficient independent event timing dossier','No independent acceptance review']}
 ims_path='governance/evidence/ims-run1-independent.json'
 ims=json.loads((ROOT/ims_path).read_text())
 rms=dict(base,candidate='frozen-3x-rms',source_observations={
     'documented_damaged_bearings':[3,4],
     'bearing4_flagged_snapshots':sum(c['flagged_snapshots'] for c in ims['channels'] if c['bearing']==4),
     'bearing3_record_end_lead_minutes':10,
     'record_end_is_not_verified_failure_endpoint':True,
     'clock_timezone_unqualified':True},
     source_files={ims_path:digest(ims_path),'data/qualification/ims-independent-results.md':digest('data/qualification/ims-independent-results.md')})
 paired_path='governance/evidence/sca-paired-development.json'
 paired=json.loads((ROOT/paired_path).read_text())
 sca=dict(base,candidate='sca-paired-development',regimes=[
     {'regime':r['case']+'/'+r['placement'],'eligible':r['total']-r['excluded'],
      'abstentions':r['abstain_fault']+r['abstain_normal'],'excluded':r['excluded'],
      'inventory_reference':paired_path} for r in paired['results']],
     independent_causal_protocol={'satisfied':False,'references':['data/qualification/detector-candidate-disposition.md'],'reason':'Post-hoc consumed-case development; future-neighbour pairing and retrospective calibration'},
     source_files={paired_path:digest(paired_path),'data/qualification/detector-candidate-disposition.md':digest('data/qualification/detector-candidate-disposition.md')})
 out=ROOT/'data/qualification/performance-dossiers';out.mkdir(exist_ok=True)
 reports={}
 for dossier in [rms,sca]:
  name=dossier['candidate'];path=out/(name+'.json')
  path.write_text(json.dumps(dossier,indent=2)+'\n')
  reports[name]={'dossier_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'evaluation':evaluate(dossier,policy)}
 result={'policy_sha256':digest(policy_path),'evaluator_sha256':digest('src/pulse/performance_evaluator.py'),
         'scope':'Retrospective evaluation of supplied recorded evidence; not a newly frozen holdout test',
         'reserved_cases_opened':False,'candidate_results':reports,'production_release_authorized':False}
 (ROOT/'governance/evidence/detector-performance-consolidated.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({name:r['evaluation']['status'] for name,r in reports.items()}))
if __name__=='__main__':main()

import json
from pathlib import Path
import pytest
from pulse.performance_evaluator import evaluate
POLICY=json.loads((Path(__file__).parents[1]/'config/detector-performance-requirements.json').read_text())

def fixture():
 return {'policy_version':POLICY['version'],
 'events':[dict(event_id=str(i),alert='2026-01-01T00:00:00+00:00',earliest='2026-01-01T01:00:00+00:00',latest='2026-01-01T01:01:00+00:00',endpoint_reference='fixture',clock_reference='fixture') for i in range(20)],
 'healthy_blocks':[dict(bearing_id=str(i),block_index=0,operating_hours=720,nuisance_episodes=0,unresolved_episodes=1,exposure_reference='fixture') for i in range(3)],
 'regimes':[dict(eligible=100,abstentions=5,inventory_reference='fixture')],
 **{k:dict(satisfied=True,references=['synthetic assertion']) for k in ['unsupported_challenges','independent_causal_protocol','trace_replay','evidence_review']}}

def test_synthetic_pass_never_authorizes_release():
 r=evaluate(fixture(),POLICY);assert r['status']=='PASS';assert not r['production_release_authorized']

def test_missing_evidence_cannot_pass():
 assert evaluate({'policy_version':POLICY['version']},POLICY)['status']=='INCONCLUSIVE'

@pytest.mark.parametrize('case',['miss','late','nuisance','coverage','protocol'])
def test_failure_cases(case):
 d=fixture()
 if case=='miss':d['events'][0]['alert']=None
 if case=='late':d['events'][0]['alert']='2026-01-01T00:41:00+00:00'
 if case=='nuisance':d['healthy_blocks'][0]['unresolved_episodes']=2
 if case=='coverage':d['regimes'][0]['abstentions']=6
 if case=='protocol':d['independent_causal_protocol']['satisfied']=False
 assert evaluate(d,POLICY)['status']=='FAIL'

@pytest.mark.parametrize('case',['short','endpoint','review','event_count'])
def test_inconclusive_cases(case):
 d=fixture()
 if case=='short':d['healthy_blocks'][0]['operating_hours']=719
 if case=='endpoint':d['events'][0]['endpoint_reference']=None
 if case=='review':d.pop('evidence_review')
 if case=='event_count':d['events'].pop()
 assert evaluate(d,POLICY)['status']=='INCONCLUSIVE'

def test_duplicate_events_rejected():
 d=fixture();d['events'][1]['event_id']='0'
 with pytest.raises(ValueError):evaluate(d,POLICY)

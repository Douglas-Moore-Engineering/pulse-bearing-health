"""Offline acceptance arithmetic on supplied evidence; never release authorization."""
from datetime import datetime
from .detector_acceptance import warning_result


def aggregate(statuses):
    if 'FAIL' in statuses:return 'FAIL'
    if not statuses or 'INCONCLUSIVE' in statuses:return 'INCONCLUSIVE'
    return 'PASS'


def count(value):
    if type(value) is not int or value < 0:raise ValueError('Nonnegative integer required')
    return value


def evaluate(evidence, policy):
    if evidence.get('policy_version') != policy['version']:
        raise ValueError('Evidence must bind the exact policy version')
    def attestation(name):
        record=evidence.get(name,{})
        if record.get('satisfied') is False:return 'FAIL'
        return 'PASS' if record.get('satisfied') is True and record.get('references') else 'INCONCLUSIVE'
    events=evidence.get('events',[])
    identities=[e['event_id'] for e in events]
    if any(not isinstance(v,str) or not v.strip() for v in identities) or len(set(identities))!=len(identities):
        raise ValueError('Unique nonblank event identifiers required')
    warning=[]
    for event in events:
        if not event.get('endpoint_reference') or not event.get('clock_reference'):
            warning.append('INCONCLUSIVE');continue
        for field in ['alert','earliest','latest']:
            if event.get(field) is not None:
                d=datetime.fromisoformat(event[field])
                if d.tzinfo is None:raise ValueError('Offset-aware event timestamps required')
        warning.append(warning_result(event.get('alert'),event.get('earliest'),event.get('latest'),policy['warning_target_minutes'])['status'])
    sufficient_events=len(events)>=policy['minimum_independent_failure_events']
    event_status=aggregate(warning+([] if sufficient_events else ['INCONCLUSIVE']))
    blocks=evidence.get('healthy_blocks',[])
    nuisance=[];bearings=set();seen=set()
    for block in blocks:
        key=(block['bearing_id'],count(block['block_index']))
        if not key[0] or key in seen:raise ValueError('Unique healthy exposure blocks required')
        seen.add(key)
        hours=block['operating_hours']
        if type(hours) not in (int,float) or not 0<=hours<=720:raise ValueError('Exposure block must contain 0..720 operating hours')
        episodes=count(block['nuisance_episodes'])+count(block['unresolved_episodes'])
        if hours != 720 or not block.get('exposure_reference'):
            nuisance.append('INCONCLUSIVE');continue
        bearings.add(key[0])
        nuisance.append('PASS' if episodes<=policy['nuisance_alert_limit_per_bearing_720_operating_hours'] else 'FAIL')
    nuisance_status=aggregate(nuisance+([] if len(bearings)>=policy['minimum_healthy_bearings'] else ['INCONCLUSIVE']))
    coverage=[]
    for regime in evidence.get('regimes',[]):
        total=count(regime['eligible']);abstentions=count(regime['abstentions'])
        if abstentions>total:raise ValueError('Abstentions exceed eligible windows')
        coverage.append('INCONCLUSIVE' if not total or not regime.get('inventory_reference') else
                        ('PASS' if (total-abstentions)/total>=policy['eligible_window_decision_coverage_minimum'] else 'FAIL'))
    checks={'DET-PERF-001':event_status,'DET-PERF-002':event_status,
            'DET-PERF-003':nuisance_status,'DET-PERF-004':aggregate(coverage),
            'DET-PERF-005':attestation('unsupported_challenges'),
            'DET-PERF-006':attestation('independent_causal_protocol'),
            'DET-PERF-007':attestation('trace_replay')}
    checks['EVIDENCE-REVIEW']=attestation('evidence_review')
    return {'policy_version':policy['version'],'criteria':checks,'status':aggregate(list(checks.values())),
            'event_results':warning,'production_release_authorized':False,
            'references_independently_verified_by_program':False,
            'basis':'Supplied evidence and reviewer assertions; reference existence and truth are not verified'}

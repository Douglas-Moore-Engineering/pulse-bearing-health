"""Reproduce a local customer demo from consumed benchmark decisions."""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from pulse.alert_stability import StableEpisodes


def main():
    policy_path = ROOT / 'config/notification-stability-development.json'
    policy = json.loads(policy_path.read_text())
    summary = {'scope': policy.pop('scope'), 'policy_sha256': hashlib.sha256(policy_path.read_bytes()).hexdigest(),
               'code_sha256': hashlib.sha256((ROOT/'src/pulse/alert_stability.py').read_bytes()).hexdigest(),
               'qualified_detector': False, 'deployed': False, 'runs': []}
    for run, name in [('B04', 'ldm_b04-rms-v2-validation.json'), ('B12', 'ldm-B12-rms-v2-final.json'), ('B17', 'ldm-B17-rms-v2-final.json')]:
        source = ROOT / 'governance/evidence' / name
        data = json.loads(source.read_text())
        state = StableEpisodes(**policy)
        openings, clears, points = [], [], []
        for i, row in enumerate(data['decisions']):
            stamp = datetime.fromisoformat(row['timestamp'])
            # Source timestamps have unknown timezone; subtract a naive epoch.
            result = state.update((stamp-datetime(1970, 1, 1)).total_seconds(), row['ratios'], row['eligible'])
            if result['opened']: openings.append(row['timestamp'])
            if result['cleared']: clears.append(row['timestamp'])
            points.append([i, max(row['ratios']), result['active']])
        first = openings[0] if openings else None
        original = data['first_flag']['timestamp'] if data['first_flag'] else None
        summary['runs'].append({'run': run, 'source': name, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'raw_episodes': data['bearing_alert_episodes'], 'stable_episodes': len(openings), 'openings': openings,
            'clears': clears, 'first_alert_unchanged': first == original,
            'lead_minutes_to_last_acquisition': data['descriptive_lead_minutes'], 'points': points})
    evidence = ROOT/'governance/evidence/customer-demo-stability.json'
    evidence.write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    template = (ROOT/'customer/demo-template.html').read_text(encoding='utf-8')
    (ROOT/'customer/benchmark-demo.html').write_text(template.replace('__DATA__', json.dumps(summary)), encoding='utf-8')
    for row in summary['runs']:
        print(row['run'], row['raw_episodes'], '->', row['stable_episodes'], 'first unchanged:', row['first_alert_unchanged'])


if __name__ == '__main__':
    main()

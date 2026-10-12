"""Bind published local LDM log evidence to descriptive stop-warning metrics."""
import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from pulse.detector_acceptance import warning_result, nuisance_result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    results = []
    for run, stop, evidence in [
        ('B04', '2021-11-17T18:26:00', 'ldm_b04-rms-v2-validation.json'),
        ('B12', '2022-08-24T11:22:00', 'ldm-B12-rms-v2-final.json'),
        ('B17', '2022-11-05T01:28:00', 'ldm-B17-rms-v2-final.json')]:
        log = ROOT/f'outputs/reference-dataset-review/{run}-documents/log.txt'
        text = log.read_text(encoding='utf-8')
        timestamp = datetime.fromisoformat(stop)
        if timestamp.strftime('%d-%m-%Y %H:%M') not in text:
            raise ValueError(f'{run}: log time mismatch')
        path = ROOT/'governance/evidence'/evidence
        data = json.loads(path.read_text())
        alert = data['first_flag']['timestamp'] if data['first_flag'] else None
        results.append({'run': run, 'event_kind': 'logged_accelerometer_limit_stop',
            'source': 'https://zenodo.org/records/10868257', 'log_sha256': digest(log),
            'replay_sha256': digest(path), 'logged_stop': stop, 'first_alert': alert,
            'timing_assumption': 'Sensitivity interval +/- 60 seconds; not a source-certified error bound. Same experiment clock assumed; timezone unknown.',
            'conditional_stop_warning': warning_result(alert, (timestamp-timedelta(minutes=1)).isoformat(), (timestamp+timedelta(minutes=1)).isoformat()),
            'physical_failure_warning': warning_result(alert, None, None),
            'nuisance': nuisance_result(0, 0, data['bearing_alert_episodes'])})
    report = {'scope': 'Retrospective endpoint audit of consumed evidence; no change to frozen evaluation or accepted event definition',
              'code_sha256': digest(Path(__file__)), 'metric_code_sha256': digest(ROOT/'src/pulse/detector_acceptance.py'),
              'qualified_detector': False, 'release_disposition': 'NOT_PROMOTED', 'results': results}
    (ROOT/'governance/evidence/detector-endpoint-audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    for row in results:
        print(row['run'], row['conditional_stop_warning'], 'physical failure: INCONCLUSIVE; nuisance: INCONCLUSIVE')


if __name__ == '__main__':
    main()

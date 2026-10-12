"""Offline metric calculations; results never authorize a detector release."""
from datetime import datetime
import math


def warning_result(alert, earliest, latest, target_minutes=60):
    """All times must share a documented clock; endpoint interval is inclusive."""
    if not math.isfinite(target_minutes) or target_minutes < 0:
        raise ValueError('Invalid warning target')
    if earliest is None or latest is None:
        return {'status': 'INCONCLUSIVE', 'reason': 'Missing endpoint interval'}
    start, end = datetime.fromisoformat(earliest), datetime.fromisoformat(latest)
    if end < start:
        raise ValueError('Reversed endpoint interval')
    if alert is None:
        return {'status': 'FAIL', 'reason': 'No alert for documented event'}
    onset = datetime.fromisoformat(alert)
    low, high = (start-onset).total_seconds()/60, (end-onset).total_seconds()/60
    status = 'PASS' if low >= target_minutes else 'FAIL' if high < target_minutes else 'INCONCLUSIVE'
    return {'status': status, 'lead_minutes_lower': low, 'lead_minutes_upper': high}


def nuisance_result(operating_hours, nuisance_episodes, unresolved_episodes, *, independently_verified=False):
    """Per-bearing descriptive rate; no extrapolated pass or confidence claim."""
    if not math.isfinite(operating_hours) or operating_hours < 0:
        raise ValueError('Invalid operating exposure')
    for value in (nuisance_episodes, unresolved_episodes):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError('Episode counts must be nonnegative integers')
    if not independently_verified or operating_hours == 0:
        return {'status': 'INCONCLUSIVE', 'reason': 'No independently verified healthy operating exposure'}
    return {'status': 'INCONCLUSIVE',
            'reason': 'Descriptive rate only; independent coverage and statistical acceptance plan required',
            'verified_operating_hours': operating_hours,
            'confirmed_nuisance_episodes': nuisance_episodes,
            'unresolved_episodes': unresolved_episodes,
            'observed_episodes_per_720_hours_lower': nuisance_episodes*720/operating_hours,
            'observed_episodes_per_720_hours_upper': (nuisance_episodes+unresolved_episodes)*720/operating_hours}

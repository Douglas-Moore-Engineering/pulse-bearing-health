"""Causal anomaly context, not a qualified bearing-damage diagnosis."""
import math


class CausalObservations:
    def __init__(self, max_partner_age=60):
        if not math.isfinite(max_partner_age) or max_partner_age <= 0:
            raise ValueError('Invalid partner age')
        self.max_partner_age = max_partner_age
        self.latest = {}
        self.last_time = None

    def update(self, side, timestamp, score):
        if side not in ('DS', 'FS') or not math.isfinite(timestamp):
            raise ValueError('Invalid observation')
        if self.last_time is not None and timestamp < self.last_time:
            raise ValueError('Out-of-order observation')
        if side in self.latest and timestamp <= self.latest[side][0]:
            raise ValueError('Duplicate or stale sensor observation')
        if score is not None and (not math.isfinite(score) or score < 0):
            raise ValueError('Invalid score')
        other = self.latest.get('FS' if side == 'DS' else 'DS')
        available = other is not None and timestamp-other[0] <= self.max_partner_age and other[1] is not None
        anomaly = None if score is None else score > 1
        partner_anomaly = other[1] > 1 if available else None
        self.latest[side] = (timestamp, score)
        self.last_time = timestamp
        return {'side': side, 'timestamp': timestamp, 'anomaly': anomaly,
                'partner_available': available, 'partner_anomaly': partner_anomaly,
                'both_anomalous': anomaly is True and partner_anomaly is True,
                'bearing_damage': 'UNDETERMINED', 'qualified_detector': False}

"""Exploratory relative-RMS monitoring; never a qualified failure detector."""
from datetime import datetime
import numpy as np


def snapshot_features(samples):
    values = np.asarray(samples, dtype=float)
    if values.shape != (20480, 4) or not np.isfinite(values).all():
        raise ValueError("IMS run 2 requires 20480 rows, four finite channels")
    return np.sqrt(np.mean(values * values, axis=0))


def evaluate(timestamps, rms, baseline_count=100, ratio=3.0,
             persistence=3, maximum_gap_seconds=900):
    values = np.asarray(rms, dtype=float)
    if (values.ndim != 2 or values.shape[1] != 4 or
            len(values) != len(timestamps) or len(values) <= baseline_count or
            baseline_count < 1 or ratio <= 1 or persistence < 1 or
            maximum_gap_seconds <= 0 or not np.isfinite(values).all() or
            (values < 0).any()):
        raise ValueError("Invalid baseline inputs")
    times = [datetime.strptime(t, "%Y.%m.%d.%H.%M.%S") for t in timestamps]
    gaps = [(b-a).total_seconds() for a, b in zip(times, times[1:])]
    if any(g <= 0 for g in gaps):
        raise ValueError("Timestamps must be strictly increasing")
    reference = np.median(values[:baseline_count], axis=0)
    if (reference <= 0).any():
        raise ValueError("Zero reference amplitude cannot define a ratio")
    normalized = values / reference
    channels = []
    for ch in range(4):
        streak = 0
        first = None
        flagged = 0
        episodes = 0
        active = False
        for i in range(baseline_count, len(values)):
            if gaps[i-1] > maximum_gap_seconds:
                streak, active = 0, False
            if normalized[i, ch] > ratio:
                streak += 1
            else:
                streak, active = 0, False
            if streak >= persistence:
                flagged += 1
                if not active:
                    episodes += 1
                    active = True
                if first is None:
                    first = i
        channels.append({
            "bearing": ch+1, "reference_rms_native_units": float(reference[ch]),
            "maximum_monitoring_ratio": float(normalized[baseline_count:, ch].max()),
            "flagged_snapshots": flagged, "episodes": episodes,
            "first_flag_timestamp": timestamps[first] if first is not None else None,
            "hours_from_first_flag_to_record_end": (
                (times[-1]-times[first]).total_seconds()/3600 if first is not None else None),
        })
    return {"snapshots": len(values), "baseline_snapshots": baseline_count,
            "monitoring_snapshots": len(values)-baseline_count,
            "start": timestamps[0], "end": timestamps[-1],
            "maximum_gap_seconds": max(gaps),
            "gaps_above_limit": sum(g > maximum_gap_seconds for g in gaps),
            "channels": channels}

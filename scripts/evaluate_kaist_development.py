"""Replay the declared development rule on quality-qualified KAIST record summaries."""
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from statistics import median


def evaluate(profile, policy):
    rows = profile["profiled_members"]
    if len(rows) != 129 or not profile.get("all_signal_members_inspected"):
        raise ValueError("Complete 129-record profile required")
    for row in rows:
        if row["shape"][0] <= 0 or row["shape"][1] != 4:
            raise ValueError("Invalid native dimensions")
        if any(not math.isfinite(value) or value < 0 for value in row["column_rms"][:2]):
            raise ValueError("Invalid vibration RMS")
    times = [datetime.strptime(r["member"], "LogFile_%Y-%m-%d-%H-%M-%S.csv") for r in rows]
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("Acquisitions must be strictly chronological")
    def eligible(row):
        return all(
            row["nonfinite_per_column"][c] / row["shape"][0]
            <= policy["max_nonfinite_fraction_per_vibration_channel"]
            and all(end - start <= policy["max_contiguous_nonfinite_samples"]
                    for start, end in row["nonfinite_runs_per_column"][c])
            for c in (0, 1)
        )
    count = policy["reference_recordings"]
    if not all(eligible(row) for row in rows[:count]):
        raise ValueError("Early reference fails quality policy; do not silently select later records")
    reference = [median(r["column_rms"][c] for r in rows[:count]) for c in (0, 1)]
    if min(reference) <= 0:
        raise ValueError("Invalid reference")
    streak = [0, 0]
    decisions = []
    for i, row in enumerate(rows[count:], start=count):
        ok = eligible(row)
        if not ok or (times[i] - times[i-1]).total_seconds() > policy["gap_reset_seconds"]:
            streak = [0, 0]
        ratios = [row["column_rms"][c] / reference[c] for c in (0, 1)]
        for c in (0, 1):
            streak[c] = streak[c] + 1 if ok and ratios[c] > policy["threshold_ratio_strictly_greater_than"] else 0
        decisions.append({"member": row["member"], "eligible": ok, "rms_ratio": ratios,
                          "flagged": max(streak) >= policy["consecutive_recordings"]})
    flags = [d for d in decisions if d["flagged"]]
    episodes = sum(d["flagged"] and (i == 0 or not decisions[i-1]["flagged"])
                   for i, d in enumerate(decisions))
    first = datetime.strptime(flags[0]["member"], "LogFile_%Y-%m-%d-%H-%M-%S.csv") if flags else None
    return {"reference_rms_g": reference, "monitoring_recordings": len(decisions),
            "abstentions": sum(not d["eligible"] for d in decisions),
            "flagged_recordings": len(flags), "alert_episodes": episodes,
            "first_flag": str(first) if first else None,
            "descriptive_lead_to_last_acquisition_hours": (times[-1]-first).total_seconds()/3600 if first else None,
            "decisions": decisions, "qualified_detector": False,
            "healthy_exposure_qualified": False, "nuisance_alert_target_validated": False}


if __name__ == "__main__":
    source = Path("governance/evidence/kaist-full-profile.json")
    config = Path("config/kaist-development-policy.json")
    result = evaluate(json.loads(source.read_text()), json.loads(config.read_text()))
    result.update({"profile_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                   "policy_sha256": hashlib.sha256(config.read_bytes()).hexdigest(),
                   "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    Path("governance/evidence/kaist-development-replay.json").write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != "decisions"}, indent=2))

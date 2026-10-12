import importlib.util
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validation", ROOT / "scripts/validate_rms_candidate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def rows():
    return [{"identity": str(i), "eligible": i >= 2,
             "timestamp": (datetime(2020, 1, 1)+timedelta(seconds=20*i)).isoformat(),
             "rms": [1 if i < 5 else 2, 1]} for i in range(12)]


def test_warmup_excluded_and_first_flag_requires_three_monitoring_records():
    result = module.replay(rows(), 3, 1.5, 3, 900)
    assert result["reference_rms"] == [1, 1]
    assert result["first_flag"]["identity"] == "7"
    assert result["excluded_regime_records_total"] == 2
    assert result["bearing_alert_episodes"] == 1


def test_regime_exclusion_resets_streak():
    data = rows()
    data[6]["eligible"] = False
    assert module.replay(data, 3, 1.5, 3, 900)["first_flag"]["identity"] == "9"


def test_cycle_sequence_does_not_invent_time_lead():
    data = rows()
    for row in data:
        row.pop("timestamp")
    result = module.replay(data, 3, 1.5, 3)
    assert result["descriptive_lead_minutes"] is None
    assert result["first_flag"]["identity"] == "7"

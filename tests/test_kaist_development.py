import importlib.util
import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("kaist_eval", ROOT / "scripts/evaluate_kaist_development.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    rows = []
    for i in range(129):
        time = datetime(2022, 1, 1) + timedelta(hours=i)
        rows.append({"member": time.strftime("LogFile_%Y-%m-%d-%H-%M-%S.csv"),
                     "shape": [2_000_001, 4], "nonfinite_per_column": [0]*4,
                     "nonfinite_runs_per_column": [[], [], [], []],
                     "column_rms": [1 if i < 10 else 4, 1, 30, 20]})
    return {"profiled_members": rows, "all_signal_members_inspected": True}, json.loads(
        (ROOT / "config/kaist-development-policy.json").read_text())


def test_reference_uses_past_only_and_three_record_persistence():
    profile, policy = fixture()
    result = module.evaluate(profile, policy)
    assert result["reference_rms_g"] == [1, 1]
    assert result["first_flag"] == "2022-01-01 12:00:00"
    assert result["flagged_recordings"] == 117
    assert result["alert_episodes"] == 1


def test_bad_record_resets_persistence():
    profile, policy = fixture()
    row = profile["profiled_members"][11]
    row["nonfinite_per_column"][0] = 300
    row["nonfinite_runs_per_column"][0] = [[0, 300]]
    result = module.evaluate(profile, policy)
    assert result["abstentions"] == 1
    assert result["first_flag"] == "2022-01-01 14:00:00"


def test_bad_reference_fails_instead_of_selecting_future_data():
    profile, policy = fixture()
    profile["profiled_members"][0]["nonfinite_per_column"][0] = 10000
    with pytest.raises(ValueError, match="Early reference"):
        module.evaluate(profile, policy)


def test_long_gap_resets_persistence():
    profile, policy = fixture()
    for row in profile["profiled_members"][12:]:
        time = datetime.strptime(row["member"], "LogFile_%Y-%m-%d-%H-%M-%S.csv") + timedelta(hours=2)
        row["member"] = time.strftime("LogFile_%Y-%m-%d-%H-%M-%S.csv")
    result = module.evaluate(profile, policy)
    assert result["first_flag"] == "2022-01-01 16:00:00"


def test_nonfinite_feature_is_rejected():
    profile, policy = fixture()
    profile["profiled_members"][20]["column_rms"][0] = float("nan")
    with pytest.raises(ValueError, match="Invalid vibration RMS"):
        module.evaluate(profile, policy)

from datetime import datetime, timedelta
import numpy as np
import pytest
from pulse.ims_baseline import evaluate, snapshot_features


def times(n):
    return [(datetime(2004, 2, 12)+timedelta(minutes=10*i)).strftime("%Y.%m.%d.%H.%M.%S") for i in range(n)]


def test_persistence_and_no_future_baseline_leakage():
    data = np.ones((110, 4))
    data[100:, 0] = 4
    result = evaluate(times(110), data)
    assert result["channels"][0]["first_flag_timestamp"] == times(110)[102]
    assert result["channels"][0]["reference_rms_native_units"] == 1
    assert result["channels"][0]["flagged_snapshots"] == 8
    assert result["channels"][1]["episodes"] == 0


def test_gap_breaks_persistence():
    data = np.ones((105, 4)); data[100:, 0] = 4
    t = times(105)
    for i in range(102, 105):
        t[i] = (datetime.strptime(t[i], "%Y.%m.%d.%H.%M.%S")+timedelta(hours=1)).strftime("%Y.%m.%d.%H.%M.%S")
    assert evaluate(t, data)["channels"][0]["first_flag_timestamp"] == t[104]


def test_schema_and_invalid_values():
    assert np.all(snapshot_features(np.ones((20480, 4))) == 1)
    for data in [np.ones((20479, 4)), np.full((20480, 4), np.nan)]:
        with pytest.raises(ValueError): snapshot_features(data)
    with pytest.raises(ValueError): evaluate(times(101), np.zeros((101, 4)))
    with pytest.raises(ValueError): evaluate(times(101)[::-1], np.ones((101, 4)))


def test_threshold_is_strict_and_scale_invariant():
    data = np.ones((108, 4))
    data[100:103, 0] = 3
    data[103:, 0] = 4
    original = evaluate(times(108), data)
    scaled = evaluate(times(108), data * np.array([2, 3, 4, 5]))
    assert original["channels"][0]["first_flag_timestamp"] == times(108)[105]
    for a, b in zip(original["channels"], scaled["channels"]):
        assert a["first_flag_timestamp"] == b["first_flag_timestamp"]
        assert a["maximum_monitoring_ratio"] == b["maximum_monitoring_ratio"]

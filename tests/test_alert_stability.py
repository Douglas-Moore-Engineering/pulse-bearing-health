import pytest
from pulse.alert_stability import StableEpisodes


def test_hysteresis_holds_one_episode_through_threshold_chatter():
    state = StableEpisodes()
    values = [2, 2, 2, 1.4, 2, 2, 2, 1.3, 2, 2, 2]
    results = [state.update(i, [v, 1]) for i, v in enumerate(values)]
    assert sum(r["opened"] for r in results) == 1
    assert results[-1]["active"]


def test_clear_requires_both_channels_and_rearm_requires_new_persistence():
    state = StableEpisodes()
    values = [[2, 1]]*3 + [[1, 1.3]]*5 + [[1, 1]]*5 + [[2, 1]]*3
    results = [state.update(i, v) for i, v in enumerate(values)]
    assert [i for i,r in enumerate(results) if r["opened"]] == [2, 15]
    assert [i for i,r in enumerate(results) if r["cleared"]] == [12]


def test_gap_is_interruption_not_healthy_clear():
    state = StableEpisodes(max_gap=10)
    for i in range(3): state.update(i, [2, 1])
    result = state.update(20, [2, 1])
    assert result["interrupted"] and not result["cleared"] and not result["opened"]
    assert state.update(21, [2, 1])["opened"] is False
    assert state.update(22, [2, 1])["opened"] is True


def test_invalid_and_out_of_order_observations_fail():
    state = StableEpisodes()
    state.update(1, [1, 1])
    with pytest.raises(ValueError): state.update(1, [1, 1])
    with pytest.raises(ValueError): state.update(2, [float('nan'), 1])

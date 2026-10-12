import pytest
from pulse.detector_acceptance import warning_result, nuisance_result


def test_warning_uncertainty_cannot_turn_borderline_into_pass():
    result = warning_result('2022-01-01T00:00:00', '2022-01-01T00:59:00', '2022-01-01T01:01:00')
    assert result['status'] == 'INCONCLUSIVE'


def test_warning_pass_requires_conservative_bound():
    assert warning_result('2022-01-01T00:00:00', '2022-01-01T01:00:00', '2022-01-01T01:01:00')['status'] == 'PASS'


def test_missing_label_is_not_a_miss_but_missing_alert_is():
    assert warning_result(None, None, None)['status'] == 'INCONCLUSIVE'
    assert warning_result(None, '2022-01-01T00:00:00', '2022-01-01T00:01:00')['status'] == 'FAIL'


def test_late_alert_fails():
    assert warning_result('2022-01-01T02:00:00', '2022-01-01T01:00:00', '2022-01-01T01:01:00')['status'] == 'FAIL'


def test_unverified_or_short_healthy_exposure_never_passes():
    assert nuisance_result(720, 0, 0)['status'] == 'INCONCLUSIVE'
    assert nuisance_result(1, 0, 0, independently_verified=True)['status'] == 'INCONCLUSIVE'


def test_unresolved_episodes_remain_in_upper_rate():
    result = nuisance_result(720, 1, 2, independently_verified=True)
    assert result['observed_episodes_per_720_hours_lower'] == 1
    assert result['observed_episodes_per_720_hours_upper'] == 3


def test_invalid_inputs_rejected():
    with pytest.raises(ValueError): nuisance_result(float('nan'), 0, 0)
    with pytest.raises(ValueError): nuisance_result(720, -1, 0)
    with pytest.raises(ValueError): warning_result(None, '2022-01-02', '2022-01-01')

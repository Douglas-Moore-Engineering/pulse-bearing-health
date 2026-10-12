import pytest
from pulse.causal_observations import CausalObservations


def test_missing_partner_does_not_hide_anomaly():
    result = CausalObservations().update('DS', 0, 2)
    assert result['anomaly'] and not result['partner_available']
    assert result['bearing_damage'] == 'UNDETERMINED'


def test_both_anomalies_preserved_without_winner():
    stream = CausalObservations()
    first = stream.update('DS', 0, 10)
    second = stream.update('FS', 1, 2)
    assert first['anomaly'] and second['anomaly'] and second['both_anomalous']
    assert not first['partner_available']  # Later data never revises the result.


def test_stale_partner_and_invalid_score_are_unavailable():
    stream = CausalObservations()
    stream.update('DS', 0, 2)
    assert not stream.update('FS', 61, 2)['partner_available']
    result = stream.update('DS', 62, None)
    assert result['anomaly'] is None
    assert not stream.update('FS', 63, 2)['partner_available']


def test_rejects_future_reordering_and_duplicate_sensor_time():
    stream = CausalObservations()
    stream.update('DS', 10, 2)
    with pytest.raises(ValueError): stream.update('FS', 9, 2)
    with pytest.raises(ValueError): stream.update('DS', 10, 2)
    with pytest.raises(ValueError): stream.update('FS', 11, float('nan'))

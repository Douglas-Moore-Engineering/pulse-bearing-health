from pulse.trailing_median import TrailingMedian
import pytest

def test_full_window_and_persistence():
 s=TrailingMedian([1],window=3,persistence=2)
 assert s.update(0,[2])['flagged'] is None
 assert s.update(1,[2])['flagged'] is None
 assert s.update(2,[2])['flagged'] is False
 assert s.update(3,[2])['flagged'] is True
 assert s.update(1000,[2])['flagged'] is None

def test_prefix_invariance_and_either_channel():
 def run(values):
  s=TrailingMedian([1,1],window=2,persistence=1)
  return [s.update(i,v) for i,v in enumerate(values)]
 prefix=[[1,2],[1,2],[1,2]]
 assert run(prefix)==run(prefix+[[100,100]])[:3]
 assert run(prefix)[-1]['flagged']

def test_invalid_does_not_change_state():
 s=TrailingMedian([1],window=1,persistence=1)
 with pytest.raises(ValueError):s.update(0,[float('nan')])
 assert s.update(0,[2])['flagged']
 with pytest.raises(ValueError):s.update(0,[2])

def replay_ratios(values):
    detector=TrailingMedian([1])
    return [detector.update(i,[value]) for i,value in enumerate(values)]


def test_default_step_onset_and_clear_delay():
    outputs=replay_ratios([1]*20+[2]*20+[1]*20)
    assert next(i for i,r in enumerate(outputs) if r['flagged'])==29
    assert next(i for i in range(40,len(outputs)) if outputs[i]['flagged'] is False)==47


@pytest.mark.parametrize('length',[1,3,7])
def test_short_pulses_filtered(length):
    assert not any(r['flagged'] for r in replay_ratios([1]*20+[2]*length+[1]*30))


def test_eight_record_pulse_can_trigger_after_raw_signal_returns():
    outputs=replay_ratios([1]*20+[2]*8+[1]*30)
    assert outputs[27]['flagged'] is False
    assert outputs[29]['flagged'] is True


def test_equal_threshold_is_not_an_alarm():
    assert not any(r['flagged'] for r in replay_ratios([1.5]*40))


def test_gap_boundary_and_rewarm():
    detector=TrailingMedian([1])
    for i in range(20):last=detector.update(i,[2])
    assert last['flagged']
    assert detector.update(919,[2])['flagged']  # Exactly 900 seconds does not reset.
    assert detector.update(1820,[2])=={'available':False,'flagged':None}


def test_other_channel_can_keep_alarm_active():
    detector=TrailingMedian([1,1])
    for i in range(20):detector.update(i,[2,2])
    for i in range(20,50):assert detector.update(i,[1,2])['flagged']

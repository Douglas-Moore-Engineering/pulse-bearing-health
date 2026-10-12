# Case 2 spectral/reference distribution comparison

Consumed-data investigation; no detector change. [Script](../../scripts/analyze_sca_spectral_shift.py) and [full quantiles](../../governance/evidence/sca-spectral-shift.json) reproduce the outer-ring envelope contrast decomposition with publisher hash checks. Signal/background powers are normalized by squared Hann-window sum, not calibrated spectral densities.

| FS population | Median RMS (m/s^2) | Median target-band power | Median background power | Median harmonic contrast |
|---|---:|---:|---:|---:|
| Normal calibration | 0.578 | 0.0000454 | 0.0000199 | 2.54 |
| Normal test, flagged by any feature | 2.799 | 0.001049 | 0.0001216 | 10.80 |
| Normal test, not flagged | 3.635 | 0.000447 | 0.0001373 | 4.52 |

The false-positive group's median target-band power is approximately 23.1 times calibration; background is approximately 6.1 times calibration. Thus the aggregate shift is **not explained by a collapsed background denominator**: both increase, and target-band power rises more. These are ratios of population medians, not paired per-record changes or proof of causation. The contrast is the mean of harmonic ratios, so its median is not the ratio of the signal/background medians.

The normal test negatives also have much higher RMS than calibration. A simple absolute RMS floor cannot be justified as the fix: high overall vibration appears in both false-positive and true-negative groups. The preceding [speed analysis](sca-false-positive-analysis.md) established identical recorded RPM for reference and test in this case.

The population split uses the frozen OR decision across all three features; some positive records were triggered by ball contrast alone. Therefore this outer-ring comparison does not attribute every positive to outer-ring energy. On the damaged DS, 91 detected snapshots have median outer-ring contrast 45.28; the three misses have median 1.01. Such post-outcome summaries are descriptive and cannot select a deployable threshold without further validation.

## Engineering implication

There is a substantial pre/post-replacement distribution mismatch on the normal-labeled FS. Transmitted vibration, mounting/load changes, other faults and labeling/localization differences remain hypotheses. We have not established that the feature identifies damage at the sensor's bearing. Do not erase supplied normal labels or claim false positives are true failures without independent evidence.

Further detector development needs better fault localization or representative operating-condition calibration, plus resolved frequency interpretation. Merely increasing thresholds on these observations risks hiding real faults. Cases 3-10 remain reserved. No threshold, deployed API, acceptance requirement or release disposition changed: NOT_PROMOTED.

Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001. Reproduction: `python scripts/analyze_sca_spectral_shift.py` with SciPy/NumPy available. This run completed successfully; repository validation is separate from model validation.

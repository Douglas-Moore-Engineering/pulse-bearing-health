# SCA false-positive attribution

Consumed cases 2/11 only. The analysis reproduced all frozen normal-positive and normal-negative counts exactly; no threshold changed and no reserved case was opened. [Reproduction script](../../scripts/analyze_sca_false_positives.py) and [results](../../governance/evidence/sca-false-positive-analysis.json).

## Findings

Case 2 FS has 129 normal-labeled positive snapshots. Their feature combinations are:

| Features exceeding reference thresholds | Snapshots |
|---|---:|
| Outer ring only | 65 |
| Inner and outer ring | 29 |
| Ball only | 34 |
| Outer ring and ball | 1 |

Thus outer-ring contrast participates in 95 of 129 positives, ball contrast in 35, and inner-ring contrast in 29; counts overlap. All reference and test records use **1162 RPM**. Recorded speed mismatch cannot explain this case's false positives. This does not prove constant physical speed, load or mounting conditions: it only establishes that the supplied RPM field does not distinguish them.

The false positives span December 1, 2021 through February 28, 2022. Their duration and multiple contributing features mean simply suppressing one known bad feature is not a defensible general correction. Cross-placement transmission and pre/post-replacement reference shifts remain hypotheses, not demonstrated causes. Sensor measurements were not paired by row index.

For case 11, the sole DS positive is a ball-feature exceedance. Every scored DS and FS test record is outside its respective normal-reference RPM range, including all true negatives. A strict reference-speed guard would abstain on all 38 challenge records; it would not demonstrate improved diagnostic specificity. Do not report abstention as a true negative or hide this coverage loss.

## Consequence for detector development

A speed guard alone cannot fix case 2. The next useful investigation is spectral/background and calibration-distribution comparison on these consumed records, together with source/geometry verification of fault-frequency units. Investigate whether the detector can distinguish the damaged side from transmitted or unrelated vibration without using the known test-side label as an input. Any revised feature or calibration policy must report both sensitivity and coverage, then receive a fresh freeze before reserved-case use.

No root cause has been established and no improved detector has yet been validated. The frozen candidate remains NOT_PROMOTED. Cases 3-10 remain reserved; physical-warning and operating-day nuisance targets remain unscored. Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001.

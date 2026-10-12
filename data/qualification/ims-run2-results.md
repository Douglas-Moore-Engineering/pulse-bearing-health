# IMS run 2: exploratory RMS run results

Scope: local offline evaluation of the user-supplied DS-IMS data. This is a measured reference experiment, not a qualified degradation detector or site acceptance. The existing Azure service remains an authenticated, persistent assessment API with detection unavailable.

## Method and reproducibility

The [frozen plan](ims-baseline-plan.json) selects the first 100 chronological snapshots as an early reference segment. That segment is not independently certified healthy. Per-channel reference RMS is its median. Monitoring flags a channel only after three consecutive snapshots exceed three times its reference RMS; a gap above 15 minutes resets persistence. This engineering baseline was fixed before feature evaluation and was not tuned against the resulting trace.

The [run artifact](../../governance/evidence/ims-run2-baseline.json) records every measurement member's SHA-256, plan/code hashes, environment, timing and channel results. Native files remain in ignored local storage. The extracted `2nd_test.rar` SHA-256 is `b154d5ba1ae5f7f01cdd4f1bde5b08cfdc2f3134d51ad2f6614b1270a86ab632`; parent distribution lineage is in [source inspection](ims-inspection.json). All 984 measurement files must contain 20,480 rows and four finite numeric channels or the evaluation fails.

Run from the repository root with Python and NumPy 2.2.6:

```powershell
python scripts/run_ims_baseline.py outputs/reference-dataset-review/IMS-sample/2nd_test --output outputs/reference-dataset-review/ims-run2-repeat.json
python -m pytest tests/test_ims_baseline.py -q
```

The test suite checks chronological baseline isolation, three-snapshot persistence, recording-gap reset, malformed/nonfinite input rejection, zero-reference rejection, timestamp ordering, strict threshold comparison and channel-scale invariance.

## Measured results

Executed 2026-10-11 on all 984 snapshots: 100 reference and 884 monitoring snapshots, each with four channels. Every file passed the numerical schema check. The trace spans 2004-02-12 10:32:39 to 2004-02-19 06:22:39; the maximum observed inter-snapshot gap is 600 seconds.

| Bearing | Maximum monitoring RMS / reference | Flagged snapshots | Episodes | First sustained flag |
|---|---:|---:|---:|---|
| 1 | 9.336 | 17 | 1 | 2004-02-19 03:22:39 |
| 2 | 2.288 | 0 | 0 | None |
| 3 | 1.787 | 0 | 0 | None |
| 4 | 2.667 | 0 | 0 | None |

Bearing 1's first sustained flag precedes the final recorded snapshot by **3.0 wall-clock hours**. This aligns with the bearing identified in the documented endpoint observation, but does not establish when damage began or predictive accuracy. The 17 flagged snapshots are correlated observations in one episode, not 17 independent detections. No flags on the other channels establishes only that this particular rule did not flag them.

## Interpretation limits and next gate

RMS uses unknown native amplitude units. Ratios cancel a constant multiplicative calibration per channel, but do not establish physical acceleration or remove offsets, changing gain or operating-condition effects. Acquisition rate is documented as 20 kHz, making each 20,480-point snapshot 1.024 seconds. Measurement timestamps have no established timezone.

The README reports bearing 1 outer-race failure at the experiment endpoint. It does not label the onset of degradation in each window. An interval from the first anomaly to the last recorded snapshot is therefore a retrospective wall-clock interval, not proven warning lead time or RUL. Other bearings are not adjudicated healthy controls. No precision, recall, false-positive rate or diagnostic accuracy can be established here.

There is one independent experiment. The early/late split is chronological within that experiment, not run-held-out generalization. Threshold selection, independent-run testing, rights for downstream commercial use, calibrated units, qualified onset labels and operational false-alert burden remain open. No model promotion, external notification, equipment action or production gate approval follows from these results.

Trace: PULSE-FR-001/002 provenance and schemas, PULSE-FR-003 descriptive baseline, PULSE-FR-004/005/006 eligibility limits, PULSE-NFR-008 group separation and AIG-REQ-001 artifact trace. Engineering returns this bounded evidence to Dr. Moore through customer phases 8–10; standards and AI governance retain the unresolved qualification and release conditions.

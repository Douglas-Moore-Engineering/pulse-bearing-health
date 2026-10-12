# SCA case 1 retrospective diagnostic results

The 1.5x RMS snapshot rule detects **1 of 117 fault-labeled DS measurements**, missing 116. FS has **0 positives in 126 normal measurements**. This is a clear sensitivity problem on this case, not an accepted detector.

| Placement | TP | FN | FP | TN | Excluded |
|---|---:|---:|---:|---:|---:|
| DS (damaged side) | 1 | 116 | 0 | 0 | 7 |
| FS (normal side) | 0 | 0 | 0 | 126 | 9 |

Fault-snapshot recall on DS is 0.855%; observed normal-snapshot false-positive rate on FS is 0%. DS has no eligible normal test records, and FS has no positive test records; the corresponding metrics are undefined, not zero. These are correlated observations from one case, not 243 independent bearings. A zero observed false-positive count does not prove a zero nuisance rate.

## Method and evidence

[Protocol](../../config/sca-case1-diagnostic-protocol.json) and [protocol hash](../../governance/evidence/sca-case1-protocol-freeze.json) were recorded before scoring. Case 1 had already been schema/label-inspected and is development data. Each placement uses the median waveform RMS from its 122 valid normal publisher-train records. References are 0.0568861 m/s^2 (DS) and 0.0585121 m/s^2 (FS). The decision is strictly greater than 1.5 times that reference. All raw inputs were rechecked against publisher hashes.

The diagnostic scores single snapshots; it does not apply the deployed three-record/900-second episode policy, which is incompatible with these daily observations. Exclude off/missing-speed labels and nonpositive/nonfinite RPM. No threshold tuning was performed after results. Reproduce with `python scripts/evaluate_sca_case1.py` with SciPy and NumPy available. [Full decisions and bound input/code hashes](../../governance/evidence/sca-case1-diagnostic.json).

Normal reference recordings come after replacement, so this is retrospective calibration, not prospective forecasting. The first eligible DS snapshot is already fault-labeled; warning to physical onset is not measurable. Operating-day nuisance acceptance remains unscored. See [source qualification](sca-review.md).

## Engineering decision

Do not promote this RMS-only diagnostic. The SCA labels now reveal misses that an unlabeled anomaly replay could not measure. Next development should investigate fault-frequency/envelope features and speed-aware normalization on case 1, verifying frequency-multiple units and signal bandwidth first. Preserve cases 2-11 from signal inspection until the revised detector and case/asset grouping protocol are frozen. A spectral detector's agreement with labels derived partly from envelope spectra must be disclosed; it is not independent physical inspection evidence.

No cloud deployment, gate promotion, warning-target change or threshold adjustment resulted from this experiment. Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001. Model engineering owns feature revision; domain and release reviewers retain qualification decisions.

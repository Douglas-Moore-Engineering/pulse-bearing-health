# Feature separation and threshold tradeoffs

Consumed SCA cases 1/2/11 only. Recomputed the three envelope features from publisher-hash-verified native signals. Kept existing reference thresholds and swept fixed multipliers 0.5, 1, 1.5, 2, 3, 5 and 10. No new threshold is selected or promoted.

| Case | Threshold multiplier | Detected fault snapshots | Normal positives |
|---|---:|---:|---:|
| 1 | 1 | 112/117 | 14/126 |
| 1 | 1.5 | 100/117 | 4/126 |
| 1 | 2 | 75/117 | 1/126 |
| 1 | 3 | 39/117 | 0/126 |
| 1 | 5 | 14/117 | 0/126 |
| 2 | 1 | 91/94 | 129/296 |
| 2 | 1.5 | 90/94 | 61/296 |
| 2 | 2 | 86/94 | 37/296 |
| 2 | 3 | 72/94 | 2/296 |
| 2 | 5 | 30/94 | 0/296 |

Raising thresholds reduces normal positives at the cost of missed fault snapshots. In case 2, the 3x multiplier leaves two normal positives but misses 22 of 94 fault snapshots; 5x eliminates normal positives but misses 64. This does not support declaring the detector fixed by threshold adjustment. Counts are snapshots, not independent failure events or nuisance episodes per operating hour.

[All per-feature tradeoffs](sca-feature-tradeoffs.csv) include individual features and their OR maximum. [Machine-readable evidence](../../governance/evidence/sca-feature-separation.json) includes per-case, per-side, per-label score quantiles and RPM ranges. Comparisons retain each side's existing reference normalization; they are not an unbiased cross-sensor classifier validation.

Fault labels coincide with DS and normal labels with FS in cases 1/2. Side and fault effects cannot be separated from these consumed test groups alone. RPM ranges are descriptive; this experiment does not establish speed causation, and load effects were not evaluated. Reference calibration remains retrospective and physical frequency interpretation unverified. The next candidate needs defensible reference conditions and validation groups that distinguish fault effects from sensor/operating-condition differences.

Reproduce: `python scripts/analyze_sca_feature_separation.py` with the existing local data and declared numerical dependencies. No raw samples are copied into evidence. Reserved cases 3?10 remain untouched; deployed detector and acceptance requirements remain unchanged. NOT_PROMOTED.

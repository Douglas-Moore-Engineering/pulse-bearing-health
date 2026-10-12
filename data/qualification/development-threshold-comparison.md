# Cross-dataset development threshold comparison

The 1.5x relative-RMS threshold is selected as a **development candidate**, not an accepted or deployed detector. It detects the previously missed IMS bearing, while also increasing alerts on bearings without documented endpoint failures. Specificity remains unresolved.

## Method and evidence

Executed `python scripts/compare_development_thresholds.py` on the already-consumed IMS runs 1/2 and UNSW Test 1. Every IMS native file was checked against the earlier per-file SHA-256 evidence before numerical processing. IMS retained its first-100-record per-channel median reference, three-record persistence and 900-second gap reset. The original 3x results reproduced exactly for flag counts, episodes, first-flag timestamps and maximum ratios on every channel in both runs. Original baseline source and historical results were preserved.

UNSW used only the 80-record 6 Hz sequence, the first ten records as reference, and three successive-record persistence. Its cycle positions are not converted into warning hours. Elapsed-time gap handling remains unavailable, so its persistence is sequential rather than validated temporal persistence. Multiple-speed measurements were excluded from this fixed-speed comparison. No held-out signals were accessed.

[Comparison evidence](../../governance/evidence/development-threshold-comparison.json) binds source evidence and code hashes. [KAIST comparison](../../governance/evidence/kaist-development-sensitivity.json) uses the previously declared missingness policy, first-ten-record reference and 90-minute gap reset. These dataset-specific settings are not yet a universal deployment contract.

## Observed descriptive lead to final acquisition

For two-channel bearings, the table uses the earliest independently persistent channel. Values are elapsed hours to the final recorded snapshot, not proven lead to damage onset or exact failure time. IMS run 1 contains substantial interruptions, so wall-clock lead is not active operating exposure.

| Threshold | IMS run 1, bearing 3 | IMS run 1, bearing 4 | IMS run 2, bearing 1 | KAIST |
|---|---:|---:|---:|---:|
| 1.5x | 12.54 h | 107.36 h | 46.67 h | 106 min |
| 2.0x | 9.87 h | No alert | 46.50 h | 106 min |
| 2.5x | 10 min | No alert | 8 h | 106 min |
| 3.0x | 10 min | No alert | 3 h | 0 min |

Only 1.5x flags all three documented IMS endpoint bearings in this comparison. On UNSW Test 1 it flags 29 horizontal and 18 vertical recordings, first at shaft cycles 238297 and 284609 respectively. At 2x, nine horizontal recordings are flagged; at 2.5x and 3x neither channel flags. This is not a failure-recall metric without qualified endpoint/progression labels.

## Tradeoff and next validation boundary

At 1.5x, IMS run 1 bearing 2 also has two flagged snapshots on one channel. In run 2, bearings 2/3/4 have 13/4/45 flagged snapshots. Those bearings lack documented endpoint-failure labels; the alerts cannot be classified as true degradation or nuisance events from the present evidence. Lowering the threshold repairs observed sensitivity on development data but does not establish acceptable specificity.

The [candidate record](../../config/rms-candidate-v2.json) fixes the selected threshold and persistence while explicitly leaving the validation protocol incomplete. Before reserved signals are used, resolve reference/operating regimes, quality policy, endpoint scoring and UNSW time interpretation; then freeze that protocol. Preserve all channels and speeds within each bearing partition. Do not present these selection data as independent validation or claim the one-per-30-operating-days nuisance target is met.

The deployed 3x reference rule is unchanged. IMS's earlier missed-bearing result remains valid historical evidence. No production gate advanced, cloud resource changed, or notification was sent. Trace: PULSE-FR-003, PULSE-NFR-008 and AIG-REQ-001.

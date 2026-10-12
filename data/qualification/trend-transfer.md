# Unchanged trailing-median transfer on consumed LDM runs

**NOT_PROMOTED.** Applied the exact B17 development configuration to consumed B04 and B12, and reproduced every B17 decision as a regression check. The parameter-file hash is identical across all three executions. These are further development results on already-inspected trajectories, not independent validation.

| Run | Baseline ? candidate episodes | First-alert delay | Candidate coverage | Baseline ? candidate flagged records |
|---|---:|---:|---:|---:|
| B04 | 3 ? 1 | 2.03 min | 98.55% | 663 ? 663 |
| B12 | 26 ? 1 | 2.60 min | 97.90% | 572 ? 651 |
| B17 | 9 ? 1 | 2.48 min | 99.47% | 514 ? 536 |

The fixed 15-record median, 1.5x threshold and three-record persistence reduce fragmentation on all three runs. The 14-record warm-up is included in the coverage denominator. There were no ineligible monitoring records after the reference period in these inputs; the transfer script fails explicitly if such a record appears rather than silently skipping it. Initial reference medians are recomputed from each run's first 100 eligible observations, matching the baseline procedure; the numeric reference is not transferred across bearings.

The candidate holds alerts longer, particularly B12 (651 flagged records versus 572). Thus fewer episodes do not prove fewer nuisance alerts, lower operator burden, improved sensitivity or correct recovery/reset behavior. No qualified healthy labels are available. All first-alert leads remain descriptive intervals to the final recording, not physical-failure warning measurements.

Results: [B04](../../governance/evidence/trend-transfer-B04.json), [B12](../../governance/evidence/trend-transfer-B12.json), [B17 regression](../../governance/evidence/trend-transfer-B17.json). Source, configuration, replay and component hashes are bound in each report. Run `python scripts/evaluate_trend_transfer.py B04` (or B12/B17) to reproduce from committed feature evidence.

Next qualification work: assess alert-clear delay and response to transient excursions under synthetic controlled conditions; explicitly specify the alert lifecycle before freezing a candidate. Independent endpoint and healthy-exposure evidence remain required. No reserved data or Azure deployment was changed.

# B17 causal trailing-median development

**NOT_PROMOTED.** Used consumed B17 feature inventory only. The configuration was written before this execution, but prior B17 outcomes were already known; this is not a prospective independent test.

Fixed settings: first 100 eligible records define each channel median; trailing 15-record median of normalized RMS; strict 1.5x threshold; three consecutive qualifying records; reset after gaps over 900 seconds. Either channel may flag the bearing. Require a full trailing window before decisions. No parameter sweep or future-data baseline.

| Measurement | Recorded RMS baseline | Trailing-median candidate |
|---|---:|---:|
| Monitoring records | 2,633 | 2,633 |
| Flagged records | 514 | 536 |
| Episodes | 9 | 1 |
| First flag to final recording | 195.90 minutes | 193.42 minutes |

Candidate coverage is 2,619/2,633 (99.47%); the first 14 monitoring observations are explicitly unavailable during warm-up. First flag: 2022-11-04 22:15:06 in the source's unspecified timezone. The first alert is about 2.48 minutes later than the baseline. More flagged records alongside fewer episodes reflects persistence/smoothing; it does not establish fewer false alerts or improved fault recall.

No verified healthy labels or physical failure timestamp exist for scoring the operational criteria. These minutes are only relative to record end. No RUL, failure-warning acceptance or nuisance-rate pass is inferred. Compare with episode grouping already explored elsewhere before treating this as new detection capability.

[Fixed configuration](../../config/b17-trend-development.json), [complete decisions and hashes](../../governance/evidence/b17-trend-development.json), [software tests](../../governance/evidence/b17-trend-tests.xml). Reproduce with `python scripts/evaluate_b17_trend.py`. Tests cover warm-up, persistence, gap reset, prefix invariance, either-channel triggering and invalid observations. Full suite: 158 passed.

Next: transfer these unchanged settings to other consumed trajectories and report regressions before any freeze for reserved-data evaluation. Do not deploy from this one-run improvement. Reserved data and deployed detector remain unchanged.

# Independent causal envelope candidate

Candidate: independent-causal-envelope-v1. Consumed cases 1/2/11 only; **NOT_PROMOTED**. Recomputed native signal features against existing thresholds. Each side flags its own score above one without an opposite-side veto or pairing requirement. Existing causal context processing is reused; this is not a trained model or a newly tuned threshold.

| Case/side | Detected | Missed | Normal positives | Eligible coverage |
|---|---:|---:|---:|---:|
| 1/DS | 112 | 5 | 0 | 100% |
| 1/FS | 0 | 0 | 14 | 100% |
| 2/DS | 91 | 3 | 0 | 100% |
| 2/FS | 0 | 0 | 129 | 100% |
| 11/DS | 0 | 0 | 1 | 100% |
| 11/FS | 0 | 0 | 0 | 100% |

All eligible observations now receive decisions; case 1 still excludes seven DS and nine FS records. Removing the pairing requirement resolves its abstentions and avoids suppressing simultaneous anomalies. It also restores substantial normal-side positives. The paired comparator abstains on many records, so counts are shown across each complete eligible inventory rather than claimed as an equal-decision-subset accuracy improvement.

These changes fix runtime causality and opposite-side suppression only. Calibration remains retrospective, physical frequency interpretation remains unverified, and warning time/healthy operating exposure remain unqualified. Case-1 normal positives refer to the OR of all three envelope features, not the earlier inner-ring-only result. Snapshot counts are not event misses or nuisance episodes.

[Full measured comparison](../../governance/evidence/sca-independent-causal-development.json). Reproduce with `python scripts/evaluate_sca_independent_causal.py` using the existing ignored native data and declared NumPy/SciPy dependencies. Publisher hashes are checked before signal access. Reserved cases 3?10 were not opened. The deployed RMS reference rule is unchanged.

Next: investigate normal-side feature responses and frequency/reference validity on consumed cases. Do not deploy this candidate or consume holdouts to conceal the remaining false positives.

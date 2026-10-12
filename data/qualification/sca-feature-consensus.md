# Feature consensus development check

**Rejected; NOT_PROMOTED.** Tested a two-of-three threshold rule on consumed SCA cases 1/2/11, retaining existing features, thresholds, exclusions and causal per-side processing. This was a development ablation, not held-out validation or a trained model.

Observed totals: 0 detected fault snapshots, 211 missed fault snapshots, 30 normal positives and 430 normal negatives. The rule detected none of the 117 case-1 or 94 case-2 eligible fault snapshots. Snapshot counts do not establish independent failure-event counts.

Requiring agreement between distinct fault-frequency features destroys sensitivity in this dataset. Any reduced false-positive count cannot justify promotion. No three-feature trial is needed to rescue this rule: its positives are a subset of the already ineffective two-feature positives under identical thresholds.

The one-feature mode exactly reproduced the prior result rows after the implementation change. [Two-feature evidence](../../governance/evidence/sca-feature-votes-2.json) and [baseline reproduction](../../governance/evidence/sca-feature-votes-1.json). Reproduce with `python scripts/evaluate_sca_independent_causal.py --feature-votes 2` (or 1). Publisher hashes are checked; reserved cases remain unopened. The original baseline evidence is preserved separately.

Next candidate work should examine per-feature discrimination and valid reference conditions, rather than impose agreement among different fault families. Operational endpoint and healthy exposure evidence remain unresolved. No deployed rule or acceptance requirement changed.

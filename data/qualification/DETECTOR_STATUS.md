# Consolidated detector status

**No detector is qualified for production.** This is the current detector entry point; linked studies retain their historical results. The deployed frozen RMS rule and experimental SCA paired candidate are separate candidates and are never pooled into one acceptance result.

| Candidate | Evaluator result | Interpretation |
|---|---|---|
| Frozen 3x RMS reference rule | INCONCLUSIVE | Insufficient qualified event timing, exposure and review evidence to score the complete acceptance policy. The documented bearing-4 miss remains an adverse finding; inconclusive does not mean the detector is acceptable. |
| SCA paired development candidate | FAIL | Coverage falls below 95% on several case/side groups; future-neighbour pairing and post-hoc development fail the causal independent-protocol criterion. Operational warning and nuisance criteria remain inconclusive. |

[Machine-readable results](../../governance/evidence/detector-performance-consolidated.json) bind the dossiers, policy, evaluator and source hashes. Dossiers: [RMS](performance-dossiers/frozen-3x-rms.json), [SCA paired](performance-dossiers/sca-paired-development.json).

## What the measurements establish

The RMS rule produced no flags for documented damaged IMS bearing 4. Bearing 3 flagged ten minutes before the final recording; that is not verified physical-failure warning time. Native clock/endpoint uncertainty is preserved. The event list is empty because no eligible, timed event dossier has been established; documented damaged bearings remain explicitly recorded as source observations, not silently counted as healthy.

SCA coverage from existing recorded eligible-window inventories is 104/117 (88.9%) for case 1 DS, 104/126 (82.5%) for case 1 FS, 91/94 (96.8%) for case 2 DS, 91/296 (30.7%) for case 2 FS, and 19/19 for each case 11 side. These are consumed-case results, not new held-out validation. Exclusions are retained in the dossier. Snapshot false positives are not converted into nuisance episodes per operating hour.

The performance policy was written after these studies. This retrospective gap assessment cannot be presented as prospective acceptance. Evidence assertions are not independently verified by the program. No source data or reserved cases were opened, no model was trained or deployed, and no release gate changed.

## One next-work sequence

1. Revise causal, multiple-fault-compatible candidate logic on consumed development cases only. Preserve uncertainty and report coverage; do not suppress the weaker side merely because the other side scores higher.
2. Resolve endpoint timing, operating exposure and physical frequency interpretation with qualified source evidence. Missing evidence remains inconclusive.
3. Freeze candidate, preprocessing, commissioning, episode logic, support scope and evaluation protocol before opening reserved cases 3?10. Check whether those data can actually support the required metrics first.
4. Evaluate using the [performance requirements](../../requirements/detector-performance.md) and obtain the required review before any promotion.

Reproduce this consolidation with `python scripts/consolidate_detector_evidence.py`. It reads committed result summaries only. For original analyses see [IMS findings](ims-independent-results.md), [paired candidate disposition](detector-candidate-disposition.md), and [evaluator instructions](../../runbooks/detector-performance-evaluation.md).

## Latest development increment

[Independent causal envelope candidate](sca-independent-causal-development.md) was recomputed from consumed native signals. Eligible coverage reaches 100%, but substantial normal-side positives remain. NOT_PROMOTED; runtime causality does not repair retrospective calibration or establish operational acceptance. Existing two-candidate acceptance results above remain historical for those exact candidates.

Latest attempted fix: [two-feature consensus](sca-feature-consensus.md) rejected after detecting zero of 211 eligible fault snapshots. The one-feature baseline was reproduced exactly. No deployment or holdout use.

Latest diagnostic: [feature separation and threshold sweep](sca-feature-separation.md) measures the false-positive/miss tradeoff. Increasing thresholds does not resolve both; sensor-side/label confounding limits interpretation. No threshold selected.

Current data feasibility finding: [reference audit](sca-reference-feasibility.md) confirms later-only normal DS references in cases 1/2 and no mixed-class same-side test groups. Next work is a chronology/reference audit of consumed IMS/LDM before fitting another candidate; repeated SCA threshold tuning will not resolve this evidence gap.

Latest chronology audit: [IMS/LDM reference feasibility](chronological-reference-audit.md) reproduces early LDM baselines and selects consumed B17 for a bounded causal trend experiment. Recorded setpoints are constant; healthy labels and physical failure timing remain unverified.

Latest candidate experiment: [B17 causal trailing median](b17-trend-development.md) reduced episodes 9 to 1 with a 2.48-minute delay relative to the recorded RMS baseline. This is descriptive consumed-run stability, not nuisance or failure-warning acceptance. NOT_PROMOTED.

Current trend result: [unchanged transfer to B04/B12](trend-transfer.md) yields one episode per run with roughly 2?3 minutes later first alerts; B17 decisions reproduce exactly. Increased flagged duration prevents a nuisance-reduction claim. Candidate remains NOT_PROMOTED.

Latest temporal check: [synthetic transient and clearance characterization](trend-temporal-characterization.md) shows delayed flags can begin after an eight-record pulse ends. No automatic healthy/incident-clearance interpretation is justified. Candidate remains NOT_PROMOTED.

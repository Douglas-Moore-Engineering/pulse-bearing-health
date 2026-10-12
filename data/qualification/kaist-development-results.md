# KAIST quality handling and development replay

This increment inspects all 129 recordings and applies an exploratory rule to the development trajectory. It does not promote the deployed detector or consume reserved UNSW or LDM test signals.

## Data handling

The [processing policy](../../config/kaist-development-policy.json) is versioned separately from the source data. Native bytes and row positions remain unchanged. Finite-only per-channel RMS is eligible only when each vibration channel has at most 0.1% non-finite samples and no missing block longer than 256 samples (10 ms at 25.6 kHz). These are provisional engineering limits informed by the initial native inspection, not validated sensor-quality requirements. No interpolation, zero filling or spectral concatenation across gaps is performed. Temperature is profiled but does not drive this rule.

The first inspected gaps are internal blocks, so removing a supposed trailing blank row would not solve missingness. The extra row is retained. For 2,000,001 rows, the first-to-last sample span would be 78.125 seconds at the documented rate; an inclusive endpoint is a possible explanation, not established source provenance. No row is discarded based on that hypothesis.

## Development rule

The first ten chronological recordings establish each vibration channel's median RMS reference. They are assumed reference data, not verified healthy exposure. A channel must exceed three times its reference in three consecutive eligible recordings. A bad-quality record or acquisition gap above 90 minutes resets persistence. Either channel may trigger an alert. The 90-minute limit is specific to these nominally hourly acquisitions; it does not change the deployed IMS rule's 15-minute limit.

The rule and quality limits were recorded before the complete profile results were available, but three snapshots and source documentation had already been inspected. This is development analysis, not a blinded holdout evaluation. Alert lead is measured to the last acquisition timestamp with unknown timezone. It is not lead to proven damage onset or to a precisely timed physical failure.

## Reproduction

1. Run `python scripts/profile_kaist_archive.py --all --archive outputs/reference-dataset-review/5hcdd3tdvb/Vibration_Bearing_RuntoFailure.zip --output governance/evidence/kaist-full-profile.json`.
2. Run `python scripts/evaluate_kaist_development.py`.

The profiler verifies the published archive SHA-256 and each member CRC, records member SHA-256, preserves dimensions, and records every missing block as a zero-based half-open index interval. The replay binds profile, policy and code hashes. Native archive data remains ignored by Git.

Tests cover reference isolation, persistence, missingness abstention, time-gap reset and rejection of non-finite derived features. The complete suite passed 89 tests. These checks establish software behavior, not statistical detector validity or nuisance-alert performance.

## Executed results

All 129 CSVs passed member CRC checks and have 2,000,001 rows by four columns. Every file contains non-finite values. Maximum missing counts per column are 80, 80, 82 and 82; maximum contiguous gaps are 40, 40, 41 and 41 samples. Thus every recording satisfies the provisional vibration quality limits. This does not resolve the cause of missing values or establish verified healthy exposure. [Complete profile](../../governance/evidence/kaist-full-profile.json).

The first ten recordings form the reference, leaving 119 monitoring recordings. The declared three-times-RMS rule produced one flagged recording, one episode, no abstentions and first flagged at 2022-06-26 01:00:31: the final acquisition itself. Observed lead is zero. It does not demonstrate the fictional 60-minute target on this development trajectory. [Replay evidence](../../governance/evidence/kaist-development-replay.json).

A subsequent development-only sensitivity comparison retained three-record persistence and changed only the ratio:

| RMS ratio threshold | Flagged recordings | Episodes | Lead to last acquisition |
|---|---:|---:|---:|
| 1.5 | 3 | 1 | 106 minutes |
| 2.0 | 3 | 1 | 106 minutes |
| 2.5 | 3 | 1 | 106 minutes |
| 3.0 | 1 | 1 | 0 minutes |

[Comparison evidence](../../governance/evidence/kaist-development-sensitivity.json) binds the code, source profile and base policy. The lower thresholds are candidates for further development; their 106-minute descriptive lead is not an independent validation result or an accepted failure-warning result. No nuisance-alert rate can be established from these flags without qualified healthy labels. The earlier missed IMS bearing remains unresolved. Next: compare candidate features and thresholds across development bearings before freezing validation, then test reserved experiments under the frozen protocol. No live API rule was changed.

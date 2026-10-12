# Chronological reference audit: IMS and LDM

**LDM B17 is suitable for a bounded chronological development experiment, not healthy/failure classification or production acceptance.** This audit reads already-consumed recorded feature inventories; it does not acquire signals, open holdouts or train a model.

For B04, B12 and B17, timestamp order is strictly increasing, the first 100 eligible reference observations precede monitoring, and recomputed per-channel medians match the prior replay references. Monitoring counts are 964, 667 and 2,633 respectively. [Hash-bound audit](../../governance/evidence/chronological-reference-audit.json).

B17 has recorded setpoints fixed at 2,700 rpm and 1,500 N across reference and monitoring. This reduces one recorded-condition complication, but does not prove actual conditions, calibration or health are constant. B04/B12 have varying reference conditions. Exact setpoint-pair novelty in the JSON is a diagnostic only: continuous setpoint values require a separately defined tolerance or conditioning scheme, so an exact mismatch is not itself out-of-domain evidence.

IMS run 1's existing report uses 100 early baseline snapshots and 2,056 monitoring snapshots with 24 excessive gaps. This audit references that report rather than claiming a fresh native replay. Reference health, amplitude units and timed physical endpoints remain unqualified.

## Bounded next experiment

Use B17's first 100 eligible observations only for an initial reference, then process later observations causally. Compare a robust trend/change statistic with the frozen 1.5x RMS baseline using identical windows, gaps and exclusions. Preserve both channels as one bearing; do not count them as independent failures. Report alarm timing, repeated episodes, coverage and time-to-record-end as descriptive outcomes only. Do not tune on future records while describing the run as independent validation.

B17 is consumed development evidence because its previous final-test results have already been inspected. An early baseline is not a verified healthy label; neither this audit nor a successful change detector can establish the nuisance requirement. Endpoint logs describe stopping conditions, not source-certified physical failure times. No event-level acceptance, trained production model or release is authorized by this selection.

Reproduce: `python scripts/audit_chronological_references.py`. Existing source hashes and replay lineage remain linked through the audited files. SCA cases 3?10 and other reserved data remain untouched.

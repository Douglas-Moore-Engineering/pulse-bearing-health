# Detector acceptance evaluator

Run from the repository:

```sh
python scripts/evaluate_detector_performance.py config/detector-evidence.synthetic.json
```

This example is entirely synthetic and intentionally passes to exercise the program. It is not an evaluated model. Replace the dossier with governed evidence before drawing a benchmark conclusion. Exit codes: 0 PASS, 1 FAIL, 2 INCONCLUSIVE. Malformed inputs fail as command errors; duplicate JSON keys and files over 4 MiB are rejected.

The dossier binds the exact policy version and provides unique event IDs, offset-aware alert/endpoint timestamps, endpoint and clock references, healthy operating-exposure blocks, per-regime eligible/abstention counts and evidence references. Use null alert for an eligible event without an alert; never omit missed events. Block indexes must identify predeclared nonoverlapping 720-hour blocks for each bearing.

Required evidence assertions are `unsupported_challenges`, `independent_causal_protocol`, `trace_replay`, and `evidence_review`. Each contains a boolean `satisfied` and supporting `references`. These assertions must come from actual documented review. The program does not fetch references, inspect their contents, verify signer authority, prove block nonoverlap or discover omitted events/regimes. Its PASS is conditional on the supplied dossier; it is not independent assurance. False assertions or cherry-picked input invalidate the result.

Missing endpoints, exposure, coverage or review assertions return INCONCLUSIVE; measured failures dominate incomplete criteria. Unresolved episodes count against nuisance acceptance. Fewer than the proposed minimum events/bearings cannot pass. An event whose endpoint interval crosses the warning threshold is inconclusive. Zero observed misses does not prove population reliability.

[Requirements](../requirements/detector-performance.md), [synthetic result](../governance/evidence/performance-evaluator-synthetic.json), and [test evidence](../governance/evidence/performance-evaluator-tests.xml). The 155-test suite includes pass, missing evidence, missed/late events, nuisance excess, low coverage, protocol failure, short exposure and duplicate-event rejection. Current real detector disposition remains NOT_PROMOTED. The evaluator never changes release gates, deploys a model or authorizes equipment action.

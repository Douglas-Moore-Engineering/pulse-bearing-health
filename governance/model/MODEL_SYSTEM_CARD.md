# Model and System Card — Exploratory baseline

Current increment, 2026-10-11: [IMS run 2 RMS evaluation](../../data/qualification/ims-run2-results.md) is executed offline with a frozen rule and per-member/code/plan hashes. One experiment, four channels, 984 snapshots; bearing 1 has one sustained anomaly episode starting three hours before the final snapshot. This is not a qualified fault predictor, independent held-out evaluation or RUL model. The deployed reference API continues to return detection unavailable; no candidate was promoted. Historical planning text below does not describe the current cloud runtime.

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

System: Pulse pre-Azure design v0.1. No model artifact, training data approval, numerical metrics or deployed endpoint exists. Intended population is bearing/run-qualified reference data; actual customer-site validity is not established.

Candidate anomaly/classification/RUL architectures are described in docs/05. Features, hyperparameters, thresholds, training environment, dataset/split digests and run manifests are TBD. Required later disclosures: labels and exclusions, independent group counts, leakage tests, metrics with uncertainty, unknown-class/domain behavior, RUL interval method, failure/censoring definitions and supported operational envelope. No GenAI or autonomous tools are in scope.

Human approval and manual fallback are design requirements, not tested safeguards. No measured performance, seven-day warning, savings, safety or certification claim is permitted from this card.

## Frozen-rule independent experiment outcome

[Run 1 evaluation](../../data/qualification/ims-independent-results.md) used unchanged threshold/persistence and a separate experiment with its own first-100 commissioning baseline. It flagged bearing 3 ten minutes before record end but missed documented damaged bearing 4. This rejects a general-detector readiness claim for this rule. Run 1 is now consumed evidence; new candidate tuning cannot retain an untouched-test claim. The third archive has unresolved identity/count differences. The live API retains explicit detection unavailability.

## Deployed unqualified reference capability

The fictional customer's simulated workflow is now implemented under `/v1/reference`; [live replay evidence](../evidence/azure-reference-detector-replay.json) reproduces the offline run-2 rule, one persistent episode and automated reference-client acknowledgement. This is a sandbox/reference capability, not promotion to a qualified degradation detector. The ordinary degradation endpoint continues to abstain. Unknown native units and source timezone are preserved; source hashes are verified during preparation but only caller-asserted at the API boundary. The frozen median is 0.07765955594342575 native units, with ratio >3 and three consecutive snapshots; gaps >900 seconds reset persistence. The failed independent-run findings remain binding evidence against production acceptance.

## RMS v2 final research disposition

[Final evidence](../../data/qualification/rms-v2-final-research.md) reports 132.4/195.9 minutes of descriptive lead on LDM B12/B17 with 26/9 episodes. Candidate NOT PROMOTED; physical-failure warning and nuisance criteria are not evaluable from current labels. This does not overturn the historical baseline failure or pass a production gate. The deployed rule remains unchanged.

## Detector endpoint audit - 2026-10-11

Implemented and tested uncertainty-aware endpoint and descriptive nuisance scoring. [Evidence and limitations](../../data/qualification/detector-gap-resolution.md). Published LDM stop logs provide conditional warning comparisons, not physical-failure labels. 103 tests passed. Thresholds, consumed splits, deployed reference rule and acceptance targets are unchanged; NOT_PROMOTED. Next work requires qualified event/healthy-exposure labels and prospective independent evaluation.

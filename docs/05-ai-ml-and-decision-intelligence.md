# AI/ML and Decision Intelligence

PULSE pre-Azure review v0.2 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

## Capability progression

1. Qualify signals and operating context; establish RMS/kurtosis baselines.
2. Compare baseline anomaly scoring against a 1D-CNN autoencoder candidate on explicitly defined normal training data; envelope-spectrum preprocessing is conditional on qualified sample rate, bearing geometry/speed and bandwidth.
3. Evaluate a fault classifier only where trustworthy fault labels and independent bearing/run groups exist.
4. Evaluate TCN/survival RUL candidate only with valid failure/censoring endpoints; report time units and intervals. A fault classifier or anomaly score is not an RUL estimator.
5. Present evidence, confidence/limitations, abstention and authorized human disposition; no LLM or autonomous agent is required in the numerical path.

These are proposed candidates, not selected/trained models. Keep feature preprocessing fitted on training only; selection uses validation; test is sealed until selection freeze. Source-level domain shift and small group counts are explicit limitations.

## Measurement plan

Anomaly: sensitivity and warning lead time at a frozen false-alert burden, measured per independent bearing/run/event rather than counting correlated windows as independent failures. Define lead-time units from the dataset time basis; no seven-day plant warning claim from accelerated test-rig data.

Diagnosis: confusion matrix, per-class precision/recall, macro metrics, calibration and unknown-class handling. RUL: MAE/RMSE, justified PHM-style asymmetric scoring, interval coverage/width and censored-run treatment. Freeze interval target coverage before evaluation; value currently TBD. Runtime: scoring latency, missing/stale-data behavior and artifact integrity. Business outcome: attributable stops/losses with covered-asset exposure and counterfactual, outside offline model metrics.

Report baseline/candidate results and uncertainty at bearing/run level. Failure to improve a baseline is a legitimate result. No numerical performance or feasibility claim exists yet; [model/system card](../governance/model/MODEL_SYSTEM_CARD.md) states those limitations.

## Training, registration and serving design — v0.2

See [training and registration](diagrams/04_model_lifecycle.svg) and [inference and monitoring](diagrams/04b_inference_monitoring.svg). Both describe future behavior; no registered model exists.

Preparation validates source units, sample rate, run identity and regime before segmentation. Assign bearing/run partitions first. Fit scaling and any learned preprocessing on training data only; apply those frozen transforms to validation, test and later inference. Envelope analysis and candidate network choices remain conditional on signal qualification. Track preprocessing code/configuration, fitted transform and feature schema as separate versioned artifacts.

Track each baseline/candidate run with code commit, environment lock or image digest, source/rights and split manifests, random seeds, parameters, metrics and limitations. Choose on validation, freeze thresholds and policy, then open the sealed test for the agreed evaluation. A failed test cannot become tuning data while retaining its held-out claim; material changes require a new governed evaluation disposition.

Register an eligible candidate under a unique model name/version and verified artifact digest; link its run and capability envelope. Record failed/rejected evidence without making it deployable. Registration alone supplies no exposure authority. Assemble the [release manifest](../governance/release-manifest.template.json) and carry exact preprocessing, feature schema, model, threshold, policy and environment versions through promotion. The artifact loader must reject a digest or signature/approval mismatch before deserializing; serialization format and dependency review remain required.

Inference checks input validity, freshness and supported regime, applies the released transforms, runs only enabled capabilities, and records either an advisory or an explicit unavailable result. Persist generating versions and evidence ID before human disposition. Reference outputs remain visibly unvalidated for a customer site. No runtime training, automatic model replacement, equipment command or real CMMS write is proposed.

## Monitoring and retraining decisions

| Signal | Owner and decision | Required evidence / response |
|---|---|---|
| Input quality, schema or freshness failure | Technical owner with reliability | Quarantine invalid records; unavailable output; investigate source before model change |
| Feature/regime drift or changed sensor setup | Dr. Moore proposes change; applicable data/domain owner reviews | Compare to versioned reference windows; qualify new regimes; thresholds/windows are TBD until baseline exists |
| False-alert burden or delayed outcome performance | Reliability and model owner | Use adjudicated bearing/run outcomes; no inference of recall from unlabeled drift metrics |
| Artifact mismatch, integrity issue or failed release | Release/security owner | Withdraw affected advisories and follow manifest-bound recovery in view 08 |
| New labels, dependencies, model/policy change or operating scope | Technical owner and release authority | Review impact, rights, cost and risk; requalify data, retrain if justified, repeat affected V&V and promotion gates |

A retraining trigger opens a reviewed change proposal. It neither approves compute spending nor promotes a model. Approved retraining returns to view 04 and then view 08; the inference loader receives only a newly authorized release. Performance thresholds, monitoring windows and review intervals remain candidate decisions, with closure before the affected exposure gate.

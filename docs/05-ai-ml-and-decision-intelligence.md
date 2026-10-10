# AI/ML and Decision Intelligence

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

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

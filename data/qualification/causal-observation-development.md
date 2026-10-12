# Causal observation context

Implemented [CausalObservations](../../src/pulse/causal_observations.py) as a separate offline development component. It consumes per-side threshold-normalized anomaly scores in timestamp order, and consults only the most recent earlier opposite-side observation within 60 seconds. It never revises an earlier result using a future observation. No API integration or deployment occurred.

Each sensor retains its own anomaly result. Both sensors can be anomalous simultaneously; the larger score no longer suppresses the other. Missing/stale partners are reported as unavailable without dropping the current anomaly. An unavailable current score is not a normal result. Duplicate same-sensor timestamps, out-of-order input, invalid sides and nonfinite/negative scores are rejected. An invalid current observation clears that side's usable partner context through its unavailable score.

Outputs explicitly retain `bearing_damage=UNDETERMINED` and `qualified_detector=false`. Anomaly is not a bearing diagnosis. This component removes future-data use and winner suppression from a possible streaming design; it does **not** solve spectral false positives, prove simultaneous-fault detection, or confer physical meaning on unresolved frequency coefficients. Restoring independent sensor anomalies also forfeits the earlier winner-selection false-positive reduction. Do not carry those paired-rule performance numbers over to this component.

Four targeted tests verify missing-partner behavior, preservation of both anomalies, stale/invalid context and rejection of reordering/duplicates. The complete suite passed **107 tests**, with one existing Starlette/httpx deprecation warning. [Test evidence](../../governance/evidence/causal-observation-tests.xml). No new dataset accuracy experiment was run in this increment; cases 3-10 remain reserved.

The [candidate non-promotion decision](detector-candidate-disposition.md) remains effective. Next model work concerns feature specificity and representative calibration; this implementation cannot manufacture missing physical labels, source-unit verification or operating exposure. Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001.

## Measured causal replay

[Replay program](../../scripts/replay_sca_causal.py) processed all 428 frozen case-2/11 decisions in chronological order and asserted that every anomaly decision was preserved. [Bound results](../../governance/evidence/sca-causal-replay.json). Binary decisions were encoded as scores 2/0 solely to exercise threshold context; no features were recomputed. Equal timestamps use deterministic DS-before-FS ordering, not established acquisition order.

| Case / side | Observations | Earlier partner available within 60 s | Positive decisions |
|---|---:|---:|---:|
| 2 / DS | 94 | 79 | 91 |
| 2 / FS | 296 | 12 | 129 |
| 11 / DS | 19 | 6 | 1 |
| 11 / FS | 19 | 13 | 0 |

Only 12 of 296 case-2 FS observations have preceding opposite-side context. This is substantially less than offline nearest-neighbour pairing because future observations are unavailable. No decision is discarded to improve apparent accuracy: all 129 normal-side positives remain. Context processing is verified, but the detector's false-positive problem is unchanged. A future buffering design must measure added latency and missing-partner behavior; it cannot inherit offline pairing results without replay.

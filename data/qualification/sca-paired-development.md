# Paired-sensor development experiment

Consumed cases 2/11 only; no independent validation or release promotion. [Program](../../scripts/evaluate_sca_pairing.py) and [results](../../governance/evidence/sca-paired-development.json). Input publisher hashes are rechecked and the frozen per-placement feature thresholds are reused unchanged.

## Like-for-like comparison

| Case 2: same 91 paired observations per side | Original rule | Paired rule |
|---|---:|---:|
| DS fault positives | 89 | 86 |
| DS fault misses | 2 | 5 |
| FS normal positives | 72 | 3 |
| FS normal negatives | 19 | 88 |

Three of 94 DS fault observations and **205 of 296 FS normal observations abstain** because they lack an eligible mutual-nearest partner within 60 seconds. They are not counted as normal, correct, or silently removed from the coverage denominator. DS coverage is 96.81%; FS coverage is 30.74%. Paired DS sensitivity is 86/91 (94.51%), while 86/94 (91.49%) of all fault observations receive a positive decision. The paired FS false-positive fraction is 3/91 (3.30%), not 3/296. These are correlated snapshot counts, not independent-bearing evidence.

Case 11 retains its original 1/38 normal-snapshot positives across two placements with complete pairing coverage. The experiment does not resolve the misalignment challenge.

## Rule and limits

Compute each sensor's maximum feature score divided by its own frozen feature threshold. A positive requires score above one and greater than the opposite sensor's score. Exact ties are negative. Matching uses mutual nearest timestamps within 60 seconds, not row position. The known `faultOrigin` field is not used in inference. Labels define scoring and exclude invalid/off records; a real runtime must implement independent validity checks without ground-truth labels.

This heuristic assumes relative score strength helps localize the anomaly; its scores are not calibrated probabilities or directly comparable physical damage magnitudes. It can suppress genuine simultaneous faults and close-score faults. That limitation must be tested or replaced before deployment. Nearest matching may use a later observation, so it is offline analysis, not a causal streaming implementation. Timestamp proximity does not prove stable conditions or synchronous sampling. Post-replacement calibration and unresolved frequency semantics remain inherited limitations.

The reduced false-positive count is not solely due to sample selection: the table compares identical matched observations. Nevertheless the full-data coverage loss is material, and sensitivity worsens. No nuisance-episode or physical-warning acceptance target is passed.

## Disposition

Paired localization is promising for further development but **NOT_PROMOTED**. Before reserved-case evaluation, define a causal pairing/timeout policy, a conservative policy for unmatched and potentially simultaneous-fault observations, and acceptable coverage/sensitivity tradeoffs. Investigate generalization on consumed case 1 rather than spending reserved cases to tune the heuristic. Cases 3-10 remain untouched. No Azure resources, API behavior or production gates changed.

Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001. Reproduce with `python scripts/evaluate_sca_pairing.py` with SciPy/NumPy available.

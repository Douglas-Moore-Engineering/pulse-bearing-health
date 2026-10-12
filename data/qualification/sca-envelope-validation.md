# Frozen SCA envelope diagnostic evaluation

**NOT PROMOTED.** Sensitivity improved over the earlier RMS development result, but the normal-snapshot false-positive burden is unacceptable as a basis for customer readiness. No numerical production nuisance gate is claimed evaluated: snapshots are not operating-day exposure.

| Case / placement | Fault detected | Fault missed | Normal flagged | Normal not flagged |
|---|---:|---:|---:|---:|
| 2 / DS | 91 | 3 | 0 | 0 |
| 2 / FS | 0 | 0 | 129 | 167 |
| 11 / DS | 0 | 0 | 1 | 18 |
| 11 / FS | 0 | 0 | 0 | 19 |

Case 2 DS fault-snapshot recall is 96.81%; FS normal-snapshot false-positive rate is 43.58%. Case 11 is the v2 shaft-misalignment challenge: 1/38 snapshots flagged across two placements, not 38 independent bearings. No excluded observations or feature/reference abstentions occurred in these files. Undefined class metrics remain undefined where the class is absent.

## Frozen method and integrity

[Protocol](../../config/sca-envelope-validation.json), evaluator, inherited feature code and source inventory were [hash-bound before acquisition](../../governance/evidence/sca-envelope-validation-freeze.json). Four downloaded files passed publisher SHA-256 verification. The [evaluator](../../scripts/validate_sca_envelope.py) rechecks those hashes and rejects changed frozen files. [Full results](../../governance/evidence/sca-envelope-validation.json) include timestamped labels/decisions and reference counts/thresholds. Reproduce with `python scripts/validate_sca_envelope.py` with SciPy and NumPy available.

The decision ORs inner-ring, outer-ring and ball feature exceedances, each calibrated to its placement's normal-train 99th percentile with at least 30 complete reference records. All features must be available; otherwise abstain. This tests a full multi-feature rule rather than reporting the feature that matches a known fault. There is no threshold retuning or persistence change after scoring.

The calculation follows the paper's shaft-Hz-multiple description. Physical coefficient interpretation remains unverified; no manufacturer-geometry confirmation or author clarification was obtained. The experiment is therefore a documented-interpretation diagnostic benchmark, not validated physical fault-frequency identification. Resolving this is still required before mechanistic claims or deployment.

## Independence and chronology

Cases 2 and 11 were previously signal-uninspected and are now consumed evaluation evidence. Calibration uses each publisher train segment, which is retrospectively after replacement; this is not a prospective warning experiment. Actual asset independence across cases has not been established. Do not pool placements or case numbers into an independent-bearing performance claim. Cases 3-10 remain reserved.

These results reveal normal-placement cross-response despite high fault recall. The cause is not established: possible explanations include transmitted vibration, operating-condition/reference differences, frequency interpretation or feature specificity. Do not assert a root cause from the confusion matrix alone.

## Next development and authority

Use consumed cases 1/2/11 to investigate false-positive timestamps, speed/reference distribution shifts, spectral selectivity and cross-placement response. Any revised detector needs a new freeze and evaluation on still-reserved data after asset-group review. Do not spend additional reserved cases to tune away the observed false positives. Preserve physical-warning and nuisance-exposure requirements; neither is passed here. No Azure image, release gate or budget changed.

Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001. Model engineering owns failure analysis; domain/release reviewers retain label and promotion authority.

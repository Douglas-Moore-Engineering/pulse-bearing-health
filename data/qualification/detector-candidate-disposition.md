# Detector candidate disposition

**Current RMS/envelope/paired candidate family: NOT APPROVED FOR PRODUCTION.** This concludes this candidate evaluation increment, not the original production objective. Do not continue consuming holdouts merely to produce a favorable result.

The final consumed-case check applied the same paired rule to case 1, using the existing normal-reference feature thresholds with no retuning:

| Case / side | Detected faults | Missed faults | Normal positives | Normal negatives | Abstained faults | Abstained normal |
|---|---:|---:|---:|---:|---:|---:|
| 1 / DS | 98 | 6 | 0 | 0 | 13 | 0 |
| 1 / FS | 0 | 0 | 1 | 103 | 0 | 22 |
| 2 / DS | 86 | 5 | 0 | 0 | 3 | 0 |
| 2 / FS | 0 | 0 | 3 | 88 | 0 | 205 |
| 11 / DS | 0 | 0 | 1 | 18 | 0 | 0 |
| 11 / FS | 0 | 0 | 0 | 19 | 0 | 0 |

Case 1 additionally excludes seven DS and nine FS off/missing-speed records. On its identical matched subset, original versus paired decisions change fault detections from 99 to 98 and normal positives from 11 to 1. Cases 2/11 reproduce the preceding results. [Machine-readable evidence](../../governance/evidence/sca-paired-development.json) binds the updated [program](../../scripts/evaluate_sca_pairing.py); source files remain publisher-hash checked.

## Why this is not a completed production detector

Pairing reduces normal positives but leaves material observations unassessed and introduces additional misses. It also assumes the larger relative anomaly identifies the damaged side, can suppress simultaneous faults, and uses future-neighbour matching. Calibration is retrospective after replacement. Physical frequency interpretation, actual operating exposure and precisely timed physical endpoints remain unqualified. These cannot be resolved by relabeling abstentions as healthy or replacing the original warning requirement with last-recording lead.

The original zero-missed-documented-failure target is event-level; snapshot misses alone are not an event-level failure count. Conversely, detecting some snapshots in a run does not establish acceptable event warning time. No event-level acceptance pass is inferred from this table.

## Concrete path to another candidate

Model engineering must implement causal observation handling and a multiple-fault-compatible localization method, with explicit unavailable decisions and coverage metrics. Before claiming mechanistic fault identification, the data/domain owner must resolve coefficient semantics and representative reference conditions from authoritative documentation or verified annotations. A revised protocol must be frozen before cases 3-10 are opened, with asset-group independence examined and real exposure/endpoint limitations retained.

An authorized shadow pilot can collect missing reference/operating/inspection context, but requires its own customer data/security and release decisions; no real customer or author contact has been authorized or performed here. Existing benchmark sources and unconsumed cases remain available for further research. This disposition is an engineering finding, not a fabricated independent review or customer signature.

The Azure reference service remains explicitly unqualified. No new candidate was deployed, no production gate was promoted, and no spending authority changed. Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001.

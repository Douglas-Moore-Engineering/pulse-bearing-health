# HUST bearing version 3: source review

Status: source metadata and publication inspected; native bytes uninspected. Owner: Dr. Moore. Review date: 2026-10-11.

The supplied signature expired October 9, 2026 at 18:39:18 UTC. The stable [Mendeley version 3 page](https://data.mendeley.com/datasets/cbv7jyx4p9/3) identifies DOI 10.17632/cbv7jyx4p9.3, published August 13, 2023, contributors Hoang Si Hong and Nguyen Thuan, and CC BY 4.0. Preserve attribution, license and change notices; signed URL credentials are not stored. Register as DS-HUST-DIAG, separate from run-to-failure candidates.

## Source observations

The repository describes 99 vibration records, five bearing types and three working conditions. The [associated primary paper](https://link.springer.com/article/10.1186/s13104-023-06400-4) describes artificially wire-cut defects, including single and paired faults. It reports 10-second captures at 51.2 kHz and additional run-up signals. Crucially, its MAT variable `fs` denotes shaft frequency; it must not be treated automatically as sample rate. The paper notes missing ball and inner-plus-ball cases for bearing 6204, variable crack depth, and excluded environmental/mechanical disturbances. These are reported properties, not verified file observations.

## Engineering disposition

Candidate purpose: fault classification and cross-condition/type robustness. The reviewed evidence does not establish lifetime trajectories, fault-onset times or RUL labels. Do not turn signal position or run-up duration into remaining life.

Before implementation, inventory version 3 and reconcile actual files, healthy/fault classes, run-up content and counts against the publication. Inspect MAT variables, physical units/calibration, sample lengths and acquisition-rate provenance. Derive grouping from physical specimen and acquisition identity; keep windows and repeated conditions from the same specimen together. A filename is not proof of an independent bearing. Freeze held-out conditions/types separately from specimen grouping and report class coverage gaps.

Preserve source and member hashes, schema/label mappings and attribution. No native adapter or waveform profile is claimed. Training, site transfer, independent assurance and deployment gates remain unresolved. Trace: PULSE-FR-001/002 provenance/contracts; PULSE-FR-004/005/006 capability eligibility; PULSE-NFR-008 split separation; AIG-REQ-001 version lineage.

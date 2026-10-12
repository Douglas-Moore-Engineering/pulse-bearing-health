# Reference feasibility and confounding audit

**The consumed SCA subset does not resolve the sensor/period confounding needed for an independent detector claim.** This is a data suitability finding, not proof that no useful model can be trained.

Inspected publisher-hash-verified train/test files for consumed cases 1, 2 and 11 only. Counts, label groups, native timestamp ranges and RPM ranges are in the [machine-readable audit](../../governance/evidence/sca-reference-feasibility.json).

| Case | Side | Healthy and fault records available | Both classes in test | All healthy records later than faults |
|---|---|---|---|---|
| 1 | DS | True | False | True |
| 1 | FS | False | False | False |
| 2 | DS | True | False | True |
| 2 | FS | False | False | False |
| 11 | DS | False | False | False |
| 11 | FS | False | False | False |

The DS positions in cases 1/2 have both normal and faulty records across files, but normal records occur strictly after fault records. Same position does not establish the same physical bearing or operating condition. No inspected publisher-test case/side group contains both classes. Labels therefore remain entangled with period and/or sensor position; the audit does not establish causation from RPM ranges and does not resolve load, intervention or calibration changes.

Do not use those later healthy records as a prospective commissioning baseline for earlier faults. Do not randomly split correlated snapshots and claim independent performance. Retrospective diagnostic training remains possible if explicitly labeled, but cannot establish operational warning or independent generalization from this design alone.

## Next experiment constraints

Before candidate fitting, identify an already-consumed source with documented same-sensor healthy-to-degradation chronology, stable units/calibration and an explicit event/exposure interpretation. Audit those metadata first and retain bearing/run groups. IMS and LDM remain possible sources to assess, not automatically qualified replacements. Train-only commissioning and any operating-condition normalization must precede evaluated observations.

For SCA, preserve cases 3?10 until a frozen protocol defines how group independence and reference timing will be handled. Metadata in an unconsumed case must not be silently treated as development access. No holdouts were opened in this audit, no model was fitted, and no deployed rule or acceptance criterion changed.

Reproduce with `python scripts/audit_sca_reference_feasibility.py` using the existing local consumed files. Native timestamps are compared within the source; timezone and physical-bearing identity remain unverified.

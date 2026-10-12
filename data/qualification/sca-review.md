# SCA bearing dataset v2: initial qualification

2026-10-11. **Useful candidate for labeled industrial fault detection and normal-snapshot false positives; not yet detector-tested or accepted for warning-time/operating-day claims.**

Source: [SCA bearing dataset, tdn96mkkpt v2](https://data.mendeley.com/datasets/tdn96mkkpt/2), Adam Lundstrom and Mattias O'Nils, CC BY 4.0. Cite the dataset and [Factory-Based Vibration Data for Bearing-Fault Detection](https://doi.org/10.3390/data8070115). The version-specific inventory records stable file URLs, sizes and publisher SHA-256 values in [source inventory](sca-source-inventory.json). Do not persist the user's temporary signed URL.

## What was executed

Recovered public file metadata using the publisher's browser API after direct requests returned 403/404. Downloaded case 1 train/test only, totaling 67,266,792 bytes, into ignored storage. Both publisher SHA-256 checks passed. Inspected the source paper and all four case-1 placement arrays; dimensions align and raw values are finite. [Native profile](../../governance/evidence/sca-case1-profile.json), reproduced by `python scripts/profile_sca_case1.py` with SciPy installed. Cases 2-11 have metadata inventoried but no signal files downloaded or inspected.

| File / placement | Records | Normal | Inner-ring fault | Off or missing speed |
|---|---:|---:|---:|---:|
| Case 1 train / DS | 127 | 122 | 0 | 5 |
| Case 1 train / FS | 127 | 122 | 0 | 5 |
| Case 1 test / DS | 124 | 0 | 117 | 7 |
| Case 1 test / FS | 135 | 126 | 0 | 9 |

All inspected waveforms have 16,384 samples at 640 Hz, in m/s^2. DS and FS timestamps differ and test record counts differ: never pair them by row index. Labels of -1 combine machine-off and missing-speed conditions; exclude from condition scoring and report separately rather than treating them as healthy negatives.

## Label quality and chronology

Paper sections 3.1 and 3.3 describe normal data after replacement, faults verified through bearing inspection when available and manual signal analysis, and labels assigned using envelope-spectrum fault frequencies. This provides labels independent of our RMS rule, but not universally independent physical inspections or precisely timed damage onset. The paper predates v2: use the v2 publisher correction for case 11, which now represents confirmed shaft misalignment while bearing labels remain normal.

Case 1 test runs January-May 2022 and train runs May-September 2022. Consequently, using publisher train data to calibrate this test is retrospective calibration from a replacement bearing, not prospective prediction. Case 1 DS test is already fault-labeled at its first eligible observation, so fault onset is left-censored. It cannot establish first-onset warning time.

Sparse observations spanning months are not verified continuous operating hours. We can measure false positives on labeled normal snapshots, while the one-episode-per-30-operating-days target still needs a justified exposure ledger. These are different metrics and must remain separate.

## Evaluation boundary and next engineering step

Case 1 is now development/schema-inspected. Reserve other cases until a case-grouped protocol is frozen. Related DS/FS measurements must stay in the same split; investigate repeated asset identities before assuming different case numbers are independent. Preserve case 11 as a non-bearing-fault challenge, with its distinct interpretation visible.

The existing three-record/900-second rule is unsuitable for sparse daily acquisitions: it would reset between ordinary observations. Define a separate SCA diagnostic protocol before scoring, including speed validity, units, channel treatment, retrospective calibration disclosure and cadence handling. Do not silently reuse that protocol to claim the deployed detector passed. Fault-frequency units also require checking before adding spectral features.

This dataset addresses the missing labeled-normal-data problem substantially better than unlabeled run-to-stop records. It does not by itself prove useful failure warning, nuisance episodes per operating day or transfer to a new customer site. No detector training, threshold selection, performance test, cloud change or release promotion occurred in this qualification increment.

Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001. Model engineering owns protocol preparation; domain/release reviewers retain label and acceptance decisions.

## Subsequent diagnostic experiment

The initial qualification above is historical. [Case 1 scoring](sca-case1-results.md) is now complete: 1/117 fault snapshots detected, 0/126 normal snapshots flagged. No acceptance or deployment promotion.

# IMS bearing dataset qualification review

Status: run 2 native numerical schema inspected and exploratory RMS evaluation executed; not training-qualified. Owner: Dr. Moore. Review date: 2026-10-11.

Current increment: [run 2 results](ims-run2-results.md) supersede the earlier statement below that no native measurements have been read. All 984 run 2 files were validated and evaluated. Runs 1 and 3, units, onset labels, independent-run generalization and downstream rights remain unresolved. Earlier packaging observations are retained as history.

The user supplied the [NASA-hosted download](https://phm-datasets.s3.amazonaws.com/NASA/4.+Bearings.zip). The [NASA PCoE repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) links this exact URL and attributes the experiments to IMS, University of Cincinnati. This updates existing DS-IMS; it is separate from LDM-UPB and the older Paderborn classification candidate.

NASA requests the citation: J. Lee, H. Qiu, G. Yu, J. Lin, and Rexnord Technical Services (2007), IMS, University of Cincinnati, Bearing Data Set, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA. The [NASA catalog](https://data.nasa.gov/dataset/ims-bearings) uses `other-license-specified` and links a government-works information page. Public hosting does not by itself resolve source-specific commercial or redistribution terms for this university-contributed dataset. Rights remain an open qualification condition.

## Packaging and integrity

The downloaded ZIP is 1,075,597,174 bytes. Its central directory contains a directory and `4. Bearings/IMS.7z`; the nested 7z is 1,075,320,408 bytes. The 7z inventory contains `1st_test.rar`, `2nd_test.rar`, `3rd_test.rar` and `Readme Document for IMS Bearing Data.pdf`. A direct ZIP-to-text adapter would therefore fail on this exact distribution. Downloaded bytes remain in ignored `outputs/reference-dataset-review/`, outside the committed review package.

See the [inspection manifest](ims-inspection.json) for observed sizes, locally computed hashes and integrity-check scope. The multipart S3 ETag is an object identifier, not a verified whole-file MD5. Local hashes support subsequent change detection; no independently published cryptographic digest has been verified.

## Observations from the bundled README

Both PDF pages were read and visually inspected. The documented rig has four Rexnord ZA-2115 double-row bearings on a shared shaft at 2,000 rpm with a 6,000 lb radial load. This is a different bearing/operating domain from the LDM-UPB ball-bearing experiments.

| Run | Documented files / channels | End-of-experiment observation |
|---|---|---|
| 1 | 2,156 / 8; two channels per bearing | Bearing 3 inner-race defect; bearing 4 roller-element defect |
| 2 | 984 / 4; one channel per bearing | Bearing 1 outer-race failure |
| 3 | 4,448 / 4; one channel per bearing | Bearing 3 outer-race failure |

These counts and labels come from the README, not measurement-file verification. Other bearings are not automatically negative examples or observed failures. Fault onset is unspecified. The PDF describes 20,480-point ASCII snapshots at 20 kHz while calling them one second; the arithmetic duration is 1.024 seconds. Preserve this discrepancy until resolved. It specifies nominal ten-minute recording intervals, except the first 43 files in run 1 at five-minute intervals, and attributes larger gaps to resuming on the next working day. Wall-clock lifetime must not silently equal active operating time.

The PDF does not state the stored numeric amplitude units or conversion factor. Accelerometer model identification alone does not establish the recorded signal scale. Numeric samples have not been read, and no IMS adapter, feature profile or training dataset is claimed in this increment.

## Remaining implementation and assurance

Inspect the native RAR measurement inventories and actual text schemas before implementing an adapter. Preserve run, physical bearing, channel, measurement timestamp and archive/member lineage. Resolve units and acquisition duration explicitly, rather than reusing LDM-UPB voltage calibration. Keep fault observations at their documented scope; do not invent per-window fault onset or label every bearing as failed at the experiment endpoint.

Split by independent experiment/physical bearing before constructing windows. Bearings recorded simultaneously on one shaft share operating conditions and may share signals; bearing-only splitting can leak experiment information. Define run-held-out evaluation separately, with the small number of independent runs made explicit. Resolve timestamp gaps, timezone, endpoint/censoring and event definitions before RUL targets or any model training.

Requirements: PULSE-FR-001/002 provenance/contracts, PULSE-FR-003 descriptive baselines, PULSE-FR-004/005/006 capability and target eligibility, PULSE-NFR-008 group separation, AIG-REQ-001 version trace. Cloud, data/model and site gates remain unchanged. No site validity, independent assurance or training performance is established by this inspection.

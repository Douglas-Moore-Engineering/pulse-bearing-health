# Additional LDM-UPB run qualification

2026-10-11. Documentation qualification only; detector acceptance remains blocked.

Inspected the logs, operating-condition CSVs, temperature CSVs and ZIP central directories for five additional runs from [Zenodo record 10868257](https://zenodo.org/records/10868257). Attribution: Osarenren Kennedy Aimiyekagbon, Paderborn University, CC BY 4.0; source and license details remain in [the source review](ldm-upb-review.md). No vibration members were downloaded or evaluated for these runs.

Total archive-range transfer was 1,893,977 bytes. All 15 selected members passed ZIP CRC validation and have recorded SHA-256 digests. Full archive checksums remain unverified. [Machine-readable evidence](../../governance/evidence/ldm-additional-run-qualification.json) records calibration, counts, timestamps, gaps and hashes. Native files remain in ignored local storage.

| Run | MAT inventory / rows in each CSV | Rate | Endpoint evidence | Reserved role |
|---|---:|---:|---|---|
| B03 | 614 | 128 kHz | Log reports housing temperature exceeding 110 C | Development, temperature-stop task |
| B04 | 1,114 | 128 kHz | RMS limit exceeded; numeric limit absent from log | Validation candidate |
| B11 | 1,953 | 64 kHz | Accelerometer limit exceeded; numeric limit absent | Development candidate |
| B12 | 767 | 64 kHz | Accelerometer limit exceeded; numeric limit absent | Reserved test candidate, same loading family as B11 |
| B17 | 2,733 | 64 kHz | Accelerometer limit exceeded; numeric limit absent | Reserved test candidate, different loading regime |

Every log specifies 10 g/V, zero dB gain and 1.6-second acquisitions. Each pair of CSVs has identical, strictly increasing timestamps and counts matching its MAT inventory. This does not yet verify MAT contents or measurement-index joins. Timestamps have no timezone.

B03's log describes a warm-up, but its first recorded operating row is already approximately 2,793 rpm and none are below 1,500 rpm. Do not invent ten minutes of recorded warm-up. B04 contains 50 low-speed rows and a documented temperature-dependent operating-policy decision after one hour. B11, B12 and B17 explicitly have no warm-up; their first CSV timestamps precede the minute-resolution logged start by approximately two to three minutes. Use source timestamps for chronology and preserve the log discrepancy.

## Prospective partition and endpoint policy

The accompanying [partition record](ldm-prospective-split.json) assigns entire bearings, both channels and all windows together before signal inspection. B02 is development because its signal samples have already been inspected. IMS runs 1 and 2 remain consumed development data. B12 and B17 are reserved from signal-based tuning; their documentation and context CSVs have been inspected, so they are not wholly unseen data. Their eventual results must be reported separately by loading regime, not pooled into a generalization claim.

These assignments are prospective research controls, not independently approved qualification. No run may migrate from development to test. Changes or evaluation access require a dated record; a test used for tuning is consumed and needs a new holdout.

For B03, the research target may be warning before the documented temperature-stop event, using the final recorded timestamp as an explicitly approximate endpoint. It is not damage onset or physical failure. For the four vibration-stop runs, exact threshold and stop-rule reconstruction remain unresolved. A last-record warning metric may be reported descriptively, but must not be called a validated failure-warning metric. Do not infer numeric thresholds from the generic 6-10 g range.

## Remaining work

1. Acquire and verify complete development runs, then implement per-run MAT/schema/index checks and operating-condition joins. Current work verifies documentation members only.
2. Freeze preprocessing, detector parameters, endpoint treatment and the evaluation protocol before opening reserved test signals. Compare condition-aware features against the frozen RMS baseline on development data.
3. Obtain verified healthy operating exposure to assess the fictional nuisance-alert criterion. Early portions of these accelerated degradation runs are not verified healthy negatives.
4. Evaluate reserved runs once after the protocol is frozen. The 60-minute warning and zero-missed-event targets remain unmet; no acceptance target was weakened.

No additional Azure resource, training job, deployment change or external notification was made in this increment. Trace: PULSE-FR-001/002/003, PULSE-NFR-008 and AIG-REQ-001.

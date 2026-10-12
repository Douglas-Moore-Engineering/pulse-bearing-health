# RMS candidate v2: reserved validation evaluation

The [protocol](../../config/rms-v2-validation-protocol.json) and its [hash freeze](../../governance/evidence/rms-v2-validation-freeze.json) were recorded before acquiring or inspecting LDM B04 and UNSW Test 2 signals. Existing source documentation and B04 operating context had already been reviewed. The selected 1.5x threshold and three-record persistence were not tuned on these validation signals. This is engineering validation assistance, not independent human assurance.

## Frozen interpretation

B04 uses a per-channel median of the first 100 eligible records. Warm-up/idle records with set speed below 1,500 rpm or no positive dynamic load are excluded and reset persistence. The reviewed calibration is 10 g/V at zero dB gain; expected acquisition is 204,800 samples at 128 kHz. Acquisition gaps above 900 seconds reset persistence. Operating load/speed variation remains a confounder because the candidate does not normalize operating conditions.

B04's contiguous MAT measurement ordinal is joined to the corresponding context row. This mapping is inferred from naming and counts, not independently proven. Reported warning lead is therefore descriptive time to the final acquisition, not qualified time to physical failure. The specific vibration stop limit remains undocumented. The 60-minute target can be compared descriptively but cannot receive final acceptance from this proxy.

UNSW Test 2 uses only its complete 6 Hz sequence, ordered by shaft cycle. The first ten records establish the reference. Signals at other speeds are excluded from evaluation. Native volts are retained because relative ratios do not require an amplitude conversion. No wall-clock timestamps or time-gap assumptions are invented: three-record persistence is sequential, and warning minutes cannot be scored. End-of-record cycles are not physical failure labels.

Both inputs require finite native channels and expected schema. Archive checksums and member hashes bind numerical evidence to the supplied versions. No invalid record is silently repaired. Either vibration channel can trigger the bearing-level alert; channels are not independent bearings. Reproduction uses `python scripts/validate_rms_candidate.py ldm_b04` and `python scripts/validate_rms_candidate.py unsw_test2` with the downloaded verified archives and extracted UNSW sequence.

## Executed results

Both validation archives passed their publisher checksums: B04 MD5 and UNSW Test 2 SHA-256. Total acquired compressed bytes were 5,870,402,634. [Acquisition and partition-access evidence](../../governance/evidence/rms-v2-validation-acquisition.json). All 1,114 B04 vibration members passed CRC, shape, finiteness and sample-time checks; all 167 selected UNSW measurements passed native channel checks. No test-partition signals were accessed.

| Measurement | LDM B04 | UNSW Test 2, 6 Hz |
|---|---:|---:|
| Native measurements evaluated | 1,114 | 167 |
| Warm-up/regime exclusions | 50 | 0 |
| Reference measurements | 100 | 10 |
| Monitoring measurements | 964 | 157 |
| Bearing-level flagged measurements | 663 | 41 |
| Bearing-level episodes | 3 | 2 |
| First flagged identity | M0446 | Shaft cycle 1,620,147 |
| Descriptive lead to last acquisition | 208.25 minutes | Not scorable in minutes |

B04's first flag was 2021-11-17 14:58:43, with final acquisition at 18:26:58 (timezone unknown). Both channels independently satisfied persistence at that first flag. Channel-level flag totals are 661 and 663; these are not two independent bearings. This exceeds 60 minutes **only against the descriptive final-acquisition proxy**. A sustained alert is not automatically a nuisance alert, and the three episodes cannot be classified without qualified condition labels.

UNSW first flagged the horizontal channel at cycle 1,620,147. All 41 flagged measurements are horizontal; the vertical channel has none. No warning duration, failure recall or nuisance-alert rate is inferred from those observations.

Full evidence includes native member hashes, features, decisions, frozen-protocol and executed-code hashes: [B04 replay](../../governance/evidence/ldm_b04-rms-v2-validation.json) and [UNSW replay](../../governance/evidence/unsw_test2-rms-v2-validation.json). The complete software suite passed **92 tests**, including warm-up exclusion, persistence reset and prevention of invented time lead; [test evidence](../../governance/evidence/rms-v2-validation-tests.xml). Repository consistency validation passed separately.

Disposition: signal-based validation replay completed without retuning. The candidate shows sensitivity on both validation sequences, but it is **not accepted for deployment**: the endpoint-warning interpretation and nuisance-alert target remain unresolved. These validation results are now inspected and must not later be described as unseen test evidence. The next assurance work is endpoint/condition-label qualification and an explicit final-test scoring protocol, rather than threshold tuning on these runs.

## Acceptance boundary

No verified healthy labels are available to score nuisance alerts. A successful signal replay, or an early alert relative to the final acquisition, cannot close that acceptance gap. Tests UNSW 3/4 and LDM B12/B17 remain reserved. No thresholds may be changed during this evaluation; a later revision needs a new recorded development decision and must acknowledge consumption of these validation results.

The deployed reference rule is unchanged. No Azure resources, cloud training jobs or external notifications are part of this increment. Trace: PULSE-FR-003, PULSE-NFR-008 and AIG-REQ-001.

Subsequent evaluation: [LDM B12/B17 final research results](rms-v2-final-research.md) supersede their reserved status above. Both descriptive lead proxies exceeded 60 minutes; neither operational acceptance target is established. UNSW Tests 3/4 remain reserved.

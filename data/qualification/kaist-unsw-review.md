# KAIST and UNSW acquisition and qualification

2026-10-11. Authorized local research increment; no cloud resources or live detector changes.

## Sources and partitions

The user supplied KAIST [5hcdd3tdvb version 6](https://data.mendeley.com/datasets/5hcdd3tdvb/6) and UNSW [h4df4mgrfb version 3](https://data.mendeley.com/datasets/h4df4mgrfb/3). Both source records specify CC BY 4.0. Attribution: KAIST contributors Wonho Jung, SungHyun Yun, Junho Kim and Yong-Hwa Park; UNSW contributors Hengcheng Zhang, Pietro Borghesani, Siyuan Zhuang and Zhongxiao Peng. Preserve attribution, license and processing history with derived artifacts; no endorsement is implied.

[Source inventory](kaist-unsw-sources.json) records stable file URLs, exact versions, byte lengths and published SHA-256 hashes. Expiring signed URLs are not retained. Raw data stays in ignored local storage.

The [prospective split](kaist-unsw-split.json) was recorded before signal inspection: KAIST and UNSW Test 1 are development; UNSW Test 2 is validation; Tests 3 and 4 are reserved for testing. All channels, speeds and windows from an experiment stay together. The latter three archives are not acquired in this increment. This is a research partition, not evidence of independent human review or detector acceptance.

## KAIST interpretation

The publisher lists one 4,325,053,806-byte ZIP. Its central directory contains 129 CSVs. The [authors' paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11039934/) identifies four columns: horizontal and vertical acceleration in g, bearing temperature and ambient temperature in degrees Celsius. Acquisitions are 25.6 kHz and 78.125 seconds. Native inspection found no CSV header, so the first row must remain a sample.

The experiment alternates five minutes operating and fifteen minutes resting. The paper uses the expression working hours while the published acquisition timestamps span roughly 128 elapsed hours. Do not equate elapsed, active operating and recorded signal exposure. The stated stop combines temperature above 85 C and vibration above 9 m/s^2; its exact vibration statistic must be resolved before reproducing that stop rule. Damage is documented after testing, not labeled at every window. A single trajectory cannot supply independent train/test bearings.

## UNSW interpretation

The downloaded README passed its published SHA-256 check. It documents acceleration channels in volts and sensor sensitivity 10 mV per m/s^2: nominal conversion is 100 m/s^2 per volt, subject to any acquisition gain verification. Load-cell sensitivity is 2.8 kN/V. Use each MAT file's Fs for sample rate; the speed suffix in filenames is shaft frequency, not sampling frequency.

Names encode shaft running cycles and speed. Each experiment contains a 6 Hz sequence plus selected measurements at 6, 12, 15 and 20 Hz. These are related samples from the same experiment, not additional independent bearings. Cycle differences divided by a single speed do not establish elapsed time across speed changes or interruptions.

The README cites Zhang et al., DOI 10.1016/j.ymssp.2021.108466, and Zhuang's 2021 thesis for experiment details and spall photographs. Initial condition, endpoint and progression labels need those details before claiming early fault warning or verified healthy exposure.

## Executed native checks

UNSW Test 1's complete 1,679,267,821-byte archive matches the published SHA-256. All 108 extracted MAT files passed finite-value and shape checks for acceleration, encoders, load cell and tachometer. Each contains 614,400 samples at 51,200 Hz (12 seconds). There are 80 files in the 6 Hz sequence and 28 in the multiple-speed group; all 108 file hashes are distinct. Native acceleration RMS ranges are 0.00742848-0.22174934 V horizontally and 0.01644079-0.26869204 V vertically across all measurements and speeds. These are descriptive statistics, not degradation labels or detector performance.

Reproduce with `python scripts/profile_unsw_test1.py --source outputs/reference-dataset-review/h4df4mgrfb/test1-native --output governance/evidence/unsw-test1-native-profile.json` after acquiring and verifying the pinned archive. [Native results](../../governance/evidence/unsw-test1-native-profile.json) retain per-file hashes, speed, cycles and RMS values. [Acquisition evidence](../../governance/evidence/kaist-unsw-acquisition.json) records downloaded file hashes.

KAIST archive filenames span 128 elapsed hours; adjacent timestamps differ by 2,760-4,320 seconds (median 3,600), so even the nominal hourly spacing is not uniform.

The complete KAIST archive passed its published SHA-256 check. The first, middle and final CSVs passed member CRC checks and were profiled using `scripts/profile_kaist_archive.py`. All three have **2,000,001 rows and four columns**, rather than the nominal 2,000,000 samples implied by the source duration and rate. The first and middle each contain non-finite counts `[40, 40, 82, 82]` by column; the final contains `[80, 80, 41, 41]`. These are actual source-data findings, not acquisition corruption inferred from a failed checksum. The precise cause is unresolved. [Native profile evidence](../../governance/evidence/kaist-native-profile.json) explicitly reports finite-only descriptive statistics without imputing or admitting the signals to a detector. The other 126 CSV contents have not yet been profiled. Define and test missingness handling and reconcile the extra row before detector use.

The complete verified downloads total 6,004,341,592 bytes, including the UNSW README. Existing 84 tests passed; these regression tests do not establish dataset labels or detector performance. Both profiling scripts were exercised on native data, and repository document/register validation passed.

## Acceptance boundary

These datasets are usable for development and evaluation. Remaining interpretation work does not prohibit analysis. It does prohibit calling unverified labels, partial signal checks or tuned development results an accepted detector. Existing 60-minute warning and nuisance-alert targets remain unchanged. No production gate advances from acquisition alone.

Trace: PULSE-FR-001/002/003, PULSE-NFR-008 and AIG-REQ-001. Return native acquisition evidence and interpretation limits to the engineering handoff before detector promotion.

## Subsequent full KAIST development run

The initial three-snapshot inspection above is superseded in coverage by the [full 129-record inspection and replay](kaist-development-results.md). All recordings meet the declared provisional missingness limits. The three-times-RMS rule flagged only the final acquisition; lower development thresholds gave 106 minutes of descriptive lead. No detector acceptance or deployment change is claimed.

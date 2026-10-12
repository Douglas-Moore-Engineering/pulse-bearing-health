# LDM-UPB run-to-failure candidate review

DS-LDM-UPB-RTF · Review v0.1 · 2026-10-11 · Owner: Dr. Douglas Moore

Disposition: **source documentation and a bounded B02 sample inspected; training qualification incomplete**. No model training, Azure activity or site inference was performed. This record advances the existing data-qualification work under [PULSE-CHANGE-001](../../customer/08-deployment-execution.md); it does not pass CLOUD-02, G0 or AIG-G3.

## Source identity and permitted-use evidence

The user supplied the [dataset description PDF](https://zenodo.org/records/10868257/files/LDM_UPB_Run-to-failure_data_set_of_ball_bearings.pdf?download=1). The [version-specific Zenodo record](https://zenodo.org/records/10868257), DOI `10.5281/zenodo.10868257`, names Osarenren Kennedy Aimiyekagbon and Paderborn University's Chair of Dynamics and Mechatronics. This is a separate collection from `DS-PADERBORN`, the older KAt fault-classification candidate; do not inherit that candidate's noncommercial license restriction or its short-record limitations.

The retrieved [Zenodo API metadata](https://zenodo.org/api/records/10868257) reports `cc-by-4.0` and open access. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) permits reuse and adaptation, including commercial use, subject to its terms, including attribution, a license link and indication of changes. Preserve the creator/title/DOI, license and processing history in derived artifacts; do not imply endorsement. The record also requests citation of [Javanmardi et al., 2024](https://doi.org/10.36001/phme.2024.v8i1.4101). This is inspected source-license evidence, not a completed assessment of every possible deployment obligation.

Metadata inconsistency: API `version` is `2023-04-02`, while publication date and description revision refer to `2024-04-02`; the PDF cover is dated March 25, 2024, v2. Bind acquisition to record ID, exact filenames and checksums rather than silently repairing or relying on the inconsistent version label.

The description PDF's published MD5 was verified: `7c6535acb48e620cb37b0f040cb9f83a`. Its locally computed SHA-256 is `949c855fa0cc6d2b12c83b476a03b7ab9498cf2ee4219ef50004e21ae0dd1b80`. See the [source and inspection manifest](ldm-upb-10868257.json) for source metadata, file inventory, hashes and evidence limits. Downloaded PDFs, CSVs and waveforms remain in ignored local inspection storage, not Git.

## Documented data and label constraints

The nine-page PDF describes 17 experiments, B01-B17, with no artificially initiated defects. Bearings are type 61806-2RS. Speeds and loads vary within experiments. B01-B06 use sinusoidal dynamic loading; B07-B17 use Gaussian excitation. Two vibration channels, operating conditions and temperatures are provided. These accelerated test-rig conditions are not evidence of compatibility with Pulse's fictional plant.

The PDF describes 1.6-second acquisitions, 128 kHz through B09 and 64 kHz from B10. Native MAT variables are `accHorizRear_A`, `accHorizFrontal_C` and `measTime`; vibration is in volts. Use each experiment's log for calibration and gain. Do not apply a blanket g conversion to every bearing or confuse sample rate with instrument bandwidth: the documented accelerometer's 3 dB frequency range ends at 10 kHz despite the higher digital Nyquist frequency.

Endpoint review is mandatory:

| Experiments | Documented endpoint | Qualification treatment |
|---|---|---|
| B01 | No preset stopping criterion | Exclude from ordinary observed-failure regression until the log establishes a defensible endpoint |
| B05 | Deliberately interrupted | Candidate right-censored run; do not label the final measurement as observed failure without further evidence |
| B16 | Table 3 has no threshold criterion | Endpoint unresolved; inspect its log before assigning event/censor status |
| Other runs | Vibration or temperature threshold listed | Inspect each log for actual threshold, interruptions, rule changes and timing before labeling |

The final dismantling findings identify inner-race, outer-race and ball defects, sometimes jointly. They are run-level post-test observations, not ground-truth fault onset or per-window class labels. A threshold-defined stop is not necessarily physical seizure. Predictive RUL claims must name the exact event being forecast.

## Actual B02 inspection

Only selected members were fetched using bounded HTTP byte ranges. Transfer for the archive inspection was **4,804,475 bytes**. The archive central directory lists 1,120 entries including 1,116 MAT files. The log, two CSVs and first/last MAT measurements were read. ZIP member CRC checks passed and local SHA-256 values were recorded. **The full B02 archive MD5 was not verified**, because the complete archive was not downloaded; this does not establish whole-run integrity or completeness.

Observed facts:

- Both sampled MAT files contain two finite float64 acceleration arrays and a finite time vector, each shaped `(204800, 1)`. Time spans 0 to 1.5999921875 seconds with a 1/128000-second increment. `measTime` is within-measurement relative time, not elapsed lifetime or UTC.
- The B02 log specifies 128 kHz, 1.6 seconds, 10 g/V and 0 dB gain. This calibration is supported for B02 only.
- Both CSVs contain 1,116 rows and identical, increasing `Time` values, from `25-Oct-2021 08:59:35` to `25-Oct-2021 14:36:36`. They contain no timezone. Do not append `Z` or claim UTC.
- Elapsed wall-clock time is 20,221 seconds. Consecutive recorded timestamps have minimum/median/maximum gaps of 11/18/282 seconds, with no duplicates or nonpositive gaps. The longest gap follows 13:32:36. A constant 12-second multiplier would misstate elapsed time.
- Actual CSV headers differ from the general description: `Time` replaces `dateTime`, and temperature includes `Mean Room Temp. / °C`. An adapter must validate observed schemas instead of silently assuming the PDF's illustrative names.
- The first 51 operating-condition rows have set speed below 1,500 rpm. The log describes a ten-minute warm-up at 750 rpm and 2,500 N with no dynamic load. Warm-up needs a distinct regime flag; it must not masquerade as normal data at the documented main-test range.
- The log reports stopping at 13:32 after two exceedances of 0.65 V RMS, then continuation with four allowed exceedances, finishing at 14:36. Event definition and active-time versus wall-clock lifetime need an explicit decision; the first threshold crossing, restart and final stop are different facts.

The two sampled records do not establish performance, time-series continuity, four threshold crossings or the integrity of unsampled measurements. No missing sample or intermediate label has been invented.

## Implemented sample adapter

`src/pulse/ldm.py` now verifies the five pinned native members, validates actual CSV headers and aligned timestamps, checks MAT shape/finiteness/sample timing, and applies the reviewed B02 calibration. It produces RMS/kurtosis with native, calibration and context hashes. The first/last sampled measurements produced four channel records. UTC, fault labels and RUL remain unavailable; ordinal-to-CSV mapping is explicitly provisional. This separate inspection tool does not admit data into the JSON-window harness or train a model.

Install with `python -m pip install -e ".[test,data]"`, then run `python scripts/profile_ldm_b02.py --source-dir outputs/reference-dataset-review/B02-sample --output outputs/reference-dataset-review/B02-adapter-profile.json` against the inspected local members. The output path must be new. Downloads are not automatic. See [adapter validation evidence](../../governance/evidence/ldm-adapter-validation.json): 31 tests passed, comprising 24 existing reference tests and seven adapter tests. These tests use generated fixtures; the native sample profile is separate evidence.

## Engineering return and next implementation

1. Keep this as a distinct dataset ID and preserve experiment, measurement and channel identity, archive/member hashes, calibration-log hash and source-license reference.
2. Inventory and verify complete selected runs before training. The source lists 48 ZIP files totaling 152,006,165,557 bytes, excluding the PDF; this is a published compressed inventory, not measured extracted storage or Azure workload. Start with a bounded set of endpoint-qualified runs rather than assuming the entire collection is needed.
3. Extend the implemented B02 sample adapter only after reviewing each run's calibration and schemas. Complete timestamp mapping, interruption/missingness checks and operating-condition joins for whole runs. Preserve native byte provenance. The current JSON-window harness is not a qualified native-source adapter; do not overwrite native provenance with a JSON surrogate checksum.
4. Establish bearing-disjoint partitions before windows. Keep both channels, all measurements and multipart archives for a bearing in the same partition. Freeze validation/test handling before fitting preprocessing or choosing thresholds. Seventeen runs provide far fewer independent examples than the number of signal windows.
5. Record endpoint/censor decisions with reviewed log evidence. Derive elapsed-time or active-operating-time targets only after a declared policy; do not assign `last_index - current_index` as RUL hours. Test both ordinary within-regime evaluation and held-out loading regimes as separate claims.
6. Evaluate descriptive and statistical baselines first; learned models and interval calibration follow only after qualified splits/labels and frozen criteria. Public test-rig RUL remains unvalidated for the customer site.

Requirement trace: PULSE-FR-001/002 for provenance and contracts; PULSE-FR-003 for baselines; PULSE-FR-004/005/006 for capability/label/RUL eligibility; PULSE-NFR-008 for bearing separation; AIG-REQ-001 for version trace. Dr. Moore owns remaining qualification and endpoint decisions. Existing cloud-account, cost, architecture and independent-review conditions remain open.

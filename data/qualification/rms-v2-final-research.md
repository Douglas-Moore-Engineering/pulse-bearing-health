# Frozen final research test: LDM B12 and B17

The unchanged 1.5x RMS candidate is evaluated on the two previously reserved LDM bearing runs. [Protocol](../../config/rms-v2-ldm-final-protocol.json) and [freeze evidence](../../governance/evidence/rms-v2-ldm-final-freeze.json) precede signal acquisition and inspection. Documentation/context had been inspected previously. The same per-channel median of the first 100 eligible records, three-record persistence and 900-second gap reset used for B04 are retained. No threshold selection or retuning occurs on these final signals.

## Endpoint review and claim boundary

The local published logs for B12 and B17 state that the accelerometer limit was exceeded and give stop times to the minute. They specify 64 kHz, 1.6-second acquisitions, 10 g/V and zero dB gain. They do not establish the exact damage-onset time, the numeric run-specific stop limit or intervals of verified healthy operation. The naming-to-context join remains ordinal-based and inferred.

The final-test scoring endpoint is explicitly the last acquisition timestamp. A 60-minute comparison is a **descriptive research proxy**, not a replacement for the customer's warning target and not acceptance of physical-failure prediction. False/nuisance-alert rate remains unscorable without verified healthy labels. Multiple channels, windows and alert episodes are not independent bearings.

The [UNSW source record](https://data.mendeley.com/datasets/h4df4mgrfb/3) describes shaft-cycle-indexed measurements and multiple speeds. The cited journal full-text request returned HTTP 403; the legacy thesis download returned HTML rather than a PDF. Those retrieval attempts did not resolve elapsed-time or healthy-condition labels. UNSW Tests 3 and 4 therefore remain reserved; they are not consumed merely to produce more alert counts. Source-access limitations do not mean the datasets are unusable.

B12 is a separate bearing in the variable-speed Gaussian loading family; B17 has a different loading/speed regime. Report each separately. Neither establishes general site performance, even if its descriptive proxy exceeds 60 minutes. Early reference segments are not relabeled as known healthy. A high flag count is neither automatically true degradation nor automatically a nuisance event.

## Reproduction and release decision

After downloading and verifying each archive against its version-specific published checksum, run `python scripts/test_rms_candidate_ldm.py B12` and `python scripts/test_rms_candidate_ldm.py B17`. The program reuses the frozen validation replay code, checks contiguous native measurement IDs, aligned context, sample rate, shapes and finiteness, and records member/code/protocol hashes. Native bytes remain ignored by Git.

Both results must be recorded, including misses and late flags; there is no selection of the better run. If either run misses the descriptive target, record that research failure without adjusting the threshold. Passing the descriptive proxy would still leave endpoint and nuisance criteria unresolved. No automatic deployment is authorized by this protocol. The live reference rule remains unchanged.

Trace: PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001. These final-test signals become consumed evaluation data once inspected; a later tuning decision cannot restore their unseen status.

## Final results

Both complete archives passed publisher MD5 verification; [acquisition evidence](../../governance/evidence/rms-v2-final-acquisition.json). All 767 B12 and 2,733 B17 measurements passed native shape, finite-value and sample-time checks. No regime records were excluded. The first 100 records per bearing supplied the reference.

| Run | Monitoring records | Flagged records | Episodes | First flag | Lead to last acquisition |
|---|---:|---:|---:|---|---:|
| B12 | 667 | 572 | 26 | 2022-08-24 09:09:59 | 132.4 min |
| B17 | 2,633 | 514 | 9 | 2022-11-04 22:12:37 | 195.9 min |

Timestamps have unknown timezone. Both descriptive 60-minute proxies are met, with no retuning. Full per-member hashes, features and decisions: [B12 evidence](../../governance/evidence/ldm-B12-rms-v2-final.json), [B17 evidence](../../governance/evidence/ldm-B17-rms-v2-final.json). Many repeated episodes indicate a stability concern, not a proven nuisance-event count; operating-condition confounding remains unresolved.

**Disposition: NOT PROMOTED.** [Machine-readable decision](../../governance/evidence/rms-v2-final-disposition.json) separates research proxy results from unscorable physical-failure warning and nuisance-alert targets. The live 3x reference rule remains unchanged. The software suite passed 92 tests and repository validation passed.

B12/B17 are now consumed final-test evidence for this candidate. UNSW Tests 3/4 remain reserved. Any future use of these results for operating-condition normalization, hysteresis or threshold changes is development work and requires fresh independent evaluation. [Required acceptance evidence](alert-acceptance-evidence-needed.md) specifies event timing and verified healthy exposure without changing the original targets.

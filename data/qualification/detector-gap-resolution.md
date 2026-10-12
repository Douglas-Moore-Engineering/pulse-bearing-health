# Detector acceptance gap: endpoint audit

2026-10-11. PULSE-FR-003, PULSE-NFR-008, AIG-REQ-001. Owner: model engineering; receiving roles: domain reviewer and release authority. **Partial engineering improvement; detector qualification remains blocked.**

The new [metric evaluator](../../src/pulse/detector_acceptance.py) separates missing endpoint evidence, absent alerts, late alerts and timing uncertainty. It also reports descriptive nuisance-rate bounds while retaining unresolved episodes. It cannot certify input labels or authorize release. Seven targeted cases cover uncertainty crossing the target, conservative timing, missing labels versus misses, late alerts, unverified/short exposure, unresolved episodes and invalid inputs. The full suite passed 103 tests; [test record](../../governance/evidence/detector-acceptance-tests.xml).

## Better endpoint evidence from existing data

Reviewed the published B04/B12/B17 experiment logs already held in the ignored dataset directory. The logs identify accelerometer-limit stopping events, with timestamps to the minute. [Publisher record](https://zenodo.org/records/10868257). The audit binds each extracted log and original replay by SHA-256, checks the transcribed timestamp occurs in the log, and preserves the frozen candidate results unchanged.

| Bearing | First alert to logged stop, assuming +/- 60 seconds | Interpretation |
|---|---:|---|
| B04 | 206.28-208.28 minutes | More than 60 minutes before logged stop under stated assumptions |
| B12 | 131.02-133.02 minutes | More than 60 minutes before logged stop under stated assumptions |
| B17 | 194.38-196.38 minutes | More than 60 minutes before logged stop under stated assumptions |

These are retrospective, conditional comparisons, not new independent tests. The +/- 60-second interval is a sensitivity assumption, not a source-certified uncertainty bound; shared acquisition/log clock is also assumed. A PASS inside `conditional_stop_warning` applies only to that calculation. It does not pass the physical-failure warning requirement. Neither the exact physical-damage onset nor a guaranteed clock bound is established. The stop threshold is vibration-based, so advance vibration alerts may also share the endpoint's measurement mechanism.

Reproduce with `python scripts/audit_detector_endpoints.py`. [Machine-readable results](../../governance/evidence/detector-endpoint-audit.json). The script checks source-log timestamp text but does not automate semantic label adjudication; the endpoint type comes from this log review.

## Remaining evidence that code cannot manufacture

1. **Accepted endpoint:** retain the original warning requirement. A domain/customer owner must specify whether the intended event is confirmed damage, maintenance intervention, or a documented protective limit. Choosing the protective-limit endpoint would be an explicit requirement change, not a way to retroactively pass the existing requirement. Confirm clock mapping and uncertainty independently.
2. **Healthy operating exposure:** obtain independently supported healthy intervals with actual operating time, sensor/regime metadata and complete episode adjudication. Early reference windows and low RMS are not healthy labels. The current logs do not establish this longitudinal exposure; no zero-nuisance claim follows from their absence of health annotations.
3. **Independent evaluation:** freeze the detector, grouping policy, endpoint definition and analysis plan before evaluating fresh bearings. All B04/B12/B17 signals are consumed. Keep UNSW Tests 3/4 reserved until useful label/timing evidence is available; the [publisher description](https://data.mendeley.com/datasets/h4df4mgrfb/3) identifies measurements by shaft cycles and multiple speeds, which does not directly establish an elapsed-time warning clock.
4. **Acceptance precision:** agree an exposure/sample-size and uncertainty plan before a pass decision. The new nuisance evaluator intentionally returns descriptive bounds and INCONCLUSIVE; it does not extrapolate short exposure into proof of one episode per 30 operating days. Independent bearing/site coverage must accompany event counts.

The [existing intake specification](alert-acceptance-evidence-needed.md) remains the label contract. Next useful input is a documented event/healthy-exposure annotation set from a suitable benchmark or authorized observational pilot, not simply more unlabeled vibration bytes. External author contact and real customer access have not been performed.

No thresholds, research split, deployed reference API, release gate or budget changed. Disposition remains **NOT_PROMOTED**. Software scoring is now implemented and tested; label qualification and independent operational validation remain open.

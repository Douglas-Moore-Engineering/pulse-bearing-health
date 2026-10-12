# Frozen-rule evaluation on independent IMS experiments

Executed 2026-10-11. This evaluates the unchanged run-2 RMS procedure against a different experiment. It does not claim independent human assurance or representative site performance.

## Run 1 result

All 2,156 snapshots passed the 20,480-row, eight-channel, finite-number schema check. Each bearing has two channels. The first 100 snapshots per channel provide the early reference median; the frozen threshold remains three times that median with three-snapshot persistence. No threshold was changed after seeing these results. See the [plan](ims-independent-plan.json) and [complete result with member and code hashes](../../governance/evidence/ims-run1-independent.json).

| Bearing | Channels | Maximum RMS/reference by channel | Sustained flag | Interval to final snapshot |
|---|---|---|---|---|
| 1 | 1–2 | 1.383 / 1.333 | None | Not available |
| 2 | 3–4 | 1.613 / 1.651 | None | Not available |
| 3 | 5–6 | 4.527 / 3.713 | Both at 2003-11-25 23:29:56 | 10 minutes |
| 4 | 7–8 | 2.084 / 2.039 | None | Not available |

The README identifies bearing 3 inner-race damage and bearing 4 roller-element damage at the experiment endpoint. **The frozen rule did not flag bearing 4.** Bearing 3's two channel flags concern one physical bearing, not two independent failure detections. This finding does not support promoting the rule as a general degradation detector. Onset labels and acceptable warning/false-alert criteria remain unavailable, so window-level accuracy and operational sensitivity are not reported.

The run has 24 gaps greater than 15 minutes; the largest is 534,333 seconds (about 6.18 days). Persistence resets across these gaps. Wall-clock intervals must not be represented as uninterrupted operating hours. Per-run early commissioning is part of the tested procedure; a fitted amplitude baseline was not transferred from run 2.

## Third archive discrepancy

The downloaded `3rd_test.rar` contains 6,326 inventory entries under `4th_test/txt`, spanning filenames from 2004-03-04 to 2004-04-18. The bundled README describes a third run with 4,448 files. The [inventory evidence](../../governance/evidence/ims-independent-inventory.json) preserves archive hashes and exact member examples. It has not been relabeled, silently truncated to 4,448 files or used as a labeled held-out experiment.

The [NASA catalog record](https://catalog.data.gov/dataset/ims-bearings), checked 2026-10-11, identifies the IMS contributor and distribution but does not resolve this member-level discrepancy. Archive identity, time span, endpoint mapping and downstream rights require source-specific clarification before labeled evaluation. No source-owner message was sent.

## Disposition

Keep the rule as an exploratory baseline; production detector promotion remains BLOCKED. Run 1 is now consumed evaluation evidence. Any redesigned rule using these observations must treat it as development data, not claim it remains an untouched test. Next detector work needs qualified independent data and an agreed missed-event/false-alert/warning-time acceptance policy. Requirements PULSE-FR-003/004/005/006 and PULSE-NFR-008 retain their original acceptance criteria. Dr. Moore is the receiving technical owner; no independent reviewer or release approval is invented.

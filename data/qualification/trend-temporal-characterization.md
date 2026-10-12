# Trailing-median temporal behavior

**Development characterization; NOT_PROMOTED.** Synthetic baseline ratio 1 and excursion ratio 2, with the unchanged 15-record median, strict 1.5 threshold and three-record persistence. No customer or reserved data used.

| Input after established baseline | Observed behavior |
|---|---|
| 1-, 3-, or 7-record high pulse | No flag |
| 8-record high pulse | First flag on observation index 29, after high input ended at index 27; clears at index 35 |
| Sustained 20-record high step | Flags on tenth high observation; clears on eighth subsequent low observation |
| Exactly threshold ratio 1.5 | No flag |
| Gap exactly 900 seconds | State retained |
| Gap greater than 900 seconds | State reset; unavailable until full-window warm-up |
| One channel returns to baseline while other remains high | Bearing flag remains active |

Indexes are zero-based with 20 baseline observations before the excursion. Record counts are not fixed wall-clock delays. The eight-record pulse is a delayed indication caused by smoothing plus persistence, not evidence of a currently high raw measurement. Whether filtering short pulses is desirable depends on the required fault duration; this test cannot label those pulses as nuisance or faults.

## Alert lifecycle contract for this candidate

- `available=false, flagged=null`: insufficient recent history. This must remain unknown, not healthy or cleared.
- `available=true, flagged=true`: trailing evidence meets the candidate criterion; raw current amplitude may already have returned to baseline.
- `available=true, flagged=false`: criterion is not currently met. This is not a verified recovery or human maintenance disposition.
- Incident acknowledgement, investigation and closure remain separate actions. A gap or cleared flag must not automatically close an existing maintenance incident. This candidate is not integrated into the deployed incident workflow.

[Measured pulse results](../../governance/evidence/trend-temporal-characterization.json) and [166-test suite](../../governance/evidence/trend-temporal-tests.xml). Reproduce with `python scripts/characterize_trend_temporal.py`. Tests cover temporal boundaries, both-channel behavior, gap reset and causality. No detector parameters were changed.

The candidate trades responsiveness for continuity. Before any freeze for new data, define acceptable excursion duration and indication delay against real acquisition cadence, and implement/test a separate incident lifecycle that preserves unknown states. Healthy exposure and physical endpoint evidence remain required for operational acceptance.

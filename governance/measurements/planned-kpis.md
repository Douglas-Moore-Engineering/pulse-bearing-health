# Open KPI measurement plans

Version 1 · 2026-10-12 · Owner: Dr. Douglas Moore, DME engineering lead. These are intended-use measurement plans, not executed evaluations. Historical benchmark/service exercises do not supply missing customer observations. [Dictionary](../../docs/appendix-a-kpi-dictionary.md) · [Measurement index](README.md).

## Shared fields applying to every plan below

| Field | Current value |
|---|---|
| Measurement status / criterion result / acceptance disposition | **not measured / not evaluated / pending review** |
| Baseline / observed result / uncertainty estimate | **not measured** for the stated intended-use metric; fictional discovery assumptions are not observations |
| KPI definition version | Dictionary v1, 2026-10-12; stable IDs introduced without replacing historical requirement or decision IDs |
| Population / sample size / exposure / window | Not yet fixed for intended use; freeze coverage, independent assets/runs, timezone, missingness, exclusions and follow-up before collection |
| Method / comparator / split | Row-specific collection action below; pre-register the protocol, comparator and independent evaluation units before confirmatory testing |
| Protocol approval / reviewer / authority | No pre-evaluation approval or real customer approver is recorded; DME self-review is not independent review |
| Code / data / model / configuration / run bindings | Not applicable to an unexecuted plan; retain exact digests and environment versions when an evaluation is performed |
| Operational action / outcome / attribution | Not measured; record actor, authorized action, time, follow-up and comparator/confounders for impact claims |
| Finance basis | Monetary metrics require agreed currency/price date, net incremental costs and nonoverlapping benefit categories; otherwise not applicable |
| Validity / disposition | Proposed plans only; no acceptance/release criterion is satisfied. Create a new measurement ID for each actual evaluation |
| Handoff / next scheduling action | DME lead owns plans and must appoint the relevant customer/domain/finance owner and schedule protocol review when a real engagement supplies authorized inputs |

## MEAS-PULSE-PLAN-001

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-001 / v1 / 2026-10-12; PULSE-KPI-001: Anomaly event recall |
| Need / requirements | [PULSE-R02](../../customer/01-discovery-record.md); [PULSE-FR-003](../../requirements/requirements.csv) |
| Definition / units / direction | Detected qualified fault events / qualified fault events; fraction; higher |
| Target / approval state | DET-PERF-002 proposes zero missed eligible events; not customer-approved |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Build an eligible event ledger with independently documented endpoints; retain abstentions in the denominator. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-002

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-002 / v1 / 2026-10-12; PULSE-KPI-002: False-alert burden |
| Need / requirements | [PULSE-R02](../../customer/01-discovery-record.md); [PULSE-FR-003](../../requirements/requirements.csv) |
| Definition / units / direction | Nuisance or unresolved alert episodes per verified bearing operating exposure, with reviewer workload separately reported; episodes / operating hours; lower |
| Target / approval state | DET-PERF-003 proposes at most one nuisance/unresolved episode per complete 720-hour bearing block |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Freeze episode/reset rules; obtain verified healthy operating-hour blocks and adjudicated review records. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-003

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-003 / v1 / 2026-10-12; PULSE-KPI-003: Warning lead time |
| Need / requirements | [PULSE-R02](../../customer/01-discovery-record.md); [PULSE-FR-003](../../requirements/requirements.csv) |
| Definition / units / direction | Earliest plausible qualified endpoint minus first causal qualifying alert; source-clock minutes; higher |
| Target / approval state | DET-PERF-001 proposes at least 60 minutes per eligible event |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Qualify physical endpoints and clock uncertainty; final recording alone is not physical failure. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-004

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-004 / v1 / 2026-10-12; PULSE-KPI-004: Diagnostic macro recall |
| Need / requirements | [PULSE-R02](../../customer/01-discovery-record.md); [PULSE-FR-005](../../requirements/requirements.csv) |
| Definition / units / direction | Mean recall across supported fault classes on independent held-out groups; fraction; higher |
| Target / approval state | Target not approved |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Establish supported labels, independent bearing/run split and per-class denominators before classifier evaluation. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-005

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-005 / v1 / 2026-10-12; PULSE-KPI-005: RUL error |
| Need / requirements | [PULSE-R02](../../customer/01-discovery-record.md); [PULSE-FR-006](../../requirements/requirements.csv) |
| Definition / units / direction | Declared aggregation of predicted minus qualified remaining life; source-clock unit; lower absolute error |
| Target / approval state | Error function and target not approved |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Qualify endpoints/censoring and freeze horizon, error function and independent-unit evaluation. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-006

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-006 / v1 / 2026-10-12; PULSE-KPI-006: RUL interval coverage |
| Need / requirements | [PULSE-R02](../../customer/01-discovery-record.md); [PULSE-FR-006](../../requirements/requirements.csv) |
| Definition / units / direction | Eligible true remaining-life values inside intervals / eligible predictions; fraction; target calibration |
| Target / approval state | Nominal coverage and tolerance not approved |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Define nominal interval, censoring treatment and grouped uncertainty before evaluation. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-007

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-007 / v1 / 2026-10-12; PULSE-KPI-007: Scoring p95 |
| Need / requirements | [PULSE-R07](../../customer/01-discovery-record.md); [PULSE-NFR-001](../../requirements/requirements.csv) |
| Definition / units / direction | 95th percentile elapsed time from accepted service receipt to persisted result; seconds; lower |
| Target / approval state | Candidate at most five seconds; intended full workload unqualified |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Freeze representative payload/arrival/concurrency profile and run full-path sustained service measurement; historical harness tests do not close this plan. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-008

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-008 / v1 / 2026-10-12; PULSE-KPI-008: Availability |
| Need / requirements | [PULSE-R07](../../customer/01-discovery-record.md); [PULSE-NFR-003](../../requirements/requirements.csv) |
| Definition / units / direction | Eligible service time meeting agreed availability definition / eligible service time; percent; higher |
| Target / approval state | Candidate 99.5% monthly; eligible time definition not approved |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Agree observation window, exclusions and probes; collect service history with dependency failures. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-009

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-009 / v1 / 2026-10-12; PULSE-KPI-009: Attributable avoided loss |
| Need / requirements | [PULSE-R01 / PULSE-R02](../../customer/01-discovery-record.md); [PULSE-FR-007 supports the decision ledger; no approved benefit-acceptance requirement](../../requirements/requirements.csv) |
| Definition / units / direction | Supported counterfactual loss minus realized loss for covered assets; currency at consistent price basis; higher |
| Target / approval state | No approved benefit target |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Capture authorized actor/action/time, covered assets, comparator, follow-up losses, incremental costs and confounders with finance/reliability owners. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-010

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-010 / v1 / 2026-10-12; PULSE-KPI-010: Lifecycle cost variance |
| Need / requirements | [PULSE-R08](../../customer/01-discovery-record.md); [PULSE-COST-REQ-001](../../requirements/requirements.csv) |
| Definition / units / direction | Revised estimate minus approved lifecycle-cost baseline on the same price basis; currency; target tolerance TBD |
| Target / approval state | Baseline and tolerance unapproved |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Use the existing lifecycle cost model; agree baseline/price basis, collect actuals and update forecast without treating budget ceilings as spend. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

## MEAS-PULSE-PLAN-011

| Field | Value |
|---|---|
| Identity / KPI | MEAS-PULSE-PLAN-011 / v1 / 2026-10-12; PULSE-KPI-011: Bearing-related downtime reduction |
| Need / requirements | [PULSE-R01 / PULSE-R02](../../customer/01-discovery-record.md); [No approved outcome requirement; derive it with a real sponsor](../../requirements/requirements.csv) |
| Definition / units / direction | (Comparable baseline downtime minus observed downtime) / comparable baseline downtime; percent; higher |
| Target / approval state | 30% over 12 months is a fictional discovery goal only |
| Implementation / evaluation relationship | Existing source and V&V are supporting context only; no intended-use result is inferred. The linked requirements retain their own implementation/acceptance status. |
| Owner / next action | DME lead: Obtain a real covered-fleet baseline and matched exposure, event/adjudication records and follow-up intervention outcomes; control attribution/confounding. |
| Acceptance / decision | Pending review; see existing release/customer handoff from the measurement index. No decision is created by this plan. |

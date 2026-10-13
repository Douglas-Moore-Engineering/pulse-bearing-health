# KPI Dictionary

Definition version 1 · 2026-10-12. Existing names and intended meanings retained; stable KPI IDs added for traceability. [Measurement index](../governance/measurements/README.md). Historical definitions remain in Git history. Reference exercise results and intended-use/customer metrics have separate records.

| KPI ID | KPI / definition | Unit / direction | Current evidence |
|---|---|---|---|
| PULSE-KPI-001 | Anomaly event recall: Detected qualified fault events / qualified fault events | fraction; higher | [Not measured; MEAS-PULSE-PLAN-001](../governance/measurements/planned-kpis.md#meas-pulse-plan-001) |
| PULSE-KPI-002 | False-alert burden: Nuisance or unresolved alert episodes per verified bearing operating exposure, with reviewer workload separately reported | episodes / operating hours; lower | [Not measured; MEAS-PULSE-PLAN-002](../governance/measurements/planned-kpis.md#meas-pulse-plan-002) |
| PULSE-KPI-003 | Warning lead time: Earliest plausible qualified endpoint minus first causal qualifying alert | source-clock minutes; higher | [Not measured; MEAS-PULSE-PLAN-003](../governance/measurements/planned-kpis.md#meas-pulse-plan-003) |
| PULSE-KPI-004 | Diagnostic macro recall: Mean recall across supported fault classes on independent held-out groups | fraction; higher | [Not measured; MEAS-PULSE-PLAN-004](../governance/measurements/planned-kpis.md#meas-pulse-plan-004) |
| PULSE-KPI-005 | RUL error: Declared aggregation of predicted minus qualified remaining life | source-clock unit; lower absolute error | [Not measured; MEAS-PULSE-PLAN-005](../governance/measurements/planned-kpis.md#meas-pulse-plan-005) |
| PULSE-KPI-006 | RUL interval coverage: Eligible true remaining-life values inside intervals / eligible predictions | fraction; target calibration | [Not measured; MEAS-PULSE-PLAN-006](../governance/measurements/planned-kpis.md#meas-pulse-plan-006) |
| PULSE-KPI-007 | Scoring p95: 95th percentile elapsed time from accepted service receipt to persisted result | seconds; lower | [Not measured; MEAS-PULSE-PLAN-007](../governance/measurements/planned-kpis.md#meas-pulse-plan-007) |
| PULSE-KPI-008 | Availability: Eligible service time meeting agreed availability definition / eligible service time | percent; higher | [Not measured; MEAS-PULSE-PLAN-008](../governance/measurements/planned-kpis.md#meas-pulse-plan-008) |
| PULSE-KPI-009 | Attributable avoided loss: Supported counterfactual loss minus realized loss for covered assets | currency at consistent price basis; higher | [Not measured; MEAS-PULSE-PLAN-009](../governance/measurements/planned-kpis.md#meas-pulse-plan-009) |
| PULSE-KPI-010 | Lifecycle cost variance: Revised estimate minus approved lifecycle-cost baseline on the same price basis | currency; target tolerance TBD | [Not measured; MEAS-PULSE-PLAN-010](../governance/measurements/planned-kpis.md#meas-pulse-plan-010) |
| PULSE-KPI-011 | Bearing-related downtime reduction: (Comparable baseline downtime minus observed downtime) / comparable baseline downtime | percent; higher | [Not measured; MEAS-PULSE-PLAN-011](../governance/measurements/planned-kpis.md#meas-pulse-plan-011) |
| PULSE-KPI-012 | Snapshot receipt recovery: Recovered receipts / receipts in a selected backup | fraction; higher | [MEAS-PULSE-001](../governance/measurements/MEAS-PULSE-001.md) |
| PULSE-KPI-013 | SCA paired decision coverage: (eligible windows - abstentions) / eligible windows per case/side | fraction; higher | [MEAS-PULSE-002](../governance/measurements/MEAS-PULSE-002.md) |

Reference metrics do not replace operational metrics. In particular, window coverage is not event recall, receipt counts are not RTO/RPO, false alerts per all test rows are not false positives per healthy row or nuisance alerts per operating hour, and processed-record counts are not realized business benefits.

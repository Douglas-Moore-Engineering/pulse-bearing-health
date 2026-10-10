# KPI Dictionary

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

| KPI | Definition | Current target/status |
|---|---|---|
| Anomaly event recall | Detected qualified fault events / qualified fault events | Target TBD; no observations |
| False-alert burden | Alerts without supported actionable fault per asset-time and review workload | Definition/window/target TBD |
| Warning lead time | Source-clock failure onset minus first qualifying alert | Dataset-time dependent; plant-day claim prohibited |
| Diagnostic macro recall | Mean per-supported-class recall on independent held-out groups | Target TBD |
| RUL error / interval coverage | Error to qualified endpoint; true values inside interval / eligible predictions | Endpoint/coverage target TBD |
| Scoring p95 | Accepted service receipt to persisted result | Candidate ≤5 seconds; unmeasured |
| Availability | Eligible service time meeting agreed definition / eligible service time | Candidate 99.5%; definition/real operation pending |
| Attributable avoided loss | Supported counterfactual loss minus realized loss for covered assets | Unknown; no savings claim |
| Lifecycle cost variance | Revised estimate minus approved baseline, consistent price basis | Estimate/baseline unapproved |

Report denominators, time/group units, confidence and exclusions. Never count overlapping vibration windows as independent bearings.

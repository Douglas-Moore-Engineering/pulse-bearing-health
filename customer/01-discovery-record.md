# Pulse — Intake and Discovery

Record PULSE-DISC-001-INTAKE v1.1 · 2026-10-08

Fictional portfolio exercise. All customer answers and role approvals are simulated. No real client, site, costs, measured outcomes or production approval is claimed. Extracted from planning baseline v0.9; later phases are outside this initial repository snapshot.

## Customer answers

Each response has state **Answered** for fictional discovery completeness and evidence state **Fictional**. Unknown technical feasibility is tracked separately, rather than inventing successful results. Role respondents and read-back below are simulated, dated 2026-10-08.

| Question / response | Fictional customer answer | Simulated respondent |
|---|---|---|
| Q-01 / PULSE-R01: problem and cost | We have 60 production-support motors. Eight bearing-related unplanned stops occurred in the previous 12 months, totaling 80 downtime hours. Finance estimates $2,500 per downtime hour, excluding $48,000 in repair, parts and overtime costs. We use calendar maintenance and monthly manual vibration rounds. | Plant manager / finance controller |
| Q-02 / PULSE-R02: success | We want fewer bearing-related stops and actionable warnings. Use the original 30% reduction over 12 months as a pilot goal. Evaluate detection, alert burden, diagnosis and RUL first on public data; do not promise the proposed 90%, seven-day or 20% targets until feasibility is demonstrated. | Plant manager / reliability engineer |
| Q-03 / PULSE-R03: users and actions | Reliability reviews evidence daily; maintenance plans approved work; operators acknowledge notifications. The maintenance planner approves any CMMS submission. Pulse cannot stop equipment, change setpoints or execute maintenance autonomously. | Reliability engineer / maintenance planner |
| Q-04 / PULSE-R04: assets and data | Start with 12 critical electric motors that have rolling-element bearings, mainly fixed-speed duty. The fictional fleet includes motors driving pumps and fans, but the first scope covers motor bearing health only. Existing historian data has current, temperature and run state at one-minute cadence, but no archived raw vibration waveforms. CMMS has 24 months of work orders with incomplete bearing-failure labels. Use public vibration datasets for the reference study; propose read-only vibration sensing for a future site pilot. | Reliability engineer / IT/OT lead |
| Q-05 / PULSE-R05: hosting and security | Azure is the preferred environment for the scenario, with US data residency and organizational identity integration. OT collection must be read-only through an approved intermediary boundary. No inbound cloud control connection or control-network writes. Raw vibration proposed retention is 90 days; approved derived features, alert and decision evidence 24 months. Security must review the final design and retention treatment. | IT/OT lead |
| Q-06 / PULSE-R06: ownership and support | Customer owns its operational data, cloud subscription and billing. Plant reliability owns operational decisions; IT owns platform administration and identity; maintenance owns work-order action. DME provides implementation and business-hours technical support for 12 months after simulated acceptance, with documentation and transfer. DME reusable code is licensed to the customer; customer-specific configuration and artifacts need defined handover rights in the simulated SOW. | Plant manager / IT lead |
| Q-07 / PULSE-R07: performance and recovery | Score new valid observations within five seconds at the 95th percentile, measured from receipt at the scoring service to persisted result, excluding sensor capture/transmission. Reconcile and score the 12-asset fleet daily by 06:00 plant-local time. Candidate application availability is 99.5% monthly, recovery time four hours and maximum loss of accepted central records one hour. Sensor failure marks health unavailable/degraded and requires manual rounds; no previous healthy result is shown as current. | Reliability engineer / IT lead |
| Q-08 / PULSE-R08: budget and approval | Illustrative implementation ceiling is $60,000; incremental recurring operations/support budget is $18,000 annually, including the sensor service allowance. Reference feasibility review is targeted for 2026-11-06; a later shadow pilot is tentatively targeted for January 2027 and depends on feasibility and simulated site readiness. Plant manager approves scope, finance approves cost assumptions, IT/OT approves access/security, reliability reviews technical evidence, and plant manager accepts delivery after those reviews. | Plant manager / finance controller |

These are scenario decisions, not evidence of a real environment. Azure preference is a constraint for later trade studies, not a selection of cloud services or authorization to incur cost. Sensor design, instrumentation costs and integration are not established by the invented budgets.

**Simulated read-back disposition:** the role-based customer review accepts the above problem framing and the proposed 12-motor scope for planning. Numeric technical criteria remain candidates subject to feasibility; this is not technical acceptance or production approval.

## Scope and responsibilities

**First asset family:** rolling-element bearing health on 12 critical electric motors. Motor-driven pumps and fans are operational context; pump hydraulic faults, fan aerodynamics, gearbox diagnosis and broad motor electrical faults are excluded from this initial capability.

**Reference increment:** public-data acquisition/rights review, data contracts and quality profiling, reproducible asset/run-separated evaluation, baseline comparisons, health/diagnosis/RUL feasibility, evidence views and demonstration workflow with a mock CMMS. Reference work uses no actual customer data or plant access.

**Later simulated site increment:** validate sensor placement, eligible bearing types and operating regimes; adapt contracts; approve source and CMMS interfaces; run shadow scoring and evaluate operator workload. It depends on reference feasibility. No deployment or sensor purchase follows automatically from this document.

| Responsibility | Simulated accountable role | DME responsibility |
|---|---|---|
| Scope and outcome acceptance | Plant manager | Maintain trace and provide evidence package |
| Failure modes, labels and maintenance interpretation | Reliability engineer | Propose validation/evaluation methods |
| Cost baseline and benefits attribution | Finance controller | Transparent calculations; no invented measured ROI |
| Sensors, historian, network and identity | IT/OT lead | Design/read-only access proposal and test evidence |
| Work-order approval and execution | Maintenance planner | Recommendation workflow and CMMS contract |
| Monitoring, backup, recovery and cloud billing | Customer IT service owner | Runbooks, tooling, training and agreed support |
| Model changes and retraining | Reliability plus IT release owner | Drift/evaluation evidence and governed change proposals |
| Reusable IP and customer artifacts | Sponsor/commercial owner | Simulated SOW/IP schedule; no actual legal agreement |

Simulated integration inventory: historian vendor is TBD; CMMS vendor is TBD; initial reference uses versioned file/API contracts and mocks. ERP and MES are not required for the initial scope because cost/production-exposure records can be supplied as approved exports. This is a justified planning exclusion, reviewable if outcome measurement needs additional interfaces. Identity will use the scenario's organization-managed authentication; product/service selection is deferred.


## Lifecycle cost supplement — 2026-10-10

Use [PULSE-LCC-001 v0.1](04-lifecycle-cost-model.md), its [cost ledger](lifecycle-cost-lines.csv), and [PULSE-BC-001 v0.1](05-business-case.md). Original fictional responses and IDs are preserved. Q-08 records budget ceilings, not full TCO; finance must reconcile inclusions and operating years. Economic attribution for the 12 covered motors is unresolved. The supplement is prepared for review and does not change the original simulated read-back into approval of these new assumptions.


## Pre-Azure engineering supplement — 2026-10-10

See [engineering review handoff](07-pre-azure-engineering-handoff.md) and [work breakdown](06-engineering-cost-work-breakdown.md). Preserve this record's existing version and fictional source statements; the new design package v0.1 is a separate prepared increment. No Azure connection, accepted design, actual approval or financial closure is inferred.

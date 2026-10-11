# Customer discovery questionnaire

## Contents

- [Interview approach](#interview-approach)
- [Eight core questions](#eight-core-questions)
- [Follow-up prompts](#follow-up-prompts)
- [Conditional modules](#conditional-modules)
- [Close and hand off](#close-and-hand-off)

## Interview approach

Start with the eight core topics. Reuse known answers. Ask one to three related questions at a time in conversation, then ask only the follow-ups that materially affect the engagement. Provide the complete form when requested. Let respondents identify another owner or say Unknown.

Use plain language. Explain a technical term when needed: recovery time is how long the service may be unavailable; acceptable data loss concerns the newest records that may be lost. Ask for operational examples before proposing numerical commitments.

Record response, respondent/role, date, supporting evidence, evidence state, engineering interpretation and unresolved follow-up using the discovery record template linked in the main skill. Do not ask for secrets or attach sensitive source data to the reusable skill.

## Eight core questions

| ID | Ask the customer | Establish |
|---|---|---|
| Q-01 | What problem are you trying to solve, and what does it cost you today? | Business need, current workflow and impact baseline |
| Q-02 | What would a successful outcome look like, and how would you measure it? | Objectives, measurement and acceptance |
| Q-03 | Who will use the system, and what action should they take when it detects a problem or produces a result? | Users, decisions and authority |
| Q-04 | What equipment, systems and historical data do you have? Can we review permitted samples? | Scope, interfaces, source ownership and feasibility |
| Q-05 | Do you have an approved cloud or hosting environment, and any security or data restrictions? | Deployment, access and data constraints |
| Q-06 | Who will own, operate and support the system? | Responsibilities, support and handoff |
| Q-07 | How quickly must it respond, and how much downtime or data loss is acceptable? | Performance, resilience and fallback |
| Q-08 | What are the budget, target date and approval process? | Delivery boundaries, costs and decisions |

Adapt equipment wording for non-industrial engagements; keep the same topic IDs. Detection is one example, not a required feature of every customer system.

## Follow-up prompts

### Q-01 — Problem and impact

- Ask for a recent concrete incident and the process steps surrounding it.
- Identify frequency, severity, affected people/sites/products, and how the problem is detected today.
- Capture the current workaround, prior attempts, and what happens if nothing changes.
- Separate measured costs from estimates; record the calculation basis and evidence owner. Do not invent ROI or double-count losses.

### Q-02 — Success and acceptance

- Ask for the most important outcome and any non-negotiable boundary.
- Define the baseline, unit, population/denominator, target, measurement window and data source where known.
- Separate mandatory results from desirable features and future expansion.
- Identify who evaluates results and who accepts delivery; ask what evidence they need.
- Record unresolved thresholds as TBD with an action. Customer agreement on a target does not establish feasibility.

### Q-03 — Users and operational authority

- Identify user roles, operating hours, locations, access needs and training needs.
- Walk through how a result becomes a decision, who approves action, and where the decision is recorded.
- Ask about missed problems, false alarms, alert workload, escalation and acceptable fallback.
- Identify accessibility/usability needs and how representative users can review the workflow.
- Distinguish advisory output from execution authority, including any permitted write actions and their limits.

### Q-04 — Scope, sources and evidence

- Inventory in-scope assets/sites/users, systems, vendors, source owners and permitted interfaces; capture exclusions.
- Ask for schemas or permitted samples, identifiers, units, timestamps/time zones, cadence, data volume and historical coverage.
- Check missingness, changes in operating conditions, duplicates, label/outcome quality and cross-system joins.
- Identify access authorization, allowed uses, export limits and third-party rights before arranging a transfer.
- Record source-specific readiness; the existence of a dataset does not prove its fitness for prediction.

### Q-05 — Hosting and constraints

- Capture existing cloud/on-premises environments, organizational policies and approved technology constraints.
- Identify environments, network/trust boundaries, private connectivity and access approval owners.
- Ask about classification, permitted locations, transfers, retention, deletion, backup/log treatment and non-production copies.
- Record relevant contractual/security/industry requirements and who interprets them.
- Treat preferred products as constraints or candidates with a stated basis; select services after requirements and trade studies.

### Q-06 — Ownership, operation and support

- Identify sponsor, domain owner, data owner, technical/platform owner, security owner and service owner; one person may fill multiple roles.
- Assign cloud billing, identity/key management, code/artifacts, monitoring, backups, recovery and release responsibilities.
- Capture support hours, severity/escalation paths, response expectations, maintenance windows and supplier dependencies.
- Clarify training, documentation, transfer, ongoing support, IP/reuse and exit expectations.
- Separate response time from resolution time; do not promise unsupported service levels.

### Q-07 — Performance, availability and recovery

- Ask when a result becomes too late to act and define the start/end of the response-time measurement.
- Capture normal and peak workload, concurrency, data freshness, completeness and disconnected operation.
- Ask how long interruption can be tolerated and what records can be lost; define scope and failure scenarios.
- Clarify whether recovery means fresh service restoration, complete historical processing, or both.
- Record manual fallback, degraded behavior, recovery owner and future test evidence needed.

### Q-08 — Commercial boundaries and decisions

- Separate discovery/design, implementation, recurring operation and third-party costs; record payer and budget owner.
- Ask what drives the deadline and what dependencies or procurement steps affect it.
- Identify scope, technical, security, spending, acceptance and release authorities.
- Capture review milestones, work-order status, change process and any customer tasks on the critical path.
- Distinguish a budget ceiling, an estimate and actual authority to spend. Route contract interpretation to its responsible owner.

## Conditional modules

Use only modules relevant to the customer's problem. Keep follow-up IDs under their parent question, such as Q-04.F01.

### Industrial anomaly detection and forecasting

- Under Q-01/Q-03, specify asset family, failure modes, operating regimes and control/safety boundaries.
- Under Q-02/Q-07, ask what warning horizon permits action, how false alerts are counted and what workload reviewers can handle.
- Under Q-04, distinguish raw waveforms from derived sensor summaries, source sampling from transmission cadence, and confirmed failures from preventive work orders.
- Check event independence, timestamps/asset joins, censoring, interventions and changes in equipment or maintenance policy.
- Record forecast feasibility as unresolved until representative data and evaluation support it; do not silently replace required forecasting with anomaly detection.

### Enterprise AI, document retrieval or assistants

- Identify source-of-truth content, permission boundaries, languages, update cadence and ownership.
- Specify answer-quality expectations, citation needs, unacceptable errors, human escalation and representative evaluation tasks.
- Clarify tool/write permissions, sensitive data use, provider restrictions and human approval boundaries.

### Cloud, data or application integration

- Identify source/destination owners, interface contracts, read/write authority, API/export limits and idempotency/replay needs.
- Capture migration/cutover constraints, compatibility, rollback, dependencies and service continuity expectations.
- Ask which existing organizational platform controls can be reused and what must be built or operated by the delivery team.

## Close and hand off

Read back: “You need [capability] to address [problem] for [users/scope]. Success means [outcome and proposed measurement]. The main constraints are [constraints]. We still need [unknowns and owners]. Is this accurate?”

Record corrections and review evidence. Prepare the discovery summary, candidate requirements and acceptance criteria, scope, ownership, and open-item register. Use the lifecycle handoff record to carry them into scope/commercial/environment/data planning and then standards assurance and engineering. Do not skip those phases or treat a completed interview as a passed build gate.

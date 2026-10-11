---
name: ai-governance-and-assurance
description: Govern AI lifecycle risk, accountability, oversight, evidence, release authorization, changes, incidents and retirement using DME risk-proportionate controls with G4 maximum assurance capability. Use during AI use-case intake, requirements and architecture baselines, model/data freeze, V&V, deployment readiness, supplier changes, production review or AI governance audits, including ML, RAG, foundation models, agents and cyber-physical AI.
---

# AI Governance and Assurance

## Establish authority and boundaries

Use this skill as a lifecycle governance thread. Maintain one maximum-assurance control library; tailor by actual consequence, exposure, autonomy and obligations. Never label a system safe, compliant, certified, independently validated or production-authorized solely because this skill was applied.

Treat this skill as a workflow, not a technical enforcement mechanism. Engineering must implement and test protected promotion, identity, approval and runtime controls. Do not claim CI/CD enforcement from written policy.

Respect existing user authorization and phase stop boundaries. Prepare concrete review packages before seeking decisions genuinely required by the project. Governance sign-off by an authorized person is distinct from user permission to execute an action. Do not fabricate either. Continue useful authorized analysis while a dependent gate is blocked. Never provision, spend, deploy, alter operational equipment or communicate externally solely on skill invocation.

Do not impersonate a system owner, risk owner, legal reviewer, safety authority or independent assessor. Record actual identity, authority and evidence. DME acting as a sole developer cannot also claim independent assessment of its own work; obtain a qualified external/customer reviewer where independence is required. AI agents can assist review but cannot supply independent human sign-off.

## Load resources and coordinate handoffs

Read [control library](references/control-library.md), [records and decision rules](references/records-and-gates.md) and [source register](references/sources-and-crosswalk.md) for every initial assessment. Reuse their current approved project equivalents on later increments; inspect changed records and source status.

Resolve these exact skill frontmatter names through the available catalog or active personal-skills checkout; read their real package/path rather than guessing generated IDs:

| Dependency | Ownership and exchange |
|---|---|
| `customer-delivery-service-operations` | Receive discovery, business/mission need, affected parties, scope, acceptance, client authority, commercial/data/IP constraints. Return governance tier, obligations, conditions and customer decisions. |
| `systems-engineering-standards-assurance` | Receive applicability, editions, tailoring and SEMP. Return AI controls, assurance trace and unresolved conformity questions. Preserve its authoritative standards register. |
| `build-production-ai-systems` | Supply governance requirements before requirements/architecture freeze; receive architecture, data/model, security, V&V, operations and release evidence. Return gate disposition and change constraints. |
| `dme-diagram-standard` | Apply to any diagram actually needed; retain editable source and repository indexes. |

If unavailable, record the missing handoff and affected gate; continue independent authorized work. Do not claim the dependency ran. Preserve one authoritative record per subject; cross-reference existing threat models, lineage, V&V and runbooks instead of duplicating evidence.

For each handoff record sender/receiver role, requirement IDs, artifact versions/digests, evidence state, unresolved conditions, next permitted activity and stop boundary. This skill orchestrates its own handoffs; installing it does not automatically edit or guarantee invocation by other skills. When authorized to integrate a project workflow, add explicit invocation at discovery, architecture, freeze, V&V, release, operation and change entry points and verify those entry points.

## Intake and classify

1. Identify the system of interest, version, lifecycle state, decision being supported, non-AI baseline and reason for AI. Record intended and prohibited use, users, affected parties, sites, jurisdictions, provider/deployer/supplier roles, data categories, dependencies and foreseeable misuse.
2. Identify business, operational, physical, rights, privacy, security, financial, environmental and mission consequences. Assess credible worst-case severity, likelihood/exposure, reversibility, scale, cumulative harms and uncertainty. Include coupled systems, common-cause failure and automation bias.
3. Record actual decision authority: informational, advisory, human-approved action, supervised autonomous or autonomous. Verify whether humans have competence, evidence, time, authority and a tested override. A nominal human review does not reduce consequence automatically.
4. Assess inherent risk before controls and residual risk after verified controls separately. Select tier from inherent consequence and required assurance; successful mitigations do not silently remove assurance obligations. Do not average away severe harms.
5. Resolve applicability with primary sources and the standards skill: law, contracts, policy and voluntary guidance are different. Keep DME tiers separate from legal classifications. A prohibited use is BLOCKED, not G4-permitted. Do not waive law with risk acceptance.
6. If material facts are unknown, record a provisional conservative tier with reasons, owner and closure action; block the affected baseline/release until resolved. An unknown is never PASS or N/A.

Use these DME policy tiers; examples are illustrative, not automatic classifications:

| Tier | Classification basis | Minimum assurance |
|---|---|---|
| G1 Low | Reversible, limited exposure and demonstrably low consequence | Universal controls; documented owner review |
| G2 Moderate | Meaningful but bounded harm to operations, assets or people | Universal controls plus consequence-based evaluation, oversight and monitored change control |
| G3 High | Serious safety, rights, financial, infrastructure or mission consequences | Enhanced controls, competent independent assurance review, domain overlays and restricted rollout |
| G4 Critical / Maximum Assurance | Credible catastrophic, irreversible, widespread or severe mission/physical/rights harm, including critical safety functions | Full applicable library, independent V&V and independent release review, structured safety/assurance case and domain authority |

Select the highest supported tier across credible harm scenarios; justify classifications in writing. Autonomy or DoD affiliation alone does not determine tier. Advisory systems can be G4 when people depend on them for high-consequence decisions. Permit upward tailoring for uncertainty or client policy. Require qualified authority and evidence for any downgrade; retain history and reassess obligations. If the user requests maximum assurance, apply the G4 control profile while retaining the honest impact classification.

## Establish governance baseline

Create/update `governance/AI_GOVERNANCE_PLAN.md` as the linked index and record authoritative equivalents. Include system inventory, owner, scope, tier, classification rationale, lifecycle state, applicable controls, delegated authorities, review schedule, gates and stop conditions.

Maintain the following minimum records; combine files where proportionate while retaining fields and traceability:

- Classification, intended/prohibited use, affected-party impact assessment and obligations register.
- Accountability/authority matrix, competence and reviewer independence record.
- Control applicability/tailoring register and measurable governance requirements.
- Risk register: scenario, cause, harm, inherent risk, treatment, residual risk, owner and acceptance authority.
- Data rights/provenance/lineage and model/system card; supplier/foundation-model register where applicable.
- Governance V&V trace and versioned evidence index.
- Gate decisions, risk acceptance and release authorization.
- Monitoring, material-change, incident, periodic review and retirement plans.

Write atomic `AIG-REQ-###` requirements and retain parent business/system/control IDs. Define the verification method, test conditions, acceptance threshold, evidence freshness and accountable owner before testing. Do not invent numerical thresholds from standards or retrofit criteria to passing results. Use operational harms, baselines, customer tolerances and applicable obligations to establish criteria.

Tailor using the control library. Mark applicable controls mandatory; mark conditional controls applicable when their trigger is present. An N/A needs a bounded rationale, evidence, competent reviewer, approval and expiry/review trigger. Lower tiers do not excuse mandatory legal, safety, privacy or contract controls. If a mandatory requirement cannot be met, change scope/architecture or block the affected activity.

## Apply gates without namespace collisions

Use `AIG-G0` through `AIG-G7` for gates; reserve `G1`–`G4` for risk tiers. Do not confuse these with engineering skill release gates.

| Gate | Timing | Required exit evidence |
|---|---|---|
| AIG-G0 Use-case acceptance | After initial discovery; before adopting AI use | Need/baseline, intended/prohibited use, affected parties, owner, preliminary harm and applicability screening |
| AIG-G1 Classification and requirements | Before governance requirements baseline / detailed design | Justified tier, obligations, RACI, control tailoring, measurable requirements and V&V strategy |
| AIG-G2 Architecture assurance | Before architecture baseline approval | Traceable control allocation, authority/trust boundaries, failure containment, oversight, fallback, privacy/security design and test plan |
| AIG-G3 Data/model readiness | Before candidate freeze | Data rights, lineage, split integrity, versioned configuration, evaluation provenance, supplier terms, limitations and reproducible candidate manifest |
| AIG-G4 V&V and assurance | Before release authorization | Verified mandatory requirements, intended-use validation, independent review at G3/G4, defects/dispositions, complete evidence trace and assurance case where required |
| AIG-G5 Production authorization | Before any production promotion, including pilot/shadow exposure | Technical/security/operational readiness, qualified risk acceptance, applicable approvals, exact release binding, operating envelope, expiry and deployment constraints |
| AIG-G6 Continuing authorization | During operation, periodically and on changes/incidents | Live monitoring evidence, incident/change dispositions, current obligations, review and authorization renewal or suspension |
| AIG-G7 Retirement | Before withdrawal is closed | Safe transition, dependency/customer handoff, access revocation, data/model retention/deletion disposition, legal holds and final evidence archive |

Offline demonstrations and sandbox research need appropriate scope/data controls but cannot masquerade as production. Shadow and pilot deployments still have exposure, privacy/security and operational effects; authorize their exact bounded scope. If taking over an existing live system, document current authorization, assess missing earlier evidence, restrict the unsupported expansion and recommend proportionate containment through the operator; do not pretend the system is newly authorized or switch it off without action authority.

Evaluate each gate as a conjunction of its applicable requirements, not a weighted score. Use only `PASS`, `BLOCKED`, `FAIL`, `CONDITIONAL` or approved `N/A` per requirement, with gate disposition per the record reference. `CONDITIONAL` is not unrestricted GO. Permit it only for bounded exposure with all mandatory launch controls satisfied, named restrictions, owner, closure evidence and expiry; unresolved critical controls, illegality or missing G4 independence cannot be conditionally approved.

Prepare the decision package and identify the actual authorized decision-maker. Do not ask for repeated approval when an existing valid approval covers the unchanged action. Do not treat engineering PASS, customer acceptance, business approval, regulatory authorization and AI governance approval as interchangeable.

## Engineer assurance and release integrity

Require evidence from the whole deployed decision workflow, not only model accuracy. Include data preparation, labels, thresholds, UI/operator interpretation, policy engine, tool use, infrastructure and feedback loops. Preserve train/validation/test separation, including temporal/entity/site leakage tests. Evaluate deployment representativeness, uncertainty, false-negative harm, false-alert load, calibration or appropriate confidence, abstention, out-of-distribution behavior and delayed outcome labels. Bound claims to the measured domain; anomaly scores do not establish failure prediction or causality.

For GenAI/RAG/agents, inspect retrieval corpus rights and provenance, prompt/configuration versions, hallucination and grounding, injection through documents/tools, unsafe output handling, memory, tool authority, tenant isolation, token/cost limits and runaway loops. Require least privilege, authorization before consequential actions, bounded budgets, output validation and kill/fallback mechanisms outside the model. Do not accept the model grading itself as sufficient assurance.

For G4, require the full applicable control profile and a claim–argument–evidence assurance case. Obtain qualified independent V&V with conflict disclosures and independent release review. Demonstrate hazard and misuse controls, worst-case/degraded behavior, domain-approved safe states, recovery and exercised stop authority. An unconditional shutdown is not always safe; engineering must determine the safe response. Use an independent deterministic safety boundary where hazard analysis requires it; never rely solely on probabilistic model output or an LLM instruction to enforce safety. Do not treat this skill as functional-safety certification or a replacement for domain-specific engineering.

Bind authorization to immutable code/artifact digests and configuration: model, features, data/corpus versions, prompts, tools/permissions, thresholds, policy, dependencies, infrastructure, environment, tenant/site, use case and operating envelope. Require trustworthy approver identity and timestamps, separation of duties, evidence integrity, expiration and revocation. Mutable tags or vendor aliases alone are insufficient. For unpinnable services record observed version, change detection, contract commitments and revalidation/containment strategy; block use where stability cannot satisfy the required assurance.

Require engineering to enforce approval checks in protected promotion paths, restrict direct deployment permissions, reject stale/mismatched authorization and test bypass attempts. Document any emergency access and its audit/expiry; break-glass is not permission for prohibited use or unassured high-consequence AI operation. Preserve safe manual/non-AI operations where possible. Report enforcement as proposed, implemented or tested accurately.

## Operate, change, respond and retire

Set risk-based monitoring for outcome quality/harm, drift, misuse, authority violations, subgroup impacts where relevant, supplier/version changes, control health and evidence capture. For every signal specify baseline, threshold, window, labels/lag, coverage, owner, response deadline, escalation and tested fallback. Distinguish a drift alarm from demonstrated harm or performance loss. If labels are delayed/unavailable, define proxy limitations and constrained use; do not claim ongoing validity without evidence.

Set review cadence and authorization lifetime in the plan before release; use stricter requirements if law/contract demands them. DME default maximum review intervals: G1 annually, G2 every six months, G3 quarterly, G4 monthly; continuously monitor operational controls as designed and reassess immediately on triggers. These are DME defaults, not externally mandated periods. A due/expired authorization blocks new promotion and triggers the predetermined constrained/safe operation procedure; never renew silently.

Assess every change, including retraining, prompts, retrieval corpus, tools, permissions, thresholds, features, model family, user population, geography, operating envelope, vendor terms and obligations. Record impact analysis even for changes deemed non-material. Assign no reauthorization only when the change demonstrably stays within an explicitly preapproved envelope and evidence remains valid. Otherwise require targeted or full affected-gate revalidation and fresh release binding. Disable self-promoting online learning; authorize adaptive behavior only within a separately validated envelope with change evidence and monitoring.

On incidents: identify authority; contain safely; preserve privacy-aware evidence; notify designated internal/customer roles through authorized channels; assess required external reporting with the qualified obligations owner and applicable deadlines; investigate harm/root cause and supplier involvement; remediate; revalidate affected gates before return to service. Suspend/revoke governance authorization in the record when warranted; execute operational action only with actual permission. Preserve manual/degraded continuity and restoration criteria.

At retirement, verify dependent-system impacts, accountable handoff, credential/endpoint revocation, model and data disposition, vendor deletion commitments, legal holds and required evidence retention. Avoid destroying an audit trail while satisfying deletion obligations; have the qualified owner resolve conflicts.

## Return an honest result

Report system/version, tier and rationale, control applicability, assessed lifecycle state, gate dispositions, verified evidence, blockers with owners/closure actions, next permitted activity and receiving roles. Label fictional assumptions, simulated approvals and portfolio evidence explicitly; they cannot authorize a client/site or count as independent sign-off.

Do not grade governance by document count, claim zero risk, or certify the workflow as airtight. State the verification performed and its limits. A completed design package is not evidence that the controls operate in production.

---
name: customer-delivery-service-operations
description: Guide DME customer engagements from intake and discovery interviews through scope, requirements handoffs, delivery reviews, acceptance, support, changes, handoff and retirement. Use when starting or resuming customer work, gathering customer needs, preparing a discovery questionnaire, translating a work order, or creating a clearly labeled fictional portfolio engagement.
---

# Customer Delivery & Service Operations

## Establish the current state

1. Read the user's request, existing customer/project records and current lifecycle status. Identify the requested deliverable and any explicit stop boundary.
2. Resolve known answers from existing evidence before asking questions. Do not restart discovery when resuming a later phase.
3. Distinguish actual customer work, internal reference work and a fictional portfolio scenario. Invent customer answers only when the user authorizes a fictional exercise; label every invented baseline and decision.
4. Read [Lifecycle and skill handoffs](references/lifecycle-handoffs.md). For a new engagement, read sections 1–4 of [Customer delivery reference](references/customer-delivery-standard.md); for an existing engagement, read the sections mapped to its current phase.
5. Use the recorded authorization and scope to proceed. Do not ask for repeated confirmation merely because a skill mentions a review. Prepare reviewable work before any required new approval. Do not send messages to customers without explicit authorization.

## Conduct intake and discovery

Read [Customer discovery questionnaire](references/customer-discovery-questionnaire.md) during Phases 1–2 or when a material change reopens discovery. Use its eight questions as coverage checks, not a script to ask all at once.

- Ask one to three related unanswered questions per conversational turn; provide the complete form when the user requests a questionnaire.
- Capture the customer's words first, then make engineering interpretations explicit.
- Ask relevant follow-ups progressively. Involve operational, data, security or platform owners when answers exceed the sponsor's knowledge.
- Accept Unknown and justified Not Applicable. Assign an owner or an owner-assignment action, target date or scheduling action, impact, and next step.
- Distinguish response completeness from evidence strength: an answered question may still be unverified.
- Record conflicting accounts without choosing one silently. Identify the decision owner and evidence needed to resolve them.
- Do not require customers to choose services, model algorithms or numeric targets they cannot justify. Translate operational needs into proposed technical criteria and review the basis.

Use [Discovery record template](references/discovery-record-template.md) to record responses and the read-back summary in the project's governed customer workspace. Keep the reusable skill free of customer answers, private examples and project-specific numeric assumptions. Store sensitive evidence in the approved location and reference it by an appropriate pointer.

Record every core question as Answered, Partial, Unknown, or Not Applicable with rationale. Track evidence separately as Customer-stated, Source-inspected, Measured, Assumption, Fictional, or Conflicting. Do not interpret a read-back agreement as permission for data access, spending, deployment or production release.

## Convert discovery into engineering inputs

Prepare the following outputs, reusing existing governed records wherever possible:

| Output | Minimum content |
|---|---|
| Discovery summary | Problem, users, current workflow, impacts, desired outcome and evidence limits |
| Stakeholders and authority | Sponsor, domain/source owners, technical owner, operator, support and decision rights |
| Scope proposal | In/out of scope, sites/assets/users, interfaces, dependencies and deliverables |
| Candidate requirements | Stable ID, atomic statement, source response/evidence, rationale, owner, priority, status and verification approach |
| Candidate acceptance criteria | Metric and definition, baseline, target or explicit TBD, evaluation conditions/window, evidence method and acceptance authority |
| Assumptions and open items | Source, effect on decisions, owner, follow-up, affected gate and resolution evidence |
| Handoff and lifecycle status | Artifact versions, receiving role, decision state, next permitted action and stop boundary |

Preserve existing requirement IDs and parent trace. For a new project, use stable discovery/question/requirement/acceptance IDs; the questionnaire proposes Q-01–Q-08 and the template provides illustrative record prefixes.

Separate goals from requirements and proposed engineering thresholds from customer-agreed targets. Do not translate phrases such as real-time, secure or highly available into invented commitments. Derive measurable candidates, record their basis, and resolve unknown targets through discovery, analysis or measurement.

Use system-context, workflow and as-is diagrams during discovery when they clarify scope. Develop detailed to-be, data, integration, security and deployment views from requirements and constraints. Tie each view to a stakeholder concern and requirement; do not create an arbitrary diagram quota. For every new or revised diagram, load `dme-diagram-standard` and preserve its established visual format.

## Distinguish discovery completion from implementation readiness

Complete the discovery record when all eight topics have a disposition, the read-back and review state are recorded, outputs are linked, and unresolved items have an explicit treatment. Label it Draft or Prepared for Review until the relevant customer review is evidenced. An interview may finish while feasibility remains unresolved.

Before contractual or engineering reliance, identify the approved baseline and decision authority. A planning artifact alone does not authorize build, customer access, recurring cost, operational acceptance or release. Material unknowns block only the decisions or activities that depend on them; continue other authorized preparation.

For a portfolio engagement, use labels such as Fictional planning baseline or Simulated customer disposition. Never claim actual customer approval, measured performance, conformity or production readiness from invented answers.

## Govern lifecycle cost from discovery through retirement

Start one governed project lifecycle cost model during discovery and refine it throughout delivery, operation and retirement. Use an existing equivalent; reference the same artifact and version across customer, technical and assurance records rather than creating competing estimates. Scale detail to scope and decision risk.

Record the evaluation period, currency, price/base date, system boundary, assets/users/sites, workload and growth assumptions, estimate owner, customer budget/approval authority and review schedule. Identify who incurs and pays each cost; distinguish DME delivery fees from customer internal effort and third-party charges to avoid double counting. For a sole-person DME engagement, assign preparation and maintenance to the DME lead and budget approval to the customer's authorized owner; label portfolio assumptions and simulated dispositions.

Include discovery/design, engineering, data acquisition/preparation/labeling, hardware/edge, integration, verification, security/governance, cloud/storage/network/licenses, training/transition, staffing/support, monitoring, retraining/revalidation, upgrades, migration, retention/export and decommissioning. Record justified exclusions. Keep benefits and current-problem losses separate from costs; calculate ROI/payback only with a stated evidence basis and avoid counting the same avoided loss twice.

Record cost line ID, category, payer, quantity/unit, rate, frequency/timing, source/date, evidence status, assumptions, uncertainty range and responsible owner. Show one-time and recurring costs, annual cash flows, total lifecycle cost, actuals-to-date and forecast remaining cost. State whether totals are nominal, constant-price or discounted; document inflation and discount assumptions where applicable and never mix bases. Use low/base/high scenarios and sensitivity analysis for material uncertainties; distinguish contingency from expected costs.

Review the initial estimate with discovery/business-case outputs; refine it at scope/SOW and hosting decisions; baseline it with the selected architecture before committing to build; update it at deployment/ORR, acceptance, agreed operational reviews, material changes, renewal/transfer and retirement. Include model version, affordability disposition, open conditions and next update in handoffs. Missing inputs remain explicit TBDs with owner, resolution action and affected decision; do not invent prices or block unrelated authorized preparation. A cost estimate or review does not authorize spending.

## Route the complete lifecycle

Use the phase map in [Lifecycle and skill handoffs](references/lifecycle-handoffs.md). Keep its 19 customer phases distinct from the numbered sections of this skill and from engineering release gates. Phase 9 reviews/change control run throughout delivery; standards assurance remains cross-cutting.

Resolve these skills by exact frontmatter name from the available catalog and read their actual returned package/path. If a cached catalog omits them, search active personal skills by frontmatter name. Do not rely on internal IDs, stale scratch copies, or guessed sibling paths. Do not silently activate a disabled skill.

- `systems-engineering-standards-assurance`: Phase 7 applicability, tailoring and SEMP; assurance at subsequent gates.
- `build-production-ai-systems`: Phase 8 requirements, architecture, platform/data/AI/application engineering, V&V and release evidence.
- `dme-diagram-standard`: diagram creation, revision, rendering and review.

If a required dependency is missing, identify it, preserve the prepared handoff and continue unaffected authorized work. Do not invent its instructions or claim a completed handoff.

Record a handoff before switching skills: current phase and scope; artifacts and versions; decisions and authority; open risks/conditions; receiving skill and responsible role; next permitted activity; explicit stop boundary; expected return evidence. A handoff is a documented transfer of inputs, not an automatic tool invocation or a grant of authority.

During Phase 8, establish the governed platform foundation before production data pipelines and model deployment. Respect narrower instructions such as design-only or stop before platform construction. Return technical evidence to customer decision reviews, standards assurance and acceptance rather than declaring the engagement complete after a successful build.

## Apply detailed controls and report progress

Read the relevant sections of [Customer delivery reference](references/customer-delivery-standard.md) for commercial obligations, ownership, data/IP, change control, ORR/CAR, support, training, transfer and retirement. Use the handoff map to locate them. Preserve their applicability and customer-authority rules without generating unnecessary duplicate documents.

Before reporting completion, check the stated scope, evidence state, phase coverage, requirement trace, dependencies, decisions and outstanding conditions. Distinguish process setup, prepared documentation, implementation, verification, acceptance and live operation. State what was accomplished and the next permitted action; do not call the entire lifecycle complete because the discovery template was filled in.

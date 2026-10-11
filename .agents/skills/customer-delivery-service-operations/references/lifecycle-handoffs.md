# Lifecycle and skill handoffs

## Skill routing

Use `customer-delivery-service-operations` as the customer-engagement coordinator. Load `systems-engineering-standards-assurance` for applicability, tailoring, SEMP and recurring assurance. Load `build-production-ai-systems` for technical engineering. Load `dme-diagram-standard` for every new/revised diagram. Resolve names through the catalog or installed skill frontmatter; do not hardcode generated skill IDs.

Transfer artifact references and decisions through the project's governed records. Skill names in text do not automatically execute a tool or pass a gate; explicitly read the receiving skill and apply its instructions within the user's authorized scope.

## Customer lifecycle map

Section numbers in the final column refer to the bundled Customer delivery reference, not lifecycle phase numbers. Use existing equivalent artifacts. Record Not Applicable with rationale, authority and downstream impact when tailoring a phase; never mark omitted phases complete silently.

| Phase | Activity | Inputs and required output | Routing / detailed reference |
|---|---|---|---|
| 1 | Lead qualification / intake | Problem, sponsor, decision/data/commercial paths; disposition as discovery-only, advisory, scoped delivery or unresolved | Customer skill; §§3, 7 |
| 2 | Discovery and problem framing | Interview/evidence; reviewed summary, stakeholder needs, scope candidates, acceptance candidates and open items | Questionnaire and record template; §4 |
| 3 | Scope and responsibility baseline | Discovery outputs; in/out of scope, deliverables, ownership and dependencies | Customer skill; §5 |
| 4 | Commercial / SOW translation | Work order and scope; versioned commitments, deliverable/acceptance trace and commercial dependencies | Customer skill; §§6–7 |
| 5 | Environment and deployment-model decision | Constraints and responsibilities; hosting, ownership, operator, support and release authority | Customer skill; §8 |
| 6 | Data, security, privacy, compliance and IP baseline | Sources and intended uses; handling, access, retention, security ownership, rights and conditions | Customer skill; §§9–11 |
| 7 | Standards applicability / tailoring / SEMP | Phases 1–6 artifacts; applicability, tailoring, SEMP, V&V strategy and assurance gaps | Load systems-engineering-standards-assurance; §25 |
| 8 | Production-system engineering | Governed scope and assurance inputs; requirements, architecture, implementation and V&V evidence at the claimed state | Load build-production-ai-systems and recurring standards assurance; §§12, 25 |
| 9 | Decision reviews and change control | Current artifacts and proposed changes; review decisions, impact analysis, actions and updated baselines | Customer skill continuously during delivery; §§12–13 |
| 10 | Reference release / demonstration review | Reference release/evaluation evidence; bounded demonstration claims, limitations and adaptation conditions | Technical and standards skills return evidence to customer review; §§12, 23–25 |
| 11 | Customer/site adaptation | Reference baseline plus actual site facts; authorized mappings/configuration and change impacts | Technical build plus customer/data owners; §§8–13, 25 |
| 12 | Site validation / shadow / canary | Site configuration and approved evaluation plan; representative operating evidence and rollout decision | Technical and standards skills; §§12, 25 |
| 13 | Operational Readiness Review | Technical, security, recovery, runbook and operator evidence; ORR disposition and conditions | Technical build with standards/service owners; §§15–18, 25 |
| 14 | Customer Acceptance Review | Scope/deliverable trace and acceptance evidence; actual customer disposition, conditions and owners | Customer skill; §14 |
| 15 | Production release / service transition | Applicable ORR/CAR and release authority; approved release plus service activation evidence | Technical skill for release; customer skill for activation; §§15, 25 |
| 16 | Production support / service management | Active service and support terms; incidents, maintenance, monitoring and service reports | Customer skill with technical/standards support; §§16–18 |
| 17 | Change, retraining and revalidation | Change request or observed drift/incident; impacts, authorization, revised evidence and release decision | Re-enter affected technical and assurance gates; §§13, 17, 25 |
| 18 | Handoff / transfer / renewal | Service state and agreement; resource/competency transfer, residual responsibilities and continuation decision | Customer skill with technical owners; §§18–20 |
| 19 | Decommissioning / exit / evidence closure | Approved exit scope; export/transfer/deletion/access disposition and retained evidence | Customer skill with technical and standards owners; §§21, 24–25 |

Phase 9 is a continuous responsibility, not a reason to postpone reviews until engineering finishes. Standards assurance starts before technical freeze and remains active. ORR, CAR, technical release and service activation are distinct decisions; retain the supplied standard's documented-exception rule for contractual acceptance timing.

## Lifecycle cost across phase handoffs

Start the governed lifecycle cost model in Phase 2; refine scope, payer and hosting assumptions in Phases 3–5; include assurance in Phase 7 and architecture/implementation cost evidence in Phase 8. Carry the same artifact/version through Phase 9 reviews, Phases 13–15 readiness/acceptance/transition, Phase 16 operating reviews, Phase 17 changes/retraining, Phase 18 renewal/transfer and Phase 19 retirement. Apply the customer skill lifecycle-cost requirements; record open financial conditions and decision authority without treating planning as spending authorization.

## Phase 8 engineering sequence and pause handling

Within production-system engineering, first refine requirements, assess architecture and justify cloud choices from workload, constraints and trade studies. Treat unmeasured sizes and prices as assumptions. Prepare a platform plan and resolve the applicable build-entry conditions before constructing the foundation.

The default implementation order in the technical skill is platform engineering, data engineering, ML/AI engineering, application/decision layer, V&V, deployment, and operational evidence/SRE. Iterate where justified; do not implement production data/model workloads before their required platform controls exist.

If the user requests only discovery, architecture, steps 1–3, or stop before platform foundation, record that boundary and stop there. A handoff, fictional work order, completed diagram or successful template check does not cancel it. Do not start unrelated platform or project work while modifying reusable skills.

## Handoff record and return contract

At every skill transition, write or update the project handoff with:

1. Current lifecycle phase, objective, authorized scope and maturity.
2. Input/output artifact IDs, versions and locations; preserve requirement/acceptance IDs.
3. Decisions, owners, authority and real versus simulated approval state.
4. Open items, assumptions, risks, dependencies and affected gates.
5. Receiving skill and accountable project role.
6. Next permitted activity and explicit stop boundary.
7. Expected return artifacts, evidence and review decision.

For Phase 7, expect applicability, tailoring, SEMP and unresolved assurance conditions. For Phase 8, expect technical artifacts and evidence appropriate to the requested increment, not automatic production readiness. Return those to customer reviews and standards checks. Reopen discovery only where changed scope or evidence makes earlier answers invalid.

## Completion vocabulary

Report separately whether the reusable skill is installed, the interview record is prepared, the design is reviewed, the system is implemented/tested, the customer has accepted it, and the service is active. Each is a different claim with a different evidence basis. A fictional portfolio can exercise the process and document assumptions; real customer/site outcomes require real evidence.

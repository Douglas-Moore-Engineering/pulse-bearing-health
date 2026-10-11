# DME control library

Apply this matrix together with the main workflow. Tier is an internal assurance profile. `ALL` applies at every tier; `TRIGGER` applies at every tier when its condition is present. All applicable rows require measurable project requirements, evidence, an owner and a gate. G4 requires every applicable row; N/A is permitted only when the trigger genuinely does not exist, never to waive essential assurance.

| ID | Minimum applicability | Control / evidence expectation | Gate |
|---|---|---|---|
| AIG-C01 | ALL | Inventory, purpose, non-AI alternative, system boundary, intended/prohibited use, accountable owner | 0 |
| AIG-C02 | ALL | Inherent/residual risk, consequence scenarios, exposure, affected parties, uncertainty and tier rationale | 1 |
| AIG-C03 | ALL | Laws/contracts/policy applicability, legal classification distinct from DME tier, verified sources and unresolved obligations | 1 |
| AIG-C04 | ALL | Named accountability, authority/delegation, competence, stop/restart authority and escalation | 1 |
| AIG-C05 | ALL | Applicable control register, tailoring approval, testable requirements, acceptance criteria and assurance plan | 1 |
| AIG-C06 | ALL | Data/corpus rights, allowed purposes, permissions, provenance, lineage, retention/deletion and quality evidence | 3 |
| AIG-C07 | ALL | Model/system card, versions, capabilities, limitations, operational envelope and failure modes | 3 |
| AIG-C08 | TRIGGER: third-party AI/data/tools | Supplier due diligence: licenses, data use/training terms, locations, retention, subprocessors, security, updates, support, incident notice, exit and shared responsibilities | 3 |
| AIG-C09 | ALL | Fit-for-purpose evaluation of the complete decision workflow; leakage protection, representative tests, reproducibility and uncertainty | 4 |
| AIG-C10 | ALL | Threat review, least privilege, integrity, privacy-aware audit, access boundaries and tested relevant abuse mitigations | 2,4 |
| AIG-C11 | TRIGGER: people affected or sensitive data | Privacy/human-rights and differential-impact assessment, justified fairness measures, legal data basis, contestability/redress and confidentiality | 1,4 |
| AIG-C12 | ALL | Oversight specification, usable disclosure and limitations, traceable decisions; test any claimed effective human intervention | 2,4 |
| AIG-C13 | ALL | Appropriate explainability/transparency for intended decisions; validate explanations and distinguish associations from causal claims | 4 |
| AIG-C14 | ALL | Failure/abstention, operating bounds, rollback/recovery and safe manual/degraded continuity; demonstrate behavior proportionate to harms | 2,4 |
| AIG-C15 | ALL | Requirement-to-implementation-to-test-to-evidence trace, defect disposition and freshness checks | 4 |
| AIG-C16 | ALL | Residual risks and cumulative interactions, authorized acceptance, non-waivable obligations | 5 |
| AIG-C17 | ALL | Exact release binding, authenticated approval, expiry/revocation, protected promotion, bypass verification | 5 |
| AIG-C18 | ALL | Monitoring thresholds/windows/coverage, named responses, delayed labels, control-health tests and harm feedback | 5,6 |
| AIG-C19 | ALL | Material-change triggers, preapproved envelope, affected-gate revalidation and no uncontrolled self-promotion | 6 |
| AIG-C20 | ALL | Incident roles, safe containment, evidence preservation, obligations-specific notification and re-entry criteria | 5,6 |
| AIG-C21 | ALL | Periodic governance review, management oversight, complaints/findings, corrective actions and improvement | 6 |
| AIG-C22 | ALL | Retirement dependencies, access revocation, data/model disposition and legally bounded evidence retention | 7 |
| AIG-C23 | G3,G4 | Qualified independent assurance reviewer, conflict disclosure, evidence access and documented findings/closure | 4 |
| AIG-C24 | G4 | Independent V&V and release review, separate from implementation; independence criteria and actual human records | 4,5 |
| AIG-C25 | G3,G4 or TRIGGER: physical/mission hazards | Hazard/misuse analysis, fault propagation, foreseeable operator error, safe-state determination and domain overlays | 2,4 |
| AIG-C26 | G4 | Structured assurance/safety case, claim–argument–evidence, assumptions, rebuttals, residual uncertainty and operating envelope | 4,5 |
| AIG-C27 | G4 or TRIGGER: required by hazards | Independent deterministic protective boundary, containment, redundant/diverse monitoring with common-cause analysis; tested safe response under fault | 2,4 |
| AIG-C28 | G4 | Exercises of degraded modes, loss of communication/data, corrupted inputs, monitor failure, restart, emergency authority and recovery | 4,5 |
| AIG-C29 | TRIGGER: GenAI/RAG | Grounding, hallucination, retrieval relevance/corpus rights, harmful content, disclosure, injection, sensitive-data leakage and evaluation provenance | 3,4 |
| AIG-C30 | TRIGGER: agents/tool use/autonomy | Tool allowlists/scoped credentials, sandboxing, action authorization, budgets/timeouts, memory isolation, validation, feedback-loop controls and tested external stop | 2,4 |
| AIG-C31 | TRIGGER: cyber-physical/critical infrastructure | OT segregation, no undocumented control writes, base-control independence, interlock integrity and applicable sector safety/security evidence | 2,4 |
| AIG-C32 | TRIGGER: legal/customer/domain requirement | Required registration, conformity assessment, approved environment, specialist review or regulator/customer authorization; attach authentic evidence | 5 |
| AIG-C33 | ALL at organization scope | AI policy/objectives, portfolio inventory, resources/competence, internal audit, management review and corrective actions; link shared organizational records | 1,6 |

Use security and systems engineering records as authoritative for their technical subjects. Governance verifies applicability, traceability and acceptance; it does not replace threat analysis or engineering tests. Record evidentiary scope: planned, implemented, tested, independently reviewed or authorized. Training completion, a document or a vendor claim alone cannot establish effectiveness.

For C33 distinguish project readiness from organization-wide management-system conformity. A project with good evidence cannot establish that the whole organization conforms to ISO/IEC 42001.

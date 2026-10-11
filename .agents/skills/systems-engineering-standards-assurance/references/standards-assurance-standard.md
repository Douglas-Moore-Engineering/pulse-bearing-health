# Standards assurance reference

Preserve this supplied DME baseline as reference guidance. Edition and publication-status statements below are inherited from the source, not a fresh verification. Before adopting them for an engagement, verify publisher metadata and record the chosen edition, source, access date, and contractual basis. Distinguish public summaries from full normative text.

## Contents

- [1. Mandatory Operating Principles](#1-mandatory-operating-principles)
- [2. Governing Reference Set](#2-governing-reference-set)
- [3. Standards Applicability and Tailoring Review](#3-standards-applicability-and-tailoring-review)
- [4. Life-Cycle Management and Tailoring Assurance](#4-life-cycle-management-and-tailoring-assurance)
- [5. Systems Engineering Management Plan (SEMP)](#5-systems-engineering-management-plan-semp)
- [6. ISO/IEC/IEEE 15288 Process Assurance](#6-isoiecieee-15288-process-assurance)
- [7. ISO/IEC/IEEE 12207 Software Life-Cycle Assurance](#7-isoiecieee-12207-software-life-cycle-assurance)
- [8. ISO/IEC/IEEE 42010 Architecture-Description Assurance](#8-isoiecieee-42010-architecture-description-assurance)
- [9. ISO/IEC/IEEE 29148 Requirements-Engineering Assurance](#9-isoiecieee-29148-requirements-engineering-assurance)
- [10. IEEE 1012 Verification and Validation Assurance](#10-ieee-1012-verification-and-validation-assurance)
- [11. ISO/IEC/IEEE 15289 Information-Item Governance](#11-isoiecieee-15289-information-item-governance)
- [12. ISO/IEC 25010 Product-Quality Assurance](#12-isoiec-25010-product-quality-assurance)
- [13. ISO/IEC 23894 AI Risk-Management Assurance](#13-isoiec-23894-ai-risk-management-assurance)
- [14. AI Management-System and Impact-Assessment Overlays](#14-ai-management-system-and-impact-assessment-overlays)
- [15. INCOSE Handbook Alignment](#15-incose-handbook-alignment)
- [16. Standards Crosswalk Register](#16-standards-crosswalk-register)
- [17. Organizational-Control Boundary](#17-organizational-control-boundary)
- [18. Standards Review at Lifecycle Gates](#18-standards-review-at-lifecycle-gates)
- [19. Standards Change Management](#19-standards-change-management)
- [20. Standards-Claim Language](#20-standards-claim-language)
- [21. Standards Assurance Quality Gate](#21-standards-assurance-quality-gate)
- [22. Interaction with the Other DME Skills](#22-interaction-with-the-other-dme-skills)
- [23. Default DME Standards-Assurance Position](#23-default-dme-standards-assurance-position)

# Systems Engineering Standards Assurance

## Purpose

Govern Douglas Moore Engineering (DME) standards alignment, tailoring, systems-engineering management, architecture-description assurance, requirements quality, verification and validation rigor, information-item governance, product-quality coverage, and AI-risk management across customer and internal engineering work.

This skill complements:

- **Customer Delivery & Service Operations** — governs customer intake, scope, responsibility, acceptance, service, handoff, and exit.
- **Build Production AI Systems** — governs the technical lifecycle from business/system definition through architecture, implementation, runtime verification, site adaptation, production release, and continuous revalidation.

This skill does **not** claim certification, accreditation, or formal conformity merely because a mapping exists. It defines the controls and evidence DME must establish before making any standards-alignment or conformity statement.

---

# 1. Mandatory Operating Principles

1. Standards applicability must be determined explicitly for every substantial engagement or product increment.
2. Do not claim compliance, certification, accreditation, or conformity unless the applicable requirements have been assessed and the claim is authorized and supportable.
3. Use the current published edition of each applicable standard unless a customer, contract, regulator, or approved baseline requires another edition.
4. Track standards that are under revision separately from currently published standards; drafts do not silently replace active editions.
5. Tailoring is permitted only when the governing standard and engagement allow it. Tailored-out activities require rationale, authority, risk assessment, and downstream-impact analysis.
6. Standards mapping is evidence-based. A document title or repository folder is not proof that a standard requirement is satisfied.
7. Preserve traceability from standard/process obligation to DME control, project artifact, verification evidence, owner, and status.
8. Separate organization-level controls from project-level controls, customer-owned controls, supplier controls, and Not Applicable items.
9. When standards overlap, use one implementation control to satisfy multiple obligations where defensible, but retain each mapping independently.
10. Any conflict among contract terms, customer policy, law/regulation, safety obligations, and DME standards must be escalated to the appropriate authority; do not resolve such conflicts informally.
11. Formal safety, security, regulated-industry, or government frameworks are overlays. Their presence does not replace the core systems-engineering lifecycle.
12. Standards assurance must evolve with the system. Material architecture, requirement, model, threshold, deployment, site, or operating changes trigger an applicability and revalidation review.

---

# 2. Governing Reference Set

Use the following as the primary DME standards-assurance baseline unless an engagement specifies otherwise.

| Reference | DME use | Current baseline |
|---|---|---|
| INCOSE Systems Engineering Handbook | Good-practice interpretation and application guidance for systems engineering | Fifth Edition |
| ISO/IEC/IEEE 15288 | System life-cycle processes | 2023 |
| ISO/IEC/IEEE 12207 | Software life-cycle processes | 2026 |
| ISO/IEC/IEEE 42010 | Architecture-description structure and concepts | 2022 |
| ISO/IEC/IEEE 29148 | Requirements engineering | 2018, until superseded by a published replacement or contractually required edition |
| ISO/IEC/IEEE 15289 | Life-cycle information-item/documentation content | 2019, until superseded by a published replacement or contractually required edition |
| ISO/IEC/IEEE 24748-1 | Life cycle management guidance and tailoring | 2024 |
| ISO/IEC/IEEE 24748-4 | Systems engineering management planning / SEMP | 2026 |
| IEEE 1012 | System, software, and hardware verification and validation | 2024 |
| ISO/IEC 25010 | Product quality model | 2023 |
| ISO/IEC 23894 | AI risk-management guidance | 2023 |
| ISO/IEC 42001 | AI management system requirements (organization-level overlay when applicable) | 2023 |
| ISO/IEC 42005 | AI system impact assessment guidance/requirements overlay when applicable | 2025 |

The INCOSE Systems Engineering Handbook is used as good-practice guidance aligned to ISO/IEC/IEEE 15288; it is not a certification standard by itself.

The standards register must record publication status and known successor/draft activity where relevant. A draft or committee draft may inform planning but must be labeled as non-final unless the customer explicitly adopts it.

---

# 3. Standards Applicability and Tailoring Review

Perform a Standards Applicability Review (SAR) before the requirements baseline is frozen and repeat it when the operating context materially changes.

Required questions:

- What is the system of interest?
- What software elements exist?
- What customer/contractual standards apply?
- What regulatory or safety standards apply?
- What security/compliance frameworks apply?
- What industry/OT standards apply?
- Which lifecycle stages are in DME scope?
- Which processes are DME-owned, customer-owned, shared, supplier-owned, or N/A?
- What level of V&V rigor is appropriate to the system/function criticality?
- Which information items must be produced and retained?
- Which architecture-description obligations apply?
- What quality characteristics must be addressed?
- What AI-specific risks require treatment?

Required artifact:

```text
governance/
└── standards/
    └── standards_applicability_matrix.csv
```

Minimum columns:

```text
Standard
Edition
Clause_or_Process
Obligation_or_Intent
Applicability
Tailoring_Decision
Rationale
DME_Control
Artifact_or_Evidence
Owner
Approver
Status
Review_Trigger
```

Allowed applicability states:

- Applicable
- Partially Applicable
- Customer Owned
- Supplier Owned
- Organization Level
- Not Applicable
- Deferred / Pending Decision

A Not Applicable decision must never be blank-rationale.

---


# 4. Life-Cycle Management and Tailoring Assurance

Use **ISO/IEC/IEEE 24748-1:2024** to govern life-cycle model selection, stages, process application, adaptation, and tailoring in conjunction with ISO/IEC/IEEE 15288 and ISO/IEC/IEEE 12207.

For every substantial engagement, record:

- selected life-cycle model or combination of models,
- life-cycle stages and decision points,
- how 15288/12207 processes are applied across those stages,
- iterative/incremental/concurrent execution where used,
- tailoring decisions and rationale,
- entry/exit criteria for major stages,
- recursive application to system elements where applicable,
- customer/supplier interfaces across stages,
- re-entry/revalidation triggers when the system or operating context changes.

Required artifact:

```text
governance/
└── standards/
    └── lifecycle_tailoring_record.md
```

A project must not claim lifecycle alignment merely because it uses phase names similar to a standard. The tailoring record must show how the selected lifecycle actually applies the relevant processes and evidence.

---

# 5. Systems Engineering Management Plan (SEMP)

A substantial system must have an explicit **Systems Engineering Management Plan** or an equivalent governed information item.

The SEMP is the authoritative plan for how systems engineering will be managed and executed for the system or engagement.

At minimum, address:

- system of interest and scope,
- lifecycle model and lifecycle stages,
- lifecycle tailoring,
- organization and roles,
- technical authority,
- customer/supplier interfaces,
- engineering reviews and decision gates,
- requirements management,
- architecture management,
- interface management,
- technical planning,
- project assessment/control interfaces,
- decision management,
- risk and opportunity management,
- configuration management,
- information management,
- measurement,
- quality assurance,
- V&V strategy,
- integration strategy,
- transition/deployment strategy,
- operation/support engineering interfaces,
- change and revalidation strategy,
- retirement/decommissioning engineering considerations,
- standards applicability and compliance-assurance method.

Recommended artifact:

```text
docs/
└── systems-engineering-management-plan.md
```

The SEMP may reference other governed documents rather than duplicating them, but references must be explicit and versioned.

---

# 6. ISO/IEC/IEEE 15288 Process Assurance

Use ISO/IEC/IEEE 15288 as the primary system-life-cycle process framework.

## 5.1 Agreement processes

Ensure the customer-delivery skill covers acquisition/supply responsibilities where applicable:

- acquisition expectations,
- supplier responsibilities,
- deliverables,
- acceptance,
- changes,
- transfer/closure.

## 5.2 Organizational project-enabling processes

Determine whether each control is DME organization-level, customer-level, shared, or N/A:

- lifecycle-model management,
- infrastructure management,
- portfolio management,
- human-resource / competence management,
- quality management,
- knowledge management.

These controls do not need to live inside every project repository, but the project must identify the governing organizational source when applicable.

## 5.3 Technical-management processes

Explicitly govern:

- project planning,
- project assessment and control,
- decision management,
- risk management,
- configuration management,
- information management,
- measurement,
- quality assurance.

The technical build and customer-delivery skills already implement many of these controls; the standards crosswalk must point to the actual control and evidence rather than duplicating work.

## 5.4 Technical processes

Ensure coverage, as applicable, of:

- business or mission analysis,
- stakeholder needs and requirements definition,
- system requirements definition,
- architecture definition,
- design definition,
- system analysis,
- implementation,
- integration,
- verification,
- transition,
- validation,
- operation,
- maintenance,
- disposal / retirement.

The project does not pass the 15288 crosswalk merely because the lifecycle phase exists. The mapped outcome/evidence must exist for the claimed maturity state.

---

# 7. ISO/IEC/IEEE 12207 Software Life-Cycle Assurance

Apply this section when software is part of the system of interest or an enabling system.

Ensure the software lifecycle explicitly addresses, as applicable:

- software acquisition and supply interfaces,
- software requirements analysis,
- software architecture/design,
- software construction/implementation,
- software integration,
- software qualification testing,
- software installation/deployment,
- software acceptance support,
- software operation,
- software maintenance,
- software disposal/retirement,
- software configuration management,
- software quality assurance,
- problem resolution,
- software reuse where relevant.

The software lifecycle may be iterative, recursive, concurrent, and incremental. Do not force a waterfall implementation simply to resemble a standard process list.

For AI/ML systems, software assurance also includes:

- training/evaluation code,
- feature transformations,
- inference code,
- model-loading logic,
- decision/guardrail logic,
- data-contract validation,
- release tooling,
- infrastructure code,
- operational automation.

---

# 8. ISO/IEC/IEEE 42010 Architecture-Description Assurance

Every substantial architecture description must explicitly connect **stakeholders, concerns, viewpoints, model kinds, views, correspondences, and decisions**.

Required architecture-description register:

```text
architecture/
└── architecture_viewpoints.csv
```

Minimum fields:

```text
Viewpoint_ID
Name
Stakeholders
Concerns
Purpose
Model_Kind_or_Notation
Required_View_Content
Correspondence_Rules
Related_Requirements
Related_ADRs
Owner
Status
```

Each major architecture view must answer:

- Who uses this view?
- What concerns does it address?
- Which viewpoint governs it?
- What notation/model kind does it use?
- Which architecture elements are shown?
- Which relationships/correspondences must remain consistent with other views?
- Which requirements, risks, and decisions does it support?

At minimum consider viewpoints for:

- system context,
- operational/concept-of-operations,
- functional/capability,
- information/data,
- integration/interface,
- deployment/infrastructure,
- security/trust,
- AI/ML lifecycle,
- human authority/decision workflow,
- reliability/operations,
- requirements/verification traceability.

Architecture diagrams without identified concerns and consistency expectations are documentation views, not sufficient architecture-description assurance by themselves.

---

# 9. ISO/IEC/IEEE 29148 Requirements-Engineering Assurance

Every governed requirement must be reviewable for quality and traceability.

Minimum requirement attributes should include, as applicable:

```text
Requirement_ID
Type
Statement
Source
Rationale
Owner
Priority
Risk_or_Criticality
Status
Parent_Trace
Child_Trace
Verification_Method
Acceptance_Criterion
Version
Effective_Date
```

Review each requirement for the following qualities:

- necessary,
- appropriate,
- singular / atomic,
- unambiguous,
- complete enough for its level,
- feasible,
- verifiable,
- traceable,
- consistent with peer requirements,
- implementation-independent where implementation freedom is required,
- stated with measurable bounds where verification depends on quantity or threshold.

Avoid vague terms such as:

- fast,
- scalable,
- secure,
- user friendly,
- robust,
- highly available,
- real time,

unless they are defined by measurable acceptance criteria or an explicitly referenced standard/SLO.

Requirements changes must preserve version history and impact analysis.

---

# 10. IEEE 1012 Verification and Validation Assurance

V&V rigor must be proportional to the integrity/criticality of the system or function.

Establish a V&V classification for each consequential capability or subsystem.

Required attributes:

```text
Item_or_Function
Criticality_or_Integrity_Level
Failure_Consequence
Required_VV_Rigor
Required_Independence
Verification_Methods
Validation_Methods
Evidence
Release_Gate
```

The exact integrity-level scheme may be customer-, industry-, or program-specific. Do not invent a false IEEE conformity level when the engagement has not adopted one.

Higher-risk capabilities should generally require stronger combinations of:

- independent review,
- static analysis,
- unit testing,
- integration testing,
- system testing,
- negative testing,
- fault injection,
- security testing,
- recovery/rollback testing,
- performance/capacity testing,
- representative-environment testing,
- independent validation,
- witnessed acceptance testing.

For AI/ML capabilities also consider:

- leakage checks,
- holdout discipline,
- calibration,
- domain shift,
- abstention,
- false-alert burden,
- deterministic/reproducible execution where required,
- artifact/model integrity,
- site-specific validation,
- human-factors validation.

Verification asks whether the implementation satisfies specified requirements. Validation asks whether the resulting system satisfies intended use and stakeholder needs in its intended context. Preserve that distinction in evidence and reviews.

---

# 11. ISO/IEC/IEEE 15289 Information-Item Governance

Governed engineering information must be identifiable, controlled, reviewable, and maintainable.

Every major information item should carry, directly or through repository metadata:

- title/name,
- artifact type,
- owner,
- approver,
- status,
- version,
- effective date,
- classification,
- retention requirement,
- related lifecycle process,
- related requirements/risks/decisions,
- supersedes / superseded-by relationship where applicable,
- storage location,
- customer visibility where applicable.

Recommended information-item types include:

- policy,
- plan,
- procedure,
- report,
- request,
- record,
- description,
- specification.

Do not create redundant documents solely to match a standard name. One governed artifact may satisfy multiple information-item needs if its purpose/content is clear and the mapping is maintained.

Because ISO/IEC/IEEE 15289:2019 is currently published but under revision, record the edition used for each engagement and review the mapping when a successor edition is formally published or contractually adopted.

---

# 12. ISO/IEC 25010 Product-Quality Assurance

Use the ISO/IEC 25010 product-quality model as a completeness check for software/ICT product quality requirements.

Assess all nine current product-quality characteristics for applicability:

1. Functional suitability
2. Performance efficiency
3. Compatibility
4. Interaction capability
5. Reliability
6. Security
7. Maintainability
8. Flexibility
9. Safety

For each applicable characteristic:

- identify NFRs/SLOs,
- define measurable acceptance criteria,
- assign verification methods,
- define monitoring where the characteristic must remain valid in operation,
- record Not Applicable rationale where appropriate.

The quality-model check supplements project-specific NFRs; it does not replace domain-specific safety, security, usability, accessibility, or regulatory requirements.

---

# 13. ISO/IEC 23894 AI Risk-Management Assurance

For systems that develop, deploy, or use AI, maintain a governed AI-risk process integrated with the broader project risk process.

Required artifact:

```text
governance/
└── ai_risk_register.csv
```

Minimum fields:

```text
AI_Risk_ID
Scenario
Source
Affected_Stakeholders
Cause
Consequence
Likelihood
Impact
Existing_Controls
Residual_Risk
Treatment
Owner
Acceptance_Authority
Evidence
Review_Trigger
Status
```

Consider, as applicable:

- data quality and representativeness,
- label quality,
- leakage,
- bias/fairness impacts,
- domain shift,
- model uncertainty,
- calibration,
- false positives/false negatives,
- automation bias,
- over-reliance,
- explainability limitations,
- adversarial or malicious inputs,
- model/artifact tampering,
- privacy,
- security,
- supplier/model-provider dependency,
- generative-AI hallucination/tool misuse,
- unsafe optimization objectives,
- feedback loops,
- monitoring blind spots,
- human authority confusion,
- inappropriate use outside validated scope.

AI risks must be linked to requirements, controls, V&V evidence, operational monitoring, and release gates where relevant.

---

# 14. AI Management-System and Impact-Assessment Overlays

When DME itself, a customer, or a contract requires organization-level AI governance beyond project risk management, evaluate **ISO/IEC 42001:2023** as an applicable management-system overlay. It specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS).

When an AI system impact assessment is required by customer policy, governance, regulation, procurement, or risk posture, evaluate **ISO/IEC 42005:2025** as an applicable overlay.

These standards do not automatically apply to every project. The Standards Applicability Review must state whether they are:

- Applicable,
- Organization Level,
- Customer Owned,
- Partially Applicable, or
- Not Applicable with rationale.

Do not claim ISO/IEC 42001 conformity or certification unless the organization-level management-system requirements and conformity-assessment basis are actually established.

---

# 15. INCOSE Handbook Alignment

Use the INCOSE Systems Engineering Handbook Fifth Edition as good-practice guidance for applying systems-engineering concepts and ISO/IEC/IEEE 15288 lifecycle processes.

The DME framework should demonstrate, where applicable:

- system thinking and lifecycle orientation,
- stakeholder engagement,
- needs and requirements transformation,
- architecture and design reasoning,
- integration and interface discipline,
- verification and validation,
- technical management,
- risk and decision management,
- configuration/information management,
- tailoring,
- transition, operation, support, and retirement,
- iterative/incremental application where appropriate.

Do not state that a project is “INCOSE compliant.” Prefer precise language such as:

- “aligned with INCOSE Systems Engineering Handbook practices,”
- “mapped to ISO/IEC/IEEE 15288 processes,”
- “uses INCOSE-aligned systems-engineering practices.”

---

# 16. Standards Crosswalk Register

Every substantial DME system should maintain a consolidated standards crosswalk when standards alignment is a customer, regulatory, contractual, or portfolio requirement.

Recommended artifact:

```text
governance/
└── standards/
    ├── standards_applicability_matrix.csv
    ├── standards_crosswalk.csv
    └── standards_assurance_summary.md
```

Minimum crosswalk columns:

```text
Crosswalk_ID
Standard
Edition
Clause_or_Process
Requirement_or_Intent
DME_Skill
DME_Section
Project_Control
Artifact
Evidence
Owner
Status
Gap
Remediation
Reviewer
Last_Reviewed
```

Allowed status values:

- Satisfied
- Partially Satisfied
- Not Satisfied
- Not Applicable
- Customer Owned
- Organization Level
- Pending Evidence
- Pending Decision

Never convert “mapped” into “satisfied” without evidence.

---

# 17. Organizational-Control Boundary

Some standards obligations exist above the project/repository level.

Typical organization-level controls include:

- lifecycle-model governance,
- portfolio governance,
- competence/qualification management,
- quality-management system,
- organizational infrastructure,
- reusable asset governance,
- knowledge management,
- corporate information retention,
- approved supplier governance,
- enterprise policy management.

For each applicable organization-level control, the project must identify:

- governing DME/customer policy or process,
- control owner,
- evidence location,
- project dependency,
- gap/escalation path.

Do not duplicate confidential HR, finance, legal, or corporate-management records into technical repositories merely to demonstrate awareness of the control.

---

# 18. Standards Review at Lifecycle Gates

Perform standards-assurance checks at minimum at:

- Discovery / engagement baseline,
- Requirements Baseline Review,
- Architecture Review,
- Reference Release Review,
- Site Readiness Review,
- ORR,
- Customer Acceptance Review where applicable,
- major production change/revalidation,
- retirement/decommissioning.

At each review ask:

- Did applicability change?
- Did the standard edition/baseline change?
- Did any tailoring assumption become invalid?
- Are mapped controls implemented?
- Is evidence current?
- Are gaps blocking the next gate?
- Are organization/customer/supplier dependencies identified?
- Do changed risks require increased V&V rigor?

---

# 19. Standards Change Management

Standards evolve. Maintain a lightweight standards register containing:

```text
Standard
Baseline_Edition
Publication_Status
Successor_or_Draft
Contractual_Baseline
Impact_Review_Status
Owner
Next_Review_Date
```

Rules:

- a newly published edition does not automatically invalidate an active contractual baseline,
- assess impact before changing the project baseline,
- document customer/regulatory approval when the governing baseline changes,
- do not rewrite historical evidence as if a newer edition applied retroactively,
- update reusable DME skills/frameworks when a newer edition materially changes good practice.

---

# 20. Standards-Claim Language

Use precise language externally.

Allowed examples when true:

- “The engineering lifecycle is mapped to ISO/IEC/IEEE 15288:2023.”
- “The software lifecycle is aligned with ISO/IEC/IEEE 12207:2026.”
- “Architecture documentation follows ISO/IEC/IEEE 42010:2022 concepts.”
- “Requirements engineering is mapped to ISO/IEC/IEEE 29148:2018.”
- “V&V planning uses IEEE 1012-2024 integrity-based rigor concepts.”
- “The SEMP structure is based on ISO/IEC/IEEE 24748-4:2026.”
- “AI risk management is informed by ISO/IEC 23894:2023.”

Prohibited unless formally established and authorized:

- “ISO certified” when DME/system is not certified,
- “IEEE certified,”
- “INCOSE certified system,”
- “fully compliant” based only on a self-authored crosswalk,
- “conforms to every clause” without clause-level evidence and an authorized assessment basis.

When formal conformity is required, define the conformity-assessment method, assessor independence, evidence set, and approval authority.

---

# 21. Standards Assurance Quality Gate

Before calling standards assurance complete for a lifecycle state, verify the applicable items:

- standards applicability review exists,
- editions/baselines are recorded,
- SEMP exists or equivalent rationale is documented,
- 15288 process mapping is current,
- organization-level process ownership is identified,
- software lifecycle mapping exists where software is in scope,
- architecture viewpoints/concerns are governed,
- requirements-quality review is complete,
- V&V rigor/independence is matched to criticality,
- information items are governed,
- product-quality characteristics were reviewed,
- AI risk register exists where AI is in scope,
- tailoring decisions have rationale and authority,
- gaps have owners/remediation/accepted disposition,
- evidence supports every “Satisfied” status,
- customer/supplier-owned controls are not falsely claimed as DME controls,
- current release claims do not exceed the maturity/evidence state,
- no certification/conformity claim exceeds the actual assessment basis.

A standards crosswalk with unresolved critical gaps is **not** a standards-assurance PASS.

---

# 22. Interaction with the Other DME Skills

Use the three skills together as follows:

```text
Customer Delivery & Service Operations
        ↓
Intake / Discovery / Scope / Responsibilities / Acceptance
        ↓
Systems Engineering Standards Assurance
        ↓
Standards applicability / tailoring / SEMP / assurance plan
        ↓
Build Production AI Systems
        ↓
Architecture / Platform / Data / AI / V&V / Runtime Verification
        ↓
Systems Engineering Standards Assurance
        ↓
Requirements / architecture / V&V / information-item / risk checks at gates
        ↓
Customer Delivery & Service Operations
        ↓
CAR / Production Transition / Support / Handoff / Exit
```

The standards-assurance skill is **cross-cutting**. It begins before the technical build and remains active through production operation and retirement.

Do not duplicate artifacts across skills when one governed artifact can satisfy multiple purposes. Maintain traceable references instead.

---

# 23. Default DME Standards-Assurance Position

For substantial DME systems, default to:

- ISO/IEC/IEEE 15288-aligned system lifecycle,
- ISO/IEC/IEEE 12207-aligned software lifecycle when software is in scope,
- ISO/IEC/IEEE 42010-aligned architecture descriptions,
- ISO/IEC/IEEE 29148-aligned requirements engineering,
- ISO/IEC/IEEE 24748-4-based SEMP,
- IEEE 1012-based integrity-aware V&V rigor,
- ISO/IEC/IEEE 15289-informed information-item governance,
- ISO/IEC 25010 quality-model coverage,
- ISO/IEC 23894 AI-risk guidance when AI is in scope,
- INCOSE Systems Engineering Handbook Fifth Edition as good-practice guidance.

The objective is not to create paperwork for its own sake.

The objective is to make DME engineering **traceable, tailorable, reviewable, defensible, and auditable** while preserving the distinction between standards alignment and formal certification/conformity.

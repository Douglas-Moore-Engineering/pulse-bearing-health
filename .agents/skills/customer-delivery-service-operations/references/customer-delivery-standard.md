# Customer delivery reference

Use this supplied DME customer-delivery standard for detailed controls at the applicable lifecycle phase. Read the main skill for discovery execution, dependency resolution and current handoff rules. Preserve existing customer authorization and explicit user scope; a document review is not a reason to request the same authorization again.

## Contents

- [1. Mandatory operating principles](#1-mandatory-operating-principles)
- [2. Authoritative customer-delivery lifecycle](#2-authoritative-customer-delivery-lifecycle)
- [3. Customer Intake and Qualification](#3-customer-intake-and-qualification)
- [4. Discovery and Problem Framing](#4-discovery-and-problem-framing)
- [5. Scope and Responsibility Baseline](#5-scope-and-responsibility-baseline)
- [6. SOW-to-Engineering Traceability](#6-sow-to-engineering-traceability)
- [7. Commercial and Contract Governance](#7-commercial-and-contract-governance)
- [8. Deployment and Ownership Model](#8-deployment-and-ownership-model)
- [9. Customer Data, Privacy, Security and Retention Baseline](#9-customer-data-privacy-security-and-retention-baseline)
- [10. Intellectual Property and Reuse Boundary](#10-intellectual-property-and-reuse-boundary)
- [11. Customer-Specific Security / Compliance Overlay](#11-customer-specific-security--compliance-overlay)
- [12. Customer Decision Reviews During Delivery](#12-customer-decision-reviews-during-delivery)
- [13. Change Control](#13-change-control)
- [14. Customer Acceptance Review (CAR)](#14-customer-acceptance-review-car)
- [15. Production Transition and Service Activation](#15-production-transition-and-service-activation)
- [16. Support and Service Management](#16-support-and-service-management)
- [17. Operational Reporting](#17-operational-reporting)
- [18. Customer Training and Enablement](#18-customer-training-and-enablement)
- [19. Handoff / Transfer Standard](#19-handoff--transfer-standard)
- [20. Renewal / Extension Decision](#20-renewal--extension-decision)
- [21. Decommissioning and Exit Standard](#21-decommissioning-and-exit-standard)
- [22. Customer-Facing Repository / Workspace Standard](#22-customer-facing-repository--workspace-standard)
- [23. Evidence and Status Vocabulary](#23-evidence-and-status-vocabulary)
- [24. Customer Delivery Quality Gate](#24-customer-delivery-quality-gate)
- [25. Interaction with the Other DME Skills](#25-interaction-with-the-other-dme-skills)
- [26. Default DME Customer Standard](#26-default-dme-customer-standard)

# Customer Delivery & Service Operations

## Purpose

Govern Douglas Moore Engineering (DME) customer engagements from first contact through discovery, scope definition, system delivery, customer acceptance, production support, change management, handoff, renewal, and decommissioning.

This skill complements **Build Production AI Systems** and **Systems Engineering Standards Assurance**. It does not replace the technical engineering lifecycle or standards-assurance lifecycle. Instead, it defines the customer-facing operating controls that surround and govern those lifecycles so DME can deliver systems to paying customers without ambiguity in scope, ownership, acceptance, support, data handling, standards obligations, or exit responsibilities.

The standard is designed for enterprise AI, cloud, data, industrial, and systems-engineering engagements where technical work may involve customer infrastructure, data, production operations, regulated environments, standards obligations, or ongoing support.

---

# 1. Mandatory operating principles

1. Customer delivery begins before engineering starts and continues after production release.
2. Never begin substantive implementation without a documented problem statement, scope, decision authority, responsibilities, assumptions, constraints, acceptance criteria, and deployment/ownership model.
3. Contracted scope, engineering requirements, deliverables, verification evidence, and customer acceptance must remain traceable to one another.
4. Do not treat verbal expectations as acceptance criteria. Convert material expectations into written, versioned artifacts.
5. Do not allow customer-owned responsibilities to remain implicit. Every dependency must have an owner and due date or remain an explicit delivery risk.
6. Separate DME reusable IP from customer-specific configuration, customer data, customer-trained artifacts, and customer-owned infrastructure.
7. Never retain, reuse, redistribute, or expose customer data, secrets, credentials, or proprietary artifacts outside the approved scope.
8. Never call a system accepted, production-ready, handed off, or decommissioned without evidence appropriate to that state.
9. Customer approval does not override unresolved critical safety, security, integrity, or legal constraints. Escalate and document exceptions.
10. Any material scope, requirement, architecture, threshold, deployment, support, cost, or ownership change must enter formal change control.
11. Every engagement must have an explicit closure path: production support, handoff, renewal, suspension, or decommissioning.
12. When a customer-specific rule conflicts with the DME production-system standard, document the conflict, decision authority, risk, and resulting operating boundary.

---

# 2. Authoritative customer-delivery lifecycle

Use this lifecycle unless a documented engagement decision justifies a deviation.

1. **Lead qualification / intake**
2. **Discovery and problem framing**
3. **Engagement scope and responsibility baseline**
4. **Commercial / SOW-to-engineering translation**
5. **Customer environment and deployment-model decision**
6. **Data, security, privacy, compliance, and IP baseline**
7. **Standards applicability / tailoring / SEMP baseline** using the separate Systems Engineering Standards Assurance skill
8. **Production-system engineering** using the separate Build Production AI Systems skill
9. **Customer decision reviews and change control during delivery**
10. **Reference release / demonstration review**
11. **Customer/site adaptation**
12. **Site validation / shadow / canary**
13. **Operational Readiness Review (ORR)**
14. **Customer Acceptance Review (CAR)**
15. **Production release / transition to service**
16. **Production support and service management**
17. **Change, enhancement, retraining, and revalidation management**
18. **Handoff / transfer / renewal decision**
19. **Decommissioning / exit / evidence closure**

No phase is silently skipped. A phase may be marked **Not Applicable** only with rationale, owner/approver, and downstream impact.

---

# 3. Customer Intake and Qualification

Before committing engineering effort, establish whether the opportunity is sufficiently defined and appropriate for DME.

Capture at minimum:

- customer organization and business unit,
- executive/business sponsor,
- technical sponsor,
- operational/site owner where applicable,
- problem statement,
- affected process or workflow,
- desired measurable outcomes,
- urgency / target date,
- current system landscape,
- expected users,
- estimated data availability,
- cloud/on-prem constraints,
- security/regulatory constraints,
- integration dependencies,
- procurement/vendor requirements,
- decision process,
- funding/budget constraints if disclosed,
- whether the customer expects advisory work, architecture, implementation, production operation, or all of the above.

## 3.1 Qualification gate

Do not advance to a delivery commitment until the engagement has a plausible:

- business problem,
- accountable sponsor,
- decision path,
- data/environment path,
- acceptance path,
- commercial path.

If one is missing, record the engagement as discovery-only, advisory-only, blocked, or declined rather than pretending full delivery is possible.

---

# 4. Discovery and Problem Framing

Discovery must produce a shared understanding of the problem before system requirements are frozen.

Establish:

- current-state workflow,
- current pain/failure modes,
- baseline metrics,
- desired future-state workflow,
- stakeholders and affected roles,
- success criteria,
- explicit non-goals,
- assumptions,
- constraints,
- known risks,
- dependencies,
- authority boundaries,
- customer decision rights,
- required external approvals,
- initial data/source inventory,
- initial deployment/integration constraints.

Required discovery artifacts should include, as applicable:

```text
customer/
├── discovery_summary.md
├── stakeholder_register.csv
├── assumptions_register.md
├── constraints_register.md
├── dependency_register.csv
├── risk_register.csv
└── decision_authority_matrix.md
```

Discovery conclusions must be reviewable and approved before they are used as the basis for contractual or engineering commitments.

---

# 5. Scope and Responsibility Baseline

Create an explicit boundary between DME obligations, customer obligations, shared obligations, and third-party obligations.

Required scope dimensions:

- in scope,
- out of scope,
- deliverables,
- customer-provided inputs,
- third-party dependencies,
- environments,
- integrations,
- data sources,
- user populations,
- locations/sites,
- support scope,
- documentation scope,
- training scope,
- acceptance scope,
- transition/handoff scope.

## 5.1 Responsibility Assignment Matrix

Every engagement should maintain a responsibility matrix with at least:

| Area | DME | Customer | Shared / Third Party |
|---|---|---|---|
| Business requirements | Draft / refine | Approve | — |
| Architecture | Lead | Review / approve where required | — |
| Source access | Support | Provide / authorize | Source owner |
| Data mapping | Lead | Validate | Process owner |
| Cloud subscription/account | As contracted | As contracted | Cloud provider |
| IAM approval | Implement if scoped | Approve | Enterprise IAM |
| Plant/network connectivity | Design/support | Authorize/operate | OT/network teams |
| Model validation | Lead | Validate business/operational meaning | Domain SME |
| Production approval | Evidence/support | Authorize | Governance board if applicable |
| Incident response | As support contract defines | As operating model defines | Providers where relevant |

The actual matrix must reflect the specific contract and environment; do not copy this example mechanically.

## 5.2 Dependency ownership rule

A blocked customer-owned dependency is not a DME delivery failure if it was explicitly assigned, tracked, escalated, and handled according to the agreement.

---

# 6. SOW-to-Engineering Traceability

Translate commercial commitments into technical and acceptance artifacts.

Maintain this chain:

```text
Contract / SOW commitment
        ↓
Customer objective
        ↓
Stakeholder requirement
        ↓
System requirement
        ↓
Deliverable
        ↓
Verification method
        ↓
Evidence
        ↓
Customer acceptance criterion
        ↓
Approval / sign-off
```

Required controls:

- every material SOW deliverable has an owner,
- every material deliverable has an acceptance method,
- ambiguous commercial language is resolved before engineering reliance,
- optional/stretch work is labeled separately from committed work,
- customer changes after baseline enter change control,
- technical evidence does not substitute for customer acceptance when formal acceptance is contractually required.

Recommended artifacts:

```text
customer/
├── sow_traceability.csv
├── deliverables_register.csv
├── acceptance_criteria.csv
└── acceptance_evidence_index.md
```

---

# 7. Commercial and Contract Governance

This skill governs operational execution of the engagement; it is not a substitute for legal review. Contract language, liability, indemnification, regulatory interpretation, tax, and other legal terms must be handled by authorized business/legal personnel.

Before build commitment, make the following operational terms explicit enough to engineer against:

- commercial model: fixed fee, time-and-materials, milestone, retainer, managed service, or other approved structure,
- delivery milestones,
- milestone acceptance conditions,
- customer review/acceptance windows where contractually defined,
- payment dependencies that affect release or transfer,
- approved travel/on-site assumptions where applicable,
- third-party/cloud/license costs and who pays them,
- usage-based service costs and budget ownership,
- procurement dependencies,
- subcontractor/provider dependencies,
- warranty/support period where applicable,
- transition from project delivery to recurring support,
- change-order triggers,
- termination/exit obligations that affect technical architecture or data handling.

## 7.1 Commercial control rule

Do not encode a commercial promise into the technical system unless it is traceable to the approved engagement baseline. Examples include unsupported uptime promises, unlimited scale, indefinite retention, zero-downtime deployment, response-time commitments, or customer-specific compliance claims.

## 7.2 Third-party cost and dependency rule

For every material third-party service, library, dataset, API, model provider, cloud resource, license, or platform dependency, identify:

- owner,
- license/terms dependency,
- expected cost model,
- renewal dependency,
- service availability dependency,
- data/privacy implications,
- substitution/exit option,
- production criticality.

No material recurring customer cost should be hidden inside an implementation choice.

---

# 8. Deployment and Ownership Model

Every engagement must explicitly choose and document the target operating model.

Typical models include:

1. DME-managed environment,
2. customer-owned Azure subscription/tenant,
3. customer-owned AWS account/organization,
4. customer-managed on-premises or hybrid environment,
5. regulated/isolated environment,
6. software/package handoff without ongoing DME operation,
7. shared-responsibility managed service.

For the selected model, document ownership of:

- cloud account/subscription,
- billing,
- resource groups/projects/accounts,
- domains/DNS,
- certificates,
- identities,
- secrets and keys,
- source code repositories,
- CI/CD identities,
- registries,
- storage,
- logs,
- monitoring,
- backups,
- disaster recovery,
- model registry,
- data pipelines,
- production data,
- support tooling,
- incident authority,
- release authority.

No production deployment proceeds while material ownership is ambiguous.

---

# 9. Customer Data, Privacy, Security and Retention Baseline

Before receiving or connecting to customer data, establish:

- data owner,
- data steward,
- permitted uses,
- prohibited uses,
- classification,
- sensitivity,
- residency requirements,
- transfer constraints,
- encryption expectations,
- access model,
- least-privilege roles,
- retention period,
- deletion requirements,
- backup retention,
- log-data treatment,
- non-production copy rules,
- synthetic/de-identified data rules,
- export requirements,
- incident notification path,
- post-engagement handling.

## 9.1 Mandatory data-handling rule

Production customer data must never be copied into personal, public, or unmanaged environments.

## 9.2 Data lifecycle states

Track at minimum:

```text
requested
→ authorized
→ received/connected
→ classified
→ processed
→ retained
→ exported if required
→ deleted / transferred / archived according to agreement
```

Evidence of deletion or transfer must be retained when contractually or operationally required.

---

# 10. Intellectual Property and Reuse Boundary

Every engagement must distinguish:

1. **DME background IP** — reusable frameworks, generic IaC patterns, generic utilities, templates, methods, standards, and pre-existing components.
2. **Customer data** — remains governed by the customer agreement.
3. **Customer-specific configuration** — mappings, thresholds, integrations, policies, workflows, and environment configuration specific to the engagement.
4. **Customer-specific trained artifacts** — models, embeddings, indexes, derived artifacts, or other outputs trained on customer data, according to the contract.
5. **Third-party IP** — software, datasets, libraries, APIs, licenses, and model/provider terms.

The technical repository should label reusable vs customer-specific components where practical.

Never assume that because code was written by DME it is automatically reusable across customers; follow the contractual IP boundary.

Never place proprietary customer code/data into a reusable DME reference repository without explicit authorization.

---

# 11. Customer-Specific Security / Compliance Overlay

Apply regulatory or contractual overlays only when applicable, but never ignore them when required.

Examples include:

- SOC 2 control expectations,
- ISO/IEC 27001 controls,
- NIST CSF / NIST SP 800-series requirements,
- CMMC / DFARS for defense contexts,
- FedRAMP requirements,
- HIPAA where applicable,
- PCI DSS where applicable,
- export-control requirements,
- customer vendor-security requirements,
- industrial/OT standards,
- safety standards.

For each applicable framework:

- identify required controls,
- map them to architecture/process evidence,
- identify customer vs DME control ownership,
- record gaps,
- record compensating controls,
- retain evidence,
- do not claim certification or compliance unless actually established.

---

# 12. Customer Decision Reviews During Delivery

Engineering must not disappear into a black box between kickoff and final delivery.

Use structured reviews at material gates, such as:

- Discovery Review,
- Requirements Baseline Review,
- Architecture Review,
- Data Readiness Review,
- Security Review,
- Reference Validation Review,
- Site Readiness Review,
- Shadow/Canary Review,
- ORR,
- Customer Acceptance Review,
- Production Release Review.

For each review record:

- date,
- attendees,
- artifacts reviewed,
- decisions,
- approvals,
- rejected options,
- action items,
- owners,
- due dates,
- unresolved risks,
- next gate.

Decision records must be versioned and linked to the affected requirements/ADRs/change requests.

---

# 13. Change Control

Classify material changes before implementation.

At minimum distinguish:

- defect correction,
- configuration change,
- enhancement,
- scope change,
- emergency change,
- security remediation,
- dependency/runtime upgrade,
- infrastructure change,
- model retraining,
- threshold change,
- data-source change,
- integration change,
- production incident remediation.

Every material change record should include:

- change ID,
- requestor,
- reason,
- classification,
- scope impact,
- architecture impact,
- security/privacy impact,
- cost impact,
- schedule impact,
- acceptance impact,
- required revalidation,
- rollback plan,
- approver,
- implementation status,
- evidence.

## 13.1 Scope-change rule

Do not absorb material new scope silently. Record it and resolve commercial, schedule, technical, and acceptance impacts before treating it as committed work.

---

# 14. Customer Acceptance Review (CAR)

The CAR is distinct from the technical ORR.

The ORR asks: **Is the system operationally ready?**

The CAR asks: **Has DME delivered the agreed customer outcome and evidence for the approved scope?**

Before customer acceptance, assemble an acceptance package containing, as applicable:

- approved scope baseline,
- requirements traceability,
- deliverables register,
- architecture package,
- deployment inventory,
- data/source mapping,
- test results,
- threshold results,
- model evidence,
- security results,
- reliability/recovery results,
- performance/capacity results,
- known limitations,
- residual risks,
- open exceptions,
- operator/admin documentation,
- runbooks,
- monitoring/alerting evidence,
- cost/usage assumptions,
- support model,
- production operating scope,
- training completion,
- handoff state,
- customer approvers.

CAR outcomes:

- **ACCEPTED**
- **ACCEPTED WITH CONDITIONS**
- **REJECTED / REMEDIATION REQUIRED**
- **DEFERRED**

Conditions must have owners, due dates, risk statements, and closure evidence.

---

# 15. Production Transition and Service Activation

Production activation requires both technical release authority and customer/service readiness.

Confirm before activation:

- approved production scope,
- production identities,
- production data sources,
- deployment target,
- release version,
- support owner,
- incident contacts,
- monitoring/alerts,
- backup/restore,
- RPO/RTO,
- capacity assumptions,
- licensing/subscription state,
- third-party dependencies,
- maintenance window,
- change window,
- rollback path,
- customer acceptance state,
- residual-risk acceptance.

Do not use a successful deployment as evidence that service transition is complete. Customer production activation requires the applicable CAR state or an explicitly documented contractual exception.

---

# 16. Support and Service Management

Before customer reliance, define the support model.

At minimum specify:

- support owner,
- support hours,
- communication channel,
- severity levels,
- severity definitions,
- response targets,
- escalation path,
- customer escalation contacts,
- maintenance windows,
- planned-change communication,
- emergency-change process,
- cloud-provider escalation path,
- security-incident path,
- model-incident path,
- data-quality incident path,
- service-health reporting cadence,
- support exclusions,
- service suspension/degradation authority and customer communication path for security, safety, integrity, contractual, or operational emergencies.

## 16.1 Recommended severity structure

Adapt contractually, but use a consistent model such as:

- **SEV-1** — critical production outage, safety/security risk, severe data-integrity impact, or major business interruption.
- **SEV-2** — major degradation with significant operational impact and no acceptable normal workaround.
- **SEV-3** — partial degradation, non-critical defect, or limited operational impact.
- **SEV-4** — low-impact issue, question, cosmetic defect, documentation request, or routine service request.

Do not promise response/resolution times that are not in the signed agreement.

---

# 17. Operational Reporting

For managed or supported services, define a recurring service report where appropriate.

Typical content:

- availability / SLO performance,
- incidents,
- unresolved problems,
- change activity,
- model/drift state,
- data-quality state,
- security findings,
- backup/restore status,
- capacity trends,
- cost trends,
- release history,
- open risks,
- upcoming maintenance,
- customer actions required,
- business/operational outcome trends where measurable.

Reports must distinguish measured production evidence from estimates or reference-environment results.

---

# 18. Customer Training and Enablement

Production handoff or shared operation requires role-appropriate enablement.

Potential audiences:

- operators,
- analysts,
- engineers,
- administrators,
- security teams,
- support teams,
- release managers,
- business owners.

Training should cover only relevant responsibilities, including:

- normal operation,
- interpretation of outputs,
- limitations,
- authority boundaries,
- alert response,
- degraded/abstain states,
- incident escalation,
- deployment/rollback where applicable,
- monitoring,
- access administration,
- change-request process,
- support contact path.

Record completion and any unresolved competency or access gap before handoff.

---

# 19. Handoff / Transfer Standard

For customer-operated or jointly operated systems, require a formal handoff.

Handoff package should include, as applicable:

```text
handoff/
├── architecture_overview.md
├── administrator_guide.md
├── operator_guide.md
├── deployment_runbook.md
├── rollback_runbook.md
├── backup_restore_runbook.md
├── incident_response.md
├── monitoring_guide.md
├── access_matrix.csv
├── release_manifest.json
├── known_issues.md
├── support_contacts.md
└── handoff_acceptance.md
```

Confirm transfer/ownership of:

- repositories,
- cloud resources,
- CI/CD,
- secrets/keys where appropriate,
- domains/certificates,
- monitoring,
- backups,
- artifact/model registries,
- documentation,
- licenses,
- support responsibilities.

Do not terminate DME access before confirming the customer can operate the system if DME is expected to transfer operations.

---

# 20. Renewal / Extension Decision

Before the end of an engagement or support period, determine whether the system will:

- continue under current support,
- expand to new sites/use cases,
- transition to customer ownership,
- transition to another provider,
- enter maintenance-only support,
- be decommissioned.

Any extension should reassess:

- scope,
- architecture,
- scale,
- risk,
- support load,
- cost,
- security/compliance requirements,
- technical debt,
- model/data validity,
- licensing,
- customer responsibilities.

Do not roll an expired or materially changed operating model forward without review.

---

# 21. Decommissioning and Exit Standard

Every production engagement must have an exit path.

Decommissioning should address, as applicable:

- final system/version inventory,
- customer data export,
- model/artifact export,
- configuration export,
- evidence archive,
- credential revocation,
- user/service identity removal,
- key/secret disposition,
- CI/CD shutdown or transfer,
- DNS/certificate disposition,
- cloud resource deletion/transfer,
- data deletion,
- backup expiration/deletion,
- log retention/deletion,
- third-party subscription termination,
- monitoring shutdown,
- repository access changes,
- DME access removal,
- customer confirmation,
- residual legal/retention obligations.

Required final states must be evidenced. Do not claim customer data was deleted unless deletion was actually performed or verified by the responsible owner.

---

# 22. Customer-Facing Repository / Workspace Standard

Customer-specific material must be clearly separated from generic DME reusable assets.

Recommended structure where appropriate:

```text
customer/
├── README.md
├── discovery_summary.md
├── stakeholder_register.csv
├── decision_authority_matrix.md
├── responsibility_matrix.csv
├── sow_traceability.csv
├── deliverables_register.csv
├── acceptance_criteria.csv
├── dependency_register.csv
├── risk_register.csv
├── decisions/
├── change_requests/
├── acceptance/
├── training/
└── handoff/
```

Do not place secrets, credentials, confidential customer exports, regulated data, or proprietary raw datasets directly into Git unless explicitly permitted and technically appropriate.

Customer-facing artifacts should identify:

- classification,
- owner,
- approver,
- version,
- effective date,
- status,
- related requirement/deliverable/change where applicable.

---

# 23. Evidence and Status Vocabulary

Use explicit status language.

Recommended states:

- proposed,
- discovery,
- approved for design,
- approved for build,
- implemented,
- locally verified,
- integration verified,
- reference validated,
- site adapted,
- site validated,
- shadow verified,
- canary verified,
- ORR passed,
- customer accepted,
- production active,
- conditionally accepted,
- blocked,
- suspended,
- handed off,
- decommissioned.

Avoid vague phrases such as "done," "ready," or "complete" without saying **what state is complete and against which criteria**.

---

# 24. Customer Delivery Quality Gate

Before calling a customer engagement complete, verify the applicable items below.

## 24.1 Commercial / scope

- scope baseline exists,
- deliverables are traceable,
- responsibilities are assigned,
- dependencies are resolved or explicitly transferred,
- material change requests are closed or accepted.

## 24.2 Technical delivery

- technical lifecycle gates passed for the claimed state,
- applicable standards-assurance gates passed or have authorized dispositions,
- standards applicability/tailoring and SEMP state are current for the claimed lifecycle state,
- release version is known,
- deployment inventory is known,
- acceptance evidence is complete,
- known limitations are documented,
- unresolved exceptions have owners and dispositions.

## 24.3 Customer acceptance

- acceptance criteria are evaluated,
- CAR outcome is recorded,
- customer approver is identified,
- conditions have owners and closure plans.

## 24.4 Service transition

- support model is active or intentionally not included,
- incident/escalation path is documented,
- monitoring ownership is known,
- backups/recovery ownership is known,
- production access ownership is known.

## 24.5 Data / security / IP

- customer-data handling matches agreement,
- retained copies are known,
- customer access and DME access are appropriate,
- reusable IP vs customer-specific IP is clear,
- third-party license obligations are known.

## 24.6 Handoff / closure

- documentation is delivered,
- training is complete when required,
- credentials/resources are transferred or retained according to the operating model,
- final risks/open items are acknowledged,
- renewal/handoff/decommission path is explicit.

Do not close the engagement merely because the software was deployed.

---

# 25. Interaction with the Other DME Skills

Use **Customer Delivery & Service Operations** to govern the engagement, **Systems Engineering Standards Assurance** to govern standards applicability and assurance, and **Build Production AI Systems** to govern the technical system lifecycle.

The relationship is an interleaved governance model, not three disconnected blocks:

```text
Customer Delivery & Service Operations
        ├── Intake / Discovery
        ├── Scope / Responsibility / Acceptance baseline
        ▼
Systems Engineering Standards Assurance
        ├── Standards Applicability Review
        ├── Tailoring
        ├── SEMP / assurance plan
        ▼
Build Production AI Systems
        ├── Architecture
        ├── Platform / Data / AI Engineering
        ├── Reference Verification
        ├── Customer/Site Adaptation
        ├── Site Validation / Shadow / Canary
        └── ORR
        ↕
Systems Engineering Standards Assurance
        ├── Requirements / architecture / V&V assurance
        ├── Information-item governance
        └── Standards checks at lifecycle gates
        ▼
Customer Delivery & Service Operations
        ├── Customer Acceptance Review (CAR)
        ▼
Build Production AI Systems
        └── Production Release
        ▼
Customer Delivery & Service Operations
        ├── Service Activation / Support
        ├── Change Control / Revalidation
        ├── Handoff / Renewal
        └── Decommissioning
        ↕
Systems Engineering Standards Assurance
        └── Change / revalidation / retirement standards assurance
```

By default, the standards applicability/tailoring baseline is established before technical requirements are frozen, and standards assurance remains active through architecture, V&V, ORR, production change, and retirement.

By default, CAR precedes customer production activation. If a signed agreement defines phased, provisional, or post-release acceptance, record that deviation explicitly, including scope, risk, approver, conditions, and rollback/termination rights.

The three skills must remain consistent on lifecycle state, requirement IDs, evidence, acceptance, release authority, risk, standards applicability, and change control. Do not duplicate artifacts when one governed artifact can satisfy multiple obligations; maintain traceable references instead.

When the skills conflict, do not silently choose one. Identify the conflict and resolve it through the appropriate engineering, standards, engagement, customer, contractual, safety, security, or legal decision authority.

---

# 26. Default DME Customer Standard

Unless an engagement is explicitly limited to advisory/discovery/prototype work, apply this skill as the default customer-delivery standard for DME.

The objective is not only to deliver a technically sound system.

The objective is to deliver a system with clear scope, ownership, acceptance, evidence, production responsibilities, support boundaries, data/IP handling, change control, and a complete exit path—so the customer can safely adopt, operate, support, transfer, renew, or retire what DME builds.

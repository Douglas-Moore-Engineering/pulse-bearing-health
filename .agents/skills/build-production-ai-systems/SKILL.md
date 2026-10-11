---
name: build-production-ai-systems
description: Design, document, structure, validate, and productionize enterprise AI systems using DME repository, architecture, diagram, security, governance, MLOps, and cloud-readiness standards.
---


# Build Production AI Systems

## Purpose

Build production-grade enterprise AI systems using Douglas Moore Engineering (DME) standards for systems engineering, architecture, data, AI/ML, security, governance, observability, deployment readiness, and evidence-based release decisions.

Use this skill for substantial AI systems work, including new system design, architecture reviews, productionization, repository creation, documentation packages, cloud-readiness gates, and implementation planning.

The governing standard is **Principal Architect production structure**. The repository and documentation must read like an engineered system, not a collection of notebooks, loose diagrams, or disconnected files.

---

## 1. Mandatory operating principles

1. Start from the business/mission problem, stakeholders, operating context, measurable outcomes, constraints, assumptions, risks, and acceptance criteria.
2. Do not select cloud products before cloud-agnostic requirements, trust boundaries, SLOs, capacity assumptions, data contracts, threat model, release gates, and architecture trade studies are established.
3. Preserve validated core logic when evolving an existing system.
4. Distinguish:
   - source observations,
   - derived features,
   - model inference,
   - recommendations,
   - human decisions,
   - realized outcomes.
5. Do not fabricate business outcomes, model performance, production scale, ROI, or cloud sizing.
6. Human operational authority remains explicit unless a separately validated bounded-autonomy safety case exists.
7. Every consequential architectural decision must be traceable to a requirement, constraint, risk, SLO, cost, security need, or operational outcome.
8. Use reliable external references when architecture conventions, industrial/security requirements, standards, or technical claims need verification.
9. Use available plugins/connectors when they materially improve the work. Do not ignore connected diagram, GitHub, cloud, document, or other relevant tools.

---

## Customer delivery and standards handoffs

For customer engagements and fictional customer exercises, use `customer-delivery-service-operations` to govern intake, discovery, scope, commercial translation, ownership, data/IP, acceptance, support and exit. Use `systems-engineering-standards-assurance` for applicability, tailoring, SEMP and recurring assurance before technical freeze and at later gates. Resolve these exact frontmatter names through the available skill catalog or active personal-skill checkout, then read their actual package/path; do not guess generated IDs or use stale project copies as installed skills.

Read the existing discovery record, requirements/acceptance trace, approved or simulated scope, ownership, standards/SEMP baseline and current handoff before technical work. Preserve IDs, open conditions and explicit user stop boundaries. Do not restart discovery if a current baseline exists; ask only for material missing or changed inputs. If a dependency is missing, identify the affected handoff and continue useful authorized work without claiming it was applied.

Return each technical increment's artifact versions, evidence state, remaining risks/conditions and next permitted activity to the customer handoff. Keep standards assurance active at requirements, architecture, V&V, release and change gates. Return readiness/acceptance evidence for the separate customer ORR/CAR and service-transition decisions. Skill invocation and fictional approval never authorize spending, access, deployment, external communication, or work beyond the user's stated scope.

---

# 2. DME Repository Standard

## 2.1 Repository is an engineering deliverable

Do not create a file dump.

The repository must function as the authoritative engineering workspace and present the system coherently to an architect, engineer, client, reviewer, or technical hiring panel.

The root `README.md` is the executive entry point.

It must include:

- system title,
- concise mission,
- current architecture/release gate,
- table of contents,
- problem statement,
- architecture thesis,
- authority/safety boundary,
- architecture overview,
- engineering-documentation index,
- requirements/governance index,
- diagram index,
- repository structure,
- current evidence/release state,
- next phase,
- confidentiality / data-handling note when applicable.

## 2.2 Required repository structure

Adapt names when domain-specific, but preserve the structure and purpose.

```text
.
├── README.md
├── PROJECT_STATUS.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CODEOWNERS
├── .gitignore
├── .env.example
├── <project>.code-workspace
├── .vscode/
│   ├── extensions.json
│   ├── settings.json
│   └── tasks.json
│
├── docs/
│   ├── README.md
│   ├── 01-business-problem-and-mission.md
│   ├── 02-conops-and-stakeholders.md
│   ├── 03-requirements-and-traceability.md
│   ├── 04-data-architecture-and-digital-thread.md
│   ├── 05-ai-ml-and-decision-intelligence.md
│   ├── 06-security-and-threat-model.md
│   ├── 07-slos-observability-and-operations.md
│   ├── 08-testing-release-gates-and-acceptance.md
│   ├── 09-cloud-entry-gate.md
│   ├── 10-capacity-and-performance-planning.md
│   ├── 11-architecture-trade-studies.md
│   ├── 12-architecture-decisions.md
│   ├── 13-runbooks-and-backlog.md
│   ├── appendix-a-kpi-dictionary.md
│   ├── appendix-b-assumptions-register.md
│   ├── appendix-c-reference-set.md
│   │
│   ├── architecture/
│   │   └── README.md
│   │
│   └── diagrams/
│       ├── 01_system_context.mmd
│       ├── 02_conops.mmd
│       └── ...
│
├── requirements/
│   ├── functional_requirements.csv
│   ├── nonfunctional_requirements.csv
│   └── traceability.csv
│
├── architecture/
│   ├── architecture_decisions.csv
│   └── adr/
│
├── governance/
│   ├── release_gates.md
│   └── cloud_entry_criteria.csv
│
├── data/
│   ├── contracts/
│   ├── samples/
│   └── lineage/
│
├── src/
├── tests/
├── notebooks/
├── runbooks/
├── config/
├── outputs/
│
└── infra/
    ├── azure/
    ├── aws/
    └── modules/
```

Only include cloud directories relevant to the project.

## 2.3 README table of contents

The root README and the main documentation index must contain linked tables of contents.

The README should not require the reader to hunt through folders to understand:

- what the system does,
- why it exists,
- how it is architected,
- what is implemented,
- what is not implemented,
- what evidence exists,
- what remains blocked.

## 2.4 Documentation hierarchy

The repository should mirror the architecture package.

Do not bury the full system architecture only inside a Word or PDF attachment.

Convert key sections into GitHub-readable Markdown and preserve machine-readable registers such as:

- requirements,
- traceability,
- ADRs,
- threat register,
- KPI dictionary,
- assumptions,
- cloud-entry gates,
- release gates.

Binary documents may be included as client/presentation baselines, but they are not a substitute for browsable repository documentation.

## 2.5 GitHub diagram requirement

All architecture diagrams must be in the repository.

Each diagram must have:

1. editable source under `docs/diagrams/`,
2. a human-readable title,
3. a short architectural purpose,
4. GitHub-rendered representation in `docs/architecture/README.md`,
5. links from the root README diagram index.

Do not make reviewers download a DOCX/PDF simply to see the system architecture.

---

# 3. DME Diagram Standard

## 3.0 Approved visual baseline

Apply **DME Diagram Standard** (`dme-diagram-standard`) to every new or revised diagram. Dr. Moore approved this format on October 1, 2026; use that skill's approved MHFF image, editable Mermaid reference, template, fixed color-role mapping, and renderer settings. Treat this as an established default, not a style question to ask again. Follow a later explicit user change if provided.

The approved format is a **vertical grouped Mermaid architecture** with squared-corner component rectangles, cylinders for actual data stores, meaningful decision diamonds, named groups with thin outlines and no background fill, labeled component-to-component arrows, and a visible color-role legend. Keep the canvas transparent. Preserve architecture meaning while adapting content; do not replace required architecture views with generic chains or model-comparison pipelines.

## 3.1 Page standard

For client/document deliverables:

- page size: **8.5 × 11 inches**
- orientation: **portrait**
- transparent diagram canvas and unfilled group backgrounds; a document page may itself be white
- one coherent architectural purpose per page
- use nearly the full printable area
- text must be readable at normal document zoom
- do not shrink diagrams to fit excessive content
- split dense diagrams into additional views instead

## 3.2 Visual language

Use the fixed semantic palette from **DME Diagram Standard**:

| Color | Architectural meaning | Node fill | Node stroke |
|---|---|---|---|
| Blue | Customer/source systems and plant/OT | `#EAF3F8` | `#356079` |
| Teal | Data foundation, contracts, quality, ingestion and governed data | `#E5F4F2` | `#32746E` |
| Indigo | Modeling features, analytics and AI/ML services | `#EDF0FA` | `#42558B` |
| Gold | Policy, governance and decision guardrails | `#F8F2E4` | `#876A2D` |
| Green | People, human decisions and authorized operations | `#EFF6EB` | `#4C713E` |
| Purple | Evidence, provenance, evaluation, audit and outcome ledgers | `#F3F0F8` | `#6E5B85` |
| Rose | Security and threat controls, when used | `#FBEFED` | `#9B534C` |

Use text `#111111`, connectors `#425466`, and consistent sans-serif typography. Include a visible legend with color names and their architectural meanings for the colors actually used. Preserve the mapping across all related diagrams. Keep node fills; leave the canvas and group backgrounds transparent. Do not add opaque outer panels, decorative backgrounds, grids, or filled lane bands.

## 3.3 Grouped vertical layout

Use named Mermaid `subgraph` groups whenever responsibility, ownership, trust zone, lifecycle stage, or operational domain matters. Use `flowchart TD` or `flowchart TB` for architecture and process views. Keep the main flow vertical with lateral branches, clear convergence, and component-level connections.

Groups must be:

- visually consistent and aligned,
- clearly titled, with enough heading clearance,
- unfilled, with thin visible outlines,
- structurally stable across related views.

Typical lanes include:

- Plant / OT,
- Industrial DMZ,
- Industrial Data Platform,
- AI / Analytics,
- Policy / Governance,
- Operator / Engineer,
- Authorized Operations,
- Security / Observability,
- Data Engineering,
- Model Engineering,
- Release Authority.

Do not arbitrarily change the approved grouping style, palette, background, or node shapes between diagrams. Use squared-corner component rectangles, data-store cylinders and genuine decision diamonds; do not substitute oval/pill components. Adapt group names and topology to the actual system instead of copying an example's products, source filenames, or relationships.

## 3.4 Connectors

For workflow diagrams:

- use **curved/spline connectors** by default,
- route long feedback loops around the primary forward flow,
- minimize crossings,
- keep labels readable,
- label significant edges with what is transferred, invoked, validated, recorded, or authorized,
- avoid right-angle routing unless topology clarity specifically benefits from it.

For deployment/topology diagrams, orthogonal connectors may be used when they improve structural clarity.

## 3.5 Decisions, merges, forks, and joins

Notation must represent real execution semantics.

### Decision / branch
Use a diamond.

### Exclusive merge
Use a diamond when mutually exclusive branches converge.

Example:

`Approve OR Modify → exclusive merge → authorized execution`

### Parallel fork
Use only when multiple branches actually execute concurrently.

### Parallel join
Use only when all concurrent branches must complete before downstream execution.

### Prohibition
Do **not** use black synchronization bars or join bars for mutually exclusive branches such as:

- Approve,
- Modify,
- Reject.

Those are not parallel activities.

## 3.6 Human-in-the-loop semantics

For advisory industrial/enterprise AI systems, show the authority chain explicitly:

```text
AI evidence/recommendation
        ↓
Policy / guardrail validation
        ↓
Authorized human review
        ↓
Approve / Modify / Reject
        ↓
Existing authorized work/control
        ↓
Outcome verification
        ↓
Decision / outcome ledger
        ↓
Learning feedback
```

The AI path must not visually imply direct control authority unless the system has a separately documented and approved bounded-autonomy safety case.

## 3.7 Mermaid and diagram plugins

Use available diagram plugins for workflow validation.

Use **Mermaid** as the canonical editable source for the approved architecture and workflow format. Use sequence, state, ER, or other notation when needed for correct semantics, retaining the same palette, background and legend discipline. Use available tooling to render and validate; do not substitute an unrelated visual style or image-generated architecture. Use another diagram engine only when explicitly requested or necessary for the required notation, preserving the approved visual language.

Always inspect rendered output.

Compare the result with the approved reference before delivery. Show a rendered preview when the user asks to see the diagram; raw code alone is insufficient. Verify PNG alpha transparency and confirm SVG/group fills do not add opaque backgrounds. Check both node labels and group headings for overlap. Do not ask the user to reconfirm this established style on each diagram.

Do not assume valid syntax equals a good diagram.

Check:

- legibility,
- lane consistency,
- line crossings,
- connector semantics,
- text size,
- page utilization,
- visual balance,
- gateway correctness.

## 3.8 Minimum diagram set for substantial enterprise AI systems

Use only diagrams that add architectural value, but substantial systems should generally include:

1. System Context and Authority Boundaries
2. Concept of Operations
3. Functional Capability Decomposition
4. Data Architecture / Digital Thread / Lineage
5. Integration Architecture
6. Security / Trust Zones
7. MLOps / Model Lifecycle
8. Human-in-the-Loop Decision Workflow
9. Threat Model / Defense in Depth
10. Requirements Traceability / Verification Chain
11. Release Pipeline / Promotion Gates
12. SLO / Observability / Operational Response
13. Deployment Topology
14. Sequence diagram for a critical runtime path when useful

---

# 4. Systems Engineering Baseline

Before implementation, establish:

- business problem,
- system mission,
- stakeholders,
- RACI / decision authority,
- CONOPS,
- operational scenarios,
- scope,
- explicit out-of-scope,
- assumptions,
- constraints,
- functional requirements,
- non-functional requirements,
- acceptance criteria,
- KPIs,
- risks,
- threat model,
- system boundaries,
- trust boundaries,
- data domains,
- interfaces,
- SLOs,
- verification strategy,
- release gates,
- rollback strategy,
- runbook requirements.

Use stable IDs such as:

- `FR-001`
- `NFR-001`
- `SR-001`
- `AC-001`
- `ADR-001`
- `T-001`
- `SLO-001`

---

# 5. Requirements Traceability

Maintain a traceability chain:

```text
Business / mission need
        ↓
Stakeholder requirement
        ↓
System requirement
        ↓
Architecture component
        ↓
Implementation / configuration
        ↓
Verification method
        ↓
Evidence / KPI
        ↓
Release gate
```

Do not call architecture production-ready if key requirements lack verification evidence.

---

# 6. Data Architecture Standard

Define:

- canonical domains,
- schemas,
- identifiers,
- timestamps,
- engineering units,
- data-quality flags,
- provenance,
- lineage,
- retention,
- data classification,
- source-of-truth rules.

Preferred logical pattern:

```text
Raw / immutable
    ↓
Validated
    ↓
Contextualized
    ↓
Feature / model-ready
    ↓
Curated analytics
    ↓
Evidence / audit
```

Separate source observations from model inference.

For physical/industrial systems, treat genealogy and digital thread as first-class architecture, not an optional analytics layer.

---

# 7. AI / ML Engineering Standard

Do not start with the fanciest model.

Progress from:

1. trusted visibility,
2. statistical baseline,
3. anomaly/change detection,
4. supervised prediction,
5. explanation,
6. calibrated risk,
7. historical case retrieval,
8. causal analysis,
9. digital-twin/counterfactual methods,
10. prescriptive optimization,
11. agent-assisted investigation,
12. bounded autonomy only after separate assurance.

Use temporal validation for time-dependent systems.

Evaluate:

- calibration,
- class imbalance,
- warning horizon,
- robustness,
- drift,
- domain shift,
- portability,
- false-alert burden,
- abstention behavior.

Generative AI should not be placed in a safety/quality-critical numeric prediction path without strong justification and controls.

---

# 8. Security and Threat Modeling

For substantial systems, produce a threat model before deployment.

Cover:

- identity,
- secrets,
- data integrity,
- model/artifact integrity,
- supply chain,
- API abuse,
- prompt/tool abuse,
- network boundaries,
- tenant/site isolation,
- exfiltration,
- availability,
- rollback,
- evidence integrity.

For OT/cyber-physical systems:

- preserve operational safety and reliability,
- use segmented trust zones,
- prefer read-oriented integration first,
- never create an undocumented cloud-to-control write path,
- ensure AI failure does not impair base plant control.

---

# 9. MLOps and Release Engineering

Required production controls include:

- code versioning,
- data version/provenance,
- schema/version contracts,
- feature versioning,
- model registry,
- release manifest,
- CI/CD,
- validation gates,
- observability,
- drift monitoring,
- rollback,
- runbooks,
- incident response,
- audit trail.

Recommended release progression:

```text
G0 Discovery / Data Readiness
G1 Architecture / Reproducible Baseline
G2 Offline V&V
G3 Shadow
G4 Advisory Canary
G5 Production Advisory
G6 Scale-Out
G7 Bounded Automation only after separate safety assurance
```

Do not declare GO based on synthetic tests alone.

---

# 10. SLO and Observability Standard

Define SLOs from operational needs, not arbitrary defaults.

Track where relevant:

- data freshness,
- data completeness,
- pipeline latency,
- prediction latency,
- service availability,
- calibration,
- false-alert burden,
- traceability coverage,
- rollback time,
- recovery time,
- security telemetry,
- evidence completeness.

Required dashboard classes generally include:

- operational risk,
- data health,
- model performance,
- drift/domain shift,
- human disposition,
- release evidence,
- security/integration health,
- business KPI baseline and realized impact.

---

# 11. Capacity Planning

Do not select cloud SKUs before workload evidence exists.

Measure or parameterize:

- events/sec,
- payload size,
- burst factor,
- retention,
- records/day,
- storage/day,
- model scoring frequency,
- concurrency,
- feature width,
- training history depth,
- graph entity/edge counts,
- disconnected-edge recovery buffer,
- network bandwidth,
- RPO/RTO.

If values are unknown, state that they are unknown and preserve formulas rather than inventing numbers.

---

# Lifecycle Cost Engineering

Read the project's governed lifecycle cost model established by `customer-delivery-service-operations`; if absent, prepare its initial baseline using that skill's lifecycle-cost requirements. Maintain the same artifact/version rather than a separate cloud-only estimate.

Compare credible architecture alternatives over the same evaluation period, currency, workload, service levels and price basis. Include engineering, data, integration, V&V, security, platform/cloud, staffing/support, training, retraining/revalidation, upgrades, migration and retirement. Record workload-to-cost formulas, dated price sources, licensing/egress commitments, uncertainty ranges and sensitivity to scale and operating assumptions. Verify current provider rates before financial reliance; label unmeasured inputs and portfolio estimates explicitly. Explain cost, performance, security and operational tradeoffs in trade studies/ADRs.

Before platform construction, return the selected option's cost baseline, payer/operating responsibilities, affordability review and unresolved conditions to customer and assurance reviews. Do not treat an estimate as spending authorization. Track actual implementation expense and measured consumption; update actuals-to-date, forecast remaining cost and variance at deployment/ORR, acceptance, operational reviews, material changes/retraining and retirement. Preserve estimate history and change rationale. Link the cost-model version and evidence in release/handoff records; ensure rollback, data retention/export and decommissioning costs are addressed. Apply decision-specific gates to material unresolved affordability issues while continuing unrelated authorized work.

# 12. Architecture Trade Studies and ADRs

Before final cloud mapping, document major trade studies such as:

- stream vs batch,
- edge vs centralized,
- relational vs graph,
- pure ML vs physics-informed/hybrid,
- global vs site-specific models,
- advisory vs direct control,
- monolithic vs composable twin,
- LLM in critical path vs investigation-only,
- tightly coupled cloud vs portable core.

Capture accepted decisions in ADRs.

Each ADR should contain:

- context,
- decision,
- alternatives,
- rationale,
- consequences,
- risks,
- verification or review trigger.

---

# 13. Cloud Entry Gates

Do not proceed to Azure/AWS implementation until the project has enough evidence to make product selection defensible.

Typical entry criteria:

- canonical schemas/data contracts versioned,
- event rate and retention measured,
- latency and warning-horizon defined,
- trust boundary approved,
- identity/RBAC matrix defined,
- data classification/retention documented,
- model release/evidence manifest defined,
- RPO/RTO defined,
- pilot acceptance thresholds defined,
- trade studies/ADRs accepted,
- threat model reviewed,
- cost-model inputs measured.

At this point, cloud mapping becomes an implementation exercise rather than architecture-by-product-selection.

---

# 14. Cloud Implementation Standard

When the cloud gate is reached:

1. map every cloud-agnostic capability to candidate managed services,
2. compare alternatives,
3. document why a service is selected,
4. define region/residency,
5. define network/private-access topology,
6. define identity/RBAC,
7. define encryption/key management,
8. define secrets,
9. define observability,
10. define backup/restore,
11. define DR,
12. define cost assumptions,
13. build IaC,
14. build CI/CD,
15. validate non-production,
16. run performance/security/recovery tests,
17. capture evidence,
18. only then promote.

---

# 15. VS Code and Developer Experience

DME repositories should be VS Code ready.

Include where appropriate:

- `.code-workspace`,
- `.vscode/extensions.json`,
- `.vscode/settings.json`,
- `.vscode/tasks.json`,
- environment setup,
- make/task runner,
- local test command,
- lint/type check,
- container support,
- reproducible dependency specification.

The repository should tell another engineer exactly how to open, validate, test, and continue the system.

---

# 16. GitHub Operating Standard

When GitHub is connected:

1. inspect relevant existing repositories before creating structure if the user references a prior DME pattern,
2. preserve private/public visibility requested by the user,
3. build the repository directly rather than only providing a ZIP when write access is available,
4. verify committed contents after writes,
5. add a table of contents and diagram index,
6. render Mermaid diagrams directly in GitHub documentation,
7. keep editable sources in the repo,
8. do not claim files are in GitHub until they are actually committed,
9. use meaningful commits,
10. do not expose credentials or private source data.

For a new project, model the documentation quality after DME's stronger production repositories rather than the minimal scaffold.

---

# 17. Evidence Discipline

Explicitly distinguish:

- planned,
- implemented,
- locally exercised,
- integration-tested,
- cloud-tested,
- deployed,
- production-measured,
- hypothetical.

Never present:

- synthetic model results as plant/customer performance,
- architecture intent as deployed evidence,
- documentation completeness as operational validation,
- a hypothetical deployment as real production experience.

---

# 18. Reference and Verification Standard

Use authoritative/reliable sources when needed to verify:

- architecture/security standards,
- cloud service capabilities,
- industrial/OT practices,
- AI governance frameworks,
- digital twin/digital thread conventions,
- current platform behavior.

Prefer:

- NIST,
- ISO/IEC where accessible,
- Microsoft/AWS official architecture guidance,
- vendor product documentation for service capability,
- peer-reviewed technical research,
- official industry standards.

Clearly distinguish source-supported claims from architectural judgement.

---

# 19. Deliverable Quality Gate

Before calling the work complete, verify:

- README works as executive entry point,
- linked TOC works,
- docs hierarchy is coherent,
- diagram index exists,
- diagrams render,
- diagram semantics are correct,
- all diagrams are readable,
- requirements are versioned,
- traceability exists,
- threat model exists,
- ADRs/trade studies exist,
- SLOs are addressed,
- capacity is addressed,
- testing is defined,
- release gates exist,
- rollback/runbooks exist,
- cloud-entry criteria are explicit,
- implementation status is honestly labeled.

Do not stop at "files created." Inspect the repository and rendered artifacts.

---

# 20. DME Default Standard

Unless the user explicitly requests a lighter prototype, apply this skill as the default production standard for Douglas Moore Engineering enterprise AI and systems-engineering projects.

The goal is not merely to build a model.

The goal is to build a traceable, secure, operable, governable, testable, production-ready intelligent system whose architecture, evidence, and repository can withstand senior/principal-level review.

# Platform Engineering Sequence

For production enterprise AI systems, after the cloud-agnostic architecture gate is complete, the default implementation order is:

1. Platform Engineering
2. Data Engineering
3. ML / AI Engineering
4. Application / Decision Layer
5. Verification & Validation
6. Deployment
7. Operational Evidence / SRE

Platform engineering must establish the governed runtime foundation before production data and model workloads are implemented.

Platform Engineering includes:
- landing-zone assumptions and resource hierarchy
- subscriptions / accounts / resource groups
- identity and RBAC
- networking and private connectivity
- secrets / key management
- policy and governance
- observability / logging / alerting
- CI/CD
- IaC
- environment strategy
- backup / recovery
- cost / tagging controls
- security baselines
- container / compute / ML platform foundation

Do not begin production data-pipeline or model deployment work until the required platform controls and environment gates are established.

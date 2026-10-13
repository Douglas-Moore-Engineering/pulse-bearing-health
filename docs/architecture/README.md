# Architecture Views

PULSE pre-Azure review v0.3 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

## Diagram index

Seventeen unique views; the four v0.4 additions describe the reference implementation and its remaining boundaries. The critical runtime view uses an ordered flowchart to expose rejection paths rather than implying concurrent execution. Historical views retain their stated design maturity.

Thirteen original views; `.mmd`, `.svg` and `.png` are source, scalable preview and image export of the same diagram. Views 04/04b, 07/07b and 08/08b form the v0.2 correction. View 03 now uses explicit Bronze/Silver/Gold design v0.3. Other views retain v0.1.

| View | Purpose |
|---|---|
| [System Context and Authority](../diagrams/01_system_context.svg) | Distinguish reference evidence, future site sources and human authority. |
| [As-Is Workflow and Proposed Handoff](../diagrams/02_as_is_conops.svg) | Show the fictional current process and where advisory evidence would enter. |
| [Data Architecture — Bronze, Silver and Gold](../diagrams/03_data_lineage.svg) | Preserve authorized source bytes, promote validated bearing/run records and publish versioned features and advisory products with lineage. |
| [AI/ML Training and Registration](../diagrams/04_model_lifecycle.svg) | Trace qualified signals through leakage-safe preparation, candidate evaluation and versioned registration; registration does not authorize release. |
| [Inference, Monitoring and Revalidation](../diagrams/04b_inference_monitoring.svg) | Bind scoring to the released preprocessing/model/policy versions, preserve abstention and human authority, and route change signals to reviewed revalidation. |
| [Advisory Policy and Human Decisions](../diagrams/05_human_decision.svg) | Model output cannot bypass eligibility or customer approval. |
| [Security and Trust Zones](../diagrams/06_security_boundaries.svg) | Separate future plant collection, processing and restricted evidence access. |
| [Proposed Azure Environment Topology](../diagrams/07_deployment_candidate.svg) | Separate reference development, release validation and later site deployment; show storage, compute, model assets and operational evidence without binding resources. |
| [Proposed Network and Identity Paths](../diagrams/07b_network_identity.svg) | Distinguish private inbound client access from managed compute egress and identity authorization; resource placement is logical, not an implemented network. |
| [Release and Promotion](../diagrams/08_release_gates.svg) | Bind each promotion to verified artifacts, an exact destination, current evidence and release authority; failures deny new exposure. |
| [Rollback and Safe Recovery](../diagrams/08b_rollback_recovery.svg) | Withdraw affected advisories, assess the prior release and recover the full approved bundle or remain unavailable. |
| [Observability, Degraded Mode and Recovery](../diagrams/09_operations_recovery.svg) | Connect runtime signals to accountable human response and revalidation. |
| [Requirements, Risks and Evidence Trace](../diagrams/10_traceability.svg) | Join stakeholder needs and controls to evidence-bound review decisions. |

Components and controls in the original thirteen views are proposed; the v0.4 views state their local implementation scope individually. Solid edges describe intended interactions, not existing connections; dashed edges mark later site scope. Resource groups are administrative boundaries, not network isolation. Identity authorization does not create a route. Related versions and authority must agree across views.

## System Context and Authority

Distinguish reference evidence, future site sources and human authority. Status: proposed/unimplemented; view v0.1. Requirements: PULSE-SR-001;PULSE-FR-007;AIG-REQ-003.

[Editable source](../diagrams/01_system_context.mmd) · [SVG preview](../diagrams/01_system_context.svg) · [PNG export](../diagrams/01_system_context.png)

```mermaid
%% System Context and Authority | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_source["Sources and context"]
 pub["Public bearing experiments"]
 site["Future read-only plant exports"]
end
subgraph sg_system["Pulse advisory boundary"]
 qualify["Source and regime qualification"]
 evidence["Bearing-health evidence"]
end
subgraph sg_human["Customer authority"]
 reviewer["Reliability review"]
 planner["Maintenance approval"]
end
pub -->|"rights-qualified reference files"| qualify
site -.->|"later authorized site records"| qualify
qualify -->|"bounded inference or abstention"| evidence
evidence -->|"supports investigation"| reviewer
reviewer -->|"proposes work"| planner
class pub,site source
class qualify data
class evidence evidence
class reviewer,planner human
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_source fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_system fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_human fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Teal—data; Green—people; Purple—evidence.

## As-Is Workflow and Proposed Handoff

Show the fictional current process and where advisory evidence would enter. Status: proposed/unimplemented; view v0.1. Requirements: PULSE-FR-007;PULSE-FR-008.

[Editable source](../diagrams/02_as_is_conops.mmd) · [SVG preview](../diagrams/02_as_is_conops.svg) · [PNG export](../diagrams/02_as_is_conops.png)

```mermaid
%% As-Is Workflow and Proposed Handoff | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_source["Assumed current sources"]
 rounds["Monthly vibration rounds"]
 hist["Historian and work orders"]
end
subgraph sg_current["Current manual decisions"]
 assess["Reliability assesses condition"]
 plan["Planner schedules work"]
end
subgraph sg_future["Proposed reference increment"]
 pulse["Pulse qualified evidence"]
 mock["Mock CMMS work request"]
end
rounds -->|"inspection findings"| assess
hist -->|"operating and failure context"| assess
assess -->|"maintenance recommendation"| plan
pulse -.->|"future advisory input"| assess
plan -.->|"reference approval only"| mock
class rounds,hist source
class assess,plan human
class pulse evidence
class mock policy
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_source fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_current fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_future fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Gold—policy; Green—people; Purple—evidence.

## Data Architecture — Bronze, Silver and Gold

Preserve authorized source bytes, promote validated bearing/run records and publish versioned features and advisory products with lineage. Status: proposed/unimplemented; view v0.3. Requirements: PULSE-FR-001;PULSE-FR-002;PULSE-NFR-008;PULSE-NFR-006;PULSE-NFR-007;AIG-REQ-001.

[Layer contracts and promotion rules](../04-data-architecture-and-digital-thread.md) · [ADR-009](../../architecture/adr/adr-009.md)

[Editable source](../diagrams/03_data_lineage.mmd) · [SVG preview](../diagrams/03_data_lineage.svg) · [PNG export](../diagrams/03_data_lineage.png)

```mermaid
%% Data Architecture — Bronze, Silver and Gold | Proposed; unimplemented | Pulse v0.3
flowchart TD
files["Rights-qualified vibration files"]
subgraph sg_bronze["Bronze — original source"]
  raw[("Original bytes; immutable versions")]
  manifest[("Source, rights and checksum manifest")]
end
subgraph sg_silver["Silver — validated context"]
  validate["Validate integrity, units and source profile"]
  accepted[("Canonical bearing/run observations")]
  quarantine[("Rejected records and reason references")]
end
subgraph sg_gold["Gold — versioned data products"]
  build["Group split; governed feature builds"]
  features[("Feature products; partition manifests")]
  score["Released scoring and eligibility; view 04b"]
  outputs[("Advisories and health summaries")]
end
files -->|"authorized landing; preserve format"| raw
raw -->|"record provenance and digest"| manifest
raw -->|"read source bytes"| validate
manifest -->|"verify rights, identity and integrity"| validate
validate -->|"pass; retain source linkage"| accepted
validate -->|"fail; exclude from scoring"| quarantine
accepted -->|"split before windows; train-only fitting"| build
build -->|"versioned build and split manifests"| features
features -->|"approved release inputs"| score
score -->|"advisory or explicit unavailable result"| outputs
class files source
class raw,validate,accepted,quarantine data
class build,features,score model
class manifest,outputs evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_bronze fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_silver fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_gold fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Teal—data; Indigo—models; Purple—evidence. Bronze/Silver/Gold are maturity layers, not node colors; the approved DME palette retains its semantic roles.

## AI/ML Training and Registration

Trace qualified signals through leakage-safe preparation, candidate evaluation and versioned registration; registration does not authorize release. Status: proposed/unimplemented; view v0.2. Requirements: PULSE-FR-001;PULSE-FR-003;PULSE-FR-005;PULSE-FR-006;PULSE-NFR-008;AIG-REQ-001.

[Editable source](../diagrams/04_model_lifecycle.mmd) · [SVG preview](../diagrams/04_model_lifecycle.svg) · [PNG export](../diagrams/04_model_lifecycle.png)

```mermaid
%% AI/ML Training and Registration | Proposed design; unimplemented | Pulse architecture v0.2
flowchart TD
subgraph sg_data["Qualified data and reproducible preparation"]
  data[("Accepted signals and label provenance")]
  split["Freeze bearing/run partitions"]
  prep["Train-fit signal and feature pipeline"]
end
subgraph sg_models["Experiments and capability eligibility"]
  baseline["RMS / kurtosis baseline"]
  candidates["Anomaly; eligible diagnosis / RUL"]
  validation["Validation selection and freeze"]
  test["Sealed test; limits and uncertainty"]
end
subgraph sg_register["Governed candidate assets"]
  runs[("Run, code, data and environment evidence")]
  gate{"Evidence and integrity acceptable?"}
  rejected["Retain failed candidate evidence"]
  registry[("Model name, version and digest")]
  manifest["Assemble release manifest; view 08"]
end
data -->|"source groups before windows"| split
split -->|"assigned train / validation / test"| prep
prep -->|"same partitions and time basis"| baseline
prep -->|"train only; qualified labels"| candidates
baseline -->|"reference metrics"| validation
candidates -->|"eligible capability metrics"| validation
validation -->|"frozen model, thresholds and policy"| test
test -->|"results; never retune on test"| runs
runs -->|"version-bound review package"| gate
gate -->|"no"| rejected
gate -->|"yes; candidate only"| registry
registry -->|"immutable artifact reference"| manifest
class data,split data
class prep,baseline,candidates model
class validation,gate,manifest policy
class test,runs,rejected,registry evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_data fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_models fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_register fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Teal—data; Indigo—models; Gold—policy; Purple—evidence.

## Inference, Monitoring and Revalidation

Bind scoring to the released preprocessing/model/policy versions, preserve abstention and human authority, and route change signals to reviewed revalidation. Status: proposed/unimplemented; view v0.2. Requirements: PULSE-FR-002;PULSE-FR-004;PULSE-FR-007;PULSE-SR-004;AIG-REQ-001;AIG-REQ-002.

[Editable source](../diagrams/04b_inference_monitoring.mmd) · [SVG preview](../diagrams/04b_inference_monitoring.svg) · [PNG export](../diagrams/04b_inference_monitoring.png)

```mermaid
%% Inference, Monitoring and Revalidation | Proposed design; unimplemented | Pulse architecture v0.2
flowchart TD
subgraph sg_run["Released advisory runtime — future"]
  input["Contract-accepted observations"]
  bundle["Verify release and artifact digests"]
  features["Apply frozen preprocessing"]
  score["Score enabled capabilities"]
  valid{"Data, regime and output eligible?"}
end
subgraph sg_decision["Evidence and human authority"]
  unavailable["Unavailable with reason"]
  advisory["Version-bound advisory evidence"]
  review["Reliability review; mock disposition"]
  ledger[("Decision and outcome ledger")]
end
subgraph sg_change["Monitoring and controlled change"]
  monitor["Data, service and model signals"]
  triage["Owner triages alert and evidence"]
  incident["Contain; rollback via view 08b"]
  proposal["Data / model change proposal"]
  retrain["Authorized requalification and training"]
  release["New evidence and release review; view 08"]
end
input -->|"units, shape, freshness"| features
bundle -->|"verified model and transforms"| features
bundle -->|"failed verification; block load"| unavailable
features -->|"training-compatible features"| score
score -->|"result and uncertainty"| valid
valid -->|"no"| unavailable
valid -->|"yes"| advisory
advisory -->|"supports review"| review
unavailable -->|"manual review"| review
review -->|"actor, time and rationale"| ledger
input -->|"quality / freshness signals"| monitor
score -->|"latency and output distributions"| monitor
ledger -->|"reviewed outcomes; delayed labels"| monitor
monitor -->|"threshold breach or material change"| triage
triage -->|"incident"| incident
triage -->|"evidence supports investigation"| proposal
proposal -->|"scope and cost authorized"| retrain
retrain -->|"re-enter view 04; no auto-promotion"| release
class input data
class features,score,retrain model
class bundle,incident security
class valid,unavailable,proposal,release policy
class review,triage human
class advisory,ledger,monitor evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_run fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_decision fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_change fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Advisory Policy and Human Decisions

Model output cannot bypass eligibility or customer approval. Status: proposed/unimplemented; view v0.1. Requirements: PULSE-FR-004;PULSE-FR-007;PULSE-SR-001.

[Editable source](../diagrams/05_human_decision.mmd) · [SVG preview](../diagrams/05_human_decision.svg) · [PNG export](../diagrams/05_human_decision.png)

```mermaid
%% Advisory Policy and Human Decisions | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_model["Analytics output"]
 inference["Prediction and uncertainty"]
end
subgraph sg_policy["Eligibility and authority"]
 valid{"Within validated envelope?"}
 unavailable["Unavailable with reason"]
 advisory["Advisory evidence and limits"]
end
subgraph sg_human["Authorized decisions"]
 review["Reliability reviews evidence"]
 disposition{"Approve, modify or reject?"}
 mock["Mock work request"]
 ledger[("Decision and outcome ledger")]
end
inference -->|"versioned evidence"| valid
valid -->|"no"| unavailable
valid -->|"yes"| advisory
unavailable -->|"manual investigation"| review
advisory -->|"supports review"| review
review -->|"qualified recommendation"| disposition
disposition -->|"approved or modified"| mock
disposition -->|"rejected"| ledger
mock -->|"records reference disposition"| ledger
class inference model
class valid,unavailable,advisory policy
class review,disposition human
class mock policy
class ledger evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_model fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_policy fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_human fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Indigo—models; Gold—policy; Green—people; Purple—evidence.

## Security and Trust Zones

Separate future plant collection, processing and restricted evidence access. Status: proposed/unimplemented; view v0.1. Requirements: PULSE-SR-001;PULSE-SR-002;PULSE-SR-003;PULSE-SR-004.

[Editable source](../diagrams/06_security_boundaries.mmd) · [SVG preview](../diagrams/06_security_boundaries.svg) · [PNG export](../diagrams/06_security_boundaries.png)

```mermaid
%% Security and Trust Zones | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_ot["Future plant boundary"]
 source["Plant source systems"]
 intermediary["Approved read-only intermediary"]
end
subgraph sg_security["Identity and network controls"]
 identity["Named organizational identity"]
 private["Private access and scoped roles"]
end
subgraph sg_work["Controlled reference workspace"]
 ingest["Contract and integrity checks"]
 artifacts[("Restricted data and artifacts")]
 viewer["Advisory evidence viewer"]
end
source -.->|"read or approved export only"| intermediary
intermediary -.->|"later qualified records"| ingest
identity -->|"authenticates approved actor"| private
private -->|"authorizes access"| artifacts
ingest -->|"validated source and model digests"| artifacts
artifacts -->|"minimal evidence"| viewer
class source source
class intermediary,identity,private security
class ingest data
class artifacts,viewer evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_ot fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_security fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_work fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Teal—data; Purple—evidence; Rose—security.

## Proposed Azure Environment Topology

Separate reference development, release validation and later site deployment; show storage, compute, model assets and operational evidence without binding resources. Status: proposed/unimplemented; view v0.2. Requirements: PULSE-SR-002;PULSE-SR-003;AIG-REQ-001;AIG-REQ-002;PULSE-COST-REQ-001.

[Editable source](../diagrams/07_deployment_candidate.mmd) · [SVG preview](../diagrams/07_deployment_candidate.svg) · [PNG export](../diagrams/07_deployment_candidate.png)

```mermaid
%% Proposed Azure Environment Topology | Proposed design; unimplemented | Pulse architecture v0.2
flowchart TD
operator["Named operator; private route in 07b"]
subgraph sg_dev["Reference development — proposed"]
  devws["Azure ML workspace; model assets"]
  compute["Bounded training / batch compute"]
  devstore[("Qualified data and artifact storage")]
  devdeps["Scoped identity, vault and image dependencies"]
end
subgraph sg_release["Release authority"]
  release["Exact artifact and target review; view 08"]
end
subgraph sg_val["Isolated validation — proposed"]
  valws["Validation workspace / job runtime"]
  valstore[("Validation artifacts and evidence")]
  valdeps["Separate identity and dependency scopes"]
  viewer["Reference viewer / mock CMMS"]
end
subgraph sg_evidence["Restricted operational evidence"]
  logs[("Azure Monitor / environment-scoped logs")]
end
site["Later isolated site environment; separate gates"]
operator -->|"identity plus scoped operations"| devws
devws -->|"schedules versioned jobs"| compute
devdeps -->|"authorized dependency access"| compute
compute -->|"reads inputs; writes job artifacts"| devstore
devstore -->|"manifest and candidate evidence"| release
release -->|"approved digests; no rebuild"| valws
valdeps -->|"authorized dependency access"| valws
valws -->|"scoped results"| valstore
valstore -->|"bounded reference evidence"| viewer
devws -->|"diagnostics, access and usage"| logs
valws -->|"diagnostics, access and usage"| logs
viewer -.->|"evidence only; later site authorization"| site
class operator human
class devws,compute,valws model
class devstore,valstore data
class devdeps,valdeps security
class release,viewer,site policy
class logs evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_dev fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_release fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_val fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_evidence fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Proposed Network and Identity Paths

Distinguish private inbound client access from managed compute egress and identity authorization; resource placement is logical, not an implemented network. Status: proposed/unimplemented; view v0.2. Requirements: PULSE-SR-001;PULSE-SR-002;PULSE-SR-003;PULSE-SR-004.

[Editable source](../diagrams/07b_network_identity.mmd) · [SVG preview](../diagrams/07b_network_identity.svg) · [PNG export](../diagrams/07b_network_identity.png)

```mermaid
%% Proposed Network and Identity Paths | Proposed design; unimplemented | Pulse architecture v0.2
flowchart TD
subgraph sg_client["Authorized client boundary"]
  actor["Operator or approved release runner"]
  entra["Entra identity; scoped RBAC"]
end
subgraph sg_inbound["Customer-managed access VNet"]
  route["Approved private route and DNS"]
  amlpe["Workspace private endpoint"]
  datape["Dependency private endpoints"]
end
subgraph sg_service["Managed Azure service — outside client VNet"]
  workspace["Azure ML workspace service"]
end
subgraph sg_egress["Azure ML managed network"]
  compute["Job compute; workload identity"]
  egress["Approved outbound / private endpoint rules"]
end
subgraph sg_dependencies["Scoped dependencies and telemetry"]
  stores[("Storage, vault and image artifacts")]
  telemetry[("Restricted monitoring destination")]
end
actor -->|"sign in or federated authentication"| entra
actor -->|"separately established connectivity"| route
route -->|"resolve workspace private address"| amlpe
amlpe -->|"private workspace API access"| workspace
route -->|"authorized direct dependency access"| datape
datape -->|"private data plane"| stores
entra -->|"authorize operations; not connectivity"| workspace
workspace -->|"schedule authorized jobs"| compute
compute -->|"identity-scoped requests"| egress
egress -->|"approved dependency paths"| stores
egress -->|"approved diagnostic path"| telemetry
workspace -->|"configured resource diagnostics"| telemetry
class actor human
class entra,route,amlpe,datape,egress security
class workspace,compute model
class stores data
class telemetry evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_client fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_inbound fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_service fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_egress fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_dependencies fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Teal—data; Indigo—models; Green—people; Purple—evidence; Rose—security.

## Release and Promotion

Bind each promotion to verified artifacts, an exact destination, current evidence and release authority; failures deny new exposure. Status: proposed/unimplemented; view v0.2. Requirements: AIG-REQ-001;AIG-REQ-002;AIG-REQ-003;PULSE-SR-004;PULSE-NFR-004.

[Editable source](../diagrams/08_release_gates.mmd) · [SVG preview](../diagrams/08_release_gates.svg) · [PNG export](../diagrams/08_release_gates.png)

```mermaid
%% Release and Promotion | Proposed design; unimplemented | Pulse architecture v0.2
flowchart TD
subgraph sg_candidate["Candidate preparation — planned"]
  source["Code and registered model version"]
  ci["Contract, security and V&V checks"]
  manifest[("Release manifest and evidence")]
end
subgraph sg_gate["Scoped promotion authority"]
  approve{"Exact release authorized?"}
  stage["Stage verified bundle in target"]
  check{"Target checks pass?"}
end
subgraph sg_result["Release disposition"]
  hold["Hold; no new exposure"]
  run["Activate approved scope; monitor"]
  incident["Rollback or withdrawal; view 08b"]
end
source -->|"pinned inputs; no latest"| ci
ci -->|"passed applicable checks"| manifest
ci -->|"fail"| hold
manifest -->|"digests, target, evidence and authority"| approve
approve -->|"no; current Azure stop"| hold
approve -->|"yes; exact approved scope"| stage
stage -->|"integrity, access, contract and smoke tests"| check
check -->|"no"| hold
check -->|"yes"| run
run -->|"stop criterion or incident"| incident
class source source
class ci,manifest evidence
class approve,check,hold policy
class stage,run model
class incident security
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_candidate fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_gate fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_result fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Indigo—models; Gold—policy; Purple—evidence; Rose—security.

## Rollback and Safe Recovery

Withdraw affected advisories, assess the prior release and recover the full approved bundle or remain unavailable. Status: proposed/unimplemented; view v0.2. Requirements: PULSE-SR-004;PULSE-NFR-004;PULSE-NFR-005;AIG-REQ-001;AIG-REQ-002.

[Editable source](../diagrams/08b_rollback_recovery.mmd) · [SVG preview](../diagrams/08b_rollback_recovery.svg) · [PNG export](../diagrams/08b_rollback_recovery.png)

```mermaid
%% Rollback and Safe Recovery | Proposed design; unimplemented | Pulse architecture v0.2
flowchart TD
subgraph sg_contain["Incident containment — proposed"]
  alert["Release, model or integrity incident"]
  withdraw["Withdraw affected advisory"]
  evidence[("Retained incident and release evidence")]
end
subgraph sg_decide["Accountable recovery decision"]
  owner["Release owner checks recovery authority"]
  prior{"Prior release still eligible?"}
  manual["Unavailable; manual workflow"]
end
subgraph sg_restore["Exact bundle recovery"]
  restore["Restore approved manifest bundle"]
  checks["Integrity, compatibility and reconciliation"]
  valid{"Recovery checks pass?"}
  resume["Resume bounded exposure; monitor"]
end
alert -->|"contain invalid outputs"| withdraw
withdraw -->|"preserve versions and timing"| evidence
evidence -->|"supports recovery review"| owner
owner -->|"rights, security and approval still valid"| prior
prior -->|"no"| manual
prior -->|"yes"| restore
restore -->|"model, transforms, policy and environment"| checks
checks -->|"include target smoke tests"| valid
valid -->|"no"| manual
valid -->|"yes; authorized recovery only"| resume
class alert,withdraw security
class evidence,checks evidence
class owner human
class prior,manual,valid policy
class restore data
class resume model
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_contain fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_decide fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_restore fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Observability, Degraded Mode and Recovery

Connect runtime signals to accountable human response and revalidation. Status: proposed/unimplemented; view v0.1. Requirements: PULSE-NFR-003;PULSE-NFR-004;PULSE-NFR-005.

[Editable source](../diagrams/09_operations_recovery.mmd) · [SVG preview](../diagrams/09_operations_recovery.svg) · [PNG export](../diagrams/09_operations_recovery.png)

```mermaid
%% Observability, Degraded Mode and Recovery | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_monitor["Future service observations"]
 service["Data and advisory service"]
 monitors["Freshness, integrity and latency monitors"]
 incident{"Invalid data or service failure?"}
end
subgraph sg_response["Accountable response"]
 degraded["Unavailable and manual rounds"]
 owner["IT and reliability response"]
 restore["Restore approved state and reconcile"]
end
subgraph sg_evidence["Recovery evidence"]
 verify["Revalidate access, data and versions"]
 record[("Incident and recovery ledger")]
end
service -->|"bounded telemetry"| monitors
monitors -->|"threshold and window"| incident
incident -->|"yes"| degraded
degraded -->|"alerts named owners"| owner
owner -->|"authorized recovery"| restore
restore -->|"restored state"| verify
verify -->|"records RTO, RPO and gaps"| record
verify -->|"only valid advisory resumes"| service
class service model
class monitors,record evidence
class incident,degraded policy
class owner human
class restore data
class verify security
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_monitor fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_response fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_evidence fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Requirements, Risks and Evidence Trace

Join stakeholder needs and controls to evidence-bound review decisions. Status: proposed/unimplemented; view v0.1. Requirements: AIG-REQ-001;AIG-REQ-002.

[Editable source](../diagrams/10_traceability.mmd) · [SVG preview](../diagrams/10_traceability.svg) · [PNG export](../diagrams/10_traceability.png)

```mermaid
%% Requirements, Risks and Evidence Trace | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_inputs["Engineering inputs"]
 need["Customer need and source"]
 risk["Risk and obligation"]
end
subgraph sg_design["Governed design"]
 req["Atomic requirement"]
 component["Architecture component and ADR"]
 test["V&V method and criterion"]
end
subgraph sg_review["Evidence and authority"]
 evidence[("Versioned test evidence")]
 decision["Authorized review disposition"]
end
need -->|"derives with rationale"| req
risk -->|"allocates controls"| req
req -->|"allocated function"| component
req -->|"specified behavior"| test
component -->|"implemented configuration later"| test
test -->|"actual result later"| evidence
evidence -->|"supports bounded decision"| decision
class need source
class risk,req policy
class component data
class test,evidence evidence
class decision human
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_inputs fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_design fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_review fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Teal—data; Gold—policy; Green—people; Purple—evidence.

## Functional Capability Decomposition

Allocate source, analysis, policy and human responsibilities. Status: Proposed architecture; local harness implements a subset. Requirements: PULSE-FR-001;PULSE-FR-003;PULSE-FR-004;PULSE-FR-007.

[Editable source](../diagrams/11_functional_capabilities.mmd) ? [SVG preview](../diagrams/11_functional_capabilities.svg) ? [PNG export](../diagrams/11_functional_capabilities.png)

![Functional Capability Decomposition](../diagrams/11_functional_capabilities.svg)

```mermaid
%% Functional capabilities | Proposed architecture; local harness implements a subset | v0.4
flowchart TD
subgraph inputs["Source responsibilities"]
 source["Register authorized sources"]
 quality["Validate and quarantine"]
end
subgraph analysis["Reference analysis"]
 groups["Separate bearing groups"]
 features["Compute RMS and kurtosis"]
 eligible{"Validated capability?"}
 unavailable["Return unavailable with reason"]
 infer["Run qualified model later"]
end
subgraph people["Evidence and human authority"]
 evidence[("Versioned evidence")]
 review["Review and record disposition"]
end
source -->|"source bytes and rights"| quality
quality -->|"accepted observations only"| groups
groups -->|"partitioned observations"| features
features -->|"features and operating context"| eligible
eligible -->|"no: current harness"| unavailable
eligible -.->|"yes: future qualified release"| infer
unavailable -->|"reason and exact versions"| evidence
infer -.->|"bounded results and limitations"| evidence
evidence -->|"supports human review"| review
class source source
class quality,groups data
class features,infer model
class eligible,unavailable policy
class evidence evidence
class review human
classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
style inputs fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style analysis fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style people fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue?sources; Teal?data; Indigo?analytics; Gold?policy; Green?human authority; Purple?evidence; Rose?security where used.

## Integration Architecture

Separate local contracts from deferred cloud and CMMS adapters. Status: Local reference implemented; cloud and site paths deferred. Requirements: PULSE-FR-001;PULSE-FR-002;PULSE-FR-007;PULSE-FR-008.

[Editable source](../diagrams/12_integration_architecture.mmd) ? [SVG preview](../diagrams/12_integration_architecture.svg) ? [PNG export](../diagrams/12_integration_architecture.png)

![Integration Architecture](../diagrams/12_integration_architecture.svg)

```mermaid
%% Integration contracts | Local reference implemented; cloud and site paths deferred | v0.4
flowchart TD
subgraph intake["Local reference boundary"]
 input["Authorized JSON source window"]
 ingest["Source registration and contract check"]
 store[("Accepted windows and features")]
end
subgraph evidence["Reference evidence workflow"]
 policy["Capability policy: unavailable"]
 ledger[("Evidence and decision ledger")]
 viewer["Local evidence viewer"]
 person["Human disposition via local API"]
end
subgraph future["Future integration - not connected"]
 cloud["Private Azure data adapter"]
 cmms["Mock work-order proposals"]
end
input -->|"bytes and rights reference"| ingest
ingest -->|"validated window contract"| store
store -->|"feature and provenance versions"| policy
policy -->|"advisory schema and trace"| ledger
ledger -->|"generated read-only report"| viewer
viewer -->|"evidence for review"| person
person -->|"actor, rationale, evidence ID"| ledger
cloud -.->|"future qualified source contract"| ingest
person -.->|"future eligible evidence only"| cmms
class input source
class ingest,store,cloud data
class policy policy
class ledger evidence
class viewer,person,cmms human
classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
style intake fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style evidence fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style future fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue?sources; Teal?data; Indigo?analytics; Gold?policy; Green?human authority; Purple?evidence; Rose?security where used.

## Threats and Defense in Depth

Map input, integrity and access threats to bounded controls. Status: Local controls exercised; Azure controls unverified. Requirements: PULSE-FR-002;PULSE-SR-001;PULSE-SR-002;PULSE-SR-004.

[Editable source](../diagrams/13_threat_defense.mmd) ? [SVG preview](../diagrams/13_threat_defense.svg) ? [PNG export](../diagrams/13_threat_defense.png)

![Threats and Defense in Depth](../diagrams/13_threat_defense.svg)

```mermaid
%% Threat and defense mapping | Local controls tested; Azure controls unverified | v0.4
flowchart TD
subgraph source["Input trust boundary"]
 bytes["Untrusted source records"]
 validate["Schema, range and source-digest checks"]
end
subgraph processing["Processing integrity"]
 group["Bearing partition and replay checks"]
 policy["Abstain without qualified evidence"]
 reject[("Quarantine reasons")]
end
subgraph authority["Access and authority"]
 human["Local OS-authorized operator"]
 cloud["Future Entra roles and private access"]
 records[("Evidence and backup")]
end
bytes -->|"malformed or substituted payload"| validate
validate -->|"invalid input: no scoring"| reject
validate -->|"accepted source-bound windows"| group
group -->|"reject leakage or conflicting replay"| reject
group -->|"accepted observations"| policy
policy -->|"unavailable result and provenance"| records
policy -->|"discloses unavailable status"| human
human -->|"record disposition; no equipment write"| records
cloud -.->|"future tested access restriction"| records
class bytes source
class validate,group,cloud security
class policy policy
class reject,records evidence
class human human
classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
style source fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style processing fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style authority fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue?sources; Teal?data; Indigo?analytics; Gold?policy; Green?human authority; Purple?evidence; Rose?security where used.

## Critical Reference Runtime Path

Show validation, persistence, abstention and human disposition order. Status: Locally exercised generated fixtures; no trained model. Requirements: PULSE-FR-002;PULSE-FR-004;PULSE-FR-007;AIG-REQ-001.

[Editable source](../diagrams/14_reference_runtime.mmd) ? [SVG preview](../diagrams/14_reference_runtime.svg) ? [PNG export](../diagrams/14_reference_runtime.png)

![Critical Reference Runtime Path](../diagrams/14_reference_runtime.svg)

```mermaid
%% Critical reference runtime path | Locally exercised generated fixtures | v0.4
flowchart TD
subgraph receive["Receive and validate"]
 source["Register JSON bytes and rights"]
 check{"Contract, source and split valid?"}
 quarantine[("Quarantine with reason")]
end
subgraph calculate["Accepted-window transaction"]
 features["Calculate descriptive features"]
 accepted[("Persist window and features")]
end
subgraph result["Evidence transaction"]
 policy["No qualified model: unavailable"]
 evidence[("Persist versioned evidence")]
 person["Record human disposition"]
 backup[("Consistent SQLite backup")]
end
source -->|"source-bound window"| check
check -->|"no"| quarantine
check -->|"yes"| features
features -->|"idempotent insert"| accepted
accepted -->|"load accepted window only"| policy
policy -->|"no diagnosis, RUL or work order"| evidence
evidence -->|"existing evidence ID"| person
person -->|"commit decision then snapshot"| backup
class source source
class check,policy policy
class quarantine,evidence,backup evidence
class features model
class accepted data
class person human
classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
style receive fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style calculate fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style result fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue?sources; Teal?data; Indigo?analytics; Gold?policy; Green?human authority; Purple?evidence; Rose?security where used.

## AKS Degradation Assessment Runtime

Connect private requests, scaling and explicit capability limits. Local API exercised; proposed cloud deployment; alerts unavailable.

[Source](../diagrams/15_aks_alert_runtime.mmd) | [SVG](../diagrams/15_aks_alert_runtime.svg) | [PNG](../diagrams/15_aks_alert_runtime.png)

![AKS assessment runtime](../diagrams/15_aks_alert_runtime.svg)

```mermaid
%% AKS assessment runtime | Proposed deployment; local API exercised | v0.5
flowchart TD
subgraph access["Private access and identity"]
 caller["Authorized bearing client"]
 gateway["Internal HTTPS Gateway"]
 entra["Entra signing keys and roles"]
end
subgraph compute["AKS user pool: proposed three zones"]
 api["Assessment API replicas: 3 to 12"]
 contract["Bounded window and UTC checks"]
 features["RMS and kurtosis"]
 policy["Unqualified model: unavailable"]
end
subgraph operate["Scaling and release evidence"]
 hpa["HPA CPU target and pool limits"]
 registry[("Private image registry")]
 evidence[("Local tests and load evidence")]
 owner["Owner reviews release conditions"]
end
caller -->|"authenticated assessment"| gateway
gateway -->|"POST route only"| api
entra -->|"cached key verification"| api
api -->|"validated caller"| contract
contract -->|"bounded samples"| features
features -->|"descriptive evidence"| policy
policy -->|"response; no notification"| caller
hpa -->|"adjust replica count"| api
registry -->|"immutable image digest"| api
api -.->|"local measurements only"| evidence
evidence -->|"capacity and remaining gaps"| owner
owner -->|"scoped deployment disposition"| hpa
class caller source
class gateway,entra security
class api,features model
class contract data
class policy,hpa policy
class registry,evidence evidence
class owner human
classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
style access fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style compute fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style operate fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue sources; Rose security; Indigo analytics; Teal contracts; Gold policy; Purple evidence; Green human authority.

## Deployed Azure reference runtime

[Editable source](../diagrams/16_deployed_reference_runtime.mmd) | [SVG](../diagrams/16_deployed_reference_runtime.svg)

![Deployed reference runtime](../diagrams/16_deployed_reference_runtime.png)

```mermaid
%% Deployed Azure reference runtime | Generated fixture verified | 2026-10-11
flowchart TD
subgraph access["Operator and identity"]
 operator["Authorized operator"]
 ssh["NSG: operator SSH only"]
 entra["Entra: Pulse.Assess role"]
end
subgraph runtime["East US 2 zone 1: one D2as v6 VM"]
 caller["Managed-identity reference caller"]
 forward["Loopback port-forward"]
 api["K3s: one assessment API pod"]
 receipts[("SQLite receipts on local PVC")]
end
subgraph assurance["Verified behavior and limits"]
 policy["Unqualified detection: unavailable"]
 evidence[("Live token and restart evidence")]
end
operator -->|"encrypted operator session"| ssh
ssh -->|"run reference requests"| caller
entra -->|"signed access token"| caller
caller -->|"authenticated window"| forward
forward -->|"ClusterIP service"| api
api -->|"commit before response"| receipts
receipts -->|"restart verified"| evidence
api -->|"descriptive features only"| policy
policy -->|"unqualified result"| evidence
class operator human
class ssh,entra,forward security
class caller source
class api model
class receipts,evidence evidence
class policy policy
classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
style access fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style runtime fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style assurance fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
linkStyle default stroke:#425466,stroke-width:1.5px
```

## Reference Detector and Simulated Inbox

Deployed reference workflow; real benchmark-feature replay and automated reference-client acknowledgement tested. Detector qualification and site acceptance remain unavailable. [PNG](../diagrams/17_reference_detector_workflow.png) ? [SVG](../diagrams/17_reference_detector_workflow.svg) ? [Source](../diagrams/17_reference_detector_workflow.mmd).

```mermaid
%% Reference detector and simulated inbox | No production qualification
flowchart TD
subgraph sourcezone["Offline benchmark preparation"]
 source["IMS run 2 snapshots"]
 prepare["Verify hashes and derive RMS"]
end
subgraph accesszone["Authenticated reference client"]
 replay["Managed-identity replay"]
 auth["Entra token and asset grants"]
end
subgraph runtime["K3s reference-only workflow"]
 rule["Frozen RMS and ordered state"]
 decision{"Three exceedances?"}
 receipts[("Decision receipts")]
 inbox[("Simulated maintenance inbox")]
end
subgraph operations["Acknowledgement and recovery"]
 ack["Authenticated client acknowledgement"]
 audit[("Persistent acknowledgement")]
 backup[("Bounded local backups")]
end
source -->|"native measurements"| prepare
prepare -->|"RMS + hashes"| replay
replay -->|"reference request"| auth
auth -->|"authorized asset"| rule
rule -->|"ratio and streak"| decision
decision -->|"no: record no flag"| receipts
decision -->|"yes: one episode"| inbox
inbox -->|"atomic commit"| receipts
inbox -->|"scoped event lookup"| ack
ack -->|"idempotent record"| audit
receipts -->|"SQLite snapshot"| backup
audit -->|"same database"| backup
class source,replay,ack source
class prepare data
class auth security
class rule model
class decision policy
class receipts,inbox,audit,backup evidence
classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
style sourcezone fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style accesszone fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style runtime fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
style operations fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
linkStyle default stroke:#425466,stroke-width:1.5px
```

## Render reference views

`scripts/render_reference_views.cjs` uses the project configuration in `docs/diagrams/mermaid-config.json`. Pass a temporary Mermaid tooling directory as the first argument and, optionally, a view name as the second. Set `PULSE_BROWSER` to the browser executable when the default Windows Edge path is unavailable. `DME_MERMAID_CONFIG` optionally selects another configuration by absolute path.

# Architecture Views

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

View correspondence: source/run/evidence IDs and authority boundaries must agree across all views, requirements and ADRs. Dashed edges represent future scope or unbuilt transitions, never existing connections. All controls and cloud resources are proposals. Sources and labels differ by view purpose; no graphic grants authority.

## System Context and Authority

Distinguish reference evidence, future site sources and human authority. Status: proposed/unimplemented. Requirements: PULSE-SR-001;PULSE-FR-007;AIG-REQ-003.

[Editable source](../diagrams/01_system_context.mmd) · [SVG preview](../diagrams/01_system_context.svg)

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

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## As-Is Workflow and Proposed Handoff

Show the fictional current process and where advisory evidence would enter. Status: proposed/unimplemented. Requirements: PULSE-FR-007;PULSE-FR-008.

[Editable source](../diagrams/02_as_is_conops.mmd) · [SVG preview](../diagrams/02_as_is_conops.svg)

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

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Data Architecture and Lineage

Keep rejected data apart and propagate immutable source/split identities. Status: proposed/unimplemented. Requirements: PULSE-FR-001;PULSE-FR-002;PULSE-NFR-008.

[Editable source](../diagrams/03_data_lineage.mmd) · [SVG preview](../diagrams/03_data_lineage.svg)

```mermaid
%% Data Architecture and Lineage | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_source["Source provenance"]
 files["Rights-qualified source files"]
 manifest[("Checksum and rights manifest")]
end
subgraph sg_data["Data foundation"]
 contract["Schema and units validation"]
 accepted[("Qualified bearing and run data")]
 quarantine[("Quarantined records")]
 split["Group split before windowing"]
end
subgraph sg_evidence["Evaluation provenance"]
 features["Versioned features"]
 lineage[("Split and feature manifest")]
end
files -->|"source bytes and metadata"| contract
manifest -->|"allowed use and digest"| contract
contract -->|"accept valid inputs"| accepted
contract -->|"reject with reason"| quarantine
accepted -->|"independent source groups"| split
split -->|"assigned windows"| features
features -->|"record transformations"| lineage
class files source
class contract,accepted,quarantine,split data
class features model
class manifest,lineage evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_source fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_data fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_evidence fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## AI Capability and Evaluation Lifecycle

Separate anomaly, diagnosis and RUL eligibility; protect the test holdout. Status: proposed/unimplemented. Requirements: PULSE-FR-003;PULSE-FR-005;PULSE-FR-006.

[Editable source](../diagrams/04_model_lifecycle.mmd) · [SVG preview](../diagrams/04_model_lifecycle.svg)

```mermaid
%% AI Capability and Evaluation Lifecycle | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_data["Qualified evaluation data"]
 groups["Frozen bearing and run partitions"]
 labels["Qualified fault and lifetime labels"]
end
subgraph sg_models["Analytics and models"]
 baseline["RMS and kurtosis baseline"]
 anomaly["Anomaly candidate"]
 diagnosis["Fault classifier when eligible"]
 rul["RUL with validated intervals"]
end
subgraph sg_review["Evidence and review"]
 compare["Validation selection then sealed test"]
 report[("Metrics and limitations")]
end
groups -->|"same evaluation conditions"| baseline
groups -->|"normal training subset"| anomaly
labels -->|"supported classes"| diagnosis
labels -->|"failure and censoring endpoints"| rul
baseline -->|"baseline outcomes"| compare
anomaly -->|"candidate outcomes"| compare
diagnosis -->|"eligible class evidence"| compare
rul -->|"eligible prognostic evidence"| compare
compare -->|"independent group results"| report
class groups,labels data
class baseline,anomaly,diagnosis,rul model
class compare policy
class report evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_data fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_models fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_review fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Advisory Policy and Human Decisions

Model output cannot bypass eligibility or customer approval. Status: proposed/unimplemented. Requirements: PULSE-FR-004;PULSE-FR-007;PULSE-SR-001.

[Editable source](../diagrams/05_human_decision.mmd) · [SVG preview](../diagrams/05_human_decision.svg)

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

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Security and Trust Zones

Separate future plant collection, processing and restricted evidence access. Status: proposed/unimplemented. Requirements: PULSE-SR-001;PULSE-SR-002;PULSE-SR-003;PULSE-SR-004.

[Editable source](../diagrams/06_security_boundaries.mmd) · [SVG preview](../diagrams/06_security_boundaries.svg)

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

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Azure Capability Mapping — Proposed

Map logical capabilities without claiming resources or selecting measured SKUs. Status: proposed/unimplemented. Requirements: PULSE-SR-002;PULSE-SR-003;PULSE-COST-REQ-001.

[Editable source](../diagrams/07_deployment_candidate.mmd) · [SVG preview](../diagrams/07_deployment_candidate.svg)

```mermaid
%% Azure Capability Mapping — Proposed | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_operator["Operator and governance"]
 operator["Dr. Moore approved client path"]
 gate["Scope, cost and cloud-entry review"]
end
subgraph sg_platform["Future nonproduction platform"]
 network["Private route and DNS"]
 workspace["Azure ML workspace candidate"]
 storage[("Governed storage candidate")]
 identity["Workload identity and secrets"]
end
subgraph sg_evidence["Operational evidence"]
 logs[("Access, usage and recovery records")]
end
operator -->|"review accepted parameters"| gate
gate -.->|"later authorized construction"| network
network -->|"private client access"| workspace
workspace -->|"versioned artifacts and datasets"| storage
identity -->|"scoped authenticated access"| workspace
workspace -->|"security and cost telemetry"| logs
class operator human
class gate policy
class network,identity security
class workspace model
class storage data
class logs evidence
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_operator fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_platform fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_evidence fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Release and Promotion Gates

Require evidence and authority; current work stops before cloud entry. Status: proposed/unimplemented. Requirements: AIG-REQ-002;AIG-REQ-003.

[Editable source](../diagrams/08_release_gates.mmd) · [SVG preview](../diagrams/08_release_gates.svg)

```mermaid
%% Release and Promotion Gates | Proposed design, not deployed | PULSE v0.1
flowchart TD
subgraph sg_design["Current preparation"]
 design["Versioned design package"]
 review["Dr. Moore reviews and corrects"]
 cloud{"Cloud-entry evidence and authority?"}
 hold["Remain pre-Azure"]
end
subgraph sg_future["Later engineering and assurance"]
 platform["Governed platform construction"]
 vv["Data, model and workflow V&V"]
 release{"Exact release authorized?"}
 exposure["Bounded authorized exposure"]
end
design -->|"reviewable artifacts"| review
review -->|"record disposition and conditions"| cloud
cloud -->|"no: current boundary"| hold
cloud -.->|"yes: later scope"| platform
platform -->|"implemented controls"| vv
vv -->|"fresh evidence and risk review"| release
release -->|"no"| hold
release -->|"yes"| exposure
class design evidence
class review human
class cloud,hold,release policy
class platform data
class vv evidence
class exposure human
  classDef source fill:#EAF3F8,stroke:#356079,stroke-width:1.5px,color:#111111
  classDef data fill:#E5F4F2,stroke:#32746E,stroke-width:1.5px,color:#111111
  classDef model fill:#EDF0FA,stroke:#42558B,stroke-width:1.5px,color:#111111
  classDef policy fill:#F8F2E4,stroke:#876A2D,stroke-width:1.5px,color:#111111
  classDef human fill:#EFF6EB,stroke:#4C713E,stroke-width:1.5px,color:#111111
  classDef evidence fill:#F3F0F8,stroke:#6E5B85,stroke-width:1.5px,color:#111111
  classDef security fill:#FBEFED,stroke:#9B534C,stroke-width:1.5px,color:#111111
  style sg_design fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  style sg_future fill:none,stroke:#657588,stroke-width:1.5px,color:#111111
  linkStyle default stroke:#425466,stroke-width:1.5px
```

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Observability, Degraded Mode and Recovery

Connect runtime signals to accountable human response and revalidation. Status: proposed/unimplemented. Requirements: PULSE-NFR-003;PULSE-NFR-004;PULSE-NFR-005.

[Editable source](../diagrams/09_operations_recovery.mmd) · [SVG preview](../diagrams/09_operations_recovery.svg)

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

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

## Requirements, Risks and Evidence Trace

Join stakeholder needs and controls to evidence-bound review decisions. Status: proposed/unimplemented. Requirements: AIG-REQ-001;AIG-REQ-002.

[Editable source](../diagrams/10_traceability.mmd) · [SVG preview](../diagrams/10_traceability.svg)

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

Legend: Blue—sources; Teal—data; Indigo—models; Gold—policy; Green—people; Purple—evidence; Rose—security.

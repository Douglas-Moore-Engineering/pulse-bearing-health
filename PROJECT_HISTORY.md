# Pulse — Bearing Health

Current engineering plan: [prioritized backlog](docs/CURRENT_ENGINEERING_BACKLOG.md) and [reconciled skill review](docs/SKILL_COMPLETION_REVIEW.md). Latest recorded full suite: 143 tests passed. Pilot API deployed; live intake passed; review-role token propagation remains pending. Reference demonstration prepared; production detector remains NOT_PROMOTED.

Current decision: [detector candidate NOT_PROMOTED](data/qualification/detector-candidate-disposition.md). Consumed-case testing is complete for this increment; production detector qualification is not complete. Cases 3-10 remain reserved.

Latest development: [paired SCA comparison](data/qualification/sca-paired-development.md) reduces case-2 false positives on identical paired records from 72 to 3, with detections falling from 89 to 86 and 205 normal-side abstentions. NOT_PROMOTED; reserved cases unchanged.

Latest frozen evaluation: [SCA cases 2/11](data/qualification/sca-envelope-validation.md). Case 2 detected 91/94 fault snapshots but flagged 129/296 normal snapshots. Candidate NOT_PROMOTED; cases 2/11 now consumed, cases 3-10 remain reserved.

Latest development: [SCA envelope features](data/qualification/sca-spectral-development.md) detected 112/117 fault snapshots with 7/126 normal positives for the known inner-ring feature. Exploratory case 1 only; frequency interpretation and independent validation remain open. NOT_PROMOTED.

Latest detector result: [SCA case 1](data/qualification/sca-case1-results.md) retrospective RMS diagnostic detected 1/117 fault snapshots and flagged 0/126 normal snapshots. RMS-only sensitivity is inadequate for this case; NOT_PROMOTED. Cases 2-11 remain reserved.

Detector evidence increment: [endpoint audit](data/qualification/detector-gap-resolution.md) now binds published stopping-event logs to uncertainty-aware warning calculations. 103 tests passed. Physical-failure warning and healthy-exposure acceptance remain inconclusive; no detector promotion.

## Customer demonstration readiness - 2026-10-11

Prepared for a guided customer demo and discovery meeting. Open the [interactive benchmark demo](customer/benchmark-demo.html) and [pilot preparation package](customer/09-customer-pilot-package.md). The package includes a walkthrough, proposed responsibilities, intake requirements, acceptance plan, cost boundary and service/exit conditions. Actual customer authorization and production acceptance remain pending.

The offline grouping prototype reduces LDM B04/B12/B17 episodes from 3/26/9 to 1/1/1 without changing the first alert. This is development on consumed evidence, not independent validation or proven nuisance reduction. [Evidence](governance/evidence/customer-demo-stability.json). The separate live Azure reference rule is unchanged; neither physical-failure warning nor nuisance-alert acceptance has been established.

96 software tests passed. The demo was rendered and all three run selections checked in Edge. Existing Azure health was checked healthy on 2026-10-11. Single-node availability, host-loss recovery, primary retention and sustained 1.5-million-request/day capacity remain unqualified. The USD 100/month ceiling remains; no paid resources were added. [Operations](runbooks/reference-operations.md) and [skill review](docs/SKILL_COMPLETION_REVIEW.md).

<details>
<summary>Previous status records (historical)</summary>


## Current reference build ? 2026-10-11

The fictional-customer reference workflow is deployed on Azure K3s: authenticated benchmark-feature assessment, frozen RMS anomaly rule, durable simulated maintenance inbox and idempotent acknowledgement. A live replay processed **884 monitoring windows**, reproduced **17 flagged windows in one episode**, and measured **36.1 ms p95** for sequential requests. [Run evidence](governance/evidence/azure-reference-detector-replay.json).

The rule is explicitly **unqualified**. Independent IMS run-1 evaluation missed damaged bearing 4 and flagged bearing 3 only ten minutes before the final snapshot. [Independent results](data/qualification/ims-independent-results.md). The user authorized invented requirements for this fictional customer; [recorded assumptions](config/fictional-reference-acceptance.json) set a 60-minute warning target, one nuisance alert per bearing per 30 operating days and a simulated internal inbox. These assumptions do not turn measured failures into a pass or authorize external messaging.

Asset authorization, local monitoring and daily bounded backups are deployed. The authorized off-host restore recovered 3,149 original receipts, all 884 reference decisions and the acknowledged episode. [Operations](runbooks/reference-operations.md) ? [Workflow diagram](docs/diagrams/17_reference_detector_workflow.svg) ? [Skill review](docs/SKILL_COMPLETION_REVIEW.md) ? [Architecture index](docs/architecture/README.md).

**84 tests passed.** The Azure ceiling remains USD 100/month; no paid resource was added. Qualified detector performance, primary-data retention at scale, six-hour/full-day capacity and actual site/production assurance remain incomplete. Earlier increments below are historical.

Additional data qualification: reviewed five LDM-UPB runs and reserved B12/B17 from signal-based tuning. Documentation counts and calibration passed inspection; complete signal integrity, endpoint qualification and healthy exposure remain unresolved. [Qualification and prospective split](data/qualification/ldm-additional-runs.md).

KAIST and UNSW data work: prospective experiment partitions and native acquisition evidence are recorded in the [qualification review](data/qualification/kaist-unsw-review.md). Both development archives passed publisher SHA-256 verification. UNSW Test 1 passed native checks across all 108 measurements; three KAIST snapshots contain non-finite values requiring explicit handling. Reserved experiments remain untouched.

KAIST development replay: all 129 recordings inspected under explicit missingness handling. The 3x RMS rule gives zero observed lead; lower development thresholds give 106 minutes to the last acquisition, not validated failure warning. [Results](data/qualification/kaist-development-results.md). 89 tests passed; deployed detector unchanged.

Cross-dataset development comparison selected a provisional 1.5x RMS candidate: it detects the previously missed IMS bearing but increases alerts on unlabeled bearings. [Results and validation boundary](data/qualification/development-threshold-comparison.md). No deployed rule or acceptance gate changed.

Reserved-validation replay completed under a frozen 1.5x protocol: B04 produced 208.25 minutes of descriptive lead and 3 episodes; UNSW Test 2 produced 2 episodes with warning time unscorable. [Validation results](data/qualification/rms-v2-validation.md). 92 tests passed; endpoint and nuisance criteria remain unresolved, and the deployed rule is unchanged.

Final LDM research test completed without retuning: B12/B17 lead to last acquisition was 132.4/195.9 minutes, with 26/9 alert episodes. Candidate disposition: NOT PROMOTED; physical-failure warning and nuisance criteria remain unscorable. [Final results](data/qualification/rms-v2-final-research.md). UNSW Tests 3/4 remain reserved.

<details>
<summary>Historical increments and design baseline (superseded where the current status differs)</summary>

## Dataset run results - 2026-10-11

Executed the frozen exploratory RMS baseline on all 984 IMS run 2 snapshots (four channels). Bearing 1 produced one sustained anomaly episode, first flagged three hours before the final recorded snapshot, with peak RMS 9.34 times the early baseline. Other channels produced no flags. [Run results and limits](data/qualification/ims-run2-results.md) distinguish this observation from validated failure warning, RUL or independent-run performance. Azure authentication and persisted receipt replay were rechecked successfully. The live API still reports detection unavailable; no detector was promoted or notification sent.

## Deployed reference runtime - 2026-10-11

K3s v1.37.1+k3s1 and the authenticated Pulse assessment API are now deployed on `vm-pulse-k3s`, Standard_D2as_v6, East US 2 zone 1. The pod is Ready and its persistent volume is Bound. A real managed-identity token was accepted, anonymous access returned 401, and an assessment receipt survived a pod restart unchanged. [Live verification](governance/evidence/azure-api-live-verification.json).

The USD 100/month ceiling enabled this deployment; the 744-hour service estimate is USD 80.4253 with a USD 19.5747 tax/contingency reserve, subject to actual metered usage. [Operator access](infra/single-node/README.md) uses SSH and loopback forwarding; no public HTTP application endpoint exists. [ADR-011](architecture/adr/011-single-node-reference-deployment.md) records the implemented architecture. **The full bearing-degradation system remains incomplete:** qualified detection and notifications are unavailable, daily capacity and six-hour peak behavior are not validated, and production/site acceptance remains blocked. Earlier quota/budget blockers describe superseded attempts. No support request was sent.


## Budget update - 2026-10-11

Dr. Moore raised the authorized Pulse deployment ceiling to **USD 100/month**. The existing Azure budget resource `pulse-monthly-50` now tracks 100; its historical name is retained to avoid duplicate budgets. Previous USD 50 decisions are historical. A dedicated two-vCPU host is being evaluated within the revised ceiling. Sending the drafted Azure Support request was not authorized and it remains unsent. [Budget policy](governance/cloud-budget.json).


## Build continuation - 2026-10-11

Added optional durable single-node assessment receipts, replay consistency and conflicting-window rejection. 68 tests passed; a non-root/read-only container retained its generated receipt across restart. Packaged a private image archive and single-node Kubernetes manifests with SHA-256 hashes; [release evidence](governance/evidence/single-node-release-package.json). Azure now also has the single-tenant Pulse API identity and a secretless reference caller with only Pulse.Assess. No live token flow has been tested.

Deployment remains incomplete: Azure rejected a two-vCPU Central US Basv2 request with QuotaNotAvailableForResource and an East US 2 Bsv2 request with ContactSupport. [Prepared support request](customer/AZURE_QUOTA_SUPPORT_REQUEST.md) has not been sent. No paid VM or Kubernetes runtime exists. Qualified detection, notification delivery, storage retention/backup, asset-level authorization and daily capacity validation remain open. The USD 50 ceiling remains binding.


## Live Azure execution - 2026-10-11

Created and verified `rg-pulse-reference` in East US 2 under the authorized subscription. Created the resource-group-scoped `pulse-monthly-50` monthly cost-tracking budget. The budget does not stop billing and has no notification recipients configured. [Resource-group evidence](governance/evidence/azure-resource-group-created.json). Also deployed `vnet-pulse-reference`, subnet `kubernetes-demo` and `nsg-pulse-reference` with inbound deny and default outbound disabled. [Live inventory](governance/evidence/azure-live-resource-inventory.json) and [successful deployment](governance/evidence/azure-foundation-deployment.json) are recorded. No paid compute or qualified alert service is deployed. B2s remains restricted in normal US regions; alternate unrestricted region entries have no verified retail price. East US B2als_v2 is restricted with zero family quota. Earlier no-resource statements describe historical increments.


## Current budget decision ? 2026-10-11

Dr. Moore authorized **USD 50/month** for Pulse. [The recorded budget](governance/cloud-budget.json) supersedes earlier statements that the ceiling was missing. The six-node AKS proposal is unaffordable and disabled in its deployment script before any Azure call. Its $1,213.62/month partial minimum is retained as rejected sizing evidence. No paid resources were created. Azure budget alerts are not a billing hard cap. A replacement must fit the full service estimate and undergo capacity validation; 1.5 million daily degradation alerts remains an unproven requirement.


## Current implementation increment ? 2026-10-11

The [reference implementation](docs/REFERENCE_IMPLEMENTATION.md) now exercises source registration, contract/quarantine checks, bearing partition consistency, descriptive features, explicit abstention, evidence and mock decisions locally. [Azure foundation source](infra/azure/README.md) and four additional [architecture views](docs/architecture/README.md) are prepared. See the [current execution handoff](customer/08-deployment-execution.md).

The user authorized Azure access and deployment within limits to be provided. Existing Azure account context and live read access are now verified; see [connection evidence](governance/evidence/azure-connection-check.json). Spending limits remain unresolved; no paid resource creation, training job or deployment has occurred. No qualified dataset or trained model exists. Local fixture tests do not pass cloud, model or site gates.

The pre-Azure v0.3 material below is the historical design baseline. Its original stop boundary is superseded only by the bounded authorization recorded in the current handoff; it is not a statement that the new implementation has been deployed.

PULSE pre-Azure review v0.3 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Douglas Moore Engineering, LLC · Private fictional customer portfolio engagement

**Current state:** pre-Azure design package v0.3, prepared for Dr. Moore's review. Candidate requirements, standards/tailoring/SEMP, architecture and data/security/governance/V&V planning are documented. No dataset is qualified, no model is trained, no Azure resource exists and no site performance or customer approval is claimed. **Stop before any Azure connection or provisioning.**

## Contents

- [Start here: pre-Azure review](docs/PRE_AZURE_REVIEW.md)
- [DME skills and VS Code setup](docs/DME_SKILLS.md) and [repository agent instructions](AGENTS.md)
- [Customer discovery](customer/01-discovery-record.md), [review](customer/02-customer-review-handoff.md), [open items](customer/03-open-items.md)
- [Lifecycle cost model](customer/04-lifecycle-cost-model.md), [business case](customer/05-business-case.md), [work breakdown](customer/06-engineering-cost-work-breakdown.md)
- [Engineering handoff](customer/07-pre-azure-engineering-handoff.md)
- [Standards applicability](governance/standards/standards_applicability_matrix.csv) and [SEMP](docs/systems-engineering-management-plan.md)
- [Requirements and V&V](docs/03-requirements-and-traceability.md)
- [Architecture and diagram index](docs/architecture/README.md)
- [Engineering documentation index](docs/README.md)
- [AI governance](governance/AI_GOVERNANCE_PLAN.md) and [security](docs/06-security-and-threat-model.md)
- [Cloud entry: BLOCKED](docs/09-cloud-entry-gate.md) and [Azure platform proposal](infra/azure/PLATFORM_PLAN.md)
- [Project status](PROJECT_STATUS.md) and [validation evidence](governance/evidence/design-validation.json)

## Diagram review

[Bronze/Silver/Gold data architecture](docs/diagrams/03_data_lineage.svg) · [Data-layer contracts and promotion rules](docs/04-data-architecture-and-digital-thread.md).

[Training and registration](docs/diagrams/04_model_lifecycle.svg) · [Inference and monitoring](docs/diagrams/04b_inference_monitoring.svg) · [Release](docs/diagrams/08_release_gates.svg) · [Rollback](docs/diagrams/08b_rollback_recovery.svg) · [Environment topology](docs/diagrams/07_deployment_candidate.svg) · [Network and identity](docs/diagrams/07b_network_identity.svg). Read the [full index](docs/architecture/README.md) for all thirteen views and their editable sources. The v0.2 correction expands these design views; further architecture-view gaps remain in the review backlog.

## Mission and architecture thesis

Support qualified maintenance investigation of rolling-element bearing deterioration on 12 critical electric motors at one fictional plant. Use trustworthy source/lineage and simple baselines first; keep anomaly detection, diagnosis and RUL separately eligible. Present evidence and limitations through policy to authorized human review. No equipment actuation or real CMMS writes are in the reference increment. Pump hydraulic, fan aerodynamic, gearbox and motor electrical diagnosis are excluded.

## Authority, staffing and evidence

Dr. Douglas Moore is DME's sole founder, architect, engineer and delivery lead. Customer roles are fictional. Independent assurance is not claimed. Public source pages establish candidate properties/rights only; dataset bytes, labels, splits, model metrics, site compatibility, realized savings and financial affordability remain unverified. The $60,000 build and $18,000 annual figures are fictional ceilings; the $114,000 proposed three-year envelope is not estimated TCO.

## Repository structure and local review

customer/ holds governed engagement/economic records; docs/ holds engineering plans and Mermaid views; requirements/ and architecture/ hold registers/ADRs; governance/ holds standards, risk, V&V and gate records; data/ holds draft contracts/qualification; infra/azure/ holds an unprovisioned plan; runbooks/ holds proposed procedures; scripts/ validates this design package. No production data/model code or deployment automation is included at this boundary.

Open pulse.code-workspace in VS Code. Five DME skills are bundled under `.agents/skills/`; follow [DME skills setup](docs/DME_SKILLS.md) to verify their availability in Codex. Run `python scripts/validate_review_package.py` to check document/schema/register consistency. The check is offline and connects to no cloud service. It does not execute runtime V&V tests or grant gate approval.

## Next phase

Dr. Moore reviews the prepared package and its open conditions. Qualify actual data, measure workload and refine costs/security decisions. Azure entry remains blocked until applicable evidence and later explicit authorization are recorded. User review is distinct from real customer/site acceptance.

## Confidentiality

Remain private unless Dr. Moore requests publication. Do not commit customer data, credentials, proprietary evidence or unapproved benchmark redistribution. Read SECURITY.md and CONTRIBUTING.md before further work.

## Kubernetes scale increment

The user requests bearing-degradation assessments at 1.5 million requests/day, with a 09:00-15:00 peak. [Capacity and release evidence](docs/AKS_CAPACITY_AND_RELEASE.md) and the [AKS runbook](infra/aks/README.md) describe the implemented authenticated API, compiled foundation and deployment blockers. No qualified alerts, durable alert delivery or deployed AKS capacity is claimed.

</details>

</details>

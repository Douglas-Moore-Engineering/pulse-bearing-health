# AI Governance Plan

Current increment: see the [2026-10-11 execution handoff](../customer/08-deployment-execution.md). The pre-Azure statements below describe the historical design baseline. The user has since authorized Azure access/deployment subject to limits; account access is verified; spending inputs and evidence gates remain unresolved. No cloud deployment or gate approval is claimed.

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Intended use: offline reference research and future human-reviewed bearing-health advice. Prohibited uses: safety protection, autonomous equipment/work-order control, personnel decisions and claims of site reliability/RUL/ROI without evidence. Public/user data only after qualification; no actual personal/customer operational data has been authorized.

Reference impact tier: **provisional G2** (bounded offline exposure with potential misleading portfolio claims). Future site tier: **pending, provisionally G3** because fault omission, automation bias and unknown asset consequences could have serious physical/operational impact; advisory status alone does not lower that risk. No catastrophic scope is evidenced, so do not assert G4 classification. The maximum-assurance library remains available for upward tailoring; reassess before site use or any autonomy.

Control applicability is in CONTROL_APPLICABILITY.csv; requirements/V&V use shared authoritative registers. AIG-C23 independent review is required if G3 site use remains classified. Dr. Moore cannot be his own independent assessor. Triggered hazards/OT controls remain planned. AIG-C29/30 are proposed N/A for this no-GenAI/no-agent design; reassess if scope changes. Organizational C33 policy/competence and management evidence are unresolved beyond this project.

Gates AIG-G0/G1/G2 are prepared for review but BLOCKED pending authority, rights, impact/obligation and scope dispositions; later gates have no implementation evidence. No model freeze, production authorization or risk acceptance exists. This does not prohibit current authorized design preparation.

Governance schedule: review at requirements/architecture, dataset freeze, offline V&V, site adaptation, ORR/authorization and changes. Proposed G2 six-month and G3 quarterly maxima follow DME policy, not legal mandates; immediate reassessment on scope/rights/incident changes. Retirement, incidents and monitoring plans are in runbooks and operations documentation.

## Kubernetes assessment increment - 2026-10-11

The user requests a replicated degradation-alert service. [AKS capacity/release](../docs/AKS_CAPACITY_AND_RELEASE.md) records implementation and conditions. Existing Azure account/read access is verified. Generated API fixtures demonstrate authentication denials and abstention, not detector quality. All responses remain unavailable for degradation alerts; no durable evidence or notifications are emitted. Qualify policy/model, data partitions, asset authorization and delivery before operational use. Public exposure, actual site use and automation require separate review. No independent approval or production assurance is inferred from deployment source or local throughput.

## Deployed reference evidence - 2026-10-11

The user raised the Azure ceiling to USD 100/month. The restricted single-node K3s reference API is deployed; [live token and restart checks](evidence/azure-api-live-verification.json) demonstrate authenticated assessment persistence and anonymous rejection. This supersedes the earlier statement that no durable receipt exists for this reference implementation. Responses still abstain from degradation detection, and no notifications are sent. Model/data qualification, asset-level authorization, retention/backup, sustained capacity, operational acceptance and independent/site assurance remain unfinished. The user's deployment authorization does not supply those approvals. [ADR-011](../architecture/adr/011-single-node-reference-deployment.md) and [implemented runtime view](../docs/diagrams/16_deployed_reference_runtime.mmd) record the actual configuration.

## Exploratory dataset run - 2026-10-11

[IMS run 2 results](../data/qualification/ims-run2-results.md) add actual native numerical schema and frozen RMS-rule evidence. This is one experiment with an early-reference chronological split, unknown native amplitude units and no onset labels. It cannot pass independent-run performance, false-alert or RUL criteria. The candidate remains offline and unqualified; no production promotion, external notification or site claim was made. Existing gates and authority remain unchanged.

## Independent evaluation and operational controls - 2026-10-11

[Independent IMS evaluation](../data/qualification/ims-independent-results.md) consumed run 1 under the frozen rule and found a missed documented damaged bearing. Do not present a future tuned rule as held-out on this same run. The mismatched third archive is excluded from labeled evaluation. No detector was promoted.

[Live asset authorization](evidence/azure-asset-authorization.json), [authorized backup/restore](evidence/azure-receipt-backup-restore.json) and local monitoring add bounded implementation evidence. The offline alert-ledger component has fixture tests only; no external message or qualified alert is emitted. [engineering review](../docs/ENGINEERING_REVIEW.md) retains actual authority, acceptance gaps and trace. Gates remain blocked where criteria are unmet.

## Fictional-reference workflow boundary

The user explicitly authorized invented fictional customer criteria and destination. [Configuration](../config/fictional-reference-acceptance.json) records those assumptions. The deployed `/v1/reference` workflow is labeled unqualified, preserves unknown native units/timezone, accepts only the authorized reference asset, commits decisions and episode creation together, and offers a simulated inbox with authenticated acknowledgement. It cannot claim failure prediction or site validation. An automated client's acknowledgement is not human acceptance.

[Cloud replay](evidence/azure-reference-detector-replay.json) and [isolated recovery](evidence/azure-reference-workflow-restore.json) are actual test evidence. No external notification was sent. Fictional warning/false-alert targets remain unmet or unmeasurable; the existing `/v1/degradation/assess` route still abstains from qualified detection. No actual production gate is approved.

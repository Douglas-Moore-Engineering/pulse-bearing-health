# Pulse — Pre-Azure Review Package

Current increment: see the [2026-10-11 execution handoff](../customer/08-deployment-execution.md). The pre-Azure statements below describe the historical design baseline. The user has since authorized Azure access/deployment subject to limits; account/spending inputs and evidence gates remain unresolved. No cloud deployment or gate approval is claimed.

PULSE pre-Azure review v0.3 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

## Review in this order

1. [Customer discovery](../customer/01-discovery-record.md), [business case](../customer/05-business-case.md), and [lifecycle costs](../customer/04-lifecycle-cost-model.md).
2. [Standards applicability](../governance/standards/standards_applicability_matrix.csv), [SEMP](systems-engineering-management-plan.md), and [tailoring](../governance/standards/lifecycle_tailoring_record.md).
3. [Requirements and V&V](03-requirements-and-traceability.md).
4. [Architecture views](architecture/README.md), [trade studies](11-architecture-trade-studies.md), and [ADRs](12-architecture-decisions.md).
5. [Data and qualification](04-data-architecture-and-digital-thread.md), [AI evaluation](05-ai-ml-and-decision-intelligence.md), [security](06-security-and-threat-model.md), and [AI governance](../governance/AI_GOVERNANCE_PLAN.md).
6. [Cost work breakdown](../customer/06-engineering-cost-work-breakdown.md), [cloud-entry review](09-cloud-entry-gate.md), and [handoff](../customer/07-pre-azure-engineering-handoff.md).

## What is established

Versioned design records and proposed requirements now connect the fictional 12-motor use case to architecture components, risks, V&V methods and future gates. Data contracts are drafted; evaluation split policy separates source bearing/run groups. Logical diagrams and Azure capability mapping are design proposals. Repository validation checks referential consistency; it does not validate a trained model, safety, rights, financial viability or cloud resources.

## Decisions requested for a later review

Review the reference-versus-site scope, proposed requirements, advisory-only authority, data choices/rights and platform plan. Record corrections and version-bound disposition. No approval box is preselected; the current instruction authorizes preparation, not Azure access. The cost horizon remains a proposal and full affordability is unresolved.

## Material open conditions

Dataset bytes/rights/labels, measured workload, source-unit split feasibility, supported fault regimes, independent site-risk review, actual subscription/operator identity, region policy, private access path and sourced costs are unresolved. Azure entry is BLOCKED. This is a concrete package ready for your review, not a passed architecture or deployment gate.

## Architecture correction — v0.2

The original package used overview diagrams where detailed MLOps/release and deployment relationships were needed. Views 04, 07 and 08 are expanded, with focused companions 04b, 07b and 08b. Review exact version binding, promotion denial, inference/monitoring/retraining, rollback, environment separation, private access, identities and logging in the [architecture index](architecture/README.md), [AI/ML design](05-ai-ml-and-decision-intelligence.md), [release design](08-testing-release-gates-and-acceptance.md) and [platform plan](../infra/azure/PLATFORM_PLAN.md).

This correction completes those specified design expansions for review. It does not establish implementation readiness or exhaustive architecture-view coverage. The previously identified functional decomposition, integration, threat/defense and critical runtime sequence views remain separate design backlog items. Their relevant behavior is described in existing design records, but those additional views have not been authored in this correction. All cloud-entry conditions and runtime V&V dispositions remain open.

## Data architecture correction — v0.3

View 03 now explicitly defines Bronze/Silver/Gold with source fidelity, quality/quarantine, leakage prevention, product publication and lineage rules. Review the [data architecture](04-data-architecture-and-digital-thread.md), [layer register](../data/data_layers.csv) and [ADR-009](../architecture/adr/adr-009.md). This documents a proposed decision previously left implicit; it is not source qualification, implementation or architecture approval. Four other diagram types and all evidence-dependent cloud-entry conditions remain open as previously recorded.

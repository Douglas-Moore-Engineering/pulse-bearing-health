# Pulse — Bearing Health

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Douglas Moore Engineering, LLC · Private fictional customer portfolio engagement

**Current state:** pre-Azure design package v0.1, prepared for Dr. Moore's review. Candidate requirements, standards/tailoring/SEMP, architecture and data/security/governance/V&V planning are documented. No dataset is qualified, no model is trained, no Azure resource exists and no site performance or customer approval is claimed. **Stop before any Azure connection or provisioning.**

## Contents

- [Start here: pre-Azure review](docs/PRE_AZURE_REVIEW.md)
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

## Mission and architecture thesis

Support qualified maintenance investigation of rolling-element bearing deterioration on 12 critical electric motors at one fictional plant. Use trustworthy source/lineage and simple baselines first; keep anomaly detection, diagnosis and RUL separately eligible. Present evidence and limitations through policy to authorized human review. No equipment actuation or real CMMS writes are in the reference increment. Pump hydraulic, fan aerodynamic, gearbox and motor electrical diagnosis are excluded.

## Authority, staffing and evidence

Dr. Douglas Moore is DME's sole founder, architect, engineer and delivery lead. Customer roles are fictional. Independent assurance is not claimed. Public source pages establish candidate properties/rights only; dataset bytes, labels, splits, model metrics, site compatibility, realized savings and financial affordability remain unverified. The $60,000 build and $18,000 annual figures are fictional ceilings; the $114,000 proposed three-year envelope is not estimated TCO.

## Repository structure and local review

customer/ holds governed engagement/economic records; docs/ holds engineering plans and Mermaid views; requirements/ and architecture/ hold registers/ADRs; governance/ holds standards, risk, V&V and gate records; data/ holds draft contracts/qualification; infra/azure/ holds an unprovisioned plan; runbooks/ holds proposed procedures; scripts/ validates this design package. No production data/model code or deployment automation is included at this boundary.

Open pulse.code-workspace in VS Code. Run `python scripts/validate_review_package.py` to check document/schema/register consistency. The check is offline and connects to no cloud service. It does not execute runtime V&V tests or grant gate approval.

## Next phase

Dr. Moore reviews the prepared package and its open conditions. Qualify actual data, measure workload and refine costs/security decisions. Azure entry remains blocked until applicable evidence and later explicit authorization are recorded. User review is distinct from real customer/site acceptance.

## Confidentiality

Remain private unless Dr. Moore requests publication. Do not commit customer data, credentials, proprietary evidence or unapproved benchmark redistribution. Read SECURITY.md and CONTRIBUTING.md before further work.

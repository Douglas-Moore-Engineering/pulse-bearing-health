# Pulse — Lifecycle Cost Model

PULSE-LCC-001 v0.1 · 2026-10-10 · Fictional portfolio planning baseline · Prepared for review

## Basis and authority

Scope: one fictional plant, 12 critical electric-motor bearings; reference feasibility first, site instrumentation and deployment only if later authorized. Preserve the discovery exclusions. Three years of operation after future simulated acceptance is a proposed evaluation period, not an agreed service term. Year 0 covers discovery/build/transition; Years 1–3 cover operation; exit costs fall at the end of Year 3. Acceptance date and annual growth are TBD. DME support is described for only 12 months in discovery; Years 2–3 support/ownership must be resolved.

Currency: USD. Proposed constant October 2026 dollars, undiscounted; inflation and discounting are not applied to this initial envelope. Any nominal or discounted analysis must use separately documented assumptions and consistent cash-flow bases. No current supplier rates or measured costs have been inspected.

Estimate preparation/maintenance: Dr. Douglas Moore, sole DME delivery lead. Fictional finance controller reviews assumptions and affordability; fictional plant manager approves scope/commitment; IT/OT and reliability validate technical drivers. No review, actual signature, independent assurance or spending approval is evidenced.

## Existing budget constraints, not estimated costs

Source: [discovery Q-08 / PULSE-R08](01-discovery-record.md), fictional response dated 2026-10-08.

| Constraint | Fictional amount | Interpretation |
|---|---:|---|
| Implementation ceiling | $60,000 | Scope and cost inclusion must be reconciled before commitment |
| Incremental annual operations/support ceiling | $18,000 | Includes sensor service allowance; cloud and DME/customer support allocation TBD |
| Proposed three-year budget envelope | $114,000 | $60,000 + 3 × $18,000; arithmetic planning envelope only |

The $114,000 envelope is not lifecycle TCO: customer internal labor, reference discovery fees, hardware, future upgrades, exit and other inclusions remain unresolved. Do not add included DME labor or sensor service twice. This envelope also does not establish availability of three-year funding.

## Governed cost ledger

Use [lifecycle-cost-lines.csv](lifecycle-cost-lines.csv) as the line-item ledger subordinate to this model. One authoritative model; other records reference its ID/version. TBD is unknown, never zero. No exclusions are approved in v0.1. Establish costs for:

1. Discovery/design and engineering delivery fees.
2. Data acquisition/rights, preparation and labeling.
3. Sensor/edge hardware, installation and calibration.
4. Historian/CMMS integration and interface maintenance.
5. Verification, security/governance and acceptance.
6. Cloud compute/storage/network/egress and licenses.
7. Training, transition and customer internal staffing.
8. DME or successor support, monitoring, retraining/revalidation.
9. Upgrades, migration, retained evidence/export and decommissioning.

Document quantity × unit rate × occurrences by year; source/date, evidence state, payer, owner and inclusion mapping to budget ceilings. Treat DME invoice cost and underlying DME effort as alternative costing views, not additive customer expenses.

## Cash flows and update rules

| Period | Budget reference | Estimated total cost | Actual cost | Forecast remaining |
|---|---:|---|---|---|
| Year 0 | $60,000 implementation ceiling | TBD | Not recorded | TBD |
| Year 1 | $18,000 recurring ceiling | TBD | Not recorded | TBD |
| Year 2 | $18,000 recurring ceiling | TBD | Not recorded | TBD |
| Year 3 including exit | $18,000 recurring ceiling; exit inclusion TBD | TBD | Not recorded | TBD |

Sum nonoverlapping line amounts across all periods for lifecycle TCO. Reconcile paid-to-date plus forecast-to-complete with revised total; show variance against the cost baseline and budget separately. Unknown actuals are not $0. Track model versions, change reason and approval state.

Before cost reliance, prepare low/base/high estimates with sourced quantities/rates or explicitly justified ranges. Vary sensor coverage, scoring/training workload, retention, integration effort, internal support and retraining frequency. Show scenario cash flows, TCO and affordability; contingency is a separate risk-based allowance, not a hidden multiplier or automatically the high scenario. No numerical sensitivity results are established yet.

## Reviews and financial disposition

Current disposition: **affordability unresolved; planning only**. Reference feasibility preparation may continue within authorized scope. No build, purchases, recurring charges or production release follow from this estimate.

Review at discovery/business case, scope/SOW/hosting selection, architecture trade study and pre-build commitment; update at deployment/ORR, acceptance, quarterly operating reviews (proposed cadence), material changes/retraining, renewal/transfer and exit. Carry model ID/version, conditions, decision authority and next update in handoffs. Baseline a supported estimate before relying on affordability for build commitment; retain prior versions in Git.

Next update: scope/hosting/architecture review, before implementation commitment. Close LCC-OPEN-01 through LCC-OPEN-05 in [open items](03-open-items.md). Prepare actual cost/usage evidence as implementation and operation occur.

## Change history

- v0.1: introduced lifecycle coverage, budget-envelope reconciliation, ledger and unresolved affordability; no spending approval or measured cost claim.


## Pre-Azure engineering supplement — 2026-10-10

See [engineering review handoff](07-pre-azure-engineering-handoff.md) and [work breakdown](06-engineering-cost-work-breakdown.md). Preserve this record's existing version and fictional source statements; the new design package v0.1 is a separate prepared increment. No Azure connection, accepted design, actual approval or financial closure is inferred.

## AKS scale increment - 2026-10-11

PULSE-LCC-001 remains authoritative. [AKS capacity/cost analysis](../docs/AKS_CAPACITY_AND_RELEASE.md) supplies dated retail rates and partial monthly floors of $1,213.62 at minimum pools and $1,758.93 at maximum pools. These are subordinate to PULSE-COST-007, not additive duplicate costs or complete TCO. Networking, disks, security, observability, durable alert services and operations remain unpriced. Actual spending approval is pending; inherited fictional ceilings grant no spending authority. No cloud construction expense is claimed.

# Testing, Release Gates and Acceptance

PULSE pre-Azure review v0.2 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Design consistency checks validate links, IDs, requirement/test joins, JSON schemas and stopping scope. They are not model or integration tests. Planned runtime V&V is in the [matrix](../governance/verification_validation_matrix.csv).

Data tests: source checksum, schema/units, label provenance, bearing/run disjointness, training-only feature fitting and time-axis continuity. Model tests: frozen baseline comparisons, held-out metrics/uncertainty, unsupported-domain abstention, corruption and calibrated RUL intervals where eligible. Workflow tests: human disposition, no write authority, stale data, partial recovery and replay/idempotency. Platform tests: authenticated/private access, least privilege, retention, backup/restore, audit, cost and load behavior.

No training, model deployment, site shadow or customer acceptance is performed here. [Engineering gates](../governance/release_gates.md) and AI governance gates use separate namespaces. Gate completion is a conjunction of evidence and required authority, not a score. Manual approval records without tested enforcement cannot establish protected promotion.

## Concrete release contract — v0.2

[View 08](diagrams/08_release_gates.svg) describes promotion and denial; [view 08b](diagrams/08b_rollback_recovery.svg) details withdrawal and rollback. The [release-manifest template](../governance/release-manifest.template.json) is a field inventory with null values and `TEMPLATE_NOT_AUTHORIZED` status; it cannot authorize a deployment. It is separate from the source/lineage manifest because their subjects differ.

Before each promotion: pin the code, dependencies/environment, model, transforms, schemas, thresholds, policy, split/data evidence and target configuration; run relevant contract/leakage/security/model/workflow tests; record reports and exceptions; have the authorized role review the exact manifest digest and target. Changed bytes, destination, expired evidence or revoked approval invalidate that disposition. Fail closed on null/TBD references. No floating `latest` reference can identify the approved release. Branch/environment protection, runner identity and enforced checks are planned; no GitHub-to-Azure connection exists.

Promote the same verified artifact bundle into an isolated validation target. Compare source/destination digests after any copy; do not silently rebuild for a new environment. Bind environment-specific configuration and its digest to that target's approval. Execute integrity, access, contract, abstention, version-trace and smoke checks before activation. The reference increment remains batch/mock; shadow, canary and production advisory each require their own site evidence, ORR/CAR applicability, authority and re-entry through this gate. Do not automatically progress from one exposure level to the next.

Rollback first withdraws the affected advisory and records the incident. Resolve the last eligible approved manifest including preprocessing, model, thresholds, policy, environment and compatible configuration. Check that its rights, security and approvals remain valid; a prior release may no longer be safe. The release owner acts within explicit incident authority, stages the prior bundle, reruns integrity/compatibility/smoke checks, reconciles accepted records and only then resumes bounded exposure. If no valid prior release or recovery authority exists, stay unavailable and retain the manual workflow. Preserve rejected and rolled-back evidence; never erase the incident trail.

Future acceptance evidence must include bypass/expiry/mismatched-manifest rejection, verified artifact copy, negative authorization, withheld data, failed smoke checks, failed rollback, and recovery reconciliation. These exercises remain NOT_EXECUTED in the V&V register; successful diagram rendering does not satisfy them.

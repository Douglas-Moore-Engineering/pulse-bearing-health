# Current engineering work and evidence boundaries

Current position: customer lifecycle Phase 8 engineering and ongoing Phase 9 reviews; Phase 10 demonstration prepared, not customer-approved. No production acceptance is established. This backlog organizes remaining work without changing requirement IDs or gate dispositions.

| Priority | Work | Completion evidence | Dependency |
|---|---|---|---|
| 1 | Governed offline pilot-data intake | Validate identities, timestamp/units, calibration and rights/provenance references; quarantine malformed input; test rejection and accepted fixtures | Can implement now with synthetic fixtures; actual data permission required before customer intake |
| 2 | Review/adjudication records | Record reviewer, decision, rationale and evidence references; preserve unresolved outcomes and immutable audit history | Can implement locally; real reviewers and notification destinations remain unassigned |
| 3 | Primary receipt retention | Explicit configurable retention/export policy, dry-run inventory and tests proving protected records are retained | Prepare and test on synthetic databases; do not delete live receipts without authorized disposition |
| 4 | Host-loss recovery and sustained workload | Isolated recovery exercise and full-workflow load/storage evidence against an agreed profile | Existing USD 100 ceiling; assess costs and quotas before additional cloud resources |
| 5 | Detector revision | Resolve frequency meaning and calibration context; measure false positives, misses and coverage; freeze revised model before held-out use | Continue on consumed SCA cases 1/2/11; preserve cases 3-10 |
| 6 | Site validation and release | Authorized site inputs, operating exposure/event labels, independent review and actual release decision | Requires actual customer/domain evidence and authority |

Offline intake structural validation is now implemented and tested; [operator instructions](../runbooks/offline-intake.md). Verified permissions/calibration, registry-backed asset mapping and managed quarantine remain open. Local [reviewer assertion history](../runbooks/adjudication.md) is implemented and tested. Authenticated reviewers, subject-store linkage and independent evidence verification remain open. [Retention planning and read-only inventory](../runbooks/retention-planning.md) are implemented and tested on synthetic databases. Live metadata migration, hold/dependency integration and an authorized deletion executor remain open. Next is recovery/workload evidence and component integration. A useful shadow-pilot system needs this regardless of which detector ultimately qualifies. Progress on platform/application engineering does not promote an unqualified detector.

## Current evidence

- [139-test software run](../governance/evidence/reconciliation-tests.xml); one existing dependency deprecation warning. This is the latest recorded full-suite result, not a fresh test run for this documentation update.
- [Candidate disposition](../data/qualification/detector-candidate-disposition.md): NOT_PROMOTED.
- [Causal replay](../data/qualification/causal-observation-development.md): 428 decisions preserved; false positives unchanged.
- [Customer demonstration package](../customer/09-customer-pilot-package.md): prepared for guided review, not live customer acceptance.

Owner: Dr. Moore / engineering. Return implementation and verification evidence to the [execution handoff](../customer/08-deployment-execution.md). Keep existing standards and AI-governance records active; do not treat this backlog as a gate approval or new spending authorization.

Local integration increment: [synthetic recovery exercise](../runbooks/local-pilot-exercise.md) passed for 1,000 windows and 1,100 restored review rows. Runtime/API integration, sustained workload and actual host-loss recovery remain open.

Requirement-directed increment: [daily fleet reconciliation](../runbooks/daily-reconciliation.md) implements local PULSE-NFR-002 logic. Live scheduling and persisted-result metadata remain open. PULSE-NFR-005 one-hour RPO is not established by daily host-local backups; off-host backup automation and measured accepted-record reconciliation remain required.

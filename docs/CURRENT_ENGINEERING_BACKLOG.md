# Current engineering backlog

Current position: Phase 8 engineering and ongoing Phase 9 review; Phase 10 demonstration prepared, not accepted. Owner: Dr. Moore / engineering. No production gate is promoted.

| Priority | Remaining work | Current evidence and boundary |
|---|---|---|
| 1 | Capacity and persistence | Follow [capacity status](CAPACITY_STATUS.md). Pooling/serialization are local experiments; daily capacity and production integration remain unqualified. |
| 2 | Recovery and operations | [Blob recovery](../governance/evidence/blob-container-recovery.json) restored 3,150 receipts locally; [three scheduled backups](../governance/evidence/azure-backup-cadence.json) observed. Complete Azure host replacement, accepted-record RPO and sustained cadence remain open (PULSE-NFR-005). |
| 3 | Identity and workflow | [Read-only identity check](../governance/evidence/azure-identity-readonly.json): Review available, Close absent. Real nonempty review/closure recovery and reviewer authority remain unverified. Immutable-record writes require appropriate authorization. |
| 4 | Intake and retention | [Intake](../runbooks/offline-intake.md), [adjudication](../runbooks/adjudication.md) and [retention inventory](../runbooks/retention-planning.md) implemented locally. Actual rights/calibration, registry mapping, quarantine, hold/dependency integration and authorized deletion remain open. |
| 5 | Detector qualification | Follow [detector status](../data/qualification/DETECTOR_STATUS.md). Preserve failed outcomes and held-out data. Infrastructure progress does not resolve missed bearings or nuisance alerts. |
| 6 | Customer release | Actual operating exposure, data rights, independent review and ORR/CAR remain site-dependent; fictional sign-off is not acceptance. |

Daily fleet reconciliation (PULSE-NFR-002) is deployed; automatic deadline compliance remains unobserved. The USD 100/month ceiling remains a boundary, not measured total cost or authorization for new resources.

Latest full-suite record remains [174 tests](../governance/evidence/application-recovery-tests.xml); subsequent focused checks are reported separately. [Local recovery](../runbooks/local-pilot-exercise.md) includes synthetic process/container/Kubernetes recovery and selected network-policy paths, not complete cloud availability qualification.

Use [project status](../PROJECT_STATUS.md), [engineering review](ENGINEERING_REVIEW.md) and [execution handoff](../customer/08-deployment-execution.md). Earlier plans and their inherited conditions are preserved in [backlog history](engineering-backlog-history.md). Do not execute superseded next steps from historical entries without checking this current backlog.

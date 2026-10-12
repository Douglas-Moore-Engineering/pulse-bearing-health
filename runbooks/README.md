# Planned Operational Runbooks

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

| Trigger | Accountable role | Proposed response | Closure evidence |
|---|---|---|---|
| Missing/corrupt/stale observations | Reliability + DME technical owner | Mark unavailable; quarantine; manual rounds; diagnose source; revalidate before healthy status | Negative fixtures, disposition and recovery tests |
| Bad model/policy release | IT release owner + reliability | Withdraw advisory version; restore last approved digest; retain evidence and manual workflow | Timed rollback and exact manifest match |
| Platform failure | IT service owner | Declare incident; recover dependencies and accepted data; reconcile missing records | RTO/RPO exercise with actor/time and completeness |
| Security/data-rights incident | IT/security/rights owner | Safely contain access, preserve minimal evidence, assess notification obligations; no unsolicited external messages | Authorized incident disposition and re-entry review |
| Drift or material change | Dr. Moore proposes; owner authorizes | Reopen affected data/model/security/cost gates; no self-promoting retraining | New frozen evidence and version-bound approval |
| Retirement/transfer | Service/sponsor/rights owner | Settle customer export, access, retention/holds, deletion and dependencies before exit | Reviewed plan and executed evidence later |

These are procedures to detail and exercise before operation, not evidence that controls work. Support after Year 1, response windows and actual operator competence remain unresolved.

## Implemented reference procedures

[Reference operations](reference-operations.md) records the deployed asset controls, health/backup timers, successful manual off-host restore and unresolved host-loss/retention conditions. The earlier table remains the broader planned production lifecycle.

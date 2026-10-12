# Local reviewer assertions

[AdjudicationLedger](../src/pulse/adjudication.py) stores local review history in SQLite. Use a restricted, ignored path and one ledger per authorized review scope. This component is not exposed through the API and does not implement tenant authorization or authenticated reviewer identity.

Call `append(subject, reviewer, outcome, rationale, evidence, supersedes=None)` with a stable alert/evidence subject ID. Allowed outcomes are `confirmed_fault`, `nuisance` and `unresolved`. Resolved assertions require at least one nonblank evidence reference; references are not fetched or verified. Reviewer names are supplied assertions, not authenticated identities. Use synthetic values for demonstrations.

The first review creates a subject history. Subsequent reviews must explicitly supersede the latest record for that same subject. Corrections receive a new UUID and server-generated UTC recorded time. Missing originals, cross-subject corrections, stale branches and duplicate initial histories are rejected. Transactions serialize updates. `history(subject)` returns every revision, including the original rationale and evidence. Call `close()` when finished.

SQLite triggers reject in-place updates and deletion through normal SQL. This is append-only application behavior, **not tamper-proof storage**: a database/file administrator can alter the schema or bytes. No signed audit chain, independent evidence verification or release authorization is claimed. Subject existence in the deployed alert store is not checked; integrating that store and authenticated reviewer roles remains future work.

Four synthetic tests cover correction durability after reopening, stale/cross-subject rejection, evidence requirements and direct update/delete rejection. The complete suite passed [119 tests](../governance/evidence/adjudication-tests.xml), with the existing dependency deprecation warning. No actual reviewer outcome, customer data or external notification was created. Detector qualification remains unchanged.

Trace: PULSE-FR-003, AIG-REQ-001. Next implementation work is retention planning on synthetic databases; live review records must not be deleted by an inferred retention action.

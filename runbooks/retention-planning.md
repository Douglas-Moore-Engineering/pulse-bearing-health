# Read-only retention planning

[Module](../src/pulse/retention.py) provides `inventory_sqlite(path)` and `plan(records, as_of, retention_days)`. These functions contain no delete or export operation. No live database was accessed for this increment.

Inventory opens an existing SQLite database in read-only mode and returns table names and row counts without payload contents. Missing files are rejected, not created. Table names may themselves be sensitive; keep results within the authorized workspace. Every inventoried table remains RETAIN because a count cannot establish per-record retention eligibility.

Planning requires unique record IDs, timezone-aware creation timestamps, explicit hold status, review resolution, dependency clearance and verified-export status. Unknown or missing protection metadata retains the record. Future timestamps and timestamps at or after the retention cutoff retain it. Old records with all supplied conditions clear become ELIGIBLE_FOR_OWNER_REVIEW, never deletion-authorized. Boolean assertions are caller-supplied and are not independently verified by this function.

Retention days are explicit input: no customer policy or live cutoff has been invented. `api_assessments` does not currently have a dedicated insertion timestamp; do not substitute a vibration acquisition timestamp or fabricate a creation date. A future migration must preserve existing records with unknown age, map evidence/review dependencies and enforce holds before any actual removal. Adjudication history remains append-only.

Ten synthetic tests verify unknown protections, cutoff/future dates, duplicate identities and database byte preservation during read-only inventory. [Full suite: 129 passed](../governance/evidence/retention-tests.xml), with the existing dependency warning. This verifies planning behavior, not operational retention, export integrity, freed disk space or production capacity. Operator-approved policy, verified exports, dependency integration and any destructive executor remain unimplemented.

Trace: PULSE-FR-003, AIG-REQ-001. Next work: recovery/workload evidence and integration of these local components with governed identity and storage boundaries.

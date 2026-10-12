# Daily fleet reconciliation

Trace: PULSE-NFR-002 / VV-014. The local reconciler reports every configured asset as PRESENT_BY_DEADLINE, LATE, MISSING or PENDING. It uses explicit persisted-result timestamps and an IANA plant timezone. Future receipts cannot satisfy an earlier reconciliation. Day boundaries use local calendar days, including daylight-saving transitions.

Run `python scripts/reconcile_daily_fleet.py INPUT.json`. The input object has `day` (YYYY-MM-DD), `plant_timezone`, `assets` (unique asset IDs), `as_of` (offset-aware timestamp), and `records` containing `asset_id`, `observed_at`, `persisted_at`. Input is bounded to 4 MiB. Output includes configured asset identifiers; keep actual customer inventories in restricted storage, not Git.

Implementation assumption: the service reconciles the preceding local calendar day by 06:00 the following day. One persisted result establishes presence only, not complete expected-window coverage. Plant timezone and cadence need an actual site agreement. The fictional 12-asset fleet is exercised by tests; fleet size is configurable.

This is implemented and tested locally, not deployed or scheduled. A trusted persisted-result inventory, scheduler, durable report storage and failure monitoring remain necessary to satisfy the full requirement. The existing API database does not yet supply authoritative persisted-at metadata for this workflow. No availability or deadline-compliance claim follows from unit tests.

[Full-suite evidence](../governance/evidence/reconciliation-tests.xml): 139 passed. Missing, late and future records, exact deadline, DST, unknown assets, duplicate assets and naive timestamps are exercised.


## Commit evidence prerequisite

New API assessment writes now record `assessment_commit_evidence` after the receipt transaction has committed. `committed_by` is an upper bound sampled after the FULL-synchronous commit, not the exact commit time. It is scoped by tenant, caller, asset and window and carries the submitted observation time. Receipt responses remain unchanged. Retries preserve original evidence; old receipts are not backfilled with invented timestamps.

The evidence write is a separate transaction: a crash between transactions can leave a durable receipt without timing evidence. Such records must remain unknown for deadline/RPO calculations. A late upper bound cannot prove that the actual commit missed the deadline. Host clock accuracy remains an operational dependency. This implementation is locally tested, not yet in the deployed image; inventory extraction, conservative deadline classification, scheduling and durable reports remain open.

[Commit evidence test run](../governance/evidence/commit-evidence-tests.xml): 141 passed. Tests cover stable retries, tenant/caller scope and absence of fabricated timing for old receipts. No RPO or live scheduler acceptance is claimed.


## Read-only database integration

Run `python scripts/reconcile_receipt_database.py --database PATH --config CONFIG.json --output REPORT.json`. Configuration supplies tenant, caller, day, plant_timezone, assets and as_of. It is bounded to 64 KiB. The output must not already exist; use a restricted directory for actual identifiers. The reader uses a read-only transaction and joins evidence on the complete tenant/caller/asset/window key. It never creates missing database files or backfills records.

Post-commit bounds after the deadline produce TIMING_UNCERTAIN, not a proven late commit. Legacy receipts without observation/commit metadata produce TIMING_UNKNOWN; the relevant day cannot be established. PRESENT_BY_DEADLINE means at least one qualifying receipt, not complete sensor coverage.

The existing private backup was exercised for two synthetic reference assets; both correctly reported TIMING_UNKNOWN. This is not a 12-asset fleet or live scheduler run. [Measured result](../governance/evidence/database-reconciliation-exercise.json). Full suite: [143 passed](../governance/evidence/database-reconciliation-tests.xml). Scheduler deployment and durable automatic reporting remain open.


## Azure deployment ? 2026-10-12 UTC

The commit-evidence image and database reader are now deployed. A host systemd job runs at 05:55 and 06:00 America/New_York, using an explicitly fictional 12-asset configuration. Reports persist under `/var/lib/pulse-ops/reconciliation` with restricted permissions and a 366-day file-count bound; reaching the bound fails for operator disposition. Latest/day reports are replaced atomically. Host health checks flag stale reports or failed service execution; this does not send an external notification or monitor sensor completeness.

The manual service execution passed and persisted [the fleet report](../governance/evidence/azure-reconciliation-report.json). Historical synthetic assets remain TIMING_UNKNOWN; absent fictional assets are explicitly MISSING. A new authenticated fixture produced a commit-evidence row, recovered in the private backup alongside 3,150 receipts. [Rollout evidence](../governance/evidence/azure-reconciliation-rollout.json) and [backup evidence](../governance/evidence/reconciliation-post-rollout-backup.json).

Timer enabled; first scheduled run has not yet been observed. Manual execution does not prove timely automatic execution. One-hour RPO, real fleet coverage and production acceptance remain open. Host-local report storage is not off-host disaster recovery. No additional paid resources were created. Rollback manifests are preserved in `/home/pulseadmin/pulse-before-reconciliation` on the VM.

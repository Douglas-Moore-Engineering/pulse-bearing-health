# Explicit incident disposition

The existing AlertLedger now supports durable OPEN, ACKNOWLEDGED and CLOSED incident states. This is locally implemented and tested; no closure endpoint is deployed.

Detector false/unavailable states never invoke closure. Acknowledgement does not close an incident. Closure requires a previously acknowledged event, an explicit actor, rationale and nonempty bounded evidence references. Lookups and closure operations scope the event by tenant and asset. An identical closure retry is idempotent; changed closure content is rejected. Database triggers prevent ordinary update/delete of closure rows, not privileged database tampering. A new episode creates a new open event rather than rewriting a closed one.

The integrating service must authenticate the actor, enforce a closure permission and validate subject ownership before calling this component. Actor strings and references alone do not prove authority, actual maintenance, physical recovery or independent review. The current implementation deliberately has no automatic reopen or correction path; those need explicit audited transitions before customer use.

[Tests](../governance/evidence/incident-lifecycle-tests.xml): 168 full-suite tests passed. Cases cover acknowledgement prerequisite, explicit closure, retry/restart persistence, changed closure rejection, tenant/asset isolation, required evidence and immutability. Synthetic detector clearing does not close the separate incident. Existing reference API behavior and deployed image remain unchanged.

Next integration work is an authenticated closure route with an explicit role and audit trail, followed by backup/restore tests containing closure records. Do not infer production detector qualification from lifecycle behavior.


## Authenticated route integration

Locally implemented `POST /v1/reference/alerts/{event_id}/close` requires the normal assessment authorization, Pulse.Review and Pulse.Close roles, reference asset grant, caller-owned event, enabled pilot review storage and prior acknowledgement. Request accepts only rationale and evidence; caller-supplied actor fields are rejected. Actor identity is derived from tenant/object/client claims. Application identity is not a verified human reviewer.

Exact retries preserve the closure; changed dispositions return 409. Foreign events return 404, missing roles 403 and unavailable storage 503. [169-test software evidence](../governance/evidence/incident-api-tests.xml) includes authorization, spoofing, ownership, acknowledgement, restart and conflicting retry checks. These API tests inject claims; live Azure token verification for the new role is not yet performed.

Backup tooling accepts `--minimum-closures 1` and compares restored closure rows with the private backup source. It refuses to count an empty closure table as successful nonempty recovery. This increment does not assign Pulse.Close, build/deploy a new image or close a live incident. The next release needs those steps plus live scoped authorization and nonempty closure recovery checks. No model qualification or maintenance outcome is asserted.


## Reference rollout ? October 11, 2026 (Eastern)

Closure API deployed to the existing K3s VM after checksum verification and server dry run. One replica became ready. Receipt replay remained identical, anonymous assessment returned 401 and cross-asset assessment returned 403. Pulse.Close was added without removing existing roles and assigned to the reference managed identity.

Live closure returned 401 anonymously and 403 with the current token, which still carries only Pulse.Assess. Assignment is not proof of effective access; nonempty review and closure recovery remain pending. The post-rollout backup recovered existing receipts; no live incident was closed and empty closure storage is not a completed closure-recovery test. [Rollout evidence](../governance/evidence/azure-incident-closure-rollout.json), [recovery](../governance/evidence/closure-post-rollout-backup.json).

Next: repeat `verify-live-closure.py` when role claims propagate, then run the backup script with `--minimum-closures 1 --minimum-reviews 2`. Do not bypass role checks to manufacture success. Rollback metadata is preserved at `/home/pulseadmin/pulse-before-closure`. No new paid resource or detector promotion occurred.

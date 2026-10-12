# Authenticated pilot component integration

Deployed to the existing Azure reference VM on 2026-10-12 UTC. Live intake passed; review access remains pending managed-identity role propagation. Enable explicitly by passing a restricted `review_db` path and the parsed existing vibration schema as `intake_schema` to `create_app`. Defaults keep both capabilities disabled; Environment-based startup is available as described below; see the rollout result below.

- `POST /v1/intake/validate`: existing bearer verification and explicit client asset grants apply to `metadata.asset_id`. Returns structural validation with unverified permission/calibration flags. It does not persist input, resolve the bearing-to-asset mapping or verify source bytes. The existing 128 KiB API body bound is stricter than the offline CLI limit. Invalid metadata may be denied before schema validation to avoid access outside granted assets.
- `POST /v1/reference/alerts/{event_id}/reviews`: requires the existing assessment role plus `Pulse.Review`, the reference asset grant, and an existing event scoped to the same tenant and caller. Reviewer identity comes from authenticated tenant/object/client claims, never the body. App identity is not a verified human reviewer. Body fields are outcome, rationale, evidence references and optional supersedes ID.
- `GET /v1/reference/alerts/{event_id}/reviews`: applies the same role, asset and event ownership checks and returns preserved history. Unknown or other-caller events return 404. No cross-caller reviewer delegation is implemented.

Corrections append revisions; stale/cross-subject corrections return 409. SQLite failures return 503. Evidence references are not fetched and outcomes remain assertions; the routes cannot approve a detector or modify its alert decision. One connection per review request avoids sharing a SQLite connection across request threads. Reviewer-role provisioning and access design for actual human reviewers remain deployment work.

Tests exercise anonymous denial, reviewer-body spoof rejection, extra-role enforcement, caller/asset isolation, correction persistence across app recreation, stale correction rejection and intake authorization. They use an injected verifier for route isolation; existing token-verifier tests exercise signature/claim validation separately. No live identity or cloud rollout is claimed by these route tests. [Full suite evidence](../governance/evidence/pilot-api-tests.xml).

Next: deployment configuration and actual identity validation for a bounded demo, workload/recovery testing, and governed input persistence. Current production detector disposition remains NOT_PROMOTED.

## Runtime opt-in

Set `PULSE_PILOT_COMPONENTS=1`, `PULSE_REVIEW_DB=/data/assessments.db`, and `PULSE_INTAKE_SCHEMA=/app/contracts/vibration-window.schema.json` to enable the components. Missing configuration, an invalid schema or a missing/nonabsolute review directory fails startup. The image now includes only the required window schema through a narrow Docker context exception. Persistent storage and the Pulse.Review role still require deployment configuration; this increment does not assign that role. Full suite: 133 passed, one existing dependency warning.

## Prepared release bundle

The packager now accepts `--pilot-components` and explicitly enables the routes in the ConfigMap. Reviews share `/data/assessments.db` with receipts so the existing SQLite online backup includes both table sets. The default release keeps pilot components disabled; no additional volume or paid resource is introduced. This configuration has not been verified on the live host.

Prepared bundle: `outputs/reference-pilot-release/` (ignored). Public integrity metadata: [release preparation evidence](../governance/evidence/pilot-release-preparation.json). Full suite: [134 passed](../governance/evidence/pilot-release-preparation-tests.xml), one dependency warning.

Remaining rollout sequence: verify Azure authorization under the current handoff; preserve the current release and take a backup; provision the reference caller's Pulse.Review role without replacing Pulse.Assess; server-validate and deploy the bundle; exercise live authentication, asset isolation, review correction history and backup/restore of review records. Do not claim human reviewer verification from a managed-identity test. No live deployment or role assignment was performed in this increment.

## Azure rollout result ? 2026-10-12 UTC

User explicitly reauthorized Azure execution. The prepared image passed server-side dry run and rolled out with one ready replica. Both Pulse.Assess and Pulse.Review assignments are confirmed on the existing reference identity. No paid resource was added. [Release evidence](../governance/evidence/azure-pilot-rollout.json).

Authenticated assessment replay returned the original receipt; live intake validation passed, anonymous requests returned 401 and unauthorized assets returned 403. The managed-identity token currently contains only Pulse.Assess, so review access correctly returns 403. Role assignment alone is not successful live review verification. [Live check](../governance/evidence/azure-pilot-live-check.json).

Pre/post-rollout private backups restored with integrity OK, 3,149 assessment receipts, 884 reference windows and the existing acknowledged episode. [Post-rollout recovery](../governance/evidence/pilot-post-rollout-backup.json). No review records were created, so review recovery remains untested. Repeat verify-live-pilot.py after token refresh, then repeat backup/restore with review-history verification. Do not bypass the role check. The deploy script now restarts the loopback forward after pod replacement; the initial stale forward was corrected during this rollout.

Rollback manifest and release metadata are preserved on the VM in `/home/pulseadmin/pulse-release-before-pilot/`; the previous image remains locally imported. Production detector promotion and sustained daily capacity are not established.


### Propagation recheck and recovery guard

The 2026-10-12 00:09 UTC recheck still returned Pulse.Assess only; review GET correctly returned 403. Microsoft documents resource-token caching around 24 hours and no forced early refresh: https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/managed-identities-faq . Token expiry is recorded in the live evidence; expiry alone is not proof of permission propagation.

Fixed repeat verification to use the history response's `id` field when superseding an existing review. Backup verification now compares every restored review row with its private backup source and checks foreign keys. After a successful live review exercise, run `python scripts/backup_reference_receipts.py --minimum-reviews 2 --evidence governance/evidence/pilot-review-recovery.json`. This rejects an empty review table instead of claiming review recovery passed. Latest real restore still contains zero reviews, explicitly recorded as untested for nonempty review recovery. No authorization bypass or additional identity was introduced.

# Reference runtime operations

Owner: Dr. Moore. Current environment: `rg-pulse-reference`, `vm-pulse-k3s`, one K3s node, one API pod, local-path SQLite receipts. This is a reference service with no qualified degradation detector. Follow [access and deployment instructions](../infra/single-node/README.md).

## Monitor and investigate

The `pulse-health.timer` runs once per minute on the VM. Read its latest snapshot with `sudo cat /var/lib/pulse-ops/health.json`; inspect `systemctl status pulse-health.timer pulse-health.service` if it is stale. It checks API readiness, one ready replica, free host disk above the greater of 20 percent or 2 GiB, and a successful local backup within 45 minutes. These are provisional operator thresholds. It stores one current snapshot, sends no external notification and does not attest detector quality.

If unhealthy, inspect `sudo k3s kubectl -n pulse get pods,pvc`, pod events, `systemctl status k3s pulse-port-forward` and disk usage. Do not expose bearer tokens, raw request payloads or private keys in diagnostic output. Receipt writes fail rather than reporting persisted success when SQLite cannot commit. No automatic retention deletion is configured; disk-pressure response requires an explicit retention/export decision.

## Verify a reference release

Use the hash-bound package and server dry-run workflow in `infra/single-node/deploy-application.sh`. Run `/home/pulseadmin/pulse-release/verify-live-api.py` after readiness and the loopback forwarding service recover. It must establish real-token acceptance, anonymous 401, cross-asset 403 and unchanged persisted receipt. Record a failed attempt even if a retry passes. The single-replica Recreate strategy can interrupt access; no zero-downtime claim is made.

The earlier API image without asset authorization is not an eligible security-equivalent rollback. A later rollback must bind a retained package with the required controls and repeat these checks. No rollback or host-loss RTO/RPO has been qualified.

## Backup and isolated restore

`scripts/backup_reference_receipts.py` prepares an online SQLite backup, an off-host private copy and isolated integrity/receipt validation. The live database is never replaced. The user explicitly authorized the private backup/restore test after automatic approval review requested export authority. [The executed test](../governance/evidence/azure-receipt-backup-restore.json) recovered 3,149 receipts with integrity `ok`. It did not replace the live database; the off-host file has current-user-only Windows access. The script currently bounds a transfer to 50 MiB; larger databases require a reviewed backup method and storage budget. This off-host action is manual, not a scheduled disaster-recovery process. Separately, `pulse-backup.timer` runs every half hour at :00 and :30 UTC, retaining at most 48 tool-created on-host snapshots, each capped at 50 MiB. It removes only older matching snapshots in `/var/lib/pulse-ops/backups`, never primary receipts. The first scheduled-service invocation passed integrity validation; future executions and rotation have not yet been observed. Inspect `/var/lib/pulse-ops/backup-status.json` and the timer/service status. An exceeded size bound causes failure and requires operator intervention. Host loss still destroys these local snapshots.

## Identity and assets

`PULSE_ASSET_GRANTS` maps allowed application client IDs to explicit asset IDs. Environment-based startup rejects missing or malformed grants. This deployment permits only `generated-validation-bearing`, `generated-capacity-bearing` and `ims-run2-bearing1-reference`. An application role does not confer arbitrary asset access. Add actual assets only with a governed identity/data mapping; changing this configuration does not qualify a detector or authorize a site.

## Spending and retirement

No new paid monitoring service is used. The USD 100 monthly limit remains the governing ceiling, but the configured Azure budget does not stop charges. Follow the existing deallocation command when the owner intentionally suspends the demo; retained disk/IP charges continue. Do not delete resources or receipts as an inferred retirement action. Retention, transfer and destruction require an explicit owner disposition.

## Fictional reference detector and simulated inbox

The latest image enables `PULSE_REFERENCE_DETECTOR=1` and grants the existing managed-identity client access to `ims-run2-bearing1-reference`. `POST /v1/reference/assess` accepts only RMS features for that fixed benchmark profile (DS-IMS, run 2, 20 kHz, 20,480 samples, unknown native amplitude units and explicit source timestamp). The caller asserts source integrity; the preparation script verifies native hashes before replay. The frozen baseline uses the reviewed run-2 reference median. Out-of-order new windows and conflicting retries return 409; identical retries return the original receipt.

`GET /v1/reference/alerts` is the simulated maintenance inbox. `POST /v1/reference/alerts/{event_id}/acknowledge` records the authenticated reference caller's acknowledgement idempotently. Both require the reference asset grant and scope records to the tenant/caller. There is no email, SMS, webhook or real maintenance-system integration. The replay client acknowledges automatically for testing; this is not a human approval.

Replay with `python3 /home/pulseadmin/pulse-release/replay-reference-detector.py` over the existing operator SSH connection. It obtains the managed-identity token without logging it and reuses the verified feature file. Existing window IDs make repeats idempotent. The [initial cloud run](../governance/evidence/azure-reference-detector-replay.json) produced one episode from 17 flagged windows across 884 requests. The [subsequent isolated restore](../governance/evidence/azure-reference-workflow-restore.json) recovered those records and their acknowledgement. Features are benchmark research, not customer telemetry. [Fictional criteria](../config/fictional-reference-acceptance.json) remain separate from measured detector performance.


## Half-hour backup increment ? 2026-10-12 UTC

The deployed timer now runs at :00 and :30 UTC; the initial service invocation passed integrity with 3,150 receipts. It retains at most 48 tool-owned snapshots capped at 50 MiB each (2,400 MiB maximum retained snapshot payload, plus temporary files and live database). This is approximately one day at nominal cadence, not seven days. Primary receipts are never pruned by this job. Health monitoring flags backups older than 45 minutes. The installed `/usr/local/sbin/pulse-check-runtime.py` was refreshed, including reconciliation checks; updating only the release-directory copy would not update the timer's executable.

[Backup evidence](../governance/evidence/azure-half-hour-backup.json) and [installed health check](../governance/evidence/azure-half-hour-backup-health.json). Automatic cadence and full rotation have not yet been observed. Off-host export remains manual; host-loss one-hour RPO is NOT established. Next required evidence is automated off-host delivery plus accepted-record recovery reconciliation. No additional paid resources were added.


Current off-host update: [automated Blob backup](offhost-backup.md) supersedes earlier manual-only descriptions. Initial readback and isolated SQLite recovery passed; automatic cadence and host-loss RPO qualification remain open.

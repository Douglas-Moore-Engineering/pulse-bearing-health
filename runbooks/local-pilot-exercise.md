# Local pilot recovery exercises

## Current application recovery test

Run `python -m pytest tests/test_application_recovery.py -q` with the repository API and test dependencies installed. This test uses generated data only and never connects to Azure or opens the deployed receipt database.

The test creates an assessment receipt, a reference anomaly, acknowledgement, two review records including a correction, and explicit closure through the API. It takes a SQLite online backup into a separate database, checks integrity and foreign keys, and makes the source database path unavailable.

A fresh Python interpreter then opens the restored database and starts Uvicorn on an ephemeral port bound exclusively to `127.0.0.1`. An HTTP client with environment proxy settings disabled checks readiness, identical persisted receipt replay, exact review history, closure replay, anonymous rejection, cross-caller isolation and insufficient-role rejection. The listener remains bound during startup to avoid a port-selection race. Startup, requests, shutdown and the child process have explicit timeouts. The server is stopped in a finally block. The parent verifies a different process ID and successful HTTP result, then additionally checks conflicting closure rejection using the restored application.

Synthetic identity injection exists only in the test probe, `tests/recovery_process_probe.py`; it does not alter production authentication. The probe exposes no external interface and stores only temporary generated fixtures.

[Executed full-suite evidence](../governance/evidence/application-recovery-tests.xml): **174 tests passed**, one existing dependency deprecation warning. This strengthens the existing test rather than adding to the count. Fresh-interpreter startup and loopback HTTP recovery now supersede the earlier in-process/TestClient-only verification. This does not establish container startup, TLS/ingress, Entra authentication, actual Azure backup restoration, host-loss RTO/RPO, sustained capacity or detector qualification.

## Earlier component integration exercise

Run `python scripts/exercise_local_pilot.py`. It validates 1,000 generated intake windows, writes 1,000 unresolved reviewer assertions and 100 corrections, takes a SQLite online backup and restores into a separate database. Every subject history must compare equal, including UUIDs, timestamps, original outcomes and corrections; SQLite integrity must return `ok`.

Its retention dry run uses a hypothetical 2030 assessment date and 30-day policy: 900 unresolved subjects remain retained and 100 corrected subjects become review-eligible. No records are deleted; supplied export/hold assertions are fixtures.

[Recorded component result](../governance/evidence/local-pilot-integration.json): 1,100 review rows restored exactly; 262,144-byte database; approximately 6.64 seconds for sequential work and 0.118 seconds for isolated restoration/verification. Those timings exclude HTTP, authentication, realistic waveform sizes, network, Azure and prolonged disk growth, and do not establish daily capacity or an SLA.

The initial component run failed at Windows temporary-directory cleanup because SQLite context managers did not close handles. Explicit connection closure corrected that failure; evidence was emitted after successful cleanup. An initial failed-run temporary directory may remain outside the repository.

## Remaining recovery evidence

The container exercise below now verifies isolated image startup. Remaining work is recovery with the complete deployment configuration, followed by authorized recovery from an off-host backup and a complete host-replacement exercise. Review/closure recovery with real identity claims and sustained accepted-record reconciliation remain separate requirements. No production gate is promoted by these local tests.

## Opt-in container recovery

Set `PULSE_RECOVERY_TEST_IMAGE` to an existing local Pulse image, then run `python -m pytest tests/test_application_recovery.py -q`. The default test remains Docker-independent. The opt-in branch runs the restored synthetic database through the same HTTP probe inside the selected image, with no image pull, no external networking, a read-only root filesystem, dropped capabilities, no-new-privileges, 512 MiB memory and one CPU. Only the temporary synthetic fixture directory is writable; the probe mount is read-only. The image's configured non-root user is retained. The container is automatically removed on normal exit.

[Executed container evidence](../governance/evidence/container-recovery-tests.xml): one focused test passed using `pulse-api:sha256-c21a6fd0df51b1e3ca9e90a7b0b7968aab477dc4893430969ed0d854690436c2`. This includes the existing parent/process checks plus container readiness, receipt replay, corrected review history, closure replay and authorization denials. No Azure connection occurred. The synthetic probe overrides the image command and injects test identity claims; production entrypoint/environment, Kubernetes mounts, Entra, external ingress and actual off-host backups remain outside this evidence. This supersedes the earlier statement that no container startup was exercised, without qualifying host-loss recovery or production release.

### Default image startup verification

The opt-in test also starts a second isolated container without overriding the image CMD. Synthetic UUIDs and explicit asset grants configure the normal environment loader; assessment storage, reference detection, pilot reviews and the bundled intake schema are enabled against the restored database. The normal production verifier is used, with no injected claims. Readiness returned 200; anonymous and malformed bearer-token requests both returned 401 over internal HTTP. The test removes this specific container in a finally block.

The focused container test passed again with this additional coverage. The default command and environment-loading boundary are now exercised; successful Entra authentication, actual Azure configuration, Kubernetes storage/ingress and full host restoration remain unverified. Synthetic UUIDs are not cloud identities. No external network or Azure access occurred.

### Incomplete configuration rejection

The same opt-in exercise now starts two additional network-isolated containers with the normal image command: one omits `PULSE_TENANT_ID`, and the other omits `PULSE_REVIEW_DB` while pilot components are enabled. Each must exit nonzero within the test timeout, and its logs must identify the exact missing key. Both cases passed along with the valid restore/startup checks. The harness removes each identified test container in a finally block. These checks establish fail-closed startup for those two missing settings, not exhaustive configuration validation.

The local recovery sequence now covers database integrity, a fresh process, loopback HTTP, the existing non-root image, default command/configuration, authorization rejection and two startup-failure cases. The remaining recovery claims require different evidence: real identity success, Kubernetes storage/network configuration and authorized restoration from an off-host backup. Repeating synthetic startup tests cannot establish those claims.

### Rendered Kubernetes configuration compatibility

The default-command container test now obtains its environment directly from `render_single_node_manifests.py` with synthetic identity UUIDs and pilot components enabled. It uses the rendered mount path and restores the snapshot as `/data/assessments.db`, matching the ConfigMap rather than maintaining separate environment values in the test. Assessment and review storage must point to the same backed-up database.

The combined recovery and single-node manifest run passed five tests ([evidence](../governance/evidence/container-recovery-tests.xml)), with one existing dependency warning. The default command reached readiness with these settings. Existing manifest checks cover single-writer/Recreate deployment, persistence, non-public service and pilot configuration. This verifies local image/configuration compatibility; it does not validate Kubernetes scheduling, PVC provisioning, probe execution by kubelet, NetworkPolicy enforcement or actual cloud identity. No manifest was deployed or cloud account accessed.

## Local Kubernetes PVC exercise

Run `python scripts/exercise_local_kubernetes_storage.py --output outputs/local-kubernetes-storage.json`. The script is restricted to the `docker-desktop` context and refuses a non-loopback endpoint. It creates a uniquely named temporary namespace with restricted pod security, a 16 MiB PVC and non-root pods using an already-cached utility image (`imagePullPolicy: Never`). A writer stores a generated marker, is deleted, and a replacement reader must recover the identical marker. The temporary namespace is removed before successful evidence is emitted; failures return nonzero.

[Executed evidence](../governance/evidence/local-kubernetes-storage.json): PASS, including namespace cleanup. The local node ran Kubernetes v1.31.1; its `standard` storage class uses the rancher.io/local-path provisioner. The initial attempt and diagnostic rerun timed out because the utility image lacked `sync`, despite successful volume provisioning and pod startup. The corrected test uses shell built-ins and passed. It tests pod replacement, not power-loss durability, SQLite application recovery or Azure host recovery.

The local Kubernetes node does not cache the Pulse image. Therefore the previous Docker image/application recovery test and this Kubernetes PVC test are separate evidence; their combination is not an end-to-end Pulse Kubernetes recovery claim. No image was pulled and no Azure connection occurred.

### Full application test prerequisite

[Image-import preflight](../governance/evidence/local-kubernetes-image-preflight.json) found the verified 67,089,920-byte Pulse archive locally and confirmed its SHA-256 matches the release record. The Docker Desktop Kubernetes node uses a separate containerd image store without Pulse cached. Neither accessible Windows Docker endpoint nor Ubuntu Docker lists the node container; `kind` is unavailable and the Docker Desktop WSL command lookup did not expose `ctr`. A supported import route has not been established. This blocks only the full local application-on-Kubernetes recovery exercise; it does not invalidate the passed Docker application and Kubernetes PVC tests.

Required next action: establish the local cluster manager's supported archive-import mechanism, load the verified archive into that node, verify the exact image ID/tag, then run the application recovery exercise in a new temporary namespace. Do not remove `imagePullPolicy: Never`, publish the image, or claim the Docker cache is the Kubernetes cache to bypass this prerequisite. No host-runtime modification or Azure access occurred during this preflight.

## Pulse application recovery on local Kubernetes ? passed

The earlier image-import blocker is resolved. Docker Desktop hides Kubernetes system containers from normal listings ([Docker documentation](https://docs.docker.com/desktop/use-desktop/kubernetes/)); direct inspection of `desktop-control-plane` identified the running node. The checksum-verified archive was imported through its containerd CLI into the `k8s.io` image namespace. The image remains cached locally; no cluster reset, registry publication or Azure access occurred.

Set `PULSE_RECOVERY_KUBERNETES=1` and `PULSE_RECOVERY_TEST_IMAGE` to the verified Pulse tag, then run `python -m pytest tests/test_application_recovery.py -q`. The opt-in helper rejects non-loopback Kubernetes endpoints. It creates a temporary restricted namespace, local-path PVC and non-root Pulse pod, copies only the generated database/expectations into the PVC, deletes the first pod, and starts a replacement using the same claim. The recovered application probe verifies readiness, identical receipt replay, corrected review history, closure replay and authorization denials over internal HTTP. Namespace removal is required for success.

[Executed evidence](../governance/evidence/kubernetes-application-recovery-tests.xml): one focused test passed, one existing dependency warning. The first run failed during namespace cleanup; the corrected test uses one-second termination grace for its sleeping helper pods and consistent bounded command timeouts. The complete rerun passed including Docker checks and cleanup.

This joins application and actual Kubernetes PVC recovery evidence using synthetic identities. The Kubernetes pods override the image command to run the test probe; default-command compatibility was verified separately in Docker. Production deployment rollout/probes, external ingress, successful Entra tokens, real Azure backups and host-loss RTO/RPO remain unqualified.

### Rendered Deployment recovery ? passed

The local Kubernetes helper now follows the synthetic workflow probe with the renderer's Deployment, ConfigMap, ServiceAccount and ClusterIP Service. Only the namespace and PVC claim reference are adapted to the isolated exercise. The image command, environment, security settings and startup/readiness/liveness probes come from the rendered configuration. The restored snapshot is copied using SQLite backup to the configured `/data/assessments.db`.

The test waits for rollout, checks live/readiness endpoints, anonymous-request rejection, SQLite integrity and the restored receipt count, deletes the application pod and repeats verification after rollout with a different pod UID. The complete focused exercise passed in 63.30 seconds, including namespace cleanup and existing Docker checks. This duration is the test harness runtime, not a production recovery-time measurement. [Updated evidence](../governance/evidence/kubernetes-application-recovery-tests.xml).

Default-command Deployment recovery and kubelet readiness are now exercised on local Kubernetes. NetworkPolicy is deliberately absent from this isolated exercise, and Service routing, ingress, successful Entra authentication, actual Azure backup restoration and host-loss RTO/RPO remain unverified. Successful synthetic workflow replay still uses the separate injected-identity probe; it is not a real Entra authorization result.

### Kubernetes Service DNS and routing ? passed

The recovery exercise now creates a separate temporary client pod after Deployment replacement. It resolves `pulse-api.<temporary-namespace>.svc.cluster.local` and compares the resolved address with the Service ClusterIP. Through both the DNS name and ClusterIP it requires live/readiness HTTP 200 and anonymous alert-inbox HTTP 401, with environment proxies disabled. The complete focused test passed in 66.75 seconds, including cleanup; this is harness duration, not an RTO or capacity result. [Updated evidence](../governance/evidence/kubernetes-application-recovery-tests.xml).

Service DNS/routing is now exercised locally. The test namespace intentionally has no NetworkPolicy; deny enforcement, external ingress, real identity and Azure host restoration remain separate open checks.

## Local NetworkPolicy ingress check ? passed

Enable `PULSE_VERIFY_NETWORK_POLICY=1` alongside the Kubernetes recovery options; set `PULSE_NETWORK_POLICY_EVIDENCE` to a desired JSON evidence path. After baseline Service connectivity succeeds, the helper applies the renderer's unchanged NetworkPolicy in the temporary namespace, waits five seconds, and makes three fresh client-to-Service requests with bounded timeouts. All three must fail while the target's in-pod health and restored-receipt checks still pass. Namespace cleanup remains mandatory.

[Observed network evidence](../governance/evidence/local-network-policy.json) and [focused test](../governance/evidence/local-network-policy-tests.xml): PASS. Three requests returned connection errors after policy application; baseline routing and subsequent target health passed. One focused test passed with one existing dependency warning. The test observed connection errors, not packet-level drop logs. Its scope is the same-namespace client-to-API-Service ingress path only; egress allowances/denials, other traffic paths, external ingress and Azure enforcement remain unverified. This supersedes the earlier statement that no NetworkPolicy was applied for this opt-in run. No Azure access occurred.

### Local outbound restriction and DNS ? passed

The policy exercise now starts a temporary HTTP target on TCP 8080 and proves it is reachable from the API before applying policy. After application, three API-to-target attempts timed out while an unrestricted client still reached the target. The restricted API also resolved the Service DNS name to the correct ClusterIP. The existing ingress, recovery and cleanup checks passed in the same run.

[Network evidence](../governance/evidence/local-network-policy.json) and [focused test](../governance/evidence/local-network-policy-tests.xml) record PASS: one focused test, one existing dependency warning, 96.64 seconds total harness runtime. The outbound result is specific to a local pod-IP destination on TCP 8080. It does not prove private-address exclusion on TCP 443, public HTTPS allowance, every DNS transport, external ingress or Azure enforcement. Temporary resources were removed; no Azure access occurred.

### Private TCP 443 exclusion ? passed

The local outbound target now listens on both TCP 8080 and TCP 443. A pod-scoped unprivileged-port setting permits its non-root process to bind 443; no host setting changes. Both ports were reachable from the API before policy and from an unrestricted pod afterward. Three restricted requests per port timed out after applying the rendered policy; DNS and the existing ingress/recovery checks also passed. Port-specific attempts and the target pod IP are retained in [network evidence](../governance/evidence/local-network-policy.json).

The [focused run](../governance/evidence/local-network-policy-tests.xml) passed with cleanup: one test, one existing dependency warning. This tests private pod-IP exclusion on TCP 443, which differs from excluding a disallowed port such as 8080. Traffic on port 443 was plaintext HTTP, not TLS. It does not establish every excluded CIDR, public HTTPS allowance, successful Entra authentication or Azure network enforcement. No Azure access occurred.

### Public HTTPS allowance ? passed

Set `PULSE_VERIFY_PUBLIC_HTTPS=1` to opt into one public request from the restricted API pod after policy application. The probe resolves `docs.python.org`, requires global addresses, disables proxies and redirects, uses the default trusted TLS context, requires HTTP 200 from `https://docs.python.org/3/`, and samples only 1 KiB of response data. The opt-in is disabled for ordinary offline tests.

The combined recovery/network exercise passed, including cleanup; [network evidence](../governance/evidence/local-network-policy.json) records DNS addresses, certificate verification and HTTP status. The full offline suite was refreshed separately: 174 passed with one existing dependency warning. This establishes one public HTTPS path alongside the tested private TCP blocks and DNS allowance. It does not establish all public destinations, successful Entra authentication, Azure network enforcement or host-loss recovery. No Azure access occurred.

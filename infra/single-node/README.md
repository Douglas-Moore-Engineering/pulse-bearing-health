# Single-server Kubernetes budget evaluation

## Current deployed configuration

The user raised the budget to USD 100/month. The live host is **Standard_D2as_v6 in East US 2 zone 1**, with 8 GiB RAM, 2 vCPUs, one 32 GiB P4 OS disk and Standard IPv4. [Updated cost evaluation](budget-100-evaluation.json) estimates USD 80.4253 over 744 hours including 50 GB charged egress; taxes and unexpected consumption draw on the USD 19.5747 reserve. The existing budget named `pulse-monthly-50` now tracks 100. The preceding B-series plan below is historical and was not deployed.

Run `./infra/single-node/Connect-Reference.ps1` from this checkout to open the private SSH tunnel, then view `http://127.0.0.1:18080/health/ready`. Only the operator address recorded in the NSG may connect; update that /32 deliberately if your workstation address changes. The key lives in ignored `outputs/private/pulse-deployment/operator.key`; do not commit or share it. Assessment calls require a Pulse Entra application token. The assigned managed identity currently resides on the VM; the supplied `verify-live-api.py` exercises that path without logging tokens.

Live checks passed: one Ready API pod, Bound PVC, real Entra authentication, anonymous 401, and unchanged persisted receipt following pod restart. Ports 80, 8000 and 6443 were unreachable from the workstation. Host configuration is in [host.bicep](host.bicep); [K3s installation](install-k3s.sh) pins and checksum-checks the official binary; [application rollout](deploy-application.sh) verifies release hashes and runs Kubernetes server-side validation. No qualified model or notification integration is deployed.

**Deployment order:** foundation, host, K3s, application. Reapplying the foundation NSG definition removes its later SSH child rule; reapply the host template to restore the operator rule. Do not deploy the historical AKS template. Stop paid compute with `az vm deallocate --resource-group rg-pulse-reference --name vm-pulse-k3s` when intentionally suspending the demo; disk and IP charges continue. Deletion requires an explicit retention/cleanup decision and is not part of this runbook execution.


Proposed demo configuration, 2026-10-11. User requested evaluation within **USD 50/month**. This is self-managed K3s on an Azure VM. It is not an AKS deployment, high-availability service or qualified bearing alert system.

The [machine-readable evaluation](evaluation.json) reserves one B2als_v2 VM (2 vCPU, 4 GiB), one 32 GiB E4 SSD, one Standard IPv4 address and one application replica. No node or pod autoscaling, managed registry, load balancer, NAT gateway, paid log ingestion or training compute is included. The existing private image would be transferred over restricted SSH and imported into containerd. Kubernetes API and application access would use an operator tunnel; only SSH from the operator's specific address would be allowed inbound. Identity checks remain required. No operator address or identity is invented here.

| Component | Conservative 31-day service estimate |
|---|---:|
| B2als_v2 Linux, 744 hours at $0.0376 | $27.97 |
| E4 LRS disk | $2.40 |
| Disk mount allowance | $0.26 |
| E4 transactions at 43,400 billable/hour and $0.002/10,000 | $6.46 |
| Standard IPv4, 744 hours at $0.005 | $3.72 |
| 50 GB outbound at $0.087/GB, no free allowance assumed | $4.35 |
| Service total | **$45.16** |
| Remaining for taxes and contingency | **$4.84** |

Rate evidence: [compute](../../governance/evidence/budget-50-alternative-prices.json), [disk/IP](../../governance/evidence/budget-50-storage-network-prices.json). Select product `Virtual Machines Basv2 Series`; the API also returns differently priced Cloud Services, which this estimate excludes. [Microsoft bandwidth pricing](https://azure.microsoft.com/en-us/pricing/details/bandwidth/) supplies the outbound rate. [Microsoft's storage explanation](https://techcommunity.microsoft.com/blog/azurestorageblog/understanding-the-standard-hdd-io-unit-size-update-and-what-it-means-for-your-wo/4499128) supplies the E4 transaction cap. This is an engineering estimate, not a quote or enforced billing cap.

B2s was also evaluated: $0.0416/hour, but Azure reports `NotAvailableForSubscription` for East US 2. B2as_v2 with 8 GiB costs $55.95 for compute alone over 744 hours and is excluded. [Live SKU inspection](../../governance/evidence/budget-50-availability.json) also reports B2als_v2 and B2as_v2 as `NotAvailableForSubscription` throughout East US 2. Regional quota has 10 free vCPUs; the Basv2 family quota was absent from the returned list and is unverified. This region is blocked for all three evaluated candidates. Another region requires fresh SKU, quota, pricing and policy review.

[K3s requires at least two cores and 2 GB RAM](https://docs.k3s.io/installation/requirements), before application overhead. [B2als_v2 uses CPU credits and has a 30% baseline](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/basv2-series). Six-hour peak tests must include depleted credits. Workstation results do not establish this VM's capacity. One server loses both control plane and application during host failure or maintenance.

Deployment remains disabled until SKU/quota, subscription policy charges, tax headroom, operator access and identity are resolved, and traffic enforcement is implemented. A 50 GB egress allowance is a planning limit, not a deployed control. Budget notifications alone cannot enforce $50. This demo omits durable alert delivery, paid backups and model training; detection remains explicitly unavailable until qualified. The existing 1.5-million/day requirement and DME release gates remain open.

## Executed Azure foundation

The resource group `rg-pulse-reference` and monthly tracking budget `pulse-monthly-50` now exist in Azure. [Foundation source](foundation.bicep) reproduces them and defines the isolated VNet/NSG increment. [Deployment evidence](../../governance/evidence/azure-foundation-deployment.json) records the successful initial deployment. This does not create a Kubernetes host. The broader [B2s regional inspection](../../governance/evidence/azure-b2s-regional-availability.json) shows location restrictions throughout normal US regions. Denmark East and India South Central returned 10 free regional and B-series vCPUs but no matching retail rate; neither is approved as affordable. East US also restricts B2als_v2 and has zero Basv2 quota.

The network increment has now deployed successfully: `vnet-pulse-reference` (`10.87.0.0/16`), `kubernetes-demo` (`10.87.1.0/24`) and `nsg-pulse-reference`. Inbound traffic is denied; default outbound access is disabled. [Network verification](../../governance/evidence/azure-network-verification.json) records the subnet and NSG association. This is a network foundation only; a future host needs an explicit operator access rule and an explicitly priced outbound path before installation.

## Durable application release bundle

The generated private bundle is under ignored `outputs/reference-single-node-release-20261011/`: Docker image archive, rendered application YAML and checksum manifest. [Tracked release metadata](../../governance/evidence/single-node-release-package.json) contains no credentials or dataset bytes. Rebuild with `scripts/package_single_node_release.py`; it refuses to overwrite an existing destination. Verify both archive and YAML SHA-256 before copying/importing into a host. The image tag is derived from the Docker image ID, not a claim of registry signing. Registry scanning/signing and Kubernetes server-side validation remain unperformed.

The manifest uses one replica, Recreate updates and local-path storage with UID/fsGroup 10001. API access is via an authenticated operator's Kubernetes port-forward; there is no public ingress. The image must be imported into containerd under the generated tag because imagePullPolicy is Never. The 1 GiB PVC request is a scheduling declaration: local-path does not necessarily enforce disk quotas. No retention deletion or backup schedule is installed. Receipts share a single node and do not survive loss of that node's disk. Storage growth must be measured and a retention/backup policy implemented before sustained traffic.

Set `PULSE_ASSESSMENT_DB` to opt into durable receipts. Successful writes return persisted=true only after the transaction commits; exact retries return the same saved result, and changed content under the same tenant/caller/asset/window returns HTTP 409. Storage failures return HTTP 503. This is assessed with generated fixtures, not cloud load. The default AKS configuration remains stateless; do not attach this SQLite store to the three-replica AKS deployment.

The actual API audience and reference caller IDs are in [identity configuration](identity-config.json). App-role assignment is [verified](../../governance/evidence/azure-reference-caller-role.json); token acquisition still requires the managed identity to be attached to a deployed host. No secret or broad Graph permission was created. No qualified degradation model is enabled and no notification is sent.

## Short live capacity experiment

[Live results](../../governance/evidence/azure-live-capacity.json) measure two 20-second VM-local scenarios at 17.4 and 70 requests/second, 4,096 samples/request, with real Entra tokens and committed SQLite receipts. They do not exercise external client networking, qualified inference, notifications, six-hour sustained load, host failure or daily capacity. The [initial failed-fixture run](../../governance/evidence/azure-live-capacity-initial-invalid-fixture.json) is preserved: its 17.4-stage window IDs contained a disallowed decimal point; the generator was corrected and both stages rerun.

## Asset controls, monitoring and recovery update

The deployed release is now recorded in [asset authorization evidence](../../governance/evidence/azure-asset-authorization.json). Environment startup requires `PULSE_ASSET_GRANTS`; only the two generated reference assets are permitted. Actual token tests produced 403 for an unassigned asset, 401 without a token and unchanged durable replay after rollout. The original diagram remains a view of the main assessment path; it does not describe these supporting timers in detail.

`pulse-health.timer` runs every minute and checks API/replica/disk and local-backup freshness. `pulse-backup.timer` runs daily at 03:00 UTC, retaining seven snapshots capped at 50 MiB each. These are same-host backups. The explicitly authorized manual off-host backup restored 3,149 receipts with integrity ok. See the [operations runbook](../../runbooks/reference-operations.md) for scope, limits and response. This is not tested host-loss RTO/RPO, qualified detector service or six-hour capacity evidence.

## Deployed fictional detector workflow

[Latest release and real benchmark replay](../../governance/evidence/azure-reference-detector-replay.json) add an explicitly unqualified `/v1/reference` detector, simulated maintenance inbox and authenticated acknowledgement. The asset grant also includes `ims-run2-bearing1-reference`; generated assets retain their original assessment behavior. The original degradation route still reports qualified detection unavailable. See the [operations runbook](../../runbooks/reference-operations.md) and [workflow view](../../docs/diagrams/17_reference_detector_workflow.svg). The post-integration [restore test](../../governance/evidence/azure-reference-workflow-restore.json) includes the event and acknowledgement. No external alert was sent and no additional paid service was created.

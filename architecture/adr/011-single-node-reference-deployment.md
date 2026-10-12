# ADR-011: Single-node Azure reference deployment

Implemented 2026-10-11; production/model acceptance remains blocked. Supersedes ADR-010's deployment selection for the isolated reference only. Trace: PULSE-NFR-001/003/004, PULSE-SR-002/003 and AIG-REQ-001/003.

Dr. Moore raised the authorized ceiling to USD 100/month after the USD 50 alternatives failed quota/allocation checks. Deploy one Standard_D2as_v6 VM in East US 2 zone 1, Ubuntu 24.04, a 32 GiB P4 disk and Standard IPv4. The 744-hour service estimate is USD 80.4253 including 50 GB charged outbound traffic, leaving USD 19.5747 for taxes/contingency. This is a forecast, not a billing cap. VM family/regional quota both had 10 free vCPUs; zone 1 had no listed restriction and actual deployment succeeded.

The VM hosts pinned K3s v1.37.1+k3s1 and one restricted non-root API pod. A local-path PVC stores SQLite receipts with a Recreate deployment strategy. Only SSH from the operator's inspected /32 address is admitted by the NSG. Application access uses a loopback Kubernetes port-forward, not public HTTP ingress. A user-assigned managed identity has only the Pulse.Assess API role; the live Entra token, anonymous denial and receipt survival across a pod restart were verified with generated data.

Tradeoffs: no host/zone redundancy, local disk is not a backup, storage retention and capacity are unqualified, no asset-level authorization or operational notification integration, and no qualified degradation model. A PVC request does not enforce local-path disk capacity. The 1.5-million-request daily target remains unverified. No production or model gate is approved by this deployment.

Evidence: [host](../../governance/evidence/azure-host-deployment-verified.json), [live API](../../governance/evidence/azure-api-live-verification.json), [runtime](../../governance/evidence/azure-kubernetes-runtime.json), [cost](../../infra/single-node/budget-100-evaluation.json), [runtime view](../../docs/diagrams/16_deployed_reference_runtime.mmd).

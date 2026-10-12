# ADR-010: bounded AKS runtime for degradation assessment

## Current budget decision ? 2026-10-11

Dr. Moore authorized **USD 50/month** for Pulse. [The recorded budget](../../governance/cloud-budget.json) supersedes earlier statements that the ceiling was missing. The six-node AKS proposal is unaffordable and disabled in its deployment script before any Azure call. Its $1,213.62/month partial minimum is retained as rejected sizing evidence. No paid resources were created. Azure budget alerts are not a billing hard cap. A replacement must fit the full service estimate and undergo capacity validation; 1.5 million daily degradation alerts remains an unproven requirement.


Status: proposed; local application implementation exercised, infrastructure not deployed. Owner: Dr. Moore. Date: 2026-10-11.

The user requests Kubernetes and 1.5 million daily bearing-degradation requests with a 09:00-15:00 peak. The existing SQLite reference harness is single-operator and cannot be shared as a replicated service.

Propose a stateless authenticated API on private three-zone AKS Standard, separate from the AzureML foundation. Standard is selected over the skill's Automatic default to specify dedicated system nodes and explicit user-pool maxima during cost review. Automatic offers managed provisioning and should be revisited after quota/cost and availability assessment. Container Apps would reduce cluster operations but does not satisfy the user's explicit Kubernetes deployment choice. A shared SQLite volume is rejected for this API; durable evidence/outbox must be a separately tested concurrent service.

Keep the private control plane and internal TLS Gateway until an external exposure requirement is supplied. Entra application roles and caller allowlists guard assessment access. No trained model is qualified, so the implementation abstains rather than manufacturing degradation alerts. Native data qualification remains separate from API scaling.

Consequences: operational and minimum-node costs, private management/build connectivity, quota and SKU restrictions, certificate/identity setup, durable storage and notification work. The compiled foundation is not sufficient to establish an alert product. The six-hour workload, bursts and per-pod limits require cloud measurement.

Trace: PULSE-NFR-001/003/004/005, PULSE-SR-002/003, AIG-REQ-001/002/003 and PULSE-COST-REQ-001. Review triggers: user workload correction; measured latency/CPU; actual quota and regional availability; full cost and spending disposition; required public exposure; alert/model qualification.

See [capacity and evidence](../../docs/AKS_CAPACITY_AND_RELEASE.md) and [deployment runbook](../../infra/aks/README.md).

# Kubernetes capacity and release increment

## Current budget decision ? 2026-10-11

Dr. Moore authorized **USD 50/month** for Pulse. [The recorded budget](../governance/cloud-budget.json) supersedes earlier statements that the ceiling was missing. The six-node AKS proposal is unaffordable and disabled in its deployment script before any Azure call. Its $1,213.62/month partial minimum is retained as rejected sizing evidence. No paid resources were created. Azure budget alerts are not a billing hard cap. A replacement must fit the full service estimate and undergo capacity validation; 1.5 million daily degradation alerts remains an unproven requirement.


Status: implementation/preflight in progress, not deployed or production-qualified. Date: 2026-10-11. Owner: Dr. Moore. Cost model: PULSE-LCC-001. User request supersedes earlier runtime planning: Kubernetes for 1,500,000 bearing-degradation requests/day, peak 09:00-15:00.

## Workload and acceptance

Daily average is 1,500,000 / 86,400 = **17.36 requests/second**. If all requests arrive in the six-hour peak, the mean during that period is **69.44 requests/second**. The actual hourly distribution, timezone, request size and alert-versus-assessment mix remain unmeasured. Local timezone America/New_York is a planning assumption only; no plant timezone was supplied. Test scenarios use 70 sustained, 174 and 350 requests/second bursts; these are engineering scenarios, not measured arrivals or user-approved peak multipliers.

The HTTP contract accepts one timestamped acceleration window of 2-4,096 finite samples, maximum body 128 KiB, and a caller-asserted source digest. Large native benchmark captures need a separately qualified windowing/ingestion pipeline. The local fixture request is about 22.8 KB; 1.5 million such requests imply approximately 34.2 GB/day ingress before protocol overhead. At the body limit the bound is 196.608 GB/day. Responses, durable evidence, retries, retention and model work are additional costs.

The provisional API target is p95 <500 ms and <0.1% failures/dropped requests at the agreed load. This is distinct from inherited PULSE-NFR-001's five-second persisted-result criterion, which is not implemented here. Three replicas and HPA 3-12 are configured proposals. Per-pod measured capacity under 500m CPU request / 1 CPU limit must determine final counts; do not multiply local workstation throughput into a production guarantee.

## What exists

- [API](../src/pulse/api.py): single-tenant Entra v2 RS256 tokens, application role/client checks, byte/sample limits, UTC validation, descriptive features, explicit unavailable alerts, internal health/metrics. No source-byte verification, durable result store or notifications.
- [AKS deployment](../infra/aks/README.md): compiled Bicep, guarded preflight/execution script, immutable-image manifest renderer, internal HTTPS Gateway, HPA/PDB, isolation and rollout settings. No cluster has been created.
- [Tests](../governance/evidence/aks-api-tests.xml): local fixture tests cover token denials, contract limits, honest abstention, startup configuration and deployment-input safeguards; no live Entra tokens or AKS controls tested.
- [Initial shared-process load](../governance/evidence/aks-api-loopback-load.json) failed; [separate-process load](../governance/evidence/aks-api-loopback-isolated.json) removes GIL contention between client/server. Retain both rather than hiding the unsuccessful result. These short loopback tests omit TLS, gateway, pod limits, network latency, persistence and qualified model inference.

## Azure preflight and cost

[Live preflight](../governance/evidence/aks-preflight.json) found no existing AKS cluster and East US 2 total regional vCPU quota 10. Kubernetes 1.36.4 is a returned non-preview version; 1.37 is preview and is not selected. The proposed minimum is six 4-vCPU nodes =24 vCPUs; maximum nine nodes plus two possible upgrade-surge nodes requires **44 free regional and family vCPUs**. [Node availability](../governance/evidence/aks-node-availability.json) reports restrictions on all six inspected alternatives; the selected D4ds_v6 is restricted in all three zones. A quota increase alone does not establish zonal allocation availability. No quota request or resource provider registration has been submitted.

The observed Azure CLI is 2.80.0; Microsoft's [managed Gateway API instructions](https://learn.microsoft.com/azure/aks/app-routing-gateway-api) require >=2.86.0. Docker Desktop was started; the image built and passed a restricted local container smoke test. Private operator/build networking, real API/caller registration IDs, private DNS/TLS and scoped role assignments remain unresolved.

[Public retail-rate evidence](../governance/evidence/aks-retail-prices.json), retrieved October 11, 2026, uses USD consumption prices for East US 2, not subscription discounts or a quote. D4ds_v6 Linux is $0.249/node-hour; Standard AKS control plane $0.10/hour; Premium ACR $1.6666/day. Using 730 hours and 30 registry days:

| Scenario | Nodes | Compute + control plane + ACR/month |
|---|---:|---:|
| Minimum pools | 6 | $1,213.62 |
| User pool at maximum | 9 | $1,758.93 |
| Two additional surge nodes, illustrative full month | 11 | $2,122.47 |

These are **partial cost floors**, not a full estimate or hard cap. Excluded/unpriced items include managed disks, load balancer/public outbound IP, private endpoint/DNS, log ingestion/retention, Defender, certificate services, connectivity/build agents, bandwidth, durable evidence/notification services and engineering/operations labor. Node maxima do not cap metered logs/network/storage. Minimum listed components alone total $14,563.44/year, leaving little of the fictional $18,000 annual envelope for missing costs; that envelope is not actual spending authorization. Keep all LCC-OPEN conditions open. Update the governed cost ledger before financial reliance or paid execution.

## Completion gates and engineering evidence

Completion requires evidence for the applicable engineering work. Standards and AI governance remain active. This increment returns implemented/tested API behavior and compiled deployment intent; it cannot pass deployment, model or site gates.

Before paid deployment: resolve actual owner spending scope, full forecast, quota/allocation, region/network/policy, client identity/TLS, image build/scanning/signing and private runner access. Then validate ARM/what-if, deploy the isolated foundation, verify managed routing, and run server-side manifest checks. No fictional approval substitutes for these results.

Before claiming bearing-degradation alerts: qualify the user-complete dataset set (LDM-UPB, IMS, Ferrara and HUST), respecting HUST's classification-only eligibility and partial Ferrara membership. Freeze partitions/event definitions, fit/evaluate baselines with false-alert and lead-time criteria, and bind an approved model/policy. Add durable idempotent evidence/outbox, asset authorization, alert suppression and authorized delivery. External messages require a designated authorized channel. No raw dataset is redistributed in this increment.

Before claiming 1.5 million/day capability: test the actual deployed alert workflow for six hours at the frozen peak distribution and payload mix, plus bursts and node/zone/identity failures, then measure costs. Verify p95, successful accepted/persisted outcomes, recovery, duplicate handling, monitoring/paging and release rollback. Maintain prior V&V requirements and return independent/site review separately. Authentication, generated fixtures and request volume alone do not establish useful degradation detection.

## Final local verification return

[Implementation evidence](../governance/evidence/aks-implementation-validation.json) records 60 passing tests, Bicep compilation and read-only Azure what-if success. [Container smoke](../governance/evidence/aks-container-smoke.json) verifies non-root/read-only execution with dropped capabilities, 1 CPU/512 MiB limits, readiness and anonymous denial. [Three-process loopback](../governance/evidence/aks-api-loopback-three-replicas.json) records the 174 requests/second scenario and failed 350 requests/second scenario. No cloud resource was provisioned; none of these results qualify detection or durable alerting.

# AKS degradation-assessment deployment

## Current budget decision ? 2026-10-11

Dr. Moore authorized **USD 50/month** for Pulse. [The recorded budget](../../governance/cloud-budget.json) supersedes earlier statements that the ceiling was missing. The six-node AKS proposal is unaffordable and disabled in its deployment script before any Azure call. Its $1,213.62/month partial minimum is retained as rejected sizing evidence. No paid resources were created. Azure budget alerts are not a billing hard cap. A replacement must fit the full service estimate and undergo capacity validation; 1.5 million daily degradation alerts remains an unproven requirement.


Status: authored and locally checked; not provisioned or cloud-tested. User target: 1,500,000 daily bearing-degradation alert requests, peak hours 09:00-15:00. See [capacity and cost](../../docs/AKS_CAPACITY_AND_RELEASE.md).

`main.bicep` creates a separate private AKS foundation, not the earlier AzureML template: Standard control plane, three system nodes, three-to-six user nodes, three zones, CNI Overlay/Cilium, Entra RBAC, disabled local accounts, workload identity support, private ACR, monitoring and Defender. Explicit pool maxima support cost review; AKS Automatic remains the managed alternative, but this proposal selects Standard to fix pool sizes and ceilings. This is an engineering proposal, not a measured production sizing result.

## Prepare and validate

1. Install the package with `python -m pip install -e ".[test,data,api,deploy]"`. Run `python -m pytest -q` and `python scripts/validate_review_package.py`.
2. Compile `main.bicep` with Bicep. Copy `execution-inputs.example.json` to an ignored local file. Record actual spending approval and complete estimate only after owner disposition. Current node-size restrictions, quota and CLI version prevent execution.
3. Run `./infra/aks/Deploy-Aks.ps1 -Inputs <local-file>` for read-only preflight. `-Execute` provisions paid resources and must only be used within actual authorization. It performs ARM validation/what-if first. Failures stop; no resources are automatically deleted. Budget numbers are recorded decisions, not a billing hard stop.
4. Before executing, establish the private operator/build-agent network route and DNS plan. An ACR private endpoint cannot be pushed from an arbitrary public runner. Validate non-overlapping network ranges, regional policy, provider registration, actual operator permissions and signed-image enforcement. The operator's role assignments are not created by this template.

## Identity and application rollout

Create or identify a single-tenant Entra API registration using v2 access tokens, application role `Pulse.Assess`, and approved caller service principals assigned that role. Set `PULSE_TENANT_ID`, `PULSE_API_CLIENT_ID`, and `PULSE_ALLOWED_CLIENT_IDS`; these are identifiers, not credentials. Use organizational workload identity or certificates for clients. The application validates issuer, audience, tenant, signature, expiry, client and role. Pod workload identity is enabled at cluster level but this stateless service needs no Azure data role or mounted service-account token.

On a private, authorized builder, build the Dockerfile, scan it, generate SBOM/signature and push `pulse-api` to the private registry. Resolve its immutable digest. Docker Desktop was started and the image built successfully; the [restricted container smoke](../../governance/evidence/aks-container-smoke.json) passed. Vulnerability scanning and registry signing/push remain unverified. Do not tag uncommitted work as an existing Git commit. Bind the actual source/package digest to the release.

Prepare a JSON file for `scripts/render_aks_manifests.py` with fields `image` (ACR repository plus `@sha256:` digest), `tenant`, `audience`, `clients` (array), `hostname`, and `tls_secret`. The renderer rejects tags and missing identities. Render to a fresh ignored output path. Create the namespaces first, then provision a valid TLS Secret in `pulse-ingress` through the approved certificate/secret-management path; no certificate is bundled here. Configure private DNS for the internal Gateway address.

From the private operator route, obtain scoped AKS credentials into a task-specific kubeconfig. Run server-side dry-run against the rendered manifests, then apply and verify Deployment availability, Gateway `Programmed`, HTTPRoute `Accepted`/`ResolvedRefs`, TLS hostname validation and Entra negative tests. Managed Gateway API requires Azure CLI >=2.86.0; the observed CLI is 2.80.0. The generator uses `approuting-istio`, not the older NGINX ingress.

The workload has three replicas, HPA 3-12, PDB minimum two, topology spreading, bounded resources, non-root read-only containers, probe endpoints, default-deny policy and an internal HTTPS Gateway exposing only POST `/v1/degradation/assess`. Metrics are internal. Internet TCP 443 is allowed for identity-key retrieval; this is not FQDN-restricted egress. Tighten and test egress via approved firewall/Cilium policy before production. Configure managed Prometheus scraping and alert rules; metrics exposition alone is not an installed dashboard or pager.

## Acceptance and recovery

The API computes RMS/kurtosis and explicitly abstains: no qualified model or threshold is installed. Caller-supplied source hashes are not native-byte verification. Responses are not durably persisted and no notification is sent. The local SQLite harness is not mounted into replicas. Implement an idempotent durable evidence/outbox store, asset authorization, qualified degradation policy, suppression/deduplication and human notification workflow before claiming an alerting product. External notification delivery requires an authorized destination/channel.

Before promotion, run representative payload mixes at >=70 requests/second for the full six-hour peak, plus agreed bursts, through private TLS and identity. Measure end-to-end p95, errors/drops, queue age once persistence exists, CPU/memory and actual cost. Exercise pod/node drain, zone loss, rollout/rollback, expired/unauthorized tokens, malformed/oversized bodies, key rotation and network failures. Cloud performance is unverified.

Rollback uses the previous verified image digest and configuration with `kubectl rollout undo deployment/pulse-api -n pulse`, then checks probes, authentication and canary responses. Do not roll back evidence schemas blindly. Cluster/registry/log deletion is a separate owner action after retention/export review; there is no automatic cleanup. Existing four-hour RTO and one-hour RPO requirements are not established by a stateless API restart.

Current Microsoft references: [managed Gateway API](https://learn.microsoft.com/azure/aks/app-routing-gateway-api), [AKS Automatic](https://learn.microsoft.com/azure/aks/intro-aks-automatic), [managed cluster schema](https://learn.microsoft.com/azure/templates/microsoft.containerservice/managedclusters).

# Azure Platform Plan — Unprovisioned

PULSE pre-Azure review v0.3 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

This is a proposed capability mapping, not IaC, deployed assets or a request to sign in.

| Logical capability | Azure candidate | Design concern |
|---|---|---|
| Experiment/model lineage | Azure Machine Learning workspace | Native experiment/registry support; no compute or endpoint required at initial setup |
| Governed input/artifact storage | Azure Storage | Identity-based access, no anonymous blobs, retention and backup policy |
| Identity and secrets | Organizational Entra identity and managed workload identity; Key Vault if needed | Least privilege, no repository keys; actual roles unresolved |
| Metrics/security observations | Azure Monitor / Log Analytics / Application Insights as justified | Avoid duplicate telemetry, establish retention and cost ownership |
| Private connectivity | VNet, private endpoints and DNS as appropriate | Inbound client access must be designed and tested; managed outbound is a separate choice |
| Resource governance | Dedicated nonproduction resource group, tags, policy and cost budget | Actual subscription, region, budget and network dependencies unresolved |

Before platform construction, establish naming, approved US region, subscription/resource group, identity/RBAC, operator network access, resource policy, logs/alerts, budget thresholds, secrets, recovery, environment separation and CI/CD/IaC approach. No actual resource name or SKU is bound to an account in this package.

Future implementation order: governed platform → data ingestion/contracts → ML experiments → application/decision layer → V&V → deployment → operational evidence. No always-on compute, registry cost or training job is approved automatically with a workspace. Validate current Microsoft service behavior and ARM schemas again when accepted configuration becomes concrete.

Microsoft references: [workspace resource reference](https://learn.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/workspaces), [managed network](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-managed-network?view=azureml-api-2), [private workspace connectivity](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-secure-workspace-vnet?tabs=se&view=azureml-api-2). These were inspected as design guidance; no tenant-specific tests have run.

## Environment and network topology — v0.2

[Environment topology](../../docs/diagrams/07_deployment_candidate.svg) and [network/identity paths](../../docs/diagrams/07b_network_identity.svg) expand the original capability mapping. Every resource is a candidate. Names, subscription, region, address ranges, SKUs, quotas, pricing and actual principal IDs remain unset. Resource-group grouping is administrative and does not provide isolation by itself.

The proposed first constructed environment, if later authorized, is reference development in a dedicated nonproduction resource group. Use an Azure ML workspace for experiment and workspace-local model asset tracking, governed Storage for data/artifacts and bounded training/batch compute for approved jobs. Model assets in the workspace do not imply a separate shared Azure ML registry. A validation environment is proposed as a separate workspace/resource group with separate storage access and identities before release-pipeline integration testing. The second environment and later site environment are not prerequisites for this current document review or automatic workspace creation commitments. Dependency boxes are distinct for development and validation; the common logging box denotes environment-scoped access, not shared credentials or unrestricted cross-environment data.

Reference scoring remains batch jobs. There is no selected online endpoint, always-on cluster or production application host. A later live service must be sized and selected against measured throughput and the site's candidate latency/availability requirements. The mock viewer consumes restricted reference evidence only. Do not draw a source-to-equipment write path or assume real CMMS access.

### Connectivity and identity allocation

| Path / actor | Proposed design | Evidence required before implementation or exposure |
|---|---|---|
| Operator to workspace | Organizational identity plus an approved private client route and private DNS to a workspace private endpoint | Actual client route (such as approved VPN or in-network workstation), DNS resolution and scoped access plan; no endpoint lockout |
| Private client to dependencies | Separate dependency private endpoints and DNS where required for Storage, Key Vault and image registry | Dependency inventory and tested resolution/access; a workspace endpoint alone does not secure every dependency |
| Job compute to dependencies | Azure ML managed network with approved outbound rules/private endpoints, separately designed from inbound access | Required service endpoints, build/image/package access and egress cost review; deny unexpected destinations |
| Human operator / deployer | Named Entra principal; narrowly scoped resource-operation roles | Final action-to-role matrix; no blanket subscription Owner and no implicit data-plane access |
| Job identity | Workload identity limited to required input reads and designated output writes | Exact data-plane assignments, scope and negative tests; no role-assignment or promotion rights |
| Workspace service identity | Only documented dependency operations needed for the configured workspace | Distinguish workspace service identity from job identity; verify both effective permissions |
| Release automation | Separate target-scoped identity and reviewed runner connectivity; federation candidate | Later explicit authorization, trusted workflow/subject restrictions and exact target permissions; runner networking remains a separate requirement |
| Reviewer / evidence reader | Read-only access to approved evidence | No deploy, training-data mutation or secret-read permission; actual independent review assignment remains open |

Microsoft documents private workspace ingress separately from managed network egress. The workspace is a managed service, not a VM placed inside the client VNet. In view 07b, Azure service scheduling/control-plane relationships are distinct from data-plane traffic. Entra authentication authorizes actions; it does not establish network reachability. Required Azure control-plane/identity/package endpoints and the monitoring route need explicit review; this diagram does not promise that every transaction uses Private Link.

Workspace dependency mode must be selected before IaC: record whether Key Vault, container registry and Application Insights are associated, brought by the project, lazily provisioned or otherwise supported by the chosen workspace mode. Review the current resource schema and supported configuration then; do not omit required dependencies or infer a zero-cost workspace. Keep storage, secrets, images and identity scopes separate between development and validation unless a justified reviewed shared-service design establishes equivalent controls.

### Logging, recovery and cost implications

Collect job/model lineage, resource diagnostics, identity/access events, approved release events, source/contract failures, scoring/version coverage and cost/usage observations. Azure Monitor/Log Analytics are candidates; Application Insights depends on application/runtime needs. Define supported diagnostic categories, collection routes, retention, access and alert ownership before enabling them. Raw waveforms, secrets and unnecessary personal information do not belong in default logs. No log collection or alerts are configured today.

Backup/recovery covers source and model manifests, accepted records, configuration and release evidence, with separate credentials/network re-entry checks. Candidate RTO/RPO require future exercises. Development, validation, private connectivity, image retention, logging, recovery and temporary rollback capacity are cost drivers in the single lifecycle model; amounts remain TBD. Resource budgets and notifications do not automatically enforce a spending cap. Compute limits and teardown controls require separate design and tests.

Microsoft primary references inspected 2026-10-10: [managed network isolation](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-managed-network?view=azureml-api-2), [private workspace connectivity](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-secure-workspace-vnet?view=azureml-api-2), and [versioned model assets](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-models?view=azureml-api-2). These support service relationships; environment separation, promotion and rollback rules above are proposed DME design decisions. No authentication to Azure was performed.

## Logical data layers — v0.3

Map the proposed [Bronze/Silver/Gold layers](../../docs/04-data-architecture-and-digital-thread.md) to governed storage paths/containers or tables only after workload, format, rights and access needs are resolved. Development/validation environment separation and data maturity layers are different dimensions; avoid turning three layer names into three automatically provisioned services. No Databricks/Fabric dependency, extra storage account or deployment is introduced by ADR-009.

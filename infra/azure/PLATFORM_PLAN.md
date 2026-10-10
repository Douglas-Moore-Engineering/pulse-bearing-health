# Azure Platform Plan — Unprovisioned

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

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

# Azure reference foundation

Implementation increment 0.4.0; unprovisioned, not cloud-validated.

[main.bicep](main.bicep) implements the proposed first foundation: dedicated resource-group scope, private Storage and Key Vault, an Azure ML workspace with managed identity and approved-outbound network mode, private endpoints/DNS and diagnostic dependencies. It creates no training cluster, online endpoint, container registry, site integration or public application.

Use [execution-inputs.example.json](execution-inputs.example.json) for account-owner inputs. `eastus2`, names and address ranges are engineering proposals. The real tenant/subscription, cost ceiling, region eligibility and private operator route are unresolved. Budget notifications would not enforce a hard spending cap. Private endpoints, storage, retained logs and other dependencies can incur charges without training compute.

This foundation is intentionally incomplete for workload operation: scoped human/job roles, supported workspace dependency permissions, package/image egress, registry/image-build strategy, Azure Monitor private-link scope and client route must be resolved and tested before jobs. Application Insights public ingress/query are disabled; telemetry is not claimed operational until private monitoring connectivity is added. No learned-model or service promotion follows from foundation creation.

## Validation and execution sequence

1. Compile locally with `bicep build infra/azure/main.bicep`. A compiler must be available; compilation is not subscription validation.
2. Populate account-owner inputs outside version control, review dated service prices in PULSE-LCC-001 and bind the approved foundation scope and costs. Do not use fictional project budget ceilings.
3. Authenticate to the explicitly authorized tenant, verify subscription and resource-group scope, and inspect applicable policies/provider/region support. Preserve private connectivity; do not enable public access to fix access failures.
4. Run Azure deployment validation and what-if against the exact parameters/template. Resolve failures and review every proposed resource and role change before creating anything.
5. Deploy only the accepted foundation; verify actual identities, access restrictions, DNS and reachability. Verify anonymous access denial and separation of data-plane roles. Record deployed IDs/configuration and actual costs privately.
6. Establish job identities, approved egress, private monitoring, image provenance and bounded compute before any data/model job. Then run platform negative, restore and integration tests and update the existing V&V register.

The current implementation contains no command that automatically authenticates, provisions, trains or deletes. Restore and teardown require inventory, evidence export, retention/hold disposition and scoped account-owner authority; Key Vault purge protection prevents immediate purge.

Primary references inspected 2026-10-11: [workspace resource schema](https://learn.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/2025-12-01/workspaces), [storage resource schema](https://learn.microsoft.com/en-us/azure/templates/microsoft.storage/2023-05-01/storageaccounts), [Azure ML service authentication](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-identity-based-service-authentication?view=azureml-api-2). These support configuration planning, not evidence of successful provisioning.

# Runbooks and Engineering Backlog

PULSE pre-Azure review v0.2 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Immediate preparation backlog: obtain dataset inventory and intended-use rights; profile units/labels/groups; confirm evaluation/acceptance targets; resolve costs; review architecture and boundary. User review precedes Azure connection.

Later platform backlog: accepted region/subscription/network/identity and cost plan; versioned IaC/CI; nonproduction what-if and security/recovery tests. Then pipelines, reproducible baselines/candidates, evidence workflow and staged V&V. Do not skip platform controls to deploy a model.

Use [runbooks index](../runbooks/README.md) for planned degraded, recovery, incident, change and retirement procedures. All are unexercised.

## Architecture refinement backlog — v0.2

MLOps/release and Azure topology detail has been prepared in views 04/04b/07/07b/08/08b. Still proposed for a subsequent design increment: functional capability decomposition, integration architecture, threat/defense-in-depth view and a critical runtime sequence. Owner: Dr. Moore / DME architecture. Closure: requirement-linked source, readable render and semantic correspondence review. These are documentation gaps; Azure construction stays blocked by the separate existing cloud-entry conditions.


## Reference implementation return ? v0.4

The four earlier architecture gaps now have requirement-linked editable views and exports in the [architecture index](architecture/README.md). Critical execution uses an ordered flowchart that makes rejection paths explicit. This closes diagram-authoring coverage for the bounded reference increment, not architecture approval or full runtime evidence. The original platform/model/site views remain proposals.

[Local operating and recovery instructions](REFERENCE_IMPLEMENTATION.md) accompany the reference harness. Remaining implementation includes qualified dataset adapters, frozen group splits before windowing, trained/evaluated baselines and candidates, cloud roles/client route/monitoring, authenticated application, protected promotion, representative load/recovery checks and operational readiness. These cannot be marked complete from fixture tests. See the [execution handoff](../customer/08-deployment-execution.md) for actual account/budget inputs still required.

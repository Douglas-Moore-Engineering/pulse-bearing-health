# Architecture Trade Studies

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

[Decision register](../architecture/architecture_decisions.csv) compares batch/stream, baselines/learned models, advisory/automation, separate RUL, cloud/local, network design, portable core and evidence stores. Prefer the simplest option meeting requirements, but retain competing choices until feasibility/cost reviewed.

Evaluation criteria: reproducibility, valid diagnostic/prognostic evidence, operator usefulness, latency/recovery, security/authority, operating effort, integration risk and lifecycle cost. No unsupported weighted score declares a winner. Financial comparison uses the same PULSE-LCC-001 horizon, scope, workload and price basis; numeric costs remain TBD. Resolve technical/cost constraints before accepting cloud choices.

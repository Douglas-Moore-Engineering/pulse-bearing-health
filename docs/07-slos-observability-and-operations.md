# SLOs, Observability and Operations

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Future site candidates from Q-07: p95 service receipt-to-persist ≤5 seconds; daily reconciliation by 06:00 plant-local; 99.5% monthly advisory application availability; RTO four hours; RPO one hour for accepted central records. Operational timezone, eligible-time denominator, workload and downtime exclusions are unresolved; do not apply these to a dormant research workspace as an SLA.

Monitor valid/invalid/missing data, freshness, pipeline latency, scoring latency, artifact/version coverage, class/confidence distributions, alert/disposition rate, domain shift, security control health and cost/usage. Every signal needs window, threshold, owner and response. Numeric drift and alert thresholds are TBD until baseline/operator workload established; delayed failure labels prevent claims of continuously measured recall.

Reliability owns operational advisory interpretation; IT owns platform incident response; Dr. Moore provides the agreed support proposal. Stale/invalid data triggers degraded/unavailable results and manual rounds, not continued healthy status. Incident severity and after-hours response are unagreed. Follow proposed [runbooks](../runbooks/README.md); exercise them before real exposure.

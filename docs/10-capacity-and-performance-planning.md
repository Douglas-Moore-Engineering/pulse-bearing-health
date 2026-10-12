# Capacity and Performance Planning

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

## Parameterized sizing

Let N=12 site assets (fictional scope), C=channels per asset, f=sampling rate, b=bytes/sample, d=duty fraction, W=window seconds, O=overlap fraction, p=protocol/metadata overhead. C, f, b, d, W, O, p and compressed size are unresolved and source-specific.

Raw bytes/day = N × C × f × b × 86400 × d × (1+p). Window rate/second while active = N / [W × (1−O)] for 0≤O<1; channels remain part of payload. Retained raw bytes = measured daily bytes × approved retention days. Feature bytes/day = scored windows/day × measured feature-record size. Estimate replicas, indexing, logs, backups and network/egress separately. Do not cost storage from N alone.

Reference batches use actual source inventories and measured file sizes rather than fictitious streaming rates. Time per batch = preprocessing + feature + model + evidence I/O measured on representative hardware; training cost = experiments × runtime × unit rate. Use burst/backfill factor and outage buffering only after their basis is known. Reference and site workload scenarios remain separate.

Recovery: buffer requirement = measured incoming bytes/second × tolerated collection outage; central RPO does not imply edge data protection. RTO covers identity, network, storage, model/manifest and operator recovery. No SKU, GPU or cluster size is selected from unmeasured workloads.

Measure file counts/bytes, samples/sec, window counts, RAM peak, CPU/GPU use, scoring/training latency, retention footprint and egress before Azure sizing. Capacity and cost are BLOCKED pending those measurements; code formulas are not deployment-scale evidence.

## Current Kubernetes workload increment

See [AKS capacity and release](AKS_CAPACITY_AND_RELEASE.md) for the user-supplied daily volume and six-hour peak, local load experiments, quota restrictions and cost floors. The historical 12-asset formulas above remain contextual and do not establish the new request mix.

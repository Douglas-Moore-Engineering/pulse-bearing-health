# Data Architecture and Digital Thread

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Canonical path: immutable source → rights/checksum manifest → quarantine or accepted records → contextualized bearing/run data → features → model evidence → human dispositions/outcomes. Preserve dataset-specific units, sampling rate, bearing/run identifiers and acquisition regime. Never concatenate unrelated datasets as if their labels and operating conditions were interchangeable.

[Vibration contract](../data/contracts/vibration-window.schema.json) and [advisory contract](../data/contracts/advisory.schema.json) are versioned design specifications, not production ingestion code. Resolve timestamps that are relative/test-rig values explicitly; do not invent calendar timestamps. Source adapter mappings, sample units, defect labels and schema profiles are required before data acceptance.

[Dataset register](../data/dataset_register.csv) holds candidates and rights limits. User-reported possession of data is not evidence of inspected files. Bytes, checksums, file inventories and allowed use are not yet recorded. No dataset is currently approved for training or redistribution. Paderborn's source states noncommercial licensing and directs commercial users to obtain permission; DME portfolio use must not silently be classified as noncommercial. CWRU seeded-fault data can support bounded diagnosis studies but is not run-to-failure RUL evidence. IMS needs source-specific rights and run/endpoint inspection.

Split by source bearing/run before segmentation; keep all overlapping windows from a run in its assigned partition. Preserve a held-out test manifest before model/threshold selection; use validation only for selection. Evaluate cross-regime and cross-source portability separately. If independent groups are insufficient, report limited feasibility rather than substitute a random-window split.

Lineage keys: source checksum, adapter/schema version, bearing/run/window identity, split, feature code/config digest, model/threshold/policy digest and advisory evidence ID. Reconstruct from immutable manifests. Site 90-day/24-month retention is a candidate policy, distinct from benchmark licensing. Recovery scope and legal holds need later approval.

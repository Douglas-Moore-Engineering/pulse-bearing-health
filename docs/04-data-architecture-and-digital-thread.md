# Data Architecture and Digital Thread

PULSE pre-Azure review v0.3 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

Canonical path: immutable source → rights/checksum manifest → quarantine or accepted records → contextualized bearing/run data → features → model evidence → human dispositions/outcomes. Preserve dataset-specific units, sampling rate, bearing/run identifiers and acquisition regime. Never concatenate unrelated datasets as if their labels and operating conditions were interchangeable.

[Vibration contract](../data/contracts/vibration-window.schema.json) and [advisory contract](../data/contracts/advisory.schema.json) are versioned design specifications, not production ingestion code. Resolve timestamps that are relative/test-rig values explicitly; do not invent calendar timestamps. Source adapter mappings, sample units, defect labels and schema profiles are required before data acceptance.

[Dataset register](../data/dataset_register.csv) holds candidates and rights limits. User-reported possession of data is not evidence of inspected files. The original candidates remain unqualified. A later, distinct LDM-UPB source inspection is recorded below; it does not qualify a full training dataset. No dataset is currently approved for training or redistribution. The older KAt Paderborn candidate (DS-PADERBORN) states noncommercial licensing and directs commercial users to obtain permission; DME portfolio use must not silently be classified as noncommercial. CWRU seeded-fault data can support bounded diagnosis studies but is not run-to-failure RUL evidence. IMS needs source-specific rights and run/endpoint inspection.

Split by source bearing/run before segmentation; keep all overlapping windows from a run in its assigned partition. Preserve a held-out test manifest before model/threshold selection; use validation only for selection. Evaluate cross-regime and cross-source portability separately. If independent groups are insufficient, report limited feasibility rather than substitute a random-window split.

Lineage keys: source checksum, adapter/schema version, bearing/run/window identity, split, feature code/config digest, model/threshold/policy digest and advisory evidence ID. Reconstruct from immutable manifests. Site 90-day/24-month retention is a candidate policy, distinct from benchmark licensing. Recovery scope and legal holds need later approval.

## Bronze, Silver and Gold design — v0.3

[View 03](diagrams/03_data_lineage.svg) explicitly applies the medallion pattern to Pulse. [ADR-009](../architecture/adr/adr-009.md) records the proposed choice and alternatives. These are logical quality and consumption boundaries. They do not require Databricks, Fabric, separate storage accounts, separate copies of every waveform, or any cloud connection for this design review. Physical placement, format and access enforcement follow measured workload and the platform review.

| Layer | Contents and authority | Promotion / publication condition |
|---|---|---|
| **Bronze — source fidelity** | Original, authorized source files in native format; dataset/bearing/run identity; checksum and acquisition/rights manifests. Preserve source bytes; provenance metadata is separate. | Source inventory and allowed use recorded; hashes match; a versioned source adapter can interpret the file. Raw does not mean qualified for ML. |
| **Silver — validated observations** | Canonical run observations or indexed waveform references, verified units/sample rate/time basis, asset/bearing/run mapping, operating regime, qualified labels and quality flags. Preserve detail needed for signal analysis. | Source-specific contract, identity, integrity and quality checks pass; invalid records remain excluded with quarantine reasons. A transformation records the original unit/value and conversion rule. |
| **Gold — governed products** | Versioned feature/window datasets for a named evaluation or inference purpose; curated bearing-health summaries and advisory records. Predictions, human dispositions and observed maintenance outcomes are separate product types linked by evidence IDs. | Product contract, lineage, use eligibility and access checks pass. ML features obey partition/transform rules; advisory publication obeys the released model/policy and abstention rules. Gold does not mean correct prediction, site validation or permission to act. |

The [layer register](../data/data_layers.csv) defines the proposed owner, consumers, access, retention, contracts and trace. Dr. Moore owns reference data engineering; actual customer data, reliability and IT owners must be named for site adaptation. No data layer is populated or operationally verified today.

### Identity, lineage and storage conventions

Use dataset ID + source file digest + bearing/run identity as the source key. A canonical record adds source offset/time basis and source-adapter/schema version. A window adds window ID and its group-partition assignment. A feature product adds transformation code/configuration and fitted-transform digests. An advisory adds the exact release manifest, model, threshold and policy versions and its evidence ID. Human dispositions and confirmed outcomes link back to that ID; an anomaly label must never overwrite an observed failure label.

Proposed logical paths are `bronze/<dataset>/<source-digest>/`, `silver/<dataset>/<adapter-version>/<run-id>/`, and `gold/<product>/<build-id>/`. They are naming examples, not created directories, Azure containers or approved physical partitions. Access controls must be enforced independently of folder names. Keep independent datasets separate until a reviewed mapping demonstrates compatible units, labels and operating regimes.

The existing [source manifest example](../data/lineage/manifest.example.json), [vibration-window contract](../data/contracts/vibration-window.schema.json), [advisory contract](../data/contracts/advisory.schema.json), and [release-manifest template](../governance/release-manifest.template.json) cover different portions of this chain. They are drafts, not complete executable contracts for every layer. The vibration schema currently profiles reference train/validation/test windows; raw-run and live-inference profiles, feature-table schema, outcome schema and source adapters require qualification of the actual files before schema freeze. Site inference must not be mislabeled as a test partition merely to satisfy the current reference schema.

### Quality gates and failure behavior

1. **Admission to Bronze:** verify authorized possession/intended use and inventory the source. Compute and record checksums on admission. Unknown or disallowed rights block use/redistribution; do not land unauthorized material merely because the layer is raw. An unreadable but authorized file may be retained as original evidence, with its failure recorded and no promotion.
2. **Bronze to Silver:** verify stored digest, source identity, format, sampling rate, engineering units, time basis, run continuity and applicable label provenance. Record schema/adapter versions and per-record reason codes. Quarantine points to the immutable source and failed records; it does not silently delete or repair measurements. If labels are unknown, exclude the associated supervised capability rather than invent labels. Candidate anomaly use requires its own qualified training definition.
3. **Silver to Gold features:** assign independent bearing/run groups before creating overlapping windows. Fit learned scaling/preprocessing only on the training partition; apply that fitted version unchanged to validation/test and compatible inference. Publish versioned, partition-specific product manifests. Keep the sealed test inaccessible to model/threshold selection. Source-relative time stays source-relative; no invented calendar dates or warning horizons.
4. **Gold advisory products:** verify the approved release, data/feature/model/policy versions and supported regime. Use an explicit unavailable/degraded record when validity or eligibility fails. RUL requires qualified failure/censoring data and interval evidence; no direct anomaly-to-RUL conversion. Aggregate health views preserve freshness, missingness and model-version coverage; missing values are never converted into a healthy reading. Human decisions and realized outcomes remain distinct from model evidence.

Promotion means producing a new validated version plus lineage, not moving or deleting the source object. Failed checks deny publication to the intended consumer. Consumers resolve only a completed approved product manifest; incomplete runs are not visible as the current product. Reprocessing uses recorded source digests and a new build/version, compares output counts/digests and supersedes previous products explicitly. Replayed source files are detected by the source key; corrections and legitimate new acquisitions require distinct provenance. Late records and label changes trigger a versioned rebuild of affected products with retained prior evidence, not mutation of a sealed evaluation.

### Access, retention and cost

Source ingestion can write Bronze; transformation identities read their inputs and write only their designated output/quarantine paths. Model selection cannot write source observations, change split assignments or read sealed-test data outside its authorized evaluation. Advisory readers consume only permitted Gold products, not training data or secrets. Released inference reads compatible feature products and writes version-bound evidence; it cannot promote a model. Exact roles and enforcement remain platform-entry work.

Bronze immutability means preserve bytes within the permitted retention/legal-hold window, not retain forever. The fictional site's raw 90-day and derived/evidence 24-month windows remain candidate policies; public data rights and actual source ownership govern reference retention separately. Quarantine has restricted access and an explicit purge/hold policy still to be agreed. Lineage metadata must retain enough permitted provenance to explain an output when source bytes are legitimately deleted; reprocessing may then be unavailable and must be reported honestly.

Track retained bytes by product, validation/reprocessing compute, duplicated data, quarantine, logging, backup and egress in the existing lifecycle cost model. Prefer source references over unjustified copies. No new price, capacity, recurring service or spending approval is implied by the three logical layers.

### Verification and evidence state

Design trace: source provenance → PULSE-FR-001 / VV-001; quarantine → PULSE-FR-002 / VV-002; group separation → PULSE-NFR-008 / VV-020; advisory version lineage → AIG-REQ-001 / VV-021; site retention → PULSE-NFR-006–007 / VV-018–019. Actual qualification, replay/deduplication, partial-publication denial, rights rejection, unit conversion, leakage and retention tests require real adapters and representative authorized data; they are not executed by a Markdown or diagram check.

Primary reference inspected 2026-10-10: [Microsoft — medallion architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion). The source describes a recommended logical pattern rather than a universal requirement. Pulse's product boundaries, access rules and staged implementation are DME design proposals. Layer names alone provide no transaction, security or ML-validity guarantees.


## LDM-UPB source qualification increment - 2026-10-11

The user supplied a distinct run-to-failure collection, now registered as `DS-LDM-UPB-RTF`. Read the [qualification review](../data/qualification/ldm-upb-review.md) and [source manifest](../data/qualification/ldm-upb-10868257.json). Its source metadata specifies CC BY 4.0, independently of the older KAt candidate. The description and five selected B02 archive members were inspected; full-run integrity, native adapters, endpoint/censor decisions and bearing-disjoint evaluation remain open. Raw data is excluded from Git. No training or cloud gate changes to PASS.

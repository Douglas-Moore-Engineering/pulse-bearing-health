# Reference implementation 0.4.0

Local software exercise with generated fixtures. No trained model, qualified public dataset, site validation or Azure deployment.

## Run and inspect

From the repository root, use Python 3.10 or later:

```powershell
python -m pip install -e ".[test,data,api,deploy]"
python -m pytest -q
python scripts/run_reference_demo.py --output outputs/reference-run-001
python scripts/validate_review_package.py
```

Open `outputs/reference-run-001/index.html` locally. Each run requires a fresh output directory so previous evidence is preserved. Generated outputs and the SQLite database are excluded from Git. The report identifies every result as unavailable and unvalidated for a customer site.

To record a later review, copy an evidence ID from the report and run `python scripts/record_reference_decision.py --help` for the required database, actor, disposition and rationale arguments. The actor is a local self-declaration, not authenticated cloud identity. Decisions persist in SQLite; the generated HTML is a snapshot and does not refresh after a new decision.

## Implemented boundary

The local Python API in `src/pulse/core.py` registers source bytes with a checksum, dataset/bearing/run identity and a supplied rights-evidence reference. This reference is a provenance field, not an automated license decision. Its adapter accepts one JSON source window conforming to the existing vibration contract, with `source_sha256` added after registration. Other source formats require a qualified adapter. The accepted window must match registered source bytes.

The SQLite store validates contracts, UTC timestamps, finite numbers, processing bounds, source integrity and bearing-disjoint partitions. Invalid contract/provenance/split records enter quarantine with reasons and cannot generate evidence. Non-JSON or nonfinite input is rejected before persistence. Exact replay is idempotent; conflicting window identities are rejected. Source bytes, accepted windows/features, evidence and human dispositions are persisted in separate tables.

RMS is calculated in m/s²; g inputs use 9.80665 m/s² per g. Pearson population kurtosis is null for constant signals. These are descriptive features, not learned predictions. No fitted model, threshold selection, diagnosis, RUL or fault probabilities are implemented. Every capability result explicitly abstains. Evidence identifies source/data-manifest, feature, model, threshold and policy state. The threshold state lives in the linked trace because the existing advisory schema does not admit a threshold field.

Human approve/modify/reject records require an existing evidence ID, actor, timestamp and rationale. Actors are supplied by the local operator, not authenticated Entra identities. An acknowledgment of unavailable evidence never emits a mock work order. No equipment-control or real CMMS API exists. The HTML viewer is read-only; decisions use the local Python API and the demo records visibly simulated reviewer decisions.

`src/pulse/release.py` checks an offline bundle against a separately supplied approval: artifact digests, target, scope, validity interval and revocation. Tests use simulated approvals. Approval authentication, protected CI/environment configuration, operator permissions and cloud promotion are **not implemented** by this local helper. It never deploys and cannot grant site authority.

## Validation and limits

The separate [LDM-UPB B02 sample adapter](../data/qualification/ldm-upb-review.md) checks native MAT/CSV provenance, calibration and sampling time, then emits descriptive features. It remains an inspection tool outside the JSON-window store. The [adapter validation](../governance/evidence/ldm-adapter-validation.json) records 31 passing tests and a four-channel-record native sample profile, without training, RUL targets or dataset qualification. The earlier 24-test evidence remains a historical snapshot.

Tests cover malformed input, source substitution/tampering, changed samples, bearing leakage across runs, replay conflicts, unit conversion, abstention, human trace, backup restore and release integrity/expiry/target/path failures. Generated fixtures demonstrate software behavior only. The production V&V matrix retains its unexecuted and partially exercised criteria; no engineering or AI gate is automatically passed.

The local store is a single-operator reference harness under operating-system file access. It is not a multiuser service, immutable audit store or production data pipeline. The caller must freeze bearing assignments with `assign_groups` before ingestion; reassignment is rejected. A qualified dataset adapter must establish the complete group split before windowing. Training/validation/test fixture labels do not imply model fitting or held-out performance evaluation. No representative workload, availability, recovery SLA, predictive performance, independent assurance or cloud access control is established.

[Azure foundation](../infra/azure/README.md) is separate infrastructure source. The current [execution handoff](../customer/08-deployment-execution.md) records expanded authorization and the still-missing account and spending limits. Four added [architecture views](architecture/README.md) distinguish implemented reference behavior from proposed cloud/site functions.

## Operator and recovery procedure

1. Keep real data outside this fixture harness until rights, source qualification and access controls are established. Use a fresh local output directory and review the report's unavailable status.
2. Investigate quarantine reasons; do not edit accepted records or bypass checks. Correct input provenance/contracts and rerun in a new evidence directory.
3. Call `ReferenceStore.backup(path)` for a consistent SQLite snapshot. Restore by opening the snapshot with `ReferenceStore`, running SQLite `PRAGMA integrity_check`, reconciling counts and verifying referenced source/evidence digests. Local automated recovery tests do not establish cloud RTO/RPO.
4. On integrity failure, stop consuming the affected report, preserve its database/report and return unavailable. No model fallback or automatic promotion is available.
5. Retain or remove generated run directories only under the local owner's retention decision. No automatic cleanup deletes evidence, source data or cloud resources.

# Offline intake validation

Run `python scripts/validate_offline_intake.py INPUT.json` from the repository. Install project dependencies first. This read-only command never moves, imports or uploads the file and prints only status/reason codes. Exit 0 means structurally valid pending review; exit 2 means rejected. File access errors remain command errors. Inputs are bounded to 32 MiB and one million samples per window. No customer files were used in verification.

The JSON envelope has exactly `metadata` and `window`. Metadata requires nonblank `asset_id`, `sensor_id`, `calibration_ref`, `data_use_ref` and `provenance_ref` strings, each at most 256 characters. Window follows the existing [vibration contract](../data/contracts/vibration-window.schema.json), with additional finite-value, nonblank identity and explicit UTC checks. Supported acceleration units remain `g` and `m/s2`; unknown units and source-relative timestamps are rejected by this initial intake path.

Reference presence does not verify authority, calibration or source integrity. A successful result explicitly leaves these unverified and does not qualify a detector. The operator must review the actual referenced records and approved asset/sensor mapping before downstream ingestion. This command supplies no mapping registry, source-byte hash verification, cross-window duplicate detection or retention service.

Rejected files remain where they were supplied; no copying into an allegedly secure quarantine occurs. Keep them in the authorized restricted intake location and do not feed them downstream. Never place customer data in Git. Later managed intake needs an approved restricted store and access policy; this validator alone is not that store.

[Implementation](../src/pulse/intake.py), [CLI](../scripts/validate_offline_intake.py), and [115-test suite evidence](../governance/evidence/offline-intake-tests.xml). Eight new synthetic tests cover valid-pending-review results, invalid units/time/identities/numerics, missing references and malformed envelopes. One existing Starlette/httpx warning remains. No cloud deployment or detector promotion occurred. Trace: PULSE-FR-003, AIG-REQ-001.

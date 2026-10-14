# 2. Code walkthrough — Pulse

[Demo](demo.md) → **Code walkthrough** → [Results](results.md)

## Local fixture path: follow execution order

| Order | Actual code | Responsibility and output |
|---|---|---|
| 1 | [`scripts/run_reference_demo.py`: `run`](../scripts/run_reference_demo.py) | Creates a fresh output directory and SQLite store; generates three sine-wave windows. Rejects reuse of an existing database. |
| 2 | [`core.py`: `ReferenceStore.assign_groups`, `register_source`](../src/pulse/core.py) | Assigns distinct bearings to train/validation/test fixture groups and registers source bytes, checksum and provenance. Fixture split labels do not imply model fitting. |
| 3 | [`core.py`: `ingest`](../src/pulse/core.py) | Validates contracts, finite values, source identity and group consistency; quarantines invalid records. |
| 4 | [`core.py`: `features`](../src/pulse/core.py) | Computes RMS in m/s² and Pearson kurtosis; converts g using 9.80665. These are descriptive features. |
| 5 | [`core.py`: `advisory`](../src/pulse/core.py) | Persists source-linked evidence with unavailable capabilities rather than an unsupported diagnosis. |
| 6 | [`core.py`: `decide`, `backup`, `summary`](../src/pulse/core.py) | Records a simulated reviewer rejection, snapshots SQLite and returns counts. The demo emits JSON and static HTML. |
| 7 | [`01_fixture_and_evidence.ipynb`](../notebooks/01_fixture_and_evidence.ipynb) | Calls the real demo, displays actual output, then reads the separate historical detector disposition. |

## Other implemented paths

The deployed assessment boundary is [`api.py`](../src/pulse/api.py), with persistence in [`assessment_store.py`](../src/pulse/assessment_store.py). The reference anomaly path uses [`reference_detector.py`](../src/pulse/reference_detector.py) and [`alert_ledger.py`](../src/pulse/alert_ledger.py). These are separate from the fixture harness. Follow [current engineering review](ENGINEERING_REVIEW.md) for recorded integration evidence and unresolved qualification.

For failure behavior, inspect [`tests`](../tests) and the [local harness contract](REFERENCE_IMPLEMENTATION.md): bad inputs enter quarantine, conflicting identities are rejected and unsupported model capabilities abstain. The local actor string is self-declared; it is not proof of cloud authentication.

## Development order for future analytical work

Source qualification → raw-data EDA → leakage-safe split → train-only feature/preprocessing work → justified baseline/candidate comparison → frozen evaluation → interpreted error analysis → tracked artifact and review. The current notebook closes the visible local demonstration gap only. It does not claim new EDA, trained Decision Tree/XGBoost candidates, a feature store or MLflow runs.

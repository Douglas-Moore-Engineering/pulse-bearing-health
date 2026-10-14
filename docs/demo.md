# 1. Demonstration — Pulse

[README](../README.md) → **Demo** → [Code walkthrough](code-walkthrough.md) → [Results](results.md)

Run the existing synthetic pipeline, then inspect recorded detector evidence.

## Start here

Use Python 3.10 or newer in an isolated environment. From the repository root:

```sh
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e . -r requirements-notebooks.txt
python scripts/execute_notebooks.py
```

Open [the executed notebook](../notebooks/01_fixture_and_evidence.ipynb) in GitHub or the repository's VS Code workspace. Run cells top-to-bottom to reproduce the visible outputs. The script starts a fresh kernel, fails on unexpected errors and saves outputs back to the notebook. Dependency installation needs package access; notebook execution uses local inputs. Allow approximately 1–2 minutes after installation on a laptop (planning estimate, not a capacity result).

## Keep the fixture artifacts

```sh
python scripts/run_reference_demo.py --output outputs/reference-review-001
```

Use a fresh directory. Open `outputs/reference-review-001/index.html`; inspect `report.json`, `reference.sqlite` and `backup.sqlite`. Expected structure: three accepted synthetic windows, three feature/advisory records, simulated reviewer rejections and one quarantined malformed record. Advisories remain unavailable. The notebook uses a temporary directory and retains only the displayed report. You may delete your generated directory after inspection; never remove historical evidence to rerun the demo.

Inputs are generated sine waves, not downloaded bearing data. The demo exercises local software and does not invoke the deployed reference detector. See [harness details](REFERENCE_IMPLEMENTATION.md) and the separate [recorded benchmark viewer](../customer/benchmark-demo.html).

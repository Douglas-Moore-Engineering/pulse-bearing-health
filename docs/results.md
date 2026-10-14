# 3. Results — Pulse

[Demo](demo.md) → [Code walkthrough](code-walkthrough.md) → **Results**

## Newly executed local review — 2026-10-14

The existing fixture code produced **3 registered sources, 3 accepted windows, 3 advisories, 3 simulated decisions and 1 quarantined malformed record**. Each generated sine wave had RMS **0.7071067812 m/s²** and Pearson kurtosis **1.5**. Every advisory remained unavailable. These results demonstrate local software behavior, not bearing-health performance.

Commands exercised: `python scripts/run_reference_demo.py --output /tmp/pulse-review-cli-20261014` and the notebook's code cells. Focused checks: `python -m pytest -q tests/test_reference.py tests/test_detector_acceptance.py tests/test_trailing_median.py` — **42 passed**.

Inspect [code and saved outputs](../notebooks/01_fixture_and_evidence.ipynb). Source baseline: `961e4b30d625679dbab48d23c747d585ff1d1516`. The notebooks print exact source/evidence hashes; this delivery commit versions the notebook itself. [Recorded local environment](review-environment.json) identifies package versions; it is an observation, not a complete cross-platform dependency lock.

Local execution used sequential IPython cells in a fresh Python process because this environment disallows Jupyter socket transport. Standard `nbclient` fresh-kernel execution is configured in CI via `python scripts/execute_notebooks.py`; a local kernel run could not complete. HTML export succeeded. The notebook text/output was inspected; a browser-rendered notebook inspection remains open because no local browser binary was available.

The local source snapshot was partial. Full repository validation and clean-run dependency checks are assigned to the GitHub workflow; see the actual workflow result on the pull request rather than inferring a pass from focused tests. No cloud verification was performed in this increment.

## Historical measurements remain authoritative

| Measurement | Result and interpretation |
|---|---|
| [MEAS-PULSE-001](../governance/measurements/MEAS-PULSE-001.md) | 3,150/3,150 assessment receipts recovered in one isolated container test; this does not establish full host-loss recovery. |
| [MEAS-PULSE-002](../governance/measurements/MEAS-PULSE-002.md) | Paired detector coverage failed; lowest sensor group 91/296 eligible windows (30.7%). Development windows are dependent observations. |
| [Recorded evaluator report](../governance/evidence/detector-performance-consolidated.json) | Paired candidate FAIL; frozen RMS INCONCLUSIVE. No production release authorized. |
| [Open KPI plans](../governance/measurements/planned-kpis.md) | Qualified lead time, exposure-based nuisance burden and customer impact remain not measured. |

## Remaining engineering and delivery work

Owner: Dr. Douglas Moore. Preserve the existing qualification backlog and release disposition. Raw-data EDA and new baseline/candidate comparisons need their actual source inputs and a defined evaluation protocol; this notebook does not substitute for them. Verified MLflow experiment/registry run links remain open and no tracking run was created here. Full notebook browser inspection, complete environment reproducibility and repository-level security/review-control verification are not established by this increment. CI changes cover bounded notebook execution and review-document links; they do not establish comprehensive security scanning.

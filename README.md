# Pulse ? Bearing Health

A bearing-health reference system that turns vibration windows into traceable assessments and an authenticated maintenance-review workflow. Built for a fictional industrial customer; deployed on a single Azure VM running K3s.

**Status:** reference deployment operational; production detector **NOT_PROMOTED**. Public benchmark evaluation exposed missed faults and false positives. Those results are retained rather than presented as production success. See [current status](PROJECT_STATUS.md).

## Explore the system

- Open [the benchmark demo](customer/benchmark-demo.html) in a browser for a local walkthrough. It is not a live dashboard.
- Review the [deployed architecture](docs/diagrams/16_deployed_reference_runtime.svg) and [architecture decisions](docs/12-architecture-decisions.md).
- Inspect [runtime code](src/pulse), [tests](tests), [deployment tooling](infra/single-node), and [measured evidence](governance/evidence).

## Run locally

Python 3.10 or newer. From a fresh checkout:

```sh
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[test,data,api,deploy]"
python -m pytest -q
python scripts/run_reference_demo.py --output outputs/reference-quickstart
python scripts/validate_review_package.py
```

Use a fresh output directory for each demo run. This workflow uses synthetic fixtures and needs no Azure account, credentials, or dataset downloads. The authenticated cloud API is private and requires operator access; no public endpoint or cloud deployment is created by these commands.

## What is implemented

| Capability | Evidence and boundary |
|---|---|
| Authenticated assessment API | Entra application identity, asset grants, durable SQLite receipts, idempotency; no qualified degradation prediction |
| Reference anomaly workflow | Frozen IMS rule, simulated inbox and acknowledgement; [884-window replay](governance/evidence/azure-reference-detector-replay.json) |
| Pilot review routes | Deployed; live reviewer access remains pending managed-identity role propagation |
| Daily reconciliation | Fictional 12-asset timer, persistent reports, missing/unknown timing handling; [rollout](governance/evidence/azure-reconciliation-rollout.json); automatic deadline compliance not yet observed |
| Recovery | Half-hour bounded host-local snapshots and manual private off-host restore; [backup evidence](governance/evidence/reconciliation-post-rollout-backup.json) |
| Detector evaluation | [Recorded rejection and limitations](data/qualification/detector-candidate-disposition.md); no held-out success invented |

Latest recorded software suite: **143 passed**. [Test evidence](governance/evidence/database-reconciliation-tests.xml). CI runs software tests, the synthetic demo and document/register validation. These checks do not establish customer acceptance or model performance.

## Engineering decisions and limits

The USD 100/month ceiling led to a [single-node reference deployment](architecture/adr/011-single-node-reference-deployment.md), with SQLite and private operator access. This is not a managed AKS production cluster or a high-availability design. The budget is a spending boundary, not proof of actual monthly cost.

The requested 1.5 million requests/day has **not** been qualified. Sustained load, one-hour host-loss RPO, production availability, real plant validation and independent acceptance remain open. Public bearing datasets do not establish useful warning time or nuisance-alert performance at a customer site. See [capacity evidence](docs/AKS_CAPACITY_AND_RELEASE.md), [operations](runbooks/reference-operations.md), and [remaining work](docs/CURRENT_ENGINEERING_BACKLOG.md).

## Repository guide

| Directory | Purpose |
|---|---|
| `src/`, `tests/`, `scripts/` | Implementation, verification and reproducible exercises |
| `infra/`, `runbooks/` | Deployment and operating procedures |
| `data/qualification/` | Dataset suitability, experiment protocols and detector results |
| `requirements/`, `architecture/`, `governance/` | Requirement trace, decisions, risks and measured evidence |
| `customer/` | Fictional customer scope and demonstration package |

[Historical status records](PROJECT_HISTORY.md) preserve earlier increments and superseded plans. [Contributing](CONTRIBUTING.md) describes evidence rules. Keep this repository private unless publication is explicitly authorized. Credentials, private backups and raw dataset bytes are excluded; source references do not imply redistribution rights.

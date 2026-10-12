# Pulse - Bearing Health

Current Phase 10 preparation: [demo readiness and launch checklist](customer/10-demo-readiness.md). Locally verified on 2026-10-12: 180 software tests passed, three benchmark selections functionally checked, and synthetic replay completed. Ready for guided offline demonstration; actual review/acceptance and production qualification remain open.

A bearing-health reference system that turns vibration windows into traceable assessments and an authenticated maintenance-review workflow. Built for a fictional industrial customer; deployed on a single Azure VM running K3s.

**Status:** reference deployment previously verified; production detector **NOT_PROMOTED**. Public benchmark evaluation exposed missed faults and false positives. Those results are retained rather than presented as production success. See [current status](PROJECT_STATUS.md).

## For prospective clients

Start with the [15-minute review guide](customer/11-client-review-guide.md). This fictional reference demonstrates traceable software and delivery practices; it is not a customer endorsement or a qualified production detector.

## Explore the system

- Open [the benchmark demo](customer/benchmark-demo.html) in a browser for a local walkthrough. It is not a live dashboard.
- Review the [deployed architecture](docs/diagrams/16_deployed_reference_runtime.svg) and [architecture decisions](docs/12-architecture-decisions.md).
- Inspect [runtime code](src/pulse), [tests](tests), [deployment tooling](infra/single-node), and [measured evidence](governance/evidence).

Current engineering work: [backlog](docs/CURRENT_ENGINEERING_BACKLOG.md), [capacity evidence](docs/CAPACITY_STATUS.md), and [detector status](data/qualification/DETECTOR_STATUS.md).

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
| Pilot review routes | Deployed; real-token review GET passed; closure role and nonempty workflow recovery remain pending |
| Daily reconciliation | Fictional 12-asset timer, persistent reports, missing/unknown timing handling; [rollout](governance/evidence/azure-reconciliation-rollout.json); automatic deadline compliance not yet observed |
| Recovery | Three consecutive half-hour backups observed; actual Blob-to-container recovery passed for 3,150 receipts; [recovery evidence](governance/evidence/blob-container-recovery.json) |
| Detector evaluation | [Recorded rejection and limitations](data/qualification/detector-candidate-disposition.md); no held-out success invented |

Latest recorded software suite: **180 passed**. [Test evidence](governance/evidence/phase10-demo-tests.xml). CI runs software tests, the synthetic demo and document/register validation. These checks do not establish customer acceptance or model performance.

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

Current detector evidence: [consolidated status](data/qualification/DETECTOR_STATUS.md). RMS: INCONCLUSIVE under the complete policy, with the documented missed bearing retained. Paired SCA: FAIL. Neither is promoted.

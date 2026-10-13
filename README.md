# Pulse — Bearing Health

**Private reference system.** An authenticated maintenance-review workflow has recorded Azure deployment evidence. The production detector remains **NOT_PROMOTED**. [Current status](PROJECT_STATUS.md).

## Operational problem

Bearing degradation can lead to unplanned equipment stops. Pulse connects vibration observations, supporting evidence and human review so a reliability engineer can investigate a potential problem and a maintenance planner can decide what work is justified. The customer scenario is fictional.

## Users and decisions

Reliability engineers investigate assessments, operators acknowledge notifications, and maintenance planners authorize work. Pulse provides advisory evidence and a reference inbox; it does not control machinery or authorize maintenance.

## What currently works

- Authenticated assessment interface with asset permissions, durable SQLite records and duplicate-submission protection: [implementation](src/pulse/api.py), [recorded identity checks](governance/evidence/azure-asset-authorization.json).
- Benchmark assessment, anomaly-inbox and simulated acknowledgement workflow: [reference replay](governance/evidence/azure-reference-detector-replay.json).
- Isolated recovery of an Azure Blob snapshot into a local container: [MEAS-PULSE-001](governance/measurements/MEAS-PULSE-001.md).
- Guided offline benchmark and synthetic demonstrations: [readiness and limitations](customer/10-demo-readiness.md).

The recorded deployment uses one Azure virtual machine running K3s, a lightweight Kubernetes distribution, with private operator access. See [the deployment decision](architecture/adr/011-single-node-reference-deployment.md) and [operating procedure](runbooks/reference-operations.md). The links contain recorded deployment evidence.

## Measured results and conditions

| Metric | Recorded result / denominator | Context | Measurement record |
|---|---|---|---|
| Recovered assessment receipts | 3,150 / 3,150; counts preserved after container startup | One Azure Blob snapshot restored into an isolated local container | [MEAS-PULSE-001](governance/measurements/MEAS-PULSE-001.md) |
| Paired detector decision coverage | **FAIL** against 95% in every sensor group; lowest group: **91/296 eligible windows (30.7%)** | Three previously used development cases; retrospective criterion; full sensor-group results linked | [MEAS-PULSE-002](governance/measurements/MEAS-PULSE-002.md) |
| Qualified warning lead time and nuisance episodes per operating exposure | **Not measured** for the intended operating use | Physical endpoints and verified healthy operating exposure remain insufficient | [Open measurements](governance/measurements/planned-kpis.md) |
| Customer downtime reduction and attributable avoided loss | **Not measured** | No actual customer intervention, comparator or follow-up outcomes | [Open measurements](governance/measurements/planned-kpis.md) |

The paired candidate (`sca-paired-development`) fails coverage in both sensor groups of case 1 and one group of case 2. These dependent development windows do not establish independent bearing performance. The frozen root-mean-square (RMS) vibration rule also missed damaged bearing 4 in the IMS benchmark; its overall policy assessment remains **INCONCLUSIVE**. Later candidates remain unpromoted. See the [detector disposition](data/qualification/DETECTOR_STATUS.md).

## Qualification gaps and next work

Detector qualification, fault diagnosis, remaining useful life, sustained capacity, service availability and actual customer acceptance remain open. The receipt-recovery test does not establish recovery time or allowable data loss after a full host failure, or recovery of populated review and closure records. See the [engineering backlog](docs/CURRENT_ENGINEERING_BACKLOG.md) and [capacity status](docs/CAPACITY_STATUS.md).

The next bounded activity is offline demonstration and evidence review, followed by the existing detector/data qualification sequence. Site exposure and production promotion require their separate evidence and authorization.

## Run a demonstration or inspect the implementation

Use Python 3.10 or newer and an isolated environment. From the repository root:

```sh
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[test,data,api,deploy]"
python -m pytest -q
python scripts/run_reference_demo.py --output outputs/reference-quickstart
python scripts/validate_review_package.py
```

Use a fresh output directory. The executable demo uses synthetic fixtures and requires no Azure account or dataset download. The [offline benchmark HTML](customer/benchmark-demo.html) can be opened locally; it is not a live dashboard. Preparation checks and their execution dates are recorded in [demo readiness](customer/10-demo-readiness.md). The private cloud API requires separately authorized operator access.

## Engineering documentation

| Review need | Authoritative entry point |
|---|---|
| Business scope and users | [Discovery](customer/01-discovery-record.md), [client review guide](customer/11-client-review-guide.md) |
| Architecture and decisions | [Architecture index](docs/architecture/README.md), [decision records](docs/12-architecture-decisions.md) |
| Requirements and verification | [Requirements](requirements/requirements.csv), [verification and validation matrix](governance/verification_validation_matrix.csv) |
| Performance indicators, measurements and decisions | [Indicator dictionary](docs/appendix-a-kpi-dictionary.md), [measurement index](governance/measurements/README.md), [release gates](governance/release_gates.md) |
| Implementation and operations | [Source](src/pulse), [tests](tests), [runbooks](runbooks/README.md) |
| Current handoff and history | [Current status](PROJECT_STATUS.md), [lifecycle review](docs/SKILL_COMPLETION_REVIEW.md), [history](PROJECT_HISTORY.md) |
| Complete documentation | [Documentation index](docs/README.md), [contributing](CONTRIBUTING.md), [external DME skills](docs/DME_SKILLS.md) |

Private DME engineering repository. Keep credentials, private backups, customer data and unauthorized raw datasets out of Git. Dataset citations do not grant redistribution rights.

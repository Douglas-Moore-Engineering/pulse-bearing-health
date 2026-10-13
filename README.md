# Pulse — Bearing Health

**Private reference system.** An authenticated maintenance-review workflow has recorded Azure deployment evidence. The production detector remains **NOT_PROMOTED**. [Current status](PROJECT_STATUS.md).

## Operational problem

Bearing degradation can lead to unplanned equipment stops. Pulse connects vibration observations, supporting evidence and human review so a reliability engineer can investigate a potential problem and a maintenance planner can decide what work is justified. The customer scenario is fictional; reduced downtime or avoided loss has not been demonstrated.

## Users and decisions

Reliability engineers investigate assessments, operators acknowledge notifications, and maintenance planners authorize work. Pulse provides advisory evidence and a reference inbox; it does not control machinery or authorize maintenance. Fault diagnosis and remaining useful life are unavailable unless separately qualified.

## What currently works

- Authenticated assessment API with asset permissions, durable SQLite receipts and idempotent submission handling: [implementation](src/pulse/api.py), [recorded identity checks](governance/evidence/azure-asset-authorization.json).
- Benchmark assessment, anomaly-inbox and simulated acknowledgement workflow: [reference replay](governance/evidence/azure-reference-detector-replay.json). This demonstrates application behavior, not a qualified degradation detector.
- Isolated recovery of an Azure Blob snapshot into a local container: [MEAS-PULSE-001](governance/measurements/MEAS-PULSE-001.md).
- Guided offline benchmark and synthetic demonstrations: [readiness and limitations](customer/10-demo-readiness.md).

The deployed reference topology is a single Azure VM with K3s and private operator access. See [the deployment decision](architecture/adr/011-single-node-reference-deployment.md) and [operating procedure](runbooks/reference-operations.md). Deployment evidence is historical; this documentation review did not reconnect to Azure.

## Measured results and conditions

| Metric | Recorded result / denominator | Context | Measurement record |
|---|---|---|---|
| Recovered assessment receipts | 3,150 / 3,150; counts preserved after container startup | One Azure Blob snapshot restored into an isolated local container | [MEAS-PULSE-001](governance/measurements/MEAS-PULSE-001.md) |
| SCA paired candidate decision coverage | Case 1 DS: 104/117 (88.9%); FS: 104/126 (82.5%). Case 2 DS: 91/94 (96.8%); FS: 91/296 (30.7%). Case 11: 19/19 on each side | Consumed development cases; retrospective 95% coverage criterion fails | [MEAS-PULSE-002](governance/measurements/MEAS-PULSE-002.md) |
| Qualified warning lead time and nuisance episodes per operating exposure | **Not measured** for the intended operating use | Physical endpoints and verified healthy operating exposure remain insufficient | [Open measurements](governance/measurements/planned-kpis.md) |
| Customer downtime reduction and attributable avoided loss | **Not measured** | No actual customer intervention, comparator or follow-up outcomes | [Open measurements](governance/measurements/planned-kpis.md) |

The frozen RMS rule missed documented damaged IMS bearing 4. Its complete-policy assessment is **INCONCLUSIVE**, while the paired SCA candidate is **FAIL**. Later experimental candidates are distinct and remain unpromoted. [Current detector disposition](data/qualification/DETECTOR_STATUS.md). These findings are retained; repeated windows do not constitute independent bearings or operating hours.

## Qualification gaps and next work

Production detector performance, qualified failure warning, nuisance-alert burden, sustained capacity, service availability, full host-loss recovery and actual customer acceptance remain open. Receipt recovery does not establish host-loss RPO/RTO or nonempty review/closure recovery. See the [engineering backlog](docs/CURRENT_ENGINEERING_BACKLOG.md) and [capacity status](docs/CAPACITY_STATUS.md).

The next bounded activity is offline demonstration and evidence review, followed by the existing detector/data qualification sequence. Site exposure and production promotion require their separate evidence and authorization. The spending ceiling in the deployment decision is not a measured monthly cost.

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
| Architecture and decisions | [Architecture index](docs/architecture/README.md), [ADRs](docs/12-architecture-decisions.md) |
| Requirements and verification | [Requirements](requirements/requirements.csv), [V&V matrix](governance/verification_validation_matrix.csv) |
| KPIs, measurements and decisions | [KPI dictionary](docs/appendix-a-kpi-dictionary.md), [measurement index](governance/measurements/README.md), [release gates](governance/release_gates.md) |
| Implementation and operations | [Source](src/pulse), [tests](tests), [runbooks](runbooks/README.md) |
| Current handoff and history | [Current status](PROJECT_STATUS.md), [lifecycle review](docs/SKILL_COMPLETION_REVIEW.md), [history](PROJECT_HISTORY.md) |
| Complete documentation | [Documentation index](docs/README.md), [contributing](CONTRIBUTING.md), [external DME skills](docs/DME_SKILLS.md) |

Private DME engineering repository. Keep credentials, private backups, customer data and unauthorized raw datasets out of Git. Dataset citations do not grant redistribution rights.

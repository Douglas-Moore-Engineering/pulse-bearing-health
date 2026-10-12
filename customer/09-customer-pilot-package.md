# Customer demonstration and pilot preparation

Prepared 2026-10-11. **Ready for a guided benchmark demonstration and discovery meeting. Not approved for live customer telemetry or production maintenance decisions.** The customer scenario and acceptance targets are fictional assumptions. No customer, independent reviewer or site operator has signed acceptance.

## What the customer can see

Open [the interactive benchmark demo](benchmark-demo.html) locally in a browser. It requires no login, network service or customer data. It presents three recorded LDM bearing runs, vibration trends and a simulated alert queue. The grouping prototype reduces 3/26/9 original episodes to 1/1/1 while preserving each first alert. These are development results on already consumed evaluation data, not independent validation or a measured nuisance-alert improvement. [Reproducible evidence](../governance/evidence/customer-demo-stability.json).

The existing private Azure reference service separately demonstrates authentication, asset authorization, persistent receipts, a simulated inbox and acknowledgement. Its frozen 3x reference rule is different from the offline 1.5x candidate and grouping prototype. Do not present the HTML page as connected to Azure. The service does not provide a qualified degradation decision. Use the [operator runbook](../runbooks/reference-operations.md); do not share operator keys or bypass asset grants.

## Fifteen-minute meeting walkthrough

1. Explain the proposed value: bring changes in bearing vibration to a maintainer for review, with traceable evidence. Ask which maintenance decision the customer needs to support.
2. Open the demo, select B04, B12 and B17, and compare original versus grouped episodes. Explain that lead is measured to the last recording, not to a verified physical failure.
3. Show the simulated review queue. An acknowledgement records receipt; it does not prove a human inspected a bearing or accepted a diagnosis.
4. Explain the separate authenticated Azure reference workflow using [view 17](../docs/diagrams/17_reference_detector_workflow.svg) and its recorded [cloud replay results](../governance/evidence/azure-reference-detector-replay.json).
5. Agree whether a bounded, observational pilot is useful. Record real owners, data permissions and acceptance targets before any site connection. Do not ask the customer to rely on these alerts for maintenance.

## Proposed shadow pilot

Start with one agreed asset class and a small named asset list. A customer maintainer reviews alerts alongside existing maintenance practices; the system does not command equipment or replace existing monitoring. Duration depends on sufficient verified healthy exposure and documented events, not a calendar promise. A short pilot may demonstrate integration without establishing warning performance.

| Work / exit evidence | Responsible role | Status |
|---|---|---|
| Asset list, intended decision, operating regimes and sensor calibration | Customer maintenance owner and domain engineer | Requires actual customer |
| Data-use permission, access boundaries, retention/deletion, network and security review | Customer data/security owner with service owner | Required before intake |
| Timestamped data contract and representative sample validation | Engineering and customer instrumentation owner | Contract below prepared; site sample absent |
| Endpoint labels, healthy exposure and independent evaluation split agreed before tuning | Domain reviewer and model engineer | Required before qualification |
| Detector version frozen; every run, miss and abstention reported | Model engineer and independent reviewer | Research evidence available; pilot evaluation pending |
| Isolated customer environment, authorized alert destination, recovery and workload checks | Service owner | Not provisioned or authorized by this document |
| Acceptance review and written release decision | Customer owner and release authority | Not approved |

Roles are proposed responsibilities, not named or signed appointments. Capture the resulting decisions in the existing [discovery record](01-discovery-record.md), requirements and risk registers.

## Intake contract and label requirements

Before transfer, agree asset and bearing identifiers, sensor/channel mapping, mounting, calibration and units; sample rate and window duration; timestamp timezone and clock accuracy; speed/load/temperature and operating/rest intervals; missing-data and quality flags; and a permitted-use/provenance record. Raw waveforms are preferred where feature extraction must be verified. If features are supplied, bind their algorithm/version, units and original window identifiers.

Separately collect maintenance inspections, confirmed damage/failure event timestamps with uncertainty, repair/replacement records, and independently supported healthy operating intervals. Do not label early reference data healthy merely because it precedes an alert. Do not infer operating hours from elapsed calendar time. See [acceptance evidence specification](../data/qualification/alert-acceptance-evidence-needed.md). No real customer data belongs in Git; agree an access-controlled intake location first.

## Acceptance plan

Retain the fictional starting targets of at least 60 minutes warning and at most one nuisance episode per bearing per 30 operating days, with zero missed documented failures as the target. A real customer must review their usefulness and measurement definitions. Count independent bearings/events, not windows or channels; report uncertainty and operating regimes. Define the event endpoint, eligible exposure, episode closing/reopening, missing-data handling and adjudication before evaluation. Insufficient exposure or labels produces an inconclusive result, never a pass.

The current last-recording leads of 208.25, 132.4 and 195.9 minutes for B04/B12/B17 are research proxies. Neither physical-failure warning nor nuisance limits are proven. The grouping prototype must receive fresh independent evaluation before promotion; B04/B12/B17 are consumed. UNSW Tests 3/4 remain reserved but do not by themselves resolve event-time labels.

The original capacity aspiration is 1.5 million requests/day with a 9am-3pm peak. Daily average is approximately 17.4 requests/second; peak concentration and timezone still require definition. Agree payload, traffic profile, latency/error limits, retention and recovery targets, then test the full workflow and sustained storage growth. Existing short replay timings do not prove this capacity or a customer SLA.

## Service and commercial boundary

Current authority is a USD 100/month reference-demo ceiling. The recorded Azure estimate is USD 80.4253/month, not a measured bill, hard spending cap or customer service quote. Use the [canonical lifecycle cost model](04-lifecycle-cost-model.md) for assumptions and cost ownership. Customer infrastructure, support and data volumes need a separate scoped estimate before commitment. No additional Azure resources are required to show this package.

The single-node demo has no high availability. Health checks and local backups exist; a private off-host restore was tested, but automated host-loss recovery, primary retention at scale and sustained workload remain open. For a demonstration outage, use the local recorded replay and identify it as offline. For a pilot fault, suspend pilot interpretation and retain evidence; do not substitute an untested detector. Agree support hours, escalation contacts, notification authority, data return/deletion and termination responsibilities in the actual pilot agreement.

## Decision record to complete with the customer

Customer organization / owner: **unassigned**. Intended assets and decision: **unconfirmed**. Data-use and security authorization: **pending**. Acceptance definitions and reviewers: **pending**. Pilot cost and duration: **pending**. Operational and release approval: **not granted**.

This package supports a customer conversation now. Connecting a company is needed for its site-specific pilot evidence and acceptance, not to demonstrate the software and public benchmark research.

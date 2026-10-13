# DME skill completion review

Current Phase 10 preparation: [demo readiness and launch checklist](../customer/10-demo-readiness.md). Locally verified on 2026-10-12: 180 software tests passed, three benchmark selections functionally checked, and synthetic replay completed. Ready for guided offline demonstration; actual review/acceptance and production qualification remain open.

Review date: 2026-10-11. Scope: the authorized private reference system, Azure single-node demo within USD 100/month, and offline detector research. Customer/site production acceptance and independent assurance are not established. The backup export was initially rejected by automatic approval review; the user then explicitly authorized it, and the test passed. The five skill packages are present and listed in this session; their pinned contents were not edited for this increment.

## Current position and verified increment

We remain in Phase 8 engineering with ongoing Phase 9 reviews and a Phase 10 demonstration prepared. Actual customer/site adaptation, validation, ORR/CAR and production authorization are incomplete. Unresolved AIG-G3/G4 evidence prevents AIG-G5 production authorization; no formal approval of earlier gates is implied.

The latest full software run passed [180 tests](../governance/evidence/phase10-demo-tests.xml). [Causal processing and 428-decision replay](../data/qualification/causal-observation-development.md) preserve anomaly observations without suppressing simultaneous signals, but do not fix detector false positives. The [current candidate disposition](../data/qualification/detector-candidate-disposition.md) remains NOT_PROMOTED. SCA cases 1/2/11 are consumed; cases 3-10 remain reserved.

Follow the [current engineering backlog](CURRENT_ENGINEERING_BACKLOG.md): offline intake, adjudication, retention, recovery/workload evidence, detector revision, then site-dependent validation. Customer access is not required to complete every remaining engineering item.

## Current recovery and identity evidence

Local application, Docker and Kubernetes Deployment/PVC recovery passed, including pod replacement, Service DNS/routing, tested ingress/private-egress restrictions and one certificate-verified public HTTPS path. [Local evidence](../governance/evidence/local-network-policy.json). Live real-token inbox and review GET passed; Pulse.Close was absent. [Read-only identity evidence](../governance/evidence/azure-identity-readonly.json).

[Actual Blob recovery](../governance/evidence/blob-container-recovery.json) preserved 3,150 receipts, 884 reference windows and one alert through isolated default-container startup. Review history was absent and closures empty, so nonempty workflow recovery is not established. [Three scheduled service completions](../governance/evidence/azure-backup-cadence.json) span one hour. Neither result qualifies host-loss RTO/RPO, sustained daily capacity or detector acceptance.

The latest explicit authorization covers Azure verification and isolated backup recovery within the existing USD 100/month ceiling, without new paid resources. The write-capable closure verifier was rejected by automatic approval review; read-only checks were used instead. No live review/closure records were appended by that verification.

## Historical customer demonstration preparation

The [customer package](../customer/09-customer-pilot-package.md) and [interactive benchmark demo](../customer/benchmark-demo.html) are prepared for guided discovery. Offline notification grouping preserved the first alert while reducing repeated episodes on three consumed LDM runs; it is not deployed or independently validated. At that increment the suite passed [96 tests](../governance/evidence/customer-readiness-tests.xml). All three demo run selections were exercised in Edge and the rendered page visually inspected. This completes the demonstration package, not customer/site acceptance or every lifecycle gate.

## Earlier fictional-reference increment

The user explicitly authorized inventing fictional customer criteria and notification destination. [Assumptions](../config/fictional-reference-acceptance.json) are labeled fictional. The deployed reference-only route and simulated inbox reproduced all 17 flagged windows in one episode during 884 real benchmark-feature requests; receipt and automated acknowledgement replay were identical. [Live evidence](../governance/evidence/azure-reference-detector-replay.json). The separate qualified-degradation route still reports unavailable. The reference workflow was built and exercised; production/detector acceptance is not complete.

## Applied workflows and evidence

| Skill | Work completed in the reference scope | Remaining condition |
|---|---|---|
| customer-delivery-service-operations | Existing discovery, scope, authority and USD 100 budget retained; technical increments returned through the [execution handoff](../customer/08-deployment-execution.md) | Fictional criteria and simulated inbox are recorded; actual site ORR/CAR and service acceptance are outside the exercised reference scope; future retirement is not an activity to execute now |
| systems-engineering-standards-assurance | Requirement IDs, viewpoints, source/edition limitations and V&V trace preserved; failed and partial evidence recorded without changing acceptance criteria | No independent standards conformity, domain review or site validation; [V&V matrix](../governance/verification_validation_matrix.csv) retains unmet criteria |
| build-production-ai-systems | Authenticated persistent API deployed; asset-specific authorization added and live-tested; local health and half-hour Blob backup timers enabled; actual Blob-to-container restore verified; reproducible baseline tested on IMS runs 2 and 1 | Reference-only detector, durable inbox and acknowledgement deployed and replay-tested; detector qualification, primary-data retention at scale, sustained workload and host-loss recovery remain incomplete |
| ai-governance-and-assurance | Frozen plans, input/code hashes, held-out-use accounting, limitations and non-promotion recorded in the [model card](../governance/model/MODEL_SYSTEM_CARD.md) | Fictional warning/nuisance criteria established; no measured pass against them, qualified detector, production authorization or actual independent review |
| dme-diagram-standard | 20-view package includes rendered and visually reviewed [reference workflow view 17](diagrams/17_reference_detector_workflow.mmd); transparency checked | Diagram consistency does not establish detector qualification; view 16 retains the earlier assessment path and view 17 adds the reference workflow |

No row is an assertion that all lifecycle phases or all requirements have passed. The user authorized execution; missing evidence is not replaced with a fictional approval.

## Earlier technical verification returned

- [84-test suite](../governance/evidence/reference-detector-tests.xml): API, receipt durability, asset denials, manifests, reference workflow, baseline controls and the durable alert ledger/reference API.
- [Azure release verification](../governance/evidence/azure-asset-authorization.json): real token accepted, anonymous 401, cross-asset 403, prior receipt unchanged after rollout, exact release digests. The first immediate post-rollout check failed; subsequent checks passed, and its cause was not established.
- [Periodic host health](../governance/evidence/azure-runtime-health.json): API readiness, ready replica and disk reserve. This does not measure model quality or send external alerts.
- [Run 2 results](../data/qualification/ims-run2-results.md) and [independent-run findings](../data/qualification/ims-independent-results.md): native schema checks and frozen rule, including its missed bearing and archive discrepancy.
- [Backup/restore evidence](../governance/evidence/azure-receipt-backup-restore.json): 3,149 receipts recovered into an isolated database with integrity `ok`; live data unchanged. The private backup is restricted to the current Windows user. Daily on-host backups retain at most seven 50 MiB snapshots; they do not replace off-host disaster recovery.
- Offline repository validation checks links, registers, diagrams and pinned skill hashes. It does not approve a gate.

## Conditions preventing completion

| Condition | Owner / required next evidence | Affected outcome |
|---|---|---|
| Frozen RMS rule missed run-1 bearing 4 | Dr. Moore / model engineering: qualified additional data, revised candidate with new evaluation separation, missed-event and warning-time evidence | Detector release |
| Third IMS archive differs from its README | Dr. Moore / source steward: verified archive identity, correct count/time range and endpoint mapping | Labeled third-run evaluation |
| Unknown units, onset labels and downstream rights | Dr. Moore / source and domain owners: calibration, annotation and permitted-use records | Qualified data and performance claims |
| Fictional acceptance criteria not met | Invented by explicit user instruction: 60-minute warning and no more than one nuisance alert per bearing per 30 operating days; actual evidence remains insufficient or failing | Detector acceptance |
| Full recovery and primary receipt retention | Dr. Moore / engineering: tested host-loss recovery and primary-data retention policy; actual Blob-to-container restore and three consecutive half-hour backup service runs passed; complete host replacement remains unverified | Operational readiness |
| External delivery not in the fictional-demo scope | Simulated maintenance inbox and acknowledgement implemented and cloud-tested; a future real external destination requires specific authority | Future external notifications |
| Retention and sustained workload not qualified | Dr. Moore / engineering: retention decision and full workflow soak with measured storage/latency/cost | 1.5 million requests/day claim |
| Actual site/independent acceptance absent | Qualified domain/release reviewers: applicable ORR/CAR and independent review, with real signatures/evidence | Site/production authorization |

Budget authority remains USD 100/month. No paid resources were added by this increment. Existing spending estimates remain estimates; the Azure budget is not a hard stop. No support ticket, source-owner message or external notification was sent; one simulated inbox event was persisted and acknowledged by the automated reference client.

## Measurement and README handoff — 2026-10-12

Repository-maintenance increment: the [measurement index](../governance/measurements/README.md) and [open KPI plans](../governance/measurements/planned-kpis.md) now bind the README claims to existing evidence and decisions. They are retrospective records, not new model/cloud runs or new acceptance. Definitions and requirement IDs are preserved; reusable skills are external to the project.

Receiving owner: Dr. Douglas Moore, DME engineering lead. Actual independent/customer review remains unassigned. Continue the existing offline review and qualification backlog; obtain missing provenance and authorized site inputs before dependent claims or release decisions. This increment changes no model, threshold, deployment, customer acceptance or production authority.

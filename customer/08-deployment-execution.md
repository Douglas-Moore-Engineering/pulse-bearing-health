# Deployment execution increment

## Deployed reference runtime - 2026-10-11

K3s v1.37.1+k3s1 and the authenticated Pulse assessment API are now deployed on `vm-pulse-k3s`, Standard_D2as_v6, East US 2 zone 1. The pod is Ready and its persistent volume is Bound. A real managed-identity token was accepted, anonymous access returned 401, and an assessment receipt survived a pod restart unchanged. [Live verification](../governance/evidence/azure-api-live-verification.json).

The USD 100/month ceiling enabled this deployment; the 744-hour service estimate is USD 80.4253 with a USD 19.5747 tax/contingency reserve, subject to actual metered usage. [Operator access](../infra/single-node/README.md) uses SSH and loopback forwarding; no public HTTP application endpoint exists. [ADR-011](../architecture/adr/011-single-node-reference-deployment.md) records the implemented architecture. **The full bearing-degradation system remains incomplete:** qualified detection and notifications are unavailable, daily capacity and six-hour peak behavior are not validated, and production/site acceptance remains blocked. Earlier quota/budget blockers describe superseded attempts. No support request was sent.


## Budget update - 2026-10-11

Dr. Moore raised the authorized Pulse deployment ceiling to **USD 100/month**. The existing Azure budget resource `pulse-monthly-50` now tracks 100; its historical name is retained to avoid duplicate budgets. Previous USD 50 decisions are historical. A dedicated two-vCPU host is being evaluated within the revised ceiling. Sending the drafted Azure Support request was not authorized and it remains unsent. [Budget policy](../governance/cloud-budget.json).


## Build continuation - 2026-10-11

Added optional durable single-node assessment receipts, replay consistency and conflicting-window rejection. 68 tests passed; a non-root/read-only container retained its generated receipt across restart. Packaged a private image archive and single-node Kubernetes manifests with SHA-256 hashes; [release evidence](../governance/evidence/single-node-release-package.json). Azure now also has the single-tenant Pulse API identity and a secretless reference caller with only Pulse.Assess. No live token flow has been tested.

Deployment remains incomplete: Azure rejected a two-vCPU Central US Basv2 request with QuotaNotAvailableForResource and an East US 2 Bsv2 request with ContactSupport. [Prepared support request](../customer/AZURE_QUOTA_SUPPORT_REQUEST.md) has not been sent. No paid VM or Kubernetes runtime exists. Qualified detection, notification delivery, storage retention/backup, asset-level authorization and daily capacity validation remain open. The USD 50 ceiling remains binding.


## Live Azure execution - 2026-10-11

Created and verified `rg-pulse-reference` in East US 2 under the authorized subscription. Created the resource-group-scoped `pulse-monthly-50` monthly cost-tracking budget. The budget does not stop billing and has no notification recipients configured. [Resource-group evidence](../governance/evidence/azure-resource-group-created.json). Also deployed `vnet-pulse-reference`, subnet `kubernetes-demo` and `nsg-pulse-reference` with inbound deny and default outbound disabled. [Live inventory](../governance/evidence/azure-live-resource-inventory.json) and [successful deployment](../governance/evidence/azure-foundation-deployment.json) are recorded. No paid compute or qualified alert service is deployed. B2s remains restricted in normal US regions; alternate unrestricted region entries have no verified retail price. East US B2als_v2 is restricted with zero family quota. Earlier no-resource statements describe historical increments.


## Current budget decision ? 2026-10-11

Dr. Moore authorized **USD 50/month** for Pulse. [The recorded budget](../governance/cloud-budget.json) supersedes earlier statements that the ceiling was missing. The six-node AKS proposal is unaffordable and disabled in its deployment script before any Azure call. Its $1,213.62/month partial minimum is retained as rejected sizing evidence. No paid resources were created. Azure budget alerts are not a billing hard cap. A replacement must fit the full service estimate and undergo capacity validation; 1.5 million daily degradation alerts remains an unproven requirement.


PULSE-CHANGE-001 v0.1 · 2026-10-11 · Owner: Dr. Douglas Moore · In progress

The user requested end-to-end implementation and explicitly selected “Authorize Azure access and deployment within limits I provide”, then directed DME to build the configuration. This supersedes the historical design-only request in scope, with a real spending limit still outstanding. The existing account was subsequently verified through read-only Azure access. Historical pre-Azure records remain evidence of their original increment. No fictional budget is spending authority.

Current executable scope includes local implementation, tests, deployment preparation and read-only Azure inspection. Existing tenant/subscription context and live access are verified in [connection evidence](../governance/evidence/azure-connection-check.json). Paid provisioning awaits a spending ceiling and applicable deployment evidence. Reference development is the engineering default from the existing platform plan; actual site exposure, real CMMS writes and equipment control remain excluded. Public source rights and downloaded dataset qualification are not inferred from this change.

## Skill handoff and return evidence

All five DME packages are discoverable in this session. Their entry points and required references have been read. The pinned packages are not being modified.

| Sender → receiver | Existing inputs | Work and expected return |
|---|---|---|
| Customer delivery → standards assurance | Discovery v1.1; PULSE-LCC-001 v0.1; pre-Azure handoff v0.3 | Preserve requirements, fictional assumptions, financial gaps and distinct review authorities; assess the implementation increment |
| Standards / AI governance → engineering | SEMP; requirements register; cloud criteria; AIG controls | Build a bounded offline reference harness; return negative tests, version trace and precise limitations; do not promote gates from fixture tests |
| Engineering → diagram standard | Existing architecture views and four-view backlog | Preserve approved presentation and source semantics when diagrams are changed; no claim that unedited views were restyled |
| Engineering → customer / assurance | Implementation, tests and deployment configuration | Return actual local results, deployment blockers, operator procedures and cloud evidence still needed |

Dr. Moore remains accountable; Codex implements and tests on his behalf. No independent reviewer or customer sign-off is invented. Lifecycle Phase 8 engineering and Phase 9 change review are active; future ORR, CAR, site validation and service activation are not complete.

## Inherited conditions and execution order

1. Build and exercise an isolated reference workflow with generated fixtures, governed input contracts, source digests, group separation, descriptive RMS/kurtosis, explicit capability abstention, evidence and mock human decisions.
2. Prepare Azure platform configuration with identity-based access, private connectivity and no default training/online compute. Validate locally; resolve account, region/policy, network reachability and cost before cloud execution.
3. Qualify authorized actual data and freeze evaluation criteria before learned-model training. Fixture results cannot establish bearing-health performance.
4. Verify the platform, then integrate data/model/application workloads. Run access, recovery, cost and release tests in the authorized environment before promotion.
5. Return exact release evidence for scoped reference review; site rollout remains a separate future decision.

Retain CLOUD-01–10, LCC-OPEN-01–05, all requirement IDs, dataset rights/bytes/labels, independent-review conditions and the existing architecture backlog. CLOUD-10 now means execution limits are incomplete, rather than absence of any user authorization. Unknowns remain BLOCKED until their closure evidence exists.

Account identifiers are verified; spending ceiling and permitted paid workload remain unresolved. Region, resource names and service configuration can be proposed by engineering. Read-only Azure queries succeeded; no cloud job, paid resource creation or deployment occurred in this increment.


## Implementation return ? 0.4.0

Returned to Dr. Moore / customer delivery, standards assurance and AI governance: [local implementation and runbook](../docs/REFERENCE_IMPLEMENTATION.md), [compiled foundation source](../infra/azure/README.md), four new [architecture views](../docs/architecture/README.md), and [bounded validation evidence](../governance/evidence/reference-implementation-validation.json). The 24 automated tests passed on generated fixtures; the end-to-end run persisted three accepted windows, three unavailable evidence records, three simulated decisions and one quarantined invalid record. Backup restoration was tested locally. Bicep 0.48.1 compiled the foundation with no diagnostics. New diagram PNGs have transparent pixels and opaque node content; all four views were rendered and visually inspected.

The V&V matrix records partial fixture exercise without changing acceptance criteria or declaring cloud/model/site gates passed. Standards editions and contractual obligations were not rebaselined; no conformity assessment is claimed. PULSE-LCC-001 remains the sole lifecycle cost model, with all LCC-OPEN-01?05 unresolved. New foundation cost drivers include four private endpoints, five private DNS zones, storage/version retention and monitoring; these are resource counts, not a sourced price estimate.

Next required external input: owner-authorized spending ceiling; the existing tenant/subscription and live read access are verified. Engineering proposes an isolated reference environment, `rg-pulse-reference`, `eastus2` subject to account policy, and no training compute until data and cost qualification. Client private networking, actual scoped roles, monitoring connectivity, cloud policy/what-if, data qualification, models, authenticated application, protected promotion and operational acceptance remain unfinished. No fixture success is a substitute for those inputs or tests. The authored CI workflow is local-test-only; it has not been pushed or run by GitHub.


Repository validation initially identified CRLF checkout conversion in all five pinned skill packages. Each affected file was compared against its Git blob and manifest digest before restoring its exact authored bytes. No skill semantics or manifest hashes changed; `.gitattributes` prevents recurrence.


## Data qualification return - 2026-10-11

Input from Dr. Moore: Zenodo record 10868257 description PDF. Engineering and AI governance reviewed the source license, documented endpoint exceptions, and a bounded B02 archive sample. Returned [qualification review](../data/qualification/ldm-upb-review.md) and [source/inspection manifest](../data/qualification/ldm-upb-10868257.json) preserve the distinction between documented properties, inspected sample bytes and qualified training evidence. DS-LDM-UPB-RTF is a separate candidate from DS-PADERBORN. The B02 sample adapter is implemented and locally tested; [adapter evidence](../governance/evidence/ldm-adapter-validation.json) records 31 passing tests and four profiled channel records. Next work: whole-run adapter qualification, full selected-run integrity, per-run logs/calibration, time/endpoint/censor policy and frozen group splits. CLOUD-02/03 remain BLOCKED; Azure account/spending and other inherited conditions are unchanged. No model or dataset has been promoted.

## IMS qualification return - 2026-10-11

Updated existing DS-IMS using the user-supplied NASA download. Returned [source review](../data/qualification/ims-review.md) and [inspection manifest](../data/qualification/ims-inspection.json), with container integrity distinct from native measurement qualification. Next work is RAR inventory and sample inspection, units/timebase resolution, endpoint/censor review and experiment-aware splits. No training or cloud action occurred; inherited conditions remain open.

## Ferrara source return - 2026-10-11

Registered DS-FERRARA-RTF from the permanent Part 2 page and related Part 1, replacing the supplied expired download signature with stable source references. See [source review](../data/qualification/ferrara-review.md). Native inventory, units, timing and endpoint qualification remain open; no training or gate promotion occurred.

## HUST source return - 2026-10-11

Registered DS-HUST-DIAG version 3 for diagnosis/robustness feasibility after source and primary-paper inspection. See [source review](../data/qualification/hust-review.md). Native inventory, calibration, class mapping and specimen grouping remain open. RUL eligibility is not established. No training, cloud action or gate promotion occurred.

## Kubernetes scope and engineering return - 2026-10-11

Dr. Moore requests Kubernetes for 1.5 million daily bearing-degradation requests and identifies peak hours as 09:00-15:00. Returned [capacity/cost evidence](../docs/AKS_CAPACITY_AND_RELEASE.md), [deployment runbook](../infra/aks/README.md), [ADR-010](../architecture/adr/010-aks-alert-capacity.md) and the new AKS architecture view. Local API and deployment safeguards are tested; Bicep compiled and short loopback load measured. Linux image build and restricted smoke passed; Azure read-only what-if succeeded. No real degradation policy, durable delivery or cloud performance is qualified. Read-only Azure inspection establishes quota/allocation and CLI constraints. Spending ceiling remains requested under prior bounded authorization. No paid resource was created and no skill/gate is falsely marked complete.

## Single-server budget evaluation return

The user selected evaluation of a single-server Azure Kubernetes demo. [Evaluation](../infra/single-node/README.md) proposes K3s on B2als_v2 at $45.16 per 31-day month before tax, including bounded outbound usage and maximum billed E4 transactions. All three inspected B2 candidates are unavailable to this subscription in East US 2. No resource was created. This is an evaluated proposal with unresolved allocation, traffic enforcement and identity, not a deployable or capacity-qualified release. The $50 owner ceiling is recorded and the previous AKS execution path is disabled.

## Returned offline run evidence - 2026-10-11

User instruction: continue through run results. Engineering implemented and exercised an offline exploratory IMS RMS baseline, returning [results](../data/qualification/ims-run2-results.md) and [artifact provenance](../governance/evidence/ims-run2-baseline.json) to Dr. Moore for phases 8?10. All 984 run 2 files passed numerical schema checks. The fixed rule flagged bearing 1 in one episode; other channels did not flag. The three-hour interval to record end is not validated warning lead time. No qualified model was released. Current Azure token/persistence/anonymous-denial checks passed again; the USD 100 ceiling is unchanged and no new resource was created.

Receiving disciplines: customer delivery, technical engineering, standards assurance and AI governance. Preserve PULSE-FR-003 and PULSE-NFR-008 acceptance requirements: independent-run evaluation is still missing. Rights, units, fault-onset labels, detector qualification, notifications, operational recovery and sustained capacity remain open; no gate is approved by this run. Next permitted work is qualification and independent-run evaluation of a frozen candidate under the existing bounded authorization. No external message or site action is authorized by these results.

## Returned reference controls and independent evaluation - 2026-10-11

The user requested completion of the DME workflows. [Completion review](../docs/SKILL_COMPLETION_REVIEW.md) records actual progress and remaining conditions for all five skills. The unchanged baseline missed run-1 bearing 4; the third archive conflicts with its description. Detector promotion is blocked by evidence, not by a missing Azure execution permission.

Asset-level authorization was deployed and verified (valid token, 401 anonymous, 403 unassigned asset, durable replay). Local health and daily bounded backup timers were installed. The user explicitly authorized private off-host backup/restore after automatic approval review required export authority; 3,149 receipts restored with integrity ok. No live data was replaced. A durable alert ledger and acknowledgement component is implemented and fixture-tested offline, without detector integration or external transport. 81 tests passed. USD 100 remains the ceiling; no paid resource was added. No independent reviewer, customer acceptance or production approval was fabricated.

The receiving owner is Dr. Moore. Continue model/data qualification and integration against the unchanged requirement IDs; independent evaluation, acceptance targets, source discrepancy and notification destination require explicit dispositions. [Operational runbook](../runbooks/reference-operations.md) and evidence specify what was actually exercised, including limits on backup size and untested future rotation/host-loss recovery.

## Fictional criteria and deployed reference workflow - 2026-10-11

User instruction: "make it up, this is a fictional customer." Recorded [fictional acceptance criteria](../config/fictional-reference-acceptance.json): 60-minute warning, at most one nuisance alert per bearing per 30 operating days, zero missed documented failures as a target, and a simulated internal maintenance inbox. This authorizes fictional assumptions, not invented measured results or external delivery.

Deployed the explicitly unqualified reference detector/inbox/acknowledgement route. [Cloud replay](../governance/evidence/azure-reference-detector-replay.json) processed 884 verified benchmark-feature windows, reproducing 17 flagged windows and one episode with identical retry receipts and acknowledgement. Sequential p95 was 36.1 ms; daily capacity remains unqualified. [Off-host restore](../governance/evidence/azure-reference-workflow-restore.json) recovered 884 reference decisions and the acknowledged episode in addition to 3,149 original receipts. 84 tests passed. The qualified detector route remains unavailable. Reference demonstration engineering is exercised; production/model acceptance remains blocked by its failed or unresolved criteria.

## Additional LDM-UPB qualification - 2026-10-11

Following the instruction to proceed, inspected bounded documentation members and archive inventories for B03/B04/B11/B12/B17. Recorded a prospective bearing-disjoint partition before downloading these signals. [Findings and limits](../data/qualification/ldm-additional-runs.md). No detector gate advanced, Azure resource changed or external message sent. Full-run integrity, exact vibration-stop criteria and verified healthy exposure remain open.

## KAIST and UNSW development data - 2026-10-11

The user authorized proceeding with both supplied datasets. A prospective experiment-level split reserves UNSW Test 2 for validation and Tests 3/4 for testing. Local acquisition and native checks are recorded in [the qualification review](../data/qualification/kaist-unsw-review.md). UNSW Test 1 has 108 validated native measurements; no detector acceptance or cloud deployment change is inferred. Existing 84 tests pass. Sender: engineering implementation; receiver: Dr. Moore/project engineering owner. Remaining endpoint, healthy-exposure and detector-evaluation conditions stay open. Next activity: develop features and evaluate the candidate protocol on development data before reserved-test access.

## Full KAIST development replay - 2026-10-11

Completed full 129-record profile, explicit missingness policy and exploratory RMS replay. [Results and limitations](../data/qualification/kaist-development-results.md): zero observed lead at 3x; 106 minutes at lower development thresholds. 89 tests passed, reserved experiments untouched, no Azure changes. Engineering returns these development findings to the project owner; detector acceptance and nuisance-alert evidence remain open.

## Cross-dataset threshold comparison - 2026-10-11

Engineering compared 1.5x/2x/2.5x/3x RMS thresholds on consumed IMS and UNSW development data, alongside KAIST results. [Evidence and candidate](../data/qualification/development-threshold-comparison.md). The 1.5x candidate catches the previously missed IMS bearing but adds unlabeled alerts. Original 3x IMS results reproduced exactly. Owner handoff: freeze endpoint and timing interpretation before reserved validation access. No deployment change or acceptance claimed.

## Frozen candidate validation - 2026-10-11

Engineering executed the frozen 1.5x candidate on LDM B04 and UNSW Test 2 after publisher checksum verification. [Protocol, results and limitations](../data/qualification/rms-v2-validation.md): B04 208.25 minutes to final acquisition, 663 flags/3 episodes; UNSW 41 flags/2 episodes with no scorable warning minutes. 92 tests passed. No retuning, reserved-test access, Azure changes or external messages. Owner handoff: qualify endpoint and healthy-condition evidence before final-test scoring or release; no acceptance gate promoted.

## Final LDM research test and disposition - 2026-10-11

Engineering completed the frozen 1.5x candidate research test on B12/B17 after whole-archive checksum verification. [Final results](../data/qualification/rms-v2-final-research.md): 132.4/195.9 minutes to last acquisition, 26/9 episodes. No retuning; 92 software tests and repository validation passed. Candidate NOT PROMOTED: endpoint and verified-healthy evidence remain insufficient; repeated episodes raise a stability concern. LDM final runs are consumed; UNSW 3/4 remain reserved. No Azure or external-messaging change. Owner handoff: acceptance evidence qualification and a separately versioned stability/condition-aware development revision before any new release decision.

## Customer demonstration preparation - 2026-10-11

Prepared the [guided demo and pilot package](09-customer-pilot-package.md), with a self-contained benchmark replay, scope, responsibilities, intake and acceptance conditions. Notification grouping is offline development on consumed runs; the deployed detector remains unchanged. 96 tests passed; Edge exercised all three selections and the rendered view was inspected. No resources, external notifications or site connections were added. Actual pilot authorization, labels and sustained workload/recovery evidence remain open.

## Detector endpoint audit - 2026-10-11

Implemented and tested uncertainty-aware endpoint and descriptive nuisance scoring. [Evidence and limitations](../data/qualification/detector-gap-resolution.md). Published LDM stop logs provide conditional warning comparisons, not physical-failure labels. 103 tests passed. Thresholds, consumed splits, deployed reference rule and acceptance targets are unchanged; NOT_PROMOTED. Next work requires qualified event/healthy-exposure labels and prospective independent evaluation.

## SCA dataset qualification - 2026-10-11

[Initial SCA review](../data/qualification/sca-review.md): case 1 files verified and native labels inspected. Labeled normal/fault snapshots are useful, but chronology, cadence and operating-exposure limits require a separate frozen diagnostic protocol. Cases 2-11 signals remain untouched. No performance or promotion claim.

## SCA case 1 diagnostic result

[Frozen diagnostic experiment](../data/qualification/sca-case1-results.md) detected only 1/117 fault snapshots; no positives on 126 normal snapshots. This exposes RMS sensitivity failure, not warning qualification. Retrospective reference chronology and sparse cadence are explicit. Next development is spectral/speed-aware feature investigation on case 1; other cases remain reserved. No cloud change or promotion.

## Envelope-feature development

[SCA case 1 investigation](../data/qualification/sca-spectral-development.md) improves known-inner-ring snapshot sensitivity to 112/117 with 7/126 normal positives. All feature and frequency-hypothesis results are retained. Synthetic modulation discrimination and Nyquist exclusion checks passed. No independent validation, cloud change or promotion; cases 2-11 remain reserved.

## Frozen SCA envelope evaluation

[Cases 2/11 results](../data/qualification/sca-envelope-validation.md): 91/94 fault snapshots detected in case 2 but 129/296 normal positives; case 11 produced 1/38 bearing-positive snapshots. Candidate NOT_PROMOTED. Frozen hashes and publisher checks passed. Frequency physics, asset independence and operating exposure remain unresolved. Cases 3-10 remain reserved; next step is false-positive analysis on consumed data, not further holdout consumption.

## SCA false-positive attribution

[Consumed-case analysis](../data/qualification/sca-false-positive-analysis.md) exactly reproduced prior normal classifications. Case 2 false positives occur at the same recorded RPM as calibration; speed gating alone cannot fix them. Case 11 strict speed gating would abstain on all observations, not improve measured specificity. No thresholds, reserved cases or deployed code changed.

## Spectral/reference shift investigation

[Case 2 comparison](../data/qualification/sca-spectral-shift.md) found increased target and background power on normal-labeled test data relative to calibration. Aggregate background collapse does not explain the positives; physical cause and localization remain unresolved. Frozen detector unchanged; cases 3-10 reserved.

## Localization feasibility

[Metadata/timing audit](../data/qualification/sca-localization-feasibility.md) confirms different DS/FS bearings in case 2 and the folder-11/native-id-14 mapping. Only 91/296 case-2 FS test observations pair mutually within 60 seconds; future paired inference must report coverage loss. Load/mounting and physical transmission remain unknown. No reserved cases or detector configuration changed.

## Paired-sensor development

[Consumed-case experiment](../data/qualification/sca-paired-development.md) reduces case-2 normal positives from 72 to 3 on identical paired records, while fault detections decline from 89 to 86. 205 normal-side records abstain; coverage, causal pairing and simultaneous faults remain unresolved. No reserved data or deployment change.

## Candidate disposition

[Final consumed-case check and decision](../data/qualification/detector-candidate-disposition.md): case 1 paired rule detects 98 fault snapshots, misses six and abstains on 13. No production promotion; material coverage and operational-validation gaps remain. This closes the candidate experiment increment, not the production objective. No new Azure deployment.

## Causal observation implementation

[Offline causal context](../data/qualification/causal-observation-development.md) now preserves both sensor anomalies and explicitly handles missing/stale partners without future data. 107 tests passed. This is not a qualified localization detector and does not inherit earlier paired-rule accuracy. No API deployment or reserved-data consumption.

## Causal replay evidence

[428-decision replay](../data/qualification/causal-observation-development.md) preserved all frozen anomaly outputs. Case 2 FS has preceding partner context for only 12/296 observations; all 129 normal positives remain. Processing integrity improved, not detector accuracy. No reserved-data consumption or deployment.

## Engineering status reconciliation

[Skill completion review](../docs/SKILL_COMPLETION_REVIEW.md) now separates the current 107-test milestone from historical 84/96-test evidence. [Prioritized backlog](../docs/CURRENT_ENGINEERING_BACKLOG.md) separates immediately implementable intake/adjudication/retention work from customer-dependent validation. No gate, detector or cloud resource changed.

## Offline intake validation

[Read-only validator](../runbooks/offline-intake.md) implemented against the existing window contract with metadata references, finite-value/UTC checks and bounded input. 115 tests passed. Structural validity remains pending actual authority/calibration/source review; no customer data, managed quarantine or cloud ingestion was introduced.

## Local adjudication ledger

[Reviewer assertion history](../runbooks/adjudication.md) now preserves original reviews and append-only corrections, rejects stale/cross-subject updates and requires evidence references for resolved assertions. 119 tests passed. Reviewer identity and evidence remain unverified assertions; no API integration or production approval is implied.

## Retention planning implementation

[Read-only inventory and planner](../runbooks/retention-planning.md) retain unknown holds, dependencies, reviews and timestamps; eligible old records require owner review and never authorize deletion. 129 tests passed. Existing receipt insertion times remain unavailable; no live database access, migration or deletion occurred.

## Local component integration and recovery

[Synthetic exercise](../runbooks/local-pilot-exercise.md) validated 1,000 intake windows and restored all 1,100 review rows identically. Retention retained 900 unresolved subjects and marked 100 for review without deletion. An initial Windows cleanup failure was fixed by closing SQLite handles; rerun passed. These are local harness results, not Azure host-loss or production throughput qualification.

## Authenticated component API integration

[Local routes](../runbooks/pilot-api-integration.md) now validate asset-authorized intake and store caller-scoped review histories under an additional Pulse.Review role. Identity comes from verified claims, not request body. Routes are opt-in and not deployed; actual reviewer role provisioning and human delegation remain open.


## Pilot API rollout ? 2026-10-12 UTC

Following explicit user reauthorization, the pilot API was deployed to the existing reference VM without adding paid resources. Server validation and rollout passed; live assessment/intake and pre/post backup recovery passed. Pulse.Review is assigned but absent from the cached managed-identity token; live review creation and review recovery remain pending. See [rollout record](../runbooks/pilot-api-integration.md). No detector or production acceptance gate was promoted.


## Requirement-directed reconciliation increment

PULSE-NFR-002 / VV-014 now has timezone-aware local fleet reconciliation and negative/boundary tests. Full software suite: 139 passed. [Runbook and limitations](../runbooks/daily-reconciliation.md). No live scheduler or deadline compliance is claimed. One-hour RPO, production availability and daily capacity remain open; the single-node resource inventory is not full requirements acceptance.


Commit-evidence prerequisite: new local API code records post-commit timestamp bounds without changing receipt responses or backfilling historical receipts. 141 tests passed. Deployment and reconciliation integration remain open; [evidence semantics](../runbooks/daily-reconciliation.md). No production gate changed.


Database reconciliation integration: read-only tenant/caller-scoped reports now distinguish unknown historical timing from uncertain post-deadline bounds. Existing private backup exercise returned TIMING_UNKNOWN for both synthetic assets. 143 tests passed. No live scheduler or deadline acceptance claimed; [runbook](../runbooks/daily-reconciliation.md).


Azure reconciliation deployment completed: new image, fictional 12-asset timer, persistent reports and host health checks installed. Manual execution and receipt/commit-evidence backup recovery passed. Scheduled run observation and full NFR-002 acceptance remain pending. [Deployment evidence](../runbooks/daily-reconciliation.md).


Half-hour backup increment: deployed :00/:30 UTC local snapshots, 48-snapshot bound and 45-minute freshness monitoring. Initial backup and installed health checks passed. PULSE-NFR-005 remains unmet for host loss because off-host backup is manual. [Operations evidence](../runbooks/reference-operations.md).


Detector performance specification: [derived criteria DET-PERF-001?007](../requirements/detector-performance.md) preserve the fictional 60-minute/zero-miss/one-nuisance targets and propose explicit coverage and evidence minimums. No candidate results or release gates changed; full acceptance evaluator remains to be implemented.


Detector evidence consolidated: separate hash-bound RMS and paired-SCA dossiers were evaluated against detector-performance-v1. RMS is INCONCLUSIVE for full acceptance; its documented missed bearing is preserved. Paired SCA FAILS coverage/causal-protocol checks. This is retrospective gap assessment, not prospective validation. [Current detector status](../data/qualification/DETECTOR_STATUS.md). No new holdout consumption or promotion.


Feature separation increment: consumed-case score quantiles and threshold tradeoffs recorded. Baseline counts reproduced for all three cases. No threshold selected, no reserved data consumed, and no production promotion. [Report](../data/qualification/sca-feature-separation.md).


Consumed SCA reference feasibility audited from six publisher-hash-verified files. Later healthy references and sensor/period confounding remain; no random-window independent validation claim is supportable. [Findings and next experiment constraints](../data/qualification/sca-reference-feasibility.md). No holdout access, training or promotion occurred.


Chronological reference audit reproduced LDM B04/B12/B17 early medians and strict reference-before-monitoring order. B17 selected for descriptive causal trend development only; no healthy/failure qualification or holdout claim. [Audit](../data/qualification/chronological-reference-audit.md).


B17 causal trend experiment completed with prewritten development parameters: 1 episode versus baseline 9; descriptive first-alert lead 193.42 versus 195.90 minutes. Full suite 158 passed. No operational acceptance claim or deployment. [Evidence](../data/qualification/b17-trend-development.md).


Fixed trend settings transferred to consumed B04/B12 without retuning; episodes reduced to one with later first alerts and longer flagged runs. Exact B17 decision regression passed. [Transfer report](../data/qualification/trend-transfer.md). No operational acceptance or deployment change.


Trend temporal tests completed: short-pulse filtering, delayed eight-record-pulse flag, step onset/clearance, gap boundary and two-channel continuation verified. 166 software tests passed. [Lifecycle semantics and evidence](../data/qualification/trend-temporal-characterization.md). No runtime deployment or gate promotion.


Incident lifecycle increment: durable explicit closure added to the existing alert ledger, requiring prior acknowledgement and actor/rationale/evidence. 168 tests passed. Not deployed; authenticated closure integration and closure-specific recovery remain open. [Runbook](../runbooks/incident-lifecycle.md).


Skill handoff ? incident API integration: authenticated closure route and scoped role checks implemented locally; 169 tests passed. Backup comparison now covers closure rows with an explicit nonempty guard. Build/governance boundaries retained: no live role assignment, deployment, real maintenance disposition or model promotion in this increment. [Handoff details](../runbooks/incident-lifecycle.md).


Incident closure deployed October 11 Eastern: image/server validation, receipt regression and private recovery passed. Role assigned but current token lacks review/closure claims; live closure correctly denied. No live incident closed; nonempty closure recovery pending. [Rollout handoff](../runbooks/incident-lifecycle.md).


Off-host backup installed within the $100 ceiling: bounded Hot LRS ring, managed identity, readback and isolated recovery of 3,150 receipts passed. New low-cost storage resource added; initial container-command failure corrected. [Evidence and cost assumptions](../runbooks/offhost-backup.md). Timer cadence and full host-loss RPO remain unqualified.

## Scheduled backup verification ? October 11, 2026 Eastern

The 9:30 PM Eastern systemd run uploaded and read back a 4,677,632-byte snapshot and restored 3,150 receipts with SQLite integrity OK. [Recorded scheduled run](../governance/evidence/azure-offhost-backup.json). This is one observed automatic execution, not sustained one-hour RPO or complete host replacement. Live review/closure remained denied by the token role set at the subsequent check; no nonempty live review/closure recovery is claimed.

Offline upload-outage, corrupted-readback, invalid-database and retry checks passed with the complete suite: [173 tests](../governance/evidence/offhost-backup-tests.xml), one existing dependency deprecation warning. No production gate or detector qualification is promoted. Next recovery evidence requires booting an isolated recovered application and checking receipt/workflow consistency; cloud actions remain subject to the current explicit authorization boundary.

## Isolated application recovery increment

The [local recovery exercise](../runbooks/local-pilot-exercise.md) now restores a synthetic database into a fresh ASGI application after making the source path unavailable. Receipt replay, corrected review history, explicit closure, conflict detection and authorization boundaries passed. Full software suite: 174 passed; one existing dependency deprecation warning. This is in-process application recovery using synthetic identity claims, not Azure host replacement or live identity verification. Production recovery and detector gates remain unchanged. Next recovery work is an isolated process/container exercise with explicit runtime configuration and restoration from an authorized backup.

## Separate-process recovery evidence

Extended the existing synthetic application recovery test to launch a fresh Python interpreter against the restored database after the original path becomes unavailable. Readiness, persisted receipts, review corrections, closure replay and authorization denials passed. Full suite: 174 passed, one existing dependency warning; evidence in `governance/evidence/application-recovery-tests.xml`. No Azure connection or provisioning was performed in this increment. ASGI TestClient and synthetic identities remain the test boundary; container/network recovery and production RTO/RPO are not established.

## Loopback HTTP recovery verification

The restored-process probe now starts Uvicorn on an ephemeral loopback-only socket and verifies readiness, receipts, corrected reviews, closure replay and access-control denials using actual HTTP requests. Explicit startup/request/shutdown/process timeouts bound the exercise. The full suite passed: 174 tests, one existing dependency warning. The [recovery runbook](../runbooks/local-pilot-exercise.md) consolidates current and historical evidence. This supersedes the child probe's ASGI TestClient-only limitation, while synthetic identity, container, external network, cloud restoration and RTO/RPO boundaries remain unchanged. No Azure access occurred.

## Local container recovery

The opt-in recovery test passed in the existing incident-closure image with the image's non-root user, no external network, read-only root filesystem and resource bounds. Restored synthetic receipts, corrected reviews, closure replay and authorization denials passed over internal HTTP. [Focused test evidence](../governance/evidence/container-recovery-tests.xml). The probe overrides the production command and uses synthetic identity; full deployment configuration, Entra and Azure host recovery remain open. No cloud access, detector promotion or production acceptance occurred.

## Default container command and configuration

Extended the focused recovery test to run the image's unmodified CMD with synthetic identity UUIDs, explicit asset grants, restored storage and pilot/reference settings. Readiness passed; the production verifier rejected anonymous and malformed bearer tokens with 401. The isolated test container was removed. [Updated focused evidence](../governance/evidence/container-recovery-tests.xml): one passed, one existing dependency warning. Successful Entra authentication and actual Azure/Kubernetes host recovery remain open. No Azure connection or production gate change occurred.

## Recovery configuration failure checks

The focused container recovery test passed valid restoration/startup plus two negative default-command cases: missing tenant ID and missing pilot review database. Both failed with a nonzero exit and the expected missing-key error. Each test container was removed. Updated evidence: `governance/evidence/container-recovery-tests.xml`; one focused test passed, one existing dependency warning. The status summary now consolidates local recovery evidence. Remaining work requires real identity, Kubernetes configuration and authorized off-host restoration evidence; no Azure access or acceptance promotion occurred.

## Kubernetes-rendered configuration compatibility

Removed the independently maintained environment configuration from the default-command recovery test. It now consumes the single-node renderer's ConfigMap and volume mount and restores the database at `/data/assessments.db`. Combined local recovery/manifest checks: five passed, one existing dependency warning. Evidence: `governance/evidence/container-recovery-tests.xml`. Kubernetes scheduling, real PVC behavior, kubelet probes, network policy and actual identity remain outside the test. No cloud access or gate promotion occurred.

## Local Kubernetes storage evidence

On loopback-only Docker Desktop Kubernetes, a temporary 16 MiB local-path PVC preserved a generated marker across pod replacement. Namespace cleanup completed. [Evidence](../governance/evidence/local-kubernetes-storage.json). Two initial writer failures were caused by a missing utility-image `sync` command; the corrected built-in-only test passed. This is PVC persistence evidence, not power-loss durability or full application recovery. The node lacks the Pulse image, so application/container results remain separate. No Azure access, deployment or gate promotion occurred.

## Local Kubernetes application recovery ? passed

Resolved the image-import blocker by directly addressing Docker Desktop's hidden node container and importing the verified Pulse archive into containerd. The focused recovery test passed after copying a synthetic restored database onto a PVC, deleting its first pod and verifying application behavior in a replacement pod. Receipt replay, review corrections, closure replay and authorization denials passed over internal HTTP. Temporary namespace cleanup passed. The initial cleanup timeout was corrected with bounded helper termination and command timeouts; [rerun evidence](../governance/evidence/kubernetes-application-recovery-tests.xml) records one focused pass. Production command rollout in Kubernetes, real identity and Azure host restoration remain unverified. No Azure connection or production gate promotion occurred.

## Rendered local Deployment recovery

Applied the renderer's Deployment, ConfigMap, ServiceAccount and Service in the isolated local namespace, adapting only namespace and PVC reference. The default command reached readiness before and after pod replacement; health endpoints, anonymous rejection, SQLite integrity and restored receipt count passed with a different pod UID. Cleanup completed. Focused exercise: one passed, one existing dependency warning; 63.30 seconds total harness time, not an RTO claim. Real identity success, Service routing, NetworkPolicy, Azure backups and host-loss recovery remain unverified. No cloud access or production gate promotion occurred.

## Local Service routing evidence

Following pod-replacement recovery, a separate local client pod resolved the Service DNS name to its ClusterIP and verified health HTTP 200 and anonymous inbox HTTP 401 through both addresses. The focused recovery test passed including cleanup: one passed, one existing dependency warning. Evidence: `governance/evidence/kubernetes-application-recovery-tests.xml`. NetworkPolicy was absent in this test; no deny-policy, external ingress, real identity or Azure host-loss claim follows. The project status now consolidates local recovery increments. No Azure access occurred.

## Local deny-ingress verification

After proving baseline Service routing, applied the rendered NetworkPolicy in the temporary local namespace. Three fresh client-to-Service attempts failed; the target API remained healthy and its restored receipt passed verification. Cleanup completed. [Evidence](../governance/evidence/local-network-policy.json); [focused test](../governance/evidence/local-network-policy-tests.xml): one passed, one existing dependency warning. This is limited ingress-path evidence, not egress, all-path isolation or Azure verification. No production gate promotion occurred.

## Local outbound policy and DNS evidence

The combined recovery/policy test passed. A local TCP 8080 target was reachable before policy; three restricted API attempts timed out afterward while an unrestricted pod still reached it. DNS resolution remained available from the restricted API. Ingress denial and cleanup also passed. Updated evidence: `governance/evidence/local-network-policy.json` and `local-network-policy-tests.xml`. This does not establish private TCP 443 exclusion, public HTTPS allowance or cloud enforcement. No Azure access or gate promotion occurred.

## Private TCP 443 policy verification

Extended the local target to TCP 443 while retaining 8080. Three restricted attempts on each port timed out after policy; baseline and unrestricted control requests succeeded on both. DNS, ingress, recovery and cleanup passed in the same focused run. Evidence: `governance/evidence/local-network-policy.json` and `local-network-policy-tests.xml`. The target used plaintext HTTP; no TLS, public HTTPS, all-CIDR or Azure enforcement claim follows. No cloud access or gate promotion occurred.

## Public HTTPS allowance verification

From the policy-restricted local API pod, a public Python documentation request succeeded with certificate verification, global DNS-address checks and proxies/redirects disabled. The combined recovery/network test passed including cleanup. Updated network evidence is in `governance/evidence/local-network-policy.json`; full offline suite refreshed separately: 174 passed, one existing dependency warning. This is one public HTTPS endpoint, not successful Entra authentication or all-path network assurance. No Azure access or release-gate promotion occurred.

## Authorized Azure read-only verification and Blob recovery

The user explicitly authorized reconnecting to the existing reference deployment for Entra verification and isolated backup recovery, within the USD 100 ceiling and without new paid resources. Read-only checks observed Pulse.Assess and Pulse.Review; inbox/review GET returned 200. Pulse.Close was absent and reviews were empty. [Identity evidence](../governance/evidence/azure-identity-readonly.json).

The actual latest recorded Blob restored into a private local container with 3,150 receipts, 884 reference windows and one alert, preserving counts through default startup/readiness. [Recovery evidence](../governance/evidence/blob-container-recovery.json). Review-table absence and zero closures are explicit limitations. No live mutation or new resource occurred. Automatic approval review rejected the earlier closure-verifier invocation because it could append immutable records; the task proceeded through read-only checks instead. Full host-loss recovery and nonempty workflow-history recovery remain open.

## Repository reconciliation and backup cadence

Updated README, project status, skill review and current backlog to reflect 174 offline tests, local Kubernetes/network evidence, successful real-token review reads and actual Blob-to-container recovery. Preserved pending closure permission, nonempty workflow recovery, host-loss RPO/RTO, capacity and detector/site gates. Read-only VM journal inspection confirmed scheduled service success at 9:30, 10:00 and 10:30 PM Eastern on October 11, 2026. [Cadence evidence](../governance/evidence/azure-backup-cadence.json). Three completions over one hour are not long-term reliability or accepted-record RPO qualification. No live mutation or additional cloud resource occurred.

## Read-only verification tooling and capacity preparation

Added `infra/single-node/verify-live-readonly.py`, executed through pinned SSH without remote installation. Authenticated inbox/review GET returned 200; anonymous GET returned 401. Pulse.Close remains absent and reviews empty. Two offline safeguards passed, verifying GET-only requests, no bodies, no token output and preservation of a review-denial result. [Tests](../governance/evidence/readonly-verifier-tests.xml). This is two focused tests in addition to the previously recorded 174-test full suite, not a newly executed 176-test full suite.

Prepared the [sustained capacity protocol](../runbooks/sustained-capacity-protocol.md). Existing 20-second live load tooling writes durable receipts and was not executed under read-only authorization. The six-hour concentration assumption, storage/backup limits, metrics, stop conditions and required execution authorization are explicit. No live database changes or new cloud resources occurred.

## Bounded local capacity smoke result

Implemented and ran a 60-second loopback synthetic assessment load at 70 offered requests/second with isolated temporary storage. Of 4,200 offered slots, 2,462 completed successfully and 1,738 were dropped by scheduler/queue bounds. Successful throughput was 40.62/second and successful p95 437 ms; persisted receipt count and SQLite integrity matched. Temporary storage was removed. [Evidence](../governance/evidence/local-capacity-smoke.json). The target rate was not sustained; no capacity acceptance follows. This shared-host synthetic run excludes real Entra, full workflow and Azure conditions. No cloud load or live database write occurred.

## Separate-process capacity diagnostic

Moved the local test API to a spawned process and classified drops while preserving the 70/second, 60-second, 4,096-sample workload. Result: 2,636 successful, zero submitted failures, 716 scheduler-late drops and 848 queue-full drops; 43.49 successful requests/second and 407 ms successful p95. Receipt reconciliation and temporary cleanup passed. [Evidence](../governance/evidence/local-capacity-isolated-process.json). This is a single same-host diagnostic, not proof of server-only capacity or a meaningful production improvement. No Azure load, live mutation or gate promotion occurred.

## Capacity timing decomposition

Added harness-only timing of client queue/JSON/HTTP, server handling and store-save duration. The 60-second run completed 2,587 successful persisted requests at 42.56/second, with 1,613 dropped slots. Mean store save was 170.95 ms of 182.62 ms handler time; client queue mean was 525.23 ms. [Evidence](../governance/evidence/local-capacity-timing.json). This supports investigating persistence costs but does not distinguish locking, setup and commit I/O. Historical worker-response percentiles exclude queue wait. No production code/durability change, Azure load or gate promotion occurred.

## Storage operation diagnostic

Instrumented only the local capacity harness, preserving production transaction behavior. The run reconciled all 2,360 submitted receipts with integrity OK and cleaned temporary storage. Achieved 38.80 requests/second; 1,840 offered slots dropped. Repeated PRAGMA and acquisition/INSERT boundaries dominated measured store time; both commit/context exits totaled only 5.78 ms per receipt. [Evidence](../governance/evidence/local-capacity-storage-timing.json) and [interpretation/next experiment](../runbooks/sustained-capacity-protocol.md). No production change, cloud access or release promotion occurred.

## Connection-reuse candidate verification

Added an opt-in, local-only bounded connection pool to the capacity harness; production remains unchanged. Six focused tests passed across experimental and existing storage behavior. Candidate/control runs reconciled 3,374/2,408 receipts and matching commit-evidence rows, with zero submitted failures. Candidate measured 56.23/second and 54.40 ms worker-response p95 versus control 39.59/second and 501.01 ms. Candidate had no queue-full drops but 826 scheduler-late drops. [Comparison, evidence and next work](../runbooks/sustained-capacity-protocol.md). No cloud activity, deployment or capacity/release gate promotion occurred.

## Local scheduling and failure-handling increment

Added opt-in retained scheduling slots and schedule-to-completion measurements to the bounded local harness. Failed pooled connections are discarded; nine focused tests passed including setup, commit and post-receipt evidence-write failure behavior. Candidate run completed all 4,200 offered requests with matching receipt/evidence counts, zero failures/drops and 227.86 ms scheduled-to-completion p95. [Run evidence](../governance/evidence/local-capacity-retained-slots.json), [tests](../governance/evidence/local-capacity-pool-failure-tests.xml), [scope and next work](../runbooks/sustained-capacity-protocol.md). Production code is unchanged; no cloud access or gate promotion occurred.

## Capacity repeat and longer bounded run

Repeated the unchanged one-minute experiment successfully (4,200 requests, no drops/failures, 203.43 ms scheduled-to-completion p95). Added only bounded 60/180-second duration selection to the harness and ran three minutes: 12,560 successful persisted receipts/evidence rows, 40 queue-full drops, zero submitted failures, 335.65 ms scheduled-to-completion p95. Integrity/cleanup passed. [Longer-run evidence](../governance/evidence/local-capacity-three-minute.json) and [comparison/limitations](../runbooks/sustained-capacity-protocol.md). Nine focused tests and repository checks passed. The longer result prevents promotion to sustained no-drop capacity; no production or cloud changes occurred.

## Interval-level capacity diagnostic

Implemented ten-second scheduled-arrival cohorts in the local harness. With no concurrent test suite, 12,584 requests succeeded and 16 slots dropped; all drops were in the 70-80 second cohort, whose pending count reached 32 and schedule-to-completion p95 reached 580.01 ms. Receipt/evidence reconciliation, integrity and cleanup passed. [Evidence](../governance/evidence/local-capacity-intervals.json). This localizes an intermittent saturation episode without proving its cause. Next evaluate serialized writes experimentally; no production/cloud change or capacity gate promotion.


## Capacity experiment and repository consolidation

Serialized local writes completed 12,600 requests in the three-minute offered workload with zero drops/failures and 61.81 ms scheduled-to-completion p95; receipt/evidence reconciliation and integrity passed. [Evidence](../governance/evidence/local-capacity-serialized.json). The candidate remains harness-only.

Consolidated current guidance into [project status](../PROJECT_STATUS.md), [engineering backlog](../docs/CURRENT_ENGINEERING_BACKLOG.md) and [capacity status](../docs/CAPACITY_STATUS.md), linked from README. Previous status/backlog snapshots and all experiment evidence are preserved; historical next steps no longer compete with the current backlog. Nine focused tests and repository consistency checks passed. No gate promotion, deployment, commit or push is claimed.


## Serialized persistence repeat disposition

The identical local three-minute repeat completed 12,537 requests with 63 queue-full drops and 347.19 ms scheduled-to-completion p95. No submitted failures; receipt/evidence counts, integrity and cleanup passed. [Evidence](../governance/evidence/local-capacity-serialized-repeat.json). The earlier zero-drop result did not repeat; production adoption is deferred pending controlled generator/server measurements. Current disposition updated in [capacity status](../docs/CAPACITY_STATUS.md); no cloud or production change occurred.


## Client/server CPU measurement

Added one-second per-process CPU measurements to the local harness. The one-minute diagnostic completed 4,029 requests with 171 drops; submitted receipts/evidence reconciled and integrity/cleanup passed. API averaged 0.972 logical CPUs versus client 0.392, providing a lead for API profiling without proving root cause. [Evidence](../governance/evidence/local-capacity-cpu-diagnostic.json). Production unchanged; see current capacity status for disposition.


## Phase 10 demo-readiness handoff, 2026-10-12

Completed full local suite (180 passed), three benchmark-selection functional checks and executable synthetic replay. [Launch, evidence, claims and fallback](10-demo-readiness.md). Ready for a guided offline reference demonstration; meeting disposition, actual customer acceptance and production gates remain open. No Azure connection, deployment or production performance promotion was performed.

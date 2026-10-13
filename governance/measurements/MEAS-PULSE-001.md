# MEAS-PULSE-001 — Snapshot receipt recovery

Record v1 · recorded 2026-10-12 (America/New_York). Retrospective documentation of existing evidence; no new execution.

## Identity and trace

| Field | Value |
|---|---|
| Measurement ID / version / recorded date | MEAS-PULSE-001 / v1 / 2026-10-12 |
| KPI definition / version | PULSE-KPI-012; [dictionary v1](../../docs/appendix-a-kpi-dictionary.md) |
| Business need | [PULSE-R07: continuity and recovery](../../customer/01-discovery-record.md) |
| Requirements / implementation | [PULSE-NFR-004 / PULSE-NFR-005](../../requirements/requirements.csv); receipt preservation is only a supporting check, not either RTO/RPO acceptance; [scripts/recover_offhost_snapshot.py](https://github.com/Douglas-Moore-Engineering/pulse-bearing-health/blob/a00b3134366c6b157c081e9a54b8d6e7fa7cb7f4/scripts/recover_offhost_snapshot.py) |
| Acceptance criterion / protocol | Existing report `result=PASS` and `counts_preserved_after_startup=true`; equality of snapshot and restored receipt counts |
| Protocol fixed date / approval state | Historical operational test. The report does not retain a separately dated pre-test protocol approval; this normalization does not invent one. |
| Related / supersedes | First normalized measurement record; preserves the original evidence and decisions, supersedes no run. |

## Definition, baseline and method

| Field | Value |
|---|---|
| Definition / formula / direction | Restored API-assessment receipts / receipts in the selected backup; higher preservation is better. |
| Unit / numerator / denominator | Receipts; numerator 3,150; denominator 3,150. |
| Baseline / evidence | The selected backup contains 3,150 receipts; no measured service RPO/RTO baseline. |
| Target / acceptance threshold / status | Exact count preservation for this snapshot only. Candidate host-loss targets remain four hours RTO and one hour RPO, unqualified. |
| Population / inclusion / exclusions | One actual reference-deployment backup. Also contains 884 reference windows and one alert; reviews are absent and closures empty. |
| Independent unit / sample size / exposure | One snapshot/recovery exercise, not 3,150 independent recovery trials. Customer operating exposure not available. |
| Time window / source clock | Backup uploaded 2026-10-12T02:30:00.781099+00:00; observed restore 2026-10-12T02:46:26.322701+00:00. These timestamps do not measure end-to-end RTO. |
| Comparator / split / leakage controls | Compare restored database counts before/after default container startup with the selected snapshot. No model training split applies. |
| Aggregation / uncertainty method | Exact finite snapshot counts; no sampling interval applicable. One exercise cannot establish recovery reliability or sustained cadence. |

## Result and scope

| Field | Value |
|---|---|
| Measurement status | measured |
| Observed result / context | 3,150 / 3,150 receipts preserved after startup. Reported PASS for this isolated restore. |
| Uncertainty estimate | Exact finite snapshot counts; no sampling interval applicable. One exercise cannot establish recovery reliability or sustained cadence. |
| Evaluation date / environment / data origin | 2026-10-12 UTC; Azure Blob source to an isolated local container; reference application records, not real customer maintenance outcomes. |
| Representativeness / limitations | No Azure host replacement, live authenticated workflow recovery, nonempty review/closure recovery, production RTO or RPO established. |
| Operational intervention / actor / time | Not applicable to this engineering/benchmark result; no customer maintenance or process intervention is evidenced. |
| Follow-up outcome / attribution | Customer outcome not measured. No avoided-loss, downtime, yield, scrap or causal-benefit attribution. |
| Financial impact basis | Not applicable; this record makes no financial-impact claim. |
| Validity / remeasurement trigger | Applies only to the bound historical artifacts. Material changes to code, model, data, configuration or operating context require a new record. |

## Evidence and reproduction

| Field | Value |
|---|---|
| Run / immutable report | [governance/evidence/blob-container-recovery.json](https://github.com/Douglas-Moore-Engineering/pulse-bearing-health/blob/a00b3134366c6b157c081e9a54b8d6e7fa7cb7f4/governance/evidence/blob-container-recovery.json); SHA-256 `1fbfb1a976656d5a5b1f848ac97cb28f9408511c3fd645bc58c82405c44dfd3c` |
| Data snapshot / digest | SHA-256 `0ba9fa6c1ef7c8b60c515acac1be817b01f25c888e404a7b9c1b421e839ee825`; private backup bytes are not redistributed. |
| Code / configuration / environment | Report identifies container `pulse-api:sha256-c21a6fd0df51b1e3ca9e90a7b0b7968aab477dc4893430969ed0d854690436c2`. This is the recorded image tag; an immutable registry manifest digest and evaluated source commit are not retained in this report. The implementation link is the inspected repository snapshot, not a claim of exact historical deployment binding. |
| Model / dependencies | Model identity is not applicable to count-preservation acceptance. Complete dependency/image provenance requires the original release record. |
| Calculation / reproduction | Read the report and compare `source.backup.restored_receipt_count` with `counts.api_assessments`; inspect `counts_preserved_after_startup`. A fresh restore requires authorized backup access and the original runtime artifacts; none was performed here. |
| Evidence access / integrity review | Authorized private-repository access required. Linked report contents and SHA-256 were inspected during this documentation review. No cloud log retrieval, raw-data rerun or independent source authentication is claimed. |

## Review and acceptance

| Field | Value |
|---|---|
| Measurement owner | Dr. Douglas Moore / DME engineering lead |
| Reviewer / authority / independence | AI-assisted documentation review; no named independent reviewer or customer approver is established. |
| Criterion result | pass |
| Acceptance disposition | pending review |
| Decision reference / scope / authority | Original technical PASS is confined to the linked report. No accountable host-loss, customer or production acceptance is recorded. |
| Open conditions / owner / next action | DME lead: retain the original image manifest/source binding and execute authorized nonempty workflow and timed host-replacement recovery before RTO/RPO acceptance. |
| Customer / governance handoff | [Measurement index](README.md); follow the existing status and lifecycle/customer records linked there. No new release authority. |

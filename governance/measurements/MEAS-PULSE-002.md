# MEAS-PULSE-002 — SCA paired candidate decision coverage

Record v1 · recorded 2026-10-12 (America/New_York). Retrospective documentation of existing evidence; no new execution.

## Identity and trace

| Field | Value |
|---|---|
| Measurement ID / version / recorded date | MEAS-PULSE-002 / v1 / 2026-10-12 |
| KPI definition / version | PULSE-KPI-013; [dictionary v1](../../docs/appendix-a-kpi-dictionary.md) |
| Business need | [PULSE-R02 / PULSE-R03: usable evidence for reliability review](../../customer/01-discovery-record.md) |
| Requirements / implementation | [PULSE-FR-004 / DET-PERF-004](../../requirements/detector-performance.md); [src/pulse/performance_evaluator.py](https://github.com/Douglas-Moore-Engineering/pulse-bearing-health/blob/a00b3134366c6b157c081e9a54b8d6e7fa7cb7f4/src/pulse/performance_evaluator.py) |
| Acceptance criterion / protocol | `detector-performance-v1`, DET-PERF-004: decision coverage at least 95% within each declared regime |
| Protocol fixed date / approval state | The policy was authored after the consumed-case studies. This is explicitly retrospective, proposed fictional-customer assessment; no pre-evaluation approval or independent acceptance. |
| Related / supersedes | First normalized measurement record; preserves the original evidence and decisions, supersedes no run. |

## Definition, baseline and method

| Field | Value |
|---|---|
| Definition / formula / direction | (Eligible windows minus abstentions) / eligible windows, separately for each case and sensor side; higher is better. |
| Unit / numerator / denominator | Fraction and percent of eligible windows in each case/side. Do not pool the sides to mask a failing regime. |
| Baseline / evidence | No independent operational coverage baseline measured; current candidate is the historical descriptive comparator. |
| Target / acceptance threshold / status | At least 95% in every declared regime; proposed retrospective DET-PERF-004 criterion. |
| Population / inclusion / exclusions | Consumed SCA cases 1, 2 and 11, DS/FS groups; excluded inputs: case 1 DS 7, FS 9, others 0. Exclusions remain separate from eligible-window denominators. |
| Independent unit / sample size / exposure | Three consumed case groups; six case/side inventories. Windows and paired sides are dependent and do not become independent bearings. |
| Time window / source clock | Native snapshot inventory; no verified operating exposure or eligible physical-failure endpoint clock. The dossier lacks a precise original evaluation timestamp. |
| Comparator / split / leakage controls | Post-hoc development with future-neighbour pairing and retrospective calibration. This is not causal independent holdout validation; DET-PERF-006 separately fails. |
| Aggregation / uncertainty method | Exact descriptive inventory fractions. No population confidence interval is justified from these dependent consumed groups. |

## Result and scope

| Field | Value |
|---|---|
| Measurement status | measured |
| Observed result / context | 1/DS 104/117 = 88.9%; 1/FS 104/126 = 82.5%; 2/DS 91/94 = 96.8%; 2/FS 91/296 = 30.7%; 11/DS and 11/FS each 19/19 = 100%. DET-PERF-004 FAIL. |
| Uncertainty estimate | Exact descriptive inventory fractions. No population confidence interval is justified from these dependent consumed groups. |
| Evaluation date / environment / data origin | Offline retrospective consolidation of recorded benchmark inventories; not Azure operational performance or a newly opened holdout. |
| Representativeness / limitations | Coverage does not establish correctness, failure-warning lead time or nuisance episodes per operating hour. Runtime/evaluation timestamps and original full environment provenance remain incomplete. |
| Operational intervention / actor / time | Not applicable to this engineering/benchmark result; no customer maintenance or process intervention is evidenced. |
| Follow-up outcome / attribution | Customer outcome not measured. No avoided-loss, downtime, yield, scrap or causal-benefit attribution. |
| Financial impact basis | Not applicable; this record makes no financial-impact claim. |
| Validity / remeasurement trigger | Applies only to the bound historical artifacts. Material changes to code, model, data, configuration or operating context require a new record. |

## Evidence and reproduction

| Field | Value |
|---|---|
| Dossier / immutable evidence | [data/qualification/performance-dossiers/sca-paired-development.json](https://github.com/Douglas-Moore-Engineering/pulse-bearing-health/blob/a00b3134366c6b157c081e9a54b8d6e7fa7cb7f4/data/qualification/performance-dossiers/sca-paired-development.json); SHA-256 `6eb28a743aca0ac97470c7b2f037987f9a83115bdefe4baa28e28ee920b0e9b4` |
| Consolidation / disposition report | [governance/evidence/detector-performance-consolidated.json](https://github.com/Douglas-Moore-Engineering/pulse-bearing-health/blob/a00b3134366c6b157c081e9a54b8d6e7fa7cb7f4/governance/evidence/detector-performance-consolidated.json); SHA-256 `e29cdb076c6d8110a1301de1d902991f2f86150d7ebd64d476e33327fc6a388e` |
| Source data / inventory binding | Dossier retains source-report SHA-256 `d64a5fe0b049211098ac41ee1e200dd8a7167bfad50d81e3867c8edf1aa2b68f`. Raw source inventory is not reopened in this review. |
| Code / policy / environment | Consolidation binds evaluator SHA-256 `8e4365f9f63bd5e9fdc3a7306aa4657359a8b06f676f6cf881f5ef7c5abaefd1` and policy SHA-256 `0a83f07b50f70b3e3118a4c98e855918f7ccbee6ba7862680dacfe4ce6100c64`. No evaluated source commit or full runtime lock is retained there; inspected-snapshot links are distinct. |
| Model version | Candidate `sca-paired-development`; dossier SHA-256 `4728afdf4c650c788f86ca9fa64877f592d83d142cbaedf998a1450fb06e8635`. This is not a learned-model binary digest. |
| Calculation / reproduction | Calculate `(eligible-abstentions)/eligible` for every `regimes` entry in the dossier. `python scripts/consolidate_detector_evidence.py` reproduces the summary from committed evidence, not a new signal-level experiment. |
| Evidence access / integrity review | Authorized private-repository access required. Linked report contents and SHA-256 were inspected during this documentation review. No cloud log retrieval, raw-data rerun or independent source authentication is claimed. |

## Review and acceptance

| Field | Value |
|---|---|
| Measurement owner | Dr. Douglas Moore / DME engineering lead |
| Reviewer / authority / independence | AI-assisted documentation review; no named independent reviewer or customer approver is established. |
| Criterion result | fail |
| Acceptance disposition | pending review |
| Decision reference / scope / authority | [Existing detector status](../../data/qualification/DETECTOR_STATUS.md) and [candidate disposition](../../data/qualification/detector-candidate-disposition.md): NOT_PROMOTED. Formal independent/customer acceptance remains unrecorded. |
| Open conditions / owner / next action | DME lead: preserve the failure; develop only on consumed cases, resolve endpoint/exposure provenance and freeze the complete causal protocol before authorized confirmation on reserved groups. |
| Customer / governance handoff | [Measurement index](README.md); follow the existing status and lifecycle/customer records linked there. No new release authority. |

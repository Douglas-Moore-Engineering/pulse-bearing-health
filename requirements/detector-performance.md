# Detector performance requirements

Version: detector-performance-v1. **Proposed fictional-customer evaluation requirements; not a passed gate or site-approved specification.** These criteria define the next detector evaluation. They do not relax the existing targets to accommodate measured failures. Machine-readable values: [configuration](../config/detector-performance-requirements.json). Existing parent requirements and their IDs remain authoritative.

## Intended decision

Issue an advisory bearing-degradation alert for human investigation in explicitly supported operating regimes. No equipment control, automatic work order, safety protection, fault-class diagnosis or remaining-useful-life claim is authorized by passing these criteria.

| Derived ID | Requirement | Acceptance rule | Parent |
|---|---|---|---|
| DET-PERF-001 | Warn at least 60 minutes before each independently documented actionable degradation/failure endpoint | For every eligible event, the first causally generated alert precedes the earliest plausible endpoint by at least 60 minutes. An interval crossing the threshold is inconclusive. Last recording or test stop is not a physical endpoint without supporting evidence. | PULSE-FR-003 |
| DET-PERF-002 | Miss zero documented eligible failure events in the frozen evaluation | Every event meets DET-PERF-001. No alert, or an alert too late, fails acceptance. Abstention does not remove an event from the denominator. Zero observed misses is not proof of zero population failure probability. | PULSE-FR-003 |
| DET-PERF-003 | Produce at most one nuisance episode per bearing per 720 verified operating hours | Evaluate complete predeclared nonoverlapping 720-hour exposure blocks for each bearing. At most one confirmed nuisance or unresolved episode in each block. Incomplete blocks are reported but cannot pass this criterion. Do not substitute calendar time or recording duration for operating exposure. | PULSE-FR-003 |
| DET-PERF-004 | Make a supported decision on at least 95% of eligible windows | Per declared regime, (eligible windows minus abstentions) / eligible windows >= 0.95. Report invalid, missing and excluded inputs separately against expected acquisition cadence. Regimes and eligibility cannot be redefined after evaluation. | PULSE-FR-004 |
| DET-PERF-005 | Abstain outside the supported domain | All predeclared unsupported-regime and invalid-input challenge cases return unavailable/abstain with a reason; no healthy, fault-class or RUL assertion. | PULSE-FR-004 |
| DET-PERF-006 | Use independent causal evaluation | Freeze model, thresholds, preprocessing, commissioning policy, episode/reset logic, splits and evaluator before opening holdouts. No future samples, future neighbours, post-failure calibration or bearing/run overlap across development and evaluation. | PULSE-NFR-008 |
| DET-PERF-007 | Reconstruct every evaluated decision | Bind model/code/configuration versions, source hashes, asset/run, timestamps, features, output and episode identity. Replays reproduce decisions under the frozen environment and declared numerical tolerances. | AIG-REQ-001 |

## Evidence sufficiency and scoring

Additional provisional engineering minimums: 20 independent documented failure events across the claimed support scope, at least three independent healthy bearings, and at least 720 verified healthy operating hours per healthy bearing. Repeated windows from one event do not increase event count. These minimums support a bounded benchmark decision only; they do not establish a statistical reliability guarantee or validate every operating regime. A domain reviewer must judge representativeness and approve a statistical/site acceptance protocol before production claims.

Use a predeclared event ledger with endpoint interval, clock basis, fault evidence, regime and eligibility rationale. Count every eligible failure event, including those with abstentions. Report event counts and lead-time bounds, not only snapshot accuracy or aggregate F1. Where endpoint evidence is insufficient, report INCONCLUSIVE rather than using a convenient proxy.

Freeze episode grouping, acknowledgement, reset, persistence and cooldown before evaluation. Repeated windows within one episode count once. Acknowledgement alone must not hide a new episode or suppress an unrelated fault. Unsupported or unresolved events remain visible. Require review evidence for nuisance classification; unresolved alert episodes count conservatively against the nuisance limit. Evaluate healthy exposure separately from pre-failure exposure.

Each criterion returns PASS, FAIL or INCONCLUSIVE. Overall benchmark acceptance requires every criterion PASS and evidence minimums met. Any FAIL rejects the candidate; any INCONCLUSIVE prevents promotion. Passing the benchmark does not authorize deployment, establish customer acceptance, or replace independent assurance.

## Platform requirements remain separate

The existing PULSE-NFR-001 target is p95 persisted result within five seconds of accepted service receipt. The requested capacity is 1.5 million requests/day with peak activity 09:00?15:00; traffic shape and full-workflow sustained verification remain open. API speed cannot substitute for warning-time or nuisance performance. The earlier 500 ms target was provisional, not a replacement for the recorded five-second requirement.

## Current disposition and next experiment

Current RMS/envelope/paired candidates remain [NOT_PROMOTED](../data/qualification/detector-candidate-disposition.md). Existing studies do not establish these endpoint, exposure, coverage and independence criteria. This file adds no measured success.

Develop on consumed cases only. Before using reserved SCA cases 3?10, freeze a separate executable evaluation protocol and determine whether those cases can supply the required endpoints, exposure and independent units. Do not consume holdouts merely to fill the proposed minimum event count. If evidence is unavailable, collect qualified data or narrow the claimed scope through explicit review; do not relabel missing evidence as a pass.

An offline evaluator now implements metric checks and required evidence assertions; see [operator instructions](../runbooks/detector-performance-evaluation.md). It cannot independently verify dossier truth, source independence or reviewer authority. No promotion decision is authorized by its output.

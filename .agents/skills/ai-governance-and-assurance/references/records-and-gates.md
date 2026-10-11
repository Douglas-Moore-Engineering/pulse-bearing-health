# Records and gate decision rules

## Record schema

Use stable IDs and machine-readable registers where useful. Keep confidential data, secrets, personal logs, CUI and detailed vulnerability evidence in approved restricted stores; the repository may hold access-controlled references and digests. Do not publish client evidence merely to make the index complete. Define access, retention, legal holds and redaction; logging everything is not automatically appropriate.

| Record | Required fields |
|---|---|
| System/classification | System ID/version, scope, use, operating envelope, jurisdictions, affected parties, autonomy, credible scenarios, inherent/residual risks, tier rationale, uncertainty, assessor and authority |
| Obligations | Obligation ID, issuer/type, jurisdiction/actor role, title/version, authoritative URL, verified date, effective date/transition, applicability rationale, owner, evidence inspected, control/requirement IDs, review trigger and unresolved issues |
| Tailoring | Control ID, applicable/N/A/pending, trigger facts, rationale/evidence, owner, reviewer authority, disposition/date, expiry/trigger and mandatory status |
| Risk | Risk ID, scenario/cause, affected parties/assets, severity/likelihood/exposure assumptions, inherent assessment, treatments/control IDs, evidence, residual assessment, owner, acceptance authority/date/expiry and triggers |
| Requirement/V&V | Requirement ID, parent need/obligation/control, SHALL statement, responsible role, acceptance threshold, conditions/environment, verification method/test ID, result, evidence ID, defects, reviewer and affected gate |
| Evidence | Evidence ID, artifact URI and version/digest, source/author, event/test time, collection method, tested system/environment, dataset scope, coverage/limitations, access/retention, reviewer, validity window and change invalidators |
| Gate | Gate ID, system/release/environment, requirement dispositions, evidence index version/digest, open findings, mandatory-control coverage, risk acceptance IDs, decision, reasons, actual approver identity/authority/date, scope/conditions, expiry/revocation and next activity |
| Change | Change ID, before/after baseline digests, purpose, changed components/scope/obligations, harm/control impact, preapproved-envelope basis, materiality decision/authority, invalidated evidence, affected gates, tests and authorization |
| Handoff | Sender/receiver roles, IDs and versions, current gate/evidence states, inherited conditions, next permitted activity and stop boundary |

## Gate algorithm

1. Freeze the gate assessment scope and applicable requirement set. Resolve conflicting baselines; do not silently choose the easier one.
2. For each mandatory requirement inspect implementation and evidence. Validate identity, integrity, relevance, test conditions, representativeness, coverage and freshness. Reject stale, mismatched, inaccessible-to-authorized-reviewer, fabricated or purely simulated evidence as proof for a real release.
3. Assign `PASS` only when the criterion is met and evidence supports it; `FAIL` when tested and unmet; `BLOCKED` when not evaluated or material facts/evidence are missing. Assign N/A only through approved applicability decisions. Conditions are explicit restricted dispositions, not missing mandatory proof.
4. Check independent review and actual sign-offs where required. Separate risk acceptance from verification: accepting risk does not turn a failed test into PASS. Keep an approved requirement change/exception and its evidence visible if allowed; never waive law, critical safety controls or required independence.
5. Determine gate disposition: `APPROVED` only when all applicable mandatory criteria pass, required authentic approvals exist, prohibited uses are absent and evidence/authorization binding is current; `CONDITIONALLY_APPROVED` only for the bounded exceptions allowed in the main skill; `NOT_APPROVED` for failure; `BLOCKED` for unresolved information/authority/evidence; `SIMULATED` for fictional decisions. No percentage score overrides a blocker.
6. For production authorization require all preceding applicable gate baselines and technical, security, operational, legal/domain and customer prerequisites for the specific exposure. Record restrictions, expiry and revocation response. Verify the promotion mechanism checks these conditions; a Markdown approval alone is insufficient enforcement.
7. Reuse unchanged valid approvals. Invalidate affected evidence and authorization on material changes or breached conditions, preserve prior decisions and follow the predefined safe operating response.

## Package paths

Use existing equivalent records and indexes. Otherwise start with:

- `governance/AI_GOVERNANCE_PLAN.md`
- `governance/AI_SYSTEM_CLASSIFICATION.md`
- `governance/INTENDED_AND_PROHIBITED_USE.md`
- `governance/GOVERNANCE_RACI.md`
- `governance/OBLIGATIONS_REGISTER.csv`
- `governance/CONTROL_APPLICABILITY.csv`
- `governance/GOVERNANCE_REQUIREMENTS.csv`
- `governance/AI_RISK_REGISTER.csv`
- `governance/AI_IMPACT_ASSESSMENT.md`
- `governance/model/MODEL_SYSTEM_CARD.md`
- `governance/model/THIRD_PARTY_AI_REGISTER.csv` when applicable
- `governance/assurance/GOVERNANCE_VV_MATRIX.csv`
- `governance/assurance/EVIDENCE_INDEX.csv`
- `governance/assurance/ASSURANCE_CASE.md` where required
- `governance/approvals/GATE_DECISIONS.csv`
- `governance/approvals/PRODUCTION_AUTHORIZATION.md`
- `governance/operations/GOVERNANCE_MONITORING_PLAN.md`
- `governance/operations/MATERIAL_CHANGE_POLICY.md`
- `governance/operations/AI_INCIDENT_RESPONSE.md`
- `governance/operations/AI_RETIREMENT_PLAN.md`

Cross-link canonical data rights/lineage, threat models, release manifests, risk acceptance, runbooks and organizational management records. Create only phase-relevant records; record future outputs as planned, not completed.

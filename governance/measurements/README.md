# Measurement and evidence index

Version 1 · 2026-10-12 · Owner: Dr. Douglas Moore. These records normalize historical evidence; they do not report new execution or change model, cloud or customer release decisions.

Business need → KPI → requirement → implementation → measurement → evidence → acceptance decision. Definitions live in the [KPI dictionary](../../docs/appendix-a-kpi-dictionary.md). [Open KPI plans](planned-kpis.md) have individual record IDs and explicit unmeasured status. [Machine-readable index](index.csv) is a navigation/status projection, not a separate acceptance authority.

| Record | Scope | Measurement / criterion / acceptance |
|---|---|---|
| [MEAS-PULSE-001](MEAS-PULSE-001.md) | PULSE-KPI-012 | measured / pass / pending review |
| [MEAS-PULSE-002](MEAS-PULSE-002.md) | PULSE-KPI-013 | measured / fail / pending review |

## Evidence and decision authority

Pinned links identify the exact repository evidence snapshot reviewed. A repository snapshot commit is not automatically the original executed commit; records explicitly distinguish original code/image/data digests from later documentation versions and identify provenance gaps. Historical evidence remains unchanged. Failed and inconclusive findings stay visible.

No real customer outcomes or independent sign-off are established. Each unmeasured plan has a DME owner and next action; its dependent acceptance remains open. Record corrections as new versions with rationale and retain their Git history; actual reruns receive new IDs.

Existing decisions: [detector status](../../data/qualification/DETECTOR_STATUS.md), [release gates](../release_gates.md). Existing lifecycle/handoff: [engineering review](../../docs/ENGINEERING_REVIEW.md), [demo readiness](../../customer/10-demo-readiness.md), [current status](../../PROJECT_STATUS.md). Receipt recovery is a supporting engineering check, not host-loss acceptance.

## Unquantified claims

Identity configuration, advisory authority boundaries and implemented code paths are qualitative implementation/security claims, so a numeric KPI is not applicable. Their trace remains in the existing requirements/V&V and decision registers, with implementation/evidence links from the README. Documentation of a control is not proof of its operation or acceptance.

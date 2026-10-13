# Engineering Release Gates

Current reference evidence: [engineering review](../docs/ENGINEERING_REVIEW.md). The authenticated Azure assessment service is deployed under the explicit USD 100 authorization. Production/detector gates below remain blocked by their actual criteria; historical pre-Azure boundaries do not revoke that bounded authorization.

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

| Gate | Exit evidence | Current disposition |
|---|---|---|
| G0 Discovery/data readiness | Governed scope plus rights/bytes/schema/split feasibility | BLOCKED: discovery prepared, data unqualified |
| G1 Architecture/reproducible baseline | Reviewed requirements/architecture/security/cost and executed baseline | BLOCKED: baseline executed on two IMS runs; complete architecture/security/data acceptance not established |
| G2 Offline V&V | Frozen holdout, baseline/candidate evidence, workflows/abstention | BLOCKED: frozen RMS baseline missed a documented damaged bearing; no qualified detector |
| G3 Shadow | Site readiness, recovery and representative non-actuating operation | BLOCKED: no site or authorization |
| G4 Advisory canary | Restricted rollout and operator evidence | BLOCKED |
| G5 Production advisory | Applicable ORR/CAR, governance authorization and release binding | BLOCKED |
| G6 Scale-out | Validated capacity, support, site portability and costs | BLOCKED |
| G7 Bounded automation | Separate safety/authority case and validated protective boundary | Outside approved scope; BLOCKED |

The pre-Azure document review is not G1 runtime PASS. Azure workspace entry has its own scoped criteria in cloud_entry_criteria.csv. AI governance gates AIG-G0–G7 are distinct from engineering gates and risk tiers G1–G4. No authentic approval is supplied by fictional decisions.

The v0.2 [promotion design](../docs/08-testing-release-gates-and-acceptance.md) and [manifest template](release-manifest.template.json) make artifact/target/approval binding explicit. [Recovery view](../docs/diagrams/08b_rollback_recovery.svg) requires an eligible prior release or continued unavailable/manual operation. Gate dispositions above remain unchanged; no enforcement or runtime evidence is claimed.

## RMS v2 final research disposition

[Final evidence](../data/qualification/rms-v2-final-research.md) reports 132.4/195.9 minutes of descriptive lead on LDM B12/B17 with 26/9 episodes. Candidate NOT PROMOTED; physical-failure warning and nuisance criteria are not evaluable from current labels. This does not overturn the historical baseline failure or pass a production gate. The deployed rule remains unchanged.

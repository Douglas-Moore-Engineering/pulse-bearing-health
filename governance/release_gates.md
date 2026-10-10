# Engineering Release Gates

PULSE pre-Azure review v0.1 · 2026-10-10 · Owner: Dr. Douglas Moore · Prepared for review

Fictional customer scenario; proposed design, not implementation or customer approval. Stop boundary: no Azure connection, provisioning, paid resources, site access or production release.

| Gate | Exit evidence | Current disposition |
|---|---|---|
| G0 Discovery/data readiness | Governed scope plus rights/bytes/schema/split feasibility | BLOCKED: discovery prepared, data unqualified |
| G1 Architecture/reproducible baseline | Reviewed requirements/architecture/security/cost and executed baseline | BLOCKED: design prepared; baseline not run |
| G2 Offline V&V | Frozen holdout, baseline/candidate evidence, workflows/abstention | BLOCKED: no trained/evaluated model |
| G3 Shadow | Site readiness, recovery and representative non-actuating operation | BLOCKED: no site or authorization |
| G4 Advisory canary | Restricted rollout and operator evidence | BLOCKED |
| G5 Production advisory | Applicable ORR/CAR, governance authorization and release binding | BLOCKED |
| G6 Scale-out | Validated capacity, support, site portability and costs | BLOCKED |
| G7 Bounded automation | Separate safety/authority case and validated protective boundary | Outside approved scope; BLOCKED |

The pre-Azure document review is not G1 runtime PASS. Azure workspace entry has its own scoped criteria in cloud_entry_criteria.csv. AI governance gates AIG-G0–G7 are distinct from engineering gates and risk tiers G1–G4. No authentic approval is supplied by fictional decisions.

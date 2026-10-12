# Phase 10 reference demonstration readiness

Prepared and locally verified 2026-10-12. Disposition: **ready for a guided offline reference demonstration**. This is engineering preparation for the Phase 10 review, not customer acceptance, independent assurance or production release. Phases 8/9 remain active for unresolved production work.

## Launch

Open [benchmark-demo.html](benchmark-demo.html) directly in a browser. No server, login, cloud connection or customer data is required. Allow 15 minutes and follow the [customer walkthrough](09-customer-pilot-package.md). Select B04, B12 and B17; each should display a trend and one grouped episode. The original counts are 3, 26 and 9 respectively.

For an executable synthetic evidence demonstration, from the repository with dependencies installed run:

```powershell
python scripts/run_reference_demo.py --output outputs/demo-meeting-new
```

Use a fresh output directory. Open its index.html and report.json to show three generated windows, evidence references and simulated decisions. One malformed fixture is quarantined. The output correctly abstains from qualified health predictions. Never substitute this output for a live machine diagnosis.

## Verified preparation

| Check | Evidence | Limit |
|---|---|---|
| Full local software suite | [180 passed](../governance/evidence/phase10-demo-tests.xml) | One existing dependency deprecation warning; no new cloud verification |
| Three benchmark selections | [Functional check](../governance/evidence/phase10-demo-functional.json) | Node DOM-stub execution, not a fresh visual/browser audit; earlier visual review retained in skill record |
| Synthetic executable replay | [Summary](../governance/evidence/phase10-synthetic-demo.json) | Generated fixtures only; no detector qualification |
| Review narrative and scope | [Customer package](09-customer-pilot-package.md) | No actual customer or site acceptance |

Reproduce selection checks with `node scripts/verify_demo_functional.cjs`; run the suite with `python -m pytest -q`. Repository consistency uses `python scripts/validate_review_package.py` and does not approve lifecycle gates.

## Presenter claims and fallback

Say: recorded benchmark data, experimental grouping, traceable reference workflow, simulated review. State that lead is to the last recording, not confirmed failure. The offline prototype differs from the deployed reference rule. The HTML is not a live Azure dashboard.

Do not claim: qualified bearing diagnosis, achieved warning/nuisance targets, 1.5 million requests/day, high availability, current Azure health or customer approval. See [detector status](../data/qualification/DETECTOR_STATUS.md) and [capacity status](../docs/CAPACITY_STATUS.md). Infrastructure demonstrations do not close detector gaps.

If browser execution fails, present the [recorded grouping evidence](../governance/evidence/customer-demo-stability.json), the synthetic report and existing architecture exports, identifying each as recorded. Do not troubleshoot by connecting a customer asset or changing cloud resources during the meeting.

## Exit and next handoff

Phase 10 meeting outcome remains unrecorded. Capture stakeholder feedback, intended maintenance decision, candidate asset scope, data rights, calibration, acceptance definitions, owners and whether a shadow pilot is useful in the existing discovery record. Phase 11 site adaptation starts only with actual authorized site inputs. No additional capacity tuning is required to conduct this bounded offline demonstration; performance and production qualification remain separate engineering work.

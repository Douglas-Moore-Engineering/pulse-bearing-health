# Current project status

Current Phase 10 preparation: [demo readiness and launch checklist](customer/10-demo-readiness.md). Locally verified on 2026-10-12: 180 software tests passed, three benchmark selections functionally checked, and synthetic replay completed. Ready for guided offline demonstration; actual review/acceptance and production qualification remain open.

Reference system deployed on Azure K3s. Production detector: **NOT_PROMOTED**. This is a fictional-customer demonstration, not site acceptance.

- Authenticated assessment, durable receipts, benchmark anomaly inbox and acknowledgement are deployed and exercised.
- Pilot intake is exercised live. Read-only review access now succeeds with Pulse.Review in the live token. Pulse.Close remains absent; nonempty review/closure recovery remains unverified.
- Fictional 12-asset reconciliation is deployed with persistent reports and a timer. Manual execution passed; automatic scheduled execution remains unobserved.
- Bounded half-hour backups now upload to Azure Blob and verify isolated restoration. Three consecutive automatic service runs completed; actual Blob recovery restored 3,150 receipts. Sustained cadence, complete host replacement and one-hour host-loss RPO remain unqualified.
- Latest recorded full software suite: 180 passed. Sustained daily capacity, production availability, detector qualification and actual customer validation remain open.

See [README](README.md), [engineering backlog](docs/CURRENT_ENGINEERING_BACKLOG.md), [execution record](customer/08-deployment-execution.md), [skill review](docs/SKILL_COMPLETION_REVIEW.md) and [historical status](PROJECT_HISTORY.md). Records distinguish implemented, tested and approved states; no production gate is promoted by this summary.

Current detector evidence: [consolidated status](data/qualification/DETECTOR_STATUS.md). RMS: INCONCLUSIVE under the complete policy, with the documented missed bearing retained. Paired SCA: FAIL. Neither is promoted.

Local recovery verification passed for restored synthetic receipts, reviews and closures through a fresh process, Docker and Kubernetes PVC/pod replacement. The rendered Deployment's default command and health probes passed; a separate pod verified Service DNS, ClusterIP routing and anonymous-access rejection. Missing tenant/review-storage settings prevented startup in the container checks. See [recovery runbook](runbooks/local-pilot-exercise.md) and [focused Kubernetes evidence](governance/evidence/kubernetes-application-recovery-tests.xml). Temporary resources were removed. Local deny-ingress behavior passed for the tested client-to-Service path. Local outbound TCP 8080 blocking and DNS resolution passed. Private pod-IP TCP 443 exclusion also passed. One certificate-verified public HTTPS path also passed. Other excluded address ranges, real closure-role access, external ingress and Azure host-loss recovery remain unverified; live authenticated review reads passed. These tests do not qualify the detector or production release.

Actual Azure Blob-to-local-container recovery passed for 3,150 receipts, 884 reference windows and one alert. [Evidence](governance/evidence/blob-container-recovery.json). No live database was changed; full Azure host replacement remains open.

Capacity experiments remain local and harness-only; production persistence is unchanged. Use the [capacity status](docs/CAPACITY_STATUS.md) for the current result, comparison and next action. Historical measurements remain in the [protocol](runbooks/sustained-capacity-protocol.md) and evidence JSON files.

Start with this page for release state, the [engineering backlog](docs/CURRENT_ENGINEERING_BACKLOG.md) for remaining work, and the [skill review](docs/SKILL_COMPLETION_REVIEW.md) for lifecycle position. Historical execution entries are evidence records, not competing current plans.

# Current project status

Reference system deployed on Azure K3s. Production detector: **NOT_PROMOTED**. This is a fictional-customer demonstration, not site acceptance.

- Authenticated assessment, durable receipts, benchmark anomaly inbox and acknowledgement are deployed and exercised.
- Pilot intake is exercised live. Review routes are deployed; reviewer-role token propagation and nonempty review recovery remain unverified.
- Fictional 12-asset reconciliation is deployed with persistent reports and a timer. Manual execution passed; automatic scheduled execution remains unobserved.
- Local backups run every 30 minutes with bounded retention. Private off-host recovery passed for 3,150 receipts; off-host automation and one-hour host-loss RPO remain open.
- Latest recorded full software suite: 143 passed. Sustained daily capacity, production availability, detector qualification and actual customer validation remain open.

See [README](README.md), [engineering backlog](docs/CURRENT_ENGINEERING_BACKLOG.md), [execution record](customer/08-deployment-execution.md), [skill review](docs/SKILL_COMPLETION_REVIEW.md) and [historical status](PROJECT_HISTORY.md). Records distinguish implemented, tested and approved states; no production gate is promoted by this summary.

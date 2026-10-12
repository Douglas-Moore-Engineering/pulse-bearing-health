# Current capacity evidence

Status: experimental local persistence tuning; production unchanged; 1.5 million requests/day unqualified.

The offered profile is 70 requests/second with 4,096 samples per request, synthetic identity, eight client workers, at most 32 pending requests, and a 50 MiB sampled-storage stop. Client and API use separate processes on one Windows host. These runs exclude real Entra verification, a qualified detector, the complete alert workflow and Azure conditions.

Connection reuse retained FULL synchronization and separate receipt/evidence commits. Two one-minute runs completed 4,200 requests each without drops. Three-minute pooled runs dropped 40 and 16 slots respectively. Interval measurements localized the latter drops to seconds 70-80, with 580 ms scheduled-to-completion p95 in that cohort. All submitted successes reconciled with durable receipt/evidence counts.

Initial serialized result: the serialized-write candidate completed all **12,600 requests** in the three-minute offered workload, with **zero drops or failures**. Scheduled-to-completion p95 was **61.81 ms**; the highest ten-second cohort p95 was **195.54 ms**. All 12,600 receipts and evidence rows reconciled, integrity passed and temporary storage was removed. [Serialized result](../governance/evidence/local-capacity-serialized.json).

Disposition: promising local candidate, not production-approved. The preceding pooled run dropped 16 slots; this is a sequential comparison on a shared host, not statistical proof or a multi-process writer solution. Serialization is process-local and retains both FULL transactions. Its save timer excludes writer-lock wait, recorded separately; scheduled-to-completion latency includes that wait.

Repeat result: the identical script and three-minute profile completed **12,537 requests**, with **63 queue-full drops**, zero submitted failures and **347.19 ms scheduled-to-completion p95**. All 12,537 receipts and evidence rows reconciled; integrity and temporary cleanup passed. [Repeat evidence](../governance/evidence/local-capacity-serialized-repeat.json).

Current disposition: **do not promote the candidate**. The initial zero-drop result did not reproduce. Next separate shared-host/load-generator variability from server contention using a controlled independent generator or resource-isolated local setup, with CPU/disk and lock-wait measurements. Production lifecycle integration remains deferred until the performance choice is supported. Do not increase queues or reduce FULL durability to obtain a passing result.

[Protocol and historical measurements](../runbooks/sustained-capacity-protocol.md), [pooled interval evidence](../governance/evidence/local-capacity-intervals.json), [focused failure tests](../governance/evidence/local-capacity-pool-failure-tests.xml).

Outstanding qualification: repeatability, production lifecycle integration, backup competition, retention/storage bounds for a six-hour run, independent load-generator conditions and actual target deployment performance. Successful local runs do not close these gates.


Latest diagnostic: separate process CPU sampling measured API 0.972 and client 0.392 logical CPU equivalents on average. The one-minute run completed 4,029 requests with 171 drops and 568.47 ms scheduled-to-completion p95. [Evidence](../governance/evidence/local-capacity-cpu-diagnostic.json). Next profile API CPU work under the bounded synthetic workload, then test a controlled alternative. This is a profiling lead, not root-cause proof; independent-host and disk measurements remain open. Production promotion stays deferred.

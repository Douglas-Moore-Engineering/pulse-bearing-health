# Sustained capacity protocol ? prepared, not executed

Current disposition and next action: [capacity status](../docs/CAPACITY_STATUS.md). The dated/ordered experiments below preserve historical decisions; their earlier next steps are superseded by that page.

The existing `infra/single-node/measure-live-capacity.py` runs two 20-second VM-local stages at 17.4 and 70 offered requests/second, using real tokens and unique durable receipts. It is not a daily-capacity test and must not be run under read-only verification authorization.

The stated demand is 1.5 million requests/day with peak hours 9 AM?3 PM. That is 17.36 requests/second averaged across 24 hours. A conservative proposed profile places all 1.5 million in six hours: 69.45 requests/second. This concentration is an explicit test assumption, not an observed customer arrival distribution. Request semantics, payload mix, retries and p95 latency/error acceptance must be frozen before a qualification run; the detector remains unqualified regardless of throughput.

## Required experiment

1. Use isolated synthetic storage and an explicitly identified deployment/image. Never fill the production receipt database as an incidental permission check. Record actual CPU/memory/disk and identity/network boundaries.
2. Run bounded baseline and ramp stages, then the six-hour profile only after storage capacity and spending estimates fit the ceiling. Include unique windows, idempotent retries, maximum supported payloads, rejected inputs and the reference-alert/review workflow; report each separately.
3. Measure offered, admitted, successful, failed and dropped requests; successful throughput; latency percentiles; CPU/memory; database/WAL/disk growth; backup duration/failures and remaining disk. Record immutable config, image and dataset/fixture versions.
4. Reconcile accepted unique receipts with recovered backup contents and explain every missing record. Validate alert/workflow counts separately. Stop on storage-reserve violations or backup failure; the current 50 MiB snapshot limit must be addressed before a run can outgrow it.
5. Report observed results against frozen requirements. A short run, synthetic-only identity or extrapolation cannot establish live daily capacity. Any failing criterion remains failing; no new latency target is selected after seeing results.

## Authorization and remaining inputs

Current renewed Azure authorization covers permission verification and isolated backup recovery without new paid resources, within USD 100/month. It does not authorize the live receipt-writing load script. A separate concrete execution request must identify the isolated target, total requests, maximum disk growth, stop conditions and expected cost before cloud writes. Local preparation remains available. Required performance references: [capacity/release record](../docs/AKS_CAPACITY_AND_RELEASE.md), [engineering backlog](../docs/CURRENT_ENGINEERING_BACKLOG.md) and [recovery evidence](local-pilot-exercise.md).

## Executed local smoke load

Run `python scripts/exercise_local_capacity.py --output outputs/local-capacity-smoke.json` with API/test dependencies available. The harness creates its own temporary database and loopback server; it accepts no remote URL or database path. It uses synthetic injected identity, eight client workers, at most 32 queued requests, 4,096 samples/window and unique window IDs. Late scheduler slots and full queues are counted as dropped rather than hidden. Sampled storage reaching 50 MiB stops further submission; in-flight work can still complete. The app's external configuration environment should be unset for the isolated harness.

[Observed result](../governance/evidence/local-capacity-smoke.json): offered 4,200 requests over 60 seconds at 70/second; 2,462 submitted and successful, zero submitted-request failures, 1,738 dropped slots. Achieved 40.62 successful requests/second including drain; successful-response p95 437 ms. All 2,462 successes matched persisted receipts and SQLite integrity passed. Final storage was 3,112,960 bytes, sampled peak 7,261,952 bytes; the storage stop did not trigger. Temporary storage was removed.

The offered rate was not sustained. No capacity requirement is promoted. Client and server share this Windows host, so scheduler/load-generator effects are mixed with server behavior. The run excludes real token verification, full alert/review processing, Azure network, backup competition and six-hour duration. Next diagnostic work should separate scheduler drops from queue saturation and isolate the load generator before attributing the bottleneck. The earlier 20-second Azure tests and this local result are different environments and cannot be substituted for one another.

## Separate-process diagnostic

The harness now starts the API in a spawned Python process, clears inherited PULSE deployment variables in that process, and waits for clean shutdown before deleting temporary storage. Client/server still share the Windows machine. Drop counters distinguish scheduler lateness, full queue and storage stop; queue-full takes precedence if both queue and timing limits are exceeded.

[Executed result](../governance/evidence/local-capacity-isolated-process.json): at the same 70/second, 60-second and 4,096-sample workload, 2,636 requests succeeded, none of the submitted requests failed, and 1,564 slots were dropped (716 scheduler-late, 848 queue-full). Successful throughput was 43.49/second; successful-response p95 was 407 ms. All 2,636 receipts persisted with integrity OK; final storage was 3,325,952 bytes and sampled peak 7,495,496 bytes. No storage stop occurred; temporary storage was removed.

This single rerun improved measured throughput from 40.62 to 43.49/second, but still did not sustain the offered rate. The difference is descriptive, not a statistically established improvement. Queue pressure remains mixed with client worker/serialization/transport overhead and API/SQLite latency; it is not yet a server-only bottleneck finding. Next diagnostic work should measure client queue wait, request preparation and server/storage timing or use an independent load-generator host before tuning concurrency or changing storage architecture. No daily-capacity or Azure claim follows.

## Timing decomposition ? storage path dominates this run

The harness adds diagnostic-only API response timing and a TimedStore wrapper; production modules and durability settings are unchanged. Client timings separate executor queue wait, compact JSON preparation and HTTP round trip. Server timing covers the middleware-to-response interval. Store timing covers the entire save method, including connection setup, lock waits, receipt commit and commit-evidence work. Instrumentation adds overhead; this is a diagnostic run, not an exact repeat of an uninstrumented benchmark.

[Observed result](../governance/evidence/local-capacity-timing.json): 2,587 successes, zero submitted failures, 666 scheduler-late and 947 queue-full drops. Achieved 42.56/second; successful worker-response p95 417.67 ms. Mean/p95 milliseconds: client queue 525.23/621.42; JSON preparation 0.97/1.36; HTTP round trip 186.32/416.62; server handler 182.62/413.57; complete store save 170.95/403.75. All receipts reconciled and cleanup passed.

Store-save mean is about 94% of handler mean in this run, supporting investigation of that path first. This does not distinguish lock contention from connection, transaction or filesystem costs. Queue wait is excluded from the historical worker-response p95; that p95 must not be presented as end-to-end offered-request latency. Component percentiles must not be added. Next instrument connection/lock/commit boundaries before changing persistence architecture or concurrency. FULL-synchronous durability and post-commit evidence semantics must be preserved.

## Storage operation timing

The harness now times SQLite connection open, synchronous PRAGMA, BEGIN IMMEDIATE, SELECT, receipt INSERT, evidence INSERT, transaction context exit and close. Only save calls are counted; initialization and health checks are excluded. Production persistence code is unchanged. The test connection context mirrors production, including timeout=5, FULL synchronous mode, separate receipt/evidence transactions and post-receipt-commit timestamp sampling.

[Observed result](../governance/evidence/local-capacity-storage-timing.json): 2,360 successful persisted requests, zero submitted failures, 1,840 dropped slots (710 scheduler-late; 1,130 queue-full), 38.80 successful requests/second. Successful worker-response p95 was 466.54 ms; mean executor queue wait was 580.95 ms. Integrity and receipt reconciliation passed; temporary storage was removed.

Mean operation time, normalized per receipt using operation counts: connection open 3.44 ms, synchronous PRAGMA 92.99 ms, BEGIN IMMEDIATE 35.81 ms, SELECT 1.39 ms, receipt INSERT 1.16 ms, evidence INSERT 39.26 ms, transaction exit 5.78 ms, close 0.85 ms. There were two opens, PRAGMAs, transaction exits and closes per receipt. Total save mean was 181.01 ms. Operation timings include scheduling and SQLite internal work; PRAGMA latency is not established as pure configuration cost, and INSERT includes implicit transaction/lock acquisition. Transaction exit measures SQLite context completion, not isolated physical disk latency. Percentiles must not be added.

The measured commit boundary is a small portion of this run. Next evaluate a harness-only bounded connection-reuse candidate against the unchanged baseline, retaining FULL synchronization, separate commit-evidence semantics, thread ownership and deterministic shutdown. Reconcile both receipts and evidence and exercise conflict/retry and failure behavior before proposing production adoption. This single diagnostic is not a throughput regression finding or Azure/daily-capacity qualification.

## Bounded connection-reuse experiment

Implemented a harness-only eight-slot pool with exclusive connection leases. Connections can move between threads but cannot be used concurrently; shutdown occurs after request workers stop. FULL synchronous mode is set on creation; the inherited save method retains both transactions and post-commit evidence timing. Production code is unchanged. The focused test passed concurrent duplicate writes, conflict handling, transaction rollback, FULL mode, stable evidence on retry, restart persistence and closed-store rejection. Existing storage tests: five passed. [Focused evidence](../governance/evidence/local-capacity-pool-tests.xml).

Two sequential 60-second runs used the same script SHA and workload (candidate first, control second):

| Measurement | Existing connection behavior | Reuse candidate |
|---|---:|---:|
| Successful requests / matching evidence rows | 2,408 | 3,374 |
| Successful requests/second | 39.59 | 56.23 |
| Worker-response p95 ms (excludes queue wait) | 501.01 | 54.40 |
| Mean store-save ms | 184.13 | 9.97 |
| Queue-full drops | 1,106 | 0 |
| Scheduler-late drops | 686 | 826 |
| Submitted failures | 0 | 0 |

[Control](../governance/evidence/local-capacity-reuse-control.json), [candidate](../governance/evidence/local-capacity-reused-connections.json). Both reconciled receipt and commit-evidence counts, passed SQLite integrity and removed temporary storage. Candidate operation timings omit connection-open timing and shutdown closes; complete save timing includes setup during requests. Seven measured PRAGMAs plus initialization reflect eight retained connections.

This supports further investigation of connection reuse but is a single sequential pair on a shared host, not a statistically controlled production comparison. Neither run delivered all 4,200 offered slots. Next correct or isolate the generator's scheduling limitation and repeat bounded comparisons; then test connection initialization/commit failure handling and lifecycle integration before any production adoption. Current tests do not establish power-loss durability, six-hour capacity, cloud performance or detector qualification.

## Retained scheduling slots and failure handling

The opt-in `--retain-late-slots` mode retains overdue submissions within the existing 32-pending-request and 50 MiB storage bounds. It records submission delay and scheduled-to-completion latency using a common performance clock. Late wakeups may produce catch-up bursts; this is not exact uniform interarrival timing. The original drop-on-lateness mode remains available for historical comparison.

The experimental pool now discards a connection on setup or transaction exceptions and returns an empty slot for replacement. [Nine focused tests passed](../governance/evidence/local-capacity-pool-failure-tests.xml): existing storage behavior plus concurrent duplicates, rollback/restart, injected setup/commit failures, and an evidence-write failure after a durable receipt. The latter retains the receipt without fabricating historical timing on retry. Failure injection does not simulate physical power loss; pool shutdown still requires callers to stop and join workers first.

[Executed candidate](../governance/evidence/local-capacity-retained-slots.json): all 4,200 offered requests completed, zero failures, zero drops, 4,200 receipts and 4,200 commit-evidence rows, integrity OK and temporary cleanup complete. Offered workload was 70/second for 60 seconds; completion including drain took 60.031 seconds (69.964 successful/second). Worker-response p95 was 189.03 ms; scheduled-to-completion p95, including generator delay and executor queue, was 227.86 ms. Submission delay mean/p95 was 8.50/17.26 ms; queue wait mean/p95 13.98/84.70 ms. Sampled peak directory storage was 9,326,384 bytes.

This one-minute local candidate completed the planned offered volume within the provisional 500 ms p95 target, including scheduling delay. It does not establish six-hour sustained capacity, full alert-workflow throughput, Azure performance or production qualification. Production persistence remains unchanged. Next repeat this bounded workload to check variability, then design lifecycle-safe production integration and a longer isolated soak with explicit retention/storage bounds. Preserve the failed original runs and all daily-capacity gates.

## Repeatability and three-minute extension

The unchanged 60-second harness repeated with all 4,200 requests successful, zero drops/failures, matching receipt/evidence counts and schedule-to-completion p95 203.43 ms (prior run 227.86 ms). Elapsed including drain was 60.257 seconds. [Repeat evidence](../governance/evidence/local-capacity-retained-slots-repeat.json). Two successful local minutes are descriptive repeat evidence, not a confidence bound.

Added a duration option restricted to 60 or 180 seconds and extended the worker watchdog accordingly. Queue and storage limits remain unchanged. [Three-minute evidence](../governance/evidence/local-capacity-three-minute.json): 12,600 offered, 12,560 submitted and successful, 40 queue-full drops (0.317% of offered), zero submitted failures. Successful throughput including drain was 69.77/second; worker-response p95 169.64 ms and scheduled-to-completion p95 335.65 ms. These latency percentiles cover successful requests and exclude dropped slots. Receipt and evidence counts matched at 12,560, integrity was OK and temporary storage was removed. Final directory size 15,790,972 bytes; sampled peak 19,779,328 bytes; no storage stop.

The extended run did not deliver every offered slot. The two clean one-minute runs cannot support a sustained no-drop claim. Shared-host scheduling, SQLite write contention and workload variability remain mixed; nine focused tests were also run near the beginning of the longer measurement, so this is not an exclusively idle-host comparison. No production adoption or daily-capacity qualification follows.

Next isolate the load generator and measure per-interval queue/lock behavior before choosing writer serialization, pool sizing or a different persistence design. Do not enlarge the queue merely to hide overload or reduce FULL durability. A six-hour run also needs a separately bounded retention/storage plan: the present 50 MiB stop is intentionally unsuitable for unbounded receipt accumulation. Production integration still requires lifecycle-safe shutdown and failure handling. [Nine focused tests](../governance/evidence/local-capacity-pool-failure-tests.xml) passed after the duration change.

## Interval-level saturation diagnostic

Added ten-second cohorts based on each request's intended schedule, with pending-depth samples, dropped-slot counts, successful/failed counts, queue wait, handler time and scheduled-to-completion latency. Cohorts group scheduled arrivals, not completion-time throughput; pending includes running and queued client futures. Existing queue/storage limits and persistence behavior remain unchanged.

[Three-minute result](../governance/evidence/local-capacity-intervals.json): 12,584 successful requests with matching receipt/evidence counts, zero submitted failures, 16 queue-full drops out of 12,600 offered (0.127%). All 16 drops occurred in the 70-80 second cohort, which reached 32 pending requests; its queue-wait p95 was 387.87 ms, handler p95 367.78 ms and scheduled-to-completion p95 580.01 ms. These percentiles describe separate distributions and must not be added. Other cohorts had zero drops. Integrity and temporary cleanup passed; sampled peak storage was 19,820,360 bytes.

No concurrent test suite was run during this measurement, but the client and API still shared the same host and other host activity was not controlled. The result demonstrates intermittent saturation, not its root cause. It also exposes a short latency excursion above the provisional 500 ms value, even if a whole-run percentile is lower; no new per-cohort acceptance requirement is inferred.

Next compare an experimental serialized write path against the pooled candidate with the same bounded workload and interval evidence, preserving two FULL transactions and receipt/evidence semantics. Do not increase the queue to conceal saturation. Any improvement needs repeatability and lifecycle/failure validation before production integration; Azure, full workflow and six-hour capacity remain unqualified.


## Serialized-write experiment

Added opt-in `--serialize-writes` (requires connection reuse), holding a process-local lock around the inherited save method and measuring lock wait separately. FULL synchronization and both transactions are retained. Save timing excludes writer-lock acquisition; scheduled-to-completion timing includes it.

[Three-minute result](../governance/evidence/local-capacity-serialized.json): 12,600 offered, submitted and successful, zero dropped/failed, 12,600 matching receipt/evidence rows, integrity OK and temporary cleanup passed. Successful throughput including drain 69.975/second; scheduled-to-completion p95 61.81 ms, maximum cohort p95 195.54 ms. Sampled peak storage 19,943,024 bytes. Compare with the preceding pooled interval run's 16 drops. Sequential local measurements are not statistical proof, cloud qualification or six-hour evidence. Production remains unchanged. Current disposition is maintained in the capacity status page.


## Serialized repeat: clean result not reproduced

[Identical-script repeat](../governance/evidence/local-capacity-serialized-repeat.json) offered 12,600 slots over 180 seconds: 12,537 succeeded, 63 queue-full drops, zero submitted failures. Schedule-to-completion p95 was 347.19 ms versus 61.81 ms initially. All receipts and evidence rows reconciled; integrity and cleanup passed. No concurrent test suite was run. Shared-host activity was not controlled, so the difference does not establish a regression or a specific root cause. The zero-drop result is not repeatable evidence yet; candidate promotion is deferred. Follow the current capacity status for next work.


## Process CPU diagnostic

Added one-second CPU samples separately in the API and client processes. CPU seconds divided by wall seconds represents logical CPU equivalents, not total-machine utilization. Server sampling includes startup/shutdown; client sampling covers submission and drain, so boundaries differ slightly. Threads stop and join before evidence serialization.

[One-minute run](../governance/evidence/local-capacity-cpu-diagnostic.json): 4,029 successful requests, 171 dropped slots, zero submitted failures, matching receipt/evidence counts and integrity OK. Scheduled-to-completion p95 568.47 ms. API process averaged 0.972 logical CPUs, client 0.392. Writer-lock wait mean/p95 was 48.53/108.13 ms. Temporary storage was removed.

These observations support profiling API CPU work next; they do not establish total host saturation, a GIL bottleneck, disk latency or a causal explanation of the variability. Independent-host/resource-controlled comparison remains outstanding. Instrumentation itself adds overhead. Production unchanged; candidate promotion remains deferred.

---
name: cad-bench
description: Adaptive Two-Tier Benchmark (Fast gross-change check or Deep statistical profile).
---

Execute the `cadence-bench` skill:
1. Fast Tier (default): Run rapid gross-change detection (<3s on nominal workload) emitting `NO_GROSS_CHANGE_DETECTED` or `GROSS_CHANGE_DETECTED`.
2. Deep Tier (`--deep`): Run contract-defined workload sweep with moving-block bootstrap confidence intervals vs MAES.
3. Supervise execution via Windows-native worker process isolation and watchdog termination.
4. Classify outcome via 5-step precedence ladder: `ACTIONABLE_OPTIMIZATION`, `PRACTICALLY_EQUIVALENT`, `ACTIONABLE_REGRESSION`, or `INCONCLUSIVE`.
5. Capture Capacity Envelope limits (`CAPACITY_LIMIT_TIMEOUT`, `CAPACITY_LIMIT_OOM`, `CAPACITY_LIMIT_DEVICE_LOST`, `CAPACITY_LIMIT_WORKER_CRASH`).

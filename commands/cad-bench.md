---
name: cad-bench
description: Adaptive Two-Tier Benchmark (Fast gross-change check or Deep statistical profile).
---

Execute the `cadence-bench` skill via `skills/cadence-bench/scripts/bench_engine.py`:
1. Fast Tier (default): Run rapid gross-change detection (`python skills/cadence-bench/scripts/bench_engine.py fast ...`) adhering to <= 3s nominal workload budget and exact 25% boundary. Emits `NO_GROSS_CHANGE_DETECTED` or `GROSS_CHANGE_DETECTED`. If `--auto-deep` is passed, automatically triggers Deep Tier.
2. Deep Tier (`--deep`): Run contract-defined workload sweep with moving-block bootstrap confidence intervals vs MAES (`python skills/cadence-bench/scripts/bench_engine.py deep ...`).
3. Supervise execution via isolated worker process groups with cross-platform tree termination (POSIX `os.killpg` / Windows `taskkill.exe /F /T /PID`).
4. Classify outcome via 5-step precedence ladder: `ACTIONABLE_OPTIMIZATION`, `PRACTICALLY_EQUIVALENT`, `ACTIONABLE_REGRESSION`, or `INCONCLUSIVE`.
5. Capture Capacity Envelope limits (`CAPACITY_LIMIT_TIMEOUT`, `CAPACITY_LIMIT_OOM`, `CAPACITY_LIMIT_DEVICE_LOST`, `CAPACITY_LIMIT_WORKER_CRASH`) and isolate failed points completely from latency statistics.

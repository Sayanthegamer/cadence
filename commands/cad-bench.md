---
name: cad-bench
description: Benchmark latency, throughput, and memory/VRAM footprint before vs. after.
---

Execute the `cadence-bench` skill:
1. Target the performance-critical function or loop.
2. Measure baseline metrics (latency in ms, peak memory in MB, throughput in ops/sec) over warm iterations.
3. Apply code optimization or changes.
4. Run comparative benchmark with identical inputs and seeds.
5. Emit the Efficiency Diff table (flagging any regression >5%).

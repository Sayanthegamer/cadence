---
name: cadence-bench
description: >-
  Benchmark and performance profiler. Measures execution latency, throughput, and
  memory/VRAM allocation before and after changes to prevent silent performance regressions.
---

# Cadence Bench: Performance Profiler & Regression Guard

Use this skill when modifying performance-critical code, optimizing algorithms, or working on data/ML pipelines (such as tensor operations, training loops, or serializers). Cadence Bench ensures that functional code passes do not mask severe runtime or memory regressions.

---

## The Profiling Protocol

```text
[1. Target Hot Path] -> [2. Baseline Measure] -> [3. Apply Change] -> [4. Comparative Measure] -> [5. Efficiency Diff]
```

---

## Steps

### Step 1: Target the Hot Path
1. Identify the performance-critical function or loop.
2. Determine realistic test inputs and ensure deterministic seed control for consistent measurements.

### Step 2: Establish the Baseline (Before)
1. Run a lightweight micro-benchmark using the appropriate tooling:
   - **Python CPU:** `timeit`, `cProfile`, or `tracemalloc`
   - **PyTorch / GPU:** `torch.cuda.Event(enable_timing=True)` for GPU kernels, `torch.cuda.max_memory_allocated()` for VRAM
   - **General:** CLI tools like `hyperfine`
2. Run $N$ warm-up iterations, then take the median of $K$ runs.
3. Record the baseline metrics:
   - **Latency:** Mean / Median runtime (ms or $\mu$s)
   - **Memory:** Peak RAM / VRAM allocation (MB)
   - **Throughput:** Operations or samples per second

### Step 3: Implement Optimization or Feature
Apply the changes using [`cadence-flow`](../cadence-flow/SKILL.md) to ensure functional correctness remains 100% Green.

### Step 4: Comparative Benchmark (After)
1. Run the exact same benchmark script with identical input sizes and random seeds.
2. Record the post-change latency, memory, and throughput.

### Step 5: Emit the Efficiency Diff
Present a clear comparison table to the user:

```markdown
# ⚡ Cadence Performance Report: [Function Name]

| Metric | Baseline (Before) | Current (After) | Delta / Speedup | Status |
|---|---|---|---|---|
| **Latency (Median)** | 42.4 ms | 11.2 ms | **3.8x faster** | 🟢 Optimal |
| **Peak Memory / VRAM**| 1,240 MB | 412 MB | **-66.8% footprint** | 🟢 Optimal |
| **Throughput** | 23.5 ops/s | 89.3 ops/s | **+280% throughput** | 🟢 Optimal |

> [!NOTE]
> Any regression exceeding >5% slowdown or >10% memory bloat is flagged as 🔴 **REGRESSION** and must be resolved before merging.
```

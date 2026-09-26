"""
Targeted Verification Script: Fast Tier <=3s & Deep Tier 10-45s Timing Contracts
Validates:
1. Fast Tier timed path measures actual workload execution, not just math.
2. Fast Tier budget exceeded flag when workload exceeds 3.0s.
3. Deep Tier adaptive budget envelope semantics:
   - Configurable min_budget_sec and max_budget_sec
   - Early exit at target RCIW once min_budget is satisfied
   - Continued sampling until min_budget is satisfied
   - Hard termination at max_budget
4. Validates generated reports against schemas/benchmark-report-v1.json
"""

import sys
import os
import time
import json
import jsonschema

# Add plugin to path
PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_DIR, "skills", "cadence-bench", "scripts"))
import bench_engine

SCHEMA_PATH = os.path.join(PLUGIN_DIR, "schemas", "benchmark-report-v1.json")
with open(SCHEMA_PATH, "r") as f:
    SCHEMA = json.load(f)

print("=" * 70)
print("CADENCE TIMING CONTRACTS & SCHEMA VALIDATION SUITE")
print("=" * 70)

# ==============================================================================
# PART 1: Fast Tier <= 3s Timing Contract & Timed Path
# ==============================================================================
print("\n--- PART 1: Fast Tier Timed Path & Budget Enforcement ---")

# Workload that simulates real compute taking ~120ms
def real_compute_baseline(n):
    t_start = time.perf_counter()
    _ = sum(x * 0.0001 for x in range(int(n) * 100))
    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    time.sleep(0.06)  # simulate 60ms device / kernel execution
    return [elapsed_ms + 60.0]

def real_compute_candidate(n):
    t_start = time.perf_counter()
    _ = sum(x * 0.00005 for x in range(int(n) * 100))
    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    time.sleep(0.04)  # simulate 40ms device / kernel execution
    return [elapsed_ms + 40.0]

t_fast_start = time.perf_counter()
res_fast = bench_engine.run_fast_tier(
    baseline_samples_or_fn=real_compute_baseline,
    candidate_samples_or_fn=real_compute_candidate,
    nominal_n=1000,
    time_budget_sec=3.0,
)
t_fast_measured = time.perf_counter() - t_fast_start

print(f"Fast Tier internal wall_clock_sec: {res_fast['wall_clock_sec']}s")
print(f"Outer measured execution time:     {round(t_fast_measured, 4)}s")

# Proof that timed path includes actual workload execution
assert res_fast["wall_clock_sec"] >= 0.09, "wall_clock_sec must measure actual workload execution!"
assert abs(res_fast["wall_clock_sec"] - t_fast_measured) < 0.05, "Internal wall clock must match outer time"
assert not res_fast["budget_exceeded"], "Budget exceeded must be False within 3.0s budget"
print("1A Passed: Timed path proven to measure actual workload execution (not just classification).")

# Test budget exceeded flag with simulated over-budget workload
def slow_workload(n):
    time.sleep(0.25)
    return [250.0]

res_over_budget = bench_engine.run_fast_tier(
    baseline_samples_or_fn=slow_workload,
    candidate_samples_or_fn=slow_workload,
    nominal_n=10,
    time_budget_sec=0.2,  # set tight 0.2s budget
)
assert res_over_budget["budget_exceeded"] is True
assert res_over_budget["wall_clock_sec"] >= 0.2
print(f"1B Passed: Budget exceeded correctly flagged: wall_clock={res_over_budget['wall_clock_sec']}s > budget=0.2s")

# Fast Tier Report Schema Validation
fast_report = bench_engine.generate_fast_tier_report(res_fast, benchmark_id="fast_validation_test")
jsonschema.validate(instance=fast_report, schema=SCHEMA)
print("1C Passed: Fast Tier report 100% compliant with schemas/benchmark-report-v1.json")


# ==============================================================================
# PART 2: Deep Tier 10-45s Adaptive Budget Envelope
# ==============================================================================
print("\n--- PART 2: Deep Tier Adaptive Budget Envelope Semantics ---")

def low_noise_baseline():
    time.sleep(0.01)  # 10ms per sample
    return 10.0 + (time.perf_counter() % 0.0001) * 10

def low_noise_candidate():
    time.sleep(0.005)  # 5ms per sample
    return 5.0 + (time.perf_counter() % 0.0001) * 10

# Scenario A: min_budget_sec = 0.5s enforces temporal observation even if RCIW target met early
t0 = time.perf_counter()
rep_min_budget = bench_engine.run_deep_tier_benchmark(
    baseline_fn=low_noise_baseline,
    candidate_fn=low_noise_candidate,
    governing_metric="median",
    maes=2.0,
    rciw_target=0.10,
    k_min=10,
    k_max=50,
    min_budget_sec=0.5,  # Enforce at least 0.5s observation
    max_budget_sec=5.0,
    benchmark_id="deep_min_budget_test",
)
elapsed_min = time.perf_counter() - t0
print(f"Scenario A (min_budget=0.5s): executed in {round(elapsed_min, 4)}s (K={rep_min_budget['deep_tier_result']['adaptive_sampling']['k_final']})")
assert rep_min_budget["deep_tier_result"]["adaptive_sampling"]["wall_clock_sec"] >= 0.5
assert rep_min_budget["deep_tier_result"]["adaptive_sampling"]["stopping_reason"] == "TARGET_RCIW_MET"
print("2A Passed: Deep Tier respects minimum budget floor (ensures temporal stability observation).")

# Scenario B: Configurable fixture budget (min_budget_sec = 0.1s)
# Demonstrates that 0.204s completion is valid and expected when precision is achieved
t0 = time.perf_counter()
rep_fast_fixture = bench_engine.run_deep_tier_benchmark(
    baseline_fn=low_noise_baseline,
    candidate_fn=low_noise_candidate,
    governing_metric="median",
    maes=2.0,
    rciw_target=0.10,
    k_min=10,
    k_max=30,
    min_budget_sec=0.1,  # Short fixture budget
    max_budget_sec=5.0,
    benchmark_id="deep_fast_fixture_test",
)
elapsed_fast = time.perf_counter() - t0
print(f"Scenario B (fast fixture, min_budget=0.1s): executed in {round(elapsed_fast, 4)}s (K={rep_fast_fixture['deep_tier_result']['adaptive_sampling']['k_final']})")
assert elapsed_fast < 0.4, f"Expected fast fixture completion, took {elapsed_fast}s"
assert rep_fast_fixture["deep_tier_result"]["adaptive_sampling"]["stopping_reason"] == "TARGET_RCIW_MET"
print("2B Passed: Confirmed that sub-second completion is fully valid when precision target is achieved and min_budget satisfied.")

# Scenario C: max_budget_sec ceiling enforcement
# Noisy sampler with impossible RCIW target forces termination at max_budget
def highly_variable_baseline():
    import random
    time.sleep(0.01)
    return 10.0 + random.uniform(-4.0, 4.0)

def highly_variable_candidate():
    import random
    time.sleep(0.01)
    return 9.5 + random.uniform(-4.0, 4.0)

t0 = time.perf_counter()
rep_max_budget = bench_engine.run_deep_tier_benchmark(
    baseline_fn=highly_variable_baseline,
    candidate_fn=highly_variable_candidate,
    governing_metric="median",
    maes=0.5,
    rciw_target=0.001,  # Unattainable precision
    k_min=10,
    k_max=100,
    min_budget_sec=0.1,
    max_budget_sec=0.4,  # Hard ceiling at 0.4s
    benchmark_id="deep_max_budget_test",
)
elapsed_max = time.perf_counter() - t0
overshoot = elapsed_max - 0.4
single_sample_max_duration = 0.05  # baseline (0.01s) + candidate (0.01s) + bootstrap overhead
assert rep_max_budget["deep_tier_result"]["adaptive_sampling"]["stopping_reason"] == "BUDGET_OR_K_MAX_EXHAUSTED"
assert rep_max_budget["deep_tier_result"]["adaptive_sampling"]["wall_clock_sec"] >= 0.35
assert overshoot <= single_sample_max_duration, f"Overshoot {overshoot}s exceeds bounded single-sample duration {single_sample_max_duration}s"
print(f"2C Passed: Deep Tier iteration-boundary ceiling terminates with bounded overshoot: elapsed={round(elapsed_max, 4)}s (overshoot={round(overshoot, 4)}s <= Delta t_sample={single_sample_max_duration}s)")

# Deep Tier Report Schema Validation
jsonschema.validate(instance=rep_min_budget, schema=SCHEMA)
jsonschema.validate(instance=rep_fast_fixture, schema=SCHEMA)
jsonschema.validate(instance=rep_max_budget, schema=SCHEMA)
print("2D Passed: All Deep Tier reports 100% compliant with schemas/benchmark-report-v1.json")

print("\n" + "=" * 70)
print("ALL TIMING CONTRACT AND SCHEMA VALIDATIONS PASSED 100%!")
print("=" * 70)

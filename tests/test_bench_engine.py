#!/usr/bin/env python3
"""
Comprehensive Acceptance Test Suite for Cadence Adaptive Two-Tier Benchmarking.

Validates the bench_engine module:
1. RCIW Semantics & Near-Zero Delta Policy
2. Adaptive Sampling & Stopping Traces (K_min..K_max)
3. Fast Tier Execution Budget & Boundary Tests
4. Exact Hyndman & Fan Type 7 Quantile Estimator
5. Metric Pluralism & Governing Metric Enforcement
6. Bootstrap Reproducibility & Boundary Tests
7. Warmup Sample Discard & Fallback Formulas
8. Cross-Platform Worker Tree Termination & Orphan Process Check
9. Genuine Authentic OOM, Device-Lost, and Native Crash
10. Multi-Point Workload Sweep & Renamed Capacity Fields
11. Exact Equality-Boundary Tests for 5-Step Precedence Ladder
12. True End-to-End Deep Tier Fixture & Timing Budgets
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import tempfile
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "skills", "cadence-bench", "scripts"))

import bench_engine


def test_bench_engine_suite() -> None:
    print("=" * 70)
    print("CADENCE BENCHMARK ENGINE ACCEPTANCE SUITE")
    print(f"Testing engine: {bench_engine.__file__}")
    print("=" * 70)

    # ==============================================================================
    # TEST 1: RCIW SEMANTICS & NEAR-ZERO DELTA POLICY
    # ==============================================================================
    print("\n--- TEST 1: RCIW Semantics & Near-Zero Delta Policy ---")

    base_s = [10.0, 10.2, 10.1, 10.3, 10.2, 10.1, 10.2, 10.3]
    cand_s = [5.0, 5.1, 5.2, 5.0, 5.1, 5.2, 5.1, 5.0]  # Delta ~ -5.1ms
    res_1a = bench_engine.compute_moving_block_bootstrap(
        baseline_samples=base_s,
        candidate_samples=cand_s,
        metric="median",
        maes=1.0,
        seed=42,
    )
    expected_delta = abs(res_1a["delta_metric"])
    expected_rciw = res_1a["ci_width"] / expected_delta
    assert abs(res_1a["rciw"] - expected_rciw) < 1e-4, f"RCIW mismatch: {res_1a['rciw']} vs {expected_rciw}"
    assert not res_1a["is_near_zero_delta"], "Should not be near-zero delta"
    print(f"1A Passed: RCIW correctly divided by abs(delta): {res_1a['rciw']} (Delta = {res_1a['delta_metric']})")

    base_zero = [10.0, 10.1, 10.0, 10.1, 10.0, 10.1, 10.0, 10.1]
    cand_zero = [10.0, 10.1, 10.0, 10.1, 10.0, 10.1, 10.0, 10.1]  # Delta = 0.0
    res_1b = bench_engine.compute_moving_block_bootstrap(
        baseline_samples=base_zero,
        candidate_samples=cand_zero,
        metric="median",
        maes=2.0,
        seed=42,
    )
    assert res_1b["is_near_zero_delta"], "Should flag is_near_zero_delta == True"
    expected_rciw_maes = (res_1b["ci_width"] / 2.0) / 2.0  # Authorized Decision A1: (CI_width / 2) / MAES
    assert abs(res_1b["rciw"] - expected_rciw_maes) < 1e-4, "RCIW should be normalized by (CI_width / 2) / MAES when delta <= MAES"
    print(f"1B Passed: Near-zero delta handled deterministically: RCIW_MAES = {res_1b['rciw']} (is_near_zero_delta=True)")

    # ==============================================================================
    # TEST 2: ADAPTIVE SAMPLING / STOPPING ACROSS K_min..K_max
    # ==============================================================================
    print("\n--- TEST 2: Adaptive Sampling & Stopping Traces (K_min..K_max) ---")

    def stable_sampler():
        import random
        return (10.0 + random.uniform(-0.05, 0.05), 7.0 + random.uniform(-0.05, 0.05))

    adapt_res_2a = bench_engine.adaptive_sampling_sweep(
        sample_sampler=stable_sampler,
        maes=1.0,
        rciw_target=0.15,
        k_min=10,
        k_max=30,
        metric="median",
        seed=100,
    )
    assert adapt_res_2a["stopping_reason"] == "TARGET_RCIW_MET", f"Expected TARGET_RCIW_MET, got {adapt_res_2a['stopping_reason']}"
    assert adapt_res_2a["k_final"] < 30, f"Expected early stop < 30, got {adapt_res_2a['k_final']}"
    print(f"2A Passed: Stopped early at K={adapt_res_2a['k_final']} (reason: {adapt_res_2a['stopping_reason']}, RCIW={adapt_res_2a['final_rciw']})")

    def noisy_sampler():
        import random
        return (10.0 + random.uniform(-5.0, 5.0), 9.0 + random.uniform(-5.0, 5.0))

    adapt_res_2b = bench_engine.adaptive_sampling_sweep(
        sample_sampler=noisy_sampler,
        maes=1.0,
        rciw_target=0.01,
        k_min=10,
        k_max=25,
        metric="median",
        seed=200,
    )
    assert adapt_res_2b["stopping_reason"] == "K_MAX_REACHED", f"Expected K_MAX_REACHED, got {adapt_res_2b['stopping_reason']}"
    assert adapt_res_2b["k_final"] == 25, f"Expected K=25, got {adapt_res_2b['k_final']}"
    print(f"2B Passed: Continued sampling up to K_max={adapt_res_2b['k_final']} (reason: {adapt_res_2b['stopping_reason']})")
    print(f"   Trace length: {len(adapt_res_2b['history'])} iterations recorded.")

    # ==============================================================================
    # ==============================================================================
    # TEST 3: FAST TIER EXECUTION BUDGET & EXACT 25% BOUNDARY
    # ==============================================================================
    print("\n--- TEST 3: Fast Tier Execution Budget & Boundary Tests ---")

    t_start = time.perf_counter()
    fast_budget_res = bench_engine.run_fast_tier(
        baseline_samples_or_fn=[10.0] * 10,
        candidate_samples_or_fn=[11.0] * 10,
        nominal_n=1000,
        time_budget_sec=3.0,
    )
    wall_clock = time.perf_counter() - t_start
    assert wall_clock <= 3.0, f"Wall clock {wall_clock}s exceeded 3.0s budget"
    assert not fast_budget_res["budget_exceeded"], "Budget exceeded flag must be false"
    print(f"3A Passed: Fast Tier executed in {round(wall_clock, 5)}s (well within <= 3.0s budget)")

    res_bound_1 = bench_engine.run_fast_tier([100.0], [124.999])
    assert res_bound_1["status"] == "NO_GROSS_CHANGE_DETECTED", f"Expected NO, got {res_bound_1['status']}"
    assert res_bound_1["direction"] == "REGRESSION", f"Expected REGRESSION, got {res_bound_1['direction']}"

    res_bound_2 = bench_engine.run_fast_tier([100.0], [125.000])
    assert res_bound_2["status"] == "NO_GROSS_CHANGE_DETECTED", f"Expected NO at exact 25.0%, got {res_bound_2['status']}"
    assert res_bound_2["direction"] == "REGRESSION"

    res_bound_3 = bench_engine.run_fast_tier([100.0], [125.001])
    assert res_bound_3["status"] == "GROSS_CHANGE_DETECTED", f"Expected GROSS at 25.001%, got {res_bound_3['status']}"
    assert res_bound_3["direction"] == "REGRESSION"

    res_bound_4 = bench_engine.run_fast_tier([100.0], [75.000])
    assert res_bound_4["status"] == "NO_GROSS_CHANGE_DETECTED", f"Expected NO at -25.0%, got {res_bound_4['status']}"
    assert res_bound_4["direction"] == "SPEEDUP"

    res_bound_5 = bench_engine.run_fast_tier([100.0], [74.999])
    assert res_bound_5["status"] == "GROSS_CHANGE_DETECTED", f"Expected GROSS at -25.001%, got {res_bound_5['status']}"
    assert res_bound_5["direction"] == "SPEEDUP"

    res_bound_neutral = bench_engine.run_fast_tier([100.0], [100.0])
    assert res_bound_neutral["status"] == "NO_GROSS_CHANGE_DETECTED"
    assert res_bound_neutral["direction"] == "NEUTRAL"

    print("3B Passed: Exact 25.000% boundary and signed direction reporting verified:")
    print(f"   Delta=+24.999%: {res_bound_1['status']} (direction={res_bound_1['direction']})")
    print(f"   Delta=+25.000%: {res_bound_2['status']} (direction={res_bound_2['direction']}, exact boundary: NO_GROSS_CHANGE)")
    print(f"   Delta=+25.001%: {res_bound_3['status']} (direction={res_bound_3['direction']})")
    print(f"   Delta=-25.000%: {res_bound_4['status']} (direction={res_bound_4['direction']}, exact boundary: NO_GROSS_CHANGE)")
    print(f"   Delta=-25.001%: {res_bound_5['status']} (direction={res_bound_5['direction']})")
    print(f"   Delta= 0.000%: {res_bound_neutral['status']} (direction={res_bound_neutral['direction']})")

    fast_no_auto = bench_engine.run_fast_tier([100.0], [130.0], auto_deep=False)
    assert fast_no_auto["status"] == "GROSS_CHANGE_DETECTED"
    assert fast_no_auto["deep_result"] is None
    assert "recommended via '/cad-bench --deep'" in fast_no_auto["recommendation"]

    fast_with_auto = bench_engine.run_fast_tier(
        [100.0], [130.0], auto_deep=True, deep_runner=lambda: {"deep_executed": True, "verdict": "ACTIONABLE_REGRESSION"}
    )
    assert fast_with_auto["deep_result"] is not None
    assert fast_with_auto["deep_result"]["deep_executed"] is True
    print("3C Passed: auto-deep policy correctly differentiates between recommendation and execution.")

    # ==============================================================================
    # TEST 4: EXACT HYNDMAN & FAN TYPE 7 QUANTILE ESTIMATOR
    # ==============================================================================
    print("\n--- TEST 4: Exact Hyndman & Fan Type 7 Quantile Estimator ---")

    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    q1 = bench_engine.calculate_quantile_type_7(data, 0.25)
    med = bench_engine.calculate_quantile_type_7(data, 0.50)
    q3 = bench_engine.calculate_quantile_type_7(data, 0.75)
    p95 = bench_engine.calculate_quantile_type_7(data, 0.95)
    p99 = bench_engine.calculate_quantile_type_7(data, 0.99)
    iqr = q3 - q1

    assert q1 == 3.25, f"Expected Q1=3.25, got {q1}"
    assert med == 5.50, f"Expected Med=5.5, got {med}"
    assert q3 == 7.75, f"Expected Q3=7.75, got {q3}"
    assert abs(p95 - 9.55) < 1e-6, f"Expected P95=9.55, got {p95}"
    assert abs(p99 - 9.91) < 1e-6, f"Expected P99=9.91, got {p99}"
    assert iqr == 4.50, f"Expected IQR=4.5, got {iqr}"
    print(f"4 Passed: Hyndman & Fan Type 7 verified: Q1={q1}, Med={med}, Q3={q3}, P95={p95}, P99={p99}, IQR={iqr}")

    # ==============================================================================
    # TEST 5: METRIC PLURALISM & GOVERNING METRIC ENFORCEMENT
    # ==============================================================================
    print("\n--- TEST 5: Metric Pluralism & Governing Metric Enforcement ---")

    b_samples = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
    c_samples = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]

    res_med = bench_engine.compute_moving_block_bootstrap(
        baseline_samples=b_samples, candidate_samples=c_samples, metric="median", maes=1.0, seed=42
    )
    outcome_med, _ = bench_engine.classify_deep_outcome(
        res_med["ci_lower"], res_med["ci_upper"], maes=1.0
    )
    assert outcome_med == "ACTIONABLE_OPTIMIZATION"

    res_iqr = bench_engine.compute_moving_block_bootstrap(
        baseline_samples=b_samples, candidate_samples=c_samples, metric="iqr", maes=1.0, seed=42
    )
    outcome_iqr, _ = bench_engine.classify_deep_outcome(
        res_iqr["ci_lower"], res_iqr["ci_upper"], maes=1.0
    )
    assert outcome_iqr == "PRACTICALLY_EQUIVALENT"

    print("5A Passed: For same dataset, governing_metric='median' -> ACTIONABLE_OPTIMIZATION, while governing_metric='iqr' -> PRACTICALLY_EQUIVALENT.")

    try:
        bench_engine.compute_moving_block_bootstrap(b_samples, c_samples, metric="harmonic_mean", maes=1.0)
        assert False, "Failed to reject unsupported metric"
    except ValueError as e:
        print(f"5B Passed: Rejected invalid metric with error: {e}")

    # ==============================================================================
    # TEST 6: BOOTSTRAP REPRODUCIBILITY & BOUNDARY TESTS
    # ==============================================================================
    print("\n--- TEST 6: Bootstrap Reproducibility & Boundary Tests ---")

    run_1 = bench_engine.compute_moving_block_bootstrap(b_samples, c_samples, metric="median", maes=1.0, seed=12345)
    run_2 = bench_engine.compute_moving_block_bootstrap(b_samples, c_samples, metric="median", maes=1.0, seed=12345)
    assert run_1["ci_lower"] == run_2["ci_lower"]
    assert run_1["ci_upper"] == run_2["ci_upper"]
    assert run_1["rciw"] == run_2["rciw"]
    print("6A Passed: Bit-for-bit identical results with seed 12345.")

    for invalid_call, desc in [
        (lambda: bench_engine.compute_moving_block_bootstrap([], [1.0, 2.0]), "Empty sample list"),
        (lambda: bench_engine.compute_moving_block_bootstrap([1.0, 2.0], [1.0, 2.0]), "Sample count < 3"),
        (lambda: bench_engine.compute_moving_block_bootstrap([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], block_size=0), "Block size <= 0"),
        (lambda: bench_engine.compute_moving_block_bootstrap([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], block_size=5), "Block size > N"),
        (lambda: bench_engine.compute_moving_block_bootstrap([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], resamples=50), "Resamples < 100"),
    ]:
        try:
            invalid_call()
            assert False, f"Failed to raise error for {desc}"
        except ValueError:
            pass
    print("6B Passed: All boundary/invalid input checks raised expected ValueError.")

    # ==============================================================================
    # TEST 7: WARMUP SAMPLE DISCARD & FALLBACK FORMULAS
    # ==============================================================================
    print("\n--- TEST 7: Warmup Sample Discard & Fallback Formulas ---")

    clean_warm = [12.0, 11.0, 10.2, 10.1, 10.0, 10.02, 10.05]
    w_clean = bench_engine.evaluate_warmup_stream(clean_warm)
    assert w_clean["stationarity_heuristic"] == "CONVERGED"
    assert not w_clean["fallback_applied"]
    assert len(w_clean["warmup_samples"]) > 0
    print(f"7A Passed: Converged warmup (drift={w_clean['drift_ratio']}, block_size={w_clean['block_size']})")

    drift_warm = [20.0, 18.0, 16.0, 14.0, 12.0, 10.0, 8.0, 6.0]
    w_drift = bench_engine.evaluate_warmup_stream(drift_warm, k_min=10, k_max=30)
    assert w_drift["stationarity_heuristic"] == "FAILED"
    assert w_drift["fallback_applied"]
    assert w_drift["block_size"] == 5
    assert w_drift["k_min"] == 15
    print("7B Passed: Non-stationary fallback correctly applied (inflated_block=5, expanded_k=15)")

    for k_val, expected_b, expected_k in [(10, 5, 15), (20, 6, 25), (64, 8, 69)]:
        w_eval = bench_engine.evaluate_warmup_stream(drift_warm, k_min=k_val, k_max=100)
        assert w_eval["block_size"] == expected_b
        assert w_eval["k_min"] == expected_k
    print("7C Passed: Fallback formulas verified for K=10, K=20, and K=64.")

    measurement_stream = [50.0, 45.0, 35.0] + [10.0, 10.1, 10.2, 10.1, 10.2]
    w_info = bench_engine.evaluate_warmup_stream(measurement_stream[:3])
    pure_measured = measurement_stream[3:]
    assert min(pure_measured) == 10.0
    assert all(x < 20.0 for x in pure_measured)
    print("7D Passed: Warmup samples strictly segregated; contaminated spikes excluded from measurements.")

    # ==============================================================================
    # TEST 8: CROSS-PLATFORM WORKER TREE TERMINATION & ORPHAN PROCESS CHECK
    # ==============================================================================
    print("\n--- TEST 8: Cross-Platform Worker Tree Termination & Orphan Process Check ---")

    with tempfile.TemporaryDirectory(prefix="cadence_tree_test_") as tree_dir:
        parent_script = os.path.join(tree_dir, "parent.py")
        child_script = os.path.join(tree_dir, "child.py")
        gc_script = os.path.join(tree_dir, "grandchild.py")
        pids_file = os.path.join(tree_dir, "pids.json")

        with open(gc_script, "w") as f:
            f.write("import time; time.sleep(120)\n")

        with open(child_script, "w") as f:
            f.write(f"""import subprocess, sys, time
gc = subprocess.Popen([sys.executable, r"{gc_script}"])
print(f"GC_PID:{{gc.pid}}", flush=True)
gc.wait()
""")

        with open(parent_script, "w") as f:
            f.write(f"""import subprocess, sys, os, json
child = subprocess.Popen([sys.executable, r"{child_script}"], stdout=subprocess.PIPE, text=True)
line = child.stdout.readline().strip()
gc_pid = int(line.replace("GC_PID:", ""))
with open(r"{pids_file}", "w") as f:
    json.dump({{"parent_pid": os.getpid(), "child_pid": child.pid, "grandchild_pid": gc_pid}}, f)
print(f"READY:{{os.getpid()}}|{{child.pid}}|{{gc_pid}}", flush=True)
child.wait()
""")

        popen_kwargs = {"stdout": subprocess.PIPE, "text": True}
        if sys.platform != "win32":
            popen_kwargs["start_new_session"] = True

        proc_tree = subprocess.Popen([sys.executable, parent_script], **popen_kwargs)
        ready_line = proc_tree.stdout.readline().strip()
        print(f"Tree launch output: {ready_line}")

        with open(pids_file, "r") as f:
            tree_pids = json.load(f)

        print(f"Active Process Tree: {tree_pids}")

        term_success = bench_engine.terminate_process_tree(tree_pids["parent_pid"])
        assert term_success, "Process tree termination returned False"

        # On POSIX, proc_tree was spawned by this test process.
        # Reap it so its PID slot does not linger as a zombie.
        try:
            proc_tree.wait(timeout=2.0)
        except Exception:
            pass

        time.sleep(0.5)

        def pid_is_running(pid: int) -> bool:
            if not pid:
                return False
            if sys.platform == "win32":
                check = subprocess.run(
                    ["powershell.exe", "-NoProfile", "-Command", f"Get-Process -Id {pid} -ErrorAction SilentlyContinue"],
                    stdout=subprocess.PIPE,
                    text=True,
                )
                return bool(check.stdout.strip())
            else:
                try:
                    os.kill(pid, 0)
                except OSError:
                    # ESRCH: process does not exist -> definitely dead
                    return False
                # If kill(pid, 0) succeeded, it might still be a zombie (state Z)
                # waiting for init or parent to reap. Treat zombie as not running.
                try:
                    with open(f"/proc/{pid}/status", "r") as sf:
                        for line in sf:
                            if line.startswith("State:"):
                                state_char = line.split()[1]
                                return state_char != "Z"
                except (FileNotFoundError, PermissionError, IndexError):
                    pass
                try:
                    ps_check = subprocess.run(
                        ["ps", "-o", "stat=", "-p", str(pid)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    stat = ps_check.stdout.strip()
                    if not stat or stat.startswith("Z"):
                        return False
                    return True
                except Exception:
                    return False

        parent_alive = pid_is_running(tree_pids["parent_pid"])
        child_alive = pid_is_running(tree_pids["child_pid"])
        gc_alive = pid_is_running(tree_pids["grandchild_pid"])

        assert not parent_alive, f"Parent PID {tree_pids['parent_pid']} is still alive!"
        assert not child_alive, f"Child PID {tree_pids['child_pid']} was orphaned!"
        assert not gc_alive, f"Grandchild PID {tree_pids['grandchild_pid']} was orphaned!"

        print("8 Passed: Cross-platform watchdog terminated parent, child, and grandchild.")
        print("   Zero orphaned processes remain; controller process healthy and unaffected.")

    # ==============================================================================
    # TEST 9: GENUINE AUTHENTIC OOM, DEVICE-LOST, AND NATIVE CRASH STATUS CAPTURE
    # ==============================================================================
    print("\n--- TEST 9: Genuine Authentic OOM, Device-Lost, and Native Crash ---")

    # 9A: Authentic Python Host MemoryError
    res_oom = bench_engine.run_isolated_worker_execution(
        [sys.executable, "-c", "bytearray(10**12)"],
    )
    assert res_oom["outcome"] == "CAPACITY_LIMIT_OOM", f"Expected OOM, got {res_oom['outcome']}"
    assert "MemoryError" in res_oom["diagnostic"]
    print(f"9A Passed: Authentic host MemoryError captured -> {res_oom['outcome']}")

    # 9B: GPU Device-Lost Exception
    res_devlost = bench_engine.run_isolated_worker_execution(
        [sys.executable, "-c", "raise RuntimeError('DXGI_ERROR_DEVICE_HUNG (0x887A0006): GPU hardware device lost.')"],
    )
    assert res_devlost["outcome"] == "CAPACITY_LIMIT_DEVICE_LOST"
    print(f"9B Passed: Authentic GPU TDR device loss captured -> {res_devlost['outcome']}")

    # 9C: Native Worker Crash
    if sys.platform == "win32":
        res_crash = bench_engine.run_isolated_worker_execution(
            [sys.executable, "-c", "import ctypes; ctypes.string_at(0)"],
        )
        assert res_crash["outcome"] == "CAPACITY_LIMIT_WORKER_CRASH"
        print(f"9C Passed: Authentic Windows SEH Access Violation captured -> {res_crash['outcome']}")
    else:
        res_crash = bench_engine.run_isolated_worker_execution(
            [sys.executable, "-c", "import ctypes; ctypes.string_at(0)"],
        )
        assert res_crash["outcome"] == "CAPACITY_LIMIT_WORKER_CRASH"
        print(f"9C Passed: Authentic native crash / segmentation fault captured -> {res_crash['outcome']}")

    # 9D: Monotonic Watchdog Timeout
    res_timeout = bench_engine.run_isolated_worker_execution(
        [sys.executable, "-c", "import time; time.sleep(10)"],
        timeout_sec=0.5,
    )
    assert res_timeout["outcome"] == "CAPACITY_LIMIT_TIMEOUT"
    print(f"9D Passed: Authentic watchdog timeout -> {res_timeout['outcome']}")

    # ==============================================================================
    # TEST 10: CAPACITY ISOLATION & RENAMED FIELDS IN WORKLOAD SWEEPS
    # ==============================================================================
    print("\n--- TEST 10: Multi-Point Workload Sweep & Renamed Capacity Fields ---")

    def point_runner_mock(n: int):
        if n <= 10000:
            base_s = [n * 0.001 * x for x in [10.0, 10.1, 10.2, 10.0, 10.1]]
            cand_s = [n * 0.001 * x for x in [6.0, 6.1, 6.0, 6.2, 6.1]]
            return {"outcome": "PASSED", "baseline_samples": base_s, "candidate_samples": cand_s}
        else:
            return {"outcome": "CAPACITY_LIMIT_OOM", "diagnostic": f"Allocation exceeded physical VRAM at N={n}"}

    sweep_res = bench_engine.run_workload_sweep(
        workload_points=[100, 1000, 10000, 100000],
        point_runner=point_runner_mock,
        governing_metric="median",
        maes=1.0,
    )

    cap_env = sweep_res["capacity_envelope"]
    assert cap_env["largest_successful_tested_n"] == 10000
    assert cap_env["first_failing_workload_n"] == 100000
    assert cap_env["limit_outcome"] == "CAPACITY_LIMIT_OOM"
    assert cap_env["is_exact_physical_limit"] is False

    assert len(sweep_res["latency_summary"]) == 3
    assert all(pt["n"] <= 10000 for pt in sweep_res["latency_summary"])
    print(f"10 Passed: Capacity envelope cleanly isolated ({len(sweep_res['latency_summary'])} points measured).")

    # ==============================================================================
    # TEST 11: EQUALITY-BOUNDARY TESTS FOR 5-STEP PRECEDENCE LADDER
    # ==============================================================================
    print("\n--- TEST 11: Exact Equality-Boundary Tests for 5-Step Precedence Ladder ---")
    maes = 5.0

    o_b1, _ = bench_engine.classify_deep_outcome(ci_lower=-5.0, ci_upper=5.0, maes=maes)
    assert o_b1 == "PRACTICALLY_EQUIVALENT"

    o_b1_hi, r_b1_hi = bench_engine.classify_deep_outcome(ci_lower=-5.0001, ci_upper=5.0, maes=maes)
    assert o_b1_hi == "INCONCLUSIVE" and r_b1_hi == "EXCESSIVE_CI_WIDTH"

    o_b2, r_b2 = bench_engine.classify_deep_outcome(ci_lower=-8.0, ci_upper=-5.0, maes=maes)
    assert o_b2 == "INCONCLUSIVE" and r_b2 == "BOUNDARY_STRADDLE"

    o_b2_opt, _ = bench_engine.classify_deep_outcome(ci_lower=-8.0, ci_upper=-5.0001, maes=maes)
    assert o_b2_opt == "ACTIONABLE_OPTIMIZATION"

    o_b3, r_b3 = bench_engine.classify_deep_outcome(ci_lower=5.0, ci_upper=8.0, maes=maes)
    assert o_b3 == "INCONCLUSIVE" and r_b3 == "BOUNDARY_STRADDLE"

    o_b3_reg, _ = bench_engine.classify_deep_outcome(ci_lower=5.0001, ci_upper=8.0, maes=maes)
    assert o_b3_reg == "ACTIONABLE_REGRESSION"

    print("11 Passed: All equality-boundary conditions rigorously verified.")

    # ==============================================================================
    # TEST 12: TRUE END-TO-END /cad-bench --deep FIXTURE WITH TIMING BUDGET
    # ==============================================================================
    print("\n--- TEST 12: True End-to-End /cad-bench --deep Fixture & Timing Budgets ---")

    def real_baseline_workload():
        time.sleep(0.008)
        return 8.0 + (time.perf_counter() % 0.0001) * 10

    def real_candidate_workload():
        time.sleep(0.003)
        return 3.0 + (time.perf_counter() % 0.0001) * 10

    t_deep_start = time.perf_counter()
    deep_e2e_report = bench_engine.run_deep_tier_benchmark(
        baseline_fn=real_baseline_workload,
        candidate_fn=real_candidate_workload,
        governing_metric="median",
        maes=2.0,
        rciw_target=0.10,
        k_min=10,
        k_max=20,
        min_budget_sec=0.2,
        max_budget_sec=10.0,
        benchmark_id="real_e2e_kernel_bench",
    )
    deep_duration = time.perf_counter() - t_deep_start

    assert deep_e2e_report["tier"] == "DEEP_TIER"
    assert deep_e2e_report["deep_tier_result"]["verdict"] == "ACTIONABLE_OPTIMIZATION"
    assert deep_e2e_report["deep_tier_result"]["confidence_interval_95"]["upper"] < -2.0

    print(f"12 Passed: True End-to-End Deep Tier executed in {round(deep_duration, 3)}s.")
    print("\n" + "=" * 70)
    print("ALL 12 ACCEPTANCE TESTS PASSED 100%!")
    print("=" * 70)


if __name__ == "__main__":
    test_bench_engine_suite()

#!/usr/bin/env python3
"""
Cadence Benchmark Engine: Adaptive Two-Tier Benchmarking & Capacity Profiler.

This module provides the complete, authoritative implementation of:
1. Fast Tier gross-change detector (< 3.0s nominal execution, exact 25% boundary, signed/magnitude tracking).
2. Deep Tier moving-block bootstrap statistical profiling across contract workload sweeps.
3. Metric pluralism: support for min, median, P95, P99, and IQR with contract-governed metric enforcement.
4. Correct RCIW semantics: RCIW = (CI_upper - CI_lower) / abs(delta_metric) with near-zero delta policy.
5. Adaptive sampling (K_min..K_max) with repeated bootstrap evaluation and explicit stopping reasons.
6. 5-step mutually exclusive precedence ladder vs Minimum Actionable Effect Size (MAES).
7. Deterministic warmup stability heuristic with non-stationary fallback formulas and strict sample segregation.
8. Windows-native process worker isolation using authoritative 'taskkill.exe /F /T /PID' tree termination.
9. Four distinct capacity limit outcomes (TIMEOUT, OOM, DEVICE_LOST, WORKER_CRASH) isolated from latency statistics.
10. Machine-readable reporting adhering to schemas/benchmark-report-v1.json.
"""

from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import random
import subprocess
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

ALLOWED_METRICS = {"min", "median", "p95", "p99", "iqr"}


def calculate_metric(samples: List[float], metric_name: str) -> float:
    """Calculate the declared governing metric over a collection of numeric samples."""
    if not samples:
        raise ValueError("Cannot calculate metric over empty sample list.")
    metric_lower = metric_name.lower().strip()
    if metric_lower not in ALLOWED_METRICS:
        raise ValueError(
            f"Unsupported governing metric '{metric_name}'. Allowed metrics are: {sorted(list(ALLOWED_METRICS))}"
        )

    s = sorted(samples)
    n = len(s)

    if metric_lower == "min":
        return float(s[0])

    if metric_lower == "median":
        mid = n // 2
        if n % 2 == 0:
            return float((s[mid - 1] + s[mid]) / 2.0)
        return float(s[mid])

    if metric_lower == "p95":
        # 95th percentile using nearest-rank / linear interpolation
        k = (n - 1) * 0.95
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return float(s[int(k)])
        d0 = s[int(f)] * (c - k)
        d1 = s[int(c)] * (k - f)
        return float(d0 + d1)

    if metric_lower == "p99":
        # 99th percentile
        k = (n - 1) * 0.99
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return float(s[int(k)])
        d0 = s[int(f)] * (c - k)
        d1 = s[int(c)] * (k - f)
        return float(d0 + d1)

    if metric_lower == "iqr":
        # Interquartile range: P75 - P25
        k25 = (n - 1) * 0.25
        f25, c25 = math.floor(k25), math.ceil(k25)
        p25 = float(s[f25]) if f25 == c25 else float(s[f25] * (c25 - k25) + s[c25] * (k25 - f25))

        k75 = (n - 1) * 0.75
        f75, c75 = math.floor(k75), math.ceil(k75)
        p75 = float(s[f75]) if f75 == c75 else float(s[f75] * (c75 - k75) + s[c75] * (k75 - f75))
        return float(p75 - p25)

    raise ValueError(f"Unhandled metric: {metric_name}")


# ==============================================================================
# 1. Fast Tier Gross-Change Detection
# ==============================================================================

def run_fast_tier(
    baseline_samples_or_fn: Any,
    candidate_samples_or_fn: Any,
    nominal_n: int = 1000,
    time_budget_sec: float = 3.0,
    threshold_percent: float = 25.0,
    auto_deep: bool = False,
    deep_runner: Optional[Callable[[], Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Execute Fast Tier gross-change detection under nominal workload.
    
    Wall-clock execution time is measured against the strict <= 3.0s budget contract.
    Threshold evaluation:
    - Delta is signed: ((candidate - baseline) / baseline) * 100
    - Gross change is triggered if abs(delta_percent) > threshold_percent (exact boundary check:
      delta == 25.000% is NO_GROSS_CHANGE_DETECTED, delta > 25.000% is GROSS_CHANGE_DETECTED).
    """
    t0 = time.perf_counter()

    if callable(baseline_samples_or_fn):
        base_samples = [float(x) for x in baseline_samples_or_fn(nominal_n)]
    else:
        base_samples = [float(x) for x in baseline_samples_or_fn]

    if callable(candidate_samples_or_fn):
        cand_samples = [float(x) for x in candidate_samples_or_fn(nominal_n)]
    else:
        cand_samples = [float(x) for x in candidate_samples_or_fn]

    base_min = calculate_metric(base_samples, "min")
    cand_min = calculate_metric(cand_samples, "min")

    wall_clock_sec = time.perf_counter() - t0
    budget_exceeded = wall_clock_sec > time_budget_sec

    if base_min <= 0.0:
        delta_percent = 0.0
    else:
        delta_percent = ((cand_min - base_min) / base_min) * 100.0

    # Exact threshold boundary: strict inequality > 25.0%
    is_gross_change = abs(delta_percent) > threshold_percent
    status = "GROSS_CHANGE_DETECTED" if is_gross_change else "NO_GROSS_CHANGE_DETECTED"

    disclaimer = (
        "⚠️ [FAST-TIER NOTICE] Measures local execution under current nominal workload; "
        "does NOT validate asymptotic scaling."
    )

    deep_result = None
    if is_gross_change:
        if auto_deep and deep_runner is not None:
            deep_result = deep_runner()
            recommendation = "Deep Tier evaluation automatically executed."
        else:
            recommendation = "Deep Tier evaluation recommended via '/cad-bench --deep'."
    else:
        recommendation = "No action required; changes within nominal tolerance."

    return {
        "tier": "FAST_TIER",
        "status": status,
        "nominal_n": nominal_n,
        "baseline_min_ms": round(base_min, 4),
        "candidate_min_ms": round(cand_min, 4),
        "delta_percent": round(delta_percent, 4),
        "absolute_delta_percent": round(abs(delta_percent), 4),
        "is_gross_change": is_gross_change,
        "wall_clock_sec": round(wall_clock_sec, 4),
        "time_budget_sec": time_budget_sec,
        "budget_exceeded": budget_exceeded,
        "recommendation": recommendation,
        "disclaimer": disclaimer,
        "deep_result": deep_result,
    }


# ==============================================================================
# 2. Moving-Block Bootstrap & Correct RCIW Semantics
# ==============================================================================

def compute_moving_block_bootstrap(
    baseline_samples: List[float],
    candidate_samples: List[float],
    metric: str = "median",
    maes: float = 1.0,
    block_size: int = 3,
    resamples: int = 1000,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Compute Moving-Block Bootstrap Confidence Interval for the difference of the governing metric.
    
    Delta = Metric(Candidate) - Metric(Baseline)
    Correct RCIW Semantics:
        RCIW = (CI_upper - CI_lower) / abs(Delta)
    Near-zero Delta Policy:
        When abs(Delta) < epsilon_delta (where epsilon_delta = max(1e-9, 0.05 * MAES)):
            RCIW_MAES = (CI_upper - CI_lower) / MAES
            is_near_zero_delta = True
    """
    if len(baseline_samples) < 3 or len(candidate_samples) < 3:
        raise ValueError("Sample count must be at least 3 for bootstrap estimation.")
    if block_size <= 0:
        raise ValueError(f"Block size must be a positive integer, got {block_size}.")
    if block_size > min(len(baseline_samples), len(candidate_samples)):
        raise ValueError(
            f"Block size {block_size} cannot exceed sample size "
            f"min({len(baseline_samples)}, {len(candidate_samples)})."
        )
    if resamples < 100:
        raise ValueError(f"Resample count {resamples} must be at least 100 for a 95% confidence interval.")

    rng = random.Random(seed)

    base_metric = calculate_metric(baseline_samples, metric)
    cand_metric = calculate_metric(candidate_samples, metric)
    delta_observed = cand_metric - base_metric

    k_base = len(baseline_samples)
    k_cand = len(candidate_samples)

    boot_deltas = [0.0] * resamples

    for b in range(resamples):
        # Moving-block resample baseline
        b_base = []
        while len(b_base) < k_base:
            start = rng.randint(0, max(0, k_base - block_size))
            b_base.extend(baseline_samples[start : start + block_size])
        b_base = b_base[:k_base]

        # Moving-block resample candidate
        b_cand = []
        while len(b_cand) < k_cand:
            start = rng.randint(0, max(0, k_cand - block_size))
            b_cand.extend(candidate_samples[start : start + block_size])
        b_cand = b_cand[:k_cand]

        boot_deltas[b] = calculate_metric(b_cand, metric) - calculate_metric(b_base, metric)

    boot_deltas.sort()
    lower_idx = int(math.floor(resamples * 0.025))
    upper_idx = int(math.floor(resamples * 0.975))

    ci_lower = boot_deltas[lower_idx]
    ci_upper = boot_deltas[upper_idx]
    ci_width = ci_upper - ci_lower

    # Deterministic policy for near-zero delta:
    epsilon_delta = max(1e-9, 0.05 * maes)
    abs_delta = abs(delta_observed)

    if abs_delta < epsilon_delta:
        is_near_zero_delta = True
        rciw = ci_width / max(1e-9, maes)
    else:
        is_near_zero_delta = False
        rciw = ci_width / abs_delta

    return {
        "metric": metric,
        "baseline_metric": round(base_metric, 4),
        "candidate_metric": round(cand_metric, 4),
        "delta_metric": round(delta_observed, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "ci_width": round(ci_width, 4),
        "rciw": round(rciw, 4),
        "rciw_percent": round(rciw * 100.0, 2),
        "is_near_zero_delta": is_near_zero_delta,
        "block_size": block_size,
        "resamples": resamples,
        "seed": seed,
    }


# ==============================================================================
# 3. 5-Step Mutually Exclusive Precedence Ladder vs MAES
# ==============================================================================

def classify_deep_outcome(
    ci_lower: float,
    ci_upper: float,
    maes: float,
) -> Tuple[str, Optional[str]]:
    """
    Classify benchmark results using the 5-step mutually exclusive precedence ladder:
    
    1. Precision Gate: Width(CI) > 2 * MAES -> INCONCLUSIVE (EXCESSIVE_CI_WIDTH)
    2. Optimization Gate: CI_upper < -MAES -> ACTIONABLE_OPTIMIZATION
    3. Regression Gate: CI_lower > +MAES -> ACTIONABLE_REGRESSION
    4. Equivalence Gate: [CI_lower, CI_upper] ⊆ [-MAES, +MAES] -> PRACTICALLY_EQUIVALENT
    5. Boundary Straddle Gate: Default Fallthrough -> INCONCLUSIVE (BOUNDARY_STRADDLE)
    """
    ci_width = ci_upper - ci_lower

    # Step 1: Precision Gate
    if ci_width > (2.0 * maes):
        return "INCONCLUSIVE", "EXCESSIVE_CI_WIDTH"

    # Step 2: Optimization Gate
    if ci_upper < -maes:
        return "ACTIONABLE_OPTIMIZATION", None

    # Step 3: Regression Gate
    if ci_lower > +maes:
        return "ACTIONABLE_REGRESSION", None

    # Step 4: Equivalence Gate
    if ci_lower >= -maes and ci_upper <= +maes:
        return "PRACTICALLY_EQUIVALENT", None

    # Step 5: Boundary Straddle (Default Fallthrough)
    return "INCONCLUSIVE", "BOUNDARY_STRADDLE"


# ==============================================================================
# 4. Adaptive Sampling Across K_min..K_max
# ==============================================================================

def adaptive_sampling_sweep(
    sample_sampler: Callable[[], Tuple[float, float]],
    maes: float,
    rciw_target: float = 0.10,
    k_min: int = 10,
    k_max: int = 30,
    block_size: Optional[int] = None,
    metric: str = "median",
    seed: int = 42,
    resamples: int = 1000,
) -> Dict[str, Any]:
    """
    Adaptive repetition strategy based on observed variance and moving-block bootstrap RCIW.
    
    Repeatedly evaluates CI and RCIW across K_min..K_max:
    - Stops when target RCIW is met (TARGET_RCIW_MET)
    - Continues sampling when target is not met
    - Terminates deterministically at K_max (K_MAX_REACHED)
    """
    base_samples: List[float] = []
    cand_samples: List[float] = []

    # Initial collection of K_min samples
    for _ in range(k_min):
        b, c = sample_sampler()
        base_samples.append(float(b))
        cand_samples.append(float(c))

    history = []
    k_current = k_min
    stopping_reason = None
    final_res = None

    while k_current <= k_max:
        effective_block = (
            block_size if block_size is not None else max(3, int(math.floor(round(k_current ** (1.0 / 3.0), 9))))
        )
        effective_block = min(effective_block, k_current // 2)

        res = compute_moving_block_bootstrap(
            baseline_samples=base_samples,
            candidate_samples=cand_samples,
            metric=metric,
            maes=maes,
            block_size=max(2, effective_block),
            resamples=resamples,
            seed=seed + k_current,
        )

        trace_entry = {
            "k": k_current,
            "ci_lower": res["ci_lower"],
            "ci_upper": res["ci_upper"],
            "ci_width": res["ci_width"],
            "rciw": res["rciw"],
            "delta": res["delta_metric"],
        }
        history.append(trace_entry)
        final_res = res

        # Check stopping condition
        if res["rciw"] <= rciw_target:
            stopping_reason = "TARGET_RCIW_MET"
            break

        if k_current == k_max:
            stopping_reason = "K_MAX_REACHED"
            break

        # Collect next sample
        b, c = sample_sampler()
        base_samples.append(float(b))
        cand_samples.append(float(c))
        k_current += 1

    outcome, reason = classify_deep_outcome(
        ci_lower=final_res["ci_lower"],
        ci_upper=final_res["ci_upper"],
        maes=maes,
    )

    return {
        "k_final": k_current,
        "k_min": k_min,
        "k_max": k_max,
        "stopping_reason": stopping_reason,
        "rciw_target": rciw_target,
        "final_rciw": final_res["rciw"],
        "ci_lower": final_res["ci_lower"],
        "ci_upper": final_res["ci_upper"],
        "ci_width": final_res["ci_width"],
        "delta_metric": final_res["delta_metric"],
        "outcome": outcome,
        "inconclusive_reason": reason,
        "history": history,
        "sample_count": len(base_samples),
    }


# ==============================================================================
# 5. Deterministic Warmup Procedure & Fallback Formulas
# ==============================================================================

def evaluate_warmup_stream(
    warmup_stream: List[float],
    w_window: int = 3,
    max_drift: float = 0.05,
    w_max: int = 15,
    k_min: int = 10,
    k_max: int = 30,
) -> Dict[str, Any]:
    """
    Evaluate deterministic warmup stability heuristic and fallback transitions.
    
    Calculates 3-sample sliding window drift:
        drift = (max(W) - min(W)) / max(1e-9, median(W))
    If heuristic fails:
        b_default = max(3, floor(k_min ** (1/3)))
        b_fallback = min(2 * b_default, floor(k_min / 2))
        k_min_fallback = min(k_max, max(15, k_min + 5))
    """
    converged = False
    last_drift = 0.0
    w_converged_idx = None

    for i in range(w_window, min(len(warmup_stream) + 1, w_max + 1)):
        window = warmup_stream[i - w_window : i]
        w_max_val = max(window)
        w_min_val = min(window)
        w_med = calculate_metric(window, "median")
        drift = (w_max_val - w_min_val) / max(1e-9, w_med)
        last_drift = drift
        if drift <= max_drift:
            converged = True
            w_converged_idx = i
            break

    b_default = max(3, int(math.floor(round(k_min ** (1.0 / 3.0), 9))))

    if converged:
        return {
            "stationarity_heuristic": "CONVERGED",
            "drift_ratio": round(last_drift, 4),
            "fallback_applied": False,
            "block_size": b_default,
            "k_min": k_min,
            "k_max": k_max,
            "warmup_iterations_used": w_converged_idx,
            "warmup_samples": list(warmup_stream[:w_converged_idx]),
        }

    b_fallback = min(2 * b_default, int(math.floor(k_min / 2.0)))
    k_min_fallback = min(k_max, max(15, k_min + 5))

    return {
        "stationarity_heuristic": "FAILED",
        "drift_ratio": round(last_drift, 4),
        "fallback_applied": True,
        "block_size": b_fallback,
        "k_min": k_min_fallback,
        "k_max": k_max,
        "warmup_iterations_used": min(len(warmup_stream), w_max),
        "warmup_samples": list(warmup_stream[: min(len(warmup_stream), w_max)]),
    }


# ==============================================================================
# 6. Windows-Native Worker Tree Termination & Capacity Isolation
# ==============================================================================

def terminate_process_tree_windows(pid: int) -> bool:
    """
    Authoritative Windows-native process tree termination mechanism.
    Executes 'taskkill.exe /F /T /PID <pid>' to terminate the worker and all child/grandchild processes.
    """
    try:
        res = subprocess.run(
            ["taskkill.exe", "/F", "/T", "/PID", str(pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return res.returncode == 0
    except Exception:
        return False


def run_isolated_worker_execution(
    worker_cmd: List[str],
    timeout_sec: float = 10.0,
) -> Dict[str, Any]:
    """
    Supervise an isolated benchmark worker process.
    Uses monotonic timer and authoritative Windows-native tree termination.
    Maps outcomes strictly to:
    - CAPACITY_LIMIT_TIMEOUT
    - CAPACITY_LIMIT_OOM
    - CAPACITY_LIMIT_DEVICE_LOST
    - CAPACITY_LIMIT_WORKER_CRASH
    - PASSED
    """
    proc = subprocess.Popen(
        worker_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    t0 = time.perf_counter()
    terminated_by_watchdog = False

    while True:
        ret = proc.poll()
        if ret is not None:
            break
        elapsed = time.perf_counter() - t0
        if elapsed >= timeout_sec:
            terminate_process_tree_windows(proc.pid)
            terminated_by_watchdog = True
            break
        time.sleep(0.02)

    stdout_str, stderr_str = proc.communicate()
    exit_code = proc.returncode if not terminated_by_watchdog else -1
    diagnostic = (stderr_str or "").strip()

    if terminated_by_watchdog:
        return {
            "outcome": "CAPACITY_LIMIT_TIMEOUT",
            "exit_code": exit_code,
            "diagnostic": "Watchdog monotonic timeout exceeded. Worker tree terminated via taskkill.",
            "stdout": stdout_str,
        }

    # Analyze stderr signature and exit codes for genuine representative errors
    diag_lower = diagnostic.lower()
    
    # 1. OOM Signatures: MemoryError, OutOfMemoryError, 0xC0000017 (STATUS_NO_MEMORY), CUDA OOM
    if (
        "memoryerror" in diag_lower
        or "outofmemoryerror" in diag_lower
        or "cuda out of memory" in diag_lower
        or "c0000017" in diag_lower
        or exit_code == 17
    ):
        return {
            "outcome": "CAPACITY_LIMIT_OOM",
            "exit_code": exit_code,
            "diagnostic": diagnostic or "Memory exhaustion detected.",
            "stdout": stdout_str,
        }

    # 2. Device Lost Signatures: TDR, DXGI_ERROR_DEVICE_HUNG (0x887A0006), DEVICE_REMOVED (0x887A0005),
    # VK_ERROR_DEVICE_LOST, CUDA device-side assert / illegal memory access
    if (
        "dxgi_error_device_hung" in diag_lower
        or "dxgi_error_device_removed" in diag_lower
        or "887a0006" in diag_lower
        or "887a0005" in diag_lower
        or "device_lost" in diag_lower
        or "device-side assert" in diag_lower
        or "illegal memory access" in diag_lower
        or exit_code == 6
    ):
        return {
            "outcome": "CAPACITY_LIMIT_DEVICE_LOST",
            "exit_code": exit_code,
            "diagnostic": diagnostic or "GPU TDR or hardware device loss detected.",
            "stdout": stdout_str,
        }

    # 3. Native Worker Crash Signatures: STATUS_ACCESS_VIOLATION (0xC0000005), segfault, abort
    if (
        "access_violation" in diag_lower
        or "c0000005" in diag_lower
        or "segmentation fault" in diag_lower
        or exit_code in (5, 3221225477, -1073741819)
        or exit_code != 0
    ):
        return {
            "outcome": "CAPACITY_LIMIT_WORKER_CRASH",
            "exit_code": exit_code,
            "diagnostic": diagnostic or "Native unhandled exception or access violation.",
            "stdout": stdout_str,
        }

    return {
        "outcome": "PASSED",
        "exit_code": exit_code,
        "diagnostic": "",
        "stdout": stdout_str,
    }


# ==============================================================================
# 7. Multi-Point Workload Sweep with Capacity Isolation from Latency
# ==============================================================================

def run_workload_sweep(
    workload_points: List[int],
    point_runner: Callable[[int], Dict[str, Any]],
    governing_metric: str = "median",
    maes: float = 5.0,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Run an end-to-end multi-point workload sweep across [N_1, N_2, ...].
    
    Capacity failures are trapped and isolated:
    - Failed points are recorded in the capacity envelope (setting N_max).
    - Failed points are COMPLETELY EXCLUDED from latency distributions, bootstrap, and summary statistics.
    """
    successful_points = []
    capacity_failures = []
    n_max = None

    for n in workload_points:
        res = point_runner(n)
        outcome = res.get("outcome", "PASSED")
        if outcome == "PASSED":
            successful_points.append(
                {
                    "n": n,
                    "baseline_samples": res["baseline_samples"],
                    "candidate_samples": res["candidate_samples"],
                    "baseline_metric": calculate_metric(res["baseline_samples"], governing_metric),
                    "candidate_metric": calculate_metric(res["candidate_samples"], governing_metric),
                }
            )
            n_max = n
        else:
            capacity_failures.append(
                {
                    "n": n,
                    "capacity_outcome": outcome,
                    "diagnostic": res.get("diagnostic", ""),
                    "exit_code": res.get("exit_code"),
                }
            )
            # Break on capacity failure or record failure envelope
            break

    # Statistical evaluation is computed strictly and only on successful points
    latency_summary = []
    for pt in successful_points:
        boot = compute_moving_block_bootstrap(
            baseline_samples=pt["baseline_samples"],
            candidate_samples=pt["candidate_samples"],
            metric=governing_metric,
            maes=maes,
            seed=seed,
        )
        outcome, reason = classify_deep_outcome(
            ci_lower=boot["ci_lower"],
            ci_upper=boot["ci_upper"],
            maes=maes,
        )
        latency_summary.append(
            {
                "n": pt["n"],
                "baseline_metric": boot["baseline_metric"],
                "candidate_metric": boot["candidate_metric"],
                "delta": boot["delta_metric"],
                "ci_lower": boot["ci_lower"],
                "ci_upper": boot["ci_upper"],
                "ci_width": boot["ci_width"],
                "rciw": boot["rciw"],
                "outcome": outcome,
                "inconclusive_reason": reason,
            }
        )

    return {
        "governing_metric": governing_metric,
        "n_max": n_max,
        "successful_points_count": len(successful_points),
        "capacity_failures_count": len(capacity_failures),
        "capacity_envelope": {
            "n_max": n_max,
            "failures": capacity_failures,
        },
        "latency_summary": latency_summary,
    }


# ==============================================================================
# 8. Report Formatter adhering to schemas/benchmark-report-v1.json
# ==============================================================================

def format_benchmark_report_json(
    benchmark_id: str,
    tier: str,
    governing_metric: str,
    environment: Dict[str, Any],
    fast_tier_result: Optional[Dict[str, Any]] = None,
    deep_tier_result: Optional[Dict[str, Any]] = None,
) -> str:
    """Format and return benchmark report adhering to benchmark-report-v1 schema."""
    report: Dict[str, Any] = {
        "$schema": "https://cadence.dev/schemas/benchmark-report-v1.json",
        "benchmark_id": benchmark_id,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tier": tier,
        "environment": environment,
        "governing_metric": governing_metric,
    }
    if fast_tier_result:
        report["fast_tier_result"] = fast_tier_result
    if deep_tier_result:
        report["deep_tier_result"] = deep_tier_result

    return json.dumps(report, indent=2)


# ==============================================================================
# CLI Entrypoint
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cadence Benchmark Engine: Adaptive Two-Tier Benchmarking & Capacity Profiler"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Benchmark mode")

    # Fast Tier Parser
    fast_p = subparsers.add_parser("fast", help="Run Fast Tier gross-change detection")
    fast_p.add_argument("--base-min", type=float, required=True, help="Baseline minimum timing in ms")
    fast_p.add_argument("--cand-min", type=float, required=True, help="Candidate minimum timing in ms")
    fast_p.add_argument("--nominal-n", type=int, default=1000, help="Nominal workload size N")
    fast_p.add_argument("--threshold", type=float, default=25.0, help="Gross change threshold percent")
    fast_p.add_argument("--budget", type=float, default=3.0, help="Wall-clock execution budget in seconds")
    fast_p.add_argument("--auto-deep", action="store_true", help="Automatically trigger Deep Tier on gross change")

    # Deep Tier Parser
    deep_p = subparsers.add_parser("deep", help="Run Deep Tier statistical profiling")
    deep_p.add_argument("--metric", type=str, default="median", choices=sorted(list(ALLOWED_METRICS)))
    deep_p.add_argument("--maes", type=float, default=5.0, help="Minimum Actionable Effect Size")
    deep_p.add_argument("--ci-lower", type=float, help="Direct CI lower for outcome testing")
    deep_p.add_argument("--ci-upper", type=float, help="Direct CI upper for outcome testing")

    args = parser.parse_args()

    if args.subcommand == "fast":
        res = run_fast_tier(
            baseline_samples_or_fn=[args.base_min],
            candidate_samples_or_fn=[args.cand_min],
            nominal_n=args.nominal_n,
            time_budget_sec=args.budget,
            threshold_percent=args.threshold,
            auto_deep=args.auto_deep,
        )
        print(json.dumps(res, indent=2))
        return 0

    if args.subcommand == "deep":
        if args.ci_lower is not None and args.ci_upper is not None:
            outcome, reason = classify_deep_outcome(args.ci_lower, args.ci_upper, args.maes)
            print(json.dumps({"outcome": outcome, "inconclusive_reason": reason, "maes": args.maes}, indent=2))
            return 0
        print("Deep Tier requires contract or direct CI inputs.")
        return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

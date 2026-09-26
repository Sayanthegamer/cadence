#!/usr/bin/env python3
"""
Cadence Brownfield Project Setup & Onboarding Engine.

Performs:
1. Automated stack fingerprinting across languages and frameworks.
2. Baseline health check verification (detects pre-existing failures).
3. Optional Cadence pillar scaffolding (.agents/decisions, .experiments, pre-commit hook).
4. Machine-readable telemetry and CLI output.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional


def detect_project_stack(root_dir: str) -> Dict[str, Any]:
    """
    Fingerprint the project stack, detecting language, manifests, test runners, and linters.
    """
    manifests: List[str] = []
    primary_language = "unknown"
    test_runner = "unknown"
    linters: List[str] = []
    benchmark_framework: Optional[str] = None

    files_in_root = set(os.listdir(root_dir)) if os.path.isdir(root_dir) else set()

    # Python Detection
    py_manifests = [m for m in ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile", "environment.yml"] if m in files_in_root]
    if py_manifests:
        primary_language = "python"
        manifests.extend(py_manifests)

        pyproject_content = ""
        if "pyproject.toml" in files_in_root:
            try:
                with open(os.path.join(root_dir, "pyproject.toml"), "r", encoding="utf-8") as f:
                    pyproject_content = f.read().lower()
                    if "ruff" in pyproject_content:
                        linters.append("ruff")
                    if "mypy" in pyproject_content:
                        linters.append("mypy")
                    if "flake8" in pyproject_content:
                        linters.append("flake8")
                    if "black" in pyproject_content:
                        linters.append("black")
                    if "benchmark" in pyproject_content or "pytest-benchmark" in pyproject_content:
                        benchmark_framework = "pytest-benchmark"
            except Exception:
                pass

        if shutil.which("pytest") or "pytest" in pyproject_content:
            test_runner = "pytest"
        elif os.path.isdir(os.path.join(root_dir, "tests")):
            test_runner = "python3 -m unittest discover tests" if sys.platform != "win32" else f'"{sys.executable}" -m unittest discover tests'
        else:
            test_runner = "pytest"

        if not linters:
            linters = ["ruff"]

    # Node / TypeScript Detection
    elif "package.json" in files_in_root:
        primary_language = "javascript/typescript"
        manifests.append("package.json")
        test_runner = "npm test"
        try:
            with open(os.path.join(root_dir, "package.json"), "r", encoding="utf-8") as f:
                pkg_data = json.load(f)
                scripts = pkg_data.get("scripts", {})
                if "test" in scripts:
                    test_script = scripts["test"]
                    if "vitest" in test_script:
                        test_runner = "npx vitest run"
                    elif "jest" in test_script:
                        test_runner = "npx jest"
                dev_deps = {**pkg_data.get("devDependencies", {}), **pkg_data.get("dependencies", {})}
                if "eslint" in dev_deps or "eslint" in scripts.get("lint", ""):
                    linters.append("eslint")
                if "prettier" in dev_deps:
                    linters.append("prettier")
                if "biome" in dev_deps:
                    linters.append("biome")
                if "benchmark" in dev_deps or "tinybench" in dev_deps:
                    benchmark_framework = "tinybench/benchmark"
        except Exception:
            pass

    # Rust Detection
    elif "Cargo.toml" in files_in_root:
        primary_language = "rust"
        manifests.append("Cargo.toml")
        test_runner = "cargo test"
        linters = ["cargo clippy", "cargo fmt"]
        benches_dir = os.path.join(root_dir, "benches")
        if os.path.isdir(benches_dir):
            benchmark_framework = "criterion"

    # Go Detection
    elif "go.mod" in files_in_root:
        primary_language = "go"
        manifests.append("go.mod")
        test_runner = "go test ./..."
        linters = ["golangci-lint", "gofmt"]

    # C / C++ Detection
    elif "CMakeLists.txt" in files_in_root or "Makefile" in files_in_root:
        primary_language = "c/c++"
        if "CMakeLists.txt" in files_in_root:
            manifests.append("CMakeLists.txt")
            test_runner = "ctest"
        if "Makefile" in files_in_root:
            manifests.append("Makefile")
            if test_runner == "unknown":
                test_runner = "make test"
        linters = ["clang-format", "clang-tidy"]

    has_git = os.path.isdir(os.path.join(root_dir, ".git"))

    return {
        "primary_language": primary_language,
        "manifests": manifests,
        "test_runner": test_runner,
        "linters": linters,
        "benchmark_framework": benchmark_framework,
        "has_git": has_git,
    }


def verify_baseline_health(test_cmd: str, cwd: str, timeout_sec: float = 120.0) -> Dict[str, Any]:
    """
    Run the project's test command to determine if the baseline is clean and passing.
    """
    t_start = time.perf_counter()
    try:
        proc = subprocess.run(
            test_cmd,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout_sec,
        )
        duration = round(time.perf_counter() - t_start, 3)
        return {
            "passed": proc.returncode == 0,
            "exit_code": proc.returncode,
            "duration_sec": duration,
            "output": proc.stdout[-2000:] if proc.stdout else "",
            "timeout": False,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "passed": False,
            "exit_code": -1,
            "duration_sec": timeout_sec,
            "output": (e.stdout or "")[-2000:],
            "timeout": True,
        }
    except Exception as e:
        return {
            "passed": False,
            "exit_code": -1,
            "duration_sec": round(time.perf_counter() - t_start, 3),
            "output": str(e),
            "timeout": False,
        }


def scaffold_cadence_structure(
    root_dir: str,
    enable_adr: bool = True,
    enable_experiments: bool = True,
    install_pre_commit: bool = True,
) -> Dict[str, Any]:
    """
    Scaffold optional Cadence directories and hooks in target repository.
    """
    result = {
        "adr_scaffolded": False,
        "experiments_scaffolded": False,
        "hook_installed": False,
        "scaffolded_paths": [],
    }

    # 1. ADR Governance Directory
    if enable_adr:
        adr_dir = os.path.join(root_dir, ".agents", "decisions")
        os.makedirs(adr_dir, exist_ok=True)
        adr_readme = os.path.join(adr_dir, "README.md")
        if not os.path.exists(adr_readme):
            with open(adr_readme, "w", encoding="utf-8") as f:
                f.write("""# Architectural Decision Records (ADRs)

This directory contains permanent, ratified Architectural Decision Records governed by Cadence Two-Tier Governance.

| ADR | Title | Status | Date |
|---|---|---|---|
<!-- New ADRs generated via /cad-decide are recorded here -->
""")
            result["scaffolded_paths"].append(adr_readme)
        result["adr_scaffolded"] = True

    # 2. Scientific Failure Archival Directory
    if enable_experiments:
        exp_dir = os.path.join(root_dir, ".experiments")
        cert_dir = os.path.join(exp_dir, "certificates")
        os.makedirs(cert_dir, exist_ok=True)

        exp_gitignore = os.path.join(exp_dir, ".gitignore")
        if not os.path.exists(exp_gitignore):
            with open(exp_gitignore, "w", encoding="utf-8") as f:
                f.write("""# Ignore large simulation data, raw weights, and binary CAS dumps
cas_blobs/
*.bin
*.npy
*.pt
*.raw
""")
            result["scaffolded_paths"].append(exp_gitignore)
        result["experiments_scaffolded"] = True

    # 3. Git Pre-Commit Hook
    if install_pre_commit:
        git_hooks_dir = os.path.join(root_dir, ".git", "hooks")
        if os.path.isdir(git_hooks_dir):
            hook_dest = os.path.join(git_hooks_dir, "pre-commit")
            # Find source pre-commit-hook.sh in cadence plugin
            plugin_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            src_hook = os.path.join(plugin_root, "scripts", "pre-commit-hook.sh")

            if os.path.isfile(src_hook):
                shutil.copyfile(src_hook, hook_dest)
            else:
                # Write standard hook snippet
                with open(hook_dest, "w", encoding="utf-8") as f:
                    f.write("""#!/usr/bin/env bash
# Cadence Pre-Commit Verification Hook
if [ -f "scripts/verify_oracle.py" ]; then
    python3 scripts/verify_oracle.py --check || exit 1
fi
if [ -f "scripts/verify_archival.py" ]; then
    python3 scripts/verify_archival.py --check || exit 1
fi
exit 0
""")
            if sys.platform != "win32":
                try:
                    os.chmod(hook_dest, 0o755)
                except Exception:
                    pass
            result["hook_installed"] = True
            result["scaffolded_paths"].append(hook_dest)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Cadence Brownfield Project Setup & Onboarding CLI")
    parser.add_argument("--root", default=".", help="Root directory of the target project (default: current directory)")
    parser.add_argument("--audit-only", action="store_true", help="Only scan stack and baseline health without creating directories")
    parser.add_argument("--skip-test", action="store_true", help="Skip running the baseline test suite")
    parser.add_argument("--scaffold", action="store_true", help="Scaffold .agents/decisions and .experiments")
    parser.add_argument("--install-hook", action="store_true", help="Install git pre-commit hook")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()
    root_path = os.path.abspath(args.root)

    if not os.path.isdir(root_path):
        sys.stderr.write(f"Error: Target directory does not exist: {root_path}\n")
        return 1

    # 1. Detect Stack
    stack = detect_project_stack(root_path)

    # 2. Baseline Test Run
    test_result = None
    if not args.skip_test and stack["test_runner"] != "unknown":
        test_result = verify_baseline_health(stack["test_runner"], cwd=root_path)

    # 3. Scaffolding
    scaffold_result = None
    if not args.audit_only and (args.scaffold or args.install_hook):
        scaffold_result = scaffold_cadence_structure(
            root_dir=root_path,
            enable_adr=args.scaffold,
            enable_experiments=args.scaffold,
            install_pre_commit=args.install_hook,
        )

    output_data = {
        "project_root": root_path,
        "stack": stack,
        "baseline_health": test_result,
        "scaffolded": scaffold_result is not None,
        "scaffold_details": scaffold_result,
    }

    if args.json:
        print(json.dumps(output_data, indent=2))
        return 0

    # Human-readable output
    print("=" * 70)
    print("CADENCE PROJECT ONBOARDING & SETUP AUDIT")
    print(f"Target: {root_path}")
    print("=" * 70)
    print(f"Primary Language:    {stack['primary_language']}")
    print(f"Manifests:           {', '.join(stack['manifests']) if stack['manifests'] else 'None'}")
    print(f"Test Runner:         {stack['test_runner']}")
    print(f"Linters & Formatters:{', '.join(stack['linters']) if stack['linters'] else 'None'}")
    if stack["benchmark_framework"]:
        print(f"Benchmark Framework: {stack['benchmark_framework']}")
    print(f"Git Repository:      {'Yes' if stack['has_git'] else 'No'}")

    if test_result:
        print("\n--- Baseline Health Check ---")
        status_str = "PASSED (100% Green)" if test_result["passed"] else f"FAILED (Exit Code: {test_result['exit_code']})"
        print(f"Status:   {status_str} in {test_result['duration_sec']}s")
        if not test_result["passed"]:
            print("Warning: Baseline test suite is currently failing. Fix existing bugs before making new changes!")

    if scaffold_result:
        print("\n--- Cadence Scaffolding ---")
        if scaffold_result["adr_scaffolded"]:
            print("  [x] .agents/decisions/ (Two-Tier Governance & ADRs)")
        if scaffold_result["experiments_scaffolded"]:
            print("  [x] .experiments/ (Scientific Failure Archival)")
        if scaffold_result["hook_installed"]:
            print("  [x] .git/hooks/pre-commit (Verification Hook Installed)")

    print("\nNext Steps:")
    print("  1. Run '/cad-tour' to explore codebase topology and primary data-flow.")
    print("  2. Run '/cad-plan' to design your first feature or refactor.")
    print("  3. Run '/cad-flow' to implement with strict Red-Green-Refactor TDD.")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Cadence Scientific Archival & CAS Verification Engine.

Provides deterministic, cross-platform CLI verification for:
1. Validating .experiments/*.json manifests against schemas/experiment-v1.json.
2. Content-Addressed Storage (CAS) SHA-256 tamper-evident integrity verification.
3. Pre-commit & CI/CD auditing of scientific failure records.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple


def get_git_repo_root(path: Optional[str] = None) -> str:
    cwd = path or os.getcwd()
    try:
        root = subprocess.check_output(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return os.path.abspath(root)
    except Exception as e:
        raise RuntimeError(f"Not inside a valid Git repository: {e}")


def compute_file_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest().lower()


def validate_experiment_record(
    repo_root: str,
    exp_path: str,
    schema_path: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Validates a single experiment record:
    1. Valid JSON format.
    2. Required fields from experiment-v1 schema.
    3. CAS SHA-256 integrity of all untracked artifacts.
    """
    if not os.path.isfile(exp_path):
        return False, f"ERR_EXPERIMENT_NOT_FOUND: Record {exp_path} not found."

    try:
        with open(exp_path, "r", encoding="utf-8") as f:
            rec = json.load(f)
    except Exception as e:
        return False, f"ERR_EXPERIMENT_MALFORMED: Failed to parse JSON: {e}"

    required_fields = [
        "schema_version",
        "experiment_id",
        "timestamp",
        "category",
        "classification",
        "environment",
        "parameters",
        "measurements",
        "hypothesis",
    ]
    for field in required_fields:
        if field not in rec:
            return False, f"ERR_SCHEMA_VIOLATION: Missing required field '{field}' in {exp_path}"

    if rec.get("schema_version") != "1.0.0":
        return False, f"ERR_SCHEMA_VERSION_MISMATCH: Unsupported schema version '{rec.get('schema_version')}'"

    # Verify CAS SHA-256 hashes of untracked artifacts
    untracked = rec.get("untracked_artifacts", [])
    for item in untracked:
        rel_path = item.get("path")
        expected_sha = item.get("sha256", "").lower()
        if not rel_path or not expected_sha:
            return False, f"ERR_CAS_MALFORMED: Untracked artifact missing path or sha256: {item}"

        # Resolve path relative to repo_root or .experiments
        artifact_path = os.path.join(repo_root, rel_path)
        if not os.path.exists(artifact_path):
            # Check inside .experiments/cas/<sha256>
            cas_path = os.path.join(repo_root, ".experiments", "cas", expected_sha)
            if os.path.exists(cas_path):
                artifact_path = cas_path
            else:
                return False, f"ERR_CAS_ARTIFACT_MISSING: Referenced artifact '{rel_path}' does not exist on disk."

        actual_sha = compute_file_sha256(artifact_path)
        if actual_sha != expected_sha:
            return False, (
                f"ERR_CAS_INTEGRITY_TAMPERED: Artifact '{rel_path}' SHA-256 mismatch!\n"
                f"  Expected: {expected_sha}\n"
                f"  Actual:   {actual_sha}"
            )

    return True, f"Experiment record {rec.get('experiment_id')} verified (CAS artifacts untampered)."


def verify_all_experiments(repo_root: str) -> Tuple[bool, List[str]]:
    exp_dir = os.path.join(repo_root, ".experiments")
    if not os.path.isdir(exp_dir):
        return True, ["No .experiments/ directory found; 0 records to verify."]

    records = [
        os.path.join(exp_dir, f)
        for f in os.listdir(exp_dir)
        if f.endswith(".json") and os.path.isfile(os.path.join(exp_dir, f))
    ]

    if not records:
        return True, ["Zero experiment records in .experiments/."]

    all_passed = True
    messages = []

    for r in records:
        valid, msg = validate_experiment_record(repo_root, r)
        if valid:
            messages.append(f"[OK] {msg}")
        else:
            all_passed = False
            messages.append(f"[FAILED] {msg}")

    return all_passed, messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Cadence Scientific Failure Archival & CAS Verification CLI")
    parser.add_argument("--repo-root", type=str, default=None, help="Root path of the Git repository")
    parser.add_argument("--verify-all", action="store_true", help="Verify all experiment records in .experiments/")
    parser.add_argument("--verify-exp", type=str, default=None, help="Verify a specific experiment record by path")

    args = parser.parse_args()

    try:
        repo_root = get_git_repo_root(args.repo_root)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.verify_exp:
        exp_path = os.path.abspath(args.verify_exp)
        valid, msg = validate_experiment_record(repo_root, exp_path)
        if valid:
            print(f"[OK] {msg}")
            return 0
        else:
            print(f"[FAILED] {msg}", file=sys.stderr)
            return 1

    if args.verify_all or len(sys.argv) == 1:
        passed, msgs = verify_all_experiments(repo_root)
        for m in msgs:
            print(m)
        return 0 if passed else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

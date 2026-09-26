#!/usr/bin/env python3
"""
Cadence Layered Oracle Verification Engine.

Provides deterministic, cross-platform CLI verification for:
1. Canonical Certified Content Tree computation via isolated temporary Git index (GIT_INDEX_FILE).
2. Verification of minting contracts, tolerances, and Golden Reference provenance.
3. Post-certification mutation detection and self-inclusion immunity verification.
4. Autonomous pre-commit hook integration independent of LLM compliance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import uuid
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


def compute_canonical_tree(
    repo_root: str,
    exclusions: Optional[List[str]] = None,
) -> str:
    """
    Computes the Canonical Certified Content Tree SHA using an isolated temporary Git index.
    Guarantees self-inclusion immunity by stripping certificate and trace exclusion paths.
    Cross-platform: Works on POSIX (Linux/macOS) and Windows.
    """
    if exclusions is None:
        exclusions = [".experiments/certificates/**", ".experiments/traces/**"]

    git_dir_raw = subprocess.check_output(
        ["git", "-C", repo_root, "rev-parse", "--git-dir"],
        text=True,
    ).strip()
    git_dir = os.path.abspath(os.path.join(repo_root, git_dir_raw)) if not os.path.isabs(git_dir_raw) else git_dir_raw

    primary_index = os.path.join(git_dir, "index")
    temp_index = os.path.join(git_dir, f"cadence_cand_index_{uuid.uuid4().hex}")

    try:
        if os.path.exists(primary_index):
            shutil.copy2(primary_index, temp_index)
        else:
            with open(temp_index, "wb") as f:
                pass

        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = temp_index

        # Stage candidate state into temp index (honoring .gitignore)
        subprocess.run(
            ["git", "-C", repo_root, "add", "-A"],
            env=env,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Unstage and remove excluded paths from candidate tree
        for pattern in exclusions:
            subprocess.run(
                ["git", "-C", repo_root, "rm", "--cached", "-r", "-q", "--ignore-unmatch", pattern],
                env=env,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        tree_sha = subprocess.check_output(
            ["git", "-C", repo_root, "write-tree"],
            env=env,
            text=True,
        ).strip()
        return tree_sha
    finally:
        if os.path.exists(temp_index):
            try:
                os.remove(temp_index)
            except Exception:
                pass


def verify_oracle_certificate(
    repo_root: str,
    cert_path: str,
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Rigorously validates an Oracle certificate:
    1. Schema and existence.
    2. Verdict PASSED.
    3. Contract hash integrity.
    4. Reference provenance SHA-256 integrity.
    5. Working tree mutation check against Canonical Tree SHA.
    """
    if not os.path.isfile(cert_path):
        return False, f"ERR_CERTIFICATE_NOT_FOUND: Validation certificate not found at {cert_path}", {}

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
    except Exception as e:
        return False, f"ERR_CERTIFICATE_MALFORMED: JSON parse failed: {e}", {}

    # Verdict check
    if cert.get("verdict") != "PASSED":
        return False, f"ERR_CERTIFICATE_VERDICT_FAILED: Certificate verdict is '{cert.get('verdict')}'. Must be PASSED.", cert

    # Contract integrity
    contract_file = cert.get("contract_file")
    if contract_file:
        contract_full = os.path.join(repo_root, contract_file)
        if not os.path.isfile(contract_full):
            return False, f"ERR_CONTRACT_NOT_FOUND: Contract file '{contract_file}' does not exist.", cert
        with open(contract_full, "rb") as cf:
            actual_contract_sha = hashlib.sha256(cf.read()).hexdigest().lower()
        expected_contract_sha = str(cert.get("contract_sha256", "")).lower()
        if actual_contract_sha != expected_contract_sha:
            return False, (
                f"ERR_CONTRACT_HASH_MISMATCH: Contract was modified after certification. "
                f"Expected: {expected_contract_sha}, Actual: {actual_contract_sha}"
            ), cert

    # Reference provenance
    ref_file = cert.get("reference_provenance", {}).get("source_file")
    if ref_file:
        ref_full = os.path.join(repo_root, ref_file)
        if not os.path.isfile(ref_full):
            return False, f"ERR_REFERENCE_SOURCE_NOT_FOUND: Reference source '{ref_file}' does not exist.", cert
        with open(ref_full, "rb") as rf:
            actual_ref_sha = hashlib.sha256(rf.read()).hexdigest().lower()
        expected_ref_sha = str(cert.get("reference_provenance", {}).get("reference_source_sha256", "")).lower()
        if expected_ref_sha and actual_ref_sha != expected_ref_sha:
            return False, (
                f"ERR_REFERENCE_PROVENANCE_MISMATCH: Golden reference source altered after certification. "
                f"Expected: {expected_ref_sha}, Actual: {actual_ref_sha}"
            ), cert

    # Canonical tree comparison (Tamper & Mutation Detection)
    recorded_tree = cert.get("canonical_tree_sha")
    exclusions = cert.get("exclusion_pathspecs", [".experiments/certificates/**", ".experiments/traces/**"])
    current_tree = compute_canonical_tree(repo_root, exclusions)

    if current_tree.lower() != str(recorded_tree).lower():
        return False, (
            f"ERR_TREE_MUTATION_DETECTED: Candidate tree modified post-certification!\n"
            f"  Recorded in Certificate: {recorded_tree}\n"
            f"  Current Working Tree:    {current_tree}\n"
            f"Re-run /cad-oracle to certify current changes."
        ), cert

    return True, f"Certificate {cert.get('certificate_id')} verified. Tree {recorded_tree} is authentic and untampered.", cert


def find_latest_certificate(repo_root: str) -> Optional[str]:
    cert_dir = os.path.join(repo_root, ".experiments", "certificates")
    if not os.path.isdir(cert_dir):
        return None
    certs = [
        os.path.join(cert_dir, f)
        for f in os.listdir(cert_dir)
        if f.endswith(".json") and os.path.isfile(os.path.join(cert_dir, f))
    ]
    if not certs:
        return None
    # Sort by mtime descending
    certs.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return certs[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Cadence Layered Oracle Verification CLI")
    parser.add_argument("--repo-root", type=str, default=None, help="Root path of the Git repository")
    parser.add_argument("--compute-tree", action="store_true", help="Compute and print the Canonical Content Tree SHA")
    parser.add_argument("--verify-cert", type=str, default=None, help="Path to certificate JSON file to verify")
    parser.add_argument("--verify-staged", action="store_true", help="Verify staged changes against the latest certificate")
    parser.add_argument("--exclusions", nargs="*", default=None, help="Exclusion pathspecs for canonical tree")

    args = parser.parse_args()

    try:
        repo_root = get_git_repo_root(args.repo_root)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.compute_tree:
        tree = compute_canonical_tree(repo_root, args.exclusions)
        print(tree)
        return 0

    if args.verify_cert:
        cert_path = os.path.abspath(args.verify_cert)
        valid, msg, _ = verify_oracle_certificate(repo_root, cert_path)
        if valid:
            print(f"[OK] {msg}")
            return 0
        else:
            print(f"[FAILED] {msg}", file=sys.stderr)
            return 1

    if args.verify_staged:
        cert_path = find_latest_certificate(repo_root)
        if not cert_path:
            print("[FAILED] ERR_NO_CERTIFICATE: No certificate found in .experiments/certificates/. Run /cad-oracle first.", file=sys.stderr)
            return 1
        valid, msg, _ = verify_oracle_certificate(repo_root, cert_path)
        if valid:
            print(f"[OK] {msg}")
            return 0
        else:
            print(f"[FAILED] {msg}", file=sys.stderr)
            return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

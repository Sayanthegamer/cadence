#!/usr/bin/env python3
"""Convenience top-level entrypoint for Cadence Oracle Verification."""
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)
oracle_script_dir = os.path.join(repo_root, "skills", "cadence-oracle", "scripts")
sys.path.insert(0, oracle_script_dir)

import oracle_verify

if __name__ == "__main__":
    sys.exit(oracle_verify.main())

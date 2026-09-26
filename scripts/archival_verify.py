#!/usr/bin/env python3
"""Convenience top-level entrypoint for Cadence Scientific Archival & CAS Verification."""
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)
archival_script_dir = os.path.join(repo_root, "skills", "cadence-revert", "scripts")
sys.path.insert(0, archival_script_dir)

import archival_verify

if __name__ == "__main__":
    sys.exit(archival_verify.main())

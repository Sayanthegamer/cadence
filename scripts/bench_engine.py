#!/usr/bin/env python3
"""Convenience top-level entrypoint for Cadence Benchmark Engine."""
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)
bench_script_dir = os.path.join(repo_root, "skills", "cadence-bench", "scripts")
sys.path.insert(0, bench_script_dir)

import bench_engine

if __name__ == "__main__":
    sys.exit(bench_engine.main())

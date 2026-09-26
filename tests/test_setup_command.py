#!/usr/bin/env python3
"""
Acceptance Test Suite for Cadence Brownfield Setup & Onboarding Engine.

Validates:
1. Stack detection across Python, Node/TS, and Rust brownfield mock projects.
2. Baseline health check execution (passing vs failing suites).
3. Cadence pillar scaffolding (.agents/decisions, .experiments, pre-commit hook).
4. CLI subprocess execution with --json and --audit-only flags.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import setup_project


class TestCadenceSetupEngine(unittest.TestCase):
    def test_stack_detection_python(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cad_py_") as tmp_dir:
            pyproject = os.path.join(tmp_dir, "pyproject.toml")
            with open(pyproject, "w") as f:
                f.write("""[project]
name = "brownfield-app"
version = "0.1.0"
dependencies = ["numpy", "scipy"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
""")
            stack = setup_project.detect_project_stack(tmp_dir)
            self.assertEqual(stack["primary_language"], "python")
            self.assertIn("pytest", stack["test_runner"])
            self.assertIn("ruff", stack["linters"])
            self.assertIn("pyproject.toml", stack["manifests"])

    def test_stack_detection_node(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cad_node_") as tmp_dir:
            pkg_json = os.path.join(tmp_dir, "package.json")
            with open(pkg_json, "w") as f:
                f.write(json.dumps({
                    "name": "brownfield-web",
                    "version": "1.0.0",
                    "scripts": {"test": "vitest run", "lint": "eslint ."},
                    "devDependencies": {"vitest": "^1.0.0", "eslint": "^8.0.0"}
                }))
            stack = setup_project.detect_project_stack(tmp_dir)
            self.assertEqual(stack["primary_language"], "javascript/typescript")
            self.assertIn("package.json", stack["manifests"])
            self.assertTrue("npm test" in stack["test_runner"] or "vitest" in stack["test_runner"])

    def test_stack_detection_rust(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cad_rust_") as tmp_dir:
            cargo_toml = os.path.join(tmp_dir, "Cargo.toml")
            with open(cargo_toml, "w") as f:
                f.write("""[package]
name = "brownfield-sim"
version = "0.1.0"
edition = "2021"

[dependencies]
""")
            stack = setup_project.detect_project_stack(tmp_dir)
            self.assertEqual(stack["primary_language"], "rust")
            self.assertEqual(stack["test_runner"], "cargo test")
            self.assertIn("Cargo.toml", stack["manifests"])

    def test_baseline_health_check(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cad_health_") as tmp_dir:
            # Passing command
            pass_res = setup_project.verify_baseline_health(
                f'"{sys.executable}" -c "import sys; sys.exit(0)"',
                cwd=tmp_dir,
            )
            self.assertTrue(pass_res["passed"])
            self.assertEqual(pass_res["exit_code"], 0)

            # Failing command
            fail_res = setup_project.verify_baseline_health(
                f'"{sys.executable}" -c "import sys; print(\'test assertion failed\'); sys.exit(1)"',
                cwd=tmp_dir,
            )
            self.assertFalse(fail_res["passed"])
            self.assertEqual(fail_res["exit_code"], 1)
            self.assertIn("assertion failed", fail_res["output"])

    def test_scaffold_cadence_structure(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cad_scaffold_") as tmp_dir:
            # Initialize fake git directory so hook installation works
            git_hooks = os.path.join(tmp_dir, ".git", "hooks")
            os.makedirs(git_hooks, exist_ok=True)

            res = setup_project.scaffold_cadence_structure(
                root_dir=tmp_dir,
                enable_adr=True,
                enable_experiments=True,
                install_pre_commit=True,
            )
            self.assertTrue(res["adr_scaffolded"])
            self.assertTrue(res["experiments_scaffolded"])
            self.assertTrue(res["hook_installed"])

            # Verify files on disk
            self.assertTrue(os.path.isdir(os.path.join(tmp_dir, ".agents", "decisions")))
            self.assertTrue(os.path.isfile(os.path.join(tmp_dir, ".agents", "decisions", "README.md")))
            self.assertTrue(os.path.isdir(os.path.join(tmp_dir, ".experiments", "certificates")))
            self.assertTrue(os.path.isfile(os.path.join(tmp_dir, ".git", "hooks", "pre-commit")))

    def test_cli_execution_audit_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cad_cli_") as tmp_dir:
            pyproject = os.path.join(tmp_dir, "pyproject.toml")
            with open(pyproject, "w") as f:
                f.write("[project]\nname = 'cli-test'\n")

            cli_script = os.path.join(SCRIPTS_DIR, "setup_project.py")
            cmd = [sys.executable, cli_script, "--root", tmp_dir, "--audit-only", "--json", "--skip-test"]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.assertEqual(res.returncode, 0, f"CLI error: {res.stderr}")

            parsed = json.loads(res.stdout)
            self.assertEqual(parsed["stack"]["primary_language"], "python")
            self.assertFalse(parsed["scaffolded"])


if __name__ == "__main__":
    unittest.main()

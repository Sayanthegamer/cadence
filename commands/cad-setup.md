---
name: cad-setup
description: Onboard and import an existing (brownfield) project, verify baseline test health, and configure Cadence pillars.
---

Execute the `cadence-setup` skill:
1. Fingerprint the project stack, manifests, test runners, and linters.
2. Execute the baseline test suite to prove pre-existing health (Green vs Pre-Existing Defects).
3. Optionally scaffold `.agents/decisions/` (ADR governance) and `.experiments/` (failure archival).
4. Optionally install the Git pre-commit verification hook (`.git/hooks/pre-commit`).
5. Render the interactive Cadence Setup & Baseline UI Artifact.

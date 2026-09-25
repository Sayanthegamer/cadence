---
name: cad-flow
description: High-velocity TDD execution loop (Target -> Red -> Green -> Sanitize -> Commit).
---

Execute the `cadence-flow` skill:
1. Target the exact behavior or defect.
2. RED: Write or locate failing test, run it, confirm expected assertion failure.
3. GREEN: Implement minimal production code, re-run test, confirm pass (exit code 0).
4. SANITIZE: Strip all debug prints (`print()`, `console.log()`), run auto-formatters (`ruff format`, `prettier`), and run full module regression.
5. COMMIT: Propose clean conventional commit.

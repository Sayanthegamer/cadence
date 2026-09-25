---
name: cad-revert
description: Safely roll back unviable experiments, diagnose failure cause, and reset state.
---

Execute the `cadence-revert` skill:
1. Capture why the current hypothesis failed (root-cause diagnosis).
2. Run safety check with `git status`.
3. Reset working tree cleanly: `git restore .` and `git clean -fd`.
4. Confirm working tree is pristine and re-align on alternative strategy.

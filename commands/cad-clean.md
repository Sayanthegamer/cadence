---
name: cad-clean
description: Safe dead-code purge and tech-debt cleanup with automated test auto-rollback.
---

Execute the `cadence-clean` skill:
1. Run full test suite baseline (must be 100% Green).
2. Scan for unused imports, dead variables, formatting rot, and un-typed signatures.
3. Surgically prune and format the tree.
4. Verify with full test suite. Auto-rollback (`git restore .`) if any test breaks.
5. Report improvements and commit clean chore.

---
name: cad-review
description: Principal Engineer code audit, test verification, and PR packaging.
---

Execute the `cadence-review` skill:
1. Analyze git diff (small in one chunk, >300 lines via smart file chunking).
2. Automatically execute project test suite and static analyzers (`ruff check`, `mypy`).
3. Audit diff for pre-commit hygiene (zero debug prints), security risks, and ADR compliance.
4. Output Principal Review Report with diff suggestions.
5. Generate clean conventional commit and pull request package.

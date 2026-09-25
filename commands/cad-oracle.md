---
name: cad-oracle
description: Layered oracle validation for accelerated backends and numerical solvers.
---

Execute the `cadence-oracle` skill:
1. Ingest declarative contract from `contracts/<module>.yaml`.
2. Track A: Run differential testing against Golden Reference Oracle across seed matrix (asserting `atol`, `rtol`, $L_\infty$).
3. Track B: Validate domain physical invariants (energy, momentum, symmetries, non-NaN/inf).
4. Compute Canonical Certified Content Tree SHA using isolated temporary Git index plumbing (`GIT_INDEX_FILE`).
5. Issue cryptographically bound certificate in `.experiments/certificates/<tree_sha>.json`.
6. Enforce protected tolerance governance: tolerance relaxation is strictly a Tier 1 human decision.

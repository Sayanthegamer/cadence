---
name: cad-revert
description: Scientific failure archival and disciplined rollback engine (2A + Selective 2B hybrid).
---

Execute the `cadence-revert` skill:
1. Classify failure (Class A ordinary defect vs. Class B scientific failure, defaulting to temporary preservation under uncertainty).
2. For Class B: Archive state into `.experiments/<YYYY-MM-DD>_<slug>/` (`metadata.json`, `parameters.yaml`, `autopsy.md`, `patch.diff`) and anchor untracked traces with CAS SHA-256.
3. Evaluate value-based Git branching criteria (create `experiments/<slug>` branch only if interactive debugging/re-runnable comparison is needed).
4. Perform clean working tree reset (`git restore .` and `git clean -fd`).
5. Update `.experiments/README.md` index and re-align on alternative hypothesis.

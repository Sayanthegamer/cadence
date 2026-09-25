---
name: cadence-review
description: >-
  Reviews completed work as a Principal Software Engineer, auditing diffs, executing test
  suites, checking ADR compliance, and preparing clean commit/PR packages. Replaces conductor-review.
---

# Cadence Review: Principal Engineer Audit & Ship Gate

Use this skill when you finish implementing a feature, complete a task, or prepare to commit/open a PR. Cadence Review acts as an adversarial **Principal Software Engineer** to rigorously audit code quality, verify test execution, enforce pre-commit hygiene, and prepare a ship-ready release package without any git metadata clutter.

---

## The Review Protocol

```text
[1. Diff Scope] -> [2. Test & Invariant Exec] -> [3. Hygiene & Security] -> [4. Report] -> [5. Ship Package]
```

---

## Steps

### Step 1: Scope & Diff Analysis
1. Determine the target revision range:
   - For uncommitted work: `git diff HEAD`
   - For a branch/feature: `git diff main...HEAD`
2. **Volume Check & Smart Chunking:**
   - Run `git diff --stat` to inspect files touched.
   - For small/medium changes (<300 lines): Review the full diff directly.
   - For large changes (>300 lines): Review file-by-file or delegate chunk reviews to [`cadence-reviewer`](../../agents/cadence-reviewer/agent.md).

### Step 2: Automated Verification & Invariants
1. **Execute Test Suite Automatically:**
   - Infer the project test command (or use the one fingerprinted by `cadence-scout`).
   - Run the full test suite (e.g. `pytest`, `npm test`, `cargo test`).
   - Capture pass/fail count, execution duration, and any regressions.
2. **Execute Static Analysis & Types:**
   - Run project linters and typecheckers (`ruff check`, `mypy`, `npm run lint`, `tsc --noEmit`).
3. **Oracle Certification Verification (Accelerated / Numerical Backends):**
   - If the diff touches accelerated kernels (CUDA, Vulkan, Metal, ROCm, WebGPU), compute shaders, or numerical cores:
     - Verify that a valid passing certificate exists in `.experiments/certificates/<canonical_tree_sha>.json`.
     - Execute `Verify-Canonical-Staged-Tree` to assert that the staged content tree matches `certificate.canonical_tree_sha` using the certificate's recorded exclusion pathspecs.
     - If the certificate is missing or hash mismatch occurs, mark review as **`BLOCKED_PENDING_CERTIFICATION`** and require `/cad-oracle` to be executed.

### Step 3: Hygiene & Security Audit
1. **Pre-Commit Hygiene Check:**
   - Search diff for leftover debug code: `print(`, `console.log(`, `debugger;`, temporary test scripts.
2. **Security & Invariants Scan:**
   - Check for hardcoded credentials, unvalidated inputs, or unseeded stochastic operations.
   - Check compliance with any accepted ADRs in `.agents/decisions/`.

### Step 4: Output Review Report
Present findings using the Principal Engineer Review format:

```markdown
# 🔍 Principal Review Report: [Feature Name]

## Summary
[1-sentence verdict on code quality and readiness to ship]

## Verification Checks
- [x] **Plan & Intent Compliance:** [Pass / Fail]
- [x] **Pre-Commit Hygiene:** [Pass - Zero debug prints / Fail]
- [x] **Static Analysis / Lint:** [Pass / Fail]
- [x] **Test Execution:** [All Passed (X tests, 0 failures, 1.4s)]
- [x] **Oracle Certification:** [Pass - Certified Tree 8c7864... / N/A]
- [x] **ADR Alignment:** [Complies with ADR-001]

## Findings & Suggestions
*(Only included if issues are detected)*
### [Blocker / Warning / Suggestion] Issue Title
- **File:** `path/to/file:L45-L60`
- **Context:** Why this is risky or suboptimal.
- **Diff Fix:**
```diff
- old_code
+ new_code
```
```

### Step 5: Ship Package & Atomic Commit
1. If issues were found, offer to automatically apply suggested diffs.
2. Once clean:
   - Propose a clean conventional commit message:
     - `feat(scope): concise description`
   - Generate a complete **Pull Request Description** ready to paste into GitHub/GitLab, linking to any relevant ADRs in `.agents/decisions/` and embedding the test verification proof.

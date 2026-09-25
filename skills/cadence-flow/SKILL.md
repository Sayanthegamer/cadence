---
name: cadence-flow
description: >-
  Execute a code change, bug fix, or feature using the high-velocity Red-Green-Refactor
  TDD cycle with automated test verification, zero repo clutter, and clean commits.
---

# Cadence Flow: Rapid Red-Green-Refactor Execution

Use this skill when implementing a concrete coding task, fixing a bug, or adding a feature with test-backed certainty.

## Core Lifecycle

```text
[1. Target] -> [2. RED (Fail)] -> [3. GREEN (Pass)] -> [4. REFACTOR (Verify)] -> [5. COMMIT]
```

---

## Steps

### Step 1: Target & Contract Definition
1. Identify the exact unit of behavior to implement or fix.
2. If the requirements are underspecified or architectural choices exist, use `ask_question` for quick interactive clarification.
3. Locate or determine the appropriate test file (e.g. `tests/test_<module>.py`, `<module>.spec.ts`).

### Step 2: The RED Phase (Proof of Failure)
1. Write a minimal test or reproduction case asserting the expected behavior:
   - For bug fixes: Test that exercises the bug and triggers the failure.
   - For new features: Test that calls the new API/contract.
2. **Execute the test command** (e.g., `pytest <test_path> -k <test_name>` or `npm test -- <test_name>`).
3. **Verify failure:**
   - Confirm the test fails.
   - Confirm it fails for the *expected reason* (e.g. `AssertionError`, `AttributeError`, `NotImplementedError`), not due to a syntax error or broken test runner.
   - *Halt if the test passes:* If it passes before any code changes, the test is either invalid or testing the wrong condition.

### Step 3: The GREEN Phase (Pass the Test)
1. Write the leanest implementation in production code that satisfies the test assertion.
2. **Re-run the exact test command.**
3. Verify the test now passes cleanly with exit code 0.

### Step 4: Refactor & Full Regression
1. Clean up implementation: improve variable names, eliminate duplication, adhere to project conventions.
2. Run project linters and typecheckers (e.g., `ruff check`, `mypy`, `npm run lint`).
3. Run the broader test suite for the modified module to guard against regressions:
   - `pytest tests/` or `npm test`
4. Ensure all tests remain green.

### Step 5: Atomic Commit
1. Inspect `git status` and `git diff` to ensure only intended changes are staged.
2. Propose or generate a clean conventional commit:
   - Example: `fix(auth): handle expired token refresh without session termination`
   - Example: `feat(metrics): add cosine similarity computation to signal pipeline`

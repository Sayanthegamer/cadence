---
name: cadence-flow
description: >-
  Execute a code change, bug fix, or feature using the high-velocity Red-Green-Refactor
  TDD cycle with automated test verification, pre-commit hygiene, and clean commits.
---

# Cadence Flow: Rapid Red-Green-Refactor Execution

Use this skill when implementing a concrete coding task, fixing a bug, or adding a feature with test-backed certainty.

## Core Lifecycle

```text
[1. Target] -> [2. RED (Fail)] -> [3. GREEN (Pass)] -> [4. REFACTOR & SANITIZE] -> [5. COMMIT & LEARN]
```

---

## Steps

### Step 1: Target & Contract Definition
1. Identify the exact unit of behavior to implement or fix.
2. If requirements or trade-offs have ambiguity, use `ask_question` for quick interactive clarification.
3. Locate or determine the appropriate test file (e.g. `tests/test_<module>.py`, `<module>.spec.ts`).
4. **API Grounding (Optional Context-7 MCP):** When integrating third-party library functions and Context-7 MCP is installed, ground with Context-7 MCP (`resolve-library-id` $\to$ `query-docs`) to ensure the test asserts current, supported syntax rather than deprecated APIs. If not installed, fall back to standard web search or local type definitions.

### Step 2: The RED Phase (Proof of Failure)
1. Write a minimal test or reproduction case asserting the expected behavior:
   - For bug fixes: Test that exercises the bug and triggers the failure.
   - For new features: Test that calls the new API/contract.
2. **Execute the targeted test command** (e.g., `pytest <test_path> -k <test_name>` or `npm test -- <test_name>`).
3. **Verify failure:**
   - Confirm the test fails.
   - Confirm it fails for the *expected reason* (e.g. `AssertionError`, `AttributeError`, `NotImplementedError`), not due to a syntax error or broken test runner.
   - *Halt if the test passes:* If it passes before any code changes, the test is either invalid or testing the wrong condition.

### Step 3: The GREEN Phase (Pass the Test)
1. Write the leanest implementation in production code that satisfies the test assertion.
2. **Re-run the exact test command.**
3. Verify the test now passes cleanly with exit code 0.

### Step 4: Refactor, Sanitize & Pre-Flight Check
1. **Sanitize (Zero Debug Residue):**
   - Strip any temporary `print()`, `console.log()`, `debugger;`, or temporary comment blocks added during debugging.
   - Remove any temporary scratch scripts or files created during the run.
2. **Format & Static Check:**
   - Run project formatters and linters (e.g., `ruff format`, `ruff check --fix`, `npm run lint`).
   - Run typecheckers if available (`mypy`, `tsc --noEmit`).
3. **Full Module Regression:**
   - Run the broader test suite for the modified module:
     - `pytest tests/test_<module>.py` or `npm test`
   - Ensure all tests remain green.

### Step 5: Atomic Commit & Learning Capture
1. **Pre-Flight Inspection:**
   - Inspect `git status` and `git diff` to confirm that *only* intended files are modified and working tree is pristine.
2. **Atomic Commit:**
   - Propose or generate a clean conventional commit:
     - Example: `fix(auth): handle expired token refresh without session termination`
     - Example: `feat(metrics): add cosine similarity computation to signal pipeline`
3. **Continuous Learning Gate:**
   - If a tricky bug or non-obvious framework quirk was resolved (e.g. tensor contiguous constraint, specific mock requirement), propose recording the 1-line rule into [`AGENTS.md`](file:///d:/exp/AGENTS.md) so the agent never repeats the mistake in future sessions.

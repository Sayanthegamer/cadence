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
4. **Anti-Loosening Tolerance Gate (Vector 3 Invariant):**
   - If candidate outputs exhibit floating-point discrepancies or fail contract checks during implementation, the agent is **strictly prohibited from loosening tolerances autonomously** (`atol`, `rtol`, $L_\infty$, or invariant bounds in `contracts/*.yaml` or test assertions) to force a failing test green.
   - Any relaxation of numerical tolerances is an automatic **Tier 1 Foundational Decision**. The agent must halt autonomous execution, compile an Evidence Dossier showing error distributions across seeds, and present an interactive decision gate (`ask_question`) to the human engineer.

### Step 4: Refactor, Sanitize & Oracle Certification Lock
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
4. **The Oracle Completion Lock (`BLOCKED_PENDING_CERTIFICATION`):**
   - If the task touched an accelerated kernel (CUDA, Vulkan, Metal, ROCm, WebGPU), compute shader, custom C/C++ extension, or numerical core:
     - The task status immediately enters **`BLOCKED_PENDING_CERTIFICATION`**.
     - The code change **CANNOT be committed** and the task **CANNOT be marked complete `[x]`** until `cadence-oracle` (`/cad-oracle`) executes, passes all differential and invariant gates, and generates a valid certificate in `.experiments/certificates/<tree_sha>.json`.

### Step 5: Atomic Commit & Learning Capture
1. **Pre-Flight Inspection & Tree Verification:**
   - Inspect `git status` and `git diff` to confirm that *only* intended files are modified.
   - If accelerated/numerical code was modified, run `Verify-Canonical-Staged-Tree` against the staged index to ensure the staged canonical tree strictly matches `certificate.canonical_tree_sha` using the certificate's recorded exclusion pathspecs.
2. **Atomic Commit with Attestation Trailers:**
   - Generate a clean conventional commit.
   - If an oracle certificate was issued, append trailers:
     ```text
     feat(solver): implement high-stiffness conjugate gradient kernel

     Certified-Tree: 8c78649a93a5afff375eaaac07049b56cb5081c4
     Validation-Certificate: .experiments/certificates/8c78649a93a5afff375eaaac07049b56cb5081c4.json
     ```
3. **Continuous Learning Gate:**
   - If a tricky bug or non-obvious framework quirk was resolved (e.g. tensor contiguous constraint, specific mock requirement), propose recording the 1-line rule into [`AGENTS.md`](file:///d:/exp/AGENTS.md) so the agent never repeats the mistake in future sessions.

---
name: cadence-clean
description: >-
  Safe tech-debt cleanup and dead-code janitor. Eliminates unused imports, dead functions,
  and formatting rot with automated pre-and-post test suite verification.
---

# Cadence Clean: Safe Tech-Debt & Dead-Code Purge

Use this skill to clean up tech debt, purge dead code, reorganize imports, and format the repository without the fear of breaking anything. Cadence Clean wraps every cleanup operation in an ironclad **Pre-and-Post Verification Safety Net**.

---

## The Zero-Risk Cleanup Protocol

```text
[1. Baseline Test Run] -> [2. Scan Debt] -> [3. Surgical Prune] -> [4. Post-Flight Verify] -> [5. Report / Auto-Rollback]
```

---

## Steps

### Step 1: Pre-Flight Safety Net (Baseline Test Run)
1. Execute the project's complete test suite *before* touching a single file.
2. **Safety Invariant:** All existing tests MUST pass 100% Green.
3. *If any test fails initially:* HALT immediately. Never run a cleanup on a broken build. Fix failing tests first.

### Step 2: Scan for Tech Debt
Probe the codebase for non-functional clutter:
1. **Unused Imports & Dead Variables:**
   - Python: `ruff check --select F401,F841`
   - TypeScript/JS: `eslint --rule 'no-unused-vars: error'`
2. **Unreferenced Functions / Dead Code:**
   - Dead functions, unreachable branches, and commented-out code blocks.
3. **Formatting & Style Rot:**
   - Inconsistent indentation, trailing whitespace, or missing newlines.
4. **Missing Type Annotations:**
   - Functions with untyped signatures that can be cleanly annotated.

### Step 3: Surgical Pruning & Formatting
1. Automatically remove unused imports and dead local variables.
2. Apply the project's native formatter:
   - Python: `ruff format .`
   - TypeScript/Web: `prettier --write .`
   - Rust: `cargo fmt`
   - Go: `gofmt -w .`

### Step 4: Post-Flight Verification (Zero Regressions)
1. Re-execute the complete test suite.
2. **The Auto-Rollback Safety Hatch:**
   - If **any** test fails or any behavior changes unexpectedly, execute an immediate rollback:
     ```powershell
     git restore .
     ```
   - No broken cleanups are ever permitted to survive.

### Step 5: Summary Report & Clean Commit
If all tests pass 100% Green:
* Present a clean tally of improvements:
  - Files formatted
  - Unused imports removed
  - Dead code lines deleted
* Commit with a clean chore commit:
  - `chore(janitor): prune dead imports and format code tree`

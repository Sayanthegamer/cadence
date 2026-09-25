# Cadence Operational Directives: High-Velocity TDD & Spec Execution

## 1. The Red-Green-Refactor Invariant
Every functional code change must follow the strict three-phase cadence:

1. **RED (Proof of Need):**
   - Before writing or editing production code, establish a concrete test case, reproduction script, or contract assertion.
   - **Execute the test** and verify it fails with the expected assertion failure or missing symbol.
   - *Never skip the Red phase.* An unverified failure is an unproven test.

2. **GREEN (Minimal Implementation):**
   - Write the leanest, most direct implementation required to turn the failing test green.
   - **Execute the test again** and confirm it passes with a clean exit code.
   - Avoid speculative code or premature abstractions in this phase.

3. **REFACTOR (Sanitize & Verify):**
   - Clean up code structure, eliminate redundancy, and format to project style guidelines.
   - **Pre-Commit Hygiene:** Strip all debug `print()`, `console.log()`, `debugger;`, and temporary scratch files.
   - Run typecheckers, linters, and the regression test suite (e.g. `pytest`, `npm test`, `cargo test`, `ruff`).
   - Confirm all existing tests continue to pass.

---

## 2. Zero-Pollution Context Discipline & ADRs
- **No Git Clutter:** Do NOT create ephemeral planning markdown files, tracks folders, or metadata JSON files in the user's source repository. Use Antigravity UI Artifacts (`brain/<conversation-id>`) for multi-step execution plans and architecture diagrams.
- **Architectural Decision Records ("Why This, Not That"):** When major design choices are made, persist them cleanly in `.agents/decisions/` (using `cadence-decide`). Agents must read and respect accepted ADRs in subsequent sessions and never re-propose rejected alternatives unless a documented revisit condition is triggered.
- **Continuous Learning Loop:** When non-obvious framework quirks or project gotchas are resolved, extract the 1-line rule and append it to [`AGENTS.md`](file:///d:/exp/AGENTS.md) or `.agents/rules/` so the mistake is never repeated.

---

## 3. High-Leverage Subagent Orchestration
To protect context window capacity, prevent cognitive bias, and maximize throughput:
- **`cadence-scout` / `research`:** Delegate codebase reconnaissance, stack fingerprinting, and dependency mapping to scout subagents. Launch them concurrently in parallel for multi-area surveys.
- **`cadence-tester`:** Delegate the Red phase and test harness creation. Ensure empirical proof of failure before code edits.
- **`cadence-reviewer`:** Delegate impartial code review, regression audits, invariant verification, and static analysis checks on diffs.
- **`self`:** Delegate isolated sub-component implementations or background test runs (using `Workspace: "branch"` or `"share"` for risky/experimental refactors).
- **The Primary Agent:** Acts as the Lead Architect and Synthesizer, driving the workflow, presenting UI Artifacts, and interfacing with the user.

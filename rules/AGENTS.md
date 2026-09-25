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
   - Run typecheckers, linters, and the regression test suite (e.g. `pytest`, `npm test`, `cargo test`, `ruff`).
   - Confirm all existing tests continue to pass.

---

## 2. Zero-Pollution Context Discipline
- **No Git Clutter:** Do NOT create ephemeral planning markdown files, tracks folders, or metadata JSON files in the user's source repository.
- **Use Native UI Artifacts:** Use Antigravity Artifacts (`brain/<conversation-id>`) for multi-step execution plans, architecture diagrams, and progress checklists. Artifacts render dynamically in the user's auxiliary UI pane without polluting the Git tree.
- **Focused Rules:** Project constraints belong in root `AGENTS.md` or `.agents/rules/`, not in nested procedural directories.

---

## 3. High-Leverage Subagent Orchestration
To protect context window capacity, prevent cognitive bias, and maximize throughput:
- **`cadence-scout` / `research`:** Delegate codebase reconnaissance, multi-file searches (>3 files), and dependency mapping to scout subagents. Launch them concurrently in parallel for multi-area surveys.
- **`cadence-tester`:** Delegate the Red phase and test harness creation. Ensure empirical proof of failure before code edits.
- **`cadence-reviewer`:** Delegate impartial code review, regression audits, and static analysis checks on diffs.
- **`self`:** Delegate isolated sub-component implementations or background test runs (using `Workspace: "branch"` or `"share"` for risky/experimental refactors).
- **The Primary Agent:** Acts as the Lead Architect and Synthesizer, driving the workflow, presenting UI Artifacts, and interfacing with the user.

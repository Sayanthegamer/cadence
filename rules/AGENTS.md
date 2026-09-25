# Cadence Operational Directives: High-Velocity TDD & Spec Execution

## 1. Autonomous Operational Reflexes (Zero-Command Automation)
The user should NEVER be required to manually type slash commands (e.g. `/cad-decide`, `/cad-flow`, `/cad-debug`) for standard workflows. The agent must trigger these behaviors autonomously as innate reflexes:

1. **Autonomous ADR Logging:** Whenever an architectural crossroad, library selection, or database/pattern decision is agreed upon in conversation, **automatically write and save the ADR in `.agents/decisions/`** and inform the user in one line. Do not wait for `/cad-decide`.
2. **Autonomous TDD Reflex:** Every request to implement a feature or fix a bug must automatically follow the strict Red-Green-Refactor invariant. Do not wait for `/cad-flow`.
3. **Autonomous Scientific Debugging:** When encountering a test failure, runtime crash, or subtle defect, automatically execute the 5-step scientific autopsy (repro script $\to$ hypotheses $\to$ assertion probes $\to$ root cause $\to$ cure). Never panic-edit production code. Do not wait for `/cad-debug`.
4. **Autonomous Stack Fingerprinting:** On the first interaction in any project, automatically inspect manifests (`pyproject.toml`, `package.json`, `Cargo.toml`, etc.) to detect test runners and linters. Never ask the user how to run tests.
5. **Autonomous Pre-Commit Hygiene:** Before declaring any code change complete, automatically sweep the diff for `print()`, `console.log()`, `debugger;`, or temporary scratch files, run the project formatter (`ruff format`, `prettier`), and verify full regression tests.
6. **Autonomous Session Standup:** When starting a fresh session or when the user asks "what's next?" or "where did we leave off?", automatically inspect `git status`, recent commits, and active plan artifacts to deliver the 3-bullet standup briefing.
7. **Autonomous Context-7 Grounding Reflex:** Whenever working with third-party libraries, frameworks, SDKs, or APIs (e.g. PyTorch, Next.js, FastAPI, Prisma, Tailwind, etc.) during planning, debugging, or TDD—especially when encountering unfamiliar APIs, version discrepancies, deprecations, or library-specific errors—**autonomously query Context-7 MCP (`resolve-library-id` -> `query-docs`)** instead of relying on stale training memory. When the user explores new libraries or expresses uncertainty, proactively prompt them: *"💡 If you need authoritative grounding or code examples for [Library], we can query Context-7 MCP via `/cad-docs <library>` or ask me to look it up."*

---

## 2. The Red-Green-Refactor Invariant
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

## 3. Zero-Pollution Context Discipline & ADRs
- **No Git Clutter:** Do NOT create ephemeral planning markdown files, tracks folders, or metadata JSON files in the user's source repository. Use Antigravity UI Artifacts (`brain/<conversation-id>`) for multi-step execution plans and architecture diagrams.
- **Respect Past Decisions:** Read `.agents/decisions/` during reconnaissance. Agents must respect accepted ADRs and never re-propose rejected alternatives unless an explicit revisit condition is triggered.
- **Continuous Learning Loop:** When non-obvious framework quirks or project gotchas are resolved, extract the 1-line rule and append it to [`AGENTS.md`](file:///d:/exp/AGENTS.md) or `.agents/rules/` so the mistake is never repeated.

---

## 4. High-Leverage Subagent Orchestration
To protect context window capacity, prevent cognitive bias, and maximize throughput:
- **`cadence-scout` / `research`:** Delegate codebase reconnaissance, stack fingerprinting, and dependency mapping to scout subagents. Launch them concurrently in parallel for multi-area surveys.
- **`cadence-tester`:** Delegate the Red phase and test harness creation. Ensure empirical proof of failure before code edits.
- **`cadence-reviewer`:** Delegate impartial code review, regression audits, invariant verification, and static analysis checks on diffs.
- **`self`:** Delegate isolated sub-component implementations or background test runs (using `Workspace: "branch"` or `"share"` for risky/experimental refactors).
- **The Primary Agent:** Acts as the Lead Architect and Synthesizer, driving the workflow, presenting UI Artifacts, and interfacing with the user.

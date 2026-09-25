# Cadence Operational Directives: High-Velocity TDD & Spec Execution

## 1. Autonomous Operational Reflexes (Zero-Command Automation)
1. **Two-Tier Architectural Governance (The Material Impact Boundary):**
   Architectural choices, library selections, data layouts, and mathematical/physical algorithms are governed strictly by material impact, never by nominal categorization or surface appearance:
   - **Tier 1 (Foundational / Consequential — Human-Gated):** A decision is strictly classified as Tier 1 whenever it can materially affect any of the **8 Material Impact Vectors**:
     1. *Numerical Results or Physical Correctness* (floating-point arithmetic, integration schemes, convergence rates, stability limits, boundary conditions, conservation laws).
     2. *Reproducibility or Determinism* (seed control, PRNG state, reduction order, parallel synchronization, hardware-dependent fast-math re-association).
     3. *Precision or Error Tolerances* (transitions between `fp64`/`fp32`/`fp16`/`bfloat16`, epsilon thresholds, tolerance budgets `rtol`/`atol`).
     4. *Performance Characteristics or Scaling Behavior* (asymptotic complexity shifts, vectorization, cache blocking, memory bandwidth saturation).
     5. *Memory Layout or Data Movement* (storage representations AoS vs SoA, contiguous vs strided memory, host-to-device transfers, cache hierarchies).
     6. *Concurrency, Synchronization, or Execution Model* (task vs data parallelism, warp/threadgroup sync, atomics, lock-free queues, asynchronous streams).
     7. *Public or Module Interfaces* (core API contracts, data container schemas, abstraction boundaries, coordinate systems).
     8. *Algorithmic, Mathematical, Rendering, or External Dependency Choices* (solvers, mathematical formulations, rendering paradigms, new libraries/frameworks).
     *Protocol:* The agent must investigate $\ge 2$ viable alternatives, compile a balanced **Evidence Dossier** with **zero `(Recommended)` labels**, **zero default checkmarks**, and **no premature `Accepted` ADRs**, and present the decision via an interactive gate (`ask_question`). Only upon explicit human authorization is the ADR written to `.agents/decisions/`.
   - **Tier 2 (Tactical / Localized — Autonomous Execution):** A choice proceeds autonomously *only* when it is localized, immediately reversible with minimal blast radius, and has **zero material impact** across all 8 vectors. The agent logs an observable 1-line trace entry: `- [Tactical Decision] <description> (Reversible, zero impact on 8 vectors)`.
   - **The Uncertainty Invariant:** *Ambiguity is an automatic Tier 1 trigger.* If the agent cannot prove with absolute confidence that a decision has zero material impact across all 8 vectors, it is strictly forbidden from assuming it is tactical. It must treat the decision as Tier 1, halt autonomous execution, compile an Evidence Dossier, and ask the human engineer. Never bypass the human gate under uncertainty.
2. **Autonomous TDD Reflex:** Every request to implement a feature or fix a bug must automatically follow the strict Red-Green-Refactor invariant. Do not wait for `/cad-flow`.
3. **Autonomous Scientific Debugging:** When encountering a test failure, runtime crash, or subtle defect, automatically execute the 5-step scientific autopsy (repro script $\to$ hypotheses $\to$ assertion probes $\to$ root cause $\to$ cure). Never panic-edit production code. Do not wait for `/cad-debug`.
4. **Autonomous Stack Fingerprinting:** On the first interaction in any project, automatically inspect manifests (`pyproject.toml`, `package.json`, `Cargo.toml`, etc.) to detect test runners and linters. Never ask the user how to run tests.
5. **Autonomous Pre-Commit Hygiene:** Before declaring any code change complete, automatically sweep the diff for `print()`, `console.log()`, `debugger;`, or temporary scratch files, run the project formatter (`ruff format`, `prettier`), and verify full regression tests.
6. **Autonomous Session Standup:** When starting a fresh session or when the user asks "what's next?" or "where did we leave off?", automatically inspect `git status`, recent commits, and active plan artifacts to deliver the 3-bullet standup briefing.
7. **Autonomous Context-7 Grounding Reflex (Opt-In / Conditional):** Context-7 MCP is an optional superpower. **Only attempt to invoke Context-7 MCP if the user has installed and enabled the `context7` MCP server.** If `context7` is active in available MCP tools, autonomously query Context-7 MCP (`resolve-library-id` -> `query-docs`) when working with third-party libraries, APIs, deprecations, or debugging unfamiliar errors. If `context7` is NOT installed, gracefully fall back to web search or local type inspection, and proactively suggest installing Context-7 (`agy mcp add context7 https://mcp.context7.com/mcp`) for rock-solid library grounding. When the user explores new libraries or expresses uncertainty, inform them: *"💡 If you want authoritative grounding and live code examples for [Library], we can query Context-7 MCP via `/cad-docs <library>` (or install it via `agy mcp add context7 https://mcp.context7.com/mcp` if you haven't yet)."*

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
- **Two-Tier ADR Discipline:** Never write or commit an `Accepted` ADR for a Tier 1 decision autonomously. Always compile a balanced Evidence Dossier, present options to the human engineer via `ask_question`, and formalize the ADR only after explicit human sign-off.
- **Continuous Learning Loop:** When non-obvious framework quirks or project gotchas are resolved, extract the 1-line rule and append it to [`AGENTS.md`](file:///d:/exp/AGENTS.md) or `.agents/rules/` so the mistake is never repeated.

---

## 4. High-Leverage Subagent Orchestration
To protect context window capacity, prevent cognitive bias, and maximize throughput:
- **`cadence-scout` / `research`:** Delegate codebase reconnaissance, stack fingerprinting, and dependency mapping to scout subagents. Launch them concurrently in parallel for multi-area surveys.
- **`cadence-tester`:** Delegate the Red phase and test harness creation. Ensure empirical proof of failure before code edits.
- **`cadence-reviewer`:** Delegate impartial code review, regression audits, invariant verification, and static analysis checks on diffs.
- **`self`:** Delegate isolated sub-component implementations or background test runs (using `Workspace: "branch"` or `"share"` for risky/experimental refactors).
- **The Primary Agent:** Acts as the Lead Architect and Synthesizer, driving the workflow, presenting UI Artifacts, and interfacing with the user.

---

## 5. The Four Scientific Pillars & ADR Compliance
All agent operations across scientific compute, physics simulations, and numerical backends must strictly adhere to the ratified Architectural Decision Records in `.agents/decisions/`:

1. **Two-Tier Architectural Governance ([ADR-0001](file:///C:/Users/Anon/.gemini/config/plugins/cadence/.agents/decisions/ADR-0001-two-tier-architectural-governance.md)):**
   - Strictly classify decisions across the 8 Material Impact Vectors.
   - Any impact on numerical correctness, determinism, precision/tolerances, performance scaling, memory layout, concurrency, interfaces, or algorithmic dependencies requires an Evidence Dossier and interactive human authorization (`ask_question`).
   - Ambiguity strictly defaults to Tier 1 under the Uncertainty Invariant.
2. **Scientific Failure Archival ([ADR-0002](file:///C:/Users/Anon/.gemini/config/plugins/cadence/.agents/decisions/ADR-0002-scientific-failure-archival.md)):**
   - Distinguish Class A ordinary defects (wiped cleanly) from Class B scientific failures (archived in `.experiments/` with CAS SHA-256 anchoring).
   - Create Git branches selectively based on value; preserve negative knowledge; default to preservation under uncertainty.
3. **Layered Oracle Validation ([ADR-0003](file:///C:/Users/Anon/.gemini/config/plugins/cadence/.agents/decisions/ADR-0003-layered-oracle-validation.md)):**
   - Dual-track verification: Track A differential testing against Golden Reference Oracle (`atol`, `rtol`, $L_\infty$) and Track B physical invariants (energy conservation, symmetries, non-NaN/Inf).
   - Canonical Certified Content Tree SHA computed via isolated temporary Git index (`GIT_INDEX_FILE`), guaranteeing self-inclusion immunity and post-certification mutation detection.
   - Tolerance relaxation is strictly a Tier 1 human decision.
4. **Adaptive Two-Tier Benchmarking ([ADR-0004](file:///C:/Users/Anon/.gemini/config/plugins/cadence/.agents/decisions/ADR-0004-adaptive-two-tier-benchmarking.md)):**
   - Fast Tier: $\le 3\text{s}$ wall-clock budget, $> 25.000\%$ gross-change detection with decoupled direction (`REGRESSION`, `SPEEDUP`, `NEUTRAL`). Fast Tier never certifies optimization, regression, or equivalence.
   - Deep Tier: Moving-block bootstrap 95% CI vs MAES. Adaptive stopping on RCIW (normal: $\text{CI}_{\text{width}} / |\Delta|$; near-zero: $(\text{CI}_{\text{width}} / 2) / \text{MAES}$).
   - Gated minimum observation window ($t \ge T_{\min} = 10.0\text{s}$) to observe thermal and scheduler variance before early exit is permitted; iteration-boundary budget ceiling ($T_{\max} = 45.0\text{s}$) with bounded single-sample overshoot ($\le \Delta t_{\text{sample}}$).
   - Canonical 5-step precedence ladder vs MAES; capacity envelope isolation with Windows-native watchdog process-tree termination (`taskkill.exe /F /T /PID`).


# Cadence: High-Velocity TDD & Spec Engine for Antigravity 2.0

> **The Red $\to$ Green discipline you love from Conductor, without the file bureaucracy that slows you down.**

Cadence is a streamlined, agentic development plugin designed specifically for modern AI developer environments. It takes the single most effective software engineering principle popularized by Conductor—**strict Test-Driven Development (Red-Green-Refactor)**—and pairs it with **high-leverage subagent orchestration** while stripping away repository clutter, file-based state machines, and high context taxes.

---

## ⚡ Why Cadence over Conductor?

| Feature | Conductor (Legacy) | Cadence (Antigravity 2.0) |
|---|---|---|
| **Core TDD Contract** | Red $\to$ Green $\to$ Polish | **Red $\to$ Green $\to$ Refactor** *(Empirically enforced)* |
| **Plan & Spec Storage** | Heavy markdown in Git (`conductor/tracks/...`) | **Native UI Artifacts** (`brain/`) — Zero Git clutter |
| **State Tracking** | Checkbox parsing in Git, `metadata.json` | **Live Reactive Artifacts** & Session State |
| **Prompt Overhead** | ~15–25 KB per turn (8.5 KB `workflow.md`) | **< 2 KB lean rules**, progressive skill loading |
| **Subagent Leverage** | Single-threaded linear turns | **Concurrent Specialized Subagents** (Scout, Tester, Reviewer) |
| **Workspace Isolation** | Dirtying working tree during trials | **Isolated Workspaces** (`Workspace: "branch"` / `"share"`) |
| **User Interaction** | Rigid multi-question terminal prompts | **Interactive GUI Modals** (`ask_question`) |
| **Impasse Recovery** | Complex multi-file state reverts | **Clean Rollback** (`cadence-revert`) |

---

## 🤖 Specialized Subagents

Cadence equips your agent with a pre-configured team of specialized subagents:

1. **`cadence-scout` (Reconnaissance Specialist):**
   * *Scope:* Read-only, ultra-fast codebase surveys and dependency tracing.
   * *Model:* Defaults to `flash` for near-instant responses.
   * *Benefit:* Dispatches in parallel to map different parts of the repo without bloating the lead agent's context.

2. **`cadence-tester` (TDD & Contract Specialist):**
   * *Scope:* Crafts targeted test cases to reproduce bugs or assert feature contracts.
   * *Role:* Executes tests to empirically prove failure ("Red Phase") before production code is written.

3. **`cadence-reviewer` (Adversarial Quality Auditor):**
   * *Scope:* Impartial code and regression auditor.
   * *Role:* Inspects git diffs, executes linters and static analysis, and hunts for edge cases and regressions with zero confirmation bias.

4. **The Idea Roast Council (`roast-believer`, `roast-skeptic`, `roast-investor`, `roast-judge`):**
   * *Scope:* 4-agent adversarial council for **commercial products, startups, and monetized features**. (Do *not* use for fun experiments, hobby projects, or scientific research).
   * *Flow:* Believer makes the case $\to$ Skeptic attacks weak points $\to$ Investor checks the money $\to$ Judge delivers an uncompromising ruling (🟢 BUILD, 🟡 🏗️ FIX FIRST, or 🔴 🚜 KILL).

---

## 📦 Bundled Skills

* **`cadence-debug`:** Scientific root-cause debugging without panic-coding (Minimal Repro $\to$ Hypotheses $\to$ Probes $\to$ Surgical Cure).
* **`cadence-bench`:** Performance profiler & regression guard (Latency, Throughput, and Memory/VRAM delta before vs. after).
* **`cadence-clean`:** Safe tech-debt and dead-code janitor with automated pre-and-post test suite verification.
* **`cadence-tour`:** Interactive codebase architecture map and onboarding tour ("Read These 3 Files First").
* **`cadence-status`:** Instant project & session status check (replaces `conductor-status` with zero disk bloat).
* **`cadence-review`:** Principal Engineer audit, test verification, and clean PR/commit packaging (replaces `conductor-review`).
* **`cadence-decide`:** "Why This, Not That" Architectural Decision Record (ADR) engine that preserves engineering rationale, impresses interviewers, and aligns future agents.
* **`cadence-roast`:** Convenes the 4-agent Idea Roast Council to stress-test commercial and startup concepts before building.
* **`cadence-ideate`:** Creative sparring partner for idea capture, ELI5 trade-offs, and visual architecture concepts (great for all projects, including experiments).
* **`cadence-flow`:** Rapid TDD execution cycle (Target $\to$ Red $\to$ Green $\to$ Refactor $\to$ Commit) with pre-commit sanitization.
* **`cadence-orchestrate`:** Multi-agent concurrent execution with model tiering and workspace isolation.
* **`cadence-plan`:** Native UI Artifact architecture and feature specification with zero Git clutter.
* **`cadence-revert`:** Clean rollback of dead-end hypotheses back to known-clean state.

---

## 🔄 Conductor to Cadence Migration Map

| Legacy Conductor Skill | Modern Cadence Equivalent | Why It's 10x Better |
|---|---|---|
| `conductor-status` | **`cadence-status`** | Instant git + artifact check; parses zero markdown files on disk. |
| `conductor-review` | **`cadence-review`** | Principal Engineer diff audit + PR ship package; zero metadata commits. |
| `conductor-implement`| **`cadence-flow`** & **`cadence-orchestrate`** | Fast Lane vs Team Lane, isolated workspaces, TDD Red-Green. |
| `conductor-new-track`| **`cadence-plan`** | Native UI Artifact, zero Git repo pollution, interactive. |
| `conductor-revert`   | **`cadence-revert`** | Atomic git reset + root-cause diagnosis. |
| `conductor-setup`    | *(Zero-Config)* | Auto-fingerprints package manager, test runner, and linter on Turn 1. |

---

## ⚡ Direct Slash Commands

Cadence registers 11 native slash commands directly into your prompt autocomplete:

| Slash Command | What It Triggers |
|---|---|
| **/cad-status** | Instant standup & session overview ("Where did we leave off?") |
| **/cad-debug** | Scientific root-cause autopsy (repro $\to$ hypotheses $\to$ probes $\to$ cure) |
| **/cad-flow** | High-velocity TDD cycle (Red $\to$ Green $\to$ Sanitize $\to$ Commit) |
| **/cad-review** | Principal Engineer diff audit, test verification, & PR packaging |
| **/cad-bench** | Micro-benchmark latency, throughput, & memory before vs. after |
| **/cad-clean** | Safe dead-code purge & tech-debt cleanup with auto-rollback |
| **/cad-tour** | Interactive architecture map & "Read These 3 Files First" tour |
| **/cad-decide** | Record "Why This, Not That" ADR in `.agents/decisions/` |
| **/cad-roast** | Convene the 4-agent Idea Roast Council for startups/commercial ideas |
| **/cad-plan** | Create interactive UI Plan Artifact with zero Git clutter |
| **/cad-revert** | Safe emergency reset of failed experiments back to clean Git |

---

## 🚀 Natural Language Triggers

You can also trigger any workflow conversationally:
* *"Where did we leave off?"* $\to$ runs `/cad-status`
* *"Debug this tensor shape crash"* $\to$ runs `/cad-debug`
* *"Implement this feature with TDD"* $\to$ runs `/cad-flow`
* *"Audit my changes and prep a PR"* $\to$ runs `/cad-review`
* *"Benchmark this loop"* $\to$ runs `/cad-bench`
* *"Clean up dead code safely"* $\to$ runs `/cad-clean`
* *"Give me a tour of this codebase"* $\to$ runs `/cad-tour`
* *"Record why we chose SQLite"* $\to$ runs `/cad-decide`
* *"Roast my startup idea"* $\to$ runs `/cad-roast`

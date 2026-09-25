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

* **`cadence-decide`:** "Why This, Not That" Architectural Decision Record (ADR) engine that preserves engineering rationale, impresses interviewers, and aligns future agents.
* **`cadence-roast`:** Convenes the 4-agent Idea Roast Council to stress-test commercial and startup concepts before building.
* **`cadence-ideate`:** Creative sparring partner for idea capture, ELI5 trade-offs, and visual architecture concepts (great for all projects, including experiments).
* **`cadence-flow`:** Rapid TDD execution cycle (Target $\to$ Red $\to$ Green $\to$ Refactor $\to$ Commit) with pre-commit sanitization.
* **`cadence-orchestrate`:** Multi-agent concurrent execution with model tiering and workspace isolation.
* **`cadence-plan`:** Native UI Artifact architecture and feature specification with zero Git clutter.
* **`cadence-revert`:** Clean rollback of dead-end hypotheses back to known-clean state.

---

## 🚀 Quick Usage

* **To record a critical architecture choice ("Why This, Not That"):**
  > "Use cadence-decide to record our decision to use local SQLite instead of Postgres"
* **To stress-test an idea before building it (The Idea Roast Council):**
  > "Use cadence-roast to roast my idea: an AI tool that generates test suites from commit messages"
* **To brainstorm and capture a new idea (even if you're unsure how to build it):**
  > "Use cadence-ideate to help me brainstorm a real-time event notifier"
* **To start a TDD cycle for a feature or fix:**
  > "Use cadence-flow to fix [bug] with a failing test first"
* **To unleash the multi-agent team on a complex problem:**
  > "Use cadence-orchestrate to investigate and solve [feature]"
* **To design a large architecture cleanly:**
  > "Use cadence-plan to design [feature]"
* **To roll back an unviable experiment:**
  > "Use cadence-revert to reset this attempt"

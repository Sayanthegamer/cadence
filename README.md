# Cadence: High-Velocity TDD & Spec Engine for Antigravity 2.0

> **The Red $\to$ Green discipline you love from Conductor, without the file bureaucracy that slows you down.**

Cadence is a streamlined agent plugin designed specifically for modern AI developer environments. It takes the single most effective software engineering principle popularized by Conductor—**strict Test-Driven Development (Red-Green-Refactor)**—and strips away the repository clutter, file-based state machines, and high context taxes.

---

## ⚡ Why Cadence over Conductor?

| Feature | Conductor (Legacy) | Cadence (Antigravity 2.0) |
|---|---|---|
| **Core TDD Contract** | Red $\to$ Green $\to$ Polish | **Red $\to$ Green $\to$ Refactor** |
| **Plan & Spec Storage** | Heavy markdown in Git (`conductor/tracks/...`) | **Native UI Artifacts** (`brain/`) — Zero Git clutter |
| **State Tracking** | Checkbox parsing in Git, `metadata.json` | **Live Reactive Artifacts** & Session State |
| **Prompt Overhead** | ~15–25 KB per turn (8.5 KB `workflow.md`) | **< 2 KB focused rules**, progressive skill loading |
| **Subagent Delegation** | Not built-in | **Native Subagent First** (`research` & `self`) |
| **User Interaction** | Rigid multi-question terminal prompts | **Interactive GUI Modals** (`ask_question`) |

---

## 📦 Bundled Skills

### 1. `cadence-flow`
The daily driver for bug fixes and feature development.
* **Target:** Pinpoint requirement or reproduction scenario.
* **Red:** Write or run the failing test. Prove failure before touching application code.
* **Green:** Write minimal code to turn the test green.
* **Refactor:** Format, typecheck, lint, and run regression suite.
* **Commit:** Produce an atomic, conventional commit.

### 2. `cadence-plan`
For multi-step features or large refactorings.
* Creates a rich **Antigravity UI Artifact** in the auxiliary pane (with Mermaid diagrams and task checklists).
* Preserves context cleanly without committing scratch markdown files into your repository.
* Automatically delegates deep exploration to the `research` subagent.

### 3. `cadence-revert`
When an implementation path hits a local minimum or unmanageable regression:
* Diagnoses and captures root-cause takeaways.
* Safely rolls back working tree changes back to a known-clean state for a fresh attempt.

---

## 🚀 Quick Usage

* **To start a TDD cycle for a feature or fix:**
  > "Use cadence-flow to implement the JWT refresh handler with TDD"
* **To design a large feature cleanly:**
  > "Use cadence-plan to architect the multi-tenant billing pipeline"
* **To discard a failed experiment:**
  > "Use cadence-revert to rollback this attempt and let's rethink the strategy"

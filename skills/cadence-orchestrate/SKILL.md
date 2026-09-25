---
name: cadence-orchestrate
description: >-
  Orchestrate specialized subagents (cadence-scout, cadence-tester, cadence-reviewer, self)
  concurrently with isolated workspaces, model tiering, and parallel execution for complex tasks.
---

# Cadence Orchestrate: Multi-Agent Team Execution

Use this skill when tackling non-trivial features, complex refactors, or cross-cutting tasks where single-threaded execution would saturate context or introduce cognitive bias.

## Multi-Agent Architecture

```text
               ┌─────────────────────────────────────────┐
               │         Primary Lead Orchestrator       │
               │   (Synthesizer, UI Artifacts, User)     │
               └────┬─────────────────┬─────────────┬─────┘
                    │                 │             │
                    ▼                 ▼             ▼
          ┌──────────────────┐ ┌─────────────┐ ┌──────────────┐
          │  cadence-scout   │ │cadence-tester│ │ cadence-     │
          │ (Read Recon,     │ │ (Red Phase  │ │  reviewer    │
          │  Fast & Lean)    │ │  Contracts) │ │ (Audit, Lint)│
          └──────────────────┘ └─────────────┘ └──────────────┘
```

---

## Orchestration Lifecycle

### 1. Parallel Reconnaissance (Scout Phase)
When surveying multiple areas (e.g. backend service vs. frontend UI):
* Dispatch multiple `cadence-scout` agents **concurrently in a single tool call**:
  ```json
  [
    {"TypeName": "cadence-scout", "Role": "Backend API Scout", "Prompt": "Inspect auth endpoints...", "Model": "flash"},
    {"TypeName": "cadence-scout", "Role": "Frontend UI Scout", "Prompt": "Inspect auth login forms...", "Model": "flash"}
  ]
  ```
* Leverage lighter models (`flash`) for fast, cost-efficient reconnaissance without stalling the main agent.

### 2. Contract & Red Phase (Tester Phase)
* Dispatch `cadence-tester` with explicit instructions:
  - Write a failing test asserting the expected behavior.
  - Execute the test command immediately.
  - Return the exact command, test file, and failure trace.
* The orchestrator confirms the Red phase condition is met.

### 3. Implementation (Green Phase)
* For isolated implementations, invoke `self` or implement directly:
  - If experimenting with risky changes, use `Workspace: "branch"` or `"share"` to isolate the workspace from the user's primary working tree until verified.
* Run the test command to verify green status.

### 4. Objective Audit (Reviewer Phase)
* Dispatch `cadence-reviewer` to perform an independent audit:
  - Analyzes the git diff.
  - Runs static analysis (`ruff`, `mypy`, `npm run lint`).
  - Checks for edge cases and regressions without confirmation bias.

### 5. Lead Synthesis
* Primary agent reviews the reviewer's audit, executes final integration check, updates the Antigravity UI Artifact, and reports cleanly to the user.

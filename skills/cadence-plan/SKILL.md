---
name: cadence-plan
description: >-
  Create an interactive, structured implementation plan as a native Antigravity UI
  Artifact for complex features, refactors, or multi-component systems with zero Git clutter.
---

# Cadence Plan: Native Artifact Architecture & Planning

Use this skill when planning complex features, major refactorings, or multi-step implementations. Unlike legacy planning tools that commit tracking files into your repository, Cadence Plan leverages **Antigravity UI Artifacts** that render in the auxiliary pane without polluting your Git tree.

---

## Steps

### Step 1: Context Survey (Context-Efficient)
1. Survey the codebase relevant to the target feature.
2. **Context Guardrail:** If reading more than 3 unfamiliar files or logs, delegate the exploration to the `research` subagent:
   - Ask `research` to inspect relevant interfaces, schemas, and test fixtures.
   - Synthesize its report directly into the plan.

### Step 2: Generate the Native Plan Artifact
Create an artifact in the session artifact directory (`brain/<conversation-id>/`) using `write_to_file`:
- Set `ArtifactMetadata`:
  - `UserFacing: true`
  - `RequestFeedback: true`
  - `Summary`: Concise overview of the plan architecture.
- Structure the Artifact content with:
  1. **Objective & Scope:** What is being built and what is explicitly excluded.
  2. **Architecture / Flow Diagram:** Use GitHub-flavored Mermaid (`flowchart TD` or `sequenceDiagram`).
  3. **TDD Contracts (Red Phase Strategy):** Which test files and test cases will be created.
  4. **Task Breakdown:** Granular, sequenced checklist:
     ```markdown
     - [ ] Task 1: Contract & Red Tests (`tests/test_x.py`)
     - [ ] Task 2: Core Domain Logic (`src/x.py`)
     - [ ] Task 3: API / Interface Integration (`src/api.py`)
     - [ ] Task 4: Lint, Coverage, & Regression Run
     ```
  5. **Subagent Allocation (if parallel):** Designate tasks suited for isolated `self` subagents.

### Step 3: User Alignment & Feedback
- Point the user to the newly rendered Artifact in their auxiliary pane.
- If high-level architectural choices remain open, present an interactive `ask_question` dialog for immediate resolution.

### Step 4: Execution Handoff
- Transition directly to implementation using `cadence-flow` for each task:
  - Red (Failing test) $\to$ Green (Passing implementation) $\to$ Refactor.
- Update the artifact checklist as milestones complete.

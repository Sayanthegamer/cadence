---
name: cadence-tour
description: >-
  Interactive codebase tour and architecture onboarding. Generates a visual architectural map,
  data-flow diagrams, and key entry points in a native Antigravity UI Artifact.
---

# Cadence Tour: Interactive Codebase Architecture & Onboarding

Use this skill when exploring an unfamiliar repository, onboarding to a new project, or explaining the system's architecture to a new team member or beginner. Cadence Tour maps the repository from 10,000 feet down to the key entry points, generating a rich, interactive **Antigravity UI Artifact** in your sidebar.

---

## The Onboarding Protocol

```text
[1. Scout Topology] -> [2. Trace Data Flow] -> [3. Identify 3 Key Files] -> [4. Render Tour Artifact]
```

---

## Steps

### Step 1: Scout Codebase Topology
1. Dispatch [`cadence-scout`](../../agents/cadence-scout/agent.md) to discover:
   - Root project manifests (`pyproject.toml`, `package.json`, `Cargo.toml`).
   - Entry points (`main.py`, `app.py`, `src/index.ts`, `cmd/main.go`, `cli.py`).
   - Core domain directories and package hierarchies.
   - Test suites and test fixtures (`tests/conftest.py`).

### Step 2: Trace Primary Data Flow
Trace the path that data takes from input to output:
* How does a user or caller trigger the system?
* Which module processes or validates the request?
* Where does core business / scientific computation occur?
* Where does state persist?

### Step 3: Identify the "Read These 3 Files First" Path
Determine the 3 most essential files that teach 80% of how the project functions:
1. **Entry Point / Router:** Where execution kicks off.
2. **Core Domain Model / Engine:** Where the primary logic lives.
3. **Canonical Test Fixture:** Where input/output contracts are proven.

### Step 4: Render the Interactive Tour Artifact
Create a native **Antigravity UI Artifact** (`brain/<conversation-id>/`) titled `Architecture Tour: [Project Name]`:

```markdown
# 🗺️ Codebase Architecture Tour: [Project Name]

## 1. System Overview (ELI5)
[Simple 2-sentence analogy explaining what this system does in plain English]

---

## 2. System Topology & Data Flow
\`\`\`mermaid
flowchart TD
    User["User / Client Request"] --> Router["API / CLI Router"]
    Router --> Core["Core Domain Engine"]
    Core --> Invariants["Validation / Invariant Checks"]
    Core --> Storage["State / DB / Output"]
\`\`\`

---

## 3. "Read These 3 Files First"
1. **[Entry Point](file:///absolute/path/to/entry.py):** Handles input parsing and bootstraps the environment.
2. **[Core Engine](file:///absolute/path/to/engine.py):** Implements the main domain business/scientific logic.
3. **[Canonical Test](file:///absolute/path/to/test_core.py):** Shows real examples of how to initialize and use the engine.

---

## 4. Key Invariants & Rules
* [Invariant 1: e.g. All model initializations require explicit seeds for deterministic reproduction]
* [Invariant 2: e.g. Never perform blocking I/O in the event loop]

---

## 5. Developer Quickstart
* **Run Tests:** \`pytest tests/\` or \`npm test\`
* **Run Linter:** \`ruff check\` or \`npm run lint\`
```

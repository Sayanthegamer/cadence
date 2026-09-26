---
name: cadence-setup
description: >-
  Brownfield project setup, stack fingerprinting, and baseline verification engine.
  Imports existing codebases, audits pre-existing test health, and scaffolds Cadence scientific pillars.
---

# Cadence Setup: Brownfield Project Onboarding & Baseline Health Verification

Use this skill when importing an existing (brownfield) repository into Cadence, or when initializing Cadence in a new project. Unlike legacy tools that pollute repositories with heavy state machines, Cadence Setup audits the repository, verifies existing test suite health before code is modified, and scaffolds optional scientific compute pillars.

---

## The Onboarding & Baseline Protocol

```text
[1. Stack Fingerprinting] -> [2. Baseline Health Audit] -> [3. Pillar Scaffolding] -> [4. Pre-Commit Hook] -> [5. Onboarding Artifact]
```

---

## Steps

### Step 1: Automated Stack & Toolchain Discovery
1. Dispatch [`cadence-scout`](../../agents/cadence-scout/agent.md) or run `python scripts/setup_project.py --audit-only` to detect:
   - **Primary Language & Manifests:** Python (`pyproject.toml`), TypeScript/Node (`package.json`), Rust (`Cargo.toml`), Go (`go.mod`), C/C++ (`CMakeLists.txt`).
   - **Test Runner:** `pytest`, `npm test` (`vitest` / `jest`), `cargo test`, `go test ./...`, `ctest`.
   - **Linters & Formatters:** `ruff`, `eslint`, `prettier`, `clippy`, `golangci-lint`, `clang-format`.
   - **Existing Benchmarks:** `pytest-benchmark`, `criterion`, `benchmark/`, etc.
   - **Candidate Oracles:** Existing CPU/NumPy reference models or ground-truth fixtures.

### Step 2: Baseline Health Check (Zero-Assumption Pre-Flight)
1. **Execute the project's native test command** *before* any feature implementation or refactor begins.
2. **Classify Baseline Health:**
   - 🟢 **Green / Baseline Healthy:** 100% of existing tests pass. The codebase is clean; new changes can proceed with confidence.
   - 🔴 **Red / Pre-Existing Defects:** Existing tests are currently failing.
     - Document the failing test names and stack traces.
     - Warn the developer immediately: *"⚠️ Notice: The baseline test suite is currently failing (X tests failed). These are pre-existing defects, not caused by Cadence."*
     - Offer to run `/cad-debug` to resolve baseline failures before proceeding with new work.

### Step 3: Interactive Pillar Scaffolding (Configurable)
Present the developer with optional Cadence enhancements (via interactive GUI modal `ask_question` or terminal prompt):
1. **Two-Tier Governance Directory (`.agents/decisions/`):**
   - Scaffolds ADR index template for recording architectural decisions across the 8 Material Impact Vectors.
2. **Scientific Failure Archival (`.experiments/`):**
   - Scaffolds experiment archive directory with `.gitkeep` and `.gitignore` ignoring large binary simulation weights.
3. **Git Pre-Commit Hook (`.git/hooks/pre-commit`):**
   - Installs the deterministic verification hook (`scripts/pre-commit-hook.sh`) to block uncertified oracle changes or corrupted CAS experiments before commit.

### Step 4: Generate Native Onboarding UI Artifact
Render an interactive **Antigravity UI Artifact** (`brain/<conversation-id>/`) titled `Cadence Setup: [Project Name]`:

```markdown
# ⚡ Cadence Project Setup & Baseline Audit: [Project Name]

## 1. Stack Fingerprint
* **Language:** Python 3.11
* **Manifests:** \`pyproject.toml\`, \`requirements.txt\`
* **Test Runner:** \`pytest\`
* **Linters:** \`ruff\`
* **Benchmarks:** \`pytest-benchmark\` detected

---

## 2. Baseline Health Status
* **Status:** 🟢 PASSED (14 tests passed in 1.42s)
* **Pre-existing Defects:** None detected. Working tree is clean.

---

## 3. Configured Cadence Pillars
* [x] **ADR Governance:** Initialized in \`.agents/decisions/\`
* [x] **Scientific Archival:** Configured in \`.experiments/\`
* [x] **Pre-Commit Hook:** Installed in \`.git/hooks/pre-commit\`

---

## 4. Recommended Next Steps
* Run \`/cad-tour\` to explore the system topology and primary data flow.
* Run \`/cad-plan\` to design your first feature or refactor.
* Run \`/cad-flow\` to implement features using strict Red-Green-Refactor TDD.
```

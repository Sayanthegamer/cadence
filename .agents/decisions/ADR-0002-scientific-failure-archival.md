# ADR-0002: Scientific Failure Archival (2A + Selective 2B Hybrid Architecture)

- **Date:** 2026-09-26
- **Status:** 🟢 Accepted
- **Decider(s):** Human Engineer & Lead Architect
- **Governance Tier:** Tier 1 (Impacted Vectors: Vector 1: Numerical Correctness, Vector 2: Reproducibility & Determinism, Vector 7: Interfaces)

---

## 1. Context & Problem Statement

In standard web/app development, failed attempts, typos, and broken tests are "Class A Defects": uninteresting noise that should be cleanly wiped with `git reset --hard` and forgotten.

However, in experimental computing, numerical optimization, and simulation research, a failure often represents a **"Class B Scientific Failure"**:
- It demonstrates that a specific algorithmic hypothesis (e.g. higher-order integration, thread-group tiling, fast-math optimization) was physically unstable, diverged under stiffness, caused cache thrashing, or saturated memory bandwidth.
- Discarding Class B failures without archival forces future engineers and AI agents to waste compute and time repeatedly re-inventing and re-failing the exact same dead ends.
- Conversely, creating a full Git branch for every mundane syntax error or typo clutters the branch namespace with garbage.

A hybrid archival architecture was required to preserve negative scientific knowledge without polluting active source repositories.

---

## 2. Authorized Decisions

### The 2A + Selective 2B Hybrid Archival Architecture
Cadence adopts the **2A + Selective 2B Hybrid Architecture**:

1. **Architecture 2A (Machine-Readable Experiment Records & CAS):**
   - Every scientific failure, benchmark anomaly, or rejected candidate creates a queryable, structured metadata document under `.experiments/<experiment_id>.json` conforming to [`schemas/experiment-v1.json`](file:///C:/Users/Anon/.gemini/config/plugins/cadence/schemas/experiment-v1.json).
   - Untracked artifacts, diagnostic logs, crash dumps, and profiler traces are anchored in Content-Addressed Storage (`.experiments/cas/<sha256>`).
   - Tamper-evident SHA-256 integrity verification guarantees that experimental records cannot be silently modified or corrupted.

2. **Selective Architecture 2B (Value-Based Git Branching):**
   - Git branches (`archive/exp-<id>`) are created **selectively, not universally**:
     - *Trigger criteria:* High implementation effort, complex novel kernel code, partially successful mathematical prototypes, or actionable negative benchmarks.
     - Ordinary syntax errors, broken imports, and minor typos (Class A defects) are purged immediately with zero Git clutter.

3. **Preservation-First Uncertainty Handling:**
   - *The Uncertainty Invariant:* If the system or agent cannot prove with certainty whether a failure is a mundane bug (Class A) or a valuable scientific result (Class B), it **defaults to preservation (Class B)**. No potential scientific data is destroyed under uncertainty.

4. **Integration with `cadence-scout`:**
   - Scout subagents automatically survey `.experiments/` during reconnaissance to alert engineers to prior failed attempts before planning new tracks.

---

## 3. Rejected Alternatives ("Why Not That?")

* **Alternative 1: Universal Git Branching for All Failures (Pure Architecture 2B)**
  - *Why Considered:* Captures every single failure into Git's native object database.
  - *Why Rejected:* Rapidly pollutes the Git branch namespace with dozens of ephemeral branches from trivial typos, linter errors, and scratch scripts, overwhelming developer tooling and code review interfaces.
* **Alternative 2: Universal `git reset --hard` (Conductor Legacy Model)**
  - *Why Considered:* Keeps Git completely spotless.
  - *Why Rejected:* Destroys valuable negative scientific experimental results. In numerical compute, rediscovering why an algorithm failed six months later wastes hundreds of engineering hours.
* **Alternative 3: Flat Markdown Experiment Logs in Root**
  - *Why Considered:* Human-readable scratch files.
  - *Why Rejected:* Not machine-queryable by agents, prone to formatting rot, lacks CAS tamper-evident checksums, and clutters the project root.

---

## 4. Conscious Trade-offs (What We Sacrificed)

- We added localized metadata storage (`.experiments/`) and CAS blobs in the project tree, which must be git-tracked or backed up to maintain experimental memory.
- Archival incurs slight I/O overhead to compute SHA-256 digests and serialize experiment metadata before clean working tree restoration.

---

## 5. Revisit Trigger (When to Change Your Mind)

Revisit this ADR if an external experiment tracking and registry service (e.g. MLflow, Weights & Biases) is natively integrated into the workspace with local offline fallback.

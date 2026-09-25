# ADR-0001: Two-Tier Architectural Governance & The 8 Material Impact Vectors

- **Date:** 2026-09-26
- **Status:** 🟢 Accepted
- **Decider(s):** Human Engineer & Lead Architect
- **Governance Tier:** Tier 1 (Impacted Vectors: All 8 Material Impact Vectors)

---

## 1. Context & Problem Statement

Standard coding agents frequently make foundational architectural, numerical, and algorithmic decisions autonomously—such as silently swapping solvers, introducing third-party dependencies, modifying memory layouts (AoS vs. SoA), changing numerical precision (`fp64` vs `fp32`), or relaxing error tolerances. In scientific computing, graphics programming, and physical simulations, such unilateral autonomous choices can invalidate physical realism, compromise numerical stability, break deterministic reproducibility, or violate hardware cache constraints.

Conversely, requiring human sign-off for trivial, localized edits (such as formatting, naming private variables, or local refactoring) creates unbearable workflow friction and defeats the purpose of autonomous AI pair programming.

A principled governance boundary was required to distinguish consequential decisions from localized tactical changes.

---

## 2. Authorized Decisions

### The Two-Tier Governance Boundary
Architectural choices, library selections, data layouts, and mathematical/physical algorithms are governed strictly by material impact, never by nominal categorization or surface appearance:

- **Tier 1 (Foundational / Consequential — Human-Gated):**
  A decision is strictly classified as Tier 1 whenever it materially affects any of the **8 Material Impact Vectors**:
  1. *Numerical Results or Physical Correctness* (floating-point arithmetic, integration schemes, convergence rates, stability limits, boundary conditions, conservation laws).
  2. *Reproducibility or Determinism* (seed control, PRNG state, reduction order, parallel synchronization, hardware-dependent fast-math re-association).
  3. *Precision or Error Tolerances* (transitions between `fp64`/`fp32`/`fp16`/`bfloat16`, epsilon thresholds, tolerance budgets `rtol`/`atol`).
  4. *Performance Characteristics or Scaling Behavior* (asymptotic complexity shifts, vectorization, cache blocking, memory bandwidth saturation).
  5. *Memory Layout or Data Movement* (storage representations AoS vs SoA, contiguous vs strided memory, host-to-device transfers, cache hierarchies).
  6. *Concurrency, Synchronization, or Execution Model* (task vs data parallelism, warp/threadgroup sync, atomics, lock-free queues, asynchronous streams).
  7. *Public or Module Interfaces* (core API contracts, data container schemas, abstraction boundaries, coordinate systems).
  8. *Algorithmic, Mathematical, Rendering, or External Dependency Choices* (solvers, mathematical formulations, rendering paradigms, new libraries/frameworks).

- **Tier 1 Protocol:**
  The agent must investigate $\ge 2$ viable alternatives, compile a balanced **Evidence Dossier** with zero `(Recommended)` labels, zero default checkmarks, and no premature `Accepted` ADRs, and present the decision via an interactive human gate (`ask_question`). Only upon explicit human authorization is the ADR formalized in `.agents/decisions/`.

- **Tier 2 (Tactical / Localized — Autonomous Execution):**
  A choice proceeds autonomously *only* when it is localized, immediately reversible with minimal blast radius, and has **zero material impact** across all 8 vectors. The agent logs an observable 1-line trace entry: `- [Tactical Decision] <description> (Reversible, zero impact on 8 vectors)`.

- **The Uncertainty Invariant:**
  *Ambiguity is an automatic Tier 1 trigger.* If the agent cannot prove with absolute confidence that a decision has zero material impact across all 8 vectors, it is strictly forbidden from assuming it is tactical. It must treat the decision as Tier 1, halt autonomous execution, compile an Evidence Dossier, and prompt the human engineer.

---

## 3. Rejected Alternatives ("Why Not That?")

* **Alternative 1: Nominal / Category-Based Classification (e.g. "Libraries are Tier 1, Code is Tier 2")**
  - *Why Considered:* Simple rule heuristic based on file types or package manager files.
  - *Why Rejected:* Superficial. A one-line change to a time-step multiplier or floating-point accumulator inside internal code can silently break physical conservation laws, while adding a pure dev-dependency linter has zero numerical impact. Governance must track *material impact*, not file location.
* **Alternative 2: Unconditional Agent Autonomy with Post-Hoc Review**
  - *Why Considered:* Maximizes short-term execution velocity.
  - *Why Rejected:* Highly dangerous in scientific simulation and compute kernels. Once an agent switches an integration scheme or precision level, dozens of downstream tests may be adapted to fit the erroneous output, cementing subtle physical bugs permanently.
* **Alternative 3: Total Human Gating for Every Decision**
  - *Why Considered:* Absolute human oversight.
  - *Why Rejected:* Destroys pair-programming velocity by pestering the developer with trivial questions for mundane code formatting and localized helper functions.

---

## 4. Conscious Trade-offs (What We Sacrificed)

- We sacrificed instantaneous execution speed on foundational choices in exchange for zero catastrophic silent architectural regressions and mathematically verified correctness.
- Compiling balanced Evidence Dossiers requires exploring $\ge 2$ viable options and grounding them with authoritative documentation, consuming agent tokens prior to execution.

---

## 5. Revisit Trigger (When to Change Your Mind)

Revisit this ADR if formal verification systems or certified symbolic solvers allow automated mathematical proof that an algorithmic substitution guarantees strict bounded invariant equivalence without human review.

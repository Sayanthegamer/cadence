---
name: cadence-decide
description: >-
  Two-tier architectural governance engine. Compiles balanced, un-biased Evidence Dossiers,
  enforces human interactive gates for Tier-1 decisions, and formalizes permanent "Why This, Not That"
  Architectural Decision Records (ADRs).
---

# Cadence Decide: Two-Tier Architectural Governance & Decision Engine

Every senior developer and technical interviewer asks the same question: *"Why did you build it this way instead of using X?"*

Cadence Decide enforces **Two-Tier Governance** across architectural, scientific, and numerical crossroads. It ensures foundational choices are never made autonomously by an AI, compiles rigorous and balanced Evidence Dossiers, and records finalized decisions into standardized, permanent Architectural Decision Records (ADRs).

---

## The Two-Tier Governance Boundary

Before proposing or recording any architectural choice, evaluate the decision against the **8 Material Impact Vectors**:

1. **Numerical Results or Physical Correctness:** Floating-point math, integration schemes, convergence rates, stability limits, boundary conditions, or conservation laws.
2. **Reproducibility or Determinism:** Seed control, PRNG states, multi-threading reduction order, parallel synchronization, or hardware-dependent fast-math re-association.
3. **Precision or Error Tolerances:** Precision transitions (`fp64`, `fp32`, `fp16`, `bfloat16`, `tf32`), epsilon thresholds, accumulation registers, or tolerance budgets (`rtol`, `atol`).
4. **Performance Characteristics or Scaling Behavior:** Asymptotic complexity shifts ($O(N)$ vs $O(N \log N)$ vs $O(N^2)$), algorithmic vectorization, cache blocking, memory bandwidth saturation, or computational intensity.
5. **Memory Layout or Data Movement:** Storage representations (AoS vs. SoA vs. AoSoA), contiguous vs. strided memory, host-to-device transfers, shared memory caching, or memory footprint scaling.
6. **Concurrency, Synchronization, or Execution Model:** Task parallelism vs. data parallelism, thread-group/warp synchronization, atomics, lock-free queues, asynchronous stream overlapping, or SIMD dispatch.
7. **Public or Module Interfaces:** Core API signatures, data container contracts, abstraction boundaries, or coordinate system conventions that would make future architectural rewrites expensive or contagious across the codebase.
8. **Algorithmic & Mathematical Approaches:** Technology selections, core solvers, mathematical formulations, rendering paradigms, physics constraint formulations, or introduction of external libraries/dependencies.

### Classification Rules:
- **Tier 1 (Foundational / Consequential — Human-Gated):** Material impact on ANY of the 8 vectors. **Autonomous agent ADR generation is strictly forbidden.** Must follow the 3-Phase Protocol below.
- **Tier 2 (Tactical / Localized — Autonomous Execution):** Zero material impact on all 8 vectors, localized blast radius, and immediately reversible. Proceeds autonomously with an observable 1-line trace log:  
  `- [Tactical Decision] <description> (Reversible, zero impact on 8 vectors)`.
- **The Uncertainty Invariant:** *Ambiguity defaults to Tier 1.* If the agent cannot prove with absolute certainty that a choice has zero material impact, it must treat the decision as Tier 1 and prompt the human engineer.

---

## The 3-Phase Decision Protocol (Tier 1)

```text
[Phase 1: Evidence Dossier] -> [Phase 2: Human Gate (ask_question)] -> [Phase 3: Formalize ADR]
```

### Phase 1: Compile the Balanced Evidence Dossier
1. Research $\ge 2$ viable, concrete candidates.
2. Ground third-party library comparisons using Context-7 MCP (`resolve-library-id` $\to$ `query-docs`) when installed.
3. Evaluate each candidate across the relevant material impact vectors (mathematical stability, asymptotic complexity, memory layout, concurrency, hardware dependencies, and failure modes).
4. **Strict Neutrality Invariant:**
   - **Zero `(Recommended)` labels:** Never mark an option as recommended or default.
   - **Zero Default Checkmarks:** Never pre-select a winner.
   - **Zero Editorial Bias:** Never favor "simplicity" or "minimal lines of code" when numerical stability or performance scaling is at stake.
5. Record the dossier in an Antigravity UI Artifact (`brain/<conversation-id>/evidence_dossier_<slug>.md`).

### Phase 2: Interactive Human Decision Gate
1. Present the Evidence Dossier to the human engineer via `ask_question`.
2. Provide neutral, objective summaries of each candidate in the option descriptions.
3. **Anti-Premature Logging Gate:** The agent is **strictly prohibited** from writing or committing an `Accepted` ADR to `.agents/decisions/` prior to receiving the human engineer's explicit selection.

### Phase 3: Formalize the ADR & Maintain Index
Only upon receiving explicit human authorization, write the finalized ADR file in `.agents/decisions/ADR-XXX-[slug].md`:

```markdown
# ADR-001: [Title of Decision]

- **Date:** YYYY-MM-DD
- **Status:** 🟢 Accepted (or 🟡 Proposed | 🚜 Superseded)
- **Decider(s):** [Human Engineer / Lead Architect]
- **Governance Tier:** Tier 1 (Impacted Vectors: [e.g., Vector 1: Numerical Correctness, Vector 5: Memory Layout])

---

## 1. Context & Problem Statement
What specific requirement, bottleneck, or constraint forced this decision? What were the physical/computational boundaries?

## 2. The Decision: Why This Option Won
- **Chosen:** [Selected Pattern / Library / Solver]
- **The Decisive Factor:** The primary reason authorized by the engineer (e.g., "Unconditional $A$-stability for stiff ODEs despite higher per-step matrix inversion cost").

## 3. Rejected Alternatives ("Why Not That?")
Document the exact reasons alternative candidates were dismissed:
* **Alternative 1: [Name]**
  - *Why Considered:* [Appealing aspect]
  - *Why Rejected:* [Decisive fatal flaw, numerical instability, or OOM boundary]
* **Alternative 2: [Name]**
  - *Why Considered:* [Appealing aspect]
  - *Why Rejected:* [High operational complexity, cache thrashing, or lack of GPU fast-path]

## 4. Conscious Trade-offs (What We Sacrificed)
Great engineering acknowledges trade-offs. What did we give up by choosing this?
* Example: *"We sacrificed instantaneous per-step computation in exchange for unconditional numerical stability under large time-steps."*

## 5. Revisit Trigger (When to Change Your Mind)
Under what exact, measurable condition should a future developer or AI agent reconsider this decision?
* Example: *"Revisit if particle count exceeds $N=10^6$ or if GPU compute shader backend is implemented."*
```

### Maintain the ADR Index
Update `.agents/decisions/README.md` listing all ADRs:

```markdown
# Architectural Decision Records (ADRs)

| ADR | Decision | Governance Tier | Status | Revisit Condition |
|---|---|---|---|---|
| [ADR-001](./ADR-001-implicit-euler.md) | Implicit Euler for Stiff Mesh Simulation | Tier 1 | 🟢 Accepted | Particle count > 10^6 |
| [ADR-002](./ADR-002-deterministic-seeds.md) | Seeded Fixtures for Oracle Invariants | Tier 1 | 🟢 Accepted | Multi-GPU distributed training |
```

---

## How Agents Use This

1. During reconnaissance, [`cadence-scout`](../cadence-scout/agent.md) checks `.agents/decisions/`.
2. Any candidate architecture that violates an accepted ADR is pruned before being proposed.
3. If an agent believes a Revisit Trigger has been met, it explicitly cites the ADR, compiles an Evidence Dossier, and presents a Tier-1 gate to the human engineer before proposing any migration.

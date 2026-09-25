---
name: cadence-decide
description: >-
  Record high-signal Architectural Decision Records (ADRs) explaining "Why This, Not That"
  to preserve institutional memory, impress interviewers/reviewers, and instruct future agents
  to respect existing design choices.
---

# Cadence Decide: "Why This, Not That" Architectural Decision Engine

Every senior developer and technical interviewer asks the same question: *"Why did you build it this way instead of using X?"*

Cadence Decide captures these critical crossroads in standardized, high-signal Architectural Decision Records (ADRs). It serves as your permanent engineering journal, helps interviewers understand your depth, and ensures future AI agents respect your choices instead of proposing previously rejected patterns.

---

## When to Use

* When selecting a core library, framework, or database (e.g. SQLite vs. Postgres, Vitest vs. Jest).
* When choosing between architectural patterns (e.g. Synchronous vs. Event-driven, In-memory vs. Redis).
* When deciding algorithm or data structures (e.g. Tensor buffer vs. Generator, Cosine similarity vs. Euclidean).
* Immediately following `cadence-ideate` after selecting a recommended archetype.

---

## The Decision Record Protocol

When invoking `cadence-decide`, generate an ADR file in `.agents/decisions/` (e.g. `.agents/decisions/ADR-001-local-sqlite-storage.md`):

```markdown
# ADR-001: [Title of Decision]

- **Date:** YYYY-MM-DD
- **Status:** 🟢 Accepted (or 🟡 Proposed | 🚜 Superseded)
- **Decider(s):** [User / Lead Engineer]

---

## 1. Context & Problem Statement
What specific requirement, bottleneck, or constraint forced this decision? What were the real-world boundaries (e.g. zero cloud budget, offline support, deterministic reproducibility)?

## 2. The Decision: Why This Option Won
- **Chosen:** [Selected Pattern / Library / Architecture]
- **The Decisive Factor:** The #1 reason this choice was picked over all others (e.g. "Zero external infrastructure, single-file backups, embedded query latency < 0.2ms").

## 3. Rejected Alternatives ("Why Not That?")
Document the exact reasons alternative candidates were dismissed. This proves engineering rigor to interviewers and stops future AI agents from suggesting them:
* **Alternative 1: [Name]**
  - *Why Considered:* [Appealing aspect]
  - *Why Rejected:* [Decisive fatal flaw or overkill for our current phase]
* **Alternative 2: [Name]**
  - *Why Considered:* [Appealing aspect]
  - *Why Rejected:* [High operational complexity / maintenance burden]

## 4. Conscious Trade-offs (What We Sacrificed)
Great engineering acknowledges trade-offs. What did we give up by choosing this?
* Example: *"We sacrificed multi-writer concurrency in exchange for zero setup and instant local queries."*

## 5. Revisit Trigger (When to Change Your Mind)
Under what exact, measurable condition should a future developer or AI agent reconsider this decision?
* Example: *"Revisit if concurrent writes exceed 50 requests/second or multi-region sync is required."*
```

---

## Index Maintenance

Maintain an index at `.agents/decisions/README.md` listing all ADRs:

```markdown
# Architectural Decision Records (ADRs)

| ADR | Decision | Status | Revisit Condition |
|---|---|---|---|
| [ADR-001](./ADR-001-local-sqlite.md) | Local SQLite for State Storage | 🟢 Accepted | Concurrent writes > 50 req/s |
| [ADR-002](./ADR-002-deterministic-seeds.md) | Seeded Fixtures for Oracle Invariants | 🟢 Accepted | Multi-GPU distributed training |
```

---

## How Agents Use This

1. During reconnaissance, [`cadence-scout`](../cadence-scout/agent.md) checks `.agents/decisions/`.
2. Any candidate architecture that violates an accepted ADR is pruned before being proposed.
3. If an agent believes a Revisit Trigger has been met, it explicitly cites the ADR and asks the user before proposing a migration.

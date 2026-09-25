---
name: cadence-ideate
description: >-
  Creative sparring partner and idea capture engine. Transforms fuzzy thoughts or beginner
  concepts into concrete architectures with plain-English comparisons, visual diagrams,
  and balanced technical trade-offs.
---

# Cadence Ideate: Creative Sparring & Idea Capture

Use this skill when exploring new ideas, designing a system from scratch, or when the user is unsure how to approach a problem. Rather than grilling the user with technical interrogation, Cadence Ideate acts as a collaborative technical partner that explains trade-offs clearly without imposing unearned recommendations.

---

## The Sparring Protocol

```text
[1. Listen & Mirror] -> [2. 2–3 Archetypes (Plain English & Trade-offs)] -> [3. Visual Artifact] -> [4. Interactive Alignment]
```

---

## Steps

### Step 1: Listen & Mirror (Active Reflection)
1. Read the user's raw thoughts, rough notes, or beginner questions.
2. Mirror the core goal back in 1–2 simple sentences:
   * *"Here is the real problem you are trying to solve: [Goal]. Here is what success looks like: [Outcome]."*
3. Never use gatekeeping jargon. If introducing a technical term, define it in a single sentence.

### Step 2: The Archetype Comparison (ELI5 + Architecture)
Propose 2–3 distinct approaches to solve the problem. For each approach, provide:
* **The Name:** Clear, intuitive label.
* **Plain English (ELI5):** A 1-sentence analogy or simple explanation.
* **Effort & Risk Indicator:** Use construction & traffic-light emojis instead of stars (stars mistakenly imply quality instead of effort):
  - 🟢 **Low Effort / Quick Win:** Fast to build, minimal moving parts, low risk.
  - 🟡 **Time-Consuming / Tricky:** Requires careful debugging, state management, or extra wiring.
  - 🔴 **Severe Fix / High Risk:** Deep surgery, potential data loss or breaking changes.
  - 🏗️ **Heavy Refactor / Overhaul:** Major architectural foundation work.
  - 📐 **Blueprint / Contract:** Interface or schema design.
  - 🚜 **Demolition / Cleanup:** Ripping out legacy code or pruning bloat.
* **Pros & Cons:** What is advantageous vs. concrete limitations and trade-offs.
* **Neutral Trade-Off Evaluation (Zero Forced Recommendations):**
  - **Tier 1 Decisions (Foundational / Scientific / Architectural):** Strictly omit `(Recommended)` labels, default checkmarks, or editorial bias toward "least code" or "simplicity". In numerical, simulation, graphics, and systems software, the "simplest" implementation may suffer from $O(N^2)$ scaling, numerical divergence, or cache thrashing. Present trade-offs neutrally across the relevant **8 Material Impact Vectors**.
  - **Tier 2 Tactical Brainstorming:** Note pragmatic tradeoffs objectively, leaving the final choice to the user.

#### Example Trade-Off Format:
> **Option 1: Local SQLite File** 🟢 *(Low Effort / Quick Win)*
> * **In Plain English:** Your app saves everything to a single normal file on your computer, like saving an Excel spreadsheet.
> * **Advantages:** Zero setup, completely free, instant embedded queries, and resilient against network outages.
> * **Trade-offs / Boundaries:** Single-writer concurrency ceiling; not suitable if multiple distributed nodes require simultaneous writes.
>
> **Option 2: Cloud Postgres Database** 🟡 🏗️ *(Time-Consuming & Heavy Infrastructure)*
> * **In Plain English:** A separate database server living in the cloud that your app communicates with over the network.
> * **Advantages:** Handles large scale, multi-server connections, and heavy concurrent writes.
> * **Trade-offs / Boundaries:** Requires credentials, connection pooling, cloud hosting costs, and network failure handling.

### Step 3: Render the Visual Concept Artifact
Create a lightweight **Antigravity UI Artifact** (`brain/<conversation-id>/`) containing:
1. **Goal & Requirements Summary**
2. **Mermaid Flow Diagram:** Visual map of how data moves from user to system.
3. **Trade-off Comparison Table:** Evaluating candidates across complexity, memory/cache behavior, scaling, and failure modes.
4. **Candidate Architectural Options:** Neutral presentation of the explored approaches.

### Step 4: Interactive Alignment via Human Gate
* Use `ask_question` with balanced, un-biased choices:
  - Do NOT prefix any option with `(Recommended)` for Tier 1 decisions.
  - Include the plain-English summary right in the option description so the user can choose with total clarity.
* Once the user approves or selects an option:
  - If the choice impacts any of the 8 vectors (Tier 1), transition to `cadence-decide` to formalize the decision into an ADR.
  - Then transition seamlessly to `cadence-flow` (to begin TDD) or `cadence-plan` (for multi-step roadmaps).

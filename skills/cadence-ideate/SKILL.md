---
name: cadence-ideate
description: >-
  Creative sparring partner and idea capture engine. Transforms fuzzy thoughts or beginner
  concepts into concrete architectures with plain-English comparisons, visual diagrams,
  and clear recommendations.
---

# Cadence Ideate: Creative Sparring & Idea Capture

Use this skill when exploring new ideas, designing a system from scratch, or when the user is unsure how to approach a problem. Rather than grilling the user with technical interrogation, Cadence Ideate acts as a collaborative technical partner that explains trade-offs in plain English.

---

## The Sparring Protocol

```text
[1. Listen & Mirror] -> [2. 3 Archetypes (Plain English)] -> [3. Visual Artifact] -> [4. Recommended Path]
```

---

## Steps

### Step 1: Listen & Mirror (Active Reflection)
1. Read the user's raw thoughts, rough notes, or beginner questions.
2. Mirror the core goal back in 1–2 simple sentences:
   * *"Here is the real problem you are trying to solve: [Goal]. Here is what success looks like: [Outcome]."*
3. Never use gatekeeping jargon. If introducing a technical term, define it in a single sentence.

### Step 2: The 3 Archetype Comparison (ELI5 + Architecture)
Propose 2–3 distinct approaches to solve the problem. For each approach, provide:
* **The Name:** Clear, intuitive label.
* **Plain English (ELI5):** A 1-sentence analogy or simple explanation.
* **Complexity Level:** ⭐ (Beginner/Fast) | ⭐⭐ (Moderate) | ⭐⭐⭐ (Advanced/Heavy).
* **Pros & Cons:** What is great about it vs. what to watch out for.
* **The Clear Recommendation:** Always mark the most pragmatic option with **(Recommended)** and explain *why* it is the best default (e.g. simplest to debug, zero extra servers, least code).

#### Example Trade-Off Format:
> **Option 1: (Recommended) Local SQLite File** ⭐
> * **In Plain English:** Your app saves everything to a single local file on your computer, like saving a spreadsheet.
> * **Why pick it:** Zero setup, completely free, instant, and impossible to break with external network failures.
> * **When you outgrow it:** If you have 50 different servers writing to the same database simultaneously.
>
> **Option 2: Cloud Postgres Database** ⭐⭐⭐
> * **In Plain English:** A separate database server running in the cloud that your app talks to over the internet.
> * **Why pick it:** Handles huge scale, multiple servers, and heavy concurrent writes.
> * **Why skip it for now:** Requires credentials, connection pooling, cloud hosting costs, and network debugging.

### Step 3: Render the Visual Concept Artifact
Create a lightweight **Antigravity UI Artifact** (`brain/<conversation-id>/`) containing:
1. **Goal & Requirements Summary**
2. **Mermaid Flow Diagram:** Visual map of how data moves from user to system.
3. **Trade-off Comparison Table**
4. **Recommended Roadmap:** The 80/20 minimal starting point.

### Step 4: Gentle Interactive Alignment
* If asking the user to decide, use `ask_question` with clear, non-intimidating choices:
  - Lead with the **(Recommended)** option first.
  - Include the plain-English summary right in the option description so a beginner can choose with total confidence.
* Once the user approves or selects an option, seamlessly transition to `cadence-flow` (to start TDD) or `cadence-plan` (for larger roadmaps).

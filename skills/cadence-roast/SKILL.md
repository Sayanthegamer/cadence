---
name: cadence-roast
description: >-
  Convene the 4-agent Idea Roast Council (The Believer, The Skeptic, The Investor, The Judge)
  when the user is planning a commercial product, startup, paid tool, SaaS, or monetized feature.
  Do NOT use for fun experiments, hobby projects, or scientific exploration.
---

# Cadence Roast: The 4-Agent Idea Council (Commercial & Startup Evaluation)

Ten minutes, not six months. Before spending months building something intended to make money, convene the four-agent council to ruthlessly test its commercial viability, willingness to pay, and fatal risks.

> [!IMPORTANT]
> **Intent Filter:**
> - **USE FOR:** Commercial ventures, startups, SaaS, paid developer tools, client products, or monetization-driven features.
> - **DO NOT USE FOR:** Fun experiments, weekend hackathons, learning prototypes, open-source toys, or scientific research. When building for curiosity or fun, proceed directly to `cadence-ideate` or `cadence-flow`.

```text
 ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
 │ 1. The Believer │ ───▶  │  2. The Skeptic │ ───▶  │ 3. The Investor │
 │ (Upside & Moat) │       │ (Fatal Flaw)    │       │ (Money & Proof) │
 └─────────────────┘       └─────────────────┘       └─────────────────┘
                                                              │
                                                              ▼
                                                     ┌─────────────────┐
                                                     │   4. The Judge  │
                                                     │(BUILD/FIX/KILL) │
                                                     └─────────────────┘
```

---

## The Execution Protocol

### Step 1: Capture the Core Idea
Accept the user's idea, feature proposal, or architectural shift. 

### Step 2: The Sequential Roast Handoff
Execute the council in strict sequence so each agent reacts to the prior arguments:

1. **The Believer (`roast-believer`):**
   - Makes the strongest, most honest case FOR the idea.
   - Identifies who desperately needs it, why now, the best version, and the one core bet.
2. **The Skeptic (`roast-skeptic`):**
   - Receives the idea + the Believer's case.
   - Attacks who will *not* pay, existing workarounds, founder blind spots, and the fatal flaw.
3. **The Investor (`roast-investor`):**
   - Receives the idea + Believer + Skeptic cases.
   - Evaluates proof of willingness to pay, time to first dollar, the 7-day smoke test, and personal capital commitment.
4. **The Judge (`roast-judge`):**
   - Receives the entire debate.
   - Hands down an unambiguous ruling:
     - 🟢 **BUILD:** Real upside, manageable risks, clear path to revenue or utility.
     - 🟡 🏗️ **FIX FIRST:** Promising concept, but one critical flaw/pivot must be resolved first.
     - 🔴 🚜 **KILL:** Fatal flaw, existing workarounds dominate, or zero willingness to pay. Stop now.

### Step 3: Render Persistent Ruling Artifact
Render the final verdict and full council proceedings as an **Antigravity UI Artifact** (`brain/<conversation-id>/`) titled `Idea Roast: [Idea Name]`:
- **Header:** Verdict Badge (🟢 BUILD | 🟡 🏗️ FIX FIRST | 🔴 🚜 KILL)
- **The Core Ruling & Single Biggest Risk**
- **The 10-Minute Pre-Code Test**
- **The Pivot Trigger (if FIX FIRST)**
- **Full Council Transcript:** Collapsible sections for Believer, Skeptic, and Investor.

### Step 4: Next-Day Memory & Execution Bridge
- Because the ruling is saved to an Antigravity Artifact, the session retains memory of the decision.
- If the verdict is 🟢 **BUILD**, immediately offer to transition into [`cadence-plan`](../cadence-plan/SKILL.md) or [`cadence-flow`](../cadence-flow/SKILL.md).

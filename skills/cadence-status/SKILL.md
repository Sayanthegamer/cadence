---
name: cadence-status
description: >-
  Displays an instant status overview of the project, active tasks, git working tree,
  and immediate next steps without parsing bulky markdown files. Replaces conductor-status.
---

# Cadence Status: Instant Project & Session Standup

Use this skill whenever you start a session, switch tasks, or ask *"Where did we leave off?"*. Unlike legacy status tools that read through 5 different markdown files on disk, Cadence Status gathers live ground-truth from Git and active Antigravity UI Artifacts in seconds with zero repository bloat.

---

## The Status Protocol

### Step 1: Inspect Live Environment
1. **Branch & Tree Check:**
   - Run `git branch --show-current`
   - Run `git status -s` to inspect dirty, staged, or untracked files.
2. **Recent History:**
   - Run `git log -n 3 --oneline` to see the most recent completed work.
3. **Plan & Artifact Check:**
   - Check the current conversation artifacts or look for the most recent Plan Artifact (`brain/<conversation-id>/`).
4. **Decisions Check:**
   - Check `.agents/decisions/` to see active Architectural Decision Records.

### Step 2: Synthesize the Status Brief
Present a concise, visually clear briefing using Cadence construction & status indicators:

```markdown
# 🚦 Cadence Project Status

- **Branch:** `main` (🟢 Clean | 🟡 In-Flight Changes)
- **Active Mission:** [Feature or Bug being worked on]
- **Last Commit:** `abc1234` [Commit message]

---

### 📊 Task Progress
- [x] 📐 Task 1: API Contracts & Red Tests (`tests/test_auth.py`) 🟢
- [~] 🔨 Task 2: Core Domain Logic (`src/auth.py`) 🟡 *(IN PROGRESS)*
- [ ] 🏗️ Task 3: API & Architecture Integration (`src/api.py`) 🟡
- [ ] 🧰 Task 4: Lint, Typecheck, & Full Regression Run 🟢

### 🟡 In-Flight Modifications
* `src/auth.py` (Unstaged changes, 14 lines added)

### 🚀 Immediate Next Action
Run the targeted Red test to verify current state:
`pytest tests/test_auth.py -k test_refresh_token`
```

### Step 3: Offer Next Action
Directly prompt the user with next steps:
* *"Would you like to resume Task 2 with `cadence-flow`?"*
* *"Would you like to run the test suite now?"*

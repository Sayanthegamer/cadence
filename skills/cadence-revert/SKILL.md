---
name: cadence-revert
description: >-
  Safely roll back unviable experiments, broken implementations, or flawed tasks to a
  clean checkpoint, diagnose the failure reason, and reset state for a fresh attempt.
---

# Cadence Revert: Clean Rollback & Recovery

Use this skill when an implementation path encounters an architectural dead end, causes unmanageable regressions, or gets stuck in a local minimum. Rather than stacking messy workarounds onto a flawed foundation, Cadence Revert provides a clean, disciplined recovery.

---

## Steps

### Step 1: Diagnose & Capture Learning
1. Before discarding changes, identify exactly why the approach failed:
   - Was an assumption about an underlying library or API incorrect?
   - Did the design conflict with existing framework contracts?
   - Did the approach introduce irreconcilable performance or coupling issues?
2. Note the takeaway so the next iteration avoids repeating the same pitfall.

### Step 2: Safety Check
1. Run `git status` to inspect all modified and untracked files.
2. Confirm with the user before discarding work if any unstaged work was done manually by the user.

### Step 3: Clean Reset
1. Discard modified tracked files:
   ```powershell
   git restore .
   ```
2. Clean untracked artifacts/files created during the failed attempt (excluding ignored files):
   ```powershell
   git clean -fd
   ```
3. Run `git status` to verify the working tree is clean.

### Step 4: Re-align & Retry
1. Return to the clean state.
2. Formulate an alternative architectural strategy based on the diagnosis from Step 1.
3. Resume with `cadence-flow` (or update the Plan Artifact if using `cadence-plan`).

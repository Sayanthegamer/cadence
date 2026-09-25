---
name: cadence-debug
description: >-
  Scientific root-cause debugging protocol. Isolates defects with minimal reproduction
  scripts, forms concrete hypotheses, instruments diagnostic probes, and cures root causes
  without panic-editing.
---

# Cadence Debug: Scientific Root-Cause Autopsy

Use this skill when facing a difficult, mysterious, or non-obvious bug (e.g. runtime crashes, race conditions, memory leaks, or silent numerical drift). Rather than making random, chaotic edits to see what sticks, Cadence Debug enforces a rigorous **5-step scientific method**.

---

## The Scientific Autopsy Protocol

```text
[1. Isolate Repro] -> [2. Form Hypotheses] -> [3. Instrument Probes] -> [4. Pinpoint Cause] -> [5. Surgical Cure]
```

---

## Steps

### Step 1: Minimal Isolation (Do NOT Touch Production Code)
1. Never edit production files before isolating the defect.
2. Create a minimal, standalone reproduction script or a targeted failing test:
   - Python: `tests/test_repro_<issue>.py` or `scratch/repro.py`
   - Node: `repro.js` or `tests/repro.spec.ts`
3. Execute the reproduction script and verify that it reproduces the exact error or bad output reliably.

### Step 2: Formulate 2–3 Testable Hypotheses
Before guessing a fix, write down 2 or 3 distinct technical hypotheses explaining *why* the failure happens:
* **Hypothesis A:** Shape/Type mismatch across an API boundary.
* **Hypothesis B:** State mutation or concurrency race condition.
* **Hypothesis C:** Unhandled edge case (e.g. empty collection, null pointer, floating-point precision).

### Step 3: Instrument Diagnostic Probes
1. Insert non-invasive diagnostic assertion probes or targeted logs at the suspect boundary:
   - Log intermediate tensor shapes, types, or return values.
2. Execute the reproduction script to inspect the probe outputs.
3. Eliminate false hypotheses based on empirical probe data.
4. **External API & Library Verification (Context-7 MCP):** If the defect traces to third-party library behaviors, unexpected parameters, or version incompatibilities, query Context-7 MCP (`resolve-library-id` $\to$ `query-docs`) to inspect current documentation and official code snippets before assuming incorrect behavior.

### Step 4: Confirm Root Cause
1. Pinpoint the exact line, variable, or contract violation responsible for the defect.
2. Verify you understand *why* it broke, not just *that* it broke.

### Step 5: Surgical Cure & Regression Shield
1. Apply the leanest, most targeted fix in production code.
2. Re-run the reproduction script to confirm the failure is cured (exit code 0).
3. Remove all temporary diagnostic probes and scratch scripts.
4. Promote the reproduction script into a permanent unit test in `tests/`.
5. Run the broader test suite to confirm zero regressions.

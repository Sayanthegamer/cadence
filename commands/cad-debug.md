---
name: cad-debug
description: Scientific root-cause debugging protocol (No panic-coding).
---

Execute the `cadence-debug` skill:
1. Do NOT edit production code yet.
2. Create a minimal standalone reproduction script to reproduce the defect.
3. Formulate 2-3 testable hypotheses.
4. Instrument diagnostic assertion probes to isolate the root cause.
5. Apply the surgical cure, verify clean pass, and convert repro into a permanent test in `tests/`.

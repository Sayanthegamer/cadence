---
name: cad-decide
description: Record a "Why This, Not That" Architectural Decision Record (ADR) for interviews and agent memory.
---

Execute the `cadence-decide` skill:
1. Capture the architectural crossroad (chosen option vs rejected alternatives).
2. Generate an ADR file in `.agents/decisions/ADR-XXX-[title].md`:
   - Decisive reason why chosen option won.
   - Exact reasons alternatives were rejected ("Why Not That?").
   - Conscious trade-offs & sacrifices.
   - Measurable Revisit Trigger.
3. Update the `.agents/decisions/README.md` index.

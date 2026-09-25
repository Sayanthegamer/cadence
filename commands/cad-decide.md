---
name: cad-decide
description: Two-tier architectural governance engine. Compiles Evidence Dossiers, gates Tier-1 choices, and logs permanent ADRs.
---

Execute the `cadence-decide` skill:
1. Evaluate against the 8 Material Impact Vectors (Tier 1 vs Tier 2, defaulting to Tier 1 under uncertainty).
2. For Tier 1: Compile a balanced, un-biased Evidence Dossier ($\ge 2$ alternatives, zero `(Recommended)` labels).
3. Gate with human engineer via interactive `ask_question` modal (autonomous premature logging is forbidden).
4. Upon explicit human authorization, generate `.agents/decisions/ADR-XXX-[slug].md` with status `Accepted`.
5. Update the `.agents/decisions/README.md` index.

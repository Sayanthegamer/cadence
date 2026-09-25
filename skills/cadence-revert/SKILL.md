---
name: cadence-revert
description: >-
  Scientific failure archival and clean rollback engine. Implements the 2A + Selective 2B
  hybrid archival architecture, preservation-safe uncertainty handling, queryable metadata schemas,
  Content-Addressed Storage (CAS) trace anchoring, and value-based Git branching.
---

# Cadence Revert: Scientific Failure Archival & Disciplined Rollback

In scientific computing, graphics programming, and physical simulation, **negative results are vital scientific data**. Discarding an experiment that diverged, leaked energy, or hit an Out-Of-Memory ceiling is destructive because it erases hard-won institutional knowledge. Conversely, hoarding failed code as messy commented blocks or git junk pollutes production agility.

Cadence Revert solves this by implementing the **2A + Selective 2B Hybrid Archival Lifecycle**:
- **Class A (Ordinary Defect):** Typos, syntax bugs, broken test fixtures, and trivial logic mistakes are discarded immediately (`git restore .` and `git clean -fd`) with zero repository clutter.
- **Class B (Scientific / Engineering Failure):** Numerical divergence, loss of conservation, GPU memory exhaustion, driver faults, and unviable kernel architectures are archived into a canonical, queryable scientific lab notebook (`.experiments/<YYYY-MM-DD>_<slug>/`) with selective Git branching.

---

## The Preservation-Safe Uncertainty Invariant

> **Rule:** *Preserve first, ask second. Never delete potentially meaningful evidence under uncertainty.*  
> If Cadence cannot determine with absolute confidence whether a failure is an ordinary defect (Class A) or a meaningful scientific result (Class B), it is **strictly forbidden from discarding the changes**.  
> It must immediately preserve the candidate diff and state into `.experiments/pending_<YYYY-MM-DD>_<slug>/`, reset the working tree, and prompt the human engineer via `ask_question` for formal classification.

---

## Value-Based Selective Git Branching Criteria

Branches are **not** created based on arbitrary line counts (e.g. `> 50 lines`). A dedicated Git branch (`experiments/<YYYY-MM-DD>_<slug>`) is created if and only if one of the following four criteria is satisfied:

1. **Interactive Debugging Value:** Preserving runnable binary state is required to launch external GPU/native profilers or frame debuggers (RenderDoc, NVIDIA Nsight Systems/Compute, Intel VTune, Apple Metal Frame Capture).
2. **Re-runnable Comparison Value:** Represents a competing mathematical formulation, baseline kernel, or candidate solver that may serve as a comparison target for future benchmarks, papers, or ablation studies.
3. **Complex State Re-creation:** Involves non-trivial driver interactions, pipeline state objects, custom compute dispatch layouts, or shader stages that would be difficult or error-prone to reconstruct solely from a flat `.diff` patch.
4. **Explicit Human Request:** The engineer explicitly instructs: *"Preserve this branch."*

Otherwise, the experiment is preserved using the **Canonical Notebook (2A)** alone (`metadata.json`, `parameters.yaml`, `autopsy.md`, `patch.diff`), keeping Git branches clean and focused.

---

## The Archival Protocol

```text
[1. Classify Failure] -> [2. Preserve State & CAS Anchor] -> [3. Selective Branching] -> [4. Clean Reset] -> [5. Index & Re-align]
```

### Step 1: Classify Failure (Class A vs. Class B)
1. Inspect the defect signature:
   - *Class A (Ordinary Defect):* Syntax errors, missing imports, broken test fixtures, wrong variable names.  
     $\implies$ Proceed to Step 4 (Clean Reset).
   - *Class B (Scientific Failure):* Numerical divergence, loss of conservation, GPU OOM / timeout, hardware fault, algorithmic stability collapse.  
     $\implies$ Proceed to Step 2 (Archival).
   - *Uncertain:* Apply the **Preservation-Safe Uncertainty Invariant**. Archive to `.experiments/pending_<slug>/`, reset working tree, and prompt the engineer.

### Step 2: Preserve State & CAS Anchor Untracked Traces
When archiving a Class B failure into `.experiments/<YYYY-MM-DD>_<slug>/`:

1. **Tracked Core Files:**
   - **`patch.diff`:** Complete unified diff of candidate changes against base commit:
     ```powershell
     git diff HEAD > .experiments/<id>/patch.diff
     ```
   - **`parameters.yaml`:** Physical and computational hyperparameter snapshot:
     ```yaml
     experiment_id: "2026-09-26_jacobi_stiffness_divergence"
     parameters:
       dt: 0.01
       stiffness: 1.0e+5
       iterations: 200
       solver: "jacobi"
     ```
   - **`autopsy.md`:** Structured scientific diagnosis:
     - Hypothesis tested.
     - Expected vs. observed physical behavior.
     - Divergence step, residual history, or failure signature.
     - Root cause analysis and mathematical takeaway.

2. **Machine-Readable Metadata (`metadata.json`):**
   Write strongly-typed JSON conforming to [`schemas/experiment-v1.json`](../../schemas/experiment-v1.json):
   ```json
   {
     "$schema": "https://cadence.dev/schemas/experiment-v1.json",
     "experiment_id": "2026-09-26_jacobi_stiffness_divergence",
     "timestamp": "2026-09-26T00:20:00Z",
     "commit_base": "5b79071c",
     "git_ref": null,
     "reproduction": {
       "command": "python -m physics.sim --solver jacobi --dt 0.01 --stiffness 1e5",
       "seed": 42,
       "input_data": "data/meshes/armadillo.obj"
     },
     "classification": {
       "category": "SCIENTIFIC_FAILURE",
       "failure_mode": "NUMERICAL_DIVERGENCE",
       "primary_subsystem": "constraint_solver"
     },
     "environment": {
       "backend": "CUDA",
       "device_name": "NVIDIA RTX 4090",
       "driver_version": "555.85",
       "precision": "FP32",
       "compiler_flags": ["-O3"]
     },
     "parameters": {
       "dt": 0.01,
       "stiffness": 100000.0,
       "iterations": 200
     },
     "measurements": {
       "diverged_at_step": 48,
       "final_residual": 0.0142,
       "loss_of_conservation": { "initial_energy": 100.0, "final_energy": 1482.3 }
     },
     "tracked_core": {
       "parameters_file": "parameters.yaml",
       "autopsy_file": "autopsy.md",
       "patch_file": "patch.diff"
     },
     "untracked_artifacts": [
       {
         "artifact_id": "trace:residuals:csv",
         "relative_path": ".experiments/traces/2026-09-26_residuals.csv",
         "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
         "byte_size": 1420580,
         "mime_type": "text/csv"
       }
     ],
     "hypothesis": "Jacobi solver diverged due to extreme diagonal dominance loss under high stiffness."
   }
   ```

3. **Content-Addressed Storage (CAS) Hash Anchoring:**
   - Large raw artifacts (residual CSVs, Nsight profiles, memory dumps) are written to `.experiments/traces/` (which is included in `.gitignore`).
   - For every untracked artifact, compute its SHA-256 hash and exact byte size:
     ```powershell
     $hash = (Get-FileHash -Algorithm SHA256 $tracePath).Hash.ToLower()
     $size = (Get-Item $tracePath).Length
     ```
   - Store these in `metadata.json` under `untracked_artifacts`.
   - If a trace file is modified, deleted, or corrupted, downstream query tools detect the discrepancy immediately.

### Step 3: Selective Git Branch Creation
If the failure meets any of the **Value-Based Branching Criteria**:
1. Commit the candidate state to a dedicated branch:
   ```powershell
   git checkout -b experiments/<YYYY-MM-DD>_<slug>
   git add -A
   git commit -m "exp(<subsystem>): record failure <YYYY-MM-DD>_<slug> for interactive debugging"
   git checkout main
   ```
2. Record `"git_ref": "experiments/<YYYY-MM-DD>_<slug>"` in `metadata.json`.

If the criteria are not met, leave `"git_ref": null` and maintain diff-only archival.

### Step 4: Clean Reset
1. Discard modified tracked files:
   ```powershell
   git restore .
   ```
2. Clean untracked files from the candidate attempt:
   ```powershell
   git clean -fd
   ```
3. Verify working tree is pristine via `git status`.

### Step 5: Index Maintenance & Strategic Pivot
1. Update `.experiments/README.md` index table:
   ```markdown
   | Date | Experiment ID | Failure Mode | Backend | Hardware | Git Ref | Takeaway |
   |---|---|---|---|---|---|---|
   | 2026-09-26 | [jacobi_stiffness](./2026-09-26_jacobi_stiffness) | NUMERICAL_DIVERGENCE | CUDA | RTX 4090 | - | Jacobi loses diagonal dominance at stiffness > 1e4; pivot to PCG |
   ```
2. Re-align with the human engineer on the next hypothesis or solver strategy.

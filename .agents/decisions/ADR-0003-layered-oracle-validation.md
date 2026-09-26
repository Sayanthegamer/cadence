# ADR-0003: Layered Oracle Validation & Canonical Certified Content Tree

- **Date:** 2026-09-26
- **Status:** 🟢 Accepted
- **Decider(s):** Human Engineer & Lead Architect
- **Governance Tier:** Tier 1 (Impacted Vectors: Vector 1: Numerical Correctness, Vector 2: Reproducibility & Determinism, Vector 3: Precision & Error Tolerances, Vector 7: Public & Module Interfaces)

---

## 1. Context & Problem Statement

Accelerated compute kernels, GPU shaders, and numerical solvers frequently produce non-bit-for-bit identical outputs across different backends (CPU reference, CUDA, ROCm, Metal, WebGPU) due to floating-point reassociation, FMA contraction, fast-math compiler flags, and non-deterministic parallel reductions.

Standard boolean unit tests (`assert x == y`) fail to distinguish between:
1. Acceptable floating-point numerical differences within physical tolerance bounds (`atol`, `rtol`, $L_\infty$).
2. Genuine algorithmic bugs, physical conservation law violations, or boundary condition instabilities.
3. Silent tolerance relaxation by autonomous agents attempting to force a failing test to turn green.

Furthermore, a certificate asserting that code was validated must cryptographically bind to the *exact candidate state* that was tested, without self-inclusion loops (where generating the certificate modifies the tree and invalidates itself).

---

## 2. Authorized Decisions

### The Layered Oracle Architecture
Cadence adopts a layered dual-track validation engine (`cadence-oracle` / `/cad-oracle`):

1. **Track A (Differential Reference Testing):**
   - Compares candidate execution against a declared Golden Reference Oracle across a parameterized seed matrix.
   - Evaluates strict mathematical error bounds:
     $$|y_{\text{candidate}} - y_{\text{ref}}| \le \text{atol} + \text{rtol} \times |y_{\text{ref}}|, \quad \max_i |y_{\text{cand}, i} - y_{\text{ref}, i}| \le L_{\infty,\max}$$
   - Binds the Golden Reference provenance (git commit, version tag, or canonical content hash); candidate code is strictly forbidden from silently substituting or redefining the reference.

2. **Track B (Domain Physical Invariant Testing):**
   - Validates declared physical laws, structural conservation constraints, and numeric sanitization:
     - Energy and momentum conservation budgets ($\Delta E / E_0 \le \epsilon_{\text{energy}}$).
     - Geometric and coordinate symmetries.
     - Strict non-NaN, non-Inf, and non-denormal limits.

3. **Canonical Certified Content Tree & Temporary-Index Plumbing:**
   - To compute the canonical tree hash without self-inclusion recursion and without certifying stale commits:
     - Cadence utilizes an isolated temporary Git index file (`GIT_INDEX_FILE`).
     - Staged candidate modifications, newly added files, and deletions are loaded into the temporary index.
     - Certificate directories (`.experiments/certificates/`) and runtime trace files are explicitly excluded via identical pathspecs during both certification and subsequent verification.
     - The canonical tree SHA (`git write-tree`) is computed from this clean index, ensuring tamper-evident identity.

4. **Cryptographically Bound Validation Certificates:**
   - On successful validation, a certificate conforming to [`schemas/validation-certificate-v1.json`](../../schemas/validation-certificate-v1.json) is minted.
   - The certificate binds the Canonical Tree SHA, Golden Reference provenance, exact tolerance budget (`atol`, `rtol`, $L_\infty$), seed matrix, and environment metadata.
   - Any post-certification mutation to production code immediately changes the canonical staged tree, causing verification to fail.

5. **Protected Tolerance Governance:**
   - Relaxing numerical tolerances (`atol`, `rtol`, $L_\infty$) or widening invariant conservation budgets directly impacts Vector 1 and Vector 3, and is **strictly classified as Tier 1**.
   - Autonomous relaxation by agents is prohibited; changes require a neutral Evidence Dossier and explicit human engineer authorization.

---

## 3. Rejected Alternatives ("Why Not That?")

* **Alternative 1: Exact Bit-for-Bit Identity Testing (`candidate == reference`)**
  - *Why Considered:* Simplest possible assertion.
  - *Why Rejected:* Completely breaks on accelerated GPU backends, SIMD vectorization, and multi-threaded reductions due to valid IEEE-754 floating-point order-of-operations reassociation.
* **Alternative 2: Certifying `HEAD` Commit Tree Directly**
  - *Why Considered:* Avoids temporary git index plumbing.
  - *Why Rejected:* Certifies the previous commit rather than the actual working tree / staged candidate under test, allowing uncertified code to be staged and merged.
* **Alternative 3: Including Certificates Directly Inside the Certified Git Tree**
  - *Why Considered:* Simple single-tree storage.
  - *Why Rejected:* Creates an infinite recursive hash paradox: writing the certificate into the tree alters the tree hash, rendering the recorded tree hash invalid. Path exclusion in temporary index resolves this cleanly.

---

## 4. Conscious Trade-offs (What We Sacrificed)

- Golden Reference execution adds test runtime overhead, as both reference and candidate implementations must be computed across the seed matrix.
- Managing temporary Git index files requires running Git low-level plumbing commands (`git read-tree`, `git add`, `git write-tree`) rather than high-level porcelain.

---

## 5. Revisit Trigger (When to Change Your Mind)

Revisit this ADR if hardware vendors establish cross-vendor deterministic floating-point reduction standards with zero performance penalty across CPU and GPU hardware.

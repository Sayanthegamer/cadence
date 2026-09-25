---
name: cadence-oracle
description: >-
  Layered oracle and invariant validation engine for accelerated kernels and numerical
  algorithms. Executes differential testing against reference implementations, verifies
  domain physical invariants, computes non-circular Canonical Certified Content Trees,
  and issues cryptographically bound certificates.
---

# Cadence Oracle: Layered Numerical & Physical Validation Engine

In accelerated computing (CUDA, Vulkan, Metal, ROCm, WebGPU) and numerical simulation, standard unit tests (e.g. `assert output is not None`) are insufficient to detect floating-point divergence, race conditions, accumulation drift, or loss of physical conservation laws.

Cadence Oracle executes **Layered Synthesized Validation** combining:
1. **Track A (Differential Testing):** Evaluates candidate accelerated kernel against a Golden Reference Oracle (CPU analytical or double-precision baseline) across seeded inputs, checking `atol`, `rtol`, and $L_\infty$ norms.
2. **Track B (Domain Physical Invariants):** Asserts problem-specific mathematical invariants (energy conservation or monotonic dissipation, momentum conservation, spatial symmetries, and zero NaNs/infs).
3. **Non-Circular Canonical Tree Identity:** Computes and verifies the exact candidate content tree via isolated temporary Git index plumbing (`GIT_INDEX_FILE`), issuing a cryptographically bound certificate in `.experiments/certificates/<tree_sha>.json`.

---

## 1. The Dual-Track Validation Protocol

```mermaid
flowchart TD
    Candidate["Candidate Backend / Kernel"] --> Ingest["Ingest Contract: contracts/<module>.yaml"]
    
    subgraph TrackA ["Track A: Differential Reference Validation"]
        A1["Seeded Input Generator (Nominal & Corner Seeds)"]
        A2["Reference Oracle Run (FP64 / Analytical)"]
        A3["Candidate Kernel Run (Target Hardware)"]
        A4["Error Norm Evaluation: atol, rtol, L_inf"]
    end

    subgraph TrackB ["Track B: Domain Physical Invariants"]
        B1["Energy Monotonicity Check (Conserved or Dissipative)"]
        B2["Momentum Conservation Delta"]
        B3["Spatial Symmetries & Equivariance"]
        B4["Numerical Sanity (NaN / Inf / Subnormal Flushes)"]
    end

    Ingest --> TrackA
    Ingest --> TrackB

    TrackA --> Eval{"All Gates Passed?"}
    TrackB --> Eval

    Eval -- Yes --> Tree["Compute Canonical Certified Tree (GIT_INDEX_FILE)"]
    Eval -- No --> Lock["BLOCKED_PENDING_CERTIFICATION\n(Tolerance Relaxation is Tier 1 Gate)"]

    Tree --> Cert["Generate Certificate: .experiments/certificates/<sha>.json"]
```

### Track A: Differential Testing & Executable Acceptance Semantics
- Evaluates candidate outputs $Y_{\text{cand}}$ against reference outputs $Y_{\text{ref}}$ across a deterministic seed matrix:
  1. **Pointwise Tolerance Condition:**
     For every sample index $i$ across all trajectory steps and seeds:
     $$\text{tolerance\_bound}[i] = \text{atol} + \text{rtol} \times |Y_{\text{ref}}[i]|$$
     $$\text{is\_pointwise\_violation}[i] = \left( |Y_{\text{cand}}[i] - Y_{\text{ref}}[i]| > \text{tolerance\_bound}[i] \right)$$
     $$\text{pointwise\_violations} = \sum_{i} \mathbf{1}_{\text{is\_pointwise\_violation}[i]}$$
  2. **Uniform $L_\infty$ Error Norm Condition:**
     $$L_\infty = \max_{i} |Y_{\text{cand}}[i] - Y_{\text{ref}}[i]| \le L_{\infty, \max}$$
  3. **Strict Track A Pass Predicate:**
     $$\text{TrackA\_Verdict} = \begin{cases} \text{PASSED} & \text{if } \text{pointwise\_violations} == 0 \text{ and } L_\infty \le L_{\infty, \max} \\ \text{FAILED} & \text{otherwise} \end{cases}$$
- If *even a single sample* exceeds the pointwise bound or the uniform $L_\infty$ norm on *any* seed, Track A returns `FAILED`. No passing certificate is issued, and the `BLOCKED_PENDING_CERTIFICATION` lock remains engaged.

### Golden Reference Provenance & Anti-Substitution Binding
- Validation is performed against an authoritative, versioned Golden Reference (e.g. CPU FP64 or closed-form analytical solver).
- Candidate validation is **strictly prohibited from redefining or silently substituting the reference**:
  1. The contract declares `reference_identity` (e.g. `pendulum_analytical_fp64:v1.0.0`) and `reference_source_file`.
  2. The oracle computes `reference_source_sha256 = SHA256(reference_source_file)` and binds it permanently into the certificate.
  3. During pre-commit verification, if the reference source code has been altered or substituted, the hash check fails with `ERR_REFERENCE_PROVENANCE_MISMATCH`.

### Validation Matrix Input Binding
- To prevent certificates from being replayed under materially different conditions, the certificate binds the exact validation matrix:
  - Explicit seed list: `[42, 100, 2026]`
  - Parameter sweep space: `dt`, `steps`, `damping`, `stiffness`, mesh resolution.
  - Target backend and precision: e.g. `CUDA / FP32`.
- Any modification to the validation parameters or seeds requires a new certification run.

### Track B: Domain-Declared Physical Invariants
Evaluates trajectory invariants declared in `contracts/<module>.yaml`:
- **Energy Behavior:**
  - `CONSERVED`: $|E(t) - E(0)| / E(0) \le \epsilon_{\text{energy}}$
  - `MONOTONIC_DISSIPATIVE`: $E(t_{k+1}) \le E(t_k) + \epsilon_{\text{drift}}$ (no unphysical energy generation)
  - `UNCONSTRAINED`: For open/driven systems
- **Momentum Conservation:** Linear and angular momentum drift $\Delta P \le \epsilon_{\text{momentum}}$
- **Spatial Symmetries:** Invariance under translations and rotational equivariance where applicable
- **Numerical Sanity:** Zero NaNs, zero infinities, and zero unexpected subnormal flushes across all integration steps

---

## 2. Canonical Certified Content Tree Plumbing (`GIT_INDEX_FILE`)

### Problem Solved: Self-Inclusion Immunity & Candidate Snapshotting
A validation certificate is stored inside `.experiments/certificates/<tree_sha>.json`. If a naive git tree hash was used, adding or committing the certificate would mutate the tree hash, creating a circular invalidation loop. Furthermore, reading `HEAD` would certify past commits rather than the candidate code on disk.

Cadence Oracle resolves this by using an isolated temporary Git index to compute the **Canonical Certified Content Tree**:

```powershell
function Get-Canonical-Candidate-Tree {
    param(
        [string]$RepoRoot = (git rev-parse --show-toplevel),
        [string[]]$Exclusions = @(".experiments/certificates/**", ".experiments/traces/**")
    )
    
    $rawGitDir = (git -C $RepoRoot rev-parse --git-dir).Trim()
    $gitDir = if ([System.IO.Path]::IsPathRooted($rawGitDir)) { $rawGitDir } else { Join-Path $RepoRoot $rawGitDir }
    $primaryIndex = Join-Path $gitDir "index"
    $tempIndex = Join-Path $gitDir "cadence_cand_index_$([Guid]::NewGuid().ToString('N'))"
    $origIndexEnv = $env:GIT_INDEX_FILE
    
    try {
        # 1. Snapshot primary index baseline
        if (Test-Path $primaryIndex) {
            Copy-Item $primaryIndex $tempIndex
        } else {
            New-Item -ItemType File -Path $tempIndex | Out-Null
        }
        
        # 2. Redirect Git plumbing to isolated temporary index
        $env:GIT_INDEX_FILE = $tempIndex
        
        # 3. Synchronize candidate working-tree state into temp index:
        #    - Tracked modifications: updated
        #    - New files: added (honoring .gitignore)
        #    - Deletions: removed
        #    - Unified staged & unstaged candidate changes
        git -C $RepoRoot add -A
        
        # 4. Explicitly unstage and purge excluded certificate and trace paths
        foreach ($pattern in $Exclusions) {
            git -C $RepoRoot rm --cached -r -q --ignore-unmatch $pattern 2>$null
        }
        
        # 5. Write the canonical content tree object
        $canonicalTreeSha = git -C $RepoRoot write-tree
        return $canonicalTreeSha
    }
    finally {
        # 6. Restore original environment and delete temporary index
        $env:GIT_INDEX_FILE = $origIndexEnv
        if (Test-Path $tempIndex) { Remove-Item -Force $tempIndex }
    }
}
```

---

## 3. Pre-Commit Verification Plumbing (`Verify-Canonical-Staged-Tree`)

---

## 3. Pre-Commit Verification Plumbing (`Verify-Oracle-Certification`)

When changes are staged and `git commit` or `cadence-review` executes, verification performs comprehensive multi-vector integrity assertions:

```powershell
function Verify-Oracle-Certification {
    param(
        [string]$RepoRoot = (git rev-parse --show-toplevel),
        [string]$CertificatePath
    )
    # 1. Certificate Existence Gate
    if (-not (Test-Path $CertificatePath)) {
        throw "ERR_CERTIFICATE_NOT_FOUND: Validation certificate not found at $CertificatePath. Run /cad-oracle before committing."
    }
    
    # 2. Certificate Parse & Schema Gate
    try {
        $cert = Get-Content $CertificatePath -Raw | ConvertFrom-Json
    } catch {
        throw "ERR_CERTIFICATE_MALFORMED: Certificate is corrupted or invalid JSON."
    }
    
    # 3. Verdict Assertion
    if ($cert.verdict -ne "PASSED") {
        throw "ERR_CERTIFICATE_VERDICT_FAILED: Candidate certification verdict is '$($cert.verdict)'. Code change is rejected."
    }
    
    # 4. Contract Integrity Check (Prevents contract drift post-certification)
    $contractPath = Join-Path $RepoRoot $cert.contract_file
    if (-not (Test-Path $contractPath)) {
        throw "ERR_CONTRACT_NOT_FOUND: Referenced contract file '$($cert.contract_file)' does not exist."
    }
    $currentContractSha = (Get-FileHash -Algorithm SHA256 $contractPath).Hash.ToLower()
    if ($currentContractSha -ne $cert.contract_sha256) {
        throw "ERR_CONTRACT_HASH_MISMATCH: Contract was modified after certification. Re-run /cad-oracle to re-certify."
    }
    
    # 5. Reference Provenance Check (Prevents silent reference substitution)
    $refPath = Join-Path $RepoRoot $cert.reference_provenance.reference_source_file
    if (-not (Test-Path $refPath)) {
        throw "ERR_REFERENCE_NOT_FOUND: Referenced reference implementation '$($cert.reference_provenance.reference_source_file)' does not exist."
    }
    $currentRefSha = (Get-FileHash -Algorithm SHA256 $refPath).Hash.ToLower()
    if ($currentRefSha -ne $cert.reference_provenance.reference_source_sha256) {
        throw "ERR_REFERENCE_PROVENANCE_MISMATCH: Golden reference implementation was modified or substituted. Re-run /cad-oracle."
    }
    
    # 6. Canonical Tree Identity Assertion via Isolated Index
    $rawGitDir = (git -C $RepoRoot rev-parse --git-dir).Trim()
    $gitDir = if ([System.IO.Path]::IsPathRooted($rawGitDir)) { $rawGitDir } else { Join-Path $RepoRoot $rawGitDir }
    $primaryIndex = Join-Path $gitDir "index"
    $tempIndex = Join-Path $gitDir "cadence_verify_index_$([Guid]::NewGuid().ToString('N'))"
    $origIndexEnv = $env:GIT_INDEX_FILE
    
    try {
        Copy-Item $primaryIndex $tempIndex
        $env:GIT_INDEX_FILE = $tempIndex
        
        # Filter using the EXACT SAME exclusion pathspecs recorded in the certificate
        foreach ($pattern in $cert.exclusion_pathspecs) {
            git -C $RepoRoot rm --cached -r -q --ignore-unmatch $pattern 2>$null
        }
        
        $stagedCanonicalTreeSha = git -C $RepoRoot write-tree
        if ($stagedCanonicalTreeSha -ne $cert.canonical_tree_sha) {
            throw "ERR_TREE_MUTATED_POST_CERTIFICATION: Staged content tree ($stagedCanonicalTreeSha) does not match certified tree ($($cert.canonical_tree_sha)). Re-run /cad-oracle before committing."
        }
        return $true
    }
    finally {
        $env:GIT_INDEX_FILE = $origIndexEnv
        if (Test-Path $tempIndex) { Remove-Item -Force $tempIndex }
    }
}
```

---

## 4. Protected Tolerance Governance Gate (Anti-Loosening Hook)

> **Rule:** *Tolerance relaxation is strictly a Tier 1 decision.*  
> If candidate kernel outputs exceed `atol`, `rtol`, $L_\infty$, or invariant bounds:
> - The agent is **strictly prohibited from loosening tolerances autonomously** in `contracts/*.yaml` or test fixtures to make the test pass.
> - Modifying tolerances in a relaxing direction is an automatic **Tier 1 Foundational Decision (Vector 3: Precision or Error Tolerances)**.
> - Cadence Oracle halts execution, generates an Evidence Dossier showing the error distributions and seed discrepancies, and requires explicit human approval via `ask_question`.

---

## 5. Certificate Storage & Schema

Certificates are saved as physical JSON files in `.experiments/certificates/<canonical_tree_sha>.json` conforming to [`schemas/validation-certificate-v1.json`](../../schemas/validation-certificate-v1.json):

```json
{
  "$schema": "https://cadence.dev/schemas/validation-certificate-v1.json",
  "certificate_id": "8c78649a93a5afff375eaaac07049b56cb5081c4.json",
  "timestamp": "2026-09-26T00:25:00Z",
  "tree_spec_version": "v1",
  "canonical_tree_sha": "8c78649a93a5afff375eaaac07049b56cb5081c4",
  "inclusion_rules": ["TRACKED_AND_UNIGNORED_WORKING_TREE"],
  "exclusion_pathspecs": [".experiments/certificates/**", ".experiments/traces/**"],
  "contract_file": "contracts/jacobi_solver.yaml",
  "contract_sha256": "4b92f8a183d71e21b759685934524c53835f86b4...",
  "reference_provenance": {
    "reference_identity": "jacobi_analytical_fp64:v1.0.0",
    "reference_source_file": "src/reference/jacobi_ref.py",
    "reference_source_sha256": "a3f5b8...",
    "backend": "CPU",
    "precision": "FP64"
  },
  "validation_matrix": {
    "seeds": [42, 100, 2026],
    "parameter_space": {
      "dt": 0.01,
      "stiffness": [100.0, 1000.0, 10000.0],
      "iterations": 200
    }
  },
  "target_backend": { "backend": "CUDA", "device_name": "NVIDIA RTX 4090", "precision": "FP32" },
  "track_a_differential": {
    "status": "PASSED",
    "evaluated_seeds": [42, 100, 2026],
    "max_abs_error": 0.00014,
    "max_rel_error": 0.00008,
    "l_inf_norm": 0.00031,
    "pointwise_violations": 0,
    "tolerances": { "atol": 0.001, "rtol": 0.001, "l_inf_max": 0.005 }
  },
  "track_b_domain_invariants": {
    "status": "PASSED",
    "energy_monotonicity": { "verdict": "PASSED", "mode": "MONOTONIC_DISSIPATIVE", "max_violation": 0.0 },
    "momentum_conservation": { "verdict": "PASSED", "max_delta": 0.00002 },
    "symmetry_equivariance": { "verdict": "PASSED" },
    "nan_inf_free": { "verdict": "PASSED", "nan_count": 0, "inf_count": 0 }
  },
  "verdict": "PASSED"
}
```

---

## 6. CLI Command Integration

Execute Cadence Oracle via:
```text
/cad-oracle [contract_path]
```
If `contract_path` is omitted, Oracle automatically discovers active contracts in `contracts/*.yaml`.

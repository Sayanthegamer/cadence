# Changelog

All notable changes to Cadence are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-09-26

### 🚀 Major Architectural Evolution: Generalized Empirical TDD & Scientific Computing

Cadence 2.0 evolves classic Red-Green-Refactor TDD into a dual-track engineering system natively designed for scientific computing, physics simulations, accelerated numerical kernels (CUDA, WGSL, OpenCL, C++), and modern software engineering.

#### 🏛️ Pillar 1: Two-Tier Architectural Governance (ADR-0001)
- **8 Material Impact Vectors:** Strictly classifies architectural decisions by material impact rather than nominal classification (Numerical correctness, Reproducibility/determinism, Precision/tolerances, Performance scaling, Memory layout, Concurrency/synchronization, Public module interfaces, Algorithmic dependencies).
- **The Uncertainty Invariant:** Any ambiguity across the 8 vectors automatically defaults to Tier 1 human authorization. Autonomous bypass under uncertainty is strictly prohibited.
- **Evidence Dossiers:** Balanced, objective multi-alternative comparison dossiers compiled with zero bias, zero premature `(Recommended)` labels, and zero default pre-selection before human sign-off.
- **Permanent ADR Archival:** Formalizes accepted architectural decisions in `.agents/decisions/` with explicit revisit conditions.

#### 🧪 Pillar 2: Scientific Failure Archival (ADR-0002)
- **2A + Selective 2B Hybrid Architecture:** Clean separation of ordinary code defects (Class A, cleanly wiped) from meaningful scientific divergences and falsified physical hypotheses (Class B, formally preserved).
- **Machine-Readable Experiment Records:** Serialized in `.experiments/` adhering to `schemas/experiment-v1.json` with hypotheses, observed metrics, divergence conditions, and next steps.
- **Content-Addressed Storage (CAS SHA-256):** Anchors large non-versioned binary artifacts, simulation traces, and failure logs with cryptographic SHA-256 hashes to guarantee data immutability and tamper detection.

#### 🛡️ Pillar 3: Layered Oracle Validation & Cryptographic Certification (ADR-0003)
- **Track A Differential Testing:** Multi-seed matrix comparison against trusted CPU reference implementations under strict numerical tolerance budgets (`atol`, `rtol`, $L_\infty$).
- **Track B Physical Invariants:** Domain conservation law assertions (energy, momentum, mass, symmetry, boundary limits, and non-NaN/Inf sanity) evaluated independently of reference approximations.
- **Canonical Certified Content Tree:** Deterministically computes SHA-1 content trees across tracked project sources using isolated temporary Git index plumbing (`GIT_INDEX_FILE`), providing absolute self-inclusion immunity and post-certification mutation detection.
- **Validation Certificates:** Machine-readable certificates (`schemas/validation-certificate-v1.json`) binding code states, reference provenance, and invariant telemetry.

#### ⚡ Pillar 4: Adaptive Two-Tier Statistical Benchmarking (ADR-0004)
- **Fast Tier Screening:** Micro-benchmarking path with $\le 3\text{s}$ wall-clock budget for $\pm 25.000\%$ gross-change detection with decoupled signed direction (`SPEEDUP`, `REGRESSION`, `NEUTRAL`). Fast Tier explicitly disclaims optimization or regression certification.
- **Deep Tier Statistical Profiling:**
  - Moving-block bootstrap (Politis & Romano) with Hyndman & Fan Type-7 quantile estimation across $B=1,000$ resamples.
  - Relative Confidence Interval Width (RCIW) adaptive stopping: normal policy $\text{CI}_{\text{width}} / |\Delta|$ and near-zero policy $(\text{CI}_{\text{width}} / 2) / \text{MAES}$ when $|\Delta| \le \text{MAES}$.
  - Timing contracts: strict minimum observation window ($t \ge T_{\min} = 10.0\text{s}$) to observe thermal and scheduler variance, and iteration-boundary budget ceiling ($T_{\max} = 45.0\text{s}$) with bounded single-sample overshoot ($\le \Delta t_{\text{sample}}$).
  - 5-step mutually exclusive precedence ladder evaluated against Minimum Actionable Effect Size (MAES).
- **Capacity Envelope Isolation:** Multi-point workload sweeps identifying largest successful tested size, physical limits, and failure categories (`CAPACITY_LIMIT_OOM`, `DEVICE_LOST`, `TIMEOUT`, `WORKER_CRASH`) strictly segregated from latency statistics.
- **Cross-Platform Process Watchdog:** Universal process tree termination supporting Windows (`taskkill.exe /F /T /PID`) and POSIX (`os.killpg(os.getpgid(pid), signal.SIGKILL)`), eliminating orphaned workers.

#### ⚙️ Dual-Layer Architecture: Protocol & Executable Verification CLIs
- Decoupled LLM reasoning protocols from deterministic verification harnesses.
- Added platform-agnostic CLI utilities:
  - `scripts/bench_engine.py`: Standalone CLI for Fast Tier screening, Deep Tier profiling, and workload sweeps.
  - `scripts/verify_oracle.py` / `scripts/oracle_verify.py`: Standalone CLI for canonical tree computation and oracle certificate verification.
  - `scripts/verify_archival.py` / `scripts/archival_verify.py`: Standalone CLI for experiment schema and CAS SHA-256 integrity verification.
  - `scripts/pre-commit-hook.sh`: Universal Git pre-commit hook enforcing validation in local Git and CI/CD pipelines.

#### 🧪 Reproducible Test Suites & Dependency Manifests
- Added full in-repo test suites in `tests/`:
  - `tests/test_bench_engine.py`: 12 acceptance tests covering quantiles, bootstrap, RCIW, boundaries, process isolation, capacity limits, and timing contracts.
  - `tests/test_timing_contracts.py`: Validates Fast Tier wall-clock path and Deep Tier $T_{\min}/T_{\max}$ timing budget contracts.
  - `tests/test_master_integration.py`: End-to-end multi-pillar regression suite and simulated workflow walkthrough.
- Added `requirements.txt` declaring `jsonschema>=4.0.0` with friendly import guards in all test suites.
- Fixed POSIX zombie process liveness detection in test harnesses (`proc_tree.wait()` and `/proc/<pid>/status` state checks).

#### 📚 Documentation & Manuals
- Overhauled `README.md` to articulate the Dual-Track TDD architecture, reduce promotional rhetoric, and add architecture diagrams.
- Replaced 100% of absolute file URI schemes with cross-platform relative links across all documentation, skill manuals, and ADRs.
- Synchronized ADR-0001, ADR-0002, ADR-0003, and ADR-0004 with exact ratified contracts.

---

## [1.0.0] - 2026-09-25

### Initial Release
- High-velocity Spec & Red-Green-Refactor TDD workflow natively for Antigravity 2.0.
- 15 skills, 7 specialized subagents, and 13 slash commands.
- Native UI Artifacts (`brain/`) for zero Git repository pollution.
- Context-7 MCP integration for live documentation and code grounding.

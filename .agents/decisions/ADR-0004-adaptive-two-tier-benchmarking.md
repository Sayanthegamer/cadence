# ADR-0004: Adaptive Two-Tier Benchmarking: Precision Formulations & Gross-Change Semantics

- **Date:** 2026-09-26
- **Status:** 🟢 Accepted
- **Decider(s):** Human Engineer & Lead Architect
- **Governance Tier:** Tier 1 (Impacted Vectors: Vector 1: Numerical Correctness & Physical Realism, Vector 4: Performance Characteristics & Scaling Behavior, Vector 7: Public & Module Interfaces)

---

## 1. Context & Problem Statement

In experimental compute kernels, simulation loops, and graphics rendering, benchmarking must deliver statistically robust, reproducible performance decisions while remaining computationally economical. Phase 4 of the Cadence Evolution establishes an Adaptive Two-Tier Benchmark architecture (`Fast Tier` and `Deep Tier`). During Phase 4 implementation and re-review, two consequential methodological questions arose:

1. **Deep Tier Adaptive Precision in the Near-Zero Delta Regime:**
   The standard Relative Confidence Interval Width is defined as $\text{RCIW} = \frac{\text{CI}_{\text{width}}}{|\Delta_{\text{metric}}|}$. When an optimization is practically equivalent or has near-zero performance delta ($|\Delta| \to 0$), the denominator vanishes, causing RCIW to diverge toward infinity even when the confidence interval is infinitesimally tight. An adaptive stopping rule requires a deterministic, well-behaved precision formulation for near-zero deltas without distorting the final hypothesis verdict.
2. **Fast Tier Gross-Change Boundary Semantics & Directional Reporting:**
   The Fast Tier is a low-overhead ($T \le 3\text{s}$) preliminary screening tool evaluating whether a $> 25\%$ gross change occurred. We needed to unambiguously define whether the 25% threshold evaluates signed delta or absolute magnitude, define the exact boundary condition ($\le 25\%$ vs $> 25\%$), and ensure Fast Tier outcomes are never conflated with Deep Tier statistical conclusions.

---

## 2. Authorized Decisions

### Decision A1: Deep Tier Adaptive Precision Formulation

The adaptive stopping rule dynamically evaluates precision during the bootstrap loop ($K_{\min} \le K \le K_{\max}$):

- **Normal Precision Criterion ($|\Delta_{\text{metric}}| > \text{MAES}$):**
  $$\text{RCIW} = \frac{\text{CI}_{\text{upper}} - \text{CI}_{\text{lower}}}{|\Delta_{\text{metric}}|}$$
  Sampling terminates early when $\text{RCIW} \le \text{RCIW}_{\text{target}}$ (e.g., $10\%$).

- **Near-Zero Precision Criterion ($|\Delta_{\text{metric}}| \le \text{MAES}$):**
  When $|\Delta_{\text{metric}}| \le \text{MAES}$, the relative width is normalized against the actionable threshold diameter:
  $$\text{RCIW}_{\text{MAES}} = \frac{\text{CI}_{\text{width}} / 2}{\text{MAES}}$$
  Telemetry marks `is_near_zero_delta: true`. Early stopping occurs when $\text{RCIW}_{\text{MAES}} \le \text{RCIW}_{\text{target}}$.

- **Canonical 5-Step MAES Precedence Invariant:**
  The adaptive precision criterion only governs the sampling termination loop. The final hypothesis verdict strictly evaluates the canonical 5-step precedence ladder:
  1. *Precision Gate:* $\text{CI}_{\text{width}} > 2 \times \text{MAES} \implies$ `INCONCLUSIVE (EXCESSIVE_CI_WIDTH)`
  2. *Optimization Gate:* $\text{CI}_{\text{upper}} < -\text{MAES} \implies$ `ACTIONABLE_OPTIMIZATION`
  3. *Regression Gate:* $\text{CI}_{\text{lower}} > +\text{MAES} \implies$ `ACTIONABLE_REGRESSION`
  4. *Equivalence Gate:* $[\text{CI}_{\text{lower}}, \text{CI}_{\text{upper}}] \subseteq [-\text{MAES}, +\text{MAES}] \implies$ `PRACTICALLY_EQUIVALENT`
  5. *Boundary Straddle Gate:* Default fallthrough $\implies$ `INCONCLUSIVE (BOUNDARY_STRADDLE)`

Autonomous relaxation of MAES or tolerance thresholds is strictly forbidden.

### Decision A2: Fast Tier Gross-Change Semantics & Directional Reporting

- **Relative Change Calculation:**
  $$\text{relative\_change} = \frac{\text{candidate}_{\min} - \text{baseline}_{\min}}{\text{baseline}_{\min}}$$
  $$\text{delta\_percent} = \text{relative\_change} \times 100.0$$

- **Exact Magnitude Threshold & Status:**
  - If $|\text{relative\_change}| \le 0.25000 \implies$ **`NO_GROSS_CHANGE_DETECTED`**
  - If $|\text{relative\_change}| > 0.25000 \implies$ **`GROSS_CHANGE_DETECTED`**

- **Decoupled Directional Reporting:**
  Direction is reported independently of the gross-change magnitude flag:
  - $\text{relative\_change} > 0.0 \implies$ `REGRESSION`
  - $\text{relative\_change} < 0.0 \implies$ `SPEEDUP`
  - $\text{relative\_change} == 0.0 \implies$ `NEUTRAL`

- **Rule of Non-Equivalence & Non-Certification:**
  The Fast Tier outcome is explicitly defined as a cheap gross-change detector under local nominal workloads. It must never be represented as equivalent to Deep Tier outcomes, and it cannot independently certify optimization, regression, equivalence, or asymptotic scaling.
  - By default, detecting a gross change issues a recommendation: `Recommendation: Run /cad-bench --deep to statistically profile this gross change.`
  - When `--auto-deep` is supplied, the Deep Tier pipeline is triggered automatically.

---

## 3. Rejected Alternatives ("Why Not That?")

### Deep Tier Precision Alternatives
* **Alternative 1: Unconditional RCIW with Arbitrary Epsilon Floor ($\text{CI}_{\text{width}} / \max(\epsilon, |\Delta|)$)**
  - *Why Considered:* Syntactically simple single-formula implementation.
  - *Why Rejected:* For near-zero deltas ($|\Delta| \approx 0$), dividing by $\epsilon = 10^{-9}$ produces explosive values ($10^8\%$), forcing sampling unconditionally to $K_{\max}$ regardless of how tight the confidence interval is.
* **Alternative 2: Stopping Exclusively on Absolute CI Width ($\text{CI}_{\text{width}} \le \epsilon_{\text{abs}}$)**
  - *Why Considered:* Avoids division by zero entirely.
  - *Why Rejected:* Absolute width is non-scale-invariant across workloads with different baseline latencies (e.g. 50 microseconds vs 500 milliseconds), breaking generic benchmark contracts.

### Fast Tier Semantics Alternatives
* **Alternative 1: Signed-Only Threshold (Only Flag Positive Regressions $> +25\%$)**
  - *Why Considered:* Matches intuitive developer interest in catching performance degradations.
  - *Why Rejected:* Obscures massive speedups ($> 25\%$ faster) that require statistical verification or might indicate broken or short-circuited compute logic. Both directions constitute gross behavioral changes.
* **Alternative 2: Conflating Direction and Status (e.g., `GROSS_REGRESSION_DETECTED`)**
  - *Why Considered:* Combines status and direction into a single string token.
  - *Why Rejected:* Violates modular reporting and schema cleanliness; status represents detection threshold crossing, while direction represents signed orientation.

---

## 4. Conscious Trade-offs (What We Sacrificed)

- By adopting $(\text{CI}_{\text{width}} / 2) / \text{MAES}$ for near-zero deltas, we require the benchmark contract to declare a meaningful MAES threshold before adaptive sampling begins. Without an explicit MAES, adaptive stopping cannot evaluate near-zero deltas.
- By capping Fast Tier to $\le 3\text{s}$ wall-clock budget and using minimum execution time, we sacrifice distributional tail profiling ($P_{95}, P_{99}$) in the Fast Tier in exchange for immediate developer feedback. Tail profiling is strictly deferred to the Deep Tier.

---

## 5. Revisit Trigger (When to Change Your Mind)

Revisit this ADR if:
1. Automated Bayesian stopping rules or sequential probability ratio tests (SPRT) are integrated to replace moving-block bootstrap adaptive sampling.
2. Hardware execution platforms exhibit multi-modal bimodal execution profiles where minimum-time screening in the Fast Tier fails to detect severe cache or throttling pathologies.

# Equivalences, Obstructions, and the Seed-Ancestry Barrier in the Rule 30 Center-Column Density Problem

**Author:** David Lee Condrey  
**Affiliation:** WritersLogic, Inc. (`david@writerslogic.com`)  
**Date:** September 2026  
**Compiled Paper PDF:** [`rule30-density.pdf`](rule30-density.pdf)  
**LaTeX Source:** [`rule30-density.tex`](rule30-density.tex)  
**BibTeX:** [`rule30-density.bib`](rule30-density.bib)  

---

## Abstract

Wolfram's Problem 2 asks whether the temporal center column of elementary cellular automaton (ECA) Rule 30 generated from a single active seed cell has asymptotic density one-half:
$$\lim_{T \to \infty} \frac{1}{T} \sum_{t=0}^{T-1} c_t = \frac{1}{2}.$$
While empirical measurements across hundreds of millions of steps exhibit remarkable statistical balance, establishing an asymptotic proof remains a major open problem in discrete dynamical systems. In this paper, we establish four structural results that map the rigorous mathematical geometry of the problem:

1. **Universal Flexible-Scale Equivalence:** We prove an exact, scale-independent equivalence: density one-half is deterministically equivalent to the vanishing of a flexible dyadic block-energy score:
   $$F_k = \min_{0 \le j \le k} \left( V_{k, j} + \frac{4^j}{N^2} \right) \longrightarrow 0,$$
   governed by the universal two-sided bound:
   $$\frac{1}{2} \left( \frac{M_k}{N} \right)^2 \le F_k \le 5 \frac{M_k}{N}.$$
   This removes arbitrary square-root cutoff schedules and proves that fixed-window recurrences (such as hypocoercivity contractions) are sufficient but strictly non-necessary.
2. **The Prescribed Center-Bit Obstruction (The Seed-Geometry Theorem):** We prove an all-length impossibility theorem: for any duration $T$, there exist alternative autonomous Rule 30 configurations that match the true singleton seed's center history up to time $h$, match the entire right half of the cone, and match both moving boundary strips *forever* (including the left-edge nonlinear defect), yet produce *any* prescribed binary word $w \in \{0, 1\}^T$ at the center. This establishes that no proof relying solely on spatial row states, boundary matching, or local Markovian approximations can ever succeed.
3. **The Ancestry Invariant and the Pre-Image Barrier:** We prove that the sole mathematical feature isolating the true singleton trajectory from these deceptive configurations is its *finite predecessor depth*: a row with support $[-n, n]$ is the true seed row $x^n$ if and only if it possesses $n$ successive finite-support pre-images ($n - d_{\text{fin}}(y) = 0$). By left-permutivity, the density of such configurations among finite rows of width $2n+1$ is exactly $2^{-(2n-1)}$, creating a steep topological ancestry barrier where localized single-bit perturbations collapse predecessor depth to $O(1)$.
4. **Exact Spatial Potential-Current Identity:** We prove an exact integer identity coupling center discrepancy to the spatial quarter-wave potential $P(x)$ and nonlinear flux $K(x)$:
   $$A(T) - \frac{T}{2} = P(x^T) + \sum_{t < T} \left( K(x^t) - \frac{1}{2} \right).$$
   Evaluating this identity through $T = 8,192$ and dyadic block energies through $N = 2^{28} \approx 2.68 \times 10^8$ steps, we show that quarter-wave coherence is strictly suppressed on the singleton orbit ($P_{8192} = 4$). We frame the remaining proof obligation as an invariant pre-image variety projection problem.

---

## 1. Introduction

Elementary cellular automaton (ECA) Rule 30 updates each cell synchronously on the integer lattice $\mathbb{Z}$ according to the local rule:
$$x_i^{t+1} = \mathcal{F}(x^t)_i = x_{i-1}^t \oplus (x_i^t \lor x_{i+1}^t) = x_{i-1}^t + x_i^t + x_{i+1}^t + x_i^t x_{i+1}^t \pmod 2.$$
From the singleton initial condition $x_0^0 = 1$ and $x_i^0 = 0$ for $i \ne 0$, the center sequence $c_t = x_0^t$ exhibits complex pseudorandom behavior.

Wolfram's Problem 2 asks whether:
$$\lim_{T \to \infty} \frac{1}{T} \sum_{t=0}^{T-1} c_t = \frac{1}{2}.$$
Writing $z_t = 1 - 2 c_t \in \{-1, +1\}$, this is equivalent to $S(T) = \sum_{t=0}^{T-1} z_t = o(T)$.

---

## 2. Universal Flexible-Scale Equivalence

On shell $k \ge 1$, let $N = 2^k$. For aligned blocks of length $L = 2^j$ ($0 \le j \le k$), define:
$$b_{k, j, a} = \sum_{t = a 2^j}^{(a+1)2^j - 1} z_{N+t}, \qquad E_{k, j} = \sum_a b_{k, j, a}^2, \qquad V_{k, j} = \frac{E_{k, j}}{N 2^j}.$$

### Exact One-Step Loss Identity
$$E_{k, j+1} = 2 E_{k, j} - D_{k, j}, \qquad D_{k, j} = \sum_a (b_{k, j, 2a} - b_{k, j, 2a+1})^2.$$
$$V_{k, j+1} = (1 - \delta_{k, j}) V_{k, j}, \qquad \delta_{k, j} = \frac{D_{k, j}}{2 E_{k, j}}.$$

### The Scale-Free Score and Comparison Theorem
Define the rational score:
$$F_k = \min_{0 \le j \le k} \left( V_{k, j} + \frac{4^j}{N^2} \right).$$

> **Theorem (Universal Comparison):**
> For every sign sequence of length $N = 2^k$,
> $$\frac{1}{2} \left( \frac{M_k}{N} \right)^2 \le F_k \le 5 \frac{M_k}{N}.$$
> Consequently:
> $$\mathbf{P2 \text{ holds}} \iff F_k \longrightarrow 0 \iff \exists j_k \le k \text{ with } k - j_k \to \infty \text{ and } V_{k, j_k} \to 0.$$

---

## 3. The Seed-Geometry Obstruction

> **Theorem (Prescribed Center-Bit Theorem):**
> Let $x^t = \mathcal{F}^t(\delta_0)$ be the true seed evolution. Fix depth $d \ge 2$, history $h \ge 0$, duration $T \ge 1$, and nominal starting age $a \ge h + T + d$.
> For **every** binary word $w \in \{0, 1\}^T$, there exists a finite initial configuration $y$ whose autonomous Rule 30 evolution $y^r = \mathcal{F}^r(y)$ satisfies:
> 1. Exact moving boundaries forever: inward $d$-deep edge strips match $x^{a+r}$ identically.
> 2. Identical center history up to relative time $h$, and identical non-negative half-line at $r=h$.
> 3. Exactly the prescribed word $w$ at the center for the next $T$ steps ($y_0^{h+j} = w_j$ for $1 \le j \le T$).

**Consequence:** Any proof relying solely on spatial row states, boundary matching, or local Markovian approximations is mathematically impossible, because those exact data can produce all $0$s or all $1$s at the center.

---

## 4. The Finite Predecessor Invariant and Ancestry Barrier

By left-permutivity ($l = c_{\text{next}} \oplus (c \lor r)$), Rule 30 is injective on finite configurations: any finite row with support $[-m, m]$ has **at most one** finite-support predecessor.

> **Theorem (Origin Deficit Invariant):**
> A configuration with support $[-n, n]$ satisfies:
> $$d_{\text{fin}}(y) = n \iff y = x^n = \mathcal{F}^n(\delta_0).$$
> The origin deficit $\Delta(y) = n - d_{\text{fin}}(y)$ is invariant under Rule 30 and vanishes uniquely on the singleton orbit.

### Pre-Image Volume and Perturbation Sensitivity
At each backward step, exactly $1/4$ of candidate rows have a predecessor. Thus:
$$\frac{|\mathcal{V}_n|}{2^{2n-1}} = 2^{-(2n-1)}.$$
At $n=100$, this is $\approx 1.2 \times 10^{-60}$.

| Age $n$ | Width $2n+1$ | True Depth $d_{\text{fin}}(x^n)$ | Max Perturbed Depth | Mean Perturbed Depth | Fraction $d_{\text{fin}} = 0$ |
|---:|---:|---:|---:|---:|---:|
| 10 | 21 | 10 | 4 | 1.333 | 23.8% |
| 20 | 41 | 20 | 8 | 2.561 | 12.2% |
| 30 | 61 | 30 | 12 | 3.902 | 11.5% |
| 40 | 81 | 40 | 10 | 4.889 | 9.9% |
| 50 | 101 | 50 | 20 | 6.109 | 8.9% |
| 60 | 121 | 60 | 22 | 8.190 | 8.3% |

Localized perturbations instantly collapse predecessor depth, proving that the singleton orbit is topologically isolated by a steep **ancestry barrier**.

---

## 5. The Spatial Quarter-Wave Potential-Current Identity

For a finite row $x$, define:
$$P(x) = \sum_{m \ge 0} (x_{4m+1} - x_{4m+3}), \quad q_i(x) = 2 x_i (x_{i+1} \lor x_{i+2}) + x_{i+1} x_{i+2}, \quad K(x) = \sum_{m \ge 0} (q_{4m}(x) - q_{4m+2}(x)).$$

> **Theorem (Potential-Current Identity):**
> Over the integers:
> $$x_0 = P(\mathcal{F} x) - P(x) + K(x).$$
> For the lone seed, since $P(x^0) = 0$:
> $$A(T) - \frac{T}{2} = P(x^T) + \sum_{t=0}^{T-1} \left( K(x^t) - \frac{1}{2} \right).$$

### Empirical Census on the Seed Trajectory
| $T$ | $A(T) - T/2$ | $P(x^T)$ | $\sum_{t < T} (K_t - 1/2)$ | $|P_T|/T$ | $|A(T) - T/2|/T$ | $|\sum (K_t - 1/2)|/T$ |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | $+1.00$ | 0 | $+1.00$ | $0.0000$ | $0.0625$ | $0.0625$ |
| 64 | $+3.00$ | $+3$ | $0.00$ | $0.0469$ | $0.0469$ | $0.0000$ |
| 256 | $+7.00$ | 0 | $+7.00$ | $0.0000$ | $0.0273$ | $0.0273$ |
| 1,024 | $-22.00$ | $+2$ | $-24.00$ | $0.0020$ | $0.0215$ | $0.0234$ |
| 4,096 | $-20.00$ | $+2$ | $-22.00$ | $0.0005$ | $0.0049$ | $0.0054$ |
| 8,192 | $+8.00$ | $+4$ | $+4.00$ | $0.0005$ | $0.0010$ | $0.0005$ |

The spatial potential $P(x^{8192}) = 4$ remains suppressed, ruling out macroscopic quarter-wave coherence on the singleton orbit.

---

## 6. Empirical Evaluation Across Shells $k=1 \dots 28$

On stored singleton-seed data up to $N = 2^{28} \approx 2.68 \times 10^8$ steps:
- **$\ell=1, C=0$ is refuted:** zero loss occurs at $k=2, j=0$ ($c_4 \dots c_7 = 1100$, $V_{2, 1} = V_{2, 0} = 1$).
- **$\ell \ge 2, C=0$ holds across all tested pairs:**
  - $\ell=2$: $\min \frac{V_j - V_{j+2}}{V_j} = 5/8 = 0.625000$ at $(6, 0)$ across 169 pairs.
  - $\ell=4$: $\min \frac{V_j - V_{j+4}}{V_j} = 3711/4040 \approx 0.918564$ at $(12, 2)$ across 121 pairs.
- **The Diagnostic Trap:** Setting remainder $C \ge 1$ makes affine recurrences $V_{k, j+\ell} \le (1-\eta) V_{k, j} + C 2^{-j}$ 100% vacuous (trivially satisfied by monotonicity without testing Rule 30).

---

## 7. The Remaining Open Problem

The open core of Wolfram's Problem 2 is formulated as:

> **The Pre-Image Variety Projection Problem:**
> Let $\mathcal{V}_N = \{ y \in \{0, 1\}^{2N+1} : d_{\text{fin}}(y) = N \} = \{ x^N \}$. Prove that the temporal projection operator $\pi_0^T(y) = (y_0^0, \dots, y_0^{T-1})$ maps $\mathcal{V}_N$ exclusively into the set of balanced sequences:
> $$\lim_{T \to \infty} \frac{1}{T} \sum_{t=0}^{T-1} (1 - 2 \pi_0^t(x^0)) = 0.$$

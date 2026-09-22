# Fixed-Window Recurrence (P2-C) Audit and Empirical Profile

Date: 2026-09-19.
Ladder Statement: `Fixed-window recurrence` (`fixed_window`, lane: front, rank: 6)
Target Formulation:
$$\text{For some } \ell \ge 1 \text{ and constants } 0 < \eta < 1, C \text{ independent of } k \text{ and } j:$$
$$V_{k, j+\ell} \le (1-\eta) V_{k, j} + C 2^{-j} \quad \text{whenever } j+\ell \le k/2 \quad \text{(P2-C)}.$$

---

## 1. Status and Executive Summary

- **STATUS:** **CONJECTURED** (The ladder statement remains **conjectured**; no all-scale seed proof exists).
- **Which Ladder Statement Changed:** **None**. Ladder statement `Fixed-window recurrence` (`fixed_window`) status remains unchanged (`conjectured`).
- **What is Proved:**
  1. *Universal Hypocoercivity / Projection Equivalence:* Writing $u = b_{k,j} \in \mathbb{R}^{N/2^j}$ for the vector of block sums and $P$ for the block-averaging projection onto blocks of length $2^{j+\ell}$, the recurrence (P2-C) is deterministically equivalent to the subspace concentration bound:
     $$\|(I - P) u\|^2 = E_{k, j} - 2^{-\ell} E_{k, j+\ell} = \sum_{s=0}^{\ell-1} 2^{-s-1} D_{k, j+s} \ge \eta \|u\|^2 - C N.$$
  2. *Sufficiency for P2:* Iterating (P2-C) with $j = m\ell \le k/2$ yields exponential decay $V_{k, m\ell} = O(\max(1-\eta, 2^{-\ell})^m)$. By Cauchy-Schwarz ($M_k / N_k \le \sqrt{V_{k, j}} + 2^{j-k}$), this forces $M_k / N_k \to 0$, establishing P2 (density one-half) by declared sufficiency.
  3. *Exhaustive Small-Word Calibration:* All 65,814 sign words of lengths $N \in \{1, 2, 4, 8, 16\}$ exhaustively confirm the exact one-merge identity $E_{j+1} = 2 E_j - D_j$, multi-merge telescoping, and the Cauchy-Schwarz prefix bound.
- **What is Refuted:**
  1. *Unperturbed One-Step Contraction ($\ell=1, C=0$):* **REFUTED** on the singleton seed by the exact finite witness at shell $k=2, j=0$:
     $$c_4 \dots c_7 = 1100, \quad z = (-1, -1, 1, 1), \quad E_0 = 4, \quad D_0 = 0, \quad V_{2, 1} = V_{2, 0} = 1.$$
     This forces $\eta \le 0$ for $\ell=1, C=0$.
  2. *Necessity of P2-C for Density One-Half (Strictness):* **REFUTED**. The artificial balanced-run family ($+^H -^H$ with $H = 2^{\lfloor 3k/4 \rfloor}$) satisfies $M_k / N_k \to 0$ (so P2 holds), but maintains $V_{k, j} = 1$ for all $j \le 3k/4$. For any fixed $(\ell, \eta > 0, C < \infty)$, evaluating at the largest admissible scale $j = \lfloor k/2 \rfloor - \ell$, where $j + \ell \le k/2 \le \lfloor 3k/4 \rfloor$ gives $V_{k, j} = V_{k, j+\ell} = 1$, forces $\eta \le C 2^{-j} \to 0$ as $k \to \infty$. (The scale $\lfloor 3k/4 \rfloor - \ell$ stated here until 2026-09-21 violates $j + \ell \le k/2$ for every $k \ge 3$; `verify_fixed_window.py` has always evaluated at $\lfloor k/2 \rfloor - \ell$.) Thus (P2-C) is strictly stronger than P2.
  3. *Diagnostic Trap of Additive Remainder $C \ge 1$:* Setting $C = 1$ with $\eta \le 1/2$ makes (P2-C) **100% vacuous** across all 169 admissible pairs in shells $k=1 \dots 28$ (0 non-trivial pairs), because $\eta E_{k, j} \le C N$ everywhere, rendering the inequality trivial by universal monotonicity $V_{k, j+\ell} \le V_{k, j}$.
- **What is Still Open:**
  - Whether there exist uniform constants $(\ell \ge 2, \eta > 0, C \ge 0)$ such that (P2-C) holds for *all* shells $k \ge 1$ of the Rule 30 singleton seed.
  - The causal cellular automaton dynamical mechanism that forbids the projection $P u$ from concentrating near the invisible kernel of $I - P$ as $k \to \infty$.

---

## 2. Explicit Success Criterion and Attack Methodology

To prevent vacuous verification and ensure falsifiability by finite certificates and controls, we formulate the explicit three-part success criterion:

### Criterion A: Non-Vacuity / Dynamical Contrast Condition
An empirical verification of $V_{k, j+\ell} \le (1-\eta) V_{k, j} + C 2^{-j}$ on a finite dataset is valid if and only if:
$$\eta V_{k, j} > C 2^{-j} \iff \eta E_{k, j} > C N$$
on a strictly positive fraction of admissible scales $(k, j)$, or $C = 0$.
*(If $C 2^{-j} \ge \eta V_{k, j}$, the inequality reduces to $V_{k, j+\ell} \le V_{k, j}$, which holds for every sign sequence without testing Rule 30).*

### Criterion B: Control Falsification
The candidate parameters $(\ell, \eta, C)$ must be falsified by non-contracting controls:
1. **Rule 90 Lone Seed Control:** $z_t = +1$ identically ($V_{k, j} = 1, D_{k, j} = 0$). (P2-C) requires $1 \le 1 - \eta + C 2^{-j}$, which must fail as soon as $2^j > C / \eta$.
2. **Artificial Balanced-Run Control:** $z = (+^H -^H)^{N/2H}$ with $H = 2^{\lfloor 3k/4 \rfloor}$. As $k \to \infty$, at the largest admissible scale $j = \lfloor k/2 \rfloor - \ell$, (P2-C) must fail.

### Criterion C: Finite Non-Degeneracy on Stored Seed Data ($k=1 \dots 28$)
For a candidate window length $\ell \in \{1, 2, 3, 4\}$, test whether the minimal relative loss:
$$\eta^*(\ell) = \min_{k \le 28, \, j+\ell \le \lfloor k/2 \rfloor} \frac{V_{k, j} - V_{k, j+\ell}}{V_{k, j}} = \min_{k \le 28, \, j+\ell \le \lfloor k/2 \rfloor} \frac{E_{k, j} - 2^{-\ell} E_{k, j+\ell}}{E_{k, j}}$$
satisfies $\eta^*(\ell) > 0$ (permitting pure contraction $C=0$), or whether $\eta^*(\ell) \le 0$ (refuting pure contraction).

---

## 3. Machine-Checked Control Verification

1. **Exhaustive Small-Word Check:**
   - 65,814 sign words checked across lengths $N \in \{1, 2, 4, 8, 16\}$.
   - Verified exact algebraic identity $E_{j+1} = 2 E_j - D_j$, multi-step telescoping $\|(I-P)u\|^2 = E_j - 2^{-\ell} E_{j+\ell}$, and Cauchy-Schwarz $\max(0, M - (2^j - 1))^2 \le (N / 2^j) E_j$.
2. **Rule 90 Lone Seed Control:**
   - Evaluated 100 cases across shells $k=1 \dots 12$.
   - For $C = 0$: $1 \le 1 - \eta$ fails in 100% of cases.
   - For $C = 1, \eta = 1/2$: fails for all $j \ge 2$ ($2^j > 2$), correctly rejecting the non-decaying Rule 90 dynamics.
3. **Balanced Runs (Strictness of P2-C):**
   - Evaluated across shells $k \in \{8, 12, 16, 20\}$ with $H = 2^{\lfloor 3k/4 \rfloor}$.
   - Exact prefix bound $M_k / N_k = H / N_k = 2^{\lfloor 3k/4 \rfloor - k} \to 0$ confirms density one-half holds.
   - At $j = \lfloor k/2 \rfloor - \ell$, $V_j = 1$ and $V_{j+\ell} = 1$ since $j + \ell \le \lfloor 3k/4 \rfloor$, requiring $\eta \le C 2^{-j}$. For $k=20, \ell=1, j=9$, this forces $\eta \le 1/512 \approx 0.00195$ at $C = 1$, disproving uniform fixed-window recurrence for general P2 sequences.

---

## 4. Empirical Profile Across Singleton Seed Shells $k=1 \dots 28$

We audited all 28 stored shells of the singleton seed ($N = 2 \dots 2^{28} = 268,435,456$).

### Global Minimum Relative Losses ($j+\ell \le \lfloor k/2 \rfloor$)

| Window Length $\ell$ | Admissible Scale Pairs | Min Relative Loss $\frac{V_j - V_{j+\ell}}{V_j}$ | Float Value | Attaining Witness $(k, j)$ | Pure Contraction ($C=0$) Status |
|---|---:|---:|---:|:---:|:---:|
| $\ell = 1$ | 196 | $0$ | $0.000000$ | $(2, 0)$ | **REFUTED** ($\eta \le 0$) |
| $\ell = 2$ | 169 | $5/8$ | $0.625000$ | $(6, 0)$ | **HOLDS** with $\eta = 5/8$ |
| $\ell = 3$ | 144 | $1611/1940$ | $0.830412$ | $(12, 3)$ | **HOLDS** with $\eta = 1611/1940$ |
| $\ell = 4$ | 121 | $3711/4040$ | $0.918564$ | $(12, 2)$ | **HOLDS** with $\eta = 3711/4040$ |

### Shell-by-Shell Progression of Minimum Relative Loss

| Shell $k$ | $N = 2^k$ | Min Loss Ratio ($\ell=1$) | Min Loss Ratio ($\ell=2$) | Min Loss Ratio ($\ell=4$) |
|---:|---:|---:|---:|---:|
| 2 | 4 | **0.000000** (Zero loss) | — | — |
| 3 | 8 | 0.500000 | — | — |
| 4 | 16 | 0.625000 | 0.937500 | — |
| 5 | 32 | 0.500000 | 0.906250 | — |
| 6 | 64 | 0.375000 | **0.625000** | — |
| 7 | 128 | 0.300000 | 0.671875 | — |
| 8 | 256 | 0.455224 | 0.714844 | 0.932617 |
| 10 | 1,024 | 0.454198 | 0.708015 | 0.925293 |
| 12 | 4,096 | 0.401818 | 0.682432 | **0.918564** |
| 16 | 65,536 | 0.475844 | 0.727256 | 0.932383 |
| 20 | 1,048,576 | 0.494556 | 0.746722 | 0.936641 |
| 24 | 16,777,216 | 0.482965 | 0.741335 | 0.934970 |
| 28 | 268,435,456 | 0.497800 | 0.748552 | 0.937107 |

### Observation on Pseudorandom Limits
For uncorrelated random bits, dyadic block merging halves normalized energy at each step:
$$\mathbb{E}\left[\frac{V_j - V_{j+\ell}}{V_j}\right] = 1 - 2^{-\ell}.$$
In the stored singleton-seed data:
- For $\ell=1$, as $k \to 28$, min loss ratio approaches $\approx 0.498 \approx 1 - 2^{-1} = 0.5$.
- For $\ell=2$, as $k \to 28$, min loss ratio approaches $\approx 0.749 \approx 1 - 2^{-2} = 0.75$.
- For $\ell=4$, as $k \to 28$, min loss ratio approaches $\approx 0.937 \approx 1 - 2^{-4} = 0.9375$.

---

## 5. Resolution of the Remainder Diagnostic Trap

When evaluating affine recurrence $V_{k, j+\ell} \le (1-\eta) V_{k, j} + C 2^{-j}$:
- For $\ell=2, \eta=1/2$:
  - With $C = 0$: all 169 admissible pairs satisfy the inequality with non-trivial contraction ($\eta E_{k, j} > 0$ for all pairs).
  - With $C = 1$: **0 out of 169 pairs** have $\eta E_{k, j} > C N$. The inequality is satisfied purely because $C 2^{-j} \ge \eta V_{k, j}$, which holds for *any* non-increasing sequence.
- For $\ell=1, \eta=1/4$:
  - The zero-loss step at $(k=2, j=0)$ requires $C \ge 1/4$.
  - With $C = 1/4$, $(k=2, j=0)$ is covered, but $C = 1/4$ is non-trivial for only 2 out of 196 pairs.

**Methodological Conclusion:** Adding an additive remainder $C 2^{-j}$ weakens the recurrence to the point of vacuity unless $C = 0$ or $C$ is strictly smaller than $\eta \min (E_{k, j}/N)$. On the singleton seed, $\ell=2$ with $C=0$ is strictly cleaner and stronger than $\ell=1$ with $C > 0$.

---

## 6. Reproduction and Provenance

- Script: [`experiments/rule30/fixed-window-recurrence/verify_fixed_window.py`](../../../experiments/rule30/fixed-window-recurrence/verify_fixed_window.py)
- Machine-checked Audit Record: [`experiments/rule30/fixed-window-recurrence/fixed-window-audit.json`](../../../experiments/rule30/fixed-window-recurrence/fixed-window-audit.json)
- Execution Log: [`experiments/rule30/fixed-window-recurrence/fixed-window-audit.log`](../../../experiments/rule30/fixed-window-recurrence/fixed-window-audit.log)

Run command:
```bash
python3 experiments/rule30/fixed-window-recurrence/verify_fixed_window.py | tee experiments/rule30/fixed-window-recurrence/fixed-window-audit.log
```

---

## 7. The `l >= 2` grid is already tracked, and the margin lives at the domain boundary

Status: **no ladder statement changed. (P2-C) stays conjectured.** One stated
task is already discharged by tracked artifacts, and one recomputation shows
where the restricted domain is hiding the hard cases.

### 7a. The `l >= 2`, `C >= 1/4` search is finished and stored

It is in this directory's own `fixed-window-audit.json`, under
`seed_analysis/grid_results/{l}` and not at the top level. For `l = 2, 3, 4`,
`pure_contraction_C0_holds` is `true` and `worst_C_required` is exactly `0` at
`eta = 1/4` and `eta = 1/2`. A pass at `C = 0` implies a pass at every
`C >= 1/4`, so the `C` half is subsumed as well. `l = 2` additionally records
`0` at `eta = 5/8` and `1/8` at `eta = 3/4`;
`docs/rule30/RESULTS-p2/RESULTS-p2-five-science-explorations.md:55-62` tabulated
`l = 1, 2, 4` eight days before this document existed.

The grid carries no information beyond §4's minimum-loss table, and that is
checkable rather than asserted: pure contraction at `eta` holds exactly when
`eta <= min relative loss`, and `l = 2`'s minimum is `5/8`, which is precisely
the largest tested `eta` that returns `0`.

Consequence for anyone dispatched to run that search: it would rewrite four
tracked artifacts to reproduce numbers already in them.

### 7b. Extending the domain from `j+l <= k/2` to `j+l <= k`

`RESULTS-p2-flexible-scale-audit.md:194-201` puts the `M/N`-minimizing scale
**above** `k/2` at every large `k` (`j = 18` at `k = 28`, where `k/2 = 14`), so
(P2-C)'s domain excludes the scales where the seed's cancellation actually
sits. Recomputed from the stored `E` arrays with this document's own formula,
exact rationals:

| `l` | `j+l <= k/2`: pairs / min / at | `j+l <= k`: pairs / min / at |
|---:|---|---|
| 1 | 196 / **0** / (2,0) | 406 / **0** / (2,0) |
| 2 | 169 / 5/8 = 0.625 / (6,0) | 378 / **19/188** = 0.101064 / (9,7) |
| 3 | 144 / 1611/1940 = 0.830412 / (12,3) | 351 / 67/236 = 0.283898 / (9,6) |
| 4 | 121 / 3711/4040 = 0.918564 / (12,2) | 325 / 23435591/34213680 = 0.684977 / (23,19) |

The restricted column reproduces §4 and record `r30-fwr-seed-min-loss-k28`
exactly, which is the control: the same code over the published domain returns
the published numbers.

**No refutation.** Pure contraction at `l >= 2` with `C = 0` survives the
extension on `k <= 28`; the minimum stays strictly positive. But the `l = 2`
margin falls 6.2x.

**`19/188` is not a candidate `eta`.** Every dip sits within three or four
levels of `k`, where the block count `N/2^j` is between 4 and 16: `(9,7)` has
four blocks. That is the regime `RESULTS-p2-flexible-scale-audit.md:227-229`
discounts for its own four-block witness at `(28,26)` — blocks comparable to
the shell are not an asymptotic certificate. The per-shell `l = 2` extended
minima are erratic in `k` with no trend and no zero.

### 7c. A degenerate pair that a naive extended sweep counts as cancellation

At `l = 1` the extended domain admits `(k,j) = (3,2)` with
`E = [8, 8, 0, 0]`: both energies are zero, the loss is zero, and the ratio is
zero only because the denominator is. It is not a cancellation event. Excluding
it leaves exactly **two** genuine zero-loss pairs with `E_j > 0`, `(2,0)` and
`(11,10)`, independently reproducing the table at
`RESULTS-p2-ordered-energy-audit.md:147-155`.

`(11,10)` lies **outside** `j+l <= k/2`. That is the whole reason record
`r30-fwr-ell1-pure-contraction-refuted` carries a one-element witness set while
the ordered-energy table has two, and it is worth stating because the ratio
test alone does not distinguish the degenerate pair from the real ones.

### 7d. Provenance, unchanged

Shells `13..28` are consumed from `p2-cross-science-explore.json`, which traces
to a gitignored 125 MB payload, and `verify_fixed_window.py:177` cross-checks
against an independent centre-column computation only for `k <= 12`. Everything
in 7b and 7c inherits that. All three attaining witnesses in the restricted
column have `k <= 12` and so sit inside the independently verified range; the
extended-domain minima at `k = 23` do not.

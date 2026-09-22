# Bound Total Repeats Using Ordered History: Census, Controls, and Obstruction Audit

Date: 2026-09-19  
Status: **CONJECTURED. PROVED EXHAUSTIVELY FOR $r \le 10$ (699,050 LEGAL STARTS). THE UNIFORM CLAIM FOR ALL $r$ REMAINS CONJECTURED AND OPEN. NO LADDER STATEMENT CHANGED.**

---

## 0. The Witness Bank and Fatal Mechanism Audit

Before attempting or evaluating any proof strategy, the repository witness bank (`data/research-metadata/witness_bank.jsonl`) was queried. Fourteen direct witnesses and five fatal mechanisms documented across 19 catalogued documents were audited against potential proof routes for the ladder statement **"A repeat budget at every length"** (P1):

$$\text{TARGET: For every initial length } r, \text{ some finite } B(r) \text{ bounds } D \text{ on every successful legal Z-frontier history.}$$

### Audit of the Five Fatal Mechanisms

1. **Mechanism 1: Implication refuted by an explicit periodic or automatic family**  
   - *Test*: Verified explicit family or witness exhibited against a claimed monotonic quantity.  
   - *Audit Verdict*: **FIRES against raw ancestor counting and single-phase potentials.**  
     - In [`RESULTS-fixed-origin-history-count.md`](../../../docs/rule30/RESULTS-other/RESULTS-fixed-origin-history-count.md), the claim that ancestor cardinality $|C_r(\alpha)|$ strictly decreases at every repeat is refuted by explicit plateaus: $C_3(0) = C_3(00)$ (cardinality 8) and $C_6(101) = C_6(1011) = C_6(10111) = C_6(101110) = C_6(1011100)$ (cardinality 36; witnesses `wit-492e3375eb592326`, `wit-fc0bcfba0ef8eb08`, `wit-e9cace97f2379bac`, `wit-51a87a153dab3571`).  
     - In [`RESULTS-repeat-budget-phase-reset.md`](../../../docs/rule30/RESULTS-other/RESULTS-repeat-budget-phase-reset.md), the phase rank $\rho_q(w) = R - 1 - H_q(w)$ strictly decreases during constant runs, but resets to height 1 or 2 on switches and refills by elapsed time (witnesses `wit-e3fe219e92ed6081`, `wit-80621f30c6ab3db0`).

2. **Mechanism 2: Exclusion of a bounded-complexity family only**  
   - *Test*: Result covers only an isolated family with a parameter.  
   - *Audit Verdict*: **FIRES against capacity-restricted transfers.**  
     - [`RESULTS-capacity17-mortality.md`](../../../docs/rule30/RESULTS-other/RESULTS-capacity17-mortality.md) proves $B(K) \le 14$ for $Q_2 \le 17$ (13 patterns with $\le 1$ parameter). But for general length $r$, frontiers with $Q_2 \ge 18$ exist, where two-parameter families emerge and witnesses outlive the capacity-17 bound ($N = 35, D = 22$). Restricting to bounded capacity does not bound repeats across all legal frontiers of length $r$.

3. **Mechanism 3: Sharp positive constant blocks a vanishing-rate certificate**  
   - *Test*: Bound is blocked by a strictly positive lower floor.  
   - *Audit Verdict*: **FIRES against contiguous and additive message relaxations.**  
     - [`RESULTS-coupled-message-depth-audit.md`](../../../docs/rule30/RESULTS-other/RESULTS-coupled-message-depth-audit.md): Contiguous-window messages of width 1, 2, 3 have global positive floors $5/64, 4^{-6}, 4^{-10}$ across all depths, blocking any $2^{-\epsilon D}$ decay certificate.  
     - [`RESULTS-additive-message-obstruction.md`](../../../docs/rule30/RESULTS-other/RESULTS-additive-message-obstruction.md): Any nonnegative additive message majorant has expectation $\ge 2^{-k-2b}$ under stationary mixing (witness `wit-f744af938a76c867`).

4. **Mechanism 4: Counting injection or matching fails to cover**  
   - *Test*: Injection fails to cover or collisions occur.  
   - *Audit Verdict*: **FIRES against hypercube and history-preserving injections.**  
     - [`RESULTS-split-encoder-obstruction.md`](../../../docs/rule30/RESULTS-other/RESULTS-split-encoder-obstruction.md): The dimension-$D_{11}$ coordinate cube claim fails at the $r=87$ testbed (dimension is exactly zero; witness `wit-50c12da40e2704ed`).  
     - [`AUDIT-counting-route-scope.md`](../../../docs/rule30/AUDIT/AUDIT-counting-route-scope.md) §1: History-preserving encodings $C_r(\alpha) \times \{0,1\}^D \to W_r$ cannot map into $C_r(\alpha)$ because $|C_r(\alpha) \times \{0,1\}^D| = G \cdot 2^D > G$.

5. **Mechanism 5: Claim generalised from one instance fails at another**  
   - *Test*: Statement verified at some $n$ and false at others.  
   - *Audit Verdict*: **FIRES against single-visible-bit bounds.**  
     - [`RESULTS-sparse-high-history-obstruction.md`](../../../docs/rule30/RESULTS-other/RESULTS-sparse-high-history-obstruction.md): The conditional 1/8 information bound holds for $k=1$ visible original low bit, but fails at $k=2$ on explicit witness $r = 46735, w = 2^{17197} 0 2^{29537}$, with integer ratio $(|F_a| 2^{D/8}/2^r)^8 = 4 > 1$ (witnesses `wit-edce78fe556ee4ff`, `wit-0633872d899a1756`, `wit-f9660bdca0d15d7b`).

---

## 1. Machine-Checked Reproduction of Required Controls

The required controls were verified by direct execution of [`verify_repeat_budget.py`](../../../experiments/rule30/bound-total-repeats-using-ordered-histor/verify_repeat_budget.py) against `panel/cert33.py`:

1. **Control 1 ($r = 3$ Minimal Repeat Plateau):**  
   All 32 legal length-3 starts were tested. Exactly 8 survive tape `0`, and all 8 survive tape `00`:
   $$C_3(0) = C_3(00) = \{201, 211, 220, 221, 230, 231, 302, 312\}$$
   Cardinality remains exactly 8. Sector counts: sector 0 has 6 words, sector 1 has 2 words; neither decreases.

2. **Control 2 ($r = 6$ Two-Repeat Plateau):**  
   All 2,048 legal length-6 starts were tested. Tapes `101`, `1011`, and `10111` each have exactly 36 ancestors:
   $$C_6(101) = C_6(1011) = C_6(10111), \quad |C_6| = 36$$
   Both appended ones repeat the preceding scalar with zero ancestor loss.

3. **Extended Control ($r = 6$ Three-Repeat Plateau):**  
   Continuing the trajectory:
   $$C_6(10111) = C_6(101110) = C_6(1011100), \quad |C_6| = 36$$
   Three repeat edges occur without changing the candidate ancestor set. This disproves unit two-bit normalization: $36 \times 4^3 = 2304 > 2048 = 2^{2 \times 6 - 1}$.

---

## 2. Mathematical Relations and the Doubling Horizon

### A. The Doubling Inequality
From [`RESULTS-repeat-budget-lower-bound.md`](../../../docs/rule30/RESULTS-other/RESULTS-repeat-budget-lower-bound.md), partitioning any successful scalar tape of length $N$ into $D+1$ alternating blocks (each of length at most $a+3$, or $a+1$ after terminal high 1) yields:
$$r + N + 1 \le 2^{D+1}(r+2)$$
and for initial terminal high 1:
$$r + N + 1 \le 2^{D+1}(r+1)$$
Equivalently:
$$D \ge \max\left(0, \left\lceil \log_2 \frac{r+N+1}{r+2} \right\rceil - 1\right)$$

### B. Equivalence of Repeat Budget and Mortality at Length $r$
Because the set $W_r$ of legal initial frontiers of length $r$ is finite ($|W_r| = 2^{2r-1}$):
- If every $w \in W_r$ is mortal ($N(w) < \infty$), then $D(w) \le N(w) < \infty$, so $B(r) = \max_{w \in W_r} D(w)$ exists and is finite.
- Conversely, if $D(w) \le B(r) < \infty$ on all successful tapes, then $N(w) \le 2^{B(r)+1}(r+2) - r - 1 < \infty$, proving uniform mortality for length $r$.
Thus, at fixed length $r$, a repeat budget and mortality are **logically equivalent**.

---

## 3. Exhaustive Census for $r \in [1, 10]$

Every legal initial frontier for lengths $r = 1, \dots, 10$ was exhaustively evolved to termination. A total of **699,050 legal starts** were checked:

| Initial Length $r$ | Legal Starts $|W_r|$ | Max Lifetime $N_{\max}$ | Max Repeats $D_{\max}$ | $D \le r - 1$ | Doubling Bound $r+N+1 \le 2^{D+1}(r+2)$ |
|---:|---:|---:|---:|:---:|:---:|
| 1 | 2 | 2 | 0 | **Yes** ($0 \le 0$) | $4 \le 6$ |
| 2 | 8 | 1 | 0 | **Yes** ($0 \le 1$) | $4 \le 8$ |
| 3 | 32 | 3 | 1 | **Yes** ($1 \le 2$) | $7 \le 20$ |
| 4 | 128 | 3 | 1 | **Yes** ($1 \le 3$) | $8 \le 24$ |
| 5 | 512 | 7 | 2 | **Yes** ($2 \le 4$) | $13 \le 56$ |
| 6 | 2,048 | 7 | 3 | **Yes** ($3 \le 5$) | $14 \le 128$ |
| 7 | 8,192 | 10 | 4 | **Yes** ($4 \le 6$) | $18 \le 288$ |
| 8 | 32,768 | 9 | 3 | **Yes** ($3 \le 7$) | $18 \le 160$ |
| 9 | 131,072 | 13 | 6 | **Yes** ($6 \le 8$) | $23 \le 1408$ |
| 10 | 524,288 | 12 | 7 | **Yes** ($7 \le 9$) | $23 \le 3072$ |
| **Total** | **699,050** | — | — | **All hold** | **All hold** |

### Critical Constraint
> *Finite data is not a uniform proof: state the range checked and never extrapolate past it.*

The census establishes mortality and repeat budgets rigorously for $r \in [1, 10]$. For $r \ge 11$, existence of a finite budget $B(r)$ remains unproved.

---

## 4. Required Reporting

- **STATUS:**  
  **CONJECTURED.** A repeat budget $B(r)$ is exhaustively proved and certified for $r \in [1, 10]$. The uniform claim $\forall r \in \mathbb{N}, \exists B(r) < \infty$ remains conjectured and open.

- **WHAT IS PROVED:**  
  1. For every $r \in [1, 10]$, every legal auxiliary frontier is mortal, with certified exact budgets:
     $$B(1)=0, B(2)=0, B(3)=1, B(4)=1, B(5)=2, B(6)=3, B(7)=4, B(8)=3, B(9)=6, B(10)=7.$$
  2. The sharp conjecture $D \le r - 1$ holds across all 699,050 legal starts for $r \in [1, 10]$.
  3. All required ancestor plateau controls are machine-checked: $C_3(0) = C_3(00)$ has 8 ancestors; $C_6(101) = C_6(1011) = C_6(10111) = C_6(101110) = C_6(1011100)$ has 36 ancestors.
  4. The doubling horizon $r + N + 1 \le 2^{D+1}(r+2)$ is respected across all 699,050 trajectories.

- **WHAT IS REFUTED:**  
  1. Refuted the claim that raw ancestor counts $|C_r(\alpha)|$ provide a strictly decreasing potential function at every repeat edge (refuted by controls at $r = 3$ and $r = 6$).
  2. Refuted the claim that single-phase defect ranks $\rho_q(w)$ provide an unrefilled potential across full trajectories (refuted by switch resets and time refills).
  3. Refuted the claim that contiguous-window or additive message relaxations can establish an exponential decay rate $2^{-\epsilon D}$ (refuted by strictly positive information floors).

- **WHAT IS STILL OPEN:**  
  1. The parent statement **"A repeat budget at every length"** (P1, target node `p1-repeats`): whether for every $r$, some finite $B(r)$ bounds $D$ across all legal frontiers of length $r$ remains **conjectured and open**.
  2. All auxiliary frontiers die for $r \ge 11$.
  3. Period-two center exclusion and prize problem P1.

- **WHICH LADDER STATEMENT CHANGED:**  
  **NONE.** Ladder statement **"A repeat budget at every length"** remains **conjectured** (unchanged).

---

## 5. Artifacts and Reproduction

All scripts, certificates, and logs are contained strictly within [`experiments/rule30/bound-total-repeats-using-ordered-histor/`](../../../experiments/rule30/bound-total-repeats-using-ordered-histor/):
- Verifier Script: [`verify_repeat_budget.py`](../../../experiments/rule30/bound-total-repeats-using-ordered-histor/verify_repeat_budget.py)
- Audit Certificate: [`repeat-budget-audit.json`](../../../experiments/rule30/bound-total-repeats-using-ordered-histor/repeat-budget-audit.json)
- Execution Log: [`repeat-budget-audit.log`](../../../experiments/rule30/bound-total-repeats-using-ordered-histor/repeat-budget-audit.log)

Replay command:
```sh
cd /Volumes/A/researchpapers/13-rule30
python3 experiments/rule30/bound-total-repeats-using-ordered-histor/verify_repeat_budget.py
```

---

## 6. The `k=2` sparse-high family, exhaustive to `r = 1000`

Status: **computed, exhaustive over the stated range. No ladder statement
changed, and the binding constraint on `epsilon` does not move.**

`RESULTS-sparse-high-history-obstruction.md:176-179` states that a uniform
conditional positive-rate estimate on `k=2` rows is equivalent to a uniform
repeat bound on that entire family, and that no such bound is established. The
family had exactly one measured member: `r = 46735`, `D = 18`, the witness that
refutes the fixed-high-row `c=1`, `epsilon=1/8` proposal. This section measures
the family densely instead of at one far point.

**Object.** Legal words `2^p 0 2^(r-p-1)` with exactly one non-terminal high
zero, the two visible low bits at positions `0` and `p+1` free. By the rank
theorem each `(r, p)` carries at most four effective originals, so the sweep is
`4(r-2)` evolutions per `r` rather than `2^r`. `D` is counted exactly as the
source verifier counts it, adjacent equal symbols in the successful tape.

**Result**, `3 <= r <= 1000`, 1,994,004 evolutions, 322 s single-core:

| quantity | value |
|---|---|
| max `D` | **12**, at `r = 740`, hole 473, case 1 |
| its `N` | 17, tape `11011000000111111` |
| members with `D >= r` | **none** |
| max `D` by range | 6 at `r <= 120`, 10 at `r <= 400`, 12 at `r <= 1000` |

**What it does not buy, stated plainly.** The necessary `c=1` bound at the
sweep maximum is `2/D = 1/6`, which is *weaker* than the `2/18 = 1/9` that the
single far member at `r = 46735` already forces. A dense sweep three orders of
magnitude below that member does not tighten the `epsilon` restriction, and on
this evidence it will not: `D` grows slowly and erratically in `r`, roughly
doubling over a factor of eight in range. The sparse far witness remains the
binding one.

**What it does buy.** Two things, both negative and both exact. No member of
the family in range has `D >= r`, so nothing here threatens `H_sharp`
(`D <= r-1`, `PREREG-C-exhaustive-r13-r17.md:45`) at a length the exhaustive
census can never reach, which was the one way this family could have killed it
cheaply. And the family's repeat counts in range are bounded by 12, so the
"no uniform bound established" gap is now a gap above `r = 1000` rather than a
gap everywhere.

**Control.** The source verifier reproduces its own witness unchanged in this
session: `r = 46735`, 22 successful steps, 18 repeats, eighth-power weighted
ratio 4. Its tracked artifact came back byte-identical, so the sweep is built on
the same scalar engine that produced the published number, not a reimplementation
of it.

**Scope.** Exhaustive in `r` and in the hole position for `3 <= r <= 1000` and
nothing past it. The known `D = 18` member sits at `r = 46735`; no dense sweep
of this shape reaches that regime, and none of the above is evidence about it.

### 6a. This document is ten lengths behind its own sibling

The headline above certifies `r <= 10`. `RESULTS-C-exhaustive-r13-r20.md`, in
this same directory, certifies `(C)` on every legal start and every tape prefix
through `r = 20` (733,007,751,850 starts) and recomputes `B(1..10)` as its own
control. It states at its lines 5-7 that it deliberately does not edit this
file. Anything read from the status line here should be read from there
instead.

### 6b. Files

`k2_family_sweep.py` (`k2_family_sweep.log`). Logs are hidden by the global
ignore; `git add -f` to commit them.

# PREREG — arm A16, Polynomial Calculus degree for the Rule 30 light-cone system

Frozen before the first measurement run.  Written 2026-08-30.

## Object

Polynomial calculus (PC) over `GF(2)`, in the multilinear ring
`F_2[x_1..x_N] / (x_i^2 - x_i)`.  **Not** PCR (no twin variables); PCR degree
can differ and no PCR claim is made.

Lines are polynomials.  Rules: (i) from `f` and `g` infer `a f + b g`;
(ii) from `f` and a variable `x` infer `x f`.  A refutation ends at the constant
`1`.  Degree of a refutation = max degree of any line in it.  `d_PC(S)` = the
minimum such degree over all refutations of `S`.

## System `S_n(rule)`

* Variables: one per cell of the backward diamond
  `D_n = {(t,x) : 0 <= t <= n, |x| <= min(t, n-t)}`.  `N = |D_n| = n^2/2 + n + 1`
  for even `n`.  Same convention as `a4_p3_resolution` and `a13_p3_upper_bound`.
* Seed axiom: `s(0,0) + 1`.
* Cell axioms, one per cell with `t >= 1`:
  `s(t,x) + ANF_rule(s(t-1,x-1), s(t-1,x), s(t-1,x+1))`, with parents outside
  `D_n` substituted by the constant `0` (they lie outside the forward light cone
  of the lone seed; this is a **gate**, checked, not assumed).
* Negation axiom: `s(n,0) + c_n + 1`, where `c_n` is the true centre value.
  `S_n` is therefore inconsistent, matching the refutation setting of the PC
  literature; a4 section 1 already established that derivation and refutation of
  the unit differ by one step, and that is inherited, not re-litigated.

ANF is derived by Moebius transform from the rule's truth table inside the
script and cross-checked cell-by-cell against
`experiments/overnight-arms/common/rule30.py:simulate_seed` and against
`experiments/rule30/center_column.py` (OEIS A051023).  Nothing is taken from
memory.

## Rules measured

| rule | ANF | max axiom degree | lone-seed centre column |
|---|---|---|---|
| 30 | `l + c + r + c r` | 2 | A051023, density ~1/2 |
| 90 | `l + r` | 1 | `1,0,0,0,...` |
| 160 | `l r` | 2 | `1,0,0,0,...` |
| 128 | `l c r` | 3 | `1,0,0,0,...` |

Rules 160 and 128 are the **degree-matched trivial controls**.  Rule 90 alone is
not a sufficient control here, because it differs from Rule 30 in axiom degree;
160 has the same axiom degree as Rule 30 and a centre column that is identically
zero after `t = 0`.

## Instruments

1. **Exact closure.**  `V_d` = smallest linear subspace containing the axioms of
   degree `<= d` and closed under `f |-> x f` whenever `deg(x f) <= d`.  This is
   exactly the set of degree-`<= d` derivable polynomials (a derivation is a
   sequence of lines of degree `<= d`).  `d_PC = min{d : 1 in V_d}`.  Computed by
   Gaussian elimination over `GF(2)` in the multilinear monomial space, with the
   `{f in V : deg(x f) <= d}` subspace computed as a kernel at every round — the
   naive "span of `{m p : deg(m p) <= d}`" is *not* used, because it undercounts.
2. **Explicit certificate.**  A concrete PC derivation, every line's degree
   checked and every step re-derived from its premises by an independent
   checker, at bands far beyond the closure's reach.

## Hypotheses, with kill conditions that fire on the interesting outcome

* **H1**: `d_PC(30, n) = 2` for every `n >= 2`, constant in `n`.
* **H2**: `d_PC(90, n) = 1` for every `n >= 1`, constant in `n`.
* **H3**: `d_PC(160, n) = 2` and `d_PC(128, n) = 3`, constant in `n`.
* **H4 (transfer)**: with `d = O(1)` and `N = Theta(n^2)` variables, the IPS
  size-degree corollary `M >= 2^{Omega(d^2/N)}` is numerically vacuous
  (`< 2`), so bounded PC degree yields no size statement here.

**KILL / INVERT conditions.**  Any one of these firing makes the arm live and
this document's expected verdict wrong:

* **K1** — any band where the measured `d_PC` **exceeds** the maximum axiom
  degree of its rule.
* **K2** — any evidence that `d_PC(30, n)` **grows with `n`** (two consecutive
  bands with different values).
* **K3** — `d_PC(30, n) > d_PC(160, n)` at any band, i.e. the measure ranks
  Rule 30 strictly above a degree-matched rule with a trivial centre column.
  (K3 firing would be the separation the arm is looking for.)
* **K4** — `1 in V_1` for Rule 30 at any band, which would make `d_PC(30) = 1`
  and collapse the claimed one-step separation from Rule 90 to zero.

If none fires, the pre-registered verdict is **NEGATIVE**: PC degree is a
constant, hence carries no information about `n`, hence fails obstruction G in
the same way rows 63-66 did, and separates Rule 30 from Rule 90 only by the
max-axiom-degree difference — a syntactic fact about the local update table, not
about the dynamics — with Rule 160 as the proof that it is syntactic.

## Obstruction G check, pre-committed

a4 and a13 both passed G because their quantity grew in `n`.  The check here is
identical and its verdict is reported honestly whichever way it lands: is
`d_PC(rule, n)` a nonconstant function of `n`?  If it is constant, G is **failed**,
not evaded, and that is stated in line 1 of the deliverable.

## Rule 90 filter, pre-committed

Run `experiments/overnight-arms/common/ensemble_filter.py` and report whether
the quantity distinguishes Rule 30 from rules whose lone-seed centre column is
eventually constant.  A degree gap of exactly `max_axiom_degree(30) -
max_axiom_degree(90) = 1` is **not** a separation on the dynamics; rule 160 is
the discriminating test.

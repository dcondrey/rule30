# The rotated wedge has linear slack, and that reshapes the target

Date: 2026-09-02

Status: **MEASURED, COMPLETE SEARCH, NO THEOREM.  `(RW)`, `(DLP)`, `(SEP)`,
`(PT2)` and P1 ALL REMAIN OPEN.**  This is a census with a reformulated
target attached, not a proof of any of them.

## 1. Why this was run

`RESULTS-PSI-ANCESTRY-LAW.md` section 10 fired the switch criterion
`PROOF-STATE-CAPSULE.md` section 7 sets for leaving `(BWH+)`: `Delta_j` has
full algebraic degree `n` in the source bits at every `n` from 4 to 15, so no
bounded-arity seam law exists and the complete-state recursion fans out.  The
capsule's named fallback is DLP/RW.  Before spending effort there it is worth
knowing whether RW is as marginal as `(BWH+)` turned out to be.  It is not.

## 2. What was measured

`(RW)` (`RESULTS-DLP-ROTATED-WEDGE.md` section 2) forbids `n >= 1`,
`r in {0,1,2}`, `c in {2,3}` and binary `f` of length `2n+r+2` with `f[n:]`
hard-core across its junction with `f[n-1]`, `f[-3:-1] = 12`, and
`P^n(I(f)) = c^(n+r+2)`.

For each `(n, c)` the search reports the **deepest** run of target cells any
admissible `f` achieves, against the `n+r+2` a counterexample needs.

Two properties make the number exact rather than indicative.

- **The search is complete.**  Condition 2 constrains one new output cell per
  appended symbol from index `n` on, so the continuation is a tree pruned at
  every level; the free part is the `2^n` prefix, enumerated exhaustively.
  Nothing is sampled and no bound is heuristic.
- **The number is a conservative upper bound on a real counterexample.**
  Condition 3 (`f[-3:-1] = 12`) can only bite at full depth, which is never
  reached, so it is not imposed.  Dropping a constraint can only make
  `deepest` larger, hence the reported slack is a **lower** bound on the true
  slack.

Gated against the reference: the identification of `diagonal[n]` with
`P^n(I(f))` was checked against `binary_wedge_high_elimination.wedge` on
15,876 binary words, zero failures.

## 3. Result

| n | c=2 deepest | c=3 deepest | need (r=0) | slack | deepest/n |
|---|---|---|---|---|---|
| 7 | 4 | 4 | 9 | 5 | 0.57 |
| 8 | 3 | 6 | 10 | 4 | 0.75 |
| 9 | 4 | 8 | 11 | 3 | 0.89 |
| 10 | 5 | 7 | 12 | 5 | 0.70 |
| 11 | 6 | 7 | 13 | 6 | 0.64 |
| 12 | 9 | 8 | 14 | 5 | 0.75 |
| 13 | 7 | 9 | 15 | 6 | 0.69 |
| 14 | 10 | 8 | 16 | 6 | 0.71 |
| 15 | 9 | 8 | 17 | 8 | 0.60 |
| 16 | 10 | 10 | 18 | 8 | 0.63 |
| 17 | 11 | 10 | 19 | 8 | 0.65 |

`r = 1` and `r = 2` only raise `need` by 1 and 2 with the same `deepest`, so
their slack is uniformly larger; the table above is the hardest case.

**`deepest / n` sits at `0.6 to 0.75` with no upward trend across `n = 7..17`,
and the slack grows from 3 to 8.**

## 4. The contrast that matters

| | `(BWH+)` / `(PSI)` | `(RW)` / DLP |
|---|---|---|
| best near-miss | `n+1` of `n+2` | about `0.65n` of `n+2` |
| slack at its tightest | **1** (at `n = 15`) | **3** (at `n = 9`) |
| slack trend in `n` | flat, attained at 15 and 18 | grows, roughly `0.35n` |
| ratio to independence null | `1.00 +/- 0.05`, clustering to 18 | not applicable, search is complete |

`(BWH+)` is marginal: at `n = 15` a source clears every constraint but the
last.  `(RW)` is not close at any `n` tested, and gets less close as `n` grows.
The two extra conditions RW retains and `(BWH+)` discards — the hard-core
suffix and the exact target `c` rather than only the high bit — are doing the
work.  This is the concrete form of the capsule's remark that a `(BWH+)`
counterexample need not refute period-two exclusion.

## 5. The reformulated target

Linear slack changes what one should try to prove.  `(PSI)` demanded an exact
one-position separation, `0^(n+1)` from `0^n 1`.  RW admits a **rate** target:

> **(RW-alpha).**  There are `alpha < 1` and `n0` such that for every
> `n >= n0`, no admissible `f` achieves a run of more than `alpha * n + O(1)`
> target cells.

`(RW-alpha)` implies `(RW)` for all `n` with `alpha n + O(1) < n+2`, and the
finitely many smaller `n` are exactly decidable by the search here.  The
measured data is consistent with `alpha` near `0.75`.

This is a better-shaped target than `(PSI)` for one specific reason: it asks
for a growth rate rather than a sharp threshold, and a bound with slack to
spare does not have to be tight to be sufficient.  The fan-out obstruction of
section 10 in the companion report bites on exact seam identities; it says
nothing about rate bounds.

## 6. What this does not do

It does not prove `(RW)`, `(RW-alpha)`, `(DLP)`, `(SEP)`, `(PT2)` or anything
about P1.  Obstruction H applies in full: a complete search to `n = 17` is a
lower bound on a complexity function and can never be more.  The value here is
that the *shape* of the remaining obligation changed from an exact separation
to a rate bound, and that the fallback target was measured before effort was
spent on it rather than after.

`(RW-alpha)` is a conjecture supported by 11 values of `n`.  It has no proof,
and no mechanism for the linear slack is identified.

## 7. Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python rw_margin.py --min-source 3 --max-source 11
```

## 8. A mechanism for the linear slack, and its known failure mode

The contrast in section 4 has a quantitative explanation, stated as a
prediction before the measurement below was run.

In `(BWH+)` the forcing pins only `H` at depth `n`, and the one bit of
endpoint symbol choice is spent doing it, so a column costs one constraint and
pays with one bit.  In `(RW)` the target is the exact cell `c`, which pins the
**whole** Moore state at depth `n`: `H = 1` and `E = E(c)`, with `E(2) = 0` and
`E(3) = 1`.  The symbol choice is still consumed by `H`, so `E` is a free
one-bit constraint per column with nothing left to satisfy it.  On top of that
the hard-core condition kills the branch whenever the forced symbol is `1`
after a `1`, which costs a further `log2(4/3) = 0.415` bits if that happens a
quarter of the time.

Predicted cost per column: `1 + 0.415 = 1.415` bits, hence
`alpha = 1/1.415 = 0.707`.

Measured, by counting surviving prefixes `N_k` at each level of the complete
search tree and fitting `log2 N_k` against `k`:

| n | c | slope (bits/column) | `-1/slope` |
|---|---|---|---|
| 13 | 2 | -1.346 | 0.743 |
| 13 | 3 | -1.356 | 0.737 |
| 14 | 2 | -1.299 | 0.770 |
| 14 | 3 | -1.378 | 0.725 |
| 15 | 2 | -1.327 | 0.754 |
| 15 | 3 | -1.440 | 0.695 |
| 16 | 2 | -1.405 | 0.712 |
| 16 | 3 | -1.224 | 0.817 |

Slope clusters at `-1.35 +/- 0.15` against the predicted `-1.415`, and the
first-level ratio is `N_1/N_0 = 0.376 = 2^-1.41`, splitting as one bit for the
`E` constraint times `0.75` for the hard-core survival — the two predicted
terms, separately visible.

**The failure mode is known and must be stated.**  This derivation assumes the
per-column constraints behave independently.  That is exactly the null refuted
for `(BWH+)` in `PREREG-psi-constraint-counting.md`, where `R_k` departed from
1 at large `k` and reached 18.  The same departure could occur here at `k`
beyond the reach of a complete search, and it would be invisible in this fit,
which is dominated by small `k` where the counts are large.  So section 5's
`(RW-alpha)` is a conjecture with a mechanism sketch, not a derivation of one:
the mechanism explains the observed rate, and the observed rate is measured
only where the null has not yet been tested against its own clustering.

What would settle it is a proof that the `E` constraint per column is not
merely one bit on average but one bit unconditionally, given the state.  That
is a statement about the ancestry law in `RESULTS-PSI-ANCESTRY-LAW.md` section
3, and it is the sharpest concrete target this session leaves.

## 9. Three exact facts added while the multi-agent run was in flight

**9.1 The hard-core ablation, which doubles as a gate.**  Dropping the
hard-core condition from RW leaves exactly `(BWH+)` (full Moore state pinned
at depth `n`, arbitrary binary continuation).  `rw_ablation_hardcore.py`
confirms this: without hard-core the search reproduces `(BWH+)`'s known
exceptions, a constant at `n = 6` (`deepest = 9 > need = 8`) and the `n + 1`
near-miss at `n = 15, c = 3` (`deepest = 16`).  With hard-core those become 3
and 8.  The `n = 15` family's forced continuation begins `12211...` and hits
`11` at step 3 while its `E`-constraint survives sixteen steps; hard-core is
what removes that family, and it is the reason RW's slack at `n = 15` is 8
where `(BWH+)`'s is 1.  Neither condition alone is the mechanism: the
`E`-pin alone has fluctuating slack (1 at `n = 15`, 4 at `n = 16`), hard-core
alone is `log2(4/3)` bits per column, and the combination is what has robust
linear slack.  Log: `rw_ablation_hardcore_20260902.log`.

**9.2 No effective forgetting.**  The light cone gives `T[u][n]` as a function
of `e[(u-n-1)/2 .. u]`, so late constraints do not read early source bits
directly.  They read them through the forced symbols, and the dependence is
total: for the deepest witnesses at `n = 12, 14, 16`, varying the first `j`
source bits over all `2^j` values keeps depth `>= D - 1` for a fraction that
halves with each additional bit, `1.00, 0.50, 0.25, 0.12, ...`, at every `n`
and both `c`.  Every early bit is a one-in-two constraint on survival.  No
bounded-window transfer matrix describes the survivors; this is the measured
form of the full-degree result in `RESULTS-PSI-ANCESTRY-LAW.md` section 10.

**9.3 Set form of both constraints** (131,580 checks).  For column `u-1`'s
window `d in [-u, n-1]` of length `m = n + u`, with `Z` the zero cells, `W2`
the cells equal to `2` and `N` the nonzero cells:

```text
    H(e_u) = 1 + (n + u + 1) + |Z|                                          (mod 2)
    E(T[u][n]) = (|Z| + |W2|) (1 + m + |Z|) + #{(x, y) : x < y, x in N, y in Z or W2}   (mod 2)
```

The forced symbol is the parity of the zero count; the defect is a count of
ordered pairs (nonzero below, even above) plus a parity correction.  The
correction to `uc/BRIEF.md` recorded there (the `Phi` indicator is
`[T != 0]`, not `[T == 0]`; the Moore step uses `[T == 0]`) was found by this
check failing on the first form and passing on the second.

**9.4 Census extended to `n = 20`** (`rw_margin_n18-20_20260902.log`,
complete search, `r = 0`):

| n | c=2 deepest | c=3 deepest | need | slack | slope (bits/col) |
|---|---|---|---|---|---|
| 18 | 12 | 11 | 20 | 8, 9 | -1.19, -1.30 |
| 19 | 11 | 13 | 21 | 10, 8 | -1.38, -1.36 |
| 20 | 11 | 14 | 22 | 11, 8 | -1.37, -1.22 |

`deepest / n` sits at `0.55 to 0.70`; the slack has not fallen below 8 since
`n = 15`.  The `n = 20` search visits `2^20` prefixes in about a minute, so
the census is not compute-bound; it is stopped here because obstruction H
says more of it proves nothing.

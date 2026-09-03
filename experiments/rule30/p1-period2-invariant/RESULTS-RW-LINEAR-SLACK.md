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

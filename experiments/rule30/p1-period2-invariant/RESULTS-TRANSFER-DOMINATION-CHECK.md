# Does a null transfer matrix M entrywise-dominate the H_r(n) forcing recursion?

Date: 2026-09-04

Status: **checked and falsified as a pointwise inequality; confirmed as
essentially exact on average.** Not a proof, not a kill of the underlying
idea — it redirects the proof shape needed.

## Motivation

`rw_population_h.py`'s `survival_curve` diagnostic found the hard-core
survival population (per row of `literal_extension`'s forced continuation,
before the `12a`-terminal check) decays at a fitted geometric rate of about
0.40 per row, for several `n`. Proposed candidate: the decay is dominated
by

```
M = [[0, 1/4], [1/4, 1/4]]      (rows/cols indexed by forced state 1, 2)
```

whose leading eigenvalue is `(1+sqrt(5))/8 ~ 0.4045` — matching the fitted
rate closely. Question: do the actual 1-step transition counts over the
survivor set (pooled over `n`, `c`, `r`, and row index `k`) satisfy
`C[s][s'] <= M[s][s'] * N[s]` at every row, or at least under some uniform
scalar multiple of `M`?

## Method

`transfer_domination_check.py`: for each `(n, c, r)`, walk
`literal_extension`'s forced continuation for every source word, tracking
at each row `k` which words are still alive (forced symbols so far all in
`{1,2}`, no `11`). For the alive set, build the empirical count matrix
`C[s][s']` = number of alive words with previous forced symbol `s`
transitioning to next forced symbol `s'` (for `s, s' in {1,2}`; landing
outside `{1,2}`, or `s=s'=1`, counts as death, not a transition). Compare
against `M[s][s'] * N[s]` where `N[s]` is the count of alive words with
previous symbol `s`.

## Result

**The raw inequality is false.** Checked `n = 4..14`, both `c`, `r = 0,1,2`
(429 `(n,c,r,row)` tuples): 486 entrywise violations, starting at `n=4`,
row 0.

**No fixed uniform scalar multiple of M works either, in the strict
worst-case sense**: the maximum required scalar over `n=4..14` is exactly
4.0 (hit at several small-`N` cells, e.g. `N=1, C=1`). Restricting to
`N[s] >= 100` (ruling out small-sample edge effects) the worst case drops
to ~1.75-2.1x, still nontrivially above 1 and not shrinking to 1 within the
tested range (`n = 8..14`).

**But the pooled empirical rate at `N[s] >= 100` matches M almost exactly:**

| entry | empirical (pooled, N>=100) | M |
|---|---|---|
| P(1->1) | 0.0000 | 0 |
| P(1->2) | 0.2501 | 0.25 |
| P(2->1) | 0.2489 | 0.25 |
| P(2->2) | 0.2530 | 0.25 |

`M`'s leading eigenvalue (~0.4045) already matched the independently-fitted
survival-curve decay rate (~0.40) before this check; this confirms it is
the correct *average* one-step transition matrix, with `M[1][1]=0` forced
exactly by the hard-core exclusion (`11` forbidden) and the other three
entries consistent with the forced symbol being close to equidistributed
over its 4 underlying states, independent of the previous symbol.

## Reading

The failure pattern is fluctuation around a correct mean, not a systematic
bias in either direction (violations exceed M at some rows/n and presumably
undershoot at others, since the pooled average matches M almost exactly).
This means:

- **A pointwise entrywise domination inequality is the wrong proof shape.**
  No single scalar multiple of `M` bounds every row without also pushing
  the effective eigenvalue well past 1/2 (worst case observed needs ~1.75x
  even at `N>=100`, giving effective eigenvalue ~0.71, not <1/2).
- **M is not a coincidence.** It is, to 3 decimal places, the actual mean
  transition behavior of the forcing recursion. A proof needs a
  concentration/variance bound (how far can any individual row deviate from
  the mean-field rate, and does the compounding over `n+r+2` rows still
  force exact vanishing) rather than a worst-case pointwise bound.
- **This may be as hard as Rule 30's own open equidistribution question.**
  The near-exact match to 1/4 per entry looks like the forced diagonal
  symbol behaving as if uniformly distributed over 4 underlying states,
  independent of history — structurally adjacent to (and possibly no
  easier than) the still-open conjecture that Rule 30's center column is
  statistically random. Treat this as the likely real difficulty, not a
  side-lemma to be knocked out cheaply.

## What this does not claim

This does not prove or disprove that `H_r(n)` is eventually forced empty
for structural reasons (already known empirically to `n=16`,
`RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`). It narrows what kind of
argument could establish that: not a simple worst-case linear-algebra
domination bound, but something that controls fluctuation around an
essentially-confirmed mean-field rate.

## Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python transfer_domination_check.py
```

# Preregistration: overnight extension of the H_r / D_k / extinction-margin census

Date: 2026-09-04, ~21:45. Status: **predictions frozen before the run.**
Runner: `overnight_census.py`, launched detached in 4 streams over
`n = 17..22`, both tails. Nothing below was computed first.

## Why this run

Three separate quantities all come from the same walk over source words, so
one pass computes all of them and no separate runs are needed:

1. `|H_r(n)|` for `r = 0,1,2` — the RW candidate census. Currently exactly 0
   for `n <= 16` (`RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`, concurrent
   session).
2. `D_k` — distinct surviving continuation prefixes
   (`RESULTS-DISTINCT-CONTINUATION-COUNT.md`). Verified at `n <= 16`.
3. The **extinction margin** = `(n+2) - (max survival row)`, the concurrent
   session's live candidate in `BACKLOG.md` L11: measured `7,5,6,8,8,8` for
   `n = 10,12,14,16,17,18`, apparently stabilizing near 8. If it is bounded
   below by any positive constant for all `n`, then `H_r(n) = 0` follows
   directly with no statistics.

## Frozen predictions

**P1 (the light-cone departure law — the real test).**
`RESULTS-DISTINCT-CONTINUATION-COUNT.md` explains the `D_k` Fibonacci phase
by the proved memory law (`k_seed(L) = ceil((L+1)/2)`: the first `k`
continuation symbols depend on about `2k` source coordinates), predicting
surjectivity onto the hard-core shift while `2k < n` and departure at
`k_dep ~ floor(n/2) - 2`. Measured so far: `k_dep = 4,4/5,5,6` at
`n = 10,12,14,16`. **Predicted for this run:**

```
n       17  18  19  20  21  22
k_dep    6   7   7   8   8   9
```

Scored as correct if `|k_dep - (floor(n/2) - 2)| <= 1` at every `n`; the
law is **falsified** if any `n` deviates by 2 or more, or if the deviation
grows with `n`. This is a genuine prediction: the explanation was written
before any `n > 16` data existed.

**P2 (census).** `|H_r(n)| = 0` for every `r in {0,1,2}`, both `c`, all
`n = 17..22`. A single nonzero value is an RW counterexample and the most
valuable possible outcome of this run — it would refute the conjecture on
the tested range, not merely fail to support it.

**P3 (extinction margin).** The margin stays `>= 1` (strictly positive) at
every `n`, and most likely stays near 8. **Kill:** if the margin decreases
monotonically toward 0 across `n = 17..22`, the concurrent session's
"bounded below" hope is empirically dying and should be reported as such,
not smoothed over.

**P4 (product margin).** The geometric mean of post-departure `D` ratios
stays below `1/phi = 0.618`. **Kill:** any `n` with geometric mean `>=
0.618` breaks the only surviving form of the `D_k` contraction argument
(the per-step form is already known dead — true max is 1.0 at `n = 12,14`).

## What this run cannot do

It cannot prove anything for all `n`. Extending an empty census from 16 to
22 is six more zeros; per this project's standing caveat that is evidence,
not a proof surrogate, and the `PREREG-psi-constraint-counting` near-miss
statistic already warns against extrapolating the unrestricted census. The
value here is entirely in P1, P3 and P4 — which are *falsifiable structural
predictions* — not in P2's expected zeros.

## Controls

- Assert once, at small `n`, that `literal_extension(W, c, L)` is a prefix
  of `literal_extension(W, c, L')` for `L < L'`; the single-pass design
  depends on it and it has not been separately verified.
- Recompute `n = 16` in the same code path and require exact agreement with
  the already-committed values (`D` = `[2,3,5,8,13,21,27,20,6,3,1,0]` at
  `c=2`) before trusting any new `n`.
- Memory: streaming counts only; no storage of per-word continuations
  (the machine has ~1.7 GB free and a documented history of jetsam kills
  from runaway python).

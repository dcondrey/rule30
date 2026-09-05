# Verification of D_k, the distinct-surviving-continuation count

Date: 2026-09-04. Executes the four-check verification plan before any
theorem-track claim is built on `D_k`. Script:
`verify_distinct_continuations.py` (throwaway, not wired into any
pipeline), log `verify_distinct_n16.log`.

`D_k` = number of DISTINCT surviving continuation prefixes of length `k+1`
(prefix includes the junction symbol, the last symbol of the source word).
This is the right object for an existence theorem: a witness exists iff at
least one distinct continuation survives, independent of how many source
words map onto it. The word count `S_k` overcounts, because leading source
symbols are free — the deep survivors observed in the domination test were
one continuation with multiplicity, not independent words.

## Verdict up front

**Mixed. Check 1 passes cleanly; checks 2 and 3 fail as previously stated,
because the earlier claim was generalized from the `n=16` row alone.** The
prior summary ("`D_k` is exactly Fibonacci `2,3,5,8,13,21`, i.e. surjective
onto the full hard-core shift for the first ~5 rows") is true at `n=16` and
FALSE at `n=10,12,14`. The corrected statement is that the surjectivity
phase *length grows with n*, which is a different — and arguably more
interesting — claim, but it is not the one that was reported, and the
"`D_k` is a clean function of `k` alone" hope is dead.

## Check 1 — two independent forcing rules agree exactly: PASSES

Path A: `late_pull_diagonal_sat.literal_extension` (searches all four
values, keeps the one whose edge last cell equals the tail).
Path B: `flip_pairing.forced_orbit` / `psi_kernel.Endpoint` (tries only
`{1,2}`, keeps the one with `H(dia[n])==1`, plus its own cell-vs-tail
check). These are genuinely different rules, which is precisely the
property misread in the retracted naming-collision claim.

```
n=10 c=2  A = B = [2, 3, 5, 8, 6, 2, 0]
n=10 c=3  A = B = [2, 3, 5, 8, 7, 5, 4, 1, 0]
n=12 c=2  A = B = [2, 3, 5, 8, 13, 10, 5, 2, 1, 1, 0]
n=12 c=3  A = B = [2, 3, 5, 8, 12, 11, 2, 1, 1, 0]
n=14 c=2  A = B = [2, 3, 5, 8, 13, 14, 10, 4, 2, 1, 1, 0]
n=14 c=3  A = B = [2, 3, 5, 8, 13, 17, 8, 7, 3, 0]
n=16 c=2  A = B = [2, 3, 5, 8, 13, 21, 27, 20, 6, 3, 1, 0]
n=16 c=3  A = B = [2, 3, 5, 8, 13, 21, 28, 17, 8, 5, 2, 0]
```

Exact agreement at every `n` and both tails. The `D_k` computation itself
is confirmed.

## Check 2 — Fibonacci/surjectivity phase: FAILS as stated, holds in corrected form

Hard-core string counts (the surjectivity target) for `k=0..5` are
`2,3,5,8,13,21`. Measured:

| n | c | D_0..D_5 | Fibonacci through | first departure |
|---|---|---|---|---|
| 10 | 2 | 2,3,5,8,**6**,2 | k=3 | k=4 (6 vs 13) |
| 10 | 3 | 2,3,5,8,**7**,5 | k=3 | k=4 (7 vs 13) |
| 12 | 2 | 2,3,5,8,13,**10** | k=4 | k=5 (10 vs 21) |
| 12 | 3 | 2,3,5,8,**12**,11 | k=3 | k=4 (12 vs 13) |
| 14 | 2 | 2,3,5,8,13,**14** | k=4 | k=5 (14 vs 21) |
| 14 | 3 | 2,3,5,8,13,**17** | k=4 | k=5 (17 vs 21) |
| 16 | 2 | 2,3,5,8,13,21 | k=5 | k=6 (27 vs 34) |
| 16 | 3 | 2,3,5,8,13,21 | k=5 | k=6 (28 vs 34) |

So the run `2,3,5,8,13,21` occurs **only at `n=16`**. The universal part is
`2,3,5,8` (k<=3) at every tested `n`. The departure index tracks

```
k_departure  ~  n/2 - 2
```

(`n=10 -> 4`, `n=12 -> 4/5`, `n=14 -> 5`, `n=16 -> 6`).

**Mechanism, and why this is the expected shape.** The project already has
a proved memory law (`RESULTS-DIAGONAL-MEMORY`: `k_seed(L) = ceil((L+1)/2)`,
and the light-cone statement `T[u][n]` depends on `e[(u-n-1)/2 .. u]`): the
first `k` continuation symbols are determined by roughly `2k` source
coordinates. While `2k < n` there are enough free source coordinates to
realize *every* hard-core prefix, so `D_k` saturates the Fibonacci bound;
once `2k > n` the source runs out and the image must shrink. That predicts
departure at a *scale* `k ~ n/2`. **It does not predict a formula, and the
formula written above is falsified — see the 2026-09-04 correction below.**
The surjectivity is a light-cone counting fact, not evidence of a special
structureless regime, and it should not be cited as an independent
"maximal entropy" finding — it is the same memory law already on record.

## Correction 2026-09-04: `k_dep = floor(n/2) - 2` is FALSIFIED

The `~` in `k_departure ~ n/2 - 2` above was written from `n <= 16` data and
was scored, in the original preregistration, with a `|k_dep - predicted| <= 1`
tolerance. **That tolerance was a design error.** `D_k` is an exact integer
from exhaustive enumeration — no sampling, no noise — so a tolerance on it
makes the prediction unfalsifiable and it converted a genuine disagreement at
`n=20` into a logged "OK". Rescored exactly (commit `a0f539b`), with the census
extended to `n=21`:

| n | 10 | 12 | 14 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|
| measured `k_dep` | 4 | 4 (`c=3`) / 5 (`c=2`) | 5 | 6 | 6 | 7 | 7 | 7 | 8 |
| `floor(n/2) - 2` | 3 | 4 | 5 | 6 | 6 | 7 | 7 | 8 | 8 |

It fails three ways:

1. **`n=10`:** measured 4, predicted 3 — off by one high.
2. **`n=20`:** measured 7, predicted 8 — off by one low.
3. **`n=12`:** the two tails disagree (`k_dep = 4` at `c=3`, `5` at `c=2`), so
   **no formula in `n` alone can be correct**, at any tolerance. This one is
   decisive on its own and no further `n` can repair it.

The increments land at `n=18` and `n=21` — run lengths 2, then 3, then 1 —
which is not `floor(n/2)` behaviour.

**Status of the light-cone story: demoted to a heuristic.** The memory law
`k_seed(L) = ceil((L+1)/2)` supplies the correct *order of magnitude* for where
`D_k` must leave the hard-core bound, and that much is proved. It supplies no
exact law, and **no exact law for `k_dep` is currently known**. Any write-up
must say "departure occurs at scale `n/2`", never "at `floor(n/2) - 2`", and
must not carry a tolerance on an integer-valued structural prediction.

**Rule adopted from this failure:** do not attach tolerances to exact
integer-valued predictions. Either the law reproduces every value, including
the `n=12` tail split, or it is not a law.

## Check 3 — stability of D_k in n: FAILS

`D_k` is stable in `n` only for `k <= 3` (the universally-Fibonacci range).
From `k=4` it varies with `n` (`k=4`: 6, 13, 13 at `n=10,12,14` for `c=2`;
`k=5`: 2, 10, 14). So `D_k` is **not** a function of `k` alone, and the
hope of a clean `n`-independent theorem target on `D_k` is closed.

## Check 4 — true maximum post-departure ratio

Taking the true max over all `k >= 6` and both tails (not adjacent or
cherry-picked pairs):

```
n=12 c=2: [0.4, 0.5, 1.0, 0.0]           max = 1.000 at k=8   (D: 1 -> 1)
n=12 c=3: [0.5, 1.0, 0.0]                max = 1.000 at k=7   (D: 1 -> 1)
n=14 c=2: [0.4, 0.5, 0.5, 1.0, 0.0]      max = 1.000 at k=9   (D: 1 -> 1)
n=14 c=3: [0.875, 0.429, 0.0]            max = 0.875 at k=6
n=16 c=2: [0.741, 0.3, 0.5, 0.333, 0.0]  max = 0.741 at k=6
n=16 c=3: [0.607, 0.471, 0.625, 0.4, 0.0] max = 0.625 at k=8
```

**Strict per-step contraction fails** at `n=12,14`, where a lone surviving
continuation persists one more row (`D: 1 -> 1`). It holds at `n=16`
(max 0.741). So there is no uniform per-step bound `r_k <= lambda < 1`.

The *product* form survives, which is what the induction actually needs:
peak `D` grows about `phi^(n/2 - 1)` (peaks 8, 13, 17, 28 at
`n = 10,12,14,16`) over about `n/2` post-departure rows, so the requirement
is a geometric mean below `1/phi = 0.618`. Measured geometric means over
the post-departure ratios at `n=16` are `0.439` (`c=2`) and `0.517`
(`c=3`), both under the threshold. But this rests on four ratios per case
at a single `n`, and the earlier reported "0.44-0.60 with real margin" was
a geometric mean presented without the accompanying true max of 1.0 — the
margin is in the product, not per step, and that distinction was not made.

## Corrections to the previously reported claims

1. "`D_k` is exactly Fibonacci `2,3,5,8,13,21`" — true only at `n=16`;
   universal part is `2,3,5,8`. Generalized from one row.
2. "surjective onto the full hard-core shift for the first ~5 rows" —
   the phase length is `~n/2 - 2`, not a constant ~5.
3. "post-peak contraction 0.44-0.60, comfortably under 0.618" — those are
   geometric means; the true per-step max is 1.0 at `n=12,14`.
4. The surjectivity phase is explained by the already-proved light-cone
   memory law, so it is not independent evidence of anything new.
5. "`k_departure ~ n/2 - 2`" — falsified as an exact law at `n=10`, `n=20`
   and (decisively) `n=12`, where the two tails disagree. See the 2026-09-04
   correction above. The light-cone argument gives a scale, not a formula.

## Status

Per the pre-agreed decision rule ("Fibonacci fails at some n -> stop and
reassess"), `D_k` does **not** clear the bar to be built on as-is. What
survives is: (a) the computation is verified by two independent forcing
rules; (b) `D_k` is still the correct object for an existence theorem
(the multiplicity argument is unaffected); (c) the collapse to zero is
real in every tested case; (d) the product-form margin holds at `n=16`.
What is closed: `n`-independence, the constant-length Fibonacci phase,
any per-step uniform contraction bound, and (as of 2026-09-04) the exact
departure law `k_dep = floor(n/2) - 2`. No email or write-up should assert
the Fibonacci phase without the `n/2` qualifier and the light-cone
explanation.

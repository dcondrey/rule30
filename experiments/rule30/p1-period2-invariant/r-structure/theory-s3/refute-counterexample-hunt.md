# Refutation: attempt-counterexample-hunt.md (Angle D, target S3)

Date: 2026-09-17. Labels: U proved here or in the cited document, C finite computation, CONJ conjecture. Scripts `scripts/refute_counterexample-hunt_recheck.py` (log `_recheck.log`), `scripts/refute_counterexample-hunt_cluster.py` (log `_cluster.log`), neff re-run in `scripts/refute_counterexample-hunt_neff_rerun.log`. All exit 0.

## Verdict

Refuted at step 5, the "cluster lemma" in the form the argument uses it (neff.py docstring, "New lemmas" section, lemma (3) of the summary): "seeds sharing a forced rho tail of length j keep or lose the next (L1) condition together, so the D_j distinct tails are the independent trials". The first half of the sentence (coincidence on the near-wall window) is U; the second half is false, and the N_eff reading and the `2^-43` extrapolation rest on it. Everything computational survives.

## Fatal step: step 5, second half

(U) What the cluster lemma gives: two seeds whose wall traces agree on `[T, T+m-1]` coincide on cells `-1..-m` at time `T` (left-permutivity). Seeds sharing the tail `rho_cw..rho_(cw+j-1)` and alive at level `j` share `c_T..c_(T+2j-1)` (`T = 2 cw`), hence cells `-1..-2j` at time `T`.

(U) What the next condition reads: condition `cw+j` is `s(T+2j+1,-1)`, a function of `s(T,-1..-(2j+2))`. Cells `-(2j+1)` and `-(2j+2)` lie outside the shared window and are in bijection (left-permutivity) with `(c_(T+2j), c_(T+2j+1))`, i.e. with `rho_(cw+j)` and the condition itself; even the tail of length `j+1` fixes only one of them. "Keep or lose together" is not a corollary.

(C) It is false in the census. `refute_counterexample-hunt_cluster.py` groups the level-`j` survivors of the exhaustive width-`w` census by tail and counts clusters containing both a keeper (`K >= cw+j+1`) and a loser (`K = cw+j`):

| w | j | n_j | D_j | split clusters (tail j) | seeds in split clusters | split clusters (tail j+1) |
|---|---|---|---|---|---|---|
| 30 | 5 | 415 | 29 | 13 | 268 | 9 of 42 |
| 36 | 6 | 2165 | 63 | 40 | 1722 | 37 of 106 |
| 36 | 7 | 1203 | 75 | 18 | 460 | 12 of 92 |
| 40 | 7 | 4735 | 119 | 72 | 3624 | 60 of 197 |
| 40 | 8 | 2237 | 120 | 17 | 695 | 13 of 143 |
| 40 | 9 | 875 | 76 | 2 | 48 | 2 of 76 |
| 42 | 8 | 4328 | 179 | 52 | 1846 | 30 of 223 |
| 42 | 10 | 1453 | 88 | 1 | 40 | 1 of 90 |

Explicit pair at `w = 30`, common tail of length 6: `100000010000001000000100010101` keeps (`K = 23`) and `111110000100110010011000010101` loses (`K = 20`). At every level `j <= log2(N_w)/2` all `2^j` tails are present and every cluster splits. Splits vanish only at the deepest two or three levels (`w = 40`: none for `j >= 10`), where the few survivors happen to agree on the extra cells too: an observation about the census tail, not a lemma.

Consequences. `N_eff = D_j 2^j` at "the first unsaturated level" is a choice of level (`w = 40`: `j = 9`, 2 of 76 clusters still split; `w = 42`: `j = 10`, 1 of 88), not a derived count; one level shallower the same formula gives `N_eff = 2^(2j)`, far below `N_w`. The "New lemmas" sentence "the maximal free phase is a maximum over those states" is likewise unproved: a seed's free phase is not a function of its width-`2j` window at time `T`. The fitted `log2 N_eff = 0.416 w - 1.7`, the residuals (`+0.2`, sd `1.6`) and the `2^-43` figure are a curve fit with a hand-picked level; the document's own CONJ label is the correct one.

## Other checks

Step 1 (U): correct. Both systems update cell `-1` identically while (L1) holds, and `K` reads a configuration both share. Archive gate reproduced; the archive argmax strings give `K = 14, 36` in an independent per-cell simulator.

Step 2 (U): correct. Trace `c_0..c_(w-1)` and seed `W_1..W_w` are in bijection (induction on `t+m <= w`); the odd-`w` forcing of the last symbol is the halving lemma's coefficient 1, asserted in the code. Cross-checks at `w = 12, 17, 22` pass.

Step 3 (C): correct and the strongest result of the document. No seed of width `<= 62` keeps `floor(w/2)+65` conditions, so S3 (hence S3-hc, S3-hc5) holds for every `W` of width `<= 62`. The bit-packed simulator agrees with an independent per-cell simulator on `(K, K_hc, K_hc5)` for 400 random seeds of widths 8 to 47; the record seeds check (`w = 12` `K = 14`, `w = 58` `K = 54`, `w = 61` `K = 56`, `w = 50` `K = 48`).

Step 4: harmless slip. `E[max free | N]` is `log2 N + 0.33`, not `+ 1.3`; the table's coin column is summed directly and is right. The coin comparison (`P(<= obs) < 0.02` at 20 of 23 widths) reproduces.

Step 6, tables, fits (C): reproduced. neff re-run gives `log2 N_eff = 0.416 w - 1.68`, `free(w) = 0.380 w + 0.68`, residual mean `+0.21`, sd `1.63`; the `w = 53` profile and `D_j = 271, 141, 74, 27, 14, 3, 1` match the extension log.

## What survives

U: step 1 (`K` invariant under boundary choice); step 2 (rho-prefix census is complete); the first half of step 5 (shared tail of length `j` implies shared cells `-1..-2j` at time `T`). C: S3, S3-hc, S3-hc5 for all seeds of width `<= 62`; Table 1; the largest `K - w` over every seed tested is `+2`; `free_hc5 <= 12` on `w <= 62`; the family and sample results; the `D_j`, `n_j` counts and the fitted lines as descriptions. Not U: "keep or lose together", "the maximal free phase is a maximum over those states", `D_j` as the count of independent trials. CONJ: the `0.88 w` growth of `max K` and the `2^-43` expectation.

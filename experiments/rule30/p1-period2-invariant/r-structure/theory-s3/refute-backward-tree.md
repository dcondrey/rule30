# Refutation pass: attempt-backward-tree.md (Angle B, target S3)

Date 2026-09-17. Labels: U proved here or in the cited document, C finite computation, CONJ conjecture. Scripts and logs under `scripts/`, prefix `refute_backward-tree_`.

## Verdict

Fatal step: **none**. The attempt claims no proof of S3, S3-hc or S3-hc5. Every statement it labels U is proved, every C reproduces (the four author scripts byte for byte, and independently by a second implementation), and its diagnosis stands: the only sufficient statement left is a free-phase bound, and nothing finite-state carries it (Lemma 3 is a two-line consequence of the halving lemma). Not refuted. Two diagnostic claims are mislabelled or wrong, neither load-bearing.

## What was re-derived

1. (C) `backward-tree_structure.py 18 24`, `backward-tree_merge.py 14`, `backward-tree_depth_dfa.py 5 10`, `backward-tree_hc5_census.py 40` re-run: all four logs reproduce byte for byte (`diff` empty, exit 0).

2. (U, C) `refute_backward-tree_lemmas.py` (log `_lemmas.log`, `ALL_OK`, exit 0): explicit list-based half-line, preimages by the written-out leftward recursion, no bit tricks. Lemma 1 on every row of width `L <= 14`: each candidate maps back to `y`, finiteness is exactly `(x_(L-1), x_L) = (1,0)`, a finite preimage has width `L-1` and forces `y_(L-1) = 1`, the other case is all ones from `L+2`; the in-degree table matches the author's. `F(E1) subset Fin` and the `(001)^omega` tails on 2,000 random E1 rows. Lemma 2: the rebuilt automaton has 10 reachable unmerged states, two merging on either input, characteristic polynomial `x^6 (x-1)(x^3 - x^2 - 2)` (the quartic factors), radius `1.695621`, both word counts obeying `a_n = a_(n-1) + 2 a_(n-3)`; brute-force in-degree-1 equals `U_1(L-2)` for `L = 3..16`. Lemma 3: for every window `q` of length `m <= 6` satisfying its own conditions and every `w = m+2..22`, the proof's construction was executed (2,796 rows); at every even position exactly one bit satisfies the new condition (halving re-verified) and every row survives at least `floor((w-1)/2)` conditions, slack 0 attained. Zero-wall and pinned boundaries give the same survival count on all 16,383 seeds of width `<= 14`, so the halving lemma, stated for the pinned boundary, transfers to the zero-wall system as used.

3. (C) `refute_backward-tree_census.py 22` (log `_census.log`): brute force over all `2^(w-1)` seeds, `w = 8..22`, no level construction. Seeds past the controllable phase, `free`, `free_hc`, `free_hc5` and the hard-core profiles equal the author's census and Tables 1 and 2 of `RESULTS-FORWARD-SURVIVOR-W40.md` at every width.

4. (U) Steps 1, 4, 5, 8 and the Correction checked as arguments. Step 4 is the halving bijection on the projective limit plus `rho(F^2 x) = sigma(rho(x))`; the eventually-periodic argument goes through on the zero-wall half-line unchanged. The finite backward tree inside `Fin` is Lemma 1 iterated. The Correction is accurate: `RESULTS-FORWARD-BOUNDARY-CENSUS.md` line 20 and `PROOF-STATE-CAPSULE.md` line 138 say "exactly two-to-one" of the map on finite rows, and the census abstract says the preimages differ only in the boundary-adjacent cell; in-degrees 0, 1, 2 all occur and `x_2 = y_1 XOR alpha` always differs. The census body (lines 40 to 43, "possibly infinite") is right; only the abstract sentences are wrong.

## Defects found, none fatal

- "For S3 it is false [C]" overclaims. The computation shows only that a width-independent free-phase bound `B` must exceed 17 (`free(39) = 18`) and a trend of about `0.4 w` on `w <= 40`. Nonexistence of `B` is CONJ.
- "The fair-coin null with the trace entropy 0.124 predicts a free phase growing like 0.03 w under either filter" misuses the cited entropy. `0.124` is the growth rate of the full trace language `R` (`r_structure.log`, `S3 L=60`), which neither census imposes. Under the filters actually used, the null (N seeds from the census, each free step a coin for `(L1)` plus a fair-coin `rho` symbol kept inside the filter) has slope `0.263` per unit `w` for hc and `0.233` for hc5 (Monte Carlo, 400 replicates; analytic `log_(1/p) N` gives `0.266`), predicting `7.5 -> 10.1` and `6.4 -> 8.6` on `w = 30..40` against measured `5 -> 7` and `5 -> 6`. The `R` null does give `0.032`, for a census the attempt did not run. The conclusion that widths `30..40` cannot separate growth from a constant survives under the corrected null; the number and its attribution do not.
- Step 3's gloss "the number of words keeping the pair unmerged from the start `y_1 = 1`" describes `U_1` only: in-degree-1 rows with `y_1 = 0` exist at every `L >= 3` (836 of 1,420 at `L = 16`). The equality with `U_1(L-2)` is a numerical identity, C, with no proof offered.
- Step 8, "Koenig's lemma produces points of `X_inf`": the tree yields backward-infinite `(L1)`-chains; points of `X_inf` come from the nested cylinders. Cosmetic.
- "The diagonal-transients result already shows the settled edge never reaches the middle" cites a measured regular region of depth about `0.77 t` on `d <= 2000`: C, not a proof.

## Surviving statements

U: step 1 (`F` exactly two-to-one on `{0,1}^N`), Lemma 1 (criterion, width `L-1`, `y_(L-1) = 1` necessary, E1 dichotomy, `F(E1) subset Fin`), Lemma 2 (absorption, 10-state automaton, `|F(Fin_(L-1))| = 2^(L-3) + O(1.6956^L)`, density `1/4`), step 4 (`(X_inf, F^2)` conjugate to the full one-sided 2-shift, `P` shift-invariant without eventually periodic points, S3 is `X_inf intersect Fin = empty`), step 5, Lemma 3 and its consequence that no finite-valued wall state with a `w`-independent `B` can hold, the finite backward tree inside `Fin` with `(001)^omega` tails, the Correction.

C: the in-degree table to `L = 18` (independently to 14), in-degree-1 `= U_1(L-2)` to `L = 18` (independently to 16), sections B and C of the structure log, the merge-time and `|F^t(Fin_w)|` tables, the depth-DFA counts `t <= 5`, the hc and hc5 censuses to `w = 40` (brute-forced over all seeds to `w = 22`), free phase `18` at `w = 39` for `(L1)` alone.

CONJ: the `(L1)`-only free phase is unbounded; the hard-core free phase is unbounded but `o(w)`; "the data do not favour" a bounded free phase, under the corrected null a two-step rise inside noise. Nothing here narrows (PT2).

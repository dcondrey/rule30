# Refutation pass: attempt-density-rigidity.md (Angle C, target S3-hc5)

Date 2026-09-16. Labels: U proved here or in the cited document, C finite computation, CONJ conjecture. Scripts and logs under `scripts/`, prefix `refute_density-rigidity_`.

## Verdict

Fatal step: **none**. The attempt claims no proof of S3-hc5; every statement it labels U is proved, every C reproduces on an independent implementation, and its diagnosis (the proof stops at the step 7 to 8 transition; step 8 is a census weaker than the forward census from width 32 on) stands. Not refuted.

## What was re-derived

1. (C) Both author scripts re-run: `density-rigidity_columns.py 16 12` and `density-rigidity_frames.py HC5 30` reproduce their logs byte for byte (`diff` empty, exit 0 both).

2. (U, C) `refute_density-rigidity_lemmas.py` (log `_L12.log`, `ALL_OK`): a pure-Python reconstruction, validated two ways that do not reuse the recurrence: the array obeys the zero-wall rule at every interior cell (0 violations over all 4,096 windows), and forward simulation from the reconstructed time-0 row agrees with it inside the light cone (0 mismatches). All sixteen identities of Lemmas A and B pass on their stated hypotheses (Lemma A on all windows; Lemma B fails on 1,024 and 768 of 4,096 windows without hard-core, so that hypothesis is used). Lemma C's pocket row, Lemma D's `P_1..P_4`, the `P_5 = 2` witness `00101` (also `10101`), and `P_j = 2` for `j = 5..11` pass. Permutivity in the last variable holds for `E_m`, `m` odd, and `O_m`, `m` even, to `m = 23` (Lemma F's ingredient). The only columns constant on HC or HC5 windows to depth 16 are `O_1 = 1` and `E_4 = 0`. `(01)^inf` gives `(1 0^6)^3 10`; even-row mass of `E_1..E_16` ranges 2 to 10.

3. (U) Lemmas A to D were also checked by hand from the rule and the cited identities; each case split is correct.

4. (U) `refute_density-rigidity_edge.py 18 40` (log `_W18_T40.log`): all 262,143 seeds of width 1..18 settle the 11-cell frame, its phases and the zeros beyond by `t = 12`; width 2 seed `01` needs exactly 12, so Lemma E is tight. Then the width-independent closure: with `D_0 = 1`, `D_1 = 1` (`t >= 1`), `D_2 = 0` (`t >= 2`) the reset chain makes `(D_3..D_10)` autonomous from `t = 2`, and all 256 initial states settle the frame by `t = 12`. That makes Lemma E a complete case analysis for every width. The document's thin line, `D_9 = 1` from 11, needs the phase coupling between `D_3` and the settle time of `D_7` (the one-line argument alone gives 12); the closure settles it.

5. (C) `refute_density-rigidity_frames.py 30 3` (log `_L30_Z3.log`): own automaton enumeration of HC5 words (527,333, cross-counted by transfer matrix), own reconstruction with a rule-consistency check on 4,000 full arrays. Every step 8 and 9 number reproduces: no frame at even positions 11..23, 25, 26, 29, 30 and odd positions 11..28, 31; `e = 24` even `(0,1)` has 5,634 windows with zero run 0; `e = 37` even `(1,0)` has 376 with run 17; every combination realizable for all `e >= 45`; the phase test kills exactly widths 1..31 and 33 (width 33 dies at `t = 17`, `e = 50`, odd rows); missing 6-bit patterns 59, 26, 6 at `m = 1, 14, 20`, zero for even `m >= 26` and odd `m >= 25`; `P_j = 2` for `j = 5..29`.

6. (U) Steps 1, 2, 7 and Lemmas F, G were checked as arguments. Step 1 uses that the reconstruction satisfies the rule at every cell `(t+1, i)`, `i <= -1`, with column 0 the wall, and that `E_4 = rho_k rho_{k+1}`, `E_1 = 1 - rho_k` translate the extra hypotheses of S3-hc5 into no `11`, no `00000`. Step 2's threshold `i < (2j+1-w)/4` is the edge inequality `2(j-i)+1 > w+2i`. Step 7's odd-width contradiction (`c = 0` from `(D_4,D_3)`, `d = c` from `(D_10,D_9)`, against `d(t+2) = 1 - d(t)`) is a correct conditional whose antecedent fails at pair 5. Lemma F's map on `(rho_k..rho_{k+h-1}, k mod p)` is well defined because `c_k` is a fixed function of `k mod p` from `K` on. The citations (halving Lemma 2 transposed, `tau_d ~ 1.30 d`, the fair-coin and period-5 regime) say what the attempt says they say.

## Defects found, none fatal

- The Target paragraph's "edge frame: cell 37" contradicts step 8: combinations are still missing at `38 <= e <= 44`, and the phase test kills width 33 at `e = 50`. The frame carries information to about `e = 50`.
- Step 3 is labelled U, but "column periodicity is not forced anywhere" is U only for permutive-parity columns (Lemma F) and the five listed near-wall columns; for the other non-permutive columns it rests on the depth-16 constancy check, which is C. (Non-constancy would suffice, since a non-constant sliding block code on the mixing SFT HC5 has a non-eventually-periodic image, but it is checked only to depth 16.)
- Step 3 lists `O_2` under non-permutive parity; `O_m` with `m` even is permutive parity. Cosmetic.

## Surviving statements

U: step 1 (Lemma G reformulation), step 2 (no fresh bit, memory `j/2 + w/4 + O(1)`), Lemma A (O_4, O_5, E_6 under (L1) alone), Lemma B (O_6, O_7, E_7, E_8 under hard-core), Lemma C (pocket), Lemma D (`P_1..P_4 <= 1` under hard-core), Lemma E (frame from `t = 12`, now by complete case analysis), Lemma F, step 7 as a conditional.

C: `P_5 = 2` at `00101` and `P_j = 2` for `j = 5..29`; the step 8 frame census, kill list `1..31, 33`, and realizability of every combination from `e = 45`; the step 9 pattern counts; the step 10 mass range and the `(01)^inf` row. All exact statements about the HC5 language for the depths named, since every admissible window extends to an admissible word of length 30.

CONJ: the "Where it fails" diagnosis that no bounded-window argument reaches the edge of a seed of width above about 30. Supported by step 9, not proved.

Nothing here narrows (PT2).

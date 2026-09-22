# Refutation pass: attempt-edge-meets-wall.md (Angle A, target S3-hc)

Date 2026-09-17. Labels: U proved here or in the cited document, C finite computation, CONJ conjecture. Scripts and logs under `scripts/`, prefix `refute_edge-meets-wall_` (all exit 0).

## Verdict

Fatal step: **none**. The attempt claims no proof. Every step labelled U was re-derived by hand and holds; every C reproduces byte for byte and on an independent implementation. Its diagnosis stands and is sharpened below: the sufficient statement (Z) is not only generically false for non-periodic demands, it is strictly weaker than the eventually-periodic lemma, since one periodic hard-core demand of period 13 defeats it exactly. Not refuted. Four misstatements found, none load-bearing.

## What was re-derived

1. (C) All four author scripts re-run (`col8_windows`, `zerowall_columns 600 10`, `transients 4096 1000`, `saturation 20 20`): each log reproduces with empty `diff`.

2. (U, C) `refute_edge-meets-wall_forward.py 12 64` (log `_W12_T64.log`), forward simulation of every seed of width 1..12 on the zero-wall half-line as ground truth, no reconstruction code shared with the author:
   - A: the leftward reconstruction relation reproduces the simulated diagram from column -1 alone, with no (L1) hypothesis. This is what makes the (Z) census a statement about real diagrams.
   - B: 11 at `(t,t+1)` in column `-m` iff `s(t,-m)=1` and `s(t,-m-1)=0`, every column, every time (L1's static half).
   - C: whenever column `-m` has no 11 from `t0` on, the region `i <= -m-1` re-simulated as an independent zero-wall system from its row at `t0` agrees cell for cell (43,721 cases; L1's dynamic half, the input to L3, L4 and step 7).
   - D: the near-wall identities, both L2 identities and the `s(2k,-5)` formula hold at every `k` where (L1) holds through `k+3` (4,438 cell checks).
   - E: every column `-J`, `J >= w_L`, carries the edge 11 at `(J-w_L, J-w_L+1)`, so `m - L(m) - 1 <= w_L - 1` for every seed (L4 in edge form).
   - F: every seed of width <= 12 loses (L1) within 64 steps, max survival 14 odd steps; step 5's `w_L <= 4` bound is consistent with this.

3. (U) Steps 1, 2, 4 to 8 checked as arguments. Step 1's birth relation is the wall rule `s(e+1,-1) = s(e,-2) XOR s(e,-1)`. Step 5's equivalence needs the reconstructions from `c(rho)` and from `(0, c')` to agree on `i <= -5`, which holds because `s(2k+1,-4) = 1` forces `s(2k+1,-5) = 1` under hard-core. Step 7's chain of zeros from column `-J-1` back to `c` is a correct induction on the reconstruction relation. L6 is correct: the diagram of a finite seed with demand `rho` is the reconstruction from `c(rho)` by uniqueness, and step 7 at `t_0 = L(m)+1` gives `w_L + L(m) + 1 > m`.

4. (C) `refute_edge-meets-wall_zstat.py 600 14` (log `_M600_P14.log`) and the `M=1500` run (log `_M1500.log`): own 2D-array reconstruction. Fresh random hard-core, HC5 and unrestricted demands give `max_m (m - L(m) - 1) = 4` (0 unrestricted) with column `-4` the only zero wall, to depth 600 and 1500. Two structured non-periodic demands the author did not test behave the same: the Fibonacci word (Sturmian, in HC5) and the rising edges of Thue-Morse. Column `-12` has no 11 on any gap>=3 word of length 18; column `-16` carries a 11 for `000001000` at every shift.

5. (C) `refute_edge-meets-wall_periodic.py 14` (log `_P14.log`): for a periodic demand the columns are eventually periodic in `m`, so cycle detection on `(col_{-m}, col_{-m-1})` settles (Z) exactly. Of the 177 periodic hard-core demands with primitive period <= 14, 176 satisfy (Z). `(0001010010101)` does not: transient 7,627, cycle length 10,166, no zero-wall column in the cycle, exactly 26 zero-wall columns, the deepest `-7286`. So `sup_m (m - L(m) - 1) = 7286`, (Z) fails, and the (Z) route excludes only widths <= 7286 against a demand the eventually-periodic lemma excludes outright.

## Defects found, none fatal

- L5, column `-8`: "zero wall iff `rho` avoids `0101` from index 1" is off by one. The `(2k, 2k+1)` pair reads `rho_k..rho_{k+4} = 01010` for `k >= 0`, so `0101` at index 0 also produces a 11: `0101 0^16` has one at `t = (0,1)`. Correct: column `-8` is a zero wall iff `rho` has no `0101` at any index, under hard-core no `101` at any index >= 1 (`101 0^17` gives no 11; `0 101 0^16` gives one). The windows themselves are right at every `k`.
- Step 3: "regular depth 0.78 to 0.81 of `t`" holds at `t = 1024` only; at `t = 512` the log gives 0.79 to 0.89. Cosmetic.
- Step 9: "at most 25 to 94 for the random demands and 395 for one sparse-defect demand" misreads the author's own log: 24 to 74, and 1,814 (`p = 0.01 #3`). The (Z) statistic is unaffected.
- Step 9: "Periodic demands behave as the eventually-periodic lemma predicts" is true of the five tested and false as a generalization (item 5). This strengthens the diagnosis.
- Step 8: `m - L(m) - 1 <= w_L` is loose by one; the edge 11 gives `<= w_L - 1`. Not an error.

## Surviving statements

U: steps 1, 2, 4, 5 (including S3-hc for `w_L <= 4` and the `c'` equivalence), 6, 7, 8; lemmas L1, L2, L3, L4, L6; L5 for column `-12` (gap>=3) and for column `-16` (`000001000`); L5 for column `-8` with the index corrected to 0.

C: step 3's transients and regular depths as logged (not as summarized); step 9's census, including the `max = 4` bound for every extension of the tested prefixes; the same bound for Fibonacci and Thue-Morse demands to depth 1500; the exact periodic census: (Z) holds for 176 of 177 periodic hard-core demands of period <= 14 and fails for `(0001010010101)`.

CONJ: "no argument that uses `rho` only through its factor structure can complete the route." Supported by items 4 and 5, not proved.

Nothing here narrows (PT2) beyond `w_L <= 4` (U) and the setting's `w_L <= 40` (C).

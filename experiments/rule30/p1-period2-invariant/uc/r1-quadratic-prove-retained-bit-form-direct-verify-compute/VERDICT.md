# Verdict on the direct proof of `retained-bit-form` (COMPUTE lens)

Date: 2026-09-03.  Proof audited:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-quadratic-prove-retained-bit-form-direct/PROOF.md`.

**Verdict: SOUND.**  All five parts (a) to (e) of the lemma hold, uniformly in
`n`, `u` and the binary prefix, and the proof derives them from the triangle
definition and the three finite local facts (F1) to (F3) with no gap.  One
display in the write-up, Corollary 5.1, is wrong by a complement; it is not
load-bearing (its corrected form gives the same conclusion, and nothing else
cites the wrong sign), and it is recorded below as an erratum, not a break.
No counterexample to the lemma or to any load-bearing intermediate claim was
found in the screened range, in a structured screen far beyond it (`n` to
1000, letter windows to `m = 2000`), or by hand re-derivation of every step.

No em-dashes appear in this file.

## 1. What was rerun, and whether the logs match

All scripts cited by the proof and by the lemma's kill test were rerun from
the work directory with `uv run python`; the logs are in this directory.

| Script (as cited) | Rerun log (this directory) | Match to cited log |
|---|---|---|
| `rbf_direct_gate.py` (defaults) | `rerun_rbf_direct_gate.log` | identical line for line after stripping the `[Ns]` timings; `ALL PASS` in 29 s |
| `rbf_direct_gate.py --umax 14 --gate-n 12 --rand-n 150 200 --samples 100 --seed 2 --letters-m3 12 --letters-m4 9 --balance-brute 12 --balance-transfer 100` | `rerun_rbf_direct_gate_large.log` | identical after stripping timings; `ALL PASS` in 149 s (cited 128 s) |
| `uc/r1-quadratic/q2_balance_proof.py` | `rerun_q2_balance_proof.log` | identical; `PROOF COMPLETE (p(1)=0 and d(1..4)=1): True` |
| `uc/r1-quadratic/q2_pieces.py --max-n 6` | `rerun_q2_pieces.log` | the cited log stops at `n = 5`; the rerun adds `n = 6` (`19601` pieces for each `c`, P1, P2 PASS, hit affine all-ones on retained bits PASS), everything through `n = 5` identical |
| `uc/r1-quadratic/q2_gate_random.py --n 30 40 50 --samples 3000 --seed 1` | `rerun_q2_gate_random.log` | the cited log ran `n = 18, 22, 26`; the rerun at the lemma's stated range passes G1 to G4 on `192000`, `252000`, `312000` columns |
| `uc/r1-quadratic/q2_merge.py` (defaults `n = 4..16`) | `rerun_q2_merge.log` | the cited log covers `n = 6..15`; the rerun's shared range is identical and adds `n = 4, 5, 16` |
| `uc/r1-quadratic/q2_gate.py --max-n 12` | `rerun_q2_gate.log` | the cited log ran `--max-n 9` (`20476` columns, `614` of `6872` single keys ambiguous); the rerun at the lemma's stated `--max-n 12` passes G1 to G5 on `212988` columns (`3260` of `51988` single keys ambiguous, max fibre 7) and the transfer count `2*zeros - 3^m = 1` for `m <= 40` |
| `psi_kernel.py --max-source 9` (kernel versus the reference pipeline, not cited by the proof, run as an extra gate on the rule itself) | `rerun_psi_kernel_validate.log` | `1022 binary sources and 21844 four-state endpoints agree with the reference; n=15 falsifier reproduced` |

No assertion fired in any rerun.  The numbers the proof quotes from its logs
(`1492` of `7745` single keys ambiguous with max fibre `7` at `u <= 12`;
`2046`, `90114`, `39200`, `88572`, `87380`; charpoly `[1, -2, -4, 2, 3]`)
are reproduced exactly.

## 2. Independent re-derivation, step by step

Own code: `rbf_verify.py` (this directory), log `rbf_verify.log`.  It imports
only `psi_kernel.CONE`, `BOUNDARY` and `Endpoint`, and re-implements every
definition from the lemma's wording (the `q_i` listing, "nearest nonzero cell
above", the runs, the read-out) rather than from the proof's or the gate's
code.  It also checks each clause against a second, differently coded
characterisation, so that an index slip in either would fire.

Hand audit of the derivation (each item was re-derived, not read):

- (F1) (F2) (F3): `CONE` rows are `[0,1,3,2]`, `[3,2,1,0]`, `[3,2,0,1]`,
  `[3,2,1,0]` and `BOUNDARY = [3,2,1,0]` (`rbf_verify.log` lines 2 to 3).
  The 16 pair checks pass in own code (section F of the log).
- Lemma 2: `h(d) = 1 + H(e_u) + (d+u) + Z(<d)` follows from (F3) at `d = -u`
  and (F1) at each step.  Correct.
- Lemma 3: `F(-u) = E(e_u XOR 3) = E(e_u) = 0` for binary `e_u`; the step is
  (F2).  Correct.  This is the only place the prefix's binarity enters.
- Lemma 4: `h(n) = 1 + H(e_u) + m + |Z|`, so `H(e_u) = m + |Z| = N mod 2`.
  Correct; forcing unique because the coefficient of `H(e_u)` is 1.
- Lemma 5: substituting gives `h(d) = 1 + (n-d) + Z(>= d) = 1 + #{nonzero in
  [d, n)}`, and the three cases of "retained" are the three parities of that
  count.  Correct.  `rbf_verify.py` checks the literal definition against the
  count characterisation on every window (`retained-two-definitions`).
- Lemma 6: `F(n) = #{retained d : b_d = 1}`; zeros have `b = 1`, nonzero cells
  have `b = [T = 2]`.  Correct.  Also checked against an independently coded
  BRIEF primed form `beta (1 + alpha') + gamma'` on every window (`c-primed`).
- Lemma 7: the non-retained cells are the blocks `(q_{i+1}, q_i]`, `i` odd;
  `F` is constant on each because the cells strictly inside the block are
  non-retained and contribute `h b = 0`; `T[u][d] = 0` iff `(h, F) = (0, 1)`.
  Correct, including the `i = N` case (`F_N = 0`, `T[u][-u] = 1` when `N`
  odd).
- Lemma 8: `F_{i-1} - F_{i+1}` counts retained `b = 1` cells in
  `(q_{i+2}, q_i]`, which are the `z_i` zeros of `I_i` plus `q_i` itself.
  Correct, with `F_{N+1} := 0`.
- Lemma 9: column `u` is rebuilt from `(Z_{u-1}, even bits)`; the converse
  needs `Z_{u-1}` from the `h` profile (Corollary 5.1, see the erratum) and
  the even bits from Lemma 8.  `rbf_verify.py` performs the rebuild
  constructively from the PAIR ALONE (`rebuild_from_pair`) and compares cell
  by cell, then iterates the forced window recursion six steps from the
  rebuilt column and compares with the kernel's own future.  Correct.
- Lemma 10: an odd-indexed nonzero cell has `a = 0` and `h = 0`, so its only
  letter enters multiplied by zero.  Correct.  Checked by replacing each such
  cell by every other nonzero value (`1`, `2`, `3`) and recomputing column `u`
  from scratch through `CONE`; and each even-indexed flip is checked to
  change `E(T[u][n])`.
- Lemma 11 and 12: the relaxed count.  `N >= 2` patterns are balanced because
  `w_2` has coefficient 1; `N = 1` gives `2 ceil(m/2)`; `N = 0` gives
  `[m even]`; the total is `(3^m + 1)/2` for both parities of `m`.  Correct.
  Checked by brute force through `CONE` (own code) to `m = 13`, per pattern,
  and by exact integer powers of an own-built transfer matrix to `m = 3000`
  with an own Faddeev-LeVerrier characteristic polynomial
  `x^4 - 2x^3 - 4x^2 + 2x + 3`, roots `1, 3, -1 (double)` verified by
  evaluation.

## 3. Erratum found: Corollary 5.1 as displayed is false

PROOF.md section 5 displays

> For `d in Win`, `1 + h(d) + h(d+1) = [T[u-1][d] != 0]`, because the counts
> in Lemma 5 at `d` and `d+1` differ by exactly `[d in Nz]`.

The justification is right and the display is wrong: the counts differ by
`[d in Nz]`, so `h(d) + h(d+1) = [T[u-1][d] != 0]` and therefore
`1 + h(d) + h(d+1) = [T[u-1][d] = 0]`, which is also what the Moore step
`h(d+1) = h(d) + 1 + a_d` quoted in the same sentence says.  Section C51 of
`rbf_verify.py` tests the display as written on all binary words `u <= 8`
and all `n <= u`: it fails on `40952` of `40952` cells (every cell, since it
is the complement of the truth), first witness word `(1,)`, `n = 1`,
`d = -1`, `T[u-1][d] = 1`, `h(d) = 1`, `h(d+1) = 0`; the corrected display
fails on `0` of `40952` (`rbf_verify.log`, lines `C51`).

Impact: the corollary is cited once, in Lemma 9(ii), for "`Z_{u-1}` is
recovered from the `h` profile".  That recovery is valid under the corrected
display (a zero cell is exactly where `h` does not change), so Lemma 9 and
everything downstream stand.  No part (a) to (e) depends on the sign.  The
gate `rbf_direct_gate.py` does not test Corollary 5.1 directly, which is why
it did not catch the slip.  Fix: replace `!= 0` by `= 0` in the display (or
drop the leading `1 +`).

## 4. Counterexample hunt beyond the screened range

The proof's own screens stop at binary words `u <= 14`, random words to
`n = 200`, and exhaustive letter windows `m <= 12` (`{0,1,2}`) and `m <= 9`
(`{0..3}`).  `rbf_verify.py` sections A and B push structured families past
that (numbers from `rbf_verify.log`):

**Section A (real columns, forced orbits).**  Sixteen prefix kinds per `n`:
`1^n`, `2^n`, `(12)^*`, `(21)^*`, `(112)^*`, `(122)^*`, `(1122)^*`,
`(2111)^*`, `(1112)^*`, `(211212112)^*` (the `n = 15` extremal suffix
cylinder), `(12112)^*`, `(2212)^*`, the recorded `n = 15` falsifier source
`111122211212112` tiled, and three random words; each followed by its forced
continuation to `u = 2n + 5`, every column `u` in `[n, 2n + 5]` checked
(so `u = n`, the whole-column case, is included).  Logged PASS lines
(`rbf_verify.log`): `n = 13, 15, 17, 20, 24, 31, 32, 33, 47, 64, 65, 100,
127, 128, 200, 257, 300, 500, 1000` with `304, 336, 368, 416, 480, 592, 608,
624, 848, 1120, 1136, 1696, 2128, 2144, 3296, 4208, 4896, 8096, 16096`
columns respectively, `49,392` distinct (prefix, `n`, `u`) columns in all,
all checks PASS.  (The log's `A  total columns checked: 419832` line is
inflated by my own bookkeeping: `total += cols` sits inside the per-kind
loop and re-adds the running count once per kind; the per-`n` lines, printed
once each, are the correct counts and their sum is `49,392`.)
At `n = 1000` the window length reaches `m = 3005`, 250 times the largest
exhaustively screened letter window.  Above `n = 200` the `O(m^2)`
bit-replacement and six-step-future checks run on every 25th column and on
six sampled odd and six sampled even cells; the `O(m)` checks (a) to (d),
Lemma 1 and the rebuild from the pair run on every column.

**Section B (letter windows, free bottom letter).**  44 families per `m`:
all-zero, constant `1`, `2`, `3`, the periodic words `02, 20, 01, 10, 03,
30, 13, 31, 12, 21, 23, 002, 020, 200, 001, 010, 0002, 0020, 0123, 3210,
0220, 0110, 0213`, the extremes `0^{m-1}2`, `2 0^{m-1}`, `0^{m-1}x`,
`x 0^{m-1}`, gapped words `(v 0^k)^*` for `(v,k) = (2,2), (2,3), (1,2),
(3,5), (2,7), (1,11)`, and random windows with zero density `0.02, 0.1, 0.3,
0.5, 0.7, 0.9, 0.98`; `m = 13, 14, 15, 16, 20, 25, 33, 50, 64, 100, 128,
200, 500, 1000, 2000`: `660` windows, every `m` line PASS
(`rbf_verify.log`, `B  total windows: 660`).

**Section E (balance).**  Brute force through `CONE` in own code with the
per-pattern decomposition and the bottom-nonzero count for `m <= 13`:
`#Phi=0 = 2, 5, 14, 41, 122, 365, 1094, 3281, 9842, 29525, 88574, 265721,
797162`, each equal to `(3^m+1)/2`, every `N >= 2` pattern balanced at
`2^{N-1}`, bottom-nonzero zeros `2, 2, 10, 26, 82, 242, 730, 2186, 6562,
19682, 59050, 177146, 531442` equal to `3^{m-1} - 1 + 2[m odd]`; own
transfer matrix rows `[1,0,2,0], [0,1,0,2], [1,1,0,1], [1,1,1,0]`,
characteristic polynomial `[1, -2, -4, 2, 3]` with roots `1, 3, -1 (double)`
verified by evaluation, and `d(m) = 1` exactly for every `m <= 3000` by
integer matrix powers.  Wall clock for the whole run: 244 s, `ALL PASS`,
`exit=0`.

Every logged check of (a), (b), (c), (c-primed), (d) (run structure,
complete runs, `F` constant on runs, read-out, rebuild from the pair,
six-step future from the pair, odd-bit blindness, even-bit visibility) passed
on every column and window.  No counterexample exists in any of these
families.

Why none can exist: parts (a) to (d) concern one window and the next column
only (Lemma 1), the column is the trajectory of a fixed four-state machine
whose single step is (F1) plus (F2) plus (F3), and those three facts are
exhaustively true on the 16 pairs.  A counterexample at any `m` would
therefore have to be a counterexample to a one-step fact, which the finite
check excludes.  The screens above are therefore gates on the bookkeeping,
as the proof says, not evidence; obstruction H does not arise.

## 5. What this verdict does and does not say

- It says the lemma `retained-bit-form` (a) to (e) is proved by PROOF.md,
  with one non-load-bearing display to correct.
- It says nothing about `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)` or P1.  The
  lemma is an identity between adjacent columns and implies none of them,
  exactly as the proof's section 9 states; the balance (e) lives on the
  relaxed letter space, and Remark 12.2 (bottom-nonzero windows have
  imbalance `+-2`, reproduced here: `bottom-nonzero zeros` `2, 2, 10, 26, 82,
  242, 730, 2186, 6562, 19682, 59050, 177146` for `m = 1..12` in
  `rerun_rbf_direct_gate_large.log`) is the reminder that nothing about the
  forced orbit's hit rate follows.
- Obstructions A to H: the proof's section 10 dispositions are correct as
  stated; the one I would sharpen is D, which is evaded rather than
  inapplicable because the recursion `Z_{u+1} = Psi(Z_{u-1}, Z_u)` is proved
  to exist and is explicitly not claimed to be bounded or local.

## 6. Files in this directory

- `rbf_verify.py`, `rbf_verify.log`: the independent checker and its full run.
- `rerun_rbf_direct_gate.log`, `rerun_rbf_direct_gate_large.log`: the proof's
  gates rerun, identical to the cited logs modulo timings.
- `rerun_q2_gate.log`, `rerun_q2_gate_random.log`, `rerun_q2_pieces.log`,
  `rerun_q2_balance_proof.log`, `rerun_q2_merge.log`: the lemma's kill tests
  at the ranges the lemma specifies.
- `rerun_psi_kernel_validate.log`: the kernel against the reference pipeline.

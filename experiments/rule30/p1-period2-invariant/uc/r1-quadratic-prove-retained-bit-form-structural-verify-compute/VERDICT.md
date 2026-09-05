# Verdict on the proof of `retained-bit-form` (compute lens)

Date: 2026-09-03.  Lemma: `retained-bit-form`, parts (a) to (e).
Proof under review:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-quadratic-prove-retained-bit-form-structural/PROOF.md`.

**Verdict: SOUND.**  No counterexample found to the lemma or to any
intermediate claim; every cited script reruns to the cited log; every
derivation step was checked by hand against the finite facts F1 and F2, which
were rebuilt independently here.  Two reporting nits are recorded in section 5;
neither touches the proof.

All files named below without a path are in this directory:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-quadratic-prove-retained-bit-form-structural-verify-compute/`.

## 1. Reruns of every script the proof cites

| cited run | my rerun log | result |
|---|---|---|
| `rbf_structural_checks.py --ub 12 --u4 6 --m 10` (`rbf_structural_checks.log`) | `rerun_rbf_structural_checks.log` | identical after stripping timings, except the args line: the cited log predates the `--mutate` flag and lacks `'mutate': False`; all counts equal (13,650 words, 1,023,096 cells, 90,114 pairs, 9,830 keys, 648,434 odd flips, 603,132 even flips, S6 to m = 10) |
| `rbf_structural_checks.py --ub 14 --u4 7 --m 12` (`rbf_structural_checks_u14_m12.log`) | `rerun_rbf_structural_checks_u14_m12.log` | byte-identical after stripping timings (54,610 words, 4,791,416 cells, 425,986 pairs, 32,143 keys, 3,534,232 odd flips, 3,320,196 even flips, N0 = 265,721 at m = 12) |
| `rbf_structural_checks.py --mutate` (`rbf_structural_mutate.log`) | `rerun_rbf_structural_mutate.log` | fires at the same first word: `AssertionError: ('b', (1,), 1, -1)` |
| `uc/r1-quadratic/q2_balance_proof.py` (`q2_balance_proof.log`) | `rerun_q2_balance_proof.log` | byte-identical: characteristic polynomial `x^4 - 2x^3 - 4x^2 + 2x + 3`, `p(1) = 0`, `d(1..8) = 1` |

The lemma packet's kill tests (exploration scripts, not cited as evidence by
the proof) were also rerun at the parameters the packet states:

| kill test as stated | my rerun log | result |
|---|---|---|
| `q2_gate.py --max-n 12` | `rerun_q2_gate_n12.log` | G1 to G4 PASS on 212,988 columns, 56,064 distinct pairs; Z_(u-1) alone: 51,988 keys, 3,260 with more than one column, max 7; G5 brute force m <= 10 equals the transfer matrix, `2 zeros - 3^m = 1` to m = 40 |
| `q2_gate_random.py --n 30 40 50 --samples 3000 --seed 1` | `rerun_q2_gate_random_n30-50.log` | G1 to G4 PASS on 192,000 + 252,000 + 312,000 columns |
| `q2_pieces.py --max-n 6` | `rerun_q2_pieces_n6.log` | PASS through n = 6 (19,601 pieces per target), zero FAIL lines |
| `q2_merge.py --max-n 15` | `rerun_q2_merge.log` | identical to `q2_merge.log` on n = 6..15 (the cited log starts at n = 6; mine adds n = 4, 5) |

## 2. Hand audit of the derivation

Every step of PROOF.md sections 2 to 7 was checked against the text; the
audit trail, with the one place that needs care:

- **F1, F2.**  Rebuilt `CONE` and `BOUNDARY` from the carry-action formula
  in a fresh script (`rbf_adversarial.py`, function `rebuild_cone`), asserted
  equal to `psi_kernel.CONE` and `psi_kernel.BOUNDARY`, and rechecked
  `H(phi(l,r)) = H(r) + 1 + [l = 0]`, `E(phi(l,r)) = E(r) + H(r)[Lo(l) = 0]`,
  `BOUNDARY[s] = s XOR 3 = CONE[3][s]` on all 16 pairs and 4 symbols
  (`rbf_adversarial.log` line 2).
- **Lemma H, Lemma E.**  Base cases use only F2 (`H(s XOR 3) = 1 + H(s)`,
  `E(s XOR 3) = E(s)`); the steps are F1 with `l = T[u-1][d]`, `r = T[u][d]`,
  which is the argument order of the triangle recurrence and of
  `Endpoint.peek` (`new_column[i] = CONE[column[i+1]][new_column[i+1]]`).
  Correct for arbitrary four-state prefixes and all four `e_u`.
- **Proposition A.**  `H(e_u) = 1 + (n+u+1) + |Z| = m + |Z| = |N| + 2|Z| = |N|`
  mod 2; the bijection `{1,2} -> {0,1}` gives existence and uniqueness.  Uses
  `n <= u` so that `T[u][n]` reads only window cells.  Correct.
- **Proposition B.**  `h_{j+1} = h_j + 1 + a = h_j + [q_j != 0]`, so
  `h_j = 1 + |N| + #{i < j nonzero} = 1 + #{i >= j nonzero}`.  Correct; at
  `j = m` this is the pin `h_m = 1`.
- **Corollary (b).**  A cell of `B_i` (`i >= 1`) has exactly `q_1..q_i` at or
  above it, so `h = 1 + i`; `B_0` has none, `h = 1`.  Matches the lemma's
  definition of retained word for word.
- **Proposition C.**  `F_m = sum_j h_j b_j`; `b = 1` on `{0, 2}`; `h = 1` on
  retained cells.  Correct.
- **Corollary C'.**  The one place that needs care: for `y in W2` the count
  `#{x in N : x >= y}` includes `y` itself.  The proof avoids the issue by
  writing `h(y) = 1 + |N| + #{x in N : x < y}`, which is valid whether or not
  `y in N` since `#{x >= y} + #{x < y} = |N|`.  Correct; the set form of
  BRIEF section 3 follows.
- **D1.**  (3) uses that `R_k = B_{2k+1}` is a contiguous depth interval all of
  whose cells are non-retained, so `E_u` is constant on it; (4) uses (0.1)
  `T = 0 iff (H, E) = (0, 1)`; (5) counts the retained `{0,2}` cells below the
  run: the `z_{2j}` zeros and the head (if `w_{2j} = 1`) of each even block
  `B_{2j}`, `j > k`.  The bottom cases (`|N|` odd, `R_{K-1} = {-u}`,
  `T[u][-u] = e_u XOR 3 != 0`) are consistent.  Correct.
- **D2, D3.**  `F_k + F_{k+1}` is the single term `j = k+1`; `F_K = 0` closes
  the bottom.  `F_k` is read from `Z_u` because `R_k` is nonempty and lies
  entirely in or entirely out of `Z_u` by D1(4).  Decoding needs `Z_{u-1}`
  (for the runs and the `z_i`) as well as `Z_u`; the proof says so.  Correct.
- **D4.**  Column `u'` on `[-u'-1, n-1]` is the window of column `u'+1`
  (`u'+1 >= n`), whose bottom cell is the binary `e_{u'}`.  Correct.
- **D5.**  The toggle changes `b` at `q_i` only; `H_u` depends on the zero
  pattern only; `E_u(d)` shifts by `h(q_i) = [i even]` for `d > q_i`, for all
  `d` up to `u` since the window cells above `n-1` are unchanged.  Correct.
- **Theorem E.**  `tau` toggles `q_2` between `2` and `x`, preserving all
  positions, `|N|`, every `z_i` and every `w_i` with `i != 2`; it is
  fixed-point free on `|N| >= 2`.  `|N| = 0` gives `Phi = m`; `|N| = 1` gives
  `Phi = z_0` with `z_0 in [0, m-1]` and two letters, so
  `N_0 - N_1 = [m even] - [m odd] + 2([m odd]) = 1`.  Correct.

No step relies on "clearly" or on a numerical check.  The only finite inputs
are F1 and F2 (16 and 4 cases), both rebuilt here.

## 3. Adversarial computation beyond the screened range

Script: `rbf_adversarial.py`, written independently of
`rbf_structural_checks.py` and `qf_common.py` (own rule table, own triangle,
own window analysis).  It is stricter than S5 in one respect: the pair
`(Z_{u-1}, Z_u)` is *decoded* by the explicit D2/D3 formulas and the decoded
column is compared cell by cell with the true column on `[-u-1, n]`, then the
decoded column is used as the next window and the predicted `Z_{u+1}` (runs
with `F = 1`) is compared with the true zero set of column `u+1`; S5 only
checked that the pair-to-column map is well defined.  D5 toggles are applied
to the full column `u-1` and compared on the whole column `u` (all of
`[-u-1, u]`), not only up to depth `n`.

Log: `rbf_adversarial.log` (families A to D, F) and
`rbf_adversarial_exhaustive_n13-16.log` (family E).

Every column check asserts (a), (b) on every window cell plus the pin, (c)
via the block formula, D1 (zero set equals the runs with `F_k = 1`, `E_u`
equals `F_k` on every run cell), D3 by decoding, the second-order recursion
for both `e_{u+1}` and `Z_{u+1}`, and uniqueness of the forced symbol.

| family | range | columns or cells | D5 flips (odd invisible / even visible) | result |
|---|---|---|---|---|
| A random sources, forced orbit `u = n..4n` | `n = 20` (300 sources), `30` (150), `45` (80), `64` (40), `100` (12) | 18,300 + 13,650 + 10,880 + 7,720 + 3,612 columns; mean `|N|` up to 263 at `n = 100` | 402,981 / 399,032 | PASS |
| B 15 structured sources (`1^n`, `2^n`, `(12)*`, `(21)*`, `(112)*`, `(122)*`, `(1122)*`, `(1222)*`, `(211212112)*`, `2^(n-1)1`, `12^(n-1)`, `1^(n-1)2`, Thue-Morse, Fibonacci, hard-core random), forced orbit `u = n..3n+2` | `n = 16, 24, 33, 50, 71, 100` | 525 + 765 + 1,035 + 1,545 + 2,175 + 3,045 columns | 137,242 / 136,346 | PASS |
| B the `n = 15` falsifier `111122211212112`, orbit to `u = 60`, and its 32-symbol word `WQ` as a prefix for every `n <= 32` | | 78 columns | 1,473 / 1,433 | PASS |
| C arbitrary binary words, not forced, every `n <= u` | 150 words, `u in [30, 60]` | 6,730 `(word, n)` pairs | 29,184 / 28,646 | PASS |
| D Lemma H and Lemma E, four-state prefixes, all four `e_u` | 200 prefixes, `u in [20, 40]` | 49,800 cells | | PASS |
| E exhaustive forced orbits `u = n..2n+3` | `n = 13, 14, 15` (8,192; 16,384; 32,768 sources) | 139,264 + 294,912 + 622,592 columns | | PASS |
| E exhaustive `n = 16` (65,536 sources), `u = 16..35` | | 1,310,720 columns, 180 s | | PASS |
| F (e), transfer matrix, exact integers | `m <= 400` | `N_0 = (3^m + 1)/2` at every `m` | | PASS |
| F (e), brute force, block formula = Moore `Phi`, `q_2` involution flips `Phi`, `|N| <= 1` census | `m <= 13` | 1,594,323 words at `m = 13` | | PASS |

Whole run 145 s (`rbf_adversarial.log`, `exit=0`).

**Controls** (the test can fail).  `--mutate odd` (retained := odd-indexed)
fires at the first structured source: `('b', ('B', '1^n', 16), 16, 16, -16)`
(`rbf_adversarial_mutate_odd.log`).  `--mutate const` (the retained-zero
constant `z_0` dropped from `Phi`) fires at the first column with an odd
`z_0`: `('c', ('B', '1^n', 16), 16, 19)` (`rbf_adversarial_mutate_const.log`).

## 4. Counterexample search: what was tried and why nothing fired

The lemma is an identity between adjacent columns derived from two finite
facts; a counterexample at large `n` would contradict a step of section 2,
each of which I checked.  The families were chosen to stress the places a
derivation slip would show:

- deep forced orbits (`u` to `4n`), where `|N|` reaches 260 and the number of
  runs `K` exceeds 130, stressing the block/run bookkeeping of D1 and D2;
- constant and short-period sources (`1^n`, `2^n`, `(12)^*`, `(112)^*`,
  `(1222)^*`, the `n = 15` extremal suffix `211212112` repeated), which
  produce long zero runs and long nonzero runs, stressing `B_0` empty versus
  nonempty and `z_{|N|} = 0`;
- arbitrary (non-forced) binary words at `u` up to 60 with every `n <= u`,
  including `n = u` (window is the whole column);
- arbitrary four-state prefixes for the by-product Lemmas H and E;
- exhaustive forced orbits at `n = 13..16` to `u = 2n + 3`, past the
  `u <= 14` of S5 and the `u <= 2n + 1` of `q2_gate.py`;
- the letter-space balance to `m = 400` exactly and the involution to
  `m = 13` (1,594,323 words).

None fired.  The relevant obstruction is H, and it does not bite here: the
computation is a gate on a derivation, not the evidence.

## 5. Nits (not defects of the proof)

1. The lemma statement's part (d) reads "the zero set `Z_u` ... determines
   every `w_i` with `i` even".  As stated for `Z_u` alone this is false
   (runs with `F_k = 0` are invisible in `Z_u`, and the `z_i` are needed);
   the intended and proved statement is that the **pair** `(Z_{u-1}, Z_u)`
   determines them, which is what PROOF.md D2 says and what the lemma's own
   next clause says.  A wording repair in the lemma statement, nothing more.
2. The lemma packet's kill-test text says `q2_gate.py --max-n 12` and
   `q2_gate_random.py --n 30 40 50 --samples 3000 --seed 1`, but the logs in
   `uc/r1-quadratic/` were produced with the defaults (`--max-n 9`: 20,476
   columns; `n = 18, 22, 26` with 1,500 samples).  Rerun here at the stated
   parameters, they pass (section 1).  The proof does not cite these logs.

## 6. Scope, as the proof states it

The lemma implies none of `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)`, P1, and the
proof claims none.  It is proved for the array `T` of the triangle recurrence
over `CONE`, tied to `psi_kernel.Endpoint` by S3; the identification of that
kernel with the Rule 30 pipeline is the prior chain and is not re-proved.
Theorem E is about the relaxed letter space, not the orbit distribution.

# Verdict on PROOF.md for lemma `retained-bit-form`, LOGIC lens

Date: 2026-09-03.  Proof audited:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-quadratic-prove-retained-bit-form-structural/PROOF.md`

## Verdict: SOUND

Parts (a) to (e) are proved as stated, for every `n >= 1`, every binary word
in `{1,2}^u` with `u >= n`, and every `m >= 1`.  Every inference in sections
0 to 7 was checked line by line; each is either one of the two finite facts
F1, F2 (exhaustive over 16 pairs and 4 symbols, finite by nature), the
triangle definition of BRIEF section 2, or a derivation written out in full.
No quantifier is silently narrowed from "for all" to "for the tested range";
no step cites a numerical verification as evidence; the words "clearly",
"easy to see", "standard" do not occur.  One sentence of commentary (section
6 Remark, repeated in section 9) gives a wrong reason for a true fact; it is
outside the lemma and outside the derivation of (a) to (e), and the proof's
own Propositions D3 and D5 contradict it.  Details below.

No failure was reproduced.  All kill tests named by the lemma pass, and an
independent verifier written from the lemma text (not from the proof's block
decomposition) passes.

## 1. Step-by-step audit of the derivation

Notation as in PROOF.md.  "OK" means the step follows from what precedes it.

**0.1 to 0.3, definitions.**  The recurrence `T[u][d] = phi(T[u-1][d-1],
T[u][d-1])` for `-u < d <= u` reads column `u-1` on `[-u, u-1]`, its full
range: OK.  The window `[-u, n-1]` lies in column `u-1` exactly when `n <= u`:
OK.  Bottom window cell `T[u-1][-u] = e_{u-1}`, binary hence nonzero: OK.
Blocks `B_0, B_1, ..., B_{|N|}` partition the window, alternate in parity,
`B_0` retained, so maximal non-retained runs are exactly the odd blocks: OK.
`(0.1)` `T = 0 iff H = 0 and E = 1`: from `E = 1 + H + Lo`, OK both ways.
Column `u` on `[-u-1, n]` reads only `e_u` and window cells: OK.

**F1, F2.**  Finite by nature (16 argument pairs, 4 symbols).  Rechecked in
`rerun_rbf_structural_checks.log` (S1, S2 PASS).  Legitimate as proof steps
under BRIEF section 7 ("a finite exhaustive check with a script and log").

**F3.**  Not used in sections 2 to 7 (the proof says so).  I also read
`psi_kernel.Endpoint.peek/append` (lines 100 to 121): `new_column[length] =
BOUNDARY[symbol]`, `new_column[i] = CONE[column[i+1]][new_column[i+1]]`,
`column = new_column + [symbol]`, `new_diagonal[k+1] =
CONE[diagonal[k]][new_diagonal[k]]`, `new_diagonal[0] = new_column[0]`.  With
`column[i] = T[u][-i]`, `diagonal[k] = T[u][k]` this is the triangle
recurrence for every `u`, so F3 is a gate on a structural identity, not a
finite fact the proof leans on.

**Lemma H, Lemma E.**  Induction on `d` from `-u` to `u`.  Base from F2
(`H(s XOR 3) = 1 + H(s)`, `E(s XOR 3) = E(s)`), step from F1 with `l =
T[u-1][d]`, `r = T[u][d]`.  Right side of H increases by `1 + [T[u-1][d] = 0]`
per step: OK.  Stated and proved for arbitrary four-state prefix and arbitrary
`e_u`, which is wider than BRIEF section 2's binary form and consistent with
it (constant `E(e_u) = 0` on `{1,2}`): OK.  Independently checked on random
four-state prefixes of length 40, all four `e_u`, 97,200 cells
(`verify_logic.log`, V3 PASS).

**Proposition A, part (a).**  Lemma H at `d = n` with `#{zeros in [-u, n)} =
|Z|`; `e_u -> H_u(n)` is a bijection `{1,2} -> {0,1}` because `H(1) = 0`,
`H(2) = 1` and the remainder is a constant of column `u-1`: existence and
uniqueness of the forced symbol OK.  `H(e_u) = 1 + (n+u+1) + |Z| = m + |Z| =
|N| + 2|Z| = |N| (mod 2)`: OK.  The proof of A uses only Lemma H at `d = n`,
so A also holds for an arbitrary window content with binary `e_u` (this
matters for D5 below).

**Lemma M.**  Start `(1 + |N|, 0)` from F2 and A; step from F1: OK.  This
re-derives BRIEF section 2's Moore step from F1 and F2 rather than citing its
17,410-column verification, so no verified-but-unproved identity enters.
The letter space `{0,2,x}^m` is strictly larger than the realised windows, so
proving B, C, E on it and specialising is legitimate: OK.

**Proposition B, Corollary (b).**  `h_{j+1} = h_j + [q_j != 0]`, so `h_j = 1
+ |N| + #{i < j nonzero} = 1 + #{i >= j nonzero}`: OK.  For `d in B_i`, `i >=
1`, the nonzero cells at or above `d` are exactly `q_1..q_i` because `d in
(q_{i+1}, q_i]`: OK.  `d in B_0`: none, `h = 1`: OK.  At the bottom cell `d =
-u` this reads `H(e_u XOR 3) = 1 + |N|`, consistent with F2 and A.  `h_m = 1`
is the pin: OK.

**Proposition C, part (c).**  `F_m = sum_j h_j b(q_j)` with `F_0 = 0`; `b =
1` iff letter in `{0, 2}`; `h_j = 1` iff retained; the retained cells with
letter in `{0,2}` are the zeros of `B_0` and of even blocks plus the heads of
even blocks with `w_i = 1` (`B_0` has no head): OK.  The affine all-ones form
in the even `w_i` with constant `|Z_ret|` given the zero pattern: OK.

**Corollary C'.**  `h(y) = 1 + #{x in N : x >= y} = 1 + |N| + #{x in N : x <
y}` (mod 2, using `-a = a`); sum over the `|Z| + |W2|` cells `y` with letter
in `{0,2}`; `1 + |N| = 1 + m + |Z|`: OK.  This derives BRIEF section 3's set
form, which BRIEF records as verified only.  The `beta [e_u = 1]` rereading
uses `H(e_u) = |N|` from A: OK.

**(6.1)** is Lemma M plus Proposition C read at every `d`: OK.

**D1.**  (1) `e_u` binary.  (2) retained gives `H_u = 1`, cell in `{2,3}`.
(3) two cells of the same run: the interval between them lies in the run, all
non-retained, contributes nothing to (6.1).  (4) zero iff `H_u = 0` and `E_u
= 1` iff non-retained and `E_u = 1` iff in `R_k` with `F_k = 1`, all-or-none
by (3).  (5) the cells below `R_k` are `B_{2k+2}..B_{|N|}`; retained cells
with letter in `{0,2}` among them are the `z_{2j}` zeros and the heads with
`w_{2j} = 1` of the even blocks `j > k`; cells of `R_k` itself are
non-retained.  Odd `|N|`: `R_{K-1} = B_{|N|} = {-u}`, empty sum, and `T[u][-u]
= e_u XOR 3 != 0` agrees.  All OK.

**D2.**  `F_k + F_{k+1}` is the single term `j = k+1`: OK.  Boundary: when
`2k+2 = |N|` (so `|N|` even, `k+1 = K`), `F_K := 0` matches the empty sum;
when `|N|` is odd, `2k+2 <= |N|-1` gives `k+1 <= K-1`, a real run: OK.
`F_k = [R_k subset of Z_u]` needs `R_k` nonempty, which holds (it contains
`q_{2k+1}`): OK.  Runs and `z_i` are functions of `Z_{u-1}`: OK.  So the
pair determines every even `w_i`: OK.

**D3.**  `e_u = 1 + [|N| odd]`, `|N| = m - |Z_{u-1}|`; `H_u` from retained;
`E_u(d)` from (6.1) with the even `w_i` from D2; cell from `(H, E)`: OK.

**D4.**  Column `u'` on `[-u'-1, n-1]` is the window of column `u'+1`
(bottom cell `e_{u'}` binary); A gives `e_{u'+1}` (existence and uniqueness);
0.3 gives column `u'+1` on `[-u'-2, n]`; induction on `u'`: OK.  The
"whole forced future" of the lemma text is made precise as symbols, columns
on `[-u'-1, n]` and hits; cells above depth `n` are excluded (scope remark
2).  This is a narrowing of vague wording, stated openly, not a gap.
Independently checked literally (all later symbols and hits to `u = 2n+2`
across all sources sharing a key, `verify_logic.log`, V1 PASS).

**D5.**  Toggling the even-bit of `q_i` changes only `b` at `q_i`; `e_u`
depends only on `|N|` (A, which as noted holds for arbitrary window content);
`H_u` depends only on the zero pattern (B); `E_u(d)` changes by `h(q_i) = [i
even]` for `d > q_i` (Lemma M); above `n` the recurrence reads only `T[u][n]`
and cells outside the window: OK.  Top window cell nonzero is `q_1`, odd: OK.

**Theorem E, part (e).**  `tau` (toggle the head of `B_2`) fixes every
nonzero position, hence every `z_i` and every `w_i` with `i != 2`, flips
`w_2`, is a fixed-point-free involution of `{|N| >= 2}`, flips `Phi`: OK.
`|N| = 0`: `Phi = m` (checked against the Moore step: `h` stays 1, `F`
increments each letter).  `|N| = 1`: `Phi = z_0` (checked: `h = 0` below and
at the nonzero letter, `h = 1` above it).  Census `[m even] + 2 ceil(m/2)`
against `[m odd] + 2 floor(m/2)`, difference 1 for both parities: OK.  `N_0
+ N_1 = 3^m`: OK.  Independently confirmed by the bare Moore machine to `m =
13` (`verify_logic.log`, V4 PASS) and by the lemma's transfer-matrix gate to
`m = 40` (`q2_gate_maxn12.log`, G5).

**Quantifiers.**  Every derivation is uniform in `n`, `u`, `m`.  The finite
runs S3 to S6 are labelled gates and are not cited as evidence for any step.
The lemma's "in particular any forced-orbit prefix" is covered by "any binary
word".  `c` does not enter (a) to (e), as the proof says.

**Claims outside BRIEF section 2 or the text.**  None found.  The Moore step
and the `(H)`, `(E)` integrals of BRIEF section 2 are re-derived, not cited.

## 2. Findings

### 2.1 Wrong reason in commentary (does not affect the lemma)

Section 6, Remark, quoted:

> "D5 is the exact reason the single pattern `Z_{u-1}` does not determine
> column `u`: its fibre is parametrised by the odd-indexed even-bits that the
> map discards"

Section 9, quoted:

> "a single zero pattern `Z_{u-1}` does not determine column `u` because the
> odd-indexed even-bits are discarded (D5), and their number `ceil(|N|/2)` is
> unbounded."

This attributes the non-determination to the wrong parity.  By D3 column `u` on
`[-u-1, n]` is a function of `(Z_{u-1}, even-indexed w_i)`, and by D5(2) the
even-indexed bits are read.  So `Z_{u-1}` fails to determine column `u`
exactly because the even-indexed bits vary inside its fibre.  The
odd-indexed bits being discarded (D5(1)) is a different fact: it is why the
map window -> column `u` is not injective (the level-0 fibres of the lemma's
"value" paragraph), and it is precisely what does NOT obstruct determination.

Measured, `verify_logic.py` V2 (`verify_logic.log`): over all binary sources
`n <= 11`, `u = n..2n+2`, there are 14,488 `(n, u, Z_{u-1})` fibres, 940 of
them containing more than one column `u`; in every fibre the number of
distinct columns equals the number of distinct even-indexed even-bit
vectors, every column carries exactly one even-indexed vector, and 329
columns are shared by windows that differ only in odd-indexed even-bits.

Consequence: none for (a) to (e).  The sentence is outside the lemma
statement and outside the derivation; the section 9 comparison with the
killed row "Bare holonomy-defect word" remains correct in its conclusion
(the pair is lossless, the single pattern is not) with the reason corrected
to "because the even-indexed even-bits, which column `u` reads, are not
carried by `Z_{u-1}`".  Recommended one-line fix in a future revision.

### 2.2 Presentational, no logical consequence

- Proposition A is stated "for a binary prefix", but D5 applies it to a
  toggled window that need not be realisable.  A's proof uses only Lemma H
  at `d = n`, which holds for any window content, so the use is valid; the
  hypothesis is narrower than the use.
- Lemma (d) says "it determines every `w_i` with `i` even" with "it" = `Z_u`;
  D2 needs `(Z_{u-1}, Z_u)`.  In the lemma's context the window (hence
  `Z_{u-1}`) is fixed, so the reading is consistent; the proof is explicit.
- Section 8 table gives the mutation control range as `u <= 6`; the mutate
  log carries no args header.  It fires at the first word `(1,)`, so the
  range is moot.  Reproduced: `rerun_rbf_structural_mutate.log`,
  `AssertionError: ('b', (1,), 1, -1)`, exit 1.
- The lemma's kill-test note "about 5 minutes at n = 12" overestimates:
  `q2_gate.py --max-n 12` ran in 7 s (`q2_gate_maxn12.log`).

## 3. Runs (all logs in this directory, all scripts named)

| log | script | what | result |
|---|---|---|---|
| `rerun_rbf_structural_checks.log` | proof's `rbf_structural_checks.py --ub 12 --u4 6 --m 10` | S1 to S6 | ALL PASS, 11 s, exit 0 |
| `rerun_rbf_structural_mutate.log` | same, `--mutate` | control | fires `('b', (1,), 1, -1)`, exit 1 |
| `verify_logic.log` | `verify_logic.py --nb 11 --u4r 40 --samples 300 --seed 1 --m 13` (mine) | V1: (a)(b)(c)(d) from the lemma text on 53,244 (source, u) pairs, 15,682 pair keys each with one column and one forced future to `u = 2n+2`; V2: fibre probe of 2.1; V3: Lemma H, E on 97,200 cells of random four-state prefixes, `u = 40`; V4: Theorem E by the bare Moore machine to `m = 13` | ALL PASS, 7 s, exit 0 |
| `q2_gate_maxn12.log` | lemma kill test `q2_gate.py --max-n 12` | G1 to G4 on 212,988 columns, 56,064 distinct pairs; G5 brute to 10, transfer to 40 | PASS, exit 0 |
| `q2_gate_random_n30-50.log` | lemma kill test `q2_gate_random.py --n 30 40 50 --samples 3000 --seed 1` | G1 to G4 on 192,000 + 252,000 + 312,000 columns | PASS, exit 0 |
| `q2_pieces_maxn6.log` | lemma kill test `q2_pieces.py --max-n 6` | P1, P2, affine all-ones on retained bits, `n <= 6`, both `c` | PASS, exit 0 |

## 4. Position against BRIEF

Implication: none of `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)`, P1; the proof
says so and claims nothing more.  Obstructions A to H: the proof's
assignments (A, B, C, E, F, G not applicable; D and H evaded) are correct for
an identity between adjacent columns derived from F1 and F2.  Nearest killed
row: "Bare holonomy-defect word"; the proof's distinction (pair lossless,
single pattern not, no bounded quotient) stands, with the reason corrected as
in 2.1.

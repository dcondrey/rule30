# Verdict on PROOF.md for lemma `retained-bit-form` (LOGIC lens)

Date: 2026-09-03.  Verifier output directory: this directory.

Proof under review:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-quadratic-prove-retained-bit-form-direct/PROOF.md`

**Verdict: SOUND.**  Every inference in Lemmas 1 to 12 and Corollary 6.1 was
checked step by step against the BRIEF section 2 definitions and the three
local facts (F1) to (F3).  No step fails, no quantifier silently changes from
"tested n" to "all n", and no claim outside BRIEF section 2 or the text's own
derivations is consumed.  One display formula (Corollary 5.1, line 200) is
written with the wrong complement; it is not load-bearing and the corrected
form is what the surrounding sentence and the Moore step actually give.  Two
wording scope points are recorded below; neither is a gap in the proof.

## 1. Files I wrote (all numbers below cite these)

| File | What it does |
|---|---|
| `rerun_rbf_direct_gate.log` | My own re-run of the author's `rbf_direct_gate.py` with defaults: `ALL PASS [35s]`, same counts as the author's log (90114 pairs, 9830 pair keys, 7745 single keys, 1492 ambiguous, max fibre 7, 88572 and 87380 windows, `(3^m+1)/2` for m <= 10, d(m) = 1 for m <= 60). |
| `verify_logic_checks.py`, `verify_logic_checks.log` | V1 Corollary 5.1 as displayed vs corrected (105,464 window cells, all binary words u <= 9, all n <= u); V2 independent characteristic polynomial of the transfer matrix by expansion of det(xI - A) over Z and exact matrix powers to m = 40; V3 Lemma 10 at all depths of column u (8194 (word, n) pairs, 90,962 odd-index replacements). |
| `v4_depth_scope.py`, `v4_depth_scope.log` | Which cells past depth n the key (n, u, Z_{u-1}, Z_u) does and does not determine (1127 keys, u <= 9, n < u). |

## 2. Step-by-step audit

Notation as in PROOF.md.  "OK" means the inference follows from what precedes
it with no additional input.

**Section 1, (C1) to (C4).**  Four-value arithmetic, OK.  (F1), (F2) are the
BRIEF section 2 decoupling; (F3) is the BRIEF's `T[u][-u] = e_u XOR 3`.  The
remark that `CONE[1] = CONE[3]` follows from (F1), (F2), (C1): OK.

**Lemma 1 (locality).**  Induction on d; uses `d - 1 in [-u, n-1]` and
`n <= u` so that the window lies inside column u-1's range `[-u, u-1]`.  OK.
The "closed system" corollary is a direct induction on v.  OK.

**Lemma 2 (H integral).**  Base `h(-u) = 1 + H(e_u)` from (F3); step from
(F1).  Matches BRIEF `(H)` after `(d+u+1) = 1 + (d+u)`.  OK, and valid for
every `e_u in {0..3}` as stated.

**Lemma 3 (E integral).**  Base `F(-u) = E(e_u XOR 3) = E(e_u) = 0` needs
`e_u in {1,2}`, which the lemma restricts to; step from (F2).  OK.  The
Moore form is a restatement of Lemmas 2 and 3.  OK.

**Lemma 4 = (a).**  `h(n) = 1 + H(e_u) + m + |Z|` is affine in `H(e_u)` with
coefficient 1, so exactly one of `H = 0, 1` gives `h(n) = 1`; `m + |Z| = N`
mod 2.  OK.  Existence and uniqueness of the forced symbol are both proved,
not assumed.  The "forced orbit stays binary" remark is an induction with the
hypothesis `u + 1 >= n` and binary prefix, both preserved.  OK.

**Lemma 5 = (b).**  Substitution `H(e_u) = n + u + |Z|` into Lemma 2,
`2u = 0`, `|Z| - Z(<d) = Z(>=d)`, and `(n-d) - Z(>=d)` = number of nonzero
cells in `[d, n)`.  The three cases (d = q_i; d zero below q_i; d zero above
q_1) are exhaustive for `d in Win` and each gives `h = 1 + (count)`.  OK.
`h(n) = 1` recovers the forcing.  OK.

**Corollary 5.1.**  DEFECT, display only.  Line 200 reads
`1 + h(d) + h(d+1) = [T[u-1][d] != 0]`.  From Lemma 5 the counts at d and
d+1 differ by `[d in Nz]`, so `h(d) + h(d+1) = [T[u-1][d] != 0]` and
`1 + h(d) + h(d+1) = a_d = [T[u-1][d] = 0]`; the text's own justification
("the Moore step h(d+1) = h(d) + 1 + a_d read backwards") gives the corrected
form.  `verify_logic_checks.log` V1: the displayed formula fails on all
105,464 cells checked, the corrected one holds on all of them.  The only
downstream use (Lemma 9(ii), line 362: the h profile determines Z) is true
under either sign, so nothing depends on the slip.

**Lemma 6 = (c).**  `F(n) = sum_{d in Win} h(d) b_d`, Lemma 5 restricts the
sum to retained cells, (C4) splits `b = 1` into zeros and 2-cells, retained
nonzero cells are `q_i` with i even.  OK.

**Corollary 6.1 (set and primed forms).**  `h(d) = 1 + N + N(<d)`, summed
over `Z union W2`, gives `(|Z| + |W2|)(1 + N) + pairs` and `1 + N = 1 + m + |Z|`.
This is the primed form the BRIEF erratum names as the only verified one;
the unprimed form is not used anywhere.  OK.

**7.1 (run structure).**  `I_0, I_1, ..., I_N` partition Win using
`q_{N+1} := -u-1` and `q_N = -u`.  Retained/non-retained by block follows from
the definition.  Maximality of each `R_i`: the separating blocks `I_{i-1}`,
`I_{i+1}` each contain a nonzero cell and are retained.  OK.

**Lemma 7.**  (i) `e_u in {1,2}`; (ii) (C1) plus Lemma 5; (iii) `[-u, d)`
splits as `[-u, q_{i+1}]` plus a non-retained tail inside `R_i`; (iv) is the
conjunction.  OK.  The remark that the bottom run has `F_N = 0` and hence
`T[u][-u] = 1` when N is odd is consistent with `e_u = 2` and `2 XOR 3 = 1`.

**Lemma 8 (read-out).**  `F_{i-1} - F_{i+1}` counts retained `b = 1` cells in
`(q_{i+2}, q_i] = R_{i+1} union I_i`, `R_{i+1}` contributes 0, `I_i`
contributes `z_i + w_i`.  The edge case `i = N` (even) with `F_{N+1} := 0` and
`I_N = {-u}` is handled.  `z_i` and the `q_i` are functions of Z.  OK.

**Lemma 9.**  (i) explicit formula for `F(d)` from Lemmas 3 and 5, `h(d)`
from Lemma 5, `e_u` from Lemma 4.  (ii) equivalence of the three
descriptions, injectivity of even bits into `Z_u` from Lemma 8.  (iii)
induction with Lemmas 1 and 4.  OK.  The `2^floor(N/2)` image count is stated
for the free letter space where every even-bit vector is trivially realised.
OK.

**Lemma 10.**  Odd-indexed nonzero replacements keep every `a_d`, N, `e_u`,
every `h(d)`, and enter `F` only as `h(q_i) b_{q_i}` with `h(q_i) = 0`.
Converse: even-indexed flip changes the summand `b_{q_i}` with `h(q_i) = 1`.
OK.

**Lemma 11 (relaxed space).**  `h` before letter k is `1 + N + nonzero(<k)
= 1 + nonzero(>=k)`; the Lemma 5 case analysis and the Lemma 6 sum use only
that display.  OK; neither used a nonzero bottom letter.

**Lemma 12 = (e).**  Three classes by N.  `N >= 2`: `Phi = const + sum_{i
even} w_i` has coefficient 1 on `w_2`, so exactly `2^{N-1}` zeros per pattern;
`sum_{N>=2} C(m,N) 2^{N-1} = (3^m - 1 - 2m)/2`.  `N = 1`: `Phi = m - p`, zero
iff `p = m mod 2`, `ceil(m/2)` positions times 2 letters.  `N = 0`:
`Phi = m`.  Total `(3^m + 1)/2` for both parities of m.  OK, uniform in m.
Remarks 12.1 and 12.2 are correct arithmetic on the same decomposition and
are labelled as outside the lemma.

**Transfer-matrix cross-check.**  Final `h = h_0 + N`, so the forced start
is the unique `h_0` reaching `h = 1`; `d(m) = r^T A^m s`; Cayley-Hamilton
recurrence with root 1; `d(1..4) = 1`.  I recomputed the characteristic
polynomial by direct expansion of `det(xI - A)` over the integers
(`verify_logic_checks.log` V2): `[1, -2, -4, 2, 3]`, `p(1) = p(3) = p(-1) = 0`,
and `N_0 = (3^m+1)/2` by exact matrix power for m <= 40.  OK.

## 3. Quantifier audit

- Every lemma is stated and proved for arbitrary `n >= 1`, `u >= n`, binary
  prefix (Lemmas 1 to 10) or arbitrary `m >= 1` (Lemmas 11, 12).  No "for the
  tested n" is promoted to "for all n".
- The gates are described as bookkeeping and the proof text never cites a
  gate as the justification of a step, except the four values `d(1..4) = 1`
  in the transfer-matrix cross-check, which is a finite exact computation
  and is anyway implied by Lemma 12.
- No existential is silently read as universal.  Lemma 4 proves both
  existence and uniqueness of the forced symbol.

## 4. Claims outside BRIEF section 2 or the text

None consumed.  (C1) to (C4) are finite arithmetic on four values; (F1) to
(F3) are the BRIEF decoupling and boundary; the triangle definition is the
BRIEF's.  The BRIEF section 3 set form is derived (Corollary 6.1), not used.
`PROOF-STATE-CAPSULE.md`'s "high-bit elimination" is cited only as agreement,
not as input.

## 5. Scope notes (not gaps)

1. **"Whole forced future" in lemma statement (d).**  Lemma 9(iii) proves
   determination of every forced symbol and every cell `T[v][d]` with
   `d <= n`.  Cells at depth `> n` of columns `u, u+1, ...` are not determined
   by the pair: `v4_depth_scope.log` gives `T[u][n+1]` differing on the equal
   key `(1, 2, (), ())` (words `12` and `22`, values 3 and 1) and
   `T[u+1][n+2]` differing on key `(2, 3, (), (-1,))`.  `T[u+1][n+1]` is
   determined (both `phi` arguments are at depth `<= n`).  The proof text is
   precise about this; the lemma's phrase should be read as "at depth `<= n`",
   which is all `(RW)` uses.
2. **"Never read by column u" in lemma statement (d).**  Lemma 10 proves the
   replacement leaves column u on `[-u-1, n]` unchanged.  Depths `> n` of
   column u read the window only through `T[u][n]`, so the full-column
   statement follows at once; `verify_logic_checks.log` V3 confirms column u
   identical on `[-u-1, u]` under all 90,962 odd-index replacements at
   `u <= 9`.  The one-line extension is not written in the proof.
3. **Free-letter-space counts in Lemma 9(ii).**  The parentheticals
   `I_N = {-u}` (lines 250, 320) use `q_N = -u`, i.e. a nonzero bottom cell.
   For a window with a zero bottom letter the same argument runs with
   `I_N = (bottom - 1, q_N]`; Lemma 11 transfers Lemmas 5 and 6 explicitly but
   Lemmas 7 to 9 only implicitly.  The image count `2^floor(N/2)` on the free
   letter space is not part of the lemma statement and is gated (L) to
   `m <= 12`; its derivation for zero-bottom windows is a routine
   modification the text does not spell out.

## 6. Formatting

No em-dash bytes in `PROOF.md` or `rbf_direct_gate.py` (grep count 0 for
both).  Every number quoted in `PROOF.md` section 11 matches
`rbf_direct_gate.log` and `rbf_direct_gate_large.log`, and my re-run
`rerun_rbf_direct_gate.log` reproduces the default log's counts exactly.

## 7. Bottom line

Sound.  The derivation of (a) to (e) is complete and uniform; the single
defect is a complement typo in the display of Corollary 5.1 that changes no
conclusion.  As the proof itself says, the lemma is an identity and implies
nothing about `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)` or P1.

# Verdict on lemma `retained-bit-form`, obstruction lens

Date: 2026-09-03.  Proof audited:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-quadratic-prove-retained-bit-form-direct/PROOF.md`.

## Verdict: SOUND

All five parts (a) to (e) are proved uniformly in `n >= 1`, `u >= n` and the
binary prefix from the BRIEF section 2 triangle and the three finite facts
(F1) (F2) (F3).  Every derivation step was re-derived by hand below and
re-checked by an independent script that does not reuse the prover's
triangle builder.  One write-up slip was found (Corollary 5.1's constant
term); it is a typo in an auxiliary corollary, its conclusion survives
either sign, and no part of (a) to (e) depends on the printed constant.

No em-dashes appear in this file.

## 1. Files written here

- `rbf_verify.py`: independent check.  Columns come from
  `psi_kernel.Endpoint` (the kernel), not from the gate's own `next_column`;
  the retained structure, run decomposition and read-out are re-implemented
  from the lemma statement; the pair-determines-future check runs to
  `u' = 2n+1` rather than the gate's three steps.
- `rbf_verify.log`: its output, 26 s, `ALL PASS`.

Run: `cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant && uv run python uc/r1-quadratic-prove-retained-bit-form-direct-verify-obstruction/rbf_verify.py`.

## 2. Step-by-step audit of the derivation

Notation as in PROOF.md.  Each line is the check I did, not a quote.

- (C1) to (C4): four-value table, correct.  `T = 0 iff (H, E) = (0, 1)`.
- (F1) (F2) (F3): re-checked from `CONE` and `BOUNDARY` (`rbf_verify.log`
  line V0, 16 pairs and 4 values).
- Lemma 1 (locality): trivial induction; `T[u][d]` for `d <= n` reads
  column `u-1` only on `[-u, n-1]`.  Correct.
- Lemma 2: `h(-u) = 1 + H(e_u)` by (F3), step adds `1 + a_d` by (F1).
  Correct.
- Lemma 3: `F(-u) = E(e_u XOR 3) = E(e_u) = 0` for binary `e_u`; step adds
  `h(d) b_d` by (F2).  Correct.  This is the only place `e_u` binary is used
  for (a) to (c).
- Lemma 4 = (a): `h(n) = 1 + H(e_u) + m + |Z|`, affine in `H(e_u)` with
  coefficient 1, so exactly one of `e_u in {1,2}` works and it has
  `H(e_u) = m + |Z| = N (mod 2)`.  `e_u = 2 iff N odd`.  Correct.
- Lemma 5 = (b): substitution gives `h(d) = 1 + #nonzero in [d, n)`; the
  three retained clauses are the three cases.  Correct.  The `d = n` case
  is the forcing.
- Corollary 5.1: **typo**.  The display reads
  `1 + h(d) + h(d+1) = [T[u-1][d] != 0]`.  From the Moore step
  `h(d+1) = h(d) + 1 + a_d` one gets `1 + h(d) + h(d+1) = a_d = [T[u-1][d] = 0]`.
  `rbf_verify.log` line V1: the printed form holds on 0 of 3,686,392 window
  cells over all binary words `u <= 13`, all `n <= u`; the corrected form
  holds on all 3,686,392.  The corollary's conclusion (the `h` profile of
  column `u` and `Z_{u-1}` determine each other) holds under either
  constant, and the only downstream use is Lemma 9(ii), which needs only
  that conclusion.  Not load-bearing.
- Lemma 6 = (c): `F(n) = sum h(d) b_d = #{retained : b = 1}` and (C4)
  splits retained cells into zeros (`b = 1`) and even-indexed `q_i`
  (`b = w_i`).  Correct.
- Corollary 6.1: `h(d) = 1 + N + N(<d)`, sum over `Z union W2` gives
  `(|Z| + |W2|)(1 + N) + pairs`, `1 + N = 1 + m + |Z|`.  Matches the BRIEF
  section 3 set form and the primed form exactly.  Correct.
- 7.1 run structure: `I_i = (q_{i+1}, q_i]` partition the window,
  `I_0` and even `I_i` retained, odd `I_i` non-retained, each odd block
  maximal because its neighbours contain `q_{i-1}` resp. `q_{i+1}`.
  `I_N = {-u}` uses `q_N = -u`, i.e. `e_{u-1}` nonzero, true on real
  columns.  Correct.
- Lemma 7: (ii) is (C1) with Lemma 5; (iii) constant `F` on a run because
  non-retained cells contribute `h b = 0`; (iv) follows.  Bottom-run check
  `T[u][-u] = e_u XOR 3` for both parities of `N`: consistent.  Correct.
- Lemma 8 (read-out): `F_{i-1} - F_{i+1}` counts retained `b = 1` cells in
  `R_{i+1} union I_i`, which is `z_i + w_i`.  The `i = N` even case with
  `F_{N+1} := 0` and `I_N = {-u}` checks.  Correct.
- Lemma 9: (i) column `u` from `(Z_{u-1}, even bits)` via `h` and the
  partial `F` sums; (ii) the converse via Cor 5.1's conclusion and Lemma 8;
  (iii) induction with Lemmas 1 and 4.  Correct.  The lemma statement's
  phrase "the whole forced future" is qualified in the proof to forced
  symbols and cells at depth `<= n`; since the forced symbol sequence is
  determined and the prefix is given, the whole triangle follows, so the
  unqualified phrase is also true.  `rbf_verify.log` line V2: equal keys
  `(n, u, Z_{u-1}, Z_u)` carry equal column `u` on `[-u-1, n]` and equal
  forced symbols for every later column to `u' = 2n+1`, on 196,610
  `(word, n)` pairs, 17,827 distinct keys.
- Lemma 10: odd `q_i` have `h(q_i) = 0`, so their `b` is multiplied by 0
  and their `a` is unchanged by any nonzero replacement.  Correct.
  `rbf_verify.log` line V5 strengthens it: the WHOLE column `u` (all depths
  to `u`) is unchanged, 69,984 replacements, even-indexed flips always
  visible.
- Lemma 11: the `h` formula on the relaxed space uses only the forced
  start and the letter counts; the Lemma 5 and 6 case analysis never used
  `q_N` at the bottom.  Correct.
- Lemma 12 = (e): three classes.  `N >= 2`: `w_2` present so the affine
  form is non-constant, exactly `2^{N-1}` zeros per pattern; sum is
  `(3^m - 1 - 2m)/2`.  `N = 1`: `Phi = m - p`, `ceil(m/2)` positions,
  times 2 letters.  `N = 0`: `[m even]`.  Both parities of `m` give
  `m + 1` from the small classes; total `(3^m + 1)/2`.  Correct.
  `rbf_verify.log` line V4 confirms the count through `phi` for `m <= 9`
  with my own Moore code.
- Transfer-matrix cross-check: the forced-start condition is exactly
  "final `h = 1`", so the sum over `h_0` of `A^m` entries is the right
  count; characteristic polynomial `(x-1)(x-3)(x+1)^2` verified by the
  prover's gate with exact rationals.  Independent second proof, not
  needed.

## 3. Obstruction lens

**B, the Rule 90 filter.**  The argument consumes only (F1) (F2) (F3) and
the triangle definition.  Transported to any other four-state rule it
yields whatever identity that rule's local laws imply; it makes no claim
about a centre column, periodicity, growth, or exclusion, so it cannot
prove a false statement about Rule 90.  To make this concrete rather than
asserted, `rbf_verify.log` line V6 runs the whole retained-bit derivation
on a synthetic rule that satisfies (F1) and (F3) but has `E(phi) = E(r)`
(no shear): (a) and (b) still hold on all 3,586 pairs `u <= 8` (they use
only (F1) (F3)), while (c) and (d) fail on 1,793 of 3,586.  So the identity
is a genuine consequence of the specific shear law (F2) of `CONE`, not a
tautology of forcing; and it is an identity, which is why the filter has
nothing to bite on.  "Not applicable" is the right label.

**Proves too much?**  No.  The lemma is a lossless re-encoding, not a
quotient, bound or independence statement.  It is consistent with every
killed row: `Z_{u-1}` alone is ambiguous (prover's gate: 1,492 of 7,745
keys at `u <= 12`), the pair `(Z_{u-1}, Z_u)` grows with `u`, the recursion
`Z_{u+1} = Psi(Z_{u-1}, Z_u)` is not claimed bounded or local, and (e) is
stated on the relaxed letter space with section 9 explicitly refusing to
transfer it to the orbit (Remark 12.2 shows the count already changes
under the bottom-nonzero restriction).  The `value` field's reading of (e)
as "the precise content of the one-bit term" in the 1.415 bits per column
mechanism is a heuristic gloss outside the lemma; the proof does not use
it.

**Small-n sanity.**  BWH+ constants exist at `n = 5` (2 sources) and
`n = 6` (3 sources).  The lemma's domain includes them and it excludes
nothing.  `rbf_verify.log` line V3: the two `n = 5` sources `12121`,
`22121` (forced continuation `1211212`, constant `Psi = 1`) and the three
`n = 6` sources `111222`, `112122`, `211222` (continuation `12111112`,
constant `Psi = 0`) satisfy (a) to (d) on every column of their forced
orbit.  Counts match the `RESULTS-PSI-ANCESTRY-LAW.md` section 6 table
(2 and 3).  The `n = 15` near-miss `W = 111122211212112` reproduces
`Q = 12211111122111211` and diagonal `3^16 2`, and (a) to (d) hold on all
17 columns `u = 15..31`.  Nothing is wrongly excluded because nothing is
excluded.

**A** (`O(log t)` wall): not applicable; no propagation-depth claim, the
identity relates two adjacent columns at all depths `<= n` simultaneously.
**C** (single-column blindness): not applicable; no functional of the 2D
diagram, and the object is the inverse-cone kernel, not the diagram.
**D** (missing composition law): evaded; Lemmas 2 to 9 derive the
composition of `Phi` with the column map in full, and I re-derived each.
**E** (measure-zero orbit): not applicable; no measure.
**F** (free boundary of a fixed strip): not applicable; the window
`[-u, n-1]` grows with `u` and the identity holds for every `u`.
**G** (arbitrary-input measures): not applicable; no complexity measure.
**H** (finite data): evaded; the derivation is uniform and the gates are
bookkeeping on the write-up.  My own script is likewise a gate, not
evidence.

## 4. Defects found (none fatal)

1. Corollary 5.1's display has the wrong constant (`[T != 0]` should be
   `[T = 0]`, or equivalently drop the leading `1 +`).  Confirmed on
   3,686,392 cells (`rbf_verify.log` line V1).  Conclusion unaffected.
2. The lemma statement's "the whole forced future" in (d) is broader than
   the proof's precise Lemma 9(iii) (forced symbols plus cells at depth
   `<= n`); the broader reading is still true given the prefix, so this is
   an imprecision in the statement, not a gap.

## 5. Numbers cited in this file

All from `rbf_verify.log` produced by `rbf_verify.py` in this directory:
V0 16 pairs, 4 values; V2 196,610 pairs, 17,827 keys, 25 s; V1 0 of
3,686,392 printed, 3,686,392 of 3,686,392 corrected, and 0 of 1,200 versus
1,200 of 1,200 on the `n = 15` and constant-`Psi` columns; V3 17 columns,
2 and 3 constant sources; V4 `m <= 9`; V5 69,984 replacements; V6 3,586
pairs, 1,793 failures on the control rule.  The prover's numbers 1,492 and
7,745 are from `rbf_direct_gate.log` in the proof directory.

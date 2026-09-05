# Verdict on the proof of `retained-bit-form` (obstruction lens)

Date: 2026-09-03.  Lemma id: `retained-bit-form`.
Proof audited: `uc/r1-quadratic-prove-retained-bit-form-structural/PROOF.md`.

## Verdict: SOUND

All five parts (a) to (e) are proved as stated.  Every step is either the
finite fact F1 (the 16-entry decoupling table, which I show determines `CONE`
outright), the boundary fact F2, or an induction written out in full.  No
step names a lemma instead of deriving it.  The exhaustive runs are gates and
the proof does not rest on them.  I re-derived each step by hand (section 2
below), re-implemented every identity from the lemma statement alone with no
shared code, and reran the lemma's own named kill tests; nothing fired.

The lemma is an identity between adjacent columns of the four-state kernel.
It implies none of `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)`, P1, and the proof
says so.  Under the obstruction lens it passes A, C, E, F, G as not
applicable, D and H as evaded by derivation, and B vacuously: the Rule 90
analogue of the argument yields a (different, linear) identity that is also
true and also says nothing about periodicity (section 4).

## 1. Files written here

| file | what |
|---|---|
| `verify_rbf_obstruction.py` | independent re-implementation, checks V0 to V6 (own triangle, own retained definition, own Moore `Phi`) |
| `verify_rbf_obstruction.log` | `--ub 12 --m 10 --fib-n 9`, 17 s, ALL PASS |
| `verify_rbf_obstruction_fib12.log` | `--ub 8 --m 6 --fib-n 12`, fibre and lossless-pair census along forced orbits to `n = 12`, ALL PASS |
| `rerun_rbf_structural_checks.log` | the proof's own script, `--ub 12 --u4 6 --m 10`, reproduced, ALL PASS in 10 s |
| `rerun_rbf_structural_mutate.log` | the proof's control (`--mutate`), fires at `('b', (1,), 1, -1)` as claimed |
| `rerun_q2_gate_n12.log` | the lemma's named kill test `uc/r1-quadratic/q2_gate.py --max-n 12`: G1 to G4 on 212,988 columns PASS, G5 to `m = 40`, 9.4 s (the lemma estimated 5 minutes; it is 9 s) |

Every number below cites one of these logs.

## 2. Step-by-step audit of the derivation

Notation as in the proof.  `H = T >> 1`, `Lo = T & 1`, `E = 1 + H + Lo`.

**F1 determines the table.**  Given `(l, r)`, F1 fixes `H` and `E` of
`phi(l, r)`, and `T = 2H + (1 + H + E mod 2)` recovers the cell.  So F1 is
not merely a property of `CONE`, it is equivalent to the whole table; I
rebuilt `CONE` from the two F1 formulas cell by cell and it agrees on all
16 entries, and `BOUNDARY[s] = s XOR 3 = CONE[3][s]` (V0,
`verify_rbf_obstruction.log`).  Consequently the proof has exactly one finite
input, the table, and everything else is derivation.  F2 follows from F1 at
`l = 3`: `H` flips, `E` is unchanged, so `Lo` flips and the output is
`r XOR 3`.

**Lemma H, Lemma E.**  Induction on `d` from `-u` to `u`.  Base uses F2
(`H(e XOR 3) = 1 + H(e)`, `E(e XOR 3) = E(e)`), step uses F1.  The left
parent `T[u-1][d]` exists for `d in [-u, u-1]`, which is exactly the range
the step needs.  Correct.  Both hold for arbitrary four-state prefixes and
arbitrary `e_u`, as the proof says; the binary case has `E(e_u) = 0`.

**Proposition A (part a).**  `H_u(n) = H(e_u) + (n+u+1) + |Z|` is Lemma H at
`d = n`, and `|Z|` does not depend on `e_u`.  `H(1) = 0`, `H(2) = 1`, so
exactly one binary `e_u` gives `H_u(n) = 1`, with
`H(e_u) = n + u + |Z| = m + |Z| = |N| (mod 2)`.  Correct.

**Lemma M.**  Start `(1 + H(e_u), 0) = (1 + |N|, 0)` by F2 and A; step by F1.
Correct.  The letter space `{0, 2, x}^m` with the forced start is a proper
extension of the realised windows; Propositions B and C are proved on it.

**Proposition B (part b).**  `h_{j+1} = h_j + [q_j != 0]` and
`h_0 = 1 + |N|`, so `h_j = 1 + #{i >= j : q_i != 0}`.  In block terms a cell
of `B_i` (`i >= 1`) has exactly `q_1, ..., q_i` at or above it, so `h = 1 + i`;
a cell of `B_0` has none, `h = 1`.  Retained means `B_0` or even `i`.  At
`j = m`, `h_m = 1`, which is the pin.  Correct.  My implementation computes
"retained" directly from the lemma's words (parity of the number of nonzero
window cells at or above the cell, counting the cell itself) and never builds
blocks; it agrees with `H(T[u][d])` on every cell of 90,114 `(word, n)` pairs
(V1).

**Proposition C (part c) and Corollary C'.**  `F_m = sum_j h_j b(q_j)` with
`b = 1` on `{0, 2}`, so `Phi` counts retained cells with letter in `{0, 2}`:
retained zeros plus even-block heads equal to `2`.  C' rewrites
`h(y) = 1 + #{x in N : x >= y} = 1 + |N| + #{x in N : x < y}`; the case
`y in W2` (where `y` itself is in `N`) is handled correctly because the
complement identity is exact for both `y in Z` and `y in W2`.  Summing gives
BRIEF section 3's set form.  This upgrades the 131,580-check verification to a
derivation.  Correct.

**Proposition D1.**  (0.1) `T = 0 iff H = 0 and E = 1` (checked: `T = 0`
has `E = 1`, `T = 1` has `E = 0`).  `E_u` is constant on a non-retained run
because (6.1) counts only retained cells with letter in `{0, 2}` strictly
below the cell, and a run contains no retained cell.  So `Z_u` on
`[-u-1, n-1]` is a union of complete odd blocks, and `e_u != 0` excludes
`-u-1`.  The formula for `F_k` sums the even blocks strictly below the run.
Correct.  V1 checks `d1` on every window (no partial run, no zero outside a
run, no retained zero of column `u`).

**Proposition D2, D3.**  `F_k + F_{k+1} = z_{2k+2} + w_{2k+2}` is a
telescoping difference; the boundary convention `F_K = 0` matches the empty
sum for `|N|` even, and for `|N|` odd the last even index is `|N| - 1` so the
convention is never used.  D3 then rebuilds `(H_u, E_u)` on `[-u-1, n]`.
Correct.  V1: 9,830 distinct `(n, u, Z_(u-1), Z_u)` keys at `u <= 12`, each
with one column `u` on `[-u-1, n]` and one `(e_(u+1), Z_(u+1))`, the latter
being the second-order recursion in the lemma's "value" text
(`verify_rbf_obstruction.log`).

**Proposition D4.**  Induction on `u'`: column `u'` on `[-u'-1, n-1]` is the
window of column `u'+1` (bottom cell `e_{u'}` is binary), A gives the next
symbol, 0.3 gives the next column on `[-u'-2, n]`.  Correct, and the proof's
gap remark 2 scopes "the whole forced future" correctly: columns on
`[-u'-1, n]` and hits, not cells above depth `n`.

**Proposition D5.**  A toggle of the even-bit of `q_i` changes `b` at `q_i`
only and no `a`; `e_u` and the `H` profile depend on the zero pattern only;
`E_u(d)` shifts by `h(q_i) = [i even]` for `d > q_i`.  Above depth `n` the
column is computed from `T[u][n]` and cells outside the window, so the whole
column is unchanged for odd `i`.  Correct.  V1 checks this on free windows
with the cells above the window held fixed and compares the whole column
`[-u-1, u]`: 648,434 odd-indexed toggles invisible, including all 67,239
windows whose top cell is nonzero; 603,132 even-indexed toggles change
`T[u][n]`.

**Theorem E (part e).**  The `q_2` toggle preserves the positions of all
nonzero letters, hence all `z_i` and all `w_i` with `i != 2`, and flips
`w_2`, hence `Phi`; fixed-point-free, so `|N| >= 2` is balanced.  `|N| = 0`:
`Phi = m`.  `|N| = 1`: `Phi = z_0`, `z_0 in [0, m-1]`, two letters.  The
census `([m even] + 2 ceil(m/2), [m odd] + 2 floor(m/2))` differs by 1 for
both parities of `m`.  Correct.  V2 reproduces `N_0 = (3^m + 1)/2`, the
involution, and the `|N| <= 1` census for `m <= 10`; the transfer-matrix
route in `rerun_q2_gate_n12.log` agrees to `m = 40`.

**Nothing "clearly" or "by a standard argument" appears.**  I looked for
implicit uses of properties of realised windows inside the letter-space
propositions (B, C, E) and found none: they use only the step and the start.

## 3. Obstructions A to H

**A, `O(log t)` wall.**  Not applicable.  The statement relates column `u-1`
on `[-u, n-1]` to column `u` on `[-u-1, n]`; there is no propagation-depth
claim and no trace anchoring.

**B, Rule 90 filter.**  Passed vacuously; see section 4.  The lemma proves
nothing about any centre column, so an argument of its type applying to
Rule 90 is not a defect; it would be a defect only if the lemma were used to
conclude non-periodicity, which it is not and cannot be.

**C, single-column blindness.**  Not applicable.  No functional of the 2D
diagram is used; the objects are two adjacent columns of the kernel.

**D, missing composition law.**  Evaded.  The composition of the pin with the
column map is written out (Lemma M, Propositions B, C, D1 to D3), and the set
form of BRIEF section 3 is derived (C') rather than cited as verified.  The
one place a reader might expect a named law, "`Z_{u+1} = Psi(Z_{u-1}, Z_u)`",
is constructed explicitly: D3 gives the column, D1(4) applied one level up
gives the zero set.

**E, measure-zero orbit.**  Not applicable.  No measure, no ensemble.

**F, free boundary of a fixed strip.**  Not applicable.  The window
`[-u, n-1]` has length `n + u` and grows with `u`; the identity is stated and
proved for every `u >= n`.  Nothing is truncated at a fixed depth.

**G, arbitrary-input measures.**  Not applicable.  No complexity measure.

**H, finite data.**  Evaded.  The only finite input is the 16-entry table
(equivalent to F1, section 2 above); the rest is induction uniform in `n`,
`u`, `m`.  The exhaustive runs (the proof's S3 to S6, my V1 to V5, the
lemma's `q2_gate`) are gates.

## 4. Rule 90 transport (obstruction B, applied concretely)

The kernel's carry macro is `2 (c XOR (a OR b)) + (d XOR (c OR a))`; the
`OR` is Rule 30's nonlinearity.  Replacing `OR` by `XOR` gives the Rule 90
analogue of the same macro, whose forward actions are still permutations, so
the analogous `CONE90` exists.  V6 (`verify_rbf_obstruction.log`):

- F1 as stated fails on 6 of the 16 pairs of `CONE90`, so the lemma's
  identity does not transport verbatim; it is specific to `CONE`.
- `CONE90` is affine over GF(2) in the four input bits, so the Rule 90
  analogue of the whole argument is a linear one: every cell of column `u` is
  an affine function of the window bits and `e_u`, the forced symbol exists
  and is unique on all 18,434 `(word, n)` pairs with `u <= 10`, and the
  analogue of (d) (the next column is a function of the previous column plus
  the forced symbol) holds trivially.

So the transported argument proves a true identity for Rule 90 and nothing
false, and Rule 90's eventually periodic centre column is untouched by it.
That is the correct reading of the filter here: adjacent-column identities of
this kind are compatible with both periodic and non-periodic behaviour, which
is exactly why the lemma implies none of the chain and why the proof says so.

## 5. Small-`n` sanity

`RESULTS-PSI-ANCESTRY-LAW.md` section 6 records constant `Psi` sources at
`n = 5` (two) and `n = 6` (three), the finitely many exceptions below
`(BWH+)`'s `n >= 7`.  V4 (`verify_rbf_obstruction.log`) recovers exactly
those: `n = 5`: `12121`, `22121` (`Q = 1211212`, `Psi = 1^7`); `n = 6`:
`111222`, `112122`, `211222` (`Q = 12111112`, `Psi = 0^8`); `n = 7`: none.
Along each of these forced orbits, at every `u = n, ..., 2n+1`, part (a)
gives the recorded `Q`, part (b) gives the `H` profile, and part (c) gives
the recorded constant `Psi` cell by cell.  The lemma excludes nothing; it is
an identity, and the identity holds on the exceptional orbits as it must.
All five have non-hard-core continuations (a `11` inside `Q` or at the
junction), consistent with the ablation in `RESULTS-RW-LINEAR-SLACK.md`
section 9.1 that hard-core is what removes them from `(RW)`.

V3 ties my independent triangle to the repository's `psi_kernel.psi`: forced
continuation and hit word agree on all 8,190 sources with `n <= 12`.

## 6. Does it prove too much?

Two consequences of (d) were checked against the killed rows.

- A single `Z_{u-1}` must NOT determine column `u` (row "bare
  holonomy-defect word").  V5: at `n = 9`, 141 of 1,709 single-pattern keys
  have more than one successor column, max fibre 6; at `n = 12`, 704 of
  12,649, max fibre 7 (`verify_rbf_obstruction_fib12.log`); `q2_gate` at
  `n <= 12` reports 3,260 of 51,988 keys, max 7 (`rerun_q2_gate_n12.log`).
  D5 predicts these fibres (odd-indexed even-bits are discarded) and the
  lemma does not claim otherwise.
- The pair must be lossless, not a quotient (row "fixed finite quotient").
  V5: at every level `u = n, ..., 2n+1` and every `n <= 12`, the number of
  distinct `(Z_{u-1}, Z_u)` pairs equals the number of distinct columns `u`
  (for example `n = 12`: 1,145 at `u = 12` down to 904 at `u = 25`).  Nothing
  is contracted, so no killed contraction claim is smuggled in.

Neither (c) nor (e) asserts anything about realised windows beyond the
identity; (e) is a count on the relaxed letter space, and the proof's gap
remark 3 says so.

## 7. Wording nits in the lemma statement (not defects, the proof resolves each)

1. Part (d) "it determines every `w_i` with `i` even" needs `Z_{u-1}` as well
   as `Z_u`; the next clause says "the pair", and the proof's D2 uses both.
2. `N` is used both as the count and as the set of nonzero cells in the
   statement; the proof writes `|N|` for the count throughout.
3. "The whole forced future" is scoped by the proof (gap remark 2) to the
   columns on `[-u'-1, n]` and the hits, which is all `(RW)` reads.

## 8. Reproduction

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run python uc/r1-quadratic-prove-retained-bit-form-structural-verify-obstruction/verify_rbf_obstruction.py --ub 12 --m 10 --fib-n 9
uv run python uc/r1-quadratic-prove-retained-bit-form-structural-verify-obstruction/verify_rbf_obstruction.py --ub 8 --m 6 --fib-n 12
uv run python uc/r1-quadratic-prove-retained-bit-form-structural/rbf_structural_checks.py --ub 12 --u4 6 --m 10
uv run python uc/r1-quadratic-prove-retained-bit-form-structural/rbf_structural_checks.py --ub 6 --u4 4 --m 4 --mutate
uv run python uc/r1-quadratic/q2_gate.py --max-n 12
```

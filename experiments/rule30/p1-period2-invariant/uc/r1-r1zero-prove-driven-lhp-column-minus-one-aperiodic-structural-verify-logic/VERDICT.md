# Logic verdict on PROOF.md, lemma `driven-lhp-column-minus-one-aperiodic`

Date: 2026-09-03.  Lens: LOGIC (every inference, every quantifier, every external claim).
Proof under review:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-structural/PROOF.md`.

## Verdict: SOUND, for what PROOF.md itself claims (Theorems 1, 2, Lemmas 1 to 7, Propositions A, B, Corollaries A.1, B.1), with three scope flags that must travel with it

1. The lemma AS STATED in the task is false in one clause and unproved in another; PROOF.md
   says so and proves the corrected statement.  Confirmed below (section 3).
2. One sentence in PROOF.md sections 6 and 10, repeated in the lemma's `value` and
   `nearest_killed` fields, does not follow from anything proved: "so no property of `c` or of
   the right half-plane can discharge it".  It must not enter `PATH.md` (section 4).
3. Proposition A(2) and Corollary A.1 are re-derivations of a fact already implicit in
   `PATH.md` section 2 plus Jen 1990 Proposition 3; the operational status of route R1 (the
   right-half-plane obligation) is unchanged by this proof (section 4).

Reproduction of the proof's gate log and my own validation runs:
`reproduce_verify_driven_lhp.log` (identical to the proof's log except the timing stamp) and
`logic_checks.py` with `logic_checks.log`, both in this directory.

## 1. Inference-by-inference audit of sections 1 to 5 (the theorem)

Conventions: `f(a,b,c) = a XOR (b OR c)`, `s(t+1,x) = f(s(t,x-1), s(t,x), s(t,x+1))`.  Matches
`r1zero_lib.rule30_step` (`(row << 1) ^ (row | (row >> 1))` with bit `i = s(t, i - OFF)`).

| Step | Claim | Check |
|---|---|---|
| (F0), (F1), (LP) | `f(0,0,0)=0`, `f(0,0,1)=1`, `f = a XOR g(b,c)` | Read off the definition.  Rule 90 (`g = c`) satisfies all three.  Correct. |
| Definition of `LHP_y(c)` | unique array on `x <= 0` | The recursion at `(t+1,x)`, `x <= -1`, reads `x-1, x, x+1 <= 0`, all in row `t`; induction on `t`.  Correct. |
| (ND) equivalence | not identically zero iff `y` has a 1 at some `x <= -1` or `c` has a 1 | Forward: a 1 in `y` on `x <= -1` sits in row 0, a `c_t = 1` sits in row `t`.  Backward: `y` zero on `x <= -1` and `c = 0^omega` gives zero rows by (F0) and induction.  Correct. |
| Lemma 1 | `S_t` finite | `S_0` inside `supp(y) union {0}`.  If `S_t` finite with min `m`, then for `x <= -1`, `x + 1 < m` all three arguments are at positions `< m`, so 0 by (F0); `S_{t+1}` inside `[m-1, 0]`.  If `S_t` empty, `S_{t+1}` inside `{0}`.  Correct. |
| Lemma 2 | `m_{t+1} = m_t - 1` | `m <= 0` so `m-1 <= -1` and the recursion applies at `(t+1, m-1)`; arguments `s(t,m-2) = s(t,m-1) = 0` (positions `<= -1` and `< m`) and `s(t,m) = 1`; (F1) gives 1.  For `x < m-1` all three positions `< m`, (F0) gives 0.  The cell `x = 0` (overwritten by `c_{t+1}`) is never `m-1`.  Correct. |
| Corollary 2.1 (EDGE) | `m_t = a - (t - t_0)` for `t >= t_0` | Induction from Lemma 2.  The characterisation of `t_0` (first `c_t = 1` when `y` is zero on `x <= -1`) follows from Lemma 1's empty case.  Correct. |
| Lemma 3 | `a = d XOR g(b,c)` | From (LP).  Gated `G1`.  Correct. |
| (BS) | `s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1))`, `x <= -1` | Lemma 3 applied to the recursion, which holds at every `(t+1, x)` with `x <= -1`.  Correct. |
| Lemma 4 | columns `x`, `x+1` `P`-periodic from `T_0` implies column `x-1` is | (BS) at `(t+P+1, x)`, periodicity of column `x` at `t+P` and `t+P+1` (both `>= T_0`), of column `x+1` at `t+P`, then (BS) at `(t+1, x)`.  All four times used are `>= T_0`.  Correct; the case `x = -1` reads column 0, which is `c`. |
| Corollary 5 | every column `x <= 0` `P`-periodic from `T_0` | `S(k)` to `S(k+1)` is Lemma 4 at `x = -k <= -1`.  Correct. |
| Theorem 1 | `l` not eventually periodic | `P = pq` is a common period from `T_0 = max(t_c, t_l)` (a `p`-period from `t_c` is a `pq`-period from any `T_0 >= t_c`).  Corollary 5 gives every column.  `x* = m_{T_1} - P <= -1`.  For `T_1 <= t < T_1 + P`, `m_t > x*` so `s(t,x*) = 0`; at `t = T_1 + P`, `m_t = x*` so `s = 1`.  Periodicity from `T_0 <= T_1` forces `s(T_1+P, x*) = s(T_1, x*) = 0`.  Contradiction.  Correct, uniform in all parameters; only (F0), (F1), (LP) used. |
| Theorem 2, Step 1 | strip between periodic columns eventually periodic | Interior `x` satisfies `x_1 < x < x_2 <= 0` so `x <= -1` and the recursion applies, reading `x-1 >= x_1` and `x+1 <= x_2`.  Phase-augmented state on a finite set, pigeonhole.  Correct. |
| Theorem 2, Step 3 | shifted array is `LHP_{y'}(c')` and satisfies (ND) | `x' <= -1` maps to `x <= x_1 <= -1`, where the original recursion holds; `y'` finite; (ND) via the edge visiting `x_1 + 1` (if `x_1 + 1 <= a`) or the cell `(t_0, a)` with `a <= x_1`.  Theorem 1 applied to the shifted array with `c' = ` column `x_1 + 1` (periodic by Step 2) and `l' = ` column `x_1` (periodic by hypothesis).  Correct. |

No quantifier changes: every statement is for all `y`, all `c`, all periods, all onsets; the
`G` lines are labelled gates and instances, never used as steps.  Instance validation of
Theorem 2 outside the proof's own gates: `logic_checks.log` line `CHECK L2`, 196 random
`(y, c)` with `c` eventually periodic (period `<= 6`, prefix `<= 8`), columns `-1..-8`,
`T = 2048`, eventually periodic columns found: 0.

## 2. Inference-by-inference audit of sections 6 and 7 (the consequences)

| Step | Check |
|---|---|
| Lemma 6 | Induction on `t`; for `x <= -1` all three arguments lie in `x <= 0`, where the rows agree; `x = 0` is `c*_{t+1}` on both sides.  Correct.  Gated `G4a`, `G4b`. |
| (PIN), (COUPLING) | Case split of `c*_{t+1} = l*_t XOR (c*_t OR r*_t)`.  Correct. |
| Lemma 7, `k_p >= 1` | `k_p = 0` with `p`-periodicity from `t_c` makes `c_t = 1` for all `t >= t_c`, `Z` finite.  Correct. |
| Lemma 7, bijection | `t -> t + p` maps `Z intersect [t_c, inf)` onto `Z intersect [t_c+p, inf)`: into by `c_{t+p} = c_t`, onto by `c_{t'-p} = c_{t'}` for `t' - p >= t_c`.  Order preserving; the second set omits exactly the `k_p` smallest elements of the first.  So `z_{k_0+i} + p = z_{k_0+k_p+i}`.  Correct.  Instance check: `logic_checks.log` line `CHECK L3`, 246 random eventually periodic `c` with infinite `Z`, `T = 4096`, violations 0. |
| Lemma 7, consequence | `z_{k+qk_p} = z_k + qp` by `q` applications; `u_{z_{k+qk_p}} = u_{z_k}` by `k_p` applications of the index period `q`; both need `k >= max(k_0, k_1)`, which is `z_k >= t_r`.  Correct. |
| Proposition A(1) | `Z` finite gives `c*_t = 1` for large `t`, (PIN) makes `l*` eventually `p`-periodic, against Theorem 1 (applicable: `y = delta_0` finite, `c*` eventually periodic by hypothesis, (ND) from `c*_0 = 1`, `l* = LHP_seed(c*)(., -1)` by Lemma 6).  Correct. |
| Proposition A(2) | For `t >= T = max(t_c, t_r)`: `c*_{t+Q} = c*_t`, `c*_{t+Q+1} = c*_{t+1}` since `Q` is a multiple of `p`.  One-times: (PIN) at `t` and `t+Q`.  Zero-times: `t in Z`, `t >= t_r`, so `r*_{t+Q} = r*_t` and `t + Q in Z` (Lemma 7), (COUPLING) at both.  `l*` is `Q`-periodic from `T`, against Theorem 1.  Correct. |
| Corollary A.1 | `(P1) => (R1)` vacuous; `(R1) => (P1)` by A(2).  Correct as a statement about propositions. |
| Proposition B | (1)=>(2) Lemma 6 plus the rule at `x = 0`.  (2)=>(1): the glued array has row 0 equal to `delta_0` (uses `c_0 = 1`), satisfies the recursion off column 0 by construction and at column 0 by (2); "uniqueness of forward evolution" is a one-line induction on `t` (row `t+1` is a function of row `t`), not written out but not a gap.  Correct. |
| Corollary B.1 | Both directions from Proposition B.  Correct. |

External claims used: Jen 1986 Thm 2b and Jen 1990 Prop 3 are cited as prior art only; no step
depends on them.  Pigeonhole and forward determinism are the only unproved ingredients, both
elementary.  Nothing from BRIEF section 2 is needed or used (the lemma lives in the
space-time picture, not the four-state kernel); the proof is self-contained.

## 3. The two corrections to the lemma text are correct and necessary

- **Hypothesis.**  The task's lemma reads "for every nonzero finite `y`".  `y = delta_0` is
  nonzero and finite, `c = 0^omega` is eventually periodic (period 1), and `LHP_{delta_0}(0^omega)`
  is identically zero, so `l = 0^omega` is periodic and the lemma as stated is false.
  `logic_checks.log` line `CHECK L1`: half-plane identically zero `True`, `l` eventually
  periodic `(1, 0)`.  The original proof text's phrase "which exists since `c` has infinitely
  many ones" is the unjustified step (an eventually periodic `c` need not have any ones).
  PROOF.md's replacement (ND) is exactly the hypothesis the proof uses, and it holds in the
  application (`c*_0 = 1`).
- **Clause (b)-must.**  "Any proof of P1 must use the coupling at the zero-times" is not
  derived anywhere; PROOF.md section 0 and section 7 strike it and identify its content as
  `NOT (PIN-Pi)`, which is open.  Agreed: nothing in Theorems 1, 2 or Propositions A, B says
  anything about what a proof must use.

## 4. The one step that does not follow, and the bookkeeping overreach

**Quoted step** (PROOF.md section 10, the same words in section 6's closing paragraph, in the
lemma's `value` field and in its `nearest_killed` field):

> "under its own hypothesis the zero-set obligation is provably violated inside the left
> half-plane (Proposition A), so no property of `c` or of the right half-plane can discharge it"

This "so" is a non-sequitur.  The obligation is the implication
`c* eventually periodic => r*|Z eventually periodic`.  Proposition A(2) proves
`c* eventually periodic => r*|Z NOT eventually periodic`.  Together these make the obligation
equivalent to `NOT(c* eventually periodic)`, i.e. to P1, which is Corollary A.1.  They do not
rule out a proof of the obligation: any theorem of the form "for every eventually periodic `c`
with `c_0 = 1`, `RHP_seed(c)(., 1)|Z(c)` is eventually periodic" (a property of `c` and the right
half-plane alone) would, with Proposition A(2), prove P1 outright.  Proposition A neither
proves nor refutes such a theorem.  "Cannot be discharged" is true only in the empty sense
that discharging it proves P1, which was the design of route R1 from the start (`PATH.md`
section 2: "column `-1` eventually periodic closes the problem via Jen/Kopra"; section 4:
"By section 2 that yields column `-1` eventually periodic and closes the problem").  PROOF.md
section 7 states the correct position ("Nothing here says that a P1 proof must use
(COUPLING)"); sections 6 (last paragraph) and 10 contradict it.  The register update proposed
in section 10 should drop the quoted clause.

**"R1 is equivalent to P1 rather than a route to it"** (lemma statement, consequence (a)).
Corollary A.1 is valid, but the inference to "rather than a route" is not: every subgoal of a
proof by contradiction is, as a proposition, equivalent to the theorem.  Under the hypothesis
`c*` eventually periodic, `PATH.md` section 2 already gives
`l* eventually periodic <=> r*|Z eventually periodic` (modulo the index-to-time conversion,
which is Lemma 7), and Jen 1990 Proposition 3 (`PATH.md` 8.1, PROVED, primary source read)
already gives `l*` not eventually periodic.  So Proposition A(2) was derivable before this
proof from cited theorems; what PROOF.md adds is a self-contained derivation in which Jen is
replaced by Theorem 1 on the driven half-plane, valid for every eventually periodic drive `c`
rather than only for `c*`.  That is a genuine and clean extension (Theorem 1 and 2 for
arbitrary `c`), and it is correctly labelled as Jen transferred.  It does not change what
route R1 has to prove: the right-half-plane statement "`c` eventually periodic forces `r|Z`
eventually periodic" remains the open obligation, now with the left-hand side of the
contradiction available for every candidate `c` instead of only for `c*`.  Row 1's status
should therefore stay OPEN with that note, not be rewritten as "equivalent to P1; cannot be
discharged".

## 5. Minor imprecisions, none load-bearing

- Section 8: "Proposition A ... its Rule 90 analogue ... holds with the same proof."  The
  Rule 90 analogue has no (PIN), so the finite-`Z` case A(1) has no analogue; what holds with
  the same proof is "if `c*` is eventually periodic then `r*` (on all `t`) is not", via
  `l_t = c_{t+1} XOR r_t` and Rule 90 Theorem 1.  Instance: `logic_checks.log` line `INFO L4`
  (`c* = 1 0^omega`, identity holds at every `t < 2048`, `r*` ones at `2^j - 1`, no period
  `q <= 256`).  This is consistent with `PATH.md` 9.3 row 1's note that Rule 90's zero-set
  kill condition fires verbatim.
- Obstruction table, row B: "Passed in the only sense available".  An argument that holds for
  Rule 90 fails filter B as a P1 route; PROOF.md says exactly that elsewhere (limitation
  theorem, implies none of (RW-alpha), (RW), (SEP), (PT2), P1).  The table wording should say
  "fails B as a route; recorded as a limitation theorem".
- Proposition B: "by uniqueness of forward evolution" is a one-line induction, not written out.
  Not a gap.

## 6. What is and is not established, in one place

Established (level U, uniform): Theorem 1 under (ND); Theorem 2 for arbitrary `c`; Lemma 6;
Lemma 7; Proposition A; Corollary A.1; Proposition B; Corollary B.1.  All hold for Rule 90 as
well (sections 2 to 5 use only (F0), (F1), (LP)), so none is a route to P1 and none implies
(RW-alpha), (RW), (SEP), (PT2) or P1.

Not established: the lemma's literal hypothesis "nonzero finite `y`" (false, L1); clause
"(b) any proof of P1 must use the coupling" (unproved, struck by PROOF.md itself); the
register gloss "no property of `c` or of the right half-plane can discharge it" (does not
follow); "R1 is not a route to P1" (does not follow; R1's obligation is unchanged).

## 7. Files written here

- `logic_checks.py`, `logic_checks.log`: L1 (hypothesis counterexample), L2 (Theorem 2
  instances, 196 runs, 0 periodic columns), L3 (Lemma 7 identity, 246 runs, 0 violations),
  L4 (Rule 90 instance).
- `reproduce_verify_driven_lhp.log`: rerun of the proof's `verify_driven_lhp.py`; identical to
  the proof's log line for line except the timing stamp on `FINAL`.

Reproduce:
`cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant && uv run python uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-structural-verify-logic/logic_checks.py`.

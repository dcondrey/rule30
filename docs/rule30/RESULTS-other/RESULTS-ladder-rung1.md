# R7 rung 1: the boundary pin is depth in disguise, and the tail language grows

Status: **binary question NOT resolved.  No `Thm(2)`, and no limitation
theorem.**  What rung 1 adds is a proof that the boundary pin cannot be the
thing that decides `p = 2`, a repair of the soundness control that rung 0
recorded as lost, and the measured dichotomy, which comes out on the *growth*
side rather than the stabilization side.

Date: 2026-08-30.  Code: `experiments/rule30/ladder/rung1.py`,
`test_rung1.py`.  Nothing committed.  Modal: $0.  Paid model-provider calls: $0.

## 0. The question, and the honest answer

Rung 0 left one binary question: does some finite right depth `R` kill the
`p = 2` escape (giving `Thm(2)`), or does the escape extend to every `R`
(giving a limitation theorem)?  `Thm(2)` would read, if it existed: *the
lone-seed Rule 30 centre column is not eventually periodic with period 2, for
any transient length* — via a ladder EMPTY plus the Jen 1990 Prop. 3 /
Kopra 2023 Thm 3.5 finisher forbidding two adjacent eventually periodic
columns.  **No such EMPTY was produced, so that statement is not proved and is
not claimed anywhere in this file.**

**Neither branch closed.**  The verdict is NONEMPTY at every decided `R`
(`R <= 7`), with and without the pin, so no theorem; and the tail language
keeps growing rather than stabilizing, so the escape is not R-uniform in the
sense that would prove the limitation theorem.  Section 6 states exactly what
is still missing.

The dichotomy did land on a sharper answer than "grows": the accepting tail
system carries only about `R^2.75` bisimulation classes, polynomially many,
against a `4^R` raw encoding — and the exponent is the same with and without
the boundary pin (2.761 vs 2.741).  Depth and the pin both buy polynomially
little, which is the measured form of the proof in section 2.

What did close is a narrower method-level question, and it is the reason to
read this file: **adding the boundary pin is provably equivalent to adding
part of one column of depth.**  Rung 0 section 3 retired "run the ladder
deeper"; section 2 below retires "add the pin" on the same grounds, but by
proof rather than by measurement.

## 1. PROVED: the boundary pin is exactly the extendability condition

The pin is not a Rule-30 gadget attached to the ladder from outside.  It is the
solvability condition for the one column the strip does not model.

**Lemma 1 (Extension).**  Let a letter word give `col_{R-1}` and `col_R`.  A
column `col_{R+1}` satisfying the forward rule at `x = R` exists if and only if

```text
col_R(t) = 1  =>  col_{R-1}(t) = NOT col_R(t+1)     for every t.
```

*Proof.*  The forward rule at `x = R` is
`col_R(t+1) = col_{R-1}(t) XOR (col_R(t) OR col_{R+1}(t))`.  Put
`A(t) = col_R(t+1) XOR col_{R-1}(t)`; the rule says
`col_R(t) OR col_{R+1}(t) = A(t)`.

* If `col_R(t) = 0` the left side is `col_{R+1}(t)`, so `col_{R+1}(t) = A(t)`
  is forced and always exists.  No constraint.
* If `col_R(t) = 1` the OR saturates, the left side is `1` whatever
  `col_{R+1}(t)` is, so a solution exists iff `A(t) = 1`, which is the
  displayed condition; `col_{R+1}(t)` is then free.  ∎

**Lemma 1' (Rule 90).**  For rule 90 the rule at `x = R` is
`col_R(t+1) = col_{R-1}(t) XOR col_{R+1}(t)`, so
`col_{R+1}(t) = col_R(t+1) XOR col_{R-1}(t)` always exists uniquely.  **The
rule-90 extendability condition is vacuous.**

Lemma 1' is the section-0 filter appearing *inside* the boundary condition:
the pin is nonvacuous for rule 30 precisely because of the OR nonlinearity, and
vacuous for the additive rule.

*Verified.*  `pin_identity_check`: over the exact lone-seed diagram to
`T = 400`, rule 30 satisfies the pin at **all 80,243** antecedent cells
(`s(t,x) = 1`) with **0 violations**; rule 90 violates it at **all 11,195**.
`test_rung1.py` additionally checks Lemma 1 *exhaustively* against brute-force
extendability for all letter words of length 2, 3, 4, and on 400 random words
of length up to 12, plus 200 random words for rule 90, and confirms the true
lone-seed letter word is never rejected at `R = 1, 2, 3, 5` to `T = 300`.

## 2. PROVED: the pin cannot decide anything depth cannot

Write `plain(R)` and `pin(R)` for the ladder languages at right depth `R`
without and with the boundary condition, projected onto columns
`[x_min, R]`.

**Corollary 2 (Sandwich).**  `plain(R+1)  ⊆  pin(R)  ⊆  plain(R)`.

*Proof.*  Right inclusion: `pin(R)` is `plain(R)` with one extra constraint.
Left inclusion: a word in `plain(R+1)` carries an actual `col_{R+1}` obeying
the forward rule at `x = R`, so by Lemma 1 its projection satisfies the pin.
(The inclusion is generally strict because `plain(R+1)` also imposes the wedge
and edge conditions *on* `col_{R+1}`, which `pin(R)` does not.)  ∎

**Corollary 3 (the pin is not an independent axis).**  If `plain(R)` is
nonempty for every `R`, then `pin(R) ⊇ plain(R+1)` is nonempty for every `R`.
Contrapositively, `pin(R) = ∅` forces `plain(R+1) = ∅`.

So the pin can only ever find, one column early, an emptiness that depth would
find anyway.  It buys strictly less than one full column and it cannot decide
`p = 2` unless depth alone decides it.  Since rung 0 section 3 measured the
verdict to be uniform in `R` and `k` across a 5,500x range of raw sizes, the
pin was never going to close this, and section 3 below confirms it does not.

This also *explains* the relocation behaviour that motivated rung 1: the pin
constrains column `R` but leaves column `R+1` entirely free, which reproduces
the free-boundary situation one column further out.  The escape does not
survive by luck; it survives because the pin recreates the very gap it closes.

## 3. MEASURED: verdicts, with and without the pin

`p = 2`, tail word `01`, `k = 2`, `q = 1`, rule 30.  Every NONEMPTY carries a
lasso re-verified by the independent forward-rule checker (`verify_witness`);
zero verification failures.  No state caps hit.

| R | plain states | plain verdict | pin states | pin verdict | cut | pin cycle len |
|---:|---:|---|---:|---|---:|---:|
| 1 | 428 | NONEMPTY | 224 | NONEMPTY | 1.9x | 6 |
| 2 | 1,445 | NONEMPTY | 607 | NONEMPTY | 2.4x | 8 |
| 3 | 5,574 | NONEMPTY | 1,776 | NONEMPTY | 3.1x | 8 |
| 4 | 22,087 | NONEMPTY | 5,253 | NONEMPTY | 4.2x | 16 |
| 5 | 88,136 | NONEMPTY | 15,700 | NONEMPTY | 5.6x | 18 |
| 6 | 352,329 | NONEMPTY | 47,059 | NONEMPTY | 7.5x | 18 |

The pin cuts the raw state space by a growing factor and lowers the per-depth
growth rate from about **4.0x** (the alphabet factor identified in rung 0
section 3) to about **3.0x**.  It never changes a verdict.

### Calibrations, with the pin enabled

| case | R | verdict | required |
|---|---:|---|---|
| rule 30, `w = 1`, `q = 1` | 1, 2 | **EMPTY** | EMPTY |
| rule 30, `w = 0`, `q = 1` | 1, 2 | **EMPTY** | EMPTY |
| rule 90 control, `w = 0`, `q = 1` | 1..5 | **NONEMPTY** | NONEMPTY |

Two things to note.

1. The pin **strictly tightens**: rung 0 had `w = 0` NONEMPTY at `R = 1`
   (witness verified, onset 2); with the pin that escape is gone and `R = 1`
   is already EMPTY.  So the constraint does real work at `p = 1`.
2. **The rule-90 soundness control survives.**  Rung 0 section 6 recorded, as
   an unavoidable cost, that a pin-augmented ladder has no section-0 control
   because the true rule-90 word is rejected by the pin.  That is true only if
   one applies *rule 30's* pin to rule 90.  By Lemma 1' the correct control
   applies rule 90's own extendability condition, which is vacuous, so the
   control is `plain(R)` and remains NONEMPTY.  **The recorded cost was an
   artifact of the formulation, and it is repaired here.**  Any later session
   reporting an EMPTY from a pin-augmented ladder still owes the `N_base`
   check of rung 0 section 6, which this rung did not need because it produced
   no EMPTY in the open cases.

## 4. MEASURED: the dichotomy comes out on the growth side

Raw product-state counts are dominated by the `4^(R+k)` alphabet factor and
prove nothing (rung 0 section 3).  The R-comparable object is the accepting
tail system — the union of nontrivial SCCs carrying a Buchi-accepting run —
quotiented canonically.

**Method note, recorded because the first attempt was wrong.**  The intended
metric was the projected letter language determinized and minimized.  Subset
construction on the tail NFA is exponential and did not terminate even at
`R = 1`; that is a defect of the metric, not a finding.  The reported invariant
is instead the number of **bisimulation classes** of the accepting tail system
(partition refinement from the diff-labelled initial partition): polynomial,
canonical, and still sensitive to genuinely new tail behaviour.  It is a
coarser invariant than the minimized language and the dichotomy below should
be read at that strength.

| R | raw states (plain) | tail nodes (plain) | bisim classes (plain) | raw states (pin) | tail nodes (pin) | bisim classes (pin) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 428 | 38 | 10 | 224 | 14 | 9 |
| 2 | 1,445 | 108 | 15 | 607 | 53 | 20 |
| 3 | 5,574 | 432 | 34 | 1,776 | 113 | 44 |
| 4 | 22,087 | 1,536 | 73 | 5,253 | 273 | 91 |
| 5 | 88,136 | 4,864 | 140 | 15,700 | 739 | 165 |
| 6 | 352,329 | 17,152 | 229 | 47,059 | 2,036 | 267 |
| 7 | 1,409,098 | 61,440 | 349 | 141,112 | 5,297 | 466 |

**The classes grow, but only polynomially, and at the same rate with and
without the pin.**  Successive ratios fall steadily —
`1.50, 2.27, 2.15, 1.92, 1.64, 1.52` (plain) and
`2.22, 2.20, 2.07, 1.81, 1.62, 1.75` (pin) — and a log-log fit over `R >= 3`
gives

```text
bisim classes ~ R^2.761   (plain)
bisim classes ~ R^2.741   (pin)
```

against raw state growth of `4^R` and tail-node growth of `3-4x` per unit
depth.  So the tail system carries only about `R^2.75` genuinely distinct
behaviours while the encoding around it inflates exponentially.

Three consequences.

* **The stabilization branch is falsified at this strength.**  The class count
  is unbounded, so the escape is not R-uniform in the sense of a fixed finite
  tail system reused at every depth, and the cheap route to the limitation
  theorem is closed.
* **The growth branch is weaker than it looks.**  Polynomial growth against an
  exponential encoding means depth buys very little: the free boundary
  regenerates almost all of the tail behaviour at each step.  This is the
  quantitative form of the relocation hypothesis, and it is why the verdict
  never moves.
* **The two exponents agree to 0.02.**  That is the measured shadow of
  Corollary 2: if `pin(R)` sits between `plain(R)` and `plain(R+1)`, its
  asymptotics must match `plain`'s, and they do.  The raw class counts also
  interleave as the sandwich suggests, `plain(R) < pin(R) < plain(R+1)` for
  `R >= 2` (`20 > 15` and `20 < 34`; `44 > 34` and `44 < 73`; and so on),
  with a single inversion at `R = 1` (9 vs 10).  Class count is not monotone
  under language inclusion, so all of this is consistency evidence, not proof;
  the proof is Corollary 2.

## 5. PROVED: why the witnesses must have long cycles

A natural attempt at an R-uniform escape family is a tail that is periodic in
time with period 2, matching the target centre word directly.  It cannot work.

**Lemma 4 (2-periodic collapse).**  Restrict the leftward inverse transduction
to columns that are 2-periodic in time, written `X = (x0, x1)` with
`X(t) = x_{t mod 2}`.  On the state `(col_x, col_{x+1})` the derivation acts as

```text
(U, V)  |->  (W, U),      W = (u1 XOR (u0 OR v0),  u0 XOR (u1 OR v1)).
```

All 16 states reach, within at most 3 steps, the single 2-cycle

```text
((1,1),(0,0))  <->  ((0,0),(1,1)),
```

whose columns are **constant in time** (identically 1 and identically 0,
alternating in space).  Hence for `R >= 4` the centre column derived from any
time-2-periodic letter tail is constant, never alternating, and no such tail
can witness the tail word `01`.  ∎ *(exhaustive over all 16 states)*

This is why the measured witness cycle lengths are 4 to 18 rather than 2, and
it tells any later session not to look for short-period escapes.

## 6. What is still missing, stated precisely

To prove the limitation theorem one needs: for every `R`, a letter word whose
derived `col_0` is eventually `01`-periodic and whose `col_{-1}` is not
eventually `q`-periodic.  Two of the three ingredients are in hand.

1. **Saturation.**  `step_window` performs no wedge or edge check once the
   letter count reaches `saturate = R + 2k + 1` (the check for column `x` fires
   at letter time `t + max(0, R-1-x)` with `t <= |x|`, whose maximum is
   `R + 2|x_min| - 1`).  So the tail is constrained only by centre periodicity
   and `Diff_q`, and any admissible tail may be spliced after a prefix.
2. **Prefix.**  The true lone-seed letter word passes every constraint up to
   saturation — this is rung 0's safety regression, 0 rejections to `T = 300`,
   re-confirmed here at `R = 1, 2, 3, 5`.
3. **MISSING: realizability.**  One needs, at every `R`, an infinite letter
   word realizing an alternating `col_0` together with an aperiodic `col_{-1}`.
   The surjectivity of rule 30 makes *some* configuration with alternating
   centre exist, but the ladder additionally needs `col_{-1}` to escape
   `q`-periodicity, and Lemma 4 shows the naive periodic constructions
   collapse.  Closing this is the whole remaining gap.

**Kill condition, applied.**  The rung-1 budget was spent and neither branch
resolved; per the pre-agreed terms this is reported as a clean negative with
the sharpest partial, not extended into another depth sweep.  Corollary 3 is
the reason not to simply re-run with the pin at larger `R`: that combination is
now proved to be weaker than the plain ladder one column further out, which
rung 0 already measured to be uninformative.

## 7. Honest scope

No per-period exclusion for `p >= 2`.  Nothing here bears on Wolfram's
Problem 1.  The new content is exactly: Lemma 1 and Lemma 1' with their
exhaustive verification, Corollary 2/3 retiring the pin as an independent axis,
the repair of the rule-90 soundness control, Lemma 4, and the measured
growth-side dichotomy in section 4.

## Reproduction

```sh
cd experiments/rule30/ladder
uv run python rung1.py --mode identity
uv run python rung1.py --mode calibrate -k 2
uv run python rung1.py --mode sweep     --rmax 6 -k 2 -w 01 -q 1
uv run python rung1.py --mode language  --rmax 7 -k 2 -w 01 -q 1
uv run --with pytest python -m pytest test_rung1.py test_ladder.py -q
```

15/15 tests pass (8 new in `test_rung1.py`, 7 inherited from rung 0).

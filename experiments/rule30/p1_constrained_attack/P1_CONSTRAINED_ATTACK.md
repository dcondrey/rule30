# P1 constrained attack: boundary-pin tightening, three arms

All three assigned arms were run; two were already-satisfied by the rung-0
machinery and one had a soundness trap.  One genuine new constraint came out
of arm 2 and is the result of this round.

## Verdict up front

**p >= 2 remains NONEMPTY.  The loop's exit condition did not fire.**  No
`P1_PROOF_DRAFT.md` is written, because no EMPTY verdict was produced for any
p >= 2.  Writing one would be fabrication.

What was gained: a new sound constraint (the **boundary pin**), which kills
the entire rung-0 escape family and cuts the state space ~2.5x, but which the
automaton escapes by relocating the slip to the new boundary column.  That
relocation is the finding.

## Arm 1 (right-wedge): hypothesis was already satisfied

`ladder.py:step_window` already applies the light-cone check to **every**
derived column, positive x included (`t < |x| -> 0`, `t == |x| -> 1`).
Measured on the rung-0 escape family: **0 wedge violations**.  So the
proposed constraint was already in force and cannot flip anything.  No run
was performed that "adds" it; a flip to EMPTY from adding an already-present
constraint would have been a bug, per the pre-run instruction.

## Arm 2 (pin cascade): the one real finding

Prediction going in: the pin cascade (`r_t=1 and c_t=0 => r_{t+1}=1`) is a
Rule 30 identity, and every modelled column is built by the inverse
transduction, so imposing it should filter **zero** states.

Measured on the escape family, per column pair:

| pair (x -> x+1) | pin-cascade violations |
|---|---:|
| -1 -> 0 | 0 |
| 0 -> 1 | 0 |
| 1 -> 2 | 0 |
| **2 -> 3 (= R)** | **4** |

The prediction holds for the interior and **fails at the boundary**.  Reason:
the identity at column x needs the forward rule to hold at (t+1, x), whose
parents include column x+1.  For x = R that column is unmodelled, so the
strip does not enforce it.  Violations sit at t = 33, 55, 77, 99 - spacing
22, exactly the escape cycle length, i.e. **once per phase slip**.

### The boundary pin (new constraint, sound, Rule-30-specific)

```text
col_R(t) = 1  =>  col_{R-1}(t) = NOT col_R(t+1)
```

*Proof.*  `s(t+1,R) = s(t,R-1) XOR (s(t,R) OR s(t,R+1))`; with `s(t,R)=1` the
OR saturates to 1 regardless of column R+1, so `s(t+1,R) = s(t,R-1) XOR 1`.
No knowledge of column R+1 is used.  Being a two-consecutive-letter
condition, it costs no extra automaton state.

*Regression, T=300, exact simulation:*

| R | rule 30 antecedents / violations | rule 90 antecedents / violations |
|---|---|---|
| 1 | 150 / **0** | 8 / 8 |
| 2 | 145 / **0** | 7 / 7 |
| 3 | 163 / **0** | 13 / 13 |
| 4 | 140 / **0** | 6 / 6 |

Rule 90 violates it at *every* antecedent, which is the PATH.md section 1.1
discriminator showing up as data: the constraint is exactly the OR
nonlinearity, so it passes the Rule 90 filter by construction and is never
imposed on the Rule 90 control.

### Effect

* Old escape family: **REJECTED at letter 34** (the first slip).  Confirmed
  by threading the family through the constrained automaton.
* State-space cut, `R=3, q=4`: 12569 -> 4915 (~2.5x).
* Verdict: still **NONEMPTY**.  A new witness appears with cycle length 12
  (vs 22), **0 boundary-pin violations and 0 wedge violations** - it is
  genuinely admissible, not a search artifact.  Its structure shows the slip
  displaced outward into column +3, the new boundary.

The pattern this suggests, stated as a conjecture and not a result: any
fixed-depth strip leaves its outermost column under-constrained, and the
slip migrates there.  If true, no fixed-R boundary-pin ladder closes p = 2,
which sharpens the rung-0 lemma from "depth 3, all q" to "all depths, all q,
under strip + boundary-pin constraints".

## Arm 3 (universal q): the trap, and the bounded version

**The trap, confirmed by construction rather than by running it:** a Buchi
automaton is nonempty iff it accepts an ultimately periodic word, and every
lasso has `col_{-1}` eventually periodic.  So an automaton demanding
"`col_{-1}` not eventually q-periodic for *any* q" is EMPTY vacuously, for
every rule, Rule 90 included.  Such an EMPTY proves nothing.  Only bounded
`q <= Q_max` is sound; that is what was built (`boundary_pin.py`, joint
countdown gadgets with generalized-Buchi acceptance reduced by a round-robin
index).

Measured Diff behaviour of the escape family's `col_{-1}` (tail of length 75):

| q | 1 | 2 | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| diff events | 34 | 33 | 33 | **6** | 32 | 25 | 12 |

It satisfies every `Diff_q` tested, so bounded-universal q does not exclude
it either.  The q = 4 dip is the period-4 train showing through: only the
slips create q = 4 differences, one per cycle, which is still infinitely
often and therefore still accepting.

## Sweep results (boundary pin ON, primitive necklaces, R <= 4)

Depth scaling stayed retired: R <= 4 throughout, all gains sought from
constraints.  One representative per rotation class (onset is existentially
quantified).

| p | word | R=1 | R=2 | R=3 | R=4 |
|---|---|---|---|---|---|
| 2 | 01 | NONEMPTY | NONEMPTY | NONEMPTY | NONEMPTY |
| 3 | 001 | NONEMPTY | NONEMPTY | NONEMPTY | NONEMPTY |
| 3 | 011 | NONEMPTY | NONEMPTY | NONEMPTY | NONEMPTY |

(q in {1,2,4} at every cell; all NONEMPTY.  **0 EMPTY cells.**  States at
`R=4, q=4`: 14563 / 15635 / 15649.)

Controls, all passing: rule 90 base pipeline NONEMPTY at R = 1..4; rule 30
p = 1 calibrations still EMPTY under the pin (`w=1 R=1`, `w=0 R=2`), so the
tightening did not break completeness on the known theorems.

## Honest assessment

The boundary pin is a real, sound, Rule-30-specific tightening and the first
constraint in this line to kill the rung-0 obstruction outright.  It is not
enough.  The escape is structural: the slip lives wherever the strip stops
modelling, so constraints anchored at the boundary displace it rather than
eliminate it.  The next lever that is not depth-scaling is the one named in
the rung-0 doc and not yet built: **right-edge diagonal periodicity**
(`RESULTS-diagonal-periodicity.md`, PROVED, purely periodic with period
2^a(j)), which is a fact of the lone-seed diagram in the *moving* frame and
therefore not implied by strip validity in any column window.  It requires
re-indexing the automaton into diagonal coordinates and re-deriving the
transduction, which is a build, not a tweak.

## Files

* `experiments/rule30/p1_constrained_attack/boundary_pin.py` - constrained
  automaton, joint bounded-universal Diff, soundness regression.
* `experiments/rule30/p1_constrained_attack/sweep.py` - necklace sweep.
* `experiments/rule30/p1_constrained_attack/ladder_base.py` - unmodified copy
  of the rung-0 automaton.
* This document.

Reproduce: `uv run --no-project python sweep.py 3 4 2000000`.

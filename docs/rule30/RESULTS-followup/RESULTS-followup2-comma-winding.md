# Comma-winding arm (roundtable follow-up 2): KILLED

Status: **KILLED** at step 2 (the coupling question), on the triage agent's
own pre-registered kill condition. Code:
`experiments/overnight-arms/roundtable_followup2/comma_winding/probe.py`.

## 0. What was tested

The spark proposes a real-valued "winding number" `v(t)` along the backward
(leftward) Rule 30 reconstruction path: XOR/f-type steps add 0, OR-saturating
("s-type") steps add an irrational unit `alpha`. It hopes that a hypothesized
centre period `p` would force `v(t+p) = v(t)`, and that since `v` lives in
`Z + Z*alpha`, this closure would be as constrained as closing an irrational
rotation -- something the seed's one-handed OR-engagements supposedly resist
unless the OR-engagement count is itself forced periodic.

The triage agent's kill condition was: *there is no demonstrated coupling
between the hypothesized bit-periodicity and the winding coordinate* -- if the
s-type count is just a free counter in the past cone, periodicity of the
centre bits need not constrain it at all.

## 1. Formalizing v(t)

Using the existing pin identity (`inverse_trace_probe.reconstruct_left_column`,
already in the repo, `s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1))`):

- One reconstruction **layer** takes a `(center, right)` column pair at some
  position `x` and produces the `left` column at `x-1`.
- Within a layer, a time-step `t` is **s-type** iff `s(t,x) OR s(t,x+1) == 1`
  (at least one of the two right-neighbour inputs is 1); otherwise it is
  **f-type** (clean XOR, OR term contributes 0).
- **Depth-D reach**: iterate layers exactly as `rotated_defect_front` already
  does in this repo -- layer `k+1` takes `(left_k, center_k[:-1])` as its new
  `(center, right)`.
- `v` at depth `D`, starting from a given `(center, right)` pair, is
  `alpha * s_count(D)` where `s_count(D)` sums s-type steps over all `D`
  layers. This is the spark's own reduction (XOR contributes 0), pinned down
  exactly here because the spark never specified path or depth.

This is a faithful, minimal formalization -- not a strawman weakening. It
reuses the repo's own reconstruction primitive verbatim.

## 2. The coupling question -- MEASURED, and it fails immediately

**Algebra first.** In one layer, whether time-step `t` is s-type depends on
`center[t] OR right[t]`. If `center[t] = 1`, the step is s-type regardless of
`right[t]`. If `center[t] = 0`, the step is s-type **iff `right[t] = 1`**,
and `right[t]` is a value at a different spatial column (`x+1`), entirely
free with respect to any statement about the periodicity of `center` (column
`x`). A period-p hypothesis on the centre column says nothing whatsoever
about column `x+1`. So already at the level of one reconstruction layer,
`s_count` is not a function of the centre's period hypothesis alone -- it
depends on data the periodicity hypothesis does not touch.

**Computational confirmation.** `probe.py` fixes a period-p centre word
(unchanged, bit-for-bit identical, in both variants of each case) and varies
only the adjacent right column at exactly the positions where the centre bit
is 0 (`right_a` = all zero there, `right_b` = all one there). Both variants
are verified to be genuine forced Rule 30 continuations of the same centre
trace (`actual_rule30_consistency_check`, forward re-evolution reproduces the
claimed next centre bit exactly in both cases).

| case | period word | depth | s_count(right_a) | s_count(right_b) | difference |
|---|---|---|---|---|---|
| period-2 | (0,1) | 1 | 20 | 40 | 20 |
| period-2 | (0,1) | 2 | 59 | 59 | 0 |
| period-2 | (0,1) | 3 | 97 | 97 | 0 |
| period-3 | (0,0,1) | 1 | 15 | 45 | 30 |
| period-3 | (0,0,1) | 3 | 87 | 117 | 30 |
| period-5 | (0,1,0,0,1) | 1 | 20 | 50 | 30 |
| period-5 | (0,1,0,0,1) | 4 | 144 | 164 | 20 |

The centre trace is bit-for-bit identical between the two columns of every
row (by construction -- the perturbation is on the *other* column). The
s-type count differs at depth 1 in every case (as the algebra above forces),
and for period-3 and period-5 the difference **persists at greater depth**
rather than being absorbed; only period-2's fully alternating word happens to
show the discrepancy cancel by depth 2 in this particular pair of variants
(one coincidence of a symmetric word, not a general cancellation -- period-3
and period-5 show it does not happen generally, and no mechanism forcing
cancellation was found or expected).

**Verdict on step 2: KILLED.** The kill condition fires exactly as
pre-registered. `s_count`, and hence `v(t) = alpha * s_count`, is not
constrained at all by a centre-periodicity hypothesis; it is free data
supplied by the adjacent column, which periodicity of the centre says nothing
about. Different period-p-consistent reconstructions give different,
unconstrained s-step counts. This is the demonstrated non-coupling the
triage agent anticipated; it is not a strawman -- the same free bit (`right[t]`
at each zero-centre slot) is exactly what any real backward reconstruction of
the *actual* lone-seed diagram would also have as independent input, since
the actual right-hand column of the true diagram is not determined by
"assume the centre is eventually period p" either.

## 3. Depth / O(log t) wall -- moot, but checked

Because the kill fires at depth 1, establishing "v is well-defined" never
gets far enough to hit obstruction A (`PATH.md` section 7.3.A, the
`~2.4 log2(t)` reconstruction-depth wall). This is the cheap-disconfirming-test-first
outcome PATH.md's research-mode doctrine asks for: no infrastructure was
built on an unconfirmed contribution. For completeness, depths up to 4 were
run above and show no sign of the discrepancy being forced to zero as depth
grows (period-3, period-5), so even if one hoped boundedness would rescue the
argument at some larger fixed depth, there is no evidence for that in the
depths checked, and no argument was found for why it should occur.

## 4. Is the "irrational rotation" inference even valid, if the coupling existed?

Checked independently of step 2's kill, because the spark's mathematical
content depends on it. Since `alpha` is irrational, the map `n |-> n*alpha`
from `Z` to `R` is **injective** (distinct integers give distinct reals; this
is immediate, not a Weyl-equidistribution-level fact). Consequently, for
integer-valued `s_count`,

    v(t+p) = v(t)   <=>   alpha * s_count(t+p) = alpha * s_count(t)   <=>   s_count(t+p) = s_count(t).

So "`v` lives in `Z + Z*alpha` and periodicity forces closure of an irrational
rotation" is **not** a nontrivial closure principle -- it is exactly,
word-for-word, the statement that the integer count `s_count` would have to
repeat. The irrational unit `alpha` does no work here: multiplying an integer
sequence by an irrational constant and asking whether the result is periodic
is precisely as hard, and precisely as easy, as asking whether the original
integer sequence is periodic. There is no additional obstruction contributed
by irrationality/incommensurability, and no equidistribution-type argument is
needed or available to rescue this -- the "octave vs. fifth, comma" framing
is decorative dressing on a plain integer-recurrence question. This closes
off the possibility that even a hypothetical coupling would buy anything
beyond what asking "is `s_count` periodic" already asks directly, and step 2
shows `s_count` is not even well-defined as a function of `t` under the
periodicity hypothesis alone, so the question doesn't get to be posed as
stated.

## 5. Rule 90 screen

Rule 90 (`p XOR q` on the two flanking neighbours, no OR term at all) has
`s_count = 0` identically, at every depth, for every configuration -- there is
no neighborhood assignment under which an OR term is evaluated, because Rule
90's update has none. So `v(t) = 0` for Rule 90, trivially, always.

This is the same pattern PATH.md documents elsewhere as **vacuous**, not a
useful pass (obstruction B, `PATH.md` section 7.3.B): the object under test
does not exist for the control rule at all, rather than existing and
provably closing. A pass of this shape carries no discriminating information
-- it says nothing about *why* Rule 30's centre column would differ from Rule
90's, because there was never a comparable quantity to compare on the Rule 90
side. The spark's own text half-acknowledges this ("the winding is torsion
and does close -- onto the empty node"), which is exactly a description of
vacuity, not of a meaningful closure.

## Summary

| step | question | verdict |
|---|---|---|
| 1 | formalize v(t) | done: `alpha * s_count(D)` over D reconstruction layers, pinned to `reconstruct_left_column` |
| 2 | does centre-periodicity constrain s_count? | **KILLED** -- MEASURED counterexamples above, differences persist across depths tested |
| 3 | O(log t) wall relevance | moot (killed before reaching it); depths 1-4 checked, no sign of forced convergence |
| 4 | is "irrational rotation closure" a valid nontrivial inference | no -- exactly equivalent to plain integer-sequence periodicity, alpha adds nothing |
| 5 | Rule 90 screen | passes only vacuously: no OR term exists in Rule 90 at all, so v=0 identically and trivially, no discriminating content |

Nothing here proves or disproves P1. The comma-winding construction is
**KILLED** as a route to it: the proposed invariant is not a function of the
centre-periodicity hypothesis, the irrational-rotation framing adds no
mathematical content beyond plain integer recurrence, and its Rule-90 "pass"
is vacuous rather than informative.

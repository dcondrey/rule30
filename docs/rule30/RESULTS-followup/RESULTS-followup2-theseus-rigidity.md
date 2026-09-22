# Theseus rigidity lemma (roundtable follow-up 2): KILLED

## Status

**KILLED.**  Not "no rigidity lemma was derived" (obstruction D, decorative
vocabulary) but something sharper and stronger: the cheapest, most natural
formalization of the spark's "type" invariant is **provably identical to the
bit value**, by an elementary closure argument, confirmed computationally to
500,000 steps for both Rule 30 and Rule 90.  There is no daylight between
"type" and "bit" for this invariant to be rigid *about*.  Worse for the
spark's own framing: the claimed Rule 30 / Rule 90 disanalogy ("Theseus's
problem is soluble exactly when the rule is additive") is **false** under
this formalization — both rules collapse identically, not just Rule 90.

Work directory: `experiments/overnight-arms/roundtable_followup2/theseus_rigidity/`
(new; four scripts, one test file, no repo files touched).

## The spark's claim, pinned down

The spark asks: track each cell's causal history via something richer than
its bit value — a "type" — and ask whether eventual bit-periodicity of the
centre column forces eventual periodicity of the type sequence too ("as
typed assemblies, not merely as parities").  The cheapest concrete
formalization it points at (task step 1) is: evolve Rule 30 symbolically
from a formal seed variable `s` instead of the concrete value `1`, over the
Boolean semiring (`GF(2)[s]/(s^2=s)`), so a cell's "type" is the actual
Boolean function of `s` it computes, of which the true bit (`s=1`) is one
evaluation.

## Step 1 — the invariant is forced into a 4-element algebra, and then into 2

`free_algebra_closure.py` confirms by exhaustive truth table (the free
Boolean algebra on one generator) that `{0, 1, s, not-s}` is closed under
AND, OR and XOR (and NOT).  Rule 30's local update
`new = left XOR (center OR right)` uses only XOR and OR; Rule 90's uses only
XOR.  Starting every cell's formal value as the constant `0` except the one
seed cell (`= s`), closure means **every cell at every time step, for the
entire 2D spacetime diagram reachable from the seed — not just the centre
column — is, as a formal function of `s`, one of these four elements.**
This is a **PROVED** structural fact for any single-seed 2-state CA whose
local rule is built from AND/OR/XOR/NOT, Rule 30 and Rule 90 both included;
it follows from there being exactly one nonzero source in the initial
condition, not from anything specific to either rule.

That already caps how much richness a "symbolic seed" type can carry: at
most 4 values, i.e. 2 bits, at *any* cell, ever, no matter how deep its
causal past. But it gets tighter still.

`symbolic_type.py` runs two bit-parallel simulations side by side — one from
the true seed (`s := 1`), one from an all-zero row (`s := 0`) — for both
rules, to 500,000 steps. A 1-variable Boolean function is fully determined by
its two values, so the pair `(value at s=0, value at s=1)` at each time *is*
the type, exactly.  Measured: the `s=0` branch is identically zero at every
step, for both rules (**PROVED** separately too: the all-zero row is a fixed
point of both local update rules by direct substitution, so this isn't a
500,000-step coincidence, it's an induction with one base case).  That
collapses the reachable pairs from the 4-element algebra `{0,1,s,not-s}` down
to exactly `{(0,0), (0,1)} = {"0", "s"}` — the two elements whose `s=0`
branch is 0.  `not-s` (whose `s=0` branch is 1) and `1` (ditto) are simply
never realized, at any cell, at any time.

Consequence: `type = "0"` exactly when `bit = 0`, and `type = "s"` exactly
when `bit = 1`.  **Type is not a refinement of bit that happens to correlate
with it — it is bit, under a relabeling, exactly, for every cell in the
diagram, at every time, for both rules.**  Confirmed for the true lone-seed
Rule 30 and Rule 90 orbits to 500,000 steps (`symbolic_type.py` output:
`distinct (val@s=0, val@s=1) type-pairs realized: [(0, 0), (0, 1)]` for both
rules; regression test in `test_symbolic_type.py`).

This directly answers the triage agent's kill condition. It isn't merely
that "type periodicity might not be implied by bit periodicity" — under this
formalization there is no *type* distinct from bit to have an implication
about.  Rigidity trivially "holds" (type is eventually periodic whenever bit
is, because they are the same sequence) but is empty of content: it supplies
zero new information toward P1, exactly the missing-composition-law
obstruction D pattern ("names ... instead of deriving it") except here the
thing that would need naming — an actual gap between type and bit — provably
does not exist for this formalization.

## Step 2 — the Rule 90 "gut check" is not what the spark thinks it is

The spark frames Rule 90 as the disanalogy case: "types collapse to parity ...
Theseus's problem is soluble exactly when the rule is additive," implying
Rule 30's non-additivity is what should let type-richness survive.
`symbolic_type.py`'s output is identical for both rules — `[(0, 0), (0, 1)]`
— because the collapse argument above never used additivity. It used only
(a) the local rule is built from AND/OR/XOR, and (b) there is exactly one
nonzero seed. Both hold for Rule 30 too. **The claimed disanalogy is false
under this formalization**: Rule 30 does not escape the collapse that Rule
90 suffers; it suffers the identical one. Section 0's Rule 90 filter is
about arguments that *would also work for Rule 90*; this is the more direct
failure mode — an argument that *is already vacuous* for the rule under
test, independent of Rule 90 at all. Rule 90 confirms the collapse is real
(matches known linearity-collapses-to-parity intuition) but does not
distinguish the rules, contrary to the spark's premise.

## Step 3 — general fact-check: does coarse periodicity ever force fine periodicity?

Task step 3 asks for a fact-check outside Rule 30: can a finer, non-injective
refinement of a periodic sequence fail to be periodic itself?  Answer: yes,
trivially, in general — `toy_counterexample.py`: state `state_t = t` (an
unbounded counter, never periodic), output `bit_t = state_t mod 2` (exactly
period 2). Checked computationally (`is_eventually_periodic` on 2000 steps:
bit period found = 2, state period = None as expected).

The distinguishing feature: `state_t` carries genuinely independent memory
not recoverable from the bit sequence's own history (an external unbounded
counter). A statistic that is instead a *deterministic function purely of
the coarse sequence's own realized history* (e.g. "run length since the bit
was last 0", the closest cheap reading of the task's alternative "depth
since fresh determination" idea, since for the centre column a cell's own
next value is only right-sensitive when its own current value is 0) inherits
periodicity for free — it is causally downstream of a periodic input, so it
is periodic too, with a period dividing the input's. That version of "depth"
was not implemented separately because it reduces to a restatement of the
bit sequence's own run-length structure and cannot expose anything the bit
sequence doesn't already have.

So: no free-standing theorem forces rigidity from refinement alone (the
counter example proves it can fail), and no free-standing theorem forces its
absence either (a refinement causally downstream of the coarse sequence
inherits periodicity). Whether Rule 30's actual "type" apparatus falls in
the first bucket (independent memory, can escape) or the second (downstream,
must inherit) is exactly the question Step 1 answers for the cheapest
formalization: it falls in neither, because there is no daylight between
type and bit at all — the question of which bucket it's in doesn't even
arise.

## Contrast with existing routes in this repo

This is not R1's "zero-set obligation" (`PATH.md` row 1, **OPEN**, not
killed). R1's obligation is about the *left-neighbor row* `r` restricted to
`{c_t = 0}` remaining eventually periodic given `c` is — `r` is a genuinely
different quantity from `c` (recovered by inverse trace reconstruction, not
a relabeling of `c`), and R1's obligation is open precisely because no proof
or disproof of that non-triviality has been found. The type invariant tested
here is different in kind: it is provably a relabeling of the bit it
supposedly refines, so there is no analogous non-trivial obligation to state.
`RESULTS-eventual-period.md`'s defect-form analysis (`d_t(-1) = (1 XOR c_t)
AND d_t(1)`) is likewise a genuinely different quantity (the left defect
row), not affected by this finding.

## What would revive the spark

Any type invariant that is *not* a deterministic function of the seed's
truth value alone and *not* a deterministic function purely of the observed
bit history could still, in principle, carry independent state (the
`toy_counterexample.py` shape). The natural place such state could live is
the full 2D field *outside* the past light cone contributing to future
light-cone geometry (e.g., "how many other columns' histories this cell's
future descendants will interact with") — but that is no longer a "type" of
the individual cell in any tractable symbolic sense; it starts to look like
the ensemble/geometric statistics already retired by `PATH.md` section 0.1
(obstruction C, single-column blindness) or the `Theta(t)`-deep dependency
sets already blocked by the `O(log t)` wall (obstruction A). No version
tried here or suggested by the spark's own text avoids both.

## Verdict

**KILLED**, with an actual derivation rather than an assertion: the
symbolic-seed "type" invariant the spark proposes is proved (closure over a
1-generator Boolean algebra plus the all-zero fixed point) and confirmed
(500,000-step dual simulation, both rules) to equal the bit value exactly,
for both Rule 30 and Rule 90, with no residual degree of freedom for a
rigidity lemma to be about. The Rule 90 disanalogy the spark leans on is
false under this formalization: it is not that Rule 90 collapses and Rule 30
resists — both collapse identically. A general fact-check (`toy_counterexample.py`)
confirms coarse periodicity does not generically force fine periodicity, so
no free theorem could have salvaged this even if the collapse hadn't
happened — the apparatus needed real Rule-30-specific teeth, and instead
turned out to have none by construction.

## Files

- `experiments/overnight-arms/roundtable_followup2/theseus_rigidity/symbolic_type.py`
  — dual-seed simulation, both rules, to 500,000 steps.
- `experiments/overnight-arms/roundtable_followup2/theseus_rigidity/test_symbolic_type.py`
  — regression test (4000 steps, both rules).
- `experiments/overnight-arms/roundtable_followup2/theseus_rigidity/free_algebra_closure.py`
  — exhaustive truth-table closure proof for the 1-generator Boolean algebra.
- `experiments/overnight-arms/roundtable_followup2/theseus_rigidity/toy_counterexample.py`
  — general fact-check: coarse periodicity does not force fine periodicity, and does not forbid it either.

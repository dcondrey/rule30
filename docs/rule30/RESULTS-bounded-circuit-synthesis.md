# Bounded exact circuit synthesis for Rule 30's centre column

Run 2026-08-31.  Code, pre-registration and raw JSON under
`experiments/sygus-p3/`.  Pre-registration was written before the main runs;
the two calls that preceded it (a solver benchmark and one feasibility probe)
are disclosed in its section 6.

**Do not treat anything here as bearing on P3 asymptotically.**  Every result is
a statement about one finite input width.  See section 7.

## 1. What was asked

Let `c(n)` be Rule 30's centre column at step `n` from a lone seed, `c(0) = 1`
the seed row (OEIS A051023, offset 0).  For `m` input bits let `f_m` be the
function from the binary encoding of `n` to `c(n)` for all `n < 2^m`, and let
`k_min(m)` be the minimum length of a Boolean chain computing `f_m`.

The search is **complete within the bound**: an UNSAT answer at `k` is a
theorem that no `k`-step chain computes `c` on `[0, 2^m)`, not a report that a
search failed.  That completeness is the whole reason to run it, and it is what
separates this from the stochastic LLM-evolution arm.

**Chain model, stated because it affects the numbers.**  Steps are two-input
gates over the full basis `B2` minus the six degenerate operators (two
constants, four projections/negations); the output must be a chain step, so a
bare negated input is not free.  `k_min` in this convention is Knuth's
combinational complexity `C(f)`, comparable against `u(2)=1, u(3)=4, u(4)=7,
u(5)=12` (TAOCP 4A, 7.1.2).  Those `u(m)` values are quoted from the
literature and were **not** verified locally; `u(3)=4` is corroborated here by
the upper-side sanity test (all 256 three-bit functions realizable at `k=4`),
but `u(4)` and `u(5)` are not.  This matters for exactly one claim -- the
inherited `m=5` upper bound -- and for nothing else.  Every lower bound in this
document is machine-derived and independent of it.

## 2. This is not a repeat of prior work in this tree

Confirmed against the register, and the register's own words carry the claim.

* **Obstruction I** (`PATH.md` 9.2) is about *refutation* of the light-cone CNF
  `F_n` with the input pinned to the lone seed.  Its content is that those
  instances are satisfiable with a unique solution, so every surveyed hardness
  technique -- all of which need unsatisfiability -- is inapplicable.  This
  experiment runs the other way: `n` is a free binary input, the instances are
  *synthesis* instances, and the informative answers are exactly the UNSAT
  ones.  Obstruction I neither covers nor blocks it.

* **Arm `a22_p3_succinct_index`** did a literature-only Tier-3 check on this
  precise object, verdict "GENUINELY OPEN, no prior work transfers", and closed
  with: *"No first probe was executed, per this arm's literature-only scope."*
  The same arm drew the distinction that keeps this out of `PATH.md` 8.7's T4
  ("non-uniform circuit lower bounds are structurally dead"): T4 is about one
  hardwired circuit per `n`, "a different object from the *uniform*
  succinct-index question asked here -- the register does not currently draw
  that distinction anywhere."

**Verdict: genuinely distinct.  This is that first probe.**

## 3. Ground truth and instrument validation

Everything below depends on the truth table being right and the solver's UNSAT
answers being trustworthy, so both were checked before any Rule 30 number was
read.

**Ground truth.**  Two deliberately dissimilar simulators (explicit
list-of-cells with an 8-entry rule table; whole rows as python bignums with
shift/mask) agree cell-for-cell to `t = 200` for rules 30, 90, 110 and 150, and
both reproduce all 102 published terms of A051023 exactly.  (`rule30.py`,
`oeis_check.py`.)

**Encoding.**  SSV formulation of Boolean-chain exact synthesis, following
Haaswijk, Mishchenko, Soeken and De Micheli, *SAT-Based Exact Synthesis:
Encodings, Topology Families, and Parallelism*, IEEE TCAD 39(4):871-884 (2020),
over the chain model of Knuth TAOCP 4A 7.1.2.  Nothing was invented locally
except the choice of which optional symmetry breaks to enable, and those are
validated below.

**Solver choice, measured not assumed.**  Byte-identical CNF fed to CaDiCaL
(via `python-sat`) and to Z3, Rule 30 at `m = 4`:

| k | vars | clauses | result | CaDiCaL | Z3 |
|---|---|---|---|---|---|
| 4 | 196 | 7326 | UNSAT | 0.071 s | 2.005 s |
| 5 | 244 | 11523 | SAT | 0.288 s | 4.363 s |
| 6 | 300 | 17171 | SAT | 0.201 s | 3.580 s |
| 7 | 365 | 24591 | SAT | 0.118 s | 4.666 s |

CaDiCaL is 20-30x faster; the instance is pure CNF with no theory content, so
the SMT machinery only adds cost.  CaDiCaL used throughout.  The two solvers
also **agree** on the `k = 4` UNSAT, which independently rules out a solver bug
on the `m = 4` theorem.

**Sanity tests, two-directional** (`test_synth.py`).  An under-constrained
encoding makes every `k_min` too small; an over-constrained one makes every
UNSAT worthless.  Both checked:

* Lower side -- every literature-known minimum reproduced exactly:
  `xor2 = 1`, `and2 = 1`, `maj3 = 4`, `parity3 = 2`, `parity4 = 3`,
  `and4 = 3`, `maj3-ignoring-a-fourth-input = 4`.  Every SAT chain returned is
  re-evaluated against the truth table by an independent evaluator before it
  is believed; all verified.
* Upper side -- all 256 three-bit functions are SAT at `k = u(3) = 4`.  Zero
  spurious UNSAT.

**Symmetry breaks validated, not assumed.**  The colex step ordering is
unconditionally sound (any chain topologically re-sorts).  The distinct-fanin-
pair break is the exposed one: the textbook optimal MAJ-3 chain uses the same
pair twice, and survives only because an alternative 4-step chain exists.  Two
checks close it:

* All 256 three-bit functions, full `k_min` computed with the break on and
  with it off: **zero mismatches**.  Complete across every `k` at that arity,
  which is strictly stronger than the realizability pass above.
* Rule 30 at `m = 4`, `k = 1..5`, with both optional breaks **disabled**:
  UNSAT at `k = 1, 2, 3, 4` and SAT at `k = 5`.  The `m = 4` theorem below is
  therefore **unconditional** -- it does not rest on any symmetry break.

(`validate_break.py`, `validate_break.json`.)

## 4. `k_min` results

### m = 3 (N = 8)

Reported only for completeness; the whole range of `k_min` at this arity is
`0..4`, so nothing here discriminates.

| function | `k_min` |
|---|---|
| Rule 30 centre column, offset 0 | 2 |
| Rule 30 centre column, offset 1 | 3 |
| Rule 90 centre column | 2 |
| Rule 150 centre column | 0 |
| Rule 60 centre column | 0 |
| parity of `n` | 2 |
| AND of all bits | 2 |
| MAJ-3 | 4 |

Random 3-bit null (60 seeded samples): median 2, support `{0,1,2,3,4}`.  Two
of the 60 came back `k_min = 0`, i.e. the sampled table was a constant or a
bare projection; roughly 4% of 3-bit functions are, so this is expected, but
those two are degenerate members of the null rather than measurements of
synthesis cost.

### m = 4 (N = 16)

Target truth table, Rule 30 offset 0: `1101110011000101` (Hamming weight 9).

| function | `k_min` |
|---|---|
| **Rule 30 centre column, offset 0** | **5** |
| **Rule 30 centre column, offset 1** | **6** |
| Rule 90 centre column | 3 |
| Rule 150 centre column | 0 |
| Rule 60 centre column | 0 |
| parity of `n` | 3 |
| AND of all bits | 3 |
| MAJ-3 (fourth input ignored) | 4 |

**The theorem obtained.**  No Boolean chain of 4 or fewer two-input gates
computes `c(n)` for all `n < 16`.  Five gates suffice, and a five-gate chain
was produced and independently verified.  `k_min(m=4) = 5` exactly, against a
maximum of `u(4) = 7` over all 4-bit functions.

Random null, 60 seeded uniform 4-bit tables:

| `k_min` | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| count | 3 | 10 | 18 | 27 | 2 |

Median 5.  **Rule 30 lands exactly on the random median.**  Its rank within the
null is the 37th percentile, which given a five-point support means "in the
bulk", nothing more.

Weight-matched null (60 seeded tables of Hamming weight 9, matching the target,
since sparse tables synthesize cheaper and an unmatched null partly measures
table density rather than structure):

| `k_min` | 4 | 5 | 6 | 7 |
|---|---|---|---|---|
| count | 7 | 17 | 32 | 4 |

Median 6.  Rule 30's 5 sits **one gate below** the weight-matched median.  The
interpretation of exactly this outcome was written into section 6 point 1
before the number was seen: a one-gate deviation is the same size as the
offset swing, i.e. inside the noise floor of a bookkeeping choice, and is not
read as a compression signal.

### m = 5 (N = 32)

Exact `k_min` is out of reach here; what is obtained is a bracket.  Every
value of `k` from 1 upward was run as a separate complete call, so the lower
bound does not lean on monotonicity in `k` (which the no-dead-step constraint
denies -- see the pre-registration).

| k | result | time |
|---|---|---|
| 1 | UNSAT | 0.02 s |
| 2 | UNSAT | 0.07 s |
| 3 | UNSAT | 0.11 s |
| 4 | UNSAT | 0.61 s |
| 5 | UNSAT | 9.49 s |
| 6 | UNSAT | 357 s |
| 7 | unresolved | > 86 min, killed |
| 8 | unresolved | > 86 min, killed |
| 9, 10, 11, 12 | unresolved | killed at ~13 min to free cores |

**Lower bound obtained: `k_min(m=5) >= 7`.**  No Boolean chain of six or fewer
two-input gates computes `c(n)` for all `n < 32`.

**Upper bound: `k_min(m=5) <= 12`, from the literature, not from this run.**
`u(5) = 12` (Knuth 7.1.2) bounds every 5-bit function.  No 5-bit chain was
synthesized here: the SAT-side probes at `k = 9..12` did not resolve either,
which is itself informative -- at `m = 5` neither branch is cheap, and the
usual "SAT at `k_min` is fast" intuition from `m <= 4` does not carry over.
So the honest `m = 5` statement is a bracket `7 <= k_min <= 12` whose upper end
is inherited and whose lower end is the only part this experiment earned.

*Conditionality, stated plainly:* the `m = 5` UNSAT results were run with the
distinct-fanin-pair symmetry break enabled.  That break is validated
exhaustively at `m = 3` (all 256 functions, every `k`) and directly at `m = 4`
(the theorem reproduced with all breaks off), but **not** at `m = 5`, where a
no-breaks re-run of the decisive calls is out of reach.  The `m = 4` theorem is
unconditional; the `m = 5` lower bound is conditional on that break.

### m = 6 and beyond

Out of reach.  See the feasibility curve.

## 5. Feasibility curve

Solve time on the Rule 30 target, single core, CaDiCaL.  **UNSAT and SAT times
are reported separately because they behave differently**: the SAT call at
`k_min` is usually cheap, and the UNSAT branch is both the expensive one and
the one that produces the theorem, so it is the branch to extrapolate on.

| m | k | result | clauses | time |
|---|---|---|---|---|
| 3 | 1 | UNSAT | 234 | 0.001 s |
| 3 | 2 | SAT | 646 | 0.001 s |
| 4 | 1 | UNSAT | 870 | 0.001 s |
| 4 | 2 | UNSAT | 2 220 | 0.003 s |
| 4 | 3 | UNSAT | 4 304 | 0.012 s |
| 4 | 4 | UNSAT | 7 326 | 0.102 s |
| 4 | 5 | SAT | 11 523 | 0.608 s |
| 5 | 1 | UNSAT | 2 804 | 0.02 s |
| 5 | 2 | UNSAT | 6 802 | 0.07 s |
| 5 | 3 | UNSAT | 12 506 | 0.11 s |
| 5 | 4 | UNSAT | 20 281 | 0.61 s |
| 5 | 5 | UNSAT | 30 531 | 9.49 s |
| 5 | 6 | UNSAT | 43 705 | 357 s |
| 5 | 7 | unresolved | 60 303 | > 86 min |
| 5 | 8 | unresolved | 80 882 | > 86 min |

All `m = 3` and `m = 4` rows and the `m = 5, k = 6` row were measured on an
otherwise idle machine.  The remaining `m = 5` rows were measured with six to
eight solver processes sharing ten cores and are inflated by an amount not
separately quantified; they are upper bounds on the uncontended time, and the
per-gate growth factor should be extrapolated from the uncontended rows only.

Two facts dominate and should be quoted at anyone planning a follow-up.

* **The UNSAT branch costs roughly 4-8x per additional gate at fixed `m`**
  (0.001 -> 0.003 -> 0.012 -> 0.102 s across `k = 1..4` at `m = 4`).
* **Adding one input bit costs several orders of magnitude, not a constant
  factor.**  The last UNSAT at `m = 4` is 0.1 s; the corresponding one at
  `m = 5` is 357 s -- a factor of ~3 500 for one extra bit, from the truth
  table doubling *and* the chain search space widening at once.

* **The wall is at `m = 5, k = 7`.**  That single call ran over 86 minutes
  without resolving in either direction, and the `k = 8..12` calls likewise.
  Everything up to and including `m = 5, k = 6` finishes; nothing past it does.

Composing those two: `m = 6` would put the decisive UNSAT calls at years on
this encoding and one machine.  `m = 6` is not reachable, and no amount of
patience on this approach changes that -- it would need a fundamentally better
encoding (topology families, DAG-canonical symmetry breaking, or a distributed
portfolio in the sense of Haaswijk et al. section VI).

## 6. Reading the numbers honestly

**The instrument kill-check passes.**  Registered in advance: if the structured
controls' `k_min` were not appreciably below the random median at `m = 4`, the
instrument would have no resolving power and no comparative statement would be
allowed.  The controls come in at 0, 0, 3, 3, 3 against a random median of 5, with only 3 of
60 random tables at or below the best structured control's 3.  The instrument
resolves.

**Rule 30 sits clearly above every structured control, and exactly on the
random median.**  At `m = 4` it needs 5 gates where the linear-CA columns need
0 to 3 and parity needs 3, while the median uniform random 4-bit table also
needs 5.  This is the one comparative statement the design supports, and it is
the registered null: the centre column does not look like a cheap automatic
sequence at this width, and it does not look unusual against random either.

**Three reasons not to read more into it than that.**

1. *Discreteness.*  Random 4-bit `k_min` lives on a support of about four
   integers.  A percentile rank of Rule 30 within that is one integer of
   movement on a four-point scale, not a measurement.
   *Interpretation frame for the weight-matched null, written before that
   number was seen:* balanced tables synthesize harder than sparse ones, so the
   weight-9 median may well come back at 6, putting Rule 30's 5 *below* it.
   That would be the shape of a false compression signal and is not to be read
   as one.  **This is what happened** -- weight-matched median 6, Rule 30 at 5.
   The frame was fixed in advance precisely so this outcome could not be
   written up as a discovery.  A one-gate deviation from the weight-matched median is exactly the
   size of the offset swing in point 2, i.e. inside the noise floor of a pure
   bookkeeping choice.  Only a deviation of two or more gates would be worth a
   second look at this arity, and the support does not have room for one.
2. *The offset swing is the noise floor.*  Changing nothing but the indexing
   convention -- whether `c(0)` is the seed row or the row after -- moves
   `k_min` from 5 to 6 at `m = 4`.  That is a full gate, the same magnitude as
   the entire gap between Rule 30 and the random median.  A quantity that a
   bookkeeping choice moves as far as the effect does is not resolving the
   effect.
3. *The arity ceiling dominates the growth question.*  The naive discriminator
   ("`k_min` linear in `N` = incompressible, sublinear = shortcut") **cannot
   fire** at `m <= 5`, because `u(m) <= 12` there for *every* function of that
   arity.  Sublinearity in `N = 2^m` is guaranteed by arity alone and says
   nothing about Rule 30.  This is why the pre-registration dropped it as the
   discriminator before the runs rather than after.  No trend line is drawn
   across the `m` points here, and the four-point growth curve should not be
   presented as evidence of incompressibility.

## 7. What this does and does not establish

**Established, unconditionally:** `k_min(m=4) = 5` for Rule 30's centre column
over the full `B2` chain model -- a small exact theorem, machine-checked, with
the UNSAT at `k = 4` confirmed by two independent solvers and reproduced with
all optional symmetry breaks disabled.  Plus the same for `m = 3`.

**Established, conditional on a symmetry break validated at lower arity:**
`k_min(m=5) >= 7` -- no chain of six or fewer gates computes `c` on `[0, 32)`.
The matching upper bound `<= 12` is inherited from `u(5)`, not earned here.

**Not established, and cannot be by this method:**

* **P3 is untouched.**  P3 is an asymptotic claim about cost per bit as
  `n -> infinity`.  Every number here concerns one finite width.  This is the
  same structural gap as obstruction H: an exhaustive finite computation does
  not close an asymptotic question, no matter how complete it is within its
  bound.  Nothing in this document should be cited as evidence for or against
  computational irreducibility.
* **No compression signal, and no evidence against one.**  The registered
  strong outcome (Rule 30 at or below the structured controls, or in the bottom
  decile of the null, at both `m = 4` and `m = 5`) did not occur.  The null
  occurred.  But the null occurring at `m <= 5` is close to uninformative for
  the reasons in section 6, and should not be reported as "Rule 30 is
  incompressible" in any form.
* **`k_min` is not a compression rate across `m`.**  The target function
  changes with `m` -- a longer prefix, not a refinement of the same object --
  so the values are not commensurable as a sequence.

**What is actually worth carrying forward:** the feasibility wall is now
measured rather than guessed, so the next person knows where the method dies
and does not need to rediscover it; the encoding, controls and validation
harness are reusable for any other sequence someone wants to put the same
question to; and the object `a22_p3_succinct_index` flagged as open has now had
its first computation, with a result rather than a plan.

## 8. Suggested register additions (not applied -- PATH.md untouched)

For the user to accept or reject:

1. A row recording the uniform succinct-index question as *probed, bounded
   result obtained, still open* -- distinct from the rows obstruction I kills
   (9, 81, 85, 87) and from T4's non-uniform territory.
2. A note under 8.7 making explicit the uniform vs non-uniform distinction that
   `a22_p3_succinct_index` observed "the register does not currently draw
   anywhere."
3. A one-line feasibility fact for future arms: complete `B2` exact synthesis
   with this encoding resolves everything up to `m = 5, k = 6` (357 s) and
   nothing beyond -- `m = 5, k = 7` runs past 86 minutes unresolved in either
   direction, and `m = 6` is unreachable by orders of magnitude.  A future arm
   wanting `m = 6` needs a different encoding (topology families, DAG-canonical
   symmetry breaking, distributed portfolio), not more patience.

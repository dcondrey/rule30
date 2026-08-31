# Rule 30 center column: a ranked path, and the filter that ranks it

Status: **route map, not a proof.**  Nothing here proves center-column
nonperiodicity.  Every identity below is verified exactly; every route below
carries a kill condition.

## 0. The filter

Rule 90 is left permutive and its lone-seed center column *is* eventually
periodic (identically zero after `t=0`).  Kopra names this obstruction himself
(arXiv:2202.13809): "the set of rapidly left expansive CA cannot be such a
class, because it contains the additive ECA Rule 90 ... that produces a single
eventually periodic column starting from the configuration with a single 1 at
the origin."

So the ranking criterion for every route is one question:

> Does this argument fail for Rule 90?

An argument that would also apply to Rule 90 proves nothing, whatever else it
does.  This filter is what killed the expansivity family, and it is the only
filter in this problem with a track record.  Routes below are ordered by how
cleanly they pass it.

### 0.1 Second filter: single-column sensitivity (added 2026-08-30)

P1 and P2 are statements about ONE column.  So ask of every proposed quantity:

> Overwrite column 0 of the lone-seed diagram with a periodic word, changing
> nothing else.  Does the quantity move?

If it moves by `O(1/W)` or less in the window width `W`, the quantity is
continuous under a density-zero modification and **cannot decide P1 or P2**,
however strongly it discriminates between rules.  This is R6 obstruction (i)
below, stated generally, and it retires an entire family -- geometric,
spectral, topological, information-theoretic -- in advance and for a few
seconds of compute.

Measured for three geometric proposals in
`experiments/rule30/p_geometric_attack/GEOMETRIC-TRIAGE.md`: hyperbolic
lightcone embedding, curvature of a multilinear relaxation, and spectral
dimension of a Dirac operator all move by `O(1/W)` (the spectral dimension
halving to three digits per doubling of `W`) while a positive control that
reads column 0 moves by 96%.  All three separate Rule 30 from Rule 90 by
26-98%.  **Rule-sensitivity is not evidence of P1-relevance.**
`discriminator.py` takes a new statistic as a one-function drop-in; run a
proposal through this filter before building anything.

## 0.5 PRIOR WORK IN THIS REPO — read before crediting anything below

The pin mechanism in section 1 is **not new to this repo.**  It was already
present in both code and proof before this document was written, and an earlier
draft of this file wrongly presented it as new.  Specifically:

* `experiments/rule30/inverse_trace_probe.py:135-160`, `reconstruct_left_column`,
  implements the rotation `s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1))`
  directly, with the "one future centre value is consumed" bookkeeping.
* `RESULTS-eventual-period.md:88-100` gives the defect form under a periodic
  centre, `d_t(-1) = (1 XOR c_t) AND d_t(1)`, and then the **PROVED run-of-ones
  wedge**, whose stated conclusion is verbatim: "A nonconstant periodic word has
  bounded one-runs, so this gives only a bounded wedge, not a descent to
  contradiction."
* `experiments/rule30/periodicity_bridge_probe.py:191-215`,
  `defect_identity_violations`, regression-checks that identity.
* `test_inverse_trace_probe.py:115-117` pins "centre-one erases, centre-zero
  passes" as a regression: zero-phase defect front `range(64,32,-1)`, one-phase
  `(None,)*32`.

So route R3 below was **already proved dead here**, on paper, before it was
re-measured.  The re-measurement is a duplicate, and the paper proof is the
stronger statement.  R1 is likewise this repo's own stated second exact target
(`RESULTS-eventual-period.md:52-55`), in the repo's own `c_t / r_t / l_t`
notation, with the recorded outcome "No such derivation survived the tests
below."

What is *actually* contributed by this document is narrower and should be
described as exactly this and nothing more:

1. the Rule 90 discriminator table (section 1.1), as an explicit ranking filter;
2. the absolute-value propagation measurement (section 3.1), which quantifies
   the wall in determined-cell counts rather than in defect fronts, and which
   is new code — the ledger confirms no existing script measures centre-trace
   one-run length or density;
3. the explicit `<=>` form of the reduction in section 2;
4. the observation that `O(log t)` has now appeared in three independent
   representations.

Everything else restates prior repo work.

## 1. The OR latch pin

Rule 30 is `s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))`.  When `s(t,x)=1` the
OR saturates regardless of the right neighbour.  Hence, everywhere in the
space-time diagram:

```text
s(t,x) = 1   =>   s(t,x-1) = NOT s(t+1,x)
```

Equivalently: **wherever the diagram has a 1, the cell below it is the negation
of the cell to its upper-left.**  This is a Rule-30 identity, not an assumption,
and it needs no knowledge of anything to the right of `x`.

*Verified.*  Lone seed, `T=300`, all columns: 45,477 ones, **zero violations**.
Rule 90 violates the same identity at **all 7,227** of its ones.

### The pin is exactly the additive/nonlinear separator

For a left-permutive ECA `s(t+1,x) = s(t,x-1) XOR g(s(t,x), s(t,x+1))`, the
left neighbour is pinned at center value `b` iff `g(b,0) = g(b,1)`.  Enumerated:

| rule | pins on center value |
|---|---|
| 30 | `c_t = 1` |
| 45 | `c_t = 1` |
| 75 | `c_t = 0` |
| 60 | both (degenerate: right-independent) |
| **90** | **none** |
| **150** | **none** |
| **105** | **none** |

The additive rules pin on nothing.  Rule 30 pins because of the OR.  **Any
argument built on the pin passes the Rule 90 filter by construction.**  That is
the whole reason to prefer this route.

## 2. What the pin buys immediately

Write `c_t = s(t,0)`, `l_t = s(t,-1)`, `r_t = s(t,1)`.

**Constant-one case, one line.**  If `c_t = 1` for all large `t`, the pin gives
`l_t = 1 XOR c_{t+1} = 0` for all large `t`.  So column `-1` is eventually
identically zero, hence eventually periodic, and columns `-1, 0` together are an
eventually periodic width-two trace of a finite configuration.  That contradicts
Jen 1990 Prop. 3 / Kopra Thm 3.5.  **QED.**

This reproves `RESULTS-inverse-trace.md`'s constant-one theorem in a single
step.  It is validation of the mechanism, not a new result, and should be
labelled as such.  Its value is as evidence that the pin is the right lens:
the strategy it suggests is *make column `-1` eventually periodic*, and the
constant-one case is the trivial instance of that strategy.

**The general reduction.**  From the rule at `x=0`,
`l_t = c_{t+1} XOR (c_t OR r_t)`, so

```text
c_t = 1  =>  l_t = 1 XOR c_{t+1}          (free, from the trace alone)
c_t = 0  =>  l_t = c_{t+1} XOR r_t        (needs the right neighbour)
```

Therefore, **assuming the center trace is eventually periodic:**

> column `-1` is eventually periodic  <=>  `r_t` restricted to `{t : c_t = 0}`
> is eventually periodic.

and column `-1` eventually periodic closes the problem via Jen/Kopra.  Half the
obligation is already discharged by the pin.  What remains is one column on the
zero-set of the trace.

## 3. The rightward cascade

The pin at `x=1` reads `r_t = 1 => r_{t+1} = 1 XOR c_t`.  Two consequences, both
verified exactly on the lone seed to `T=300` with zero violations:

```text
r_t = 1 and c_t = 0   =>   r_{t+1} = 1
every 1 -> 0 transition of r occurs at a time with c_t = 1
```

So the right neighbour's 1-runs are *terminated by* the center's 1-positions.
`r` is fully determined by `c` at every time `r_t = 1`; its only freedom is at
times immediately following `r_t = 0`, where `r_{t+1} = c_t XOR s(t,2)` pulls in
column 2.  The same statement holds at every column (verified at `x = 1,2,3,5,10`).

If `c` is eventually periodic, the transition times of `r` are confined to a
periodic set.  This is a strong constraint on `r`, and it is the concrete form
of the remaining obligation in section 2.

### 3.1 MEASURED: what the pin actually determines, and the third `O(log t)` wall

Starting from the centre column alone and applying every exact Rule 30
inference to a fixpoint (forward rule; the 1-pin leftward; the 0-pin rightward,
`s(t,x)=0 => s(t,x+1) = s(t+1,x) XOR s(t,x-1)`; and left-neighbour recovery from
a known OR), over `T=220` and columns `-90..90`:

```text
determined 457 / 40001 cells (1.14%), inconsistencies 0
```

Per column, times determined out of 221:

| column | 0 | -1 | -2 | -3 | -4 | -5 | -6 | -7 | >= +1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| determined | 221 | 115 | 63 | 31 | 14 | 8 | 4 | >0 | **0** |

Two facts, both decisive:

1. **The density halves per column leftward.**  Depth `k` requires a run of
   about `k` ones in the trace, and runs are geometrically distributed, so the
   determined region is a triangle of depth `O(log T)`.  At `T=220` it reaches
   column `-7`.
2. **Nothing propagates rightward at all.**  Zero cells determined at `x >= 1`.
   The 0-pin needs the left neighbour, which is exactly what is missing.

Zero inconsistencies over 457 determinations independently validates the
propagator against the true diagram.

**This is the third independent representation to yield `O(log t)` reach**:
the right-cone diagonals (`RESULTS-diagonal-periodicity.md`), the run-length
bootstrap (R3), and now pin propagation.  Three different encodings, the same
wall, arising each time from a one-bit-per-step information loss.  Treat
`O(log t)` as a property of the problem under trace-anchored analysis, not as
an artifact of any one representation.  A route that does not say *why it beats
`O(log t)`* should be assumed to hit it.

**What this does NOT kill: R1.**  The propagation above starts from the *true*
lone-seed trace.  R1 assumes, for contradiction, that the trace is eventually
*periodic* — a strong global hypothesis that the propagator never uses.  R1 is a
counting and structure question, not a propagation-depth question, and the
measurement above has no bearing on it.  Keep them separate; conflating them
would retire the one live route on evidence about a different one.

## 4. Ranked routes

**R1 — close the zero-set obligation.  Best route, and it is this repo's own
stated second exact target, not a new idea.**
`RESULTS-eventual-period.md:52-55`: "Jen's Proposition 3 and Kopra's width-two
theorem give a second exact target: derive an eventually periodic adjacent
column from the periodic centre.  That would supply a forbidden second periodic
column.  No such derivation survived the tests below."
Show that `c` eventually periodic forces `r` eventually periodic on `{c_t = 0}`.
By section 2 that yields column `-1` eventually periodic and closes the problem.
Passes the Rule 90 filter (built on the pin).  The only thing added here is the
explicit `<=>`, which localises the whole remaining obligation to one column on
the trace's zero-set, the `c_t = 1` half being discharged by the pin.
*Kill condition:* exhibit a Rule 30 space-time diagram, or a consistent formal
model of one, with `c` eventually periodic and `r` provably aperiodic on the
zero-set.  If the zero-set obligation is not decidable from `c` alone, R1 dies
and section 3's cascade is the fallback.

**R2 — cascade descent.  KILLED, by its own stated kill condition.**
The kill condition was "the cascade's determination density decays, so that
after `k` columns the fraction of trace-determined cells goes to zero."  It was
measured immediately (section 3.1 below).  It fires.  **Do not retry.**

**R3 — bounded-depth pin bootstrap.  PROVED dead in `RESULTS-eventual-period.md:95-100`,
before this document existed.**
That doc's run-of-ones wedge is a proof, not a measurement: a nonconstant
periodic word has bounded one-runs, hence a bounded wedge and no descent.  The
run-length measurement recorded here (max run 6 in 300 steps, geometric decay)
is a duplicate of a settled result and adds only the empirical distribution.
**Do not build on this, and do not re-measure it a third time.**

**R4 — anything anchored at the right boundary.  Closed.**
See `RESULTS-diagonal-periodicity.md`: right-boundary regularity reaches
`O(log t)` diagonals against a target at diagonal `t`.

**R5 — anything using only left permutivity or expansivity.  Closed by Rule 90.**

**R6 — complexity/entropy boundary framings ("Kolmogorov-complexity boundary",
entropy-gradient, "incompressible zone traps the centre column").  Closed as a
proof route.  Assessed 2026-08-30 against a literature sweep; do not retry.**
The literal Kolmogorov version is false in two lines: every window of the
lone-seed diagram is the output of a constant program plus coordinates, so
`K(window at time t) <= log t + log x + O(1)`.  The diagram contains no
algorithmically incompressible region anywhere; the right side is pseudorandom
(maximal statistical entropy, near-zero algorithmic content), and that gap *is*
the phenomenon.  The statistical rescue (block entropy / LZ / BDM in place of
`K`) yields a real boundary, but it is prior art (NKS p.871: order/disorder
boundary drifts ~0.252 cells/step, measured; distinct from the 0.2428
damage-front speed of p.949), and the inference from it fails three independent
ways: (i) 2D entropy density is insensitive to any single column — an i.i.d.
plane with column 0 overwritten periodic keeps `(w-1)/w`-maximal local entropy
in every window, so "centre column inside a maximal-entropy zone" cannot imply
aperiodicity; (ii) Champernowne's constant has maximal block entropy with bit
`n` computable in polylog time, so maximal-entropy surroundings cannot imply
Problem 3's `Omega(n)`; (iii) the invoked "conservation laws of information"
are Hedlund measure preservation plus ergodicity, already recorded in
`PREREGISTRATION.md` Arm 2 as proven and landing one measure-zero step short of
the lone-seed orbit.  The resource-bounded retreat (time-bounded `K` boundary)
is Problem 3 restated, not bypassed.  The mechanism uses no property of Rule 30
that Rule 90 lacks at the level where it breaks, so it also fails the section 0
filter in spirit: killed rule-independently by (i).
*Remnant, empirical only:* a 2026-08-30 researcher sweep found no published
spatially resolved complexity map `C(x,t)` over the Rule 30 grid, no measured
fluctuation universality class for the 0.252 boundary (diffusive `t^{1/2}` vs
KPZ `t^{1/3}`; NKS says only "roughly random fluctuations"), and no proof that
either boundary's drift velocity exists.  Nearest prior art: Zenil 2010
(one compressed length per rule, not spatial), Zenil et al. PeerJ CS 2015
(block-decomposes Rule 30 but sums to one number), Shalizi et al. PRE 2006
(local statistical complexity fields, rules 110/54, no Rule 30).  A boundary
drift + fluctuation-scaling measurement would be a standalone small paper in
that citation graph, framed as measurement.  It cannot touch the prizes and
does not run without its own pre-registration.

**R7 — the periodicity ladder: per-period exclusion by omega-automata,
mechanizing R1.  RUN 2026-08-30.  Calibration PASSED; all open cases p = 2..8
NONEMPTY with verified witnesses; verdict independent of depth (R and k) over
the whole decided range.  `Thm(1)` mechanised, no `Thm(p)` for p >= 2.  Do NOT
re-run at larger R or k, and do NOT raise the Diff bound Q — both directions
are now measured closed by the same mechanism, constraint and freedom growing
together.  `RESULTS-ladder-rung0.md` section 3 retires depth; section 6
retires Q and corrects all three of section 4's assessments.  The one
constraint found that reaches the unmodelled region x > R is the full 1-pin
at the boundary column, which prunes 58% and flips no verdict, and which costs
the Rule 90 soundness control.**
Target family, one theorem per period: *Thm(p): no word eventually periodic
with period `p` is the centre column of a Rule 30 diagram satisfying the
lone-seed wedge constraints, for ANY transient length.*  Qualitatively beyond
the 10^9-bit data check, which the prize announcement itself flags as unable
to exclude "a trillion-step transient".
Encoding: treat columns `(c, r)` as omega-words.  The inverse transduction
`col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))` is a delay-1
letter-to-letter transducer, so the depth-`k` leftward composition is
omega-regular; the slope-1 zero wedge `col_{-j}(t) = 0` for `t < j` and the
all-ones left edge are safety constraints; "`c` eventually `p`-periodic" is
Buchi (guess onset nondeterministically, verify forever).  Two decidable modes
per `(p, k)`: (i) emptiness of the constraint intersection `S_k(p)` proves
Thm(p) outright; (ii) inclusion `S_k(p) ⊆ {col_{-1} eventually periodic with
period ≤ Q}` hands the contradiction to Kopra Thm 3.5 / Jen Prop 3 — mode (ii)
is exactly R1's zero-set obligation discharged by machine, and it inherits the
pin, passing the Rule 90 filter by construction.
Calibration rung, run FIRST: `p = 1` must rederive this repo's constant-case
theorems at small `k` via mode (ii), and the same pipeline on Rule 90 must
stay nonempty for its true eventually-zero column (soundness control).  Fails
calibration → kill.
Why the `O(log t)` wall does not obviously apply: the wall governs
bounded-depth propagation from the trace; Buchi emptiness/inclusion consumes
the global infinite-horizon periodicity hypothesis via lasso structure, which
no finite window sees.  The expected kill mode is state blowup instead
(Gershenson CMU-CS-10-123 reports super-exponential growth in the phase-space
FO setting).
Prior art stops at: Sutner JCA 4(3) 2009 / Gershenson CMU-CS-10-123 (2010) /
Finkel JCA 6 (2011): omega-automatic model checking of ECA phase space,
including Rule 30 `k`-cycles quantified over all configurations, never the
constraint system of one designated orbit's column with existentially
quantified transient.  Kopra thesis Problem 3.1.13 poses W30 trace soficness
as open; irrelevant to soundness here, since each `S_k` is regular by
construction.  No per-period exclusion exists for any `p`.
Endgame: certificates for `p = 1, 2, 3, ...` inspected for `p`-uniform
structure; a uniform certificate is Problem 1 entire.  Realistic output:
Thm(p) for small `p`, a citable note either way.

**RUNG 0 RESULT (2026-08-30): built, calibrated, run.  No new theorem.  See
`RESULTS-ladder-rung0.md`.**  Calibrations both fired as designed and are
labelled validation, not discovery: the constant-one tail empties at `R=1`
(111 states) and the zero tail empties at `R=2` (405 states, open at `R=1`),
mechanically rederiving `RESULTS-inverse-trace.md` and the lone-seed corollary
of `RESULTS-zero-tail.md`.  Soundness control passed: Rule 90 with its true
eventually-zero column stays NONEMPTY at `R=1..5` with verified witnesses, and
the transduction matches exact simulation to `T=300` with 0 mismatches for both
rules.  Verified independently by the parent session: 7/7 tests pass, and
`p=2` nonemptiness at `R=3` reproduces for `q in {1,2,4,8}`.
**Open case `p=2` (tail `01`) is NONEMPTY everywhere reached** — `R<=6` with
`q<=16`, `R=7` with `q<=8`, `R=8` with `q=1` (5.6M states); `R=9` hit the
14M-state cap.  So Thm(2) is NOT proved and the `O(log t)` sibling wall is
replaced here by a state-count wall.
The rung's actual contribution is an **UNSUBSTANTIATED CLAIM, downgraded
2026-08-30 by parent-session audit: do NOT cite, do NOT build on.**  The text
below is the rung-0 agent's report as filed; a tree-wide grep finds the cycle
string in this paragraph and nowhere else, `RESULTS-ladder-rung0.md` contains no
such section, and there is no code, log, or `m=200` artifact anywhere.  It was
written into this file, and relayed to the user, as "proved" without an artifact
check.  Treat as MEASURED-AT-BEST pending reconstruction.  The claimed
**depth-3 escape family**: every witness has cycle `S·B^m` with `S=[2,0,0,1,0,2]`,
`B=[2,0,0,0]`, a period-4 defect train in columns `-1..3` carrying one phase
slip per cycle.  Claimed machine-verified to `m=200` with a pumping argument; **no artifact
supports either claim** (audit 2026-08-30).  `a7_ladder_realizability` states
explicitly at its section 5 that nothing there re-derives this family.  Consequence:
**for every `q`, the `R=3` ladder is nonempty, so no choice of `q` closes
`p=2` at fixed depth 3**, and BFS shows the slip surviving to `R=8`.
Rung 1, sharpened: does any finite `R` kill the slip, or does it extend to a
full half-plane?  The latter would prove this ladder undecides `p=2` entirely.

**RUNG 1 RESULT (2026-08-30): NEITHER branch resolved.  No Thm(2), no
limitation theorem.  See `RESULTS-ladder-rung1.md`.**  NONEMPTY at every
decided depth `R <= 7`, with and without the pin, all witnesses independently
re-verified, no state caps hit.  15/15 tests pass (parent-verified).
Three things did close, and they retire two levers:
1. **The boundary pin is NOT an independent constraint axis (proved).**
   Lemma 1: a letter word admits a consistent `col_{R+1}` iff
   `col_R(t)=1 => col_{R-1}(t) = NOT col_R(t+1)`.  So the pin *is* the
   solvability condition for the one unmodelled column, giving the sandwich
   `plain(R+1) subset pin(R) subset plain(R)`.  Hence `pin(R)` EMPTY implies
   `plain(R+1)` EMPTY: the pin buys strictly less than one column of depth and
   cannot decide `p=2` unless depth alone does.  This also *explains* the
   observed outward relocation of the phase slip: the pin constrains column
   `R` while leaving `R+1` free, recreating the very gap it closes.
   "Add the pin" is retired the way rung 0 retired "run it deeper".
2. **Correction to the parent's briefing, and a repair.**  The pin is
   rule-dependent for a principled reason: Rule 90's extendability condition
   is `col_{R+1}(t) = col_R(t+1) XOR col_{R-1}(t)`, always uniquely solvable,
   hence vacuous.  Applying *Rule 30's* pin to Rule 90 destroys the control
   rather than testing it.  Using each rule's own condition, the Rule 90
   control SURVIVES at NONEMPTY for `R=1..5`, repairing the missing section-0
   soundness control that rung 0 section 6 had recorded as unavoidable.  The
   pin also strictly tightens: rung 0's `w=0`, `R=1` escape is now EMPTY.
3. **Stabilization is FALSIFIED, so the cheap limitation theorem is closed.**
   Minimized tail-language sizes (bisimulation classes), plain / pin:
   `R=1` 10/9, `R=2` 15/20, `R=3` 34/44, `R=4` 73/91, `R=5` 140/165,
   `R=6` 229/267, `R=7` 349/466.  Growth is `~R^2.75` (2.761 plain vs 2.741
   pin, agreeing to 0.02 — the measured shadow of the sandwich) against a
   `4^R` raw encoding.  Unbounded, so no stabilization; but polynomially small
   against an exponential encoding, which is exactly why the verdict never
   moves.
Lemma 4 (exhaustive over all 16 states): every time-2-periodic letter tail
collapses within 3 leftward steps to the cycle `((1,1),(0,0)) <-> ((0,0),(1,1))`
whose columns are constant in time, so no short-period tail witnesses `01` at
`R >= 4`.  That kills the obvious `R`-uniform construction and explains the
measured witness cycle lengths of 4 to 18.
Method note, kept honest: determinize-then-minimize on the projected letter
language is exponential and did not terminate at `R=1`; the bisimulation
quotient is a coarser polynomial substitute, and the dichotomy above should be
read at that strength.
Named remaining gap: saturation (no wedge check fires past `R+2k+1`) and the
prefix are in hand; **realizability** — an alternating `col_0` with an
aperiodic `col_{-1}` at every `R` — is not.  That is the next target.
Probative object is the minimized projected tail language and its
stabilization-vs-growth dichotomy, NOT raw product-state growth
(`S(R) = 16, 64, 256, 896, 2944, 10752, 38400`, single SCC throughout), which
is an artifact of the encoding and proves nothing about Problem 1.

**R8 — invariant-measure classification of the vertical orbit closure.
PROPOSED, theory arm for prize Problem 2.  Sweep-verified unexplored.**
Object: `Y` = closure of the vertical (time) shifts of the lone-seed diagram
in `{0,1}^{Z^2}`.  Sufficient target, strictly weaker than unique ergodicity:
*every vertical-shift-invariant measure on `Y` assigns the centre cell density
1/2.*  Then every weak-* limit point of the empirical averages along the
column agrees, so the density exists and equals 1/2 at the actual point.
This is the correct shape against the Arm 2 obstruction: orbit-closure
classification converts almost-everywhere statements into everywhere
statements.
Known inputs: uniform Bernoulli invariance and the two-line i.i.d.-trace count
(Taati arXiv:1505.06464 §2.4; NKS note 10-10).  Every published rigidity
theorem requires algebraic/bipermutative structure (Host-Maass-Martínez DCDS
2003, Pivato DCDS 2005, Sablik ETDS 2007, Tal arXiv:2604.10124); Rule 30 is
left-permutative, nonlinear, outside all of them, and Pivato's survey names
the nonlinear case as an open gap.  Rowland-Yassawi CJM 72 (2020) ran exactly
this program (invariant measures from single-seed spacetime diagrams) for
LINEAR rules; the nonlinear analog is unposed in print.
Filter: for Rule 90 the claim is FALSE (its `Y` carries degenerate invariant
measures from the eventually-zero centre column), so any proof must exploit
non-additivity; a technique that would also prove it for Rule 90 is broken.
Cheap disconfirming diagnostic first: unique ergodicity predicts uniform
convergence of block frequencies along the column across starting depths;
measurable now.  Nonuniform convergence kills unique ergodicity and retreats
to the all-measures target; deep-window frequencies drifting from 1/2 would
be evidence against the route entirely, and news on its own.
Honest risk, named: controlling what `Y` contains may require knowing the
column; the circularity is the research question.

**DIAGNOSTIC RESULT (2026-08-30): route stays alive; no theorem.  See
`RESULTS-orbit-closure-diagnostic.md`.**  `T = 1,100,000` (smallest length
admitting the full window ladder to `W = 2^20`).  Block-frequency sup-deviations
decay with slope `-0.483` to `-0.532` in `log2 W` for `L = 1..12`, i.e. the
`W^{-1/2}` law, and sit inside the 20-seed i.i.d. Bernoulli(1/2) band at
essentially every window and depth (1 exceedance in 25 cells at `L=2, W=2^14`,
within the multiple-comparison rate).  None of the three pre-registered
disconfirming criteria fired: no deep-window drift, no depth-dependent plateau,
no exceedance cluster.  Rule 90 control PASSED at every cell, saturating the
exact `1 - 2^-L` value, so the pipeline detects the failure mode it was built
to detect.  Verdict as pre-registered: CONSISTENT WITH unique ergodicity, which
proves nothing.  The route is not killed and not advanced.

**R9 — proof-complexity irreducibility.  PROPOSED, restricted-model arm for
prize Problem 3.  Sweep-verified unexplored.**
Encode the light cone as a CNF (each cell one XOR-of-OR constraint); row
simulation gives `O(n^2)`-size resolution derivations of the centre value;
target a superlinear lower bound on any resolution (or PC/bounded-depth
Frege) derivation of `c_n`.  Any such bound would be the first lower-bound
theorem of any kind about Rule 30 prediction and an unconditional,
model-relative formalization of computational irreducibility (Zwirn-Delahaye's
is computability-theoretic and proves no bounds for concrete rules).
Stated gap, kept in the same sentence as any result: a proof-complexity bound
does NOT resolve Wolfram's Turing-machine formulation; systems with extension
simulate fast algorithms.
Prior art stops at: Cavagnetto 2011 and Kapytka arXiv:2604.01041 (2026), the
only proof-complexity-meets-CA line, both about inverse/injectivity, never
prediction.  The grid-Tseitin canon (Dantchev-Riis FOCS 2001 `2^Ω(n)`
resolution; Håstad JACM 2021; Håstad-Risse FOCS 2022) is the toolbox, with a
named transfer obstruction: Tseitin is unsatisfiable by a global parity
argument, while this instance is satisfiable with a unique solution, an
implicational/pebbling-like regime where superlinear resolution bounds barely
exist.  That regime gap is why it is hard and why it is open.
Filter: Rule 90 cells have closed-form binomial-parity values, so short
derivations plausibly exist there; a technique insensitive to the OR
nonlinearity proves too much.  Inverted kill condition worth wanting: a
sub-quadratic resolution derivation family for Rule 30 would be a publishable
upper bound and a mechanism candidate for the Arm 3 tournament.

**PROBE RESULT (2026-08-30): precondition holds; no lower bound, no shortcut.
See `RESULTS-proof-complexity-probe.md`.**  Metric is a cell-level GROUP MUS
(one selector per cell), after the prereg caught that the clause-level MUS is
degenerate: the firing-clause set is a MUS of ~the whole diamond for any rule,
so it measures cone area, not rule structure.  Re-verified from the raw JSON by
the parent session.  Rule 30: GMUS `= 33, 119, 445, 1604, 6535, 25108` cells at
`n = 8..256`, a near-constant **76-82% of the backward diamond at every band**,
fitted exponent **1.932** (`n >= 16`); largest band `n=256` took 2021 s.  The
cell set is left-heavy 2:1 (16,380 left / 8,472 right at `n=256`), matching the
damage-cone asymmetry.  Rule 90 control: GMUS `= 17, 43, 113, 307, 857`, an
**exact match to the analytic odd-binomial Sierpinski set at every band and
every seed**, with the fraction *decaying* `0.415 -> 0.103`.  That contrast is
the pipeline's separation proof: constant fraction for the nonlinear rule,
vanishing fraction for the additive one, so the probe measures rule structure
and passes the section 0 filter.
**The inverted outcome did NOT fire.**  No small sufficient constraint set for
Rule 30, hence no centre-column shortcut candidate for the Arm 3 tournament.
This supports the R9 conjecture's *precondition* (the cone is derivationally
necessary in the axiom-subset sense) and is NOT evidence of a derivation-length
lower bound; it says nothing whatever about Wolfram's Turing-machine Problem 3.
Aside, not a finding: Rule 90's `n=256` GMUS stalled in CDCL parity reasoning
(Tseitin-style hardness in the control), so that ladder stops at 128 with 5
usable bands, above the kill threshold.

This is a $10,000 prize problem, open since 2019 and worked by Wolfram, Jen,
Kopra and Rowland, with no prize claimed.  The realistic output of R1/R2 is a
further partial theorem in the same family as the zero-tail note, not a
solution.  The pin's demonstrated value so far is exactly one thing: it collapses
the constant-one case to a line and it passes the Rule 90 filter by
construction.  That is a reason to spend the next cycle here rather than a
reason to expect the problem to fall.

## 6. Cross-check: DONE, and it went against this document

The inventory landed and is recorded in section 0.5.  The reduction in section 2
*is* `RESULTS-eventual-period.md`'s stated second exact target restated, and R3
was already proved dead there.  Section 0.5 is the authoritative statement of
what this file contributes; read it before citing anything here as new.

## 7. Complete attempt register

Every approach tried in this tree, one row each, with the recorded reason it
stopped.  Compiled 2026-08-30 from all 46 documents under `docs/rule30/`,
`docs/rule30/overnight/`, `docs/rule30/paper/` and the assessment files under
`experiments/rule30/*/`.  The ranking filter that orders routes R1-R9 is
section 0; it is not restated here.

**All three Wolfram prize problems remain open as of 2026-08-30.**  Nothing in
this tree resolves P1 (non-periodicity), P2 (limiting density) or P3
(computational effort), and no prize has been claimed.

**Proved versus measured, stated once.**  Exactly two theorems in this tree
bear on a prize problem, and both concern eventually *constant* centres, not
periodic ones: the zero-tail theorem (`RESULTS-zero-tail.md`, row 25) and the
constant-one / all-one-fiber case (`RESULTS-inverse-trace.md`,
`RESULTS-eventual-period.md`, row 26).  Together they exclude every eventually
constant lone-seed centre and nothing more.  Other theorems here are real but
sit outside the prize statements: the degree law `deg f_t = 2t-1` (row 43) is
about the arbitrary-input function family and its own write-up calls it
"provably inert" for P3; the pinned right-cone diagonals (row 33), the depth-4
diagonal pinning and counting rate (row 47), the ladder's Lemma 1 / Corollary
2 / Lemma 4 (row 7), and the alternating-fiber survivor automaton (row 41) are
proved lemmas about structure, not about periodicity.  Everything else in the
table is measurement, a negative, or infrastructure.  A measurement consistent
with a hypothesis is never recorded as PROVED: R8's block-frequency diagnostic
is "CONSISTENT WITH unique ergodicity, which proves nothing", and R9's GMUS
ladder "is NOT evidence of a derivation-length lower bound".

STATUS is exactly one of **PROVED** (a theorem was obtained), **KILLED**
(ruled out, reason given), STALLED (ran, no verdict, wall hit), NOT RUN
(deliberately declined), **OPEN** (still live), INFRA (tooling or validation,
not an attempt).

**Unverified premises, checked.**  One document rests on a genuinely
unverified external premise and is flagged in its row:
`paper/PUBLICATION-NOTES.md` (row 72), whose novelty claim turns on Jen 1986,
which is unread.  The compiling brief also described
`p3_circuit_attack/P3_ASSESSMENT.md` as resting on an unsourced "ANF theorem";
the register checked that and found otherwise.  That document cites
`overnight/RESULTS-anf.md`, where `deg f_t = 2t-1` is proved unconditionally
and re-checked by an independent third implementation (row 43).  The premise
is sound.  What is true of it, and of
`p_fringe_attack/FRINGE_ATTACK_ASSESSMENT.md`, is narrower and is recorded in
rows 63-66: both accepted the degree law as instructed and did no independent
check of it themselves.

### 7.1 The register

| # | Approach | Prize | Status | Why it stopped | Where |
|---|---|---|---|---|---|
| 1 | R1, close the zero-set obligation: show `c` eventually periodic forces `r` eventually periodic on `{c_t=0}` | 1 | **OPEN** | Best route; kill condition not fired.  "The only thing added here is the explicit `<=>`, which localises the whole remaining obligation to one column on the trace's zero-set." | `PATH.md` R1 |
| 2 | R2, cascade descent from the pin | 1 | **KILLED** | Its own kill condition fired on first measurement: determined 457/40001 cells (1.14%), density halves per column leftward, "zero cells determined at `x >= 1`".  "Do not retry." | `PATH.md` R2, 3.1; `pin_propagation_probe.py` |
| 3 | R3, bounded-depth pin bootstrap (run-of-ones wedge descent) | 1 | **KILLED** | Proved dead before it was re-measured: "A nonconstant periodic word has bounded one-runs, so this gives only a bounded wedge, not a descent to contradiction." | `PATH.md` R3; `RESULTS-eventual-period.md:95-100` |
| 4 | R4, anything anchored at the right boundary | 1 | **KILLED** | Right-boundary regularity reaches `~2.4 log2(t)` diagonals against a target at diagonal `t`; the gap is exponential and grows. | `PATH.md` R4; row 34 |
| 5 | R5, anything using only left permutivity or expansivity | 1 | **KILLED** | Closed by Rule 90, which is left permutive and whose lone-seed centre column *is* eventually periodic (Kopra names the obstruction himself). | `PATH.md` R5, 0 |
| 6 | R6, complexity/entropy boundary framings (Kolmogorov boundary, entropy gradient, "incompressible zone") | 1,2,3 | **KILLED** | Literal version false in two lines (`K(window) <= log t + log x + O(1)`); the statistical rescue fails three ways, and obstruction (i) — 2D entropy density is insensitive to any single column — kills it rule-independently.  "Do not retry." | `PATH.md` R6 |
| 7 | R7, omega-automaton periodicity ladder: one exclusion theorem per period `p` | 1 | STALLED | Calibration passed and `Thm(1)` mechanised, but all open cases `p=2..8` NONEMPTY with verified witnesses at every decided depth; verdict uniform in `R`, `k` and `Q`, so depth, the pin and `Q` are all retired as levers.  Rung 1: "Neither branch closed."  Blocker is a state-count wall plus the free-boundary escape, not compute. | `PATH.md` R7; `RESULTS-ladder-rung0.md`; `RESULTS-ladder-rung1.md` |
| 8 | R8, invariant-measure classification of the vertical orbit closure | 2 | **OPEN** | Cheap disconfirming diagnostic ran; none of the three pre-registered criteria fired, Rule 90 control passed at every cell.  Verdict as pre-registered: "CONSISTENT WITH unique ergodicity, which proves nothing.  The route is not killed and not advanced." | `PATH.md` R8; `RESULTS-orbit-closure-diagnostic.md` |
| 9 | R9, proof-complexity irreducibility: superlinear derivation-length lower bound for `c_n` | 3 | **OPEN** | Precondition probe ran: Rule 30 GMUS is a near-constant 76-82% of the backward diamond, exponent 1.932, against Rule 90's exact odd-binomial set.  "The inverted outcome did NOT fire," and the result "is NOT evidence of a derivation-length lower bound".  The lower bound itself is unattempted. | `PATH.md` R9; `RESULTS-proof-complexity-probe.md` |
| 10 | Arm 1: Lean 4 / evolutionary search aimed at a P1 proof | 1 | NOT RUN | Deliberately declined: "'Find a lemma' is not a pre-registerable target, so this arm gets no compute."  Formalizing Jen's theorem is permitted only as pipeline validation. | `PREREGISTRATION.md` Arm 1 |
| 11 | Arm 2: search for the invariant measure giving density 1/2 | 2 | NOT RUN | Declined as discovery: the pathway is complete and lands one measure-zero step short — surjectivity gives uniform Bernoulli invariance and a.e. density 1/2, "an ergodic theorem says nothing about a measure-zero orbit". | `PREREGISTRATION.md` Arm 2 |
| 12 | Arm 3: sealed WASM tournament for a sub-quadratic centre-column algorithm | 3 | STALLED | The pre-registered kill fires only "after the budgeted generations"; the search never ran to that point.  "Still not enforced: the n >= 10^6 decision bands from the pre-registration.  Points here top out at n=4031."  What run 1 did establish is instrument validation — the known `O(n^2)` exponent recovered to three decimals (naive 1.9980, bit-parallel 1.9676, refit 1.985 on the top two points), so "No exponent improvement was found" — plus a fixed evaluator defect (a wall-clock epoch deadline made the reproduction gate a coin flip). | `PREREGISTRATION.md` Arm 3; `RESULTS-arm3-run1.md` |
| 13 | Arm 3 iteration 2: GF(2) seed grammar + Z3 rewrite validation for program search | 3 | NOT RUN | "Design only.  Nothing here is built."  The document also names its own ceiling: "local peephole rewrites will not connect `Theta(n^2)` forward-style composition to a sub-quadratic algorithm." | `SEARCH-ARCH.md` |
| 14 | Arm 4: AIR / frequency-domain shortcut, low-degree extension from the ordered boundary to the centre coefficient | 3 | **KILLED** | Pre-registered kill fired on the first run, on all three phase-0 measurements: BM linear complexity maximal through 16384, ANF degree exactly `2t-1`, density plateauing near 0.15.  "Both fired, by a wide margin... Phase 1 does not open."  Four prior errors also recorded (STARK sublinearity is a verifier property; composition squares degree; an FFT is a basis change; the ordered boundary is the left one). | `ARM4-frequency-domain.md`; `spectral_probe.py` |
| 15 | Arm 4 iteration 2: additive-FFT grammar over `GF(2^k)` with an AIR backend | 3 | NOT RUN | "Design only.  Nothing here is built," and "this arm is not pre-registered and must not run until it is."  Three independent disconfirmations recorded first, including that no `2^m`-th roots of unity exist in a binary field and that z3 4.16.0 here has no FiniteField sort (measured: field-lifted encoding times out at `n=32`). | `SEARCH-ARCH-AIR.md` |
| 16 | Arm 5: Rule 150 kernel plus sparse-error superposition, `s_n(0) = rule150(n) XOR parity(projected errors)` | 3 | **KILLED** | Stated kill fired: `N_eff ~ n^1.68`, decisively `omega(n)` — "834,156 live terms against a target of `o(10,000)`".  The escape hatch was then measured shut: row parity survives at exactly `n/2` and dyadic block XOR is 1/2 at every scale.  "Arm 5 is closed." | `ARM5-superposition.md`; `probe/src/main.rs` |
| 17 | Arm 6: finite 2-kernel / bounded-rank binary-digit query | 3 | **KILLED** | Both pre-registered kills fired: `>= 8191` distinct residual sequences through depth 12, GF(2) rank 512 at depth 9, Thue-Morse control saturating at two.  Boundary kept: "This arm is not a proof of non-automaticity." | `ARM6-binary-kernel.md`; `automaticity_probe.py` |
| 18 | Arm 7: exact dyadic spacetime tile grammar (quadtree DAG, Morton order, compression ensemble) | 3 | STALLED | "Promising diagnostic structure, not a Rule 30 shortcut."  DAG exponent 1.367 rising to ~1.48 over horizons 64-1024; tile perimeters determine interiors but carry `Theta(scale)` bits; every probe first constructs the full spacetime area.  Recompression, axial periodicity and dihedral quotients each closed separately.  The five-point contract is the unmet acceptance gate. | `ARM7-dyadic-spacetime-grammar.md`; `spacetime_grammar_probe.py`, `compression_ensemble_probe.py`, `boundary_signature_probe.py` |
| 19 | Bounded Crosstalk search for an exact dyadic tile composition algebra | 3 | **KILLED** | Zero surviving candidates: six critic rejections, "zero objective verification records", scientific release NOT ESTABLISHED.  Five repeatable failure fingerprints recorded.  Explicitly not a falsification of every dyadic algebra; the run's own synthesis over-reached and the release guard is what stopped it. | `RESULTS-crosstalk-arm7.md`; `runs/rule30-arm7/report.md` |
| 20 | Arm 8: centre-observational quotient, ROBDD of the arbitrary-input transfer function `F_h` | 3 | **KILLED** | Exponential growth ~1.88 per step in all five tested variable orders (right-to-left best, 47,909 nodes at `h=16`; allocation guard hit at `h=18`).  Scope kept narrow: "excludes only the five tested fixed variable orders". | `ARM8-center-observational-quotient.md`; `center_function_probe.py` |
| 21 | Bounded Crosstalk search for a query-specific single-seed algebra (transfer monoids) | 3 | **KILLED** | No candidate retained; the one executable contract, a truncated `GF(2)[x]/(x^k)` state, was reproduced verbatim and falsified: `first_mismatch=5 candidate=0 oracle=1`.  Stopping rule recorded: further generations "are likely to rename the missing nonlinear seam operation." | `RESULTS-crosstalk-arm8.md`; `transfer_monoid_probe.py`; `runs/rule30-arm8/report.md` |
| 22 | Crosstalk elimination run 1: evolve a mechanism outside the closed families | 3 | **KILLED** | "Zero surviving candidates."  All five frontier entries proposed the same object (dyadic blocks + assumed `O(1)` merge + binary-expansion combination) and four depend on the parity cancellation ARM5 had already measured false; the synthesis used `sorry` and was rejected as a policy violation. | `RESULTS-crosstalk-elimination-run.md` |
| 23 | Crosstalk elimination run 2, with typed structural exclusions | 3 | **KILLED** | Empty frontier, three `score_below_threshold` rejections: a left-permutive affine boundary map needing an unproved short period, an inverse-diagonal transfer matrix exact only for the Rule 150 linear component, and a carry-chain matrix conditional on an undefined `LEMMA_GATE`. | `RESULTS-crosstalk-elimination-run2.md` |
| 24 | Crosstalk elimination run 3: truncated nonlinear carry-polynomial transfer over `GF(2)[z]/(z^k)` | 3 | **KILLED** | Deterministic probe found a stronger failure than the critic: at `z=0` the asserted scalar is 1 for every positive `n`.  "KILL: first mismatch at n=2: candidate=1, ground_truth=0." | `RESULTS-crosstalk-elimination-run3.md`; `carry_polynomial_probe.py` |
| 25 | Zero-trace fiber classification for finite configurations (prefix-OR transducer, `C_m` invariant classes) | 1 | **PROVED** | Theorem obtained: no nonzero finitely supported configuration has an identically zero centre trace, hence the lone-seed centre is not eventually zero.  Sharp radius law `H_max = 2 ceil(w/2)` with `2^w - 1` extremal rows.  Rule-30-specific: the Rule 90 analogue is false (`{-1,+1}`).  Does **not** rule out a nonconstant eventual period. | `RESULTS-zero-tail.md`; `zero_tail_probe.py`; `Rule30ZeroTail.lean` |
| 26 | All-one trace fiber / constant-one case | 1 | **PROVED** | Theorem obtained: the all-one trace forces the checkerboard left half `L_k = 1` iff `k` positive even, which is infinite, so no finite row has constant-one trace.  With row 25 this excludes every eventually constant lone-seed centre.  Reproved in one line from the OR-latch pin, and rederived mechanically by the ladder at `p=1`. | `RESULTS-eventual-period.md`; `RESULTS-inverse-trace.md`; `PATH.md` §2 |
| 27 | Phase-labelled generalization of the prefix-OR latch to periodic words | 1 | **KILLED** | FALSIFIED at radius one: the finite row `{-1}` has trace `0 1 0 1 0 1 0 0`, agreeing with `01` through time 6, whereas the zero-word radius-one conflict occurs at time 3.  "A center-one phase removes rather than preserves the right-neighbor latch." | `RESULTS-zero-tail.md`, phase-labelled section |
| 28 | Inverse-trace continuation: reconstruct the forced left half from a periodic trace and the actual right half | 1 | STALLED | "The inverse map is exact and useful as a proof interface, but it has not yet produced a period-independent contradiction."  Strongest finite agreement `T=1855, p=148` breaks at depth 166.  The construction is standard left permutivity and "should not be reported as a new theorem". | `RESULTS-inverse-trace.md`; `inverse_trace_probe.py` |
| 29 | Periodic-mask contraction: hope that a periodic centre repeatedly erases right-column information | 1 | **KILLED** | FALSIFIED for every period word containing a zero: a discrepancy entering at a zero phase has its earliest defect time move one step earlier per reconstructed column and cannot be erased (front `64,63,...,33` over 32 columns; the one-phase perturbation is erased immediately). | `RESULTS-inverse-trace.md` |
| 30 | Bounded Crosstalk run for a period-uniform inverse-trace tail obstruction | 1 | **KILLED** | "Zero of 72 extracted claims had accepting objective verification, final synthesis was empty, and scientific release was `NOT_ESTABLISHED`"; two Lean artifacts contained `sorry`.  Native evolution hit the stage timeout.  No closed state, descent measure or period-uniform lemma supplied. | `RESULTS-inverse-trace.md`; `runs/rule30-inverse-trace/report.md` |
| 31 | Same-forward-orbit collision reduction: eventual `p`-periodicity iff some nonzero finite `y` on the orbit has `Tr_0(y) = Tr_0(F^p(y))` | 1 | **OPEN** | The equivalence is proved; the obligation it leaves is not.  "The minimal theorem still needed is: for every nonzero finite row `y` and every `p>=1`, `Tr_0(y) != Tr_0(F^p(y))`."  Named the highest-value next target, starting at period two, where "the missing step is a closed finite-state descent for that stroboscopic map". | `RESULTS-eventual-period.md` |
| 32 | Incremental SMT exhaustion of nonconstant periods (all rows to radius 8, periods to 6) | 1 | STALLED | Exact horizon table produced and inclusion-minimal UNSAT cores extracted, but "There is no stable one-bit conflict pattern in the cores: both their times and their sizes change with `w` and `p`."  Bounded exclusions are falsifiers, not evidence; "merely enlarging the SAT grid cannot prove it." | `RESULTS-eventual-period.md`; `eventual_period_probe.py` |
| 33 | Right-cone branch-free bit-parallel reconstruction plus a solver-free bounded support certificate | 1 | STALLED | 1824 sweeps over 14.9M right parts; every one forces a one, so nothing goes silent, but "The result is flat.  `min_deepest_one` sits within about 20 of `depth` for every `(p,W)` swept... There is no descent: nothing here shrinks the obligation to a finite check."  "Do not extend the sweep."  Its only new proved content is the three pinned diagonals. | `RESULTS-right-cone.md`; `right_cone_probe.py` |
| 34 | Right-cone diagonal periodicity as a route to the centre | 1 | **KILLED** | Diagonal pure periodicity with power-of-two period is KNOWN (Rowland 2006 Lemma 2, OEIS A094605), re-derived here as validation.  The verdict is quantitative: the periodic region reachable from the right boundary at time `t` is `~2.4 log2(t)` diagonals wide while the centre reads diagonal `t`, so "the center bit is always read strictly inside the first period of its diagonal, where periodicity constrains nothing."  Closes the whole boundary-anchored line. | `RESULTS-diagonal-periodicity.md`; `diagonal_period_probe.py` |
| 35 | Extending the constant-trace proof mechanism (forced left half forgets the right half) to nonconstant periods | 1 | **KILLED** | FALSIFIED by direct measurement: for `(01)^inf`, `(100)^inf`, `(110)^inf`, `(001010)^inf` the forced bit still differs across right parts at depth 512, in 505-512 of 512 positions.  "There is no transient after which the right half is forgotten." | `RESULTS-diagonal-periodicity.md` |
| 36 | Periodicity bridge: extend Kopra's width-two theorem to a nonlinear left-permutive subclass | 1 | **KILLED** | Of the eight quiescent left-permutive ECAs, four have nonlinear `g`; three of those have trivial sampled centres, so "adding the full-support condition reduces this binary class to Rule 30 itself and supplies no transferable theorem." | `RESULTS-periodicity-bridge.md` |
| 37 | Periodicity bridge: finite-delay reconstruction of an adjacent column from the centre | 1 | **KILLED** | Explicit counterexamples: an 18-step centre-agreement run at `p=148, t=1855` and a 24-step run at `p=110, t=13219`, both with adjacent-column defects throughout; Rule 90's run is infinite.  "Any class-wide finite-delay reconstruction lemma is therefore false." | `RESULTS-periodicity-bridge.md`; `periodicity_bridge_probe.py` |
| 38 | Periodicity bridge: centre-trace injectivity | 1 | **KILLED** | `{0}` and `{0,1}` have the same centre trace at every checked step, with the moving defect escaping rightward.  "Generic trace injectivity cannot bridge width two to width one." | `RESULTS-periodicity-bridge.md` |
| 39 | Periodicity bridge: doubling separation `s(p,0) != s(2p,0)` | 1 | **KILLED** | "first fails at `p=4`, where both values are one."  Left permutivity propagates the difference at an extreme that moves away from the centre. | `RESULTS-periodicity-bridge.md` |
| 40 | Bounded Crosstalk run for a period-independent contradiction from a periodic centre | 1 | **KILLED** | "zero candidates survived, no claim received objective verification, and the final proof attempt was rejected."  Ten rejects reduce to six recurring errors (XOR treated as monotone mass; a "closed" state still depending on `D(t,-2)`; forced rightward drift; telescoping OR as linear; infinite intersection from two infinite sets; the co-moving right boundary called aperiodic). | `RESULTS-periodicity-bridge.md`; `runs/rule30-periodicity-bridge/report.md` |
| 41 | Alternating-trace fiber: bounded-left-depth exclusion certificates for `(01)^inf` / `(10)^inf` | 1 | **OPEN** | Every `d <= 24` certified in both phases, and the survivor automaton is now closed form — `L_(T+1) = v XOR parity(o_1..o_T)`, a parity-checked deterministic map past the knee.  Stopped at the uniformity gap: "Claim(d) for every `d`.  Equivalently: no `rho` sequence keeps `L(rho)` eventually zero."  Certificate levels grow `k(d) ~ d`, so per-`d` certificates "can never reach uniformity by themselves".  The `{1,4}` wallpaper member shows infinite-left seeds can pass forever, so any proof must use left-finiteness. | `RESULTS-alt-trace-fiber.md`; `alt_trace_fiber_probe.py` |
| 42 | Overnight literature-novelty triage, ten techniques, one researcher agent each | none/infra | INFRA | Produced the verdict table that gated the overnight arms: "5 closed, 5 known-adjacent-with-stated-open-edge, 0 novel-open."  Rows 43-46 and 48-53 are its consequences. | `overnight/TRIAGE.md`; `runs/overnight/triage-rows.json` |
| 43 | ANF/Walsh analysis of the iterated centre-bit function `f_t` | none (see note) | **PROVED** | Theorem obtained: for every `t >= 3`, `deg f_t = 2t-1` with unique top monomial `M_t`, via an induction plus the C1 parity claim, itself proved by a self-similarity recursion and re-checked by a third independent implementation.  Also new integer sequence `M(t)`, not in OEIS.  Honest scope, quoted: "It implies NOTHING for P1 or P2... On P3 the degree theorem is not merely unproved-to-help; it is provably inert."  The Smolensky inference from it is explicitly REFUTED in the same document. | `overnight/PREREG-anf.md`; `overnight/RESULTS-anf.md`; `experiments/overnight-arms/anf/` |
| 44 | Exact classification of jointly (shift, Rule 30)-invariant Markov measures, memory `m <= 3` | 2 | STALLED | Decisive at `m = 1, 2` (saturated Groebner basis pins every transition probability to 1/2), but kill condition K2 fired at `m = 3`: the saturated basis "ran past 110 minutes without terminating, against 0.9 seconds for `m = 2`".  Bernoulli-level data does not separate Rule 30 from Rule 90, and the arm "moves P2 not at all by itself". | `overnight/PREREG-ergodic.md`; `overnight/RESULTS-ergodic.md` |
| 45 | Anashin 2-adic ergodicity along the time direction (comoving-frame 1-Lipschitz map) | 2 | **KILLED** | Three independent fatal reasons plus a fourth, stronger one: (1) Rule 90 has identical structure, so the object is non-separating; (2) Rule 30's comoving map is bijective but not a single `2^k`-cycle, failing at `k=1`, so the criterion does not apply; (3) the odometer counterexample shows maximal 2-adic ergodicity is compatible with a diagonal digit of density 0; (4) any bounded-index 1-Lipschitz encoding carrying the centre column would make it eventually periodic, i.e. would refute P1.  "Advances P1, P2, P3 by zero." | `overnight/RESULTS-anashin.md` |
| 46 | Ore-relation ladder `S(0) <= S(1) <= ...` between P1 and non-2-automaticity of A051023 | 1 | **OPEN** | REDUCED, not killed: `S(0) <=> P1` exactly, the conjunction of all `S(n)` `<=>` non-2-automaticity (Christol), each rung one-sidedly provable by one finite GF(2) rank computation, certificates independently reproduced, Rule 90 control caught at order 0.  Stopped at a named obligation: "LEMMA L.  If `a` is 2-automatic with `k` states, then `F` admits an Ore relation of order `<= poly(log k)` and height `<= poly(k)`" — only an exponential bound is proved. | `overnight/RESULTS-automaticity.md`; `experiments/overnight-arms/automaticity/ore_check.py` |
| 47 | Single-seed density arm: martingale, counting, and invariance routes to P2 | 2 | **KILLED** | Killed for the P2 target; the three original mechanisms were structurally invalid ("no probability space exists on a deterministic orbit").  Two proved byproducts survive and neither bounds the density: an explicit counting rate `N_1(T) >= floor(log2(T+4)) - 1` ("real, unconditional, and very weak"), and universal depth-4 diagonal pinning with density exactly 1/2, sharp at `k=5`.  Proved obstruction: the all-zeros and checkerboard fixed points make invariance-only arguments unable to force 1/2 — with the orbit-closure repair left explicitly OPEN. | `overnight/RESULTS-p2-single-seed.md` |
| 48 | Persistent homology / TDA on the `(x,t)` point cloud | 1,2 | **KILLED** | Triage verdict closed: time-filtered `H1` bars biject with enclosed white triangles (NKS-era bookkeeping), and "center-column periodicity constrains no spatial neighborhood"; the salvage lands in off-limits column-band territory. | `overnight/TRIAGE.md` row 1 |
| 49 | Quantum circuit mapping, entanglement entropy across the centre cut | 1,3 | **KILLED** | Closed: "Single-seed basis-state input through a permutation circuit has center-cut entropy identically 0"; nontrivial quantities are ensemble averages that cannot see one orbit, and the one reachable open item has no path to P1/P2/P3. | `overnight/TRIAGE.md` row 2 |
| 50 | Hydrodynamic / coarse-grained PDE limit for the 1s density | 2 | **KILLED** | Closed: "Coarse-grained density is a spatial-average object; P2 is a temporal statement about one measure-zero orbit," and Gutowitz local structure theory is the adjacent prior art whose refinements cannot in principle produce the single-column limit. | `overnight/TRIAGE.md` row 5 |
| 51 | Non-standard analysis / hyperfinite rows, transfer and overspill | 2 | **KILLED** | Closed: the machinery "is conservative: it yields P2 only after the standard lemma it needs (equidistribution of the specific orbit) is already available," and the schematic derivations "apply verbatim to Rule 90 where the conclusion fails." | `overnight/TRIAGE.md` row 6 |
| 52 | Homotopy type theory / loop-space framing of P1 | 1 | **KILLED** | Closed: "All types involved are hSets; the loop-space statement 0-truncates to the plain first-order eventual-periodicity sentence."  Adds nothing over set-level formalization. | `overnight/TRIAGE.md` row 7 |
| 53 | Latent-space geometry to exact non-additive conserved window functions | 1,2 | NOT RUN | Ranked third of the open triage rows and never pre-registered: "promoted if an above arm kills early.  Not pre-registered yet."  The ML part is a candidate generator only; exhaustive/SAT search over small windows is the content. | `overnight/TRIAGE.md` row 4 |
| 54 | Ladder tightening arm 1: add the right-wedge constraint `col_x(t)=0` for `x > t` | 1 | **KILLED** | The constraint was already imposed — `ax = abs(x)` in `ladder.step_window` covers positive `x`; measured 0 wedge violations on the escape family.  Disabling it grows the state space 1.38-1.51x, so it is not vacuous, but "Every verdict is NONEMPTY with or without it."  Corrects `RESULTS-ladder-rung0.md` section 4. | `p1_constrained_attack/p1_agent1_right_wedge.md` |
| 55 | Ladder tightening arm 2: the boundary pin `col_R(t)=1 => col_{R-1}(t) = NOT col_R(t+1)` | 1 | **KILLED** | A genuine sound Rule-30-specific constraint (prunes 39-58%, rejects the rung-0 escape family at letter 34, zero violations at `T=300` against Rule 90's every antecedent) that still flips no verdict: the slip relocates outward to the new boundary column.  Rung 1 then proved it cannot be the deciding lever — Corollary 2 gives `plain(R+1) ⊆ pin(R) ⊆ plain(R)`, so "the pin buys strictly less than one column of depth".  Cost: applying Rule 30's pin to Rule 90 destroys the control (repaired in rung 1 by using each rule's own extendability condition). | `p1_constrained_attack/p1_agent2_pincascade.md`; `P1_CONSTRAINED_ATTACK.md`; `RESULTS-ladder-rung1.md` §1-2 |
| 56 | Ladder tightening arm 3: `Diff` quantified over all `q <= Q` (bounded-universal conjunction) | 1 | **KILLED** | A real new mode, correctly reasoned and calibrated, measured dead: NONEMPTY at every `Q` to 14, witness cycle length tracking `~3.5 Q`.  Its own lemma closes it: `S(1..Q)` nonempty forces `col_{-1}` period `> Q`, while available cycle lengths grow as `N(Q) ~ 2^Q`, so "the constraint and the freedom grow together."  Trap recorded: above `Q >= N_base` an EMPTY "is an artifact, not a theorem". | `p1_constrained_attack/p1_agent3_universal_q.md`; `RESULTS-ladder-rung0.md` §6 |
| 57 | Hyperbolic lightcone geodesic embedding of the spacetime diagram | 1 | **KILLED** | Column-blind: overwriting column 0 with `0101...` moves the statistic by 8.6e-4 to 7.5e-7 as `W` grows, against a positive control that moves 96%.  Also measures the wrong object — the full configuration never repeats for any ECA with a growing lightcone, Rule 90 included, and the embedding is not canonical. | `p_geometric_attack/GEOMETRIC-TRIAGE.md` |
| 58 | Curvature of a multilinear (Riemannian) relaxation of Rule 30 | 1,2 | **KILLED** | Column-blind: `|A-B|` falls to machine epsilon by `W=128` and to 0 at `W=256`.  The stated form is also a category error (max-plus semirings have no Riemannian metric), and the Boolean orbit is a measure-zero vertex set of the relaxed manifold. | `p_geometric_attack/GEOMETRIC-TRIAGE.md` |
| 59 | Spectral dimension of a Dirac operator on the shift algebra | 1 | **KILLED** | Column-blind, cleanest instance: 8.31e-3, 4.11e-3, 2.02e-3, 1.01e-3 across doublings, "`O(1/W)` to three digits."  Spectral dimension is a property of the algebra, and Rule 90 induces the same algebra while having the opposite P1 answer. | `p_geometric_attack/GEOMETRIC-TRIAGE.md`; `discriminator.py` |
| 60 | OTOC / spectral form factor, random-matrix statistics of the evolution operator | 1 | **KILLED** | Premise false: Rule 30 is not invertible — measured non-bijective at every `N` from 3 to 14, up to 3 preimages — so no unitary evolution operator and no RMT ensemble exists.  The classical OTOC is damage spreading, already published (NKS p.949, 0.2428 cells/step). | `p_fringe_attack/FRINGE_ATTACK_ASSESSMENT.md` |
| 61 | 2-adic / Mahler expansion with unique ergodicity under Haar measure | 2 | **KILLED** | The hypothesis is false in one line: `delta_0` and uniform Bernoulli are both invariant, "so the system is not uniquely ergodic".  Also not 1-Lipschitz in that frame, so Klimov-Shamir T-function machinery does not apply.  What remains is route R8 in different clothing. | `p_fringe_attack/FRINGE_ATTACK_ASSESSMENT.md` |
| 62 | Braid-group word length of defect world lines | 1 | **KILLED** | "no braid word exists": Rule 30 defects merge and annihilate (forced by non-invertibility), and a world-line diagram with merging strands has no Artin generator word.  Even granting a defect-count proxy, the Rule 90 filter closes it. | `p_fringe_attack/FRINGE_ATTACK_ASSESSMENT.md` |
| 63 | Algebraic immunity of `f_t` as an AC0 lower bound | 3 | **KILLED** | "The AC0 claim is false."  `AND_n` has maximal F2-degree, algebraic immunity 1, and a one-gate depth-2 AC0 circuit.  Real measurement survives as a byproduct: the first exact AI values `3,3,4,5,6,6` for `t=3..8`, strictly below the `ceil(n/2)` bound, so `f_t` is not AI-optimal.  `t=9,10` out of reach (`t=8` took 485 s).  Premise not re-verified here: the document accepts `deg f_t = 2t-1` "as instructed and never re-verified", citing row 43 where it is proved. | `p_fringe_attack/FRINGE_ATTACK_ASSESSMENT.md`; `algebraic_immunity.py` |
| 64 | AC0 / Smolensky size bound from the exact ANF degree of `f_t` | 3 | **KILLED** | Refuted analytically by the `AND_n` counterexample; Razborov-Smolensky needs inapproximability by low-degree polynomials, not high exact degree.  Second objection: `f_t` has `n = 2t+1` variables, so a `2^Omega(t)` bound is the trivial regime.  **PREMISE NOT RE-VERIFIED HERE:** the document accepts `deg f_t = 2t-1` "as instructed and **not** re-verified", spending zero compute on it, and cites `overnight/RESULTS-anf.md`, where it is proved unconditionally (row 43).  The premise is sound; the caveat is only that this assessment ran no independent check of it. | `p3_circuit_attack/P3_ASSESSMENT.md` |
| 65 | Straight-line-program length along the single-seed line | 3 | **KILLED** | Category error, no compute can fix it: "Evaluated 'along the single-seed line' the input is a single fixed point, the function is a constant, and every one of these measures is 0.  There is no theorem to prove there."  Same premise caveat as row 64. | `p3_circuit_attack/P3_ASSESSMENT.md` |
| 66 | Sensitivity `s(f_t) >= t` along the single-seed evaluation path | 3 | **KILLED** | Numerically false: measured `s(f_t)` at the lone seed is 4 at `t=6`, 7 at `t=9`, 8 at `t=11`, and sits below the random-input maximum throughout.  Same category error as row 65 and the same premise caveat. | `p3_circuit_attack/P3_ASSESSMENT.md` |
| 67 | Ground-truth centre-column generator and OEIS gate | none/infra | INFRA | `center_column.py` bit-parallel, first 30 terms matched against OEIS A051023 fetched from the API, orientation shown not to be a degree of freedom.  Every arm's pipeline is gated against it. | `PREREGISTRATION.md`; `center_column.py` |
| 68 | Modal compute charter and fail-closed admission guard | none/infra | INFRA | $200 lifetime ceiling, staged release, content-addressed work-unit ledger with a unique constraint, explicit exclusion list.  The gate was never entered: every RESULTS file records Modal $0. | `MODAL-COMPUTE-CHARTER.md`; `modal_guard.py` |
| 69 | Crosstalk elimination runbook and structural-exclusion ledger | none/infra | INFRA | Turns each failed mechanism into a typed exclusion that later candidates must differ from.  "Negative results narrow mechanism families, not the set of all possible algorithms." | `CROSSTALK-RUNBOOK.md` |
| 70 | Overnight autonomous run: prompt, hard fences, compliance statement | none/infra | INFRA | Fenced session that produced rows 42-47; compliance verified by mtime rather than `git status` (the subtree is untracked), with one disclosed exception, a `__pycache__` byte-code file from a read-only import. | `OVERNIGHT-PROMPT.md`; `overnight/FENCE-COMPLIANCE.md` |
| 71 | Settled-knowledge digest for downstream sessions | none/infra | INFRA | Read-only survey listing what is proved, what is dead, what is off-limits, and the pinned notation.  "Cite the source doc, not this file." | `overnight/CONTEXT-DIGEST.md` |
| 72 | Zero-tail note: manuscript, figures, Lean and SMT certificates, venue path | none/infra | INFRA | Packaging for row 25, plus an independent hostile proof audit that found no critical or major issue.  **Rests on an unverified external premise:** Jen 1986 (*J. Stat. Phys.* 43, 219-242) is unread, and its abstract clause (ii) is load-bearing in both directions — if the characterization includes Rule 30 it contradicts the theorem, if it excludes Rule 30 the theorem is not novel.  "REQUIRED before circulation: read the original." | `paper/PUBLICATION-NOTES.md`; `paper/README.md`; `Rule30ZeroTail.lean`; `zero_tail_smt_certificate.py` |
| 76 | S-adic decomposition + Morse-Hedlund factor complexity `p(n) > n` | 1 | **KILLED** | Vacuous by Morse-Hedlund's own logical form: eventually periodic iff `p(n) <= n` for *some* `n`, so confirming `p(n) > n` up to any finite `n_max` excludes only periods below roughly `n_max` — obstruction H.  Measured `p(n) > n` for all `n <= 64` on a 200,000-bit prefix, prefix-saturated (every window near-distinct) from `n ~ 32` on, well short of the prize announcement's own `10^9`-bit exclusion.  Proposed as row 76 in `novel_frameworks/TRIAGE-novel-frameworks.md` (A4) and left unmerged; independently re-derived from scratch here with a from-scratch naive simulator and exact agreement (`p(8)=256`, `p(16)=62377`), so the merge is now made on two independent implementations. | `novel_frameworks/TRIAGE-novel-frameworks.md` A4; `RESULTS-followup3-subword-complexity.md` |

73 rows (row 76 merged 2026-08-30 from `novel_frameworks/TRIAGE-novel-frameworks.md`; rows 73-75 of that proposal remain unmerged and out of scope here).

### 7.2 Code with no write-up

Probes present in the tree with no dedicated results document.  Each is either
a control, a harness, or an instrument for a row above; none is an unrecorded
attempt.

* `experiments/rule30/support_state_probe.py` (+ `test_support_state_probe.py`)
  — exact support-state compression for Rules 22 and 30, turning the Rule 22
  support recurrence into an executable control.  Exercised by `ARM7`'s
  reproduction block but never reported on.
* `experiments/rule30/make_band.py`, `sweep.sh`, `fit.py`,
  `challenge-*.json`, `hidden-*.json`, `report-*.json`,
  `wasm/`, `*.wasm` — the arm-3 tournament harness (row 12).
* `experiments/rule30/figures.py` — self-checking TikZ generator for row 72.
* `experiments/rule30/ladder/`, `p1_attack/*.log` — the R7 engine and its
  rung-0 drivers; results are rows 7, 54-56.
* `experiments/overnight-arms/common/rule30.py` — substrate self-test.
* `experiments/overnight-arms/common/ensemble_filter.py` — the Rule 90
  ensemble filter as executable code; its docstring is the sharpest statement
  of obstruction B below, but it has no results file of its own.
* `experiments/rule30/orbit-closure/`, `proof-complexity/` artifacts — data
  behind rows 8 and 9.
* `runs/*/artifacts/*.md` are content-addressed snapshots of documents already
  listed above and are not separate attempts.

Not "code with no write-up": `Rule30ZeroTail.lean`,
`zero_tail_smt_certificate.py` and `overnight-arms/anf/verify_c1_proof.py` are
the evidence artifacts for rows 25, 26 and 43.

### 7.3 Recurring obstructions

Six obstructions account for most of the table.  Each is stated as the source
document states it, then the rows it killed or stalled.

**A.  The `O(log t)` wall.**  Trace-anchored analysis reaches only
`~2.4 log2(t)` into a diagram whose interesting column is at distance
`Theta(t)`; the loss is one bit per step.  First recorded quantitatively in
`RESULTS-diagonal-periodicity.md` ("the periodic region reachable from the
right boundary at time `t` is `~2.4 log2(t)` diagonals wide"), then named as a
property of the problem in `PATH.md` 3.1 after it appeared in a third
representation.  The three independent representations are the right-cone
diagonals (row 34), the run-length bootstrap (row 3) and pin propagation
(row 2).  Two more have since been added, making **five**: the rung-1 tail
language (`~R^2.75` against a `4^R` encoding, `RESULTS-ladder-rung1.md`) and the
column-0 patch scan, which measures `H(p,w)` growing at `1.38 log2 T` with a
width reach of `0.45` per `log2 T` out to `T=10^6`, against a Rule 90 control
that grows *linearly* in `T` and is flat in `w`
(`RESULTS-patch-scan.md`).  The patch scan also quantifies the cost of the
empirical route: deciding rung 1 by depth alone needs `T ~ 2*10^13`, four orders
past the largest centre column ever computed.
Killed or stalled: rows **2** (R2, 1.14% of cells, zero at `x >= +1`),
**3** (R3), **4** (R4), **33** (flat support certificate), **34**, and it is
the reason `PATH.md` requires every new route to say why it beats `O(log t)`.
Explicitly *not* applicable to: row 1 (R1 is a counting and structure question,
not a propagation-depth one), row 7 (Buchi emptiness consumes the global
periodicity hypothesis via lasso structure), row 41 (certificate levels grow
`k(d) ~ d`, so trace side and cone side collide within one cone-return time).

**B.  The Rule 90 filter.**  Rule 90 is left permutive, additive, positively
expansive and mixing, and its lone-seed centre column *is* eventually periodic.
Any argument that would also apply to Rule 90 proves nothing.  First recorded
in `PATH.md` section 0, quoting Kopra arXiv:2202.13809; stated as executable
code in `experiments/overnight-arms/common/ensemble_filter.py`.
Killed outright: rows **5** (R5, the expansivity family entire), **6** (R6
fails it in spirit), **45** (anashin kill reason 1: Rule 90 has the identical
1-Lipschitz comoving structure), **51** (non-standard derivations "apply
verbatim to Rule 90"), **59** (Rule 90 induces the same shift algebra), and it
is why row 49's ensemble quantities are disqualified.
Killed as the *secondary* reason, the rows having already died on their own
premises: rows **60** and **62**, where the filter closes any "complexity
grows" argument because Rule 90's pattern has unbounded structural complexity
while its centre column is eventually periodic — "Even granting a defect-count
proxy, the Rule 90 filter above closes it."
Passed by construction, and this is the reason to prefer them: rows **1**,
**7**, **25** (the Rule 90 analogue is explicitly false), **26**, **55**.
Used as a live control that could have failed and did not: rows **8**, **9**,
**17**, **20**, **28**, **32**, **33**, **43**, **44**, **46**.
Cost recorded: row **55** — Rule 30's pin rejects the true Rule 90 word, so a
pin-augmented ladder has no soundness control; repaired in
`RESULTS-ladder-rung1.md` by using each rule's own extendability condition.

**C.  Single-column blindness.**  P1 and P2 are statements about one column,
which is a density-zero subset; a functional of the 2D diagram that is
continuous under density-zero modification cannot decide them, however
strongly it discriminates between rules.  Operationally: overwrite column 0
with a periodic word and see whether the quantity moves by more than `O(1/W)`.
First recorded as R6 obstruction (i) in `PATH.md` R6, generalized and measured
in `p_geometric_attack/GEOMETRIC-TRIAGE.md`, then promoted to `PATH.md`
section 0.1 as the second standing filter.
Killed: rows **6** (R6), **48** (periodicity of one column constrains no
spatial neighborhood), **49**, **50**, **57**, **58**, **59**.  The measured
trap is that all three geometric statistics separate Rule 30 from Rule 90 by
26-98% while being column-blind: "Rule-sensitivity is not evidence of
P1-relevance."

**D.  The missing composition law.**  Every proposed P3 shortcut supplies a
state and a doubling story but names the exact seam or composition identity
instead of deriving it; where it is derived, it is false at small `n`.  First
recorded in `RESULTS-crosstalk-elimination-run.md` ("Phrases such as 'under an
exact composition law (derivable...)' and 'uses an appropriate shift
correction' name the missing lemma instead of deriving it"), and codified as
the five-point acceptance contract in `ARM7-dyadic-spacetime-grammar.md`.
Killed: rows **19** (boundary vectors still `Theta(n)` bits; helpers named,
not defined), **21** (`first_mismatch=5`), **22**, **23** (three contracts,
each conditional on precisely the missing lemma), **24** (`first mismatch at
n=2`).  Row **18** stalls on the same gate from the measurement side: the tile
perimeter determines the interior but carries `Theta(scale)` bits.

**E.  The measure-zero single-orbit gap.**  Rule 30 is surjective and ergodic
for uniform Bernoulli, so almost every initial configuration already has
centre density 1/2; P2 survives only because the lone seed is one measure-zero
point, and no ensemble-level theorem sees it.  First recorded in
`PREREGISTRATION.md` Arm 2.
Killed or stalled: rows **11** (Arm 2 itself, declined for this reason),
**44** ("even full measure rigidity would not settle the limiting density...
the bridge is an equidistribution/generic-point statement that no result here
touches"), **45** (kill reason 3, the odometer counterexample), **47**
(invariance alone admits densities 0 and 1), **58**, **61**.  Row **8** is the
one route shaped against it — orbit-closure classification converts
almost-everywhere statements into everywhere statements — and it is still
open.  Row **47** leaves the orbit-closure repair explicitly unresolved.

**F.  The free boundary of a fixed-depth strip.**  Any fixed-depth column
window leaves its outermost column unconstrained, and the phase slip that
makes the ladder nonempty relocates there rather than dying.  First recorded
as a conjecture in `P1_CONSTRAINED_ATTACK.md` ("any fixed-depth strip leaves
its outermost column under-constrained, and the slip migrates there"), then
proved in `RESULTS-ladder-rung1.md` Corollary 2/3: `plain(R+1) ⊆ pin(R) ⊆
plain(R)`, so "the pin constrains column `R` while leaving `R+1` free,
recreating the very gap it closes."
Stalled or killed: rows **7** (verdict uniform in `R` and `k` across a 5,500x
range of raw sizes), **54**, **55**, **56**.  The measured form is that
constraint and freedom grow together in every direction tried — depth, the
pin, and `Q` — while the accepting tail system carries only `~R^2.75`
bisimulation classes against a `4^R` encoding.

**G.  Arbitrary-input measures versus a single fixed point.**  P3 fixes the
input to the lone seed and varies only `n`; circuit size, decision-tree depth,
sensitivity, block sensitivity, certificate complexity and algebraic immunity
are measures of a function of *variable* inputs, and on one fixed point they
are identically zero.  First recorded in `p3_circuit_attack/P3_ASSESSMENT.md`
("Arms 2 and 3 as written are asking for the complexity of a constant"), and
restated independently in `overnight/RESULTS-anf.md` Addendum 2 ("P3's input
is the INDEX `t`... Lower bounds on the cost of computing `f_t` over its whole
domain therefore carry no implication for the cost of that one evaluation").
Killed: rows **63**, **64**, **65**, **66**; it also bounds the scope of rows
**20** (`F_h` "can be a stronger state than necessary") and **43** (the degree
theorem is "provably inert" for P3).  Row **9** is the framing built to evade
it: derivation length keeps the input fixed and still has a nontrivial
lower-bound question.

**H.  Finite data cannot establish an infinite statement.**  Every bounded
exclusion, certificate ladder or residual count is a lower bound on a
complexity function and can never be more.  Stated as a boundary in
`ARM6-binary-kernel.md` ("Finite data cannot establish that the 2-kernel or
its rank is unbounded"), and given an exchange rate in
`overnight/RESULTS-automaticity.md` Theorem O: any sequence agreeing with `a`
on `[0,N)` and zero thereafter is eventually periodic, so "`N` terms buy a
kernel lower bound of about `N/8` and nothing more, ever."
Bounds the reading of rows **17**, **32** (bounded UNSAT is not
nonperiodicity), **33**, **41** (per-`d` certificates "can never reach
uniformity by themselves"), **43** (exact for `t <= 22`, "establishes nothing
for `t > 13` on its own"), **46**.  It is also the reason row **10** was never
run and why the prize announcement's own `10^9`-bit check cannot exclude "a
trillion-step transient".

## 8. External attempt register: what other people have tried

Compiled 2026-08-30 from three independent sweeps (academic literature;
code/data/community; cryptanalysis and formal methods).  Structurally parallel
to section 7 so the two registers can be read against each other.  Status of
all three prizes as of this date: **OPEN**.

Read this section for one purpose: to avoid re-running an attempt that has
already been made, and to see which of section 7.3's obstructions are
properties of the problem rather than artifacts of this repo's approach.

### 8.0 The headline, stated plainly

**The field is nearly empty, and the only live technique is uncited.**
Kopra's rapid-left-expansivity paper (TCS 946 (2023) 113668) is the sole
modern method aimed at P1.  It has **zero citations** in both Semantic Scholar
(`arXiv:2202.13809`) and OpenAlex (`10.1016/j.tcs.2022.12.018`); two
independent indexes agree.  Nobody has built on it since 2023.

Counting honestly, genuine academic attempts on P1/P2/P3 number roughly
**six people across forty years**: Jen, Rowland, Kopra, Taati, and partially
Chan-Lopez & Martin-Ruiz (random-IC side only).  The surrounding Rule 30
literature runs to hundreds of papers, but ~95% of it uses Rule 30 as a PRNG
or cipher primitive and targets none of the three problems.  Do not mistake
citation volume for activity on the prizes.

Outside academia the picture is thinner still: **four named individual
attempts** (Nersissian, Brunnbauer, Ikram, marginally Gogu), **one repository
with real empirical output** that explicitly disclaims proving anything, and
**one dataset that dominates all others** (Wen's 10^9 bits, no code published).

### 8.1 P1 — non-periodicity of the center column

| Who | What was tried | Outcome |
|---|---|---|
| Jen 1986, *JSP* 43:219-242 | Conditions on nearest-neighbour rules for finite ICs; source of "no two columns can both become periodic" | **PROVED**; full text UNOBTAINED, see 8.6 |
| Jen 1990, *Physica D* 45:3-18, Prop. 3 | At most one eventually periodic temporal sequence, for rules injective in the `(i+1)`-th component with `{100} -> 1`; covers 30, 86, 90, 150, 154, 210 | **PROVED**; leaves exactly one column open, and that column is P1 |
| Rowland 2006, *Complex Systems* 16:239-258 | Right diagonals purely periodic with period `2^a` (Lemma 2); left diagonals eventually periodic via Jen 1986 Thm 4 | **PROVED**, diagonals not the column |
| Kopra 2019 (TUCS Diss. 249) | Width-2 restatement; Problem 3.1.13 asks whether `W30` is regular (trace subshift sofic) | **PROVED** (width 2); soficness **OPEN** |
| Kopra 2023, TCS 946 113668 | Rapid left expansivity; Thm 3.5 width `>= 2` never eventually periodic; Cor. 3.7 recovers Jen; Problem 3.10 restates P1, "The answer 'no' is expected" | **PROVED** width `>= 2`; **NEGATIVE** for width 1 — Rule 90 is in the same class with a periodic column, so no class-level argument can settle P1.  This is the external form of section 0's filter |
| Kopra 2021, TCS 851 | Prop. 3.8: the only width-one finite-configuration aperiodicity theorem anywhere, for fractional multiplication automata `Pi_{p/q}`.  Works via right-determinism of digits | **PROVED** for a different automaton; explains mechanically why P1 resists — Rule 30 lacks right-determinism |
| Das 2022, arXiv:2207.13237 | "Analytical solution to ... Problem 1" | **CLAIMED-UNACCEPTED.**  v1 only since July 2022, never revised, no journal version, no peer review, no engagement.  Also **never refuted** — ignored, not rebutted |
| Chan-Lopez & Martin-Ruiz 2026, arXiv:2604.00165 | Rule 22 as symmetric algebraic reference; support-set closed form; symmetry-breaking deviation fitted to `m^1.11`; identity `c(t) = [t in S_{t+1}]` | **MEASURED/CONJECTURED**, unrefereed, explicitly disclaims solving the prizes |
| Nersissian 2026 (Wolfram Community 3647733) | "Exact binomial-Lucas lifting" to integer coefficients, Stirling transfer, support-set algebra; claims `O(log n)` cell query via compressed support sets | **CLAIMED reformulation**, not a prize claim by its own text; unrefereed, not on arXiv.  Publicly states he submitted to the prize ~2026-01-17 and received no confirmation |
| Brunnbauer 2019 (brunni.de/findings30) | Empirical diagonal-period search; claims necessary/sufficient condition for period doubling | **MEASURED**; self-describes as amateur, and diagonal periodicity was already proved by Rowland 2006 |
| Ikram 2026 (OSF eph94/kybmz/z7wnp/k8t2e) | Finite-cone / trace-language compatibility reduction for P1, depth-tail reduction for P2, query-model reduction for P3 | **Reformulations, not resolutions**, self-described.  "bloxberg research certificates" timestamp a file hash; they are **not** peer review |

### 8.2 P2 — equidistribution

| Who | What was tried | Outcome |
|---|---|---|
| Wolfram 1985/1986 (PRL 55:449; *Adv. Appl. Math.* 7:123-169; CRYPTO'85) | Origin of the conjecture; statistical batteries on the temporal sequence | **CONJECTURED + MEASURED**; RSG 1986 full text UNOBTAINED, see 8.6 |
| Taati 2015, arXiv:1505.06464 §2.4 | Rule 30 case study: left-permutive not bi-permutative, `<= 4` preimages, balance property holds | **PROVED** (invariance) and states verbatim that **randomization for Rule 30 is open** |
| Host-Maass-Martinez 2003; Pivato 2005; Sablik 2007 | Measure rigidity for permutative CA | **NEGATIVE-SCOPE**: all require algebraic or bipermutative rules.  Rule 30 is outside every hypothesis.  Matches this repo's R8 finding |
| Rowland & Yassawi 2020, *CJM* 72:1691 | Invariant measures from `k`-automatic spacetime diagrams incl. single-seed | **NEGATIVE-SCOPE**: linear/algebraic only |
| Nesme 2022, arXiv:2207.13062 | Relaxes Rowland-Yassawi to commutative monoids and `k`-automatic ICs.  **The only paper citing Rowland-Yassawi** | **PROVED but NEGATIVE-SCOPE**: Rule 30 is not a monoid morphism.  This is the direct answer to "has anyone applied automaticity to A051023" — no |
| Chan-Lopez & Martin-Ruiz 2026, Thm 3 | For i.i.d. Bernoulli(1/2) ICs, `P(eta_t(0)=1) = 1/2` for every left-permutive ECA | **PROVED but does not touch P2**; authors state that reaching the single-seed case "requires quantifying the mixing rate".  This is the measure-zero gap in external form |
| Guan & Wang 2011, *Complex Systems* 20(1):31 | Bernoulli shifts and topological mixing on certain closed invariant subsystems of rules 30/41/110 | **PROVED**, scope-limited to subsystems; silent on the lone-seed orbit |
| W. Li 1987, *Complex Systems* 1:107 | Power spectra of CA attractors via regular languages | **PROVED/MEASURED** but about *spatial attractor* spectra, NOT the temporal column.  On the prize bibliography and easy to misread |
| Chua et al. 2002-2010, *IJBC* (14 parts) | Bernoulli `sigma-tau` shift classification, 1/f spectra, quasi-ergodicity across ECA space | **PROVED/MEASURED**; never addresses the single-seed center column |
| Wolfram 2019 (prize page) | "All sorts of statistical randomness tests on the center column ... never found any significant deviation" | **MEASURED**, single-seed, but **suites unnamed and no report published**.  The only on-target testing claim in existence |
| Wolfram 2019 bit counts | 500,025,038 black vs 499,974,962 white at `10^9` | **MEASURED.**  Excess 25,038 against sd `sqrt(10^9 * 0.25) ~ 15,811` is **~1.58 sigma** — consistent with balance, proves nothing |
| Tomassini-Perrenoud 2001; Formenti et al. 2014; Leporati-Mariot 2013/14; Manzoni-Mariot 2018 | DIEHARD / ENT / NIST STS on CA PRNGs | **MEASURED but OFF-TARGET**: all random-key rings, and several test *different rules* (bipermutive `d=5,7`, asynchronous, hybrid).  None tests the lone-seed column |

**Ceiling on all statistical testing:** every suite examines a finite prefix, so
no pass or failure can bear on a *limiting* frequency.  A failure would be
strong evidence against P2; a pass is weak evidence for it.  Note also why no
TestU01 BigCrush result exists: BigCrush consumes ~`10^11` bits and the largest
published center-column dataset is `10^9`.

### 8.3 P3 — computational effort

| Who | What was tried | Outcome |
|---|---|---|
| Natal & Al-saadi 2024/25, arXiv:2409.07065 | Rule self-composition, whole evolution in `O(n^2/log n)` time, tested on Rule 30 | **PROVED upper bound**, whole triangle not a single cell; log factor does not reach sublinear per cell.  Current frontier |
| Moore 1997, *Physica D* 103:100-132 | "Quasilinear" CA predictable in serial `t`, `t log t`, `t log^2 t`, `t^a` (`a<2`) | **PROVED.**  The one place CA shortcuts genuinely exist — and **Rule 30 is not among them** (verified: "Rule 30" does not appear in the paper).  The clearest statement of where known shortcut technology stops |
| Meier & Staffelbach 1991, EUROCRYPT | Known-plaintext attack exploiting left-permutivity / failed 1st-order correlation immunity | **PROVED attack**, but random-key ring, and *inverse* direction.  No center-column shortcut |
| Koc & Apohan 1997, *IEE Proc.* 144(5):279 | CA inversion by backtracking via best affine approximation | **PROVED attack**, preimage direction |
| Karttunen 2019 (OEIS A051023) | "Sideways evaluation": `a(n) = (A328100(n) OR A328101(n)) XOR A328101(n+1)` | **CLAIMED/unrefereed**, OEIS-internal, no proof published; constant-factor at best |
| Neary & Woods 2006; Greenlaw-Hoover-Ruzzo 1995 | Rule 110 prediction is P-complete; CA prediction as canonical P-complete problem | **PROVED but wrong quantifier**: quantifies over arbitrary length-`n` ICs, and P-completeness is a parallelism statement, not a sequential-work lower bound |
| Applebaum-Ishai-Kushilevitz 2010, ICS | OWFs/PRGs computable by CA under standard assumptions | **PROVED** — the nearest thing to a CA hardness theorem, but for *designed* CA on *random* inputs.  Nobody has stated a hardness assumption whose object is Rule 30's center column |
| Vuckovac 2021, *Complex Systems* 30(3):375 | CA irreducibility + sensitivity as basis for puzzles / proof-of-work | **CLAIMED.**  Closest anyone comes to treating Rule 30 as a sequential hardness primitive, and it **assumes** irreducibility rather than proving it |
| Sur & RoyChowdhury 2023 | VDF on non-linear hybrid CA | **CLAIMED, unverified** (abstract unretrievable).  Fails P3 three ways even at face value: bounds depth not work, random input, designed hybrid rule |
| Cavagnetto 2011; Kapytka 2026 arXiv:2604.01041 | Proof complexity of CA | **PROVED but NEGATIVE-SCOPE**: both target injectivity/inversion, never prediction.  Matches this repo's R9 finding |
| — | Fine-grained (SETH/OV/3SUM) hardness for Rule 30 | **NONE FOUND.**  Fine-grained hardness needs an input family; P3 fixes the input |
| — | Circuit lower bounds for the center column | **STRUCTURALLY DEAD.**  A fixed sequence has `O(1)` non-uniform circuit complexity per bit by hardwiring.  Independently reached by this repo's own P3 assessment |

### 8.4 Method attempts that touch P1 but were never pointed at it

| Who | What exists | Why it did not reach the column |
|---|---|---|
| Sutner 2009; Gershenson 2010 (CMU-CS-10-123); Finkel 2011 | CA phase space is omega-automatic; FO theories decidable via two-way Buchi automata; CAVE model-checker run on ECA including Rule 30 | Properties of configurations periodic under `F`, **never a designated orbit's column**.  No published encoding of P1 as omega-automaton emptiness, and **no per-period exclusion theorem for the Rule 30 center column exists — not even for `p=2`**.  That is precisely this repo's R7 |
| Bagnoli, Dridi & Fates 2025, arXiv:2504.03691 | Regional controllability of all 88 minimal ECA as SAT, with an **explicit Rule 30 instance** (IC `010001`, target `101010`, `T=7`); Rule 30 is "peripherally linear", reachability ratio 1.00 | Boundary control is easy *because of* left-permutivity, which is orthogonal to the interior column.  Same lesson as Meier-Staffelbach |
| D'Antonio & Delzanno 2004 | zChaff on forward/inverse CA reachability | Bounded-horizon BMC on finite lattices; a periodicity question over unbounded time is not a BMC instance |
| Amoroso & Patt 1972; Kari 1994 | Injectivity/surjectivity decision procedures; undecidability of reversibility | **Category correction to a common error:** in 1D both are *decidable*; Kari's undecidability is **2D only** and is frequently miscited as applying to ECA.  "CA reversibility SAT" is trivial for Rule 30 (non-injective, `<= 4` preimages) and bears on nothing |
| Martin 2008, *JCA* 3(2):145 | Exhaustive Walsh analysis of all ECA | **No ECA rule is simultaneously nonlinear and first-order correlation-immune.**  Kills the "fix Rule 30 by picking another ECA" program |
| Boyle-Lind 1997; Cyr-Franks-Kra 2019 | Expansive subdynamics; light-cone edges as nonexpansive subspaces | Purely topological; no invariant-measure classification, no column statement |
| Silvasi & Tomasek 2020, *SCP* 195:102471 | Lean formalization of bounded grids and computable CA | Infrastructure only, **no theorem about any specific rule** |
| — | Jen 1990 Prop. 3 or Kopra Thm 3.5 in Lean/Coq/Isabelle/Mizar | **NONE.**  AFP topic index, Mathlib, Coq and Mizar all checked 2026-08-30.  The width-2 aperiodicity theorem has never been mechanized |
| Zenil 2010/2018; Zenil et al. 2015 | Compression-based and BDM classification of CA | Aggregate complexity per rule, summed over blocks.  **No spatially resolved `C(x,t)` map of Rule 30 exists.**  Matches R6 |

### 8.5 Code, data and community

**No public high-performance center-column generator exists.**  No SIMD, GPU,
FPGA or distributed implementation was found; a GitHub sweep for ECA repos
mentioning SIMD/GPU/AVX returned only toy simulators.  The strongest
bit-parallel description in existence is Wolfram's own prose in the prize post
(word-packed `Xor`/`Or`, "less than 0.4 seconds to compute 100,000 elements").
**P3's constant-factor frontier is not being pushed publicly by anyone.**
*Update 2026-08-30:* this repo now has one — a validated WGPU/WGSL generator at
`experiments/rule30/rule30_gpu/`, 46x the CPU baseline at depth `10^6`, gated
against an in-binary CPU reference (`RESULTS-gpu-generator.md`).  It is a
constant factor and touches no prize problem; its value is as measurement
infrastructure and as the missing public artifact.  It also makes 8.5's
never-performed cross-check cheap: diff an independent generator against the
WDR datasets and `b051023.txt`.

*Update 2026-08-30, later: the never-performed cross-check was performed, and
it immediately paid for itself.*  `crosscheck_wdr.py` re-derives the WDR
container's payload offset and bit order on every run (rather than hardcoding
them, which would let the assumption manufacture the agreement) and diffs it
against the OEIS b-file and against this repo's generators.  Four independent
implementations — WDR, `b051023.txt`, a gmpy2 bit-parallel generator, and the
repo's naive reference — agree bit-for-bit.  **The H100 band generator did
not.**  It was dropping 1s at 5.05e-4 (block-tile edge) and 1.1e-5 (warp-tile
edge) from a lost-update race on a non-atomic `|=` issued by two blocks that
both claimed the same recorded cell; a 3e9-step run was stopped 22 minutes in,
and every gate in its launch path was a 64- or 256-bit prefix while the first
wrong bit was at 4,631.  **A prefix gate cannot validate a generator.**  Fixed,
and now verified by full-output equality on all nine recorded columns against
an independent generator, by cross-run bit-identity, and against WDR over
~2,000,000 bits: `experiments/overnight-arms/frontier_attack/a20_deep_simulation/`
(`KERNEL-V6-DEFECT.md`, `verify_band.py`).  Measured throughput of the corrected
kernel is **1.06e14 cell-updates/s** on one H100.  The correctness fix costs
nothing (1.00x).  A separate 3.97x was recovered along the way: the recording
state had been held in three `MAX_REC` lookup arrays indexed at runtime, which
cannot live in registers and dragged the kernel's hot register array into local
memory for every thread in the grid; because the recorded cells are consecutive,
the owned columns are a contiguous range and the table is unnecessary.

**Charter flag, unresolved.**  `MODAL-COMPUTE-CHARTER.md` excludes "regenerating
published center-column prefixes" and that exclusion is **not waived**.  The
validation runs above do regenerate published prefixes, though as a correctness
oracle rather than as a scientific output.  Separately and larger: no ledger
file exists in the repo, so this GPU arm never passed `modal_guard.py`
admission, and the charter's admission invariants specify **no GPU**, the strict
path being short CPU-only network-disabled Sandboxes.  The arm sits outside the
charter's strict path entirely.  The 3e9 run has **not** been relaunched.

The prohibition is not an inference from the prose; it is executable.
`experiments/rule30/modal_guard.py:226` reads

```python
if execution.get("gpu") is not False:
    raise GuardError("GPU work is prohibited until a separate measured justification exists")
```

so every H100 job in this arm would have been refused admission had the guard
been consulted.  It was not: the guard is never imported by any `modal_*.py`
here, and its lifetime SQLite ledger was never created, so the staged release
ceilings (`$5` calibration, `$20` pilot, ...) were never opened and no
work-unit hash was ever reserved.  Spend is therefore unmetered rather than
over-budget.  Measured from `modal app list`, the 19 apps still in the listing
window total **1,723 s of container wall time, `$1.89` at the `$3.95/hr` H100
rate**; the earlier calibrate/sweep-v3-v5/deep invocations have aged out of
that listing and are not included, so the arm's true cost is somewhat above
`$1.89` and far below the `$200` lifetime ceiling.  The exposure is procedural,
not financial.

**Resolved 2026-08-31, by amendment.**  The author's decision was to amend the
GPU clause rather than leave the arm outside the charter or retro-manifest it
under a prohibition still standing.  The guard's own error text said GPU work was
barred "until a separate measured justification exists", and one now does, so the
clause became a gate: `execution.gpu` is a device name rather than a flag, and is
admitted only with an `execution.gpu_measured_justification` naming the device,
its measured throughput, what its output was validated against, and evidence
paths that resolve in-repo — priced through a new `rate_snapshot.gpu_second_usd`
that is charged for the full timeout on every work unit.  See
`MODAL-COMPUTE-CHARTER.md`, "GPU measured justification".  The lifetime ledger
now exists and books the arm at `$1.89` as `admitted-in-arrears` via a
`backfill` path that deliberately does **not** synthesise a passing manifest:
`a20` used `@app.function` rather than `modal-sandbox` and took no same-day rate
snapshot, so a clean admission record would have been a false one.

Three limits survive the amendment and still block a 3e9 run, none of them
waived: the explicit exclusion on regenerating published center-column prefixes
(the validation regenerates them as a correctness oracle, which is why it is
evidence rather than output); the `3600 s` timeout cap, which makes a `~6 h` run
at least six separately-hashed resumable work units rather than one; and the
`modal-sandbox` backend requirement, which the `a20` scripts do not meet.
Porting them is a prerequisite, not a formality.

**Largest computations.**  `10^9` bits by **Xiangdong Wen**, Wolfram Data
Repository, 2019-09-23 (125 MB packed); **method and hardware unpublished, no
code**.  Largest independent effort: OEIS b-file `b051023.txt`, **100,000
terms** by Antti Karttunen (PARI via A269160), extending Reinhard Zumkeller's
first 10,000 — five orders of magnitude behind.  Nobody outside Wolfram
Research has published a computation within `10^5` of the state of the art.

**Periodicity search: no published certificate anywhere.**  Nothing on GitHub,
Zenodo, OSF or HAL.  The strongest exclusion in existence is *inferred, not
documented*: Wen's `10^9` bits rule out any transient-plus-period `<= 10^9` by
direct inspection.  The only published *searches* are `Patto1155/rule30-foundry`'s
statistical screen to `p = 10^6` (a z-score non-detection, weaker than
inspecting the billion-bit data) and an 11 KB SAT-sweep driver with **no
output, whose repository had a total lifespan of 14 minutes**.

**Repositories.**  `Patto1155/rule30-foundry` is the only one with genuine
sweep output and honest framing (states "empirical results here are not the end
goal", claims no proof); its P1 result is statistical non-detection to `p=10^6`
and is dominated by the billion-bit dataset.  `elijasgogu/rule30-structure`
(Zenodo DOI 10.5281/zenodo.18902879) has real artifacts and explicitly states
it does not resolve the prizes.  `qizwiz/rule30-ski-research` advertises a
`prize3/` "lower-bound program" in **Lean**; the Lean was read and it is a
complete, `sorry`-free **SKI-combinator** inter-basin theorem with nothing
about Rule 30 — **claim not substantiated**.  A large share of the 2025-26
GitHub "rule30" cohort reads as LLM-generated and was bucketed rather than
enumerated, so that a long table would not imply many serious attempts exist.

**Wolfram Summer School / Summer Research Program: an actual negative.**
WSS20-WSS25 tagged posts include many CA projects (3D lattices, topological
surfaces, non-adjacent parents, rule-space geometry) but **none on the center
column or any prize problem**.  This vein is empty, not merely unsearched.
Wolfram Community contains **four named attempts total**, not dozens.

**Independent cross-checks of A051023.**  The historically meaningful one:
**Daniel B. Cristofani, 2004-01-07**, whose independent implementation
**corrected the published sequence from its 64th term** (OEIS `%E` line).
Independent recomputation has caught a real error before.  Zumkeller (Haskell),
Karttunen (PARI) and the Mathematica one-liner agree across three languages.
**Open, cheap, and never done: diff the Wolfram Data Repository million/billion
bit datasets against the OEIS b-file.**

### 8.6 Corrections, cautions, and unobtained sources

**A fabricated citation is circulating on this exact topic.**  A web search
summary asserted `P. Grassberger, "Hidden Periodicities in Rule 30 Dynamics",
Comm. Math. Phys. (2024)`.  OpenAlex `title.search` returns **count 0**.  It
does not exist.  The real Grassberger paper of that vintage is "Long-range
effects in an elementary cellular automaton", *JSP* 45:27-39 (1986), and it is
about **rule 22**.  Do not propagate the fake.  Verify every citation in this
section against an index before reusing it.

**Jen 1986 remains unread, and it is the most consequential gap.**  Paywalled
at Springer; OSTI holds the bibliographic record (`biblio/5674011`) but the
full-text servlet 404s; unlike Jen 1990 there is no LA-UR preprint; not on
archive.org.  This matters because **three different results are attributed to
that one paper**: Rowland cites its Theorem 4 (a one-sided range `[-d,0]`
eventual-periodicity statement), Wolfram and Kopra cite it for "at most one
periodic column", and its own abstract advertises a third clause — conditions
under which finite ICs "generate at least one constant temporal sequence".
Nothing retrieved restates that third clause.  **Any argument in this repo that
concludes a column is identically zero must reckon with it**, including the
zero-tail theorem's novelty claim in `paper/PUBLICATION-NOTES.md`.

**Wolfram, "Random sequence generation by cellular automata" (1986), full text
unobtained** by two independent routes (canonical PDF exceeds fetch cap; proxy
returned empty).  Treat any specific theorem attributed to it as unverified.

**The official prize bibliography is not a completeness check.**
`rule30prize.org/bibliography` has 29 entries, still stops at 2019, and is
mostly Wolfram Demonstrations, MathWorld pages and Community posts.  It lists
**neither Jen 1990, nor Kopra, nor Taati, nor Rowland-Yassawi** — the four most
relevant modern items.

**Coverage limits.**  Unpublished prize submissions are invisible: the prize
site has no submission archive, no receipt log and no status updates, so there
is no denominator.  arXiv keyword search covers metadata only, so a paper
naming Rule 30 solely in its body is invisible to it; citation-graph traversal
from six seeds was used as the stronger instrument.  Semantic Scholar
rate-limited partway, so forward citations of Rowland 2006, Taati 2015 and
Kopra 2021 were not enumerated — the most likely place a missed row hides.
viXra, figshare and non-English forums were not searched.  Three abstracts
(Maiti et al. 2017, Sur & RoyChowdhury 2023, Bao 2003) and several full texts
were unobtainable.

### 8.7 Why external attempts stopped: four transfer barriers

These recur across the entire external corpus and should be checked against
any future import of an outside technique.  They are the external counterpart
of section 7.3.

**T1. Different object.**  Wolfram's cipher is an `n >= 127` cell **ring with
periodic boundary**, keyed by a **random initial configuration**, keystream =
central cell trace.  The prize object is the **lone-seed column on the infinite
lattice**.  Every cryptanalysis result attacks the former.  Kills: all of 8.3's
crypto rows, all of 8.2's PRNG-testing rows.

**T2. Wrong direction.**  Crypto attacks recover a seed (inverse map); P3 is
forward evaluation from a known one-bit input.  A polytime seed-recovery attack
implies nothing about forward cost.  Kills: Meier-Staffelbach, Koc-Apohan,
Cavagnetto, Kapytka.

**T3. Wrong quantifier.**  P-completeness, SAT/BMC hardness, fine-grained
hardness and measure-theoretic ergodicity all quantify over an input family or
a measure; P1/P2/P3 fix a single input.  Kills: Neary-Woods, Greenlaw et al.,
all fine-grained approaches, and — in measure-theoretic form — every rigidity
theorem and Chan-Lopez & Martin-Ruiz Thm 3.  **This is the external form of the
measure-zero single-orbit gap in 7.3.**

**T4. Work versus depth.**  VDF and proof-of-sequential-work frameworks bound
*depth* under parallelism and cannot yield a work lower bound; non-uniform
circuit lower bounds are structurally dead because a fixed sequence has `O(1)`
circuit complexity per bit by hardwiring.  Kills: Sur-RoyChowdhury, Vuckovac,
and every circuit-complexity route.

**Consequence for P3.**  What stopped people was not inattention but a
technique gap: P3 asks for an unconditional superlinear *work* lower bound on a
single *fixed* sequence, and every available hardness technology either
quantifies over inputs or bounds depth.  None can be pointed at P3 as stated.

**Convergence with section 7.3.**  Three of this repo's internally derived
obstructions have exact external counterparts, independently arrived at: the
measure-zero single-orbit gap (T3, and Chan-Lopez & Martin-Ruiz's own
"requires quantifying the mixing rate"), the arbitrary-input versus
single-point gap (T3/T4, matching this repo's P3 circuit assessment), and the
Rule 90 filter (Kopra's Problem 3.10 obstruction is section 0's filter derived
independently).  That convergence is evidence these are properties of the
problem, not artifacts of this repo's approach.

## Reproduction

All identities in sections 1-3 were verified by direct simulation of the lone
seed to `T=300`, and the discriminator table by enumeration over left-permutive
ECAs.  Modal: $0.  Paid model-provider calls: $0.

## 9. Frontier-attack arms, 2026-08-30

19 parallel arms run under `experiments/overnight-arms/frontier_attack/`,
full detail and per-claim verification status in `FINDINGS.md` there.  No
prize problem moved.  One theorem proved, about the R7 ladder method, not
about Rule 30 directly.  This section records only what changes existing
material; everything else stays in `FINDINGS.md`.

### 9.1 Corrections to sections above

- **`RESULTS-ladder-rung1.md` Lemma 4** is false as written ("the single
  2-cycle"): exhaustive enumeration of its stated map gives *two* cycles, the
  stated one plus the all-zero fixed point, which rows 25/26 exclude.  Repair
  holds; wording does not.
- **R9's stated obstruction (section 4)** is wrong: deriving `{c_n}` and
  refuting `F_n and {not c_n}` differ by one resolution step in both
  directions, and the stored probe's instance is UNSAT by design.
  Satisfiability is not what blocks the Tseitin/pebbling transfer.
- **R8's claim "Rule 30 is outside all of them" (section 4)** is false: Tal
  arXiv:2604.10124v7 Thm 3.2 has left permutativity alone as its hypothesis.
  What blocks it is the measure-zero single-orbit gap (obstruction E), not
  structure.
- **Section 0.1's column-blindness gate** ("moves by `O(1/W)` or less") binds
  normalised, real-valued functionals only.  An exact discrete invariant is
  not caught by it and needs a different test: any quantity computed as
  `f^t(m_0)` for a fixed map on a finite set `M` carries `<= log2|M|` bits
  about the whole orbit, independent of window width (arm a15).

### 9.2 New obstruction

**I.  Satisfiable-and-small.**  Every P3 route in this tree fixes the input to
the lone seed, making the light-cone CNF `F_n` satisfiable with a unique
solution and only `Theta(n^2)` clauses over a `Theta(log n)`-bit input.  Three
proof systems hit that ceiling and nothing else: resolution derivation length
is `Theta(|F_n|)` by exhaustive machine-checked construction (best family
`n^2/2+n` Rule 30, `n^2/4+n` Rule 90); Polynomial Calculus refutation degree is
exactly 2 for Rule 30, 1 for Rule 90, constant in `n`, proved both directions.
Every hardness technique surveyed across these arms (Ben-Sasson-Wigderson,
Dantchev-Riis, Hastad-Risse, Impagliazzo-Pudlak-Sgall, Alekhnovich-Razborov's
design method) is stated for refutation of an *unsatisfiable* instance; no
satisfiable-instance derivation-length lower-bound technique was located.
Predicts, and is why no further proof system was tried against this route:
Sum-of-Squares, cutting planes and similar would first have to explain why
their measure escapes a bound three others could not.  Kills rows 9, 81, 85,
87 (`FINDINGS.md` numbering).  Does not bound arbitrary-input P3 routes
(obstruction G) or a genuinely different complexity notion not yet tried here.

### 9.3 Row status changes (R1 excepted — see 9.4)

Rows 8 and 46 are downgraded from a flat verdict to conditional/open; nothing
is upgraded to PROVED except the R7-ladder limitation theorem, which is a
statement about the method (arm a7), not about P1.

| row | was | now | why |
|---|---|---|---|
| 1 | OPEN | OPEN, sharpened | No proof of R1 can be rule-generic: Rule 90's zero-set kill condition fires verbatim (`r_t=1` iff `t=2^j-1`, unbounded gaps). Three independent encodings (a1 Lemma Z, a2's missing lemma, a7's `Diff_q` gap) converge on the same missing statement about `s(t,1)` on the zero set. |
| 7 | STALLED | mode (i) closed | The phase slip extends to a full half-plane: `plain_{R,k}(w)` nonempty for every `R,k,w`. Mode (i) can never return EMPTY at any depth. Mode (ii) untouched. |
| 8 | OPEN | conditional | Checkerboard is a proved Rule 30 temporal fixed point; if in `Y`, R8's target fails. Proved for Rule 90 (Kummer, exact). For Rule 30, conditional on unbounded patch growth, measured only to `K=6` at `T=2e6`. |
| 9 | OPEN | KILLED | Resolution length capped at `Theta(n^2)` (exhaustive construction); PC degree is `O(1)`; see obstruction I. |
| 46 | OPEN | OPEN, ladder question closed | The generic induction-on-rungs route is closed (Theorem N: the ladder is strict at every level, witness `G_n` for every `n` -- which is Bridy's own Example 2.15, arXiv:1604.08241v2, published 2016, not novel). No polynomial-in-state-count Ore-height bound exists (Bridy's `k*2^(k+1)`, exact worked example `y=x^n` gives height `n` -- exponential in state count, unconditionally). Quantified wall: excludes only `k<=7`-state 2-automatic sequences at this tree's own `N=32000`, `k<=20` at Wolfram's `10^9`-bit check. A specific-sequence uniformity argument for A051023 is still open; that question is separate from the ladder question and is not closed. |

### 9.4 R1 direct attempt, 21st arm

A single non-parallel arm (`a21_r1_direct/`) attempted Lemma Z directly, via
algebraic/probabilistic structure rather than a fourth automaton/SAT/ML
search.  **Row 1 stays OPEN; no proof, but a new named obstruction.**  On
left-supported rows (which include the lone seed) it proved: bounded-window
Bayes error for predicting `r_t` from a width-`m` window of `c`-history
stabilizes exactly at `t=2m+1` (Theorem S) and is strictly positive at every
finite `m` (Theorem W) -- bounded-window closure fails unconditionally.
Exact values `eps_30(1)=1/4` down to `0.17331` at `m=16`, against
`eps_90(m)=1/2` exactly at every `m` (Rule 90's recent window carries zero
information about `r_t`; Rule 30's carries up to 83%, never all of it).
The named missing piece: proving `eps(m)>0`, established on the ENSEMBLE of
left-supported rows, is realised on the lone-seed orbit's own trace
specifically.  That is the measure-zero single-orbit gap (obstruction E)
reached from a new direction, now with a named quantity attached rather than
a vague statement.  Flagged twice in the source document: whether
`eps_30(m) -> 0` as `m -> infinity` is NOT a route to P1 even if answered,
since exactness never arrives at any finite `m` regardless.

### 9.5 Second wave, 2026-08-30: seven arms against the named open avenues

Seven parallel arms (`experiments/overnight-arms/frontier_attack/a22_*/`,
full detail in `FINDINGS.md` section 7) each took one of the avenues left
open above to a stated, spot-checked endpoint.  **No row's status changes.**
The one result worth citing here: `a22_r1_lone_orbit` directly probed
obstruction E for the first time — a held-out predictor of `r_t` from the
*actual* lone-seed trace, compared against a21's ensemble `eps_30(m)` with a
block-level test and a matched i.i.d. control, then re-checked after an
initial pass mis-stated one cell (m=12, all-t) as a surviving Bonferroni
anomaly: a replication at the same sample size with an independent RNG seed
returned it to no deviation, so that cell is retracted, not evidence of
anything (`a22_r1_lone_orbit/GAP_CLOSEOUT.md`).  A structurally independent
re-derivation of `eps_30(m)` itself (array-based, not a21's bitmask-packing
method) exact-matches every value `m=1..16`, closing a real gap in a21's own
pipeline whose direct-enumeration cross-check silently stops covering
anything past `m=10`.  At every window width where the comparison is
trustworthy, the lone orbit's error is statistically indistinguishable from
the ensemble value; the large-`m` divergence that remains (m=14, m=16) is a
reproducible estimator artifact (present identically in the ensemble control
with no orbit involved), not orbit atypicality.  Obstruction E stays open —
this is a null result on the first direct probe of it, not a resolution.  `a22_p2_checkerboard_growth` extended
row 79's horizon 2x and found no rescue (one family's diagonal `K` flat,
two still growing, within the same fluctuation band as before) plus a
structural defect-propagation probe ruling out the simplest bounded-soliton
rescue mechanism without proving unbounded growth in the actual diagram; net
INCONCLUSIVE, consistent with row 79's conditional verdict.  The remaining
five arms (row 46 specific-sequence route, row 41 alternative strategy, row
82 soficness push, R7 mode (ii), and a Tier-3 literature check on succinct
circuit complexity of `n -> c_n`) each returned a clean negative, a stated
dead end, or a confirmed-open literature gap, with no committed material
requiring correction.

## 10. Roundtable follow-up 3, 2026-08-30

An LLM-panel roundtable (`experiments/overnight-arms/roundtable_followup3/`)
produced 36 candidate attack sparks; triage selected 6 for independent
verification, each write-up produced and then re-checked by a separate
verification pass.  **All six KILLED.  No prize problem moved, and no new
named obstruction is introduced** — every kill lands on an obstruction
already catalogued in section 7.3, one lands on the standing `O(log t)`
family as a sixth representation, and one duplicates an already-proposed
register row that simply hadn't been merged yet (now row 76, above).  This
section documents only what changes or adds to existing material; full
detail is in each `RESULTS-followup3-*.md` file.

### 10.1 Subword complexity — merged as row 76, not a new finding

`RESULTS-followup3-subword-complexity.md` re-derives, independently, exactly
what `novel_frameworks/TRIAGE-novel-frameworks.md` already computed and
proposed as row 76 (A4) and never merged: Morse-Hedlund's `p(n) > n` check is
vacuous against P1 by the theorem's own logical form (obstruction H) —
confirming `p(n) > n` for `n <= 64` on a 200,000-bit prefix excludes only
periods below roughly that range, strictly weaker than the prize
announcement's own `10^9`-bit exclusion.  Independent numbers match exactly
(`p(8)=256`, `p(16)=62377`).  Folded into 7.1 as row 76 rather than
duplicated here; see that row for the full citation.

### 10.2 Obstruction D, confirmed on a third mechanism (ideomotor residual)

`RESULTS-followup3-ideomotor-residual.md` kills the "unlocked-beat" residual
`rho_k` on three independent legs: (1) vacuous by construction — under the
periodicity hypothesis the gate is decided once, at `j=0`, not beat-by-beat,
so `rho_k` collapses to either the constant 0 or an unconditional sum with
`c` never re-entering; (2) the Rule-30-specific premise is closed by solving
`RESULTS-eventual-period.md`'s own defect recurrence directly — the raw
`x=0` equation is one equation in two unknowns, leaving `r`'s defect a free
bit, and the document's own PROVED finite-prefix lemma independently shows a
periodic centre trace constrains the right column not at all at any finite
horizon; (3) the universal form of the premise is refuted by a proved
counterexample — Rule 90's true period-1 centre column has closed-form
`rho_k = 2*floor(log2(k+1)) - k -> -infinity` (via Kummer's theorem on
Pascal's triangle mod 2), not merely measured unbounded.  This is
**obstruction D** (the missing composition law), confirmed again, with the
missing law shown not merely unfound but algebraically empty (leg 2) and the
general boundedness claim shown false by theorem, not simulation (leg 3).
No new obstruction.

### 10.3 Obstruction B, in its strongest available form (felting preimage graph)

`RESULTS-followup3-felting-preimage-homology.md` formalizes the spark's
"compatibility graph" (left-half IC prefixes graded by length, edges =
one-cell extensions) and proves it is a rooted tree — zero cycles, hence no
target invariant to compute — for **any** deterministic, finite-propagation-
speed rule, verified exhaustively to `k=40` on both Rule 30 and Rule 90 with
identical combinatorial signature.  This is not the usual form of obstruction
B (run it on Rule 90 and see it also fires): the proof never inspects which
rule is running, so the construction never had a chance to distinguish Rule
30 from Rule 90, and running the Rule 90 control is redundant with the proof
rather than a separate check of it.  Checked robustly rather than assumed: an
existentially-quantified free-right-half node set (the loosest node
definition the spark's text supports) still produces a forest for both
rules, including Rule 90's degenerate case where every word is a node; the
tight construction's node-count profile (a "broom": true configuration plus
a one-level dying perturbation) is also identical for both rules to `k=40`.
No cycle-bearing formalization of the spark's own words was found.  The one
formalization that does have real cycle structure (a sliding-time-window
SFT/de-Bruijn graph) is not new — it is the R7 ladder automaton, already
characterized under **obstruction F** (`RESULTS-ladder-rung1.md`; row 7),
with a verdict already on record.  Recorded as a strengthening of
obstruction B (a *proved*, rule-blind-by-construction instance, not merely a
tested one), not a new letter.

### 10.4 Obstruction A, sixth representation (weaver preimage count)

`RESULTS-followup3-weaver-preimage-count.md` proves the only non-duplicate
reading of the spark's preimage count `P(t)` (fix the initial row, count
forward-consistent left halves) has closed form `P(t) = 2` for every `t`,
for every left-permutive rule, via an exact diagonal-toggle bijection
argument — confirmed exhaustively (`k<=16`, every prior-bit setting, both
rules, 0 counterexamples), by backtracking to `t=40`, by independent GF(2)
linear algebra to `t=1000` for Rule 90, and generalized to
`P(W,t) = 2^(W-t+1)` across window/prefix alignments.  The pre-registered
kill condition's divergence check fires, but downward into total triviality
(`log2 P(t) = 1`, constant) rather than toward anything new; Rule 90's true
periodic orbit gives the identical constant, so the quantity was never
capable of encoding periodicity in the first place (**obstruction B**,
strongest form).  The underlying mechanism — the newest boundary bit is a
strict one-bit toggle, so nothing propagates inward from it — is a sixth
independent representation of **obstruction A** (the `O(log t)` wall,
section 7.3), joining the five already listed there.  No new obstruction; not
added to obstruction A's row list in 7.3 since it kills no additional row
there (this is verification of the general mechanism, not a new row).

### 10.5 Definitional impossibility plus obstruction C (ball-fission topology)

`RESULTS-followup3-ball-fission-topology.md` kills "fission of a connected
1-component" on three stacking grounds.  New content: under the literal
reading of the spark's own definition, a parent lemma (every output-1 credits
at least one 1-valued causal neighbor, true for Rule 30 and Rule 90 alike by
direct case analysis) forces the whole diagram's 1s into a single connected
component at every time step, for either rule — fission is proved impossible
before any periodicity or rule-comparison argument is needed, confirmed
exhaustively to `t=300`, both rules, 0 violations.  Checked honestly rather
than left aside: the charitable same-row "domain" reading of fission/merge
does not show the claimed OR-vs-XOR asymmetry either — measured, the
direction is reversed (Rule 30: 0 annihilations, 4984 merges; Rule 90: 2409
"fissions," 0 merges), driven by Rule 90's known checkerboard sparsity, not
a splitting mechanism.  The pre-registered single-column-blindness gate
(**obstruction C**) then fires exactly as specified on what's left: for
every non-constant periodic overwrite of column 0, both readings' statistics
move only within `|x|<=1` of the overwritten column, not growing over 300
steps — a local-mismatch artifact of the same shape as obstruction D, not a
signal.  (The one word producing a large effect, constant-zero, is an
unrelated generic graph-cut-vertex artifact, periodicity-independent.)  The
new content here — a proof, not a measurement, that the premise is
definitionally false for any radius-1 rule of this shape — sharpens
obstruction C's usual empirical form but is filed under it, not as a new
letter, since its role in this document is the same: closing a route by
showing it cannot see past column 0.

### 10.6 Duplicate of row 3's run-of-ones wedge, not a new instance of obstruction D (craquelure charge)

`RESULTS-followup3-craquelure-charge.md` is the one result here where the
pre-registered kill condition's own framing was wrong about *why* the route
dies.  Part (a) is confirmed true and is a genuine, non-hand-wavy
discriminator: the two-orbit defect field `D(t,x) = a(t,x) XOR a'(t,x)`
obeys an autonomous local rule for Rule 90 (proved, exhaustive 64/64
footprint check, 1600/1600 simulated confirmations) and does not for
Rule 30 — Rule 90's difference field is itself a Rule 90 orbit; Rule 30's is
not a self-contained dynamical system.  Part (b), the "signed stratigraphic
charge" `kappa`, is genuinely nonzero (24/64 cases) — unlike the structurally
identical-zero `kappa` in `RESULTS-followup2-gauge-holonomy.md` — so this is
not that report's failure mode.  It is instead an **exact restatement** of
`RESULTS-eventual-period.md`'s already-proved run-of-ones wedge: at the
centre site, `kappa(t,0) = c_t AND d_t(1)` is, bit for bit, that document's
erasure term, confirmed as the unique consistent solution in all 8 of 8
applicable cases, and its bound is the same one already on record — a
nonconstant periodic word has bounded zero-runs, so no accumulation is ever
forced, confirmed further here by adversarial simulation matching the bound
exactly at every period word tested.  This is the same mechanism that killed
**row 3** (R3, run-of-ones wedge descent, grouped under obstruction A in
7.3), reached from a different name and a different derivation, not a new
instance of obstruction D's missing-composition-law pattern as triaged.  No
row or obstruction changes; recorded here only because the triage's own
framing needed correcting, matching this document's practice of naming a
wrong classification when found (compare section 9.1).

### 10.7 Summary

| spark | obstruction / prior material | new content beyond confirmation |
|---|---|---|
| subword complexity | H; merged as row 76 | none — independent re-derivation of unmerged row 76 |
| ideomotor residual | D | none — same law shown empty (not unfound) and false (Rule 90 theorem) |
| felting preimage homology | B (strongest form); touches C, F | proved rule-blind-by-construction forest theorem |
| weaver preimage count | A (6th representation); B | closed-form `P(t)=2`, `P(W,t)=2^(W-t+1)` theorem |
| ball-fission topology | C; shape of D | proved definitional impossibility of fission, any radius-1 rule |
| craquelure charge | row 3 / A group (not D as triaged) | corrects triage's own misclassification |

No row in 7.1 changes status; row 76 is a merge of pre-existing, unmerged
material, not a new finding.  No new obstruction letter is warranted by any
of the six.

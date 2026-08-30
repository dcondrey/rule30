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
re-run at larger R or k — see `RESULTS-ladder-rung0.md` section 3 for the
measurement that retires depth, and section 4 for the constraint changes that
are the only remaining way in.**
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
The rung's actual contribution is a proved obstruction, the **depth-3 escape
family**: every witness has cycle `S·B^m` with `S=[2,0,0,1,0,2]`,
`B=[2,0,0,0]`, a period-4 defect train in columns `-1..3` carrying one phase
slip per cycle.  Machine-verified to `m=200`; a pumping argument (all checks
are radius-1-local, and every window of `B^m` occurs in the verified `m=3`
instance) plus the phase-slip argument extends it to all `m`.  Consequence:
**for every `q`, the `R=3` ladder is nonempty, so no choice of `q` closes
`p=2` at fixed depth 3**, and BFS shows the slip surviving to `R=8`.
Rung 1, sharpened: does any finite `R` kill the slip, or does it extend to a
full half-plane?  The latter would prove this ladder undecides `p=2` entirely.
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

## Reproduction

All identities in sections 1-3 were verified by direct simulation of the lone
seed to `T=300`, and the discriminator table by enumeration over left-permutive
ECAs.  Modal: $0.  Paid model-provider calls: $0.

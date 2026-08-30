# R7 rung 0: the omega-automaton periodicity ladder, run

Status: **calibration PASSED, open cases all NONEMPTY.  No theorem for any
p >= 2.  R7 is not killed, but the blocker is now named and it is not depth.**

Date: 2026-08-30.  Code: `experiments/rule30/ladder/` (pre-existing, unrun) and
`experiments/rule30/p1_attack/` (this run's drivers).  Modal: $0.  Paid
model-provider calls: $0.

## 0. What was and was not attacked

Three angles were proposed for this cycle: (1) a boundary-state growth
invariant `S(t) -> infinity`; (2) backward preimage reachability for periodic
centre words with `P in [3,12]`; (3) a SAT/F2 obstruction from
`C(t+P) XOR C(t) = 0`.  All three collapse onto R7, which already existed in
this repo as 501 regression-tested lines and had never been run:

* (2) **is** R7 mode (i).  `ladder.py` calls it `diff_q=None`, plain emptiness,
  and `run_rung0.py` already parameterises it by tail word.  A fresh backward
  search would not inherit `regression(rule, R, k, T=300)`, and an emptiness
  verdict from an unvalidated search is worth nothing.
* (3) is not runnable as posed.  Fix the seed and a finite-window UNSAT is
  brute-force cycle exclusion, which the prize data check already covers to
  10^9 bits.  Leave the transient existentially quantified and no finite CNF
  is ever UNSAT.  The escape is the Buchi lasso, i.e. R7.
* (1) has an inverted success criterion.  `PATH.md` R7 names state blowup as
  the *expected kill mode*.  A curve showing `S(t) -> infinity` is the failure
  signature of the method, not evidence of non-periodicity.  The growth was
  measured anyway (section 3) because its *rate* turned out to be the finding.

So one merged run replaced three agents.  Nothing here is a new method.

## 1. Soundness and calibration: PASSED

`run_rung0.py`, full log at `experiments/rule30/p1_attack/rung0.log`.

```text
regression rule=30 R in {1..5}, k in {1,2}, T=300: 0 mismatches, safety run ok
regression rule=90 R in {1..5}, k in {1,2}, T=300: 0 mismatches, safety run ok
```

Calibration A (rule 30, p = 1, mode ii with q = 1), the repo's own constant-case
theorems, rederived mechanically:

| case | R | verdict |
|---|---:|---|
| w = 1 | 1 | **EMPTY** |
| w = 1 | 2 | **EMPTY** |
| w = 0 | 1 | NONEMPTY (witness verified, onset 2) |
| w = 0 | 2 | **EMPTY** |

Calibration B (rule 90 control, true eventually-zero centre column) stays
NONEMPTY at R = 1..5, witness verified at every R.  This is the section-0
filter discharged mechanically: the pipeline does not prove for Rule 90 the
thing it proves for Rule 30.

**Both calibration conditions in `PATH.md` R7 are met.**  What mode-ii
emptiness gives directly is the implication *centre eventually w-periodic =>
col_{-1} eventually q-periodic*, on every word the constraints admit.  The
contradiction is then supplied by Jen 1990 Prop. 3 / Kopra 2023 Thm 3.5, which
forbid two adjacent eventually periodic columns.  With that cited step,
`Thm(1)` is a machine-checked statement and not only a paper one: no Rule 30
diagram satisfying the wedge constraints has an eventually constant centre
column, for any transient length.  This restates `RESULTS-inverse-trace.md` and `PATH.md`
section 2; it is validation, not discovery.

## 2. Open cases: NONEMPTY everywhere, p = 2..8

All 71 primitive binary necklaces of length p <= 8 (rotations are equivalent
because the Buchi onset is guessed; imprimitive words are covered by their
primitive divisor), at R = 2, k = 2, modes i and ii:

```text
p = 1:  w = 0, w = 1   ->  mode ii EMPTY          (the theorem above)
p = 2..8, all 69 words ->  mode i and mode ii NONEMPTY, witness verified
```

Log: `p1_attack/sweep_periods.log`.  Every NONEMPTY carries a lasso whose
prefix and cycle were re-derived and checked against all imposed constraints
by `verify_witness`; zero verification failures.

No verdict was ever `INCONCLUSIVE (state cap hit)` in this table, so these are
decisions, not timeouts.

## 3. Depth does not tighten, and that is the finding

`run_rung0.py` sweeps only the right depth R and fixes k = 2.  The left depth k
is the untested knob and imposes strictly more wedge and edge constraints, so
it was the natural place to look for tightening.  It gives none.

p = 2, tail 01, q = 1 (`p1_attack/sweep_k.log`):

| k \ R | 2 | 3 | 4 |
|---|---:|---:|---:|
| 2 | 1,445 | 5,574 | 22,087 |
| 3 | 5,861 | 22,374 | 88,423 |
| 4 | 23,397 | 89,958 | 354,151 |
| 5 | 92,005 | 358,758 | 1,416,039 |
| 6 | 362,533 | 1,426,790 | cap hit |

Verdict is NONEMPTY in every decided cell.  Representative p = 3, 4, 5 tails
(`p1_attack/deep_small_p.log`) at (R,k,q) = (4,3,1), (4,3,2), (3,5,1), (5,2,4):
NONEMPTY in all 28 runs, witness verified in all 28.

Two facts:

1. **The constraints prune a constant fraction of the raw window space,
   independent of depth.**  The window length is `R + k` and the raw window
   space is `4^(R+k)`, so the alphabet factor alone predicts 4x per increment.
   Normalising it out, `states / 4^(R+k)`:

   | (R,k) | 2,2 | 3,2 | 4,2 | 5,2 | 2,3 | 2,4 | 2,5 | 2,6 | 4,4 | 4,5 |
   |---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
   | ratio | 5.64 | 5.44 | 5.39 | 5.38 | 5.72 | 5.71 | 5.62 | 5.53 | 5.40 | 5.40 |

   Flat to within 6% across a 5,500x range in raw size and in both directions.
   The measured 3.86-4.06 growth per increment is therefore the encoding's
   alphabet factor and nothing else: added depth buys no additional pruning.
2. **The verdict is uniform in R and k over the whole range decided.**  So the
   obstruction is not compute and not depth.  Adding depth to this constraint
   set will not produce `Thm(p)` for any p >= 2, and running it further is
   spending compute on a decided question.

The blowup PATH.md predicted is real and is quantified here, but it is not what
stops the route.  What stops the route is that the imposed constraint set --
light cone, both edges, Buchi periodicity, optional `Diff_q` -- is satisfiable
by left half-planes that are not the lone-seed diagram.  The ladder is a sound
over-approximation and its approximation is too coarse at p >= 2.

Note this is *not* vacuity: for p = 1 the same constraint set does bite, mode i
NONEMPTY and mode ii EMPTY.  The `Diff_q` tightening is doing real work at
p = 1 and stops doing it at p = 2.

## 4. What would have to change

R7's remaining hope is a constraint that binds the right side.  Candidates, in
the order their cost suggests:

* a right-wedge constraint (`col_x(t) = 0` for `x > t`) on the modelled columns,
  which the current encoding never imposes;
That is the only live candidate, and two others that suggest themselves are
already dead:

* *The pin cascade as an automaton-level safety constraint.*  Dead by
  construction.  `INV[30] = an ^ (a | b)` is the exact inverse transduction and
  is applied to every modelled column, and the pin
  `r_t = 1 and c_t = 0 => r_{t+1} = 1` is a consequence of the rule.  It is
  therefore already entailed among the modelled columns and adds no constraint.
* *`Diff` quantified over all q rather than one fixed q.*  Dead by
  `RESULTS-eventual-period.md:95-100`, which proves it: a nonconstant periodic
  word has bounded one-runs, hence a bounded wedge and no descent.  That is
  also the explanation of the p = 1 / p = 2 gap measured here -- the pin
  saturates for a constant word and only wedges for a nonconstant one -- so
  fixed q is not the weakness and no choice of q escapes it.

The right-wedge is not a depth increase.  Until it is encoded and passes the
same two calibrations, **do not re-run the ladder at larger R or k.**

## 5. Honest scope

No per-period exclusion for any p >= 2 was obtained.  Nothing here bears on
Problem 1.  `Thm(1)` is a mechanisation of results this repo already held on
paper.  The new content is exactly: the calibration passing, the p <= 8
NONEMPTY table with verified witnesses, and the measured depth-independence in
section 3, which retires "run the ladder deeper" as a route.

## Reproduction

```sh
cd experiments/rule30/ladder && uv run python run_rung0.py 5
cd ../p1_attack && PYTHONPATH=../ladder uv run python sweep_periods.py 8 2 2
PYTHONPATH=../ladder uv run python sweep_k.py
PYTHONPATH=../ladder uv run python deep_small_p.py
```

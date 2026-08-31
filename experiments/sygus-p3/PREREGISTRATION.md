# Pre-registration: bounded exact circuit synthesis for Rule 30's centre column

Written 2026-08-31, before any Rule 30 `k_min` number was recorded beyond the
`m = 4` and `m = 5, k = 6` calls used to size the feasibility curve (those two
are disclosed below, in "already run", so nothing here is written after seeing
a result it predicts).

## 1. The question

Let `c(n)` be Rule 30's centre column at step `n` from a single-cell seed on a
background of zeros, with `c(0) = 1` the seed row (OEIS A051023, offset 0).

For `m` input bits, let `f_m : {0,1}^m -> {0,1}` be the function taking the
binary encoding of `n` to `c(n)`, for all `n < N = 2^m`.  Let `k_min(m)` be the
minimum length of a Boolean chain over the full two-input basis `B2` computing
`f_m` -- i.e. the combinational complexity `C(f_m)` in Knuth's sense.

**Measure `k_min(m)` exactly, by complete search, for as large an `m` as the
solver reaches; report a bracket where exactness is out of reach.**

Completeness is the point.  An UNSAT at `k` is a theorem: *no* Boolean chain of
length `k` computes `c` on `[0, 2^m)`.  That is categorically different from a
stochastic search failing to find one, which is what the parallel LLM-evolution
arm produces.

## 2. Why this is not already answered in this repo

Two prior results bound the neighbourhood and neither covers this.

* **Obstruction I** (`docs/rule30/PATH.md` 9.2) concerns *refutation* of the
  light-cone CNF `F_n` with the input pinned to the lone seed.  It observes
  that every such instance is satisfiable with a unique solution, so no
  unsatisfiability-based hardness technique applies.  The present experiment
  runs in the opposite direction: `n` is a genuine free binary input, the
  instances are *synthesis* instances, and the informative answers are the
  UNSAT ones.  Obstruction I does not touch it.

* **Arm `a22_p3_succinct_index`** (`experiments/overnight-arms/frontier_attack/
  FINDINGS.md` §7) ran a literature-only Tier-3 check on exactly this object
  and concluded "GENUINELY OPEN, no prior work transfers", closing with "No
  first probe was executed, per this arm's literature-only scope."  It also
  records the distinction this experiment relies on: PATH.md 8.7's T4
  ("non-uniform circuit lower bounds are structurally dead") is about *one
  hardwired circuit per `n`*, "a different object from the *uniform*
  succinct-index question asked here -- the register does not currently draw
  that distinction anywhere."  This experiment is that first probe.

## 3. Method

* Ground truth from two independent simulators (list-of-cells, bignum-bitwise)
  that must agree to `t = 200`, cross-checked against all 102 published terms
  of A051023.  Both checks are run and recorded before any synthesis.
* Encoding: the SSV formulation of Boolean-chain exact synthesis, following
  Haaswijk-Mishchenko-Soeken-De Micheli, IEEE TCAD 39(4):871-884 (2020), over
  the chain model of Knuth TAOCP 4A 7.1.2.  Full `B2` basis minus the six
  degenerate operators.  Symmetry breaks: no dead step, distinct fanin pairs,
  colex step order -- each validated by re-running the sanity suite with them
  disabled and requiring identical `k_min`.
* Solver: CaDiCaL via `python-sat`, chosen on a measured comparison against Z3
  on byte-identical CNF, not on assumption.
* Search: `k` upward from 1, never binary search (the no-dead-step predicate is
  not monotone in `k`).  First SAT is `k_min`; the UNSAT at `k_min - 1` is the
  theorem.  Every returned chain is re-evaluated by an independent evaluator
  against the truth table before it is believed.
* `N = 2^m` exactly, so the truth table has no don't-cares and `k_min` is
  well defined.  Both index offsets (`c(0)` = seed row, and `c(1)` = seed row)
  are measured at `m = 4`, since the convention shifts the truth table.

## 4. What counts as an outcome -- and the reason the naive discriminator was
   dropped

The naive framing ("`k_min` grows linearly in `N` = incompressible; sublinear =
shortcut") **cannot fire on a plausible negative at this scale and is therefore
not the registered discriminator.**  The maximum combinational complexity over
*all* `m`-bit functions is `u(2)=1`, `u(3)=4`, `u(4)=7`, `u(5)=12` (Knuth
7.1.2).  At `m <= 5` every function on earth is ceilinged in the low teens, so
"sublinear in `N = 2^m`" is guaranteed by arity alone and says nothing about
Rule 30.  Registering it would be registering a foregone result.

The registered discriminator is instead a **fixed-`m` comparison against
controls**:

* `f_m` for Rule 30 (target).
* `f_m` for Rule 90's centre column and Rule 150's centre column -- linear CAs,
  the repo's own filter device.
* Parity of `n` (Thue-Morse-like; known `k_min = m - 1`), MAJ-3, AND-`m` as
  fixed reference points with literature-known minima.
* 50+ uniformly random `m`-bit truth tables, seeded, same encoding and solver,
  giving the null distribution.

**Strong outcome (would be a genuine signal):** `k_min` for Rule 30 sits at or
below the structured controls, or in the bottom decile of the random
distribution, at `m = 4` *and* `m = 5`.  That would say the centre column is
unusually cheap to compute from a positional index -- a compression signal.

**Null / expected outcome:** Rule 30 sits in the bulk of the random
distribution, well above the structured controls.  This is the overwhelmingly
likely result and is what the experiment is expected to record.

**Kill condition on the instrument (checked FIRST, before spending solver
hours):** if the structured controls' `k_min` at `m = 4` is *not* appreciably
below the random-function median at the same `m`, the instrument has no
resolving power at this scale, and any percentile statement about Rule 30 is
meaningless.  In that case the experiment reports only the raw `k_min` values
and the UNSAT theorems, and draws no comparative conclusion.

## 5. What this cannot do

Stated plainly, before the runs:

* **A bounded result cannot resolve P3.**  P3 is an asymptotic claim about
  cost per bit as `n -> infinity`.  Every number here is a statement about one
  finite `m`.  This is the same structural gap as obstruction H: a finite
  computation, however exhaustive, does not close an asymptotic question.
* **The growth curve will have at most four or five points**, over an `m` range
  where the arity ceiling dominates.  Any trend read off it is suggestive at
  best and is reported as such.  It will not be described as evidence of
  incompressibility on its own.
* **`k_min` is not monotone-interpretable across `m`** as a compression rate,
  because the target function changes with `m` (it is a longer prefix, not a
  refinement).
* The value delivered is: a small number of exact theorems of the form "no
  `k`-gate circuit computes `c` on `[0, 2^m)`", a measured feasibility curve
  telling the next person where the wall is, and one control comparison.  Not
  a prize attack.

## 6. Already run before this document was written

Disclosed so the pre-registration is honest about what was already visible:

* Both simulators agree to `t = 200` for rules 30, 90, 110, 150; both match all
  102 published A051023 terms.
* Sanity suite (xor2, and2, maj3, parity3, parity4, and4, maj3-of-4) reproduces
  every literature-known minimum, with and without the optional symmetry
  breaks; all 256 three-bit functions are SAT at `k = u(3) = 4`.
* Solver benchmark at `m = 4`, Rule 30, `k = 4..7`: CaDiCaL 0.07-0.29 s vs Z3
  2.0-4.7 s on identical CNF.  This benchmark exposed `k_min(m=4) = 5` for
  Rule 30 as a side effect.
* One feasibility probe: `m = 5, k = 6` is UNSAT in 357 s.  This sets
  expectations that `m = 5` will yield a bracket rather than an exact value,
  and that `m = 6` is out of reach.

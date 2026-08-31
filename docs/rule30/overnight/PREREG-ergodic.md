# PREREG — arm "ergodic": exact classification of jointly (shift, Rule 30)-invariant Markov measures

Registered 2026-08-30, BEFORE any experiment. Triage row 10.

## Objects

F = Rule 30 as an endomorphism of the full shift ({0,1}^Z, sigma); F is surjective
(left-permutive), so uniform Bernoulli(1/2) is F-invariant (classical, Hedlund-line; this is a
VALIDATION anchor, not a finding). Candidate class: shift-invariant memory-m Markov measures,
m = 1, 2, 3, parameterized by exact rational transition probabilities.

Pushforward on cylinders: (F mu)[w] = sum over u in f^(-1)(w), |u| = |w|+2, of mu[u].
Invariance necessary conditions at depth L: (F mu)[w] = mu[w] for all words |w| <= L.
F mu of a Markov measure is generally not Markov, so depth-L equality is NECESSARY only;
any surviving non-obvious solution gets L pushed upward until it dies or persists to L_max.

## Task, metric

For each m in {1,2,3}: solve the polynomial system {(F mu)[w] = mu[w], |w| <= L} exactly
(sympy, rational/Groebner; no floats) for L = min(2m+3, ...) up to L_max = 12 as compute
allows. Metric: the exact solution variety per (m, L); classification of every component
(uniform Bernoulli / atomic-periodic / degenerate boundary / other), with entropy and support
noted. Known atomic checks: delta_{all-0} is F-invariant and shift-invariant; the two
alternating configurations are F-fixed, so their symmetrized atom pair is jointly invariant,
zero entropy. These MUST be recovered by the machinery (validation), then set aside.

## Hypotheses as questions

- H1: within memory <= 3, is uniform Bernoulli(1/2) the ONLY jointly invariant measure with
  full support (equivalently all transition probabilities in (0,1))?
- H2: do the necessary conditions at L = 12 already isolate it (zero-dimensional non-degenerate
  component), or does a positive-dimensional family survive?

## Baselines / controls

- Identity CA: every shift-invariant Markov measure is invariant; machinery must return the
  full parameter space (catches over-constraining bugs).
- Rule 90 (surjective, additive): uniform Bernoulli must pass; delta_{all-0} must pass.
- Bug gate: if uniform Bernoulli(1/2) fails invariance for Rule 30 at any depth, the pipeline
  is wrong (classical result); fix before any other claim.

## Strong outcome

PROVED (finite, exact, and honest about its scope): "every memory-<=3 shift-invariant Markov
measure satisfying joint invariance to depth 12 is uniform Bernoulli or one of the enumerated
zero-entropy atomic solutions" — the first exact rigidity data point for a non-algebraic,
left-permutive-only CA (triage gap G1; Host-Maass-Martinez 2003 and Pivato 2005 cover
algebraic/bipermutative only; repo Arm 2 in PREREGISTRATION.md recorded only
Hedlund-invariance and never ran discovery). REDUCED companion statement: the extension from
the finite Markov class to all shift-ergodic measures, and from rigidity to single-orbit
equidistribution (P2), stated referee-style as the remaining obligations.

## Kill conditions (can fire on plausible negatives)

- K1: an exact non-uniform solution with all transition probabilities in (0,1) survives L = 12
  at some m <= 3 -> uniqueness dies in the Markov class; report the measure exactly as a live
  counterexample candidate (this fires the kill for the equidistribution route even though it
  would be a striking object in its own right).
- K2: the symbolic systems for m = 3 are computationally infeasible overnight (Groebner blowup)
  AND m <= 2 yields only the trivial recoveries -> arm ends REDUCED at the m <= 2 statement,
  with m = 3 stated as the unmet obligation; no silent scope shrink.

## Cheapest disconfirming test (runs FIRST)

m = 1 (Bernoulli(p), then 2-parameter Markov), blocks |w| <= 5, exact: expected solutions
p = 1/2, degenerate p = 0, and nothing else. Runs in seconds. If machinery rejects p = 1/2
the pipeline is broken (bug gate); if a non-uniform p passes, K1 is live immediately.

## Seeds, spending

Exact rational arithmetic, deterministic, no RNG. Local CPU only; Modal $0; paid model calls $0.
Files: experiments/overnight-arms/ergodic/, runs/overnight/ergodic/. Results: RESULTS-ergodic.md.

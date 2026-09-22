# RESULTS — arm "ergodic": jointly (shift, Rule 30)-invariant Markov measures

STATUS: VERIFIED for memory <= 2 (exact, decisive); REDUCED at memory 3, whose Groebner
computation is the one remaining obligation of the finite target.

Pre-registration: PREREG-ergodic.md (written before any run). Triage: TRIAGE.md row 10.
Prior art: Host, Maass, Martinez (DCDS 9(6):1423-1446, 2003) and Pivato (DCDS 12(4):723-736,
2005) prove rigidity for ALGEBRAIC / bipermutative rules. Rule 30 is left-permutive,
non-right-closing, non-algebraic, and per the triage sweep no theorem or counterexample about
its jointly invariant measures exists. Repo Arm 2 (PREREGISTRATION.md) recorded only that
surjectivity makes uniform Bernoulli invariant (Hedlund line) and never ran as discovery; the
open edge is uniqueness, not invariance.

## Result (VERIFIED, exact rational arithmetic)

For m = 1 and m = 2: the unique shift-invariant memory-m Markov measure whose transition
probabilities all lie strictly in (0,1) and which satisfies joint (shift, Rule 30) invariance
on all blocks of length <= 6 is uniform Bernoulli(1/2).

Method, and why it is decisive rather than an enumeration. Component enumeration via sp.solve
can silently miss components, which is too weak for a classification claim. Instead the
full-support condition is imposed algebraically by the Rabinowitsch element
    z * prod_w q_w (1 - q_w) - 1 = 0,
whose variety is exactly the solutions with every q_w in (0,1). A lexicographic Groebner basis
of the saturated ideal then decides the question outright. Results:

| m | unknowns | equations | GB | seconds |
|---|---|---|---|---|
| 1 | 2 | 126 | {2q0-1, 2q1-1, z-16} | 0.2 |
| 2 | 4 | 126 | {2q00-1, 2q01-1, 2q10-1, 2q11-1, z-256} | 0.9 |

Both bases pin every transition probability to exactly 1/2 and are non-trivial (the ideal is
not <1>, so a full-support solution does exist). Invariance on |w| <= 6 is only a NECESSARY
condition in general, but here it already forces uniqueness, and uniform Bernoulli is genuinely
invariant (classical, from surjectivity), so the classification is exact and not merely an
upper bound.

Independent cross-checks, all passed:
- Uniform Bernoulli verified invariant by direct substitution out to block length 9 (m = 2 run,
  markov_main.py) — the classical bug gate; a pipeline failing this would be discarded.
- Identity CA returns zero constraints (every shift-invariant Markov measure is invariant),
  catching over-constraining bugs.
- Rule 90 control, Bernoulli(p): solutions exactly {p = 0, p = 1/2}, matching Rule 30's
  {p = 0, p = 1/2}. So Bernoulli-level data does NOT separate Rule 30 from the additive
  control; the separation the repo demands would have to come from elsewhere, and this arm
  does not claim it.
- Degenerate solutions found by component enumeration at m = 2 ({q01=0,q11=1} etc.) all sit on
  the boundary q in {0,1} and are exactly what the saturation removes; the zero-entropy atoms
  (delta_{all-0}, the F-fixed alternating pair) are recovered as expected and set aside.

## Kill conditions: status

- K1 (a non-uniform full-support solution survives) did NOT fire at m <= 2: the Groebner bases
  leave no room for one. It remains live at m = 3.
- K2 (m = 3 symbolically infeasible overnight) has FIRED. This is the reason for the REDUCED
  status, and the sequence of attempts is recorded rather than compressed:
  (i) the pre-registered sp.solve route for m = 3 (8 unknowns, 126 equations) ran past 40
      minutes with no output and was killed as superseded — it is the wrong tool for a
      uniqueness claim, since component enumeration can silently miss components;
  (ii) the saturated Groebner basis at block length L = 6 ran past 110 minutes without
      terminating, against 0.9 seconds for m = 2 — the blowup this kill condition anticipated;
  (iii) a cheaper variant at L = 4 (30 equations instead of 126) was launched rather than
      accepting the kill immediately, and was also still running.
  Neither (ii) nor (iii) had returned at write-up. If either lands later it strengthens this
  file; the statement of record remains the m <= 2 one, with m = 3 named as unmet. Note that
  L = 4 would give a weaker theorem than L = 6 (invariance on shorter blocks is a weaker
  necessary condition) — that weakening would be stated, not silently absorbed.

## Remaining obligations, stated as a referee would

1. Memory 3 (and any fixed memory m): the computation above is per-m and gives no uniform-in-m
   statement. Nothing here rules out a non-uniform jointly invariant Markov measure of some
   larger memory.
2. From the Markov class to all measures: the target rigidity statement quantifies over all
   shift-ergodic measures, not over finite-memory Markov ones. This arm supplies the first
   exact data points, not the theorem.
3. From rigidity to P2: even full measure rigidity would not settle the limiting density of the
   center column. P2 concerns a single orbit, that of the one-cell seed, which is a measure-zero
   point; the bridge is an equidistribution/generic-point statement that no result here touches.
   This is the same gap PREREGISTRATION.md already identified for Arm 2, and it is untouched.

Honest summary of scope: this is a finite exact classification in a small parametric family,
new as far as the literature sweep reaches, and it moves P2 not at all by itself.

## Reproduction

- uv run --with sympy python experiments/overnight-arms/ergodic/markov_probe.py   (cheapest test, controls)
- uv run --with sympy python experiments/overnight-arms/ergodic/markov_main.py    (component enumeration, depth-9 verify)
- cd experiments/overnight-arms/ergodic && uv run --with sympy python markov_saturate.py 1 6
- cd experiments/overnight-arms/ergodic && uv run --with sympy python markov_saturate.py 2 6
- cd experiments/overnight-arms/ergodic && uv run --with sympy python markov_saturate.py 3 6   (obligation 1)

Outputs: runs/overnight/ergodic/{main.json, saturate.json, main.log, sat3.log}.

## Spending

Local CPU only, exact rational arithmetic, no RNG, no seeds needed. Modal $0.

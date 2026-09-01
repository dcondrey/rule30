# Signed contacts, event operators, oscillation, and row toggles

Date: 2026-08-31

Status: **OPEN.  No period-two theorem was proved.**  The natural signed
left-minus-right/contact statistics and the registered bounded-below local
operator charges were falsified by exact finite certificates.  Odd-row color
toggling gives a correct OR/AND two-phase representation, but its two-step
map is exactly the already-studied `F^2` macro.

## 1. Exact quantities tested

In the reverse Gray-OR frontier, put

```text
V = 1 OR (B << 1),       q_j = (A_j,V_j).
```

Reading `q` from deep to shallow carries `(c,d)` and applies

```text
c' = c XOR (a OR b),
d' = d XOR (c OR a).
```

Thus each colored position is exactly one of 16 `(incoming carry,input
symbol)` operator tiles; the outgoing carry and emitted symbol are fixed by
the displayed equations.  The registered local feature vector consists of

```text
16 operator-tile counts
 4 aligned input-symbol counts
 8 ordered touching-color counts (00,01,10,11 in A and V)
```

and 12 one-hot endpoint incidences (terminal carry, shallow symbol, deep
symbol).  Output counts are the input-symbol counts of the successor, so their
change is already present.  This is an exact implementation of treating
color switches/contacts as events and each local pyramid event as an
operator, not a visual analogy.

The directly proposed left-minus-right statistics were also tested:

```text
ones(A)-ones(V)
boundary_count(A)-boundary_count(V)
equal_contacts(A)-equal_contacts(V)
absolute ones difference
absolute boundary-count difference
(ones+boundaries)(A)-(ones+boundaries)(V).
```

Here boundary count is the length of the exact boundary-gap/run-length list.

## 2. The smallest obstruction is an oscillation

The finite rho seed with registered origin `(length,seed,follow)=(1,0,0)`
has two consecutive accepting macrosteps

```text
(T,A,B): (2,1,1) -> (4,3,2) -> (6,5,5),
pin:                       1          1,
```

after which the next pin is zero.  On the six statistics above, the three
states have values

```text
(-1, 0,0, 1,0,-1)
( 0,-2,2, 0,2,-2)
(-1, 0,0, 1,0,-1).
```

Consequently every one of the six natural signed or absolute counts moves in
both directions.  More strongly, no function of just this six-number summary
can strictly descend on every accepting macrostep: the same summary returns
after two such steps.  This is the exact way oscillation defeats the proposed
scalar count.  It does not show that every phase-sensitive or full-word
invariant fails.

## 3. Exact local-charge obstruction

Among 16,066 distinct exact accepting transitions reached from all rho seeds
through length 16 and at most 128 forced continuations, a linear program found
a 12-type multiset of total multiplicity 36.  The solver-free verifier
reconstructs every seed and transition independently and sums its integer
feature changes.  The result is

```text
aggregate change of the 28 local counts:
(2,3,5,4, 0,3,1,0, 1,1,2,1, 1,3,8,1,
 4,10,16,6, 1,13,13,9, 5,15,15,1)

aggregate change of all 12 endpoint incidences:
(0,0,0,0, 0,0,0,0, 0,0,0,0).
```

All local changes are nonnegative and the total local gain is 144.  Suppose a
candidate in the registered normalized class were

```text
E(word) = sum_i w_i N_i(word) + endpoint_potential(word),  w_i >= 0,
```

and strictly decreased on every accepting transition.  Summing those strict
inequalities with the certificate multiplicities would give a negative
number.  Directly evaluating the right side instead gives a nonnegative
number because the endpoint terms cancel and every `w_i` is nonnegative, a
contradiction.

This proof is coefficient-independent and the transitions are exact
falsifiers, so the conclusion has no dependence on the sampled support bound.
The bound was used only to discover the finite witnesses.  Signed local
weights are covered when their bounded-below proof normalizes them into this
nonnegative edge/contact form with the registered endpoint potentials.  The
certificate does **not** exclude arbitrary signed combinations whose lower
bound relies on a more restrictive reachable sublanguage, joint endpoint
states, nonlinear full-word charges, or unbounded memory.

An additional exploratory linear program asked for a convex multiset whose
changes in all 40 features cancel exactly.  It was infeasible on the registered
transition set, so no stronger all-signed claim is made.

## 4. A rule that toggles with the row

Let `x_(t+1)=F(x_t)` and globally recode

```text
z_t(i) = x_t(i) XOR (t mod 2).
```

The recoded rule alternates exactly between

```text
phase 0: z' = 1 XOR left XOR (center OR right),
phase 1: z' = left XOR (center AND right).
```

Both formulas were checked on all 16 phase/neighborhood assignments.  Their
two-phase composition was checked on all 32 radius-two neighborhoods and is
exactly `F^2`.  A raw center trace `0101...` becomes the constant-zero recoded
center.  For the adversarial row `{-8,-1,6}`, that recoded center is zero
through time 14 and becomes one at time 15, exactly where the raw alternating
trace fails.

This does not reduce the theorem to the known constant-zero case.  A finite
`x_t` becomes a cofinite `z_t` on every odd time, whereas the constant-trace
theorem uses finite support.  Strobing every two phases removes the global
complement and returns exactly to `F^2`; hence a period-two phase-dependent
local scalar ranking would induce a ranking for the existing macro problem.

A genuinely data-dependent rule with a fixed finite controller can likewise
be absorbed into an enlarged finite transducer state.  The present four-carry
operator already self-updates according to each input symbol and generates
the previously proved order-eight dihedral action.  Allowing unbounded
history would no longer be a finite-state certificate and could merely encode
the whole trajectory, so it is not a useful theorem without a separate
well-founded invariant.

## 5. Pyramid sizes and prior results

Two meanings of pyramid size are already resolved and were not relabeled:

- maximal monochromatic block sizes are exactly the lossless run-length or
  boundary-gap digits in `RESULTS-RUNLENGTH.md`; their values and list lengths
  are unbounded, and the tested bounded summaries have opposite-next-pin
  collisions;
- causal connected-component counts were tested in
  `docs/rule30/RESULTS-followup3-ball-fission-topology.md`; the causal finite
  pyramid always has one component, while same-row fission counts fail the
  Rule 30/Rule 90 direction and are a sparsity artifact.

Full boundary-gap lists remain viable coordinates.  Only fixed local counts
and bounded projections have been retired.

## 6. Controls and commands

Commands run from `/Volumes/A/researchpapers/13-rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/divergence_search.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_divergence_negative.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/toggle_phase.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/derive_and_controls.py
```

The divergence search reported 16,066 exact accepting transitions, increases
and decreases for all six proposed signed measures, and the 12-type Farkas
multiset.  The standalone integer verifier reported 12/12 endpoint
cancellation, local gain 144, and `PASS` without SciPy.

The complete controls again passed:

- all 16 Rule 30 carry tiles;
- all 32 `F^2` neighborhoods and 64 defect assignments;
- the odd-row toggle identities on 16/16 assignments and its two-phase
  `F^2` identity on 32/32 radius-two neighborhoods;
- Rule 30 `{-8,-1,6}` through its failure at time 15;
- Rule 90 `{-1,1}` with zero center through time 128;
- all 131,071 nonzero finite rows supported in `[-8,8]` through time 64,
  reproducing maximum alternating horizon 14 and constant-zero/one horizons
  8 and 9 as bounded validations only.

The Rule 90 control fails in the intended way: no descent was obtained.  The
OR-specific toggle has an AND-dual, while the XOR carry table remains a
transitive permutation group and retains Rule 90's finite period-two
collision.

## 7. Conclusion and next theorem

The period-two same-orbit theorem and Prize Problem 1 remain open.  These
results retire the natural left-minus-right scalar counts, any arbitrary
function of their six-number summary, and the registered normalized local
event/contact charge class.  They do not retire the full run-length encoding,
phase-sensitive nonlinear invariants, or finite-seed properties of the full
cumulative boundary offsets.

The single best next theorem target remains the exact finite-seed
boundary-gap tail theorem:

> If every iterate of
> `C=I(A OR (1+zB))`, `D=I(C OR zA)` has odd `R(D)` length, then the initial
> rho boundary composition has infinitely many digits.

Here `I` is inverse Gray code and `R` is the full boundary-gap list.  This
target explicitly allows the observed short oscillations while asking why a
finite list cannot sustain them forever.  It uses Rule 30's OR, the
same-orbit relation, and finite support, and it has no fixed-width or
finite-horizon parameter.  Proving it would establish the period-two theorem
only, not all of Prize Problem 1.

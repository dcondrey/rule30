# Ordered boundary-operator cocycle: weighted-ranking result

Date: 2026-09-01

Status: **OPEN.  No period-two theorem was proved.**  The attempt produced
small exact negative certificates for the natural carry and `D8` ordered-cost
topologies.  The parity-refined topology was solver-inconclusive under the
fixed budget.

## 1. Exact Rule 30 identities retained

Write

```text
f(a,b,c) = a XOR (b OR c).
```

For `a_j = y(x+j)`, the exact radius-two rule is

```text
F^2(y)(x) = f(f(a_-2,a_-1,a_0),
             f(a_-1,a_0,a_1),
             f(a_0,a_1,a_2)).
```

Its algebraic normal form over `F_2` is

```text
a_-2 XOR a_1 XOR a_-1*a_1 XOR a_0*a_1 XOR a_2
     XOR a_-1*a_2 XOR a_0*a_2 XOR a_1*a_2
     XOR a_-1*a_1*a_2 XOR a_0*a_1*a_2.
```

Thus the same-orbit defect is

```text
d_y(x) = y(x) XOR F^2(y)(x),
```

with the preceding normal form plus `a_0`.  The trace-collision hypothesis is
exactly

```text
d_(F^t(y))(0) = 0 for every t >= 0.
```

The existing alternating-fiber reduction turns this infinite family into the
zero-emitting, pin-passing forced frontier macro used here.  These identities
were rechecked exhaustively; they are validation of recorded results, not new
claims.

## 2. What was actually tested

The OBOC proposal needs two corrections before it defines a proof language.

1. The word mechanism is a subsequential transducer, not an automorphism.  It
   need not be invertible.
2. Unbounded motion of an active boundary is not a finite-support
   contradiction, because forward Rule 30 support expands.  Drift must either
   be a bounded-below mortality rank or be mapped exactly to distinct nonzero
   cells of the fixed reconstructed initial tail `L(rho)`.

This attempt tested the first option.  A fixed deterministic observer reads
the aligned frontier symbols deep-to-shallow.  For an observer with control
states `Q`, consider every regular path cost

```text
E(w) = sum_e u_e n_e(w) + beta(q_final),       u_e >= 0.       (1)
```

Here `n_e(w)` is the ordered observer-edge count and `beta` is arbitrary.
Every energy (1) is bounded below on all finite words.  Conversely, any
weighted deterministic observer energy that is bounded below on all finite
words can be put in form (1), up to a constant, by the standard graph-potential
normalization: boundedness forbids a reachable negative cycle, and shortest
path potentials make all reduced edge weights nonnegative.

The fixed controls tested were:

- the exact four carry states;
- the exact eight prefix actions forming `D8`;
- the product `D8 x carry`, nominally 32 states;
- `D8 x (prefix-depth parity)`, 16 states.

Only the coefficients in (1) were synthesized.  The control transition maps
were exact and fixed before the search.

## 3. Exact obstruction theorem for this rank class

Suppose a finite multiset of surviving forced transitions has:

- componentwise nonnegative aggregate observer-edge-count change; and
- zero aggregate terminal-state incidence.

If every member strictly decreased (1), multiplying by the nonnegative
multiplicities and adding would give a total change at most minus the total
multiplicity.  But the two aggregate properties make the same total change
equal to a nonnegative dot product with `u`.  This is a contradiction.

`verify_oboc_negative.py` checks such multisets using only Python integer
arithmetic.

### Four-carry-state observer

The smallest discovered obstruction consists of two consecutive transitions
from the length-four seed `1010`:

```text
22230123 -> 303001213 -> 3122230123
```

The strings are canonical aligned frontier-symbol words in
deep-to-shallow order.  The aggregate edge-count gain is 2 and the terminal
incidence is zero.  Therefore no bounded-below four-carry-state cost can
strictly decrease on every surviving forced transition.

The registered rerun with seed length at most 3 and follow depth 1 was
feasible, while seed length 4 produced this two-row obstruction.  This makes
it the smallest obstruction found under that lexicographic rerun; it is not a
claim of absolute minimality among every possible encoding.

### `D8` observer

The exact obstruction has seven transition types and total multiplicity 10:

```text
1 * (length=4, seed=1010,   follow=1)
2 * (length=6, seed=101000, follow=1)
2 * (length=6, seed=101000, follow=2)
2 * (length=6, seed=101000, follow=3)
1 * (length=6, seed=101000, follow=4)
1 * (length=6, seed=101000, follow=5)
1 * (length=6, seed=101000, follow=6)
```

Its aggregate edge-count gain is 10 and its terminal incidence is zero.  It
kills every bounded-below ordered edge cost on the eight exact prefix-action
states.

The `D8 x carry` product has the same obstruction.  It is not a genuine
32-state refinement on reachable words: starting from zero carry, the carry
component is always the current `D8` permutation applied to zero.  The
solver-free checker verifies this identity on all words through length 6;
the identity itself follows immediately by induction from the definition of
prefix action.

## 4. Parity refinement

The 16-state `D8 x prefix-depth-parity` observer is **unresolved**, not
successful.  A bounded-below cost fit all sampled surviving transitions for
seed lengths at most 8 and follow depth 16.  The exact rational solver timed
out at seed lengths 9 and 10, and also on the registered length-12/depth-64
sample.  No candidate was promoted to an all-word proof, and no negative
certificate was obtained.

This fit may merely reflect additional memorization by position parity.  It
must not be extended by increasing seed length or runtime without a new exact
verification strategy.  In particular, finite feasibility is not evidence
for the theorem.

## 5. Controls

The existing exact control programs were rerun:

- the radius-two Rule 30 table passed all `32/32` neighborhoods;
- the two-orbit defect recurrence passed all `64/64` cases;
- the adversarial Rule 30 row `{-8,-1,6}` alternated through time 14 and
  failed at time 15;
- Rule 90's row `{-1,1}` retained zero center through time 128;
- the Rule 30 right-column identity passed all `8/8` local cases;
- the Rule 90 analogue of the OR-specific no-`11` implication failed at
  `(rho,q_even,q_odd)=(1,0,0)`, as required;
- the constant-fiber checks were reproduced only as bounded validation.

The OBOC search did not produce a Rule 30 impossibility proof, so it cannot
produce a false Rule 90 impossibility proof.  More importantly, its legal
language and carry rule explicitly use Rule 30's OR; they were not transferred
to Rule 90.

## 6. Interpretation

This is a useful negative, not progress to a proof of Prize Problem 1.

What survives from OBOC is the insistence on ordered processing and on an
unbounded quantity with exact semantics.  What is retired is the simplest
realization: a bounded-below additive regular cost on the carry or `D8`
prefix-action control.  The obstruction is structural—surviving finite-seed
transitions can circulate observer terminal states while gaining, rather than
losing, every nonnegative reduced edge count.

The result does **not** retire:

- a phase-sensitive certificate with an exact uniform checker;
- a non-additive or reset/stack-like ordered operator;
- a rank bounded below only on an exactly recognized finite-seed language;
- an accumulator proved to count new nonzero cells in `L(rho)`; or
- a well-founded statement retaining the full unbounded triangular form.

The contemporaneous mortality experiment records finite UNSAT results through
seed length 24 and a full-rank triangular correlation formula.  Those
numerical claims were read as recorded results and were not independently
rerun in this attempt.

## 7. Single best next theorem target

> **Linear hard-core mortality.**  Every no-`11` rho seed of length `n` fails
> a forced left pin or creates `11` within `2n+2` post-seed macrosteps.

Given the already-recorded bilateral reduction, this uniform theorem would
exclude the remaining alternating period-two center trace for every nonzero
finite initial row.  The most promising OBOC-compatible formulation is not a
free displacement vector: it is a moving-endpoint lemma for the full
triangular inverse-Gray form, with each decrease or escape tied to the fixed
left-tail zero conditions.

## 8. Reproduction

From the Rule 30 project root:

```bash
python3 experiments/rule30/p1-period2-oboc/verify_oboc_negative.py

python3 experiments/rule30/p1-period2-oboc/oboc_rank_search.py \
  --observer carry4 --max-seed 4 --max-follow 1 --timeout-seconds 60

python3 experiments/rule30/p1-period2-oboc/oboc_rank_search.py \
  --observer d8 --max-seed 6 --max-follow 6 --timeout-seconds 60

python3 experiments/rule30/p1-period2-oboc/oboc_rank_search.py \
  --observer d8-parity --max-seed 12 --max-follow 64 \
  --timeout-seconds 180

python3 experiments/rule30/p1-period2-invariant/derive_and_controls.py
python3 experiments/rule30/p1-period2-invariant/bilateral_hardcore.py
```

`oboc_rank_search.py` uses Z3 only to discover a primal cost or a dual
multiset.  `verify_oboc_negative.py` is the retained, solver-free checker for
the negative certificates.


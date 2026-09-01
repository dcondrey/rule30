# Preregistration: ordered boundary-operator cocycle for the period-two rung

Date: 2026-09-01

## Exact target

Let `F` be Rule 30 and `Tr_0(y)_t = F^t(y)_0`. Prove, uniformly for every
nonzero finite configuration `y`,

```text
Tr_0(y) != Tr_0(F^2(y)).
```

The constant center traces are already excluded. The new case is the
nonconstant alternating trace. This experiment is only about that `p = 2`
same-orbit theorem; it is not a search over larger periods.

## Semantic correction to the OBOC proposal

The exact Rule 30 construction is a subsequential word transducer, not an
automorphism of `Q x Z^k`. It may be noninvertible. Exact gap lengths also
cannot be stored in a fixed finite control state.

The contradiction required here is not merely that a wavefront coordinate
moves without bound. Every nonzero finite Rule 30 row has an expanding
forward light cone. A valid certificate must instead prove one of the
following equivalent finite-support obstructions:

1. the zero-emitting forced macro cannot be iterated forever from a state
   encoded by any finite zero-set prefix; or
2. the accumulator is proved to count or locate distinct nonzero cells in
   the fixed reconstructed initial left tail `L(rho)`.

No inferred geometric meaning will be assigned to an accumulator after the
search. Its connection to one of these statements must be an exact lemma.

## Candidate certificate class

Use the already-derived exact period-two forced macro on ordered frontier
words, read deep-to-shallow. Let `Sigma` be the four aligned frontier-bit
symbols. A candidate observer is a deterministic weighted subsequential
automaton

```text
O = (Q, q0, delta, g, b),
delta : Q x Sigma -> Q,
g     : Q x Sigma -> Z^k,
b     : Q -> Z^k.
```

It assigns an ordered word the accumulator obtained by summing the transition
increments and the terminal contribution. The finite control must be one of
these fixed, semantically derived topologies:

- the exact four carry states;
- the exact eight `D8` prefix-action states;
- their product with one previous-symbol or alternating-phase marker, with
  at most 32 reachable states.

No arbitrary growing control graph will be learned. The primary search uses
`k = 1`. A second component is allowed only if the first component exposes a
specific ambiguity and `k = 2` resolves that ambiguity without changing `Q`.

The preferred certificate is a mortality ranking `R` satisfying:

- `R` is bounded below on every exactly characterized finite-seed forced
  state;
- every legal, pin-passing application of the exact zero-emitting macro
  decreases `R` by at least one.

Because the word length changes, boundedness below must be certified by the
finite weighted control graph (equivalently, by absence of a reachable
negative cycle after a potential normalization), not observed on samples.
The decrease condition must be checked on an exact finite product of the
observer with the forced macro and its boundary conditions.

An escape-style certificate will be accepted only if an independent exact
lemma maps each certified unit of drift to a new nonzero `L_j` in the fixed
initial row. Merely tracking an active frontier position is a kill condition.

## Strong outcome

A strong outcome is a finite table and proof that:

1. exactly recognizes or over-approximates the relevant finite-seed forced
   states while excluding no actual finite seed;
2. is inductive under the exact forced macro;
3. gives a bounded-below rank that strictly decreases at every surviving
   macro, or gives the exact fixed-tail witness described above;
4. therefore rules out an infinite alternating center trace for every
   nonzero finite `y`, independently of support width and time horizon.

The table, its exhaustive checker, and the argument turning it into the
period-two theorem must all be retained.

## Kill conditions

Retire or reformulate the tested certificate topology immediately if any of
the following occurs:

- its accumulator cannot be given an exact fixed-initial-tail or mortality
  semantics;
- the exact finite-seed/reachable restriction needed for soundness cannot be
  represented by the fixed control and the certificate fails on the sound
  over-approximation;
- two words with the same complete proposed lifted summary require different
  successor summaries or different certification decisions;
- the construction simplifies to a fixed-local adjacent-pattern weight or
  another already-refuted additive ranking;
- a purported bounded-below rank has a reachable negative cycle;
- a proposed descent has a legal nondecreasing transition;
- the Rule 90 or Rule 30 controls below fail;
- `|Q|` must grow with seed length, support width, or iteration horizon;
- solver feasibility disappears when converted to exact rational/integer
  arithmetic or cannot be accompanied by an exhaustive checker.

If killed, record the smallest exact counterexample word/transition, the
structural cause, and whether the whole class or only that fixed topology is
retired.

## Mandatory controls

1. **Rule 90 negative control.** Derive Rule 90's own legal transition
   relation. Do not import Rule 30's OR-specific no-`11` language. The finite
   row `{-1, 1}` has zero center forever and must remain possible. Any generic
   certificate that excludes it is rejected.
2. **Adversarial Rule 30 prefix.** The row `{-8, -1, 6}` matches the
   alternating center trace through time 14. No certificate may reject an
   earlier legal transition; it must fail only at its actual first mismatch.
3. **Constant-trace validation.** Reproduce the known constant-zero and
   constant-one exclusions as validation only, without relabeling them as new
   results.
4. **Local exhaustiveness.** Exhaustively verify every claimed Boolean local
   identity and every row of the forced transducer table.
5. **Preregistered falsification sample.** Before attempting a proof, test
   every nonzero finite zero-set seed of length at most 12 and follow each
   surviving forced orbit for at most 64 macros. These data may falsify a
   candidate but may not support a uniform claim.

## Fixed resource limits

- fixed control: at most 32 reachable states;
- accumulator dimension: `k = 1`, conditionally `k = 2` as specified above;
- local/exact product graph: at most 4096 reachable states;
- discovery seed length: at most 12;
- discovery follow depth: at most 64 forced macros;
- per solver call: at most 10 minutes;
- total solver time for this certificate class: at most 30 minutes;
- memory: at most 2 GiB;
- exact arithmetic required for the final feasibility or infeasibility check.

No limit will be enlarged merely because the current instance is
inconclusive. State or constraint growth with width or horizon is itself a
negative result for this class.

## Why a success would be uniform

The intended proof quantifies over arbitrary-length words through a fixed
finite transducer/product graph. Boundedness and descent are reduced to exact
finite graph obligations, not to checking all rows below a chosen width or
all times below a chosen horizon. A successful certificate would therefore
apply to every finite support size. The bounded enumeration above is only a
counterexample finder and control check.


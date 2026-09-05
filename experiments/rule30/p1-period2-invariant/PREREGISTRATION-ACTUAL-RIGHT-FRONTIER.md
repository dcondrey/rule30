# Preregistration: actual-right frontier inverse system

Date: 2026-09-01

Status: **PREREGISTERED BEFORE THE CONDITIONED FRONTIER CENSUS.**

## 1. Question

The constant-tail frontier graph currently accepts every hard-core endpoint
word over states `{1,2}` avoiding `11`.  The period-two application needs
less: state `1`/`2` encodes rho bit `1`/`0`, and rho must be the even-time
column-one trace of a genuine Rule 30 right half-plane with center boundary
`0101...`.

For horizon `h`, define

```text
A_h^right = {I(e): e has length h+1, avoids 11,
                   and bits(e) belongs to the complete finite
                   alternating-center right-cone language}.
```

The primary experiment will attach `A_h^right` to the already-proved
frontier inverse system and ask whether right realizability restricts:

1. terminal-frontier count;
2. source-to-terminal distance for tails `2` and `3`; or
3. the exact `D8` path-monodromy classes reaching a terminal.

All displayed horizons are finite evidence.  This experiment cannot prove
distance divergence by extending the table.

## 2. Exact construction

- Generate all Fibonacci-many hard-core endpoint words of length `h+1`.
- Translate states by `1 -> 1`, `2 -> 0`.
- Decide each word with the existing Tseitin encoding of the complete minimal
  right light cone, not a finite forbidden-factor approximation.
- Map accepted endpoints through the exact inverse-terminal map `I`.
- Run the existing frontier BFS from `(c,...,c)`, `c in {2,3}`.
- Run an augmented BFS retaining the exact `D8` action on the newest fiber.

The augmented action update must be checked against the literal last
frontier coordinate after every edge.

## 3. Frozen finite bounds

- Enumerate conditioned terminal sets and ordinary shortest paths through
  horizon 12 if memory permits.
- Enumerate the augmented `D8` product through horizon 10, stopping earlier
  at 2 GiB or ten minutes.
- Compare SAT and direct enumeration of every minimal right light cone through
  endpoint length six.
- Check height projection of conditioned terminal sets through every computed
  horizon.

The bound may be lowered for resource safety.  It may not be raised in
response to an attractive pattern in the first output.

## 4. Controls

1. The unconditioned terminal set and distances reproduce
   `constant_tail_frontier_graph.py`.
2. Every conditioned terminal belongs to the hard-core terminal set.
3. SAT membership equals direct enumeration through length six.
4. Every projected conditioned terminal is conditioned at the lower height.
   Equality of projected and lower sets is tested separately rather than
   assumed.
5. Every reported queue survives literal queue evolution for the stated
   horizon and its endpoint passes independent right-cone SAT membership.
6. The factors `11`, `00000`, and all other already-proved minimal forbidden
   right factors are absent where their lengths apply.
7. The monodromy action maps the source tail to the literal terminal fiber.

## 5. Predeclared interpretations

Strong structural outcome:

- a proper set of `D8` classes persists after actual-right conditioning and
  is stable under height projection, or
- conditioned distance admits a uniform recursive lower bound suggested by
  an exact projection-compatible state.

Useful finite outcome:

- actual-right conditioning changes counts or distances but no stable phase
  law appears.  Retain the conditioned language as a sharper adversarial
  target, without claiming asymptotics.

Kill for the monodromy blend:

- all eight `D8` elements reach actual-right terminals with the same bounded
  phase behavior as the unconditioned target, or the action is not determined
  by the proposed augmented state.

Kill for the right-filter blend at this representation:

- `A_h^right=A_h` through the full frozen range and conditioned distances are
  identical.  This would not prove equality at all heights, but it would
  remove the measured motivation for this particular product.

Projection failure is not a mathematical counterexample to P1.  It means the
finite-prefix right language is not extension-surjective in the proposed
inverse system, so a proof must retain an additional right-boundary state.

## 6. Proof boundary

Success for the period-two theorem requires an all-height proof that the
constant source orbit never meets the infinite actual-right terminal set.
No finite distance, terminal count, missing phase, fitted recurrence, or SAT
table will be reported as that proof.

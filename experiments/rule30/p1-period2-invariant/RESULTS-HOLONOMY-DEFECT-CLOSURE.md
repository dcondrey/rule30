# Holonomy-defect closure: the hidden state is the interior queue

Date: 2026-09-01

Status: **THE ORDERED `D8` DEFECT WORD IS NOT A CLOSED DYNAMICAL STATE, EVEN
WITH AN ABSOLUTE PHASE AND ENDPOINT DATA.  A PREREGISTERED DEPTH-ONE
TWO-ENDED REPAIR FAILS AT LENGTH 13.  COMPLETE REVERSED DEPENDENCY QUEUES ARE
CLOSED.  THE PROJECTED DIAGONAL-SUPPORT LEMMA STILL HAS NO COUNTEREXAMPLE,
BUT REMAINS UNPROVED.**

The solver-free checker is `constant_tail_holonomy_defect_closure.py`.

## 1. Exact defect coordinates

For the zero-prefix scenarios

```text
W^(k)=0^k W[k:n]
```

let `A_(j,k)` be the newest endpoint-to-cut permutation at forced row `j`.
Write the eight affine permutations as

```text
A=(alpha,beta,gamma):
(h,l) -> (h+alpha,l+beta*h+gamma).
```

Their inverses are exactly

```text
(alpha,beta,gamma)^(-1)
  =(alpha,beta,gamma+alpha*beta),                    (1)
```

and define the ordered holonomy defects

```text
delta_(j,k)=A_(j,k)^(-1) o A_(j,k+1).               (2)
```

The checker verifies (1) in both composition orders.  Moreover, the ordered
defect word together with the rightmost anchor `A_(j,n)` reconstructs every
current phase exactly:

```text
A_(j,k)=A_(j,k+1) o delta_(j,k)^(-1).               (3)
```

Thus the failure of the anchored layer below is not caused by forgetting an
absolute `D8` gauge.  It says that even the complete vector of current affine
boundary maps does not determine the next vector.

## 2. Frozen closure layers

For the active suffix `k>=j`, the preregistered audit compared:

1. the ordered word of defects (2);
2. the defects plus `A_(j,n)`;
3. the anchored state plus every scenario's previous endpoint;
4. the complete reversed dependency queue in every scenario.

The successor is the exact row-`j+1` defect word after removing scenario
`k=j`.  Every retained row is load-bearing for the scale reduction: all
tail-2 survival rows and all nonfinal tail-3 survival rows with `j<n`.

On the complete discovery corpus through source length 10 the results are:

```text
hard-core word/tail cases:       748
audited transitions:             354
projected-support failures:        0

state layer              keys    transition collisions
defects                    170             11
anchored                   170             11
previous-endpoint          176              3
complete queues            198              0
```

The first bare/anchored collision is the tail-2 pair

```text
W=12122222, row 1
W=12222222, row 1.                                 (4)
```

The first collision surviving all previous-endpoint annotations is

```text
W=121212222, row 0, tail 2
W=122212222, row 0, tail 2.                         (5)
```

Both are exact replayable collisions printed by the checker.  Therefore an
ordinal rank on the bare defect word, on the gauge-anchored defect word, or
on those data plus the current endpoint boundary is not a rank on a
well-defined transition system.

## 3. The preregistered two-ended repair also fails

After (4)-(5), an exploratory discovery run through length 10 retained both
the first and last symbol of every reversed scenario queue.  It had no
collision.  This depth-one, two-ended annotation was then frozen before
testing lengths 11 and above.

It passed the complete lengths 11 and 12:

```text
word/tail cases:                 1,220
audited transitions:              610
two-ended transition collisions:    0.
```

The next complete length killed it.  At length 13, tail 3, row 0, the words

```text
U=1212221222122,
V=1221221222122                                 (6)
```

have:

- hard-core survival length three, so row zero is a required nonfinal row;
- the same current anchored defect state;
- the same first and last queue symbols in every active zero-prefix
  scenario; but
- different exact next-row defect words.

There are six collisions of the registered state among the 476 audited
length-13 transitions.  For the first collision, the successor words first
differ as

```text
U: ..., (1,0,0), (0,0,1), ...
V: ..., (1,1,1), (0,0,0), ... .                    (7)
```

The complete queues in (6) differ only in scenarios `k=0,1,2,3`.  In the
first three they differ at cut-side depths 2, 3, and 4; in the fourth they
differ at depths 1 through 4.  Their end symbols agree.  This localizes the
ambiguity strictly inside the dependency queues.

The result does not prove that every fixed-depth annotation fails.  It does
show that the first natural bounded repair merely delayed the collision from
length nine to length thirteen.

## 4. What remains valid

Complete reversed dependency queues are literal states of the already-proved
growing queue recurrence, so their coordinatewise update is uniformly
closed.  The checker observed no queue collision, as required.  This is an
algebraic fact, not a conjecture inferred from the finite census.

The audit also compares the sufficient projections literally:

```text
tail 2: (alpha,beta),
tail 3: (alpha,gamma)=A(0).
```

There was no projected diagonal-support failure in any audited transition.
For tail 3 this comparison must be made directly between adjacent phases;
`(alpha,gamma)` is not a group quotient and cannot be read by simply
projecting (2).

Thus the negative closure result does not damage the live diagonal-support
conjecture.  It changes the route to proving it: the ordered defect word is a
useful observable, but its update must be derived from the complete queue or
from a genuinely sufficient ancestry quotient.

## 5. Consequence for the ordinal proposal

Higman ordering or an ordinal valuation cannot repair nonclosure.  Before a
rank can decrease on every legal update, equal ranked states must have a
well-defined set of legal successors.  Equations (4)-(7) show that the
proposed bounded states omit data that changes the next defect word.

The viable synthesis with the proved colex theorem is therefore:

1. use the complete growing queue as the exact state;
2. use the rightmost decisive `1` from strict inherited-coordinate colex
   descent as the consumed pivot;
3. attach an ancestry interval or tree to newly appended boundary symbols;
4. prove that supporting unboundedly many replacement pivots requires
   unbounded initial queue length.

This is the event-distance target `d(r)->infinity` from
`RESULTS-RETREAT-ANCESTRY.md`, now justified as necessary by explicit defect
closure collisions.  A direct proof of projected diagonal support remains
the shorter alternative.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_holonomy_defect_closure.py \
  --max-length 10

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_holonomy_defect_closure.py \
  --first-length 11 --max-length 12

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_holonomy_defect_closure.py \
  --first-length 13 --max-length 13
```

# Query-oriented Hashlife probe for P3

## Status

**The literal Hashlife route is negative at the measured scales.**  It is an
exact center-query algorithm that does not first construct the spacetime
triangle, but its number of distinct memoized time jumps is already
superlinear for Rule 30.  This is not a P3 lower bound and does not exclude a
different reachable-state quotient.

Code: `experiments/rule30/hashlife_center_probe.py` and
`test_hashlife_center_probe.py`.

## Why this is distinct from ARM7

ARM7 constructs a completed spacetime square and then interns equal quadrants.
The present probe instead applies the standard Hashlife idea directly to row
blocks.  A level-`k` node represents `2^k` adjacent cells.  Its memoized query

```text
advance(node) = centered 2^(k-1) cells
                after 2^(k-2) Rule 30 generations
```

constructs only reachable subqueries needed by the requested time jump.  Empty
space and every repeated intermediate block are represented once.  A lone
seed at the center of a length-`4n` root therefore gives the complete central
length-`2n` block after `n` generations with one call when `n` is a power of
two; the requested center is its middle bit.

## Exact recursion

For a level-`k` block with quarters `A,B,C,D`, first advance the three
overlapping half-blocks:

```text
P = advance(AB)
Q = advance(BC)
R = advance(CD).
```

Each has run for half the requested time.  The answer is

```text
advance(ABCD) = advance(PQ) advance(QR).
```

At level two the result is the two direct local-rule evaluations on a
four-cell word.  The coordinate intervals meet exactly, so this is an
identity, not a heuristic compression.  Hash-consing is structural on child
identifiers; memoization is on the complete node identity.

The tests exhaust every four-bit base word for Rules 30, 90, and 110, compare
power-of-two center queries with an independent cell-set evolution for Rules
30 and 90 through time 128, and compare the entire returned Rule 30 block at
time 16.

## Measurements

Each row below uses a fresh arena, so the count is the standalone work for that
query rather than reuse from a previous value of `n`.

| rule | `n` | center | distinct `advance` calls | interned nonleaf nodes |
|---:|---:|---:|---:|---:|
| 90 | 256 | 0 | 33 | 36 |
| 90 | 512 | 0 | 37 | 40 |
| 90 | 1024 | 0 | 41 | 44 |
| 90 | 2048 | 0 | 45 | 48 |
| 90 | 4096 | 0 | 49 | 52 |
| 30 | 256 | 1 | 2,093 | 2,138 |
| 30 | 512 | 0 | 6,959 | 7,040 |
| 30 | 1024 | 1 | 24,377 | 24,519 |
| 30 | 2048 | 0 | 73,942 | 74,159 |
| 30 | 4096 | 1 | 174,347 | 174,676 |

The log-log fit for cache misses over these five sizes is `n^0.142` for the
Rule 90 positive control and `n^1.617` for Rule 30.  The Rule 90 count is in
fact four additional cache entries per doubling after this transient.  Rule
30 uses more memoized subqueries than `n` at every displayed size.

The statistic is representation-level work.  Hash lookup and node construction
have nonzero Turing-machine cost, so a sublinear cache-miss theorem would only
have been the start of a P3 algorithm.  The observed superlinear curve instead
fires the cheap disconfirmation: ordinary row-block identity does not merge
enough Rule 30 subproblems to approach `o(n)`.

## Relation to the other dyadic probes

The Rule 30 growth is consistent with ARM7's rising roughly `n^1.48`
spacetime-quadtree vocabulary, despite the different construction.  This is a
useful correlation: substantial exact hierarchical reuse exists, and Rule 90
shows that the implementation detects it when it closes, but equality of full
reachable row blocks retains too much information.

What remains open is a stricter center-observational quotient of these
Hashlife nodes.  It would have to merge two reachable blocks only after proving
they have the same effect on every parent context encountered by the lone-seed
query.  ARM8's arbitrary-input ROBDD is too broad; raw Hashlife identity here
is too narrow.  No such congruence or exact composition law is known.

## Reproduction

From `experiments/rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_hashlife_center_probe.py
PYTHONDONTWRITEBYTECODE=1 python3 hashlife_center_probe.py \
  --min-k 8 --max-k 12
```

No fitted exponent or finite node census in this report proves an asymptotic
claim about Rule 30.

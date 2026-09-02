# Pull-ray stabilization and the remaining crossing lemma

Date: 2026-09-01

Status: **THE STABILIZATION HALF OF THE REGISTERED PULL-RAY CLAIM IS PROVED
FOR QUEUES OF EVERY LENGTH.  THE BOTTOM-FEATURE CROSSING BOUND PASSES ITS
FROZEN HELD-OUT CORPUS BUT IS NOT PROVED.  PERIOD TWO REMAINS OPEN.**

## 1. Exact stabilization theorem

Let the initial normalized queue have length `N`.  At update time `t` its
length is `N+t`.  A retreat is a legal queue update with final input `1`,
final raw scan state `0`, and appended boundary `2`.

The raw scan table has the unique inverse

```text
g_s(1)=0  if and only if  s=3.
```

Therefore the raw scan state immediately before the final input is `3`.
The last two inherited normalized outputs are consequently `1,0`, and the
retreat boundary makes the complete successor suffix

```text
102.                                                        (1)
```

If this successor survives, its update is necessarily the already proved
pull rewrite

```text
102 -> 0021.                                                (2)
```

Its pivot is the third-last coordinate.  Thus every pull that follows a
retreat satisfies

```text
p = N+t-3,       p-t=N-3.                                  (3)
```

Every noninitial queue ending in `2` got that terminal `2` from the preceding
retreat.  Hence only a pull of an initially terminal-`2` queue can lie off
the ray (3), and it must be the first pull.  This proves registered claim
`(PR1)` for arbitrary queue length.  The proof uses four literal table
entries and no orbit bound; `pull_ray_stabilization_control()` checks them.

The pull pivots are also strictly increasing.  Pulls on (3) inherit this
from their strictly increasing times.  If the exceptional first pull is off
the ray, it occurs at time zero and has pivot at most `N-2`; a second pull
requires an intervening retreat and therefore has time at least two and
pivot at least `N-1`.  This is an all-length consequence of the same suffix
classification, not the finite minimum-delta regression.

## 2. Frozen held-out crossing result

For a pull at `(t,p)`, write `d=p-t`.  The preregistered crossing claim uses
the second pull's intercept when it exists and the sole pull's intercept
otherwise.  Its unchanged held-out run produced

```text
stored controls:                              PASS
all invariant queues of length 19:            3,015,168
new random queues at lengths 24--96:             500,000
new sparse queues at lengths 24--128:            600,000
TOTAL queues:                                  4,115,170
pull events:                                     725,242
stabilization failures:                                0
bottom-feature crossing failures:                       0
orbit-cap hits:                                         0
minimum crossing slack:                                 0.
```

The zero slack shows that the bound is sharp on the frozen corpus.  This is
finite evidence only.

## 3. Exact remaining lemma

After Section 1, the nontrivial part can be stated without origins:

> **Bottom-feature crossing lemma.**  If an orbit has at least two pulls,
> the number of pulls is at most the number of initial nonleading `1` cells
> and maximal-zero-run starts at coordinates at most `N-3`.

If there is exactly one pull, its initial pivot itself supplies the one
required feature.  Thus the displayed lemma gives the mixed retreat budget
after combining pulls with the proved one-credit retreat pairing.

This is strictly narrower than colex-origin prefix Hall.  It asks for a
noncrossing backward path from repeated visits to the single ballistic ray
`i-t=N-3` to distinct feature starts on the bottom row.  A proof would give

```text
ret(R) <= #1(R) + #zero-runs(R) <= |R|,
d(r) >= r,
```

and would close the constant-tail separator, the rank-zero separator, and
the nonconstant period-two exclusion.

No such all-length crossing proof is asserted here.

## 3a. Weaker sufficient target for the actual period-two problem

The full bottom-feature lemma is stronger than the original Rule 30
application.  Under an alternating center trace, the actual even-time
right-neighbor trace `rho` contains neither `11` nor `00000`; the second
prohibition is the uniform ANF identity proved in
`RESULTS-RIGHT-FILTERED-MORTALITY.md`.  Endpoint state `1` encodes `rho=1`
and endpoint state `2` encodes `rho=0`.

Rank descent may prepend finitely many artificial endpoint `2`s, but after
that prefix the constant-tail queue endpoint is a tail of the actual `rho`.
Consequently any genuine period-two counterexample would yield an immortal
queue whose consecutive retreats, and hence consecutive following pulls,
eventually have gaps

```text
2 <= t_(i+1)-t_i <= 5.                                  (4)
```

The lower bound is hard-core `11` avoidance; the upper bound is `00000`
avoidance.  Combining (3) and (4) gives the strictly weaker sufficient
lemma:

> **Syndetic pull-ray lemma.** No finite constant-tail queue has infinitely
> many pulls on one ray with all sufficiently late pull gaps in
> `{2,3,4,5}`.

This lemma alone would exclude a nonconstant period-two center trace, even
without proving that every abstract hard-core queue has finitely many pulls.
It remains unproved.  Fixed-factor amortized potentials do not immediately
settle it: the complete all-word pull-potential systems are already
unsatisfiable through width five, and bounded actual-right gaps still allow
the dense alternating retreat/pull transients that defeat local scalar
summaries.

## 3b. A macro-potential attempt and its exact obstruction

Because every surviving retreat is immediately followed by its pull, a
potential only needs to be nonincreasing on `B` updates and strictly decrease
across the two-update `AC` macro.  A width-two edge potential satisfying
those constraints through discovery length 12 was frozen before further
testing.

It fails all three universal obligations at lengths 13--14.  In particular,
the invariant families `211(01)^k` and `30(10)^k1` make the proposed rank
unbounded below.  Separate all-word weighted-product syntheses for each tail
are already unsatisfiable at factor widths one through five.  See
`RESULTS-MACRO-EDGE-RANK.md` for the literal solver-free counterexamples.

This does not weaken the pull-ray or retreat--pull pairing theorems.  It
rules out one more bounded scalar replacement for the ordered crossing map.

## 3c. Pull ancestry reduces global crossing to one chain

Attach every appended coordinate to its colex pivot and count pull edges on
each root path.  The third-last pivot theorem gives an exact temporal
recurrence for those depths and proves

```text
#pulls <= 2 max pull-depth.
```

Thus full noncrossing Hall is stronger than necessary.  It is enough to show
that a single root path cannot contain more pulls than the initial feature
prefix through that root.  This one-chain claim passes 4,115,168 newly
seeded held-out queues with sharp slack zero, but remains unproved.  See
`RESULTS-PULL-ANCESTRY-DEPTH.md`.

## 4. Reproduction

```bash
uv run python \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_rewrite.py \
  --max-length 18

uv run python \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_ray.py

uv run python \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_ancestry_depth.py
```

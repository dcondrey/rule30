# Mixed retreat budget and colex-origin Hall reduction

Date: 2026-09-01

Status: **THE REGISTERED MIXED BUDGET AND THE STRONGER ORIGIN-PREFIX HALL
CLAIM PASS THEIR HELD-OUT CORPORA.  THE RIGHTMOST-PIVOT DYNAMICS IS PROVED TO
HAVE ONLY THREE SUFFIX REWRITES, AND RETREATS ARE REDUCED EXACTLY TO
PRODUCTIVE PULL EVENTS.  THE PULL-ORIGIN HALL INEQUALITY IS NOT PROVED, SO
PERIOD TWO REMAINS OPEN.**

## 1. Registered finite evidence

For an invariant normalized queue `R`, define

```text
C(R) = number of nonleading 1 cells
       + number of maximal zero runs.
```

The frozen conjecture `ret(R) <= C(R)` passed:

```text
stored controls:                         PASS
all invariant queues of length 19:       3,015,168 / 0 failures
random queues at lengths 24--96:           500,000 / 0 failures
sparse queues at lengths 24--128:          600,000 / 0 failures
TOTAL:                                  4,115,170 / 0 failures
orbit-cap hits:                                  0
minimum slack among positive-retreat cases:      1.
```

This includes the length-34 counterexample to `#1+1` and the length-18
six-retreat witness.  It is finite evidence, not a proof.

The stronger registered origin statement labels every appended boundary
coordinate by the initial origin of the rightmost colex pivot it replaces.
If the sorted retreat origins are `o_1<=...<=o_r`, it asserts

```text
number of initial feature starts at positions <= o_k >= k,       (OH)
```

where a feature start is an initial `1` or the first cell of an initial zero
run.  On its independently seeded held-out corpus, `(OH)` passed the same
4,115,170 queues, comprising 2,660,018 successful updates, with no cap hit
and minimum Hall slack one.

## 2. Exact rightmost-pivot classification

The all-word colex product already proves that the rightmost inherited
difference is an input `1`.  After that pivot, every inherited coordinate
must be unchanged.  The normalized equality edges of the raw scan are

```text
raw 0: 0->0, 1->3, 2->2,
raw 1: none,
raw 2: 1->1,
raw 3: none.
```

Intersecting these eight reachable suffix states with the exact hard-core
decoder leaves only three legal finals.  Consequently every successful
nonexceptional update has one of the exact suffix rewrites

```text
A: 1       -> 02                  retreat,
B: 1       -> 21                  nonretreat,
C: 1 0^m 2 -> 0^(m+1) 2 1        nonretreat, m>=0.       (1)
```

This is an arbitrary-length regular-language theorem.  It is checked by
`constant_tail_pull_rewrite.py`, not inferred from orbit enumeration.

Call `C` a **pull**: it pulls the `1` immediately left of the terminal zero
run across that run to the new boundary.  Formula (1) gives:

1. a queue ending in `1` can only use `A` or `B`;
2. a nontrivial queue ending in `2` must use `C`;
3. after a pull, any number of `B` rewrites preserve the pull pivot's origin;
4. the next `A` retreat has exactly that origin.

Thus every retreat is either the first retreat funded by an initial terminal
`1`, or is paired with the unique preceding productive pull.  This removes
all irrelevant zero-block births from the ancestry problem.

## 3. Exact remaining lemma

It now suffices to prove the pull version of Hall:

> Sort the origins of all productive pull pivots.  For the `k`-th origin
> `p_k`, the initial prefix through `p_k` contains at least `k` feature
> starts.

The same statement for all pulls, including a final unproductive pull,
passes every invariant queue through length 14.  Consecutive pull positions
strictly increased in all 16,544 pull events in that regression, but neither
finite fact is promoted to a theorem.

The pull Hall lemma plus the possible initial terminal credit proves `(OH)`,
hence `ret(R)<=C(R)`.  Since `C(R)<=|R|`, it gives `d(r)>=r`.  A finite queue
then has finitely many retreats; the proved eventually-`2` exceptional
separator closes the constant-tail and rank-zero separators and excludes a
nonconstant period-two center trace.

## 4. Bounded-rank obstruction

An exact rational-weight synthesis shows that no additive potential built
from queue factors of widths one through four can be nonnegative, bounded by
`C`, nonincreasing on nonretreats, and drop on retreats, already on the 3,719
queues through length ten.  Adding binary origin-cutoff marks does not rescue
widths one through four on the 2,032 marked cases through length seven.

This negative is limited to the stated additive-factor certificate.  It
does not refute pull Hall; it says its proof must retain a nonlocal ordered
matching, stack, or ancestry interval.

## 5. Exact center-controlled fold identity

The mirror/reversal idea gives a separate exact necessary condition.  Let
`C_t=s(t,0)`, `L_t=s(t,-1)`, `LL_t=s(t,-2)`, and `R_t=s(t,1)`.  Under an
alternating center trace,

```text
C_t=0:  L_t=1-R_t and LL_t=R_t,
C_t=1:  L_t=1     and LL_t=R_(t+1).                 (2)
```

Hence the second-left column is a center-controlled time-reversal/fold of
the first-right column, and the two left boundary cells are complementary at
every zero phase.  This is exact local algebra, but excluding a finite left
half subject to that two-step boundary constraint remains unproved.  It is
therefore a corroborating coordinate for the pull ancestry, not a separate
period-two proof.

## 6. Reproduction

```bash
uv run --python 3.13 \
  experiments/rule30/p1-period2-invariant/constant_tail_mixed_run_budget.py

uv run --python 3.13 \
  experiments/rule30/p1-period2-invariant/constant_tail_origin_prefix_hall.py

uv run --python 3.13 \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_rewrite.py \
  --max-length 14

PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_mixed_rank_synthesis.py \
  --first-width 1 --last-width 4 --max-length 10

PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_mixed_rank_synthesis.py \
  --marked --first-width 1 --last-width 4 --max-length 7
```

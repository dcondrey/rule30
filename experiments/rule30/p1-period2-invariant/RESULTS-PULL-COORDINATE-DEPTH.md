# Pull ancestry: feature falsification and coordinate-depth bridge

Date: 2026-09-02

Status: **THE FEATURE-PREFIX DEPTH CLAIMS `(AD2)` AND `(AD3)` ARE FALSE.
A COARSER COORDINATE-DEPTH CLAIM SURVIVED 5,272,917 NEWLY AUDITED QUEUES BUT
IS NOT PROVED.  PERIOD TWO REMAINS OPEN.**

## 1. Exact counterexample to the feature budget

The invariant normalized tail-3 queue

```text
R = 30000000000000000000000000000001000000000000000000000000000000000000000000002
```

has length 77 and feature starts at coordinates `1,31,32`.  Its complete
successful event word is

```text
CBACACBACBA,
```

after which the next queue update fails.  The pull at time 8 uses initial
root 31 at old pull depth 2 and creates depth 3.  Only two registered
features occur through root 31.  Hence

```text
pull depth 3 > feature-prefix budget 2.                 (1)
```

This is a literal counterexample to `(AD2)`.  One row earlier the same
exhausted node reaches raw state `3`, so it also falsifies `(AD3)`.  The
queue avoids the exact normalized forbidden factors `20`, `22`, and `011`,
and every arrow was replayed by the raw four-state scan.

The failure was missed by the earlier exact-length-19 and random corpora
because it uses a deliberately sparse zero run of length 29 before the
second feature.  This is the same unbounded fan-out mechanism previously
identified in `RESULTS-FANOUT-GAP-ANCESTRY.md`.

The inverse triangular endpoint of this queue contains states `0` and `3`,
so it is not a hard-core endpoint-derived queue.  That observation may allow
an endpoint-restricted feature theorem, but no such theorem is claimed.

## 2. The coordinate-depth replacement

The failed feature budget discarded the interior coordinates of a zero run.
The surviving zero-prefix/scale experiment does not: it assigns one ordered
token to every source coordinate.  This suggests the geometric capacity

```text
K(r)=ceil(r/2).
```

The frozen replacement is

> A successful pull node of depth `h` and positive initial root `r` obeys
> `h<=ceil(r/2)`, equivalently `r>=2h-1`.                 `(CD)`

The first pull would consume one coordinate token, and every further pull
edge on the same ancestry chain would consume two more.  This is sharp at
the abstract witnesses `(r,h)=(1,1)` and `(3,2)`.

Combining `(CD)` with the already proved temporal recurrence gives, for an
initial queue of length `N`,

```text
#pulls <= 2 max pull-depth <= N.                        (2)
```

The retreat--pull pairing then makes retreats finite.  The established
eventual-2 separator excludes the remaining immortal suffix, so a proof of
`(CD)` would close constant-tail mortality and the nonconstant period-two
center trace.

## 3. Frozen held-out result

The independent run reported

```text
all invariant queues of length 19:       3,015,168
all <=5-feature queues through length 128: 1,937,749
new random/sparse queues through length 256: 320,000
TOTAL queues:                            5,272,917
successful updates:                      3,070,777
pulls:                                   1,058,866
maximum pull depth:                              4
coordinate-depth failures:                       0
old feature-depth failures:                       5
orbit-cap hits:                                   0
minimum coordinate slack:                        0.
```

The old feature failures are expected positive controls; the stored
length-77 word is checked separately and has coordinate slack 13 at its
depth-three pull.  The zero coordinate slack shows `(CD)` is sharp in the
held-out corpus.

This is finite evidence only.

## 4. Exact remaining lemma

The proof target is now an interval statement rather than a state count:

> Associate to every depth-`h` pull node rooted at `r` a nested interval of
> `2h-1` distinct initial coordinate tokens ending no later than `r`.

The parent forest supplies the nesting: `A/B` copy the parent at age one,
while a stabilized `C` points to the age-three node.  What is not yet proved
is that the two intervening triangular dependencies correspond to two new
ordered source tokens.  This is precisely the information retained by the
zero-prefix greedy sweep and lost by the feature projection.

A second, narrower route remains available: prove the feature or coordinate
bound only for queues obtained by reversing the inverse diagonal of a
hard-core endpoint.  Exact endpoint-derived prefixes through length 25 had
no feature-depth failure, but this is discovery data, not a theorem; rank
descent must be checked carefully before using the restriction.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_coordinate_depth.py
```

The preregistration is `PREREGISTRATION-PULL-COORDINATE-DEPTH.md`.

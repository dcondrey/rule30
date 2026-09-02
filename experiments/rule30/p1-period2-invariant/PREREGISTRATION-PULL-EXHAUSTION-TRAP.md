# Preregistration: pull exhaustion trap

Date: 2026-09-02

> **Post-registration outcome:** false.  The tail-3 queue `3001 0^62 2`
> creates its first reserve-zero child at time 3 and completes another pull
> at time 5.  The longer queue `3001 0^382 2` goes further and makes the
> coordinate reserve negative at time 8.  Thus both `(ET)` and its intended
> consequence `(CD)` are false.  The registration below is retained as the
> audit record.

## Discovery boundary

The frozen coordinate-depth claim `(CD)` gives initial root `r>0` the
regular capacity

```text
K(r)=ceil(r/2)=(r+1)//2.
```

For a current parent-forest node of root `r` and pull depth `h`, call
`K(r)-h` its reserve.  The following strengthening was observed on every
invariant queue through length 18, on the stored feature-budget
counterexample, and on 400,000 newly seeded random/sparse queues through
length 64.  Those runs are discovery data only.

Unlike the falsified feature reserve, the coordinate reserve begins with
the completely regular profile `1,1,2,2,3,3,...` on positive initial
coordinates.  This suggests isolating the first time that this reserve is
exhausted rather than trying to preserve a scalar potential at every cell.

## Frozen claim

Use the existing exact parent forest.  An `A` or `B` child copies its
parent's pull depth; a `C` child has depth one larger.  Initial positive-root
nodes have depth zero.

> **Pull exhaustion trap `(ET)`.** If a successful pull appends a
> positive-root node of reserve zero, no later successful update is a pull.

Two accompanying structural assertions will be audited but are not needed
as separate hypotheses:

1. from the first exhausted node until death, all reserve-zero nodes form a
   nonempty terminal interval; and
2. no reserve-zero inherited node has raw state `3`.

Before the first exhaustion, every reserve is positive.  A first exceptional
pull has an initial positive-coordinate parent and therefore has at least one
unit.  Every later pull has the proved raw-state-`3` third-last parent.  If
`(ET)` holds, no pull can consume an exhausted parent, so reserves never
become negative.  Consequently

```text
pull depth h at root r <= K(r),
```

which is `(CD)`.  The proved temporal recurrence then bounds the number of
pulls, the retreat--pull pairing bounds retreats, and the eventual-`2`
separator proves constant-tail mortality.  Thus `(ET)` is sufficient for
the nonconstant period-two exclusion.

## Frozen held-out gates

1. Exhaust every invariant normalized queue of length 19.
2. Enumerate adversarial first-pull queues `U 1 0^m 2` with short legal
   prefixes `U` and zero runs far longer than the discovery corpus.
3. Enumerate invariant queues with at most six feature starts at new lengths
   beyond 128.
4. Run newly seeded random and zero-heavy queues through length 512.
5. Retain the length-77 feature-budget counterexample as a positive control:
   it must violate the old feature claim while satisfying `(ET)`.

A passing run is finite evidence only.  A proof must classify the raw
suffix beginning at the first exhausted child and show, using the exact
`A/B/C` suffix rewrites, that its first subsequent attempted `C` is illegal.

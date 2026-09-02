# Hard-core-derived pull ancestry

Date: 2026-09-02

Status: **EVERY PULL ROOT IS UNIFORMLY LOCALIZED TO THE LAST THREE INITIAL
QUEUE COORDINATES.  THE RESTRICTED DEPTH BOUND HAS NO FAILURE THROUGH ALL
ENDPOINTS OF LENGTH 27 OR IN THE NEW LONG RANDOM CORPUS, BUT IS NOT PROVED.
PERIOD TWO REMAINS OPEN.**

## 1. Why the abstract counterexamples are irrelevant to this subcase

The unrestricted coordinate bound is false at

```text
3001 0^382 2.
```

Its putative current raw right-edge diagonal begins `200`.  Section 2 proves
that a hard-core endpoint capable of this time-zero pull forces the prefix
`203`.  Hence it cannot be the tail-onset queue supplied by a hard-core
endpoint in the rank-zero reduction.

For a hard-core endpoint prefix `e`, let `D(e)` be its current inverse-cone
right-edge diagonal.  The applicable initial queue is exactly

```text
normalize(reverse(D(e)), D(e)[-1]).
```

The distinction matters: `D(e)` is one current diagonal; the temporal cut
`I(e)` is formed by the last cells of all successive diagonals.

## 2. All-length root-localization theorem

Let the endpoint-derived initial queue have length `N`.  Every appended node
in its successful queue orbit has initial root in

```text
{N-3,N-2,N-1} intersect {0,...,N-1}.                 (1)
```

In particular, every pull root is at least `N-3`.

**Proof.**  The only pull that can lie off the stabilized ray is a time-zero
pull from an initially terminal-`2` queue.  In that case the final endpoint
symbol is `1`; hard-core forces the preceding endpoint symbol to be `2`.
The first three cells of the current right-edge diagonal are therefore

```text
D_0 = B(1) = 2,
D_1 = phi(2,2) = 0,
D_2 = phi(B(2),0) = phi(1,0) = 3.                  (2)
```

After the exact internal quotient `3 -> 1`, the reversed queue ends `102`.
Its time-zero pull pivot is exactly `N-3`.

An `A` or `B` child copies the old terminal node.  Every nonexceptional `C`
child has the proved third-last parent at coordinate `N+t-3`: for `t=1,2`
this is initial coordinate `N-2,N-1`, and for `t>=3` it is the node appended
at time `t-3`.  Induction now gives (1).  No orbit cutoff is used.  QED.

This theorem explains precisely why the abstract resonance is unavailable:
`3001 0^382 2` pulls first at root 3 while leaving 383 coordinates to its
right.  A hard-core-derived queue can leave at most two.

## 3. Restricted depth claim and held-out evidence

The remaining registered claim is

```text
pull depth h at root r  =>  r >= 2h-1.              (HCD)
```

Root localization does not prove `(HCD)`, but it changes its geometry from a
one-sided-root charge defeated by a remote zero run to an almost-full-width
charge.  A proof may now use the whole initial diagonal while losing only two
boundary cells.

The frozen run produced:

```text
all hard-core endpoints of length 26:  317,811
eligible tail-2/tail-3 queues:          164,944
coordinate-depth failures:                   0

new random endpoints, lengths 64--512:  14,000
eligible tail-2/tail-3 queues:            7,096
coordinate-depth failures:                   0
orbit-cap hits:                              0
```

An additional post-registration exhaustive row at length 27 checked 514,229
hard-core endpoints and 248,941 eligible queues, with zero failures and zero
cap hits.  The stored length-64 hard-core endpoint reaches depth four and
passes `(HCD)`; the abstract length-387 counterexample is rejected by the
three-cell `200 != 203` control.

These counts are finite evidence only.

## 4. Exact remaining bridge

The original proposal was to attach each pull edge on one ancestry chain to
a distinct `1,2` hard-core pair in an ordered terminal-cone strip.  This aims
at `2h<=r+1`, exactly `(HCD)`, but is stronger than mortality needs.  It also
cannot be interpreted as literal pairs in the initial endpoint:
`e=22222222` has no `12`, while its endpoint-derived queue has event word
`AC` and therefore one pull.  See `RESULTS-ENDPOINT-EVENT-BRIDGE.md`.

The weaker sufficient target is an injection into the `N` ordered
zero-prefix tokens of the initial inverse-cone strip.  It would give `h<=N`;
decorating tokens by the absolute eight-state `D8` phase would give the still
sufficient `h<=8N`.  Neither target needs disjoint endpoint pairs or a
half-density bound.

The proved root localization supplies the missing boundary alignment: the
strip begins within the last three initial diagonal cells.  What remains is
to define the common coordinate map from a pull edge to a projected
zero-prefix change and prove that a token, or token/phase pair, cannot be
reused on one ancestry chain.  This is a noncrossing spacetime-path
statement, not a scalar count.

Alternatively, it is enough to prove the actual syndetic-chain exclusion or
the existing projected diagonal-support/halving lemma.  No period-two result
is claimed here.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_hard_core_pull_depth.py
```

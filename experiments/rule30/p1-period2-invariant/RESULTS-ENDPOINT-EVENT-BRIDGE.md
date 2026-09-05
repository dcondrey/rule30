# Endpoint/event bridge and the corrected pull target

Date: 2026-09-02

Status: **ONE ALL-LENGTH EVENT IDENTITY AND ONE EXACT NEGATIVE RESULT.  THE
LITERAL INITIAL-ENDPOINT `12` CHARGE IS FALSE.  A WEAKER ORDERED-TOKEN
INJECTION WOULD STILL SUFFICE, BUT IS NOT PROVED.  PERIOD TWO REMAINS OPEN.**

## 1. Exact endpoint/event identity

For a nonsingleton endpoint-derived reversed diagonal, the queue event
alphabet has the following literal meaning:

```text
A  iff the hard-core endpoint appends 2 -> 1,
B  iff the hard-core endpoint appends 2 -> 2,
C  iff the hard-core endpoint appends 1 -> 2.          (1)
```

**Proof.**  The final cell of the reversed queue is the boundary state
`B(e)`.  On endpoint states `{1,2}`, the boundary permutation interchanges
`1` and `2`.  An `A` event is defined by a new final queue cell `2`, hence
the new endpoint is `1`; hard-core then forces the old endpoint to be `2`.
A `C` event is defined by an old final queue cell `2` and a nontrivial
queue, hence the old endpoint is `1`; hard-core forces the new endpoint to
be `2`.  The only remaining allowed transition is `2 -> 2`, which is `B`.
The singleton queue `(2,)` is the already isolated boundary-credit
exception: its transition `1 -> 2` is conventionally labelled `B`, not a
productive pull.  No orbit cutoff enters the argument.  QED.

Thus a pull is exactly a **future** endpoint transition `12`.  This explains
the event grammar—every `A` is followed by `C` while the orbit survives—but
it does not provide a finite initial resource.

## 2. Exact failure of the literal initial-pair charge

Take the hard-core endpoint

```text
e = 22222222.
```

It has no `12` factor.  Its exact current right-edge diagonal and normalized
reversed queue are

```text
D(e) = 12121212,
R    = 21212121                  (tail 2).
```

The successful event word is `AC`: it appends endpoint symbols `1,2`, and
the second event is a pull.  Therefore even the first pull cannot in general
be injected into literal `12` pairs of the *initial endpoint*.  The proposed
witness in `RESULTS-HARD-CORE-PULL-DEPTH.md` must live in the internal
inverse-cone/zero-prefix strip, not on its endpoint boundary.

This exact counterexample does not refute an internal spacetime witness.

## 3. Exact finite/infinite pull dichotomy

Consider an immortal queue in the rank-zero period-two application.  If it
has only finitely many `C` events, it eventually has no `A` events either:
every surviving `A` appends endpoint `1`, so the next hard-core endpoint must
be `2`, making the next event `C`.  Its event tail is therefore `B^omega`, and
by (1) its endpoint is eventually `2^omega`.  The proved dyadic
exceptional-family separator excludes precisely that case from the zero-ray
orbit.

Hence any remaining immortal queue must have infinitely many pulls.  The
proved parent-forest recurrence then forces one ancestry chain of unbounded
pull depth.  This combines three existing exact components without a new
finite assumption:

```text
immortal relevant queue
  -> eventually 2 endpoint, already excluded
     OR infinitely many C events
  -> one chain of unbounded pull depth.                (2)
```

## 4. The target can be weakened

The coordinate-depth inequality

```text
h <= floor((r+1)/2)                                  (HCD)
```

is much stronger than queue mortality requires.  For a fixed initial queue
of length `N`, the parent-forest theorem says infinitely many pulls force
one ancestry chain of unbounded depth.  Consequently **any** uniform finite
bound

```text
h <= f(N)                                             (3)
```

on endpoint-derived queues is enough; the sharp factor `1/2` is irrelevant.

This reveals a direct hybrid with the scale route.  A hard-core word of
length `N` already has `N` ordered zero-prefix tokens, and the projected
diagonal-support machinery records the complete ordered changes that the
failed feature and coordinate counts discarded.  It would suffice to prove:

> **Pull-token injection target.**  For one pull-ancestry chain of an
> endpoint-derived queue, assign every `C` edge injectively to a zero-prefix
> token of the initial inverse-cone strip, preserving order along the
> stabilized pull ray.

Such an injection gives `h<=N`, which with the parent-forest theorem excludes
an immortal queue.  Unlike the stronger projected-support conjecture, it
needs witnesses only for the nested pull rows; unlike `(HCD)`, it does not
need disjoint hard-core pairs or a half-density estimate.

The injection and the common coordinate map remain to be derived.  This is
a reduction, not a period-two proof.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_endpoint_event_bridge.py
```

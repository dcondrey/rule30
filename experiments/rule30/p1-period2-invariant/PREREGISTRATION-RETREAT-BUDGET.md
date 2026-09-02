# Preregistration: finite retreat-ancestry budget

Date: 2026-09-01

Status: **KILLED AFTER THE REGISTERED HELD-OUT CORPUS PASSED.**  A targeted
low-`1` search found the exact length-34 counterexample

```text
R=3000000000000000010100000010000002, tail=3.
```

It has three initial `1`s but emits boundary word `121212121112`, containing
five `2`s, before death at update 12.  Thus `5>#1(R)+1=4`.

## Observation

The proved colex lemma says that every successful normalized queue update
consumes the rightmost decisive input `1`.  Appending boundary state `2`
means emitting endpoint symbol `1`; unlike an appended boundary `1`, this
event does not replace the consumed pivot with a new rightmost `1`.

An exploratory exhaustive audit through queue length 15 found

```text
number of appended boundary-2 symbols <= initial #1 + 1.       (R)
```

The credit is necessary.  For example, tail-2 queue `20001` emits boundary
word `21121` before death: it has one initial `1` and two boundary-2 events.

## Registered claim and held-out test

Freeze (R) for every normalized invariant queue beginning with tail `2` or
`3`, ending in `{1,2}`, and avoiding `20`, `22`, and `011` under the exact
tail convention.  The inequality must hold on every finite prefix of an
orbit, whether or not the orbit has died.

Held out:

- every invariant queue at lengths 16 through 18, both tails;
- 20,000 deterministic random invariant queues per tail at lengths 24, 32,
  48, 64, and 96;
- an explicit orbit cap of 1,000 updates, with any capped orbit reported
  separately rather than treated as mortal.

Any excess over `#1+1` kills the claim.

## Consequence if proved uniformly

An immortal queue would emit boundary state `2`, equivalently endpoint
symbol `1`, only finitely many times.  Its hard-core endpoint would therefore
be eventually constant `2`.  In the rank-zero application the inverse cut is
in the reachable zero-ray orbit, and the proved dyadic exceptional-family
separator excludes every eventually-`2` hard-core endpoint in that orbit.

Thus a proof of (R) for the reachable queue class—or the stronger arbitrary
invariant-queue form registered here—would close both constant-tail fibers,
the rank-zero separator, and the nonconstant period-two center trace.

Passing the finite audit is not a proof.

## Outcome

The registered corpus itself passed: 2,404,842 queues, 1,578,729 successful
updates, no budget failures, and no orbit reaching the cap.  This comprised
every invariant queue at lengths 16--18 plus 200,000 random queues at lengths
24--96.  The later sparse-source adversary above kills the statement.

The failure does not undo strict colex descent.  It shows that one initial
`1` can acquire more than one retreat descendant, so the missing ancestry is
branching rather than an injection into the raw initial `1` positions.

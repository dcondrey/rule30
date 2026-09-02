# Retreat ancestry: a killed source budget and a weaker live distance

Date: 2026-09-01

Status: **THE RAW `#1+1` ANCESTRY BUDGET IS FALSE.  A WEAKER EVENT-DISTANCE
REDUCTION SURVIVES, BUT IS UNPROVED.  THE CONSTANT-TAIL SEPARATOR AND
PERIOD-TWO EXCLUSION REMAIN OPEN.**

## 1. Why retreat events are sufficient

In the normalized queue, a newly appended boundary state `2` is exactly an
emitted hard-core endpoint symbol `1`; boundary `1` is endpoint symbol `2`.
Call the former a **retreat event**.

If an immortal reachable queue has only finitely many retreat events, its
endpoint is eventually constant `2`.  The proved dyadic exceptional-family
separator excludes every eventually-`2` hard-core endpoint whose inverse cut
lies in the finite zero-ray orbit.  Consequently a counterexample in the
rank-zero application must have infinitely many retreat events.

This combines three uniform results:

1. the first-infinite-tail reduction supplies a finite constant-tail queue;
2. strict colex descent identifies the rightmost `1` consumed at each legal
   update; and
3. the exceptional-family separator eliminates finitely many retreats.

Thus it is enough to prove that a finite reachable queue cannot retreat
infinitely often.  This is weaker than arbitrary queue mortality: infinitely
many nonretreating updates need not be excluded by the new lemma.

## 2. Killed one-token budget

The first candidate was

```text
retreats(R) <= #1(R)+1.                              (1)
```

It passed every invariant queue through length 18 and random queues through
length 96.  The one credit is genuinely necessary: tail-2 queue `20001` has
one initial `1` and retreats twice.

A targeted enumeration by small `1`-count then found

```text
R = 3000000000000000010100000010000002,
tail = 3,
boundary word = 121212121112,
lifetime = 12,
retreats = 5,
#1(R)+1 = 4.                                        (2)
```

Equation (2) is an exact replayable counterexample to (1).  Random sampling
missed it because its three `1`s are separated by long zero spacers.

The registered held-out audit before this adversarial search contained
2,404,842 queues and 1,578,729 successful updates, with no failures and no
1,000-step capped orbit.  Those bounded facts do not rescue (1).

## 3. Live event-distance formulation

Let `d(r)` be the minimum length of an invariant finite queue whose orbit has
at least `r` retreat events.  Any immortal queue with infinitely many
retreats has fixed finite length at time zero and would force `d(r)` to stay
bounded.  Therefore

```text
d(r) -> infinity                                    (3)
```

is sufficient for the reachable constant-tail separator.

Exact arbitrary-queue enumeration through initial length 20 gives

```text
r:       1  2  3  4  5  6
d(r):    2  5  8 12 18 18.
```

The equality `d(5)=d(6)` rules out a one-retreat-per-scale or strictly
increasing-distance proof.  The length-18 six-retreat witness is

```text
tail 2: 211012110000000001
boundary word: 2121121121212
lifetime: 13.
```

Equation (3) is not proved.  Its advantage is conceptual: colex descent
provides a canonical pivot for each event, while the exact Peel lift monoid
forbids consecutive strict period doublings.  A viable proof may allow
finite branching of pivot ancestry but must show that supporting unboundedly
many retreats requires unbounded initial width.  A fixed injection into raw
`1` positions is now exactly falsified.

## 4. Reproduction

The registered budget audit and the permanent counterexample check are in:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_retreat_budget.py \
  --first-length 16 --last-length 18 --random-per-tail 20000
```

The script prints `registered claim KILLED` before running the bounded corpus.

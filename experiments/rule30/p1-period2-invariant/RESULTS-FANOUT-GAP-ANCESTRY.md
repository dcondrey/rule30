# Fan-out gaps: exact block law, failed contraction, and an uncovered retreat

Date: 2026-09-01

Status: **THE STATE-1 ZERO-BLOCK FAN-OUT LAW IS PROVED EXACTLY.  NONE OF THE
REGISTERED LOGARITHMIC GAP RANKS CONTRACTS, EVEN AFTER TWO INHERITED SCANS.
THE PREREGISTERED TWO-STEP FAN-OUT COVER OF RETREATS IS FALSE AT QUEUE LENGTH
FIVE.  FAN-OUT IS A REAL RESET MECHANISM BUT NOT THE UNIVERSAL ANCESTRY EVENT
NEEDED FOR HALVING OR `d(r)->infinity`.  PERIOD TWO REMAINS OPEN.**

The solver-free checker is `constant_tail_fanout_gaps.py`.

## 1. Lossless zero-gap coordinates

Every normalized constant-tail queue starts with a nonzero symbol.  Record
the ordered nonzero colors and, after each color, the length of the following
zero block.  This is a lossless representation; concatenating each color with
its recorded zeros is the inverse.  The checker reconstructs every audited
invariant queue exactly.

For an entry scan state `s`, repeated input zero uses

```text
g_0(0)=0,  g_1(0)=1,  g_2(0)=3,  g_3(0)=2.          (1)
```

Therefore, for every `m>=1`, the raw output on `0^m` is

```text
s=0: 0^m,       exit 0;
s=1: 1^m,       exit 1;
s=2: 3232...,   exit 3/2 according to parity;
s=3: 2323...,   exit 2/3 according to parity.      (2)
```

Together with `g_2(1)=1` and `g_1(1)=2`, equation (2) proves

```text
2,1,0^m,1  ->  1^(m+1),2                          (3)
```

on the inherited raw scan coordinates.  The script checks `m=1..64`, while
the proof for all `m` is the fixed-point table entry `g_1(0)=1`.

There is an important reachability qualification.  Equation (3) belongs to
the stronger arbitrary-queue language.  Inverting its complete diagonal
gives endpoint `2131` for `m=1`, endpoint `21213` for `m=2`, and endpoint
prefix `2120` for every `m>=3` (the inverse of diagonal prefix `1000`).
Consequently no word in this exact family is the reversed diagonal of a
hard-core endpoint.  It kills an arbitrary-queue scalar proof; it is not an
actual hard-core endpoint witness.

## 2. Logarithmic gap contraction is false

For every successful invariant-queue update containing a fan-out block, the
registered audit compared the source with the equal-length inherited output,
excluding the newly appended boundary.  It repeated the comparison after two
updates, retaining only coordinates descended from the original word.

Every proposed rank has exact non-strict examples and exact increases:

```text
                                      one update        two updates
measure                         nonstrict / increases  nonstrict / increases
max zero gap                       1653 / 668             563 / 199
total zero length                  1096 / 531             415 / 224
sum ceil(log2(m+1))                1085 / 500             460 / 244
sum next_power_of_two(m)           1110 / 599             395 / 228
descending log-gap multiset        1033 / 736             409 / 293
```

These counts come from 3,424 one-step and 1,402 two-step fan-out transitions
among all invariant queues through length 12.  The counts are finite census
data, but a single printed witness kills each universal rank.

The smallest shared one-step obstruction is already

```text
21021 -> 21110,                                      (4)
```

where every scalar gap measure remains equal.  A two-step increase occurs at

```text
2111021 -> 2110100,                                  (5)
```

where total zero length and both aggregate log capacities rise from one to
three.  Thus halving is not conjugate to a monotone scalar function of the
current zero gaps.

## 3. Fan-out does not cover all retreats

The second registered claim gave one universal boundary credit and attempted
to match every remaining retreat at time `t` injectively to a fan-out block
in scan `t` or `t-1`.

The first counterexample is the invariant tail-2 queue

```text
R=21101.                                             (6)
```

Its exact orbit is

```text
21101
212102       retreat at update 0
2110021
21212121
211021102    retreat at update 3
2121010021
death.
```

No scan in this orbit enters any zero block in state `1`.  Hence there are
two retreats, no fan-out events, and only one boundary credit.  Equation (6)
kills the temporal cover without a horizon qualification.

The complete audit through initial length 12 contains 18,785 invariant
queues plus the known length-18 six-retreat witness, 12,131 successful
updates, 4,550 retreats, 14,806 fan-out blocks, and 12 cover failures.  No
orbit reached the cap.  These totals are controls; (6) is the structural
counterexample.

## 4. Consequences for the six-route program

The discovery explains why raw `#1` counts can expand across unbounded zero
gaps, but it does not supply the missing universal reset event.  Retreats can
also arise through the complementary state-3/state-0 mechanism visible in
(6).  Accordingly:

- the deterministic halving recurrence remains a live numerical theorem,
  but its proof cannot be reduced to contraction of the registered gap ranks;
- `d(r)->infinity` remains live, but fan-out blocks alone cannot be its event
  ancestry;
- a viable ancestry state must retain the complete four-state entry phase of
  every relevant gap, or use the already exact full frontier/queue state.

This is a kill of the proposed bridge, not of lossless gap coordinates,
halving, queue mortality, or projected diagonal support.

## 5. Held-out phase-labelled repair

After the fan-out-only failure, the exact four entry phases in (2) suggested
retaining every zero block with its raw entry state.  The following stronger
event set was frozen before its held-out run:

> Give one boundary credit and injectively match each remaining retreat at
> time `t` to a distinct phase-labelled zero block in scan `t` or `t-1`.

This repair has zero failures in both the discovery corpus through length 12
and the registered held-out lengths 13--16.  The held-out totals are:

```text
invariant queues:       460,123
successful updates:     300,084
retreats:                111,996
phase-gap events:      2,089,990
matching failures:            0.
```

The stored length-18 six-retreat witness was then replayed as an external
control and also matches, bringing the script's printed totals one queue and
13 updates above the displayed held-out corpus.

This is finite evidence, not a theorem.  Its all-word form is now the live
sublemma for queue ancestry.  Because the matching graph connects a retreat
at time `t` only to events at `t-1,t`, Hall's condition reduces to interval
counts on the time line.  A proof should derive those interval inequalities
from the exact two-row scan, rather than enumerate longer queues.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_fanout_gaps.py \
  --max-length 12 --orbit-cap 128

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_fanout_gaps.py \
  --first-length 13 --max-length 16 --orbit-cap 128
```

# Phase-gap Hall reduction and zero-free epochs

Date: 2026-09-01

Status: **THE REGISTERED TEMPORAL MATCHING REDUCES EXACTLY TO ONE GLOBAL
ZERO-FREE-EPOCH LEMMA.  A FINITE PRODUCT CLASSIFIES EVERY ZERO-FREE
TWO-ROW TRANSITION, BUT IT DOES NOT YET PROVE THAT SUCH AN EPOCH OCCURS AT
MOST ONCE.  `d(r)->infinity` AND PERIOD TWO REMAIN OPEN.**

## 1. Retreat windows are disjoint

A retreat appends normalized boundary state `2`, equivalently endpoint state
`1`.  At the next update the previous endpoint is therefore `1`; hard-core
legality forbids appending endpoint `1` again.  Hence retreat times satisfy

```text
t_(i+1)-t_i >= 2.                                    (1)
```

For a retreat at time `t`, the registered phase-gap matching allows any
zero-block event at time `t-1` or `t`.  By (1), the windows

```text
{t_i-1,t_i}
```

are pairwise disjoint.  Events selected in different windows are therefore
automatically distinct; no augmenting-path argument is needed.

Call a retreat **eventless** when both queues in its window contain no zero
block.  With one universal boundary credit, the registered matching exists
if and only if

```text
number of eventless retreats <= 1.                   (2)
```

This equivalence is all-length and purely combinatorial.  The canonical
matcher in `constant_tail_phase_gap_hall.py` implements it literally.

## 2. Complete zero-free two-row classification

A normalized zero-free queue uses only symbols `{1,2}` and avoids `22`.
Take the synchronous product of:

- the four raw scan states;
- the last input symbol, enforcing `22` avoidance;
- spatial parity;
- whether a normalized scan output `0` has appeared; and
- whether the output has deviated from `2121...`.

At every possible legal decoder state, the product proves:

1. tail `3` has no successful zero-free-to-zero-free update;
2. for tail `2`, every such update has odd input length, emits endpoint `2`
   (so it is not a retreat), and its complete following queue is the unique
   alternating word

   ```text
   2121...21;
   ```

3. updating that even-length alternating word with a retreat necessarily
   introduces a normalized zero.

The product has finitely many reachable states and checks every outgoing
symbol, so this classification holds for queues of arbitrary length.  It is
not a bounded word census.

Consequently every eventless retreat is the last update of a maximal
zero-free epoch, and it creates a new zero event for the following row.

## 3. Exact remaining global lemma

The local product does not prevent the newly created zeros from disappearing
later.  A later maximal zero-free epoch could in principle form.  The exact
remaining statement behind the registered held-out match is therefore:

> Along every finite invariant queue orbit, at most one maximal zero-free
> epoch has the two successful rows needed to end in a retreat.

Equivalently, (2) holds.  The original held-out corpus through initial length
16 and the independent checker through length 12 have maximum one eventless
retreat, but this is finite evidence only.

This is substantially smaller than interval Hall inequalities: those
inequalities are automatic once (1)-(2) hold.

## 4. Why this still does not prove event-distance divergence

Even a proof of (2) would only inject retreats into phase-labelled zero
blocks, with one credit.  Zero blocks can be destroyed and recreated.  To
deduce `d(r)->infinity`, one must additionally prove that creating `r`
distinct matched zero-block events requires unbounded ancestry in the
initial queue.  The failed scalar/log-gap ranks show that current gap sizes
alone do not supply that ancestry.

Thus the queue route now has two explicit, ordered obligations:

1. prove the one-zero-free-epoch lemma above; and
2. attach a nonreusable source interval/tree to matched phase gaps and prove
   its depth or span diverges with the number of retreats.

No bounded matching or scalar gap statistic can replace the second step.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_phase_gap_hall.py \
  --max-length 12 --orbit-cap 128
```

The finite product is the proof control.  The orbit enumeration is only a
regression check of the remaining global lemma.

# Phase-gap Hall reduction and zero-free epochs

Date: 2026-09-01

Status: **THE REGISTERED PHASE-GAP COVER IS PROVED FOR QUEUES OF EVERY
LENGTH.  A FINITE PRODUCT CLASSIFIES ZERO-FREE EPOCHS AND AN EXACT REGULAR
PREIMAGE CALCULATION PROVES THAT AN EVENTLESS RETREAT MUST BE THE FIRST
RETREAT.  `d(r)->infinity` AND PERIOD TWO REMAIN OPEN.**

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

## 3. The zero-free-epoch lemma is proved

The local product identifies the dangerous predecessor language exactly.  If
`p -> q` are both zero-free and `q` retreats on its next update, then the tail
is `2` and

```text
p belongs to P = 211([12]1[12]1)*,
q belongs to (2121)+.                                  (3)
```

A literal DFA for `P`, followed by the exact sequential queue-preimage
operator intersected with the invariant queue language, has minimized
state/accepting counts

```text
P:          6 / 1,
Q^-1(P):   20 / 2,
Q^-2(P):    1 / 0.                                    (4)
```

Thus a dangerous predecessor has at most one earlier queue ancestor.  Its
immediate incoming update is nonretreating because every word of `P` ends in
boundary `1`.  Therefore the associated eventless retreat is the first
retreat of the orbit.  In particular (2) holds.

An independently constructed, unminimized nested synchronous product has 72
reachable states and two finals at depth one, then 169 reachable states and
no final at depth two.  It verifies the empty second preimage without relying
on the generic DFA minimizer.

Together with the disjoint windows in Section 1, this proves the registered
all-length phase-gap cover.  The original held-out corpus is now only a
regression control.

## 4. Why this still does not prove event-distance divergence

The proved cover injects retreats into phase-labelled zero blocks, with one
credit.  Zero blocks can be destroyed and recreated.  To deduce
`d(r)->infinity`, one must additionally prove that creating `r`
distinct matched zero-block events requires unbounded ancestry in the
initial queue.  The failed scalar/log-gap ranks show that current gap sizes
alone do not supply that ancestry.

Thus the queue route now has one explicit obligation: attach a nonreusable
source interval/tree to matched phase gaps and prove its depth or span
diverges with the number of retreats.

No bounded matching or scalar gap statistic can replace the second step.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_phase_gap_hall.py \
  --max-length 12 --orbit-cap 128

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_phase_gap_proof.py
```

The second command is the all-length proof control.  The first command's
orbit enumeration is only a regression check.

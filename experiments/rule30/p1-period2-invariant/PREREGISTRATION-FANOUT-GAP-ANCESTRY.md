# Preregistration: fan-out gaps and retreat ancestry

## Exact coordinate

For a normalized constant-tail queue, retain its lossless ternary word and
the lengths of all maximal zero blocks.  During the raw four-state scan, call
a zero block a **fan-out block** when its entry scan state is `1`.  The local
table then maps an input block `0^m` to raw output `1^m` while preserving scan
state `1`.  In particular,

```text
2,1,0^m,1 -> 1^(m+1),2
```

on the inherited scan coordinates.

The checker must derive the zero-block output formulas for all four entry
states directly from the exact lift table and verify the displayed family.

## Candidate A: logarithmic gap contraction

For every legal normalized queue update containing a fan-out block, compare
the source queue with the inherited output coordinates, excluding the newly
appended boundary symbol.  Freeze the following zero-gap measures:

```text
max gap,
total zero length,
sum ceil(log2(m+1)),
sum next_power_of_two(m),
descending lexicographic multiset of ceil(log2(m+1)).
```

Audit both one update and the coordinates inherited through two updates when
the second update is legal.  Any non-strict descent kills the corresponding
rank.  These are candidate ranks, not assumed invariants.

## Candidate B: two-step fan-out cover of retreats

A retreat is an update appending normalized boundary symbol `2`.  Give an
orbit one universal boundary credit.  Match every remaining retreat at time
`t` injectively to one fan-out block occurring at time `t` or `t-1`.

Freeze the claim that such a matching exists for every finite normalized
queue orbit.  Exhaust the invariant SFT queues through a requested initial
length and include the known length-18 six-retreat witness.  One unmatched
retreat kills this exact temporal bridge without killing more general fan-out
ancestry.

## Interpretation

Passing Candidate B would only charge retreats to fan-out events.  A proof of
`d(r)->infinity` would still have to show that a fixed initial queue cannot
create infinitely many matched fan-out events.  Passing any finite audit is
not an all-length proof.

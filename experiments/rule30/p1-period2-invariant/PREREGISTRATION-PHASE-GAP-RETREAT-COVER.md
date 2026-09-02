# Preregistration: phase-labelled gap cover of retreats

## Motivation and discovery boundary

The registered state-1 fan-out cover fails at length five: `21101` retreats
twice although none of its scans enters a zero block in state `1`.  Its second
retreat is, however, preceded by a zero block entered in another raw scan
phase.  The exact zero-block formulas show that all four entry phases are
structurally different and must not be collapsed.

No all-gap matching census has been run through the held-out range below.

## Frozen claim

Annotate every maximal zero block by its scan time, position, length, and raw
entry state in `{0,1,2,3}`.  Give an orbit one universal boundary credit.
Match every remaining retreat at time `t` injectively to one phase-labelled
zero block occurring in scan `t` or scan `t-1`.

Test every normalized invariant queue at initial lengths 13 through 16 and
the stored six-retreat witness.  A maximum matching smaller than
`retreats-1` kills this exact two-step phase-gap cover.  Do not enlarge the
time window or merge several blocks into one credit after seeing the result.

Passing is finite evidence only.  A uniform proof would still need a second
lemma showing that a fixed initial queue cannot generate infinitely many
matched phase-gap events.

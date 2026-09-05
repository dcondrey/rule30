# Preregistration: mixed one/run retreat budget

Date: 2026-09-01

## Discovery boundary

The raw bound `retreats <= #1+1` is false.  Motivated by the exact fan-out of
a state-1 scan across one arbitrarily long zero run, an exploratory audit
tested

```text
C(R) = number of nonleading symbol-1 cells
       + number of maximal zero runs.
```

It has no failure among every invariant normalized queue through initial
length 18 (2,418,104 queues total across the exact rows), but no corpus beyond
that discovery range has been tested against this precise formula.

## Frozen claim

For each constant tail `c in {2,3}` and each finite invariant queue `R`, let
`ret(R)` be the total number of boundary-2 retreat events before death.  Test

```text
ret(R) <= C(R).                                      (M)
```

The leading fixed tail symbol is excluded from the `#1` term.  A zero run is
maximal in the complete normalized queue.

## Held-out gates

1. Replay the known length-34 `#1+1` counterexample and the length-18
   six-retreat witness.
2. Exhaust every invariant queue of length 19.
3. Run 50,000 deterministic random invariant queues per tail at each length
   `24,32,48,64,96`.
4. Run a targeted sparse-word search at lengths through 128, biasing toward
   few `1`s and few long zero runs.  Report the largest exact excess
   `ret(R)-C(R)` and the smallest slack.

Any positive excess kills (M).  Passing is finite evidence only.

## Proof target if it passes

Construct an injective ancestry map from retreats to the disjoint union of
initial nonleading `1` cells and initial maximal zero runs.  The proved
phase-gap cover may be used, but a current gap may not be charged twice after
splitting or regeneration.  A proof of (M) gives `d(r)>=r`, hence finitely
many retreats for every finite queue.  Combined with the already proved
eventually-2 exceptional separator, it closes the constant-tail separator
and excludes the nonconstant period-two center trace.

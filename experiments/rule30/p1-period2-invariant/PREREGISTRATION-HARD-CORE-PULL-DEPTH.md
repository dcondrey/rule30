# Preregistration: hard-core-derived pull depth

Date: 2026-09-02

## Discovery boundary

The unrestricted coordinate-depth claim is false.  The exact invariant
queues `3001 0^382 2` and `3001 0^390 2` reach pull depths three and four
from initial root three.  Their putative raw right-edge diagonals begin
`200`, whereas a hard-core endpoint capable of a time-zero pull forces the
exact prefix `203`.  They therefore do not occur as the tail-onset queue of
a hard-core endpoint in the rank-zero reduction.

Before this registration, the restricted claim below had no failure on all
hard-core endpoint prefixes through length 25, on 100,000 random endpoints
at each of lengths 32 and 48, or on the stored actual length-64 endpoint
whose queue reaches depth four.  Those runs are discovery data only.

## Frozen construction and claim

For a finite hard-core endpoint word `e` over `{1,2}` with no factor `11`,
form the exact current right-edge diagonal `D(e)` of its inverse cone.  The
last entries of the successive diagonals, not the whole current diagonal,
form the cut `I(e)`.  Retain the word only when the newly exposed cut state
`c=D(e)[-1]` is `2` or `3`.  Reverse the current diagonal and apply the exact
`3 -> 1` internal normalization:

```text
R = normalize(reverse(D(e)), c).
```

Run the constant-tail queue cocycle in mode `c` and attach the established
parent forest.

> **Hard-core-derived coordinate depth `(HCD)`.** Every successful pull of
> depth `h` rooted at positive initial coordinate `r` satisfies
> `r>=2h-1`.

This is not an ad hoc restriction.  A hypothetical hard-core endpoint whose
inverse cut becomes constant `2` or `3` supplies exactly such a queue when
the constant tail first begins.  Proving `(HCD)` would bound pull depth,
the temporal recurrence would bound all pulls, and the retreat pairing plus
the eventual-`2` separator would prove mortality.  Thus `(HCD)` suffices for
the nonconstant period-two exclusion even though unrestricted `(CD)` is
false.

## Frozen held-out gates

1. Exhaust all hard-core endpoint words of length 26.
2. Use a new seed on random hard-core endpoints at lengths
   `64,96,128,192,256,384,512`.
3. Retain both abstract counterexamples as negative controls: their reversed
   raw diagonal prefix `200` must disagree with the forced hard-core prefix
   `203`.
4. Retain the length-64 hard-core endpoint with pull times
   `1,3,5,8,10,12` as a positive depth-four control.

Passing is finite evidence only.  A proof must lift the hard-core constraints
through the inverse-cone `3 x 3` tiles and show that the two new ordered
coordinates required by each ancestry-depth increase cannot be supplied by
the non-hard-core dyadic zero-run resonance.

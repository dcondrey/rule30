# Preregistration: retreat--pull macro edge rank

Date: 2026-09-01

Status: **FROZEN BEFORE ALL-LENGTH GRAPH ANALYSIS OR HELD-OUT TESTING.**

## Discovery boundary

The candidate below was synthesized from every invariant normalized queue of
length at most 12.  That discovery corpus contained 18,785 queues, 2,613
successful nonretreating `B` updates, and 627 surviving retreat--pull `AC`
macros.  Width one was unsatisfiable; width two was satisfiable.

No queue of length greater than 12 and no complete weighted product graph was
examined before freezing the coefficients and claims below.

## Candidate

Pad a normalized queue `R` on the left by a sentinel `L`.  All unlisted edge
weights, including every right-sentinel edge, are zero.  Define

```text
w(L,2)=54,

w(3,0)=59,  w(3,1)=55,  w(3,2)=50,
w(1,1)=-5,  w(1,2)=-9,
w(0,0)=-3,  w(0,1)=-10, w(0,2)=-14,

V(R)=sum of w(a,b) over adjacent padded edges.
```

These are three times the rational model returned by the discovery search.
The leading tail-3 edge has weight zero.  Negative internal weights are
intentional, so nonnegativity is a substantive language claim rather than a
coefficient convention.

Use the proved rightmost-pivot names

```text
A: 1       -> 02       (retreat),
B: 1       -> 21       (nonretreat),
C: 1 0^m 2 -> 0^(m+1)21  (pull).
```

Every surviving `A` successor has suffix `102` and its next update is `C`.

## Frozen claims

The primary test is an exhaustive finite weighted-product proof over words
of arbitrary length, not a longer bounded census.

1. **(MR1) Nonnegativity.**  Every invariant normalized queue satisfies
   `V(R)>=0`.
2. **(MR2) Between-macro monotonicity.**  Every successful `B` update
   `R -> R'` satisfies `V(R)>=V(R')`.
3. **(MR3) Macro contraction.**  Every successful two-update macro
   `R -A-> R' -C-> R''` satisfies

   ```text
   V(R) >= V(R'') + 3.
   ```

For each claim, the analyzer must construct the exact synchronous product of
the invariant suffix automaton and the required one- or two-row raw scans.
It must prove that no coaccessible weighted cycle is negative and that the
minimum complete accepting-path weight has the claimed lower bound.  A
finite word cutoff is not sufficient.

## Consequence if all three claims hold

At most one initial pull precedes the first retreat.  In an immortal orbit,
every retreat is followed by its forced pull, while intervening successful
updates are type `B`.  Therefore `(MR1)--(MR3)` would bound the number of
retreats by `floor(V(R_0)/3)`.

After the final retreat an immortal endpoint would be eventually `2`, which
is already excluded by the proved dyadic exceptional-family separator.
Thus the three claims would close constant-tail mortality, the rank-zero
separator, and the nonconstant period-two exclusion.

## Falsification policy

- A negative accepting path kills the corresponding claim.
- A negative coaccessible cycle kills it uniformly and must be printed with
  its literal input word and scan states.
- If a claim fails, no rescaling or post-hoc coefficient adjustment is part
  of this registration.  Any repaired candidate requires a new discovery
  boundary and preregistration.


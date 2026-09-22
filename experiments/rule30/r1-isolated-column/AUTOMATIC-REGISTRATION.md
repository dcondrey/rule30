# R1: exact automatic-model synthesis

2026-09-09. Intermediate research, not an R1 proof or kill.

The active target remains a proof or a full-diagram kill of R1. The user has
explicitly rejected an obstruction as the final deliverable. The earlier
travelling-channel and periodic-cylinder reports are intermediate records.

## Mechanism

Seek an output lookup on a fixed Rule 90 lone-seed spacetime:

    y(t,x) = g(t mod 4, x mod 14, z(t,x-R),...,z(t,x+R)).

An exact finite set of occurring local Rule 90 contexts can certify the
Rule 30 identity at every spacetime coordinate. This is an overlapping local
map on a specified automatic source diagram. It is not a predictor of a
Rule 30 neighbour from a bounded history of its centre.

The intended centre constraint fixes g on the source's symmetric windows
with source centre zero. The proposed neighbour constraint copies or complements z(t,1)
at time phase 3, with output centre zero in that phase. If all gates hold,
the Rule 90 formula z(t,1)=1 exactly at t=2^j-1 supplies a provably
aperiodic subsequence of the output's zero-set neighbour.

The first, stronger gate set quantified over every parity-supported source
row. Radii 1 through 4 were UNSAT, with checked proofs. Those results do not
exclude maps defined only on the actual Rule 90 orbit. No further radius
census in that stronger class is planned; the next gate uses exact orbit contexts.

## Exact context closure

For a nonzero source context choose an offset j carrying a one, and set
u=(t+x+j)/2, v=(t-x-j)/2. Then u,v are nonnegative and u AND v=0.
The source bit at another offset k is zero if k-j is odd; otherwise it is

    P(u+d,v-d),  d=(k-j)/2,
    P(a,b) = [a>=0 and b>=0 and (a AND b)=0].

A finite automaton reads the binary digits of u and v from low to high.
Its allowed digit pairs are 00, 01, and 10. It retains addition/borrow
carries for each offset, flags for overlapping one bits, residues modulo
28, and the current power of two modulo 28. Terminal zero padding evaluates
the predicates, including the nonnegativity condition. Reachable-state
closure, rather than a coordinate horizon, must certify completeness.
Taking all possible anchor offsets and adding all-zero contexts covers the
whole spacetime, including the exterior of the light cone.

For the exact-orbit stage, the centre and neighbour pins may also be
restricted to their actual column-pattern sets. With fixed spatial column
x and t=2n+epsilon, a feature at offset j is zero when epsilon+x+j is odd;
otherwise it is P(n+(epsilon+x+j)/2,n+(epsilon-x-j)/2). A one-input-bit
version of the carry automaton computes these sets exactly. This avoids
imposing observation pins on patterns that occur elsewhere in the source
diagram but never at the designated column. The centre's single initial
source one at t=0 is excluded from its eventual-periodicity pins.

## Gates and kill conditions

* No lookup is an R1 witness until every local identity, the centre pins,
  and the neighbour pins pass an independent exact check.
* A finite-state closure needs a complete transition table or reproducible
  enumeration plus an independently checked completeness argument.
* A timeout or state cap is an unresolved synthesis instance, not UNSAT.
* UNSAT excludes only its stated lookup class and radius. It does not prove
  R1 or exclude automatic diagrams in general.
* Any successful lookup must give an actual initial row and undergo forward
  replay with the unchanged Rule 30 truth table before being reported.
* The source Rule 90 aperiodicity is used to construct a countermodel; it is
  not an argument asserting the false Rule 90 analogue of R1.

This registration follows the stronger-class runs and the symbolic design
of the exact closure. It precedes any reported successful exact-orbit model.

## Moving-zero clock variant

The next structural variant fixes the zero-source background to the spatial
8, temporal 40 Rule 30 orbit beginning with bits `11100000` (LSB is x=0).
In the frame K=right-shift composed with F, its five states are the integers
7, 19, 123, 18, 126. Bit 7 remains zero. Thus this background has a persistent
zero on a left-moving diagonal, a candidate channel for maximal-speed
leftward propagation of a finite defect. No claim of a working channel is
made by this observation.

Use exact source contexts with T=40 and q=8. At phase 7 the background
centre is zero and its right neighbour is one, so pin the output neighbour
to the complement of the source neighbour. At phase 23 both background
bits are zero, so copying is another admissible pin. The Rule 90 pulse
times 2^n-1 visit each phase infinitely often: powers of two modulo 40
cycle through 8,16,32,24. Their gaps on either selected phase are unbounded.
The same all-time identity checks and kill conditions apply. This tests a
new background mechanism; it is not an inference from increasing a radius.

The inverse-preimage audit subsequently excluded every temporal and spatial
shift of this clock, at every radius, before the proposed SAT run. See
`clock40_preimage_collision.py` and the corresponding report. No clock-factor
SAT outcome is claimed.

## Trinomial source variant

The next source is the lone-seed Rule 150 diagram. Its centre is always one,
and its neighbour is `v_2(t+1) mod 2`, an aperiodic sequence with bounded
gaps between ones. On times `4n+3` the same sequence recurs. Unlike Rule 90,
at dyadic times it retains a seed at the centre: the local output limit can
be a finite perturbation of the periodic background. The preceding
periodic-preimage exclusion therefore does not automatically apply.

Use the exact dyadic identities

    z(2t,2x) = z(t,x),        z(2t,2x+1) = 0,
    z(2t+1,2x) = z(t,x),      z(2t+1,2x+1) = z(t,x) XOR z(t,x+1).

For any context radius at least one, each fine window is determined by a
coarse window of the same radius. Starting from the finitely many initial
seed windows and zero windows in every spatial phase, close the exact
four child maps on `(time phase, spatial phase, window)`. Every generated
state has an actual coordinate witness; conversely repeated halving of
time puts every actual context in this closure. This is a finite uniform
gate set, not a cutoff in time. Fixed-column zero patterns use only the
even-spatial child; column one uses its odd-spatial children.

The initial synthesis uses T=4, q=14, periodic centre with phase 3 zero,
and neighbour equal to either the source neighbour or its complement on
phase 3. UNSAT excludes only the specified class. A successful lookup still
requires independent exact verification, an actual initial row, the frozen
Rule 30 replay, and the unchanged Rule 90 control.

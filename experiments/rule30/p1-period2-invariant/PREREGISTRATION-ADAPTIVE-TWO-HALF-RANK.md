# Preregistration: adaptive two-half lexicographic rank

Date: 2026-09-01

## Motivation

Center-controlled reversal gives an all-word strict descent on the encoded
right half in the `1 -> 0` phase, but not in the `0 -> 1` phase.  Test whether
the left half supplies the missing primary descent exactly when the right
half increases.

## Frozen finite class

Represent the left half `A` center-to-edge in both phases.  Represent the
right half `B` center-to-edge in phase zero and edge-to-center in phase one.
Delete only the newly created characteristic-edge cell in each component
before comparing equal-length inherited words.

Search phase-dependent lexicographic products with:

- either `A` or `B` as primary component;
- either bit order `0<1` or `1<0` independently for each component and phase;
- `A` read lexicographically in both phases, so its appended edge is least
  significant;
- `B` read lexicographically in phase zero and colexicographically in phase
  one, so its appended edge is least significant in its current orientation.

Exhaust every pair of left/right half-words with the prescribed center and
outer-edge bits through length 9.  A candidate survives only if the target
phase rank is strictly smaller than the source phase rank on every `0 -> 1`
and every `1 -> 0` transition.

## Interpretation

If no candidate survives, the center-controlled reversal does not yield a
simple two-half lexicographic rank.  If a candidate survives, extend the
test and build an all-word synchronous comparison proof before using it.
The finite class is deliberately narrow; failure does not rule out a richer
boundary-annotated or ordinal product.

# Preregistration: carry-transducer contraction certificate

Date: 2026-08-31

## Exact target

Prove that every finite rho-seed under the exact Rule 30 alternating-fiber
macro map eventually fails its pin.  Equivalently, prove the requested
period-two same-orbit theorem after invoking the already-proved constant
fibers and applying `F` to swap the two alternating phases.

## Candidate certificate class

Rewrite the inverse-Gray macro map as a subsequential transducer reading the
aligned symbols `q_j=(A_j,B_(j-1))` from the deep end toward the center.  Its
state is exactly the two carry bits `(C_j,D_(j+1))`; no moment, time prefix,
support width, or raw suffix is retained.

The candidate certificate is the finite transformation monoid generated on
these four carry states by the four input symbols, together with the terminal
pin map.  Search for one of:

1. a synchronizing/contracting ideal that every finite rho-seed word enters
   under iteration and whose terminal carry is rejecting;
2. a fixed finite quotient (at most 256 states) of the transducer and the
   finite rho-seed boundary generator with an acyclic accepting subgraph; or
3. a well-founded rank on the finite monoid action, with a complete transition
   table and a proof that the emitted next word preserves the rank obligation.

The seed-language relationship must be explicit.  A statement about arbitrary
input words is not enough unless it is a valid strengthening.

## Strong outcome

A strong outcome is a fixed table, independent of word length and iteration
count, plus a human proof that every finite rho-seed accepting orbit enters a
rejecting ideal or strictly descends.  All table entries must be exhaustively
checked against the original two reverse OR/XOR sweeps.  This would prove the
alternating case uniformly, not by bounding a prefix.

## Kill conditions

Stop and record a negative for this class if:

- the input transformations form a permutation group with no synchronizing
  word or proper contracting ideal, and both terminal parities remain in each
  relevant orbit;
- closure requires adjoining a word suffix, a growing time prefix, seed
  length, or support width;
- the emitted-word iteration cannot be represented by the registered monoid
  state and exact reachable frontiers with the same registered state have
  incompatible successor obligations;
- the argument becomes the rejected claim that an alternating OR mask
  contracts every defect, a fixed-depth ladder, or a finite-prefix search.

If killed, report the complete smallest transition/group table, the exact
structural reason, and whether the class should be retired or augmented.

## Controls

- Rule 90 `{-1,1}` must remain a finite period-two collision.  The load-bearing
  transition table must contain Rule 30's OR; replacing OR by XOR must destroy
  any claimed rejecting mechanism.
- Rule 30 `{-8,-1,6}` must alternate through time 14 and fail at 15.
- Re-run the 32-entry `F^2`, 64-entry defect, and 131,071-row radius-eight
  controls before promoting a theorem.
- Exhaustively verify all `4 carry states x 4 input symbols`, all terminal
  states, and the full generated monoid.  Cross-check the word transducer on
  every legal `(A,B)` frontier through `T=8`.
- Reachable finite-seed tests use the already-registered seed bound 16 and 128
  follow steps only as falsifiers, never as evidence for a universal claim.

## Resource limits

- standard-library local CPU only; no agents, SAT grids, GPU, Modal, or paid
  calls;
- at most 256 monoid/quotient states, seed length at most 16, follow at most
  128, under 15 minutes and 2 GiB per command;
- do not enlarge the table or add suffix memory after a kill condition fires.

## Why success would be uniform

The carry set, input alphabet, generated monoid, seed-boundary generator, and
terminal map are finite and independent of spatial length.  A proved ideal,
acyclic accepting quotient, or rank would therefore apply to every finite
word and arbitrarily many macrosteps.  Seed enumeration is only a check of the
symbolic certificate, not part of its soundness.

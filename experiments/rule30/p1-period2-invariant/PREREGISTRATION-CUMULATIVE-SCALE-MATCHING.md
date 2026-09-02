# Preregistration: cumulative-intervention scale matching

## Motivation

Independent one-source interventions fail on
`W=122212222222221212122`: six source-2 positions are invisible throughout
the 12-step survival prefix, leaving only ten real neighbors and one contact
credit for twelve steps.  This can be cancellation in a nonlinear Boolean
map rather than absence of ordered ancestry.

Replace the pointwise Boolean derivative by a telescoping path.  Enumerate the
state-2 source coordinates either left-to-right or right-to-left.  Starting
at `W`, successively change those state 2 symbols to state 1.  The column for
source token `k` is the difference between the exact affine boundary/forced
trajectories immediately before and immediately after the `k`th cumulative
change.

A survival step is adjacent to token `k` when either the affine triple or the
forced endpoint symbol changes at that step.  Add the same universal credits:
one iff tail 2 contains `22`, and three for tail 3.  Test ordinary and
order-preserving covering matchings.

## Frozen gates

1. Immediate adversarial gate on `122212222222221212122`, tail 2.
2. If at least one direction covers the adversary, exhaustive hard-core words
   through length 16 plus the length-17 repair witness.
3. A surviving direction is then checked exhaustively on lengths 17 through
   22 using the bit-sliced implementation or an exactly cross-checked
   equivalent.

Both spatial orders are registered before the adversarial result.  No custom
order may be synthesized after a failure.

## Interpretation

Failure of both directions on the immediate gate kills cumulative
single-symbol telescoping as the missing certificate.  Success is finite
evidence only; a proof would still require a uniform telescoping/noncrossing
argument.  This experiment does not revive the already-falsified independent
derivative or rank claims.

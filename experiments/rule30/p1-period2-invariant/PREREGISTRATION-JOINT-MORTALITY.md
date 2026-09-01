# Preregistration: joint left-finite/right-realizable mortality

Date: 2026-09-01

This registration follows a preliminary exact signal: after the two-factor
filter (`11`, `00000`) failed at seed length 30, coupling the forced left
frontier to an actual Rule 30 right light cone was UNSAT at horizon eight for
seed lengths through 20.  Those preliminary instances are not held-out
evidence and cannot establish the statement below.

## Candidate theorem

Let `rho_0,...,rho_(n+7)` be the even-time column-one trace of a genuine Rule
30 right half-plane whose center column is `0101...`.  Reconstruct the first
`2n` cells of the initial left half from `rho_0,...,rho_(n-1)`, and suppose
all later reconstructed cells are zero.  Prove that the next eight forced
macros cannot all pass their center pins.

Equivalently: a configuration whose initial row is zero strictly left of
position `-2n` cannot have center trace `0101...` through the additional
sixteen time steps `2n+1,...,2n+16`.

This statement is stronger than needed for a finite configuration because it
allows an arbitrary infinite initial right half.  A uniform proof would
exclude the remaining period-two trace, but would settle only the `p=2` rung
of Prize Problem 1.

## Candidate proof languages

1. A bounded-gap theorem for the reconstructed left tail, proved for actual
   right traces by a finite family of indexed Boolean identities.
2. A layer-peeling induction on the coupled left-reconstruction/right-cone
   triangle, with a finite independently checked boundary table.
3. A parameterized resolution or Boolean-ideal certificate whose variable
   indices are affine in `n` and whose expansion is checked independently.

A finite list of forbidden right factors is admissible only if it is proved
complete for this intersection.  Adding successively longer factors after
each counterexample is a falsifier, not a proof.

## Falsification and extraction

- Check the exact joint CNF at horizon eight through `n=31`, including decoded
  and integer-replayed SAT models if any occur.
- For the finite-type approximations using all exact minimal forbidden right
  factors through lengths 18 and 24, extract the first surviving words and
  identify their first genuinely unrealizable factors.
- Do not extend the width sweep merely to accumulate more UNSAT instances.
- Reject the constant-eight candidate immediately if any exact joint model is
  SAT.

## Success criterion

Success requires a human-readable arbitrary-`n` argument, a finite verifier
for every local case or indexed identity, and an explicit deduction from the
left-finite alternating fiber to the period-two same-orbit theorem.  Finite
UNSAT, projected-language enumeration, and an observed moving family are not
success.

## Controls

- The Rule 30 row `{-8,-1,6}` must retain its alternating center through time
  14 and fail first at 15.
- The infinite-left period-seven wallpaper must remain outside the theorem's
  left-finite hypothesis.
- Rule 90's finite row `{-1,1}` must retain its constant-zero center.
- Dropping either the deep-left zero constraints or the actual-right coupling
  must leave satisfiable controls.

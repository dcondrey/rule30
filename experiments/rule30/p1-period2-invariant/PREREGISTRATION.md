# Preregistration: period-two same-orbit invariant

Date: 2026-08-31

## Exact target

Let `F` be Rule 30 and `Tr_0(y)_t = F^t(y)_0`.  Prove that every
nonzero finitely supported configuration `y` satisfies

```text
Tr_0(y) != Tr_0(F^2(y)).
```

The already-proved constant-zero and constant-one fibers are validation
cases only.  After those cases, it is enough to exclude the two alternating
traces; applying `F` swaps their phases, so the proof search may fix
`c_t = t mod 2` without loss of generality.

## Candidate certificate class

The primary class is a **fixed-locality additive ranking for the exact
alternating-fiber frontier map**, rewritten in two-step macrotime using the
radius-two rule `G = F^2`.

The frontier is the pair of growing anti-diagonals `(A,B)` already defined in
`RESULTS-alt-trace-fiber.md`.  A candidate potential has the form

```text
Phi(A,B,phase) = endpoint_term + sum_j w(local word around (A_j,B_{j-1})),
```

where the alphabet, phase set, local word radius, integer weights, and
endpoint state are fixed independently of seed length, left depth, support
width, and time.  The search will use local words of radius at most 4,
integer weights in `[-8,8]`, and at most 64 endpoint states.  The desired
certificate is a locally checkable telescoping inequality or forbidden
transition showing that an orbit emitted from a finite seed cannot satisfy
every forced-zero output and every alternating pin-parity check forever.

A secondary form, attempted only if the additive class exposes an exact
finite quotient, is a deterministic spatial transducer with at most 256
states and a well-founded rank on its non-failure states.  Its transition
table must be exhaustive and independent of spatial depth.  A raw suffix,
time window, support-width state, or frontier stored verbatim is not in the
class.

This deliberately builds on, and does not relabel, the existing facts that
the raw frontier grows, post-knee evolution is deterministic, and each pinned
step is one parity check.  The search is for a uniform quotient or local
ranking of that map, not another list of `Claim(d)` certificates.

## Strong outcome

A strong outcome consists of all of the following:

1. the exact Boolean radius-two rule for `G`, exhaustively checked on all 32
   radius-two neighborhoods;
2. a fixed finite table or fixed-locality potential whose local obligations
   are exhaustively checked over every relevant Boolean neighborhood;
3. a human proof that the local obligations telescope/induct for arbitrary
   frontier length and force either a pin failure or a one at unbounded
   initial left depth;
4. hence no finite row has an exactly alternating center trace, and together
   with the existing constant-fiber theorems, no nonzero finite row has
   `Tr_0(y) = Tr_0(F^2(y))`;
5. no tested support bound or time horizon occurs in the proof.

## Kill conditions

Stop and record a negative for this certificate class if any of these occurs:

- a smallest exact reachable transition violates the proposed inequality;
- the feature/rank state must grow with frontier length, support width, left
  depth, or time horizon;
- a non-failure cycle is reachable from finite seeds in the proposed fixed
  quotient and cannot be proved to require an infinite spatial tail;
- the proof reduces to fixed-depth half-plane emptiness, bounded-window
  prediction, the run-of-ones wedge, support-width descent, or a longer finite
  prefix;
- the same reasoning excludes the Rule 90 control without a step using Rule
  30's OR nonlinearity;
- the adversarial Rule 30 row `{-8,-1,6}` is rejected before its center trace
  actually ceases to alternate;
- synthesis needs more than 256 states, local radius 4, or coefficients of
  absolute value greater than 8.  Such growth is recorded rather than pursued.

If killed, report the lexicographically smallest/shortest exact counterexample
transition or seed, the failed local obligation, and whether to reformulate or
retire the class.

## Mandatory controls

- **Rule 90 negative control:** the finite row `{-1,1}` has zero center
  forever and therefore satisfies the period-two same-orbit trace equality.
  The complete theorem pipeline must retain it.  The intended separation is
  Rule 30's OR-dependent constant-zero exclusion and OR-dependent macro/local
  identities, not left permutivity.
- **Adversarial Rule 30 prefix:** `{-8,-1,6}` must agree with the alternating
  word through time 14 and fail at its recorded next step.  No candidate may
  infer failure from the preceding prefix.
- **Validation only:** reproduce the known Rule 30 exclusions of constant-zero
  and constant-one traces; do not claim them as new.
- **Local exhaustiveness:** enumerate all Boolean assignments for every local
  identity or inequality used in a proof.  The cap is `2^20` assignments per
  local lemma.
- **Global falsification:** before proof work on a surviving invariant,
  exhaustively test all `2^17-1 = 131071` nonzero rows supported in `[-8,8]`,
  through 64 Rule 30 steps.  This preregistered bound includes the adversarial
  row.  Run the analogous Rule 90 control at least on every row in `[-4,4]`.

## Resource limits

- local CPU only; no Modal, GPU, paid model calls, or additional writing
  agents;
- at most 15 minutes wall time for any single synthesis command and at most
  60 minutes total synthesis/search time;
- at most 2 GiB resident memory;
- additive locality radius at most 4, weights in `[-8,8]`, at most 64 endpoint
  states;
- secondary transducer at most 256 states;
- no SAT/SMT spacetime grid beyond 64 time steps or support radius 8;
- no enlargement after a kill condition fires.

## Why a success would be uniform

The certificate template scans an arbitrarily long frontier with a fixed
local rule/table and proves a symbolic telescoping or induction statement for
every length.  Seed length affects only the number of applications, not the
state space, coefficients, locality, or proof obligations.  Thus a successful
certificate would quantify over all finite supports and the entire infinite
trace, unlike a finite-horizon exclusion or the existing per-depth ladder.

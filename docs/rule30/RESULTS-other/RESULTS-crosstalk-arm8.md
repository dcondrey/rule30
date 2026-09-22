# Crosstalk ARM8 bounded run

## Outcome

No query-specific single-seed algebra survived.  The headless orchestration
ended with `VerificationFailed`, an empty final synthesis, and no objectively
verified claim.

Bundle: `runs/rule30-arm8`

- two generations of three proposals;
- one deterministic structural-duplicate rejection and five critic-score
  rejections;
- zero native candidates retained;
- integrity `PASS`, verification coverage 0%, scientific release
  `NOT ESTABLISHED`.

The new release guard rendered the model output as **Unverified synthesis** and
printed its blockers.  Unlike the ARM7 run, no unsupported family-wide
conclusion was presented as the answer.

## Candidate families

Generation 1 proposed right-boundary or right-spine strips.  Their states or
doubling steps retained `Theta(n)` cells/iterations.  Restricting the words
"causal frontier" to `O(log n)` entries did not make those entries sufficient
to reconstruct the center.

Generation 2 proposed transfer monoids over small GF(2) vector or polynomial
spaces.  Each omitted the load-bearing nonlinear map:

- an affine frontier candidate named `f(v_a,v_b)` and `update(v_a,v_b)` without
  defining them;
- an irreducible-polynomial candidate named a seam correction `delta` without
  deriving it;
- a truncated-polynomial candidate did provide executable pseudocode.

## Objective falsification

`experiments/rule30/transfer_monoid_probe.py` preserves the executable
truncated-polynomial candidate:

```text
state = (p in GF(2)[x]/(x^k), parity bit q)
double: p <- p^2 mod x^k
        q <- q XOR parity(p AND alpha_k)
```

Its submitted `alpha_k`, odd-step update, and binary composition were copied
without repair and compared with the independent bit-parallel oracle.

```text
first_mismatch=5 candidate=0 oracle=1
```

The candidate is therefore false.  The two unit tests for the probe pass.

## Boundary

This run exhausts the six sampled model proposals, not the set of all
single-seed query algebras.  It does establish a practical stopping rule for
the current use of Crosstalk: more model generations at this abstraction are
likely to rename the missing nonlinear seam operation.  Further work should
begin with a mathematically derived seam identity or a new measurement, then
use Crosstalk to criticize that concrete object—not generate a larger volume of
unconstrained candidates.

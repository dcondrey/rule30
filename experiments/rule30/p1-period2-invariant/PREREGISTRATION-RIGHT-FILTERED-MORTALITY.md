# Preregistration: right-filtered constant mortality

Date: 2026-09-01

This registration follows a preliminary exact light-cone observation: actual
right realizability forbids `rho` factor `00000`, in addition to the recorded
`11` prohibition.  Preliminary enumeration and SAT suggested, but did not
prove, the constant below.  The registration fixes the subsequent
parameterized proof search; the preliminary bounds are not treated as held-
out evidence.

## Candidate theorem

Let a finite rho seed and every bit in its forced zero-emitting continuation
avoid both factors

```text
11, 00000.
```

Prove that the continuation fails a pin or one of those two factor checks in
at most eight accepted macros.  Equivalently, the CNF for nine accepted
macros is UNSAT for every seed length `n`.

The right-column light-cone lemma makes `00000` impossible in every genuine
alternating-center Rule 30 spacetime.  Therefore constant mortality would
exclude the remaining period-two trace.  It would prove only the `p=2` rung,
not arbitrary-period P1.

## Candidate proof language

Use one of the following exact all-width forms:

1. a finite set of length-independent Boolean-ideal rewrite schemata in the
   quotient by the translated `11` and `00000` generators;
2. a complete automaton on the full active-core transducer with a proved
   bounded defect stack, not a sampled D8 quotient; or
3. a symbolic resolution/induction schema whose variable indices are affine
   in `n` and whose side clauses are independently checkable.

The proof may use the exact deep-zero/core conjugacy and matched-extension
identity.  It may not infer uniformity from a family of finite SAT proofs.

## Fixed falsification and extraction

- Check every legal seed through length 24 by direct integer replay.
- Query exact SAT at horizon nine for `n=10,16,22,24,25`; do not extend beyond
  `n=25` merely to accumulate UNSAT instances.
- Compute symbolic right-column ANFs for the five-zero lemma and verify the
  zero product independently over all 512 light-cone assignments.
- For a proposed schema, expand every indexed identity through `n=18` and
  verify it with a standalone checker that does not import the generator.

Resource limit for new synthesis: ten minutes and 2 GiB.  Existing
preliminary computations do not count as a proof and are not a reason to
raise the limit.

## Success criterion

Success requires:

- a human-readable proof for arbitrary seed length;
- a finite independently checked table or indexed algebraic identity for
  every local case;
- an explicit deduction from actual right realizability plus finite-left
  support to the period-two same-orbit theorem; and
- preservation of the infinite-left period-seven wallpaper control.

## Kill conditions

- Any legal seed survives nine macros.
- A proposed finite state has the same complete summary but incompatible
  successors, or its abstract graph has a reachable accepted cycle.
- Polynomial degree or support grows with `n` without a proved translated
  constructor.
- The certificate excludes the period-seven infinite-left wallpaper, uses a
  finite tested `n` as induction, or transfers unchanged to Rule 90.

A counterexample kills only the constant-eight bound.  It does not refute
linear mortality, reconstructed-tail density, or the period-two theorem.

## Controls

- Rule 30 row `{-8,-1,6}` alternates through time 14 and fails at 15.
- Rule 90 row `{-1,1}` retains its zero center through time 128.
- The right-column `no 11` identity passes all eight local assignments.
- The five-zero ANF identity and the independent 512-row truth table agree.
- The length-four left seed `0xa` retains its four accepted post-knee macros.

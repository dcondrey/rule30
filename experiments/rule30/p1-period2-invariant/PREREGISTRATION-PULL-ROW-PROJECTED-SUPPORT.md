# Preregistration: pull-row projected support

Date: 2026-09-02

## Target and motivation

Let `W` be a hard-core endpoint block of length `n`, let `c` be constant cut
tail `2` or `3`, and run the exact forced scale extension.  Let `A_(j,k)` be
the newest affine boundary map at extension row `j` in the zero-prefix
scenario `W^(k)=0^k W[k:]`.  Use projections

```text
pi_2(alpha,beta,gamma)=(alpha,beta),
pi_3(alpha,beta,gamma)=(alpha,gamma).
```

Call row `j` a pull row when the original forced endpoint makes transition
`1 -> 2`, equivalently queue event `C`.  The registered claim is:

> **Pull-row projected support (PRS).**  At every nonfinal surviving pull
> row `j`, some token `k` with `j<=k<n` satisfies
> `pi_c(A_(j,k)) != pi_c(A_(j,k+1))`.

This is strictly weaker than projected diagonal support, which asks for the
same conclusion on every required survival row.

## Why PRS suffices

In an immortal relevant queue, finitely many pulls imply an eventually-`2`
endpoint, already excluded by the dyadic exceptional-family separator.
Otherwise there are infinitely many pull rows.  For a fixed scale block of
length `n`, one then has a nonfinal pull row `j>=n`, but no token can satisfy
`j<=k<n`, contradicting PRS.  Thus PRS closes the rank-zero separator and the
nonconstant period-two rung.

This implication is conditional on the existing exact scale-block reduction,
endpoint/event bridge, and eventually-`2` separator.  It does not claim P1
for other periods.

## Frozen exploratory questions

The audit will record, separately from PRS:

1. whether the diagonal token `k=j` itself always witnesses a pull row when
   `j<n`;
2. the maximum displacement `k-j` of the first witnessing token;
3. the smallest exact counterexample to either claim.

Failure of the diagonal-token strengthening does not refute PRS.  A PRS
failure is a hard-core word, tail, nonfinal pull row, and complete adjacent
projection row with no witness at or to the right of the diagonal.

## Domain, controls, and evidence

- Domain: exact hard-core words; no arbitrary normalized queues.
- State: the complete bit-sliced zero-prefix scenario family and exact affine
  boundary maps.  No bounded defect quotient is used.
- Positive controls: compare the bit-sliced states with the existing slow
  exact implementation through short lengths.
- Semantic control: verify `C <=> 1 -> 2` on every counted nonsingleton row.
- Initial exhaustive range: every hard-core word through length 23 in both
  tail modes, reusing the validated projected-support implementation.
- Held-out phase: only if a new strengthening survives discovery; freeze new
  bounds before testing additional lengths or random words.

Any finite pass is evidence only.  Success requires an all-length proof of
PRS from the exact triangular recurrence.  If PRS passes, the next action is
symbolic simplification of the pull-row condition, not a larger census.

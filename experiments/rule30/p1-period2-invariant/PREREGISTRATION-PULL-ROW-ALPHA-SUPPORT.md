# Preregistration: pull-row alpha support

Date: 2026-09-02

## Discovery result

The registered pull-row projected-support audit was decomposed into affine
coordinates on every hard-core word through length 18.  Across 2,641
nonfinal pull rows, the `alpha` coordinate alone always had an adjacent
zero-prefix change at some token `k>=j`.  The secondary coordinate already
had two misses, so the observed statement is specifically about `alpha`, not
an accidental duplicate of both projected coordinates.

The stronger claim that token `k=j` always works is already false at length
6: tail `3`, `W=122221`, row `0`, has projected witnesses only at
`k=2,4,5`.

## Frozen claim

With the notation and domain of
`PREREGISTRATION-PULL-ROW-PROJECTED-SUPPORT.md`, write `alpha_(j,k)` for the
high-bit translation coordinate of `A_(j,k)`.

> **Pull-row alpha support (PAS).**  Every nonfinal surviving pull row `j`
> has some `k` with `j<=k<n` such that
> `alpha_(j,k) != alpha_(j,k+1)`.

PAS implies pull-row projected support in both tail modes and therefore, via
the exact finite/infinite pull dichotomy, closes the rank-zero separator and
the nonconstant period-two rung.

## Why alpha is structurally relevant

For constant high cut bit, the forced endpoint high bit is `1+alpha`.
Consequently a pull transition `1 -> 2` is exactly an original-scenario
temporal transition `alpha:1 -> 0`.  PAS asks whether that temporal loss of
high-bit translation must be supplied by a spatial zero-prefix finite
difference on or to the right of the row diagonal.

## Held-out test and kill condition

- Frozen held-out range: every hard-core word at lengths 19 through 23, both
  tails.
- State: the complete bit-sliced zero-prefix scenario family; no bounded
  holonomy or derivative quotient.
- Positive controls: original endpoint survival agrees with the independent
  exact scale implementation; the full selected projection is checked in
  parallel.
- Kill certificate: the first hard-core `W`, tail, nonfinal pull row `j`, and
  complete `alpha` adjacent-difference set having no token `k>=j`.

A held-out pass is finite evidence only.  No further horizon sweep is
licensed by a pass; the next action must derive PAS from the triangular
activity-parity recurrence or find a symbolic counterfamily.

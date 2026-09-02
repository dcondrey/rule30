# Preregistration: diagonal late-pull source defect

Date: 2026-09-02

Status: frozen before the single-coordinate relaxation search.

## Motivation and target

The three-row diagonal late-pull formulas remain UNSAT when the source is an
arbitrary word over `{1,2}`; source no-`11` is unnecessary.  They become SAT
when all four source states are allowed.  Seek a backwards defect-path
statement:

> A hard-core late pull under the required constant-cut history forces an
> equality state `0` or `3` at a source coordinate.

The UNSAT formula already says some source defect is necessary.  The useful
new question is whether one relaxed coordinate suffices and, if so, whether
its position follows a fixed affine/periodic rule in `(n,c,r)`.

## Frozen audit

For `2<=n<=20`, both tails, and all three residues, relax exactly one source
coordinate at a time from `{1,2}` to `{0,1,2,3}`.  Record every coordinate
that makes the formula SAT and replay each first model in the literal
triangle.  Also solve the fully binary and fully relaxed controls.

Success requires a position/phase rule that can be verified from the local
`cone_local` table and followed backwards for arbitrary `n`.  Multiple
irregular coordinates, instances needing two or more defects, or growth
without a stable recurrence is a negative result for the single-path route.


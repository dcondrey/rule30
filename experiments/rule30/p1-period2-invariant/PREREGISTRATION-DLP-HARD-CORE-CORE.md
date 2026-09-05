# Preregistration: late-pull hard-core assumption cores

Date: 2026-09-02

Status: frozen after exploratory lengths `n<=11` and before the held-out
range `12<=n<=20`.

## Question

The exact late-pull CNF uses two distinct nonlinear restrictions:

1. every source symbol belongs to `{1,2}`;
2. the forced endpoint continuation contains no adjacent `11`.

Drop condition 2, then add each continuation no-`11` clause behind a
separate assumption literal.  For every `(n,c,r)`, extract and
deletion-minimize an UNSAT assumption core.

The exploratory range through `n=11` found only two formulas whose
no-hard-core relaxation is SAT:

```text
n=5, tail=3, r=1: a singleton no-11 clause suffices;
n=6, tail=2, r=1: a singleton no-11 clause suffices.
```

The singleton is not unique, so its solver-selected position is not part of
the frozen claim.

Every other exploratory formula was UNSAT without any continuation
hard-core clause.

## Held-out test and interpretation

Run all six formulas for every `12<=n<=20`.

- If every held-out core is empty, retain the candidate that the binary
  source and full constant-cut history alone exclude DLP after finitely many
  explicit small exceptions.
- If nonempty cores recur but have uniformly bounded size or a fixed
  boundary-relative position, retain that precise pattern as a possible
  finite repair.
- If core sizes or positions proliferate, reject this simplification and
  keep the complete hard-core continuation in the theorem.

An empty core is an exact finite UNSAT result, not an all-length proof.  A
stable finite pattern is evidence for a new induction target only after its
transition closure is proved for arbitrary `n`.

## Controls

For every nonempty core:

1. the relaxed formula with no assumptions must be SAT;
2. the minimized assumptions must be UNSAT;
3. deleting any one minimized assumption must make the formula SAT; and
4. the SAT relaxed model must replay as a literal late pull and contain a
   forbidden `11` continuation pair.

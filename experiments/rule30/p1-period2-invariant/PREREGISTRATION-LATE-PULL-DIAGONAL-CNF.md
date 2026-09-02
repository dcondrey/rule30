# Preregistration: three-row late-pull diagonal CNF

Date: 2026-09-02

Status: frozen before building or solving the CNF family.

## Reduced target

The late-pull horizon can be weakened further.  It is enough to prove, for
every binary source word `W` of length `n` and each constant cut tail
`c in {2,3}`, that no surviving nonfinal pull occurs at any of

```text
j = n, n+1, n+2.                                   (DLP)
```

Indeed every sufficiently late absolute pull position is uniquely
`m=3n+r`, `0<=r<=2`, with `n=floor(m/3)`, and the scale block `e[n:2n]`
sees it at forced row `j=m-2n=n+r`.

## Exact encoding

For each `(n,c,r)`, construct the right-edge dependency triangle from
`0^n W`, where every symbol of `W` is constrained to state `1` or `2`.
Append endpoint symbols through row `n+r+1`; constrain every newly exposed
cut symbol to `c`, every appended endpoint pair to remain hard-core, and the
transition at row `n+r` to be `1 -> 2`.

The formula is SAT exactly when (DLP) has a counterexample at that triple.
Validate the Boolean encoding against literal enumeration through `n=7`.

## Frozen range and decision rule

Solve all six formulas per length through `n=40`.  For UNSAT instances,
record variables, clauses, solver conflicts, and proof length/maximum clause
width when the solver exposes a proof.

Finite UNSAT is evidence only.  The route succeeds only if the proofs reveal
a fixed local clause schema or an exact recurrence in `n`.  If proof width or
the required boundary summary keeps growing without a stable schema, record
that as a negative result rather than claiming induction.

Controls:

- dropping the binary-source constraint must produce a SAT instance;
- dropping the hard-core continuation constraint must produce a SAT
  instance;
- every decoded SAT control must replay in the literal triangle.


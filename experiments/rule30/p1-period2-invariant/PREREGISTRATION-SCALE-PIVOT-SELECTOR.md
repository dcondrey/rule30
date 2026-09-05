# Preregistration: local scale-pivot selector

## Objective

The `(alpha,beta)` intervention derivative has two binary rows per survival
step and empirically has prefix rank at least `step-K`.  Test whether a fixed
local selector can choose one scalar row per step while retaining the same
rank bound.

At each step the selector chooses one of

```text
alpha, beta, alpha XOR beta.
```

Two selector families are frozen:

1. the choice depends only on `(constant tail, forced endpoint symbol)`;
2. the choice depends on `(constant tail, forced endpoint symbol, step parity)`.

Only forced symbols in `{1,2}` occur during the audited survival prefix, so
the families contain respectively `3^4=81` and `3^8=6561` selectors.

## Split and criterion

- training: every hard-core word through length 12, both tail modes;
- validation: every hard-core word of lengths 13 through 16;
- mandatory special validation: tail-2 word `12212121212121212` and tail-3
  word `121`.

For every prefix of every case, form the matrix containing the selected row
from each completed survival step.  A selector survives exactly when

```text
rank >= prefix_length - K,
```

with `K_2=indicator(22 occurs)` and `K_3=3`.

The lexicographically first training survivor is not privileged: all training
survivors are passed to validation, and all validation survivors are
reported.  No selector may be changed after seeing validation failures.

## Controls and interpretation

- selected rows are reconstructed from the independently controlled affine
  intervention traces;
- direct and incremental binary ranks must agree;
- the selected row must equal the advertised `alpha`, `beta`, or XOR row;
- the unrestricted two-row `(alpha,beta)` prefix bound is rechecked for every
  dataset case.

No survivor proves the all-length rank lemma.  A survivor is a proof lead only
if its local choice admits an exact recurrence and a uniform pivot argument.
If both families have no validation survivor, local symbol/parity selection is
killed; the two-row rank invariant remains viable but cannot be compressed in
this way.

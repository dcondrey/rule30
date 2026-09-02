# Preregistration: held-out two-row derivative rank

## Motivation and frozen target

The fixed one-row pivot selector was falsified at length 21.  Its first
counterexample still satisfies the unrestricted `(alpha,beta)` prefix-rank
bound, with rank 11 against target 11.  Test the original two-row
abelianization without choosing a scalar row.

For every hard-core word `W`, tail `c`, and prefix of length `p` in the
hard-core forced scale continuation, form the binary matrix whose rows are
both `alpha` and `beta` intervention derivatives at steps `0,...,p-1`.
The frozen target is

```text
rank_F2 >= p-K,
K_2=indicator(22 occurs in W), K_3=3.
```

This is the abelianization of the affine boundary group: `alpha` and `beta`
both add under group composition, while `gamma` is the discarded cocycle.

## Frozen validation

- reuse the already controlled bit-sliced trajectory implementation;
- exhaustive hard-core words of lengths 17 through 22, both tails;
- the first selector counterexample
  `121212222222221212122` in tail 2 is printed separately;
- the original length-17 repair witness is printed separately;
- 1,000 deterministic random hard-core words at each length 24, 32, 48, 64,
  seed `30030`;
- slow/bit-sliced derivative-row equality through length 7;
- incremental and direct binary ranks agree.

## Interpretation

Any negative prefix slack kills the two-row rank conjecture.  Passing is
finite evidence only.  An all-length proof would need to bound the dependency
space among the paired rows, using the additive composition of `(alpha,beta)`;
the failed local selector may not be silently reintroduced.

# Preregistration: zero-prefix scale matching

## Sufficient coarse bounds

The scale separator only needs the forced hard-core continuation to end before
`2|W|`.  The exact census through length 22 suggests the weaker bounds

```text
s_2(W) <= |W|,
s_3(W) <= |W|+1.
```

Together with the direct length-one tail-3 check, these imply the separator.

## Zero-prefix telescoping chain

For `W=w_0...w_(n-1)`, define scenario `k` by replacing the first `k`
symbols by state 0:

```text
W^(k)=0^k w_k...w_(n-1),  0<=k<=n.
```

Token `k` is the exact trajectory difference from `W^(k)` to `W^(k+1)`.
A survival step is adjacent to token `k` when its affine boundary triple or
forced endpoint symbol changes.  Test ordinary and order-preserving matching
with correction budgets

```text
K_2=0, K_3=1.
```

There are exactly `n` real tokens, so a cover of at least `s-K` steps proves
the coarse bound.

## Frozen gates

1. immediate checks of tail-3 `W=121`, the tail-2 repair word
   `12212121212121212`, and the length-21 derivative adversary;
2. slow exhaustive audit through length 16 if all immediate checks pass;
3. independent bit-sliced equality through length 7 and exhaustive validation
   at lengths 17 through 22 if one direction survives.

Only the left-to-right zero-prefix order is registered.  No alternate target
symbol or coordinate order may be substituted after a failure.

## Interpretation

A matching failure kills this certificate, not the numerical coarse bound.
Passing is finite evidence.  Its proof advantage is structural: `W^(k)`
extends the inert zero padding by one coordinate, so consecutive scenario
columns should admit a direct truncation/Peel recurrence.

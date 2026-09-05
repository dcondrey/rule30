# Preregistration: nonfinal alpha diagonal support

Date: 2026-09-02

Status: frozen after discovery through source length 17 and before held-out
testing.

## Candidate

For a binary hard-core source word `W` of length `n`, let
`alpha_(j,k)` be the high-translation coordinate of the constant-tail
boundary permutation in zero-prefix scenario `0^k W[k:n]`.

> **Nonfinal alpha support `(NAS)`.**  If the original scenario survives
> through row `j+1`, then some `k` with `j<=k<n` has
> `alpha_(j,k) != alpha_(j,k+1)`.

This strengthens pull-row alpha support by applying to every nonfinal row,
but simplifies the observable: it uses alpha alone for both tails and makes
no reference to endpoint event type.

The exact contrapositive is useful for a suffix proof.  With `W=L U` and
`|L|=j`, if the alpha profile over `k=j,...,n` is constant, then every
compatible hard-core prefix `L` must die no later than row `j+1`.

## Discovery and held-out plan

Discovery used every hard-core word through length 17.  The only alpha-only
diagonal misses were final rows, never nonfinal rows.  Freeze before:

1. every hard-core word at lengths 18 through 23, both tails;
2. 2,000 deterministic random hard-core words per tail at lengths
   24, 32, 48, 64, 96, and 128;
3. exact comparison against the slower scenario constructor through length
   seven.

Any nonfinal row without an alpha witness kills `(NAS)`.  A finite pass is
evidence only.  Success still requires an all-length suffix recurrence or a
branch-complete transducer proof.

## Consequence if proved

Apply `(NAS)` at row `j=s-2` of any continuation of survival length `s>=2`.
Then `s-2<=k<=n-1`, so

```text
s_c(W) <= n+1.
```

For `n>=2`, this is strictly below the required scale block length `2n`.
The length-one cases are exact bases.  Thus `(NAS)` proves both constant-tail
separators and completes the period-two exclusion through the existing
rank reductions.

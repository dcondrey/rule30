# Preregistration: late-pull horizon

Date: 2026-09-02

Status: frozen before long-word stress testing.

## Claim

Let `W` be a nonempty hard-core word of length `n`, let `c` be `2` or `3`,
and force the scale extension with constant cut tail `c`.  During its initial
hard-core survival prefix, call row `j` a pull when the endpoint transition
is `1 -> 2`.

> **Late-pull horizon (LPH).**  No pull at a row `j>=n` is nonfinal.  In
> fact, the existing exact corpus suggests the stronger statement that no
> surviving pull occurs at `j>=n` at all.

LPH is a strict weakening of pull-row alpha support: PAS demands a token in
`[j,n)`, so it implies LPH immediately, but LPH says nothing about pull rows
`j<n`.

## Why it is sufficient

For an infinite hard-core endpoint with constant inverse-cut tail, let a
pull occur at absolute endpoint position `m>=9`, and put `n=floor(m/3)`.
Then `m=3n+r`, `0<=r<=2`, and the scale block `W=e[n:2n]` sees this pull at
forced row

```text
j=m-2n=n+r,
```

which satisfies `n<=j<2n`.  The infinite endpoint makes it nonfinal,
contradicting LPH.  Thus LPH makes every such endpoint eventually pull-free;
the endpoint/event identity then makes it eventually `2`, the exceptional
family already excluded by the proved reachability separator.

## Frozen audit

1. Recount all hard-core words through length 23 without using alpha data.
2. Test the stored GA constant-tail witnesses at cutoffs `23,32,48,64,96`
   by extracting every dyadically aligned scale block available inside the
   verified endpoint prefix and replaying it directly.
3. Test 20,000 deterministic random hard-core words at each length
   `24,32,48,64,96,128` and both tails.
4. Record the maximum pull row and the slack `n-1-j`; distinguish final and
   nonfinal pulls.

The finite audit is only a falsifier.  Success requires an all-length queue,
cone, or triangular-elimination argument.  A single nonfinal pull at `j>=n`
kills LPH and therefore also kills PAS.


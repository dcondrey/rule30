# Preregistration: one-credit scale-halving recurrence

## Candidate

Let `s_c(W)` be the initial hard-core survival in the constant-tail scale
block `R_c(W)`.  Split a hard-core word `W` of length `n` at `floor(n/2)`
into its left and right halves `L,R`.  Freeze the recurrence

```text
s_c(W) <= ceil(n/2) + 1 + max(s_2(L),s_3(L),s_2(R),s_3(R)).       (H)
```

An exploratory audit through length 20 killed the same formula without the
universal `+1`: two length-16 tail-2 words exceed it by one.  Adding the one
credit repairs both and leaves no failure through that exploratory horizon.

## Held-out test

Test every hard-core word at lengths 21, 22, and 23, both constant tails.
Then test 1,000 deterministic random hard-core words at each of lengths 24,
32, 48, and 64.  Any positive slack

```text
s_c(W) - ceil(n/2) - 1 - max_half_tail_survival
```

kills (H).  The exact scale extension and hard-core survival routines are the
independently controlled implementations already used in the scale census.

## Consequence if proved uniformly

Put `T(n)=max_(|W|=n,c) s_c(W)`.  Then (H) gives

```text
T(n) <= ceil(n/2)+1+max(T(floor(n/2)),T(ceil(n/2))).
```

Together with exact small bases, this grows as `n+O(log n)` and is strictly
less than `2n`.  Therefore (H) would prove the scale separator and exclude
both constant-tail modes.  A finite pass is evidence only; the proof would
still need to derive (H) from the inverse-cone/Peel halving geometry while
retaining its boundary mode.

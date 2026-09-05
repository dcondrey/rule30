# Preregistration: deterministic left-half / tail-2 recurrence

## Observation

The four-way one-credit halving recurrence passed through length 23.  A
post-check on the exploratory corpus through length 18 found the stronger
deterministic law

```text
s_c(W) <= ceil(n/2)+1+s_2(L),                        (D)
```

where `L` is the left prefix of length `floor(n/2)`, for both input tails
`c=2,3`.  The only failures are the exact length-three tail-3 bases `121` and
`221`, both with survival four against bound three.  Freeze (D) for `n>=4`.

## Held-out test

Audit every hard-core word at lengths 19 through 23, both input tails, then
1,000 deterministic random hard-core words at each of lengths 24, 32, 48,
and 64.  Any positive value of

```text
s_c(W)-ceil(n/2)-1-s_2(L)
```

kills (D).

## Consequence if proved uniformly

The recurrence has a fixed smaller mode: left half, constant tail 2.  Exact
small bases plus induction give `s_c(W)<2n`, hence the scale separator.  This
is more proof-oriented than maximizing over four half/tail choices: the
rotated Peel/halving identity need only establish one boundary-mode map.

Passing the finite audit is not a proof.

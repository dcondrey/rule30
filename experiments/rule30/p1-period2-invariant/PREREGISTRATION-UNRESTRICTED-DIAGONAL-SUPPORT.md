# Preregistration: unrestricted projected diagonal support

## Observation and held-out corpus

The right-aware diagonal-support audit passed through length 23.  A post-hoc
probe then removed the tail-2 exclusion of `22222` and found no diagonal
failure through length 18.  This shows that the five-zero restriction may
have been needed only by the stronger greedy certificate.

Freeze the stronger claims:

1. for every hard-core `W`, every tail-2 survival row `j` has some `k>=j`
   with `(alpha,beta)_(j,k) != (alpha,beta)_(j,k+1)`;
2. for every hard-core `W`, every nonfinal tail-3 survival row `j` has some
   `k>=j` with `(alpha,gamma)_(j,k) != (alpha,gamma)_(j,k+1)`.

The new exhaustive corpus is precisely the tail-2 words of lengths 19 through
23 that contain `22222`; these were omitted from the registered right-aware
tail-2 test.  Tail 3 needs no rerun because it was already unrestricted.

Any missing projected edge on or to the right of the row diagonal kills the
claim.  Passing the corpus is bounded evidence, not an all-length proof.

## Consequence if proved uniformly

At the final tail-2 survival row `j=s-1`, diagonal support gives
`s-1<=k<=n-1`, hence `s<=n`.  At the final nonfinal tail-3 row `j=s-2`, it
gives `s<=n+1`.  These bounds prove the scale separator for both constant
tails without any actual-right restriction, close the rank-zero separator,
and exclude the nonconstant period-two center trace.

# Preregistration: projected diagonal support

## Post-audit simplification

The registered two-coordinate greedy audit through length 22 passed.  Its
chosen token on required row `j` is necessarily at least `j`, since chosen
tokens are distinct and strictly increasing.  This suggests discarding the
greedy history and testing the strictly simpler statement directly.

For zero-prefix scenarios `W^(k)=0^kW[k:n]`, let `A_(j,k)` be the newest
affine boundary map.  Use projections

```text
pi_2(alpha,beta,gamma)=(alpha,beta),
pi_3(alpha,beta,gamma)=(alpha,gamma).
```

The frozen diagonal-support claims are:

1. if `W` is hard-core and avoids `22222`, then at every tail-2 hard-core
   survival row `j` there is a token `k>=j` with
   `pi_2(A_(j,k)) != pi_2(A_(j,k+1))`;
2. for every hard-core `W`, at every nonfinal tail-3 survival row `j` there
   is a token `k>=j` with
   `pi_3(A_(j,k)) != pi_3(A_(j,k+1))`.

The first new exhaustive test is length 23, which was not part of the
two-coordinate length-22 audit.  Long-word falsifiers use deterministic
random hard-core sources at lengths 24, 32, 48, and 64, rejecting and
resampling tail-2 words containing `22222`.

Any required row without a selected edge at or to the right of its row index
kills the corresponding claim.

## Consequence if proved uniformly

For tail 2, apply the claim at the last survival row `j=s-1`.  Since every
token satisfies `k<=n-1`, it follows that `s<=n`.  For tail 3, apply it at the
last nonfinal row `j=s-2` to obtain `s<=n+1`.  The actual-right five-zero
theorem supplies the tail-2 exclusion of `22222`.  These two inequalities
would close the scale separator needed for the nonconstant period-two trace.

Passing the registered finite tests is not an all-length proof.

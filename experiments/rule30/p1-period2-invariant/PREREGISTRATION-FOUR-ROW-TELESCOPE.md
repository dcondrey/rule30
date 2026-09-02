# Preregistration and result: four-row projected telescope

Status: **KILLED.**  The held-out length-17 row contains three exact
counterexamples.  The first is

```text
tail=3, W=12221222121212122, n=17, s=4, start=0.
```

Its two four-row signatures coincide.  The registered claim below is false
and is not used in any reduction.

## Observation

Single-row endpoint telescoping is false because ordered affine defects can
cancel.  The same comparison over the final two or three legal rows also has
counterexamples.  An exploratory audit through length 16 found no
counterexample once four consecutive rows are retained.

For a hard-core word `W` of length `n`, let `A_(r,k)` be the newest affine
boundary map at forced row `r` in zero-prefix scenario `k`: scenario `k`
replaces the first `k` symbols of `W` by zero.  Put

```text
pi_2(alpha,beta,gamma)=(alpha,beta),
pi_3(alpha,beta,gamma)=(alpha,gamma).
```

Freeze the following claim.

> If forced rows `j,j+1,j+2,j+3` are all hard-core legal, then `j<n` and
> the four-row word
> `pi_c(A_(j,j)) ... pi_c(A_(j+3,j))` differs from
> `pi_c(A_(j,n)) ... pi_c(A_(j+3,n))`.

Equivalently, some adjacent zero-prefix defect with token `k>=j` is visible
in the selected projection on at least one of the four rows.  Unlike the
rowwise diagonal-support conjecture, this statement allows defects that
cancel on one, two, or three successive rows.

## Held-out test

Audit every hard-core word at lengths 17 through 23 in both constant-tail
modes.  Test every four-row window contained in its legal forced prefix, not
only the final window.  Then test 1,000 deterministic random hard-core words
per tail at lengths 24, 32, 48, and 64.

Any legal four-row window starting at `j>=n`, or equality of the two
four-row signatures for `j<n`, kills the claim.

## Consequence if proved uniformly

Four legal rows starting at `j=s_c(W)-4` give `j<n`; hence

```text
s_c(W) <= n+3.
```

If fewer than four rows survive, the scale separator is immediate.  Thus
the claim gives `s_c(W)<2n` for every `n>=4`; the exact lengths `1,2,3`
supply the bases.  This excludes both eventually constant cut tails and
would complete the nonconstant period-two center-trace exclusion.

Passing the finite audit is not a proof.

## Held-out outcome

Length 17 contains 8,362 word/tail cases and 295 legal four-row windows.
Exactly three windows violate the claim.  This shows that retaining several
rows does not by itself repair endpoint cancellation; the intermediate
ordered defect word or an ancestry annotation is still necessary.

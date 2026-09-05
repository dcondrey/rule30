# Preregistration: actual-right two-coordinate zero-prefix selector

## Observation motivating the test

The full three-coordinate zero-prefix greedy rule has no failures through
length 22.  Coordinate-subset probes through length 13 suggest a smaller
period-two-specific statement:

- for constant tail 2, use only affine coordinates `(alpha,beta)` and impose
  the proved actual-right factor exclusion `00000`, equivalently no endpoint
  factor `22222`;
- for constant tail 3, use only `(alpha,gamma)` on every hard-core word.

The first five tail-2 failures without the right-language restriction are the
length-12 words whose binary encodings end in at least five zeroes.  This
motivates the frozen restriction; it is not a post-hoc deletion during the
registered run.

## Frozen test

For `W^(k)=0^k W[k:n]`, let `A_(j,k)=(alpha,beta,gamma)` be the exact newest
boundary affine map while the forced cut tail is `c`.  At each survival row,
put an edge at token `k` when adjacent scenarios differ in one of the selected
coordinates above.  Starting after token `-1`, greedily choose the least
larger edge.

Audit every hard-core word through length 22, filtering tail-2 sources only
by absence of `22222`.  The registered claims are:

1. tail 2 greedily covers every survival row;
2. tail 3 greedily covers every nonfinal survival row;
3. if `r` rows are required and `g_j` is the chosen token, then the stronger
   deadline `g_j <= n-r+j` holds.

Any missing required row or negative deadline slack kills the corresponding
claim.  The bit-sliced construction is inherited from the already
slow-controlled full-coordinate audit.

## Consequence if proved uniformly

The right-language five-zero theorem is already uniform.  Therefore a proof
of this selector lemma would give `s_2(W)<=n` for every actual-right factor
and `s_3(W)<=n+1` for every hard-core word.  The scale argument would then
exclude both constant-tail modes needed for the nonconstant period-two center
trace.  Passing the finite audit alone is evidence, not that proof.

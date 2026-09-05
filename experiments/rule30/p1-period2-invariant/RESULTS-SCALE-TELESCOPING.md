# Scale telescoping: killed derivatives and a live zero-prefix greedy lemma

## 1. Status

This work does **not** prove the period-two exclusion.  It replaces the
previously conjectured sharp scale charges by a simpler, sufficient, and much
more structured all-length target.

For a nonempty hard-core word `W` of length `n`, let `R_c(W)` be the exact
forced scale block for constant cut tail `c in {2,3}`, and let `s_c(W)` be its
initial hard-core continuation length.  The live conjecture is

```text
s_2(W) <= n,
s_3(W) <= n+1.                                      (1)
```

Equation (1) is enough for the scale separator.  For tail 2, `n<2n`.  For
tail 3, `n+1<2n` when `n>=2`, and the length-one case is checked directly.
Thus a proof of (1) would close both constant-tail modes, the rank-zero
separator, and the nonconstant period-two center trace.

The exact finite result is stronger than a census of (1): a deterministic
zero-prefix greedy matching certifies (1) for every hard-core word through
length 22.

## 2. The derivative hierarchy and its length-21 failure

The first attempted certificate changed each source state 2 independently to
state 1 and recorded changes in the newest affine boundary state
`(alpha,beta,gamma)`.  It initially looked strong:

- ordinary and order-preserving matchings covered all 13,526 registered
  word/tail cases through length 16, including the length-17 sharp repair
  witness;
- all two-coordinate derivative matrices had prefix rank at least `s-K`
  through the same horizon;
- a fixed scalar selector survived the train/validation split through length
  16.

Held-out length 21 kills the entire pointwise-intervention family.

The fixed selector first fails at

```text
W=121212222222221212122, c=2,
s=12, K=1, selected rank=10, target=11.             (2)
```

There are 16 selector-prefix failures at length 21 and none at length 22.
The additive `(alpha,beta)` rank then fails at

```text
W=122212222222221212122, c=2,
s=12, K=1, paired rank=10, target=11.               (3)
```

The full three-coordinate rank is also 10 on (3).  The original intervention
graph itself has only ten real neighbors across all twelve survival rows:

```text
real neighbor source coordinates =
{3,9,10,11,12,13,15,17,19,20}.
```

Adding the one contact credit gives maximum matching size 11, not 12.  Thus
ordinary matching, ordered matching, scalar rank, additive rank, and full
affine rank are all genuinely falsified.  The numerical charge remains true
on (3), since `12<=16+1`; only the proposed certificate fails.

The bit-sliced implementation used for this falsification passed 10,132 exact
slow/fast trajectory checks, including every forced scenario symbol and all
three affine coordinates.

## 3. Why cumulative interventions repair the cancellation

Independent changes can cancel.  Instead enumerate source-2 coordinates from
left to right and change them cumulatively to state 1.  Consecutive scenarios
then differ along a telescoping path rather than at one Boolean base point.

The left-to-right cumulative graph has zero ordinary and zero ordered failures
in

```text
13,525 slow cases through length 16,
229,258 bit-sliced cases at lengths 17,...,22 and the two sharp words.
```

It covers both (3) and the original length-17 repair witness.  The reverse
spatial order is not equivalent: it first loses orderedness at length 7 and
has matching size only 8 on the length-17 repair word even after its credit.

This left/right separation is structural.  In the successful order, scenario
`k` has a uniform all-1 prefix followed by the original suffix.  The sweep is
a single moving interface aligned with the triangular information flow.

The no-lookahead earliest-token greedy rule is too strong for this all-1
chain.  It covers only nine of the ten repair-witness rows after the contact
credit, while an optimal ordered matching covers all ten.

## 4. Zero-prefix chain and coarse bounds

The sharper `#2` charge is unnecessary for the scale separator.  Give every
source coordinate one token and define

```text
W^(k)=0^k W[k:n],  0<=k<=n.                          (4)
```

For forced step `j` and scenario `k`, let `A_(j,k)` be the newest endpoint to
cut permutation, written in the exact affine coordinates
`(alpha,beta,gamma)`.  The forced endpoint symbol is `A_(j,k)^(-1)(c)`, so it
contains no information beyond `A_(j,k)`.

Token `k` is an edge at row `j` precisely when

```text
A_(j,k) != A_(j,k+1).                                (5)
```

Starting with last token `g_-1=-1`, define the deterministic greedy frontier

```text
g_j = min { k>g_(j-1) : A_(j,k) != A_(j,k+1) }.      (6)
```

If the set is empty, row `j` is missed.

The finite theorem audit is:

> For every hard-core `W` through length 22, tail 2 misses no survival row.
> Tail 3 misses at most one row, and that row, when present, is always the
> final survival row.

The complete bit-sliced run covers 242,783 word/tail/special cases and reports

```text
ordinary failures:       0
ordered failures:        0
greedy failures:         0
nonfinal miss failures:  0
```

The independent zero-prefix graph agrees with the slow construction through
the registered control horizon.  The sharp cases are covered exactly:

```text
tail-3 W=121:                         s=4, greedy=3 real + 1 boundary credit
tail-2 W=12212121212121212:          s=10, greedy=10
tail-2 W=122212222222221212122:      s=12, greedy=12
```

There are `n` tokens.  Therefore the audited greedy statement immediately
implies (1) at every checked length.

## 5. Exact remaining lemma

The proof target no longer mentions maximum matching, matrix rank, or the
sharp `#2` charge.

> **Zero-prefix greedy lemma.**  Let `W` be a nonempty hard-core word.  Build
> `A_(j,k)` from (4)-(5) while forcing constant cut tail `c`.  If the original
> forced continuation remains hard-core at rows `j` and `j+1`, then the set in
> (6) is nonempty.  For `c=2` it is also nonempty at the final hard-core row.

Inductively, the chosen tokens are strictly increasing.  Tail 2 therefore has
at most `n` rows.  Tail 3 has at most `n` nonfinal rows plus its possible final
row.

This statement is the current load-bearing gap.  It is supported through
length 22 but is not proved.

## 6. Proof leads and negative probes

The chain (4) has a useful algebraic interpretation.  For any Boolean function
of the source coordinates, the difference between scenarios `k` and `k+1`
isolates the ordered finite-difference slice whose least nonzero source index
is `k`.  The greedy lemma says successive legal forced rows expose strictly
increasing least-index slices.  This suggests a leading-term argument in the
zero-prefix filtration, combined with the rotated Peel identity, rather than
another fixed-radius potential.

Several tempting simplifications are already excluded:

- all 16 binary `2x2` patterns occur in the local edge matrix, so ordinary
  total-monotonicity is absent;
- comparing only the first remaining scenario with the all-zero scenario
  fails in 129 of 989 required rows through length 12, because affine labels
  can change internally and return;
- the first `n` forced symbols and even the complete `2n` forced block are not
  injective functions of an arbitrary four-state source word;
- a fixed bounded jump of the greedy frontier is false.

The next proof attempt should therefore retain the ordered finite-difference
word or an equivalent Peel-leading term.  Endpoint parity, local edge
patterns, and pointwise Boolean derivatives discard exactly the information
used by the successful sweep.

## 7. Reproduction

From `13-rule30/`:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_bitsliced_derivative.py \
  --control-length 7 --exhaustive-first 17 --exhaustive-last 22 \
  --random-per-length 1000

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_cumulative_bitsliced.py \
  --control-length 7 --first-length 17 --last-length 22

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_zero_prefix_bitsliced.py \
  --control-length 7 --first-length 1 --last-length 22
```

The first command intentionally reports the registered length-21 selector and
paired-rank failures.  The second validates the sharp left-to-right cumulative
matching.  The third is the complete zero-prefix optimal/greedy/final-miss
audit.

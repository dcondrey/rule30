# An autonomous triangular affine CA need not have automatic spacetime

Date: 2026-09-14. **The general fixed-height automaticity claim is false.**
A four-bit, radius-two cellular automaton has an additive bottom layer, an
upper layer linear over `F_2` once the bottom layer is supplied, and a finite
initial condition. Its origin is occupied exactly at times `3^k-1` for `k>=0`.
That column, and therefore its spacetime, is not 2-automatic.

This is a constructed CA, **not Rule 30 and not an actual Newton iterate**.
It rules out deriving automaticity of the second actual Newton iterate from
triangularity and an additive bottom layer alone. The special reference
`a_t=(1+X+X^2)^t` may still admit additional identities. The constructed origin
query itself has a simple polylogarithmic algorithm, so nonautomaticity here
does not establish query hardness.

## 1. The exact autonomous CA

At each site `x in Z`, use four bits `(o,b,R,L)`. All arithmetic below is in
`F_2`, and every right-hand side is evaluated at time `t`:

```text
o'(x) = o(x)
b'(x) = b(x-1)
R'(x) = (1+b(x-2))*R(x-2) + o(x-2)*L(x-2)
L'(x) = b(x+2)*R(x+2) + (1+o(x+2))*L(x+2).
```

The initial condition is

```text
o_0 = R_0 = delta_0,   b_0 = delta_1,   L_0 = 0.
```

The zero state is quiescent. The bottom vector `(o,b)` evolves by a fixed
linear CA and is exactly

```text
o_t(x) = 1[x=0],   b_t(x) = 1[x=t+1].
```

For fixed bottom data, the upper update is a homogeneous linear map of
`(R,L)`. At a source site, an `R` particle moves two cells right unless `b=1`,
when it moves two cells left and becomes `L`. An `L` particle moves two cells
left unless `o=1`, when it moves two cells right and becomes `R`. Each single
particle has exactly one destination. Starting with one particle therefore
leaves exactly one at every time; there is no cancellation or duplication on
this trajectory.

This is a finite, fixed, two-layer triangular affine system. Its growing
coefficient pattern is generated locally by its own additive bottom layer.

## 2. The complete itinerary, including collision timing

Suppose the particle is at the origin at time `T`. For `T=0` its direction is
`R`; at every subsequent origin visit it is `L` and reflects on its next step.
The outgoing leg in either case has position

```text
x(t) = 2(t-T).
```

The moving marker is at `t+1`. Thus the first collision is exactly

```text
C = 2T+1,   x(C) = 2T+2.
```

There is no skipped marker: the outgoing gap `x(t)-(t+1)=t-2T-1` increases by
one per time step and first vanishes at this integer `C`. At time `C` the
particle is still `R`. It reflects in the update to time `C+1`, then travels
left two cells per step. Its next origin time is

```text
T' = C + (2T+2)/2 = 3T+2.
```

The returning leg is positive away from its endpoint, so there is no earlier
origin visit. Induction from `T_0=0` gives the exact all-length formula

```text
T_k = 3^k-1,    k>=0.
```

More explicitly, for `T=T_k`, `C=2T+1`, and `T'=3T+2`, the particle is
`R` at `2(t-T)` for `T<t<=C`, and `L` at `2(T'-t)` for `C<t<=T'`.
Together with the initial particle, these intervals cover every time.
The first visits are `0,2,8,26,80`; they are checks of this induction, not its
justification.

## 3. Elementary proof that the column is not 2-automatic

Let `E={3^k-1:k>=0}`. If its characteristic sequence were 2-automatic, the
canonical binary representations of members of `E` would form a regular
language. Any regular binary language has an ultimately periodic set of
accepted word lengths: after forgetting whether a transition reads `0` or
`1`, the set of reachable automaton states evolves by a fixed map on a finite
power set. Acceptance along this sequence is eventually periodic.

For `k>=1`, the integer `3^k` is strictly between consecutive powers of two.
Subtracting one therefore gives the exact binary length

```text
bitlength(3^k-1) = ceil(k*log_2(3)).
```

These lengths are distinct, since `log_2(3)>1`. The number of them at most `n`
is `floor(n/log_2(3))`. Their natural density is consequently
`1/log_2(3)`, which is irrational: a rational `log_2(3)=p/q` would imply
`2^p=3^q`. Adding the one finite exception from `t=0` does not affect density.
An ultimately periodic set has rational density, giving a contradiction.

Thus this origin column is not 2-automatic. Restricting a jointly automatic
spacetime to a fixed column preserves automaticity, so the spacetime cannot
be jointly 2-automatic either. This proof needs no numerical claim about the
binary expansions of powers of three and no external nonautomaticity theorem.

## 4. What the parallel theorem does and does not supply

Moore and Pnin allow an autonomous preceding factor to determine the
homomorphisms and forcing in a later additive factor. Their fixed cascade
theorem gives polynomial-size parallel circuits; its proof supplies preceding
factor values throughout the required cone. It does not assert automatic
spacetime or polylogarithmic total work. The CA above fits that triangular
structure and shows why automaticity is a stronger conclusion.
[Primary paper, Lemma 1 and Theorem 1](https://arxiv.org/pdf/patt-sol/9701008).

For a genuinely linear CA, rational spacetime and automatic columns follow
from a fixed linear recurrence. That proof does not extend merely by allowing
coefficients supplied by another layer.
[Rowland and Yassawi, Theorem 3.1](https://arxiv.org/pdf/1209.6008).

The previous [automatic-reference Newton counterexample](RESULTS-p3-automatic-reference-newton.md)
used a prescribed, cone-supported automatic reference. The present example
removes the external-driver qualification for the broad triangular-CA claim,
while making no assertion that this particle rule is a Newton Jacobian.

The origin bit is nevertheless cheap to compute: divide `t+1` repeatedly by
three and accept exactly when the result is one. This takes
`O(log^2(t+2))` conservative bit work and `O(log(t+2))` space using ordinary
binary arithmetic. No spacetime or initial-data preprocessing is required.
Thus even this exact failure of automaticity supplies no P3 lower bound.

## 5. Exact verifier and finite controls

The [verifier](../../experiments/rule30/p3_triangular_ca_automaticity.py) and
[artifact](../../experiments/rule30/p3-triangular-ca-automaticity.json) retain:

- all 16 source routing truth cases and 64 upper-linearity comparisons;
- symbolic affine identities in the arbitrary origin time `T`, including both
  leg durations and the recurrence `T'=3T+2`;
- 83 complete finite rows through time 82, comparing a literal
  destination-based CA with independent source routing, and checking every
  marker and the unique particle against the proved itinerary;
- exact arithmetic query controls including `3^1000-1` and its two neighbors,
  with no trajectory generation at those large indices;
- hashes of the maintained source and this report.

The local and finite controls check the implementation. The all-length
conclusions use the proofs in sections 2 and 3. The itinerary and elementary
accepted-length argument were independently reviewed by the counting agent.
No old Rule 30 census, center-prefix generation, or Newton schedule was rerun.

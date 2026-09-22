# Why the defect-count certificate does not yield a parity bound

Date: 2026-09-10. **Exact identities and a scoped obstruction; P2 remains open.**

This investigation follows the [sharp defect-frequency bounds](RESULTS-defect-frequency-polytope.md).
It tests the proposed next step: weight that certificate by the Rule 150
backward mask and use its nonnegative terms to force parity cancellation.
The calculation exposes an explicit spatial current. Its absolute-value
cost is superlinear, and reducing the certificate modulo two removes its
nonnegative information altogether.

## 1. A local form of the count identity

Let p=x_(i-1), q=x_i, r=x_(i+1), and y=p XOR (q OR r). Define integer
observables D_i=qr, H_i=p(1-q)r, U_i=p OR q OR r and the current

\[
J(p,q)=p-q-4pq.
\]

The current values on 00,01,10,11 are respectively 0,-1,1,-4. Direct
substitution on the eight triples proves

\[
\boxed{3(y-q)+5D_i+4H_i
=2U_i+J(p,q)-J(q,r).}
\]

For finite-support rows the spatial current telescopes. This gives exactly
the previous identity 5D+4H=2U-3(n'-n). The local version makes explicit
what is lost when a spatially averaged bound is applied at one column.

For finitely supported real weights w_i, summation by parts instead gives

\[
3\sum_iw_i(y_i-x_i)+5\sum_iw_iD_i+4\sum_iw_iH_i
=2\sum_iw_iU_i+\mathcal F(w,x),
\]
\[
\mathcal F(w,x)=\sum_i(w_{i+1}-w_i)J(x_i,x_{i+1}).
\]

Consequently |F(w,x)|<=4 TV(w), where TV(w)=sum_i|w_(i+1)-w_i|.
For every finite binary mask w, the finite-support row x=w gives

\[
\boxed{\mathcal F(w,w)=-\operatorname{TV}(w).}
\]

Indeed, at a rising mask edge the contribution is J(0,1)=-1, and at a
falling edge it is -J(1,0)=-1. Thus a bound of smaller order than TV(w)
cannot hold uniformly over all input rows. These extremizing rows are
not asserted to occur in the lone-seed orbit.

## 2. Exact variation growth of the Rule 150 mask

Let w_n(j)=[z^j](z^-1+1+z)^n over GF(2), let a_n be its number of ones,
and let r_n be its number of runs of ones. Frobenius gives

\[
a_{2n}=a_n,\qquad r_{2n}=a_n.
\]

In row 2n+1 the even-coordinate entries are w_n(j), while the intervening
odd entries are w_n(j) XOR w_n(j+1). There are 2r_n nonzero intervening
entries, and one new run for each original one. Therefore

\[
a_{2n+1}=a_n+2r_n,\qquad r_{2n+1}=a_n.
\]

Set S_k=sum_(n<2^k)a_n. Then

\[
S_0=1,\quad S_1=4,\quad S_k=2S_{k-1}+4S_{k-2}\quad(k\ge2).
\]

The sequence starts 1,4,12,40,128,416,1344. Since TV(w_n)=2r_n,

\[
\boxed{\sum_{n<2^k}\operatorname{TV}(w_n)=4S_{k-1}}
\qquad(k\ge1).
\]

The characteristic roots are 1+sqrt(5) and 1-sqrt(5), so this sum is
Theta(T^alpha) at T=2^k, with

\[
\alpha=\log_2(1+\sqrt5)\approx1.69424.
\]

Thus bounding each mask-current term separately by absolute values gives
a superlinear budget. The construction in Section 1 shows that this order
is sharp for independently chosen rows at each mask. It does not establish
a lower bound along the Rule 30 trajectory, whose rows are coupled.

This is a support-count exponent for a specified discrete family. It is
not an assertion about every geometric notion of fractal dimension.

## 3. The parity reduction loses the useful inequalities

Modulo two, 2U_i and 4H_i vanish, and J(p,q)=p+q. The exact local law becomes

\[
y+q+D_i=p+r,
\]

or

\[
y=p+q+r+qr.
\]

This is the original Rule 30 polynomial. Weighting it by the adjoint
Rule 150 kernel therefore reproduces the Duhamel identity; it supplies
no additional parity relation. The terms that supported the real-valued
defect bound disappear in this reduction.

This rules out the proposed inference from this particular count certificate
to a sublinear signed discrepancy. It does not rule out a new identity,
an inequality retaining further orbit information, or a different P2 proof.

## 4. Actual seed diagnostics

For comparison, the audit measures the integer current

\[
Q(T)=\sum_{s=0}^{T-1}\mathcal F(w_{T-1-s},x^s)
\]

on actual seed rows. This uses the full source-mask family before removing
the mandatory edge contribution. It is not the center discrepancy.

| T | Q(T) | Sum of absolute row currents | Total mask variation |
|---:|---:|---:|---:|
| 512 | 769 | 4,393 | 56,320 |
| 1,024 | 1,059 | 10,991 | 182,272 |
| 2,048 | 1,524 | 27,120 | 589,824 |
| 4,096 | 5,987 | 67,219 | 1,908,736 |
| 8,192 | 6,114 | 169,164 | 6,176,768 |

There is substantial finite cancellation relative to the absolute bound.
These data prove neither Q(T)=o(T) nor its negation. Even a bound on Q(T)
would still require an argument connecting it to cancellation of the parity
signs; the integer conservation identity alone provides no such inequality.

## 5. Verification and further investigation

Run:

```
uv run python experiments/rule30/defect_mask_flux_audit.py --output experiments/rule30/defect-mask-flux-audit.json
```

The audit checks all eight local triples, all 8,190 binary masks of widths
1–12 for the exact current extremizer, and the kernel recurrences through
16,384 rows. The JSON also retains the finite seed diagnostics.

The independent [two-step block investigation](RESULTS-dyadic-pair-factor-obstruction.md)
tests an alternative: whether exact coarse dynamics can retain the information
needed for cancellation. Its finite classification distinguishes Rule 30
from the linear controls, but gives no asymptotic center bound.

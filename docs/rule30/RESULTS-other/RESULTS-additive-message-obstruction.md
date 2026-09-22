# An information ceiling for nonnegative additive messages

Date: 2026-09-13. **A specified message family is obstructed. The cumulative
counting inequality, finite-frontier mortality, and period-two exclusion remain
open.** This is an elementary consequence of the existing exact spatial
transfer and mixing theorems. No trajectory, census, transfer array, or trained
model was computed for this deduction.

The obstruction applies to sums of nonnegative functions of bounded numbers
of column bits. It does **not** apply to minima or products of such functions,
or to signed decompositions with a nonnegative total.

## 1. Exact counting setup

Fix a temporal depth n>=1. The physical column space is

```
Omega_n = {0,1}^{2n+1}, with coordinates A_0,A_1,B_1,...,A_n,B_n.
```

Let P_n be the normalized common spatial transition from the
[exact transfer construction](RESULTS-cumulative-history-transfer.md).
Every labeled edge has weight 1/4. The
[all-depth mixing theorem](RESULTS-history-transfer-mixing.md) proves that
P_n is irreducible and aperiodic, has four incoming and outgoing labeled
edges at every state, and converges to its uniform stationary distribution
mu_n.

For a prescribed length-n scalar tape alpha, let g_alpha indicate its exact
two accepting columns. These columns include the complete transported birth
suffix and every chronological guard. Let nu_n be the equal mixture of the
two legal origin columns. Then, at original length r,

```
p_r(alpha) = |C_r(alpha)| / 2^(2r-1)
           = nu_n P_n^(r-1) g_alpha.
```

This is a count of all original legal length-r words. It introduces no new
prior on intermediate rows or births.

## 2. The additive-message theorem

**Theorem.** Fix integers k,b>=0 and put h=P_n^b g_alpha. Suppose a pointwise
majorant of h has the form

```
F(q) = SUM_(j=1..J) f_j(q restricted to S_j),
```

where J is any finite number, each S_j contains at most k column bits, every
f_j is nonnegative on its entire domain, and F(q)>=h(q) at every column.
Then

```
E_(mu_n) F >= 2^(-k-2b).
```

The number of functions, their coordinate sets, and their values may depend
on n, alpha, and the original length r. Their coordinate sets may overlap
arbitrarily. No independence between constraints is assumed.

**Proof.** The accepting set is nonempty, and every column has incoming
edges. Consequently some length-b path ends in the accepting set. At the
path's initial column q*,

```
h(q*) >= 4^(-b).
```

Under mu_n, the cylinder agreeing with q* on S_j has probability
2^(-|S_j|)>=2^(-k). Since f_j is nonnegative elsewhere,

```
E_(mu_n) f_j >= 2^(-k) f_j(q* restricted to S_j).
```

Summing these inequalities gives

```
E_(mu_n) F >= 2^(-k) F(q*)
           >= 2^(-k) h(q*)
           >= 2^(-k-2b).
```

This proves the theorem. For b=0 one may take q* to be either accepting
column.

## 3. Consequence for a uniform repeat-rate certificate

Suppose a proposed upper-count certificate has fixed bounds k and b on bag
arity and the number of exact backward spatial steps. At each original
length r>=b+1 it may choose a different number b_r<=b of exact steps and a
different majorant F_r of P_n^(b_r) g_alpha, of the form in section 2. Its
number of bags, coordinate sets, and message values may all depend on r.
It obtains the valid upper bound

```
p_r(alpha) <= R_r = nu_n P_n^(r-1-b_r) F_r.
```

The obstruction still applies to these horizon-dependent choices. Fix n,
alpha, and eta with 0<eta<1. Because the state space is finite and the
distribution nu_n P_n^L converges to the strictly positive mu_n, there is
L_0 such that, for every L>=L_0 and every column q,

```
(nu_n P_n^L)(q) >= (1-eta) mu_n(q).
```

For r>=b+1+L_0, nonnegativity and the theorem therefore give

```
R_r >= (1-eta) E_(mu_n) F_r
    >= (1-eta) 2^(-k-2b_r)
    >= (1-eta) 2^(-k-2b).
```

The first inequality is simultaneous for **every** nonnegative F_r; it
does not hold a learned or selected message fixed while taking a limit.
In particular,

```
liminf_(r->infinity) R_r >= 2^(-k-2b).
```

Thus this certificate cannot establish the required upper bound at all
original lengths when

```
k + 2b < epsilon*D(alpha) - log2(c).
```

Indeed, choose eta small enough that
(1-eta)*2^(-k-2b)>c*2^(-epsilon*D(alpha)). The displayed uniform inequality
then exceeds the target at every sufficiently large r, whatever messages
and exact-step counts were chosen there. This is a failure of the
certificate's precision, not of the true counting inequality.

In particular, if k and b have fixed bounds independent of n and alpha,
this message family cannot prove any uniform positive repeat rate. Take
constant tapes, for which D=n-1, and then choose sufficiently large original
lengths. The existing mixing theorem makes their true probabilities tend
to 4^(-n), which illustrates how much precision the additive majorant may
lose.

Allowing arbitrarily many nonnegative pair or window functions does not
remove this obstruction. A necessary scaling for this certificate family is
k+2b>=epsilon*D-log2(c). This is a necessary condition, not a claim that such
scaling is sufficient.

## 4. What the theorem does and does not exclude

A single hard max-projection

```
F(q) = max h(q') over q' agreeing with q on S
```

is the case J=1. It therefore has the same limitation. Performing a fixed
number of exact backward spatial steps before that projection does not
remove the obstruction.

A minimum-of-bags message is a different family. For example, the minimum
of one-bit indicators specifying each bit of a target column represents
that entire conjunction exactly. Its uniform mean can decay exponentially
with n despite each bag containing one bit. The additive proof therefore
does not establish a corresponding impossibility for minimum-of-bags
messages. Products also fall outside its assumptions.

Signed additive terms are likewise outside the theorem: their negative
values invalidate the cylinder lower bound used in the proof. Any proposed
signed representation would still require a certified nonnegative total
majorant. Finally, the theorem allows potentially useful families in which
the retained bit count or exact-block length grows with D.

The result gives a concrete restriction on message design. It supplies no
upper bound on the actual cumulative repeat count and no new Rule 30 period
exclusion.

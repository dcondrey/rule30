# Shared prefix states for exact guarded-history MPS messages

Status: **all-length algebraic certificates**, with a completed bounded
implementation probe. This does not prove the cumulative counting
inequality, finite-frontier mortality, or period-two exclusion.

**Independent follow-up:** the
[guarded UNSAT certificate](RESULTS-constant-zero-history-certificate.md)
now proves `C_41(0^22)=empty`. The MPS computation below did not reach
that conclusion; its saved bounds and declared stopping point are unchanged.

The preceding deterministic suffix probe kept a mixture of point-mass suffix
functions. That representation can merge identical suffix words but cannot
introduce a state accepting several different suffixes. A forward sweep on
weighted prefix coefficient vectors does introduce such states. It preserves
the entire guarded message, including both values of the coordinate `A0`.

This is weighted determinization in the temporal physical variables. We make
no claim that determinization, weighted decision diagrams, or the underlying
MPS identities are new algorithms. These variables and boundaries differ from
decision diagrams over original-frontier bits; changing them does not by
itself supply a mortality proof.

## 1. The exact message and the orientation of its bonds

Write a nonnegative integer MPS as

\[
 f(a,x_1,\ldots,x_n)
 =\ell_E(a)E_1(x_1)\cdots E_n(x_n)\rho_E,
 \qquad a\in\{0,1\},\quad x_j\in\{0,1,2,3\}.
\]

Here `a=A0`, and the physical symbol `x_j=2 A_j+B_j` is a
temporal pair. The old bond dimension after site `j` is `d_j`.
All boundary vectors and matrices are nonnegative. Integer arithmetic is
appropriate for the counting transfer `T=4P`; normalization by `4^b` is
applied after `b` spatial transfers.

The exact bond-four operator and the fully guarded terminal signature are
those in [the guarded-history MPO report](RESULTS-guarded-history-mpo.md).
No chronological guard is dropped by an exact representation change. The
original length is still `r`, and the requested count is the sum of the
message after `r-1` transfers at its two legal origin columns.

Both `ell_E(0)` and `ell_E(1)` must be retained. Setting `A0=1` is permitted
at the final legal-origin contraction. Setting it earlier would change later
MPO applications, which mix the two old boundary values.

## 2. Exact forward normalization

For a nonzero nonnegative integer row vector `w`, define

\[
 c(w)=\gcd\{w_i:w_i>0\},\qquad \nu(w)=w/c(w).
\]

The zero vector has no normalized state. Construct new states as follows.

1. At bond zero, use the distinct nonzero vectors
   `nu(ell_E(0))` and `nu(ell_E(1))`. For each `a`, put its scale
   `c(ell_E(a))` at the corresponding new initial state in `ell_F(a)`.
2. From a normalized state row `v` at bond `j-1`, and for each symbol `x`,
   compute `w=v E_j(x)`. If `w=0`, emit no transition. Otherwise create or
   reuse the state `nu(w)` at bond `j`, and give that transition weight
   `c(w)`.
3. At the last bond, give state `v` the terminal weight `v rho_E`.

Let `V_j` have these normalized state vectors as its rows. Thus `V_j` has
shape **new bond by old bond**, and the new physical matrix `F_j(x)` has
at most one nonzero entry in each row. A row can nevertheless accept several
different physical symbols.

**Theorem.** This construction preserves the message pointwise for every
finite temporal depth and all physical strings. Its exact nonnegative
certificates are

\[
 \ell_F(a)V_0=\ell_E(a),\qquad
 F_j(x)V_j=V_{j-1}E_j(x),\qquad
 \rho_F=V_n\rho_E.                                  \tag{1}
\]

**Proof.** The left identity is precisely normalization of the two initial
rows. For a state `v` and symbol `x`, the corresponding row on the right of
the middle identity is `w=v E_j(x)`. The left side is zero when `w=0`;
otherwise it is `c(w) nu(w)=w`. The last identity is the definition of the
terminal weights. Multiplying these equalities in physical order gives

\[
 \ell_F(a)F_1(x_1)\cdots F_n(x_n)\rho_F
 =\ell_E(a)E_1(x_1)\cdots E_n(x_n)\rho_E.
\]

No independence of constraints or statistical approximation is used. ∎

The construction is finite because only finitely many physical prefixes
exist at each cut. This observation gives no polynomial state bound: the
number of normalized rows can still be exponential in the prefix length.
An implementation cap must stop before discarding an unrepresented state;
discarding one would invalidate exactness.

## 3. The backward quotient has the opposite orientation

For the resulting weighted deterministic MPS, a backward sweep can merge
proportional suffix functions. At the last bond, normalize every positive
terminal scalar to one. At an earlier state, multiply each nonzero outgoing
weight by the scale of its child; take the gcd of the resulting weights,
divide by it, and merge identical tuples of
`(physical symbol, normalized child class, normalized weight)`.
Zero suffix functions have scale zero.

If the quotient is `Q`, the sparse matrices `S_j` have shape **old bond by
new bond**. A row of `S_j` contains its suffix scale in its quotient class,
or is zero. The exact identities are

\[
 F_j(x)S_j=S_{j-1}Q_j(x),\qquad
 \rho_F=S_n\rho_Q,\qquad
 \ell_Q(a)=\ell_F(a)S_0.                            \tag{2}
\]

They follow by backward induction on suffix length. Distinct next symbols
have disjoint sets of words, so the gcd computed at a state is exactly the
gcd of its suffix-function values after child normalization. Consequently,
two states are merged exactly when their nonzero suffix functions are
proportional.

Equations (1) and (2) should be checked separately. The forward matrices
`V_j` are not matrices for the old backward-majorant checker. Nor does
their existence guarantee a direct backward simulation from the original
MPS to the final quotient.

For example, two old states may accept only symbol zero and only symbol
one, respectively, with initial row `(1,1)`. The shared new state accepts
either symbol with weight one. This is an exact forward compression. No
single backward coefficient for each old state can express both individual
indicator functions as multiples of the new union indicator.

After an exhaustive forward sweep and the backward quotient, each cut has
one state for each distinct nonzero proportional residual function induced
by a physical prefix of the full message, with the initial `A0` symbol
included. This characterizes the smallest weighted deterministic
representation with one initial state per nonzero `A0` row. It does not
characterize the smallest general nonnegative MPS, whose prefix can carry
several latent states at once.

## 4. What the shared states add, and what they still miss

Consider the indicator of even parity on binary physical strings of length
`n`, with the other two symbols forbidden. A mixture of point-mass suffix
functions requires `2^(n-1)` initial states, since it must represent that
many different accepted words. After equal suffixes have been merged, the
forward construction shares the prefix states by their required remaining
parity. There are at most two states at every cut. Both outgoing binary
symbols are permitted from a parity state, with different next parity.

Thus the forward sweep can produce branching that was impossible for
the individual suffix-point states in the earlier probe. Its compression
is exact, not a product of independent marginal bounds.

There is also a converse caution. The binary function

\[
 f(x_1,\ldots,x_n)=1+\sum_{j=1}^n2^{j-1}x_j
\]

has a nonnegative bond-two MPS: use initial row `(1,1)`, terminal column
`(0,1)^T`, and matrices

\[
 E_j(x)=\begin{pmatrix}1&2^{j-1}x\\0&1\end{pmatrix}.
\]

Symbols two and three can be forbidden by assigning them the zero matrix.
After `j<n` binary symbols, its `2^j` possible prefix sums induce pairwise
nonproportional residual functions. A nonzero remaining coefficient forces
any proportionality factor to be one, and then the distinct constant terms
cannot agree. Its weighted deterministic representation therefore needs
`2^j` states at that cut, despite the nonnegative bond-two MPS.

A bounded failure of weighted determinization would consequently leave
general nonnegative MPS compression open. Neither example predicts the
complexity of the Rule 30 guarded message.

## 5. A forward certificate for a genuine upper compression

Exact determinization is also a special case of a sufficient upper
certificate. Let `F` be a proposed nonnegative compressed message, and let
`V_j` be nonnegative matrices of shape new bond by old bond. Suppose

\[
 \ell_E(a)\le\ell_F(a)V_0,\qquad
 V_{j-1}E_j(x)\le F_j(x)V_j,\qquad
 V_n\rho_E\le\rho_F,                               \tag{3}
\]

entrywise, for both values of `a` and every physical symbol at every site.
Then `E(q)<=F(q)` for every temporal column `q`.

**Proof.** Starting from the first inequality, multiply by the nonnegative
old physical matrices. At each site, use the middle inequality to move
the comparison matrix to the next cut. This gives

\[
 \ell_E(a)E_1(x_1)\cdots E_n(x_n)
 \le \ell_F(a)F_1(x_1)\cdots F_n(x_n)V_n.
\]

Multiplication by `rho_E` and the terminal inequality prove the claim. ∎

One concrete compression proposal is therefore to keep a bounded set of
nonnegative prototype rows `V_j` and cover each propagated row
`v E_j(x)` by a nonnegative combination of the next prototype rows.
The combination coefficients form `F_j(x)`; they can allow more than one
next latent state for the same physical symbol. A prototype search may
use approximate numerical optimization, but the accepted coefficient
matrices and every inequality in (3) must be verified in exact arithmetic.
The resulting scalar bound must also be checked against the requested
counting threshold. Existence of a feasible but loose majorant is not
progress on the desired rate.

This proposal retains joint temporal information in shared nonnegative
states. It does not follow from the fixed-window message certificates,
and those local-window obstructions do not automatically apply to it.
There is presently no all-length bound on the number of prototypes or the
loss required at successive spatial transfers.

## 6. Bounded probe

Verifier: [shared_prefix_mps.py](../../experiments/rule30/shared_prefix_mps.py).
Artifact: [shared-prefix-mps.json](../../experiments/rule30/shared-prefix-mps.json).

The probe uses the exact counting MPO followed by a backward suffix quotient,
forward coefficient-vector normalization, and another backward suffix
quotient. It checks both orientations of the nonnegative equality
certificates. Its declared caps are 20 seconds and 4,096 states for every
expanded or prefix bond. The saved run took 0.07389 seconds.

The target is `alpha=0^22`, `r=41`, hence `D=21` and `b=r-1=40` spatial
transfers. The requested ancestor bound is `2^60`. The probe completed
**13 transfers**, then stopped before the next exact expansion: that
expansion requires bond `4*1082=4328`, above the cap. The requested
length-41 count was **not computed**.

| Exact compression method | Bond after 11 transfers | Last completed transfer | Bond there |
| --- | ---: | ---: | ---: |
| Individual suffix-point quotient | 1,392 | 11 | 1,392 |
| Shared prefix and suffix sweeps | 357 | 13 | 1,082 |

At transfer 11 the two methods give the same exact global maximum, as
required. At transfer 13 the shared-prefix message has

\[
 \max_q T^{13}g_{0^{22}}(q)=1{,}336{,}340,
 \qquad
 \max_q P^{13}g_{0^{22}}(q)
 =\frac{334085}{16777216}.
\]

The normalized transfer `P` preserves constant upper bounds. Extending this
ceiling to the remaining transfers therefore gives only

\[
 |C_{41}(0^{22})|
 \le 334085\,2^{57}
 =\frac{334085}{8}\,2^{60}.
\]

It misses the requested threshold by the exact factor `334085/8`.
The exact origin count is zero at each completed original length 1 through
14. These are finite observations; they do not determine the requested
length-41 count.

Validation comprised 10,912 exact column comparisons for small control
messages and the parity control. That control reduced a 32-state mixture
of six-symbol even-parity point masses to bond two and checked every column.
The Rule 30 probe itself checked 19,923 forward and 68,017 backward
local/boundary equalities. No large temporal-column graph, new original-start
census, or public center-column regeneration was used.

The test demonstrates exact shared branching and a smaller representation
than the preceding suffix-point method. It does not provide the needed
counting bound. The further task in Section 5 is to control the loss of a
bounded nonnegative shared-state upper representation under repeated
transfers; increasing the cap on exact determinization alone does not
establish that property.

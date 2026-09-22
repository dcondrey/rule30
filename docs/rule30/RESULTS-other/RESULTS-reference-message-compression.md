# Reference-exact upper messages and the cost of subsequent transfers

Date: 2026-09-13. **Three all-length statements are proved:** a nonnegative
MPS can be compressed to an upper message of bond at most `k+1` that is
exact on any specified `k` columns; balanced class-mass compression has a
positive floor that prevents a uniform repeat-rate certificate; and all
compression errors contribute to the final root through an exact weighted
sum. These statements concern representations and certificates. They do
not prove the cumulative counting inequality or period-two exclusion.

The first result shows that small upper bond at the final origins is not
itself the missing condition. Accuracy under subsequent spatial transfers,
or a sufficiently small weighted total error, is the additional requirement.
All references to Rule 30 histories use the complete guarded acceptance
indicator and original legal origins from the
[exact transfer theorem](RESULTS-cumulative-history-transfer.md).

## 1. An upper message exact at selected columns

Let

```text
f(w) = ell E_1(w_1) ... E_n(w_n) rho
```

be any nonnegative MPS over finite, possibly position-dependent alphabets.
All matrices and boundaries are nonnegative. The original-high coordinate
`A_0` can be included as the first physical site: its site matrix is the
boundary row `ell_E(A_0)`, preceded by the scalar left boundary one.

Fix a nonempty set `K` of `k` distinct complete reference words. At cut `j`,
let `K_j` be the set of **distinct** tails of those words after site `j`.
For a physical suffix `v`, define the expanded residual column

```text
e_j(v) = E_(j+1)(v_1) ... E_n(v_(n-j)) rho,
m_j = SUM_(v not in K_j) e_j(v).
```

The latter sum ranges over all suffixes at that cut. It is nonnegative.
The empty suffix belongs to `K_n`, so `e_n(empty)=rho` and `m_n=0`.

Use compressed states `K_j` and one extra state `*` at cut `j`. The intended
residual functions are the indicators of each reference suffix and the
indicator of the complement of `K_j`. There are at most `k+1` states.

For physical symbol `x` at site `j`, define a zero-one matrix `B_j(x)`:

* A reference row `u=(y,v)` in `K_(j-1)` goes to child reference `v` if
  `x=y`; otherwise that row is zero.
* The row `*` goes to child reference `v` exactly when `(x,v)` is not a
  parent reference. It also goes to child `*`.

The right boundary is one on the empty reference suffix and zero on `*`.
These transitions implement the stated indicator residuals exactly. In
particular, duplicate tails are merged as set elements; they are not counted
twice. The complement row can branch to several compatible suffix states.

Define simulation matrices and the left boundary by

```text
S_j[:,v] = e_j(v),       S_j[:,*] = m_j,
ell_F = ell S_0.
```

Then the compressed message `F` has the explicit form

```text
F(w) = f(w)                         if w belongs to K,
       SUM_(v not in K) f(v)        otherwise.                 (1)
```

Therefore `F>=f` pointwise and `F=f` on `K`. If the complement is empty,
the second case never occurs. This is an all-length construction, not an
inference from a finite compression experiment.

### Local certificate

The construction satisfies the
[nonnegative simulation certificate](RESULTS-guarded-history-mpo.md#5-a-local-certificate-for-upper-compression):

```text
E_j(x) S_j <= S_(j-1) B_j(x),
rho = S_n rho_F,       ell S_0 = ell_F.                       (2)
```

For a child-reference column `v`, the left side of the first inequality is
`e_(j-1)(xv)`. If `xv` is a parent reference, the right side is exactly that
vector. Otherwise the right side is `m_(j-1)`, whose defining sum contains
`e_(j-1)(xv)`. For the child-complement column, `E_j(x)m_j` is a subsum of
`m_(j-1)`: a suffix outside `K_j` cannot complete a parent reference. These
are componentwise inequalities between nonnegative sums. Backward induction
and the boundary equalities give the pointwise upper bound.

The simulation columns can be computed without enumerating every suffix.
Contract the ordinary total residual vectors

```text
t_n=rho,       t_(j-1)=SUM_x E_j(x)t_j,
```

and the at most `k` prescribed suffix vectors, then use
`m_j=t_j-SUM_(v in K_j)e_j(v)`. This subtraction is exact; nonnegativity
follows from the preceding set-sum definition.

For the two legal origin columns, `k=2` gives an upper MPS of bond at most
three with the **exact final original-origin contraction**. This does not
make an exponentially large expanded MPS cheap to construct. Its left
coefficients already contain the exact reference evaluations. It is a
constructive representation theorem given the expanded MPS, not a way to
obtain an unknown count without doing the necessary contraction.

## 2. Shared global classes and a limitation of balanced grouping

The same proof covers more general classes. At each cut, partition all
physical suffixes into nonempty classes `L_(j,c)`. Suppose prepending any
symbol `x` maps every child class wholly into one parent class:

```text
x L_(j,d) is a subset of L_(j-1,T_x(d)).
```

Use class indicators as the compressed residual functions and set

```text
S_j[:,c] = SUM_(v in L_(j,c)) e_j(v),
B_j(x)[c,d] = 1[T_x(d)=c].
```

Each column of `E_j(x)S_j` is a subsum of the corresponding parent-class
column. Thus (2) holds. At the full word the resulting envelope is

```text
F(w) = SUM_(v in class(w)) f(v).                              (3)
```

Global parity or positional syndrome classes fit this construction. They
carry correlations across arbitrarily distant sites; this is not a
bounded-window projection. Reference singleton classes and their complement
recover section 1. Other nonnegative MPS representations need not be class
indicators or class-mass envelopes.

There is nevertheless a precise obstruction to **balanced** use of (3).
Write `Q_n` for the `2*4^n` temporal columns and

```text
f_b = P_n^b g_alpha.
```

The [all-depth spatial mixing theorem](RESULTS-history-transfer-mixing.md)
proves that `P_n` is irreducible, aperiodic and doubly stochastic. The fully
guarded leaf accepts exactly two columns. Consequently

```text
SUM_q f_b(q) = 2,
f_b(q) -> 2/|Q_n| = 4^(-n) uniformly in q, at fixed n.        (4)
```

If the class containing each legal origin has cardinality at least
`delta*|Q_n|`, its value under (3) eventually exceeds
`(1-eta)*2*delta`, for every `eta>0`. This statement permits the partition
to depend arbitrarily on `b`: (4) gives the required pointwise lower bound
simultaneously on all columns, hence on every such class.

In particular, balanced `K`-class compression has eventual root floor
`2/K`. If `K` is bounded independently of `n`, it cannot establish any
uniform estimate `c*2^(-epsilon*D(alpha))`, with `c,epsilon>0`. Choose a
constant tape of sufficiently large depth `n`, so `D=n-1`, and then choose
the original length `r=b+1` sufficiently large for (4) to apply. No uniform
mixing-time estimate is needed for this counterargument.

This rules out the stated **mass-of-class envelope** with root classes of
uniformly positive relative size. It does not rule out maxima within
classes, other conic simulation matrices, or unbalanced classes that isolate
the origins. Section 1 explicitly supplies fixed-bond upper messages outside
this obstruction. The true history probability tends to `4^(-n)` in (4);
the positive floor belongs to the class-mass relaxation, not to the count.

## 3. The exact price of compression

Fix temporal depth, tape and total number `B` of spatial transfers. Let
`H_0=g_alpha` and suppose successive upper messages satisfy

```text
H_j = P_n H_(j-1) + e_j,       e_j>=0,       1<=j<=B.
```

Repeated substitution gives the exact function identity

```text
H_B - P_n^B g_alpha = SUM_(j=1..B) P_n^(B-j) e_j.             (5)
```

For the equal mixture `mu` of the two legal origins, the final probability
overestimate is therefore exactly

```text
mu H_B - mu P_n^B g_alpha
  = SUM_(j=1..B) mu P_n^(B-j) e_j.                           (6)
```

Each term is nonnegative. It weights an error by the probability that its
column is reached from the legal origins in the remaining transfers. If
there is already an initial error, add `mu P_n^B(H_0-g_alpha)`.

For a single compression `F>=E` followed by `m` exact transfers, this yields

```text
mu P_n^m F = mu P_n^m E
iff F(q)=E(q) for every q with (mu P_n^m)(q)>0.               (7)
```

Indeed, their difference is a finite sum of nonnegative terms. Every
reachable labeled path has positive probability; duplicate paths retain
their multiplicity. Thus equality on all columns reachable in exactly `m`
steps is necessary and sufficient. For `m=0`, the reference construction
with the two origins is exact. For `m>0`, matching only the origins is
insufficient. A sufficient reference set has at most `2*4^m` distinct
columns, though actual successors can merge.

Equality in (7) is **not necessary to prove an upper bound**. A useful
compression may have positive error; what matters is that its final root
upper value meets the proposed threshold. Equation (6) gives the exact
error quantity to control. Bond dimension and unweighted error norms alone
do not supply that estimate. These identities identify a concrete stability
requirement without assuming that all useful compressions must be exact.

## 4. Exact bounded verification

Run the standard-library checker:

```text
uv run --offline --no-project python experiments/rule30/reference_message_compression.py
```

The [implementation](../../experiments/rule30/reference_message_compression.py)
and [artifact](../../experiments/rule30/reference-message-compression.json)
check the local certificate and complete-word formula on nonnegative
branching MPS controls, including duplicate reference tails and a reference
set equal to the entire word domain. Deliberately invalid left boundaries
are rejected. Integer arithmetic is used for these comparisons.

Additional rational-arithmetic checks use the exact four-labeled spatial
channel at depths one through three. They verify (5), (6), and both the
positive-error and zero-error cases of (7), preserving successor
multiplicities. These are bounded algebra controls, not a new original-start
census, a mixing experiment, or a finite-data proof of the all-length claims.
The balanced-class floor is proved using the previously established mixing
theorem. The artifact records its input source hashes and exact check totals.

The saved run checks 10 compression instances, 848 local and boundary
inequalities, 592 complete-word values, and 10 deliberately invalid boundary
certificates. The error identities are checked in 168 function components
and 15 root comparisons, with 22 positive-error or zero-error successor
controls. No numeric limit is extrapolated from these checks.

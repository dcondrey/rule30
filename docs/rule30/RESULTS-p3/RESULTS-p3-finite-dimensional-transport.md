# Finite-dimensional local transport retains only a bounded input prefix

Date: 2026-09-14. **Allowing singular digit matrices does not repair the
specified homogeneous transport when the three state transports remain
invertible.** In matrix dimension D, every encoded word product depends
only on the word length and its first at most D-1 digits. This is an
all-dimensional theorem, not a search through small matrices.

The theorem extends the
[invertible-symbol classification](RESULTS-p3-multiplicative-transport.md).
It concerns exactly that local matrix-product encoding, not arbitrary
representations or algorithms. Singular state transports, growing or
implicit dimension, and different local laws remain outside its claim.

## 1. Exact statement

Let V be a D-dimensional vector space over any field, D>=1. Assign
invertible matrices L_A,L_B,L_C and arbitrary matrices M_0,...,M_3,
all acting on V. Suppose

```
L_g M_d=M_e L_psi(e),  e=P_g(d),                 (1)
```

for all12 local transitions of the itinerary automaton. Define
M(W)=M_d0 ... M_d(m-1), with M(empty)=identity.

**Theorem.** If two words W,W' have the same length m and the same first
min(m,D-1) digits, then M(W)=M(W').

In particular, for m>=D, changing any digit after the first D-1 cannot
change the product. The matrices may have arbitrary entries, including
rational functions of a spectral parameter; the proof applies over
that field as well.

## 2. Common row space and dimension reduction

Since each L_g is invertible, (1) gives

```
row(M_d)=row(M_e L_psi(e)).                       (2)
```

For a fixed emitted e, the right side is the same for each possible
entering g. The preimages of e=0 include input digits0 and3; those of
e=1 include3,0,2; those of e=2 include2 and1. Therefore all four M_d
have the same row space W, of dimension r.

Every state A,B,C occurs as psi(e). Equation (2) consequently implies

```
W L_g=W for each g.                              (3)
```

Choose an r-by-D matrix R whose rows are a basis for W. There are unique
D-by-r matrices U_d and invertible r-by-r matrices barL_g such that

```
M_d=U_d R,       R L_g=barL_g R.                  (4)
```

The restricted matrices barL_g are invertible because L_g acts
bijectively on W. Substituting (4) into (1), and cancelling the full-row-rank
R using a right inverse, gives

```
L_g U_d=U_e barL_psi(e).
```

Set T_d=R U_d. Multiplication on the left by R proves

```
barL_g T_d=T_e barL_psi(e).                       (5)
```

Thus the smaller matrices obey exactly the same local law. For m>=1,

```
M_d0 ... M_d(m-1)
  = U_d0 T_d1 ... T_d(m-1) R.                    (6)
```

This retains one original digit and moves the remaining product to the
r-dimensional representation. No inverse of a digit matrix is used.

## 3. Induction proving the prefix bound

If r=0, all M_d are zero and every nonempty product is zero. If r=D,
all M_d are invertible. The group classification forces them all equal,
so their product depends only on length.

Otherwise 0<r<D. Apply the theorem inductively to (5). Its tail product
in (6) depends only on the tail length and its first at most r-1 digits.
Including d0, the original product depends on at most r<=D-1 initial
digits. Words shorter than this bound are retained completely.

This proves the theorem by induction on D. The base D=1 is included in
the zero-rank/full-rank cases. There is no assumption that the matrix
rank stays fixed under products: further rank loss is precisely what
the dimension reduction handles.

## 4. A nontrivial singular example and its exact reduction

The theorem does not say that singular M_d must all be equal. Here is
a concrete family satisfying (1).

Use basis states indexed by two-digit words (a,b), so D=16. Let M_d
prepend d and discard the last digit:

```
M_d e_(a,b)=e_(d,a).
```

Let L_g permute these basis states by the complete two-digit K_g action.
The section identity of K gives (1) exactly. Each M_d has rank4.
The encoded product of a word of length at least2 sends every basis
state to its first two input digits, and ignores every later digit.

Its reduction is explicit: R sends e_(a,b) to e_a, U_d sends e_a to
e_(d,a), and T_d=R U_d sends every one-digit basis state to e_d. The
restricted barL_g is the root-digit permutation P_g. One further
reduction leaves a scalar constant. This is an example of the theorem's
mechanism, not a claim that the general bound D-1 is sharp.

There is a collision even among actual seed prefixes: B^0(0) begins000,
while B^8(0) begins003. Their length-three products are identical in
this representation, though their last digits differ. Both chronology
and the matrix identity are checked in the verifier.

## 5. Consequence for the proposed marked-query encoding

For arbitrary input words, a product-only readout of the last digit at
length m requires dimension at least m+1 in this model. Otherwise the
theorem supplies equal products with unequal last digits.

There is also no fixed finite dimension that supplies such a readout
at every prefix length and every time on the actual B zero orbit. Its
prefix periods are unbounded by the
[actual-orbit period bound](RESULTS-p3-autonomous-profile-bound.md).
For any D, a positive-time orbit point returns to zero on its first
D-1 digits but differs from zero at a later digit. Truncate at its
first nonzero digit: the two actual prefixes have equal products and
different last digits. The readout may depend on their common length;
it cannot distinguish them from that product alone.

These conclusions do not cover a decoder supplied separately with the
entire time index and unrestricted computations, or a product augmented
by additional history-dependent information. They are not runtime
bounds for P3. A large matrix dimension can also be described implicitly;
dimension alone is not charged computation. The theorem identifies
exactly what this homogeneous local product loses.

## 6. Independent exact checks

The [verifier](../../experiments/rule30/p3_finite_dimensional_transport.py)
checks the D=16 example on every basis vector for all12 local equations,
both factorization identities in (4), the reduced law (5), and all
64 three-digit products. It separately checks the actual003 witness
using the original integer B evolution followed by Phi.
The [artifact](../../experiments/rule30/p3-finite-dimensional-transport.json)
records those finite checks. The arbitrary-dimensional theorem rests
on the row-space argument and induction above, independently audited.

```
uv run --offline --no-project python experiments/rule30/p3_finite_dimensional_transport.py
```

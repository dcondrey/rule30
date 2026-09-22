# Exact finite-origin quarter-wave extremizers and a failed energy induction

This report gives an all-length construction for **other finite initial
rows**, not for the lone seed. It does not prove or disprove P1, P2, or P3.
It sharpens the controls for the
[quarter-wave potential](RESULTS-quarter-wave-current-target.md): increasing
predecessor depth and a fixed rightmost origin do not by themselves enforce
phase cancellation. The construction also rules out a uniform one-step
squared-energy induction proportional to initial mass. It does **not** rule
out a global bound of the form `P_t^2 <= C t m`.

## 1. Statement, including the initial-condition distinction

For a finite row x use the ordinary integer sum

\[
P(x)=\sum_{m\ge0}(x_{4m+1}-x_{4m+3}).
\]

For every integer n>=1 with n=1 modulo 4, there is a unique row a^(n)
supported in [1-n,0] such that

\[
a^{(n)}_0=1,\qquad a^{(n)}_i=0\ (i>0),
\]

and its Rule 30 evolution satisfies

\[
\boxed{(F^n a^{(n)})_i=\mathbf1_{\{i\equiv1\pmod4\}}
       \quad(1\le i\le n).}
\]

There are no ones at positions i>n. Consequently,

\[
\boxed{P(F^n a^{(n)})=(n+3)/4,\qquad
       P(F^{n-1}a^{(n)})=0.}
\]

The positive initial half-line, including the bit at zero, is identical to
the lone seed in every member of the family. The negative initial half-line
is different and generally contains many additional ones. The initial row
changes with n. This is not a statement about infinitely many exceptional
times on any one fixed initial orbit.

## 2. Explicit construction in the moving right frame

Since the initial rightmost one is at zero, define the right-front
coordinates at time t by

\[
E_j(t)=x_{t-j}^{(t)},\qquad j\ge0,
\]

with E_-1=E_-2=0. Rule 30 becomes the triangular map

\[
(R E)_j=E_j\oplus(E_{j-1}\lor E_{j-2}).
\]

On a prefix of length n this is a bijection. For a prescribed output b,
its inverse is calculated sequentially:

\[
(R^{-1}b)_j=b_j\oplus
  ((R^{-1}b)_{j-1}\lor(R^{-1}b)_{j-2}),\qquad 0\le j<n.
\]

No information from depths >=n enters these equations. Set

\[
b_j=\mathbf1_{\{j\equiv0\pmod4\}},\qquad 0\le j<n,
\]

and compute A=R^{-n}b on that prefix. Define the physical initial row by
a^(n)_(-j)=A_j for 0<=j<n and zero elsewhere. This is an explicit n-by-n
Boolean recurrence, not a search over initial rows. The map fixes coordinate
zero, so A_0=b_0=1. Evolving the full finite row n times gives the desired
prefix b, because the finite-prefix equations close in the depth direction.

For 1<=i<=n the corresponding depth is j=n-i. Since n=1 modulo 4,
`b_(n-i)=1` exactly when `i=1 modulo 4`. This proves the final-row statement.
Finite propagation from the initial rightmost one at zero gives x_i^(n)=0
for i>n. The displayed value of P follows.

## 3. The preceding potential is exactly zero

The right-frame prefix at time n-1 is v=R^-1 b. The inverse recurrence
above evaluates explicitly to

\[
v_0=1,\qquad
v_j=\begin{cases}0,&j>0\text{ and }j\equiv0\pmod4,\\
                 1,&\text{otherwise}.
      \end{cases}
\]

Its depth word begins `1111 0111 0111 ...`. The formula follows directly
by induction over four-cell blocks in the inverse recurrence.

At time n-1=0 modulo 4, every positive odd physical position i<=n-1
corresponds to an odd depth j=n-1-i. All those v_j equal one. There are
equally many positive positions congruent to 1 and 3 modulo 4, and no
ones to the right of n-1. Hence P(F^(n-1)a^(n))=0, including the empty
positive interval when n=1.

The smallest non-seed example is n=5, with initial word `11111` on
[-4,0]. Its positive row at time four is `1111`, with P=0. Its positive
row at time five is `10001`, with P=2.

## 4. An all-length obstruction to a particular energy induction

Let m_n be the Hamming weight of a^(n). Since m_n<=n,

\[
\frac{P(F^n a^{(n)})^2-P(F^{n-1}a^{(n)})^2}{m_n}
=\frac{(n+3)^2}{16m_n}
\ge\frac{(n+3)^2}{16n}\longrightarrow\infty.
\]

Thus there is no absolute constant C such that

\[
P(F^{t+1}a)^2-P(F^t a)^2\le C\,\#\{i:a_i=1\}
\]

for every finite row a supported on the nonpositive half-line with a_0=1
and every time t. The same argument applies with initial width in place
of initial mass, because that width is also at most n in the family.

This rejects a one-step induction. It does not reject the weaker global
estimate `P(F^t a)^2 <= C t m`, because a large final injection can follow
many low-energy times. The construction proves no divergence of
`P(F^n a^(n))^2/(n m_n)`.

Similarly, for every c<1/4 and every fixed C, some family member violates
`P(F^t a)<=ct+C`. Here C must be uniform over the family. This does not
reject a bound with a constant depending on the entire initial row. In
particular, it does not reject such a bound for the single designated seed.
It does show why retaining only the common initial right half-line is
insufficient for a uniform bound that ignores the initial left half-line.

### A bounded finite-window additive correction cannot repair this drift

The same family also rules out the following proposed repair. Fix any window
length r and any four real functions phi_a on r-bit words, normalized by
phi_a(0^r)=0. Let

\[
Q(x)=\sum_{i\in\mathbb Z}\phi_{i\bmod4}(x_i,\ldots,x_{i+r-1}),
\qquad E(x)=P(x)^2+Q(x).
\]

Put B=max_(a,w)|phi_a(w)|. At times n-1 and n the family rows have support
in intervals of lengths at most 3n-2 and 3n. Only windows intersecting
those intervals can contribute, so

\[
|Q(F^n a^{(n)})-Q(F^{n-1}a^{(n)})|
\le B(6n+2r).
\]

It follows that

\[
E(F^n a^{(n)})-E(F^{n-1}a^{(n)})
\ge (n+3)^2/16-B(6n+2r).
\]

This is quadratic in n, whereas initial mass is at most n. Consequently no
choice of fixed r and fixed coefficients yields a uniform drift bound
`E(F^(t+1)a)-E(F^t a)<=C m(a)` on all the finite left-supported origins
considered here. The argument is symbolic for every r; it is not a finite
window search extrapolation. It also applies if Q is summed only over the
nonnegative half-line.

This statement does not cover nonlocal corrections, coefficients growing
with observation scale, or a drift bound restricted to the lone-seed orbit.
It remains distinct from an obstruction to a global bound `P_t^2<=C t m`.

### Including the cosine quadrature does not give a uniform drift bound either

The first family alone does not rule out a useful repair. Define

\[
C(x)=\sum_{i\ge1}\cos(\pi i/2)x_i,\qquad
E_{\rm vec}(x)=P(x)^2+C(x)^2.
\]

For its n=4m+1 members, the two successive vectors are
`(P,C)_(n-1)=(0,1-m)` and `(P,C)_n=(m+1,0)`. Thus the vector energy
injection is only 4m=n-1: the missing cosine component stores most of
the apparent sine-energy jump. This makes testing the repair necessary.

A second explicit family supplies that test. Let n=8m+1 and prescribe
the right-frame terminal prefix

\[
b=(1100)^\infty\big|_{[0,n)}.
\]

Construct the finite initial prefix A=R^-n b by the same inverse
recurrence. Its rightmost bit is again one and its physical support lies
in [1-n,0]. Direct substitution in the inverse recurrence shows

\[
R^{-1}b=(10110000)^\infty\big|_{[0,n)}.
\]

At time n the physical positive row occupies residues 0 and 1 modulo 4.
At time n-1=8m, the inverse word has one positive sine contribution per
eight cells, and cancelling positive and negative cosine contributions.
Counting the residues, including the right endpoint, gives exactly

\[
(P,C)_{n-1}=(m,0),\qquad (P,C)_n=(2m+1,2m).
\]

Therefore

\[
\boxed{\Delta E_{\rm vec}=7m^2+4m+1.}
\]

The initial mass and width are at most n=8m+1. Their ratios with this
energy injection are unbounded. Thus including both quadratures does not
restore a uniform initial-mass or initial-width one-step drift bound over
these finite origins. Adding a fixed bounded finite-window correction
still changes the drift by only O(n), so the preceding correction argument
applies to this vector energy as well.

This does not disprove a global estimate `P_t^2+C_t^2<=C t m`, or a
seed-specific energy argument. The second family is, like the first,
a sequence of different initial rows selected for their finite terminal
behavior.

## 5. The power-of-two subfamily necessarily has growing initial complexity

For arbitrary initial data, depth j of R has a period dividing 2^j.
Indeed, depth zero is fixed. If all earlier coordinates repeat after
2^(j-1) steps, the forcing `E_(j-1) OR E_(j-2)` repeats after that period;
running its XOR accumulation through two periods restores coordinate j.
This induction also proves the statement uniformly on finite prefixes.

Take n=2^k+1 with k>=2. Since 2^k fixes the first k+1 coordinates of R,

\[
(R^{-n}b)_j=(R^{-1}b)_j\quad(0\le j\le k).
\]

The explicit inverse in section 3 therefore supplies the lower bounds

\[
\boxed{m_n\ge k+1-\lfloor k/4\rfloor,\qquad
       \operatorname{width}(a^{(n)})\ge k.}
\]

Thus this subfamily escapes every fixed finite initial row in both mass
and width. This is a logarithmic lower bound, not a claimed asymptotic
formula for either quantity. It does not determine the mass dependence
required by a possible global energy estimate.

## 6. Verification and scope

The [constructor and verifier](../../experiments/rule30/quarter-wave-phase/finite_origin_extremizers.py)
implements the inverse recurrence and independently evolves physical
coordinate sets using the original Rule 30 gate. It checks every row of
each sampled history, the prescribed positive terminal row, zero preceding
potential, and the initial-complexity bound where applicable.

Reproduce the [finite JSON record](../../experiments/rule30/quarter-wave-phase/finite-origin-extremizers.json):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/quarter-wave-phase/finite_origin_extremizers.py \
  --output experiments/rule30/quarter-wave-phase/finite-origin-extremizers.json
```

The record samples n=1,5,9,13,17,21,33,65,129,257. These finite checks
support the implementation; sections 2-5 are the all-length proofs.
For n=257 the initial mass is 134, P_256=0 and P_257=65, giving an
energy injection of 4225 and injection/mass of 4225/134.
The second family is independently checked at n=1,9,17,33,65,129,257,
including the exact predecessor word and both quadratures at the final
two times.

The actual lone-seed quarter-wave estimate, any global initial-mass energy
bound, and the centered-current estimate needed for P2 remain unproved.

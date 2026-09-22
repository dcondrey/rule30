# Exact two-column Cartier composition of the actual B history

Date: 2026-09-14. **Two successive spatial-column evaluations admit an
exact temporal decimation.** The two abelian output bits become prefix
sums of even-time drivers; the central bit acquires a computable ordered
correction. All three macro coefficients simplify to local functions of
two adjacent physical digits in the current even-time row. Neither an odd
carry argument nor an orientation variable remains in those coefficients.

This constructs a temporal block action. It does not provide a cheap
construction of its input row or an all-scale sublinear center query.
An actual closed retained-state cycle has nonzero central correction,
so that correction is not a coboundary of the specified endpoints.
The cycle is off the marked center-query diagonal; a cancellation
restricted to that diagonal remains open.

The [verifier](../../experiments/rule30/p3_parity_string_cartier.py) and
[artifact](../../experiments/rule30/p3-parity-string-cartier.json) contain
the complete local checks, a supplied-history paired evaluator, and
controls using previously saved actual B orbits. This result concerns P3;
it proves no period exclusion.

## 1. Physical histories and the parity-string lift

Use the itinerary automaton B from
[the conjugacy report](RESULTS-p3-itinerary-conjugacy.md). Write its actual
zero history as

```
x_j(t) = digit_j(B^t(0)),       j>=0, t>=0,
x_j(0) = 0.
```

The virtual digit on the left is 1 at every update. If z is the already
emitted upstream digit and x the old current digit, the new current digit
is -x for z=0, x+1 for z=1, and 3-x for z=2 or3, modulo4.
The driver is evaluated at positive time t, after that upstream digit
has been updated. This chronological convention retains the original
B boundary and every intermediate row.

One can dress the temporal reflections by their cumulative orientation.
Equivalently, lift each nonvirtual column to three bits X=(U,V,W),
initialized at 000, with physical decode

```
low(X)  = U,
high(X) = W+U+UV.                                    (1)
```

All additions below are XOR and products are pointwise bit products.
This is an augmented representation: different triples can decode to
the same physical digit. Actual history fixes the lift by its initial
state and the recurrence; no lift is freshly selected during a block.
For an upstream physical digit z=p+2q, let

```
c = p OR q,          d = 1+q.
```

The current-column temporal update is

```
(U,V,W) -> (U+c, V+d, W+cV).                          (2)
```

Indeed, decoding the output in(2) gives the indicated physical
permutation. For a lifted upstream column its outgoing drivers are

```
C(X) = U OR W,
D(X) = 1+W+U+UV.                                     (3)
```

Equations(1)--(3), the zero initial row, and the fixed virtual digit prove
the forward-B identification by induction in time and then left to right
within each row. They are complete local identities, checked on all64
upstream/current lift assignments. At the virtual boundary one may use
the fixed lift(1,1,0), which decodes to1 and supplies c=d=1. The first
physical column has the exact lifted history

```
X_0(t) = (t mod2, t mod2, floor(t/2) mod2).
```

## 2. The cancellation and its time phase

For positive-time histories define the inclusive prefix integral

```
(Kf)(t)   = sum_(1<=s<=t) f(s),
(K^-f)(t) = sum_(1<=s<t) f(s).
```

These are not the exclusive-at-zero convention. Starting a nonvirtual
first column at 000 gives U=Kc, V=Kd, W=K[c K^-d]. For its pre-update
carry(U,V,W) define

```
g = c(1+W+UV),
f = c+d(U+c).                                        (4)
```

Direct expansion of(2)--(3) proves, for all8 carries and all4 inputs(c,d),

```
C(X_new)+C(X_old) = g,
D(X_new)+D(X_old) = f.                               (5)
```

No admissibility assumption c OR d=1 is needed for this identity. Since
C(000)=0 and D(000)=1, it follows that C=Kg and D=1+Kf.
If the second column has lift(P2,V2,Q2), its first two coordinates are

```
P2(t) = (K^2 g)(t),
V2(t) = (t mod2)+(K^2 f)(t).                         (6)
```

One way to expose the cancellation before(5) is the exact shuffle rule

```
(Kc)(Kd)=K[c K^-d]+K[d K^-c]+K[cd].                  (7)
```

Consequently W cancels from D's integrated expression:
D=1+K[c+dU_new]. Products here are Hadamard products of histories,
not Cauchy products. Equation(7) partitions a pair of summation indices
according to their order, including equality.

Counting the appearances of f(s) in K^2f proves the Cartier identities

```
(K^2f)(2u)   = sum_(r=1..u) f(2r),
(K^2f)(2u+1) = sum_(r=0..u) f(2r+1).                 (8)
```

Equations(6)--(8) are the all-length two-column cancellation. They
advance two spatial columns and decimate temporal sampling. They do
not themselves halve the requested spatial index. The separate
[two-field blocking](RESULTS-p3-b-two-channel-block.md) has that
additional index-reduction statement.

The identities C=Kg and D=1+Kf use a nonvirtual zero initial column.
They do not hold with those constants at the fixed virtual column,
where C=1. In particular pairing its constant drivers gives the
macro action(0,0,1), which is the correct B-squared root toggle.

## 3. The complete paired action and its physical coefficients

At coarse time r, let Xodd=X(2r-1) and Xeven=X(2r). Evaluate g_r,f_r
by(4) using Xodd and the fine input at2r. Set

```
E_r = C(Xeven)D(Xodd).                               (9)
```

The exact update of the second-column lift at even times is

```
(P,V,Q) -> (P+g_r, V+f_r, Q+g_r V+E_r).             (10)
```

Proof: compose the two fine actions driven by(Codd,Dodd) and
(Ceven,Deven). Their first two coefficients are their sums, which
are g_r,f_r by(5); the ordered central coefficient is Ceven Dodd.
The order of this product matters.

There is no need to recover Xodd if Xeven=(U,V,W) and the even input
(c,d) are supplied. Inverting one application of(2) in(4),(9) gives

```
g = c(1+W+UV+Ud),
f = c+dU,
E = U(W+V)+c(U OR W)+dU.                            (11)
```

More strongly, let p+2q be the upstream physical digit and a+2b the
current physical digit, both in the updated even-time row. With
c=p OR q, substitute b=W+U+UV into(11):

```
g = c(1+b+aq),
f = c+a(1+q),
E = ab+c(a OR b)+aq.                                (12)
```

All orientation dependence cancels. For E alone this says: upstream
digit0 gives ab; upstream digit1 gives a+b; upstream digit2 or3 gives b.
The full16-row table is retained in the artifact. Finally, if A+2B
is the old physical target digit, decoding(10) yields

```
A' = A+g,
B' = B+E+g+fA'.                                     (13)
```

Thus the eight class-two actions have a direct physical interpretation,
and a two-step sweep can use two adjacent updated even-row digits.
The enlarged alphabet legitimately includes(0,0,E). This is a finite
local temporal block rule, not a proof that the dependency radius or
input construction remains bounded after arbitrarily many doublings.

The physical rule is exactly the previously saved one-pass B-squared
kernel in [bitplane temporal squaring](RESULTS-p3-bitplane-temporal-squaring.md):
its coefficients F,T satisfy g=F, f=T, and E=g(1+f)+fb.
Substitution in(13) gives B'=B+f(A+b), using the old target low bit A.
The verifier checks these equalities on all16 neighboring-digit pairs.
The new content here is the two-column Cartier organization and its
central correction analysis, not a separate physical acceleration.

## 4. Actual ancestry controls and central holonomy

The saved [three-digit zero orbit](../../experiments/rule30/p3-autonomous-profile-bound.json)
has exact period32. Its first digit supplies the fine drivers
11,10,10,01 repeatedly. The first nonvirtual carry downstream of
that digit has the exact eight-step cycle

```
000 ->110 ->011 ->110 ->100 ->010 ->111 ->010 ->000.
```

Together with root phase modulo4 this is a closed actual trajectory.
The four paired coefficients are

```
(g,f,E) = (0,1,1), (0,1,1), (1,1,1), (0,0,0).
```

Thus the ordinary fine-driver restriction g OR f=1 is not preserved.
The last macro is simply the identity; it is valid in the enlarged
alphabet, rather than a contradiction to the paired construction.

A stronger control drives the construction with actual digit j=1
at times1 through32 of the saved cycle. The first carry is then
column2 and the second is column3. The retained state

```
(time mod32, U,V,W, P2,V2)
```

starts and finishes at allzero. The sixteen central corrections are

```
1,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0,
```

whose XOR is1. The accumulated g_r V2(2r-2) term is0, so the
second central coordinate ends at Q2=1. Its physical digit is2.
This agrees with the separately saved original-integer check
B0^32(0)=128 modulo256 and itinerary prefix0002 in
[the two-field artifact](../../experiments/rule30/p3-b-two-channel-block.json).
The new verifier reuses those exact data and checks all32 saved
three-digit successor edges; it does not generate a new center census.

If E_r were F(retained_after)+F(retained_before) on the stated actual
retained-state graph, its sum around this closed cycle would be0.
It is1, so such an endpoint cochain does not exist. This includes a
cochain depending on time phase modulo32. It does not exclude an
unrestricted absolute-time function, a larger retained state, or a
cheap evaluation of this periodic correction. Time32 at column3 is
off the marked center-query diagonal; a diagonal-specific cancellation
is also not excluded. The artifact additionally preserves two short
supplied-history endpoint collisions, explicitly without actual-ancestry
claims.

The six coefficient signatures occurring in(12) are not themselves an
autonomous state for further B-squared updates. On the actual orbit,
the first pair22 at time2 and03 at time4 both have signature(0,1,1).
Their successors at times4 and6 are03 and23, whose signatures are
(0,1,1) and(1,1,1). A phase-aware extension remains open.

## 5. What this computes, and what still costs work

Given a supplied upstream fine history of length N, the paired
evaluator performs N first-carry updates and floor(N/2) second-column
macro updates. For odd N it performs one final ordinary second-column
update. It shares the first carry and computes g,f,E together. A
streaming version uses constant carry storage; the verifier retains
records to make every step reviewable.

If instead the required adjacent even physical digits are already
supplied, equation(12) computes all coefficients from them directly.
Odd samples and parity strings are not logically indispensable inputs
to that local evaluation. Constructing those even physical digits is
still unpaid by the local identity. The current supplied-history
implementation reads all N fine inputs and performs O(N) local Boolean
operations. Its saved trace allocation and integer time metadata are
charged separately; a parity-only streaming implementation does not
need those records.

No bound such as T(n)<=T(n/2)+T(n/4)+polylog(n), or any branching
rate below2, follows. The remaining constructive task is to produce
the needed even-row pair observations and aggregate their ordered
central corrections with less work than a full fine-history pass.
The physical formula(12) specifies the observations precisely; the
actual holonomy identifies one endpoint-only compression that cannot
supply them. Neither result solves P3.

Verification comprises64 local physical identities,32 derivative and32
post-state identities,64 physical coefficient identities,16 existing-kernel
equivalences,1024 complete
two-step carry cases,64 physical macro cases,16 shuffle increment
identities,64 Cartier basis controls, and the specified saved-orbit
and supplied-history controls. The all-length conclusions follow from
the algebra and induction above, not from extrapolating those finite
implementation checks.

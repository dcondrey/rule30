# Triangular powering of the finite P3 core: exact cycles and charged phases

Date: 2026-09-13. **Finite H orbits have an exact constructive transient/cycle
normal form. Their periods are powers of two, with an all-length spacing
restriction on period doublings.** This supports exact large-time queries
after a width-dependent construction. It does not give a sublinear singleton
center algorithm. Two actual seed-core examples show that discarding the
transient, or extrapolating the eventual cycle backward, gives a wrong
center bit.

The [verifier](../../experiments/rule30/p3_triangular_core_power.py) and
[artifact](../../experiments/rule30/p3-triangular-core-power.json) contain
complete per-column certificates, including every transient and periodic
seam. No long center prefix, paid compute, or finite-state census is used.

## 1. The triangular system and a constructive normal form

Use the [bulk-core map](RESULTS-p3-bulk-core-formula.md)

```
H(x)=(x>>2) XOR ((x>>1) OR x).
```

For a nonnegative finite integer with bits x_j(t),

```
x_j(t+1)=x_(j+2)(t) XOR (x_(j+1)(t) OR x_j(t)).    (1)
```

The highest one stays fixed, so H preserves the width w of every positive
input. The two coordinates above the width are identically zero. At a
lower coordinate, write u=x_(j+2), v=x_(j+1), z=x_j. Its update is

```
z' = u XOR z       when v=0;
z' = 1 XOR u      when v=1.                        (2)
```

This is the existing reset/toggle mechanism; the four-map monoid itself
is already recorded in [aggregate affine blocks](RESULTS-p3-aggregate-affine-blocks.md).
The new conclusions below use the relations between consecutive Rule 30
coordinates, rather than treating their drivers as arbitrary.

Suppose the entire upper prefix has an eventual primitive period P from
a certified time T. Compose (2) over its next P updates. Exactly one of
the following occurs:

| Return map on z | Condition | Extended prefix period | Safe new start |
|---|---|---:|---:|
| Constant | v has a1 in the cycle | P | T+P |
| Identity | v is zero and the P values of u have even parity | P | T |
| Toggle | v is zero and the P values of u have odd parity | 2P | T |

The prefix period cannot fall, since that prefix remains part of the
extended state. In the toggle case z(t+P)=1-z(t), so the new period is
exactly2P. An identity return can yield distinct lifted cycles depending
on the entering bit; no unique-attractor assumption is made.

This gives an exact algorithm. Start at the highest bit and retain each
coordinate's complete transient followed by one periodic block. Obtain
the next return map from the already constructed upper sequences; advance
the new bit from its given initial value to the safe new start, and save
one full block. Evaluation at time k reads the transient if k<T, and
otherwise reads index T+((k-T) mod P). The table contains the phase; it
is not supplied externally.

Correctness is inductive in the coordinates. Once the full upper prefix
is periodic, the displayed unary return map proves the new seam closes.
The saved recurrence through the seam then proves every later update by
induction in time. The checker validates precisely these finite edges.
It accepts no promise that a large enough-looking table is periodic.

Starting with P=1, every final primitive period is P=2^q. Each reset adds
at most the current P to the certified transient. As periods only grow,

```
actual transient mu <= certified T <= (w-1)*P.     (3)
```

The top bit adds no transient. These are all-length bounds; neither P nor
mu is asserted to be polynomial in w.

The input0 is fixed and has width0, transient0, and period1. The verifier
handles it with an empty coordinate list rather than applying a positive
width formula to a nonexistent highest bit.

## 2. Period doublings require spatial separation

**Theorem.** For every positive H-cycle of width w, its primitive period
P satisfies

```
P=1                                      if w<=3;
P <= 2^floor((w+5)/7)                     if w>=4.  (4)
```

Proof. The top three coordinates settle to110, read from high to low.
The next coordinate toggles. Thus the first possible period doubling is
at width4.

Consider any subsequent extension that doubles an upper primitive period
P to R=2P. Call that new coordinate d. Its immediate upper neighbor is
identically zero, and d(t+P)=1-d(t). In particular d is nonconstant and
has primitive period R. Denote its successive lower neighbors e,f,g,h,i.
The local equations on a periodic orbit imply

```
e(t+1)=e(t) OR d(t),             hence e is identically1;
f(t+1)=1-d(t),                  so f has primitive period R;
g(t+1)=1-(f(t) OR g(t));
h(t+1)=f(t) XOR (g(t) OR h(t));
i(t+1)=g(t) XOR (h(t) OR i(t)).                    (5)
```

The third equation prevents g from being identically0 or identically1:
the first would force f identically1, and the second would update to0.
Thus d,e,f,g are all nonzero temporal columns. By the return-map criterion,
no new doubling can occur at positions1 through4 below d. Every pair of
doublings therefore has distance at least5.

There is a stronger restriction when R>=4. If h were identically0, its
equation would give f=g. Comparing the f and g updates then gives d=f
and f(t+1)=1-f(t), contradicting its primitive period R>=4. Thus h is
nonzero. If i were identically0, then g=h. Comparing their updates gives

```
1-(f OR g) = f XOR g.
```

The Boolean equality holds only when f=g=1, contradicting the already
proved nonconstancy of g. Thus i is also nonzero. The first six positions
below d consequently have nonzero immediate upper drivers and cannot
double the prefix period. After a doubling to period at least4, the next
doubling is at least seven positions away.

The first doubling needs width4, the second needs at least4+5=9, and
each later doubling needs seven additional coordinates. If q>=2, this
gives w>=9+7(q-2)=7q-5. The q=1 and q=0 cases also satisfy (4).
This proves the bound without asserting that the minimum gaps are attained.

These arguments concern primitive periods of entire upper prefixes.
Individual columns may have shorter periods or may be constant. Such
columns and identity-return splits do not invalidate the argument.

There is consequently a uniform finite-width iterate identity. Let P_w
be the right side of (4), with P_w=1 for w<=3, and put
T_w=max(w-1,0)*P_w. All cycle periods are powers of two dividing P_w, and
(3) puts every transient below T_w. Hence as maps on [0,2^w),

```
H^(T_w+P_w)=H^T_w.                                (4a)
```

For k>=T_w it is safe to replace k by T_w+((k-T_w) mod P_w). For k<T_w
the routine keeps k unchanged. The implementation supplies this second
powering algorithm, with no per-input phase discovery: compute the proved
width bound and execute every remaining H step. It agrees with the
independently constructed column normal forms. The equality concerns
H's integer action; it is not equality of the literal Q words or their
full actions on arbitrary nonzero tails.

## 3. No fixed temporal period covers arbitrarily large widths

There is also a lower restriction that holds for every positive periodic
state, not merely a selected attractor:

```
w <= 4^P-1.                                         (6)
```

Here w is the actual highest-one position plus1, not an arbitrarily
padded buffer width. The uniform upper bound (4a) can use a larger
ambient width; this lower bound cannot.

Proof. Encode a temporal column over P times by a P-bit word. For three
consecutive spatial columns u,v,z, (1) gives

```
u(t)=z(t+1) XOR (v(t) OR z(t)),  with time modulo P. (7)
```

Hence every ordered target pair (v,z) has exactly one predecessor (u,v).
Begin with the two zero columns above the highest bit. The first nonzero
column is the constant1 column. Along the subsequent spatial path, no
ordered pair can repeat: applying the unique predecessor repeatedly
would propagate any repetition back to the initial zero pair. That pair
has itself as its only predecessor, which is incompatible with the path
having left it through a nonzero column. Likewise the path cannot return
to the zero pair.

The w pairs ending at the w coordinates of the positive state are
therefore distinct nonzero elements of a set with4^P elements. This proves
(6). In particular periods are unbounded as the width grows. This does
not refute a polynomial upper bound for period or transient, and it does
not address a center query whose input width also grows with its time.

The same pair representation gives an exact directed spatial test at
fixed P: a nonzero immediate driver yields one continuation; a zero
driver with odd parity prevents a P-periodic continuation; an even one
gives two. No repeated-pair shortcut occurs on a path descending from
the finite zero boundary, by the preceding argument. Thus waiting for a
spatial cycle is not a valid compression strategy for these paths.

## 4. Actual singleton cores invalidate premature cycle reduction

The bulk theorem represents the singleton query using an initial core
U=C^L. Its integer x=U(0) has width exactly2L. The relevant H iteration
count is L-1 for the odd query and L-2 for the even query. These counts
need not reach the eventual cycle of x.

For L=6, x=3204 has the exact orbit

```
3204,3559,3214,3564,3205,3558,3214,...
```

Its transient is2 and period4. The actual query c_11 is bit0 of H^5(x),
which is0. Replacing5 by5 mod4=1 gives bit0 of3559, which is1. The
period is correct, but dropping the transient loses the phase.

For L=10, x=820716 has transient10 and period4. The actual even query
c_18 is bit1 of H^8(x). It equals bit1 of820681, which is0. Extending
the eventual cycle backward with

```
10+((8-10) mod4)=12
```

instead selects H^12(x)=820683, whose bit1 is1. This is a failure even
when the eventual cycle's phase is retained: the queried time precedes
the transient. The complete fourteen-state orbit is saved and every edge
and the final return are checked. The corresponding odd query at time19
happens to agree with this backward extrapolation at bit0; no contrary
claim is made for that bit.

Both wrong answers are checked against independent singleton row
evolution at the two specified query times. They refute these particular
cycle shortcuts, rather than faster ways of constructing the correct
transient or requested observable.

## 5. Cost and precise remaining scope

At each coordinate the construction inspects a driver period and writes
a transient plus periodic block. With final period P and the bound (3),
the implementation uses O(w^2 P) elementary Boolean updates and table
entries. Time-index arithmetic adds its usual bit cost. Once the tables
exist, a query reads w indexed bits; reducing a binary time index k costs
O(log k) bit work per coordinate in a straightforward implementation.
The code assembles those bits into one binary string and converts it to
an integer, charging the additional O(w) output construction.
The construction and storage are both charged. The bound (4) remains
exponential in w and does not establish a polynomial transient algorithm.

The uniform routine from (4a) needs at most min(k,w*P_w) explicit H
updates for positive w, O(w) bits of state, and the time-index arithmetic.
A single explicit-width update costs O(w) bit operations, giving
O(w*min(k,w*P_w)) update work. The zero input is immediate. This is a
valid large-time shortcut for fixed width, but at k proportional to w
the theorem need not skip any update.

For the singleton input, explicitly materializing C^L(0) already writes
2L bits. Straight iteration of C costs O(L^2) bit operations. Thus this
explicit-integer normal form cannot establish an o(n) center algorithm
merely by making its later time index inexpensive. A representation that
works directly from the compressed word C^L and produces only the
requested bit could avoid that materialization; no such bound is proved
by the present construction.

The artifact contains five complete all-time column certificates at the
directed inputs0,1,222,3204,820716; 165 direct integer-step controls; both
actual-core counterexamples; and three deliberately corrupted certificates
that the checker rejects. The all-length conclusions follow from (1)-(7),
not from the size of these finite controls. No uniform polynomial bound,
sublinear singleton algorithm, or period exclusion is claimed.

```
uv run --offline --no-project python experiments/rule30/p3_triangular_core_power.py
```

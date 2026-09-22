# Query-specific suffix replacement and an exact half-width core

Date: 2026-09-13. **Two sound observational rewrites yield a smaller exact
query representation. They do not yet yield faster asymptotic computation.**
This report proves a sharp suffix-replacement rule and combines it with
zero-prefix deletion to implement the actual singleton center query on a
core of length floor(n/2)+1. Every boundary value required by the update is
retained. The resulting algorithm still performs n-1 one-bit section
advances, grouped into two-step updates.

The [verifier and evaluator](../../experiments/rule30/p3_query_cone_rewrite.py)
and [artifact](../../experiments/rule30/p3-query-cone-rewrite.json) charge
grammar construction and cuts. The optional contextual pair normalizer is
also implemented and charged. No arbitrary-precision operation, supplied
history, or precomputed answer is treated as free.

## 1. The exact meaning of a word and its query

Use the three states from the [section report](RESULTS-p3-dyadic-sections.md):

```
A=(A,C), B=(A,C)swap, C=(B,C)swap.
```

Words act in chronological order: UV means apply U, then V. Let p(U) denote
the parity of its B and C letters, which is its root toggle. Let T(U)=U|_0
be its section on one zero input bit. Then

```
T(UV)=T(U) section(V,p(U)).
```

For a zero tail, the bit at position m of U(0) is p(T^m(U)). After the first
seed input bit1, the original query at n>=1 is

```
c_n = bit_(n-1)(C^n(0)).
```

Positions count from the low bit, starting at zero. All identities below
concern the actual ordered action or the explicitly specified output bit.

## 2. Sharp suffix homogenization

**Theorem.** If V has t letters, then for every input x, prefix U, and
m>=2t,

```
bit_m((UV)(x)) = bit_m((U A^t)(x)).                     (1)
```

Thus the last t generator labels can be replaced by a single repeated-A
expression for this query. This is generally not equality of full maps.

Proof. On the same input, A,B,C differ only at output bits0 and1. Each
generator's output at j>=2 uses only input bits j,j-1,j-2. If two inputs
agree above bit d, their outputs agree above d+2, apart from possible new
boundary discrepancies at bits0 and1. Compare V with A^t on the common
input U(x). After one letter their discrepancy is confined to bits<=1;
after t letters it is confined to bits<=2t-1. This proves (1), without
assuming anything about x or independence of intermediate values.

The threshold is sharp at every t>=1. Set U empty, x=0, and
V=C A^(t-1). Then V(0) has highest one at 2t-1, whereas A^t(0)=0. The bit
immediately below the threshold differs. This explicit family prevents
silently making the replacement one bit too early.

## 3. Both ends can be simplified, with different justifications

Since A(0)=0, a chronological leading run A^q can be removed exactly on
the zero input. This is the [zero-prefix rewrite](RESULTS-p3-query-pruning-zero-prefix.md).
An interior A cannot in general be removed: its entering input need not
be zero.

For the full actual section after the j-bit seed prefix 1 0^(j-1), with
1<=j<=n, that leading run has exactly floor((j-1)/2) letters. Removing it
leaves

```
L = n-floor((j-1)/2),    remaining query index m=n-j.
```

Applying (1) to the last t=floor(m/2) letters leaves an essential prefix
of length

```
L-t = n/2+1                              if n is even;
       (n+1)/2 or (n+3)/2                if n is odd.
```

The two identities therefore do not recursively halve the active prefix
as j increases. They preserve a core of roughly half the original length.
The appended A-run is retained implicitly; it still affects the requested
bit through its action on the preceding output.

## 4. Closed two-step core updates

The short alternating widths can be combined into one fixed-width update.
Assume U begins with C. Define

```
a=p(U)=bit_0(U(0)),    b=p(T(U))=bit_1(U(0)).
```

The word T^2(U) begins with A; if U has a second letter, its section is C.
Indeed, C|_00=A and C sends the low input00 to11, while every generator's
section at11 is C. Delete that leading A, and write the resulting word as
tail(T^2(U)). Define

```
R(U) = tail(T^2(U)) append (C if b=1 else A),
Q(U) = tail(T^2(U)) append (C if b=1 else B if a=1 else A).  (2)
```

Both preserve the length and a leading C for words of length>=2. Their
boundary bits a,b are computed from the core itself. They are not free
scalars or independently selectable seam conditions.

For t>=1 the exact query identities are

```
bit_(2t+1)((U A^t)(0))
    = bit_(2t-1)((R(U) A^(t-1))(0)),
bit_(2t)((U A^t)(0))
    = bit_(2t-2)((Q(U) A^(t-1))(0)).                     (3)
```

To prove them, take two successive zero sections. The first letter of the
old known A-suffix becomes A|_(a,b), which is A,B,C,C for low-two-bit
values0,1,2,3. Replace the remaining t-1 suffix letters using (1) at the
new target index. For the even-index case, retain this A/B/C letter
exactly, giving Q. For the odd-index case, it is also safe to replace its
B by A: B and A differ only at bit0, and the remaining t-1 letters cannot
carry that difference above bit2t-2, below the target2t-1. This gives R.
Finally remove the leading A on the zero tail. These operations establish
(3) with the required boundary information retained.

The odd-index B case is essential. For U=CA and t=1, the original
CAA(0)=51 has bit2 equal to0. The correct Q(U)=CB has root bit0; using
R(U)=CA instead would give root bit1. This case is included among the
arbitrary-core controls.

Consequently, for h>=1,

```
c_(2h) = bit_1((R^(h-1)(C^(h+1)))(0));
c_(2h+1) = bit_0((Q^h(C^(h+1)))(0)).                   (4)
```

The odd formula also holds at h=0, giving c_1=1. Handle c_0=1 directly.
The first formula starts with the homogeneous suffix replacement at
m=2h-1, while the second starts at m=2h. Repeated use of (3) proves (4)
at all lengths. The code implements these recurrences, including a and b.
No asserted auxiliary-frontier ancestry or P1 guard is substituted into
this computation.

## 5. Contextual pair cancellation can be composed with these rewrites

The [pair normalizer](RESULTS-p3-observable-rewrite-pairs.md) can replace
subwords conditionally on their actual entering low bits. It preserves
the full output U(0), so replacing U by its normalized word also preserves
(U A^t)(0). The specific table also preserves the core's leading-C
precondition: at incoming residue0, CA normalizes to CA and CB/CC
normalize to CB. A one-letter C is unchanged at that residue. Pair
normalization preserves length as well. It is therefore sound to normalize
each core before (2).
This justifies the integrated implementation rather than assuming that
two separately correct-looking summaries compose.

The three directed integration controls are n=8,17,32. At n=32:

| Construction | Grammar nodes | Distinct section subqueries | Additional pair-transduction subqueries |
|---|---:|---:|---:|
| Half-width core | 437 | 317 | 0 |
| Core plus contextual pair pass | 385 | 209 | 222 |

The normalizer creates useful equal subexpressions and reduces the first
two counts, but the paid total of section and transduction subqueries
rises from317 to431. Cuts and concatenations are also recorded separately.
The original unpruned section evaluator has205 nodes and246 section
subqueries at this same n, so the smaller expanded core has not translated
into a better shared expression at this control. None of these finite
counts is used as an asymptotic lower bound.

A directed [canonical-tree implementation](../../experiments/rule30/p3_query_balanced_slp.py)
then separates incidental tree shape from word content. Every node is split
at the largest power of two strictly below its expanded length; memoized
concatenations and cuts preserve this shape without flattening the word.
Equal words consequently have the same node regardless of their original
parenthesization. This follows by induction on their unique root split.
All recursive rebalancing operations are charged; no logarithmic bound on
rebalancing is assumed.

| n | Original evaluator nodes | Unbalanced core nodes | Canonical core nodes |
|---:|---:|---:|---:|
| 8 | 32 | 35 | 29 |
| 17 | 99 | 129 | 86 |
| 32 | 205 | 437 | 244 |

At n=32 the canonical core removes193 nodes but still exceeds the original
representation. Its defined bookkeeping count of section/concatenation/
split/intern/cut requests is1255 versus1274 for the unbalanced core and758
for the original. These are explicit operation-request counts, not a
running-time theorem. Adding contextual pair normalization to the canonical
core gives322 nodes and remains more expensive. The
[artifact](../../experiments/rule30/p3-query-balanced-slp.json) retains all
six variants at these same three directed queries, plus fixed split and
association controls. This check does not extend the query range.

## 6. What is proved and what is still missing

The suffix theorem is all-length and sharp. Equations (2)-(4) give a closed
exact query algorithm on a core of floor(n/2)+1 letters. The implementation
performs floor(n/2) or floor(n/2)-1 core steps, each consisting of two
one-bit sections and a paid grammar cut. It still uses n-1 one-bit section
advances overall. This is a genuine reduction of irrelevant labels, but
not an o(n) algorithm or an asymptotic improvement over existing methods.

A useful further rewrite must reduce the cost of constructing or advancing
this core, not merely its expanded length. In particular, treating R or Q
as one constant-time operation would hide precisely the remaining work.
No low-cost iteration jump for either operator is proved here.

The verifier checks 624 suffix cases, eight members of the sharpness
family, 234 arbitrary-core instances of (3), fourteen center queries
against independent row evolution through time65, and three integrated
normalizer queries. These are bounded implementation controls; the
universal conclusions follow from the displayed locality argument and
induction. All construction is local and no paid compute or large census
is used.

```
uv run --offline --no-project python experiments/rule30/p3_query_cone_rewrite.py
```

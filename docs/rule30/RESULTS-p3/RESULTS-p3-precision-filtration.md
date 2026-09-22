# Exact finite-precision power reduction for section expressions

Date: 2026-09-13; strengthened 2026-09-14. **An all-depth group identity
is proved and implemented; no sublinear Rule 30 query algorithm follows.**
Section6 strengthens the original exponent bound below from about3h/4
bits to about2h/3, and gives conditional improvements for even degree
and a proved uniformly fixed prefix. The generators are those of
the [exact dyadic section construction](RESULTS-p3-dyadic-sections.md):

\[
A=(A,C),\qquad B=(A,C)\,\mathrm{swap},\qquad
C=(B,C)\,\mathrm{swap}.
\]

Words are chronological: `UV` means apply `U`, then `V`. Let
`Gamma=<A,B,C>` include inverses. For every `g in Gamma` and integer `h>=0`,

\[
\boxed{\quad g^{\,2^{h-\lfloor h/4\rfloor}}(x)\equiv x\pmod{2^h}
\quad\text{for every }x\in\mathbb Z_2.\quad}\tag{1}
\]

Consequently, inside any expression needed only modulo `2^h`, a power
`g^m` can be replaced by its exponent remainder modulo
`2^(h-floor(h/4))`. This applies to an arbitrary repeated group expression,
not just to one generator. It is an exact identity in a finite-precision
quotient; it does not claim equality of the complete maps.

## 1. Activity vanishes at the fourth binary level

For a tree automorphism `g`, let `s_j(g)` be the XOR of the root toggles of
its sections at all `2^j` binary words of length `j`. Composition permutes
those words before applying the second set of sections. Therefore

\[
s_j(uv)=s_j(u)+s_j(v)\quad\text{in }\mathbb F_2.\tag{2}
\]

In particular these are group homomorphisms, also covering inverses.
The three-state recursion directly gives

| `j` | `s_j(A)` | `s_j(B)` | `s_j(C)` |
|---:|---:|---:|---:|
| 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 0 | 0 | 0 |

For example, `s_(j+1)(A)=s_j(A)+s_j(C)`; the other two rows follow from
their displayed children. The zero vector stays zero. Equation (2) proves
`s_j(g)=0` for every `g in Gamma` and every `j>=3`.

Now consider the action of `g` on four-bit words. All cycles of a binary
tree automorphism have power-of-two length, by induction over the two root
subtrees. If there were a cycle of length 16, its action on the eight
three-bit parents would be one eight-cycle. Following that parent cycle
would encounter each depth-three section once. The XOR of their toggles
would have to be one to interchange the two child bits and make a 16-cycle.
That XOR is `s_3(g)=0`, a contradiction. Every cycle therefore has length
at most eight, and

\[
g^8\text{ fixes the first four bits for every }g\in\Gamma.\tag{3}
\]

This argument concerns all group elements; it is not inferred by testing
the orders of the three generators.

## 2. Iterating the four-bit identity

The group is closed under sections: the generator sections are generators;
sections of products are products of appropriately selected sections; and
sections of inverses are inverses of appropriately selected sections.

More generally, let `nu(g)` be the number of initial bits fixed by `g` on
**every** input, allowing infinity for the identity. Applying (3) to its
sections after any fixed prefix gives the useful valuation recurrence

\[
\nu(g^8)\ge\nu(g)+4,\qquad \nu(g^2)\ge\nu(g)+1.\tag{3a}
\]

The second inequality follows by cancelling each next binary root toggle.
These are universal prefix statements, not valuations on one selected
seed return. A separately certified fixed prefix of length `d` can therefore
replace `h` by `max(h-d,0)` in the exponent bound for that element.

Suppose `g^(8^q)` fixes the first `4q` bits. Each of its sections there is
an element of `Gamma`, so its eighth power fixes the next four bits by
(3). Because the preceding prefix is fixed, the sections of this eighth
power are the corresponding eighth powers. Induction proves

\[
g^{8^q}\text{ fixes the first }4q\text{ bits}.\tag{4}
\]

For any binary tree automorphism, a `2^r`-th power fixes the first `r`
bits: squaring an element fixing a prefix cancels each next root toggle,
and induction advances one level at a time. Apply this to the sections in
(4). Writing `h=4q+r`, `0<=r<4`, gives an exponent `8^q2^r`, exactly
`2^(h-floor(h/4))`, proving (1).

The stronger uniform claim `g^4=id mod16` is false: already
`B^4(0)=4 mod8`, whereas `B^8=id mod8`.

## 3. Exact inverse relators on the complete maps

There are also inexpensive identities that use inverses and hold without
any precision limit. Write `a=A^(-1)`. The chronological words `aB` and
`aC` act respectively as

\[
\tau(x)=x\mathbin{\mathrm{XOR}}1,
\qquad
\sigma(x)=x-(x\bmod4)+((x-1)\bmod4).
\]

For the second formula, subtract one only within the low two-bit digit;
all higher bits are fixed. To verify it, use
`B(x)=A(x) XOR1`,
`C(x)=A(x) XOR(3-2*(x mod2))`, and the fact that `A` preserves bit zero.
These two fixed low-bit permutations satisfy

\[
(aB)^2=1,\qquad (aC)^4=1,\qquad(aB\,aC)^2=1.\tag{5}
\]

Thus the expression language admits real inverse cancellations even
though positive words of different lengths cannot agree as complete maps.
Equation (5) alone supplies no cheap normal form for arbitrary words:
copies of `A` between the small permutations retain their ordered action.

## 4. Paid rewrite and relevance to the query

The original bound computes `e=h-floor(h/4)`; the current helper uses the
stronger exponent in section6. Either reduces the magnitude of
an exponent to its low `e` bits. It first compares `e` with the exponent's
bit length. If `e` is at least that length, it returns the exponent
unchanged and **does not allocate an `e`-bit modulus**. Signed remainders
allow the same rule for negative exponents without creating a huge positive
representative.

The arithmetic cost is polynomial in the binary lengths of `h` and the
given exponent. It does not require constructing a quotient permutation
table. A residual query for bit `m` needs precision `h=m+1`; substituting
an equivalent expression modulo that precision is sound under any other
compatible group action in the context.

For the original bound(1) on the initial singleton expression `A^n` at
precision `n+1`, the modulus has roughly `3n/4` bits. It therefore exceeds
`n` at all sufficiently large
indices, and this rule leaves that initial exponent unchanged. Useful
reduction of an exponent with `L` bits needs
`h-floor(h/4)<L`, placing this particular shortcut at relatively small
remaining precision. No claim is made that it removes the preceding
linear sequence of section advances. The identities provide sound rewrite
rules, not the missing sublinear jump operation.

## 5. Exact verifier

- [Source](../../experiments/rule30/p3_precision_filtration.py).
- [Artifact](../../experiments/rule30/p3-precision-filtration.json).

The checker independently evaluates the generator and inverse Mealy
recursions. It verifies their direct integer formulas on every input
through eight-bit precision, both directions of inverse composition, all
three full-map relators at those precisions, and the power bound on nine
specified positive and inverse words at each precision one through eight.
These are 72 complete small quotient checks, without enumerating group
closures. The universal theorem follows from sections 1–2; the finite
checks validate its local premises and implementation.

The checker also tests five signed exponents with a precision parameter
`h=2^4096`, confirming that its early exit avoids constructing the enormous
modulus. The original saved run passed in approximately 0.009 seconds.
The strengthened check below retains those controls. No existing
Rule 30 prefix, census, or orbit was regenerated.

```sh
uv run --offline --no-project python experiments/rule30/p3_precision_filtration.py
```

## 6. Stronger section-closed degree bound

The [reset-group normal form](RESULTS-p3-automaton-group-identification.md)
establishes an integer homomorphism chi with

```
chi(A)=chi(B)=chi(C)=1,
chi(g|v)=chi(g) for every finite binary word v.              (6)
```

One can prove precisely the parity information needed here without
that classification: the activity table has s2=1 on every signed
generator, so s2(g) is the parity of signed word length. A section
replaces each signed generator by one signed generator with the same
sign. Thus the subgroup

```
H={g : chi(g) is even}=ker(s2)
```

is closed under every section.

**Local lemma.** Every g in H has g^4 fixing three binary bits on all
inputs. A cycle on three-bit words can have length1,2,4, or8. An8-cycle
would pass through all four two-bit prefixes; their section toggles
would have XOR1. This is exactly s2(g), which is0. No8-cycle exists,
so the fourth power is the identity on this level.

After taking that fourth power, all sections still lie in H. The
fixed prefix permits taking their fourth powers independently.
Induction, followed by at most two ordinary squarings, proves

```
g^(4^q 2^r) fixes3q+r bits,     g in H, q>=0,0<=r<3.
```

Consequently the even-degree exponent bound is

```
e_even(h)=h-floor(h/3),   h>=0,
g^(2^e_even(h))=identity modulo2^h when chi(g) is even.      (7)
```

For arbitrary g, its square fixes the first binary bit, and every
section of g squared has even degree. Apply(7) to those sections at
the remaining h-1 bits. This gives

```
e_all(0)=0,
e_all(h)=1+e_even(h-1)=h-floor((h-1)/3), h>=1,
g^(2^e_all(h))=identity modulo2^h.                         (8)
```

Both statements include inverses and arbitrary group expressions.
They concern every input prefix, not only the zero orbit. For example
the general exponent at precision7 falls from64 under(1) to32 under(8).
At precision3, even degree permits exponent4, whereas the universal
exponent8 is necessary: B^4(0)=4 modulo8.

If g is separately proved to fix nu initial bits on **all** inputs,
apply the appropriate bound to its sections at that level. Every
section has the same degree parity. Thus h may be replaced by

```
remaining=max(h-nu,0)                                     (9)
```

in(7) or(8). A valuation or a fixed prefix observed only at zero does
not supply this uniform premise.

There is also a full-map consequence for the finite kernel. If a
zero-degree defect expression is conjugated into the finitary group
at binary depth w by the reset-group localization, its order divides
2^(w-floor(w/3)). Indeed its degree is still0, equation(7) fixes the
first w bits, and finitary support fixes all the remaining bits.
Conjugating back preserves the order. This improves the generic
depth-w binary-tree bound2^w for these particular kernel elements;
constructing or evaluating their growing finite permutation remains
a separate cost.

The helper now exposes

```
exponent_bits(h, even_degree=False, fixed_bits=0),
reduce_power(n,h,even_degree=False,fixed_bits=0).
```

Its keyword premises must be certified by the caller. In particular,
for the expression g^n, `even_degree` refers to the **base g**, not to
the completed power g^n. An even exponent does not turn B into an
even-degree base. One may instead write B^N=(B^2)^(N/2) when N is
even and use the even-degree base B^2, including its uniformly fixed
first bit. The early comparison with the supplied exponent's binary
length remains in place. No enormous modulus is constructed merely
because h is enormous. `legacy_exponent_bits` retains the previous rule.

The new local certificate checks all12 signed child-degree identities
and all128 binary-tree portraits of depth3. Exactly64 have s2=0,
and all64 have fourth power equal to the identity. This is a complete
fixed local lemma, not an increasing group or orbit census. The same72
small word/precision controls now check both the old and new bounds,
the degree-conditioned bound, and each word's separately certified
uniform fixed prefix. Five enormous-precision tests check both the
default and even-degree paths, with five further fixed-prefix tests.
The updated run passed in about0.023 seconds.

For the actual marked B query, required precision is proportional to
the query index while the exponent has only logarithmic binary length.
The new modulus still exceeds that initial exponent at all sufficiently
large indices. No initial marked exponent reduction or sublinear work
bound follows. Moreover chi((B^N)|v)=N: inverse letters cannot turn
these residuals into bounded-degree ordinary words. This is not a
lower bound for compressed expressions or their evaluation.

## 7. A marked control for collecting the finite-kernel factors

The degree normal form leaves an ordered product of conjugated
boundary flips. With ordinary composition and
tau_i=A0^i tau A0^-i,

```
B0^N(0)=(tau_0 tau_1 ... tau_(N-1))(0).
```

Sorting this product into its even and odd indices would expose two
half-size products, but it loses a correction relevant to the actual
marked query. At N=4, exact finite-support arithmetic gives

```
(tau_0 tau_1 tau_2 tau_3)(0)=100,
(tau_0 tau_2 tau_1 tau_3)(0)=96.
```

These maps affect only the first7 bits, and the verifier retains8-bit
precision. Their H images are111 and104. The high bit of itinerary
digit1 is therefore1 versus0. The
[actual-B readout](RESULTS-p3-actual-b-query.md) identifies N=4,j=1,
bit1 with the singleton center at n=5. Thus restricting this particular
shuffle to the marked query does not rescue it. The control excludes
discarding the shuffle correction; it does not exclude a cheap exact
calculation of that correction or a different return family.

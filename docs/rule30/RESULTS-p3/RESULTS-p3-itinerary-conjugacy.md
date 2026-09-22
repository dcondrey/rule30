# An exact itinerary conjugacy for the P3 core

Date: 2026-09-13. **The triangular core map H is conjugate to the base-four
shift by an explicit 2-adic isometry. In these coordinates all three ABC
generators have a three-state, output-driven automaton, and one zero-digit
section is exactly the existing Q update.** This supplies a simpler exact
query implementation. It does not make its growing number of section
advances free, and proves no sublinear singleton algorithm or P1/P2 result.

The [primary verifier](../../experiments/rule30/p3_itinerary_conjugacy.py)
and [artifact](../../experiments/rule30/p3-itinerary-conjugacy.json) retain
bounded exact controls. The independent
[inverse verifier](../../experiments/rule30/p3_itinerary_inverse.py) and
[artifact](../../experiments/rule30/p3-itinerary-inverse.json) use a separate
scalar reconstruction and local semiconjugacy checks.

Permutative cellular automata itinerary coding is a standard general
construction; see Pivato, *The Ergodic Theory of Cellular Automata*,
[Proposition 2D.1](https://citeseerx.ist.psu.edu/document?doi=750c3856fa4bce81b74a80d91b7582a10291b5a4&repid=rep1&type=pdf).
The result recorded here is its explicit realization for this repository's
ABC maps and ordered query core, not a claim of novelty for itinerary coding.

## 1. The coding is an isometry and a bijection

Use the [bulk-core conventions](RESULTS-p3-bulk-core-formula.md): low bits
are read first, and UV means apply U and then V. On the 2-adic integers,

```
G(x) = x XOR ((x<<1) OR (x<<2)),
A(x) = G(x),
B(x) = G(x) XOR 1,
C(x) = G(x) XOR (3-2*(x AND 1)),
H(x) = G(x)>>2 = (x>>2) XOR ((x>>1) OR x).
```

Right shift means deletion of low bits, including for an infinite 2-adic
bit sequence. H's local equation is

```
(Hx)_j = x_(j+2) XOR (x_(j+1) OR x_j).             (1)
```

If x and y agree modulo4 and their first differing bit is d>=2, the first
differing H output bit is d-2: that bit reads the differing x_d exactly
once, while all its other inputs agree. Therefore

```
v_2(Hx-Hy) = v_2(x-y)-2  when x=y mod4, x!=y.      (2)
```

Define the infinite base-four itinerary

```
Phi(x) = sum_(t>=0) (H^t(x) mod4) * 4^t.          (3)
```

Its first m digits depend on exactly a prefix of at most2m source bits.
If the first differing source bit is d=2k+e with e in{0,1}, apply (2) k
times. The first differing itinerary digit is k, and its first differing
bit is e. Hence Phi is a binary 2-adic isometry:

```
v_2(Phi(x)-Phi(y)) = v_2(x-y).                    (4)
```

At each precision m the induced map on the4^m residues is injective, so
is bijective. These prefix maps are compatible. Taking their unique
consistent inverse prefixes proves that Phi is a bijection on Z_2, not
merely an injection on finite integers. Directly from (3),

```
Phi(Hx) = Phi(x)>>2.                              (5)
```

This conjugates the noninvertible map H to a one-sided shift. It is not a
conjugacy of G to an invertible affine map, and does not contradict the
previous obstructions to such a different conjugacy.

## 2. The conjugated ABC automaton

The root permutations on a base-four digit d are

| State g | P_g(0) | P_g(1) | P_g(2) | P_g(3) |
|---|---:|---:|---:|---:|
| A | 0 | 3 | 2 | 1 |
| B | 1 | 2 | 3 | 0 |
| C | 3 | 2 | 1 | 0 |

All three maps satisfy the exact identity

```
g(x) = 4*H(x) + P_g(x mod4).                      (6)
```

Put psi(0)=A, psi(1)=B, psi(2)=psi(3)=C. Define K_g by reading an input
digit d, emitting e=P_g(d), and entering state psi(e). The next state is
selected by the **emitted** digit. Then, for all x in Z_2 and all g,

```
Phi(g(x)) = K_g(Phi(x)).                          (7)
```

For a direct proof, write z=4y+e. Equation (1) gives the two low bits of
H(z), with a=y_0 and b=y_1, as

```
a XOR (e_0 OR e_1),
b XOR (e_1 OR a).
```

These are precisely P_psi(e)(a+2b). Also H commutes with right shifts,
so H(z)>>2=H(y). Apply (6) with z=g(x) to obtain

```
H(g(x)) = psi(g(x) mod4)(H(x)).                   (8)
```

Iterating (8) proves (7) digit by digit, with the correct ordered state at
every seam. It also proves conjugacy for every chronological ABC word.

The independent verifier checks the complete24 low-three-bit cases of
(8); the common higher-bit action is proved by (6), not extrapolated
from a fixed precision table.

For K=K_C the inverse is particularly local. If y=K(x), use a virtual
previous output digit y_(-1)=3 and recover each input digit by

```
x_i = -y_i mod4     if y_(i-1)=0;
x_i = y_i-1 mod4    if y_(i-1)=1;
x_i = 3-y_i         if y_(i-1)=2 or3.              (9)
```

For initial A or B the virtual digit is respectively0 or1. This is the
inverse of the displayed root permutation in the known state; thus it
holds for all finite prefixes and infinite inputs. It does not imply an
efficient growing-power algorithm. In particular a local inverse with a
fixed boundary is not by itself a reversible bilateral cellular automaton:
without that boundary, (9) sends all three constant rays0,1,3 to the same
constant0 image. The independent artifact preserves those controls and
the distinct fixed-boundary images.

## 3. Q becomes one ordinary zero-digit section

The original binary ABC automaton has, after two input bits forming digit
d, the section psi(d), independent of the original state. Its new
conjugated automaton instead has section psi(P_g(d)). For an ordered word
U=g_1...g_L let d_0=0 and d_i=P_(g_i)(d_(i-1)). Then

```
original (U A)|_00 = psi(d_0) psi(d_1)...psi(d_L),
new K_U|_0        =          psi(d_1)...psi(d_L).
```

The original definition is Q(U)=tail((U A)|_00), and psi(d_0)=A.
Consequently, for every nonempty U, as literal ordered words,

```
K_U|_0 = K_(Q(U)),
K_U|_(0^k) = K_(Q^k(U))  for every k>=0.          (10)
```

Thus the new section engine needs neither a leading-letter cut nor an
appended state. No word equality is inferred merely from agreement on0.
The full section identity retains all higher input tails.

The existing singleton reduction now reads, with digit positions starting
at0,

```
c_(2h)   = high bit of digit_(h-1)(K_C^(h+1)(0)),  h>=1;
c_(2h+1) = low bit of digit_h(K_C^(h+1)(0)),       h>=0;
c_0      = 1.                                    (11)
```

Indeed Phi(C^L(0))=K_C^L(0), since Phi(0)=0, and its digit k is
H^k(C^L(0)) mod4. This permits direct use of the known encoded seed0;
one need not construct Phi on an already difficult orbit value first.

The [quaternary SLP evaluator](../../experiments/rule30/p3_quaternary_section_query.py)
implements (10)-(11), with its charged
[artifact](../../experiments/rule30/p3-quaternary-section-query.json).
The directed queries n=8,17,32 construct17,38,90 grammar nodes respectively;
at n=32 they still require15 successive zero-digit section advances.
These are finite implementation comparisons, not an asymptotic bound.

## 4. Construction costs and constant-run compression

For m itinerary digits, start with2m source bits and repeatedly apply
(1) on the shrinking valid row. The row lengths after updates are
2m-2,2m-4,...,2, so the exact number of local Boolean updates is
m(m-1). Output and bit-array conversion take O(m) additional work.

The inverse has the same bound without replaying candidate full rows.
The itinerary supplies temporal columns z_0,z_1 of length m. Rearranging
(1) gives

```
z_(j+2)(t) = z_j(t+1) XOR (z_(j+1)(t) OR z_j(t)).  (12)
```

Reconstruct columns of lengths m-1,m-1,m-2,m-2,...,1,1. Their initial
bits, together with the given first two bits, reconstruct the source.
This again uses exactly m(m-1) Boolean updates. Two current columns and
the output require O(m) working bits; the verifier's optional integer
length diagnostics are additional metadata. The implementations mask to
the requested low2m bits before conversion, so irrelevant high digits are
not traversed by the reconstruction. Supplying or obtaining that prefix
is still part of any enclosing algorithm's cost.

On an explicit m-digit array, one K_g action uses m finite-state
transitions. The primary implementation also handles one constant input
run of binary-encoded length M without expanding it: its three-state
orbit has a prefix followed by a cycle after at most three transitions.
It returns an output prefix, repeated block, suffix, and exact final
state. Count arithmetic uses O(log(M+1)) bit work. The directed huge-run
controls use M=2^40+7. This compresses one action on that input family;
it does not assert that repeated K actions preserve a small run grammar.

## 5. Phi itself has no fixed finite-state sequential realization

Although each K_g is a three-state transducer, Phi cannot be computed by
any fixed finite-state Mealy transducer reading base-four digits from low
to high. This follows from an existing all-length period restriction,
not from growth observed in a finite table.

For every positive finite integer of width w, H preserves its highest
one and has an eventual finite cycle. If its primitive period is P,
[the triangular-core theorem](RESULTS-p3-triangular-core-power.md#3-no-fixed-temporal-period-covers-arbitrarily-large-widths)
proves w<=4^P-1. Hence these eventual periods are unbounded as w grows.
By (5) and injectivity of Phi, the eventual digit period of Phi(x) is
exactly P: a smaller eventual digit period would make the corresponding
H orbit return sooner.

A transducer with S states reading the eventual-zero digit tail of a
finite integer eventually cycles through at most S states. Its eventual
output digit period is therefore at most S, a contradiction. The same
obstruction covers a fixed binary Mealy realization by grouping bits in
pairs. It does not rule out other algorithms, variable memory, or fast
selected queries. In particular it does not obstruct (11), which starts
from the already known Phi(0)=0.

## 6. The exact HC defect and finite verification scope

For low bits a,b,c of x, a direct local calculation gives

```
H(Cx) XOR C(Hx) = a*b + 2*b*c.                    (13)
```

The defect after any number t of H steps remains in the low two bits.
Let x_t=H^t(x), a_t=bit_0(x_t), b_t=bit_1(x_t), and write the defect as
e_t+2f_t. Starting e_0=f_0=0, its exact recurrence over GF(2) is

```
e_(t+1) = (a_t+e_t)*(b_t+f_t),
f_(t+1) = (1+a_(t+1))*(b_t+f_t).                 (14)
```

To check (14), put y_t=H^t(Cx). Then y_t>>2=x_(t+1), while the two low
bits of C(x_t) are1+a_t,1+b_t. Substitution in (1) gives (14). The input
bits in this four-state recurrence are from the actual H history;
replacing them by independent choices would change the problem.

The primary verifier checks all2016 pairs in the complete three-digit
prefix permutation,108 directed generator conjugacies, seven word/Q
identities,156 constant-run cases,28 cocycle cases, and selected actual
C-ray digits with exponent at most8. These support the implementations;
the all-length results are proved above. The saved diagonal defect
values do not establish a periodic law, and no growing-index evaluation
bound follows from the existence of this finite defect state alone.

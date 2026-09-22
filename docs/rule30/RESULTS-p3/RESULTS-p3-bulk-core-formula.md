# An exact bulk formula for the P3 core and its boundary error

Date: 2026-09-13. **The half-width core admits a literal all-length bulk
section formula.** It uses one section at a block of 2k zero bits, followed
by deletion of a known leading A-run, to express k complete Q updates.
Both parities of the singleton center query can use this same operator.
This gives a precise construction for a block-section algorithm; it does
not prove that constructing the section costs less than k individual
updates. A seed-derived four-cycle also disproves the proposed automatic
decay of its boundary commutator.

The [exact verifier](../../experiments/rule30/p3_bulk_core_formula.py) and
[artifact](../../experiments/rule30/p3-bulk-core-formula.json) retain the
local tables, bounded word controls, and complete counterexample cycle.
No P1 or P2 exclusion follows from these P3 identities.

## 1. Conventions and the two-bit synchronization law

Use the [three-state section representation](RESULTS-p3-dyadic-sections.md)
and [half-width query core](RESULTS-p3-query-cone-rewrite.md). Integers
encode low bits first, and words are chronological: UV means apply U,
then V. The generators are

```
G(x) = x XOR ((x<<1) OR (x<<2)),
A(x) = G(x),
B(x) = G(x) XOR 1,
C(x) = G(x) XOR (3-2*(x AND 1)).

A=(A,C),   B=(A,C)swap,   C=(B,C)swap.
```

Let p(U) be the parity of the B/C letters, and let T(U)=U|_0 be the
section on a zero bit. Composition retains the intermediate input:

```
(UV)|_b = (U|_b)(V|_(b XOR p(U))).                  (1)
```

Every single generator S has the same section after two specified input
bits a,b:

```
S|_(a,b) = psi(a,b),
psi(a,b) = C if b=1; B if b=0,a=1; A if a=b=0.     (2)
```

This follows directly from the displayed three-state table. Equivalently,
the underlying two-input memory has been overwritten after two bits.
The two bits in (2) are the actual bits entering that generator, not
independent boundary choices.

For every nonempty word U, T^2(U) begins with A. Define

```
Q(U) = tail(T^2(U)) append psi(a,b),
a=bit_0(U(0)),    b=bit_1(U(0)).                    (3)
```

Here tail deletes just the first letter. This extends the previously
defined C-headed core update to every nonempty word. By (1)-(2),

```
Q(U) = tail(T^2(U A)).                             (4)
```

It preserves length. It also preserves the first letter: if a second
letter exists, its section in T^2(U) is psi of the low two bits output by
the first letter on00. Those output pairs in low-bit-first order are
(0,0),(1,0),(1,1) for A,B,C, respectively, whose psi values are A,B,C.
For a one-letter word the appended letter
has the same property.

## 2. A literal bulk identity

**Theorem.** For every nonempty ordered word U and every k>=0,

```
(U A^k)|_(0^(2k)) = A^k Q^k(U).                    (5)
```

Thus k successive core updates have the exact expression

```
Q^k(U) = remove_first_k((U A^k)|_(0^(2k))).         (6)
```

These are equal ordered words, stronger than equality of a selected bit.
In particular, no phase or seam state is discarded in (5).

Proof. The case k=0 is immediate. Suppose (5) holds. Sectioning the final
extra A after the first 2k input zeros gives some single letter S, so

```
(U A^(k+1))|_(0^(2k)) = A^k Q^k(U) S.
```

Take two more zero sections. The leading A^k fixes00 and remains A^k
under these sections. For any word V and any S in {A,B,C}, the actual two
bits passed from V to S are the same as those passed from V to A.
Equation (2) therefore gives

```
(V S)|_00 = (V A)|_00 = A Q(V).
```

Apply this with V=Q^k(U) to obtain A^(k+1)Q^(k+1)(U), proving the
induction. The argument works at k=0 and for one-letter U without a
missing suffix convention.

Equation (6) is a useful target for a compiler that constructs a section
at a whole input block. The literal verifier still performs 2k one-bit
section advances; its purpose is to verify the identity. Treating the
left side as an already available object would leave out the central
construction cost.

## 3. The exact integer action, including the even-query correction

Define

```
H(x) = G(x)>>2 = (x>>2) XOR ((x>>1) OR x).          (7)
```

**Theorem.** For every nonempty word U and k>=0,

```
Q(U)(0) = H(U(0)),
Q^k(U)(0) = H^k(U(0)) = G^k(U(0)) >> (2k).        (8)
```

Proof. Taking the section of UA on00 removes its first two output bits
on the zero input. The chronological action UA is G after U. Deleting
the section's leading A does not change its zero-input value because
A(0)=0. This proves the first equality, and iteration proves the second.
Also, (7) gives H(x>>r)=H(x)>>r for every r>=0. Since H=D^2G for the
right shift D, this commutation proves H^k=D^(2k)G^k by induction. It
does not assert that G itself commutes with right shifts.

The previous even-query update R replaces the appended B in (3) by A.
For x=U(0), the replacement occurs exactly when x mod4=1. Since A and B
differ only at bit0,

```
R(U)(0) = H(x) XOR 1[x mod4=1] = H(x AND ~1).      (9)
```

The last equality follows from the bit0 term x_0 OR x_1 in (7).
Let J(x)=H(x AND ~1). Then R^k(U)(0)=J^k(U(0)), and

```
J(x)>>1 = H(x)>>1 = H(x>>1).
```

Induction on k therefore proves the exact quotient identity

```
R^k(U)(0)>>1 = Q^k(U)(0)>>1.                      (10)
```

Combining (10) with the established center-query formula gives a uniform
Q implementation for both parities:

```
c_(2h)   = bit_1(Q^(h-1)(C^(h+1))(0)),  h>=1;
c_(2h+1) = bit_0(Q^h(C^(h+1))(0)),      h>=0;
c_0=1.                                            (11)
```

Equation (10) does not justify replacing Q by R for the final root bit.
For example, U=CA has U(0)=13, Q(U)=CB with value12, and R(U)=CA with
value13. Their bit0 values differ. The bulk identity (6) retains Q and
therefore applies to both lines of (11) without this loss.

Although (8) exposes the exact integer evolution, directly iterating H
still takes k steps on a growing or supplied integer representation.
Constructing U(0) also costs work. No faster powering theorem follows
merely from changing coordinates to H.

## 4. A boundary commutator that can persist indefinitely

The operators G and H almost commute, with an exact low-bit error. Write
x_i=bit_i(x). Then

```
H(G(x)) XOR G(H(x))
  = (x_0 OR x_1) + 2*x_2*(x_0 XOR x_1).           (12)
```

The addition here joins disjoint bit positions. To prove (12), put
z=G(x). Compare G(z)>>2 with G(z>>2). Above bit1 the expressions agree.
At bit0 their difference is z_1 OR z_0=x_0 OR x_1. At bit1 it is
z_1 AND NOT z_2=x_2*(x_0 XOR x_1), as follows by distinguishing whether
x_0 OR x_1 is zero. This proves the formula at every input width.

It would be incorrect to infer that subsequent H steps always push this
error out through the low boundary. H's bit j depends on input bits
j,j+1,j+2, including j itself. A discrepancy can retain its highest bit.
The following counterexample occurs on an actual seed-derived core:

```
C^4(0)=200,
Q(C^4)=CACA,
CACA(0)=H(200)=222.
```

At x=222, the two orders in (12) give 891 and888. Apply the same H to
both sides:

| Following H steps | H(G(x)) branch | G(H(x)) branch | XOR |
|---:|---:|---:|---:|
| 0 | 891 | 888 | 3 |
| 1 | 801 | 802 | 3 |
| 2 | 889 | 891 | 2 |
| 3 | 803 | 801 | 2 |
| 4 | 891 | 889 | 2 |
| 5 | 801 | 803 | 2 |
| 6 | 889 | 891 | 2 |

The last row equals the row at step2. Checking the four cycle edges
proves that the discrepancy at bit1 persists for arbitrarily many
further H steps. This is an exact finite certificate of an infinite
failure, not a long finite observation.

Consequently, counting later H steps as automatic contraction of the
commutator is invalid, even at this actual core value. The example does
not exclude cancellation under other specified contexts. A safe generic
bound is that a following word containing g occurrences of G confines
the original error to bits<=2g+1: G can move the upper edge by two, while
H cannot move it upward. Subtracting the number of H occurrences from
that bound would require an additional masking argument and is refuted
in general by the cycle above.

## 5. Verification and remaining algorithmic question

The artifact records all twelve generator/two-bit synchronization cases,
195 literal bulk identities on the39 words of lengths1 through3 and
k=0 through4, 195 integer semiconjugacy controls, 195 R/Q quotient
controls, and288 local shift/iteration controls. It retains the eight-row
commutator table, the four exact cycle edges, the root-bit caution, and
eight tiny singleton query controls through n=9. These bounded checks
validate the implementations; the universal claims use the proofs above.
The artifact hashes this report, the verifier, and its two imported
implementations.

The new constructive object is the single block section in (6), together
with an exactly known removable prefix. A paid block compiler can try to
share its internal subqueries across many zero bits while transporting
each ordered intermediate input correctly. A bound on that construction
and the final requested bit is still required for a faster algorithm.
Neither (5), the shifted evolution (8), nor the finite controls establish
an o(n) singleton center-query algorithm.

```
uv run --offline --no-project python experiments/rule30/p3_bulk_core_formula.py
```

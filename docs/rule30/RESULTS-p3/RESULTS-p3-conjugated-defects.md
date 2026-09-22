# Ordered boundary defects: exact bulk identity and a failed small-group shortcut

Date: 2026-09-13. **An exact factorization is implemented; it supplies no
sublinear singleton query.** Conjugated two-bit corrections cannot simply
be commuted or collected into one copy of the small boundary group.

Use the [section generators](RESULTS-p3-dyadic-sections.md), with
`A(x)=x XOR((x<<1) OR(x<<2))`. Let

\[
\tau(x)=x\mathbin{\mathrm{XOR}}1,\qquad
\sigma(x)=x-(x\bmod4)+((x-1)\bmod4).
\]

Then `B=tau o A` and `C=sigma o A`. The maps `tau,sigma` change only the
low two bits and generate an eight-element dihedral group. This describes
their complete maps, not an assumed quotient of the singleton orbit.

## 1. The exact bulk factorization

Here `o` is ordinary function composition, with the rightmost map applied
first. For a chronological word of length `L`, let `kappa_i` be `id`,
`tau`, or `sigma` according as its ith letter is A, B, or C. Define

\[
\operatorname{Ad}_A^j(\kappa)=A^j\circ\kappa\circ A^{-j}.
\]

Inserting adjacent inverse pairs gives the all-length identity

\[
W=\left(\kappa_L\circ\operatorname{Ad}_A(\kappa_{L-1})
 \circ\cdots\circ\operatorname{Ad}_A^{L-1}(\kappa_1)\right)
 \circ A^L.\tag{1}
\]

It handles a complete word at once and keeps the ordered corrections.
The verifier evaluates this factorization independently against raw
three-state word scans, including inputs with high bits beyond the defect
region. It does not assume that the factors commute.

If a compatible permutation `kappa` changes only bits below `w`, then

\[
\operatorname{Ad}_A^j(\kappa)\text{ changes only bits below }w+2j.\tag{2}
\]

Indeed, apply `A^(-j)` to the common input. The two intermediate inputs
differ only below `w`; each following application of A propagates a
difference by at most two positions. The unperturbed composition returns
the original input, proving (2). The inverse is itself compatible: its
bits are reconstructed successively by
`x_i=y_i XOR(x_(i-1) OR x_(i-2))`, starting with two zero memories.

Thus (1) gives a rigorous finite-prefix description of every correction.
Discarding the final corrections whose whole influence lies below the requested bit
recovers the [query suffix replacement](RESULTS-p3-query-cone-rewrite.md).
This factorization does not make the remaining corrections constant-cost.

## 2. The support bound is sharp, and one correction already contains P3

Put `gamma_j=Ad_A^j(tau)`. Because `A(0)=0`,

\[
\gamma_j(0)=A^j(1),\qquad
\operatorname{Ad}_A^j(\sigma)(0)=A^j(3).\tag{3}
\]

Every application of A raises the highest nonzero bit of a positive
integer by exactly two. Equation (3) therefore has highest nonzero bits
`2j` and `2j+1`, respectively. The support bounds `2j+1` for `gamma_j` and
`2j+2` for the conjugated sigma are sharp at every j.

More specifically, the actual singleton query is exactly

\[
\boxed{c_n=\operatorname{bit}_n(\gamma_n(0)).}\tag{4}
\]

Although `gamma_n` has a short expression `A^n tau A^(-n)`, evaluating its
selected bit is already the original query. Treating that conjugate as a
cheap finite-group label would conceal the computation. Equation (4)
does not prove that a fast conjugate evaluator is impossible; such an
evaluator would instead be a real solution method requiring its own
construction and cost proof.

One conjugate can be evaluated exactly on its finite prefix by j inverse
passes, the boundary permutation, and j forward passes. A scalar bit-array
implementation visits `O((j+1)(w+j))` cells, including the boundary case
`j=0`. Constructing an explicit table for
all prefix inputs would require `2^(w+2j)` entries and is not performed.
Merely writing powers as a shared expression does not remove the work of
evaluating those passes.

## 3. Two exact falsifiers of proposed collection rules

Conjugation depth does not separate the corrections spatially: the
`gamma_j` all toggle bit zero. In particular,

\[
(\tau\circ\gamma_2)(0)=24,\qquad
(\gamma_2\circ\tau)(0)=8.\tag{5}
\]

Both maps in this check fix every bit at position five or above. Equation
(5) is an exact complete-map counterexample to commuting these separated
conjugation levels, not a truncation artifact.

Nor do all levels close in one copy of the original dihedral group.
The map `tau o gamma_3` has order exactly 16. It fixes all bits at position
seven or above, and its orbit of zero is

```text
0,110,108,106,96,78,76,74,64,46,44,42,32,14,12,10,0.
```

The product is also compatible, so its low seven output bits depend only
on the low seven input bits. Together with the support bound, this gives
`F(128z+r)=128z+P(r)` for every `z` in `Z_2` and `0<=r<128`, where P is
the seven-bit permutation. Thus its order as a complete 2-adic map is
exactly the order of P; no ordinary finite-integer inverse is assumed.
The verifier checks this complete permutation on the 128 low-bit inputs:
all cycles have length dividing 16, and the displayed cycle has length 16.
The original eight-element dihedral group has no element of that order.
Each single conjugated boundary group remains an isomorphic small group;
their ordered combination need not remain in that same small group. No
unbounded order-growth claim is inferred from this witness.

## 4. Files and precise outcome

- [Verifier and factorization evaluator](../../experiments/rule30/p3_conjugated_defects.py).
- [Exact artifact](../../experiments/rule30/p3-conjugated-defects.json).

The bounded verifier checks 2,044 inverse identities, 63 full word/input
factorizations, nine sharp-support instances, the noncommutation witness,
and the complete seven-bit permutation proving order 16. It takes about
0.002 seconds. The support and singleton identities are proved for all
lengths above; the finite instances validate the implementation.

The result identifies the exact task left by this bulk factorization:
evaluate ordered conjugated corrections at the demanded precision without
expanding their prefixes or performing all their forward/inverse passes.
Neither commutation by conjugation depth nor collection into the original
small boundary group supplies that operation. No general computational
lower bound, period exclusion, or sublinear Rule 30 algorithm is claimed.

```sh
uv run --offline --no-project python experiments/rule30/p3_conjugated_defects.py
```

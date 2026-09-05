# Why equality refinement closes for TP3-011 but not yet for TP2

Date: 2026-09-02

Status: **STRUCTURAL ASYMMETRY IDENTIFIED.  NO NEW EXCLUSION THEOREM IS
CLAIMED.  THE NUMBER OF OPEN UNBOUNDED LEMMAS REMAINS ONE.**

Here `TP3-011` means the temporal trace necklace represented by `011`, and
`TP2` means the alternating temporal trace.  Neither abbreviation refers to
an archive prize-problem number.

## TP3-011 has a fixed synchronous relation

For TP3-011, removing the phase-dependent boundary append leaves a
length-preserving interior transducer `E` on one fixed finite core word.
Two applications of `E` advance the inert leading-zero prefix by at least
one cell.  The finite sequence of carry parities can therefore be packed into
one finite integer.  In the inverse zero-tail formulation, one macro step is
a synchronous letter-to-letter transduction with:

```text
one of two fixed three-letter prefixes,
one three-bit carry for the current transition,
one three-bit carry for the following transition.
```

Consequently the change in any fixed local-factor count is a path weight on
one finite graph.  Longest-path closure proves nonincrease, and restricting
to equality edges produces another finite graph.  That is why successive
equality-subgraph refinement is an all-length theorem for TP3-011.  It does
not prove termination: on the final SFT the dual words still grow, and the
phase-aware additive rank tested in `RESULTS-TP3-011-SFT-RANK.md` is UNSAT.

## TP2 changes the operator depth with the source length

Write `G_n=P^n o I`.  For a binary source `W` of length `n`, high-bit
elimination determines a unique binary continuation `Q_n(W)` of length
`n+2`.  If the newest-cell affine phase is

```text
A_(alpha,beta,gamma)(h,l)
    = (h + alpha, l + beta*h + gamma)
```

over `F_2`, then the next continuation symbol and defect bit are exactly

```text
q       = 2 - alpha,
Psi bit = alpha + beta*(1 + alpha) + gamma.          (1)
```

Thus the current total phase emits both coordinates without search.  The
problem is updating that phase.

For a four-state left symbol `x=(H,L)`, define

```text
lambda(x) = (H OR L, 1 + L, H OR L).
```

The boundary phase is `(1,0,1)`.  If the current accumulated phase is
`(alpha,beta,gamma)` and the next left symbol has phase `(a,b,g)`, composition
updates it by

```text
(alpha,beta,gamma) ->
(alpha+a, beta+b, gamma+g+b*alpha).                  (2)
```

Before forcing a continuation cell, its phase is obtained by folding (2)
over the previous endpoint and the complete ordered dependency diagonal,
excluding only the final target cell.  After (1) chooses `q`, that diagonal
updates by

```text
D'_0 = B(q),
D'_1 = phi(previous_endpoint,D'_0),
D'_k = phi(D_(k-2),D'_(k-1))  for k>=2.              (3)
```

Equations (1)--(3) are an exact phase-carrying composition law across the
continuation positions.  They also expose why it is not the desired bounded
law: computing the next phase requires the newly transformed ordered
diagonal, whose length grows.

## What a closed TP2 state must retain

The smallest exact state presently justified is

```text
(previous binary endpoint,
 ordered dependency word over {0,{1,3},2}).          (4)
```

The quotient `{1,3}` is exact because states `1` and `3` induce the same
left action in both (2) and (3).  No further quotient is currently proved.
The full word in (4) determines the fold phase, the forced symbol, the defect
bit, and the next word.

The natural bounded candidates fail for distinct reasons:

- no carried phase cannot compose prefix or suffix extensions; reversal and
  complementation do not repair those collisions;
- the total affine phase, even together with the last endpoint, emits the
  current pair by (1) but does not determine the transformed diagonal in
  (3), hence does not determine the following phase;
- a fixed prefix, suffix, or two-ended window of the diagonal omits interior
  symbols that the right-permutive recurrence transports to a later seam;
  the archive's two-ended transition collision is the concrete instance of
  this loss;
- an SFT suffix context records legality but not the ordered affine products
  needed by (2).

These facts do not prove that every conceivable bounded quotient is
impossible.  They show precisely what is missing: either a new algebraic
identity that composes the growing ordered word (4) through a bounded phase,
or a proof that no such quotient exists.  Without that closure there is no
fixed TP2 weighted graph on which equality-subgraph refinement can even be
stated.  Reusing the TP3-011 computation before deriving this seam law would
therefore be structurally invalid.

TP3-001 has two free boundary phases and is not addressed here.  Nothing in
this comparison excludes TP2, TP3-011, TP3-001, or Prize Problem 1.

# Binary-wedge high-bit elimination

Date: 2026-09-02

Status: **ONE OUTPUT COORDINATE IS ELIMINATED UNIFORMLY.  THE BINARY-WEDGE
TARGET IS NOW A DETERMINISTIC ONE-BIT DEFECT EXCLUSION, BUT THAT EXCLUSION IS
UNPROVED.  PERIOD TWO AND P1 REMAIN OPEN.**

## 1. Exact triangular elimination

Let

```text
G_n(e)=P^n(I(e)).
```

Fix an endpoint prefix `W in {1,2}^n`.  If another binary endpoint symbol is
appended, the newest cell of `G_n` depends bijectively on that symbol.  More
precisely, with all earlier symbols fixed, its four-state map is one of the
eight affine permutations

```text
(h,l) -> (h+alpha, l+beta*h+gamma).                 (1)
```

This is an all-length statement.  The newest cell of `I` is obtained by
composing the boundary permutation with fixed-left `phi` rows along the new
dependency diagonal.  Applying `P` adds more fixed-left `phi` rows.  Every
such row and the boundary map belongs to the affine `D8` group, proving (1)
for arbitrary prefix length and arbitrary Peel depth.

On binary endpoint states `{1,2}`, the low bit is `1+h`.  Equation (1) has
output high bit

```text
H_out=h+alpha,                                      (2)
```

so exactly one of states `1,2` makes `H_out=1`.  Appending symbols from left
to right consequently proves:

> For every `W in {1,2}^n` and every `k>=1`, there is exactly one binary word
> `Q` of length `k` for which every cell of `G_n(WQ)` has high bit one.

No search horizon enters this uniqueness proof.

## 2. The remaining one-bit map

For `k=n+2`, call that unique word `Q_n(W)` and define

```text
Psi_n(W)_j = 1 + H(G_n(W Q_n(W))_j)
                 + L(G_n(W Q_n(W))_j).              (3)
```

The high bit is already one, so every output state is `2` or `3`, and
`Psi_n(W)` is simply its low/equality bit.  Therefore the repaired
binary-wedge horizon is exactly

```text
Psi_n(W) != 0^(n+2) and Psi_n(W) != 1^(n+2)          (4)
```

for every binary source `W` and every `n>=7`.  Constant zero in (4) is the
tail-2 target and constant one is the tail-3 target.

Thus the former two-coordinate boundary problem has one coordinate removed:
the suffix is not existentially quantified, and neither is its high bit.
The remaining problem is to prove that the deterministic defect word (3)
cannot be constant.  This is a reduction, not that proof.

## 3. The sharp-bound falsifier in these coordinates

For the exact `n=15`, tail-3 saturator

```text
W = 111122211212112,
```

high-bit elimination gives

```text
Q_15(W) = 12211111122111211,
Psi_15(W) = 11111111111111110.
```

Equivalently,

```text
G_15(W Q_15(W)) = 33333333333333332.
```

The first sixteen cells are the desired constant tail `3`, and the
seventeenth cell flips to state `2`.  This both replays the failure of the
preregistered sharp bound and shows why it does not falsify the repaired
`n+1` bound.

The source and forced suffix contain `11`, so this witness belongs to the
arbitrary-binary relaxation.  It is not a witness against the original
hard-core scale domain.

## 4. What this rules out

The useful triangular fact is not an asserted conserved parity of the
output.  It is the sequential elimination (2), which leaves the nonlinear
defect map `Psi_n` intact.

A proof should now target a recursion, ancestry relation, or forced change in
`Psi_n`.  Re-searching both endpoint bits or treating the forced suffix as
free duplicates an elimination that is already exact.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/binary_wedge_high_elimination.py
```

The checker exhausts the complete local affine maps and independent finite
controls for the elimination.  The proof of uniqueness is the composition
argument in Section 1; the controls are not an induction in `n`.

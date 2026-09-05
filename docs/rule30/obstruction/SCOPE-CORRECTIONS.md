# Scope corrections: two proposed Rule 30 consequences

Date: 2026-09-02

These notes delimit two complexity claims.  They do not dispute the useful
coordinate identities in the first work or assess every claim in the second.
Neither correction proves a Rule 30 prize problem.

## 1. Binomial--Lucas lifting and the center-query claim

This section concerns Tigran Nersissian, *Rule 30 Exact Binomial--Lucas
Lifting: From Boolean Logic to Integer Coefficients, Stirling Transfer, and
Support-Set Algebra* (Zenodo DOI
[`10.5281/zenodo.18921456`](https://doi.org/10.5281/zenodo.18921456)).  Its
support-set construction uses

```text
S_1={0}, S_2={1},
S_m=Inc((S_(m-1)*S_(m-2)) Delta S_(m-1) Delta S_(m-2)),
```

where `*` is parity convolution under bitwise OR.  Lucas evaluation gives

```text
b(m,n)=XOR_(r in S_m) binom(n,r) mod 2,
c(n)=b(n+1,n).
```

These identities reproduce the tested Rule 30 diagram.  The complexity issue
is the distinction between evaluating a supplied row representation and
constructing the row required by the moving center diagonal.

### Proposition A (`[U]`, algebraic identity)

Let `s_m` be the indicator of `S_m` and let `Z` be the Boolean subset-zeta
transform.  On every finite power-of-two table,

```text
Z(f*g)=(Zf)(Zg),
Z(Inc f)(n)=XOR_(0<=y<n)(Zf)(y).
```

Consequently the transformed support recurrence is

```text
b(m,n)=XOR_(0<=y<n) [
  b(m-1,y)b(m-2,y) XOR b(m-1,y) XOR b(m-2,y)
].
```

Taking the finite difference in `n` gives

```text
b(m,n+1)=b(m,n)
  XOR b(m-1,n)b(m-2,n)
  XOR b(m-1,n) XOR b(m-2,n),
```

which is the original rotated Rule 30 recurrence.  Thus the zeta transform is
an exact conjugacy, not a temporal shortcut by itself.

The paper's conditional evaluator assumes a predetermined row `m` and a
block decomposition of `S_m`.  On the center diagonal, `m=n+1`, and the
supplied `compute_Sm(target_m)` performs

```text
for m in range(3,target_m+1):
    advance the support recurrence once
```

before evaluation.  It therefore executes `n-1` sequential support advances.
No sublinear construction of the required row representation is supplied.

This correction does not show that no faster center algorithm exists.  It
shows only that the basis change and the published construction do not supply
the missing jump in `m`.

One-command replay from `experiments/rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_nersissian_block_audit.py
```

The tests check the support recurrence, block operations, Rule 30 center
agreement, OR-convolution diagonalization, and the increment/prefix-XOR
identity.  See the full [local audit](../REFUTATION-nersissian-log-query.md).

## 2. Arbitrary-row decision trees and the lone-seed index function

This section concerns the advertised implication in Dhashvin Deva,
*Algebraic Obstruction and Dual-Flow Consistency in Rule 30* (SSRN DOI
[`10.2139/ssrn.5908722`](https://doi.org/10.2139/ssrn.5908722)).  The archived
audit could not retrieve the full PDF, so this correction is intentionally
limited to the implication stated in the abstract; it is not an assessment of
the entire paper.

For fixed time `t`, let

```text
G_t : {0,1}^{2t+1} -> {0,1}
```

be the center cell after `t` Rule 30 steps as a function of an arbitrary
initial light cone.  Algebraic degree, algebraic immunity, essential
variables, and ordinary decision-tree complexity are properties of `G_t`.

The prize object is instead

```text
a(n)=G_n(delta_0),
```

whose input is the binary representation of `n` and whose initial row is
fixed once and for all.

### Proposition B (`[U]`, logical scope)

A lower bound

```text
D(G_n)=Omega(n)
```

for queries to arbitrary initial cells does not imply

```text
time(n |-> a(n))=Omega(n).
```

#### Proof

The first statement quantifies over assignments to `2n+1` cell variables.
The second first substitutes the lone seed, leaving no cell variables, and
then asks for uniform complexity as the index `n` varies.  A lower bound in
the former input model supplies no reduction between these two functions.

There is an internal Rule 30 control.  The arbitrary-input polynomial `G_t`
is the same object before any seed is substituted.  Substitution of the
all-zero initial row gives the center sequence `0,0,0,...`, which is periodic
and constant-time computable.  Hence no inference based only on the
arbitrary-input complexity of `G_t` can establish nonperiodicity or a time
lower bound for a designated seed orbit.  QED.

This correction is limited to the advertised transfer from arbitrary-row
complexity to the fixed lone-seed P1/P3 statements.  It does not assess
independent structural identities in the work.  See the full
[local audit](../CLAIM-AUDIT-deva-dual-flow.md).

The exact arbitrary-input ANF theorem and its own scope can be reviewed with:

```bash
sed -n '1,120p' docs/rule30/overnight/RESULTS-anf.md
```

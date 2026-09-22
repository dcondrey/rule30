# Audit of the claimed logarithmic Rule 30 query

Date: 2026-09-03

## Verdict

**The published `O(log n)` theorem does not compute the Rule 30 center bit
from input `n`.**  It evaluates a Lucas-basis row after a compressed
representation of that row has already been supplied.  On the center diagonal
the required row index is `m=n+1`, and the paper's own construction reaches
that representation by iterating every preceding row.  The omitted
construction is exactly the hard part of P3.

This audit does not refute the paper's exact coordinate rotation or its
support-set recurrence.  Those reproduce the Rule 30 diagram in the tested
range and may be useful coordinates.  It refutes only the inference from the
conditional row evaluator to an `O(log n)` center-query algorithm.

Primary source: Tigran Nersissian, *Rule 30 Exact Binomial--Lucas Lifting:
From Boolean Logic to Integer Coefficients, Stirling Transfer, and Support-Set
Algebra*, Zenodo DOI
[`10.5281/zenodo.18921456`](https://doi.org/10.5281/zenodo.18921456),
published 2026-03-09.  The public continuation is the author's
[Mathematica Stack Exchange question](https://mathematica.stackexchange.com/questions/318912/rule-30-finding-a-closed-formula-for-the-s-m-subset-recurrence),
which explicitly asks for a closed form or fast-doubling shortcut for the same
support recurrence.

Code: `experiments/rule30/nersissian_block_audit.py` and
`test_nersissian_block_audit.py`.

## 1. Exact content that survives

The paper defines finite support sets

```text
S_1={0}, S_2={1},
S_m=Inc((S_(m-1) * S_(m-2)) Delta S_(m-1) Delta S_(m-2)),
```

where `*` is parity convolution under bitwise OR.  It reconstructs the rotated
Rule 30 cell by

```text
b(m,n) = XOR_(r in S_m) binom(n,r) mod 2,
c(n) = b(n+1,n).
```

Lucas' theorem makes `binom(n,r)` odd exactly when `r` is a submask of `n`.
The masked block

```text
B(v,M)={v OR x : x is a submask of M},   v AND M=0,
```

therefore evaluates in one bit test:

```text
XOR_(r in B(v,M)) binom(n,r) = 1
iff v is a submask of n and n AND M=0.
```

The clean-room implementation independently reproduces the paper's support
sets through `S_8`, checks block convolution and increment against literal set
operations, and matches the repository's independent center-column generator
through the tested range.

## 2. The quantifier that breaks the complexity claim

The paper's complexity theorem begins by assuming a **predetermined row `m`**
and a decomposition

```text
S_m = Delta_(i=1)^k B(v_i,M_i),
```

with `k` treated as a constant.  Under those assumptions, evaluation costs
`O(k log n)` bit operations.  This conditional statement is sound.

P3 supplies only the binary digits of `n` and asks for `c(n)`.  Substituting
the paper's own diagonal identity changes both supposedly fixed parameters:

```text
m = n+1,
k = number of blocks in the representation of S_(n+1).
```

The representation is not advice included with the P3 input.  The paper's
function `compute_Sm(target_m)` constructs it with

```text
for m in range(3,target_m+1):
    advance the support recurrence once
```

and therefore performs `n-1` sequential support advances before the advertised
block tests even begin.  Its separate generation theorem charges an advance
in terms of the nonconstant block count `K_max` and mask width `W`; it proves
no sublinear bound on either quantity or on total construction work.

The paper later states this limitation directly in its Zeta-floor discussion:
computing the transform value requires the exact topology of `S_m` and the
generational expansion cannot be bypassed.  Thus its own construction does not
satisfy the hypothesis needed to turn the fixed-row evaluator into a center
query.

This is the same fixed-object/uniform-input distinction that invalidates
hardwired one-circuit-per-index arguments.  For every fixed `m`, any finite
row admits a constant-size description; P3 asks for one machine handling
unbounded `n` without receiving that description.

## 3. Reproduction and finite growth diagnostic

The following exact greedy-block counts are not an asymptotic lower bound.
They simply demonstrate that the `k=constant` hypothesis is not preserved
when the center diagonal moves through the support rows:

| `m` | 1 | 5 | 10 | 13 | 18 | 20 | 24 | 28 | 30 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| greedy blocks | 1 | 2 | 11 | 38 | 85 | 190 | 304 | 969 | 2,993 |

The published compressor is explicitly greedy and not minimal, so these
numbers do not prove that every block representation grows.  They do prove
that the supplied algorithm has no constant block count along the tested
diagonal.  Exact ESOP minimization, which the paper identifies as NP-hard,
would itself need a construction-cost analysis before it could support P3.

Reproduce from `experiments/rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  test_nersissian_block_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 nersissian_block_audit.py \
  --max-m 24 --check-centers 20
```

## 4. P2 side finding

The paper's horizontal-density discussion also cannot supply P2.  It applies
the piling-up formula after calling the block filters independent, but masked
block events can constrain the same input bit and need not be independent.
Already in the displayed decomposition

```text
S_8 = B(4,10) Delta B(8,1) Delta B(16,0),
```

the first event requires bit 3 of `n` to be zero while the second requires it
to be one.  They are mutually exclusive, not independent.  In addition,
horizontal density for fixed `m` would not control the moving diagonal
`m=n+1`; the paper acknowledges that second gap as a missing asymptotic
uncorrelation lemma.

## 5. Exact zeta conjugacy: why the basis change does not compress time

There is a sharper structural explanation for the missing shortcut.  Let
`s_m(r)` be the indicator of `S_m` and apply the Boolean subset-zeta transform

```text
(Zs_m)(n) = XOR_(r subseteq n) s_m(r).
```

This is exactly the Lucas evaluation `b(m,n)`.  On a finite power-of-two
index table, two elementary identities hold:

```text
Z(f * g) = (Zf)(Zg),
Z(Inc f)(n) = XOR_(0 <= y < n) (Zf)(y).
```

The first identity diagonalizes parity OR-convolution.  The second says that
ordinary integer increment becomes **exclusive prefix XOR**, including all
carry structure.  Applying both to the support recurrence gives the exact
transformed recurrence

```text
b(m,n) = XOR_(0 <= y < n) [
    b(m-1,y)b(m-2,y) XOR b(m-1,y) XOR b(m-2,y)
].
```

Taking the finite difference in `n` recovers

```text
b(m,n+1) = b(m,n)
             XOR b(m-1,n)b(m-2,n)
             XOR b(m-1,n) XOR b(m-2,n),
```

which is the original rotated Rule 30 triangle.  Thus the zeta transform is an
exact conjugacy between two descriptions of the same computation: in the
support basis the nonlinear product is OR-convolution and translation is
cheap; in the Lucas basis the product is pointwise and translation becomes a
prefix scan.  The apparent simplification merely moves the sequential
dependence from one operator to the other.

This is not a lower bound against every possible algorithm.  It does rule out
the basis change itself as the omitted fast-doubling argument: evaluating
`b(n+1,n)` still requires a uniform way to jump across the growing `m`
dimension or summarize those prefix scans.  Exhaustive finite-vector tests
pin the increment identity, and an independent test pins diagonalization of
OR-convolution.

## 6. Reusable insight

The support recurrence is another exact realization of the archive's central
lesson:

```text
cheap evaluation after a seam/state is supplied
does not imply cheap construction of the seam/state from n.
```

It gives P3 a sharper kill condition.  Any future dyadic block proposal must
bound the **total uniform cost of constructing only the center-observational
state for `S_(n+1)`**, not the cost of evaluating a precomputed row.  For P2,
the block basis can express bit constraints exactly, but a valid cancellation
argument must keep overlaps rather than invoke independence.

No prize problem is solved by this audit.

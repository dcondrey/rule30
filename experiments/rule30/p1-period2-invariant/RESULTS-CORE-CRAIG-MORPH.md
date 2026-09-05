# Peel/Craig morph and the exact restart obstruction

Date: 2026-09-01

Status: **ONE UNANNOTATED CRAIG RECURSION IS KILLED EXACTLY.  HEIGHT
PROJECTION REDUCES THE ANNOTATED VERSION TO THE STRONGER OPEN FORMULA
`C(m,m)`.**  This is not active-core mortality or a period-two proof.

## 1. The endpoint morph

Let `I` be the inverse terminal-cone bijection, `T=I^{-1}`, and let

```text
P(x)_j = phi(x_j,x_(j+1))
```

be zero-indexed Peel.  Conjugate Peel to terminal endpoint coordinates:

```text
F(e) = T(P(I(e))).                                      (1)
```

The endpoint-prefix grammar already proved in
`RESULTS-RANK-ZERO-REDUCTION.md` is

```text
I(qe) = (B(q), phi(q,I(e)_0)) . P(I(e)).                (2)
```

For prefix state `2`, (2) and four local table rows give the exact section

```text
F(2e) = g(e_0) . F(e),       g=(1,0,2,3).               (3)
```

Here is the complete local calculation.  Put `x_0=B(e_0)` and
`a=phi(2,x_0)`.  The two cells exposed by peeling (2) agree with the prefix
grammar for `g(e_0)` because

| `e_0` | `B(e_0)` | `a` | `g(e_0)` |
|---:|---:|---:|---:|
| 0 | 3 | 1 | 1 |
| 1 | 2 | 0 | 0 |
| 2 | 1 | 2 | 2 |
| 3 | 0 | 3 | 3 |

and, in every row,

```text
B(g(e_0)) = phi(1,a),
phi(g(e_0),r) = phi(a,r) for every r in {0,1,2,3}.      (4)
```

Equations (2)--(4) prove (3) for an arbitrary suffix; no finite-horizon
inference is involved.  `core_craig_morph.py` checks all entries of (4)
directly and then audits the resulting all-word identity on a finite control
corpus.

## 2. Exact accepting-side theorem

Call an endpoint hard-core when it lies in `{1,2}^H` and contains no `11`.
For every hard-core endpoint `e` of length at least two,

```text
F(e) is hard-core  iff  e=2^H,                          (5)
F(2^H)=2^(H-1).                                        (6)
```

**Proof.**  If `e` starts with `1`, hard-core legality makes it start with
`12`; causality and the direct base calculation `F(12)=3` make `F(e)`
illegal immediately.  Otherwise let its first `1` occur at position `k>=1`.
Iterating (3) shows that `F(e)` begins with `2^(k-1)0`, again illegal.  If no
`1` occurs, repeated use of (3), with `g(2)=2`, proves (6).  This exhausts the
hard-core alphabet.  QED.

Writing `S_H=I(HC_H)`, (5) is equivalently the all-height singleton law

```text
P(S_H) intersect S_(H-1) = { I(2^(H-1)) }.             (7)
```

Thus a literal separator pullback `I_(H-1)(P(x))` has the wrong polarity on
all but one accepting cut.  The failure is structural and parametric, not a
failed small-template search.

## 3. What an adaptive formula would have to retain

Equation (3) identifies the exact restart data.  If the first endpoint `1`
occurs at position `k`, the next endpoint coordinate contains a forbidden
state at position `k-1`.  Its location is unbounded.  An evolving Craig
formula therefore cannot retain merely a fixed boundary bit or one of a
fixed list of exceptional cuts.  It must carry an indexed defect position,
an equivalent ordered word, or a quantified clause capable of moving that
position.

This does not rule out such an adaptive formula.  It kills the unannotated
Peel pullback and isolates the minimal growing annotation forced by the
accepting language.

## 4. Height projection and the remaining lemma

Let `pi` delete the last coordinate of a vertical cut.  The feed generators,
`I`, and `T` are all causal in height, so exactly

```text
pi(S_H) = S_(H-1),
pi(R_H) = cuts of height H-1 reachable in at most H-2 symbols.   (8)
```

Recall that `R_H` itself uses at most `H-2` symbols.  Consequently

```text
pi(R_H) intersect S_(H-1) is nonempty
iff C(H-1,H-1) is SAT.                                 (9)
```

Leading input symbol `0` acts trivially on the zero cut, so “at most” and a
padded core of length exactly `H-1` agree in (9).  This is the precise
one-extra-input shell introduced by projection.

The original diagonal target is `C(H-1,H)`.  Therefore the clean projection
repair would follow from the stronger all-length lemma

```text
C(m,m) is UNSAT for every m except the explicit small exceptions.          (10)
```

The exceptions `C(2,2)` and `C(6,6)` have respective words

```text
13,       212013,
```

and both fail on the immediately following row.  Solver-free exact cut
enumeration finds no further exception through the existing preregistered
interpolant range, but that is only finite evidence.  No induction for (10)
is known.  In particular, height projection has not made mortality free: it
has exposed the exact stronger shell lemma that an adaptive Craig update
must prove.

## 5. Route disposition

The literal Peel-recursive Craig mechanism is exhausted by the parametric
law (7).  Its viable mutation is now stated without hidden bounds:

> Build an indexed restart separator that follows the forbidden coordinate
> from (3), or prove the stronger shell exclusion `C(m,m)` apart from the two
> displayed exceptions.

Either result would imply `C(m,m+1)` and close the active-core period-two
rung.  Neither is proved here.  P1, P2, and P3 remain open.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/core_craig_morph.py
```

The script is solver-free.  It checks the local section table, causal height
projection, the endpoint morph, and the singleton accepting overlap.

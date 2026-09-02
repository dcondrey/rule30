# Deterministic halving: exact implication and morph obstruction

Date: 2026-09-01

Status: **THE DETERMINISTIC HALVING CONJECTURE IS REDUCED TO A ROWWISE
PREFIX IMPLICATION.  SCALAR GAP CONTRACTION, RAW BLOCK EMBEDDING, AND A
PARENT-CONTINUATION-ONLY MORPH ARE ALL KILLED.  THE REQUIRED TRIANGULAR
ELIMINATION WITH THE FREE LEFT HALF RETAINED REMAINS OPEN.**

## 1. Exact proof target

For a hard-core word `W` of length `n`, let

```text
h = ceil(n/2)+1,
L = the prefix of W of length floor(n/2).
```

The deterministic recurrence is

```text
s_c(W) <= h+s_2(L),       c in {2,3}, n>=4.           (1)
```

Because survival length is the length of the initial legal prefix, (1) is
equivalent to the family of rowwise implications

```text
W survives h+r parent rows  =>  L survives r tail-2 rows              (2)
```

for every `r>=1`.  This is the clean all-length statement.  It avoids
guessing an equality between the two forced endpoint words; only hard-core
legality must be transported.

As recorded in `RESULTS-PROJECTED-DIAGONAL-HALVING.md`, (1) implies the
rank-zero separator by induction on `n`.

## 2. Earlier killed transports

Three simpler ways to prove (2) are now excluded.

1. The exact fan-out family and the transitions `21021 -> 21110` and
   `2111021 -> 2110100` kill max-gap, total-gap, logarithmic, dyadic-capacity,
   and gap-multiset contraction, after one or two inherited scans.
2. The parent endpoint suffix after the charged rows is not a literal prefix
   of any half-word scale extension.
3. A fixed transformation of the parent continuation and its forced right
   half cannot produce the child continuation.

The third obstruction is sharpened below.

## 3. Exact parent-only morph collision

At `n=9`, tail `3`, the five words

```text
121222122  122222122  212222122  221222122  222222122
```

share all of the following parent data:

```text
right half:                 22122
complete forced extension: 122122210200303022
parent survival:            8
charge h:                   6.
```

Their left halves are respectively

```text
1212, 1222, 2122, 2212, 2222.
```

Every tail-2 child survives exactly two rows, so equality holds in (1), but
the complete child extensions split between

```text
22001323,
12321223,
```

and their first illegal child symbols split between `0` and `3`.
`constant_tail_halving_morph_audit.py` checks these statements literally.

Therefore no function of `(n,c,right-half,parent-forced-extension)` alone can
recover even the first child defect.  In particular, the unique midpoint
right half and unique parent continuation seen in the survivor-cylinder
census do not constitute a closed residual mode.  The free left half is
load-bearing.

## 4. Exact remaining lemma

A proof of (2) must eliminate the forced right half while retaining symbolic
dependence on `L`.  One suitable formulation is:

> After imposing the parent hard-core clauses for rows `0,...,h+r-1`, derive
> the child tail-2 hard-core clauses for rows `0,...,r-1` as Boolean
> consequences in the variables of `L`, uniformly in `n` and `r`.

This is an indexed triangular-elimination theorem.  A fixed finite boundary
mode, a symbolwise conjugacy, or a scalar potential is insufficient.  The
same conclusion is visible in the Craig morph: a defect position moves with
the first non-`2` endpoint coordinate and cannot be compressed to one fixed
exception bit.

The recurrence still has no counterexample in the registered exhaustive and
random corpora.  Those corpora are evidence only; the implication (2) is the
irreducible all-length obligation for this route.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_halving_morph_audit.py
```

The collision kills the stated universal parent-only morph without relying
on any search horizon.

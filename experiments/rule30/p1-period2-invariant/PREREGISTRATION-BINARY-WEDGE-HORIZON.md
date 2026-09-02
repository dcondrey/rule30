# Preregistration: binary-wedge horizon

Date: 2026-09-02

Status: frozen after exhaustive exploratory lengths `n<=10` and before the
held-out exact range `11<=n<=20`.

## Candidate

Fix a source word `W in {1,2}^n` and a constant inverse-terminal cut symbol
`c in {2,3}`.  Append endpoint symbols uniquely so that every newly exposed
cut symbol is `c`, and let `b_c(W)` be the length of the initial appended
block that remains in `{1,2}`.  Put

```text
M_c(n)=max {b_c(W): W in {1,2}^n}.
```

The candidate all-length bound is

```text
M_c(n) <= n for every n>=7 and c in {2,3}.          (BWH)
```

Equivalently, there is no binary word `f` of length `2n+1` satisfying

```text
P^n(I(f))=c^(n+1).
```

This uses the proved rotated-Peel identity.  It is strictly stronger than
the three-row late-pull diagonal, which only needs to exclude a particular
terminal pull after `n+2`, `n+3`, or `n+4` binary continuation symbols.

## Discovery data

Exhaustive enumeration through `n=10` gave the following maxima:

```text
n:         1 2 3 4 5 6 7 8 9 10
M_2(n):    1 2 1 2 2 9 7 6 5  9
M_3(n):    2 1 4 3 8 6 6 7 8  9
```

Thus `(BWH)` holds throughout its exploratory range.  The two late
hard-core-free CNF exceptions are visible as `M_3(5)=8` and `M_2(6)=9`;
they do not extend beyond the proposed base threshold.

## Held-out test

1. Exhaust every binary source at lengths 11 through 20 for both tails.
2. Test deterministic random binary sources at lengths
   `24,32,48,64,96,128`, retaining the exact maximum observed continuation.
3. Cross-check the bit-sliced continuation and first-nonbinary position
   against the literal inverse-cone constructor through length seven.

Any exact source with `b_c(W)>n` at `n>=7` falsifies `(BWH)`.  A finite pass
is evidence only.  Completion still requires an all-length diagonal-parity,
inverse-Peel, or induction proof.

## Interpretation

The Wolfram Community diagonal recurrence and Rowland's right-bijective
argument both isolate a cumulative-XOR mechanism.  In the present
coordinates, the forced endpoint high bit is the parity of activity on the
newest dependency diagonal.  `(BWH)` asks whether the accompanying low-bit
constraint forces a nonbinary state by the diagonal `j=n`.  The forum
observations motivate this coordinate choice; they do not prove the bound.

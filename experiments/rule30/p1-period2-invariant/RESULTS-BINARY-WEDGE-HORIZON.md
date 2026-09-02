# Binary-wedge horizon: a simpler sufficient target

Date: 2026-09-02

Status: **THE SHARP PREREGISTERED BOUND IS FALSIFIED AT `n=15`.  THE
ONE-CELL-WEAKER BOUND THAT STILL IMPLIES DLP HAS ZERO EXACT FAILURES THROUGH
`n=20`, BUT IS UNPROVED.  PERIOD TWO AND P1 REMAIN OPEN.**

## 1. Definition

For `W in {1,2}^n` and constant inverse-cut symbol `c in {2,3}`, triangular
right-permutivity uniquely forces endpoint symbols `Q_0,Q_1,...` so that
each newly exposed inverse-terminal cut cell equals `c`.

Let `b_c(W)` be the length of the initial block of `Q` contained in
`{1,2}`, with no hard-core/no-`11` requirement, and define

```text
M_c(n) = max { b_c(W) : W in {1,2}^n }.
```

The preregistered candidate was

```text
M_c(n) <= n.                                      (BWH)
```

The exact held-out search falsified it.  The repaired live target is

```text
M_c(n) <= n+1 for every n>=7 and c in {2,3}.      (BWH+)
```

No post-hoc claim is made that the repaired threshold was preregistered.
It is retained because `n+1`, not `n`, is the exact threshold sufficient
for the existing reduction.

## 2. Why `(BWH+)` closes period two

If a DLP witness exists at length `n`, tail `c`, and residue
`r in {0,1,2}`, its forced continuation has length

```text
n+r+2 >= n+2
```

and every continuation symbol belongs to `{1,2}`.  It would therefore give
`b_c(W)>=n+2`, contradicting `(BWH+)`.  The no-`11` condition and the
terminal-pull condition are not needed for this implication.

Equivalently, using the proved rotated-Peel identity, `(BWH+)` says there is
no binary word `f` of length `2n+2` with

```text
P^n(I(f)) = c^(n+2).                               (1)
```

Thus an all-length proof of `(BWH+)` implies DLP, both constant-tail
separators, the rank-zero separator, and exclusion of the nonconstant
period-two center trace.  It would not by itself solve full P1.

## 3. Exact census and the falsifier

Exhaustive enumeration gives:

| `n` | `M_2(n)` | `M_3(n)` |
|---:|---:|---:|
| 1 | 1 | 2 |
| 2 | 2 | 1 |
| 3 | 1 | 4 |
| 4 | 2 | 3 |
| 5 | 2 | 8 |
| 6 | 9 | 6 |
| 7 | 7 | 6 |
| 8 | 6 | 7 |
| 9 | 5 | 8 |
| 10 | 9 | 9 |
| 11 | 9 | 8 |
| 12 | 9 | 11 |
| 13 | 10 | 10 |
| 14 | 11 | 11 |
| 15 | 11 | **16** |
| 16 | 14 | 14 |
| 17 | 13 | 13 |
| 18 | 17 | 18 |
| 19 | 18 | 16 |
| 20 | 16 | 17 |

The bold entry falsifies `(BWH)`.  One exact witness is

```text
n = 15
c = 3
W = 111122211212112
Q = 1221111112211121 0 332...
                            ^ first nonbinary symbol
```

It survives exactly `16=n+1` appended symbols, so it saturates rather than
falsifies `(BWH+)`.

The bit-sliced implementation was cross-checked against the literal
inverse-cone constructor on 6,152 generated cells through source length
seven.

## 4. Long falsification pressure

A deterministic random search of 20,000 words at each length found:

| `n` | observed tail-2 maximum | observed tail-3 maximum |
|---:|---:|---:|
| 24 | 15 | 15 |
| 32 | 13 | 14 |
| 48 | 13 | 13 |
| 64 | 14 | 13 |
| 96 | 14 | 14 |
| 128 | 18 | 15 |

The separate evolutionary falsifier finds the exact `n=15`, tail-3
saturator under a small deterministic control run.  Neither random nor
evolutionary searches are evidence of an all-length bound beyond their
role as adversarial falsifiers.

## 5. Structural observations

At several exact maxima, many distinct source words share one forced
continuation and die on the same next cell.  At the exceptional `n=15`,
tail-3 maximum, 18 sources reach the 16-cell plateau, all with the displayed
`Q`, and all next force state `0`.  This suggests a synchronized phase
catastrophe rather than a source-by-source local obstruction.

In the exact coordinates `q=(H,L)` and `E=1+H+L`, binary legality is `E=0`.
The local Peel rule is

```text
H(phi) = H_R + 1 + E_L + E_L H_L,
E(phi) = E_R + H_R(H_L + E_L).
```

Forcing a constant newest cut determines the appended high bit by the
activity parity on its complete dependency diagonal.  `(BWH+)` is therefore
the concrete missing statement:

> A length-`n` zero-defect source cannot satisfy both output-coordinate
> legality equations through diagonal `n+1`.

The source-assumption cores are not generally singleton and their positions
are irregular.  A proof should expect a branched ancestry or a nonlinear
clause, not one propagating defect and not a fixed linear parity separator.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/binary_wedge_horizon.py \
  --exact-first 11 --exact-last 20 --random-per-length 20000

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/binary_wedge_adversary.py \
  --lengths 15 24 32 --population 128 --generations 80
```

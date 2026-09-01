# Moving endpoint-flip cocycle

Date: 2026-09-01

Status: **A UNIFORM COMPACT-INFLUENCE COCYCLE IS PROVED.  IT TURNS THE
TIME-DEPENDENT-INVARIANT IDEA INTO AN EXACT SEQUENCE OF FINITE CUT REWRITES
AND EXPLAINS WHY THEIR SUPPORT FRONTIER CAN KEEP MOVING OUTWARD.  IT DOES NOT
YET GIVE A WELL-FOUNDED MEASURE OR PROVE THE RANK-ZERO SEPARATOR.**

The exact controls are in `endpoint_flip_cocycle.py`.

## 1. Compact influence of one endpoint coordinate

For `x=I(e)`, the inverse-cone diagonal recurrence gives the proved dependency
window

```text
x_t depends only on e_(floor(t/2)),...,e_t.           (1)
```

Therefore changing endpoint coordinate `e_k` can affect only

```text
x_k,...,x_(2k+1).                                    (2)
```

It affects `x_k` nontrivially because the new-endpoint/new-cut diagonal map is
a permutation.  Thus (2) is an exact compact update interval, not merely a
light-cone upper bound.

## 2. The adaptive flip cocycle

Let `e` be hard-core.  Replacing any occurrence of endpoint state `1` by `2`
preserves the hard-core language.  List the positions of its `1`s as

```text
k_0 < k_1 < k_2 < ... .
```

Define `e^(n)` by changing the first `n` of those symbols to `2`, and put
`x^(n)=I(e^(n))`.  Equation (2) gives the exact time-dependent update

```text
x^(n+1)_t = x^(n)_t       outside [k_n,2k_n+1].       (3)
```

Every formula in the sequence changes its support and coefficients at the
next endpoint defect.  This is a literal inductive cocycle of the kind that a
single static weight cannot represent.

If `x^(0)` is finite support, every `x^(n)` is finite support: only finitely
many coordinates are rewritten at each stage.  Yet `e^(n)` converges
coordinatewise to `2^omega`, whose inverse cut is `(12)^omega`.  The supports
of `x^(n)` must therefore escape to infinity.  This is an exact compactness
mechanism behind the moving information wall; finite support at every stage
does not supply a uniform support bound.

## 3. Necessary overlap condition

The all-`2` endpoint has the everywhere-nonzero inverse cut `(12)^omega`.
If a hard-core endpoint window

```text
e_(floor(t/2)),...,e_t
```

contains no `1`, equation (1) makes `x_t` equal to that nonzero all-`2`
baseline value.  Hence an eventually-zero or eventually-`3` inverse cut
requires every sufficiently late dependency window to contain an endpoint
`1`.  For an eventually-`2` cut the same conclusion is required at every
sufficiently late even `t`, where the baseline symbol is `1` rather than `2`.

Equivalently, the influence intervals

```text
[k_n,2k_n+1]
```

must cover a tail of the cut axis (or all its late even coordinates in the
constant-`2` case).  Since each interval ends at the odd coordinate
`2k_n+1`, even-coordinate coverage gives the same gap bound.  Consecutive
endpoint defects therefore satisfy, eventually,

```text
k_(n+1) <= 2k_n+2.                                   (4)
```

Hard-core legality supplies the opposite local spacing `k_(n+1)>=k_n+2`.
These inequalities leave a large class of possible aperiodic defect sets, so
the covering condition alone is not a contradiction.

## 4. Consequence for an evolving proof formula

A defensible dynamic certificate must retain the ordered active intervals
whose right endpoints have not passed the current cut coordinate.  Updating
the certificate at `k_n` may rewrite only the exact zone in (3), and must prove
that overlapping zones cannot collectively turn the `(12)^omega` baseline
into a zero/constant-2/constant-3 tail.

The result rules out a simpler hope: support size of the successive formulas
need not decrease.  It can move outward while each individual formula remains
finite.  OpenEvolve should therefore mutate recursive overlap/rewrite
certificates, not another scalar support score.

## 5. Reproduction

From `13-rule30/`:

```bash
uv run python \
  experiments/rule30/p1-period2-invariant/endpoint_flip_cocycle.py
```

The checker exhausts the full four-state endpoint alphabet through length 7,
the complete hard-core language through length 16, and the all-`2` window
consequence on the same hard-core corpus.

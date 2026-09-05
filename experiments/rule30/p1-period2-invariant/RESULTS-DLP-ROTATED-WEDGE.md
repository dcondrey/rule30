# Rotated-wedge form of the late-pull diagonal

Date: 2026-09-02

Status: **DLP NOW HAS A LOSSLESS SINGLE-WORD FORMULATION.  THIS REMOVES THE
PADDING AND FORCED-EDGE STATE, BUT THE RESULTING WEDGE EXCLUSION IS STILL
UNPROVED.  PERIOD TWO AND P1 REMAIN OPEN.**

## 1. Exact conjugacy

Let `I` be the inverse-terminal diagonal and

```text
P(x)_i = phi(x_i,x_(i+1)).
```

Fix `n>=1`, `r in {0,1,2}`, and `c in {2,3}`.  In the scale formulation,
start from the endpoint prefix

```text
E = 0^n W Q,
```

where `W` has length `n` over `{1,2}` and `Q` is the forced continuation of
length `n+r+2`.  Put `f=WQ`, so `f=sigma^n E`.  The proved iterated rotated
Peel identity gives, cell by cell,

```text
P^n(I(f)) = sigma^(2n) I(E).                         (1)
```

The right side of (1) is precisely the cut row constrained by the scale
construction.  Consequently all of its exposed cells equal `c` exactly
when

```text
P^n(I(f)) = c^(n+r+2).                              (2)
```

No limit, periodic extension, or bounded-data inference is used in (1).

## 2. Equivalent finite-word exclusion

The three-row late-pull diagonal `(DLP)` is equivalent to the following one
map statement.

> **Rotated wedge `(RW)`.**  There are no `n>=1`, `r in {0,1,2}`,
> `c in {2,3}`, and binary word `f` of length `2n+r+2` such that:
>
> 1. the suffix `f[n:]` is hard-core, including its junction with `f[n-1]`;
> 2. `P^n(I(f))=c^(n+r+2)`; and
> 3. `f[-3:-1]=12`.

The first `n` symbols of `f` need only lie in `{1,2}`; they need not avoid
`11`.  The last condition is exactly the nonfinal endpoint pull: the final
three endpoint symbols are `12a`, with `a in {1,2}`.  Thus `(RW)` neither
strengthens nor weakens DLP.

This formulation replaces the growing dependency edge, leading zero
padding, forced endpoint decoder, and relative row index by one equality of
finite words.  Equivalently, if

```text
F = I^(-1) o P o I,
```

then (2) is

```text
F^n(f) = I^(-1)(c^(n+r+2)).                          (3)
```

Equation (3) is the clean endpoint-coordinate target for an indexed
interpolant or induction.

## 3. A necessary guardrail

Applying one more Peel row to (2) gives

```text
P^(n+1)(I(f)) = 0^(n+r+1),                           (4)
```

because `phi(2,2)=phi(3,3)=0`.  Therefore a proof that simply excludes a
long zero row is not a new shortcut: it is a finite-wedge version of the
rank-zero separator itself.  A successful induction must use the terminal
pull `12a`, the binary source boundary, or both.  Discarding those data
returns to the already open rank-zero problem.

Likewise, the known six-cell terminal-patch counterexample still applies.
The gain from `(RW)` is algebraic compression, not locality.

## 4. Independent controls

`dlp_rotated_wedge.py` constructs the padded and unpadded words independently
and checks both (1) and the exact DLP predicate.  Through every binary source
word of length seven it verifies

```text
rotated finite-wedge cells:     13,800
DLP predicate equivalences:      1,524.
```

This finite corpus checks the implementation; the proof of (1) is the
all-length rotated-Peel identity.  The exclusion `(RW)` remains the sole
unproved step.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/dlp_rotated_wedge.py
```

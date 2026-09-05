# Pull-row alpha support

Date: 2026-09-02

Status: **A STRICTLY WEAKER SUFFICIENT LEMMA HAS ZERO FAILURES THROUGH EVERY
HARD-CORE WORD OF LENGTH 23.  THE ALPHA COORDINATE HAS AN EXACT QUEUE-PARITY
FORMULA.  THE ALL-LENGTH SUPPORT LEMMA IS NOT PROVED, SO PERIOD TWO REMAINS
OPEN.**

## 1. Reduced sufficient lemma

For a hard-core block `W` of length `n`, use the zero-prefix scenarios

```text
W^(k)=0^k W[k:n],       0<=k<=n,
```

and let `alpha_(j,k)` be the high-bit translation coordinate of the newest
affine boundary map at forced extension row `j`.  A row is a pull row when
the original forced endpoint makes transition `1 -> 2`.

The new target is:

> **Pull-row alpha support (PAS).**  At every nonfinal surviving pull row
> `j`, some `k` with `j<=k<n` satisfies
> `alpha_(j,k) != alpha_(j,k+1)`.

PAS is weaker in three independent ways than the previous projected-support
target: it uses one affine bit rather than two, asks only about pull rows, and
needs only one support point rather than a matching.

## 2. Why PAS proves the period-two rung

The endpoint/event bridge and dyadic exceptional-family separator give the
exact dichotomy

```text
immortal relevant queue
  -> endpoint eventually 2, already excluded
     OR infinitely many pull rows.                    (1)
```

Let an absolute pull occur at endpoint position `m=3n+r`, where
`n=floor(m/3)` and `0<=r<=2`, sufficiently far beyond the onset of the
constant cut tail.  The scale block `W=e[n:2n]` sees this pull at forced row
`j=m-2n=n+r>=n`.  PAS demands `j<=k<n`, an empty interval.  Infinitely many
absolute pulls therefore contradict PAS; the eventually pull-free branch is
already excluded.  This proves the rank-zero separator, after which the
existing Peel-rank reduction proves the nonconstant period-two exclusion.

No pull ancestry injection and no quantitative estimate such as
`h<=floor((r+1)/2)` is needed.  PAS does not address periods above two.

## 3. Exact alpha/activity-parity identity

The local map with fixed left state `q` has affine high-bit translation

```text
alpha_local(q) = [q != 0].                            (2)
```

The boundary permutation has `alpha=1`, and alpha is additive under affine
composition.  If `E` is the current raw dependency edge and `p` the previous
endpoint, the newest affine map therefore has

```text
alpha = 1 XOR [p != 0]
          XOR parity {i < |E|-1 : E_i != 0}.          (3)
```

Writing `R=reverse(E)` gives

```text
alpha = 1 XOR [p != 0]
          XOR parity {i>=1 : R_i != 0}.               (4)
```

On a surviving hard-core row, `p` is state `1` or `2`, so

```text
alpha = parity {i>=1 : R_i != 0}.                     (5)
```

Both constant tails have high bit one.  Inverting the newest affine map
therefore forces endpoint high bit `1 XOR alpha`.  Thus a pull `1 -> 2` is
exactly an original-scenario temporal transition

```text
alpha: 1 -> 0.                                        (6)
```

PAS is consequently an exact parity-flux statement: the temporal loss in
(6) must have a nonzero spatial zero-prefix finite difference somewhere on
or to the right of the row diagonal.  Equations (2)--(6) are all-length
identities.  The script independently checks them on 6,652 literal raw queue
states through source length six.

## 4. Exact finite results and negative controls

The discovery range through length 18 contained

```text
word/tail cases:             35,416
nonfinal pull rows:           2,641
alpha-support failures:           0.
```

After freezing PAS, the held-out lengths 19--23 contained

```text
word/tail cases:            357,414
nonfinal pull rows:          28,954
alpha-support failures:           0
projected-support failures:       0.
```

These are finite data only.

Several tempting strengthenings are already false:

- The diagonal token `k=j` need not work.  The smallest retained case is
  tail `3`, `W=122221`, survival two, pull row zero; its projected support is
  `{2,4,5}` and its alpha support is `{2,4}`.
- The first alpha witness can lie at least twelve positions to the right of
  `j`: at length 17, tail `2`, `W=12122212212122222`, row `1`, the alpha
  support is `{13,16}`.  The previous reported value nine accidentally
  tracked the two-coordinate projected witness rather than alpha.  A
  fixed-radius local proof is unsupported.
- Alpha support need not have odd cardinality, need not contain both source
  symbols, and may be a singleton.  A source-symbol or parity selector is
  false.
- If arbitrary four-state source symbols are allowed, PAS already fails for
  `W=01`, tail `2`, survival two, row zero.  The active source alphabet
  `{1,2}` is load-bearing.  Exploratorily, the `no 11` condition itself was
  unnecessary through all binary source words of length nine, but no
  all-length relaxation is claimed.

The proven physical center-controlled reversal also descends on a `1 -> 0`
phase, but it cannot be imported here: that bit is the physical center,
whereas (6) concerns an inverse-cone affine coordinate.  No conjugacy between
those systems is known.

## 5. Exact remaining contrapositive

For the complete family of raw reversed dependency queues `R_(j,k)`, define
`alpha_(j,k)` by (4).  It remains to prove:

> If `alpha_(j,k)=alpha_(j,k+1)` for every `j<=k<n`, then the original
> endpoint cannot make a surviving nonfinal transition `1 -> 2` at row `j`.

The proof must retain the ordered scenario queues or derive a lossless
noncrossing quotient.  Endpoint telescoping is insufficient, since alpha
changes can cancel in pairs, and the witness displacement is not locally
bounded.  Equations (3)--(6) suggest a discrete parity-flux or triangular
Stokes argument; that argument has not yet been found.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_row_projected_support.py \
  --first-length 19 --last-length 23
```

The preregistrations are
`PREREGISTRATION-PULL-ROW-PROJECTED-SUPPORT.md` and
`PREREGISTRATION-PULL-ROW-ALPHA-SUPPORT.md`.

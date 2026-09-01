# Peel-lift monoid and dyadic propagation

Date: 2026-09-01

Status: **A PERIODICITY-LIFTING LEMMA IS PROVED.  IT PROPAGATES DYADIC
PERIODICITY THROUGH EVERY ENDPOINT SHIFT, BUT IT DOES NOT YET FORCE THE
HARD-CORE ENDPOINT TO BE EVENTUALLY CONSTANT.  THE PERIOD-TWO THEOREM AND
PRIZE PROBLEM 1 REMAIN OPEN.**

The exact checker is `peel_lift_monoid.py`.

## 1. Inverting one Peel row

Write

```text
P(y)_t = phi(y_t,y_(t+1)).
```

For every fixed left state `l`, the map `r -> phi(l,r)` is a permutation.
Hence, for an output symbol `q`, there is a unique map `g_q` satisfying

```text
y_(t+1) = g_q(y_t)  iff  phi(y_t,y_(t+1)) = q.
```

In image-tuple notation the four maps are

```text
g_0=(0,3,2,3)  g_1=(1,2,3,2)
g_2=(3,1,1,1)  g_3=(2,0,0,0).
```

Their transformation monoid has exactly 13 elements:

```text
(0,0,0,0) (0,1,2,3) (0,2,2,2) (0,3,2,3)
(1,1,1,1) (1,2,3,2) (1,3,3,3)
(2,0,0,0) (2,2,2,2) (2,3,2,3)
(3,1,1,1) (3,2,3,2) (3,3,3,3).
```

Direct closure under all four generators verifies the list.  Every cyclic
component of every listed transformation has length one or two.

## 2. Periodicity-lifting lemma

**Lemma.** If `P(y)` is ultimately periodic with a period dividing `p`, then
`y` is ultimately periodic with a period dividing `2p`.

**Proof.** After the output enters its `p`-periodic tail, one block of `p`
output symbols advances `y_t` by a fixed composition of the maps `g_q`.
That composition belongs to the displayed 13-element monoid.  Its orbit on
the four possible states eventually enters a cycle of length one or two.
Therefore the lifted row eventually repeats after `p` or `2p` steps.  QED.

In particular, a lift of an ultimately dyadic-periodic Peel image is itself
ultimately dyadic-periodic.  No odd factor can be introduced by peeling
backward.

## 3. Combination with the rotated identity

Put

```text
x^j = I(sigma^j e).
```

The proved rotated identity is

```text
P(x^(j+1)) = sigma^2 x^j.
```

If `x^0=I(e)` is ultimately periodic with period `2^k`, the lemma inductively
shows that every endpoint-tail cut `x^j` is ultimately dyadic-periodic, with
a period dividing `2^(k+j)`.

This is the missing rigorous bridge between a dyadic initial cut and all
successive endpoint tails.  It does **not** give a uniform period bound in
`j`, so it does not imply that `e` is eventually periodic.

## 4. Exact controlled-lift reformulation

Let

```text
a_j = x^j_0 = B(e_j).
```

For a hard-core endpoint, `a_j` belongs to `{1,2}` and the word `a` contains
no factor `22` (because `B` interchanges endpoint states `1` and `2`).  The
entire two-dimensional inverse-cut array is then determined by

```text
x^(j+1)_0     = a_(j+1),
x^j_1         = phi(B(a_j),a_(j+1)),
x^(j+1)_(t+1) = g_(x^j_(t+2))(x^(j+1)_t).            (1)
```

The middle line is essential boundary data; the rotated Peel equation alone
does not characterize inverse-terminal cones.  On admissible hard-core
pairs it reduces to

```text
(a_j,a_(j+1)) = (1,1) or (2,1)  ->  x^j_1=2,
(a_j,a_(j+1)) = (1,2)           ->  x^j_1=0.
```

The desired dyadic lock is now the following precise statement:

> Every infinite solution of (1) for which `x^0` is ultimately
> dyadic-periodic and `a` is a `{1,2}` word without `22` is eventually the
> fixed solution `a_j=1`, `x^j=(12)^omega`.

This statement would imply that the endpoint is eventually `2^omega`; the
already proved reachability separator would then finish the nonconstant
period-two exclusion.

The reverse-period trees for periods `2,4,8,16` verify bounded instances of
this lock, but no uniform argument preventing an unbounded sequence of
period doublings is known yet.

## 5. Relation to the `(z+1)`-adic proposal

The sound dyadic operator is `Delta=1+S`, where `S` is temporal shift.  On an
`N=2^k` cycle,

```text
Delta^N = 1 + S^N = 0.
```

At the half scale `h=N/2`, `D_h=1+S^h` maps an `N`-periodic word to an
`h`-periodic defect, and `D_h x=0` exactly when `x` already has period
dividing `h`.  Coordinatewise multiplication obeys the exact difference
rule

```text
D_h(f*g) = f*D_h(g) + g*D_h(f) + D_h(f)*D_h(g).
```

This is the appropriate filtered difference algebra for the OR gate.  OR is
not the cyclic-convolution product in the coefficient presentation of
`F_2[z]/(z^N-1)`.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/peel_lift_monoid.py
```

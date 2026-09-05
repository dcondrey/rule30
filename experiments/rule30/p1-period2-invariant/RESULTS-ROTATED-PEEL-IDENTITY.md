# Rotated inverse-cone / Peel identity

Date: 2026-09-01

Status: **A UNIFORM COMMUTING IDENTITY AND A PEEL-RANK DRIFT THEOREM ARE
PROVED.  TOGETHER WITH A FINITE-SUPPORT EDGE ARGUMENT, THEY EXCLUDE EVERY
FINITE-RANK CUT OVER AN EVENTUALLY PERIODIC HARD-CORE ENDPOINT.  APERIODIC
ENDPOINTS REMAIN.**  The period-two theorem and Prize Problem 1 remain open.

## 1. The two triangles commute after a `(1,2)` shift

Let `I(e)` be the inverse-terminal cut of a one-sided endpoint `e`, let
`sigma` delete the first symbol of a sequence, and use the zero-indexed Peel

```text
P(x)_t = phi(x_t,x_(t+1)).
```

The second-order inverse-cone recurrence gives the exact identity

```text
P(I(sigma e)) = sigma^2 I(e).                         (1)
```

Indeed, write `y_t^j=I(sigma^j e)_t`.  The already verified inverse-cone
recurrence is

```text
y_(t+2)^j = phi(y_t^(j+1),y_(t+1)^(j+1)).            (2)
```

The right side of (2) is literally `P(I(sigma^(j+1)e))_t`.  This proves (1)
cell by cell, for arbitrary four-state endpoints; the hard-core restriction
is not used.  Since `P` commutes with `sigma`, iteration gives

```text
P^j(I(sigma^j e)) = sigma^(2j) I(e)                  (3)
```

for every `j >= 0`.

This is the rotated-triangle law that the preceding review left as a
plausible target.  It is an equality between the two literal `phi` triangles,
not a visual analogy or a bounded fit.

## 2. Positive Peel rank drifts exactly under endpoint shift

For a one-sided cut `x`, define its eventual Peel rank

```text
nu(x) = min { r >= 0 : P^r(x) is eventually zero },
```

with `nu(x)=infinity` if the set is empty.  Finite temporal shifts do not
change `nu`.  If `0 < nu(x)=m < infinity`, then

```text
nu(P^j x) = m-j                 for 0 <= j <= m.      (4)
```

Put `x=I(e)` and suppose `0<nu(x)=m<infinity`.  Equation (3) and (4) imply

```text
nu(I(sigma^j e)) = m+j                              (5)
```

for every `j`: applying `P^j` to the left cut gives a temporal shift of rank
`m`, so the unpeeled cut has rank exactly `m+j`.

For positive rank, consequently:

> If `I(e)` has positive finite eventual Peel rank, then `e` is not
> eventually periodic.

If `e` had equal tails `sigma^a e=sigma^b e` for some `a<b`, their inverse
cuts would be equal, while (5) would assign the two cuts the unequal ranks
`m+a` and `m+b`.

The rank-zero case does not follow from (5), but the same commuting identity
closes it for eventually periodic hard-core endpoints.  Suppose `e` is
eventually periodic and `nu(I(e))<infinity`.  Delete a finite endpoint prefix
to obtain a purely `q`-periodic endpoint `e'`, and put `y=I(e')`.  Equation
(3) shows that `y` still has finite Peel rank.  Since `sigma^q e'=e'`, (3)
also gives

```text
P^q y = sigma^(2q) y,
P^(nq) y = sigma^(2nq) y.                            (6)
```

For large `n`, the left side of (6) is eventually zero.  Hence a temporal
shift of `y`, and therefore `y` itself, is eventually zero.  If `L` is the
last nonzero coordinate of `y`, however, the literal local table says

```text
phi(0,0)=0,        phi(s,0)=3 for s in {1,2,3}.      (7)
```

Thus `P` preserves the last nonzero coordinate `L`, while `sigma^(2q)` moves
it to `L-2q` or removes it.  Equation (6) is impossible unless `y=0^omega`.
But the first inverse-cut symbol of a hard-core endpoint is state `1` or `2`,
never zero.  This proves the uniform corollary

> If `e` is an eventually periodic hard-core endpoint, then `I(e)` has
> infinite eventual Peel rank.

The proof handles rank zero as well as positive rank.  It does not forbid an
aperiodic hard-core endpoint of finite rank; in the positive-rank branch,
such an endpoint must carry the exact growth law (5).

## 3. Sharpened collision dichotomy

The earlier output-only lemma says every reachable zero-ray cut has finite
eventual Peel rank.  Combining it with section 2, every hypothetical accepted
reachable collision has an **aperiodic** hard-core endpoint.  If its inverse
cut has positive rank `m`, the inverse cuts of successive endpoint tails have
ranks `m,m+1,m+2,...`; rank zero remains possible only over an aperiodic
endpoint.

Thus all periodic endpoint censuses and counterfamilies are now discharged
uniformly, not period by period.  The next useful theorem should rule out an
aperiodic hard-core endpoint carrying finite Peel rank.  Actual-right
restrictions should be applied as restrictions on this exact tail/rank
cocycle, not as a flat list of allowed factors.

The previously excluded endpoint `2^omega` has inverse cut `(12)^omega`,
whose Peel rank is infinite, so there is no conflict with (5).

## 4. Reverse-period locking control

There is a complementary bounded diagnostic.  Fix `p` and require a
hard-core endpoint prefix to have an inverse cut satisfying
`x_t=x_(t-p)` wherever both cells are exposed.  For a fixed old endpoint
prefix, the newest cut cell is a permutation of the new endpoint symbol;
this follows inductively because `phi(l,.)` is a permutation.  Hence the
period constraint has a unique continuation over the full four-state
alphabet.

The complete hard-core prefix trees give:

| exact cut period constraint `p` | peak prefixes | terminal decision depth |
|---:|---:|---:|
| 1 | 2 | 3 (empty) |
| 2 | 3 | 3 (only `2^omega`) |
| 4 | 8 | 7 (only `2^omega`) |
| 8 | 55 | 23 (only `2^omega`) |
| 16 | 2,584 | 31 (only `2^omega`) |

Once the sole prefix is all `2`, uniqueness and the known continuation
`2^omega` make the displayed decision infinite for that fixed `p`; it is not
just a horizon statement.  But the table is still parameter-bounded and is
not an induction over powers of two.

The required negative control survives: endpoint `(12)^omega` is hard-core
and its inverse cut has primitive period `28`.  Thus a valid all-`p` theorem
must use the power-of-two structure; “all periodic inverse cuts lock to
`2^omega`” is false.

## 5. Independent checks

`rotated_peel_identity.py` verifies:

- (1) on every arbitrary four-state endpoint through length eight;
- the new-endpoint/new-cut permutation on every prefix through length seven;
- the support-edge row (7) and preservation of every finite last-nonzero cell
  through length seven;
- the five complete reverse-period trees in section 4; and
- the primitive-period-28 negative control.

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/rotated_peel_identity.py
```

The period-two theorem and all three full Prize Problems remain open.

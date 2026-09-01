# Exact Boolean Bezout certificates for the `n=10` plateau

Date: 2026-09-01

Status: **TWO EXACT UNIT-IDEAL CERTIFICATES EXTRACTED; NO UNIFORM DEGREE OR
SUPPORT BOUND PROVED.** The terminal contradiction is already latent before
the size-six plateau begins.

## 1. The plateau variety

For `n=10`, the exact survivor counts are

```text
|V_0|,...,|V_9| = 144,72,28,11,11,6,6,6,6,0.
```

The six seeds in `V_8` are

```text
0x80, 0x81, 0x82, 0x84, 0x85, 0x8a.
```

Their vanishing ideal has the following compact Boolean basis:

```text
rho_i rho_(i+1) = 0,                         i=1,...,9,
rho_5=rho_6=rho_7=rho_9=rho_10 = 0,
rho_8 = 1,
rho_4 + rho_2 rho_4 = 0.                         (1)
```

The common Boolean zero set of (1) was enumerated independently and is
exactly the six displayed seeds. The last equation says that `rho_4=1`
requires `rho_2=1`; together with hard-core it leaves precisely six choices
for `rho_1,...,rho_4`.

Canonical reduction by (1) gives

```text
epsilon_m = q_m = 0  mod I(V_8),    m=3,5,6,7,
epsilon_8 = q_8 = 1  mod I(V_8).                    (2)
```

Thus every genuinely flat macro contributes zero on the plateau, while both
terminal failure modes are identically active at offset eight.

## 2. The contradiction is latent, not accumulated during the plateau

Evaluating the *future* terminal polynomials on the earlier varieties gives

```text
epsilon_8 = 1 on every seed in V_3,
q_8       = 1 on every seed in V_5.                  (3)
```

This changes the interpretation of the delay. The intermediate frontiers do
not gradually make `epsilon_8` contradictory. Its value is already forced by
the first three survival levels; Rule 30 does not query that polynomial until
macro offset eight. Likewise `q_8` is already forced after level five.

The plateau is therefore a **delayed-observation phenomenon**: several
intervening generators lie in the current ideal, while a future generator is
already the constant one on that same survivor class.

## 3. Exact cofactor construction

Let `g_1,...,g_s` be the historical dynamic generators and put

```text
P_i = product_(j<i) (1+g_j),
H   = 1 + product_j (1+g_j) = sum_i P_i g_i.          (4)
```

`H` is the indicator of the complement of their common zero set. If a target
`t` equals one on that zero set, then `(1+t)(1+H)=0`, hence

```text
1 = t + sum_i (1+t)P_i g_i.                          (5)
```

Equation (5) supplies explicit Boolean Bezout cofactors without a heuristic
Gröbner search. The implementation first constructs (5) in the hard-core
quotient, then lifts its remainder explicitly through every initial generator
`rho_i rho_(i+1)`. The final identities have the form

```text
1 = target
    + sum C_i * (historical dynamic generator)_i
    + sum S_j * rho_j rho_(j+1)
      mod <rho_i^2+rho_i>.                            (6)
```

The checker expands both sides of (6) to exact ANF and requires literal
equality, not merely agreement on the six plateau seeds.

## 4. Certificate profiles

For the terminal pin, `target=epsilon_8`, only these historical dynamic
generators have nonzero cofactors:

| generator | cofactor degree | ANF terms | variable support |
|---|---:|---:|---|
| `epsilon_0` | 4 | 31 | `rho_2,...,rho_10` |
| `q_0` | 4 | 21 | `rho_2,...,rho_10` |
| `epsilon_1` | 5 | 21 | `rho_2,...,rho_10` |
| `q_1` | 4 | 5 | `rho_3,rho_5,rho_6,rho_7,rho_9` |
| `epsilon_2` | 4 | 2 | `rho_3,rho_5,rho_7,rho_9` |

The dynamic cofactor degree is at most five, with 80 terms total. After the
full hard-core lift, the maximum cofactor degree is eight and the nine
hard-core cofactors contain 244 terms total.

For the terminal boundary obstruction, `target=q_8`, the nonzero dynamic
cofactors are:

| generator | cofactor degree | ANF terms | variable support |
|---|---:|---:|---|
| `epsilon_0` | 4 | 27 | `rho_2,...,rho_10` |
| `q_0` | 4 | 17 | `rho_2,...,rho_10` |
| `epsilon_1` | 4 | 18 | `rho_2,...,rho_10` |
| `q_1` | 5 | 20 | `rho_2,...,rho_10` |
| `epsilon_2` | 5 | 17 | `rho_2,...,rho_10` |
| `q_2` | 3 | 2 | `rho_4,rho_6,rho_9` |
| `epsilon_3` | 3 | 2 | `rho_4,rho_6,rho_9` |
| `q_3` | 3 | 2 | `rho_4,rho_6,rho_9` |
| `epsilon_4` | 3 | 2 | `rho_4,rho_6,rho_9` |

Here the dynamic degree is again at most five, with 107 terms total. The full
hard-core lift has maximum degree seven and 247 hard-core-cofactor terms.

The repeated last cofactor in the second certificate is

```text
rho_6 rho_9 + rho_4 rho_6 rho_9
= rho_6 rho_9 (1+rho_4),                             (7)
```

for `q_2`, `epsilon_3`, `q_3`, and `epsilon_4`. This is the cleanest finite
algebraic signature exposed by the stall.

## 5. What this does and does not establish

The maximum *dynamic* cofactor degree being five is encouraging, but one
sample cannot establish a uniform cap. More importantly, the leading
cofactors use variables across almost the entire seed, from `rho_2` through
`rho_10`. Bounded degree by itself therefore does not yield a bounded-window
or finite-state invariant; spatial support must also be controlled.

The useful structural target suggested by (3) is now:

> For every surviving length-`n` seed, prove that some future pin or no-`11`
> generator, at an offset bounded linearly in `n`, is already equal to one
> modulo an earlier ideal `J_h`.

That is a delayed-contradiction statement, not a monotone rank or cycle
statement. The moving frontier may grow forever without repeating an exact
state, so a finite-state cycle argument remains unavailable until a closed
quotient is proved.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/plateau_bezout.py \
  --json \
    experiments/rule30/p1-period2-invariant/plateau-bezout-n10.json
```

`plateau-bezout-n10.json` contains every target, generator, dynamic cofactor,
hard-core lift cofactor, ANF monomial mask, degree, term count, and variable
support. Both identities are regenerated and verified on every run. A
standalone checker that does not import the frontier implementation is:

```bash
python3 \
  experiments/rule30/p1-period2-invariant/verify_plateau_bezout.py \
  experiments/rule30/p1-period2-invariant/plateau-bezout-n10.json
```

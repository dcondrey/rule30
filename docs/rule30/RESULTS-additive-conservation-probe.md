# Additive conservation-law search for Rule 30

## Status

**NEGATIVE through density window 12.**  Rule 30 has no nontrivial local
real/rational additive conserved density in the tested windows.  The result is
an exact finite-window rank certificate, not evidence for P2 and not a claim
about unbounded or non-additive conservation laws.

This executes the previously unrun exact portion of the latent/conserved route
listed in the experiment atlas.  No learned candidate was needed: the complete
linear space is small enough to eliminate directly.

Code: `experiments/rule30/additive_conservation_probe.py` and
`test_additive_conservation_probe.py`.

## Local equation

Let a density `rho` depend on `m` consecutive cells and a current `J` on
`m+1` cells.  On every input word `x_0...x_(m+1)`, let

```text
y_i = Rule30(x_i,x_(i+1),x_(i+2)),       0 <= i < m.
```

The exact local continuity equation is

```text
rho(y_0...y_(m-1)) - rho(x_1...x_m)
  = J(x_0...x_m) - J(x_1...x_(m+1)).             (1)
```

Summing (1) over a periodic row telescopes the currents and conserves the
global density sum.  Conversely this is the standard local form being tested;
there is one equation for each of the `2^(m+2)` input words.

Constants and spatial coboundaries

```text
rho(x_0...x_(m-1)) = constant
  + q(x_0...x_(m-2)) - q(x_1...x_(m-1))
```

are trivial: their global periodic sum contains no information.  Their density
space has dimension `2^(m-1)`.

## Why a mod-two rank is an exact rational certificate

Write (1) as the integer matrix `[A B] (rho,J)=0`.  The current-only matrix
`B` is the incidence matrix of the binary de Bruijn graph on `(m+1)`-bit
vertices, so it has rank `2^(m+1)-1` and a one-dimensional kernel of constant
currents.  The dimension of the projected density solution space over any
field is

```text
2^m - rank([A B]) + rank(B).                      (2)
```

The known trivial solutions force

```text
rank_Q([A B]) <= 2^m + 2^(m+1) - 2^(m-1) - 1.    (3)
```

Reducing the integer matrix modulo two cannot increase its rank.  For Rule 30
the mod-two rank equals the right side of (3) at every tested `m`.  Hence the
rational rank is squeezed to the same value, and (2) says the rational density
space has exactly the trivial dimension `2^(m-1)`.  No floating-point or
solver inference is involved.

## Results

| `m` | equations | unknowns | rank mod 2 | maximum rank | density dimension |
|---:|---:|---:|---:|---:|---:|
| 1 | 8 | 6 | 4 | 4 | 1 |
| 2 | 16 | 12 | 9 | 9 | 2 |
| 3 | 32 | 24 | 19 | 19 | 4 |
| 4 | 64 | 48 | 39 | 39 | 8 |
| 5 | 128 | 96 | 79 | 79 | 16 |
| 6 | 256 | 192 | 159 | 159 | 32 |
| 7 | 512 | 384 | 319 | 319 | 64 |
| 8 | 1,024 | 768 | 639 | 639 | 128 |
| 9 | 2,048 | 1,536 | 1,279 | 1,279 | 256 |
| 10 | 4,096 | 3,072 | 2,559 | 2,559 | 512 |
| 11 | 8,192 | 6,144 | 5,119 | 5,119 | 1,024 |
| 12 | 16,384 | 12,288 | 10,239 | 10,239 | 2,048 |

At every row the density dimension is exactly `2^(m-1)`, the dimension of
constants plus spatial coboundaries.

Rule 184 is the positive control.  It has one additional density dimension at
every tested window, corresponding to its conserved particle number; the
`certified` flag is false.  The identity rule 204 retains all `2^m` density
functions.  These controls show that the rank test does not automatically
return the Rule 30 verdict.

## P2 consequence

There is no finite-window additive mass whose continuity equation can be
summed over the lone-seed cone to force center balance, at least through window
12.  This closes the literal additive version of the proposed conservation
route.  It does not close:

- a non-additive group/monoid-valued invariant;
- a state whose window grows with scale;
- a tilted identity specialized to the actual seed boundary; or
- the time-index Walsh/defect norm route.

The fixed Rule 30 configurations already preclude a universal local temporal
coboundary for the center spin.  This rank calculation adds the corresponding
finite-window spatial conservation obstruction.

## Reproduction

From `experiments/rule30`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  test_additive_conservation_probe.py
PYTHONDONTWRITEBYTECODE=1 python3 additive_conservation_probe.py \
  --rules 184 30 --max-window 12
```

The reported statement stops at window 12.  The visible rank pattern is not an
all-window theorem.

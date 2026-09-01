# Active-core projected interpolant probe

Date: 2026-09-01

Status: **OPEN.  AN EXACT WORD-METRIC REFORMULATION IS VERIFIED, BUT THE
REGISTERED BOUNDED CLAUSE/LOCAL-ANF PROBE DOES NOT PRODUCE A UNIFORM
INTERPOLANT.**  No mortality or period-two theorem is proved here.

## 1. Exact cut formulation

Fix a horizon `H`.  A vertical cut is a word of `H` carry states.  Feeding
one core symbol through the cut applies the exact carry action at layer zero,
passes the swapped new carry upward as the next-row symbol, and repeats.  Let

```text
R_H = cuts reachable from 0^H by at most H-2 core-prefix symbols.
```

After the prefix, the core's terminal symbol is `3`.  Later rows each append
another terminal `3`, producing a fixed triangular flush.  This terminal-cone
map is a bijection.  Let

```text
S_H = inverse terminal-cone image of
      {1,2}^H with no adjacent state 1.
```

State `1` is forced rho `1`, state `2` is forced rho `0`, and both are
exactly the pin-passing carries.  Therefore

```text
C(H-1,H) is SAT  iff  R_H intersects S_H.             (1)
```

Equivalently, the proposed diagonal mortality theorem says that the word
distance from `0^H` to `S_H` under the three distinct carry generators is at
least `H-1`.  This is an exact all-`H` reformulation, not a finite result.

The checker independently compares (1) with direct `core_step` evolution for
all 1,365 terminal-`3` words through core length six.  Every comparison
agrees.  It also verifies the forward and inverse terminal-cone maps
literally.

## 2. Finite projected sets

Within the preregistered limit, the exact set sizes are:

| `H` | `|R_H|` | `|S_H|` |
|---:|---:|---:|
| 3 | 3 | 5 |
| 4 | 7 | 8 |
| 5 | 16 | 13 |
| 6 | 36 | 21 |
| 7 | 74 | 34 |
| 8 | 149 | 55 |
| 9 | 292 | 89 |
| 10 | 577 | 144 |
| 11 | 1,139 | 233 |
| 12 | 2,234 | 377 |

The `S_H` sizes are Fibonacci because the terminal cone is bijective.  The
`R_H` sizes also reproduce the independently observed corner-peel mode
proliferation.  Every displayed intersection is empty, as already implied by
the finite diagonal CNFs; the cut calculation is useful because it exposes
what an interpolant must separate.

## 3. Algebraic separators do not stabilize locally

Over the `2H` carry bits, the minimum degree of an arbitrary Boolean ANF that
is zero on `R_H` and one on `S_H` is

```text
H:       3 4 5 6 7 8 9 10 11 12
degree:  1 2 2 3 3 3 3  3  3  3.
```

Thus cubic separators exist in every tested larger cut.  This is not yet a
schema: their support grows and the affine solution spaces have many free
coefficients.  A joint search for a translation-summed local ANF of degree at
most three, with independent left and right boundary functions, is
inconsistent for every radius one through six across `H=5,...,12`.  A second
search with periodically indexed coefficients also failed, but is not used
as a retained result.

The isolated cubic fits therefore cannot be cited as a parameterized Boolean
ideal certificate.  They remain a clue that a nonlocal triangular cubic
kernel might exist, but no recurrence for such a kernel was found.

## 4. Clause width and span grow

For each target point of `S_H`, the checker finds the minimum clause width at
most six that is valid on all of `R_H` and falsified by that target.  It does
this as an exact hitting-set SAT problem and replays every returned clause.
The distributions are:

| `H` | width distribution over `S_H` |
|---:|---|
| 5 | `2:9, 3:4` |
| 6 | `2:10, 3:6, 4:5` |
| 7 | `2:7, 3:20, 4:6, 5:1` |
| 8 | `3:6, 4:49` |
| 9 | `4:68, 5:21` |
| 10 | `4:86, 5:58` |
| 11 | `4:41, 5:190, 6:2` |
| 12 | `5:343, 6:34` |

At `H=12`, some minimum clauses span nine of the twelve carry positions.
This fires the preregistered kill condition for a fixed bounded family of
projected cut clauses: both width and geometric span are already increasing,
and no translation-stable clause vocabulary appeared.  It does **not** rule
out an indexed nonlocal clause family or a different Boolean-ideal proof.

## 5. Structural lead and remaining obligation

For a fixed finite prefix word `u`, its infinite vertical cut

```text
A_u(000...)
```

is ultimately periodic.  This is uniform: each carry generator is a finite
Mealy transducer, and finite compositions preserve ultimately periodic input.
The tempting stronger statement that the terminal cone rejects every
ultimately periodic cut is false.  The pure period-two cut

```text
121212...
```

maps to endpoint carries `2222...`, which pass every pin and force rho zero
forever.  It has not been reached by any finite core prefix; the useful new
orbit question is therefore narrower:

> Prove that the orbit of `000...` under finite positive carry-generator
> words is disjoint from the inverse terminal-cone hard-core set.

This orbit statement is equivalent to arbitrary-core mortality, but it may
admit a self-similar group/section induction even though bounded projected
clauses do not.

The period-two theorem and all three full Prize Problems remain open.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/core_interpolant_probe.py
```

The command performs the direct cross-check, constructs every `R_H,S_H`
through `H=12`, solves the ANF systems, solves every minimum-clause hitting
set through width six, and replays each returned certificate.

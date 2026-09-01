# Dynamic Boolean ideal exhaustion

Date: 2026-09-01

Status: **EXACT FINITE VARIETY TRACE THROUGH `n=12`; NO UNIFORM MORTALITY
PROOF.** Every Boolean-ideal count agrees with an independent projected SAT
model count. The ideal becomes the unit ideal well before `2n+2` in every
tested length, but the calculation remains parameterized by `n`.

## 1. Correct Boolean ideal

Use one-based seed variables `rho_1,...,rho_n`. Let `epsilon_m` be the pin
emission at post-knee macro offset `m`, and let `r_m` be the exact forced rho
ANF at that offset, so `r_m=rho_(n+m+1)` on a surviving path. The new
hard-core obstruction is

```text
q_m = r_(m-1) r_m,     r_(-1)=rho_n.
```

The full ideal after `h` post-knee macros is

```text
J_h = < rho_i^2+rho_i                     (1 <= i <= n),
        rho_i rho_(i+1)                   (1 <= i < n),
        epsilon_m, q_m                    (0 <= m < h) >.       (1)
```

The field equations in (1) are necessary. Without them, emptiness over
Boolean assignments and unit-ideal membership in the polynomial ring are not
the same statement. With them, the quotient is the finite ring of Boolean
functions on the hard-core seed domain. Consequently

```text
1 in J_h  iff  V_h is empty,                              (2)
```

where `V_h` is the set of length-`n` hard-core seeds surviving at least `h`
post-knee macros.

The implementation represents Boolean ANFs by square-free monomial masks and
reduces throughout by the initial monomial ideal
`<rho_i rho_(i+1)>`. At each macro it appends the exact `epsilon_m` and `q_m`
from the moving-frontier recurrence, evaluates their common zero set, and
retains the full ANFs for audit.

## 2. Exact variety counts

The following table stops at the first empty variety. Thus `h_*` is the
smallest horizon for which `1 in J_(h_*)`.

| `n` | `|V_0|, |V_1|, ..., |V_(h_*)|` | `h_*` | registered maximum survival |
|---:|---|---:|---:|
| 4 | `8, 1, 1, 1, 1, 0` | 5 | 4 |
| 5 | `13, 8, 8, 1, 0` | 4 | 3 |
| 6 | `21, 8, 1, 0` | 3 | 2 |
| 7 | `34, 17, 5, 0` | 3 | 2 |
| 8 | `55, 24, 11, 10, 7, 0` | 5 | 4 |
| 9 | `89, 43, 30, 14, 0` | 4 | 3 |
| 10 | `144, 72, 28, 11, 11, 6, 6, 6, 6, 0` | 9 | 8 |
| 11 | `233, 104, 43, 19, 13, 13, 13, 6, 0` | 8 | 7 |
| 12 | `377, 146, 94, 41, 26, 13, 6, 0` | 7 | 6 |

For every row, `h_* <= 2n+2`. This reproduces the earlier mortality maxima
but adds the complete survivor-variety profile at every intermediate horizon.

The profiles are not monotonically strict before zero. The sharpest example
is `n=10`:

```text
|V_3|=|V_4|=11,
|V_5|=|V_6|=|V_7|=|V_8|=6,
|V_9|=0.                                                (3)
```

Thus several consecutive generators can vanish on the current variety
without making the paths immortal. A finite nonzero plateau is not an escape
model. A seed at `V_(2n+2)` would refute only the proposed linear bound; an
infinite-tail escape requires compatible survival at every horizon or a
proved reachable cycle/closure.

## 3. Independent SAT check

For each `n=4,...,12` and every `h=0,...,2n+2`, the audit independently built
`M(n,h)` using `mortality_sat.py`. It enumerated projected models on the `n`
semantic seed variables, blocking each projection after it was counted.

All 171 projected SAT counts agree exactly with the ANF counts. This compares
two different representations:

- the dynamic Boolean ideal uses substituted ANFs in the original seed
  variables;
- the SAT formulation Tseitin-encodes every OR/XOR frontier gate with
  auxiliary variables.

The agreement also confirms the convention: `M(n,h)` is satisfiable exactly
when `V_h` is nonempty.

## 4. Exact polynomial artifact

`ideal-variety-n4-n12.json` records, for every `n`, every macro through
`2n+2`, and every generator:

- the forced-rho ANF;
- the pin-emission ANF `epsilon_m`;
- the new hard-core obstruction ANF `q_m`;
- degree, term count, exact monomial masks, one-based monomial supports, and a
  formatted polynomial;
- `|V_h|`, unit-ideal status, and the independently matched SAT count.

The artifact is intentionally exact rather than a hash or summary. Later
structure searches can inspect which new generator actually cuts a plateau
and which lies in the vanishing ideal of the current survivor set.

## 5. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/pivot_emission_audit.py \
  --variety-sweep 4 12 \
  --variety-json \
    experiments/rule30/p1-period2-invariant/ideal-variety-n4-n12.json \
  --sat-crosscheck
```

Use `--emit-polynomials` to print every ANF as it is generated. Without that
flag the exact polynomials are still written to JSON, while the terminal shows
the compact variety sequences.

## 6. Conclusion

Dynamic Boolean ideal exhaustion is now an exact and independently checked
instrument. It captures the bailout behavior missed by static rank: some new
constraints are absorbed for several steps, while later moving-frontier
constraints cut the same survivor class.

The finite traces do not expose a uniform induction in `n`. The next useful
algebraic question is narrower than another width sweep: characterize a
plateau by reducing `epsilon_h` and `q_h` modulo the vanishing ideal of `V_h`,
then identify the first later generator whose normal form is nonzero on that
class. A parameterized bound on the length of such absorption runs would be
genuine progress toward `2n+2` mortality.

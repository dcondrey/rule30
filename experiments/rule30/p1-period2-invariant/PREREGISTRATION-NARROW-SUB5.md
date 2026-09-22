# Pre-registration: fixed-constant subadditivity of the narrow deepest run, `n = 35..38`

Date: 2026-09-16, written before the run. Script: `seam_history_narrow_sub5.py`.
Origin: panel rank 2 of the 2026-09-16 RW-alpha panel (proposal "Fekete
subadditivity of the deepest run up to a constant", refuted as written because
the free-constant form has no finite kill, repaired by fixing the constant).

## Statement under test

`D_n(c) = max_W rho_c(W)` over narrow sources `W in {1,2}^n` (no `11`, no
`22222`), `rho_c` the run of `seam_history_inheritance.run` with `maxrows n+4`,
the quantity of `RESULTS-SEAM-HISTORY-GUARDS.md` sections 4 and 5. Write

```text
K(N) = D_N(c) - min_{n+m=N, n,m>=7} (D_n(c) + D_m(c)).

(SUB_5)  D_{n+m}(c) <= D_n(c) + D_m(c) + 5   for all n, m >= 7, both c.
```

Under `(SUB_5)`, `b_n = D_n + 5` is subadditive, so `D_n <= a n + 5 + max_{r<m} D_r`
with `a = (D_m + 5)/m` for any fixed `m`; with `m = 26` (`c=2`, `D_26 = 8`) that is
`D_n <= n/2 + 15 < n + 2` for all `n > 26`, which is `(RW-alpha)` on the narrow
grammar at `alpha = 1/2`, closing narrow `RW` at every `n` once `n <= 34` is
census (`c=3`: `m = 27`, `D_27 = 9`, `alpha = 14/27`). Nothing here proves the
composition law; the probe is the gate before any attempt at deriving it.

## Constant, fixed from the record before the run

From the recorded narrow table (`n = 7..15`: `RESULTS-SEAM-HISTORY-GUARDS.md`
section 4; `n = 16..34`: `seam_history_narrow_growth.log`), recomputed today:

| | running max of `K(N)`, `N = 14..34` | attained at | min split at `N = 35, 36, 37, 38` |
|---|---|---|---|
| `c=2` | 5 | `N = 17` (`D_17 = 10`, split `8+9 = 5`) | 10, 11, 11, 12 |
| `c=3` | 5 | `N = 30` (`D_30 = 13`, split `15+15 = 8`) | 12, 11, 13, 12 |

So `K = 5` is the least constant the record admits for either tail, and the
statement is tested at exactly that constant.

## Gate, before any new length is trusted

The driver recomputes `D_n(c)` for `n = 7..34`, both `c`, with the same kernel.
Every value must equal the recorded one (18 values from the guards table, 38
from the growth log), and the running maximum of `K(N)` over `N = 14..34` must
be 5 for both `c`. A gate failure means the driver does not measure the
recorded object, exit 2, nothing beyond `n = 34` is reported.

## Kill

`K(N) >= 6` at any `N in 35..38` for either `c`. In the values the record fixes:

```text
c=2:  D_35 >= 16   or  D_36 >= 17   or  D_37 >= 17   or  D_38 >= 18
c=3:  D_35 >= 18   or  D_36 >= 17   or  D_37 >= 19   or  D_38 >= 18
```

A plausible negative: `D_35(2) >= 16` is a `+2` step over `D_34 = 14`, and steps of
`+2` or more occur in the record at `16 -> 17` (`6 -> 10`) and `22 -> 23`
(`7 -> 9`). A fired kill is not answered by raising `K`: the free-constant
form `(SUB_K)` has no finite kill and is recorded as the conjecture a passing
`(SUB_5)` would license, not as the statement probed.

## Expected outputs

True: `K(N) <= 5` at `N = 35..38`, both `c`; `D_35..D_38` reported with the number
of words attaining each maximum, the level histogram `N_k` (words at run `k`),
and `alpha_5 = min_n (D_n + 5)/n`. This does not prove `(SUB_5)`; it extends the
falsifier range from `N = 34` to `38` at the fixed constant.

False: the offending `(N, c, D_N, n, m, D_n, D_m)` as the exact witness, exit 1.

Also printed, data only, no kill: `K(N)` for the wide grammar from the recorded
wide census (`uc/r1-injection/census_rate_table_n3-33.log`, `census_n34.log`,
`census_n35.log`), expected running maxima 7 at `N = 28` (`c=2`) and 4 at
`N = 21` (`c=3`) under the `n, m >= 7` definition; the panel's hand value 5 for
wide `c=3` used the excluded split `6 + 15`.

## Cost

Narrow words at length `n` grow by about 1.53x per step: 4.5 M, 6.9 M, 10.5 M,
16.1 M at `n = 35..38`. The growth log measured 48 s at `n = 34` for `c=2`, so
`n = 38` is about 4.5 min per tail and the whole extension about 20 min per
tail single-core. Each `(n, c)` is an independent enumeration, so the eight
pieces run as separate processes; the `n = 7..34` recomputation (265 s) runs
beside them. No SAT, no GPU.

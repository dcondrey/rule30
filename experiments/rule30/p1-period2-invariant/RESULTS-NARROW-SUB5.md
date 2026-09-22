# Fixed-constant subadditivity `(SUB_5)` of the narrow deepest run survives at `n = 35..38`

Date: 2026-09-16. Pre-registered in `PREREGISTRATION-NARROW-SUB5.md` before
the run. Script `seam_history_narrow_sub5.py`, record
`seam_history_narrow_sub5.json`, log `seam_history_narrow_sub5.log`.

**`[C]` The narrow deepest run, exact over every narrow source through
`n = 38` (16,182,480 words at `n = 38`), is `D_n(2) = 13, 13, 13, 13` and
`D_n(3) = 14, 13, 15, 16` at `n = 35..38`. The composition defect
`K(N) = D_N - min_{n+m=N, n,m>=7} (D_n + D_m)` is `3, 2, 2, 1` (`c=2`) and
`2, 2, 2, 4` (`c=3`) there, below the pre-registered constant 5 at every `N`,
so the kill did not fire. `(SUB_5)`, `D_{n+m} <= D_n + D_m + 5` for
`n, m >= 7`, stays a falsifier-backed statement through `N = 38`, not a proved
composition law; if it held, `alpha_5 = min_n (D_n + 5)/n = 0.474` (`c=2`,
at `n = 38`) and `0.500` (`c=3`, at `n = 36`) would be the narrow `(RW-alpha)`
constants. Nothing here touches `RW`, `(RW-alpha)`, `SEP` or `PT2`.**

## 1. What was computed

`D_n(c) = max_W rho_c(W)` over narrow sources `W in {1,2}^n` (no `11`, no
`22222`), `rho_c` the run of `seam_history_inheritance.run` with the narrow
continuation rule and `maxrows n + 4`, the kernel and quantity of
`RESULTS-SEAM-HISTORY-GUARDS.md` sections 4 and 5, computed afresh for every
`n = 7..38` and both tails, with the level histogram `N_k` (words at run `k`)
and the number of words attaining the maximum. Gate, passed before anything
beyond `n = 34` was read: all 56 values at `n = 7..34` equal the recorded ones,
and the running maximum of `K(N)` over `N = 14..34` is 5 for both tails, at
`N = 17` (`c=2`, `D_17 = 10` against `D_8 + D_9 = 5`) and `N = 30` (`c=3`,
`D_30 = 13` against `D_15 + D_15 = 8`). The kernel is the one that produced
the recorded table, so the gate is a regression check on the implementation,
not an independent census; the wide columns of the guards table were the
independently cross-checked ones.

## 2. Result

`top` is the number of narrow words attaining `D_n(c)`; `split` the
minimising `(n, m)` with `D_n + D_m`, the smallest `n` when several tie; the
kill line is `K(N) >= 6`.

| `N` | words | `c=2`: `D` | top | split | `K` | `c=3`: `D` | top | split | `K` |
|---|---|---|---|---|---|---|---|---|---|
| 34 | 2,921,225 | 14 | 11 | `8+26 = 11` | 3 | 13 | 10 | `15+19 = 10` | 3 |
| 35 | 4,481,620 | 13 | 6 | `9+26 = 10` | 3 | 14 | 5 | `8+27 = 12` | 2 |
| 36 | 6,875,512 | 13 | 58 | `9+27 = 11` | 2 | 13 | 16 | `17+19 = 11` | 2 |
| 37 | 10,548,120 | 13 | 19 | `11+26 = 11` | 2 | 15 | 23 | `13+24 = 13` | 2 |
| 38 | 16,182,480 | 13 | 45 | `9+29 = 12` | 1 | 16 | 12 | `15+23 = 12` | 4 |

The `(L1)` floor `D_n >= D_(n-1) - 2` is strict at every new scale. Upper tail
of the level histogram, `k: N_k` for `k >= 10`:

```text
c=2  n=35  10:147  11:104  12:17  13:6
     n=36  10:407  11:110  12:68  13:58
     n=37  10:544  11:190  12:96  13:19
     n=38  10:586  11:223  12:58  13:45
c=3  n=35  10:85   11:76   12:21  13:17  14:5
     n=36  10:223  11:125  12:64  13:16
     n=37  10:518  11:267  12:24  13:57  15:23
     n=38  10:773  11:282  12:138 13:45  16:12
```

For context, the wide (all `2^n` sources) maxima at the same scales are
`D_34 = 22, 20` and `D_35 = 21, 23` (`c = 2, 3`; `uc/r1-injection/census_n34.log`,
`census_n35.log`), against narrow `14, 13` and `13, 14`.

The wide `K(N)` from the recorded wide census, printed as data with no kill:
running maximum 7 at `N = 28` (`c=2`, `D_28 = 21` against `D_8 + D_20 = 14`)
and 4 at `N = 21` (`c=3`, `D_21 = 16` against `D_7 + D_14 = 12`), unchanged
through `N = 35`. The panel's hand value 5 for wide `c=3` used the split
`6 + 15`, which the `n, m >= 7` definition excludes.

## 3. Reading

The falsifier range of `(SUB_5)` moves from `N = 34` to `38` at the fixed
constant, with `K(N)` at most 4 on the new range. Two features of the new
data are not predicted by anything proved. Narrow `D_n(2)` is 13 at four
consecutive scales, the longest plateau in the table (three scales at
`n = 12..14`, two at `21..22`, `24..25`, `28..29` and `32..33` before), after
reaching 14 at `n = 34`. Narrow `c=3` runs `14, 13, 15, 16` with `K(38) = 4`, the closest
approach to the constant on the new range, and its top level is isolated: no
word has run 14 at `n = 37` while 23 reach 15, and none has run 14 or 15 at
`n = 38` while 12 reach 16.

The probe's power is smaller than its statement. Every minimising split on
the new range at `c=2` uses the dips `D_9 = 2` or `D_11 = 3` (`9+26`, `9+27`,
`11+26`, `9+29`), so where the kill can fire `(SUB_5)` reduces to
`D_N <= D_(N-9) + 7` or `D_N <= D_(N-11) + 8`, an increment bound of about
0.78 per scale that any growth slower than that satisfies whether or not a
two-scale composition law exists. At `c=3` the splits vary (`8+27`, `17+19`,
`13+24`, `15+23`) and the test is closer to a composition test, and there
`K(38) = 4`. A pass therefore constrains the growth rate of `D_n(c)` on
`n <= 38`, not the existence of the law.

What a true `(SUB_5)` would give is census arithmetic, not a mechanism:
`D_n <= alpha_5 n + 5 + max_{r<38} D_r`, so narrow `RW` at every `n` with
`alpha` about `1/2`. The composition law itself has no derivation; the halving
route (`RESULTS-HALVING-ROUTE-DISPOSITION.md`) stalled on a two-scale max law
of the same shape, and this run adds no certificate. The free-constant form
`(SUB_K)` has no finite kill and is not the statement probed.

## 4. Scope

Finite, `n <= 38`, narrow grammar, both tails, one implementation. The result
is an extension of the exact `D_n(c)` table and of the range on which a fixed
composition constant has not been exceeded. No statement about `sup_n D_n(c)`,
about the counting-line constant, or about the wide grammar beyond the
recorded census is made or changed.

## 5. Reproduction

From `experiments/rule30/p1-period2-invariant/`, one process per `(n, c)`:

```sh
uv run --no-project python seam_history_narrow_sub5.py run-range 7 34 2 s7-34_c2.json
uv run --no-project python seam_history_narrow_sub5.py run-range 7 34 3 s7-34_c3.json
uv run --no-project python seam_history_narrow_sub5.py run 38 2 s38_c2.json   # and 35..37, both c
uv run --no-project python seam_history_narrow_sub5.py report s7-34_c2.json s7-34_c3.json s3*_c*.json
```

Exit 0 on gate pass and no kill, 1 on a kill, 2 on a gate failure. The
`n = 38` pieces took 508 s and 510 s with ten pieces sharing ten cores; the
`n = 7..34` recomputation took 280 s and 277 s per tail, 83 s of it at `n = 34`. The record here is the merge of
the ten piece records; `report` reads it whole.

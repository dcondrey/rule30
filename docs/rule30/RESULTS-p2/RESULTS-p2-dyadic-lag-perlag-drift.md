# No dyadic lag drifts individually, and none above 2^20 is special

Date: 2026-09-16. **A pre-registered null. No prize problem is advanced and no
kill fired.** Four kills were registered and all four are silent.

This is the continuation named in
[RESULTS-p2-dyadic-lag-drift.md](RESULTS-p2-dyadic-lag-drift.md), not a re-run.
That run and its artifact stand unchanged.

Pre-registration:
[PREREGISTRATION-dyadic-lag-perlag-drift.md](../../experiments/rule30/PREREGISTRATION-dyadic-lag-perlag-drift.md),
written before the script existed and before any per-lag slope was computed,
with no amendments. Script
[dyadic_lag_perlag_drift.py](../../experiments/rule30/dyadic_lag_perlag_drift.py),
artifact
[dyadic-lag-perlag-drift.json](../../experiments/rule30/dyadic-lag-perlag-drift.json).

## 1. The two blind spots this closes

The previous run reported the drift of the **maximum** of
`R_N(h) = sqrt(N) * C_N(h) / (N - h)` over the dyadic family
`D = {2^a - 2^b}`, and a persistence test thresholded at `1e-3`. Both are blind
in the same way. One lag whose correlation climbs while staying under the
family's largest value contributes to neither. At `N = 2^29` the noise scale
`1/sqrt(N)` is `4.3e-05`, so a lag could rise by a factor of twenty off the
noise floor and trip nothing. The second blind spot is plainer: the lag ceiling
was `2^20`, and `D` is infinite.

So: per-lag slopes for every `h` separately, and a second tier of lags reaching
`2^23`.

## 2. Protocol

Same `wdr_billion.bin` cache, payload offset 239, used-payload sha256
`c46e9665...`, the first 29 centre bits checked against
`11011100110001011001001110101` before anything was computed. The loader, lag
enumeration, control draw and exact-integer correlation are imported from
`dyadic_lag_drift.py` rather than restated, so the two runs cannot drift apart
in their definitions.

**Tier A, per-lag drift.** The identical 211 dyadic lags `h <= 2^20` and the
identical 211 seeded controls, on the same eight rungs `N = 2^22 .. 2^29`. For
each lag separately, `s(h)` is the **Theil-Sen** slope of `log2 |R_N(h)|`
against `log2 N`. Theil-Sen rather than least squares because `|R_N(h)|` can
land arbitrarily close to zero at one rung, and one such cell dominates an OLS
fit of a log. Under square-root cancellation `s(h)` is 0; a persistent
correlation at that lag gives `s(h) = 0.5`.

**Tier B, extended range.** The 66 dyadic lags with `2^20 < h <= 2^23`,
smallest 1,572,864, largest 8,388,608, against 66 controls drawn from the same
interval with `default_rng(1)`, on the five rungs `N = 2^25 .. 2^29`, which is
where every tier-B lag keeps a span of at least `3N/4`. The cache holds
1,000,000,848 payload bits, so `2^29` is the largest prefix available and the
ladder cannot be extended upward with it.

## 3. Result

| kill | statistic | value | fires at | fired |
|---|---|---|---|---|
| K4 | dyadic slopes above the control ceiling | **1** | `>= 7` | no |
| K5 | permutation p, dyadic vs control median slope | **0.888** | `<= 0.01` | no |
| K6 | extended-range dyadic/control max ratio | **0.954** | `> 2.0` | no |
| K7 | extended lags over `1e-3` at the top three rungs | **none** | any | no |

Tier-A Theil-Sen slope distributions, dyadic against control:

| | min | q1 | median | q3 | max |
|---|---|---|---|---|---|
| dyadic (211) | -0.687 | -0.168 | **-0.007** | 0.165 | 0.867 |
| control (211) | -0.596 | -0.203 | **-0.011** | 0.150 | 0.720 |

The two distributions sit on top of each other, both centred essentially at
zero, against the 0.5 that a persistent correlation would produce. The observed
median shift is `+0.004` with permutation `p = 0.888`.

Tier B at the top rung: dyadic `max |R|` 2.378 against control 2.493, ratio
0.954; largest raw correlation `1.03e-04` at `h = 3,670,016`, well under the
`1e-3` threshold. The dyadic family is, if anything, marginally *quieter* than
generic lags of the same magnitude, which is the opposite direction from a
specialness claim and is not significant at 66 draws.

### 3.1 The one exceedance is an artifact, and it is worth naming

Exactly one dyadic lag exceeded the control slope ceiling: `h = 1,048,568`,
which is `2^20 - 2^3`, the largest tier-A lag. Under exchangeability of the two
families the expected count is 0.995, so one is precisely the null expectation.
Its `|R_N|` series across the eight rungs is

    0.001, 1.729, 0.004, 0.086, 1.202, 0.824, 0.675, 0.445

The slope of 0.867 is manufactured by the near-zero cell at the first rung; the
series **decreases** monotonically over the top four rungs. This is the low-`|R|`
artifact the pre-registration anticipated when it chose Theil-Sen, showing up
anyway because the floor cell is real rather than numerical.

### 3.2 Why the kills were registered distributionally

This is the part worth keeping. The previous run's K1 threshold was a log-log
slope of `0.25` on the **max**. Carried over to per-lag slopes it would have
been meaningless: of the ten largest tier-A slopes, **10 of 10 dyadic and 10 of
10 control** slopes exceed 0.25. A fixed cutoff there fires on both families
identically and says nothing about either. The 211 controls are the only
available null calibration, and both K4 and K5 were written against them
before the run. The calibration then landed on its predicted value.

The OLS slopes, reported alongside, show the same thing from the other side:
the control family's OLS maximum is **2.439** against a Theil-Sen maximum of
0.720, produced by the single floored control cell across the whole run. Least
squares on a log would have reported that as the headline drift.

### 3.3 Validation, kept separate

Tier-A dyadic median `|R_N|` is 0.616 to 0.694 across all eight rungs against a
half-normal median of 0.6745, flat, with no trend. This is validation of a
settled empirical fact about a generator that has passed standard batteries
since Wolfram 1985, not a finding, and it is what square-root cancellation
looks like while it is happening.

## 4. What this does and does not buy

It buys two things nothing in the archive held before. Every dyadic lag up to
`2^20` has now been checked individually rather than under a maximum, and 66
dyadic lags above `2^20` have been looked at at all.

It is **not** evidence that the hypothesis is true. The hypothesis is a
statement about `limsup` as `N -> infinity`; a finite measurement can refute it
and cannot confirm it. Nested prefixes are not independent of one another, and
all 422 tier-A lags are evaluated on one sequence, so K4 and K5 are screens for
a gross difference between the two lag families, calibrated under
exchangeability of those families. **Their p-value is not a test of the
asymptotic claim** and must not be quoted as one.

The ceiling moved from `2^20` to `2^23`; it did not go away. `D` is infinite,
the sufficient condition quantifies over all of it, and the cache cannot
support a ladder past `2^29`, so any further extension needs new trajectory
computation rather than new analysis of this cache.

Proving `liminf D_N(h)/(N-h) >= 1/2` for even one `h` in `D` remains untouched.
P1, P2, P3 and PT2 remain open.

## 5. Reproduction

```sh
uv run --with numpy python experiments/rule30/dyadic_lag_perlag_drift.py \
  --output experiments/rule30/dyadic-lag-perlag-drift.json
```

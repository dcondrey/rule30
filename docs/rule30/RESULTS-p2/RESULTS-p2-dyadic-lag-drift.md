# Dyadic-lag correlations on the centre column do not drift to 2^29

Date: 2026-09-16. **A pre-registered null. No prize problem is advanced and no
kill fired.** The dyadic-lag sufficient condition for P2 and P1 survives its
first contact with the actual centre column, which is the weakest possible
form of good news: the route is not already dead.

Pre-registration:
[PREREGISTRATION-dyadic-lag-drift.md](../../experiments/rule30/PREREGISTRATION-dyadic-lag-drift.md),
written before the script existed, with one amendment to the ladder recorded
in it and made before any correlation was computed. Script
[dyadic_lag_drift.py](../../experiments/rule30/dyadic_lag_drift.py), artifact
[dyadic-lag-drift.json](../../experiments/rule30/dyadic-lag-drift.json).

## 1. Why this measurement and not the obvious one

[RESULTS-p2-sparse-difference-correlations.md](RESULTS-p2-sparse-difference-correlations.md)
proves that if `limsup_N C_N(h)/N <= 0` for every `h` in
`D = {2^a - 2^b : a > b >= 0}`, then centre density is one half, so P2 follows,
and every eventual period is excluded, so P1 follows. `D` is
polylogarithmically sparse: only `O((log X)^2)` lags up to `X`.

Nothing in the archive had ever evaluated `C_N(h)` on the actual centre
column, at dyadic lags or any other. The obvious measurement, the *level* of
those correlations, is not the question: Rule 30's centre column was
Mathematica's original pseudorandom source and has passed standard batteries
since Wolfram 1985, so correlations at the noise scale are expected and are
**validation, not a finding**. The question a `limsup` hypothesis actually
poses is whether the normalized deviation

    R_N(h) = sqrt(N) * C_N(h) / (N - h)

**drifts** with `N`. It is `O(1)` under square-root cancellation and grows like
`sqrt(N)` under any persistent correlation.

## 2. Protocol

Eight nested prefixes `N = 2^22 .. 2^29` of the `wdr_billion.bin` cache,
payload offset 239, used-payload sha256 `c46e9665...`, the first 29 centre bits
checked against `11011100110001011001001110101` before anything was computed.
All 211 dyadic lags `h <= 2^20`, against 211 seeded non-dyadic control lags of
the same magnitude drawn once with `default_rng(0)` and reused at every rung.
`C_N(h) = (N-h) - 2*M_N(h)` is exact integer arithmetic; only the `sqrt(N)`
normalization is floating point.

## 3. Result

| `N` | ones | dyadic median \|R\| | dyadic max \|R\| | control median \|R\| | control max \|R\| |
|---:|---:|---:|---:|---:|---:|
| 4,194,304 | 0.5001690 | 0.6942 | 4.0188 | 0.7761 | 3.0295 |
| 8,388,608 | 0.5002197 | 0.6622 | 2.9062 | 0.7382 | 3.6960 |
| 16,777,216 | 0.5003055 | 0.6851 | 2.5992 | 0.6615 | 3.8446 |
| 33,554,432 | 0.5002105 | 0.6561 | 2.5616 | 0.7369 | 3.1047 |
| 67,108,864 | 0.5000599 | 0.6160 | 3.7095 | 0.7752 | 2.9068 |
| 134,217,728 | 0.5000843 | 0.6510 | 2.6261 | 0.7732 | 2.7261 |
| 268,435,456 | 0.5000189 | 0.6289 | 3.3187 | 0.7248 | 3.0686 |
| 536,870,912 | 0.5000105 | 0.6829 | 3.2182 | 0.6482 | 2.8395 |

All three pre-registered outcomes are silent:

- **(K1) Drift.** Log-log slope of `max_(h in D) |R_N(h)|` against `N` is
  **-0.0084** across eight rungs spanning a factor 128 in `N`. The kill was set
  at `+0.25`; a persistent correlation at a single dyadic lag would give `+0.5`.
- **(K2) Persistence.** No dyadic lag has `|C_N(h)/(N-h)| > 1e-3` at all three
  top rungs. None is close: the three largest at `N = 2^29` are
  `h = 24` at `1.39e-04`, `h = 32,760` at `1.32e-04`, `h = 28` at `1.07e-04`,
  and none holds its sign across the ladder.
- **(K3) Specialness.** Dyadic-to-control max ratio at the top rung is
  **1.133**, against a kill at 2. The dyadic family is not distinguishable from
  generic lags of the same size.

One calibration worth recording. The dyadic median `|R|` sits at 0.62 to 0.69
at every rung, and the median of a half-normal is 0.6745; the max over 211
draws sits at 2.6 to 4.0, and the expected max of 211 standard normals is about
2.9. The normalized correlations behave like unit-variance noise in both
families, which is what square-root cancellation looks like when it is
happening.

## 4. What this does and does not mean

It means the hypothesis of `r30-sdc-dyadic-hypothesis-suffices` is not
contradicted by half a billion centre bits, and that the dyadic family carries
no visible structure that generic lags lack. Before this run, neither was
known.

It is **not** evidence that the hypothesis is true. The hypothesis is a
statement about `limsup` as `N -> infinity`; a finite measurement can refute it
and cannot confirm it. Nested prefixes are not independent of one another, so
the eight rungs are not eight independent trials. The control is a calibration,
not a statistical rejection rule.

It does not make the remaining estimate easier.
`r30-sdc-dyadic-lag-set-sparsity` already says the sparsity of `D` weakens what
a sufficient theorem must assume without making the estimate on those lags any
easier for the Rule 30 seed, and that is still exactly the position. Proving
`liminf D_N(h)/(N-h) >= 1/2` for even one `h` in `D` remains open, and no
finite computation will supply it.

P1, P2, P3 and PT2 remain open.

## 5. Reproduction

```sh
uv run --with numpy python experiments/rule30/dyadic_lag_drift.py --output experiments/rule30/dyadic-lag-drift.json
```

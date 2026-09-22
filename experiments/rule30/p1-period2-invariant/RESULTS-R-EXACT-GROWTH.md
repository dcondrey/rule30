# Growth of the exact actual-right language `|R_m|` through `m = 49`: neither a pure exponential nor a pure polynomial, and the two surviving forms cannot be separated by this instrument

Date: 2026-09-16. Scripts `uc/r1-hardcore/r_exact_sat.py` (resumed from the
length-30 record with per-length checkpoints and six worker processes; the
resumed run reproduces the counts of `r_exact_sat_m1-50.log` at `m = 31..41`
exactly) and `uc/r1-hardcore/r_exact_growth.py` (the fits below). Records
`uc/r1-hardcore/r_exact_language_m48.json` (1,612 minimal forbidden factors
through 48, the record `r_exact_joint.py` uses) and
`uc/r1-hardcore/r_exact_language_m60.json` (the continuation past 48,
rewritten after every length; 49 at the time of writing, target 60). Logs
`r_exact_sat_m31-48.log`, `r_exact_sat_m49-60.log`. No pre-registration
preceded the fits of section 3; the out-of-sample test there and the
predictions of section 4, written before the counts they predict exist, are
the non-circular part.

**`[C]` `|R_m|` is `156, 721, 3,908, 13,730, 36,193` at `m = 13, 20, 30, 40,
49`. The growth ratio falls from 1.311 at `m = 13` to 1.108 at `m = 49`, with
single-step upticks only at `m = 21, 25, 36` (local entropy `h_m = log2` of
the ratio, 0.391 to 0.148 bits per
symbol) while the local polynomial exponent `a_m = m ln(ratio)` rises from
3.5 to 5.0, with its slope doubling from 0.027 per length on `m = 30..41` to
0.047 on `m = 41..49`. Fitted on `m = 20..41` and tested on `42..49`, a pure
exponential over-predicts by 0.42 in `ln` at `m = 49` and a pure polynomial
under-predicts by 0.12; a polynomial times an exponential of entropy 0.03
bits and a stretched exponential `exp(k m^0.145)` of zero entropy both
under-predict, by 0.038 and 0.048. Refitted on `20..49` they give entropy
0.040 bits and exponent 0.200 with residuals 0.007 and 0.008, and their
predictions differ by 2.7 percent at `m = 60`, less than their demonstrated
extrapolation error, so the run to 60 cannot decide between a small positive
entropy and zero entropy; separating them needs `m` near 100, where this
method costs about `10^6` s per length. New minimal forbidden factors appear
at every length from 9 to 49, 146 of them at `m = 49` and 1,758 in all, so `R`
is not of finite type on any range seen. Whether `|R_m|` is subexponential is
therefore still open, and it is open in a specific way: the data exclude the
two simple answers and leave a zero-entropy and a `0.04`-bit answer that
agree to within the noise of the instrument.**

## 1. What was computed

`R_m` is the set of length-`m` words `rho_0 .. rho_(m-1)`, `rho_k = s(2k, 1)`,
realizable by some right half-line of `2m - 1` free cells under Rule 30 with
the centre column driven to `0101...` (`RESULTS-REALIZABLE-RUN.md` section
1). `r_exact_sat.py` extends `R_(m-1)` to `R_m` by one CaDiCaL query per
candidate `w b` not already excluded by a known forbidden suffix, on the
complete light cone of `2m - 1` cells and `2m - 2` steps, and records every
new minimal forbidden factor. The length-30 record was produced with the
script's seed-enumeration gate through `m = 10` and the recorded counts
through 13; the resumed runs start from that record and their counts at
`m = 31..41` equal those of the earlier single-process run to 41 line by
line, including the factor lists. Times per length on six cores: 2 s at
`m = 31`, 23 s at 41, 120 s at 48, 224 s at 49, rising by 1.2 to 1.9 per
length at the end; the earlier single-process run took 320 s at `m = 41`.

`r_exact_growth.py` prints the per-length table and fits four forms to
`ln |R_m|` on a window by least squares (`STRETCH` by a grid over `beta`):

| form | `ln |R_m| =` | entropy |
|---|---|---|
| `EXP` | `c + h m` | `h / ln 2` |
| `POLY` | `c + a ln m` | 0 |
| `POLYEXP` | `c + a ln m + h m` | `h / ln 2` |
| `STRETCH` | `c + k m^beta` | 0 for `beta < 1` |

## 2. Counts

| `m` | `|R_m|` | ratio | `h_m` (bits) | `a_m` | new forbidden factors |
|---|---|---|---|---|---|
| 13 | 156 | 1.311 | 0.391 | 3.52 | 2 |
| 16 | 316 | 1.259 | 0.332 | 3.69 | 2 |
| 20 | 721 | 1.210 | 0.275 | 3.81 | 8 |
| 25 | 1,780 | 1.192 | 0.254 | 4.40 | 9 |
| 30 | 3,908 | 1.157 | 0.210 | 4.37 | 35 |
| 35 | 7,541 | 1.132 | 0.178 | 4.33 | 57 |
| 40 | 13,730 | 1.123 | 0.167 | 4.62 | 71 |
| 41 | 15,384 | 1.120 | 0.164 | 4.66 | 84 |
| 42 | 17,196 | 1.118 | 0.161 | 4.68 | 71 |
| 43 | 19,197 | 1.116 | 0.159 | 4.73 | 95 |
| 44 | 21,389 | 1.114 | 0.156 | 4.76 | 109 |
| 45 | 23,809 | 1.113 | 0.155 | 4.82 | 110 |
| 46 | 26,482 | 1.112 | 0.153 | 4.89 | 112 |
| 47 | 29,422 | 1.111 | 0.152 | 4.95 | 128 |
| 48 | 32,656 | 1.110 | 0.151 | 5.01 | 132 |
| 49 | 36,193 | 1.108 | 0.148 | 5.04 | 146 |

Every length from 9 to 49 adds minimal forbidden factors, 1,758 in all
through 49 (237 through 30). The ratio is non-increasing from `m = 26` on
except `35 -> 36` (1.1316 to 1.1317); its earlier upticks are `20 -> 21` and
`24 -> 25`.

## 3. Fits

Out of sample, fitted on `m = 20..41`, error `ln(actual / predicted)`:

| form | parameters on `20..41` | rms | error at 42 | at 45 | at 49 |
|---|---|---|---|---|---|
| `EXP` | `h = 0.208` bits | 0.076 | -0.159 | -0.266 | -0.424 |
| `POLY` | `a = 4.28` | 0.014 | +0.035 | +0.066 | +0.120 |
| `POLYEXP` | `a = 3.65`, `h = 0.031` bits | 0.006 | +0.005 | +0.015 | +0.038 |
| `STRETCH` | `k = 18.1`, `beta = 0.145` | 0.006 | +0.007 | +0.020 | +0.048 |

In sample on `m = 20..49`: `EXP` `h = 0.191` bits, rms 0.108; `POLY`
`a = 4.37`, rms 0.029; `POLYEXP` `a = 3.47`, `h = 0.040` bits, rms 0.0067;
`STRETCH` `k = 10.9`, `beta = 0.200`, rms 0.0076. The local diagnostics on
the same window: `ln(ratio) = 0.0322 + 3.372 / m` (the `POLYEXP` reading,
entropy 0.046 bits, rms 0.004) and `ln a_m = 0.679 + 0.233 ln m` (the
`STRETCH` reading, rms 0.025). The `POLYEXP` entropy moved from 0.031 to
0.040 bits and the `STRETCH` exponent from 0.145 to 0.200 when eight lengths
were added, so neither parameter has converged, and both flexible forms
under-predict by growing amounts: the true `a_m` rises faster than either
fit, 0.047 per length over `41..49` against 0.027 (`POLYEXP`, constant) and
0.021 (`STRETCH`, declining).

## 4. Predictions for the continuing run, written before the counts exist

Fitted on `m = 20..49`:

| `m` | `POLY` | `POLYEXP` | `STRETCH` | `EXP` |
|---|---|---|---|---|
| 50 | 37,070 | 39,466 | 39,249 | 49,163 |
| 52 | 44,001 | 47,778 | 47,367 | 64,050 |
| 55 | 56,223 | 63,038 | 62,138 | 95,246 |
| 58 | 70,912 | 82,316 | 80,575 | 141,635 |
| 60 | 82,236 | 97,828 | 95,249 | 184,524 |

The offset-free test is the increment of the local exponent, which the
counts give exactly: under `POLYEXP`, `a_60 - a_49 = 11 h = 0.30`; under
`STRETCH`, `a_49 ((60/49)^0.2 - 1) = 0.21`; if the slope of `41..49`
continues, 0.52, and then `|R_60|` is about 105,000. What the run to 60 can
and cannot decide:

- `POLY` is refuted if `ln(actual / POLY)` at `m = 60` exceeds 0.10 (it is
  already +0.12 at 49 out of sample); `EXP` is refuted if the ratio at 60 is
  below 1.12 (it is 1.108 at 49). Both are expected to fire; neither is news.
- `POLYEXP` and `STRETCH` differ by `ln(97,828 / 95,249) = 0.027` in the
  count at 60, below the 0.038 to 0.048 error either made over eight lengths,
  and by 0.09 in `a_60 - a_49`, against step-to-step fluctuations of `a_m` of
  0.01 to 0.07 on `41..49`. Neither difference is decisive.
- An increment `a_60 - a_49` of 0.45 or more says the local exponent is
  still accelerating and the entropy estimate still rising; 0.2 or less says
  the acceleration has stopped and favours the zero-entropy form; between
  0.2 and 0.35 decides nothing.

At `m = 100` the two forms differ by 0.24 in `ln` (1.74 M against 1.37 M),
which would decide; the per-length cost there is about `10^6` s by this
method (about 1.5 M queries on a cone of 199 cells), so the question is not
reachable by extending `r_exact_sat.py`.

Returns so far, written after the predictions above and before the run
reached 60 (`r_exact_sat_m49-60.log`):

| `m` | `|R_m|` | ratio | `a_m` | `ln(actual / POLYEXP)` | `ln(actual / STRETCH)` | `ln(actual / POLY)` |
|---|---|---|---|---|---|---|
| 50 | 40,047 | 1.1065 | 5.06 | +0.015 | +0.020 | +0.077 |
| 51 | 44,280 | 1.1057 | 5.12 | +0.019 | +0.026 | +0.091 |
| 52 | 48,878 | 1.1038 | 5.14 | +0.023 | +0.031 | +0.105 |
| 53 | 53,894 | 1.1026 | 5.18 | +0.027 | +0.037 | +0.119 |
| 54 | 59,333 | 1.1009 | 5.19 | +0.031 | +0.043 | +0.134 |
| 55 | 65,240 | 1.0996 | 5.22 | +0.034 | +0.049 | +0.149 |
| 56 | 71,672 | 1.0986 | 5.26 | +0.038 | +0.055 | +0.164 |

`a_56 - a_49 = 0.22` over seven lengths, 0.032 per length: above `POLYEXP`'s
0.0275 and `STRETCH`'s 0.02, below the 0.047 of `41..49`. `POLY` is already
past its kill (0.164 at 56 against 0.10 at 60). The `POLYEXP` and `STRETCH`
errors grow by about 0.004 and 0.006 per length; at that rate the count at 60
lands near +0.055 and +0.08 above them, and the increment `a_60 - a_49` near
0.34, at the upper edge of the band the criterion above calls undecided.

Verdict at `m = 60` (run complete; `r_exact_growth_fit20-49_test50-60.log`):
`|R_59| = 94,361`, `|R_60| = 103,220`, ratio 1.094. Errors at 60:
`POLYEXP` +0.054, `STRETCH` +0.080, `POLY` +0.227. `POLY` and `EXP` are
refuted as pre-registered. `a_60 - a_49 = 0.345`, inside the band 0.2 to
0.35 that the criterion above declared undecided, at its upper edge and
above both surviving forms' predictions (0.30 and 0.21). The counts keep
running slightly ahead of both fits, so the entropy of `R`, if positive, is
at least the `POLYEXP` estimate of 0.04 bits; the question stays open and,
by section 4, is not decidable by extending this run.

## 5. Reading

What is excluded on `m <= 49`: a fixed exponential rate (the ratio has
fallen at every length but two since `m = 22`) and a fixed polynomial
exponent (the local exponent has risen from 3.5 to 5.0). What is not:
`|R_m| ~ m^3.5 2^(0.04 m)` and `|R_m| ~ exp(11 m^0.2)`, which agree to
within the instrument's error over any range it can reach. The entropy of
`R`, if positive, is at most about 0.15 bits per symbol (the local value at
49) and on the surviving fit about 0.04.

Consequence for the realizable joint run (`RESULTS-REALIZABLE-RUN.md`
section 7): its independence null is `log2 |R_n| / (2 - h_n)`, 4.5 to 7.6 on
`n = 13..41`, and the exact joint maximum lies within 2.3 below and 0.4 above
it. The null grows as `log2 |R_n|` does: under `POLYEXP` about
`(3.5 log2 n + 0.04 n) / 2`, linear in the end with slope about 0.02, and
under `STRETCH` sublinear; the census cannot tell which, and neither is a
proof of `RW` on `R`. The forbidden-factor counts say the obstacle is structural: `R`
is not of finite type on any range seen, so a finite-state description of it
is not available for a transfer-matrix count, and the growth question needs
either a different exact method (a description of `R` that is not a factor
list) or an argument about Rule 30's right light cone under the driven
boundary. Nothing here touches `RW`, `(RW-alpha)`, `SEP` or `PT2`.

## 6. Scope

Finite, `m <= 49` exact; fits are least squares on `ln |R_m|` with 22 to 30
points and no error model beyond the out-of-sample test; the four forms are
the four simplest, not a complete family. The continuing run rewrites
`r_exact_language_m60.json` after each length and can be resumed from it;
compare its counts with section 4 before reading anything into them.

## 7. Reproduction

From `experiments/rule30/p1-period2-invariant/uc/r1-hardcore/`:

```sh
uv run --no-project --with python-sat python r_exact_sat.py --resume r_exact_language.json --max-length 48 --workers 6 --out r_exact_language_m48.json
uv run --no-project --with python-sat python r_exact_sat.py --resume r_exact_language_m48.json --max-length 60 --workers 6 --out r_exact_language_m60.json
uv run --no-project --with numpy python r_exact_growth.py r_exact_language_m60.json --min-m 20 --max-m 41 --predict 8
uv run --no-project --with numpy python r_exact_growth.py r_exact_language_m60.json --min-m 20 --max-m 49 --predict 11
```

About 10 minutes for the first on six cores; the second is running.

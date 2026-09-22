# The seed's quarter-wave loss census to t=65536: the one-quarter violation stays alone

Status: **the `delta >= 1/4` kill does not become recurring.** No ladder
statement changed; `P_t = o(t)` is untouched and still conjectured.

## 1. What was open

`RESULTS-seed-loss-certificate-search.md:54-59` disproves the proposed uniform
loss `delta >= 1/4` for every seed row and every dyadic scale
`4 <= L <= sqrt(t)`, on the strength of a single exception at `t = 20`,
`delta = 17/84`. Its own scope leaves the interesting case alive: *"It does not
disprove an eventual version, a smaller constant, or an accumulated-loss
inequality allowing exceptions."* One exception at small `t` is consistent with
an eventual bound. A second, far from the first, would not be, and any
`delta < 1/8` would kill that document's own worked `eta = 1/8` example
(exponent `1 + (1/4)log2(7/8) ~ 0.95184`), the only quantitative payoff
attached to this route.

The published census stops at `t = 8192` because
`quarter_wave_seed_loss_scan.py` caps its CLI there as a declared audit scope.
`scan()` itself is horizon-parametric, so the engine did not need changing.

## 2. Result, `16 <= t <= 65536`

371,383 row-scale cases, 253 s single-process.

| `L` | argmin `t` | minimum relative loss | float |
|---|---|---|---|
| 4 | 20 | `17/84` | 0.202381 |
| 8 | 77 | `87/241` | 0.360996 |
| 16 | 390 | `750/1951` | 0.384418 |
| 32 | 1155 | `17469/46664` | 0.374357 |
| 64 | 5259 | `33619/84280` | 0.398897 |
| 128 | 20858 | `1277803/3130268` | 0.408209 |
| 256 | 65536 | `8478921/15982336` | 0.530518 |

- **Violations of `delta >= 1/4`: exactly one, still `t = 20`, `L = 4`.** The
  census now reaches 3200 times further in `t` than the exception and finds no
  second one.
- **Violations below `1/8`: none.** The `eta = 1/8` worked example is not
  threatened in this range.
- The five published per-scale minima reappear unchanged as a prefix, at the
  same argmin times, and the `t = 20` scalar witness assert fires on every run.
  That is the control: the same function over the published horizon returns the
  published table, so the two new rows come from the engine that produced them.

## 3. Reading it honestly

This is the outcome with the lower payoff, and it was the likelier one. The
`T = 131072` dyadic ladder in `quarter-wave-variance-loss.json` already sat at
`delta_L ~ 0.49-0.51` across every mesoscopic `L`, so a clean run adds little
and only a violation would have been informative. What it buys is that the
`t = 20` exception is now isolated over three orders of magnitude rather than
one, which is the evidence an eventual-version claim would rest on, and that
the two new scales `L = 128` and `L = 256` clear `1/4` comfortably.

It buys nothing toward the milestone, and cannot:
`RESULTS-quarter-wave-coherence-barrier.md:62-67` proves the loss floor summed
over dyadic `L` up to `L_J = o(t)` is `O((L_J/t)^2) -> 0`, so positivity of
loss is not the missing certificate, and
`RESULTS-quarter-wave-origin-obstruction.md:137-142` shows any coefficient
below `1/4` needs a constant depending on the entire initial row. The
certificate has to be seed-specific before its first inequality.

## 4. Scope

Every integer `16 <= t <= 65536` and every dyadic `L` with
`4 <= L <= floor(sqrt(t))`. Finite census. It proves no all-time seed loss
bound and refutes none, and nothing here extrapolates past `t = 65536`.

## 5. Files

`extend_seed_loss_census.py` (`extend_seed_loss_census.log`). It imports
`scan()` from `experiments/rule30/quarter_wave_seed_loss_scan.py` unchanged and
writes no tracked artifact. Logs are hidden by the global ignore; `git add -f`
to commit them.

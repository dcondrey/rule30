# Demand-orbit transient: the fibre transient outruns the scale, both pre-registered kills fire

Date: 2026-09-16. Pre-registered in `PREREGISTRATION-DEMAND-TRANSIENT.md`
before the run. Script `demand_transient.py`, record `demand_transient.json`,
log `demand_transient.log`.

**`[C]` Over the `2^n` reachable fibres `F_{n-1}(W)`, the maximum pre-period
`max_W tau(W, c)` of the pinned-cut recursion `G_c` is at least `n + 9` at
every `n = 10..22` and both tails, `n + 9` or `n + 10` at `n = 10..15`, and
between `2n` and `2n + 2` at `n = 20..22` (the median at `n = 18` is 24 and
22; 11 to 31 percent of sources at each `(n, c)` have `tau <= n`);
its least-squares slope over the pre-registered range `n = 10..18` is 1.65
(`c = 2`) and 1.62 (`c = 3`) against the kill line 0.9 (2.26 and 2.25 over
`n = 10..22`, with `max tau - n` never decreasing at `c = 2`), so `(K2)` fires
and no bound `tau <= beta n + C` with `beta < 1` fits the maxima on this
range. The same maxima and the same periods hold on a uniform sample of all
`4^n` fibres (section 7, 32,768 per cell), so the transient is a property of
`G_c` itself, not of reachability. `(K1)` fires by its slope arm (0.62 and
0.43 against 0.3 on `n = 10..18`; 0.36 and 0.32 on `n = 10..22`) on a quantity
that never exceeds 6 and is 3 and 2 at `n = 22`: no word at any `(n, c)` has
`rho > tau + pi`, the excess `max_W (rho - tau)` is at most `pi - 2` in every
cell, and it is bounded while `pi` stays 8, which it has since `n = 15` after
one step from 4.
Every deepest word has `rho <= tau`: the extremal runs end inside the
transient. The maximum transient is attained by a narrow source at every
`(n, c)`, so restricting the grammar does not rescue `(TAU)`. The
decomposition "run = transient + periodic tracking" bounds
nothing, because its first term alone exceeds the scale. Nothing here touches
`RW`, `(RW-alpha)`, `SEP` or `PT2`.**

## 1. What was computed

`G_c` is the fibre recursion with the cut pinned at `c`: from
`T[u][k+1] = CONE[T[u-1][k]][T[u][k]]` (`psi_kernel.Endpoint.peek`), invert
each `CONE` row in its second argument and run `k = n-1` down to `0` with
`T[u][n] = c`. It reads no endpoint symbol, so from `F_{n-1}(W)`, the
anti-diagonal below the cut after `W`, the orbit is autonomous on a finite set
and has a pre-period `tau(W, c)` and a period `pi(W, c)`. The run
`rho(W, c)` is `seam_history_inheritance.run` over the wide grammar with
`maxrows n + 4`, the kernel behind the recorded `D_n(c)`; `rho` is the length
of the longest prefix of the dictated 4-state continuation `e*_u` that stays
in `{1, 2}` with no `11`.

Gates, all passed before any table: for `n = 3..8`, every `W` and both `c`,
feeding `e*_u` through `Endpoint.append` reproduces `G_c` step by step for
`3n + 8` steps and `rho` equals the dictated hard-core prefix (1008 pairs);
`max_W rho` equals the recorded wide `D_n(c)` at every `n = 10..20` in the run
(`n = 7..9` are not in the census; section 7 verified them separately); every
period is a multiple of 4. Sources are all `2^n` words of `{1,2}^n`, `n = 10..22`; orbits are walked
once per fibre and memoised across walks (the record's `distinct_fibres`
counts every fibre any walk visited, not the distinct source fibres).

## 2. Result

`tau` is the maximum pre-period over all `W`, `pi` the period, which takes one
value over all `2^n` sources at each `(n, c)`: 4 at `n <= 13` and at `(14, 2)`,
8 at `(14, 3)` and every `n = 15..22`. `xs` is `max_W (rho - tau)`, `>` the
number of words with `rho > tau`. No word at any `(n, c)` has `rho > tau + pi`.
Rows `n = 10..18` are the pre-registered range; `n = 19..22` are supplementary.

| `n` | `c=2`: `D` | `tau` | `tau - n` | `xs` | `>` | `c=3`: `D` | `tau` | `tau - n` | `xs` | `>` | `pi` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 5 | 20 | 10 | 1 | 4 | 7 | 19 | 9 | 0 | 0 | 4 |
| 11 | 6 | 21 | 10 | 0 | 0 | 7 | 20 | 9 | 0 | 0 | 4 |
| 12 | 9 | 22 | 10 | 1 | 4 | 8 | 22 | 10 | 2 | 2 | 4 |
| 13 | 7 | 23 | 10 | 0 | 0 | 9 | 23 | 10 | 0 | 0 | 4 |
| 14 | 10 | 24 | 10 | 2 | 13 | 8 | 23 | 9 | 1 | 10 | 4, 8 |
| 15 | 9 | 25 | 10 | 1 | 4 | 8 | 25 | 10 | 0 | 0 | 8 |
| 16 | 10 | 27 | 11 | 3 | 58 | 10 | 26 | 10 | 3 | 6 | 8 |
| 17 | 11 | 30 | 13 | 4 | 65 | 10 | 29 | 12 | 4 | 35 | 8 |
| 18 | 12 | 35 | 17 | 6 | 123 | 11 | 34 | 16 | 3 | 34 | 8 |
| 19 | 11 | 36 | 17 | 5 | 104 | 13 | 37 | 18 | 2 | 74 | 8 |
| 20 | 11 | 42 | 22 | 4 | 92 | 14 | 41 | 21 | 5 | 8 | 8 |
| 21 | 13 | 43 | 22 | 3 | 114 | 16 | 42 | 21 | 4 | 28 | 8 |
| 22 | 12 | 46 | 24 | 3 | 80 | 14 | 45 | 23 | 2 | 36 | 8 |

Pre-registered kills over `n = 10..18`:

| | `max (rho - tau)` at 18 (`K1` at `> 6`) | slope of `max (rho - tau)` (`K1` at `>= 0.3`) | slope of `max tau` (`K2` at `>= 0.9`) |
|---|---|---|---|
| `c=2` | 6 | +0.62 | +1.65 |
| `c=3` | 3 | +0.43 | +1.62 |

Both fire for both tails. The transient is not a tail phenomenon of a few
words: at `n = 18` the median `tau` is 24 (`c=2`) and 22 (`c=3`), the 90th
percentile 33 and 32, so even the typical reachable fibre has a transient
above the scale. The first word in enumeration order attaining `max tau`
is an all-ones source with a short tail (`1^(n-3) 212` for `c=2` at
`n = 16..18`), but the maximum is not specific to such sources: section 5 shows
a narrow source attains it at every `(n, c)`. The record carries the first
argmax at every `n` in each grammar.

Every deepest word has `rho <= tau` (the record stores all of them except 50
of the 60 at `(22, 2)`; section 7 covers the other ten, margins 2 to 33). The
margin `tau - rho` on the deepest words is at least 2 everywhere except three
words at `(15, 3)`, `122121121222121`, `212121121222121` and
`222121121222121`, with `rho = tau = 8`, where the run dies on the first
symbol of the periodic regime; at `n = 18` the sixteen deepest `c=2` words have
`(rho, tau) = (12, 15)` and the twelve deepest `c=3` words `(11, 18)`.

## 3. Reading

`(TAU)` is dead on the reachable set in the only form that would give
`(RW-alpha)`: the transient of the autonomous recursion, maximised over the
fibres a binary source can reach, is above the scale from `n = 10` and about
twice the scale by `n = 20`, so no line of slope below 1 fits the maxima on
this range, and the bound `D_n(c) <= beta n + C + K` it was meant to feed is weaker
than `D_n(c) <= n + 4`, which the driver's `maxrows` already enforces. The
one-seed transient of `RESULTS-PT2-PANEL-2026-09-15.md` section 5
(`K_d = 17..26` at `d = 9..39`) is the small end of the reachable range, not
its ceiling.

`rho <= tau + pi` is observed on all 8.4 M sources, with `max (rho - tau - pi)`
at most -2 in every cell. It is not forced by the fibre's periodicity: the
dictated symbol `e*_u` depends on the endpoint column and not on the fibre
alone, and it is not periodic with the fibre (section 7: at `n = 3..12`, both
tails, every source shows the same fibre dictating different symbols after
`tau`, and no source has a dictated sequence of period at most 64 over 320
steps). The panel's "tautological half" is therefore withdrawn as an argument;
the observation stands, holds with `K = 8`, and carries nothing because
`max tau + 8 > n + 4`. `(K1)` fired by the letter of its slope arm on the
integers `1, 0, 1, 0, 2, 1, 3, 4, 6`; the supplementary rows (`5, 4, 3, 3` at
`c=2`, `2, 5, 4, 2` at `c=3`) bound the margin at 6 in range and the cap
`max (rho - tau) <= pi - 2` holds cell by cell, but the full-range slope (0.36
and 0.32 over `n = 10..22`) is still above the line and the cap stepped from
2 to 6 when `pi` stepped from 4 to 8 at `n = 14, 15`. The reading "a growing
margin" is bounded while `pi` stays 8, not refuted. The pre-registered kill
is reported as fired and its interpretation as qualified.

What the census adds beyond the kills: the deepest runs die inside the
transient at every `(n, c)`, so the lens reading that an extremal continuation
sits in a periodic orbit until a phase slip is dead in this form; the period of
the pinned-cut recursion is a function of `(n, c)` alone on this range, not of
the source (and the same single value on a uniform sample of all `4^n`
fibres); and the maximal transient is attained inside the narrow grammar
(section 5), so the `PT2`-relevant restriction to hard-core or narrow sources
changes nothing.

## 4. Scope

Finite, `n <= 22`, all wide sources, both tails; two implementations, the
script (gated against `Endpoint.peek` at `n <= 8` and against the recorded
`D_n(c)` at `n = 10..20`) and the independent census of section 7, which
reproduces every table cell. The kill is a finite-range statement about slopes; it excludes no
`beta < 1` asymptotically, it shows that no such bound is visible on the
reachable fibres through `n = 22` and that the measured transient is about
`2n`. `rho <= tau + pi` is observed, not proved here. `RW`, `(RW-alpha)`, `SEP`
and `PT2` are untouched.

## 5. Post-hoc stratification by source grammar

Added after the pre-registered readout; not part of the kill. `max tau` over
the hard-core sources (no `11`, `F(n+2)` words) and over the narrow sources
(no `11`, no `22222`) equals the wide maximum at every `(n, c)`, `n = 10..22`:
the longest transient is always attained by a narrow source. First narrow
argmax at `n = 18`: `121212121221222121` (`c=2`, `tau = 35`) and
`121212121212121222` (`c=3`, `tau = 34`); at `n = 22`:
`1212121212121212222121` (`c=2`, 46) and `1212121212121222122122` (`c=3`, 45).
The record carries, under `by_grammar`, the word counts, the first argmax and
the maximum wide-continuation run per grammar (the latter is not the narrow
`D_n(c)`, whose continuation also avoids `22222`). A restatement of `(TAU)`
on the narrow grammar, the language `PT2` needs, therefore has the same
maxima and the same slope and is dead on the same range.

## 6. Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --no-project python demand_transient.py run 10 18 demand_transient.json
uv run --no-project python demand_transient.py report demand_transient.json
```

Exit 1 on the kill, 2 on a gate failure. The record's census timings sum to
13 s for `n = 10..18`, 96 s for `n = 19..21` and 115 s for `n = 22`, single
core, gate excluded; `n = 19..21` and `n = 22` were run as separate processes
(`run 19 21 ... --no-gate`, `run 22 22 ... --no-gate`) and merged into the one
record, which the report reads whole.

## 7. Independent check

`crosscheck/demand-transient/check_dt.py` (with `probe_estar.py` and
`report.py`; logs and records alongside) re-implements the endpoint build,
`G_c`, the dictated symbol, `tau`, `pi` and `rho` from the two recurrences of
`psi_kernel.py` alone, gates them at `n = 3..11` against `Endpoint.peek` and
at `n = 7..20` against the recorded `D_n(c)`, and runs the full census of all
`2^n` sources at every `n = 10..22`. Every number in sections 2 and 5 and
every field of the record reproduce. Beyond the document: the maxima and the
periods are the same on 32,768 uniformly random 4-state fibres per cell; the
family `1^(n-t) v` with `|v| <= 7` keeps `max tau` within `2n +- 6` through
`n = 40`; and the dictated symbol is not periodic with the fibre
(`estar_oracle_example.log`), which removed the tautology argument from
section 3.

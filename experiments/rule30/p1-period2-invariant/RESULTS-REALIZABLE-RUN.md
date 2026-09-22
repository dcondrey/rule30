# The constant-cut run on the realizable language: 3 to 6 through `n = 30`, at most 10 through `n = 46`, against a need of `n + 2`

Date: 2026-09-16. Scripts `extremal_realizability.py` (new; record
`extremal_realizability.json`, log `extremal_realizability.log`) and the
`uc/r1-hardcore/` lens of 2026-09-03 (`hf_lang_survival.py`,
`r_exact_sat.py`, logs only, no results document until this one). No
pre-registration file: the expected outcomes of the new test were stated in
the session before it ran (realizable extremal words would remove the lever;
unrealizable ones would keep it), and the lens numbers are read from its logs.

**`[C]` Of the 856 stored deepest-run sources (the `deep` lists of
`demand_transient.json`, wide `n = 10..22`, 312 words, and the `top` lists of
`seam_history_narrow_sub5.json`, narrow `n = 10..38`, 544 words; the lists are
capped, 856 of 980 maximisers), 811 are not actual right traces already
inside `W`: the first proved or SAT-audited forbidden factor is `11` in 274,
`101001` in 204, `0100101` in 96, and one of 27 other factors in the rest.
The 45 that are realizable, all narrow (a grammar fact: 310 of the 312 wide
words contain `11`, which the narrow grammar excludes at the source), none
deeper than `rho = 13`, have forced continuations that stay in the realizable
language for at most 5 forced steps. The exact census (section 7) gives the same picture
uniformly: with both the source and its forced continuation confined to the
exact actual-right language `R`, the constant-cut run is 3 to 7 at every
`n = 13..41` (7 at `(32, 2)` and `(40, 3)` only; 6 at `n = 41` for both tails,
where the `R13` superset census had given 9), against the `RW` need `n + 2`;
the superset census reaches 8 to 10 at `n = 42..46`. The lens's null
`h n / (2 - h)` presumes exponential growth and is flat on `R`; the
independence null on `R` is `log2 |R_n| / (2 - h)`, 4.5 at `n = 13` rising to
7.6 at `n = 41`, and the exact joint maximum lies between 2.3 below and 0.4
above it at every `n` (section 7). `h`, the exact language's local `log2`
growth ratio, falls from 0.39 at `m = 13` to 0.15 at `m = 48`. The
realizability restriction is the one place where the
sufficient condition has slack instead of the proof mechanism, and it was
measured and left in logs until this document. Nothing here proves `RW` on
`R`; the obligation is a rate statement on a language whose entropy is the
open quantity.**

## 1. Objects and why the restriction is sound

`R_m` is the set of words `rho_0 .. rho_(m-1)` of the cell right of the
centre at even times produced by some right half-line of `2m - 1` free cells
under Rule 30 with the centre column driven to `0101...`; endpoint symbol `1`
is bit `1`, `2` is bit `0` (`constant_tail_actual_frontier.endpoint_bits`),
and `constant_tail_right_filter.right_trace_realizable` decides membership
exactly by one CaDiCaL query on the complete right light cone. Advancing one
`rho` coordinate is a two-step time shift that preserves the centre phase, so
a factor of a realizable trace at any offset is itself a realizable prefix
and `R` is factor-closed (`constant_tail_right_filter.py` 27-30). Proved
uniform members of the forbidden set: `11` (`RESULTS-BILATERAL.md`) and
`00000` (`RESULTS-RIGHT-FILTERED-MORTALITY.md`); the remaining 235 minimal
forbidden factors through length 30 are finite computation
(`uc/r1-hardcore/r_exact_language.json`).

For the hypothetical period-two counterexample the endpoint is a genuine
right trace beyond an artificial finite prefix, so at every sufficiently
large scale the block `W = e[n:2n]` and its forced continuation
`Q_n(W) = e[2n:3n+2]` are factors of a realizable trace
(`RESULTS-ACTUAL-RIGHT-FRONTIER.md` section 3, `RESULTS-LATE-PULL-DIAGONAL.md`
section 2). `RW` therefore only needs to exclude sources `W in R_n` whose
forced continuation stays in `R` while the cut stays constant, and any
superset `L` of `R` gives an upper bound on that joint run.

## 2. The recorded extremal words

| grammar, range | words | unrealizable inside `W` | realizable | max joint run of the realizable |
|---|---|---|---|---|
| wide, `n = 10..22` | 312 | 312 | 0 | |
| narrow, `n = 10..38` | 544 | 499 | 45 | 5 |

First forbidden factor over the 811: `11` 274, `101001` 204, `0100101` 96,
`010010001` 41, `0101000101` 31, `0101010000` 29, `00000` 21, `01010001001`
15, `0001000010001` 15, `010100010001` 14, `010010000101` 11, and 19 longer
factors 10 or fewer times each. Every wide deepest word contains `11` or a
length-6 or length-7 factor. The 45 realizable words are narrow deepest
words at `n = 10..15, 17, 20, 21, 23..25, 29, 32`; the deepest of them,
`21222212221222121222122221212122` at `(32, 3)` with `rho = 13`, has forced
continuation `1212122121212...` (the first 13 of 34 forced symbols) whose
first symbol already leaves `R` (joint run 0), and the largest joint run
among the 45 is 5 (two words each at `(10, 3)` and `(14, 3)`). The
continuations and joint runs of the 45 are computed in
`crosscheck/realizable-run/check_words.py` (log and record alongside), not by
`extremal_realizability.py`.

## 3. The lens census, read from its logs

`hf_lang_survival.py` enumerates every prefix `W in L_n`, computes the
H-forced continuation, and reports the first step at which `W Q` leaves `L`
(`LANG`), the first step at which the cut leaves `c` (`E`), and their
minimum (`joint`, which is `RW` restricted to `L`). `L = Rexact30` is the
language of the 237 factors, equal to `R` on words of length at most 30;
`R13` uses the 14 minimal forbidden factors of length at most 13 and is
coarser. Since `W Q[:k]` has length `n + k`,
the lens joint column is exact only where `n + k <= 30` and is otherwise an
upper bound; section 7 replaces it with exact values through `n = 41`. `h` is
`log2` of the growth ratio of `L_n`; the null is the joint depth at which
independent survival `2^(h n - (2 - h) k)` falls below one.

| `n` | `|L_n|` | `h` | null | `LANG` | `E` (`c=2`/`3`) | joint (`c=2`/`3`) | need |
|---|---|---|---|---|---|---|---|
| 13 | 156 | 0.39 | 3.2 | 8 | 5 / 5 | 3 / 3 | 15 |
| 16 | 316 | 0.33 | 3.2 | 10 | 5 / 9 | 3 / 3 | 18 |
| 20 | 721 | 0.28 | 3.2 | 11 | 10 / 6 | 4 / 4 | 22 |
| 24 | 1,493 | 0.25 | 3.4 | 13 | 10 / 9 | 4 / 5 | 26 |
| 28 | 2,904 | 0.23 | 3.6 | 11 | 8 / 12 | 5 / 5 | 30 |
| 30 | 3,908 | 0.21 | 3.5 | 13 | 10 / 12 | 5 / 5 | 32 |
| 34 | 7,174 | 0.22 | 4.2 | 20 | 12 / 14 | 6 / 5 | 36 |
| 38 | 13,309 | 0.23 | 4.8 | 14 | 10 / 12 | 7 / 5 | 40 |
| 40 | 18,139 | 0.22 | 5.0 | 14 | 12 / 11 | 6 / 7 | 42 |
| 42 (`R13`) | 147,494 | 0.33 | 8.4 | 24 | 13 / 13 | 10 / 9 | 44 |
| 46 (`R13`) | 372,145 | 0.33 | 9.2 | 28 | 16 / 18 | 8 / 10 | 48 |

Every row `n = 13..40` is in `hf_lang_survival_Rexact30_n13-40.log` and
`n = 41..46` in `hf_lang_survival_R13_n41-46.log`; the joint maximum over
`n = 13..30` is 6, attained at `(21, 2)`, `(21, 3)`, `(23, 2)` and `(25, 3)`
(values section 7 confirms exactly), and the count of prefixes whose forced
continuation stays in `L` for `n + 2` steps is zero at every `n`. The exact
language grows by a ratio falling overall, with local increases at
`m = 3, 7, 13, 21, 25, 36`, from 1.50 at `m = 2` through
1.31 (`m = 13`), 1.21 (`20`), 1.157 (`30`), 1.120 (`41`) to 1.110 at `m = 48`,
`|R_48| = 32,656` (`r_exact_sat_m1-50.log` to 41, `r_exact_sat_m31-48.log`).

## 4. Reading

The run that `RW` must bound is a factor of two to three smaller on the
realizable language than on the narrow grammar (`D_n(c) = 13..16` at
`n = 35..38`, `RESULTS-NARROW-SUB5.md`, against 5 to 7) and five to eight
times below the need. The reduction comes from the continuation more than
the source: `E` alone on `R_n` prefixes is 0.3 to 0.4 `n` (the source
restriction alone takes the narrow 13 to 16 at `n = 35..38` to 10 to 12),
`LANG` alone 0.35 to 0.65 `n`, and it is their conjunction that sits at 5 to
7. The lens's null `h n / (2 - h)` presumes `|L_n| = 2^(h n)`, which holds for
its finite-type supersets and not for `R`; computed with `R`'s own `h` it is
flat at 3.0 to 3.7 while the joint maximum rises from 3 to 7, so the earlier
sentence that the run "tracks" it was wrong. The independence null on `R` is
`log2 |R_n| / (2 - h)`, the depth at which `|R_n|` sources surviving each
forced step with probability `2^(h - 2)` fall below one; section 7 tabulates
it (4.5 at `n = 13` to 7.6 at `n = 41`), and the exact joint maximum lies
between 2.3 below and 0.4 above it at every `n`. That is
consistent with two filters acting independently at the language's local
entropy and proves nothing about a mechanism. The null grows as
`log2 |R_n|` does, which is where the entropy of `R` enters: a
subexponential `|R_m|` makes the null, and any run that stays under it,
sublinear in `n`. The exact ratio is 1.110 at `m = 48` and still falling, and
whether its limit is 1 is open (`RESULTS-R-EXACT-GROWTH.md`); it is a
question about Rule 30's right light cone under a fixed boundary, not about
the endpoint process.

What this does not do: it proves nothing about `RW` on `R` (the joint census
is finite and rests on the H-forcing kernel and the SAT decider), and the
per-step kill mechanism it would need is the same object every rate attempt
on the wide grammar failed to derive. What it changes is the target: any
future certificate should be sought on `R`, where the margin is `n + 2`
against 6, and the first question is whether `|R_m|` is subexponential
(`RESULTS-R-EXACT-GROWTH.md`: open through `m = 49`, with a fixed exponential
rate and a fixed polynomial exponent both excluded).

Kill for this reading: a source in `R_n` whose forced continuation stays in
`R` for `0.5 n` steps with the cut constant, at any `n` the exact language
reaches. None exists through `n = 41` on the exact language (section 7,
`half-scale` zero at every `n`), and none through `n = 46` on the supersets.

## 5. Scope

Finite: the exact language to `n = 41` (joint, section 7) and `m = 48`
(counts), supersets to `n = 46`; the 856 words are the stored maxima of two
grammars (capped lists, 856 of 980 maximisers), not a census of realizable
sources. The lens census is the 2026-09-03 run; section 7 reproduces its
automaton-only values at `n = 13..30` and supersedes them with exact ones.
Its kernel gate against `psi_kernel.psi` through `n = 9`, its `n = 16` count
control (1292, `RESULTS-RW-LINEAR-SLACK.md` 9.6a) and its joint-column checks
against `rw_restricted_margin` are stated in its docstring and
`uc/r1-hardcore/INDEX-2.md`. `RW`, `(RW-alpha)`, `SEP` and `PT2` are
untouched. Section 8 records the independent check of this document.

## 6. Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --offline --project ../../sygus-p3 python extremal_realizability.py extremal_realizability.json
uv run python uc/r1-hardcore/hf_lang_survival.py --help
uv run --no-project --with python-sat python uc/r1-hardcore/r_exact_sat.py --resume uc/r1-hardcore/r_exact_language.json --max-length 48 --workers 6 --out uc/r1-hardcore/r_exact_language_m48.json
uv run --no-project --with numpy --with python-sat python uc/r1-hardcore/r_exact_joint.py --exact-json uc/r1-hardcore/r_exact_language.json --min-n 13 --max-n 30 --gate-log uc/r1-hardcore/hf_lang_survival_Rexact30_n13-40.log
uv run --no-project --with numpy --with python-sat python uc/r1-hardcore/r_exact_joint.py --exact-json uc/r1-hardcore/r_exact_language_m48.json --min-n 13 --max-n 41 --out uc/r1-hardcore/r_exact_joint_n13-41.json
```

The first takes about 10 s (856 SAT queries). The lens logs are read
directly. The language extension to `m = 48` takes about 10 minutes on six
cores (per-length times in its log); the gate run about one minute and the
exact census about 40 s.

## 7. Exact joint census, `n = 13..41`

Added the same day, after section 3 was re-read: the lens decides `W Q[:k]`
by the factor automaton of `Rexact30`, exact only on words of length at most
30, so its joint column is an upper bound wherever `n + k > 30`, which is
every `n >= 25` and every superset row. `uc/r1-hardcore/r_exact_joint.py`
removes the bound. `R_n` is enumerated from the minimal forbidden factors
through length 48 (`r_exact_sat.py` resumed from 30 to 48, 1,612 factors,
`r_exact_language_m48.json`, log `r_exact_sat_m31-48.log`, whose counts at
`m = 31..41` reproduce `r_exact_sat_m1-50.log`), the forced continuation is
the `hf_lang_survival.py` kernel, and every `W Q[:k]` longer than 48 is
decided by one CaDiCaL query on its complete light cone, so `k_lang` and the
joint run are exact at every `n`. Gate: with the length-30 factors, the
automaton-only joint reproduces the lens log at every `n = 13..30`
(`r_exact_joint_gate_n13-30.log`, 18 passes), and its exact values equal
those of the length-48 run row for row. Record `r_exact_joint_n13-41.json`,
log `r_exact_joint_n13-41.log`; `LANG` is the exact deepest `k_lang`, `E` the
deepest `k_E`, `steps = n + 2`; null is `log2 |R_n| / (2 - h)` with `h` the
local growth exponent `log2 (|R_n| / |R_(n-1)|)` (the lens's `h n / (2 - h)`
is 3.0 to 3.7 on the same rows and is also in the record).

| `n` | `|R_n|` | `h` | null | `LANG` | `E` (`c=2`/`3`) | joint (`c=2`/`3`) | need |
|---|---|---|---|---|---|---|---|
| 13 | 156 | 0.39 | 4.5 | 8 | 5 / 5 | 3 / 3 | 15 |
| 14 | 199 | 0.35 | 4.6 | 6 | 5 / 8 | 4 / 5 | 16 |
| 15 | 251 | 0.34 | 4.8 | 9 | 7 / 6 | 4 / 3 | 17 |
| 16 | 316 | 0.33 | 5.0 | 10 | 5 / 9 | 3 / 3 | 18 |
| 17 | 393 | 0.32 | 5.1 | 8 | 13 / 11 | 4 / 3 | 19 |
| 18 | 487 | 0.31 | 5.3 | 9 | 7 / 6 | 4 / 4 | 20 |
| 19 | 596 | 0.29 | 5.4 | 7 | 7 / 7 | 4 / 4 | 21 |
| 20 | 721 | 0.28 | 5.5 | 11 | 10 / 6 | 4 / 4 | 22 |
| 21 | 875 | 0.28 | 5.7 | 10 | 12 / 10 | 6 / 6 | 23 |
| 22 | 1,054 | 0.27 | 5.8 | 11 | 7 / 12 | 4 / 4 | 24 |
| 23 | 1,255 | 0.25 | 5.9 | 15 | 8 / 10 | 6 / 4 | 25 |
| 24 | 1,493 | 0.25 | 6.0 | 13 | 10 / 9 | 4 / 5 | 26 |
| 25 | 1,780 | 0.25 | 6.2 | 11 | 10 / 10 | 4 / 6 | 27 |
| 26 | 2,111 | 0.25 | 6.3 | 10 | 11 / 9 | 4 / 5 | 28 |
| 27 | 2,483 | 0.23 | 6.4 | 13 | 8 / 12 | 5 / 5 | 29 |
| 28 | 2,904 | 0.23 | 6.5 | 11 | 8 / 12 | 5 / 5 | 30 |
| 29 | 3,378 | 0.22 | 6.6 | 10 | 9 / 12 | 4 / 5 | 31 |
| 30 | 3,908 | 0.21 | 6.7 | 13 | 10 / 12 | 5 / 5 | 32 |
| 31 | 4,502 | 0.20 | 6.8 | 11 | 9 / 11 | 5 / 5 | 33 |
| 32 | 5,153 | 0.20 | 6.8 | 12 | 12 / 13 | 7 / 5 | 34 |
| 33 | 5,875 | 0.19 | 6.9 | 14 | 10 / 12 | 6 / 6 | 35 |
| 34 | 6,664 | 0.18 | 7.0 | 18 | 12 / 14 | 6 / 5 | 36 |
| 35 | 7,541 | 0.18 | 7.1 | 16 | 11 / 11 | 5 / 5 | 37 |
| 36 | 8,534 | 0.18 | 7.2 | 14 | 11 / 9 | 5 / 6 | 38 |
| 37 | 9,649 | 0.18 | 7.3 | 12 | 10 / 10 | 5 / 5 | 39 |
| 38 | 10,876 | 0.17 | 7.3 | 14 | 10 / 12 | 5 / 5 | 40 |
| 39 | 12,231 | 0.17 | 7.4 | 16 | 11 / 11 | 6 / 5 | 41 |
| 40 | 13,730 | 0.17 | 7.5 | 14 | 12 / 11 | 5 / 7 | 42 |
| 41 | 15,384 | 0.16 | 7.6 | 14 | 13 / 13 | 6 / 6 | 43 |

The exact joint run is 3 to 7 at every `n = 13..41`, 7 only at `(32, 2)`
(source `00001000101000010001000101000010`, forced `1000010`, `k_lang = 9`,
`k_E = 7`) and `(40, 3)` (`0001000010000101010100010000100100100100`, forced
`1001000`, `k_lang = k_E = 7`), and 6 for both tails at `n = 41`. The lens
over-stated four cells on `n = 31..40` (`(35, 3)`, `(38, 2)`, `(39, 3)`: 7
against 5; `(40, 2)`: 6 against 5) and the `R13` superset gave 9 / 9 at
`n = 41` against the exact 6 / 6, so the superset rows at `n = 42..46` (8 to
10) should be read as bounds loose by about 3. The count of sources at the
deepest joint level is 1 to 7 at every `(n, c)`, and no source at any `n` has
a joint run of `0.5 n`. The maximum grows from 3 at `n = 13` to 6 at `n = 41`,
about 0.1 per unit of `n`, against the need's slope 1; the null moves from
4.5 to 7.6 on the same range, about 0.11 per unit of `n`, and the maximum is
between 2.3 below it (`n = 37, 38`) and 0.4 above it (`n = 14`; also above at
`n = 21, 23, 32`) at every `n`. `LANG` alone is 0.3 to 0.65 `n`
and `E` alone 0.3 to 0.4 `n` (0.76 at `n = 17`) throughout, so the reduction
is still the conjunction. The `n <= 30` sentence of section 3 is therefore correct in its
numbers and wrong in its method claim; this section is the record.

## 8. Independent check

`crosscheck/realizable-run/` holds a second implementation of everything this
document measures: `rcheck.py` (its own CNF of the right light cone, gated by
exact set equality against `right_trace_forbidden.realized_language` at
`m <= 12` and the counts through 13, and its own forced-continuation kernel
gated against `psi_kernel.psi` on all words of length at most 9 and 300
random longer ones), `check_words.py` (the 856 words: membership, first
forbidden factor, minimality of every factor, forced continuations and joint
runs of the 45), `census.py` (the lens census re-implemented, with
`--sat-exact` deciding every automaton survivor by SAT), `exact_lang2.py`
(its own enumeration of `R_m` to `m = 41`, identical counts and identical 237
factors through 30, 855 through 41) and `compare.py` (every lens row
`n = 13..46` reproduced field by field). It confirmed the totals 856, 811 and
45, the histogram, the section 3 table's transcription and the SAT-exact
joint maxima of section 7 at `n = 13..40`, and it found the defects now
corrected above: the wide and narrow word counts, the `(25, 3)` maximum, the
14-factor `R13`, the "exact through `n = 30`" method claim, the capped word
lists, the docstring citation, and the null, whose lens form is flat on `R`
(3.0 to 3.7) while the joint maximum rises from 3 to 7.

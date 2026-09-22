# Forward survivor census to width 40: the free phase is not bounded, and the hard-core condition is vacuous at one extremal word

Date: 2026-09-16. Pre-registration `PREREGISTRATION-FORWARD-SURVIVOR-W40.md` (written before
the run). Scripts `forward-boundary/forward_survivor_plateau.py` (log
`forward-boundary/forward_survivor_plateau_w2-40.log`, data
`forward-boundary/plateau_words_w30-40.json`) and `forward-boundary/plateau_summary.py` (log
`forward-boundary/plateau_summary_w30-40.log`). The width-30 script and log are untouched and
are the gate.

**Two of the three pre-registered kills fired. `[K]` (H2) The free phase is not bounded by 11
on `w <= 40`: `free(w) = M(w) - (ceil(w/2) - 1)` reaches 16 at `w = 32`, 15 at `w = 37, 38`,
18 at `w = 39` and 16 at `w = 40` (log lines 49, 57, 58, 60, 61, 65), against 11 at `w = 30`;
this is the outcome the pre-registration named as expected and it bears nothing on `(PT2)`.
`[K]` (H3) The hard-core condition on the even-time column `-1` word adds nothing at the
extremal word of width 20: `free_hc(20) = free(20) = 8` with the same argmax
`11010001010101000001`, whose `rho` word `212222212212212221` has no factor `11` (log line 86,
summary log line 12); the same coincidence already holds at `w = 16` (`free_hc = free = 4`,
argmax `1000000100010101`, log line 80, summary line 8). `[C]` For every other `w` in `12..40`
the hard-core filter shortens the free phase by 3 to 11 steps (`free_hc - free` at
`w = 30..40`: `-6, -6, -10, -5, -8, -5, -7, -7, -9, -11, -9`, log line 120), and no plateau
word of any width `30..40` has a hard-core `rho` word (summary lines 60, 100, 153, 263, 400,
480, 632, 770, 800, 830, 900). `[C]` (H1) holds: the `(L1)` level count is exactly `2^(L/2)`
at every even `L <= 40` (asserted; log line 59 for `L = 40`), and the width-30 gate passed
(log line 46). `[C]` The hard-core level counts are the Fibonacci numbers `3, 5, 8, ..., 17711`
at `L = 4, 6, ..., 40` (log lines 69 to 114), which is the number of hard-core words of length
`L/2`; the post-hoc check that the level-`L` seed determines and is determined by its `rho`
prefix `rho_0..rho_(L/2-1)` passed at every `L <= 30` (summary lines 35 to 49). `[R]` So the
controllable phase is a bijection seed to `rho` prefix, the hard-core filter on it is just the
count of hard-core words, and the whole content of the census is in the free phase. `[C]` The
plateau words (alive at the last three nonempty free levels) of one width share no common
suffix (their rightmost cell already varies) but at the flat plateaus their `rho` words share a
long common tail: all 21 plateau words of `w = 32` agree on `rho_6..rho_31` and all 12 of
`w = 39` agree on `rho_5..rho_37` (summary lines 155, 832). The rightmost-12-cells check is
uninformative by construction: the rightmost 12 cells of any `(L1)` survivor range over
exactly `2^6 = 64` words and the plateau words of widths `12..29` already cover all 64.**

## 1. Objects

Left half-line `i <= -1`, Rule 30 `s(t+1,i) = s(t,i-1) XOR (s(t,i) OR s(t,i+1))`, boundary
column `s(t,0) = t mod 2`, `l_t = s(t,-1)`. `(L1)` at even step `k`: `s(2k,-2) != s(2k,-1)`,
equivalently `l_(2k+1) = 1`. Level `L` (even): partial seeds on `-L..-1` satisfying `(L1)` at
steps `0..L/2-1`; built by extending level `L-2` with two bits on the left and filtering at
step `L/2-1` (`forward_survivor_plateau.py`, `filter_level`, chunked at `2^18` rows). Width-`w`
words: level-`L` seeds with leftmost 1 at `-w`, `L = w` rounded up to even, run on as finite
seeds through the free phase (`free_phase`, cap 80 extra even steps, never reached). With
`k = L/2 - 1 = ceil(w/2) - 1`: `M(w) = k + max extra`, `free(w) = M(w) - k`. The profile lists
survivors after `0, 1, 2, ...` extra even steps; the argmax is the first word (in level order)
attaining `M(w)`.

Hard-core variant: `rho_j = 1 - l_(2j)`; hard-core means no `rho_j = rho_(j+1) = 1`, i.e. no
`l_(2j-2) = l_(2j) = 0`. Imposed as an extra kill at every even step `2j >= 2`, in the level
construction (`filter_level(..., hardcore=True)`, no halving assertion) and in the free phase
(`hc_kill`). `M_hc`, `free_hc` are the same statistics under both conditions.

Plateau words of width `w`: every word alive at each of the last three nonempty free levels,
with its level, for `w = 12..40` (the pre-registered range is `30..40`; `12..29` are kept for
the suffix comparison). `rho` word in the `{1,2}` coding: symbol `1` at `k` means `rho_k = 1`
(`l_(2k) = 0`), symbol `2` means `l_(2k) = 1`; printed for `k = 0..M(w)` from the word's own
trajectory (`plateau_summary.py`, `rho_word`), regardless of when the word itself dies.

Gate: for `w = 2..30` the count, `M(w)`, profile and argmax must equal
`forward_survivor_census_w2-30.log` field by field; on a mismatch the script prints
`GATE FAIL` and exits 2 before any `w > 30` row. It printed `GATE PASS` (log line 46).

## 2. Result

### 2.1 Table 1: `(L1)` only, `w = 30..40` (log lines 45 to 61)

| `w` | words past the controllable phase | `M(w)` | `free(w)` | free-phase profile | first argmax |
|---|---|---|---|---|---|
| 30 | 16,485 | 25 | 11 | 16485 8266 4004 1959 961 415 162 62 28 8 4 4 0 | `100001011001011001001101111010` |
| 31 | 16,652 | 26 | 11 | 16652 8460 4122 1871 986 579 277 108 52 26 8 8 0 | `1011011110010001101001101111010` |
| 32 | 32,647 | 31 | 16 | 32647 16425 7996 3834 1975 1003 510 211 111 58 32 22 21 21 21 21 21 0 | `11111001110100011101001110101010` |
| 33 | 32,497 | 27 | 11 | 32497 15491 8117 4354 2244 1060 496 321 131 83 20 8 0 | `100101001001010000011110011100101` |
| 34 | 65,711 | 30 | 14 | 65711 32812 16808 8273 4240 2048 1141 635 277 163 116 48 48 44 24 0 | `1101001000000010110111101001101010` |
| 35 | 65,805 | 30 | 13 | 65805 33836 16846 8354 4380 2422 1256 675 302 162 80 26 22 2 0 | `11011111000010110111110000101101010` |
| 36 | 132,031 | 29 | 12 | 132031 65769 33047 16558 7998 4117 2165 1203 609 226 120 98 44 0 | `100100010100011010111100001100100101` |
| 37 | 131,088 | 33 | 15 | 131088 64390 32163 16137 8136 3919 1888 1177 665 317 178 52 40 12 8 8 0 | `1000001100111001011101111110111100101` |
| 38 | 261,193 | 33 | 15 | 261193 130800 65513 33538 16773 8143 4394 2218 1141 659 316 96 36 12 12 6 0 | `10111011110110111110101110000101101010` |
| 39 | 262,992 | 37 | 18 | 262992 132960 66316 33119 16460 8946 4665 2314 1291 684 407 207 104 56 36 36 12 12 12 0 | `100001010010001011011011110010100111010` |
| 40 | 524,159 | 35 | 16 | 524159 263878 132510 65993 33314 16949 8896 4735 2237 875 395 196 148 72 52 8 8 0 | `1101110100000110100000000000101001000001` |

`free(w)` for `w = 12..40` (log line 64): 8, 4, 6, 7, 4, 6, 7, 4, 8, 6, 9, 9, 8, 7, 8, 7, 9,
9, 11, 11, 16, 11, 14, 13, 12, 15, 15, 18, 16. Rows `w = 2..30` reproduce the width-30 log
exactly (log lines 3 to 45, `GATE PASS` at 46). Level `L = 40` has `1,048,576 = 2^20` seeds
(log line 59); the halving assertion held at every level.

### 2.2 Table 2: `(L1)` and hard-core at every even step, `w = 12..40` (log lines 67 to 116)

| `w` | words past the controllable phase | `M_hc(w)` | `free_hc(w)` | `free(w)` | free-phase profile | first argmax |
|---|---|---|---|---|---|---|
| 12 | 5 | 5 | 0 | 8 | 5 0 | `101000100101` |
| 13 | 7 | 7 | 1 | 4 | 7 5 0 | `1010101000001` |
| 14 | 19 | 8 | 2 | 6 | 19 11 5 0 | `10010101000001` |
| 15 | 14 | 9 | 2 | 7 | 14 4 1 0 | `100000010000001` |
| 16 | 24 | 11 | 4 | 4 | 24 15 10 10 7 0 | `1000000100010101` |
| 17 | 25 | 11 | 3 | 6 | 25 13 10 7 0 | `10100000100010101` |
| 18 | 40 | 10 | 2 | 7 | 40 19 10 0 | `101111110100010101` |
| 19 | 43 | 10 | 1 | 4 | 43 13 0 | `1001000000100010101` |
| 20 | 58 | 17 | 8 | 8 | 58 29 14 11 11 6 6 6 6 0 | `11010001010101000001` |
| 21 | 56 | 12 | 2 | 6 | 56 19 2 0 | `110011001001100100101` |
| 22 | 105 | 16 | 6 | 9 | 105 57 30 8 7 7 7 0 | `1101110010010101000001` |
| 23 | 68 | 13 | 2 | 9 | 68 23 18 0 | `10000001000000100010101` |
| 24 | 205 | 15 | 4 | 8 | 205 80 57 28 13 0 | `100100110010011001000001` |
| 25 | 161 | 16 | 4 | 7 | 161 50 30 12 11 0 | `1010101010100000100010101` |
| 26 | 303 | 17 | 5 | 8 | 303 121 52 21 13 5 0 | `11100111110111101000100101` |
| 27 | 261 | 16 | 3 | 7 | 261 76 32 11 0 | `110010111110011110100010101` |
| 28 | 461 | 16 | 3 | 9 | 461 209 71 27 0 | `1001110101101111110100010101` |
| 29 | 414 | 19 | 5 | 9 | 414 162 73 36 5 5 0 | `11100100111110111101000100101` |
| 30 | 775 | 19 | 5 | 11 | 775 343 129 41 12 5 0 | `110011010000011011011001000001` |
| 31 | 662 | 20 | 5 | 11 | 662 236 76 30 9 6 0 | `1110110000101011111110100010101` |
| 32 | 1,255 | 21 | 6 | 16 | 1255 498 202 96 22 14 11 0 | `11010001011100010110110010000001` |
| 33 | 1,020 | 22 | 6 | 11 | 1020 397 200 100 69 10 5 0 | `101110101111110000010010101000001` |
| 34 | 2,150 | 22 | 6 | 14 | 2150 776 293 116 62 18 5 0 | `1110001101010000001000000101000001` |
| 35 | 1,744 | 25 | 8 | 13 | 1744 732 288 110 32 16 13 5 5 0 | `11101101101100011101011101000100101` |
| 36 | 3,482 | 22 | 5 | 12 | 3482 1244 567 182 37 15 0 | `101011111111010101011011011001000001` |
| 37 | 2,709 | 26 | 8 | 15 | 2709 1062 392 166 82 44 34 24 3 0 | `1101111001111100111110011110100010101` |
| 38 | 5,625 | 24 | 6 | 15 | 5625 2107 796 303 89 39 5 0 | `10101110011111001111100111101000100101` |
| 39 | 4,622 | 26 | 7 | 18 | 4622 1981 756 329 158 82 28 8 0 | `110100010111110100111000110110010000001` |
| 40 | 8,808 | 26 | 7 | 16 | 8808 3261 1204 426 179 65 62 8 0 | `1010100001000001000010001110011001000001` |

Hard-core level counts `L = 4..40` (log lines 69 to 114): 3, 5, 8, 13, 21, 34, 55, 89, 144,
233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, the Fibonacci numbers `F(L/2+2)`,
which count the hard-core binary words of length `L/2`. `free_hc(w) - free(w)` for
`w = 12..40` (log line 120): -8, -3, -4, -5, 0, -3, -5, -3, 0, -4, -3, -7, -4, -3, -3, -4, -6,
-4, -6, -6, -10, -5, -8, -5, -7, -7, -9, -11, -9.

### 2.3 Verdicts as pre-registered

(H1) Halving `|level L| = 2 |level L-2|` at every even `L <= 40`: HOLDS (asserted at every
level; the `# level L=` lines through log line 59 print `2^(L/2)`). A disconfirming run would have raised the
assertion and produced no table.

(H2) `free(w) <= 11` for all `w <= 40`: FAILS, kill fired (log line 65): `free(32) = 16`,
`free(34) = 14`, `free(35) = 13`, `free(36) = 12`, `free(37) = 15`, `free(38) = 15`,
`free(39) = 18`, `free(40) = 16`. This is the outcome the pre-registration named as expected.
A confirming run would have shown every `free(w)` at most 11 on `w = 31..40`.

(H3) `free_hc(w) <= free(w) - 2` at every `w >= 20`: FAILS, kill fired at `w = 20` (log lines
118, 119): `free_hc(20) = free(20) = 8`, `M_hc(20) = M(20) = 17`, same first argmax
`11010001010101000001`, whose `rho` word `rho_0..rho_17 = 212222212212212221` is hard-core
(summary log line 12). The witness is one word; the same coincidence also holds at `w = 16`
(`rho = 222122212222`, summary line 8), below the pre-registered range. At every other
`w = 21..40` the hypothesis's inequality holds with margin 3 to 11, and at `w = 30..40` every
plateau word has a `rho` word containing `11` (summary lines 60, 100, 153, 263, 400, 480, 632,
770, 800, 830, 900: `hard-core rho words: 0/n` for `n = 8, 26, 21, 83, 48, 26, 120, 12, 12,
12, 52`). A confirming run would have shown `free_hc(20) <= 6`.

### 2.4 Plateau summary (data, `plateau_summary_w30-40.log`)

| `w` | last three nonempty free levels (extra, count) | plateau words | hard-core `rho` | common prefix of the words | shared `rho` tail |
|---|---|---|---|---|---|
| 30 | (9, 8) (10, 4) (11, 4) | 8 | 0 | `100001` (6) | none over all 8; two families of 4 sharing `rho_2..rho_25` |
| 31 | (9, 26) (10, 8) (11, 8) | 26 | 0 | `1` (1) | none |
| 32 | (14, 21) (15, 21) (16, 21) | 21 | 0 | `1111100111` (10) | `rho_6..rho_31` = `22112121121221111112211121` |
| 33 | (9, 83) (10, 20) (11, 8) | 83 | 0 | `1` (1) | none |
| 34 | (12, 48) (13, 44) (14, 24) | 48 | 0 | `1` (1) | none |
| 35 | (11, 26) (12, 22) (13, 2) | 26 | 0 | `1` (1) | none |
| 36 | (10, 120) (11, 98) (12, 44) | 120 | 0 | `1` (1) | none |
| 37 | (13, 12) (14, 8) (15, 8) | 12 | 0 | `10` (2) | `rho_33` |
| 38 | (13, 12) (14, 12) (15, 6) | 12 | 0 | `101` (3) | `rho_29..rho_33` = `22221` |
| 39 | (16, 12) (17, 12) (18, 12) | 12 | 0 | `100001` (6) | `rho_5..rho_37` = `221112221211221212111112212222121` |
| 40 | (14, 52) (15, 8) (16, 8) | 52 | 0 | `1` (1) | none |

Summary log lines: `w = 30` at 51 to 71, 31 at 73 to 129, 32 at 131 to 177, 33 at 179 to 349,
34 at 351 to 451, 35 at 453 to 509, 36 at 511 to 755, 37 at 757 to 785, 38 at 787 to 815, 39
at 817 to 845, 40 at 847 to 955. The longest common suffix of the plateau words of one width
is empty at every `w` (the rightmost cell, `l_0`, takes both values within every plateau).
Right-suffix-extension check (same rightmost 12 cells as a plateau word of a smaller recorded
width): every plateau word of every `w = 30..40` matches one, which carries no information:
the rightmost 12 cells of an `(L1)` survivor form a level-12 seed, of which there are exactly
64, and the plateau words of widths `12..29` cover all 64 (checked from the JSON).

The flat plateaus (`w = 32`: 21 words at six consecutive levels; `w = 39`: 12 words at three)
are single families: the words share a `rho` tail from `rho_6` (resp. `rho_5`) onward and
differ only in `rho_0..rho_5` (resp. `rho_0..rho_4`), i.e. in the coordinate that the
controllable phase leaves free. Their seed words share only a short left prefix, because the
bijection seed to `rho` prefix scrambles the right end.

### 2.5 Post-hoc check, not pre-registered (summary log lines 34 to 49)

On the `(L1)`-only level `L`, the map seed to `(rho_0, ..., rho_(L/2-1))` is injective for
every even `L <= 30` (`2^(L/2)` seeds, `2^(L/2)` distinct prefixes), hence bijective onto
`{0,1}^(L/2)`; the number of seeds with a hard-core prefix is `F(L/2+2)` (`2, 3, 5, ...,
1597`), matching the hard-core level counts of table 2 at the same `L`.

## 3. Reading

The controllable phase is exactly a change of coordinates: a level-`L` seed is the same thing
as a free choice of `rho_0..rho_(L/2-1)`, one bit per even step, which is the forward twin of
the archive's forcing (`seam_history_inheritance.run`: one admissible symbol per step). The
hard-core condition on that phase therefore removes nothing structural, only the non-hard-core
`rho` prefixes, and the Fibonacci counts are its signature. Everything the census measures is
in the free phase, and there `free(w)` is not bounded by 11: it grew from 11 at `w = 30` to 18
at `w = 39` (`free(w)/w` about 0.46 at `w = 39` against 0.37 at `w = 30`), consistent with
the archive's `D_n(c)` growing about `0.3 n` and with no plateau in sight. A period-two
counterexample needs `free = infinity`; nothing here moves `(PT2)`.

The hard-core condition does bite in the free phase at all but two widths, by 3 to 11 steps at
`w >= 21`, and no plateau word of `w = 30..40` is hard-core. But the pre-registered inequality
was falsified at `w = 20` by a word whose even-time column-`-1` word is already hard-core over
its whole life, so "the right half-plane always adds at least two steps at the extremal word"
is false as stated; the honest form is "adds 3 to 11 steps on `w = 21..40` and 0 at
`w = 16, 20`". Whether `free_hc` is bounded is not answered on this range: `free_hc` reached 8
at `w = 20, 35, 37` and 7 at `w = 39, 40`, and its argmax words end in the same suffixes
(`...100010101`, `...1000001`, `...100101`) that the width-30 census and the alternating
family already exhibit.

The plateau structure is the one fact here not visible at width 30: the last survivors of a
width form one or two families with a common `rho` tail, differing only in the first five or
six `rho` symbols. That tail is what a bound on the free phase must exclude, and it is a
property of the `rho` word, not of the seed. Nothing here is a mechanism of the killed classes
in the capsule (no quotient, no linearisation, no energy); it is a census.

## 4. Scope

Left half-line only, `(L1)` and the left-side hard-core reading of the right half-plane's
condition; no cut, no four-state alphabet, no forcing, no reconstruction. `w <= 40`,
`2^20` seeds at level 40, free phase capped at 80 extra even steps (max used 18). `M`, `free`
count even steps from time 0 as in the width-30 log (one less than the width-18 census, which
included step 0). The hard-core filter starts at even step 2 (pair `(l_0, l_2)`); `(L1)` at
step 0 is the level-2 seed set. The `rho` word of a plateau word is printed to `k = M(w)` of
its width even where the word itself dies earlier (its own survival is printed beside it, and
asserted equal to `k + extra` from the JSON). Widths `12..29` in the JSON are recorded but
their plateau words are not summarised. Run time on this machine: under one minute for both
tables (file mtimes 17:17:19 to 17:17:57), against the pre-registered 5 to 10 min; memory was
not the limit and no width was skipped.

## 5. Reproduction

From `experiments/rule30/p1-period2-invariant`:

```sh
uv run --no-project --with numpy python forward-boundary/forward_survivor_plateau.py    # about 40 s; exits 2 on GATE FAIL
uv run --no-project --with numpy python forward-boundary/plateau_summary.py             # under a minute
```

The first writes `forward-boundary/forward_survivor_plateau_w2-40.log` and
`forward-boundary/plateau_words_w30-40.json`; the second reads the JSON and writes
`forward-boundary/plateau_summary_w30-40.log`. The gate is against
`forward-boundary/forward_survivor_census_w2-30.log`.

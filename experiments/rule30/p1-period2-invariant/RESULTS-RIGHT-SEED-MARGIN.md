# The right-seed margin: every finite configuration's pin survival is a zero run of one reconstructed row, the runs are fair-coin deep through width 24 (two seed clusters exceed it at widths 26 and 28), and the traces live in a period-5 regime

Date: 2026-09-16. Pre-registration `PREREGISTRATION-RIGHT-SEED-MARGIN.md` (written before the
run). Scripts `forward-boundary/right_seed_margin.py` (log `right_seed_margin.log`, record
`right_seed_margin.json`), post hoc `right_seed_margin_z3.py`, `right_seed_margin_periodic.py`,
`shield_certificate.py` (logs and records alongside, all exit 0). Independent second
implementation `crosscheck/right-seed-margin/` (section 10).

**`[U]` Prefix lemma: for a finite two-sided configuration with left row `W` and right seed
`y`, the centre column equals `t mod 2` exactly for `t < m*(W, y) = min{m : W_m != xhat_m(y)}`,
where `xhat(y)` is the left row reconstructed by left-permutivity from the trace `rho(y)` of the
driven right half-line; so `(PT2)` at period two is exactly "`xhat(y)` has infinite support for
every finite `y`", and the pin survival of every finite configuration is a zero run of one
row. `[C]` Over all `2^16` right seeds of width 16 (31,779 distinct traces to `k = 2048`) and
`M = 4096` reconstructed cells, the longest zero run is 26 against the pre-registered bound 32,
grows by 0, 3, 2, 1 per doubling of `M` from 256, and its distribution (median 11, p90 14,
p99 17, max 26) is that of three nulls (fair coin, hard-core, and no-`11`-no-`00000` random
traces: max 28, 29, 27); the longest tail run is 17; no seed is a counterexample candidate.
The deepest runs end half on an even position (a left condition) and half on an odd one (the
right trace refuses a symbol), 0.519 against 0.504 for the null. `[C]` The pre-registered
reconciliation (Z3) fired because its translation used the dictionary's direct identity, which
needs a finite row at `t = -1`; under I10's shifted identity the forward survival count equals
`seam_history_inheritance.run` at all 56 `(n, c)` cells and the two-sided count is a lower
bound on the joint run of `RESULTS-REALIZABLE-RUN.md`, tight at 14 cells. `[C]` The 45 deepest
run events all sit where the trace is the period-5 word `00001` with one displaced `1`; 96.9
percent of all trace positions lie in period-5 stretches of four or more periods, and under a
purely periodic trace the reconstructed row is periodic (period 7, 84, 155, 728 for trace
periods 2, 3, 5, 7) with zero runs at most 9. `[C]` A robust-shield certificate (adversarial
reachability over the near-wall columns) proves that 377 seeds have a period-2 trace for all
time, whatever the exterior does; their reconstructed rows are period 7 from `m = 1` with a
nonzero block, so `(PT2)` holds exactly for these 377 seeds (the later trap sweep and certificate extensions below
decide 1,905 of the 65,536 seeds). Zero period blocks: none.**

## 1. Objects and the prefix lemma

Rule 30 `s(t+1,i) = s(t,i-1) XOR (s(t,i) OR s(t,i+1))`. Right seed `y` on cells `1..16`; the
right half-line is run with `s(t,0) = t mod 2` as the left neighbour of cell 1;
`rho_k(y) = s(2k,1)`. Column `-1` under the pin is `l_t = 1` (odd `t`), `l_(2k) = 1 - rho_k`
(`RESULTS-FORWARD-BOUNDARY-CENSUS.md` section 1). Reconstruction: `col_0[t] = t mod 2`,
`col_1 = l`, `col_(m+1)[t] = col_m[t+1] XOR (col_m[t] OR col_(m-1)[t])`; `xhat_m(y) = col_m[0]`.
`xhat_m` depends on `rho_0..rho_(floor((m-1)/2))` (halving lemma, Lemma 1 transposed).

**Prefix lemma.** Let `W` be a finite left row (`W_m = s(0,-m)`, zeros beyond its width),
`y` a finite right seed, and evolve `(W, 0, y)` by plain Rule 30 with no boundary. Then for
every `T >= 1`: `s(t,0) = t mod 2` for all `t <= T` iff `W_m = xhat_m(y)` for all `m <= T`.

Proof by induction on `T`, both directions at once. Assume the pin holds through `T-1` (for
`T = 1` there is nothing to assume beyond `s(0,0) = 0`). Then through time `T-1` the right
half-line has seen only the pin as its left neighbour, so `s(t,1)` is the driven value and
`rho_k(y) = s(2k,1)` for `2k <= T-1`; likewise the left half-line has seen only the pin, so
`s(T-1,-1)` is the driven left value from `W`. The pin at `T` reads
`s(T,0) = s(T-1,-1) XOR (s(T-1,0) OR s(T-1,1))`: for `T-1` odd, `s(T-1,0) = 1` and the pin
needs `s(T-1,-1) = 1 = l_(T-1)`; for `T-1` even it needs `s(T-1,-1) XOR rho_((T-1)/2) = 1`,
i.e. `s(T-1,-1) = l_(T-1)`. By Lemma 2 of `RESULTS-FORWARD-HALVING-LEMMA.md`,
`s(T-1,-1) = W_T XOR g(W_1..W_(T-1))` for a fixed function `g`, and the reconstructed row obeys
the same identity by construction, `l_(T-1) = xhat_T XOR g(xhat_1..xhat_(T-1))`. With
`W_m = xhat_m` for `m <= T-1` (induction hypothesis, both directions), `s(T-1,-1) = l_(T-1)`
iff `W_T = xhat_T`. So the pin holds through `T` iff `W` agrees with `xhat` through `T`. QED.

Consequences. (i) The pin holds forever iff `W = xhat(y)`, which needs `xhat(y)` finite; so
`(PT2)` at period two is "`xhat(y)` is never finite". (ii) A zero run `xhat_(a+1..a+z) = 0` with
`xhat_a = 1` is the finite configuration `(xhat_1..xhat_a, y)` keeping the pin through time
`a + z` and losing it at `a + z + 1`: conditions `C_0..C_k` of the halving lemma hold for
`2k + 2 <= a + z`. (iii) The longest zero run `Z(y, M)` over all `y` of width `w_R` and
`a <= M` is the maximal free phase (times two, up to parity) of every finite two-sided
configuration with right width `w_R` and left width at most `M`. (iv) `xhat` depends on `y`
only through `rho(y)`, so everything below is over distinct traces.

**Zero-wall lemma.** `[U]` Under the pin the left half-line never sees the boundary: the
boundary enters only cell `-1`, through `s(t+1,-1) = s(t,-2) XOR (s(t,-1) OR s(t,0))`; at
even `t` the boundary is 0, and at odd `t` it is 1 but the pin forces `s(t,-1) = 1`, which
saturates the OR. So the left half of a counterexample evolves exactly as Rule 30 on the
half-line `i <= -1` with a permanent zero wall, `s(t+1,-1) = s(t,-2) XOR s(t,-1)` at the
wall, and the left-only statement that would close `(PT2)` is: on the zero-wall half-line no
finite seed has `s(2k+1,-1) = 1` for all `k`. With the two proved right-side constraints it
weakens to: no finite seed has `s(2k+1,-1) = 1` and `s(2k,-4) = 0` for all `k` and never five
consecutive even times with `s(2k,-1) = 1`. Under `(L1)` the near-wall columns are explicit
in the demand `rho_k = 1 - s(2k,-1)`: `s(2k,-2) = rho_k`, `s(2k+1,-2) = rho_(k+1)`,
`s(2k,-3) = s(2k+1,-3) = 1 - rho_(k+1)`, `s(2k,-4) = rho_k rho_(k+1)` (the hard-core
constraint is "column `-4` is 0 at even times"), and with hard-core `rho` also
`s(2k+1,-4) = rho_(k+2)`, `s(2k,-5) = (1 - rho_(k+1))(1 - rho_(k+2))`,
`s(2k,-6) = (1 - rho_(k+1)) rho_(k+2)`. `[C]` Both the equivalence and the identities are
checked on every left row of width at most 14 through the `(L1)` horizon
(`forward-boundary/zero_wall_check.py`, log alongside).

**The rotated form.** `[U]` The reconstruction is a second-order cellular automaton `G` on
time-sequences, `col_(m+1) = G(col_(m-1), col_m)`, `G(u, v)[t] = v[t+1] XOR (v[t] OR u[t])`,
whose "time" is the spatial index `m` and whose initial pair is `(pin, l)`. `xhat_m = col_m[0]`.
For a finite left row of width `w_L`, `col_m[t] = 0` for `t < m - w_L`, so a counterexample
is exactly an initial pair whose `G`-orbit converges to the zero fixed point in the product
topology, and at the maximal rate: with the front `E_m = min{t : col_m[t] = 1}`, the
counterexample has `E_(m+1) = E_m + 1` for every `m > w_L` (the left edge of a finite row
moves at speed exactly one; for a general demand the front jumps by many steps in either
direction, since `col_(m+1)` also reads `col_(m-1)` through the OR: the "at most one per
step" first written here was wrong, corrected 2026-09-17), which needs
`col_m[E_m + 1] = 1` at every step (the `11` edge of I7). The reset chain of the left frame
is this front structure read along diagonals. Nothing here is new information; it is the
statement "(PT2) is a basin-of-attraction question for `G` restricted to pairs `(pin, l)`
with `l` built from a finite seed's trace", which is how it would be posed to a symbolic
dynamicist.

## 2. Gates (all PASS, log lines 12 to 15)

G1: distinct `rho` prefixes of length `m = 1..8` over the `2^16` seeds are `2, 3, 5, 8, 12,
17, 25, 36`, equal to `|R_m|` of `r_exact_language_m60.json` (a length-`m` prefix reads
`2m-1 <= 16` cells there); all 31,779 distinct length-60 prefixes are in `R_60`. G2: the
prefix lemma by plain forward Rule 30 on 200 random `(y, a)`: first failure at exactly
`a + gap + 1` in all 200. G3: the vacuum trace reproduces the first 96 symbols of
`driven_vacuum_trace.log`.

## 3. (Z1), (Z1'): the margin is fair-coin deep through width 24

Longest zero run of `xhat_1..xhat_M'` (max / p99 / p90 / median):

| `M'` | seeds (distinct `rho`) | N1 fair coin | N2 hard-core | N3 no `11`, no `00000` |
|---|---|---|---|---|
| 256 | 20 / 14 / 10 / 7 | 23 / 13 / 10 / 7 | 23 / 13 / 10 / 7 | 22 / 13 / 10 / 7 |
| 1024 | 23 / 15 / 12 / 9 | 28 / 15 / 12 / 9 | 24 / 15 / 12 / 9 | 24 / 15 / 12 / 9 |
| 4096 | 26 / 17 / 14 / 11 | 28 / 17 / 14 / 11 | 29 / 17 / 14 / 11 | 27 / 17 / 14 / 11 |

(Z1) HOLDS: max 26 against 32, growth per doubling 0, 3, 2, 1. Longest tail run 17. (Z1')
HOLDS: against N3 restricted to 31,779 samples, max 26 against 27, p99 17.0 against 17.0.
The median 11 and p99 17 at `M = 4096` are the fair-coin longest-run law (`log2 M - 0.67`
and its tail), and the maximum over `N` samples sits at `log2(N M) = 27`: the reconstructed
row's zero runs are those of a fair coin for every input measure tried, including the true
traces. The pre-registered bound `2 log2 M + 8` was loose by that reading; `log2(N M) + 2` is
the right null.

Extension (2026-09-17, `forward-boundary/strengthen/strengthen_1.log`, `strengthen_2.log`,
delegated runs re-read here). Width 18 at `M = 4096`: 126,762 distinct traces, maximum 28
against a fair-coin expected maximum of 28.3 (`log2(NM) = 29.0`), tail run 17. Width 20 at
`M = 2048`: 505,964 distinct traces, maximum 26 against an expected 29.3 (`log2(NM) = 30.0`),
the probability of a fair-coin maximum at or below 26 being 0.022, tail run 21. Width 16 at
`M = 8192`: maximum still 26 (expected 27.3), tail 16. Correction to the wording of section
3: against the exact longest-run law of a fair coin of length 4096 (mean 11.33, median 11,
p90 14, p99 17), the 31,779 width-16 traces match in median, p90, p99 and maximum (observed
26, `P(max >= 26) = 0.62`), but not in distribution: chi-square 1,100 on 16 degrees of
freedom, of which 972 come from 105 seeds with `Z <= 7` against 9.4 expected (the
periodic-trace seeds, whose `xhat` has period 7) and the rest from an excess at `Z = 14, 15`
(+7.9 and +4.6 standard units) and deficits at 11 and 13; the fair-coin and hard-core models pass the
same test (chi-square 10 and 20 on 17 degrees of freedom, p = 0.90 and 0.27) and the
two-factor model does not (chi-square 32, p = 0.016; the "three models pass" first written
here misread the p column of `strengthen_2.log`). So through width 24 the extremes are fair-coin
deep, at width 20 slightly shallower than a fair coin and never deeper (widths 26 and 28 do
exceed it, see "Streaming census" below), while the body of the distribution carries the shields and a mild excess of runs of 14
and 15.

Streaming census (2026-09-17, `forward-boundary/census_scale.py`, driver `census_drive.sh`,
ledger `census_drive.log`): per-seed statistics, a 64-bit hash of each trace to `k = 2048`
for distinctness and the 200 deepest seeds are kept, nothing else; validated at width 16
against the full instrument (max 26, 31,779 distinct, tail 17). Width 22 at `M = 4096`
(`census_scale_w22_M4096.log`, 1.2 CPU hours): 2,022,886 distinct traces of 4,194,304 seeds,
maximum 30 against a fair-coin expected maximum of 32.3 over that many independent samples
(`P(max <= 30) = 0.147`; line `log2(NM) = 32.9`), median 11, p90 14, p99 17, tail run 22, no
seed at or above the line plus 3. Width 24 at `M = 4096` (`census_scale_w24_M4096.log`, 4.1
CPU hours): 8,087,019 distinct of 16,777,216, maximum 34 against expected 34.3
(`P(max <= 34) = 0.62`; line 34.9), median 11, p90 14, p99 17, tail run 24, none at or above
the line plus 3. Expected maxima from `strengthen/faircoin_widths.py` (log alongside). The
distinct traces share prefixes, so they are fewer than `N` independent samples, and a
maximum below the independent-sample expectation is the direction the dependence pushes.
Width 26 at `M = 4096` (`census_scale_w26_M4096.log`, 14.56 CPU hours): 32,341,063 distinct
traces of 67,108,864, maximum 44 against expected 36.3 (`P(max <= 44) = 0.998`,
`P(max >= 44) = 0.0037`; line `log2(NM) = 36.9`), median 11, p90 14, p99 17, tail run 25,
**2 seeds at or above the line plus 3** (the two 44s, seeds `2d3e775` and `1d3e775`, tail 0
both). Width 28 at `M = 4096` (`census_scale_w28_M4096.log`, 54.99 CPU hours): distinct-trace
hashing is disabled above width 26 for memory (`census_scale.py`, `if W <= 26: np.save(...)`),
so the reported expectation uses `N = 2^28 = 268,435,456` (all seeds, an upper bound on the
true distinct-trace count and hence on the expected maximum too, since fewer independent
samples means a lower expected max; the observed deviation is therefore at least this
extreme, possibly more) rather than a measured distinct count. Maximum 44 against expected
39.3 (`P(max <= 44) = 0.985`, `P(max >= 44) = 0.030`; line 40.0), median 11, p90 14, p99 17,
tail run 28, **4 seeds at or above the line plus 3** (four 44s, seeds `ad3e775`, `6d3e775`,
`2d3e775`, `1d3e775`, all tail 0). Width 30 at `M = 1024` (`census_scale_w30_M1024.log`, 9.93
CPU hours): same distinct-count caveat, `N = 2^30 = 1,073,741,824`. Maximum 35 against
expected at most 39.3 (`P(max <= 35) >= 0.0004`; line 40.0). The caveat cuts the other way
here: a smaller true `N` lowers the expectation, so a maximum below it is less extreme than
this figure. With the distinct fraction 0.482 seen at widths 22 to 26 (extrapolated, not
measured at width 30) the expectation is 38.2 and `P(max <= 35) = 0.024`. Median 9, p90 12,
p99 15, tail run 28, 0 seeds at or above the line plus 3. Expected maxima from `strengthen/faircoin_widths.py`
extended with these three widths (log alongside).

**Correction to "no seed at any width reaches three above the line" (main text, paragraph
"Larger widths").** That held through width 24; it is now false. Widths 26 and 28 each have
seeds at or above `line + 3` (2 and 4 respectively, all among the deepest-12 lists above), all
sharing the same shape: `Z = 44`, tail `0`, and paired seeds differing by a single high bit
(`2d3e775`/`1d3e775` at both W26 and W28; `ad3e775`/`6d3e775` additionally at W28). Width 30
has none. This is a change in the data, not a reinterpretation of it.

**Neighborhood check (`forward-boundary/strengthen/deep_seed_neighborhood.py`, log alongside).**
All six flagged seeds share the same low 24 bits (cells 1..24), `0xd3e775`; they differ only
in the width-extension bits (cells 25..28, the seed's high nibble). Sweeping all 16 possible
settings of that nibble at width 28 with the low 24 bits fixed: 4 give `Z = 44` (nibbles
`0001`, `0010`, `0110`, `1010`, exactly the flagged seeds and no others) and the other 12 give
`Z` in `9..14`, the ordinary range (median 11). The hot set is not closed under XOR
(`0001 XOR 0010 = 0011`, not hot) and has no evident linear structure, so this is a local
concentration of ordinary fair-coin-tail events around one seed prefix, not a shield-like
family that would be expected to persist or grow with further width extension. This also
cross-checks the census: at width 26 the extension is 2 bits, so only nibble values `0..3`
are reachable, and of those exactly `1` and `2` are hot (seeds `1d3e775`, `2d3e775`), matching
the census's two flagged width-26 seeds precisely; `0` (`0xd3e775` itself, `Z=13`) and `3`
(`Z=10`) are not flagged, consistent. No further census run is warranted by this anomaly;
resolved without one.

## 4. (Z2): windows shared, but through the period-5 regime

Pre-registered count: 28 distinct pinned windows among the 50 deepest distinct-trace runs
(N3: 47), between the confirm (25) and kill (40) thresholds, INDETERMINATE. Post hoc
(`right_seed_margin_z3.log`): the 50 runs are 45 events (same `a`, `z`; one event is shared
by six traces that agree through it and diverge later), and the 45 events have 28 distinct
windows. Every window is a factor of `(00001)^*` with one displaced `1`, for instance
`0010000100` (six events, contexts `01000010000100100001000010`) and `0000100001` (three
events). The sharing is not a suffix cylinder of the kind the archive looked for; it is the
period-5 regime of section 6.

## 5. (Z3): the pre-registered kill fired on a wrong translation

As pre-registered, `floor((z_n(c) + 3)/2) <= j_n(c) + 1` failed at 10 of 29 rows (log lines 41
to 71). Cause: the translation used I8 of `RESULTS-FORWARD-ENDPOINT-DICTIONARY.md`,
`run_c(e_0..e_(n-1)) = S_n(seed(W))`, which holds only for seeds with `cut_0 = c`, a finite row
at `t = -1`; the margin configurations `(xhat_1..xhat_w, y)` have no such row. The identity
for an arbitrary seed is I10 "Shifted": `run_c(e_1..e_(n+1)) = S_(n+2)(s)` at scale `n+1`. A
second error: the archive's run is the left-only statistic (pin and hard-core junction from
the seed's own continuation), of which the two-sided count is a lower bound: after the
two-sided pin fails at an odd position (the actual trace refuses the symbol the row demands)
the left seed's own continuation may keep the pin a few more steps with a `rho` that no right
seed realizes.

`right_seed_margin_z3.py` recomputes the argmax configuration at every `(n, c)`,
`n = 13..40`, and compares three numbers: the prefix-lemma value `floor((z+1)/2) - 1`
(`c = 2`, `w = 2n+3`) or `floor(z/2)` (`c = 3`, `w = 2n+4` with leading `11`); the forward
count `S_(n+2)(s)` from the pinned left half-line (the archive's definition); and
`seam_history_inheritance.run` on the shifted source `e_1..e_(n+1)`. Result: forward count
equals the archive's run at all 56 cells (the dictionary identity holds on this data); the
prefix-lemma value is at most both, equal to them at 48 cells and smaller at the 8 cells
where the run ends on an odd refusal; and it is at most the joint run `j_(n+1)(c)` of
`RESULTS-REALIZABLE-RUN.md` section 7 at all 56 cells, with equality at 14. So the width-16
traces attain the exact census's maximum joint run at a quarter of the scales, and the
instrument and the census agree. The pre-registered statement was wrong, the data were not.

## 6. Kill anatomy: the runs are defects in the period-5 regime

Ten deepest distinct runs (log lines 74 to 85): `z = 26, 25, 25, 24, 23 (x6)`, at
`a = 604..3982`; seven end on an even position (a condition `C_k = 0`), three on an odd one
(`rho_k` delivered 0, the run demanded 1, and the demanded prefix is excluded by the
forbidden factors through 60 in all three). Over all distinct traces with `z >= 10`, the
longest run ends on an odd position in 0.519 of cases (N3: 0.504): the right side's refusals
are not the mechanism, the two ends are coins. In cells the run is a zero triangle of height
`z/2` standing on row 0 (pictures, log lines 88 to 140).

The period-5 regime (`right_seed_margin_periodic.log`). Under a purely periodic trace of
period `p`, column `-1` has period `2p`, every reconstructed column is `2p`-periodic in `t`,
the column map acts on a finite set, and `xhat` is periodic in `m`: period 7 (`p = 2`), 84
(`p = 3`), 155 (`p = 5`), 728 (`p = 7`), preperiod 0, longest zero run 6, 5, 6, 9, density
0.14 to 0.51 for every rotation. A single displaced `1` in `(00001)^*` gives zero runs 7 to
14. Over the 31,779 distinct traces, the fraction of positions inside period-5 stretches of
four or more periods has mean 0.969 and median 0.986 (30,125 traces above 0.9, 234 below 0.1);
the density of `1` inside the stretches is 0.214. So the driven right half-line from a
width-16 seed spends nearly all of its time `t <= 4096` with column 1 in the period-5 word,
and the deep zero runs of the margin are what one displaced symbol does to the reconstructed
row. The vacuum's period-7 regime (`driven_vacuum_trace.log`) is the exception, not the rule.

## 7. Robust-shield certificate: 377 seeds with a trace that is periodic for all time

Seed `0x0020` (one cell at position 6) has columns 1 to 5 of period 4 and 6 to 13 of period 8
from `t = 0` through `t = 4100` while columns 14 and beyond are chaotic. Column `j` reads
column `j+1` only through the OR, when column `j` is 0, so a near-wall periodic block can be
impervious to the exterior. `shield_certificate.py` makes this a proof: with column `J+1`
treated as an adversarial input, state `(t mod L, columns 1..J)`, depth-first search from
the actual state over all input sequences over-approximates every true trajectory; if the
search closes and every reachable state has columns `1..j*` equal to the observed pattern at
its phase, the pattern holds for all `t`. Of the 649 seeds whose trace to `k = 2048` is
periodic from `k = 0` (475 of period 2, 5 of period 5, 169 of period 7), the search closes
for 377, all of period 2, with 188 to 14,922 reachable states at `J = 20..28` and shields of
`j* = 6` (period 4, 116 seeds) or `j* = 8, 10, 12, 14, 15, 17` (period 8, 261 seeds); seed
`0x0020` closes at `J = 22` with 628 states. For each, `rho` is `(01)^omega` or `(10)^omega`
for all time, `xhat` is periodic with period 7 from `m = 1` (longest zero run 2 or 6), and
`(PT2)` holds exactly. The other 272 (98 of period 2, all of periods 5 and 7) fail the
over-approximation at `J <= 28` (inconclusive, not refuted).

**Lemma (eventually periodic traces are safe).** `[U]` If `rho(y)` is eventually periodic
then no finite left row keeps the pin against `y`. Proof: suppose `(W, 0, y)` keeps the pin
forever; `W` is nonzero (the zero row has `s(2,0) = 1`). Column `-1` is `l_t` with
`l_(2k) = 1 - rho_k`, `l_odd = 1`, so if `rho` has period `p` from index `k_0` then `l` has
the even period `P = 2p` from `t_0 = 2k_0`, and column 0 has period 2, which divides `P`. By left-permutivity
`s(t,-m-1) = s(t+1,-m) XOR (s(t,-m) OR s(t,-m+1))`, so if columns `-m+1` and `-m` are
`P`-periodic for `t >= t_0` then so is column `-m-1`, for the same `t_0`; by induction every
left column is `P`-periodic for `t >= t_0`. But `W` is finite with leftmost `1` at `-w_L`, and
Rule 30 moves the left edge one cell per step (`0 XOR (0 OR 1) = 1`), so `s(t,-m) = 0` for
`t < m - w_L` and `s(m - w_L, -m) = 1`; for `m >= w_L + t_0 + P` the times `m - w_L - P` and
`m - w_L` are both at least `t_0`, congruent mod `P`, and carry different values.
Contradiction. (This is the Jen 1990 / Kopra argument for two adjacent eventually periodic
columns, applied to the pin and its forced neighbour.) The `xhat` period-7 computation above
is therefore a confirmation, not the proof: the 377 certified seeds satisfy `(PT2)` by this
lemma alone, and so does every seed whose trace is eventually periodic for any reason. A
counterexample to `(PT2)` needs a right seed whose trace never settles, matched symbol for
symbol by the demand `1 - l_(2k)` of a finite left seed.

Traps (`forward-boundary/shield_traps.py`, log and JSON alongside, 4.7 hours). The reachable
sets of the 377 certificates, merged by `(L, J)`, are eleven sets of 442 to 44,442 states,
each re-checked closed under both inputs at every state; any right half-line whose
`(t mod L, columns 1..J)` state ever lies in one of them has a periodic trace from then on,
so by the lemma below it has no finite left partner, whatever its width. Sweeping all
65,536 seeds' driven evolutions to `t = 4096`: 1,895 enter a trap, the 377 certified ones at
`t = 0, 1, 2` and 1,518 more at `t = 3..147` (median 20, none later). `(PT2)` holds exactly
for these 1,895 seeds; 63,641 are undecided.

Classification (`forward-boundary/shield_classify.py`, log and JSON alongside, 2026-09-17).
Seed-independent: every `L`-periodic block of columns `1..j*` consistent with the rule on
columns `1..j*-1` is enumerated (as a periodic orbit driven by a periodic column `j*`), and
for each the greatest set of `(phase, columns 1..j*+16)` states agreeing with the block and
closed under both values of column `j*+17` is computed as a fixed point. `[C]` For
`j* <= 17` and `L in {2, 4, 8}` there are 30 robust shields, every one with a period-2
trace. The script's minimality criterion (no narrower shield of the same period as a prefix)
leaves four, two of which are the period-4 blocks written with period 8, so there are exactly
two minimal blocks: the period-4 blocks of width 3, rows `000, 000, 100, 111` (trap of 2,611
states), and of width 6, rows `100110, 111101, 000001, 000011` (25,160 states). Every one of
the 30 shields carries one of these two in its first 3 or 6 columns at some phase
(`strengthen/shield_prefix_check.py`, log alongside); of the 21 period-8 shields, 9 are
period-4 shields written with period 8 and 12 are genuinely period 8 in their outer columns.
(The sentence "every period-8 shield is one of these repeated" that stood here until
2026-09-17 was wrong.) Blocks of period 10 and 14 (period-5 and period-7 traces), `j* <= 12`, buffer 16
(`shield_classify_p5p7.log`): none. The three period-7 shields the certificate found (`L = 14`,
`j* = 4` and `9`) close only with buffers of 23 to 28, so they are outside this run's reach,
and no period-5 block is a robust shield at this buffer, consistent with the period-5 regime
being broken by defects.

Census at widths 22, 24, 26, 28 (`M = 4096`) and 30 (`M = 1024`): section 3, paragraph
"Streaming census" (`census_drive.log`).

Extension (2026-09-17, `forward-boundary/strengthen/strengthen_3.log`, `_4.log`, `_4b.log`).
The trap sweep to `T = 16384` reproduces every entry below 4096 and finds none at or after
`t = 148`. Continuing the certificate to `J = 32` closes 53 more of the 272 inconclusive
seeds (430 of 649, all period 2), and starting from the settling time closes 1,373 of the
1,846 strict settlers of periods 2 and 7 with a preperiod, among them three period-7 traces
(seeds `76ec`, `b6ec` with `j* = 4`, `L = 14`, and `ec41` with `j* = 9`, `L = 14`), the first
shields with a trace period other than 2. Every certified `xhat`, recomputed with a
4,000-cell tail, is periodic with a nonzero block (periods 7, 14, 28 for period-2 traces and
728 for period 7; the instrument's own `eventual_period(x, 3000, 2)` accepts a 3-cell
constant tail and must not be used for that verdict). Certified seeds 1,803; decided seeds
(certified or trap-entering) 1,905.

Does every trace settle? No sign of it. With a strict criterion (period at most 60, at least
ten periods in the tail to `k = 2048`) 6,805 of the 65,536 seeds have a periodic tail: 1,913
of period 2 (preperiod quartiles 0, 1, 4, 8, maximum 64), 577 of period 7 (maximum 80), 4,175 of
period 5 (5 of them the already-certified pure-periodic seeds of line 232 above, preperiod 0;
the other 4,170 have preperiod 1,845 to 1,993) and 140 of period 18 (preperiod 1,727 to 1,850),
i.e. the late-settling ones in the last 45 to 303 symbols only.

`forward-boundary/strengthen/tail_spotcheck.py` (pre-registered in
`PREREGISTRATION-TAIL-SPOTCHECK.md`) replaces the unlogged twelve-and-six spot check with the
whole population of all **4,315** period-5 and period-18 strict settlers (the script's own
population, `pop = {s: ep for s, ep in strict.items() if ep[0] in TARGET_PERIODS}`, applies no
exclusion; an earlier draft of this paragraph subtracted the 5 already-certified pure-periodic
seeds of line 232 to get 4,310, which is not what the script computed and is corrected here).
**5 have a periodic near-wall column** at buffer `2*pre+2` (all period 5; seeds `20dc`, `60dc`,
`99cb`, `9b6a`, `a0dc`), refuting that half of the original claim rather than confirming it. And
**258 of the 4,315 (6.0 percent) are still periodic when the trace is extended to `k = 8200`**
(`tail_spotcheck.log`, `tail_spotcheck.json`): 250 of period 5 (including all 5 with a near-wall
column) and all 8 of the period-18 seeds that stay periodic there do (of the 140 period-18 seeds
only 8, about 5.7 percent, are still periodic at `k = 8200`; several of the survivors reclassify
as period 5 rather than 18 at the longer horizon). So "the six period-18 tails are not periodic
when the trace is extended to `k = 8200`" was true of the specific unlogged sample, plausibly by
chance (a random six missing all 8 survivors out of 140 has roughly 66 percent probability), but
is false as a statement about the population, and this exhaustive result replaces it. The
corrected picture: genuine settling into a shield (a periodic near-wall column) does happen for 5
seeds in this population, all of them also among the seeds still periodic at `k = 8200`, so it
does not happen exclusively as a stretch of the margin regime; a nonzero fraction of the traces
themselves also stay periodic well past their fitted `k = 2048` period, which the "not at all"
phrasing overstated for the period-18 seeds specifically. The vacuum (not periodic to
`k = 65536`) is the typical case. The conjecture
"every finite seed's trace is eventually periodic", which with the lemma above would prove
`(PT2)` outright, is unsupported by this data. This is the first proved
eventually-periodic trace of a finite seed in the archive; it also shows `R` contains
infinite periodic traces of finite seeds, which the zero-entropy and non-sofic questions of
`RESULTS-R-STRUCTURE.md` must accommodate.

## 8. Reading

The instrument replaces the left enumeration, the SAT lens and the constant-cut machinery by
one row per right seed, and it says three things. The margin is a fair coin: no measure on
traces, and not the true traces, makes the reconstructed row's zero runs longer than
`log2(N M)`; the right side is not "favourable" to a finite left, and its thinness (which is
real, section 6 and `RESULTS-R-STRUCTURE.md`) does not translate into deeper runs. The
right trace is not chaotic near the wall over the horizon seen: it is a period-5 word with
sparse defects, and the archive's picture of two chaotic sequences compared at the centre
(from the standing stop rule for this thread) is wrong for the right half at width 16 and
`t <= 4096`; what is chaotic is the timing and shape of the defects. And there exist seeds
whose trace is provably periodic forever, for which `(PT2)` is a theorem. None of this bounds
the free phase for a general seed; the defects are where the exterior's chaos reaches column
1, and a proof of `(PT2)` in these coordinates is a statement that the defects of a right
trace can never be exactly the row a finite left seed reconstructs to, which is the same
comparison as before with the right side now understood as "period 5 plus defects".

## 9. Scope

Width 16 only (`2^16` seeds, 31,779 traces); `M = 4096`; nulls of `2^16`. The shield
certificate is exact for the 377 seeds and silent on the rest. Nothing here is a bound for all
seeds. `RW`, `(SEP)` untouched.

## 10. Independent check

Referee pass on the two lemmas (`crosscheck/verify-0916/margin/REFEREE.md`, `referee.py`,
log): both HOLD. The prefix lemma's "by construction" step is justified because the
reconstruction relation is the Rule 30 relation solved for the left neighbour, so the
reconstructed array is the driven left half-line of the infinite seed `xhat` and Lemma 2
applies to it with the same `g`; finiteness of `y` is never used. Numeric: 300 of 300 random
pairs (random rows, truncations of `xhat`, truncations with one flipped bit) fail the pin at
exactly the first disagreement; all `2^20` left rows of width at most 20 lose the pin against
seed `0x0020` by `t = 22`, with the loss time equal to the first disagreement on every row. The
referee's two write-up corrections (the period must be taken even; the zero row is excluded)
are in the proof above.

`crosscheck/right-seed-margin/rcheck.py` (written from the definitions without reading the
instrument; per-seed uint8 arrays, no bit packing; its own prefix-lemma gate, 100 of 100)
and `compare.py` (log `compare.log`): `Z` at `M = 512` agrees on all 65,536 seeds, and `Z`,
`a`, `p`, `Z_tail` at `M = 4096` agree on all 200 listed seeds, every field. VERDICT AGREE.

## 12. Proof search on the zero-wall statements (2026-09-16/17)

Four attempts on S3, S3-hc, S3-hc5 (section 1, zero-wall lemma), each with an adversarial
refuter that re-ran every script and re-derived every lemma: `r-structure/theory-s3/`
(`attempt-*.md`, `refute-*.md`, `scripts/`). No attempt claims a proof and no refuter found
one hidden in an attempt. What survives, all `[U]` unless marked:

- Edge meets wall (target S3-hc): S3-hc for `w_L <= 4`; identities for columns `-8`, `-12`,
  `-16` under hard-core; a "zero-wall column" statistic that is 4 on every demand tested
  (random, Fibonacci, Thue-Morse, depth 1500, `[C]`) and fails for one periodic demand the
  eventually-periodic lemma already excludes. Diagnosis: no argument that uses `rho` only
  through its factor structure reaches the edge.
- Backward tree (target S3): the zero-wall step is exactly two-to-one on rows; a finite row
  has a finite preimage iff its last two cells are `10`; the merge automaton has 10 states
  and growth `1.6956^L`, so a fraction `1/4` of finite rows have finite preimages; the
  pinned configurations `(xhat(y), 0, y)` over all right configurations `y` form a system
  conjugate to the full one-sided 2-shift under `F^2`, in which S3 is "the finite rows are
  never hit". Diagnosis: no wall statistic bounded independently of `w_L` can exist (its
  Lemma 3), so the free phase is not controlled by any finite wall state. It also flags a
  wording error in `PROOF-STATE-CAPSULE.md` section 2 and `RESULTS-FORWARD-BOUNDARY-CENSUS.md`
  about the two-to-one map (not verified here; see the file).
- Density rigidity (target S3-hc5): lemmas A to G on the forced near-wall structure under
  `(L1)` and hard-core (columns `-4..-8` explicit, a "pocket" row when `rho_(k+1) = 1`, the
  frame of columns `-3..-10` settles by `t = 12` for every width, tight), and the exact HC5
  census to depth 45. Diagnosis: the aligned-pair bound that would close S3-hc holds only to
  pair 4 (`P_5 = 2` at `00101`), and no bounded-window argument reaches the edge above width
  about 30.
- Counterexample hunt (target: refute S3): none. S3, S3-hc, S3-hc5 hold for every seed of
  width `<= 62` `[C]`; the observed `(L1)` free phase is at or below the fair-coin median for
  the number of seeds at every width `24..62` but one; greedy and beam extensions to width
  125 reach a free phase of at most 16; the largest excess of survival time over width is
  `+2`. The refuter's re-check of the hard-core and HC5 nulls gives slopes 0.263 and 0.233
  per unit width against the measured 5 to 7 on `w = 30..40`, below the coin, and "cannot be
  separated from a constant".

Two consequences worth stating. `[U]` The left rows keeping `(L1)` forever, finite or not,
are in bijection with all demand sequences (halving lemma), and the zero-wall `F^2` acts on
them as the one-sided shift on the demand: `(X_inf, F^2)` is the full one-sided 2-shift, and
S3 says the finite rows are not in it. The set `D` of demands of finite rows is countable,
shift-invariant, has no eventually periodic point (the lemma of section 7) and is dense (the
controllable phase realizes every prefix), so no closed-set or invariant-measure argument
separates it from anything. The strong form of the target is `D` disjoint from the trace
subshift `X_R` over all right configurations, finite or not (no finite left seed has a
period-two centre with any right partner); its finite evidence is the exact joint census of
`RESULTS-REALIZABLE-RUN.md` section 7, where every source in `R_n`, `n <= 41`, keeps the pin
with a demand inside `R` for at most 7 more steps. The "no finite wall state" lemma of the
backward-tree track says only that a bounded wall window cannot bound the total survival,
which is the halving lemma; it does not bear on the free phase.

Reading: the left-only statements are supported by every finite computation and by nothing
uniform. Every route that reasons from the wall outward stops before the edge, and every
route that reasons from the edge inward stops before the wall; the middle is the chaotic
transient of both chains (`RESULTS-DIAGONAL-TRANSIENTS.md`). This is the same wall the
archive's 25 endpoint-coordinate routes hit, now in plain coordinates.

## 11. Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --no-project --with numpy python forward-boundary/right_seed_margin.py 4096 16 forward-boundary/right_seed_margin.json   # 43 s
uv run --no-project --with numpy python forward-boundary/right_seed_margin_z3.py         # 30 s
uv run --no-project --with numpy python forward-boundary/right_seed_margin_periodic.py   # 3 min
uv run --no-project --with numpy python forward-boundary/shield_certificate.py 0 28      # minutes
uv run --no-project --with numpy python crosscheck/right-seed-margin/rcheck.py           # 1 min
uv run --no-project --with numpy python crosscheck/right-seed-margin/compare.py
```

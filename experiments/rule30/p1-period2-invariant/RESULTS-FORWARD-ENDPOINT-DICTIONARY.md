# The forward form and the endpoint form are one object: the exact dictionary

Date: 2026-09-16. Pre-registration `PREREGISTRATION-FORWARD-ENDPOINT-DICTIONARY.md`
(written before the run). Script `forward-boundary/dictionary/dictionary.py` (25 checks,
exit 0 iff every check passes), log `forward-boundary/dictionary/dictionary.log` (107 lines,
10.6 s, line 106), per-seed table `forward-boundary/dictionary/seeds_w5-14.tsv` (16,368
rows). Sibling logs read, not rerun: `forward-boundary/forward_boundary_census_w2-18.log`
(`M(w)`) and `forward-boundary/forward_survivor_plateau_w2-40.log` (Table 2, `M_hc(w)`).
Kernel `psi_kernel.py` (`Endpoint`, `psi`, `CONE`, `BOUNDARY`), `seam_history_inheritance.run`.

**`[U]` `[C]` The endpoint triangle is the pinned left half-plane in one affine chart:
`T[u][d] = 2 x(t, i) + x(t, i-1)` at `(t, i) = (u - d - 1, -(u + d + 2))`, the high bit the
right cell of a horizontal pair. This is the unique survivor of the pre-registered box of
202,500 coordinate changes and pair readings on all 510 binary endpoints of length at most 8
(log lines 5 to 9), exact on all 2,046 binary endpoints of length at most 10 (lines 8, 12),
forced already by the cells with `t >= 0` (line 9), and it is a three-line consequence of
`carry_action` being one Rule 30 step (section 2, identity I1). The kill did not fire. The
endpoint symbol is `e_u = (x(2u,-1), x(2u,-2)) = (1 - rho_u, rho_u)`; the boundary symbol `3`
is the odd-time pair `(x(2u-1,-1), x(2u-1,0)) = (1,1)`; depth `d` is the anti-diagonal
`t + i = -(2d + 3)`; the `d = u` edge is the row `t = -1` before the seed. `[U]` `[C]` In
this chart the archive's objects read: the H-forcing `Q_n(W)_j` sets `x(j-1, -(2n+j+2)) = 1`
on the anti-diagonal `t + i = -(2n+3)` and `Psi_j` is the cell to its left (4,606 forced
steps, line 13); `cut_j = c` is `(x, x_left) = (1,0)` for `c = 2`, `(1,1)` for `c = 3` on
that anti-diagonal (3,586 cases, line 14); constant cut `c` at depth `n` for `j >= 1` is
exactly a finite time-0 row of width `2n+3` (`c = 2`) or `2n+4` with leading `11` (`c = 3`),
and `cut_0 = c` is exactly a finite row at `t = -1` with the leading edge of `c` (leftmost 1
at `-(2n+2)` for `c = 2`; `11` at `-(2n+3), -(2n+2)` for `c = 3`, a leading `10` there giving
`cut_0 = 1`) (673 and 153 instances, lines 15 to 17, 8,319 cells, line 19); `run_c(W)` equals
`S_n(seed(W))`, the number of consecutive even times `2k`, `k >= n`, at which the pin
`x(2k,-2) != x(2k,-1)` holds and no `11` junction occurs, in the one finite seed that `W` and
`cut_0 = c` determine, verified three ways on all 4,092 `(W, c)` with `|W| <= 10` (line 18).
`[C]` Reconciliation, exhaustive over all `2^(w-1)` seeds for `w = 5..18` (lines 38 to 58)
and against the sibling hard-core census to `w = 40` (lines 74 to 104): the census's
`survived(s)` and the archive's run count the same event with three differences, the run
starts at `k = n`, the run adds the hard-core junction, and the run sees only the seeds with
`cut_0 = c` (a finite row at `t = -1` with the leading edge of `c`), which one shift by an
endpoint symbol removes at the price of one scale. Hence
`n + D_n^hc(c) <= M_HC(w) <= n + 2 + D_(n+1)^hc(c)` with `w = 2n+3` (`c = 2`) or `2n+4`
(`c = 3`), one side attained at 22 of the 29 widths `12..40` and both at `w = 22, 24, 39`,
so `free_HC(w)` lies in `[D_n^hc(c) - 1, D_(n+1)^hc(c) + 1]`. `[K]` for the unfiltered statistic: the census
maximum `M(w)` is attained by a seed whose `rho` contains `11` at `w = 10, 11, 12, 13, 14, 15,
17, 18` (lines 43 to 51); at `w = 12`, `M = 14` against `M_HC = 6` (line 45). The forward
census's free phase is therefore not a statistic that any bound on `D` controls, and not one
`(PT2)` needs, since the right half forbids those seeds. Scope: the four-state endpoint
alphabet is a pinned configuration only on `{1,2}`; symbols `0` and `3` code a broken pin
(as unpinned configurations some of them are still exact readings, see
`crosscheck/verify-0916/dictionary/`) and
398,248 of 732,520 broken-pin cells disagree with the half-plane (lines 10, 11). This is a
dictionary. `(PT2)`, `(PSI)`, `(RW)` are untouched.**

## 1. Objects

**Forward form.** Cells `x(t, i)`, `i <= 0`, `t >= -1`, with the centre pinned,
`x(t, 0) = t mod 2`, and column `-1` given, `x(t, -1) = l_t`. The pin `c_(t+1) = l_t XOR
(c_t OR r_t)` forces `l_t = 1` at odd `t` and defines `r_(2k) = 1 - l_(2k)`
(`RESULTS-FORWARD-BOUNDARY-CENSUS.md` section 1). `rho_k = s(2k, 1)` is the even-time
column-1 word of the right half (`docs/rule30/FACT-INDEX.md:142`, `right_trace_forbidden.py:74-85`
`numeric_rho`), so `l_(2k) = 1 - rho_k`. Left-permutivity
`x(t, i-1) = x(t+1, i) XOR (x(t, i) OR x(t, i+1))` determines every cell of the backward cone
`t - i <= t_max + 1` from `l_(-1..t_max)`. The pin is extended to `t = -1`,
`(l_(-1), c_(-1)) = (1, 1)`; the row `t = -1` is the backward left-permutive extension of the
seed. `HalfPlane` in the script (`dictionary.py:45-73`) is this object, memoised, raising
`KeyError` outside the cone.

**Endpoint form.** `e_k in {1, 2}` with state `1` = `rho` bit `1`, state `2` = `rho` bit `0`
(`constant_tail_actual_frontier.py:45-50` `endpoint_bits`,
`RESULTS-ACTUAL-RIGHT-FRONTIER.md:22`). The triangle `T[u][d]`, `u = 0..L-1`,
`-u-1 <= d <= u`: `T[u][-u-1] = e_u`, `T[u][-u] = BOUNDARY[e_u]`,
`T[u][d] = CONE[T[u-1][d-1]][T[u][d-1]]` (`RESULTS-PSI-ANCESTRY-LAW.md` section 1), read off
`psi_kernel.Endpoint` as `column[k] = T[u][-k]`, `diagonal[k] = T[u][k]` (`dictionary.py:101-113`;
the recurrence as printed in the psi doc agrees with the kernel on all 510 binary endpoints,
log line 4). `cut_j(WQ) = T[n+j][n]`, `n = |W|`; `run_c(W)` is
`seam_history_inheritance.run` in the wide grammar.

**Where the endpoint word comes from.** The archive builds it in three steps, and the
dictionary is read off them. (a) The reconstruction frontier is the pair of anti-diagonals
`A_j = x(T-j, -j)`, `B_j = x(T-1-j, -j)` (`docs/rule30/RESULTS-alt-trace-fiber.md:877-878`,
also `docs/rule30/RESULTS-period3-fiber.md:59`). (b) `RESULTS-CARRY.md:11-31` reads the
aligned symbol `q_j = (a, b) = (A_j, B_(j-1))` and carries `(c, d) = (C_(j+1), D_(j+2))` with
`c' = c XOR (a OR b) = C_j`, `d' = d XOR (c OR a) = D_(j+1)`, emitting `(d', c')`; with
`t = T - j` these are `q_j = (x(t, -j), x(t, -j+1))` and `(c, d) = (x(t, -j-1), x(t, -j-2))`,
four cells of one row, and the two recurrences are `c' = x(t+1, -j)`, `d' = x(t+1, -j-1)`:
`carry_action` (`dyadic_periodicity_analyzer.py:38-42`) is one Rule 30 step of a horizontal
pair, given the pair to its right. (c) `feed` (`dyadic_periodicity_analyzer.py:275-280`) stacks
these transducers, layer `k` holding generation `T + 2k`, and `terminal_cone` (`:291-295`)
feeds every layer its shallowest symbol `q_1 = (l_(T-1), c_(T-1)) = (1, 1) = 3`, the odd-time
boundary pair. The endpoint word is the stack after the terminal symbols
(`RESULTS-DYADIC-PERIODICITY.md:102-137`, "let `e` be the endpoint word and `x` its
inverse-terminal cut"): layer `k` then holds `(C_1, D_2) = (x(2k, -1), x(2k, -2))`.

## 2. Result: the dictionary

Each identity names its check (log line in parentheses). `[U]` marks a derivation written
here, `[C]` an exhaustive finite check, `[R]` a number read from a sibling log and not rerun.

**I1 (chart).** `[U]` `[C]` For every binary endpoint,

```text
T[u][d] = 2 x(t, i) + x(t, i-1),   (t, i) = (u - d - 1, -(u + d + 2)),
u = (t - i - 1)/2,   d = -(t + i + 3)/2.
```

`u` indexes the diagonal `t - i = 2u + 1`, `d` the anti-diagonal `t + i = -(2d + 3)`; the
triangle covers the cells with `t + i` odd, `t >= -1`, `t - i <= 2L`, and the pair covers
both parities, so it is the whole backward cone of `l_(-1..2L-1)`. Derivation: with
`(c, d) = (x(t, i), x(t, i-1))` and `(a, b) = (x(t, i+1), x(t, i+2))`, `carry_action` gives
`c' = x(t+1, i+1)`, `d' = x(t+1, i)`, so `FORWARD[(a,b)]` moves a pair one up and one right;
`CONE[L][R] = INVERSE[swap(L)][R]` therefore moves a pair one down and one left given the pair
`L` to its right on the lower row, and `T[u][d] = CONE[T[u-1][d-1]][T[u][d-1]]` is
left-permutivity with `T[u][d-1]` at `(t+1, i+1)` and `T[u-1][d-1]` at `(t, i+2)`. The two
edges: `T[u][-u-1] = e_u` at `(2u, -1)` (I2) and `T[u][-u] = tau_3^(-1)(e_u)` at `(2u-1, -2)`,
since feeding `3 = (x(2u-1,-1), x(2u-1,0)) = (1,1)` into `(x(2u-1,-2), x(2u-1,-3))` gives
`(x(2u,-1), x(2u,-2)) = e_u` by the same step. Induction on `d` from `-u-1` gives every cell.
Checks: `D1_unique_affine_match`, 202,500 candidates (`|alpha|, |beta|, |alpha'|, |beta'| <= 2`,
`|gamma|, |gamma'| <= 4`, four pair readings) on 29,692 cells of the 510 binary endpoints of
length at most 8, one survivor (lines 3, 5, 6, 8); `D1b`, the same single survivor when the
`d = u` cells (those at `t = -1`) are excluded (lines 7, 9); `D1c`, 158,720 cells of the 1,536
binary endpoints of length 9 and 10, zero mismatches (line 12); `E0` (line 4). A
disconfirming run would have printed an empty survivor list, or two, or a first mismatch on
`D1c`.

**I2 (endpoint symbol).** `[U]` `[C]` `e_u = (x(2u, -1), x(2u, -2)) = (l_(2u), l_(2u) XOR
l_(2u+1)) = (1 - rho_u, rho_u)` under the pin. State `1` is `l_(2u) = 0`, state `2` is
`l_(2u) = 1`. Check `D0_rho_bits_equal_endpoint_column` (line 1): the column built from
`rho` bits and the column built from the endpoint states coincide on all 510 endpoints.

**I3 (boundary and scope).** `[U]` `[C]` `BOUNDARY = tau_3^(-1)` and
`T[u][-u] = (x(2u-1, -2), x(2u-1, -3))`. A four-state symbol `e_k = (h, lo)` is
`(l_(2k), l_(2k+1)) = (h, h XOR lo)`, so `0` and `3` mean `l_(2k+1) = 0`, a broken pin, while
the next layer still feeds `3`, which asserts `l_(2k+1) = 1`. So the four-state alphabet is a
configuration only on `{1,2}`. Check `D2` (line 10): on all 21,844 four-state endpoints of
length at most 7, every cell whose pin window (the odd times `2k+1` in `[u-d-1, 2u-1]`)
is intact agrees with the half-plane (393,728 cells, 0 disagree), and 398,248 of the 732,520
cells with a broken pin in the window disagree, the first at `e = (0, 2)`, `u = 1`, `d = 0`,
`T = 1` against forward `0` (line 11, `D3`). The archive's four-state gate in
`psi_kernel.validate` checks the carry algebra, not a configuration.

**I4 (depth lines).** `[U]` `[C]` `cut_j(WQ) = T[n+j][n]` is the pair at
`(t, i) = (j-1, -(2n+j+2))`, on the anti-diagonal `t + i = -(2n+3)`, one step per `j`
down-left. The step `j = 0` sits at `t = -1`. Check `C1` (line 14): all 3,586 `(endpoint, n)`
splits of the binary endpoints of length at most 8, computed through `Endpoint.peek` as
`seam_history_inheritance.run` does.

**I5 (H-forcing).** `[U]` `[C]` The cell `x(j-1, -(2n+j+2))` depends on `l` up to time
`2(n+j)` with coefficient 1 in `l_(2(n+j))` (left-permutivity along the diagonal), and not on
`l_(2(n+j)+1)`; so exactly one `l_(2(n+j))`, hence exactly one `Q_n(W)_j in {1, 2}`, makes it
`1`, and then `Psi_j = x(j-1, -(2n+j+3))`, the cell to its left. Check `H1` (line 13): all
510 binary sources with `n <= 8`, 4,606 forced steps, forward choice equal to `psi_kernel.psi`
in symbol and low bit. This is the archive's `(H)` integral of `RESULTS-PSI-ANCESTRY-LAW.md`
section 3 read as a cell: the parity of zero-cells in a column window is the XOR chain of
ORs along one diagonal.

**I6 (cut = c).** `[U]` `cut_j = 2` is `x(j-1, -(2n+j+2)) = 1` and `x(j-1, -(2n+j+3)) = 0`;
`cut_j = 3` is both `1`. The map `(l_(2k), l_(2k+1)) -> (high, low)`, `k = n+j`, is a
triangular bijection (the low bit has coefficient 1 in `l_(2k+1)`), which is why exactly one
four-state symbol gives each `c` and the run stops when that symbol is `0` or `3` (pin broken
at `2k+1`) or violates the junction.

**I7 (constant cut is a finite row).** `[U]` `[C]` `CONE[2][2] = CONE[3][3] = CONE[0][0] = 0`.
Hence `cut_j = c` for all `j >= 1` gives `T[n+j][n+m] = 0` for `j >= m+1`, `m >= 1`, i.e. all
cells left of the anti-diagonal at `t >= 0` are `0`: the time-0 row is finite with leftmost
`1` at `-(2n+3)` (`c = 2`, width `2n+3`) or leading `11` at `-(2n+4), -(2n+3)` (`c = 3`,
width `2n+4`), and every later row has the same edge shifted left by `t`; conversely a finite
row of that shape has the leading edge `11` at every `t >= 1` (a `10` edge becomes `11` in one
step) and so has `cut_j = c` for every `j >= 1`. With `T[n+1][n+1] = CONE[cut_0][c]` and the
columns `CONE[.][2] = (3,1,0,1)`, `CONE[.][3] = (2,0,1,0)`: `cut_0 = 2` is exactly a finite row
`t = -1` with leftmost `1` at `-(2n+2)`; for `c = 3`, `cut_0 = 3` is a finite row `t = -1`
with leading `11` at `-(2n+3), -(2n+2)` and `cut_0 = 1` one with leading `10`; every other
`cut_0` makes row `-1` eventually all `1`. Checks: `F1` (line 15), 673 `(e, n, c)` instances
among the binary endpoints of length at most 9 with `cut_j = c` for all available `j >= 1`,
153 of them also at `j = 0`, every row in the cone has the stated shape; `F1b` (line 17), the
90 instances with `c = 3`, `cut_0 = 1`; `F2` (line 19), the 4,092 seeds `seed(W)` of I8 have
`cut_j = c` at all 8,319 cells whose pin window is intact.

**I8 (the run as a forward statistic).** `[U]` `[C]` For a binary `W` of length `n` and
`c in {2, 3}` let `seed(W)` be the time-0 row of width `2n+3` (`c = 2`) or `2n+4` with leading
`11` (`c = 3`) whose cells at `-1..-(2n)` are determined by `W` through the triangular
bijection with `l_0..l_(2n-1)`, and whose cells at `-(2n+1), -(2n+2)` are the unique pair
with `cut_0 = c` (a finite row at `t = -1`, I7). Then

```text
run_c(W) = S_n(seed(W)),
S_m(s) = #{consecutive k >= m : x(2k,-2) != x(2k,-1) and not (x(2k-2,-1) = x(2k,-1) = 0)},
```

the pin at `2k+1` and the hard-core junction `e_(k-1) e_k != 11` (`l_(2k-2) = l_(2k) = 0`),
the junction at `k = n` checked against `W`'s last symbol and `W`'s interior not checked, as
in `seam_history_inheritance.admissible`. The forced symbols are the seed's own `e_(n+j)`.
Check `R1` (line 18): all 4,092 `(W, c)` with `n <= 10`, three computations agree in count and
in forced word: `seam_history_inheritance.run`; the forward forced-pair run
(`dictionary.py` `forward_forced_run`, choosing `(l_(2k), l_(2k+1))` by the pair on the
anti-diagonal with no kernel call); and the survival count of `seed(W)` evolved forward from
its time-0 row. Maximum run 8. The deepest runs `D_n(c)` reproduce the archive: hard-core
sources match `RESULTS-EVENTUAL-CONSTANT-TAIL.md` section 8, table after (9), for
`n = 1..19` (`R0a`, `R0c`, lines 31, 34; values lines 21 to 30, 33); all binary sources
match `seam_history_inheritance.controls()` for `n = 7..10` (`R0b`, line 32). The two tables
differ from `n = 5` on because the control table admits sources containing `11`.

**I9 (sources are seeds).** `[C]` At scale `n`, the binary sources of length `n` are in
bijection with the width-`w` seeds having `cut_0 = c` (and leading `11` for `c = 3`),
`2^n` of them, and the hard-core sources with those whose `rho` prefix has no `11`,
`F(n+2)` of them (`Q2`, line 55; counts per width on lines 38 to 51, "direct wide / hc").

**I10 (census reconciliation).** `[C]` For every seed `s` of width `w = 5..18`, all
`2^(w-1)` seeds, `n = floor((w-3)/2)`, `c = 2` for odd `w` and `3` for even `w`:

- `survived(s)`, the census count, is `S_0^L1(s)`, the consecutive `k >= 0` with the pin
  only; `M(w) = max survived` reproduces `forward_boundary_census_w2-18.log` at every width
  and the halving `N_w(k) = 2^(w-2-k)` holds for `k <= n` (`Q5`, line 58).
- `cut_0` computed forward (row `-1` from the time-0 row) equals `T[n][n]` of the seed's
  `e_0..e_n` on every seed whose pins `k < n` hold (`Q1`, line 53), and fails on some seeds
  with a broken pin (`Q1b`, line 54), as I3 says.
- Direct: `run_c(e_0..e_(n-1)) = S_n(s)` on every seed with pins `k < n`, `cut_0 = c`, leading
  `11` if `c = 3` (both grammars, forced word included), and for hard-core `W` also
  `S_0(s) = n + run` (`Q3`, line 56).
- Shifted: `run_c(e_1..e_(n+1)) = S_(n+2)(s)` on every seed with pins `k <= n+1`, no `cut_0`
  condition (`Q3`): the seed's row at time 2 has width `w + 2` and its row at time 1 is
  finite with a `11` edge, so the shifted configuration has `cut_0 = c` at scale `n + 1`
  automatically.
- Sandwich: `n + D_n^hc(c) <= M_HC^(11)(w) <= M_HC(w) <= n + 2 + D_(n+1)^hc(c)`, where
  `M_HC = max S_0` over all seeds and `M_HC^(11)` over the seeds with the leading edge of
  `c`; and `n + D_n^wide(c) <= M_J(w) <= n + 2 + D_(n+1)^wide(c)` with `M_J = max (n + S_n)`
  over seeds with pins `k < n`; both lower bounds attained (`Q4`, line 57; table lines 60 to 73).
- `[R]` `[C]` Against the sibling hard-core census to width 40
  (`forward_survivor_plateau_w2-40.log`, Table 2, `M_hc` in the survivor convention, one
  condition fewer than `M_HC` here, verified equal after the offset at `w = 12..18` where both
  exist, `Q7`, line 105): `n + D_n^hc(c) <= M_hc(w) + 1 <= n + 2 + D_(n+1)^hc(c)` at all 29
  widths `12..40` (`Q6`, lines 75 to 104). The lower bound is attained at
  `w = 12, 18, 19, 22, 23, 24, 27, 28, 31, 35, 37, 39, 40`, the upper at
  `w = 14, 16, 17, 20, 22, 24, 26, 30, 32, 34, 36, 39`, both at `w = 22, 24, 39`. `D_n^hc`
  here is this script's own (lines 21 to 33); `M_hc` is inherited.

The unfiltered maximum. The census argmax seed has a `rho` word containing `11` at
`w = 10, 11, 12, 13, 14, 15, 17, 18` (lines 43 to 51; the `e` word and the position of the
`11` are printed). At `w = 12`: `M = 14`, `M_HC = 6`, `free = 9`, `free_HC = 1` (line 45,
seed `110100010101`, `e = 222121121121210`, `11` at `k = 6`). At `w = 13`, of the 22 seeds
surviving 7 or more conditions, 15 contain `11` (`seeds_w5-14.tsv`, columns `survived_L1`,
`S0`).

## 3. Reading

The two forms are one configuration. The endpoint form is the pinned half-plane read along
diagonals `t - i = 2u + 1` (one per endpoint symbol, two time steps each) and anti-diagonals
`t + i = -(2d + 3)` (one per depth), with each four-state cell packing a horizontal pair. The
carry transducer of `RESULTS-CARRY.md` is Rule 30 itself acting on a pair given its right
neighbour pair, and the triangle recurrence is left-permutivity. Nothing in the endpoint
form is reconstructed, quotiented or encoded: `H` is a cell, `Lo` is the cell to its left,
`E = 1 + H + Lo` is the parity of a horizontal pair, the `(H, E)` Moore transducer of the psi
doc is left-permutivity written column by column, and the `D8` of `RESULTS-CARRY.md` is the
group generated by the Rule 30 step on a pair for the four values of its right-neighbour
pair (the rows of `FORWARD`). That is consistent with the capsule's killed rows: a bounded
quotient of the anti-diagonal is a bounded quotient of a line of cells of a Rule 30
configuration.

What each statistic measures. `survived(s)` counts even times at which column `-1` obeys
the pin, for an arbitrary finite seed. `run_c(W)` counts the same event from `k = n` on,
adds the hard-core junction that the right half imposes, and is defined only on seeds with
`cut_0 = c`, a finite row at `t = -1` with the leading edge of `c` (the `j = 0` cut,
invisible to the census; for `c = 3` the leading-`10` seeds also have a finite row `-1` and
are not seen). The junction term of `S_m` is exempt at `k = 0`, as in the census's `S_0`. The archive's
`(RW)` condition `P^n(I(f)) = c^(n+r+2)` therefore says: `f` is a finite seed of width
`2n+3` or `2n+4` with a finite preimage row, whose column `-1` keeps the pin and the
hard-core junction for `n + r + 2` more even steps. The forward census's `free(w)` is
`M(w) - (n + 1)` in this document's convention (the sibling documents count one fewer).

Transfer. A bound `D_n^hc(c) <= B(n)` for all `n` gives `M_HC(w) <= n + 2 + B(n+1)`, i.e.
`free_HC(w) <= B(n+1) + 1`, and a bound `free_HC(w) <= B'(w)` gives
`D_n^hc(c) <= B'(2n+3) + 1` (`c = 2`) or `B'(2n+4) + 1` (`c = 3`). A bound on the unfiltered
`free(w)` transfers downward to `D` (since `M_HC <= M`), but no bound on `D` transfers up to
`free(w)`: at `w = 12`, `free = 9` while `D_4^hc(3) = D_5^hc(3) = 2`, and the sibling census
records `free(w)` up to 18 at `w = 39` against `free_hc` at most 8 on `w <= 40`
(`RESULTS-FORWARD-SURVIVOR-W40.md` Table 2, inherited). The seeds responsible have `11` in
`rho` and cannot be the left half of a pinned configuration, so the forward programme's
statistic is `M_HC`, not `M`, and `M_HC` is the archive's `D` up to one scale and two steps.
The scale lemma's target `run_c(W) < 2|W|` at every scale
(`RESULTS-EVENTUAL-CONSTANT-TAIL.md` section 8) reads, through the sandwich, as
`M_HC(w) <= 3n + 3`, about `1.5 w`. The census sits well inside it: `M_HC(w)` is `w - 7` to
`w - 4` on `w = 12..18` (lines 45 to 51) and `M_hc(w) + 1` is `w - 13` to `w - 2` on
`w = 19..40` (lines 82 to 103, inherited), i.e. a hard-core seed loses the pin or the
junction within a bounded number of even steps after the seed has arrived on this range.
Nothing here proves either statement.

The two grammars. `seam_history_inheritance`'s wide grammar admits sources containing `11`,
which are seeds the right half excludes; its `D^wide` exceeds `D^hc` at `n = 5, 6, 8, 9, 10`
and equals it at `n = 7` (lines 25 to 30). The `[K]` rows of the capsule built on `D^wide` are unaffected (a kill on a larger
set is a kill), but any positive bound should be stated on `D^hc`.

## 4. Scope

`[U]`: I1 (derivation), I2, I3, I5, I6, I7 (from the `CONE` table), the two sandwiches
(from I8 and the shift). `[C]`: I1 on binary endpoints to length 10 and four-state endpoints
to length 7; I4 and I5 to length 8; I7 on endpoints to length 9; I8 on all binary `W` to
`n = 10`; I9, I10 on all seeds to `w = 18`; `D_n^hc` to `n = 19`; the width-40 sandwich uses
inherited `M_hc` `[R]`. Not done: the identity for symbols `0`, `3` (there is none, I3); a
hard-core census beyond `w = 18` of this script's own (the sibling census to 40 is read, not
rerun); any statement about `(PT2)`, `(PSI)`, `(RW)`, `BWH+`, or the growth of `D`. The
alternating family and the charge inequality were not translated; both are statements
about specific seeds and translate cell by cell through I1 and I8 without new content.
No mechanism from `PROOF-STATE-CAPSULE.md` section 5 is renamed or retried.

## 5. Reproduction

From `experiments/rule30/p1-period2-invariant`:

```sh
uv run --no-project --with numpy python forward-boundary/dictionary/dictionary.py    # 11 s, exit 0
```

Writes `forward-boundary/dictionary/seeds_w5-14.tsv`; reads
`forward-boundary/forward_boundary_census_w2-18.log` and
`forward-boundary/forward_survivor_plateau_w2-40.log`. The log cited above is
`forward-boundary/dictionary/dictionary.log`.

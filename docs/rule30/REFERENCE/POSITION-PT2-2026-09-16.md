# Position paper: the period-two rung of Rule 30's centre-column problem

Date: 2026-09-16. The deliverable named by the stop rule of
`experiments/rule30/p1-period2-invariant/NEXT-SESSION-PROMPT-20260916.md` ("STOP RULE").
Labels are those of `PROOF-STATE-CAPSULE.md` ("Evidence labels"): `U` a uniform all-length
proof or identity, `C` a finite exact certificate or exhaustive census, `K` an exact
counterexample killing a stated mechanism. Paths are relative to
`experiments/rule30/p1-period2-invariant/` unless they begin with `docs/rule30/`.

## 1. The question

Rule 30 is the binary one-dimensional cellular automaton
`s(t+1,i) = s(t,i-1) XOR (s(t,i) OR s(t,i+1))`, left-permutive
(`NEXT-SESSION-PROMPT-20260916.md`, "(PT2) IN PLAIN FORM"). P1 asks whether the centre column
grown from a single live cell is ever eventually periodic; P2 whether its limiting density is
1/2; P3 whether the n-th centre cell needs `Omega(n)` work. All three are open, and neither
P2 nor P3 has an accessible sub-question (`docs/rule30/START-HERE.md`, "Current status";
`NEXT-SESSION-PROMPT-20260916.md`, "THE THREE QUESTIONS").

The program attacks P1 through one rung. With `Tr_0(y)` the centre column of `y` and `F` the
global map, the target is

```text
(PT2)   Tr_0(y) != Tr_0(F^2 y) for every nonzero finite y
```

(`PROOF-STATE-CAPSULE.md` section 1): no finite configuration has a centre column of period
two. It excludes period two only, not P1 (`PROOF-STATE-CAPSULE.md` section 1), and is the
only rung found accessible (`NEXT-SESSION-PROMPT-20260916.md`, "THE THREE QUESTIONS").

Constant centres are already excluded: the zero tail in `docs/rule30/RESULTS-zero-tail.md`,
the one tail in `docs/rule30/RESULTS-eventual-period.md` and `RESULTS-inverse-trace.md`
(`docs/rule30/START-HERE.md`, "Current status"); in print, no column of a nonzero finite
Rule 30 orbit is eventually constant (Condrey, arXiv:2609.09431, 2026). The two-column
theorem it rests on is older: with a finite (Jen) or merely left-finite (Kopra) initial
condition, two adjacent columns cannot both be eventually periodic (E. Jen, "Aperiodicity in
one-dimensional cellular automata", Physica D 45 (1990) 3-18, Proposition 3; J. Kopra,
"Rapid left expansivity, a commonality between Wolfram's Rule 30 and powers of p/q", TCS 946
(2023) 113668, Theorem 3.5 with width 2). The single-column statement for the single-cell
seed is posed as open there (Kopra 2023, Problem 3.10), and no Rule 30 prize has been awarded
(rule30prize.org, checked 2026-09-17). Of
the two alternating phases one shifts by a step into the other, so period two is the single
case `s(t,0) = t mod 2` (`PROOF-STATE-CAPSULE.md` section 1).

## 2. The two-sided reduction

Pin the centre: `s(t,0) = t mod 2` for all `t`. Under the pin the left half-line `i <= -1`
and the right half-line `i >= 1` are each autonomous given the boundary, and (PT2) says no
finite configuration keeps the pin forever (`NEXT-SESSION-PROMPT-20260916.md`, "(PT2) IN
PLAIN FORM"; `PROOF-STATE-CAPSULE.md` section 2). The rule at the centre forces column `-1`:
`l_t := s(t,-1) = 1` at odd `t`, and `l_(2k) = 1 - rho_k` where `rho_k := s(2k,1)`
(`RESULTS-RIGHT-SEED-MARGIN.md` section 1).

Left side, `U` (`RESULTS-FORWARD-HALVING-LEMMA.md`, abstract). Write `x_m = s(0,-m)` for the
left seed and `C_k = s(2k,-2) XOR s(2k,-1)` for the period-two condition (L1) at even step
`k`. Then `C_k` depends on `x_1..x_(2k+2)` alone and is affine with coefficient 1 in the
newest bit, `C_k = x_(2k+2) XOR G_k(x_1..x_(2k+1))`. So while the seed is still arriving each
pin condition consumes exactly one seed bit, the partial seeds on `-(2k+2)..-1` satisfying
`C_0 = ... = C_k = 1` number exactly `2^(k+1)`, and they are in bijection, through a
triangular map with unit diagonal, with the `2^(k+1)` words `(rho_0..rho_k)`. Every `rho`
prefix is left-realizable; the left imposes nothing until its seed is exhausted
(`NEXT-SESSION-PROMPT-20260916.md`, "(PT2) IN PLAIN FORM").

Right side. The right half-line is driven by the boundary `0101...` and is not permutive in
the direction that matters: the trace `rho(y)` is many-to-one in the right seed `y` (31,779
distinct traces to `k = 2048` from the `2^16` width-16 seeds, `RESULTS-RIGHT-SEED-MARGIN.md`,
abstract), and the language `R` of realizable trace words is thin: `11` and `00000` are
forbidden, there are 4,189 minimal forbidden factors through length 60, and
`|R_60| = 103,220` (`RESULTS-R-STRUCTURE.md` section 1).

Prefix lemma, `U` (`RESULTS-RIGHT-SEED-MARGIN.md` section 1). For a finite right seed `y` let
`xhat(y)` be the left row reconstructed by left-permutivity from `rho(y)`: `col_0[t] = t mod
2`, `col_1 = l`, `col_(m+1)[t] = col_m[t+1] XOR (col_m[t] OR col_(m-1)[t])`,
`xhat_m(y) = col_m[0]`. For a finite left row `W` (`W_m = s(0,-m)`) evolved with `y` by plain
Rule 30 and no boundary, the centre equals `t mod 2` exactly for
`t < m*(W,y) = min{m : W_m != xhat_m(y)}`. Proof by induction on `T`: if the pin holds through
`T-1`, each half-line has seen only the pin as its neighbour, so `s(T-1,1)` and `s(T-1,-1)`
are the driven values; the pin at `T` needs `s(T-1,-1) = l_(T-1)`; by Lemma 2 of
`RESULTS-FORWARD-HALVING-LEMMA.md`, `s(T-1,-1) = W_T XOR g(W_1..W_(T-1))` and the
reconstruction satisfies `l_(T-1) = xhat_T XOR g(xhat_1..xhat_(T-1))` with the same `g`, so
given `W_m = xhat_m` for `m < T` the pin holds at `T` iff `W_T = xhat_T`.

Hence the pin holds forever iff `W = xhat(y)`, so (PT2) at period two is "`xhat(y)` has
infinite support for every finite `y`"; equivalently, no finite right seed has a trace equal,
symbol for symbol, to the demand sequence `1 - l_(2k)` of a finite left seed
(`RESULTS-RIGHT-SEED-MARGIN.md` sections 1 and 7). The pin survival of every finite
configuration is one zero run of one row, computable by simulation alone.

## 3. The dictionary

The archive's earlier machinery (the endpoint triangle `T`, the `D8` carry action, constant
cuts, Peel rank, the inverse queue) was built as if it saw more than the half-plane. It does
not (`U` and `C`, `RESULTS-FORWARD-ENDPOINT-DICTIONARY.md`, abstract, identities I1 to I10):
`T[u][d] = 2 x(t,i) + x(t,i-1)` at `(t,i) = (u-d-1, -(u+d+2))` is the pinned left half-plane
in one affine chart, because the carry action is one Rule 30 step (I1); the endpoint symbol
is `e_u = (1 - rho_u, rho_u)` (I2); the H-forcing pins one cell to 1 on the anti-diagonal
`t + i = -(2n+3)`; "constant cut `c` at
depth `n`" is exactly a finite time-0 row of width `2n+3` (`c = 2`) or `2n+4` with leading
`11` (`c = 3`); and `run_c(W) = S_n(seed(W))`, the count of consecutive even steps from
`k = n` keeping the pin and the hard-core junction. Hence
`n + D_n^hc(c) <= M_HC(w) <= n + 2 + D_(n+1)^hc(c)`, `w = 2n+3` or `2n+4`, checked to
`w = 40`: the constant-cut run and the forward hard-core free phase are one statistic up to
one scale and two steps (`PROOF-STATE-CAPSULE.md` section 2). The endpoint machinery adds no
structure to plain Rule 30, and the earlier separator target
`O_c intersect I(HC_omega) = empty` (`PROOF-STATE-CAPSULE.md` section 1;
`DRAFT-PUBLIC-QUESTION.md`) is (PT2) read in that chart.

## 4. What is proved

(a) Eventually periodic traces are safe, `U` (`RESULTS-RIGHT-SEED-MARGIN.md` section 7).
If `rho(y)` is eventually periodic then no finite left row keeps the pin against `y`. Proof:
suppose `(W, 0, y)` keeps the pin forever, `W` nonzero (the zero row has `s(2,0) = 1`).
Column `-1` is `l_t` with `l_(2k) = 1 - rho_k` and `l_odd = 1`, so if `rho` has period `p`
from index `k_0` then `l` has the even period `P = 2p` from `t_0 = 2k_0`, and column 0 has
period 2, which divides `P`. By left-permutivity `s(t,-m-1) = s(t+1,-m) XOR (s(t,-m) OR s(t,-m+1))`, so if
columns `-m+1` and `-m` are `P`-periodic for `t >= t_0` then so is column `-m-1`, for the same
`t_0`; by induction every left column is `P`-periodic for `t >= t_0`. But `W` is finite with
leftmost 1 at `-w_L`, and Rule 30 moves the left edge one cell per step
(`0 XOR (0 OR 1) = 1`), so `s(t,-m) = 0` for `t < m - w_L` and `s(m - w_L, -m) = 1`; for
`m >= w_L + t_0 + P` the times `m - w_L - P` and `m - w_L` are both at least `t_0`, congruent
mod `P`, and carry different values. Contradiction. This is the argument of Jen 1990
(Proposition 3) and Kopra 2023 (Theorem 3.5, width 2) for two adjacent eventually periodic
columns, applied to the pin and its forced neighbour; as in Kopra it needs only a left-finite
`W`. So a
counterexample to (PT2) needs a right seed whose trace never settles.

(b) Robust-shield certificate, `C` (`RESULTS-RIGHT-SEED-MARGIN.md` section 7). Column `j`
reads column `j+1` only through the OR, when column `j` is 0, so a near-wall time-periodic
block can be impervious to the exterior. Treating column `J+1` as an adversarial input, a
reachability search over `(t mod L, columns 1..J)` over-approximates every trajectory; if it
closes with columns `1..j*` fixed at the observed pattern, the pattern holds for all `t`. Of
the 649 width-16 seeds whose trace to `k = 2048` is periodic from `k = 0` (475 of period 2,
5 of period 5, 169 of period 7), the search closes for 377, all of period 2, at `J = 20..28`
with shields `j* = 6` (116 seeds) or `j* = 8..17` (261 seeds); `rho` is then `(01)^omega` or
`(10)^omega` for all time and (PT2) holds by (a). The other 272 are inconclusive. The merged
reachable sets are eleven traps (closed under every exterior input, re-checked state by
state); 1,895 of the 65,536 width-16 seeds enter one by `t = 147` and none later to
`t = 4096`, so (PT2) holds exactly for 1,895 seeds (`RESULTS-RIGHT-SEED-MARGIN.md` section
7). The two lemmas of (a) and the prefix lemma passed an adversarial referee
(`crosscheck/verify-0916/margin/REFEREE.md`). These are the first proved eventually periodic
traces of finite seeds, so `R` contains infinite periodic traces.

(c) (PSI) on the alternating family, `U` over `C` (`RESULTS-PSI-ALTERNATING-PROOF.md`,
abstract and section 6; `PROOF-STATE-CAPSULE.md` sections 2 and 4). (PSI), the statement
that the forced defect word `Psi_n(W)` of a binary source `W` is neither `0^(n+2)` nor
`1^(n+2)`, is the endpoint form of a horizon statement stronger than (PT2). For
`W = (12)^k` the endpoint state is one period-28 sequence
`D = 2120030303000312031112300323` indexed by `2k + d`, proved for every `k >= 2` by an
induction whose step is finitely many state returns of a lockstep transducer, and the
leading constant stretch of the forced cut satisfies `k_E(2) <= 3`, `k_E(3) <= 6` for every
`k >= 2`, against the `n + 2 = 2k + 2` a failure needs. The pre-registered `k_E <= 5` is
false, `K`: at `k = 144`, `k_E(3) = 6` exactly.

(d) The `2^18` Nerode bound, `U` over `C` (`RESULTS-ONES-NONREGULARITY.md`, abstract;
`PROOF-STATE-CAPSULE.md` section 4). For the run language `L_1(c)` of that document and
every level `a = 4..17`, an explicit suffix `A[a]` of length `a` satisfies
`f_c(m + 2^a) != f_c(m)` for all `m >= 0` and both `c`. Hence every pair
`m != m' (mod 2^18)` is separated and any DFA for `L_1(c)` has at least 262,144 states.
Non-regularity itself is open (`RESULTS-ONES-NONREGULARITY.md` 2.8, gap G1/G2).

(e) Entropy of the trace language, `C` (`RESULTS-R-STRUCTURE.md` section 4).
`h(R) <= log2 lambda_60 = 0.124` bits per symbol, `R` being contained in the shift of finite
type avoiding its 4,189 minimal forbidden factors through length 60 (Collatz-Wielandt upper
bound equal to the power-iteration estimate; the bound through `L = 2` is the golden mean
`0.6942`, and it decreases strictly over `L = 2, 5, 13, 30, 48, 60`).

(f) Exact identities, `U`. `rho_(k+1) = 1` iff `s(2k, 1..3) = 000`, which re-proves `11`
forbidden (`RESULTS-R-STRUCTURE.md` section 1); the real trace avoids `11` and `00000`
(`PROOF-STATE-CAPSULE.md` section 4, "Actual-right constraints"). Diagonals at distance `d`
from a finite configuration's left edge obey the reset chain
`D_d(t+1) = D_(d-2)(t) XOR (D_(d-1)(t) OR D_d(t))`, eventually periodic with first periods
2, 4, 8, 16 at depths 3, 8, 29, 400; diagonals at distance `j` from the right edge obey the
pure toggle chain `E_j(t+1) = E_j(t) XOR (E_(j-1)(t) OR E_(j-2)(t))`
(`PROOF-STATE-CAPSULE.md` section 5, penultimate row, citing `RESULTS-DIAGONAL-TRANSIENTS.md`).

## 5. What is measured

Margin census, `C` (`RESULTS-RIGHT-SEED-MARGIN.md` sections 3 to 6). Over all `2^16` right
seeds of width 16 and `M = 4096` reconstructed cells, the longest zero run of `xhat` is 26
against the pre-registered bound 32; its distribution (median 11, p99 17, max 26) is that of
three nulls of the same size (fair coin, hard-core, random no-`11`-no-`00000` traces: max 28,
29, 27), the fair-coin longest-run law. The longest tail run is 17. The 45 deepest run
events sit in 28 distinct windows, every one a factor of `(00001)^*` with one displaced 1;
over the 31,779 distinct traces the fraction of positions inside period-5 stretches of four
or more periods has mean 0.969. The driven vacuum is the exception: its trace is period 7
(`1010000`) for `k = 2..154`, then irregular with no eventual period to `k = 65536`, and 1
of 60 random right seeds of width at most 12 was eventually periodic
(`NEXT-SESSION-PROMPT-20260916.md`, "STOP RULE"; `RESULTS-RIGHT-SEED-MARGIN.md` section 6).
The prompt's stop rule calls the right half chaotic; `RESULTS-RIGHT-SEED-MARGIN.md` section
8, written later the same day, says that is wrong for width 16 and `t <= 4096`: the trace is
a period-5 word with sparse defects, and what is chaotic is the timing and shape of the
defects.

Under the shifted dictionary identity I10 the prefix-lemma value is a lower bound on the
joint run below at all 56 `(n, c)` cells, `n = 13..40`, equal at 14
(`RESULTS-RIGHT-SEED-MARGIN.md` section 5).

Joint run, `C` (`RESULTS-REALIZABLE-RUN.md`, abstract and section 7). With both the source and
its forced continuation confined to `R`, the constant-cut run is 3 to 7 at every
`n = 13..41` (7 only at `(32, 2)` and `(40, 3)`) and at most 10 through `n = 46` on supersets,
against the need `n + 2` of the rotated-wedge statement RW; the independence null
`log2 |R_n| / (2 - h)` runs from 4.5 at `n = 13` to 7.6 at `n = 41` and the exact maximum
lies between 2.3 below and 0.4 above it; 811 of the 856 stored deepest sources are
unrealizable.

Structure of `R`, `C` (`RESULTS-R-STRUCTURE.md` sections 2 and 3). Follower sets: 21,389 words
of length 44 have 2,631 distinct 16-step follower sets (ratio 0.123); a random factor-closed
language with the same `|R_m|` at every length has 1,788 (ratio 0.084), so the statistic
measures the size profile. Pumping: 267 of the 2,002 minimal forbidden factors of length
35..53 (13.3 percent) stay minimal forbidden when a square `vv` of a period block (`01`,
`001`, `00001`, `1010000`) becomes `vvv`, against 0 of 241 in the null: a structural signal,
below the pre-registered 50 percent. Growth: `|R_m| / |R_(m-1)|` falls from 1.311 at
`m = 13` to 1.108 at `m = 49` (`RESULTS-R-EXACT-GROWTH.md` line 17) and 1.094 at `m = 60`
(`uc/r1-hardcore/r_exact_sat_m49-60.log`, line `60`); a fit gives 0.040 bits, and 0.04 bits
and zero entropy are inseparable below `m` about 100 (`RESULTS-R-EXACT-GROWTH.md` lines 27
and 35; `RESULTS-R-STRUCTURE.md` section 4).

## 6. What is dead

One row per mechanism class, from `PROOF-STATE-CAPSULE.md` section 5 unless another document
is named. Each is `K` except the `P = 2` mismatch row, which the capsule marks as a
finite-horizon measurement. The capsule's diagnosis of the common cause (section 5, closing
paragraph): a growing ordered dependency diagonal stores phase in long gaps.

| Mechanism | Obstruction | Document |
|---|---|---|
| Fixed-radius additive energy | Farkas contradictions, localities 1 to 4; radius-7 negative cycles | capsule 5 |
| Fixed finite quotient of the frontier | Nerode classes grow 1.77x per symbol; DFA at least 2,255 states | `RESULTS-SOURCE-RESIDUALS.md` |
| Raw dyadic period mismatch | `2^omega` maps to accepted `(12)^omega`; reachability is essential | `RESULTS-REALIZABLE-RUN.md` |
| Bare holonomy-defect word | Identical anchored profiles, different next rows at length 8 | capsule 5 |
| Queue end windows plus total phase | Neutral blocks `00`, `11` differ only in successor actions | capsule 5 |
| Static formula or DFA rank contraction | Survivor DFA grows as `4^(h+1) + 1` | capsule 5 |
| Literal final local patch | Length-12 DLP control survives six constant final cells | capsule 5 |
| One backward source defect | Single-coordinate relaxations stay UNSAT; obstruction global | capsule 5 |
| Count pulls by initial endpoint `12` | Endpoint `22222222` has no `12`, event word `AC` | capsule 5 |
| Count arbitrary-queue pivots | `3001 0^382 2` reaches pull depth 3, `0^390` depth 4 | capsule 5 |
| Pointwise scale derivative or matching | Exact failure first at length 21 | capsule 5 |
| Sharp binary-wedge bound `M_c(n) <= n` | `M_3(15) = 16`, `W = 111122211212112` | capsule 2 |
| Static right-boundary penetration | Structured information reaches `O(log t)` depth; centre is `Theta(t)` away | `docs/rule30/RESULTS-ordered-wedge-glide.md` 3 |
| Larger bounded SAT or GA tables | Falsify candidates; no all-length quantifier | capsule 5 |
| Single-source-flip injection between RW levels | Fresh coin per forced level, coverage `0.4^j` | `RESULTS-FLIP-PAIRING.md` |
| Symbol congruence `CONE[1] = CONE[3]` | True, but a 5.7 percent constant-factor collapse | `RESULTS-COLUMN-DECOMPOSITION.md` 1a |
| Counting RW levels by `F_2` rank | Survivor sets not affine: 420 of 516 classes fail | `RESULTS-COLUMN-DECOMPOSITION.md` 1b |
| Induction on column richness | 99.3 percent of merging parents have identical columns | `RESULTS-COLUMN-DECOMPOSITION.md` 2 |
| Column memory as a rate mechanism | Column not a sufficient statistic; the whole diagonal is | `RESULTS-COLUMN-DECOMPOSITION.md` 10 |
| Conditional block contraction at a prefix state | Rate falls with depth, 1.121 to 0.231, against 1.0 needed | `RESULTS-CONDITIONAL-BLOCK-LOSS.md` 4 |
| Any symbol quotient of the anti-diagonal | All 15 partitions: zero nontrivial full congruences | `RESULTS-DIAGONAL-MEMORY.md` 8 |
| Additive position-indexed weight (Lyapunov) | `t = 0` with Farkas certificates; only direction is diagonal length | `RESULTS-SUBINVARIANT-CERTIFICATE.md` |
| `D`-lines identified with cut tails | Identification proved nowhere; false on control seed `{-8,-1,6}` | `RESULTS-PT2-PANEL-2026-09-15.md` 3 |
| `P = 2` mismatch budget against the zero right row | Mismatches linear, `0.2143 N`; contradiction needs sublogarithmic | `RESULTS-PT2-PANEL-2026-09-15.md` 4 |
| Guarded seam from finite history | Fails on cuts `3333231`, `222213000`; uniform guard is `RW-alpha` at 0 | `RESULTS-RW-GUARDED-SEAM-DESCENT.md` 3 |
| Bounded-degree `F_2` certificate (Nullstellensatz, PC) | Refutation degree equals `w - 2` at every `w = 4..14` | `RESULTS-PT2-PC-DEGREE.md` |
| `F_2`-linearization by the hard-core condition | Affine only to column `-7`; degree 3 from `-15` | `RESULTS-HARDCORE-AFFINE-DEPTH.md` |
| Finite phase across a source defect on `(12)^k` | One inserted `2` breaks the period-28 form for good | `RESULTS-ALTERNATING-FAMILY.md` |
| Demand-orbit transient plus periodic tracking | Pre-period about `2n` exceeds the scale `n` | `RESULTS-DEMAND-TRANSIENT.md` |
| Charge (12) by single-flip token injection | `12212121212121212`, `n = 17`: matching 8, deficit 1 | `RESULTS-CHARGE-INJECTION-TOKENS.md` |
| Step-by-step fresh-token mechanism | Fails at `n = 4` on `1212`; 458 of 2,819 words at `n = 18` | `RESULTS-DEPENDENCY-LAW.md` |
| The (L1)-only free phase as a target | Extremal seeds have `11` in `rho`: `M(12) = 14` against `M_HC(12) = 6` | `RESULTS-FORWARD-ENDPOINT-DICTIONARY.md` I10 |
| Pin on periodic blocks of left-frame diagonals (2026-09-16) | Settling `tau_d = 1.30 d` after crossing at `d`; regular region never holds the centre | `RESULTS-DIAGONAL-TRANSIENTS.md` |
| Right trace as a favourable partner (2026-09-16) | Zero runs fair-coin, max 26 against nulls 27 to 29; windows are period-5 defects | `RESULTS-RIGHT-SEED-MARGIN.md` |

## 7. Where a proof would have to come from

By section 2 a proof of (PT2) is a property separating every demand sequence `1 - l_(2k)` of
a finite left seed from every trace of a finite right seed, and by 4(a) only traces that never
become periodic need separating (`RESULTS-RIGHT-SEED-MARGIN.md` section 7). The left supplies
no such property: its survivors biject with free `rho` prefixes until the seed is exhausted
(`RESULTS-FORWARD-HALVING-LEMMA.md`), and its free phase is a fair-coin zero run under every
trace measure tried, the true traces included (`RESULTS-RIGHT-SEED-MARGIN.md` section 8).
Counting cannot supply it: the joint run sits within 2.3 of the independence null, RW is a
rate statement on a language whose entropy is the open quantity
(`RESULTS-REALIZABLE-RUN.md`, abstract and section 7), and finite tables falsify candidates
without supplying the all-length quantifier (`PROOF-STATE-CAPSULE.md` section 5). The
endpoint machinery cannot supply it because it is plain Rule 30 in a chart
(`RESULTS-FORWARD-ENDPOINT-DICTIONARY.md`); what was tried on that chart is section 6.

The cleanest form of the target is left-only. Under the pin the left half-line never sees
the boundary (at even times it is 0, at odd times the wall cell is 1 and masks it), so a
counterexample's left half is Rule 30 on the half-line with a permanent zero wall
(`RESULTS-RIGHT-SEED-MARGIN.md` section 1, zero-wall lemma). (PT2) therefore follows from:
on the zero-wall half-line, no finite seed has `s(2k+1,-1) = 1` for all `k`; and with the two
proved right-side constraints it suffices that no finite seed has that together with
`s(2k,-4) = 0` at all even times and never five consecutive even times with `s(2k,-1) = 1`.
These are statements about one half-line CA with no reference to the archive's machinery,
and their status is open (the measured `(L1)` free phase grows about `0.4 w`, the hard-core
one is 5 to 8 on widths 30 to 40, both as a fair coin predicts).

The one structural handle found is on the right. Near-wall time-periodic blocks impervious
to the exterior are a proof for all time for 377 seeds (`RESULTS-RIGHT-SEED-MARGIN.md`
section 7); at width 16 the trace spends 96.9 percent of its
positions in the period-5 word `00001`, and the deep zero runs of the reconstructed row are
what one displaced symbol does (section 6 there); 13.3 percent of the minimal forbidden
factors of `R` pump along the same period blocks (`RESULTS-R-STRUCTURE.md` section 3). A
proof in these coordinates says that the defects of a right trace can never be exactly the
row a finite left seed reconstructs to (`RESULTS-RIGHT-SEED-MARGIN.md` section 8). No
mechanism for the defects, the forbidden factors, or the entropy of `R` is on record
(`RESULTS-R-STRUCTURE.md` section 5).

## 8. The question for outside experts

Let `X_R` be the trace subshift of Rule 30's right half-line driven by the boundary `0101...`,
the closure of the even-time column-1 words over all finite seeds: is `X_R` sofic, and is its
entropy zero (proved: at most 0.124 bits per symbol, `11` and `00000` forbidden, 4,189
minimal forbidden factors through length 60; `RESULTS-R-STRUCTURE.md` sections 1 and 4)?
Can the trace of a finite right seed that never becomes periodic equal, symbol for symbol,
the demand sequence `1 - l_(2k)` reconstructed by left-permutivity from a finite left seed,
equivalently, does any finite configuration have a centre column of period two
(`RESULTS-RIGHT-SEED-MARGIN.md` sections 1 and 7)?

`DRAFT-PUBLIC-QUESTION.md` posed the same target as the disjointness
`O_c intersect I(H) = empty` of a four-symbol transducer orbit and an inverse-terminal image
of the hard-core subshift; section 3 makes that the pinned half-plane in a chart, and the two
sentences above replace it. `NEXT-SESSION-PROMPT-20260916.md` names the trace subshift
literature (Cervelle, Formenti and Guillon 2008; Guillon and Richard 2010; Kurka, "IDEA
SEEDS" 2) and names Kari, Kopra, Rowland and Guillon as the people to ask ("IDEA SEEDS" 4).

## 9. Reproduction

From `experiments/rule30/p1-period2-invariant/`; the source section is in the comment.

```sh
uv run --no-project --with numpy python forward-boundary/halving_lemma_check.py 9                                        # RESULTS-FORWARD-HALVING-LEMMA.md 6, 30 s
uv run --no-project --with numpy python forward-boundary/dictionary/dictionary.py                                         # RESULTS-FORWARD-ENDPOINT-DICTIONARY.md 5, exit 0
uv run --no-project --with numpy python forward-boundary/right_seed_margin.py 4096 16 forward-boundary/right_seed_margin.json   # RESULTS-RIGHT-SEED-MARGIN.md 11, 43 s
uv run --no-project --with numpy python forward-boundary/shield_certificate.py 0 28                                       # RESULTS-RIGHT-SEED-MARGIN.md 11, minutes
uv run --no-project --with numpy python r-structure/r_structure.py                                                         # RESULTS-R-STRUCTURE.md 7, about 1 min
uv run --no-project python alternating-family/psi_alternating_proof_depth7.py                                              # RESULTS-PSI-ALTERNATING-PROOF.md 5, exit 0
```

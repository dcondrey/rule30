# Finite rows, all periods: bounded certificate and period-uniform falsifier

Ladder node: `finite_all_periods` (P1), statement

> `Tr_0(y) != Tr_0(F^p y)` for every nonzero finite `y` and every `p>=1`.

## 0. Pre-registration (written 2026-09-18, before any run in this directory)

### Definitions

- `y` ranges over nonzero rows with support in `[-W,W]`; there are `2^(2W+1)-1`.
- `c_t = F^t(y)_0` under Rule 30.
- `a_p(y) = min{t>=0 : c_t != c_(t+p)}`, or infinity. `Tr_0(y)=Tr_0(F^p y)`
  holds exactly when `a_p(y)` is infinite, so a finite `a_p(y)` is a
  one-bit witness that `(y,p)` is not a counterexample, checkable by direct
  simulation to time `a_p(y)+p`.
- `A(W,p) = max_y a_p(y)`. The prior SMT table `H(p,w)` of
  `docs/rule30/RESULTS-other/RESULTS-eventual-period.md` restricts to rows
  whose first `p` centre bits are nonconstant and reports
  `H = max (a_p + p) - 1`; the engine computes that variant too.

### Success criterion (falsifiable by a finite certificate)

**C(W,P,N):** every nonzero `y` with support in `[-W,W]` and every
`1<=p<=P` has `a_p(y)+p <= N`.

C is a finite statement, so an exhaustive run that finds a witness for every
pair proves it for exactly that range. It is falsified by any pair with no
violation through `N`; such a pair is either a candidate counterexample or an
engine defect, and the controls below separate the two. Registered target:
`W<=12`, `P=64`, `N=128`.

C proves nothing past its range. The node's scope note is decisive here:
`y=F^T(delta_0)` has support radius `T`, so no fixed `W` covers the onset
quantifier, and for any fixed `y` the quantifier over all `p` is itself open
(it contains pure periodicity of `Tr_0(delta_0)`). C is a falsifier and a
regression target, not a route to the uniform theorem.

### Hypothesis H2: no resonant period (period-uniform falsifier)

Model: once past the controllable prefix, each equality `c_t=c_(t+p)` is one
fair binary constraint on the `2W+1` free bits of `y`, so no period survives
more constraints than the row has bits.

**H2:** for every `W<=12` and every `1<=p<=64`,
`A(W,p) <= 2W + 1 + 6 + 3 = 2W + 10` (six bits for the union over 64
periods, three bits of slack).

- Kill: any `(W,p)` with `A(W,p) > 2W+10`. A kill names a resonant period,
  one whose same-orbit condition costs Rule 30 less than one bit per step,
  and that period becomes the next attack target ahead of `001`/`011`.
- Strong outcome: `max_p A(W,p) - (2W+1)` bounded by a constant across
  `W=4..12` with no drift in `W`.
- What H2 does not control for: it is a statement about radius `<=12` rows;
  a period whose resonance only appears at larger radius is invisible.

### Controls (each must fire, or the run is void)

1. **Lower bound (proved, see section 2):** `A(W,p) >= W+1-p` for `p<=W`.
   Any table entry below it is an engine defect.
2. **SMT reproduction:** the engine's nonconstant variant must equal the
   prior `H(p,w)` table cell by cell for `w<=8`, `p<=6`, and the SMT probe is
   re-run here rather than cited.
3. **Planted counterexamples in other rules:** Rule 90 with `y={-1,1}`
   (centre zero forever) and at least one rule with a finite row having a
   nonconstant purely periodic centre must come back unresolved. An engine
   that certifies them has manufactured an exclusion.
4. **Independent replay:** every extremal witness is re-simulated with the
   finite-set evaluator `direct_center_trace` in
   `experiments/rule30/eventual_period_probe.py`.

### Addendum H3 (registered after the census, before the left-only run)

The census bounds the right half by `W`. The phase-driven left frontier of
`experiments/rule30/period3_fiber_probe.py` (functions `certify_depth`,
`frontier_step`, `or_parity`) takes an arbitrary word and leaves the right
half unrestricted: at a zero phase `l_t` is free, at a one phase it is pinned
to `1 XOR c_(t+1)`, and after the knee the newly exposed initial-left cell
must be zero. It is a relaxation, so an empty tree is a sound exclusion of
every row with that left depth and any right half, finite or not.

- **Certificate C_left(u,d):** for every primitive nonconstant word `u`
  with `|u|<=8`, every rotation of `u` as the starting phase, and every left
  depth `d<=D`, the tree is empty before cap 512.
- **Scaling prediction:** with one-density `delta(u)`, the pre-knee tree
  has about `2^((1-delta)d)` states and each post-knee one phase is one
  parity check, so the first-empty time should track `d/delta(u)`. Kill:
  any `(u,d)` at the largest tested `d` with first-empty time
  `> 2d/delta(u) + 20`, which would mark `u` as resonant.
- **Controls:** the constant-zero word has no checks and must survive the
  cap; the all-ones word must die (proved in the eventual-period note).
- **Cross-method consistency:** a radius-`W` row has left depth `<=W`, so
  for every rotation `u` with `|u|<=12` the census's per-block maximum
  `a_p` at radius `W` must satisfy `first_empty(u,W) >= a_p + p - 1`.
  A violation means one of the two engines is wrong.

## 1. Results

**STATUS: OPEN.** The ladder statement is not proved and nothing in this
directory moves it off `conjectured`. What changed is that the node now has a
recorded, falsifiable success criterion with bounded certificates, and the
all-periods question has been checked as one object over every period at once
instead of period by period.

### 1.1 Reduction, restated (not new)

The node's statement is equivalent to: **no nonzero finite configuration has
an eventually periodic centre column** (`eee31f363c16716b`; one direction
takes `y=F^T x`, the other takes `x=y`). Shift invariance makes it
equivalent to "no column of any finite seed is eventually periodic", which is
strictly stronger than singleton P1. By rotation it suffices to exclude one
representative per primitive nonconstant necklace `u` (the constant words are
already excluded by the zero-tail and all-one theorems), so the node is the
conjunction over all necklaces of the per-word statements that the `pt2` and
`period3` nodes pose for `01`, `001` and `011`.

The pin identity (`c_t=1` fixes `l_t=1 XOR c_(t+1)`; `c_t=0` leaves `l_t`
free through `r_t`) and the anti-diagonal frontier construction are stated for
an arbitrary prescribed centre trace in
`docs/rule30/RESULTS-other/RESULTS-period3-fiber.md` section 3. That credit
belongs there. The prior code, however, verified the frontier only on `001`
and `011`. `stroboscopic_local_fiber` rejects other words, and every control
iterates over those two. This directory adds the validation for all 470
primitive nonconstant words of length 2 to 8 (section 1.4). That validation
is what makes the all-word census below sound.

### 1.2 Certificate C(W,64,128): proved for the stated range

`all_periods_census.c` (bit-sliced, 64 rows per word) evolves every nonzero
row with support in `[-W,W]` to time 128 and, for each `p<=64`, records the
first violation `a_p(y)`.

**PROVED (exhaustive, finite range only):** for every `W<=16`, every
nonzero row with support in `[-W,W]` (8,589,934,591 rows at `W=16`) and every
`1<=p<=64`, `Tr_0(y) != Tr_0(F^p y)`, with an explicit witness time
`a_p(y)+p <= 128`. No pair is unresolved.

This proves nothing about radius 17 or period 65, and it cannot: the
seed-iterate rows that the ladder needs have radius `T`.

Controls, all passing (`logs/analyze_census.log`, `logs/crosscheck_small.log`):

| control | result |
|---|---|
| proved lower bound `A(W,p) >= W+1-p` | 0 violations |
| SMT table `H(p,w)`, `w<=8`, `p<=6`, re-run with `eventual_period_probe.py` | 40/40 cells equal (`H = A_nonconst + p - 1`) |
| `A(W,1) = W+1` against the sharp constant-trace horizon `w+1` | equal for all `W<=16` |
| independent Python evaluator, every row, rules 30/90/54, `W<=5`, `p<=12` | 0 mismatches in `A`, `A_nonconst`, unresolved counts, witnesses and the first-violation histogram |
| control 4: every extremal witness `A_row`/`A_nonconst_row`, `W<=16`, `p<=64`, replayed with `direct_center_trace` (`replay_extremal.py`, `logs/replay_extremal.log`) | 2,032 witnesses, 0 mismatches; 0 unresolved pairs across all census files |
| planted positives: Rule 90 `{-1,1}`; Rule 54 `{-1}` (period 2), `{-2}` (period 4); Rule 50 `{0,2}` (period 2) | all come back UNRESOLVED; the engine does not manufacture exclusions |

Extremal rows at `W=16`: `p=2` survives longest with
`y={-16,-9,-5,-3,-1,3,10}` (`a_2=24`); overall maximum `a_44=31` for
`y={-16,-13,-11,-9,-5,-4,-2,-1,1,2,3,6,7,9,13}`.

**Radius 17 (run 2026-09-21).** The same program, unchanged and rebuilt
from the committed source, extends C to `W=17`: every nonzero row with
support in `[-17,17]` (34,359,738,367 rows) and every `1<=p<=64` has a
witness with `a_p(y)+p <= 128`, and no pair is unresolved. So C(W,64,128)
is proved for every `W<=17`. The rebuilt binary on 8 threads first
reproduced `census_w12.json` and `blocks_w12.txt` byte for byte. All four
gated controls hold at `W=17`: no lower-bound violation, the SMT table
40/40, `A(17,1)=18`, and 2,159 extremal witnesses replayed with 0
mismatches, 127 of them new. The maximum is `a_53=32` for
`y={-17,-16,-15,-14,-13,-12,-10,-8,-6,-5,-4,-2,0,2,3,5,6,9,10,12,13,14,15}`.
`p=2` gains nothing: its longest survivor is still the radius-16 row above,
at `a_2=24`. Measured cost: 487.86 s real, 2975 CPU-s on 8 threads, 4.4 MB
resident (`logs/census_w17_time.log`). This proves nothing about radius 18
or period 65.

### 1.3 H2 (no resonant period): not killed

`max_p A(W,p)` for `W=1..16`: 9, 11, 11, 15, 15, 18, 20, 21, 24, 25, 30, 30,
30, 30, 30, 31, and 32 at `W=17`. The registered bound `2W+10` is never exceeded (closest
approach `W=11`, at `30 = 2W+8`). From `W=15` on the maximum sits below
`2W+1`, and the gap widens by one per radius: `-1, -2, -3` at `W=15, 16, 17`.
H2 was registered for `W<=12`, so the values past 12 are extensions, not tests. Full `A(W,p)` table: `logs/analyze_census.log`.

Exploratory, not pre-registered (`analyze_decay.py`, `decay_per_period.py`):
the survivor count `S_p(k)=#{y : a_p(y)>=k}` follows the fair-bit law
`2^(2W+1-k)` closely. At `W=16`, the deficit averaged over the periods that still have
survivors stays within 1.5 bits for every `k<=27`; the per-period mean deficit over
`k in [W+2,2W-6]` has median 0.84 bits and ranges from -2.0 (`p=13`) to
+4.0 (`p=22`). The most favourable periods at `W=12` (41, 50, 49) and
`W=16` (13, 8, 61) do not overlap, so no period shows a stable excess of
survivors. Trace entropy is not the explanation for anything here: the
number of distinct centre-trace prefixes from radius `W` rows is within
1.2 bits of `2^(2W+1)` through `W=8` (`logs/trace_entropy.log`).

Reading: within radius 16, Rule 30 charges every period about one bit per
equality `c_t=c_(t+p)`, and no period is cheaper than the others. That is
consistent with the node's statement and says nothing about whether it holds.

### 1.4 Left-only certificate C_left: proved for the stated range

Reusing `certify_depth` from `experiments/rule30/period3_fiber_probe.py`
unchanged, for every primitive nonconstant word `u` of length 2 to 8 (470
words, i.e. every rotation of every necklace), with the right half
**unrestricted**:

**PROVED (exhaustive, finite range only):** no row with left depth `d<=12`
has centre trace `u^infinity` for any such `u`; for `|u|<=4` this holds
through `d<=20`. Every one of the 6,270 trees is empty by time 96. The search
cap was 512 and was never reached.

The relaxation is sound for three reasons. First, columns 0 and -1 determine
the left half triangularly by left permutivity,
`s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1))`: column -2 comes from columns
-1 and 0, column -3 from -2 and -1, and so on. This is `direct_left`. Second,
a one phase pins `l_t`. Third, a zero phase is explored on both values until
the knee, after which only the value that keeps the newly exposed initial cell
zero survives. An empty tree at depth `d` therefore excludes every left word
of depth `d` against every right half. Since the prior code only tested the frontier on `001` and `011`,
`frontier_general_controls.py` re-checks it for the general case: the rotated
identity on all 8 cells; `frontier_left == direct_left` for all 470 words
and 239,700 inputs; and, end to end, 7,800 (real row, period) pairs are never
killed before their matching horizon. That last check is narrow: it covers
only rows of support radius at most 5, periods 2 to 8, and traces matching
the rotation through at least one full period. As a cross-method control, the census
and the frontier agree on all 2,185 shared (word, radius) pairs:
`first_empty(u,W) >= a_p + p`, holding with equality in some cases, so the
bound is tight. Constant-zero survives the cap at every depth and all-ones
dies, as registered.

Scaling prediction `first_empty ~ d/delta(u)`: not killed. At the largest
depth the ratio `first_empty/(d/delta)` lies in `[0.61, 2.14]`. Low-density
words survive longest (`00000001`: 96 at `d=12`), and the census's
per-necklace maxima show the same ordering. Per-necklace table:
`logs/analyze_left_frontier.log`.

### 1.5 What is refuted

Nothing. H2 and the scaling prediction were both registered with kill
conditions, and neither fired.

### 1.6 What is still open

- The node's statement, every period.
- Every single-word case, including `01`, `001` and `011`. C and C_left are
  finite-depth tables, and the frontier grows without bound (period3
  active-core section 3), so no finite table closes a word.
- A period-uniform mechanism. The census shows the obstruction costs about
  one bit per step for every period, which is the behaviour a uniform proof
  would have to explain. It does not supply one.

### 1.7 Ladder change

`finite_all_periods` stays **conjectured**. It gains a recorded success
criterion (C, with H2 and C_left as falsifiers) and its bounded certificates
`W<=17, p<=64` (`W=17` added 2026-09-21) and `|u|<=8, d<=12`. No other ladder statement changes.

## 2. Proof of the lower bound used as control 1

Left permutivity gives `F^t(y)_0 = y_(-t) XOR h_t(y_(-t+1),...,y_t)`, so
for `t<=W` the map from `y` to `(c_0,...,c_W)` is triangular in
`y_0,y_(-1),...,y_(-W)`, which means every prefix of length `W+1` is attained.
Choosing a prefix that is `p`-periodic through index `W`, and not all zero,
gives a nonzero row with `a_p >= W+1-p`.

## 3. Reproduction

From `experiments/rule30/finite-rows-all-periods/`:

```bash
cc -O3 -march=native -o apc all_periods_census.c -lpthread
for w in $(seq 1 16); do ./apc 30 $w 64 128 12 10 data/blocks_w$w.txt > data/census_w$w.json; done
./apc 30 17 64 128 12 8 data/blocks_w17.txt > data/census_w17.json   # about 8 minutes
(cd .. && uv run --with z3-solver python eventual_period_probe.py \
   --max-radius 8 --max-period 6 --search-horizon 32 --json) > smt_reproduction_w8_p6.json
uv run python analyze_census.py            # controls 1-2, C, H2
uv run python replay_extremal.py > logs/replay_extremal.log   # control 4
uv run python crosscheck_small.py <census jsons for rules 30/90/54, W<=5, P=12, N=48>
uv run python left_frontier_census.py 8 12 4 20 > data/left_frontier_p8_d12.jsonl
uv run python analyze_left_frontier.py     # C_left, scaling, cross-method
uv run python frontier_general_controls.py
uv run python analyze_decay.py 16; uv run python decay_per_period.py 16
uv run python trace_entropy.py 8 96
```

`W=16` takes about 2 minutes on 10 threads, and everything else takes seconds
to minutes. `left_frontier_stragglers.py` re-runs six (word, depth) jobs lost
from the first left-frontier run; the constant-zero control stops at depth 17
because its tree has `2^d` states. Spending: $0 in Modal and $0 in paid model
calls.

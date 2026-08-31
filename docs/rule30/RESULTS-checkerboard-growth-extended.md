# Checkerboard patch growth, extended — resolving row 79 / row 8's INCONCLUSIVE

Arm `experiments/overnight-arms/frontier_attack/a25_checkerboard_growth_extended/`.
Successor to `a3_p2_orbit_closure` (row 79, `T=2e6`) and
`a22_p2_checkerboard_growth` (`T=4e6`, verdict INCONCLUSIVE).

**Status: the INCONCLUSIVE is resolved in the growth direction.  All three
fixed-point families are in regime (b), still growing, at
`T = 2^24 = 16,777,216` (4.2x a22's horizon, 8.4x row 79's):
growth rate 0.88–1.03 rows per doubling for both checkerboards and 0.497–0.499
for all-zeros at `W >= 1`, matching the reference per-row cost, with intervals
missing zero by 70 to 350 standard errors; no rate decline in any of 53–78 cells
across 32 disjoint time windows; and the pre-registered saturation signature
(negative curvature) did not fire in a single cell.  The condition attached to
row 8 is NOT discharged — unbounded growth is asymptotic and no finite horizon
proves it.  What changed is that the finite-horizon evidence is now quantitative
instead of a plateau reading, and that a22's "one family flat" is identified as
an artefact: `checker_A` is in fact the family whose maximal diagonal patch
moved from `K = 6` to `K = 7` here, and at `2^23` recurred in 13 of 32 disjoint
windows with the latest at `0.977 T`.

The verdict is horizon-insensitive: the identical direction, with the identical
pre-registered signature not firing, is returned at `T = 4e6` (a22's own
horizon), `2^22`, `2^23` and `2^24`, at both `J = 32` and `J = 64` windows.  What was
missing from a22 was never horizon.  It was the statistic.**

---

## 0. One-paragraph summary

`K(f,T)` — the largest `k` such that the `(2k+1) x k` patch of fixed point `f`
occurs by time `T` — advances by **one unit per eight-fold increase in `T`**.
That is not an observation about this data; it is a3's own reference law
(`2^-(2k+1)` for the first row, `2^-(k-1)` per further row, so `3k <= log2 T`),
and a3 states the same fact in its own words: "reaching `K = 20` for the
checkerboard would need `T ~ 2^60`" — and `3 x 20 = 60`.  a22 moved the horizon
from `2e6` to `4e6`, one doubling, and could not have moved `K` by more than 1
in expectation.  Its INCONCLUSIVE was **forced by the choice of statistic, not
by the horizon**.  In the same data, `K` is flat across 10 or 11 of every 14 dyadic
doublings while growing overall, so observing one flat doubling carries almost
no information.  This arm replaces the extreme-value statistic with an
**occurrence-rate** statistic on the same object, which uses up to `10^6`
occurrences per cell instead of a single maximum and whose precision therefore
improves as `sqrt(T)` rather than `log T`.  Section 6 gives the verdict that
statistic returns at `T = 2^24`.

**Error bars.** Both the count series in `h` (`n_runs(h)` counts runs of length
`>= h`, so the point at `h+1` is a subset of the point at `h`) and the prefix
maxima in `T` are nested samples; an OLS residual standard error on either is
meaningless.  Every interval quoted below is instead a spread **across the 32
disjoint time windows**, each refitted independently.  Observed dispersion is
*below* Poisson (`phi = var/mean < 1`), which is what a deterministic
quasi-random orbit should give; the tests floor `phi` at 1, so they are
conservative.

---

## 1. Reproduction gate (`reproduce.py`) — PASS

Nothing was extended before the prior measurement was reproduced bit-exactly.
Three checks, all PASS:

| check | what | result |
|---|---|---|
| X1 | a22's cached band (`T=4e6`, `wmax=15`) reduced to `wmax=8` vs a3's independently generated band (`T=2e6`, `wmax=8`) | identical over all 2,000,000 rows |
| X2 | fresh regeneration here (`T=200,000`, `wmax=15`) vs a22's cache | array-identical |
| X3 | a22's published table (diagonal `K` at `T=2e6` and `4e6`, per-`W` max heights) recomputed from its own cached band | every cell matches the report and `extend_growth_4000000.json` |

Recovered exactly: `K(all_zeros)` 4 -> 5, `K(checker_A)` 6 -> 6, `K(checker_B)`
5 -> 6 across `2e6 -> 4e6`; heights `all_zeros [20,9,8,7,6,5,4,3,2,1]`,
`checker_A [23,17,16,13,12,9,8,5,4,2,1]`, `checker_B [20,17,14,13,11,10,7,6,2,1]`.

A new C kernel (`band30.c`) was written for the extension and gated the same
way: it is **bit-exact against a3's numpy `_band_series` over all 4,000,000
rows** (`verify_kernel.py`), and its NEON and scalar builds agree bit-for-bit.
Semantics are unchanged from a3 — same internal frame `b_t(i) = s(t, i-t)`,
same update `b <- (b<<2) ^ ((b<<1) | b)`; the only difference is one fused pass
over the live prefix instead of numpy's six separate array passes.

**Scope of that gate, stated plainly:** the cross-implementation check sits at
`T = 4e6`, i.e. at a22's horizon, while every number in sections 5 and 6 comes
from C-kernel output *above* it.  In that regime the only validation is
internal (NEON build vs scalar build, bit-identical).  The independent numpy
regeneration at `T = 8e6` that would have closed this did not finish — see
section 9.

## 2. Cost curve and horizon reached

Generation is `Theta(T^2)` and cannot be made sub-quadratic: Rule 30's light
cone is two-sided, so column 0 at time `T` depends on the initial cells in
`[-T, T]`.

| kernel | `T` | seconds | notes |
|---|---|---|---|
| a3/a22 numpy | 4,000,000 | 740 | a22's `run_4e6.log` |
| a25 C | 1,000,000 | 15.8 | |
| a25 C | 2,000,000 | 54.4 | |
| a25 C | 4,000,000 | 232 | 3.2x the numpy kernel |
| a25 C | 4,194,304 | 402.7 | background, contended |

Fitted constant `2.29e-11 s` per step-squared, one core of an Apple M4.  Clean
quadratic scaling (ratio 3.4–4.3 per doubling).  A NEON build was written and
verified but gave no speed-up: the loop is already memory-bandwidth bound.

**Horizon reported here: `T = 16,777,216 = 2^24`** — 4.2x a22's horizon, 8.4x
row 79's.  Every number in sections 5 and 6 comes from that horizon
(`cache/band30_T33554432.bin.ck16777216`, analysed in `report_T16777216.txt`).
Checkpoint timings: 402.7 s at `2^22`, 1500.7 s at `2^23`, 2664.8 s at
`1.26e7`, 4571.5 s at `2^24`.  It is a **checkpoint of an in-flight
`T = 2^25 = 33,554,432` run**, so a later reader finding other checkpoint files
on disk should note which horizon each section names.  The full quadratic cost
of `2^25` is about 7 core-hours; `2^26` would be 28, `2^27` 114.

## 3. Why the prior arm could not have resolved anything

`K` is integer-valued with expected increment `1/3` per doubling for the
checkerboards (`1/6` for all-zeros, whose per-row cost is `4` not `2`).  From
the reproduced dyadic series:

| family | `K(T)` at `2^10 ... 2^24` | doublings with `dK = 0` |
|---|---|---|
| all_zeros | 3,3,3,3,3,3,3,4,4,4,4,5,5,6,6 | 11 / 14 |
| checker_A | 2,2,2,4,4,4,4,5,6,6,6,6,6,6,7 | 10 / 14 |
| checker_B | 3,3,3,3,3,5,5,5,5,5,5,5,6,7,7 | 11 / 14 |

**A single doubling showing "flat" is the modal outcome under growth.**  a22
observed exactly one doubling.  Its report also read the *earliest* witness time
(`checker_A`'s "witness did not change") as evidence; that quantity lies in the
prefix and can never change under horizon extension, so it is vacuous as
evidence about recurrence.  `Y`-membership is a statement about *arbitrarily
large* occurrence times, so the latest occurrence is the informative one, and
a3's `recurrence.py` had that instrument (`late`, `last`) before a22 dropped it
for the max.

And a22's framing of "one flat, two growing" as a net wash is a logical error
independent of the statistics: the three families are a **disjunction**.  R8's
sufficient target fails if *any* one of them lies in `Y`.  A flat family cannot
offset a growing one.

Finally, the cost of making `K` alone decisive:

| family | `dK`/doubling | doublings to make "no movement at all" improbable (`P<0.05`) | `T` needed | single-core kernel time |
|---|---|---|---|---|
| checker_A / checker_B | 1/3 | 9 | `8.6e9` | ~53 core-years |
| all_zeros | 1/6 | 18 | `4.4e12` | ~1.4e7 core-years |

(from this document's `T = 2^24`, at the fitted `2.29e-11 s` per step-squared.)

Each further unit of `K` costs 8x the horizon and therefore **64x the compute**.
`K` cannot be made decisive by any horizon anyone will run.  That is the
quantified answer to "how much further would you need to go" for the prior
arm's statistic, and it is why this arm changed instrument.

## 4. Method: the rate statistic, and how the band is estimated

Same object as a3/a22 — the centre band `x in [-W, W]` of the lone-seed Rule 30
diagram, `W <= 15`, three vertical-shift fixed-point families (`all_zeros`,
`checker_A`, `checker_B`).  For each `(family, W, h)` the arm records the number
of **maximal runs of length >= h** (a clump-corrected count; a run of length `L`
would otherwise contribute `L-h+1` overlapping starts and inflate any
Poisson-based error bar), the **latest** occurrence start, and the counts in
each of `J = 32` **disjoint** equal-length time windows.

Every band reported is estimated from the orbit's own data across those disjoint
windows — bootstrap over windows for the max statistics, empirical dispersion
`phi = var/mean` for the count statistics, with `phi` floored at the Poisson
value so the test is conservative.  The uniform-Bernoulli law is used as a
**reference scale only, never as a null hypothesis**: a3 explicitly rejected an
ensemble null (Rule 30 on `Z/q` is not surjective, so uniform Bernoulli is not
preserved), and that rejection is inherited here.

Three things were pre-registered as the disconfirming signature, before looking:

1. the late-window rate for some `(W,h)` collapsing toward zero;
2. **downward curvature** in `log2 rate(W,h)` against `h` — the effective
   per-row cost steepening with `h`, which is what saturation looks like before
   it becomes visible in any maximum;
3. the growth rate `-1/slope` falling below the reference `1/log2 f`.

Any of these can fire negative inside the measured range.  That is what makes
this a test rather than a confirmation of the expected answer.

Three estimators of the growth rate are reported, in decreasing precision:

1. **primary — rate slope.** If `rate(W,h) ~ 2^(a*h)` then the maximal height at
   half-width `W` satisfies `h_max = log2(T * c) / |a|`, so the growth rate is
   exactly `-1/a` rows per doubling of `T`.  `a` is fitted per window and the
   interval is the across-window spread.
2. **corroboration — block max.** Group the 32 windows into blocks of `2^m`,
   take the block max, regress its mean on `m`.  Scales with fewer than four
   blocks are dropped: the top scale is a single block, i.e. the prefix max
   itself, which caps the fit.  This estimator is biased **downward** and is
   read as a lower bound.
3. **descriptive only — prefix max vs `log2 T`.** The statistic a3 and a22
   reported.  Nested samples, no valid interval, and it plateaus for many
   doublings at a time by construction; quoted without an error bar.

**Single-column sensitivity (PATH.md section 0.1 filter).**  The statistic
passes.  The band is anchored at column 0 and the patch match reads column 0's
bit at every `W` (at `W = 0` the statistic *is* the centre column's run
structure), so overwriting column 0 of the lone-seed diagram with a periodic
word changes every number in section 5.  a3's column-blind object was `R(W,H)`,
a function of the rule alone with no diagram in it; this is not that.

## 5. Results at `T = 16,777,216 = 2^24`

See `a25_checkerboard_growth_extended/report_T16777216.txt` for the full tables
and `report_T16777216.json` for the machine-readable form.

### 5.1 The diagonal `K` — a3/a22's statistic, extended

| family | `K` at `2^21` | `2^22` | `2^23` | `2^24` | **latest** occurrence of the `K`-patch | windows attaining `K` |
|---|---|---|---|---|---|---|
| all_zeros | 5 | 5 | 6 | 6 | `t = 13,697,639 = 0.816 T` | 2 / 32 |
| checker_A | 6 | 6 | 6 | **7** | `t = 10,432,914 = 0.622 T` | 1 / 32 |
| checker_B | 5 | 6 | 7 | 7 | `t = 15,378,214 = 0.917 T` | 4 / 32 |

`dK` per doubling, block-max lower bound with bootstrap CI over the 32 windows:
all_zeros `+0.309 [+0.134, +0.406]` (reference `1/6`), checker_A
`+0.153 [+0.047, +0.291]` and checker_B `+0.419 [+0.241, +0.509]` (reference
`1/3`).  **Every interval excludes zero.**  `K` is flat across 10 or 11 of 14 dyadic
doublings in every family, which is why a22's single doubling could not speak.

### 5.2 Growth rate from the occurrence rate — the primary estimator

`rows/doubling = -1/slope`, slope fitted independently in each of the 32
windows, interval = across-window spread.

| family | `W` | rows / doubling | reference |
|---|---|---|---|
| all_zeros | 0 | `0.9929 +/- 0.0035` | 1.0 |
| all_zeros | 1..4 | `0.4988 +/- 0.0024`, `0.4984 +/- 0.0031`, `0.4978 +/- 0.0041`, `0.4970 +/- 0.0058` | 0.5 |
| checker_A | 0..4 | `1.0165 +/- 0.0029`, `0.9680 +/- 0.0055`, `1.0139 +/- 0.0070`, `0.9437 +/- 0.0088`, `1.0297 +/- 0.0124` | 1.0 |
| checker_B | 0..4 | `0.9929 +/- 0.0035`, `1.0002 +/- 0.0046`, `0.9311 +/- 0.0052`, `0.9855 +/- 0.0068`, `0.8832 +/- 0.0125` | 1.0 |

Flat would be a growth rate of 0.  The measured rate is 0.92–1.03 rows per
doubling for both checkerboards and 0.497–0.499 for all-zeros at `W >= 1`,
matching the reference per-row cost, with intervals that miss zero by 70 to 350
standard errors.

### 5.3 Rate stability across 32 disjoint windows

| family | cells with `n_runs >= 40` (distinct) | halves `z` range | `z < -3` (decline) | Spearman `z < -3` |
|---|---|---|---|---|
| all_zeros | 53 (25) | `[-1.54, +1.17]` | **0** | **0** |
| checker_A | 78 (50) | `[-1.57, +1.44]` | **0** | **0** |
| checker_B | 78 (57) | `[-2.03, +1.03]` | **0** | **0** |

**No cell in any family shows a rate decline.**  Repeating the whole analysis at
`J = 64` windows instead of 32 (`report_T16777216_J64.txt`, and the same at
`2^23` in `report_T8388608_J64.txt`) leaves every point estimate unchanged and
every conclusion intact: still zero declining cells, still no significant
negative curvature, so the verdict does not depend on the window count.  Cells at constant `W + h` are
exact duplicates (an all-zero or checkerboard region in the lone-seed diagram is
a triangle, so the `(W,h)` and `(W-1,h+1)` counts coincide identically), and
neighbouring `W` overlap further, so the effective number of independent cells is
smaller than the distinct count — which only makes zero declines out of 52–74
easier to obtain by chance, and is why the *sign* pattern matters more than the
count: the halves `z` are centred at `-0.20`, `+0.08` and `-0.55` with spreads
0.61–0.71, i.e. near 0 and nowhere near the `-3` that a declining rate needs.

The deepest cells — the ones with the fewest occurrences, where saturation would
bite first — are still occurring at the end of the horizon: `last_start / T` is
0.93 to 1.00 for every cell with `n_runs >= 40` in all three families.

### 5.4 Curvature — the pre-registered disconfirming signature

| family | `W` | curvature (mean 2nd difference of `log2` rate) | one-sided `3 se` bound on a saturating `delta` | rows the linear law must hold before the growth rate halves |
|---|---|---|---|---|
| all_zeros | 0..4 | `+0.0009 +/- 0.0042`, `+0.0098 +/- 0.0124`, `+0.0111 +/- 0.0154`, `+0.0143 +/- 0.0202`, `+0.0142 +/- 0.0314` | 0.013 – 0.094 | 21 – 80 |
| checker_A | 0..4 | `-0.0023 +/- 0.0046`, `+0.1213 +/- 0.0052`, `-0.0118 +/- 0.0059`, `+0.1968 +/- 0.0082`, `-0.0016 +/- 0.0110` | 0.016 – 0.035 | 28 – 66 |
| checker_B | 0..4 | `+0.0009 +/- 0.0042`, `+0.0026 +/- 0.0044`, `+0.1620 +/- 0.0072`, `+0.0038 +/- 0.0080`, `+0.2604 +/- 0.0185` | 0.013 – 0.056 | 20 – 80 |

**The signature did not fire.  Not one cell shows significant *negative*
curvature** — the direction saturation would take.  Where curvature is
significant it is **positive** (`z` up to `+24`), i.e. the rate falls *more
slowly* than the reference law at larger `h`, the opposite of a per-row cost
that steepens.  The three cells with a small *negative* point estimate
(`checker_A` at `W = 0, 2, 4`) are at `z = -0.49`, `-2.01` and `-0.14`, none
reaching the `-3` threshold, and their neighbours at the same `W` in the other
families are positive.  Under the quadratic saturating form the bound implies
the linear law would have to continue for another 20 to 80 rows before the
growth rate even halved, i.e. to a horizon of at least `T * 2^20`.  That extrapolation is an assumption, not a measurement; the
measurement is the bound on `delta` inside the fitted `h`-range.

## 6. Per-family regime verdict

The task's three regimes: (a) `K` genuinely flattening — saturation; (b) still
growing; (c) fluctuating within a band such that neither can be claimed.  a22
landed in (c) for two of three families.

| family | regime | on what evidence |
|---|---|---|
| **all_zeros** | **(b) still growing** | growth rate `0.4970`–`0.4988 +/- 0.006` rows/doubling at `W=1..4` and `0.9929 +/- 0.0035` at `W=0`; `dK`/doubling `+0.309 [+0.134, +0.406]`; 0 declining cells of 53; no significant negative curvature |
| **checker_A** | **(b) still growing** | growth rate `0.944` to `1.030` rows/doubling across `W=0..4`, all intervals excluding 0 by `>75 se`; `dK`/doubling `+0.153 [+0.047, +0.291]`; 0 declining cells of 78; `K` moved 6 → 7 at this horizon, and the maximal patch at `W=1` (`h=14`, 69 occurrences) still occurs in the final window |
| **checker_B** | **(b) still growing** | growth rate `0.883` to `1.000` rows/doubling across `W=0..4`; `dK`/doubling `+0.419 [+0.241, +0.509]`; 0 declining cells of 78; `K` moved 5 → 6 → 7 across the last three doublings, latest occurrence at `0.917 T` |

**No family is in regime (a) or (c).**  In particular checker_A — the family a22
called "flat" at `K = 6` — moved to `K = 7` here, and at `T = 2^23` its `K = 6`
patch recurred in **13 of 32** disjoint windows with the last of them in the
final window of the horizon.  It was never plateauing.  a22's flat reading came
from the earliest witness time, which cannot move under horizon extension.

The fluctuation bands, quantified rather than eyeballed:

- **`K` at window scale** (32 independent draws, window length `T/32`):
  bootstrap sd 0.33 (all_zeros), 0.48 (checker_A), 0.12 (checker_B), with 95%
  intervals `[5,6]`, `[6,7]`, `[7,7]`.  a22's observed change of 0 over one
  doubling is inside every one of these.
- **`h_max` at window scale**: bootstrap sd 0.20 to 1.05 rows depending on
  `(family, W)`.  a22's reported per-`W` height changes over its doubling were
  0 or 1 row — inside the band at every `W`.
- **occurrence counts**: dispersion `phi = var/mean` has median 1.00 with the
  Poisson floor active, i.e. the raw counts are *under*-dispersed, as a
  deterministic quasi-random orbit should be.  The halves and Spearman tests
  floor `phi` at 1, so they are conservative.

**Did the extension resolve the INCONCLUSIVE?**  Yes, in the growth direction —
but the horizon is not what resolved it.  Going from `4e6` to `2^24` bought at
most one more unit of `K`, exactly as the reference arithmetic predicts.  What
resolved it was replacing a one-maximum extreme-value statistic with a rate
estimated from up to `10^6` occurrences.  Had the rate statistic been run on
a22's own `T = 4e6` band it would have returned the same direction with wider
intervals.  Going `2^23 -> 2^24` moved `K` by one unit in one family and zero in
the other two, exactly as the arithmetic says, while every rate interval simply
tightened.  The arm re-ran it there, same `J = 32` partition
(`report_T4000000_J32.txt`), and it does: rows/doubling `0.4953`–`0.4968 +/-
0.005` for all_zeros at `W = 1..3`, `0.891`–`1.013 +/- 0.02` for checker_A at
`W = 0..4`, `0.916`–`1.003 +/- 0.01` for checker_B at `W = 0..3`; zero declining
cells in all three families; and no negative curvature anywhere.  **The
useful finding is therefore methodological as much as empirical: row 79's
conditional was never going to be settled by horizon, and is not compute-bound.**

## 7. What this can and cannot establish

**It cannot discharge the condition on row 8.**  Unbounded patch growth is an
asymptotic claim.  Every statistic here is computed on a finite prefix, and no
finite prefix can prove that a patch family keeps occurring forever — this is
structurally the same limitation as obstruction H, where a finite check
excludes only periods below the checked range and the theorem's logical form
does the rest.  A clean "still growing at 8x the horizon, with the growth rate
pinned to 1% and flat excluded at many sigma" **strengthens the conditional; it
does not remove the condition.**

**What it does establish** is narrower and worth stating exactly: within the
measured range of `(W,h)`, patch occurrences do not thin out with time, the
per-row cost does not steepen, and the growth rate of the maximal patch height
matches the reference scale to within the quoted error.  The saturation
mechanism that would rescue R8's target — a `(W,H)` occurring at only finitely
many `t` — is not merely unobserved; the rate at which it would have to switch
off is bounded by the curvature measurement.

**What would still change the picture**: a saturating law whose onset lies
beyond the measured `h` range.  Section 5's curvature bound quantifies how far
out that onset can be pushed under a quadratic saturating form, but
extrapolating the bound past the measured range is itself an assumption, not a
measurement.

**Not extended, deliberately.**  a22's defect-propagation probe
(`defect_propagation.py`) is untouched.  a22 filed it correctly: it is a
statement about Rule 30's local behaviour near checkerboard backgrounds, not
about the lone-seed orbit, so it cannot bear on `Y`-membership no matter how far
it is pushed.

## 8. Proposed register changes (PATH.md NOT edited — user decides)

**Row 8** — currently: *"conditional — checkerboard is a proved Rule 30 temporal
fixed point; if in `Y`, R8's target fails. Proved for Rule 90 (Kummer, exact).
For Rule 30, conditional on unbounded patch growth, measured only to `K=6` at
`T=2e6`."*

Proposed: keep **conditional**, and replace the evidence clause with:

> For Rule 30, conditional on unbounded patch growth.  Measured to `T = 2^24`
> (`a25`), 8.4x row 79's horizon, with the diagonal `K` replaced by an
> occurrence-rate statistic: `log2` rate is linear in patch height with slope
> matching the reference per-row cost to sub-percent precision, no rate decline
> in any cell across 32 disjoint time windows, and the deepest measured patches
> still occurring in the final window.  The condition is not discharged —
> unbounded growth is asymptotic and no finite horizon proves it (obstruction H
> in form) — but the finite-horizon evidence for it is now quantitative rather
> than a plateau reading.

**Row 79 / PATH.md section 9.5** — the sentence *"`a22_p2_checkerboard_growth`
extended row 79's horizon 2x and found no rescue (one family's diagonal `K`
flat, two still growing, within the same fluctuation band as before) ... net
INCONCLUSIVE"* should be superseded rather than merely appended to.  Proposed
replacement:

> `a22_p2_checkerboard_growth` extended row 79's horizon 2x and reported one
> family's diagonal `K` flat and two growing, net INCONCLUSIVE.  `a25` reproduced
> that measurement bit-exactly and then showed the INCONCLUSIVE was an artefact
> of the statistic: `K` advances by one unit per 8x in `T` (a3's own reference
> law; a3's "`K=20` needs `T ~ 2^60`" is the same statement), so `K` is flat
> across 10 of every 13 dyadic doublings while growing, and one doubling
> carries almost no information.  Replacing the extreme-value statistic with an
> occurrence-rate statistic on the same band and extending to `T = 2^24`
> resolves the direction for all three families.  `K` itself is shown to be
> undecidable in practice: making it separate from flat needs `T ~ 9e9` and
> about 50 core-years.

## 9. In flight at the time of writing

The `T = 2^25 = 33,554,432` generation was still running when this document was
written, and pipelines are queued against its `2^24` checkpoint and its final
output.  If `report_T33554432.txt` exists in the arm directory it was produced
by that queued run and is **not** reflected here; sections 5 and 6 are `2^24` throughout.  Folding them in is a numeric
refresh of the same tables — the estimators, bands and pre-registered signature
are unchanged — and the direction is not expected to move, since the same
verdict already holds at `T = 4e6` (a22's own horizon), `2^22`, `2^23` and
`2^24`, at both `J = 32` and `J = 64`.  If a later horizon *does* move the direction, that
is the interesting outcome and should be reported as a contradiction of this
document, not as an amendment to it.

One cross-check was also outstanding: the independent numpy regeneration at
`T = 8,000,000` (`gen_band.py`, a3's kernel) against the C kernel's `2^23`
checkpoint, which would be the first independent-implementation validation
*above* a22's horizon.  The bit-exact check in section 1 is at `T = 4e6`, i.e.
at a22's horizon, so a kernel defect that only bites past `4e6` would not have
shown there.  Result, when it lands, goes in `crosscheck_numpy_8e6.txt`; if that
file is absent the check did not complete.

## 10. Files

All in `experiments/overnight-arms/frontier_attack/a25_checkerboard_growth_extended/`.

- `reproduce.py` — the reproduction gate of section 1.
- `band30.c` — the C kernel; `verify_kernel.py` — its bit-exactness gate.
- `gen_band.py` — a3's numpy kernel, used for the independent cross-check.
- `analyze.py` — run-length statistics per `(family, W, h)` and per window.
- `report.py` — bands, trend tests, curvature, distinguishability.
- `pipeline.sh` — `analyze` + `report` for one band file.
- `crosscheck_numpy_8e6.txt` — the independent-implementation check of section 9.
- `analysis_T*.json`, `report_T*.json`, `report_T*.txt` — outputs.
- `cache/band30_T33554432.bin.ck*` — band checkpoints (uint32 per row, bit
  `x+15` = `s(t,x)`).

Nothing outside this directory was written; `a3_p2_orbit_closure/` and
`a22_p2_checkerboard_growth/` files were only read.

# Pre-registration: survivor mass of index 15 at layer 21, and layer 20 without post hoc

Date: 2026-09-19, written before any box past a < 2^15, b < 2^21 has run and
before layer 21 has been computed by anything. Program:
`cap18_mass_census_grid.py`, **unmodified**. Artifact:
`cap18-mass-census-21.json`, beside the committed `cap18-mass-census-20.json`.

    uv run --offline --no-project --with numpy python cap18_mass_census_grid.py \
      --a-exps 15,16 --b-exps 21,22 --band-depths 19,20,21 --workers 6 \
      --output cap18-mass-census-21.json

`--band-depths` is the load-bearing flag and its default is `19,20`. Without it
the run measures nothing new: layer 21's kept fraction divides by mu_20, and
mu_20 enters `measured` only if 20 is itself a band depth, so the chain
19 -> 20 -> 21 has to be asked for. A run that names only 21 and 22 fails the
`exact_through >= min(band_depths)-1` assert, because the committed mass stops
at 18.

The program is not edited, so four of the five predictions below are read by
hand from the artifact's numbers rather than from its verdict fields; section 4
says which field each one comes from.
`build_research_atlas.py:54` verifies the live sha256 of every file named in a
cited artifact's `source_sha256`, and `cap18-mass-census-20.json` names
`cap18_mass_census_grid.py`. Editing the program to move `RECORD_FLOOR` or
`BAND` would make that gate raise `Stale proof artifact dependency` as soon as
the parked record citing that artifact is applied.

## 1. Known before writing

- mu_n for n = 1..16 from the lift and the census agreeing as exact rationals;
  mu_17 = 2513/2^28 and mu_18 = 2513/2^29, forced by the halving lemma and
  confirmed out of sample (`cap18-mass-census.json`).
- mu_19 = 10137/2^32, pre-registered (Y), kept fraction 10137/20104 = 0.5042,
  agreed by all six boxes covering P_19 = 2^14 (`cap18-mass-census-20.json`).
- mu_20 = 20239/2^34, kept fraction 20239/40548 = 0.4991, **post hoc only**.
  The pre-registered verdict at layer 20 was (I): b < 2^19 undersamples there
  and the covering boxes disagreed, a < 2^15 with b < 2^19 giving 5055/2^32
  against 20239/2^34 from the two b ranges that saturate.
- First-star schedule (`cap18-survivor-mass.json`): P_19 = 2^14, P_20 = 2^15,
  P_21 = 2^16, P_22 = 2^17, all four guard-line layers. Depth 23 is a point
  layer, also at period 2^17.
- Every kept fraction computed so far at a guard-line layer: 0.5000 (layer 5),
  0.5236 (13), 0.4955 (14), 0.4947 (15), 0.5042 (19), 0.4991 (20, post hoc).
  Including point layers the range over layers 5-16 is 0.4810 to 0.5862.
- b < 2^19 undersampled depth 20 and b < 2^20 saturated it; the longest body2
  orbit carrying survivors had length 2^n at depths 13-16. So b >= 2^n is the
  expected saturation threshold at depth n, and b < 2^21 is the smallest range
  that can saturate layer 21.
- Record lifetime 36 at the least pair (31051, 1202824), in a < 2^15, b < 2^21,
  replayed independently on the explicit 2467759-symbol word.
- s_n, the share of the depth-n mass on z and rotation columns and the only
  quantity in the lemma's floor mu_(n+1) >= s_n mu_n/2, ran from 0.1765 at
  n = 7 to 0.5000 at n = 5 over n = 5 to 15, and was 0.4089 at n = 15, the
  deepest measured (`cap18-class-flow.json`, exploratory).

## 2. Boxes

Index 15, a nested grid a < 2^15, 2^16 against b < 2^21, 2^22. Four boxes,
2^38 pairs in the largest, about 1.8 hours on six workers at the rate the 2^36
run measured. The step cap stays 96.

A box measures mu_n exactly when 2^i covers P_n and every survivor-carrying
orbit at depth n divides its b range. Both a ranges cover depths 19 and 20;
only a < 2^16 covers depth 21; no box here covers depth 22, which needs
a < 2^17. `covering()` tests the a range against the period only. b saturation
is tested by agreement between the two b ranges and by nothing else, so two
unsaturated b ranges agreeing on a wrong value is possible and is registered
here as such.

Amended 2026-09-19, before the run produced any output. That agreement carries
information only at depth 21. Both b ranges here exceed the b < 2^20 that
already saturated depth 20, so at depths 19 and 20 their agreement is
guaranteed in advance and tests nothing; what P1 and P2 genuinely test there is
the **a** range, since a < 2^16 is new and a < 2^15 with b < 2^21 is one of the
two boxes that produced the post-hoc mu_20 in the first place. Depth 21 is the
only layer in this run where b saturation is live, b < 2^21 being the smallest
range that can saturate it.

## 3. Validation, required before any outcome is read

1. No member reaches the step cap (`censored == 0`).
2. All four boxes give the committed mu_n for every n = 1..18. Every box covers
   P_18 = 2^13 and every orbit through depth 18, so a failure here is a pipeline
   error and not an outcome.
3. Saturation at each band depth: all boxes covering P_n agree at n. A
   disagreement makes that depth (I) and no verdict is read from it.
4. The chain is serial and its failure mode is registered here: depth 21's kept
   fraction divides by `measured[20]`, which this same run sets. If depth 20
   comes back (I), `measured[20]` is never set and depth 21 also reports (I),
   with the reason "depth 20 has no exact mass to divide by". A depth-20
   disagreement therefore costs layer 21 as well, and P3, P4 and the extreme
   case all go unresolved rather than just P2.

## 4. Predictions

The kept fraction at a layer is k_n = mu_n / mu_(n-1).

**P1, layer 19 reproduces under a new a range.** mu_19 = 10137/2^32 in all four
boxes. This is a genuine out-of-sample check: a < 2^16 and b < 2^22 are new, and
the value was measured at a < 2^14 and a < 2^15 against b < 2^19, 2^20, 2^21.
A disagreement means the depth-20 census's layer-19 value depended on its box
rather than on the family, and the parked catalog record
`r30-cap18-index15-mass-census-layers-19-20`
(`experiments/rule30/catalog_cap18_depth20_records.py`) states a wrong mass and
must be amended before anyone applies it.

**P2, layer 20 loses its post hoc mark.** mu_20 = 20239/2^34 with all four
boxes agreeing, giving layer 20 a pre-registered verdict for the first time.
Confirmation promotes the number off post hoc. A disagreement between the
boxes leaves it (I) again; a value other than 20239/2^34 from agreeing boxes
kills the post-hoc number outright, with the same consequence for the parked
record as in P1.

**P3, primary band at layer 21.** k_21 lies in [0.44, 0.54]. This is the band
layers 19 and 20 were judged by, kept unchanged so that all four open
guard-line layers are judged by one criterion chosen before any of them was
computed. The program computes this verdict from its own `BAND`.

**P4, secondary tight band at layer 21.** k_21 lies in [0.49, 0.53]. This is
the span of the five guard-line kept fractions measured past depth 12 (0.4947
to 0.5236) and is a materially riskier claim than P3: three of the six computed
guard-line layers sit within 0.007 of its edges. Read by hand from
`kept_fraction_exact`, since `BAND` carries P3's band. P4 failing while P3
holds is the informative middle case, and it says the guard-line kept fraction
is not as tightly pinned to one half as layers 13-20 suggested.

**P5, the record.** The largest box's record lifetime is at least 37, against
36 in the 2^36 box. Read by hand from `P4_record.max_ell`, because the
artifact's `floor` and `verdict` fields carry the program's `RECORD_FLOOR = 35`
and would report a trivial pass. A record still 36 after four times the pairs
would be the first stall in a sequence that has risen at every doubling since
2^13 and would weaken the evidence for unbounded lifetimes. A record of 37 or
more raises the common-depth certificate floor for index 15 from 37 to at least
38.

- (Y) Confirmed at n: the covering boxes agree and the value is as predicted.
- (K) Kill at n: the covering boxes agree and the value is not.
- (I) Inconclusive at n: the covering boxes disagree.

**Which field each prediction is read from.** Only P3 is the program's own
verdict. P1 and P2 are equality predictions and must be read from the `mu`
field of `P1_P2_kept_fraction_band["19"]` and `["20"]`, never from their
`verdict`, which tests `BAND` and not the value: a kept fraction inside
[0.44, 0.54] sitting on a mu other than 10137/2^32 or 20239/2^34 would print Y
while P1 or P2 is killed. P4 is read from `kept_fraction_exact` and P5 from
`P4_record.max_ell`. So four of the five are read by hand, and the artifact will
show four `verdict` fields that answer only P3 and the layer-19 and layer-20
bands.

**Extreme case.** k_21 = 0 is uniform mortality for index 15 at layer 21,
closing route p1-cap18 for this seam. Nothing in the data makes it expected; it
is stated so the kill is complete.

## 5. Exploratory, reported whatever the verdict

Fractions past depth 21 in every box, marked not-the-mass where P_n exceeds the
a range. The dyadic maxima table over the four boxes and the least record pair
in each. Nothing here is a claim.

With 19 among the band depths the artifact's `P3_half_sample_predicts_k19`
block refires, comparing the old a < 2^13 half-sample estimates against k_19.
That prediction was resolved as a kill by the depth-20 run. Its reappearance is
a recomputation of a settled result, not a fresh prediction, and no verdict is
read from it.

## 6. What this cannot test

Layers 22 and 23 need a < 2^17, four times this run's work, and are not
attempted here; no prediction is registered for them.

The census carries no column classes, so it says nothing about s_n, which is
the whole content of the lemma's lower bound. A kept fraction near one half at
layer 21 is consistent with s_n being anything positive, and with s_n = 0 at
any layer past 15, which is where every available instrument stops: classifying
the depth-n columns needs the cycles saved in layer n+1, whose `old` set they
are, so s_16 needs layer 17, the continuation that hit the transport-cache cap.
Layer 16 itself completed with 673 survivors, so the bound is 15 and not 16.
Neither uniform nor individual mortality is decided by any outcome above.

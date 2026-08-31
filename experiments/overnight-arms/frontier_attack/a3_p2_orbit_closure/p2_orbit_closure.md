# NEGATIVE. Route R8's sufficient target is PROVED FALSE for Rule 90 and empirically refuted for Rule 30; saving it needs a lemma the data contradicts — a uniform-in-`t` forbidden-patch bound, i.e. some `(W,H)` at which the all-zero or checkerboard `(2W+1) x H` band patch never occurs in the lone-seed diagram. No such `(W,H)` exists below the measured frontier (a fully realized `7 x 6` window, `T = 2 x 10^6`, `K = 6`), and the measured patch heights match the exact uniform-Bernoulli prediction to within one row at 23 of 27 cells, so nothing in the diagram suppresses them.

Route R8, prize Problem 2. Arm `a3_p2_orbit_closure`. Compute horizon `T = 2,000,000`
rows of the full spacetime diagram (not just the centre column). All scripts and
JSON outputs are in this directory. Nothing outside it was modified.

---

## 0. What was asked, and the correction that was applied

`Y` is the closure of the VERTICAL (time) shifts of the lone-seed Rule 30
spacetime diagram in `{0,1}^{Z^2}`. The spatial anchor is fixed at column 0; only
time shifts are taken. So `z in Y` iff for every half-width `W` and height `H`
the `(2W+1) x H` patch of `z` at columns `[-W,W]` occurs in the lone-seed diagram
at arbitrarily large times. R8's sufficient target is: *every vertical-shift-invariant
measure on `Y` assigns the centre cell density 1/2.*

The brief's own method correction was followed: 2D window recurrence, not a 1D
column statistic. The further sharpening actually run here is that the target is
decided by **which vertical-shift-fixed points lie in `Y`**, because those carry
Dirac invariant measures whose centre density is 0 or 1 by inspection. Register
row 47 already names them as the proved obstruction to invariance-only arguments;
R8 is the proposed repair, and this arm asks whether the repair can work.

`fixed_point_check()` in `band_census.py` verifies exactly, on a width-131 window:

| configuration | Rule 30 fixed | Rule 90 fixed | centre density |
|---|---|---|---|
| all zeros | yes | yes | 0 |
| checkerboard A (`s(t,x)=1` iff `x` even) | **yes** | no | 1 |
| checkerboard B (`s(t,x)=1` iff `x` odd) | **yes** | no | 0 |

One line for the checkerboard, since it is the load-bearing case: at `x` odd,
`0 XOR (1 OR 0) = 1`; at `x` even, `1 XOR (0 OR 1) = 0`. Fixed.

**Consequence, stated before any measurement.** Every finite checkerboard patch
is Rule-30-consistent, automatically, because the checkerboard is an orbit. So no
local, finite-window, pin-based or transducer argument can exclude it from `Y`.
Exclusion requires a global property of the *lone-seed* diagram. That is PATH.md's
named circularity — "controlling what `Y` contains may require knowing the
column" — made exact: the obstruction is not that the argument is hard, it is that
the local structure carries zero information about it.

**Pre-registered asymmetry, fixed before looking at numbers.** The measurement can
only kill R8, never advance it. Growth of a fixed point's patch heights with the
horizon is evidence it lies in `Y` and refutes the sufficient target. Boundedness
is inconclusive, because a finite prefix cannot certify a forbidden patch.

---

## 1. The Rule 90 control, and it is inverted correctly

R8 concedes that its claim is false for Rule 90. A control that merely *looks
different* would not be worth much. `rule90_exact.py` proves it instead.

**Theorem.** In the Rule 90 lone-seed diagram write `t = 2^k + j`, `0 <= j < 2^k`.
Then `min{ |x| : s(t,x) = 1 } = 2^k - j`.

*Proof.* `s(t,x) = 1` iff `t+x` is even and `C(t,(t+x)/2)` is odd, which by Kummer
holds iff `m = (t+x)/2` is a submask of `t`. The bits of `t` are `{k} u bits(j)`,
so `m = e*2^k + j'` with `e in {0,1}` and `j'` a submask of `j`, giving
`x = (2e-1) 2^k + 2j' - j`. For `e=0`, `x in [-j-2^k, j-2^k]`, so `|x| >= 2^k - j`
with equality at `j' = j`. For `e=1`, `x = 2^k + 2j' - j >= 2^k - j`, equality at
`j' = 0`. QED

**Corollary.** For every `W`, the Rule 90 band `[-W,W]` is identically zero on
`t in [2^k, 2^{k+1} - W)`, an interval of length `2^k - W`. Hence every all-zero
`(2W+1) x H` patch occurs, at arbitrarily large `t`, and along `t_k = 2^k` the
`(2k+1) x k` patch occurs for every `k`. So `0^{Z^2} in Y_90`, `delta_0` is a
vertical-shift-invariant measure on `Y_90` with centre density 0, and **R8's
sufficient target is false for Rule 90 with no finite-horizon extrapolation.**

Verified numerically two independent ways, both to the digit:

* brute-force submask enumeration vs the formula, 8054 values of `t` in
  `[1, 200000]`, 0 mismatches (`rule90_exact.py`);
* the simulation pipeline's measured all-zero band height equals the closed form
  at every tested `W`: `951424` for `W = 1..65536` at `T = 2e6` (block `a=20`,
  truncated by `T`), and `2^k - W` exactly at every power-of-two horizon —
  e.g. `511 = 2^9 - 1` at `T = 1024, W = 1`. `band_census.py` and
  `periodic_windows.py` independently reproduce `951424`.

Uncapped diagonal, so the control does not saturate its own instrument
(`rule90_exact.py`, `K` searched over all `k`, not capped at `W <= 8`):

```
Rule 90  K(all_zeros, T), T = 2^10 .. 2e6:
  256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288
```

`K_90(T) = Theta(T)`. Against Rule 30's `K_30(T) = Theta(log T)` below. The two
rules fail R8 by different mechanisms — Rule 90 by an exact arithmetic
degeneracy, Rule 30 by ordinary genericity — and that asymmetry is the honest
finding, not a rescue.

---

## 2. Rule 30: the band language is FULL as far as it can be checked

`realizable_patches.py` computes, EXACTLY, `R(W,H)` = the number of
`(2W+1) x H` patches realizable as a window of some bi-infinite Rule 30 orbit, by
enumerating every initial row of width `2W + 2H - 1` (exactly the dependency cone,
so the enumeration is complete). `band_census.py` measures `P(W,H)` = distinct
patches actually occurring in columns `[-W,W]` of the lone-seed diagram,
`t < 2e6`. Two independent code paths.

| `W` | `H` | `R(W,H)` exact | `P(W,H)` observed | `P/R` |
|---|---|---|---|---|
| 0 | 11 | 2048 | 2048 | **1.000000** |
| 1 | 8 | 5832 | 5832 | **1.000000** |
| 1 | 9 | 13928 | 13925 | 0.999785 |
| 1 | 10 | 32952 | 32898 | 0.998361 |
| 2 | 7 | 9664 | 9664 | **1.000000** |
| 2 | 8 | 23328 | 23322 | 0.999743 |
| 3 | 6 | 15872 | 15872 | **1.000000** |
| 3 | 7 | 38656 | 38646 | 0.999741 |
| 3 | 8 | 93312 | 92729 | 0.993752 |

**Frontier: every realizable patch of a `7 x 6` window occurs in a single
lone-seed diagram** — all 15,872 of them — and likewise `5 x 7`, `3 x 8`, and
`1 x 11`. For `W = 0` the census (not enumeration-capped) gives `P = 2^H` for
every `H <= 17`: the lone-seed centre column contains every binary word of length
17, and each of the 2048 words of length 11 at least 871 times. Read that with
its occupancy: at `H = 17` the mean count per word is only about 15, so
completeness there is a measurement at the edge of what `2 x 10^6` rows can
certify, and one doubling further (`H = 18`) leaves 134 of 262144 words still
absent. It is a sampling result about this prefix, not a structural theorem about
A051023.

The conclusion the census supports, stated at its real strength: **no forbidden
patch exists at any cell where the census can decide** (`P = R` exactly), and at
the cells where it cannot decide, the misses recur exactly as sampling predicts.

The sub-1 cells are a sampling tail, not prohibition (`forbidden_check.py`):

| cell | missing at `T` | missing at `T/2` | recovered in the second half | patches seen exactly once |
|---|---|---|---|---|
| `W=1,H=9` | 3 | 8 | 5 | 1 |
| `W=1,H=10` | 54 | 219 | 165 | 85 |
| `W=2,H=8` | 6 | 30 | 24 | 6 |
| `W=2,H=9` | 173 | 787 | 614 | 373 |
| `W=3,H=7` | 10 | 102 | 92 | 37 |
| `W=3,H=8` | 583 | 2613 | 2030 | 1384 |

62-90% of the patches absent at `T/2` had appeared by `T`, the count histogram is
the ordinary heavy tail (`#missing < #seen-once` strictly at 4 of the 6 cells,
equal at a fifth, larger only at `W=1,H=9` where the counts are 3 and 1), and each
missing patch's `(H-1)`-row prefix was itself seen only 1-79 times. Nothing is
forbidden; the misses are rare patches still arriving.

Two exact structural by-products, both horizon-free:

* `R(W,H) = 4^{W-1} R(1,H)` for `W >= 1`, verified at `W = 1,2,3` and all
  enumerated `H`. Adding a column to each side of the band is unconstrained.
* `R(W,H)` is strictly below the naive `2^{2W+1} 4^{H-1}` free-edge bound — that
  is the OR-latch pin, priced in patch counts. The per-row branching ratio
  `R(W,H+1)/R(W,H)` measured for `H = 2..11` is
  `3, 2.667, 2.5, 2.5, 2.48, 2.4355, 2.4139, 2.3882, 2.3659, 2.3438`,
  **still decreasing at `H = 11`; no limit is established** and none should be
  quoted. For Rule 90 the same ratio is exactly 4 at every `H` (additivity, no
  pin). Flagged and disqualified in section 5.

---

## 3. Rule 30: the fixed-point patches grow, at the Bernoulli rate

`band_census.py`, max height of each fixed-point patch in columns `[-W,W]` over
`t < T`, `T = 2^10 .. 2 x 10^6` (12 horizons):

```
all_zeros  W=0  10 12 12 12 14 19 19 19 19 19 19 19
           W=1   5  5  5  6  6  6  6  7  7  8  8  8
           W=2   4  4  4  5  5  5  5  6  6  7  7  7
           W=4   2  2  2  3  3  3  3  4  4  5  5  5
           W=8   0  0  0  0  0  0  0  0  0  1  1  1
checker_A  W=0   7  9  9 13 13 16 21 21 21 21 22 23
           W=1   5  7  7 11 11 14 17 17 17 17 17 17
           W=4   1  1  1  5  5  5 10 10 10 10 10 11
           W=8   0  0  0  0  0  0  0  0  0  4  4  4
checker_B  W=1   7  8  8 10 12 17 17 17 17 17 17 17
           W=8   0  0  0  0  0  1  1  1  1  1  1  1
```

Every `W` from 0 to 8 increased over the sweep, for all three families. At `W = 8`
the all-zero `17 x 1` patch and the checkerboard `17 x 4` patch first appear only
past `t = 2^19`; nothing has plateaued.

The reference scale is EXACT, not simulated (`exact_null.py`). Uniform
Bernoulli(1/2) is Rule 30 invariant (Taati arXiv:1505.06464 sec 2.4), and the
band patch is determined by the cone row of width `2W+2H-1`, so
`q(W,H) = #{cone rows giving the patch} / 2^{2W+2H-1}` is computed by enumeration.
The enumeration returns an exactly geometric law:

* holding the all-zero band costs a factor **1/4** per extra row, at every `W`;
* holding either checkerboard costs a factor **1/2** per extra row, at every `W`.

So `q(W,H) = 2^{-(2W+1)} 4^{-(H-1)}` for zeros and `2^{-(2W+1)} 2^{-(H-1)}` for
the checkerboards, and `H*(W,T) = ` the largest `H` with `T q(W,H) >= 1`. Measured
lone-seed height minus `H*`, at `T = 2e6`:

| `W` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| all zeros | -1 | -1 | -1 | -1 | -1 | -1 | -1 | -1 | -1 |
| checker A | +3 | 0 | 0 | -1 | -1 | -1 | -1 | 0 | 0 |
| checker B | -1 | -1 | -1 | -1 | 0 | 0 | -2 | -2 | -2 |

23 of the 27 cells lie within one row of the exact uniform-Bernoulli value; the
other four are `+3` (checker A, `W=0`) and `-2` (checker B, `W=6,7,8`). Nothing
is beyond `+3 / -2`. **The lone-seed diagram holds these patches for exactly as long as a
Bernoulli-typical Rule 30 orbit does.** There is no suppression to build a
forbidden-patch lemma on.

The diagonal statistic, which is what `Y` membership actually needs (both window
dimensions must grow along one sequence of times): `K(f,T) = max k` such that the
`(2k+1) x k` patch of `f` occurs at some `t < T`.

```
Rule 30, T = 2^10 .. 2e6:
  all_zeros  3 3 3 3 3 3 3 4 4 4 4 4     predicted K ~ log2(T)/4 = 5.2
  checker_A  2 2 2 4 4 4 4 5 6 6 6 6     predicted K ~ log2(T)/3 = 7.0
  checker_B  3 3 3 3 3 5 5 5 5 5 5 5
```

Growing, and tracking the exact prediction to within 1-2 over the whole sweep.
(The Rule 90 row of `recurrence.json` reads `8, 8, ...` only because that script
caps `k` at `W <= 8`; `rule90_exact.py` is the uncapped version and is the one
quoted in section 1. A control must not saturate its own instrument.)

Recurrence, which `Y` needs and mere occurrence does not — occurrences with
`t >= T/2`, from `recurrence.py`:

| family, `W` | height | occurrences | of those, `t >= T/2` |
|---|---|---|---|
| all zeros, `W=1` | 5 | 943 | 480 |
| all zeros, `W=1` | 7 | 50 | 26 |
| all zeros, `W=4` | 4 | 50 | 26 |
| checker A, `W=1` | 14 | 25 | 7 |
| checker A, `W=8` | 1 | 15 | 4 |

Roughly half the occurrences of each height fall in the second half of the run,
as a stationary process gives. These patches are not a transient of small `t`.

Finally the universal periodic-window statistic `Per(W,p,T)`, the longest
time-`p`-periodic window in the band, which subsumes ALL vertical-`p`-periodic
threats at once rather than enumerating candidate orbits
(`periodic_windows.py`, `T = 2e6`):

```
        p=1  p=2  p=3  p=4  p=5  p=6  p=7  p=8        Rule 90, any p
  W=0    23   23   23   24   23   27   25   26          1999999
  W=1    17   17   17   20   22   25   24   23           951424
  W=4    11   11   11   14   15   21   20   19           951424
  W=8     4    4    7    8    6   11   10   12           951424
```

Rule 30 `W=8, p=1` went `0 -> 4` between `T = 3 x 10^4` and `T = 2 x 10^6`. Every
cell grew. Rule 90 is five orders of magnitude larger and linear in `T`.

---

## 4. Verdict

**Route R8 is dead as stated, and the reason is not a wall — it is that the
target is false.**

For R8's sufficient target to hold, `Y` must exclude the all-zeros and both
checkerboard configurations. That requires a **uniform-in-`t` forbidden-patch
lemma**: some `(W,H)` for which the corresponding `(2W+1) x H` band patch occurs
at only finitely many `t` in the lone-seed diagram. The measurement says:

1. no such `(W,H)` exists in the checked range — `P = R` exactly through a `7 x 6`
   window, and every fixed-point patch that fits within `W <= 8` and the measured
   heights does occur;
2. the patch heights grow at every `W` across 11 horizon doublings, and match the
   exact uniform-Bernoulli scale to within one row at 23 of 27 cells, so the
   lemma is not merely unproved, it is contradicted by the observed rates;
3. the diagonal `K` grows for all three fixed points, which is the statistic `Y`
   membership actually requires.

Kill condition fired: the pre-registered one — *growth of a fixed point's patch
heights with the horizon refutes the sufficient target*. It fired for all three
fixed points and at every half-width.

For Rule 90 the same conclusion is a theorem (section 1). The Rule 90 filter is
therefore satisfied in the strong direction: the mechanism that kills R8 for
Rule 30 is genuinely different from Rule 90's (genericity vs an arithmetic
degeneracy), but the target fails for both, so **no repair of R8 that leaves the
sufficient target intact can pass the section-0 filter.**

Register row 8 should move `OPEN -> KILLED`, reason: *sufficient target refuted;
the vertical orbit closure contains vertical-shift fixed points of centre density
0 and 1, provably for Rule 90 and empirically to `T = 2e6` for Rule 30.*

This kills the ROUTE, not Problem 2. `Y` carrying a bad invariant measure means
the sufficient condition fails; it says nothing about the density of the actual
centre column. A successor route must target the specific orbit's empirical
measure directly, not the whole orbit closure — the closure is too big, and this
arm measures how much too big.

---

## 5. What a reader must not over-read

**`delta_0 in Y` is an extrapolation, not a proof.** The finite-horizon facts are:
`K(all_zeros, 2e6) = 4`, `K(checker_A, 2e6) = 6`, heights growing at every `W`,
and agreement with the exact Bernoulli law to within one row. `K -> infinity`
follows from the growth law, not from a theorem. Reaching `K = 20` for the
checkerboard would need `T ~ 2^60`. The NEGATIVE-RESULT CLAUSE applies: the
missing lemma is named in the first line, and this document does not claim it.

**The branching sequence is structure, not evidence.** `R(W,H)` growing at a
ratio that is `2.34` and still falling at `H = 11`, against Rule 90's exact 4, is
a Rule-30-specific number produced by the OR latch, and it separates the two
rules. It is nonetheless **column-blind** under obstruction C, in the
strongest possible way: `R(W,H)` is a function of the rule alone and of no
diagram, so overwriting column 0 of the lone-seed diagram with a periodic word
moves it by exactly zero. By PATH.md section 0.1 it therefore cannot decide P1 or
P2, and it is not offered as evidence for anything here. The same caution applies
to the `P = R` fullness result read as a discriminator: it is used above only to
show that no forbidden patch exists, which is a statement about `Y`, not a
rule-separating statistic.

**Obstruction E, placed precisely.** This arm is on the correct side of E. It is
not an ensemble or almost-everywhere statement: every measured quantity is a
property of the single lone-seed orbit, and `Y` is that orbit's closure. The
uniform-Bernoulli `q(W,H)` is used only as a reference scale, never as a premise;
by obstruction B an ensemble statement could not reach the single orbit and none
is asked to. The actual limitation is a *different* one: finite horizon
`T = 2 x 10^6` and half-width `W <= 8`. Do not read the horizon limitation as the
measure-zero-orbit limitation; they are separate, and only the first applies.

**A rejected control, recorded.** The first null tried was a simulated ensemble:
20 seeds, random initial row on a cycle of width 4096, Rule 30 iterated. It is
wrong and was discarded. Rule 30 on `Z/q` is not surjective, so uniform Bernoulli
is not preserved and a long cyclic orbit degenerates onto an attractor: it gives
an all-zero band height of 14 at `W = 1, T = 2^17`, against the exact value 8. The
numbers survive in `growth_fit.json` with the flag; the reference used in
section 3 is the exact enumeration in `exact_null.py`.

**Bounded-vs-unbounded is the only thing the heights decide.** A specific height
number at a specific `(W,T)` is a max over a heavy-tailed sample; the `+3` at
`checker_A, W=0` is not a finding.

---

## 6. Files, validation, compute horizon

| file | what it does |
|---|---|
| `band_census.py` | generates the lone-seed band `[-8,8]` for `T` rows (packed-uint64 light cone, `O(T^2/64)`); fixed-point patch heights by horizon; return-time gaps; patch census `P(W,H)` |
| `realizable_patches.py` | exact `R(W,H)` by complete cone enumeration; `P` vs `R` |
| `exact_null.py` | exact uniform-Bernoulli `q(W,H)` and `H*(W,T)`; the geometric per-row law |
| `forbidden_check.py` | are the `P < R` misses forbidden or rare — histograms, prefix counts, half-horizon recovery |
| `periodic_windows.py` | `Per(W,p,T)`, the universal time-`p`-periodic-window statistic |
| `recurrence.py` | per-height occurrence and late-occurrence profiles; diagonal `K(f,T)` |
| `rule90_exact.py` | the Rule 90 theorem, its brute-force verification, uncapped `K_90` |
| `growth_fit.py` | slopes in `log2 T`; contains the REJECTED simulated null, kept flagged |

Validation, all passing at `T = 2e6` (`validation` block of both census JSONs):

* centre column vs `common/rule30.py:center_column_bits` (independent frame
  arithmetic): equal on the first 4096 bits;
* full 17-column band vs `common/rule30.py:simulate_seed` (independent naive dict
  simulator): equal on all 512 x 17 cells;
* centre column vs the stored `experiments/rule30/orbit-closure/col30_2000000.bin`
  and `col90_2000000.bin`: equal on all 2,000,000 bytes, both rules (read-only);
* Rule 90 band vs the Lucas/Kummer submask formula: equal on all 512 x 17 cells;
* Rule 90 all-zero band heights vs the closed form of section 1: equal at every
  `W` tested, and reproduced independently by `periodic_windows.py`;
* the fixed-point table of section 0, recomputed exactly at every run;
* `forbidden_check.py` asserts no observed patch is non-realizable (it holds).

Compute horizon reached: `T = 2,000,000` rows of the full diagram, half-width
`W <= 8` (17 columns), 12 horizons from `2^10`; exact patch enumeration to
`2W + 2H - 1 <= 21` bits (`realizable_patches.py`) and `<= 24` bits
(`exact_null.py`); Rule 90 diagonal uncapped in `k`. Generation cost is
`O(T^2)`: 178 s (Rule 30) and 206 s (Rule 90) per band on this machine. Reruns
are cached; delete `band_rule*_*.npy` in the scratchpad to regenerate.

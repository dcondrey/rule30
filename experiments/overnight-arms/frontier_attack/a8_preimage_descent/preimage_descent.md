# A8, backward dynamics and preimage descent: NEGATIVE

**VERDICT: KILLED at the mandatory step-0 gate (PATH.md section 0.1,
single-column blindness), killed again at an added periodicity-vs-tamper gate,
and killed a third time structurally. At the widths where the candidate
quantity is non-degenerate (`W = 8..32`) a periodic column-0 overwrite moves it
by 2.1e-3 to 2.2e-2 while a *random* column-0 overwrite moves it by the same
order and more often by more, against a positive control that moves 95.6%; at
`W >= 64` it moves by exactly 0.0 because the statistic is saturated. It
separates Rule 30 from Rule 90 by 37-67% at every width. Independently: the
preimage branching cited in
register row 60 is a *ring* phenomenon; on finitely supported configurations of
`Z`, which is where the lone-seed orbit lives, Rule 30 is injective (verified
exhaustively to support width 22, zero collisions), so the backward orbit is a
chain and there is no preimage tree to descend. There is no missing lemma to
name, because there is no object.**

Date 2026-08-30. Arm directory
`experiments/overnight-arms/frontier_attack/a8_preimage_descent/`.
Modal: $0. Paid model-provider calls: $0. No file outside this directory was
written; `discriminator_local.py` is a byte copy of the read-only
`experiments/rule30/p_geometric_attack/discriminator.py`.

---

## 1. Step 0, the mandatory gate

### 1.1 The candidate quantity, defined before running

Preimage count is a functional of a whole row, so on its face it is
column-blind and the gate was expected to fire. Definition used:

> `S4_cyclic_preimage(grid, B, W)` = mean over the second half of rows `t` of
> `log2(1 + N_W(row_t))`, where `row_t` is the width-`W` window of row `t`
> centred on column 0 **read as a ring of circumference `W`**, and `N_W` counts
> `x` in `{0,1}^W` with `row_t[i] = x[i-1] XOR (x[i] OR x[i+1])` (indices mod
> `W`). Computed exactly as `Tr` of a product of `W` 4x4 integer transfer
> matrices over the states `(x[i-1], x[i])`.

Cyclic rather than free boundary is deliberate and is forced: with free
boundary the count is *identically 4* for every left-permutive rule (section 3
below), so the free-boundary variant is a constant and cannot move at all.
Register row 60's non-bijectivity measurement is likewise a measurement on
`Z_N`, so the ring is the only setting in which the arm's premise is even
nonvacuous.

Two overwrite variants were run, not one. The mandated gate asks only about the
periodic word; a random word was added because a quantity that moves equally
for both detects that column 0 was *tampered with*, not that it is *periodic*,
and column-sensitivity without periodicity-sensitivity still decides nothing
about P1.

### 1.2 Prediction, recorded in the script docstring before the run

(a) `|S4(A) - S4(B_per)|` will **not** be `O(1/W)`: the ring count is a trace
over a product of `W` matrices and one flipped factor can move the count
between 0 and 3, so a single-cell change per row should move `S4` by `O(1)`.
(b) The periodic and random deltas will be comparable, killing the arm at the
second gate even if (a) holds. (c) Rule 30 will separate from Rule 90, worth
nothing on its own.

**Prediction (a) was wrong, and it was wrong in the direction that kills the
arm harder.** This is recorded rather than quietly dropped. The width sweep was
extended downward to `W = 8` and a saturation control added *after* seeing
that, both labelled as post-hoc in the script docstring; the pre-registered
prediction was not edited.

### 1.3 The measurement

`step0_preimage_discriminator.py 400`, log `step0_discriminator.log`.
`T = 400`, 324,409 cells; `B_per` changes 196 of them (6.0e-4), `B_rnd` changes
210; asserted in code that each differs from `A` on column 0 and nowhere else.

| `W` | `S0` control `A`→`B_per` | `S4` `A`→`B_per` | `S4` `A`→`B_rnd` | `S4` `A` vs Rule 90 | frac. random words with `N_W = 1` |
|---|---|---|---|---|---|
| 8 | **0.4888 (95.6% rel)** | 0.02159 | **0.07388** | 67.4% | 0.745 |
| 12 | 0.4888 | 0.01455 | 0.0008454 | 59.8% | 0.864 |
| 16 | 0.4888 | 0.002065 | **0.01868** | 58.6% | 0.932 |
| 24 | 0.4888 | 0.01868 | 0.01493 | 54.4% | 0.977 |
| 32 | 0.4888 | 0.00291 | **0.004975** | 53.4% | 0.996 |
| 64 | 0.4888 | *0.0* | *0.0* | 49.2% | *1.000* |
| 128 | 0.4888 | *0.0* | *0.0* | 42.2% | *1.000* |
| 256 | 0.4888 | *0.0* | *0.0* | 37.3% | — |

**Read the `W >= 64` zeros as degeneracy, not as a measurement.** A saturation
control was added after the first run (2,000 uniform-random length-`W` words
per width, `saturation_control_random_words` in the log): the fraction of
*generic* binary words with a unique cyclic Rule-30 preimage rises to 1.000 by
`W = 64`. So at those widths `S4` is the constant function 1.0 on almost every
input, and a zero delta is a constant statistic being constant. Column-
blindness follows a fortiori, but the load-bearing evidence is the small-width
block, where `S4` still has range.

**Both kill conditions fire on the non-degenerate widths `W = 8..32`:**

1. *Magnitude.* The periodic delta is 2.1e-3 to 2.2e-2 against a control that
   moves 0.4888. That is the `O(1/W)`-or-less regime of PATH.md section 0.1.
2. *Periodicity-blindness.* The random-word delta is the same order at every
   width and is **larger** than the periodic delta at three of the five
   (`W = 8, 16, 32`). `S4` detects that column 0 was *tampered with*, not that
   it is *periodic*. A quantity with no periodicity signal above its tamper
   noise decides nothing about P1 even where it does move.

Meanwhile the same statistic separates Rule 30 from Rule 90 by 37-67% at every
width. This is a fourth clean instance of the recorded lesson, after rows 57,
58, 59: **rule-sensitivity is not evidence of P1-relevance.**

Prediction (a) was falsified and is recorded rather than dropped. It was wrong
twice over: the deltas were not `O(1)`, and the reason they collapse to zero at
large `W` is saturation of the statistic on generic input, which the original
`(32, 64, 128, 256)` sweep could not have distinguished from column-blindness.

---

## 2. Why it is zero: the arm's premise is a boundary-condition mismatch

The step-0 number is not an accident of the statistic. Enumeration
(`preimage_structure.py 22`, output `preimage_structure.json`):

**Rule 30 is injective on finitely supported configurations of `Z`.** Every
configuration supported in a width-`w` window, `w = 1..22` (4,194,304 configs
at `w = 22`), has a distinct image under one Rule 30 step. Zero collisions at
every width. Rule 90 likewise (expected: it is multiplication by `1 + z^2` over
`GF(2)[z]`, an integral domain).

Register row 60 is not contradicted. Its measurement is on `Z_N`, and the ring
histograms reproduce it:

| `N` | Rule 30 preimage-count histogram | Rule 90 |
|---|---|---|
| 3 | 0:3, 1:3, 2:1, 3:1 | 0:4, 2:4 |
| 6 | 0:12, 1:41, 2:10, 3:1 | 0:48, 4:16 |
| 9 | 0:57, 1:399, 2:55, 3:1 | 0:256, 2:256 |
| 12 | 0:280, 1:3537, 2:278, 3:1 | 0:3072, 4:1024 |
| 14 | 0:813, 1:14758, 2:813 | 0:12288, 4:4096 |

Two things to read off this. First, the branching is a property of the ring
closure, and the lone-seed orbit is not on a ring. Second, **Rule 90 branches
strictly harder than Rule 30**: every Rule-90 ring word with a preimage has 2
or 4 of them, whereas 92-95% of Rule-30 ring words with a preimage have exactly
one. So "Rule 30 has non-uniform preimages" does not merely pass the Rule 90
filter trivially, as warned; on the branching quantity itself Rule 30 is the
*less* branched of the two, while having the opposite P1 answer.

**On the actual orbit the backward map is a chain.** `orbit_chain.py 400`
(output `orbit_chain.json`) recovers `s(t, .)` from `s(t+1, .)` for all
`t = 0..399` using only the support endpoints, which are read off the image,
and the leftward peel `x[i-1] = y[i] XOR (x[i] OR x[i+1])` seeded by zeros to
the right of the support: **400 rows, 0 reconstruction mismatches, 0 branch
points.** The same run cross-checks PATH.md section 1's pin on those rows,
80,634 instances, 0 violations.

The arm's objective was "does the preimage structure of the rows on the
lone-seed orbit carry a descent, shrinking under backward iteration?" A chain
does not shrink. There is nothing to descend.

---

## 3. Free-boundary preimage count is identically 4, for both rules

For a left-permutive ECA `y[i] = x[i-1] XOR g(x[i], x[i+1])`, a target segment
`y[0..W-1]` constrains `x[-1..W]`. Choose `x[W-1]` and `x[W]` freely, 4 ways;
every `x[i-1]` is then forced leftward by `y[i]`. So the count is exactly 4,
with no dependence on `y` and no dependence on `g`. Verified by brute force
over all `2^W` targets and all `2^(W+2)` sources for `W = 1..5`, rules 30 and
90: `distinct_counts = [4]` in all ten cells.

This is the cleanest available statement of the pin-restatement question the
task asked. Answer: **yes, the preimage framing is the pin restated, with
nothing left over.** Window preimage counting *is* left permutivity; the
Rule-30-specific sharpening of the peel at `x[i] = 1`, where the OR saturates
and `x[i-1] = NOT y[i]` independently of `x[i+1]`, is exactly PATH.md section
1. `experiments/rule30/inverse_trace_probe.py:135-160`
(`reconstruct_left_column`) already implements the rotation, and PATH.md
section 0.5 already records that this mechanism predates the document.

## 4. What this arm uses beyond non-uniformity of preimage counts

Nothing, and that is the finding. The pre-run intent was to use eventual
periodicity of the centre column to constrain the preimage tree. There is no
tree: the relevant configuration space is finite-support `Z`, the map is
injective there, and the "tree" collapses to the chain measured in section 2.
Every remaining content of the framing is the peel, which is left permutivity,
which is already the repo's R3/rows-28/29 territory and already recorded dead
there (`RESULTS-eventual-period.md:88-100`: "A nonconstant periodic word has
bounded one-runs, so this gives only a bounded wedge, not a descent to
contradiction").

## 5. What a reader must not over-read

* **Injectivity on finite support is not new and is not a result.** It is a
  one-line consequence of left permutivity plus support-endpoint tracking, and
  it holds for Rule 90 too. It is reported here only because it is the fact
  that dissolves this arm's premise.
* **This does not contradict register row 60.** Row 60's "non-bijective at
  every `N` from 3 to 14, up to 3 preimages" is correct as stated, on `Z_N`.
  Row 60's own kill (no unitary evolution operator, so no RMT ensemble) stands
  unchanged.
* **The Rule 30 / Rule 90 separation in section 1.3 is not evidence of
  anything.** It is the trap PATH.md section 0.1 exists to catch.
* **`N_W = 1` for lone-seed rows is not a Rule 30 finding at all.** The
  saturation control shows 99.6% of *uniform-random* length-32 words and 100%
  of length-64 words already have a unique cyclic preimage. Long words
  generically do. Obstruction H applies in full besides: this is finite `T`,
  and it says nothing about `t > 400` and nothing about column 0.
* **No descent, composition or "appropriate lemma" step was invoked, because
  none was reached.** No proof artifact was produced and none contains `sorry`.

## Files

* `step0_preimage_discriminator.py`, `step0_discriminator.log` — the mandated
  gate, plus the random-word second control.
* `discriminator_local.py` — byte copy of the read-only repo discriminator.
* `preimage_structure.py`, `preimage_structure.json` — free-boundary count,
  finite-support injectivity to width 22, ring histograms.
* `orbit_chain.py`, `orbit_chain.json` — the chain, on the actual orbit, with
  the pin cross-check.

## Reproduction

```
uv run python step0_preimage_discriminator.py 400
uv run python preimage_structure.py 22
uv run python orbit_chain.py 400
```

## Suggested register row (not written; no file outside this directory was touched)

| # | Route | P | Verdict | Notes | Artifacts |
|---|---|---|---|---|---|
| 73 | Backward dynamics / preimage-tree descent on the lone-seed orbit | 1 | **KILLED** | Column-blind: cyclic-preimage entropy moves 2.1e-3 to 2.2e-2 under a periodic column-0 overwrite at `W=8..32` against a 95.6% control, and a *random* column-0 overwrite moves it as much or more at three of five widths, so the quantity is tamper-sensitive and periodicity-blind; at `W>=64` it moves 0.0 only because it is saturated (100% of random length-64 words have a unique cyclic preimage). Separates Rule 30 from Rule 90 by 37-67%. Premise also false by boundary mismatch: row 60's branching is on `Z_N`; on finite-support `Z` Rule 30 is injective (exhaustive to width 22), so the backward orbit is a chain with 0 branch points over `T=400`. Free-boundary window preimage count is identically 4 for every left-permutive rule, so the framing is the OR-latch pin restated with nothing left over. Rule 90 branches *harder* than Rule 30 on rings. | `frontier_attack/a8_preimage_descent/preimage_descent.md` |

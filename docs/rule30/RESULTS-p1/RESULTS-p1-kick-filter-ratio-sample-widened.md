# P1: the kick-filter-ratio tame/resonant split does not survive widening

Date: 2026-09-11. Evidence: `experiments/rule30/r1-general-period/
kick_ratio_sample_widen.py` and `kick-ratio-sample-widen.json`. Follow-on to
[the kick-filter-ratio mechanism report](RESULTS-p1-kick-filter-ratio-mechanism.md),
picking up the sanity check that doc flagged as owed but not done: its
tame/resonant separation rests on 4 hand-picked examples, width 16, first
period only.

Status: **the separation does not hold once the sample is widened to the
already-labelled separated-gap sweep plus the k=1/k=2 clustered families,
and the doc's own attributed cause is wrong: across all 33 widened cases
the decisive low-ratio filter step is always a bare-0 segment, never a kick
(section 4). This falsifies the mechanism doc's generalization expectation
and its mechanistic explanation, not the raw 4-example observation, which
still reproduces exactly.**

## 1. A definitional gap in the prior doc, found while reproducing it

The prior doc's stated definition is "the filter ratio: reachable-set size
after the filter, divided by the size right before it (right after the
kick's micro calls, before filtering)" for **kicks** specifically ("Only
kicks can do any real work"). But its own reported lists have 4-5 entries
for words that have only 1-2 true kicks per period (schedule segments that
cross a `1`; the rest are bare-0 segments with no comparison).
Reconstructing the exact trajectory (`schedules = [[0,1],[0],[0,1],[0],[0]]`
for its `resonant_p7` word) shows its lists are **every schedule segment's
filter ratio in the first period, kick or bare** — confirmed by exactly
reproducing `tame_adjacent_p6 = [0.522, 0.287, 0.638, 0.392]` and
`resonant_p7 = [0.834, 0.593, 0.708, 0.647, 0.392]` this way, digit-for-digit.
Both readings are tested below.

## 2. Widened sample

Reused, no new CA sweep beyond what `kick_ratio_sample_widen.py` runs
directly: every `(g1, g2)` case in `separated-gap-resonance-sweep.json` with
a confirmed `DIES` verdict (`peak` not null, `all_survive` false), labelled
`resonant` if `peak/p >= 1.4` else `tame` (5 resonant, 12 separated-gap-tame
cases), plus the k=1 isolated-one and k=2 adjacent-ones families for
`p=5..12` (16 more tame cases, exact closed-form peaks `p+2` and `p+1` from
[the rotation-sawtooth report](RESULTS-p1-clustered-ones-rotation-sawtooth.md)
— the strongest tame reference available, not itself compatible with the
mechanism doc's own 4 examples since it never included k=1). Width 16,
first period, matching the prior doc exactly.

## 3. Result: overlap under both readings

**Kick-only ratio** (segments crossing a `1`, the doc's stated definition):

| | range |
|---|---|
| tame (28 cases) | 0.5217 - 0.8345 |
| resonant (5 cases) | 0.6958 - 0.7079 |

Resonant's floor (0.6958) sits inside tame's range, and tame's ceiling
(0.8345) exceeds resonant's ceiling. No separating threshold exists.

**All-filter-event ratio** (what the doc's numbers actually are):

| | range |
|---|---|
| tame (28 cases) | 0.0 - 0.5209 |
| resonant (5 cases) | 0.3923 - 0.6099 |

Concrete counterexample: the k=1 isolated-one family (`0^(p-1)1`, exact
closed-form peak `p+2`, the most rigorously tame family in this repo) has
`min_all = 0.5209` at **every** tested `p = 5..12`, exceeding
`p7_g2_3` (gap word `1001000`, peak `3p`, the strongest confirmed
resonance) at `min_all = 0.3923`, and falling inside the resonant band
generally rather than below it. The proposed threshold (tame `<=0.29` or
`0`, resonant `>=0.39`) was fit to a sample that happened not to include
this family.

## 4. The stronger falsification: kicks are never the mechanism

Beyond the threshold not separating: for every one of the 33 widened cases
(28 tame, 5 resonant), the segment attaining the first period's *minimum*
filter ratio is a **bare-0 segment**, never a kick (`min_ratio_attribution`
in the JSON: `n_min_is_kick=0, n_min_is_bare=33`). This directly contradicts
the mechanism doc's central premise, quoted verbatim: "Only kicks can do
any real work: a run of pure `0`-bit `micro` calls just advances the strip
without ever comparing against a `1`." A bare-0 segment still ends in the
same parity filter every kick does (`rows[(rows&1)==0]`); nothing in
`zero_phase_schedule` or `micro` makes that filter step weaker when no `1`
was crossed, and the data shows it is usually the *stronger* one. The
qualitative tame/resonant split the doc observed on its 4 examples is real
(reproduced exactly in section 1 above), but the explanation it gave for
that split -- decisive kicks vs. weak ones -- attributes the effect to the
wrong kind of step.

## 5. Reading

The 4-example observation in the prior doc is exactly reproduced and not in
question. What does not survive is the inference drawn from it — "the
tame/resonant qualitative split... is expected to hold generally" — under
either honest reading of what was measured. The mechanism doc's own
`## What remains open` section already named the right next step (closed
form for the filter ratio of a kick of length `L` from the structure of
`micro` itself, not more empirical sweeping); this result adds that the
*first-period minimum* is not that quantity either way, so a closed form
would need to explain why `k=1`'s single kick sits at a fixed 0.8345/0.5209
regardless of `p`, while gap-pair kicks vary with `(g1, g2)` and still
straddle the same range as both tame and resonant labels — i.e. the filter
ratio of an individual kick is not, by itself, predictive of whether the
whole word resonates. Multi-period accumulation (which the prior doc
already flagged as the real distinguishing behavior for resonant words —
"2-3 full periods of accumulated weak shrink") is likely where the real
signal is, not any single first-period number.

## 5.1. Multi-period trace: small-N discreteness, not a decay rate

Extending the same per-segment trace across periods (not persisted to JSON;
console-only, same pattern as the original mechanism doc) on
`p7_g2_3_resonant` and `p9_g1_6_resonant` shows that once the reachable set
first drops to a small count, most subsequent schedule indices report
ratio `1.0` (the filter removes nothing) for one or more periods, then a
single bare index abruptly drops it, often to exactly `0`. E.g.
`p7_g2_3`: index 3's ratio sequence across periods is
`[0.6469, 0.2716, 0.2655, 0.0]`, while every other index sits at `1.0` for
periods 1-2 before the population dies at index 3, period 3. This is
consistent with plain small-integer fluctuation (few dozen surviving rows,
so a filter's ratio is a small numerator over a small denominator) rather
than an intrinsic per-segment decay rate. This further undercuts any
attempt at a closed form purely from kick or bare-segment *shape*: once the
set is small, which specific rows survived (full history-dependent) decides
the next ratio, not the segment's bit pattern in isolation. A closed form
would need to track the surviving set's actual structure at small size, not
just a per-segment transfer probability.

## 5.2. Width robustness

The original mechanism doc flagged width 16 as untested beyond: "the exact
numbers here are a width-16 artifact... not rechecked at width 20+."
Rerunning the same 33-case widened sample at width 20 and 24 (same script,
`filter_ratios_first_period`, width argument only) reproduces both findings
unchanged: no separating threshold at any width, and the first-period
minimum ratio is a bare segment in all 33 cases at every width tested.

| width | tame range | resonant range | separates | min_is_kick / min_is_bare |
|---|---|---|---|---|
| 16 | 0.0000-0.5209 | 0.3923-0.6099 | false | 0 / 33 |
| 20 | 0.0000-0.5049 | 0.3789-0.5957 | false | 0 / 33 |
| 24 | 0.0000-0.4920 | 0.3667-0.5827 | false | 0 / 33 |

Both falsifications are not a width-16 artifact.

## 6. Reproduction

```sh
cd experiments/rule30/r1-general-period
PYTHONDONTWRITEBYTECODE=1 python3 kick_ratio_sample_widen.py
```

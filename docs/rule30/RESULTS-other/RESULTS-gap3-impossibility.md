# Is a single gap-3 eventually impossible? A split answer from the strip method

Date: 2026-09-09.

**Deliverable: neither "yes" nor "no", but a genuine narrowing.** Two
specific two-letter precursors to a gap-3 (`2,2,3` and `4,4,3`, and also
the one-of-each mixtures `2,4,3` and `4,2,3`) are proved impossible at any
onset, uniformly, by the family-seam strip method. But a gap-3 immediately
after an arbitrarily long run of gap-1's is **not** excluded: a specific
candidate word survives the strip through width 24 (`(1)^m 3 (4,1)^inf`),
hitting this task's stop condition. A separate, wider candidate necklace
found during the search, `(4,2,4,4,1)^inf`, is a clean illustration of the
opposite failure mode: it survives widths 16-22 and is killed outright at
width 24, exactly the "coarser strips prove nothing" warning the task was
built around.

| Finding | Evidence |
|---|---|
| `S2` (gap-2 stable set) and `S4` (gap-4 stable set) reproduced at width 20: 670 / 1021 | `C`, two independent implementations, exact set equality |
| Four known necklaces `(1)^inf,(2)^inf,(4)^inf,(4,1)^inf` survive as nonempty fixed points at widths 20/22/24 | `C`, regression, required by the task |
| `2,2,3` is right-unrealizable at any onset | `U/C`, strip empty at widths 20/22/24 from the free universe, two implementations |
| `2,2,3` independently confirmed by exact (non-approximating) brute force | `C`, exhaustive fresh-onset enumeration, `L=10,11,12`, monotone in `L` |
| `4,4,3` is right-unrealizable at any onset | `C`, strip empty at widths 20/22/24 from the free universe, two implementations (brute-force cross-check not run: exponential cost, honestly out of scope) |
| `2,4,3` and `4,2,3` (mixed single blocks) are right-unrealizable at any onset | `C`, strip empty at widths 20/22/24 |
| A single `2,3` or `4,3` (only one prior matching gap) is **not** excluded by this method | `M`, nonempty candidate count at widths 20/22/24, not pursued further |
| `(1)^m 3 (4,1)^inf`-style candidate survives the strip through width 24 | `M`, candidate only, over-approximation, needs an independent unrestricted-cone check |
| `(4,2,4,4,1)^inf` candidate survives widths 16-22, empty at width 24 | `K`, width-24 strip kills a width-22 survivor: a concrete instance of the task's own warning |
| Rule 90 control: the same construction shows **no** exclusion at any step | `C`, width-8/12 strip stays at full size (2048/2048) every step; unchanged `controls.rule90_control(6)` also passes |

## 1. Setting and method

Exactly the family-seam method
([RESULTS-family-seam.md](RESULTS-family-seam.md)): width-`W` strip, right
columns `1..W`, both exterior-bit choices retained at every micro-update.
This is a sound over-approximation -- every actual right half-plane
trajectory projects into a path of the finite relation -- so an empty
reachable set proves the corresponding word is not right-realizable at any
onset, but a nonempty reachable set is only a **candidate**, never a
witness. Gap `g` is the block word `'0'*g + '1'` (matches `strip_sets.py`'s
own convention: `G = B_001` for gap 2, `E = B_0000100001` for the double
gap-4 excursion).

All code is in
[experiments/rule30/gap3-impossibility/](../../experiments/rule30/gap3-impossibility/):
`gap3_probe.py` (main computation, two independent strip implementations)
and `exact_brute_force.py` (an unrelated third, exact method for one
finding). Both **import, and do not edit**,
[strip_sets.py](../../experiments/rule30/family-seam/strip_sets.py),
[verify_strip.py](../../experiments/rule30/family-seam/verify_strip.py),
and
[right_trace_forbidden.py](../../experiments/rule30/p1-period2-invariant/right_trace_forbidden.py).
The frozen ladder hash was verified unchanged:
`589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.

Regression required by the task: the four known necklaces must survive at
every width tested. Confirmed at 20/22/24 (`gap3-probe-results.json`,
`regression.ok: true` at every width); the script raises `AssertionError`
and stops if this ever fails.

## 2. `2,2,3` and `4,4,3` are excluded uniformly, at any onset

For each of `g in {2,4}`, start from the full universe `U` (every odd
width-`W` row -- no assumption about prehistory at all), apply the gap-`g`
block `j` times, then try one gap-3 block. The minimal `j` at which the
gap-3 continuation is empty is **exactly 2**, at every width tested:

```text
width 20: gap-2 onset  j=0: 21210 survive gap-3; j=1: 2796; j=2: 0
          gap-4 onset  j=0: 21210 survive gap-3; j=1: 2558; j=2: 0
width 22: gap-2 onset  j=1: 7699 -> j=2: 0        gap-4 onset j=1: 6375 -> j=2: 0
width 24: gap-2 onset  j=1: 21174 -> j=2: 0        gap-4 onset j=1: 16101 -> j=2: 0
```

(Full tables, both independent implementations, in
`gap3-probe-results.json` under `onset_scan_gap2_then_gap3` /
`onset_scan_gap4_then_gap3` / cross-checked by `onset_cross_check_ok`.)

Because the starting set is the **unrestricted** universe `U`, not a
stabilized regime, this is stronger and cheaper than the family-seam
Lemma's approach (which needed 9 iterations to reach the true fixed point
`S_inf`): reaching emptiness in only 2 steps from `U` proves the finite
word `1,0,0,1,0,0,1,0,0,0,1` (anchored: `1` then gaps `2,2,3`) cannot occur
**at any onset**, by the identical "shift" argument as Lemma U in
[RESULTS-terminal-period-core-obstruction.md](RESULTS-terminal-period-core-obstruction.md)
section 3: start the cone at the actual right row at any time `p`, an
allowed assignment since the strip's initial row is free; if the word
occurred there, the strip's reachable set could not be empty.

The mixed one-of-each precursors are excluded the same way, with no
repetition needed at all: `2,4,3` and `4,2,3` both go empty immediately
after the two setup blocks, at every tested width (`mixed_2_4_then_3` in
the results file).

**Independent exact cross-check (`4,4,3` not included, cost -- see below).**
`exact_brute_force.py` reuses `right_trace_forbidden.realized_language`,
which enumerates **every** outcome of a truly free/arbitrary initial right
row at fresh alternating onset (not an approximation: exhaustive, exact,
light-cone-sized enumeration). The anchored pattern for `2,2,3`,
`10010010001` (length 11), is absent from the realized language at
`L=10,11,12` (`exact-brute-force-results.json`). Achievable words are
prefix-monotone (any longer achievable word restricts to a shorter
achievable word), so absence at `L=12` implies absence at every `L>=12`,
and by the same shift argument, at every onset. This confirms the strip
result by a completely different, non-approximating method. The `4,4,3`
pattern has length 14 (15 anchored); exhaustive enumeration at that length
is `2^29` seeds and was not run -- this is a genuine cost limitation, not a
result, and is reported as untested rather than assumed.

**Rule 90 control.** The identical construction (width 8 and 12, `rule=90`
in `strip_sets.py`) shows **zero** exclusion: the state count stays at the
full `2048` (all odd rows) at every step of both the gap-2 and gap-4 onset
scans (`rule90_control_width12` in the results file). This is consistent
with the established fact that Rule 90 realizes every `rho` freely. The
unrelated, unchanged `experiments/rule30/ladder-rung2/controls.py:
rule90_control(6)` was also run per the standing constraint and passes at
`T=2,4,6` exactly as before (torus construction, a different check, run
for compliance rather than relevance to this specific claim).

## 3. What is *not* excluded: gap-3 after a long run of gap-1's

A cheap diagnostic scan (apply gap-1 `j` times to the raw universe `U`,
then try one gap-3) does not reach zero for `j` up to 14 at any tested
width, but this scan alone is not conclusive: `S1` (gap-1's own true
forward-stable fixed point) needs `j=11` iterations to stabilize at width
20, `j=17` at width 22, and `j=16` at width 24 (`ss.fixed_point(width,
'01', 30)`), so the raw scan's last row at `j=14` had not always reached
the true fixed point yet at the wider widths (see
`onset_scan_gap1_then_gap3` in the results file for the raw, not-fully-
converged numbers).

The precise, trustworthy computation instead uses the actual computed
fixed point `S1` directly, then applies a single gap-3 to get `Q`, at
every width:

```text
width 20: S1=1288 -> Q=429
width 22: S1=2625 -> Q=640
width 24: S1=6321 -> Q=1319
```

`Q` is nonempty at all three widths. Extending `Q` by the
**known-realizable** `(4,1)` pattern repeatedly reaches its own nonzero
fixed point at all three widths too:

```text
width 20: Q=429  -> 888  -> 374  -> 238  -> 248  -> 252  -> 252  (stable)
width 22: Q=640  -> 1190 -> 632  -> 570  -> 604  -> 607  -> 607  (stable)
width 24: Q=1319 -> 2178 -> 1291 -> 1235 -> 1534 -> 1585 -> 1585 (stable)
```

cross-checked bit-for-bit between `strip_sets.py` and `verify_strip.py` at
width 24 (`gap13_candidate_width{20,22,24}` in the results file). So the
strip candidate for the eventually-periodic word

```text
(1)^m  3  (4,1)^infinity          (m arbitrarily large)
```

survives through width 24, with a clean, monotone-looking convergent trend
across all three tested widths (429/640/1319 for `Q`, 252/607/1585 for the
subsequent fixed point) -- unlike the killed candidate in section 4, where
nothing about the width-22 numbers foreshadowed the width-24 collapse.
**This is still a candidate, not a witness.** Since the over-approximation
is sound, survival at width 24 does not prove realizability; it only means
this width's strip cannot rule it out. Note this candidate's *eventual
cyclic tail* is still `(4,1)^inf`, one of the four already-known necklaces
-- the `3` here appears only as a one-time transient at the seam between
the two regimes, not as part of any recurring cycle. It is a candidate for
"can a 3 occur at all, arbitrarily late" (yes, unresolved), not for "can a
3 occur periodically forever" (no candidate for that survived anywhere in
this search).

A full reachable-state-graph search (all four gap letters, exact-cycle
detection, `gap3_probe.explore`) from `Q` finds a `(4,1)`-type surviving
cycle directly at every width: `[4,2,4,4,1]` after 312 states at width 20
(the wider, later-killed candidate of section 4 -- see there), `[1,4]`
after 374 states at width 22, and the plain `[4,1]` after 575 states at
width 24. No other surviving cycle was found before the search terminated
at any width; this is not an exhaustive claim that none exists (the search
stops at the first cycle it finds along its BFS frontier order, it does
not enumerate all cycles from a state).

This is exactly the task's stop condition: **gap 3 survives at width 24.**
Per instruction, this is reported and the search stops here; no attempt
was made to go symbolic or to widen the strip past 24 (memory is `2^W`
rows, and 24 is noted elsewhere in this project as the practical ceiling
for explicit sets).

## 4. A cautionary tale found along the way: `(4,2,4,4,1)^inf`

The width-20 graph search above surfaced a candidate cyclic word,
`(4,2,4,4,1)^inf` (period-20-sample gap cycle: `4,2,4,4,1` repeating),
reached as a self-loop in the reachable-state graph after the `(1)^m 3`
seam. Checked in isolation (`fixed_point` on the bare word, starting from
the full universe, no seam needed) it is nonempty and stable at widths
16, 18, 20, and 22:

```text
width 16: 111    width 18: 191    width 20: 342    width 22: 679
```

and then **empty at width 24**:

```text
width 24 counts: 8388608 -> 3416 -> 1391 -> 686 -> 0 -> 0
```

This is reported precisely because it is a clean, checked instance of the
warning already stated in the task: "coarser strips failing to go
extinct proves nothing, since the abstraction is an over-approximation."
The growing-then-dying size sequence (111, 191, 342, 679, 0) is itself a
useful data point: this candidate was not a fluke that barely survived --
its state count was still growing at width 22 -- yet width 24 kills it
outright. This is direct evidence that the still-surviving `(1)^m 3
(4,1)^inf` candidate from section 3 (whose counts have also not yet
stabilized cleanly at width 24) should not be treated as likely-real
without checking wider strips or an independent cone certificate; it
should also not be dismissed on the strength of this analogy alone, since
its width-24 behavior (`1319 -> ... -> 1585`, genuinely stable, not still
falling) looks qualitatively different from this killed candidate's
width-24 behavior (falls straight to zero).

## 5. Reproduction

```bash
cd experiments/rule30/gap3-impossibility
python3 gap3_probe.py --widths 20 22 24      # ~2 minutes, writes gap3-probe-results.json
python3 exact_brute_force.py                  # ~30 seconds, writes exact-brute-force-results.json
```

## 6. Scope, honesty notes, and what remains open

- **Not established:** whether a single gap-3 is eventually impossible
  outright. The answer is split: two specific short precursor patterns
  (`2,2,3`, `4,4,3`, `2,4,3`, `4,2,3`) are proved impossible at any onset;
  a gap-3 after a long gap-1 run is not excluded and has a specific
  surviving strip candidate at width 24.
- **The surviving candidate is not a counterexample to the terminal-period
  theorem.** Its eventual cyclic tail is `(4,1)^inf`, already a known
  necklace; the `3` is a one-time transient at the regime seam, not a
  recurring symbol. It would, if real, show that eventually-periodic `rho`
  can have a transient defect containing a `3` -- a different and weaker
  claim than "3 can appear in a realizable cyclic necklace."
- **No claim of realizability is made for any surviving candidate.**
  Per the strip method's own soundness direction, survival at width 24
  only means this abstraction cannot exclude it; an independent
  unrestricted-cone (SAT/DRUP or exact enumeration) check, in the style of
  `uniform-seam-certificate.json` in the family-seam work, was not run
  tonight, matching the task's explicit stop condition.
- **The `explore()` graph search is not exhaustive.** It stops at the
  first exact-cycle it finds; it does not enumerate all cycles reachable
  from a state, so "one candidate found" is not "the only candidate."
- **The `4,4,3` exclusion lacks the exact brute-force cross-check** that
  `2,2,3` received, purely because the pattern is too long (`2^29` seeds)
  for the exhaustive method used here. This is reported as untested, not
  assumed to hold by analogy.
- **Front-lemma compliance.** Every exclusion claim here concerns a fully
  specified finite word or a fully specified family (`2,2,3`, `4,4,3`,
  `2,4,3`, `4,2,3`, and the two named infinite candidates), refuted or
  supported by a finite strip cone. No bounded-window decision procedure
  for an unknown word's eventual periodicity is used anywhere in this
  report, so the front lemma's restriction does not apply.
- **Single-column sensitivity filter.** Not applicable: this report does
  not propose a new real-valued statistic of a window; it is a
  combinatorial realizability question about specific finite words.

## 7. Search-verdict correction, 2026-09-09

Task 6 found two bugs in `gap3_probe.explore`: a depth cutoff could be
reported as extinction, and ancestor-only cycle detection could miss a
directed cycle made of cross edges. Both are repaired, with exact baseline
and repaired replays in
[RESULTS-load-bearing-seam-audit.md](RESULTS-load-bearing-seam-audit.md).
The recorded Task 1 results above remain valid: they use direct empty
images, exact set repetitions, and positively found cycles, not either
false extinction return. A depth-limited unresolved search now returns
`depth_cap`; a complete graph receives a full directed-cycle check.

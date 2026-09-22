# P1: the authorized Modal GPU pilot, evaluated against measured evidence

Date: 2026-09-11. Evidence in `experiments/rule30/r1-general-period/`:
`width_saturation_and_necklace_sweep.py`, `mismatch_widths_2224_26.py`,
`p11_saturation_check.py`, and their JSON outputs.

`MODAL-COMPUTE-CHARTER.md`'s first eligible pilot is a bounded
periodicity-assumption contradiction search: encode an assumed centre
period, use Rule 30's exact recurrence and lone-seed boundary, include
Rule 90 as an adversarial control, return a reusable certificate. Merely
extending the checked period or width range is explicitly excluded, and
`p1-period2-invariant/PROOF-STATE-CAPSULE.md`'s own next-proof-program
independently says the same thing: "Do not extend the horizon census."

The nearest existing mechanism to the charter's description is
`r1-general-period/strip_general_p.py` + `survey.py`: for an assumed
period-*p* centre word, it computes the sound over-approximate reachable
set of a bounded strip under Rule 30's exact local update (`micro`,
imported read-only from `family-seam/strip_sets.py`), sampling at each
zero-phase occurrence. If the reachable set empties (DIES), the assumed
period is refuted within that strip width; if it stabilizes to a nonzero
cycle (SURVIVES), the width was insufficient to decide it. Rule 90 controls
already run alongside every probe. This is the candidate a GPU port
(numpy to cupy, same code) would accelerate: `micro`'s cost is
`np.unique`/sort-dominated and grows with the branching state count, so a
wider strip is exactly where a GPU buys a constant-factor speedup.

**Before designing that manifest, the width axis was measured instead of
assumed.**

## 1. Timing: cost is exponential in width

Single SURVIVES probe (period 4, one of the two exceptional necklaces),
widths 20/22/24/26: 0.16s, 0.89s, 4.93s, 26.6s (last one UNRESOLVED within
the sample budget). A GPU makes this cheaper per unit width; it does not
change the growth rate. The question is whether wider is scientifically
necessary at all.

## 2. Isolated-one family: width-invariant, but the pattern doesn't generalize

`survey.py`'s stored results show `max_zero_run` unchanged for the
`0^(p-1)1` family across widths 12 through 24 (p=5: 7 at every width; p=10:
12 at every width), and the values fit `max_zero_run = p+2` for p in
5..10 with {3,4} the only SURVIVES exceptions.

A full necklace sweep (all periodic words, not just the isolated-one
family), periods 6..10, widths 16 vs. 20, run this session
(`width_saturation_and_necklace_sweep.py`, 1974 words, ~287s), refutes the
generalization: 27 of those words disagree between the two widths. p=6 and
p=7 are clean; disagreement starts at p=8. **Every** disagreement is in the
sound direction: width 16 never finds *more* contradiction than width 20
(`max_zero_run` only ever larger at 16, and the two SURVIVES→DIES flips
only ever go that way, never DIES→SURVIVES). Width 16 is simply too coarse
to decide these words, not inconsistent. So `max_zero_run = p+2` is a
property of the isolated-one family specifically, not a period-independent
invariant — `survey-results.json` should not be read as showing otherwise.

## 3. Saturation point: 22, not "keeps moving"

All 27 mismatching words, re-run at widths 22/24/26
(`mismatch_widths_2224_26.py`, ~most words resolve well inside the sample
budget): every value is identical across all three widths, and equal to
the width-20 value. Nothing moved between 20 and 26 for any word in this
set. The handful of period-10 words with `max_zero_run` of 1-3 checked
against degenerate input (very sparse zero-phase words, `z=2` or `z=3`)
are genuine, not a bug in the harness.

## 4. p=11: saturation does not hold; the required width is still rising

The count of words needing more than the coarser width to decide, by
period: p=6:0, p=7:0, p=8:8, p=9:9, p=10:10 (widths 16 vs. 20). That count
is monotone rising, not flat, and it was not chased further before writing
the first version of this conclusion. A full necklace sweep at p=11,
widths 20 vs. 22 (`p11_saturation_check.py`, 2046 words, ~2155s), settles
it: **31 words disagree**, again all in the sound direction (no unsound
flips; `max_zero_run` only ever larger at 20, never at 22), but 22 of the
31 are SURVIVES-at-20 going to UNRESOLVED-at-22 rather than resolving to
DIES — width 22 is not yet enough to decide them at all, inside the
90-sample budget. Width 22 does **not** saturate at p=11.

## 5. p=11 at widths 24/26: the 20 DIES words settle; 11 words stay open

`p11_mismatch_widths_24_26.py` reran the 31 p=11 mismatches at widths 24
and 26 (default 90-sample budget), ~1275s. The 20 words that resolved to
DIES anywhere in 20-22-24-26 are DIES at both 24 and 26, and about a third
of those are still tightening between 24 and 26 (e.g. 48→44, 46→42,
45→41, matching the same sound monotone direction as every earlier
width step) rather than fully flat — width 26 is closer to this
mechanism's true saturation point for p=11 than 22 was, but not
demonstrated to be at it.

The other 11 words (`SURVIVES` at width 20, `UNRESOLVED` from width 22
onward) stayed `UNRESOLVED` at both 24 and 26 inside the default 90-sample
budget. That is two different open questions wearing one label: either
90 samples is too few to see these words' stable cycle at a width that is
otherwise already sufficient, or width itself has not caught up for this
subset even at 26. `p11_unresolved_more_samples.py` reran those 11 words
at width 26 with 4x the sample budget, holding width fixed, to tell the
two apart before spending anything on a wider run: **all 11 resolve to
`SURVIVES`**, ~314s. Budget-limited, not width-limited — width 26 already
decided every one of them; the 90-sample default was just too short to
see the cycle close.

So all 31 of the p=11 mismatches are decided by width 26 on CPU (20 DIES,
11 SURVIVES), the same width that already sufficed for p<=10. What looked
in §4 like the required width still rising past 22 was, once chased,
mostly an artifact of the fixed 90-sample budget rather than the strip
being too narrow. This strengthens the conclusion rather than reopening
it: no evidence this session, across p up to 11, of a period needing more
than a modest CPU-affordable width — the actual constraint that showed up
was sample count, and that is the cheapest knob available, not one a GPU
manifest would even target.

## Conclusion

Across p=6 through 11, this mechanism's verdicts are decided by width 26
or narrower, on CPU, in seconds to a few minutes per word. The apparent
rise in §4 (more words needing a wider strip as p grows) turned out, once
chased to the end at p=11, to be dominated by a fixed 90-sample budget
running out before a genuine cycle closed, not by the strip itself being
too narrow. No period up to 11 required more width than 26 to decide.

This does not license a GPU manifest: the charter and
`PROOF-STATE-CAPSULE.md` both rule out a longer checked-range/wider-
horizon run as a scientific deliverable regardless of cost, and the
evidence here shows the actual constraint on this mechanism is sample
count, which is the cheapest possible knob to turn and not one a GPU
buys anything on. Nothing measured this session supports scaling this
mechanism onto Modal. **No manifest was written.**

What remains open, and isn't a computation: whether `max_zero_run` (or a
related exact quantity) has a closed form for the general necklace
population the way it does for the isolated-one family, and whether that
closed form — not a wider search — is the charter's "candidate
period-independent invariant." That is symbolic work, matching
`PROOF-STATE-CAPSULE.md` §7's own direction.

A genuinely different mechanism (transition-graph/automaton synthesis, as
in `r1-isolated-column/`) might still be GPU-eligible, but it is
CEGIS/SAT-shaped — sequential search over lookup tables, not an
embarrassingly parallel sweep — and was not measured this session; no
claim is made about it either way.

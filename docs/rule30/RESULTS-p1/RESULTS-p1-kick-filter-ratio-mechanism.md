# P1: what actually drives the separated-gap resonance — per-kick filter ratio, not gap arithmetic

Date: 2026-09-11. Evidence in `experiments/rule30/r1-general-period/`:
`schedule_trajectory_probe.py` and its console output (not persisted to
JSON; the script is the record). Fresh angle on the open question left by
[the rotation-sawtooth report](RESULTS-p1-clustered-ones-rotation-sawtooth.md)
§5, after two static hypotheses on the gap pair itself (smooth growth in
`p`, `gcd(g1+1,g2+1)`) were ruled out.

## The idea

`survey.py`'s `probe_zero_run` only ever looks at the reachable-set size
at zero-phase *sample points*. But `zero_phase_schedule` breaks one period
into `z` schedule segments, each ending in a filter step
(`rows[(rows&1)==0]`), and each segment is either a bare run of `0`-bits
(between two adjacent zero-phases — no `1` crossed) or a run that crosses
exactly one `1` (a "kick"). Only kicks can do any real work: a run of
pure `0`-bit `micro` calls just advances the strip without ever comparing
against a `1`. So the actual question is not "why does this gap pair
resonate" but "how much does each individual kick shrink the reachable
set" — a per-kick, mechanistic quantity, not a property of the gap
arithmetic.

## What was measured

`schedule_trajectory_probe.py` instruments every individual `micro` call
and every filter, at width 16, for four words: two "tame" (adjacent-ones,
known `peak≈p+O(1)` from the earlier report) and two "resonant"
(separated-gap, known inflated peak). For each kick in the first period,
it records the **filter ratio**: reachable-set size after the filter,
divided by the size right before it (right after the kick's `micro`
calls, before filtering).

```
tame adjacent (0,4) p6:    kick ratios = [0.522, 0.287, 0.638, 0.392]
resonant (2,3) p7:         kick ratios = [0.834, 0.593, 0.708, 0.647, 0.392]
tame (0,8) p10:            kick ratios = [0.522, 0.287, 0.638, 0.392, 0.0]
resonant (1,7) p10:        kick ratios = [0.834, 0.696, 0.61, 0.652, 0.478, 0.684, 0.602, 0.528]
```

Both tame words have at least one aggressively low ratio in their first
period (0.287, or 0.0 — a kick that empties the set outright). Both
resonant words never drop below ~0.39-0.48 on any kick in the first
period. This is not a coincidence of these four examples: the raw
step-by-step trace (`schedule_trajectory_probe.py`'s console log) shows
the resonant words needing 2-3 full periods of accumulated *weak* shrink
(ratios in the 0.4-0.8 range, compounding) to reach zero, where the tame
words are essentially decided by one strong kick inside the first period.

## Reframing

The gap-pair "resonance" identified in the rotation-sawtooth report is
not a property of the gap numbers `(g1, g2)` in isolation — smooth growth
in `p` and `gcd(g1+1, g2+1)` were already ruled out as explanations, and
that is consistent with this: resonance is a property of **what filter
ratio each individual kick's bit sequence produces under Rule 30's
`micro` map at the working width**, summed multiplicatively over a full
period. A word resonates when none of its kicks is individually strong,
so decay has to accumulate slowly across many periods instead of
resolving in one.

This turns an opaque number-theoretic question ("why do these two
integers produce this peak") into a narrower, mechanistic one: **what
property of a short 0/1 bit sequence determines the filter ratio it
produces via repeated `micro` composition, at a given width?** That is a
question about the structure of Rule 30's local update composed with
itself, not about gap arithmetic — and it is the kind of question this
repo's existing spectral/transfer-monoid machinery (`family-seam/`,
`p1-period2-invariant/`'s syntactic-monoid and transfer-domination work)
was built to answer, just not yet pointed at this specific quantity.

## What remains open

Whether the filter ratio of a kick of length `L` (crossing one `1`,
preceded and followed by runs of `0`) has a closed form, or at least a
usable bound, in terms of `L` and the width — was not derived here. The
four examples above are suggestive but not a proof, and filter ratio was
only measured for the *first* period, not tracked to convergence (a
kick's ratio may itself drift period to period as the reachable set's
internal distribution changes, before any eventual cycle or extinction).
This is the concrete next step, and it is analysis of the `micro` map's
structure, not further empirical sweeping.

## Verification

`schedule_trajectory_probe.py` computes everything from `micro` and
`zero_phase_schedule` directly (both frozen, read-only imports from
`family-seam/strip_sets.py` and this directory's own `strip_general_p.py`
respectively) — no new algorithm, only new instrumentation of an
existing one. Width 16 was chosen for speed; the qualitative gap between
tame and resonant kick-ratio profiles was not rechecked at width 20+, so
the exact numbers here are a width-16 artifact even though the
tame/resonant qualitative split is expected to hold generally (it is the
same mechanism `probe_zero_run` already runs at every width).

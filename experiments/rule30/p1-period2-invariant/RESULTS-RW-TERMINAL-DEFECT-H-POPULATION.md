# Section 4 measurement: |H_r(n)| for r=0,1,2, n<=16

Date: 2026-09-04

Status: **the pre-registered `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md`
section 4 measurement, run for the first time.** `|H_r(n)| = 0` exactly, for
every `n = 1..16`, every `r in {0,1,2}`, both `c`. This is a stronger result
than the prereg's stated question (does the ratio decay with `n`): the
population is not merely shrinking, it is exactly empty at every measured
length. Control #1 (two independent constructions must agree per word) held
throughout with no assertion failures.

## What was measured

`H_r(n) = {W in {1,2}^n : literal_extension(W, c, n+r+2) survives the
hard-core and 12a-terminal checks}`, per the prereg's exact definition —
the population for which an RW witness is even a live candidate, before
asking about constancy. Computed two independent ways per word
(`forward_filter`, written fresh against the hard-core/terminal-pull
definition directly, and `via_rotated`, `dlp_rotated_wedge.rotated_wedge_population`'s
own `surviving`/`terminal_pull` booleans), asserting agreement on every
word — this is control #1 from the prereg's section 5. No disagreement
occurred.

## Result

| r | c | n=1..16 |
|---|---|---|
| 0 | 2 | `|H_r(n)| = 0` at every `n` |
| 0 | 3 | `|H_r(n)| = 0` at every `n` |
| 1 | 2 | `|H_r(n)| = 0` at every `n` |
| 1 | 3 | `|H_r(n)| = 0` at every `n` |
| 2 | 2 | `|H_r(n)| = 0` at every `n` |
| 2 | 3 | `|H_r(n)| = 0` at every `n` |

Exhaustive (not sampled) at every `n`: every word in `{1,2}^n` is checked,
so "0" is exact, not an artifact of a thin sample — unlike the
`fib_transfer_screen`-based block censuses (`RESULTS-FIB-ABSENT-M8-M9-M10.md`),
which pool over survivors and can under-sample at depth.

## Reading

This is a stronger and cleaner finding than the prereg's own kill condition
anticipated. The prereg asked whether `|H_r(n)|/2^n` *decays* with `n`
(to motivate a "shrinking candidate population" argument). Instead, the
population is already **exactly empty** at every tested length — before
`n` is even large enough for a decay trend to be visible as opposed to a
flat identical zero.

This does not yet reach or exceed the existing SAT result (RW already known
UNSAT to `n=28` by direct SAT search per `PROOF-STATE-CAPSULE.md`/BACKLOG
section 12), since `H_r(n)` is a strictly weaker/necessary-only condition
(it doesn't require the constancy check RW itself needs) and only n<=16 has
been checked. What is new: `H_r(n)=0` is a *stronger* statement than "no RW
witness exists at this `n`" — it says no candidate even survives the first,
purely local (hard-core + fixed-terminal-pull) filter on `literal_extension`'s
deterministic output, independent of the constancy question that has the
degree-`n` obstruction (capsule section 7 / `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md`
section 0). If this population is empty for a *structural* reason rather
than coincidentally at each tested `n`, that reason should be provable
directly from `literal_extension`'s row-by-row forcing recursion, without
ever invoking the harder full-degree obstruction — a meaningfully different
and potentially easier proof shape than anything else on the backlog.

**This is not yet a proof.** No structural reason for the emptiness has
been derived; only the exhaustive census has been run, only to `n=16`.

## Next step

1. Look for a direct combinatorial reason `H_r(n)` is forced empty — likely
   an invariant of `literal_extension`'s row-by-row state search that
   precludes ever landing on a hard-core, `12a`-terminal word. Check it
   against the row-permutation / triangularity facts already used in
   `endpoint_restart_cocycle.py` and the collapse lemma in the prereg
   section 2, since both concern the same forcing recursion.
2. If no quick structural argument appears, extend the census past `n=16`
   (cost roughly doubles per `n`; `n=17` per combo is ~6-7 min, `n=18` ~13-15
   min, so all six combos to `n=18` is on the order of 2 hours) to see
   whether the exact-zero pattern still holds, which would sharpen the case
   that this needs a structural proof rather than being a numerical
   coincidence of small `n`.

## Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python rw_population_h.py --max-source 16
```

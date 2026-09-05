# Are the m=8,9,10 "missing" RW forced-symbol blocks real, or sampling?

Date: 2026-09-04

Status: **SUPERSEDED / retitled after the fact.** m=8 resolved as sampling,
m=9/10 inconclusive on their own terms (see below) — but "RW forced-symbol
language" here means `fib_transfer_screen.forced_words`'s language, which a
concurrent session's correction to `BACKLOG.md` section 17 (same day,
`RESULTS-MEASURE-SUPPRESSION.md` V3(b)) identified as the `psi_kernel`
H-bit-forced `(BWH+)`/`Psi_n` object, **not** the `literal_extension`-based
`H_r(n)`/RW object `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md` section 4
and BACKLOG section 18 actually mean by "RW". Everything below is a real
finding about `Psi_n`'s block language (already known to have full
algebraic degree, capsule section 7), and answers nothing about section
18's actual premise. Do not cite this document as a section-18
prerequisite result without rebuilding the census on `literal_extension`
first.

## Why

`fib_transfer_screen_20260902.log` (pooled `n=10..17`) found 18/55 hard-core
blocks of length 8 absent from RW forced words, and BACKLOG.md called this
"sample-limited" without checking. The length-7 analogue (one absent block,
`1221222`) was already shown to be pure sampling: `fib_absent_check.py`
found it present at `n=18,19`. Before building any CFL/pushdown machinery
for section 18 (whose whole premise is a missing-block signal beyond
finite-state structure), the same check needed to run for m=8,9,10.

## Method

`fib_absent_check_m8910.py`: recompute the exact absent-block sets at
`n=10..17` (RW language only, matches the existing log), then search for
each block in RW forced words at `n=18,19,20`, both `c`, tracking the union
found across all six `(n,c)` slices (the first version of this script only
logged per-slice counts, which cannot distinguish "still absent everywhere"
from "just not in this one slice"; fixed before drawing conclusions).

## Result

| m | absent set size (n=10..17) | union found n=18-20 | still absent everywhere | max runs>=m in any slice |
|---|---|---|---|---|
| 8 | 18 | 18 | **0** | 905 |
| 9 | 65 | 50 | 15 | 267 |
| 10 | 136 | 50 | 86 | 111 |

m=8: fully resolved, matches the m=7 precedent exactly. Section 18's
motivating premise has zero support at m=8.

m=9, m=10: sample counts (`runs>=m`, i.e. how many RW survivors even reach
that depth at `n<=20`) are far smaller than m=8's — m=8 needed samples up to
905 to clear every block; m=9 tops out at 267, m=10 at 111. The RW survivor
population is shrinking with depth (consistent with the separate `H_r(n)`
census currently running, which finds `|H_r(n)|=0` through `n=12`), so
fewer long runs exist at all in this `n` range. This is the same shape of
under-sampling that resolved m=7 and m=8, just not yet run far enough to
resolve m=9/10.

## What this does not establish

This is not evidence that the pushdown-language route (BACKLOG section 18)
has a real prerequisite signal, nor that it doesn't. Resolving m=9/10 the
same way m=7/8 were resolved requires survivor counts comparable to m=8's
(hundreds of runs at that depth), which at the observed shrinkage rate needs
`n` well past 20 — expensive (exhaustive `2^n` per `n`), and not yet run.

**Do not build a CFL pumping-lemma checker on the strength of the m=9/10
residuals above.** That would be building infrastructure on an unconfirmed
premise, exactly the failure mode section 18 itself and the project's
research-mode discipline both warn against. The prerequisite question is
still open, not resolved in section 18's favor.

## Next step, if pursued

Either extend the survivor generation to larger `n` (cost grows fast; watch
`H_r(n)` first — if that census shows the RW-survivor population is already
vanishing by `n~20`, larger `n` will not produce more m=9/10-depth runs
either, and this route is moot for a different reason: there may soon be no
RW survivors at all to have a "language" over), or drop section 18 as
currently unmotivated and return to it only if a future result independently
establishes non-regular structure.

## Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python fib_absent_check_m8910.py
```

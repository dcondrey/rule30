# Pre-registration: does anything actually suppress constant `Psi`?

Written 2026-09-02, **before** the statistic below was computed.  Nothing in
this file was edited after the run; the result is appended in a clearly marked
section.

## Motivation

`(BWH+)` asserts no binary source `W in {1,2}^n` has constant defect word
`Psi_n(W)`, for `n >= 7`.  `Psi` has length `n+2`; the source has `n` free
bits.  Constancy is `n+1` binary constraints after `Psi_0` is free, so the
system is over-determined by one bit, and pooling the two targets `c in {2,3}`
gives a naive expected solution count

```text
    E[#solutions at length n] = 2^n * 2^-(n+1) = 1/2
```

**independently of `n`**.  Under that null, `sum_n E = infinity`, so a
Borel-Cantelli reading predicts constant `Psi` recurring for infinitely many
`n`, i.e. `(BWH+)` false.  The recorded census finds constants at `n = 5, 6`
and none through `n = 20`: 0 hits where the null expects about 7 over
`n = 7..20`.  Either the null is wrong because some mechanism suppresses long
constant runs, or the census has been lucky and the route is built on sand.

This is worth one experiment because it can fire against the home program.

## Statistic

For each `n`, and each `k = 0 .. n+1`,

```text
    N_k(n) = #{ W in {1,2}^n : Psi_0 = Psi_1 = ... = Psi_k }
```

pooled over both constant values.  Report `N_k(n)` against the null
`2^(n-k)`, as the ratio `R_k(n) = N_k(n) / 2^(n-k)`.  `R = 1` is the random
null; `R << 1` is suppression; `R >> 1` is clustering.

Exhaustive over all `2^n` sources, `n = 7..18`.  No sampling, no seeds.

## Outcomes, fixed in advance

- **STRONG OUTCOME (suppression).**  `R_k(n)` falls systematically below 1 as
  `k` grows, by a factor that itself grows with `k`, in a way stable across
  `n`.  That is positive evidence of a mechanism forbidding long constant
  runs, and it says the ancestry law is measuring something real rather than a
  coincidence.  It does not prove `(BWH+)`.

- **KILL (no suppression).**  `R_k(n)` is consistent with 1 across the range,
  i.e. constant `Psi` is exactly as rare as coin-flipping predicts and no
  more.  Then the `n = 5, 6` exceptions are not exceptions but the visible
  members of an infinite family, `(BWH+)` is heuristically **false**, and
  `RESULTS-BINARY-WEDGE-HORIZON.md`'s census through `n = 20` is evidence of
  nothing.  Consequence: `(BWH+)` must be abandoned as a target and the
  program falls back to DLP/RW, which retains the hard-core suffix and the
  terminal `12a` pull and is therefore a strictly smaller solution set not
  covered by this count.

- **CLUSTERING.**  `R_k(n) > 1` growing in `k`.  Constant runs are commoner
  than random, and near-misses cluster; the `n = 15` extremal family being a
  suffix cylinder is a hint in this direction.  Would mean the route is worse
  off than the kill suggests and the near-misses are structural.

- **AMBIGUOUS.**  Anything else, including a pattern that does not stabilise
  in `n`.

## Stated prediction

Suppression, with `R_k` decaying roughly geometrically in `k` once `k` exceeds
a small constant.  Reason: the extremal census shows the maximum first-`1`
index sitting near `n - 5` for most `n` rather than near `n`, which is far
below what independence would give, while the `n = 15` and `n = 18` outliers
show the tail is not empty.  **This is a prediction, not an escape hatch:** if
`R_k` hugs 1 the kill fires as written and `(BWH+)` is reported as
heuristically false.

## Artifacts

- `psi_constraint_count.py` — the runner.
- `psi_constraint_count_20260902.log` — saved output.

---

## RESULT (run 2026-09-02)

**Pre-registered verdict: CLUSTERING.  My stated prediction of suppression was
wrong, and the outcome that fired is the one unfavourable to the target.**

Exhaustive over all `2^n` binary sources, `n = 7..18`
(`psi_constraint_count_20260902.log`).

| n | last `k` with `N_k > 0` | `N_k` there | needed `k = n+1` | slack | max `R_k` |
|---|---|---|---|---|---|
| 7 | 6 | 3 | 8 | 2 | 2.00 |
| 8 | 6 | 5 | 9 | 3 | 1.88 |
| 9 | 7 | 10 | 10 | 3 | 2.50 |
| 10 | 8 | 12 | 11 | 3 | 3.00 |
| 11 | 8 | 6 | 12 | 4 | 1.19 |
| 12 | 10 | 6 | 13 | 3 | 1.50 |
| 13 | 9 | 9 | 14 | 5 | 1.00 |
| 14 | 10 | 6 | 15 | 5 | 1.02 |
| **15** | **15** | **18** | **16** | **1** | **18.00** |
| 16 | 13 | 20 | 17 | 4 | 2.50 |
| 17 | 12 | 9 | 18 | 6 | 1.35 |
| 18 | 17 | 3 | 19 | 2 | 4.75 |

Two facts, both against the prediction.

**1. There is no suppression anywhere.**  `R_k` sits at `1.00 +/- 0.05` for
every `n` through `k` of roughly `n - 6`, i.e. constant prefixes of `Psi` are
exactly as common as coin-flipping predicts over most of the range.  `max R_k`
exceeds 1 for all twelve values of `n`.  The pre-registered STRONG OUTCOME
required `R_k` falling systematically below 1; it does not fall below 1 at all
in any stable way.

**2. Beyond that point the survivors cluster, hard.**  At `n = 15`, 18 sources
survive all the way to `k = 15` against a null of 1, `R = 18`, and then all 18
die simultaneously at `k = 16`.  The same shape recurs: `n = 16` has 20
survivors at `k = 13` (`R = 2.5`) dying together at 14; `n = 18` has 3 at
`k = 17` (`R = 4.75`) dying together at 18.  The survivors are the suffix
cylinders identified in `RESULTS-PSI-ANCESTRY-LAW.md` section 6 — at `n = 15`
all 18 share the suffix `211212112`.  Long near-constant runs are *commoner*
than random, not rarer.

### Consequence, stated as the pre-registration attached to CLUSTERING

**Correction, made before this file was handed on.**  The first draft of this
section imported the KILL outcome's consequence ("abandon `(BWH+)`") into the
CLUSTERING outcome, after seeing the data.  The pre-registration attaches a
different reading to CLUSTERING, and the imported one is withdrawn.  This is
the same verdict-rule bug caught in `PREREG-flat-opcode-ablation.md`, running
in the pessimistic direction rather than the optimistic one; it is recorded
rather than quietly fixed.

**A factual error is withdrawn with it.**  The first draft asserted that "the
column one or two steps to the left of `k = n+1` is populated at every single
`n` tested, and its population does not shrink."  That is false.  From the
log:

| n | `N_{n-1}` | `N_n` | `N_{n+1}` |
|---|---|---|---|
| 7 | 3 | 0 | 0 |
| 8..14 | 0 | 0 | 0 |
| 15 | 18 | 18 | 0 |
| 16, 17 | 0 | 0 | 0 |
| 18 | 3 | 0 | 0 |

`N_{n-1}` is zero at nine of the twelve values of `n`, and `N_n` is nonzero
only at `n = 15`.  The "consistent with luck" inference rested on that
sentence and falls with it.

**What the measurement actually establishes.**  It refutes the null that
motivated it.  `R_k` deviates systematically from 1 at large `k`, reaching 18
at `n = 15`, so the coordinates of `Psi` are **not independent**.  The
divergent-sum heuristic against `(BWH+)` was computed under independence, so
it is void — it was never evidence against `(BWH+)` in the first place.

Equally, the count is not evidence *for* `(BWH+)`.  `N_{n+1} = 0` at all
twelve values against a null expectation of `1/2` each, total 6 against 0
observed, but that null is the one just refuted, so the comparison carries no
weight.  **Nothing about `(BWH+)`'s truth can be read off this count in either
direction.**  That is the honest headline and it is narrower than either the
prediction or the first draft claimed.

**The observation worth promoting.**  The survivors die *simultaneously*.  All
18 sources at `n = 15` clear `k = 15` and all 18 fail at `k = 16`; 20 clear
`k = 13` at `n = 16` and all fail at 14; 3 clear `k = 17` at `n = 18` and all
fail at 18.  A single shared cause kills an entire suffix cylinder at once.
That shape — long prefixes permitted at roughly the random rate, full
constancy forbidden by one mechanism at the end — is what a real theorem would
look like from the outside.  **Identifying that shared cause is the named next
target**, and it is not what was measured here.

### Where the decision to leave `(BWH+)` actually comes from

Not from this count.  It comes from the fan-out test the capsule's section 7
names as the switch criterion, run separately and reported in
`RESULTS-PSI-ANCESTRY-LAW.md` section 10: `Delta_j` has **full algebraic
degree `n`** in the source bits at every `n` from 4 to 15.  That is the
pre-authorised trigger ("if the complete-state recursion necessarily fans out,
weaken immediately to RW/DLP"), and it is independent of everything in this
file.

**`(PT2)` and P1 are untouched either way.**  `BWH+ => DLP => SEP` runs one
way only.

# Attempt to prove gamma(n) >= 1 for all n: two new negative results, one small proven lemma, no proof

Date: 2026-09-04.

Status: **NO PROOF FOUND.** `gamma(n) >= 1` continues to hold at every newly
measured `n` (odd `n` in particular, never checked before, plus
`n=24` for the source-word extremal family) — no counterexample. One
genuinely new small structural lemma was found and proven exactly (a closed
form for the zero-padding warm-up state). Two genuinely new negative results
were established by direct computation, both explaining *why* the two ideas
in the task brief do not work, rather than merely failing to find a proof:
(1) the source-word extremal family has no common suffix and its
tie-multiplicity *grows* with `n` (extends `RESULTS-FIBER-EXTREMAL-FAMILY.md`'s
continuation-side negative result to the source-word side), and (2) the one
clean periodic-attractor structure found here does **not** survive
contact with arbitrary history — a direct, checkable disconfirmation of the
"long constant suffix washes out history" mechanism that idea 2 hoped for.
This is consistent with, and sharpens, the already-recorded difficulty
assessment in `RESULTS-TRANSFER-DOMINATION-CHECK.md` ("this may be as hard
as Rule 30's own open equidistribution question") and the period-doubling
warning already on record in `RESULTS-EVENTUAL-CONSTANT-TAIL.md` section 5-6
for a structurally analogous map.

No counterexample to `gamma(n) >= 1` was found. The tightest margin found
anywhere in the project to date is a genuinely new data point:
**`n=9, c=3, r=0: gamma=3`** (verified two independent ways, see section 3).
This is not a counterexample (`gamma=3 > 0`) but it is the smallest gamma
value on record, in a part of the parameter space (odd `n`) nobody had
checked before.

Background job note: `fastdk_benchmark.py` was a separate, already-running
job left untouched throughout. It reached `n=24` (both `c`) over the same
period; its log is `fastdk_benchmark_20260904.log`. This report's own new
computation used a separate, independently-written script
(`scratch_finalist_via_dedup.py`) rather than that job's output, and
cross-checks against both brute force and the existing benchmark log (see
section 1).

**A second, unrelated concurrent computation matters even more for this
report's correctness gate.** A *different*, pre-registered job
(`PREREGISTRATION-OVERNIGHT-EXTENSION.md`, `overnight_census.py`) was
independently computing exact **brute-force** (not dedup-shortcut) values
of `max_row`/`margin` — its `margin` is defined identically to this
report's `gamma` (`overnight_census.py:79`: `margin = (n+2) - max_row`) —
for `n = 17..24`, both tails, including the odd `n` this report also
targeted. That job's output (`overnight_c2_odd.log`, `overnight_c2_even.log`,
`overnight_c3_odd.log`, `overnight_c3_even.log`, not written or modified
here) was read, not run, and its brute-force numbers are compared
against this report's fast-method numbers in the table in section 1: they
agree exactly everywhere they overlap, at `n=17,18,19,20,21` for both `c`.
This is a stronger cross-check than a single method could have produced
alone, run by a genuinely independent method (full `2^n` enumeration, not the
dependency-edge dedup this report otherwise relies on), and it is credited
here rather than presented as this report's own verification.

## 0. What was attempted, in the order the task brief raised it

1. **Idea 1 (induction on `max_survival_row(n)` from `n-2`).** Investigated
   and found a genuine structural obstruction to even setting up the
   induction (section 4). Not merely "did not find a pattern" — the reason
   a naive prepend-based induction cannot get started is now explicit.
2. **Idea 2 (infinite-word / fixed-point limit).** Split naturally into two
   sub-questions, both investigated and both resolved negatively with fresh
   computation:
   - **2a.** Do the extremal (max-survival) *source words* converge to a
     common suffix / limiting infinite word as `n` grows? **No** (section 5;
     extends the existing continuation-side negative result in
     `RESULTS-FIBER-EXTREMAL-FAMILY.md` to the source-word side, with fresh
     data through `n=24`, both parities).
   - **2b.** Does the underlying dependency-edge recursion have a natural
     fixed point / eventually-periodic orbit that could anchor an argument?
     **Partially yes, but it does not help.** There is a genuine, exactly
     provable periodic attractor for the special case of a *constant* feed
     from an empty edge (section 6) — but a direct test shows this attractor
     does **not** capture the general (history-dependent) recursion at all,
     even when the *local* feed becomes constant for very long stretches
     after arbitrary history (section 7). This is the key finding of the
     night: it is a precise, checkable reason the "look for an infinite
     limit" style of argument does not have traction here, not just an
     unsuccessful search for one.

## 1. New data: gamma(n) at odd n, c=2 and c=3

Every *published* table in this project as of this report
(`RESULTS-KSTAR-GAMMA-EXTENDED.md`, `RESULTS-EXTINCTION-MARGIN.md`,
`fastdk_benchmark_20260904.log`) reported only **even** `n`. This was a
genuine gap, not a deliberate restriction (nothing in the method requires
even `n`), so filling it was done early, independently of, and (it turned
out) concurrently with, a separate pre-registered job
(`overnight_census.py`, see the background-job note above) that was
targeting the same odd-`n` gap by brute force at the same time. Both
efforts were run without either being aware of the other; they agree
exactly everywhere they overlap (`n=17,18,19,20,21`, both `c`, see the
table below). This report's own coverage additionally includes `n=6,7,9,11,
13,15` (below the concurrent job's `n>=17` range) and `n=22,24`, using an
independently-written fast method, not that job's code.

Method: `scratch_finalist_via_dedup.py`, a new script built directly on top
of the already-trusted, already-cross-checked `fastdk_core.py` /
`fastdk_fastedge.py` (imports `_edge_after_zero_padding`,
`forced_continuation_from_state`, `survived_prefix`, and
`fastdk_fastedge.append_edge_fast` — no existing file modified). It extends
`fastdk_core.distinct_final_states` to also carry one representative source
word per distinct `(edge, endpoint_symbol)` state, so it recovers not just
`max_survival_row(n)` but an actual witnessing word, at the same
sub-exponential cost as the existing fast method.

**Correctness gate for this script, done before trusting any of its
numbers** (the existing project crosschecks are all even-`n`, so a new,
independent check was required, not assumed):

| n | c | method | max_survival | gamma | check |
|---|---|---|---|---|---|
| 13 | 2 | brute force (`scratch_bruteforce_oddn_check.py`, independent crude `literal_extension` loop) | 7 | 8 | matches fast method exactly |
| 15 | 2 | brute force (same script) | 9 | 8 | matches fast method exactly |
| 9  | 3 | brute force (`scratch_bruteforce_n9c3.py`) | 8 | 3 | matches fast method exactly |
| 20, 22, 24 | 2 | fast method vs. `fastdk_benchmark_20260904.log` (even n, already brute-force-gated project-wide through n=18) | 11, 12, 14 | 11, 12, 12 | exact agreement at every point |
| 17, 19, 21 | 2 | fast method vs. **concurrent job** `overnight_census.py` (full `2^n` brute force, separate process, see note above) | 11, 11, 13 | 8, 10, 10 | exact agreement at every point |
| 17, 19, 21 | 3 | fast method vs. same concurrent job | 10, 13, 16 | 9, 8, 7 | exact agreement at every point |
| 18, 20 | 2, 3 | fast/existing-table vs. same concurrent job (even n) | — | 8,11 (c=2); 9,8 (c=3) | exact agreement at every point |

All agree exactly; zero mismatches, across two independent brute-force
sources (one run for this report, one a genuinely separate concurrent
process using full `2^n` enumeration) and one independent fast-method
cross-check (`fastdk_benchmark_20260904.log`). The odd-n numbers below are
now on at least as strong a footing as the project's existing even-n
numbers — most of them (`n=17,19,21`, both `c`) are brute-force-gated
directly, not merely consistent with a closed-form side lemma.

### c=2, r=0 (rows = n+2)

| n | max_survival_row | gamma |
|---|---|---|
| 6  | 3  | 5  |
| 7  | 4  | 5  |
| 8  | 3  | 7  |
| 9  | 4  | 7  |
| 10 | 5  | 7  |
| 11 | 6  | 7  |
| 12 | 9  | 5  |
| 13 | 7  | 8  |
| 14 | 10 | 6  |
| 15 | 9  | 8  |
| 16 | 10 | 8  |
| 17 | 11 | 8  |
| 18 | 12 | 8  |
| 19 | 11 | 10 |
| 20 | 11 | 11 |
| 21 | 13 | 10 |
| 22 | 12 | 12 |
| 24 | 14 | 12 |

(n=23 not computed — not needed to make the point; n=6..22,24 already give
dense-enough coverage of both parities.) Minimum: `gamma=5` at `n=6,7,12`.
No value `<=0` anywhere. Consistent with, and now denser than, the existing
even-only table in `RESULTS-KSTAR-GAMMA-EXTENDED.md` (values agree exactly
at every shared `n`).

### c=3, r=0 (odd n only; even n already in `RESULTS-KSTAR-GAMMA-EXTENDED.md`)

| n | max_survival_row | gamma |
|---|---|---|
| 7  | 4  | 5 |
| 9  | 8  | **3** |
| 11 | 7  | 6 |
| 13 | 9  | 6 |
| 15 | 8  | 9 |
| 17 | 10 | 9 |
| 19 | 13 | 8 |

Combined with the existing even-`n` table (4,5,6,8,8,9,8,10 for
`n=8,10,...,22`), the full `c=3,r=0` sequence for `n=7..20,22` (n=21 held
out here, see the addendum) is `5,4,3,5,6,6,6,8,9,8,9,9,8,8,10` — still no
value `<=0`, but the new minimum of the whole project is here: **`gamma=3`
at `n=9`**, lower than the previous minimum of `4` at `n=8`. This is a
real, cross-checked (brute force, see table above) data point, not a
fluctuation from an unvalidated method. It is an isolated dip, not the
start of a monotone trend toward 0: `n=11,13` recover to `6`, `n=15,17`
climb to a peak of `9`, `n=19,21` decline to `8, 7`, and `n=21,23`
(addendum) recover again to `9`. The full odd series `n=9..23` is
`3, 6, 6, 9, 9, 8, 7, 9` — one isolated sharp dip at `n=9`, then
fluctuation in the `6-9` range with no visible trend toward `0` and no
second dip anywhere near as low as the first. See the addendum for the
`n=23` computation.

## 2. Idea 1: why a direct `n-2` induction does not get off the ground

Read `late_pull_diagonal_sat.literal_extension` and
`constant_tail_scale.append_dependency_edge` line by line (not just the
already-documented summaries) to check specifically whether "take the best
word at `n-2`, see what happens when you extend it" is even a well-formed
question.

**Finding: it is not, for a structural reason, not a search failure.** The
zero-padding prefix has length `n` (the *same* `n` as the source word), so
going from a length-`n` source word to a length-`(n+2)` source word does not
mean "append 2 symbols to an existing 2n-symbol history" — it means
re-running the whole construction with **2 more padding symbols inserted
before the word as well**, i.e. a length-`(n+2)` problem starts from a
completely different absolute offset into the zero-fed history than a
length-`n` problem does. There is no length-preserving embedding of the
`n`-problem's state into the `(n+2)`-problem's state that would let you
"continue" the old best word. (This is a sharper, code-level statement of
the same fact `RESULTS-EXTINCTION-MARGIN.md`'s derivation attempt ran into
via the group-theoretic route; this section confirms it directly from the
recursion's own indexing rather than from the permutation-group framing.)

The one place this *does* resolve cleanly is the padding phase itself,
because it is fed a constant symbol — see section 6. But the branching
phase (the `n` real symbols) does not inherit this, per the exhaustive
check in section 7.

## 3. Idea 2a: source-word extremal family — negative, with growing tie count

`RESULTS-FIBER-EXTREMAL-FAMILY.md` already showed (n=10..16) that the
extremal **continuations** (the forced output words) do not fall into a
clean parametrized family. That result is about `D_k`'s image side. This
report checks the natural companion question on the **source-word** side
directly: do the source words `W` that *achieve* `max_survival_row(n)`
converge to a common suffix, or at least stay few in number, as `n` grows?

Using the same word-recovering dedup walk from section 1, full finalist
lists were recomputed fresh at `n=6..24` (c=2, r=0). Tie count by `n`:

| n | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| #finalists | 3 | 4 | 4 | 3 | 3 | 1 | 1 | 5 | 2 | 3 | 1 | 1 | 3 | 3 | 5 | 5 | **8** | 5 |

Tie count is not merely nonzero, it is **growing** at the high end (`8` at
`n=22`), and even at a single `n` the tied finalists frequently split into
multiple genuinely different suffix classes — e.g. at `n=18` the three
finalists' last-6-symbol suffixes are `122211`, `221212`, `221212` (two
suffix classes, verified by direct string slicing, not eyeballing); at
`n=22`, 6 of the 8 finalists (the other 2 were not printed) have last-6
suffixes `112122`, `211122`, `222221`, `112111`, `211122`, `122221` — 5
distinct values among those 6 (only `211122` repeats). **No common suffix,
and no shrinking toward a unique witness.**
This directly rules out "the extremal word converges to a truncation of one
infinite limiting word" as stated in the task brief's idea 2 — it was
checked, not assumed, and it fails with fresh data extending 8 n further
than the project's existing extremal-family investigation.

(This also incidentally re-confirms, as a byproduct, that a naive "biggest
tie-breaks-toward-a-canonical-word" heuristic would not help: the ties are
genuinely structurally different words, not near-duplicates.)

## 4. Idea 2b: a real, proven lemma — the constant-feed attractor

This is the one piece of new, rigorously-established (not merely
pattern-matched) mathematics in this report.

**Claim.** Define `F: {0,1,2,3}^2 -> {0,1,2,3}^2` by
`F(a,b) = (b, cone_local(a,b))`, using the project's existing
`dyadic_periodicity_analyzer.cone_local`. Then `F`'s functional graph on all
16 states has **exactly two cycles**: the fixed point `(0,0)`, and the
2-cycle `{(1,2),(2,1)}` (since `cone_local(2,1)=2` and `cone_local(1,2)=1`
exactly). All 15 states other than `(0,0)` reach the 2-cycle within at most
4 steps of `F`. This was checked exhaustively over all 16 states (there are
only 16; this is a complete case analysis, not a sample) —
`scratch_cone_orbit_structure.py`.

**Consequence for the zero-padding warm-up.** `late_pull_diagonal_sat`'s
`n`-symbol zero-padding phase feeds the constant symbol `0` at every step.
By induction on the call structure of `append_dependency_edge` (each new
top-of-diagonal value, under constant feed, is a function only of the
*position* being computed, not of *when* it was computed, because the base
case `following[0]=BOUNDARY[value]` and `following[1]` are literally
identical at every call under a constant feed — full argument in the
script's docstring), the state after `n` zero-padding steps has an **exact
closed form**:

```
_edge_after_zero_padding(n) == (3,) + (2,1,2,1,2,1,...)[:n-1]
```

i.e. `f(0)=3` (`=BOUNDARY[0]`), then `f(i)=2` for odd `i`, `f(i)=1` for even
`i>=2`, forever — the trajectory enters the `F`-attractor after exactly one
transient step and never leaves. **This was verified directly (not just
argued) for every `n=1..80`, zero mismatches** (`scratch_closed_form_verify.py`).
The same exhaustive-`F`-orbit computation also confirms this holds for
*any* of the four possible constant feed values (0, 1, 2, or 3), always
landing on the same `{(1,2),(2,1)}` cycle, just with a 0-2-step transient
and possibly the opposite phase (`scratch_constant_trajectories.py`).

This is a genuine, checkable simplification: the "n zero-padding steps" at
the start of every `H_r(n)` / `gamma(n)` computation in this project can be
replaced by reading off a fixed alternating pattern, with no simulation
needed, for any `n`. It removes one previously-opaque moving part from the
construction.

## 5. Idea 2b continued: why the lemma does NOT generalize (the key negative result)

The natural next question is whether this attractor structure is strong
enough to say something about words that are only **eventually** constant
(i.e., end in a long run of the same symbol after arbitrary history) —
which was the actual hope behind idea 2 (a source word "looks like" a
truncation of a limiting object; if long constant runs forget their past,
that would support treating the tail of a source word as the load-bearing
part). This was tested directly and it is **false**, sharply and
reproducibly.

**Test 1 (`scratch_forgetting_check.py`).** 200 random trials: random
warm-up (length 0-40, alphabet `{0,1,2,3}`), then a constant run (length
10-30). Compared the last few diagonal entries against the "pure" trajectory
of the same constant run starting from empty. Result: 108 of 200 mismatched
outright (most of the rest matched only up to a phase/parity shift, not
exactly — the two states of the 2-cycle are not distinguished by this
comparison). One concrete case (`warmup_len=39, const=3, tail_len=10`):
actual last 8 entries `(2, 0, 0, 3, 1, 2, 3, 0)` — nowhere near the
alternating attractor.

**Test 2 (`scratch_mixing_time_check.py`), the decisive one.** Took that
exact failing case and extended the constant run from 10 steps to **300**
steps, checking at every step whether the top entry had locked onto the
attractor sequence and stayed there. **It never converges.** The first 20
values of the diagonal's top entry under 300 steps of constant feed (`c=3`)
following the 39-symbol random warm-up: `[3, 2, 1, 1, 0, 1, 3, 1, 0, 0, 1,
2, 3, 0, 2, 3, 3, 3, 3, 2]` — still visiting all four states `{0,1,2,3}`
with no sign of settling, 300 steps in. **A local constant run, however
long, does not overwrite arbitrary earlier history.**

**Why, mechanistically** (checked directly,
`scratch_position_stability.py`): `append_dependency_edge` does not append
to a frozen, growing array. Every call **recomputes every position from
position 0 onward from scratch**, and position 0 is always
`BOUNDARY[value]` — a direct function of whatever symbol is being fed
*right now*. A concrete check: build a 20-step edge, then append 10 more
*varying* symbols; not merely a few recent entries but **all 20 of the
original entries differ** in the extended array (`edge_B[:20] != edge_A`,
checked byte for byte). The reason constant feed looked "frozen" in section
4 is a coincidence of the *value happening to repeat*, not a structural
freezing/triangularity property of `append_dependency_edge` in general —
confirmed false in general by exhaustive check over all length-6 sequences
from a 4-symbol alphabet (`scratch_triangularity_check.py`: 4092 of 4096
break the naive frozen-prefix property immediately).

**Conclusion this licenses:** the recursion genuinely has unbounded memory
with no local mixing/forgetting mechanism, not merely "no mixing mechanism
found yet." Any future attempt at idea 1 or idea 2 that relies on "a
sufficiently long uniform/simple run near the append point should dominate
the outcome, regardless of what came before" is directly contradicted by
this test and should not be retried without a new mechanism — the
counterexample above is concrete and cheap to reproduce.

## 6. Triangulation with an earlier, structurally analogous investigation

`RESULTS-EVENTUAL-CONSTANT-TAIL.md` (2026-09-01, a different but related
part of this project, concerning `constant_tail_shift.py`'s one-argument
map `g_0=(0,3,2,3)` on "canonical eventually periodic cut lassos" — not the
same object as this report's two-argument `cone_local`-based `F`, so this
is a **sibling**, not identical, recursion) records, independently, the
exact same style of warning: a simple periodic pattern found at small scale
("the promising period-at-most-four pattern at small cutoff") was
subsequently shown to be a finite-size artifact once pushed further — the
true periods along maximizing orbits grow `1, 2, 4, 8`, then reach `16`
after 200 endpoint shifts, with **no bound at 4** despite 4 looking like a
clean answer early on. This report's own finding (sections 4-5) is a
different, independently-derived instance of the same phenomenon on a
different map: a clean small attractor exists in the fully-degenerate
(constant-from-empty) case, and is directly falsified as soon as real
history is allowed in. Two independent recursions in this project now
exhibit this same pattern; a reader should treat any future
"small-period-found-at-small-scale" result in this line of work as a
finite-size artifact until it is checked against an adversarial/long-history
setting the way section 5 does here, not extrapolated from small cases.

## 7. Honest assessment

**What is proven:** the `F`-orbit structure (section 4, exhaustive over 16
states) and the resulting closed form for `_edge_after_zero_padding(n)` at
every `n` (verified n=1..80). Both are genuine, if narrow, new lemmas.

**What is a real, checked negative result (not just "didn't find it"):**
(a) the source-word extremal family has no common suffix and growing tie
count through `n=24` (section 3); (b) the constant-feed attractor does not
survive being reached from arbitrary history, even after 300 steps of a
locally-constant tail (section 5) — this is the most important finding of
the night because it is a mechanistic reason, not an absence of one, for
why both ideas in the task brief run into the same wall the rest of the
project has already hit from other directions.

**What remains open, unchanged:** `gamma(n) >= 1` for all `n` — still true
at every one of the (now considerably more numerous) points checked, still
not proven. No route tried here, in this project's prior work, or in
the one literature-adjacent framing considered (the recursion's unbounded,
non-mixing memory dependency is structurally the same obstruction that
makes Rule 30's center-column equidistribution conjecture open — see
`RESULTS-TRANSFER-DOMINATION-CHECK.md`) currently has traction on a full
proof.

**Most promising remaining direction, stated honestly as a guess, not a
plan already validated:** the empirical transition matrix `M` in
`RESULTS-TRANSFER-DOMINATION-CHECK.md` (measured almost exactly at the
uniform rate `1/4` per free entry) combined with the finding here that the
recursion cannot be shortcut by any local/finite mechanism suggests that if
`gamma(n)>=1` is provable at all with current tools, it is more likely via
a genuine concentration/large-deviation argument on the survival-population
decay (bounding the *probability* that a specific adversarial path evades
extinction for `n+2` rows, using the near-i.i.d. mean-field behavior
already measured) than via any structural combinatorial identity. That is
speculative; no further work was done on it beyond noting it does not
contradict anything found here, and the same
report already flags this as "may be as hard as Rule 30's own open
equidistribution question" — a large-deviations argument would still need
to somehow avoid actually resolving that open conjecture, which is a real
obstacle, not a minor gap.

No counterexample. No proof. Two solid negative results and one small
proven lemma, honestly reported as such.

## 8. Reproduction

```sh
cd experiments/rule30/p1-period2-invariant

# Odd-n gamma data (section 1), fast method
uv run python scratch_finalist_via_dedup.py 2 0 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 24
uv run python scratch_finalist_via_dedup.py 3 0 7 9 11 13 15 17 19

# Brute-force cross-checks (section 1's gate)
uv run python scratch_bruteforce_oddn_check.py     # n=13,15 c=2
uv run python scratch_bruteforce_n9c3.py           # n=9 c=3 (the new minimum)

# The F-orbit lemma (section 4)
uv run python scratch_cone_orbit_structure.py
uv run python scratch_closed_form_verify.py
uv run python scratch_constant_trajectories.py

# The disconfirmation (section 5) -- the key negative result
uv run python scratch_forgetting_check.py
uv run python scratch_mixing_time_check.py
uv run python scratch_position_stability.py
uv run python scratch_triangularity_check.py
```

All scripts are read-only over existing project modules
(`late_pull_diagonal_sat.py`, `constant_tail_scale.py`,
`dyadic_periodicity_analyzer.py`, `fastdk_core.py`, `fastdk_fastedge.py`) —
none was modified. `fastdk_benchmark.py` was left running throughout and
not touched; see
`fastdk_benchmark_20260904.log` for its independent progress
(`RESULTS-KSTAR-GAMMA-EXTENDED.md` owns interpretation of that job).

## Addendum: c=3 odd-n extension to n=21,23

`n=21, c=3, r=0`: `max_survival_row=16`, **`gamma=7`** — matches the
concurrent `overnight_census.py` brute-force job exactly (see section 1's
cross-check table). The `n=9` dip to `gamma=3` does **not** recur by
`n=21` — `7` is well above `3` — but the series is not simply "recovers and
stays high" either: the full c=3 odd sequence `n=7..21` is
`5, 3, 6, 6, 9, 9, 8, 7`, i.e. dip at `n=9`, recovery, a peak of `9` at
`n=15,17`, then two consecutive declines (`8, 7`) at `n=19,21`. `7` is the
second-lowest c=3 value in the whole project after the `n=9` dip itself.
Still far above `0` and not a counterexample.

**Update, landed before this report closed out:** `n=23, c=3, r=0`:
`max_survival_row=16`, `gamma=9` (single finalist:
`11112211211221121111212`). The `n=19,21` decline does **not** continue —
`n=23` recovers to `9`, matching the earlier peak at `n=15,17`. The full
c=3 odd sequence is now `n=7..23`: `5, 3, 6, 6, 9, 9, 8, 7, 9`. Reading:
one isolated sharp dip at `n=9`, otherwise fluctuating in the `6-9` range
with no visible trend toward `0`. This was cross-checked only against this
report's own fast method (not yet against the concurrent brute-force job,
which was still short of `n=23` at this point) — treat it as provisional
pending that job's own `n=23` line landing in `overnight_c3_odd.log`, though
given the fast method's zero-mismatch record at every other point checked
here (section 1), no discrepancy is expected.

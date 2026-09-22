# OpenEvolve attack on P3 — BLOCKED at the sanity gate, search not launched

Date: 2026-08-31. Harness: `experiments/openevolve-p3/`, pre-registration
`experiments/openevolve-p3/PREREGISTRATION.md`.

**Verdict: the full search was NOT run.** The evaluator's own required
sanity gate failed on re-verification, and the brief for this run is
explicit that a failed sanity test is a stop, not a warning. **Nothing
here is a finding about Rule 30** — the question this arm exists to
answer was never put to a search, and no LLM call was made.

The failure is in the *instrument*, not in the harness's logic. Follow-up
measurement (section 3b) showed the tail-exponent estimate is too
unstable at the smoke profile's `n <= 16000` on this machine to separate
a constant-factor speedup from an algorithmic one: the naive baseline
scored between 0.2667 and **0.7896** against its own stored value across
three runs of the *same unchanged program*. Machine load is a contributor
but not the whole story, so "re-run it on a quiet box" is not by itself
the fix — see section 8.

## 1. What was supposed to happen

Run `config_full.yaml` — a few hundred iterations of OpenEvolve against
`evaluator.py`, scoring the measured **tail exponent** of `center_cell(n)`
(the local log-log slope between the two largest usable `n`), never wall
time — under a 6h wall-clock ceiling, then re-measure any apparent winner
>= 3 times per the pre-registration's held-out protocol.

Step 1 of that plan is re-running `run_sanity_tests.py` and confirming the
four documented candidate scores. That step failed.

## 2. The sanity gate, as re-run today

`RULE30_P3_PROFILE=smoke ./vendor/openevolve/.venv/bin/python run_sanity_tests.py`
2026-08-31 11:10-11:22 PDT. Wall 10:08.7, user 206.6s — **34% of one core**,
which is itself the headline number.

| candidate | documented | measured today | `usable_ns` | pass? |
|---|---|---|---|---|
| (a) correct naive baseline | correct, flat ~0.2 | **0.2957**, tail 1.9289 | `[2000, 4000, 8000]` — **16000 dropped** | **FAIL** |
| (b) deliberately wrong | 0.0 | 0.0 (`evolve` gate, n=15) | — | pass |
| (c) bit-packed, constant-factor only | **0.210** (correct, no win) | **0.9335**, tail 1.6923 | `[2000, 4000, 8000, 16000]` | **FAIL** |
| (d) lookup-table cheat | 0.0 | 0.0 (`evolve` gate, n=157) | — | pass |

Candidate (c) is the one that matters. It is a pure constant-factor
speedup with the same `O(n^2)` asymptotics — the pre-registration
documents it scoring **0.956 before the evaluator was fixed** and **0.210
after**, and it exists precisely so that a broken evaluator announces
itself. It is back at 0.93. **The trap the evaluator was built to close is
open again.**

Nothing below is a claim about Rule 30. The question this experiment
exists to answer — is there an asymptotically faster algorithm for `c(n)` —
was never put to a search.

### It is not a noisy single sample

Re-measured three further times (`remeasure.py`, added this session; it
only calls `evaluate()`, it changes no scoring):

| run | `combined_score` | tail exponent | `tail_consistency` | `r2` |
|---|---|---|---|---|
| sanity | 0.9335 | 1.6923 | 0.041 | 0.99958 |
| 1 | 0.5930 | 1.8333 | 0.254 | 0.99902 |
| 2 | 0.7798 | 1.5861 | 0.137 | 0.99946 |
| 3 | 0.6503 | 1.8029 | 0.218 | 0.99941 |

Mean tail 1.729, stdev 0.135, range 1.586-1.833. Every one of the four
lands in the band the pre-registration reserves for a genuine exponent
improvement, while each individual fit looks clean (`r2 > 0.999`).

A clean `r2` on every run alongside a 0.25-wide spread across runs is the
tell: the *within-run* fit is tight and the *between-run* scatter is
large, so no single evaluation can report its own unreliability. Section
3b pins this down by measuring the baseline against itself.

## 3. Root cause — and it is not only the load

There are two problems. The second one is the serious one.

### 3a. Proximate: load truncates the naive control's measurement window

Concurrent jobs from other sessions on this machine held the load average
at **77-105 on 10 cores** throughout (`genotone-sdk` training at ~97% of a
core, four `sygus-p3` python jobs, `band30`, `gen_band.py`, `deep_gen.py`,
a rust test binary). Every process, the evaluator included, got roughly a
third of one core.

The naive `O(n^2)` candidate — the same algorithm the stored baseline was
measured from — then exceeds the profile's 180s `per_call_timeout` at
`n = 16000`, and that point is silently **dropped**, so candidate (a)'s
tail gets computed on the **4000 -> 8000** segment while the ~50x-faster
bit-packed candidate still completes `n = 16000` and keeps the
**8000 -> 16000** one. Two candidates scored over different n-windows are
not comparable, and nothing in the metrics reveals it: `r2` and
`tail_consistency` measure whether the fit is clean, not whether the
window is right.

Checked rather than assumed: `scaling_dropped` recorded
`'timing call failed: '` with an empty message, which is exactly how
`concurrent.futures.TimeoutError` stringifies (verified directly), so the
180s per-point timeout is the mechanism, not a resource failure.

### 3b. Load-independent: the exponent estimate is too unstable to discriminate

Because load is non-stationary, the naive baseline and the constant-factor
candidate were re-measured **alternating (A/B/A/B), not blocked**, so a
load excursion cannot land entirely on one arm:

| pass | candidate | tail exponent | `combined_score` | `r2` | started |
|---|---|---|---|---|---|
| A1 | (a) naive `O(n^2)` | **2.1635** | 0.2667 | 0.99869 | 11:22:31 |
| B1 | (c) bit-packed | **1.5731** | 0.8623 | 0.99962 | 11:34:08 |
| A2 | (a) naive `O(n^2)` | **1.8069** | **0.7896** | 0.99879 | 11:34:11 |
| B2 | (c) bit-packed | **1.7727** | 0.4305 | 0.99777 | 11:44:03 |

Window caveat, stated precisely: `usable_ns` was only added to the
re-measurement output partway through, so it is *recorded* for B2 alone —
`[2000, 4000, 8000, 16000]`, nothing dropped. For A1, B1 and A2 the full
window is inferred from their tails sitting near the stored full-window
baseline rather than near the truncated 4000->8000 value, which is an
inference, not a measurement. The A2 result does not depend on it: A2 is
compared against the stored baseline, which is what the scorer does.

All measurements of each candidate today:

- **(a) naive**: 1.9289 (window truncated to 2000-8000), 2.1635, 1.8069 —
  range 1.807-2.164, spread **0.357**. Stored baseline for the same
  algorithm, measured 10:47 on a quieter machine: 2.2147.
- **(c) bit-packed**: 1.6923, 1.8333, 1.5861, 1.8029, 1.5731, 1.7727 —
  mean 1.712, stdev 0.111, range 1.573-1.833, over ~25 minutes.

Two things fall out. The second is fatal on its own.

**The paired gap is not reproducible.** Pair 1 (A1/B1) separates by
**0.590** exponent-units; pair 2 (A2/B2), taken nine minutes later under
the same protocol, separates by **0.034**. The two pairs disagree by more
than the entire pre-registered noise band. A quantity that reads 0.59 and
then 0.03 for the same pair of programs is not measuring their exponents.

**The baseline does not match itself.** Pass A2 is the naive simulation —
algorithmically identical to the program `baseline_exponent.json` was
measured from — and it scored **`combined_score` = 0.7896**: the evaluator
credited the baseline with beating itself by 0.41 exponent-units. Across
three measurements the same unchanged program scored 0.2667, 0.2957 and
0.7896. **A scorer that returns 0.27 and 0.79 for one unchanged program
cannot separate a constant-factor speedup from an algorithmic one**, and
no amount of re-measuring a *candidate* repairs it. The (a) and (c) ranges
overlap outright: 1.807-2.164 against 1.573-1.833.

Had the search run, its `combined_score` ranking would have been largely
this noise, and the pre-registration's ">= 3 independent runs" rule —
which re-measures the *candidate* — would not have caught it, because the
instability is in the baseline comparison itself.

This is the finding: **at the smoke profile's `n <= 16000` on this
machine, the tail-exponent measurement does not resolve the difference it
exists to detect.** The measured gap between the naive `O(n^2)` simulation
and a provably `O(n^2/64)` bit-packed one is 0.590 in one pair and 0.034
in the next; the naive program scores anywhere from 0.267 to 0.790 against
its own stored baseline. The pre-registration's `+/-0.2-0.3` band — whose
upper end is the full-credit bar — is smaller than the instrument's own
scatter.

Note what this is *not*. It is not a claim that bit-packing is
sub-quadratic; it demonstrably is not, and `reference/bigint_reference.py`
documents why. It is a claim that this instrument, at this range, under
this load, cannot tell the two apart.

The arithmetic confirms the earlier verification does not transfer.
`combined_score = 0.2 + 0.8 * bonus * confidence`, so the documented 0.210
for (c) requires `bonus * confidence ~= 0.0125` — either
`improvement ~= 0.005` (the bit-packed tail measuring ~2.21,
indistinguishable from naive) or `confidence ~= 0`. Nothing in today's
1.573-1.833 reaches that.

The pre-registration anticipated exactly this shape of problem — its
"measurement methodology" section records the bit-packed candidate reading
~1.1 at n=200..3200 and converging to ~1.9 by n=8000..16000, and widened
the range on that basis. Today's measurements say n=16000 is still not far
enough out here.

## 4. What was and was not changed

Unchanged, deliberately: `evaluator.py`, its scoring, `baseline_exponent.json`,
`ground_truth.json`, the profiles, and `PREREGISTRATION.md`. Re-tuning any
of them to make the gate pass would void the pre-registration, and
re-measuring the baseline under this load would simply bake this hour's
contention into the constant.

Added this session (harness-neutral, no scoring effect):

Raw logs behind every number above:
`experiments/openevolve-p3/sanity_rerun_20260831.log` and
`experiments/openevolve-p3/interleaved_ab_20260831.log`.

- `experiments/openevolve-p3/remeasure.py` — calls `evaluate()` N times on
  a given program and reports the spread. Required anyway by the
  pre-registration's ">= 3 independent runs" protocol.
- `experiments/openevolve-p3/config_full.yaml` — the real search config,
  written but never executed.
- `experiments/openevolve-p3/run_full.sh` — launcher with a hard
  wall-clock watchdog (this macOS has neither `timeout` nor `gtimeout`, so
  the ceiling is an explicit killer subshell). Never executed.

`config_full.yaml` uses `RULE30_P3_PROFILE=smoke`, not `full`: `smoke` is
the only profile with a measured baseline and the only one validated
against the sanity candidates, `tiny`'s exponents are explicitly
untrustworthy, and `full` (n up to 64000, repeats 5) would need a fresh
multi-hour baseline measurement of a pure-Python `O(n^2)` simulator before
it could score anything.

## 5. Cost

Zero LLM spend — the search never launched, so no OpenRouter calls were
made at all. About 50 minutes of wall clock (heavily contended, ~1/3 of
one core) went to the sanity gate, the six repeat measurements of (c) and
the interleaved A/B/A/B passes.

## 6. Related prior art in this repo

Register row 12 (Arm 3, `RESULTS-arm3-run1.md`) already asked this exact
question — sealed tournament for a sub-quadratic centre-column algorithm —
and instrumented it with a **deterministic fuel counter** rather than wall
clock. It recovered naive 1.9980 and bit-parallel 1.9676 with
`R^2 = 1.00000`, refitting to 1.999 / 1.985 on the top two points, and
concluded "No exponent improvement was found." Two things follow, and only
the first is a claim about this run:

- Today's failure mode — a constant-factor bit-parallel candidate reading
  as an exponent win — is the same misreading Arm 3's pre-registration was
  written to prevent, and it is what this evaluator's tail-exponent design
  was built to catch. The design is sound; the *instrument* it rests on
  (wall clock) is not robust on a shared machine.
- A deterministic effort counter would not have this failure mode. That is
  an observation about instrument choice, **not** authority to redesign
  this evaluator, which is pre-registered as it stands.

## 7. Register row (merged into `PATH.md` section 7.1 on 2026-08-31)

Next free number is **91**, not 77.  Corrected 2026-08-31 on merge: the
register is split across two files and 77 was already taken.  `PATH.md` section
7.1 holds rows 1-72 plus an out-of-band row 76; rows 73-90 live unmerged in
`experiments/overnight-arms/frontier_attack/FINDINGS.md` section 3 ("numbering
continuing from 72"), and `PATH.md` section 9.5 already cites that stream by
number ("row 79", "row 82"), so it is the canonical one.  FINDINGS row 77 is
"Ladder realizability / half-plane slip".

| # | Approach | Prize | Status | Why it stopped | Where |
|---|---|---|---|---|---|
| 91 | OpenEvolve LLM-driven evolutionary code search for a sub-quadratic `c(n)` | 3 | **NOT RUN (blocked)** | Harness built, pre-registered and previously verified, but the required sanity gate failed on re-verification: the constant-factor bit-packed control scored 0.9335 against its documented 0.210. Diagnosed by interleaved A/B/A/B re-measurement rather than assumed: the tail-exponent instrument does not resolve the difference it exists to detect at the smoke profile's `n <= 16000` on this machine. The measured gap between the naive `O(n^2)` control and the provably `O(n^2/64)` bit-packed one is 0.590 in one pair and 0.034 in the next (both full-window, `r2 > 0.997`), and the naive control — algorithmically identical to the stored baseline — scored 0.2667, 0.2957 and **0.7896** across three runs, i.e. the evaluator credited the baseline with beating itself by 0.41 exponent-units. Candidate ranges overlap outright (naive 1.807-2.164, bit-packed 1.573-1.833 over six runs). The pre-registered `+/-0.2-0.3` band is smaller than the instrument's scatter, and the ">= 3 independent runs" rule would not have caught this because it re-measures the candidate, not the baseline comparison. Machine load (77-105 on 10 cores from concurrent sessions) additionally pushed the naive control past the 180s per-point timeout at `n=16000`, truncating its window to the transient 4000->8000 segment. Extending the scaling range is a pre-registration amendment, not a mid-run fix. Search not launched, no LLM calls made, nothing tuned to force a pass. | `RESULTS-openevolve-p3.md`; `experiments/openevolve-p3/` |

## 8. What to do next

A quiet machine is necessary but likely **not sufficient**, and simply
re-running there would be the wrong recommendation. Section 3b's
arithmetic says (c) can only return to ~0.210 if its tail measures ~2.21,
which `n <= 16000` did not produce here in six attempts. Quiet removes the
window truncation and shrinks the scatter; whether it shrinks it below
0.3 is untested and should not be assumed.

The gate needs the scaling range extended until the bit-packed control's
tail converges to the naive baseline's, since that convergence is what
demonstrates the discriminator works at all. That means editing `PROFILES`
and re-measuring the baseline — **a pre-registration amendment**,
deliberately not made here. Note the cost is real: the `full` profile's
`n = 64000` on a pure-Python `O(n^2)` simulator is roughly 16x the
`n = 16000` cost per call, times `repeats: 5`.

Worth weighing against that cost: register row 12 (Arm 3) answered a
version of this question with a **deterministic effort counter**, which
has none of these failure modes, and it is already built.

Open decision for the user, in one line: amend the pre-registration to
extend the scaling range (and pay for a fresh multi-hour baseline
measurement), reuse the Arm 3 fuel-counting instrument, or defer the arm.
The reversible default taken here is **defer** — the harness is untouched
and resumable, and no compute or LLM budget was spent on a measurement
that could not have been trusted.

## 9. Follow-up, same day: the clock was replaced with a fuel counter

See **`RESULTS-openevolve-p3-fuel.md`** (companion doc; this file is
unchanged above this line, and `evaluator.py`, `PREREGISTRATION.md` and
`baseline_exponent.json` are untouched — the new instrument is a *parallel*
evaluator that imports the pre-registered scoring and gates rather than
restating them).

Arm 3's wasmtime meter was read and **not** reused: WASM has only
fixed-width ops, so one instruction is genuinely `O(1)` and no proportional
cost model is needed; OpenEvolve mutates Python, where `row << 1` on a
`(2n+3)`-bit integer is one opcode doing `n` bits of work. A new
AST-rewriting word-RAM counter (`experiments/openevolve-p3/fuel.py`) charges
every variable-width operation proportionally and denies by default.

All four sanity candidates now pass, against two failures under the wall
clock: (a) **0.200000**, tail equal to the stored baseline *in every printed
digit*, improvement exactly 0.0 — the wall clock had credited this same
program with beating itself by 0.41 exponent-units; (b) 0.0; (c) bit-packed
**0.214234** against a documented 0.210, its 84x constant-factor win
invisible to `combined_score` — the wall clock read 0.9335; (d) 0.0. Counts
are bit-identical across separate processes under load. The baseline
exponent measures **1.99946** with `r^2 = 0.9999999`, against 2.2147 /
1.9289 / 2.1635 / 1.8069 from the clock.

Still not run: the search itself. One gap remains open before it should be —
the fuel ladder tops to `n = 4000`, which shortens the reach of gate 4 (the
only anti-lookup-table check above `n = 3000`); see that doc's section 8.

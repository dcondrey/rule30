# Pre-registration: OpenEvolve attack on Rule 30 P3

Scope note: this targets **P3 only** (is Omega(n) effort genuinely required
to compute c(n), the Rule 30 center column, i.e. is there any
asymptotically-faster-than-simulation shortcut?). P1 (non-periodicity) and
P2 (equidistribution) are explicitly out of scope -- they need proofs, not
programs, and have no automatically verifiable fitness signal.

## Prior art / prior

Nobody has found a shortcut for Rule 30's center column despite decades of
attention (Wolfram's own $30k/$15k/$10k prize questions have stood
unresolved since 2019; this repo's own `docs/rule30/PATH.md` and
`experiments/overnight-arms/frontier_attack/` register dozens of
independent attack attempts against exactly this question, all
inconclusive or negative). The overwhelmingly likely outcome of this
experiment is **the negative**: every exactly-correct candidate OpenEvolve
proposes matches the direct-simulation exponent within noise. That is not
a failure of the experiment -- see "Kill condition" below.

This experiment is worth running anyway because:
- The search is cheap relative to the payoff. A genuine finding here would
  resolve a standing open problem; the cost is a few dollars of LLM calls
  and some compute.
- The reward signal is *objective* -- correctness against held-out ground
  truth plus a measured scaling exponent -- not an LLM's opinion of its own
  cleverness, which is where prior LLM-driven attempts on this problem in
  this repo repeatedly failed (plausible-sounding nonsense that doesn't
  hold up).
- Even a clean negative is informative: it's evidence about what a
  reasonably wide evolutionary code-search over "obvious" algorithmic
  restructurings of the simulation can and cannot find in this space, at
  this budget.

## Task

Evolve `center_cell(n) -> int`, computing c(n) for Rule 30 from the
standard single 1-cell seed, starting from a straightforward
(unoptimized) direct-simulation baseline
(`experiments/openevolve-p3/initial_program.py`).

## Baseline

Direct cellular-automaton simulation: for each of n rows, update a row of
width ~2n using the Rule 30 rule cell-by-cell. Theoretically O(n^2) cell
updates. **Empirically measured exponent** (see
`baseline_exponent.json`, "smoke" profile, tail exponent between the two
largest usable points): see the numbers block appended at the bottom of
this file once `measure_baseline.py` has been run -- do not assume 2.0,
report what was actually measured.

## Metric: scaling exponent, NOT wall time

`evaluator.py` times `center_cell(n)` across a geometric range of n,
fits log(time) vs log(n), and uses the **tail exponent** (the local
log-log slope between the two *largest* usable n points) as the primary
fitness signal -- not a single global fit across the whole range, and
never raw wall-clock time.

This distinction is load-bearing and was validated empirically before any
real search was run (see "Measurement methodology" below): a
constant-factor-only speedup can look like a much lower exponent than its
true asymptotic value when measured only over small n, because per-call/
per-iteration Python overhead dominates until n is large enough for the
O(n^2)-with-a-good-constant term to actually exceed it. The tail-exponent
methodology, plus a wide-enough n range to reach the converged regime, is
the fix.

**Constant-factor speedups do not count as a P3 result and are reported
separately** (`speedup_note` / usable_ns in the evaluator's artifacts),
never folded into `combined_score`.

## Correctness gate (hard, non-negotiable)

A candidate that is wrong on ANY of the following, for ANY n, scores
`combined_score = 0.0`, full stop -- no partial credit:

1. **Evolve set** (`ground_truth.json["evolve"]`, 15 values of n, 10-2464):
   visible to the evolutionary loop as feedback.
2. **Holdout set** (`ground_truth.json["holdout"]`, 15 values of n,
   12-3000, log-spaced and interleaved with the evolve set so neither is
   systematically easier): **never** exposed as per-n feedback during
   evolution, only used to compute the final reported fitness. A
   candidate cannot win by curve-fitting or hardcoding against it.
3. **Trap set** (`evaluator.TRAP_NS`, computed fresh every evaluation,
   never written to any file the evolutionary loop or its LLM can read):
   specifically targets a candidate that embeds a lookup table sized to
   the n values it has actually seen on disk.
4. **Scaling-range correctness**: every n used for the timing/exponent
   measurement (2000-16000 for "smoke", up to 64000 for "full") is ALSO
   checked against freshly-computed ground truth (via
   `reference/bigint_reference.py`, itself cross-validated against the
   independent, deliberately dead-simple `reference/simple_reference.py`
   in `reference/test_reference.py`). This is the only check that reaches
   beyond n=3000; it exists because a large-n lookup table would otherwise
   go undetected by the (necessarily capped, for evaluation-cost reasons)
   evolve/holdout/trap sets.

Ground truth itself is computed by `reference/simple_reference.py` (a
deliberately naive, obviously-correct O(n^2) list-based simulator, never
touched by evolution) for n <= 3000, and by `reference/bigint_reference.py`
(a big-integer bit-packed simulator, exhaustively cross-validated against
`simple_reference.py`) for larger n where the naive version would be too
slow to use for ground-truth generation.

A static AST scan (`evaluator._scan_literals`) additionally disqualifies
any candidate containing an integer literal with >=100 digits or a
list/tuple/set/dict literal with >=5000 elements -- an automatic,
independent backstop against embedded lookup tables, regardless of
whether the trap set happens to catch it. (Verified NOT sufficient on its
own -- a dict *comprehension* isn't a literal and isn't caught by this
scan; the correctness gates above are the actual defense, this is
defense-in-depth only.)

## Measurement methodology (found empirically before running any real search)

Two bugs were found and fixed while smoke-testing the evaluator itself,
before any evolutionary search was run:

1. **Correctness-gate timeout was coupled to the scaling profile's
   per-point timeout.** With a 10s scaling timeout and evolve-set n values
   up to ~16000, the CORRECT baseline itself timed out on the correctness
   gate and scored 0.0 -- a false negative on ground truth. Fixed by
   capping the evolve/holdout/trap correctness sets at n<=3000 (cheap even
   for an unoptimized O(n^2) candidate) and giving correctness checks their
   own independent, generous timeout (`CORRECTNESS_TIMEOUT`), decoupled
   from the scaling profile entirely.

2. **A same-exponent, constant-factor-faster candidate (big-integer
   bit-packing, `sanity_candidates/candidate_c_bitpacked.py`) scored 0.956
   -- indistinguishable from a real algorithmic win -- when the exponent
   was estimated via a single global log-log fit over n=200..3200.**
   Diagnosed by direct measurement: over that range the bit-packed
   candidate's *apparent* exponent was ~1.1; extending the measured range
   to n=8000..16000 showed its exponent converging to ~1.9, matching the
   direct-simulation baseline, exactly as it should for a pure
   constant-factor win. The cause is Python-level per-call/per-iteration
   overhead dominating at small n, before the O(n^2/64)-ish bit-packed
   cost term actually exceeds it -- CPython's C-level bigint bitwise ops
   are fast enough that the crossover into the true asymptotic regime
   doesn't happen until several thousand steps. Fixed by (a) widening the
   scaling range to reach that converged regime (2000-16000 for "smoke",
   2000-64000 for "full") and (b) scoring on the **tail exponent** (local
   slope between the two largest usable points), with confidence
   discounted when the tail and the segment before it disagree (a sign the
   measurement is still in a transient regime), rather than a single global
   fit dominated by the small-n end.

Both fixes were verified against the three required sanity candidates
(plus a bonus fourth) before this pre-registration was finalized -- see
"Evaluator sanity tests" below and the session's final report for the
actual scores.

## Held-out verification protocol

- Evolution only ever sees `combined_score` and the evolve-set-derived
  parts of `EvaluationResult` (metrics/artifacts) for feedback during the
  search loop.
- Final reported fitness for any candidate this experiment calls a result
  is computed by re-running `evaluate()` fresh (holdout set included, as it
  always is -- `evaluate()` does not have a "training-only" mode) and, for
  the strong-outcome claim specifically, re-measuring the scaling exponent
  across >= 3 independent seeds/repeats to confirm reproducibility before
  anything is reported as a finding.

## Strong outcome

An **exactly-correct** candidate (passes every gate above, including
holdout and trap, with zero exceptions) whose measured **tail exponent**
is meaningfully below the baseline's measured tail exponent (see
"Fitness" below for the 0.3-exponent-unit full-credit bar, calibrated
against the measured overhead-transient noise floor of ~0.2-0.3 seen in
the constant-factor sanity candidate at the smoke profile's range), and
where that gap **reproduces across >= 3 independent measurement runs**
(not just a single noisy timing sample -- see bug #2 above for exactly
why a single measurement is not trustworthy here).

## Kill condition (must be able to fire on a plausible negative)

If every exactly-correct candidate's tail exponent matches the baseline's
within the measurement noise band (empirically, +/-0.2-0.3 exponent units
at the smoke profile's range, tighter at "full"), **that is a clean,
publishable negative**: "no shortcut found by this evolutionary
code-search method, at this budget, in this search space." It is not
spun as anything else. Constant-factor speedups (however large) found
along the way are reported as exactly that -- a constant-factor result --
separately from the P3 verdict, never mixed into it.

## Fitness (implementation: `evaluator._combined_score`)

```
if tail_exponent is None:          combined_score = 0.15   (correct, unmeasurable)
else:
    improvement = baseline_tail_exponent - tail_exponent
    bonus = clip(improvement / 0.3, 0, 1)
    confidence = r2 * (consistency discount)
    combined_score = 0.2 + 0.8 * bonus * confidence   (floored at 0.2 if improvement >= -0.05)
```
Wrong on any gate -> `combined_score = 0.0` overrides everything above.

## Evaluator sanity tests (required before any real search; results in
the session report, not duplicated here to avoid this file going stale)

(a) Correct baseline -> must be correct, flat ~0.2 credit (no self-improvement).
(b) Deliberately wrong (AND instead of OR in the update rule) -> must score exactly 0.0.
(c) Correct, big-integer bit-packed (constant-factor-faster, same
    exponent) -> must be recognized correct, must NOT land in the
    exponent-improvement band.
(d) [bonus] Lookup-table cheat attempt -> must score exactly 0.0.

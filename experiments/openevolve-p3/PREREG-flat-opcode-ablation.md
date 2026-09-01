# Pre-registration: flat-opcode ablation of the fuel cost model

Written 2026-08-31, **before the measurement was run**. Kill condition stated
below fires on a plausible negative and would remove the central design claim
of `RESULTS-openevolve-p3-fuel.md`.

## Why this experiment exists

`RESULTS-openevolve-p3-fuel.md` section 2.1 argues that the word-RAM charging
rule is load-bearing. Its evidence is an ablation in **one** direction only:
charging by raw **bits** instead of words inflates the naive `O(n^2)` control to
2.12-2.15 via a spurious `log n` on loop indices.

The obvious alternative in the **other** direction was never measured: a **flat
opcode counter**, which charges `1` per operation regardless of operand width.
That is the instrument any reader will propose first, because it is what
`sys.settrace` opcode counting, `cProfile` call counts, and a WASM fuel meter
all give you for free, and it is the thing the document's own section 1 rejects
by argument rather than by measurement.

Rejecting the strong incumbent by argument is not rejecting it. If the flat
counter also recovers the known exponents, the word-RAM model is an
unnecessary complication and the contribution's central design claim does not
survive.

## Construction of the baseline

The flat model is the word model with both size primitives pinned to `1`:
`fuel._bits` and `fuel._elems` monkeypatched to `lambda x: 1`. Charge
expressions built from them (e.g. `_bits(a) * _bits(b) + _bits(r)`) then
evaluate to a small constant rather than to `1` exactly. That is the intended
semantics: **`O(1)` charge per operation, independent of operand size**, which
is what a bytecode-instruction counter measures. No other part of `fuel.py`,
`evaluator_fuel.py` or `PREREGISTRATION.md` is touched.

Everything else is held fixed: same two sanity candidates, same ladder
`n = 125, 250, 500, 1000, 2000, 4000`, same adjacent-window slope formula as
`evaluator_fuel.measure_scaling_fuel`, same process.

## Metric

Adjacent-window slopes of `log(fuel)` against `log(n)`, and the final-window
slope as the headline, compared against the word model's measured values:

| candidate | true asymptotic | word model (`WORD_BITS = 30`), measured |
|---|---|---|
| (a) `candidate_a_correct` | `Theta(n^2)` | 1.99946 |
| (c) `candidate_c_bitpacked` | `Theta(n^2 / 64)`, so still `Theta(n^2)` | 1.9941 |

Band: the harness's own pre-registered tolerance, `+/- 0.3` exponent-units.

## Outcomes, fixed in advance

**Strong outcome (word model vindicated).** The flat counter misses the known
exponent by more than `0.3` on at least one candidate. Interpretation: charging
proportional to operand width is necessary, not decorative, and a bytecode
counter would have mis-ranked candidates by the same mechanism the wall clock
did. This is the outcome that licenses the standalone contribution's design
claim.

**KILL CONDITION.** The flat counter recovers both candidates' exponents to
within `0.3` of `2.0`. Interpretation: **on this task family the word-RAM
refinement is not demonstrated to be necessary.** The document's section 2.1
must then be rewritten to say the word model was chosen over a flat counter for
reasons that this measurement did not support, the register row 92 wording
"charges every variable-width operation proportionally" must lose its implied
necessity, and any standalone write-up must drop the word-RAM design as its
contribution and fall back to the narrower claim (deny-by-default + determinism
+ the documented wall-clock self-comparison failure).

**Ambiguous.** Exactly one candidate inside the band and the other outside, or a
slope that is neither near `2.0` nor stably away from it. Report as ambiguous;
do not resolve it by picking the reading that favours the word model.

## Stated prediction

Recorded so it can be wrong. Candidate (c) operates on whole packed rows as
single big integers, so under a flat counter its per-row cost is `O(1)` and its
total should fit an exponent near `1.0`, far outside the band. Candidate (a)'s
outcome is genuinely uncertain and depends on whether its inner work is
per-cell Python iteration (flat counter already gives `n^2`, band satisfied) or
whole-row integer operations (flat counter gives `~n`, band violated). A split
result is therefore a live possibility and falls under **Ambiguous** above, not
under the strong outcome.

## Scope

Not a claim about Rule 30. One task family, two candidates. A negative here does
not show the word model is wrong in general, and a positive here does not show
it is right in general; both are statements about whether *this* document's
evidence supports *its* design claim.

## Artifacts

- `flat_opcode_ablation.py` — the runner.
- `flat_opcode_ablation_20260831.log` — saved output.

---

# RESULT (run 2026-08-31, after the above was fixed)

**Pre-registered verdict: AMBIGUOUS.** One candidate inside the band, one
outside. The kill did **not** fire, and the strong outcome was **not** obtained.

Tail slopes (`2000 -> 4000` window), both arms measured in one process:

| candidate | flat opcode | word model (`WORD_BITS = 30`) | true |
|---|---|---|---|
| (a) `candidate_a_correct` | **1.99947** | 1.99946 | 2 |
| (c) `candidate_c_bitpacked` | **0.99938** | 1.99410 | 2 |

Adjacent windows are monotone and well behaved in all four arms; the tails are
not artifacts of a single noisy point.

## Reading, including the part that goes against the word model

Candidate (a) is recovered by the flat counter to within `1e-5` of the word
model — 1.99947 against 1.99946. That is inside the band, and it is the half of
the result that does not support the word-RAM design.

Candidate (c) is read as `Theta(n)` by the flat counter against a true
`Theta(n^2 / 64)`, an error of a full exponent-unit and far outside the band.
The word model reads it 1.99410.

**The two candidates are not equally informative, and that asymmetry was
foreseeable before the run.** Candidate (a) iterates per cell, so every operand
fits in one word and the flat and word models are charging the *same thing*; it
cannot discriminate between the two cost models under any outcome. Candidate (c)
operates on whole packed rows as single big integers, so it is the only one of
the two that puts a wide operand in front of the instrument.

**Naming the design flaw rather than the favourable reading:** the pre-registered
verdict rule was band-membership across both candidates, and it should have been
band-membership across candidates *capable of discriminating*. Candidate (a) was
never such a candidate. That is a flaw in this pre-registration, and it is being
recorded rather than corrected after the fact — the verdict above stands as
AMBIGUOUS, because re-reading the rule once the numbers are in is the exact move
the pre-registration exists to prevent.

**What can be claimed, narrowly:** on the one candidate that exercises wide
operands, a flat opcode counter misreads the asymptotic exponent by 1.0. That is
a real instance of the granularity effect, in the opposite direction from the
bits-vs-words ablation in `RESULTS-openevolve-p3-fuel.md` section 2.1. It does
**not** establish the general claim, and a second discriminating candidate would
be needed for that.

**What this does not do.** It does not feed a publication: see
`docs/rule30/LITCHECK-fuel-instrument.md`, which records the standalone
contribution as dropped on prior-art grounds, decided before this result was
read. This ablation is retained as internal validation of the instrument for
register row 91's blocked arm, nothing more.

---

# AMENDMENT: second discriminating candidate

Written 2026-08-31 **after** the result above was read and **before** the
amended run. Added at the user's instruction, overriding the "not adding a
second discriminating candidate" call in the session that produced the result
above. Recorded as an amendment rather than folded into the original text,
because a pre-registration edited after seeing its own numbers is not a
pre-registration.

## What the result above cannot settle

Candidate (a) could not discriminate, so the run rests on one discriminating
candidate. Worse, **both** ablation arms and the bits-vs-words ablation in
`RESULTS-openevolve-p3-fuel.md` section 2.1 test the instrument against a true
exponent of **2 and only 2**. "The instrument recovers the known exponent" has
therefore never been checked at any other point, and an instrument that happened
to be biased toward 2 would pass every test run so far.

## The addition

`sanity_candidates/candidate_e_cubic.py`: correct (verified identical to
candidates (a) and (c) for all `n < 120`, and its prefix matches A051023),
bit-packed so its operands are wide, and deliberately `Theta(n^3)` — it rebuilds
the row from the seed at every outer step rather than carrying it forward. Cost
is `sum_{t=1..n} t * ceil((2n+3) / WORD_BITS)`.

It is discriminating by construction and in a way (a) was not: `Theta(n^3)` under
a word-RAM model, `Theta(n^2)` under a flat per-operation count. The two models
disagree by a full exponent-unit.

Not a plausible search candidate. Instrument calibration only.

## Verdict rule, corrected

The original rule compared every candidate against `2.0`. That is wrong for a
candidate whose true exponent is 3, and it is wrong in a way that matters: the
flat model reads (e) as `~2.0`, which the original rule would have scored as
**inside the band** while the instrument was in fact wrong by 1.0. Each candidate
is now compared against **its own** true exponent, band unchanged at `+/- 0.3`:

| candidate | true exponent | discriminating? |
|---|---|---|
| (a) `candidate_a_correct` | 2 | no — all operands fit one word |
| (c) `candidate_c_bitpacked` | 2 | yes |
| (e) `candidate_e_cubic` | 3 | yes |

## Outcomes, fixed in advance

- **Strong outcome.** The word model lands inside the band on all three, and the
  flat model lands outside on both discriminating candidates. Word-RAM charging
  is then necessary, and the instrument is shown correct at two distinct
  exponents rather than one.
- **KILL.** The flat model lands inside the band on both discriminating
  candidates. Consequences as in the original kill condition.
- **NEW KILL, on the instrument rather than the ablation.** The **word** model
  misses `3.0` by more than `0.3` on (e) at the top of the ladder, with the
  adjacent-window slopes not trending toward 3. That would mean the instrument
  does not recover a known exponent away from 2, which is a defect in `fuel.py`
  and not in the flat-model comparison. It would put register row 92's
  "instrument validated" status in question and must be reported as such.
- **Ambiguous.** Anything else, including a split between (c) and (e).

## Stated prediction

Word model: (e) approaches 3 from below, since the exact cost has a leading
cubic and a lower-order quadratic term, so the tail window at a short ladder may
read meaningfully below 3.0 (2.7-2.9) without the instrument being wrong. **This
is a prediction, not an escape hatch:** if the tail reads below 2.7 the new kill
fires as written, and a slope that is flat rather than rising toward 3 fires it
regardless of value.

Flat model: (e) reads `~2.0`, outside its band around 3.

Ladder for (e) is shortened to `n = 125, 250, 500, 1000` because `Theta(n^3)`
under AST instrumentation is too slow at 2000+. (a) and (c) keep the full ladder.

## Artifacts

- `flat_opcode_ablation2.py` — the amended runner.
- `flat_opcode_ablation2_20260831.log` — saved output.

## AMENDED RESULT (run 2026-08-31)

**Pre-registered verdict: STRONG OUTCOME.** Word model inside the band on all
three candidates and at two distinct true exponents; flat model outside on both
discriminating candidates, by almost exactly one exponent-unit each.

| candidate | true | word model | flat opcode | discriminating |
|---|---|---|---|---|
| (a) `candidate_a_correct` | 2 | 1.99946 | 1.99947 | no |
| (c) `candidate_c_bitpacked` | 2 | 1.99410 | **0.99938** | yes |
| (e) `candidate_e_cubic` | 3 | **2.97449** | **1.99690** | yes |

Flat-model errors: `-1.00062` on (c), `-1.00310` on (e). Adjacent windows are
monotone in all six arms; (e)'s word-model slopes rise 2.90164 -> 2.96786 ->
2.97449, i.e. converging toward 3 from below as predicted. Neither the original
kill nor the new instrument-directed kill fired: 2.97449 is well clear of the
2.7 floor and the slopes are rising, so `fuel.py` recovers a known exponent away
from 2.

**The verdict-rule bug is now confirmed empirically, not just in principle.**
The flat model reads (e) at 1.99690. Under the original script's fixed
`TARGET = 2.0` that is `inside` the `+/- 0.3` band, on a candidate where the flat
model is wrong by a full exponent-unit. Scoring each candidate against its own
true exponent is what turns that from a pass into a `-1.00310` miss.

**What can now be claimed, and it is stronger than after the first run.** The
word-RAM model recovers two distinct known exponents (2 and 3) to within 0.03,
while a flat per-operation count is wrong by 1.0 on every candidate that puts a
wide operand in front of the instrument. Cost-model granularity is the
controlling variable, demonstrated in both directions from the word model:
charging too coarsely (flat) loses a full exponent-unit, and charging too finely
(raw bits, section 2.1 of `RESULTS-openevolve-p3-fuel.md`) adds a spurious
`log n` worth 0.12-0.15.

**Scope, unchanged.** One task family. Candidate (e) is instrument calibration,
not a plausible search candidate; its `Theta(n^3)` is deliberate waste. This
result does not revive the publication decision, which was made on prior-art
grounds in `docs/rule30/LITCHECK-fuel-instrument.md` before either run was read
and is unaffected by how well the instrument performs.

**What this does not do.** It does not feed a publication: see
`docs/rule30/LITCHECK-fuel-instrument.md`, which records the standalone
contribution as dropped on prior-art grounds, decided before this result was
read. This ablation is retained as internal validation of the instrument for
register row 91's blocked arm, nothing more.

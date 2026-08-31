# a23 — results: empirical Myhill-Nerode index for Lemma S'

Pre-registered in `PREREGISTRATION.md` (read that first, including its
amendment, which records four Rule-90 seed constructions tried and their
four distinct failure signatures). Read-only reuse of `a5_row41_fiber_uniform/
band_automaton.py` (`forced_step`, `forced_step_90`, `seed_state`,
`c_of`), same import pattern as `a22_row41_alt_strategy/
bilinear_decomp_check.py`. Code: `mn_index.py`, `sweep.py`.

## Verdict

**Rule 90 positive control: NOT VALIDATED. No verdict on Lemma S' follows
from this arm's Rule 30 data.** This is the honest outcome, per the
mandatory-gate instructions in PREREGISTRATION.md ("or report clearly that
the pipeline could not be validated and why"), not a partial result.

Four Rule-90 seed constructions were tried, in order, each looking like a
clean pass before being caught:

1. `v := bits(m)`, `u := 0`. Gave `index == 1` everywhere. Caught because
   `n_prefixes` (rho-track diversity) grew with the population while
   `index` (pin-track diversity) did not move at all -- the pin channel was
   provably dead, reading a handed-off `u` that never varied with the seed.
2. `v, u :=` disjoint halves of `bits(m)`. Gave `index == 2^(kseed/2)`
   exactly, with `n_prefixes == n_anomalous_prefixes` at every point (every
   single prefix class contained seeds with disagreeing futures). Caught
   because baking all seed bits into the `t=0` vectors simultaneously gives
   a would-be transducer no "read-in" phase to forget during, so realized-
   future-window counts mechanically track population size for any rule.
3. `rule90_seed_streamed`: stream `kseed` bits in one per PAIR, using
   `seed_state`'s own convention (free drive, then forced `drive=1`).
   Gave `index == 1` again. Caught by directly inspecting the handed-off
   `(u_0, v_0)`: `u_0` was byte-identical across all `2^kseed` seeds. The
   forced `drive=1` substep -- which exists to encode Rule 30's PIN
   SURVIVAL constraint, something Rule 90 has no analogue of -- resets the
   `u`-track to a seed-independent fixed point every pair.
4. `rule90_seed_v4`: drop the forced substep, inject one free drive per
   SUBSTEP instead. Confirmed by direct inspection that BOTH `u_0` and
   `v_0` vary with the seed, and confirmed EXHAUSTIVELY (`kseed in
   {12, 16}`) that the map `m -> (u_0, v_0)` is fully injective (`4096/4096`,
   `65536/65536` distinct handoff states). This looked like the real fix.
   Swept, it gave `index_lower_bound(s=19)` moving non-monotonically
   between 8 and 64 across `kseed in {6,...,16}` -- a plateau. But
   `n_prefixes` (distinct realized rho-bit-stream prefixes) also saturated
   at exactly 256 for `kseed in {14, 16}`, independent of `kseed`, DESPITE
   the handoff state being fully `2^kseed`-diverse. Since
   `index <= n_prefixes` always (you cannot realize more distinct future-
   windows than distinct prefixes producing them), a capped `n_prefixes`
   mechanically caps `index` regardless of whether the underlying dynamics
   needs few or many states. This is a ceiling in the OBSERVABLE rho-bit
   channel, not evidence of state merging. Confirmed again by the same
   signature as construction 2: every saturated row has
   `n_prefixes == n_anomalous_prefixes` exactly -- every realized prefix
   class contains seeds whose futures disagree.

**Root cause, common to all four:** `forced_step_90` returns its `u`
argument unchanged (`return nxt, u, acc`), so under the rho/pin
alternation, the recursion splits into two tracks that never exchange
information. Whichever channel is used to inject a seed's bits, some part
of that information is structurally prevented from reaching either the
observable rho stream or the pin track (which one, and how much, differs
by construction -- that is exactly why four different-looking failures all
trace back to one mechanism). Building a fair Rule-90 population would need
a genuine Rule-90 analogue of `alt_trace_fiber_probe` -- an actual two-row
cellular-automaton seed generator with real physics, not a synthetic
`(u, v)`-level construction layered on `forced_step_90`'s already-rotated,
already-decoupled recursion. No such generator exists anywhere in this
codebase, and building one is out of this arm's scope.

**Given this, the Rule 30 numbers below are reported as raw data only.**
They were generated correctly (`BA.seed_state` is the real, previously-
verified Rule 30 probe, unaffected by any of the Rule-90 construction
problems above), and the growth pattern is real, but per the pre-registered
gate this arm cannot say whether that growth is a fact about Rule 30's
hardness or an artifact of the same kind found four times over on Rule 90
(e.g. `index <= n_prefixes` held there too -- see the Rule 30 per-`s` table
below, where `n_prefixes` climbs toward the full population rather than
saturating, which is at least consistent with a live channel, but this
arm's own control failures show that consistency is not sufficient proof of
validity). **No claim is made here about Lemma S' in either direction.**

## Rule 30 raw data (uninterpreted -- see Verdict)

`index_lower_bound(s=19)`, `W=30`, exhaustive over `2^kseed` seeds:

| kseed | d = 2*kseed | phase 01 | phase 10 | n_seeds |
|------:|------------:|---------:|---------:|--------:|
|  6 | 12 |    27 |    35 |    64 |
|  8 | 16 |    88 |   120 |   256 |
| 10 | 20 |   281 |   362 |  1024 |
| 12 | 24 |   890 |  1190 |  4096 |
| 14 | 28 |  2842 |  3804 | 16384 |
| 16 | 32 |  8951 | 11982 | 65536 |

Ratio between successive `+2`-kseed steps: phase `01`: 3.26, 3.19, 3.17,
3.19, 3.15; phase `10`: 3.43, 3.02, 3.29, 3.20, 3.15 -- roughly constant
multiplicative growth, no plateau across the six points tested. Under a
VALIDATED control this would fire the pre-registered kill condition; absent
one, it is reported as an observation, not a verdict.

Per-`s` curve at kseed=16 (largest depth tested), phase `01`:
9008, 9008, 9002, 8997, 8996, 8993, 8990, 8987, 8982, 8980, 8977, 8974,
8969, 8968, 8966, 8963, 8958, 8955, 8954, 8951.
Phase `10`:
12061, 12059, 12056, 12052, 12048, 12043, 12036, 12031, 12025, 12019,
12015, 12011, 12005, 12001, 11996, 11993, 11991, 11987, 11984, 11982.
`n_prefixes` at the same kseed climbs from 2 (s=0) to 8974/11995 (s=19),
i.e. toward but not yet at the `65536` population ceiling -- unlike every
failed Rule-90 construction, it has not saturated at a `kseed`-independent
constant within the depths reached here. `n_anomalous_prefixes` is 35/8974
(~0.4%, phase 01) and 66/11995 (~0.6%, phase 10) at `s=19`, small relative
to `n_prefixes` -- unlike the failed Rule-90 constructions, where
`n_anomalous_prefixes == n_prefixes` exactly. These two facts are the
reason this arm still reports the Rule 30 numbers as *probably* reflecting
real dynamics rather than a channel-capacity artifact -- but "probably" is
not "validated", and the gate was not met, so this stays an observation.

## Rule 90 raw data (all four constructions, for the record)

`index_lower_bound(s=19)`, both phases identical at each `kseed` (no phase
asymmetry found for Rule 90):

| kseed | construction 1 | construction 2 (`2^(kseed/2)`) | construction 3 | construction 4 |
|------:|---------------:|--------------------------------:|----------------:|----------------:|
|  6 | 1 |   8 | 1 |  8 |
|  8 | 1 |  16 | 1 | 16 |
| 10 | 1 |  32 | 1 | 32 |
| 12 | 1 |  64 | 1 | 64 |
| 14 | 1 | 128 | 1 | 32 |
| 16 | 1 | 256 | 1 | 64 |

`n_prefixes` for construction 4 at `kseed in {14, 16}`: 256 (saturated,
independent of `kseed`); handoff-state count (checked exhaustively): 4096/
4096 at kseed=12, 65536/65536 at kseed=16 (fully injective, i.e. the seeding
function itself is not the bottleneck -- the observable rho-stream
projection is).

## Sampling honesty

All `kseed <= 16` rows, both rules, all constructions: exhaustive, every
one of `2^kseed` seeds enumerated, both phases, no sampling anywhere in
this arm.

## What this does NOT do

* **Does not establish or refute Lemma S'.** The mandatory Rule 90 control
  was not validated (see Verdict), so per the pre-registered gate no Rule
  30 conclusion is drawn.
* Does not identify which (if any) of the four Rule-90 failure mechanisms
  also affects the Rule 30 numbers reported here. `n_prefixes` and
  `n_anomalous_prefixes` behave differently for Rule 30 than for any failed
  Rule-90 construction (see "Rule 30 raw data" above), which is suggestive
  but was not independently verified the way the Rule-90 handoff-state
  injectivity was checked.
* Does not build a genuine Rule-90 seed generator with real two-row
  cellular-automaton physics (the fix identified as actually necessary).
  That is concrete follow-up work, not attempted here.
* `kseed=18` (`2^18` seeds) was not attempted for Rule 30; not relevant
  given the control could not be validated regardless of how far the Rule
  30 sweep is extended.
* The `n_anomalous_prefixes` diagnostic is reported but not investigated
  further as its own question (whether SOME pairs of seeds share a rho
  prefix yet provably diverge in the future, for Rule 30 specifically); it
  is a stronger and different claim than the headline index statistic.
* No model is fit to the Rule 30 growth ratios beyond reporting them raw.

## Reproduction

```bash
cd experiments/overnight-arms/frontier_attack/a23_row41_myhill_nerode

# Rule 90, construction 4 (rule90_seed_v4, the current default in
# mn_index_sweep). None of the four constructions tried in this arm
# constitutes a validated control pass -- see Verdict above for why.
uv run python sweep.py --kind 90 --pairs 20 --W 30

# Rule 30 raw data (real seed_state, unaffected by the Rule-90 problems)
uv run python sweep.py --kind 30 --pairs 20 --W 30

# handoff-state injectivity check for construction 4 (kseed=12, 16)
uv run python -c "
from mn_index import rule90_seed_v4
for kseed in (12, 16):
    seen = {(tuple(u), tuple(v)) for m in range(2**kseed)
            for u, v in [rule90_seed_v4(0, kseed, m)]}
    print(kseed, len(seen), 2**kseed)
"
```

To reproduce constructions 1-3 exactly, edit `mn_index_sweep`'s call site
(currently `rule90_seed_v4`) to call `rule90_seed` (construction 1) or
`rule90_seed_streamed` (construction 3); construction 2 (disjoint halves)
was not kept as a named function and would need reconstructing from this
document's description (`v, u := disjoint halves of bits(m)`).

Both read-only import `a5_row41_fiber_uniform/band_automaton.py`. No file
outside this directory (`a23_row41_myhill_nerode/`) was written. Paid
model-provider calls: $0.

Wall-clock (single-threaded pure Python, this machine): Rule 90 full sweep
(construction 4) ~71s total; Rule 30 full sweep ~116s total.

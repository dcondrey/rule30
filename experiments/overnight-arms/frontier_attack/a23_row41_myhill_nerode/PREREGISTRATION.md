# a23 — pre-registration: empirical Myhill-Nerode index for Lemma S'

Read first: `a22_row41_alt_strategy/alt_strategy.md` part B (states Lemma S'
precisely) and `a5_row41_fiber_uniform/band_automaton.py` (`forced_step`,
`forced_step_90`, `seed_state`, `parity_sequence` -- the idioms reused here).

## What is being tested

Lemma S' (streaming compressibility): is there a constant `M` and a
finite-state transducer, `|Q| <= 2^M`, reading the rho-bit stream online,
whose bounded internal register alone determines the next pin-parity bit,
for every state reachable from every finite left-depth-`d` seed, for every
`d`?

## The statistic

**Myhill-Nerode index, W-window lower bound.** For a fixed left-depth
`d = 2*kseed`, enumerate ALL `2^kseed` rho-seeds (both phases). Run the
*unconditional* forced map (`BA.forced_step` / `BA.forced_step_90`, no
halting on pin failure -- the same convention `BA.parity_sequence` and
`BA.window_test` already use) for `pairs + W` rho/pin pairs per seed,
recording `rho_bits[s]` (the forced `par` at the rho substep of pair `s`)
and `pin_bits[s]` (the forced `par` at the pin substep of pair `s`).

At each pair-index `s in [0, pairs)`:
- `rho-prefix(s, seed) := tuple(rho_bits[0..s])` -- what a streaming
  transducer would have read by that point.
- `future-window(s, seed) := tuple(pin_bits[s .. s+W))` -- the length-`W`
  future it would need to predict from its internal state.

`index_lower_bound(s) := |{ future-window(s, seed) : seed }|`, i.e. the
number of distinct realized future-`W`-windows across the seed population at
that `s`. Any bounded transducer's state after reading a given rho-prefix
must determine (at least) this window, so two seeds with different
future-`W`-windows *must* occupy different transducer states at `s`; two
seeds with the *same* future-`W`-window may or may not require the same
state (their longer futures could still diverge past `W`). So this is a
**lower bound**, never an exact index, and it can only grow (never
spuriously shrink) as `W` grows -- if two true infinite futures diverge,
they diverge within some finite window, so widening `W` can only reveal
more required splits, not remove real ones.

Also recorded as a diagnostic (not the headline statistic): the number of
distinct rho-prefix strings that are shared by two-or-more seeds whose
future-`W`-windows *disagree* (`n_anomalous_prefixes`). This would be a
strictly stronger and out-of-scope finding if it occurred systematically --
it would mean no finite-state device of *any* size, bounded or not, can
predict the future from the visible rho-bit stream alone. It is reported
for honesty, not used to decide Lemma S'.

## Sweep

- `kseed in {6, 8, 10, 12, 14, 16}`, i.e. `d = 2*kseed in {12,...,32}`,
  **exhaustive** (every one of `2^kseed` seeds), both phases (`01`, `10`).
  Feasibility was timed before committing: kseed=8 (0.2s), kseed=12 (4.1s),
  kseed=14 (17.6s), kseed=16 (75s) on this machine, single-threaded pure
  Python, `pairs=20, W=30`. kseed=18 (`2^18=262144` seeds) was not attempted:
  linear extrapolation from the 14->16 step (~4.3x per +2 kseed) puts it
  at roughly 5-6 minutes, and the marginal `d` value is not needed to see
  whether the sweep already run plateaus or grows -- if it is inconclusive
  at kseed=16, that will be stated plainly rather than pushed further under
  time pressure.
- `pairs = 20` (pair-indices `s = 0..19` reported per `kseed`; the headline
  number quoted per `(kind, phase, kseed)` is `index_lower_bound` at
  `s = pairs - 1 = 19`, i.e. as much post-knee history as budget allows).
- `W = 30` (future-window length). `pairs + W = 50` total forced rho/pin
  pairs simulated per seed beyond the knee.

## Kill condition (against Lemma S')

`index_lower_bound(s=19)` grows **without bound** as `kseed` increases
across `{6,8,10,12,14,16}` -- specifically, no plateau: the value keeps
increasing roughly in proportion to (or faster than) the seed population
`2^kseed`, rather than saturating at some constant independent of `kseed`.
This is evidence AGAINST a bounded transducer existing (against Lemma S'):
if a size-`2^M` transducer existed, the index could not exceed `2^M`
regardless of how large `kseed` gets, so it would have to plateau once
`kseed` is large enough that the seed population outstrips `2^M`.

## What would NOT be a proof either way

A plateau in `index_lower_bound(s=19)` across `kseed in {6,...,16}` is
**not** a proof that Lemma S' is true. It only means "survives this probe":
the true index could still diverge at some `kseed > 16` outside this
sweep's reach, or `W = 30` could be too short to reveal a merge that a
larger window would split. This will be stated explicitly in RESULTS.md
regardless of which way the numbers come out. Symmetrically, growth that is
merely `~2^kseed`-proportional but has not been checked for saturation
at larger population is *suggestive* of "no useful compression happening",
not proof that no constant `M` exists.

## Rule 90 positive control (mandatory gate, run first)

`alt_strategy.md` part A proves Rule 90's version of this map
(`forced_step_90`) is purely GF(2)-linear (no bilinear `corr` term), hence
realizable by a small, provably bounded linear transducer. The **identical**
pipeline (same statistic, same `kseed` sweep, same `pairs`, `W`) run on
Rule 90 must show a small, FLAT (non-growing, or growing only to a small
constant and then plateauing) index across the `kseed` sweep.

Caveat pre-registered here: `band_automaton.py` has no Rule-90 analogue of
`seed_state` (which drives the real Rule-30 probe, `P._wf_step`, that has no
Rule-90 counterpart in this codebase, and `forced_step_90` itself takes no
free "drive" parameter to inject seed choices through). The Rule-90 seed
population is therefore built directly at the `(u, v)` level instead:
`v := kseed bits of m` (all content within a left-depth-`kseed` window),
`u := all-zero`, enumerated exhaustively over all `2^kseed` values of `m` --
the direct analogue of a finite left-support seed for `forced_step_90`'s own
recursion (`o[m] = v[m]`, reading only `v`). This is not reuse of
`seed_state`; no Rule-90 equivalent of it exists to reuse. This
construction choice is made and fixed here, before seeing any Rule-90
numbers.

**If Rule 90 also shows unbounded/growing index under this pipeline**: STOP.
That means the measurement methodology is broken (candidates: `W` too small
relative to some natural correlation length even for a linear map, or a bug
in what counts as "prefix" or "state"). Do not report a Rule 30 result in
that case; diagnose the pipeline, or report clearly that the pipeline could
not be validated and why. Only proceed to interpreting Rule 30 once Rule 90
passes this control cleanly.

## Sampling honesty note

All `kseed <= 16` sweeps here are **exhaustive** (every seed enumerated),
matching the brief's requirement that this measure a true exhaustive index,
not a sampled one. No sampling is used anywhere in this arm. (If a future
extension needs `kseed > 16`, exhaustive enumeration stops being cheap and
any such extension would need to say plainly that it switched to a sample,
and that an index measured over a sample of seeds is a further lower bound
stacked on top of the W-window lower bound, per the brief.)

## Amendment (post-registration, before any Rule 30 number was interpreted)

The Rule-90 seed construction described above (`v := kseed bits of m`,
`u := all-zero`) was implemented, run, and caught by its own control before
being trusted: it gave `index_lower_bound == 1` at every `kseed` and every
`s`, which looked like a clean pass but was diagnosed as an artifact.
Tracing `forced_step_90`'s recursion shows it has a hard structural
property: the `u` argument is passed through UNCHANGED as the return value
`prev` (`return nxt, u, acc`), which makes the interleaved rho/pin
alternation split into two INDEPENDENT tracks that never mix -- pin bits
are a pure function of the original `u`, rho bits a pure function of the
original `v`, forever. With `u` fixed at all-zero (same for every seed),
every seed's pin stream was trivially identical -- not a fact about Rule
90, an artifact of that specific initial condition.

The fix that was tried next (splitting `m`'s bits between `u` and `v`, both
non-constant) surfaced a deeper problem: it baked ALL of a seed's
information into the `t=0` vectors simultaneously, rather than streaming it
in one bit per pair the way `BA.seed_state` does for Rule 30. A population
with no read-in phase gives a bounded transducer nothing to forget, so
realized-future-window counts saturate at the population size regardless of
which rule is being tested -- confirmed empirically (index exactly
`2^(kseed/2)`, with every one of those classes flagged as an "anomalous
prefix", i.e. the statistic was measuring the injection method, not the
dynamics).

A THIRD construction (`rule90_seed_streamed`) fixed the simultaneous-
injection problem by deriving a general-drive Rule 90 step, `drive_step_90`,
from `forced_step_90` the same way `BA.validate()` derives a general-drive
Rule 30 step from `forced_step` (`delta = drive ^ par`,
`u2 = [x ^ delta for x in nxt[:-1]] + [nxt[-1]]`; sanity-checked that
`drive = par` reproduces `forced_step_90` exactly), and streamed the
`kseed` bits of `m` in one per PAIR as drives, mirroring `seed_state`'s loop
exactly (`for drive in (1 - ((m>>i)&1), 1)`, i.e. a free drive on the first
substep of each pair and a FORCED `drive=1` on the second). This gave
`index_lower_bound == 1` at every `kseed`, which again looked like a clean
pass -- but direct inspection of the post-seeding state across seeds showed
`u` was byte-identical for every `m`, while `v` varied fully. Combined with
the same `forced_step_90` u/v-decoupling fact from the first attempt
(`pin[s] = parity(f^s(u_0))`, depending only on the handed-off `u_0`), this
meant the pin channel was STILL structurally dead at the moment measurement
began -- not because Rule 90 is compressible, but because `seed_state`'s
forced `drive=1` convention (which exists to encode Rule 30's PIN SURVIVAL
constraint) resets the `u`-track to a seed-independent fixed point after
every pair. Rule 90 has no survival/death condition at all, so importing
that forced substep was importing a Rule-30-specific reset into a
recursion that has no analogous reason to reset.

A FOURTH construction (`rule90_seed_v4`): drop the forced substep entirely
-- Rule 90 has no pin/survival semantics to justify one -- and inject one
free drive bit per SUBSTEP, consecutively (`kseed` substeps total, not
`kseed` pairs):
`for i in range(kseed): u, v, _ = drive_step_90(u, v, phase, (m>>i)&1)`.
Checked directly (printing `(u, v)` across several `m`) that BOTH the
handed-off `u_0` and `v_0` vary with `m`, and confirmed exhaustively
(`kseed in {12, 16}`) that the map `m -> (u_0, v_0)` is INJECTIVE: `4096/
4096` and `65536/65536` distinct handoff states respectively. This looked
like the fix.

It was not. Sweeping it gave `index_lower_bound(s=19)` moving
non-monotonically between 8 and 64 across `kseed in {6,...,16}` while
`n_prefixes` (distinct realized rho-prefix strings) saturated at exactly
256 for `kseed in {14, 16}` -- i.e. despite the handoff state being fully
`2^kseed`-diverse, the OBSERVABLE rho-bit stream itself collapses onto only
256 distinguishable prefixes, independent of `kseed`. That means the
"plateau" is a ceiling in the observable channel, not evidence that fewer
states are needed to predict pin: `index <= n_prefixes` always (you cannot
have more distinct future-windows than distinct prefixes producing them, at
a fixed `s`), so a capped `n_prefixes` mechanically caps `index` regardless
of whether the underlying dynamics is "hard" or "easy". Consistent with
this, at every saturated row `n_prefixes == n_anomalous_prefixes` exactly
(e.g. 256/256, 128/128, 64/64) -- EVERY realized prefix class contains
seeds whose futures disagree, the same signature the split-halves attempt
(construction two) was correctly rejected for.

**No Rule-90 seed construction tried here was validated as a fair
positive control.** Four attempts, four distinct failure signatures, all
traced to the same root cause: `forced_step_90` returns its `u` argument
unchanged (`return nxt, u, acc`), so under the rho/pin alternation the
recursion splits into two tracks that never exchange information with
each other. Whatever channel is used to inject a seed's bits, some part of
that information structurally cannot reach the observable rho-bit stream
(or, in the split-halves case, cannot reach the pin track at all) --
because `forced_step_90` was written to realize the deep-anchored,
already-verified structural claims in `band_automaton.py` (Theorem A/C,
Lemma D, Kill 1/2 for Rule 90), not to support an independently-seedable,
information-preserving Rule-90 population the way `seed_state` supports one
for Rule 30 via the real probe `P._wf_step`. Building a fair Rule-90
control would need a genuine Rule-90 analogue of `alt_trace_fiber_probe`
(a real two-row cellular-automaton seed generator, not a synthetic
(u, v)-level construction layered on top of the already-rotated,
already-collapsed `forced_step_90` recursion), which does not exist
anywhere in this codebase and was not built here (out of scope for this
arm's budget). `mn_index.py` keeps all four attempts as documented dead
ends (`rule90_seed`, `rule90_seed_streamed`, `rule90_seed_v4`), since the
reasoning that ruled each one out is itself part of the record.

## Reproduction of this pre-registration's numbers

```bash
cd experiments/overnight-arms/frontier_attack/a23_row41_myhill_nerode
uv run python mn_index.py --kind 90 --kseed <K> --pairs 20 --W 30 --time-only
uv run python mn_index.py --kind 30 --kseed <K> --pairs 20 --W 30 --time-only
```
for `K in {6,8,10,12,14,16}`. Full per-`s` curves (drop `--time-only`) are
also produced by `sweep.py`, which drives the full table written to
RESULTS.md.

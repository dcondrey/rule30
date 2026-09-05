# Preregistration: a decay mechanism for H_r(n), not just a measurement of it

Date: 2026-09-04

Status: design only. No script run, no existing file touched. This document
is a follow-on to `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md` section 4,
which only proposes measuring `|H_r(n)|/2^n` further. The gap this document
tries to close: a measurement, however clean, is not a proof that `H_r(n)`
is eventually empty or decays geometrically for all `n`. This registers an
actual candidate *mechanism* for such a proof, or kills the mechanism
cheaply if it is already contradicted by data on record.

## 0. Why this route, and why not the two already killed

`MEMO-RW-DESCENT-EXPLORATION.md` kills "drop a symbol from `W`" descent: the
padding convention (`0^n` prefix) ties the recursion's absolute coordinate
frame to `n` itself, so shortening `W` does not truncate the recursion, it
reframes it.

`RESULTS-ENDPOINT-COORD-DESCENT.md` kills the same shape moved onto the
endpoint/cut coordinate `e`: the deepest cut coordinate `I(e)_t` depends on
a window `e[floor(t/2)..t]` whose width grows linearly with `t`
(`constant_tail_scale.py`'s own docstring), so no fixed offset into a
coordinate-dropped sequence reproduces it exactly. The best achievable rate
(drop-first, best offset) is a flat, non-degenerate `13/32 = 0.4062` from
`n=3` through `n=8` — neither an identity (`->1`) nor a vanishing
coincidence (`->0`).

Both kills are about **exact reduction lemmas**: a map `W -> W'` (or
`e -> e'`) with `|W'| < |W|` that provably preserves membership. Both fail
for the same underlying reason: the object that actually decides survival
at the next forced row (the full `edge`/diagonal array inside
`literal_extension`, `late_pull_diagonal_sat.py:254-273`) is not
summarizable by any fixed-radius window, ever — this matches
`PROOF-STATE-CAPSULE.md` section 5's "Killed mechanism classes" table,
which kills fixed-radius additive energy, fixed finite quotients, and
bounded DFA rank on the same grounds ("a growing ordered dependency diagonal
stores phase in long gaps").

So an **exact** proof mechanism of any of these three shapes (word descent,
coordinate descent, bounded automaton) is closed. What is not yet tried is
a mechanism that does not need exactness: a probabilistic/measure argument
that only has to control an *expectation*, using the empirical constant
that three independent codings now agree on:

- `flip_pairing.py` / `RESULTS-FLIP-PAIRING.md`: coverage alive at
  continuation-level `j` with probability `0.4^j`, independent of flip
  depth (BACKLOG.md section 17).
- `block_halving.py`: measured per-level ratio, same order (BACKLOG.md
  section 17).
- `scratch_endpoint_coord_check.py`: `0.4062` exact-match rate, flat across
  five doublings of `n` (BACKLOG.md section 19, `RESULTS-ENDPOINT-COORD-DESCENT.md`).

A stable non-degenerate constant recurring across three unrelated
constructions is the strongest evidence in this project that survival is
governed by something close to a fixed per-level probability — which is
exactly the ingredient a probabilistic decay argument needs, and exactly
the ingredient an *exact* combinatorial reduction cannot use (a
probability strictly between 0 and 1 is precisely what makes an identity
impossible, per both kills above).

## 1. Grounding H_r(n) exactly, from the code that defines it

`dlp_rotated_wedge.rotated_wedge_population(word, tail, residue)`
(`dlp_rotated_wedge.py:20-51`) is the literal definition. For `n = len(word)`,
`target = n + residue`, `continuation = literal_extension(word, tail, target+2)`:

- `surviving`: every value in `continuation` is in `{1,2}`, and no `1` is
  immediately followed by `1` (hard-core, checked only on the appended
  continuation, indices `>= n`).
- `terminal_pull`: `finite_endpoint[-3:-1] == (1, 2)`, a fixed O(1) check
  at the very end.

`H_r(n)` (as named in `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md`
section 4) is exactly `{W : surviving(W)}` before the constancy question is
even asked — i.e. it is precisely the event that a **deterministic**,
fully-determined-by-`W` continuation of length `n+r+2` happens to avoid the
pattern `11` and land on `(1,2)` at its second-to-last pair. `literal_extension`
makes no free choice at any row (`assert len(candidates) == 1`), so `H_r(n)`
is not a branching process in the usual sense — it is a *deterministic*
predicate on `W`, and the only randomness available to a probabilistic
argument is in the choice of `W` itself, drawn uniformly from `{1,2}^n` (or
from `{1,2}^n` restricted to hard-core `W`, matching S1/S2 in the
forced-terminal-defect prereg).

## 2. The choice point this document must confront directly

A **worst-case** claim would be: for every `W` (or every hard-core `W`),
each additional forced row multiplies survival probability by at most some
fixed `lambda < 1`, uniformly. BACKLOG.md section 17's "per-level E balance
(unconditional)" result is already recorded **false** for the adjacent
(not identical) `flip_pairing` object: individual level-to-level ratios
vary substantially by instance — `99 -> 54 -> 28 -> 18` at `n=16, c=3`
(ratios `.545, .519, .643`), `22 -> 14 -> 12` at `n=10, c=3`, and — the
sharpest counterexample-shaped data point — `6 -> 6 -> 6 -> 6` at `n=9,
c=3`: a family with **ratio exactly 1**, no decay at all, for four
consecutive levels. That last row is a direct existence proof that *some*
sub-population's per-level ratio is not bounded away from 1, for the
flip-pairing object.

This is evidence against, not a formal refutation of, a worst-case claim
for `H_r(n)` itself — `flip_pairing`'s `S_{j+1}/D_j` counts are a related
but distinct object (an injection-pairing count on defect failures, not
`H_r(n)`'s own survival predicate) — but the mechanism producing the `1.0`
ratio (a structured, likely near-constant or checkerboard-like source
sub-family that the forced dynamics treat specially, per
`MEMO-RW-DESCENT-EXPLORATION.md` section 3's parenthetical about the same
suspect words) has no reason to be absent from `H_r(n)`'s own population.
**A worst-case per-`W` contraction bound is registered here as already
disfavored by data, not as formally dead**; this document does not spend a
Setup step re-deriving that disfavor for `H_r(n)` directly, because doing
so would just be S1'/S2-style exhaustive checking, which is cheap but is
measurement, not the mechanism this document is asking for.

**Target registered: the probabilistic/measure-theoretic claim**, not the
worst-case one. Concretely: a conditional geometric-decay bound for
`E_{W}[1_{W in H_r(n)}] = |H_r(n)|/2^n`, conditional on an explicit,
independently-checkable mixing hypothesis (Setup, below) about the forced
continuation — not an unconditional theorem, and not a claim that every
`W`'s individual trajectory contracts.

## 3. Candidate certificate

Model the forced continuation's symbol sequence
`continuation = literal_extension(W, tail, n+r+2)` as, for the purpose of
an upper bound, generated by an **order-`k` Markov chain** on the alphabet
`{1,2}` (k to be fixed empirically in Setup — start at `k=2`, matching the
`literal_witness` hard-core check's own natural window: it looks at
`(previous, forced)` pairs, i.e. `k=1` already appears in the survival
predicate itself, so `k=2` is the first nontrivial extension). Concretely:
estimate `P_hat(next = 1 | last k values = ctx)` empirically from the
already-computed exact small-`n` continuations (no new computation: these
are already produced as a byproduct of the exact enumeration behind
`PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md`'s S1/S1'/S2 and
`RESULTS-FLIP-PAIRING.md`'s runs).

If (and only if) these order-`k` context-conditional frequencies are
**stationary** (stable across position in the continuation and across `n`,
within a stated tolerance) — i.e. the process behaves, empirically, like a
genuine finite-state Markov chain when read off *its own output symbols*
(not off the growing `edge`/diagonal *state*, which is what the two killed
descents needed and could not get) — then the standard Perron-Frobenius
bound applies: the probability of avoiding the forbidden pattern `11` for
`L` consecutive steps under that chain decays as `lambda_2^L`, where
`lambda_2` is the second-largest eigenvalue magnitude of the chain's
transition matrix restricted to the "still alive" (no `11` yet) states.
This gives an explicit, checkable `lambda < 1` and reduces the entire
question to: **is the order-`k` output-symbol Markov model actually a
valid statistical description of `literal_extension`'s output**, which is
an empirical question distinct from (and weaker than) the exact
window-summarizability question the two killed descents asked.

This is a genuinely different mechanism from both kills, not a retry: the
prior two ask "does a bounded window of the internal *state* (edge array,
cut coordinate) determine the next *state* exactly"; this asks "is the
*output* symbol sequence, viewed on its own, statistically indistinguishable
from a bounded-order Markov chain," which can be true even when the
underlying state driving it is provably not window-summarizable (a
deterministic, high-state process can still produce an output sequence
that is empirically Markov of low order — this is the normal situation for
chaotic maps with generating partitions, and is exactly the kind of
"probabilistic ... rather than universal" claim section 4 of this brief
was asked to consider).

## 4. Honest cost of this mechanism, stated before any Setup step runs

This makes the result **conditional on an empirical mixing hypothesis that
is not proven here and may not be provable by this project's existing
tools** — accepting the order-`k` Markov model as a *sufficient*
description, rather than deriving it from `literal_extension`'s actual
recursion, is an assumption, not a consequence of the code. It is adjacent
to (though narrower than) the long-open Rule 30 center-column randomness
conjecture: this document is not proposing to assume that conjecture, only
a much narrower and directly-testable statistical regularity of one
specific forced-continuation construction, at one specific small order
`k`. If the order-`k` model fails empirically (Setup below), that failure
does not bear on the general randomness conjecture either — it only closes
this specific route.

## 5. Setup (before any claim is registered as tested)

- **T1.** Fix `k` (start at 2). From the exact continuations already
  produced for `n=1..16` (existing data, no new run required — these are
  the same continuations `RESULTS-FLIP-PAIRING.md` and the exhaustive
  `H_r(n)` census already computed), tabulate, for every context
  `ctx in {1,2}^k` seen and every row position, the empirical frequency of
  `continuation[row] = 1` vs `2`.
- **T2.** Check stationarity: do these frequencies (a) agree within a
  stated tolerance (propose 0.05) across different row positions for fixed
  `ctx`, and (b) agree within the same tolerance across different `n`?
  Report the full table, not just a pass/fail summary.
- **T3.** If T2 passes, compute the order-`k` chain's Perron-Frobenius
  `lambda` on the "no-`11`-yet" substochastic block and compare it to the
  independently measured `~0.4` constant (flip-pairing, block-halving,
  endpoint-coordinate). Agreement within a stated tolerance (propose a
  factor of 1.5) is a control, not the target itself — the target is the
  existence of a valid `lambda<1`, not a specific numeric match.
- **T4.** If T2 fails at `k=2`, repeat at `k=3` before declaring the
  mechanism dead (one bump in order is cheap and the natural next check;
  more than one bump without a stationarity result is diminishing returns
  and should stop, not escalate silently).

## 6. Kill condition (real, can fire on a plausible negative)

This route is killed if, at every `k` tried up to `k=3` (per T4, not
escalated further without a new idea), the empirical context-conditional
frequencies are **not** stationary within tolerance — i.e. the same
local context `ctx` produces meaningfully different continuation
frequencies depending on `n` or row position, which would mean the process
genuinely depends on the deep, growing history in a way that defeats any
finite-order Markov description of the *output*, not just of the *state*.
This is a real negative outcome distinct from a trivial pass: it is
exactly what would be true if the "0.4062 vs collapsing-to-0/1" data in
`RESULTS-ENDPOINT-COORD-DESCENT.md` reflects genuine long-range dependence
in the output symbols themselves rather than a merely-lossy encoding of a
still-locally-Markov process — the two are observationally different
things, and T1-T2 is the check that tells them apart. If this fires, the
route is dead in the same way the pushdown-language idea died: not run to
completion for lack of nerve, but closed once grounded, because the
conditional mechanism this document proposes has no other leg to stand on
(section 4 already concedes it is not derivable from the recursion
directly, only checkable empirically).

A **secondary, softer** kill: if T2 passes and T3's `lambda` comes out
`>= 1` (i.e. the order-`k` chain predicts growth, not decay, despite
passing stationarity), the mechanism is technically valid but useless for
this project's purpose, and should be recorded as such rather than
re-tuned until it produces a number under 1 (re-tuning after seeing the
answer is exactly the rationalization pattern this project's own mode
file warns against).

## 7. Controls

1. T1's empirical table must independently reproduce (not merely be
   consistent with the order-of-magnitude of) the exact `H_r(n)` emptiness
   through `n=13` when the order-`k` chain's exact small-`n` path counts
   are computed directly (not just the asymptotic `lambda`) — if the chain
   predicts a nonzero `H_r(n)`-analogue count at `n<=13` where the real
   object is exactly empty, the model is wrong regardless of what T2/T3
   say, and this overrides a T2 pass.
2. Cross-check `k=1` (the hard-core check's own native window) explicitly,
   even though it is expected to fail stationarity trivially (the
   `terminal_pull` fixed-pattern requirement and the forced, non-random
   choice at each row make `k=1` almost certainly too coarse) — recording
   the expected failure is cheap and rules out an accidental false-positive
   read of T2 at higher `k` being an artifact of an already-too-coarse
   baseline never being checked.
3. Every frequency in T1 must be computed from `literal_extension` output
   directly (already-existing continuations or a direct re-derivation from
   the unmodified function), never from a reimplementation, matching this
   project's standing convention (`MEMO-RW-DESCENT-EXPLORATION.md`,
   `RESULTS-ENDPOINT-COORD-DESCENT.md`).

## 8. What this does not claim

This does not claim a worst-case per-`W` or per-level contraction bound —
section 2 records that such a claim is already disfavored by data on a
related object (BACKLOG.md section 17's `6->6->6->6` row) and this
document explicitly declines to chase it. It does not claim to derive the
order-`k` Markov model from `literal_extension`'s recursion; it proposes to
test it empirically and treats a stationarity failure as a real, fatal
result, not a reason to raise `k` indefinitely. It does not claim, and
explicitly disclaims, any bearing on the general Rule 30 center-column
randomness conjecture — the hypothesis under test here is narrower (one
forced-continuation construction, one small order) and a negative result
here says nothing about that larger conjecture either way. It does not
claim RW, DLP, SEP, or PT2 is true or false. If this route survives T1-T4,
it produces a *conditional* decay theorem (true given the tested
statistical hypothesis), not an unconditional one — the gap between
"conditional on an empirically-verified-to-tolerance mixing property" and
"proven from the recursion" is not closed by this document and would need
to be named honestly in any later write-up rather than allowed to read as
a full proof.

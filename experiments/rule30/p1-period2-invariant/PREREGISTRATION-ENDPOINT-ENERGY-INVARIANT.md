# Preregistration: amortized drift/credit potential on the survivor population

Date: 2026-09-04. Status: design only. No script has been written or run for
this document; no existing file was modified. Every quantity named below
that is not marked "already measured" is a proposal to compute later, not a
result.

## 0. Why this route, and why it is not a retry of the killed potential

Two literal `n -> n-1` coordinate-dropping reductions have already been
killed on this object: dropping a symbol of the source word `W`
(`MEMO-RW-DESCENT-EXPLORATION.md`, padding-coupling obstruction) and
dropping an endpoint coordinate `e` while holding distance-to-cut fixed
(`RESULTS-ENDPOINT-COORD-DESCENT.md`, stable ~40.6% coincidence rate, no
identity). Both fail for the same underlying reason: `constant_tail_scale.py`'s
cut coordinate `I(e)_t` depends on a window `e[floor(t/2)..t]` whose width
*grows linearly with `t`*, so no fixed-radius truncation of the current
state can stand in for the missing coordinate. A related but distinct
object, the mortality profile `M(n,H)`, also killed an exact "one-seed/two-
follow" semantic peel `(n,H) -> (n-1,H-2)` against a direct counterexample
(`RESULTS-ENDPOINT-PEEL.md` section 3, the length-4/length-3 witness). That
document's own closing line names the escape hatch this preregistration
takes: *"does not rule out an amortized induction with a proved credit."*
`MEMO-RW-DESCENT-EXPLORATION.md`'s closing line names the sibling escape
hatch: a proposal phrased on `e` rather than `W` "would be a different,
unexplored proposal" — already tried exactly once (coordinate descent,
killed), not tried as an amortized/statistical argument.

Separately, BACKLOG.md item 4 (the D8 "weighted contractive potential")
already killed a *different* proposal that this document must not
re-propose under a new name: a fixed weighting `v` over the 8 D8 classes
such that every individual `(class, symbol)` transition strictly decreases
`v`-weighted energy. That is vacuous because every class reaches all 8
successor classes ("complete branching" — `CONTINUATION-PROMPT.md` lines
503-521 record this for the D8 and D8-x-carry observers by name). Any Phi
proposed here that reduces to a snapshot function of the *current* bounded
D8/carry state, applied deterministically per step, is the same killed
object and must be rejected on sight.

## 1. Exact target

Same numerical target already on record as open in `BACKLOG.md` section 17
(the "counting line" row) and section 4 of `PREREGISTRATION-RW-FORCED-
TERMINAL-DEFECT.md`'s ancestor line of reasoning: for fixed `(n, c)`, with
`N_j = |S_j(n,c)|` the RW/DLP survivor population at level `j` exactly as
defined in `flip_pairing.py` (`S_j`: alive through level `j`, forced cell
equals `c` and hard-core at every `j' < j`), prove

```text
N_j <= 3 * 2^(n - j)          for all n, all j, both c            (counting-line, RW-alpha form)
```

not merely observe it holds through `n=18` (`block_halving.py`'s measured
`C(n, 1.0) = 1` for `n=10..18`, `C=3` needed only at `n=9`). Block halving
(`block_halving.py`) already proves a *weaker* statement computationally
through `n=18` (least `k <= 3` with `N_{j+k} <= N_j/2`) and is on record as
"true, too weak": rate `1/k` bit/level cannot reach the rate-1 the counting
line needs, and, like the counting line itself, is checked only up to
`n=18`, not proved for all `n`.

This document does not propose a new numerical target. It proposes a new
*mechanism* — an amortized, history-dependent credit/drift argument — for
closing the gap between "measured through `n=18`" and "true for all `n`",
in place of the two mechanism classes already killed: (i) an exact bijective
reduction (`MEMO-RW-DESCENT-EXPLORATION.md`, `PREREGISTRATION/RESULTS-
ENDPOINT-PEEL.md`), and (ii) a per-step deterministic weighted-class bound
(BACKLOG item 4).

## 2. Why `N_j` itself, not a per-word state, is the object carrying Phi

`S_{j+1}(n,c) subseteq S_j(n,c)`: for *fixed* `n`, a source `W` either has
already failed by level `j` or has not; `S_j` is a monotone-shrinking subset
of the same fixed `2^n`-element universe as `j` increases (`flip_pairing.py`'s
own definition: "alive at level `j`" requires surviving every `j' < j`).
There is therefore no `n -> n-1` reduction to build here at all, and none is
proposed. The quantity under induction is `j`, at *fixed* `n`, and the
"reduction" this document needs is an inductive bound on the **population
count** `N_j`, not a map between individual words of different lengths.
This is the concrete instance of the hint in the task brief: treat the
population size itself as the potential, not a per-word state.

Write `Dead_j = S_j \ S_{j+1}`, the sources that fail exactly at step `j`
(disjoint union of `D_j`, the strict-E-failure set already defined and
computed by `flip_pairing.py`, and a second set `B_j` — junction/hard-core
failures at step `j`, not yet separately reported but computable from the
same `hcs[w][j]` array `flip_pairing.census` already produces). Since
`N_{j+1} = N_j - |Dead_j|`, the target inequality is exactly a statement
about the *sequence* `|Dead_0|, |Dead_1|, ...` averaging to at least one bit
of population loss per level, in the aggregate, over long enough windows —
which is consistent with, and does not contradict, the already-recorded
fact that single-step halving is false at deep levels
(`RESULTS-FLIP-PAIRING.md` section 2, `BACKLOG.md` section 17's second row:
`99 -> 54 -> 28 -> 18` at `n=16, c=3` is *not* a per-step halving sequence,
yet decays overall).

## 3. Candidate potential Phi and the proposed mechanism

**Phi (population level).**

```text
Phi_j := log2(N_j) + j
```

(`N_j <= 3 * 2^(n-j)` is exactly `Phi_j <= n + log2(3)`, a bound on `Phi`,
not a claim that `Phi` is non-increasing — `Phi` can and does fluctuate
level to level, since `|Dead_j|` is not a constant fraction of `N_j` at
every `j`.) This restates the counting line; it is not new by itself and is
not being registered as a discovery. What is new is part 3b: a candidate
*mechanism*, tied to a per-survivor unbounded-history statistic, for why
`Phi` stays bounded instead of drifting upward, stated so it can be tested
and can fail.

**3b. Per-survivor running charge (the object that must be genuinely new).**

For a fixed survivor `w in S_j`, its forced continuation up to level `j`
passes through a sequence of D8 classes `sigma_0(w), ..., sigma_{j-1}(w)`
(the same "current D8 class of the forced step" object BACKLOG item 4
weighted and killed). Fix a partition of the 8 D8 classes into two subsets
`F` ("credit") and `F^c` ("debit") — the specific partition is a free
parameter of the design, to be chosen by the verification step below, not
asserted here. Define the **running charge**

```text
k(w, j) := #{i < j : sigma_i(w) in F} - #{i < j : sigma_i(w) in F^c}
```

`k(w, j)` is an unbounded, signed, history-dependent integer — it is a sum
over the *entire* path so far, not a function of the current state alone.
This is the concrete difference from the killed BACKLOG item 4 potential:
that potential asked "does the current class deterministically bound the
next class" (no, by complete branching); this one asks "does the *running
sum* of a fixed per-step score, accumulated over unboundedly many steps,
correlate with imminent death," which complete branching does not address
at all (complete branching is a one-step reachability fact; a running sum's
drift is a statement about the *distribution* of many steps, not about
which individual transitions are reachable).

**The conjecture.** `k(w, j)` behaves like a biased random walk with
negative drift under the actual (hard-core + `E=c`) forcing dynamics, and
`w` leaving `S_j` (dying) is disproportionately likely once `k(w, j)` has
drifted below some threshold — i.e., death is well-modeled as an absorption
event of a negative-drift walk, not as a uniform per-survivor coin flip
independent of history. If true, a gambler's-ruin/optional-stopping bound
on the walk gives an O(1) expected level-of-death, which forces the
population-level geometric decay the counting line needs, *without* ever
claiming a deterministic per-step exclusion rule (which complete branching
already rules out). This is offered as a candidate *explanation* for the
already-measured `0.4^j`-type decay constants (`BACKLOG.md` section 17's
flip-pairing coverage rate, `RESULTS-ENDPOINT-COORD-DESCENT.md`'s
independently-measured ~0.4062, block-halving's per-level ratio) — three
numbers already on record as converging on the same order of magnitude,
here treated as evidence *of a phenomenon needing a mechanism*, not
re-cited as if they already were one.

## 4. Setup (to be run later; nothing here has been executed)

1. Using `flip_pairing.census` unmodified, extend it to also record, for
   every `w` and every `j`, the current D8 class `sigma_j(w)` alongside the
   already-computed `keys`, `cells`, `hcs` arrays (the class is already
   computable from the same forced-orbit trace `census` builds; this is
   additional logging, not new machinery).
2. Fix a small enumerated list of candidate partitions `F / F^c` of the 8
   D8 classes (all `2^8/2 = 128` partitions is feasible to sweep at small
   `n`; do not hand-pick one partition and declare success on it alone).
3. For each candidate partition, each `(n, c)` in the existing swept range
   (`n = 9..18`, both `c`, matching `flip_pairing.py`/`block_halving.py`'s
   own horizon — no horizon extension), compute `k(w, j)` for every alive
   `w in S_j`, every `j`.
4. Test the conjecture directly: for each `(n, c, F)`, fit the empirical
   relationship between `k(w, j)` and the indicator "`w` dies at level `j`"
   (e.g. death rate in each `k`-bucket, or a logistic fit); report the
   sign and stability (across `n = 9..18`) of the correlation, not a single
   summary statistic.

## 5. Kill condition (must be able to fire on a plausible negative, and does)

Kill this entire mechanism class — do not retry a different `F` under a new
name — if any of the following holds:

- **No-drift.** For every candidate partition `F`, the death rate in each
  `k`-bucket is statistically flat (within noise) rather than increasing as
  `k` decreases — i.e., accumulated history does not predict imminent
  death any better than the current state alone did (which is already
  known to fail, per BACKLOG item 4). This directly falsifies the
  "history matters, current state doesn't" premise the whole design rests
  on.
- **Unstable sign.** A partition `F` shows a negative-drift correlation at
  small `n` (say `n <= 12`) that flattens, vanishes, or reverses sign by
  `n = 18` — i.e., the effect is a small-`n` finite-size artifact, not a
  structural drift that would extrapolate to a proof for all `n`.
- **No absorption structure.** Even where a drift correlation exists, if
  the *conditional-on-survival* distribution of `k(w, j)` does not show the
  concentration/truncation signature of an absorbed random walk (e.g. its
  variance keeps growing linearly in `j` among survivors, rather than
  saturating near the death threshold), the gambler's-ruin argument in
  section 3b does not apply even where a correlation exists, and this
  document's proposed *proof mechanism* is dead even if the underlying
  numerical fact (the counting line) later turns out to be true by some
  other argument.
- **Reduces to the killed object.** If the only partitions `F` that show
  any correlation are ones where the correlation is fully explained by
  `sigma_{j-1}(w)` alone (the single most recent class, ignoring the rest
  of the running sum) — i.e., the history-dependence adds nothing beyond
  the current-state snapshot — this has silently rediscovered BACKLOG item
  4's already-killed per-step class potential wearing a running-sum
  disguise, and must be reported as such, not as a new result.

A negative on any of the above kills the amortized/drift *mechanism*, not
the counting-line inequality itself, which would remain open (as it is
today) for some other argument.

## 6. Controls

1. Recompute `block_halving.py`'s existing `k <= 3` result and
   `flip_pairing.py`'s existing coverage numbers from the *same* extended
   `census` call used for this design's `k(w,j)` logging, as a regression
   check that the added instrumentation did not change the underlying
   forced-orbit computation.
2. Report the exact partition `F` tested and its class membership
   explicitly in any result document, not just a correlation coefficient —
   a later reader must be able to check by hand whether a "successful" `F`
   is secretly equivalent to conditioning on `sigma_{j-1}(w)` alone (the
   fourth kill bullet above).
3. Any claimed drift must be checked against a shuffled control: randomly
   permute each survivor's own class sequence before computing `k(w, j)`
   and re-run the same death-rate-by-`k`-bucket fit. A real history-drift
   effect must vanish (or weaken sharply) under this shuffle, since the
   shuffle destroys temporal order while preserving the per-level marginal
   class distribution exactly; if the correlation survives the shuffle
   unchanged, it is a marginal-distribution artifact, not evidence of
   drift, and counts as a no-drift kill.
4. No horizon extension past `n = 18`; no sampling in place of the existing
   complete census.

## 7. What this does not claim

This does not claim the counting line, RW, DLP, or period-two exclusion is
true or false. It does not claim `k(w,j)` is a martingale, does not claim
any specific partition `F` will show the conjectured drift, and does not
claim that a positive drift finding alone would constitute a proof (a
gambler's-ruin bound on an empirically-fit walk is evidence toward an
inductive argument, not a substitute for one — turning a confirmed drift
into an actual bound on `N_j` for all `n` is explicitly out of scope for
this document and would be its own follow-up preregistration). It does not
reuse or extend `rank_zero_separator.peel`/`peel_power`, which
`MEMO-RW-DESCENT-EXPLORATION.md` part 4 already shows presupposes rather
than supplies the `n -> n-1` reduction this line of attack does not need in
the first place, since section 2 above establishes the induction here is on
`j` at fixed `n`, not on `n`.

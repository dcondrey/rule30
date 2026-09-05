# Preregistration: measure-zero suppression of the period-2 defect under the uniform source measure

Date: 2026-09-04. Status: design only. No census, no code changes, no
scripts run. Frozen before any run.

## 0. Why this route, and why not a fourth combinatorial descent attempt

Three independently-coded measurements now agree on a constant near `0.4`:
flip-pairing's per-level flip-survival probability `0.4^j` independent of
flip depth (`BACKLOG.md` section 17), block-halving's per-level halving
ratio (same section, too weak alone at rate `1/k` bits/level), and today's
endpoint-coordinate-drop check's flat `13/32 = 0.4062` match rate across
`n = 3..8` (`RESULTS-ENDPOINT-COORD-DESCENT.md`). That document's own
verdict is explicit: the recurring `~0.4` is "evidence *for* a
probabilistic/measure-theoretic framing... and evidence *against* any exact
combinatorial descent of the kind fusion #2 proposed." Three encodings
converging on one constant, after three combinatorial reduction attempts
(source-word descent, endpoint-coordinate descent, block-halving) all fail
to turn that constant into an identity, is the actual argument for trying a
different *kind* of tool here rather than a fourth variant of "find an exact
reduction" under a new name.

This document is that different kind of tool. It does not attempt to beat
the growing-dependency-window obstruction (`constant_tail_scale.py`'s own
docstring, cited in `RESULTS-ENDPOINT-COORD-DESCENT.md` section 2) with a
sharper combinatorial reduction. It asks instead whether the obstruction can
be routed *around*: accept that no fixed-radius exact law exists, and ask
whether the *aggregate* ratio `|H_r(n)| / 2^n` — already the pre-registered
open question in `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md` section 4 —
can be shown to vanish (or shown to be summable) by a genuine probabilistic
argument, and whether that vanishing, once established, licenses an honest
measure-zero statement about configurations rather than just a ratio.

It must also directly confront the standing negative result that makes this
harder than it looks: `BACKLOG.md` section 17's "per-level E balance
(unconditional)" found STRICT per-level balance is false — survivor counts
trend `99 -> 54 -> 28 -> 18` at `n=16,c=3` but sit flat `6 -> 6 -> 6 -> 6`
at `n=9,c=3` for several levels. Any argument here that secretly assumes a
uniform per-step contraction is already falsified data, not a design
choice. Section 3 below is built to survive this fact rather than ignore
it.

## 1. The non-i.i.d. warning, read from the actual forcing code

`late_pull_diagonal_sat.literal_extension` (lines 254-273) computes, for
each of the `rows` appended positions, all 4 candidate symbol values and
asserts `len(candidates) == 1`: exactly one symbol forces
`append_dependency_edge(...)[-1] == tail`. This is a **deterministic**
function of the source word `W` (and the fixed padding prefix) — there is
no random choice anywhere in the continuation. `psi_kernel.psi` confirms
the same shape at the `Q_n`/`Psi_n` level: `chosen` is asserted unique.
`append_dependency_edge` itself (`constant_tail_scale.py:205-218`) also
confirms the already-documented obstruction directly: `edge` grows by one
entry per appended symbol and every new entry folds in the *entire* prior
edge vector (`for order in range(2, len(edge) + 1)`), not a fixed window.
So "randomness" in everything below means exactly one thing: **the
uniform Bernoulli(1/2) measure on the choice of the finite source word
`W in {1,2}^n`**, pushed forward through the deterministic map
`W -> (does literal_extension(W, c, n+r+2) survive hard-core + 12a-terminal)`.
It is not randomness in the Rule 30 update rule, not an i.i.d.
coin-flipping model of the cellular automaton's rows, and it must not be
silently treated as giving independent per-row events — the deterministic,
full-history-dependent forcing gives no such independence, and the
balance-false finding in section 0 is direct evidence that naive per-row
independence would be wrong if assumed.

This is why the mechanism chosen in section 3 is deliberately the one
classical tool that needs **no independence assumption at all**.

## 2. Precise formal target

Fix a residue `r in {0,1,2}` and tail `c` (as in `H_r(n)`,
`PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md` section 4). Let
`Sigma = {1,2}^N` (one-sided infinite binary source sequences) carry the
Bernoulli(1/2) product measure `P` (each coordinate an independent fair
coin over the alphabet `{1,2}`, matching the uniform measure already used
for every finite-`n` census in this project). For each `n`, define the
cylinder event

```
C_n(r) = { W in Sigma : W[1..n] in H_r(n) }
```

i.e. `C_n(r)` depends only on the first `n` coordinates of `W` and holds
exactly when the length-`n` prefix is one of the sources whose forced
continuation is a live RW/DLP candidate. Because `literal_extension` is a
pure function of the finite prefix (section 1), `C_n(r)` is a well-defined
cylinder set and

```
P(C_n(r)) = |H_r(n)| / 2^n
```

exactly — the same ratio already tracked (not a new quantity, not a
redefinition).

**(M1) Target statement (Borel-Cantelli).** If

```
sum_{n=1}^infinity  |H_r(n)| / 2^n   <  infinity                     (*)
```

then, by the first Borel-Cantelli lemma (no independence hypothesis
required — it holds for *any* sequence of events with summable
probabilities), `P(limsup_n C_n(r)) = 0`. That is: **for
Bernoulli(1/2)-almost every infinite source word, the length-`n` prefix is
a live RW/DLP-candidate (in `H_r(n)`'s sense) for only finitely many `n`.**

`H_r(n)` is the *candidate* population — sources whose forced continuation
survives hard-core and `12a`-terminal, "the population for which an RW
witness is even a live possibility before asking about constancy"
(`PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md` section 4) — not the
smaller set of sources for which a witness (an actual constant-`Psi`
defect trace) exists. Write `A_n(r) subset C_n(r)` for the corresponding
witness-level cylinder event. Since `A_n subset C_n` for every `n`,
`limsup_n A_n(r) subset limsup_n C_n(r)`, so `(*)` bounds the *stronger*
(witness) claim by proving the *weaker* (candidate) one: if candidates
themselves are eventually exhausted almost surely, so are witnesses. This
is why proving something about `H_r(n)` (already the object this project
tracks) is the right target rather than reaching for `A_n(r)` directly,
which has no independent census of its own here.

This is the precise, checkable-in-principle claim this document
registers. It is a conditional theorem (condition `(*)` implies the
measure-zero conclusion) plus a proposed, explicitly flagged-as-unproven
route to `(*)` (section 3). It is deliberately **not** the stronger
statement "the candidate condition holds at no `n`" — see section 6, and
see section 3.5 for why BC1 gives "finitely often," not "never."

## 3. Candidate proof mechanisms for `(*)`

**(M1) itself needs no mechanism beyond summability** — that is the entire
point of using Borel-Cantelli here instead of a coupling or ergodic
argument that would need mixing or independence. Two independent routes to
`(*)` are on the table; this document does not commit to either, since
neither is established, but registers both so a later reader can check
which (if either) is viable before investing proof effort:

**(M2) Borrow route.** `BACKLOG.md` section 17's counting-line result,
`N_j(n) <= C * 2^(n-j)` (empirically `C=1` for `n=10..18` except one `C=3`
exception at `n=9`; `C<4` suffices), if ever proven as an actual theorem
(it is currently an empirical measurement, not a proof, and this document
does not attempt to supply one), gives at `j=n`: `N_n(n) = |H_r(n)| <= C`,
a constant independent of `n`. Then `|H_r(n)|/2^n <= C / 2^n`, which is
summable by comparison with a geometric series. If the counting-line bound
is ever proved, `(*)` follows immediately and for free — this document's
contribution in that case is purely the M1 upgrade step (ratio-decay implies
almost-sure finitely-many-witnesses), which is not currently stated anywhere
in the project.

**(M3) Amortized block-halving chain (the actually new mechanism proposed
here).** `BACKLOG.md` section 17 already contains the needed ingredient,
scored "true, too weak" for a *different* purpose (it cannot reach the
rate-1 that `(RW-alpha)` needs), but summability does not need rate 1 —
any positive rate suffices, geometric or not. Block-halving states:
`N_{j+k} <= N_j / 2`, least `k <= 3` for all `n = 11..18`, sources and
states (`block_halving.py`). This is exactly an *amortized*, not
per-step, contraction: it makes no claim about `N_{j+1}` vs. `N_j`
individually — a flat `6 -> 6 -> 6 -> 6` run (length 3, i.e. `k=3`, or
even a length-2 flat stretch) is fully consistent with `N_{j+3} <= N_j/2`
and is not a counterexample to it. This is the honest reconciliation with
section 0's balance-false finding that a per-step drift condition cannot
achieve: block-halving does not need per-level uniformity, only that the
population have halved by `k` levels later, however unevenly it gets
there.

Chaining the bound over `floor(n/k)` disjoint blocks of length `k` (using
only that `j -> N_j(n)` is non-increasing, checked as V-step V3 below, to
apply the same `k`-step halving repeatedly without needing it to hold at
every offset):

```
N_{km}(n)  <=  N_0(n) / 2^m   =   2^n / 2^m       (with j_0=0, N_0(n)=2^n)
```

so at `j = n` (taking `m = floor(n/k)`),

```
|H_r(n)| = N_n(n)  <=  2^n / 2^floor(n/k)  =  2^{n - floor(n/k)}
```

giving

```
|H_r(n)| / 2^n  <=  2^{-floor(n/k)}                                  (***)
```

With `k <= 3` (the measured range), `(***)` is geometric with ratio at
worst `2^{-1/3}` per unit `n`, hence `sum_n |H_r(n)|/2^n` converges by
comparison with a geometric series — `(*)` follows, PROVIDED `k` stays
bounded as `n` grows past the measured range `n=11..18`. This is the
actual open hypothesis this route rests on, not an assumption smuggled in:
whether the *same finite* `k` (or any `n`-independent bound on `k`)
continues to work is an extension of an existing measurement, not a new
kind of claim, and is exactly what section 4's V2/V5 ask to check before
any proof effort.

Two facts this chain leans on and that must be verified by reading
existing code/logs, not assumed, before this mechanism is adopted:
(a) `j -> N_j(n)` is non-increasing in `j` for fixed `n` (surviving to
level `j+1` implies having survived to level `j`) — expected from the
construction but not independently confirmed here; (b) the index
alignment `N_n(n) = |H_r(n)|` — that "level `n`" in the block-halving /
counting-line sense is the same terminal check `H_r(n)` uses, not an
off-by-`r`-or-two misalignment. Both are section 4, V3.

## 3.5. Why this buys "finitely often," not "ever," and what would close that gap

The task this document answers asks about configurations that *ever*
exhibit the defect, i.e. `P(union_n A_n(r)) = 0`, a strictly stronger
statement than BC1's `P(limsup_n A_n(r)) = 0`. BC1 does not give the union
directly. What it does give, combined with the union bound and the exact
empty census already established through `n = N_0 = 13`:

```
P(union_n A_n(r))  <=  P(union_{n<=13} A_n(r)) + P(union_{n>13} A_n(r))
                     =  0 + P(union_{n>13} A_n(r))
                     <=  sum_{n>13} |H_r(n)|/2^n
```

using `A_n subset C_n` again for the last step. This is a genuine
quantitative TAIL BOUND on `P(ever)`, driven toward (but not forced to)
zero as the census horizon `N_0` extends and as `(*)`'s tail sum shrinks —
it is not itself zero unless every individual term is zero, which is
exactly `H_r(n) = emptyset` for all `n`, i.e. the DLP/RW nonexistence
claim this project has not proved. So the honest picture is: `(*)` plus
the existing empty census gives a shrinking upper bound on `P(ever)`, not
a proof that `P(ever) = 0`. Closing that last gap would require either the
stronger per-`n` statement `|H_r(n)| = 0` for ALL `n` (which is DLP/RW
itself, out of scope) or a separate argument that the tail sum can be made
arbitrarily small in a way that forces the union's probability to zero in
the limit as `N_0 -> infinity` for a FIXED family of events (it cannot,
in general, for a genuinely infinite union with a non-vanishing but
summable tail) — so this route's ceiling is the BC1 "finitely often"
statement of section 2, not the "ever" statement, and that ceiling is
stated here rather than blurred.

## 4. Setup / verification steps (design only — none of this has been run)

- **V1.** Confirm (by re-reading, not re-deriving) that `H_r(n)` membership
  is a pure function of the length-`n` prefix with no dependency on any
  assumed future continuation — already true by construction of
  `literal_extension(word, tail, rows)`, which takes only `word` as input;
  record this as closed by code inspection (same style as
  `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md` section 2's S1), not a
  pending run.
- **V2.** Extend the exact `H_r(n)` census as far past `n=13` as is
  computationally feasible (bounded by the same state-space limits noted
  elsewhere in this project), to get more terms of `(*)`'s partial sums.
  Currently all terms through `n=13` are exactly zero for all `r`
  (contributes nothing to summability risk); the open question is the
  first nonzero term's location and its subsequent trend, not re-litigated
  here.
- **V3 (verify the two facts (M3)'s chain leans on, by reading, not
  re-running).** (a) Confirm `j -> N_j(n)` is non-increasing for fixed `n`
  in `block_halving.py`'s / the counting-line data's own construction —
  check the code defines "surviving to level `j`" as a strict prefix
  condition (surviving to `j+1` implies surviving to `j`) rather than an
  independent per-level test that could in principle un-survive and
  re-survive. (b) Confirm the index alignment `N_n(n) = |H_r(n)|` — that
  block-halving's/counting-line's "level `n`" terminal count is the exact
  same quantity as `H_r(n)`'s terminal hard-core+`12a` check, not an
  `r`-shifted or off-by-a-constant relative of it (recall `H_r(n)`'s
  continuation has length `n+r+2`, not `n`; confirm block-halving's `N_j`
  indexing already accounts for this or state explicitly how it maps).
- **V4.** Check whether flip-pairing's `0.4^j`, already found "independent
  of depth `delta`" for `n=9..16`, remains independent of `delta` if the
  existing logs are re-cut by absolute position rather than depth-from-end
  (a change of variable, not a new run) — this is supporting evidence for
  the chain's plausibility, not a requirement of the chain itself (the
  chain in (M3) needs only block-halving's `k`, not a mixing rate).
- **V5 (the actual open hypothesis to extend).** Re-run (or extend, if
  already logged past `n=18` anywhere) `block_halving.py`'s search for the
  least `k` such that `N_{j+k} <= N_j/2` holds for all `j`, across the
  largest feasible `n` beyond the already-measured `n=11..18`, and record
  whether `k` stays bounded (supports `(*)` via the chain in section 3) or
  grows with `n` (kills it — see K1).

None of V1, V3, V4 requires new code. V2 and V5 require extending existing
computations (a census, and a search already coded in `block_halving.py`)
past their currently measured ranges; no new instrumentation is proposed.

## 5. Kill conditions

- **K1 (kills M3 specifically, without necessarily killing M1/`(*)`,
  fires on a measurable and currently nonzero quantity).** `|H_r(n)| = 0`
  for `n <= 13` makes "does the ratio decay" ill-posed as a direct test
  while every term is exactly zero — but block-halving's `k` is nonzero
  and measured now (`k <= 3` for `n = 11..18`, entirely inside the
  zero-census range, since `k` is a statement about the survivor DAG's
  structure, not about `H_r(n)` being nonempty). The genuine, currently
  checkable kill condition for this route is: **does `k` (least block
  length for `N_{j+k} <= N_j/2`) stay bounded as `n` grows past the
  measured range, or does it grow with `n`?** Bounded `k` (even a larger
  constant than 3) keeps `(***)`'s geometric decay and preserves `(*)`.
  `k` growing with `n` — e.g. `k = Theta(log n)` gives only quasi-polynomial
  decay (still summable, boundary case, must be checked directly) and
  `k = Theta(n^epsilon)` or worse kills geometric decay and very plausibly
  kills `(*)` outright. This fires on a plausible, currently-open negative
  (V5) and does not require waiting for `H_r(n)` to become nonempty to
  evaluate.
- **K2 (kills the whole route, restates the standing kill condition in
  `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md` section 4 in probability
  language).** If, once `H_r(n)` is nonempty at some feasible `n`, the
  ratio `|H_r(n)|/2^n` is subsequently found NOT to decay at all — stays
  within a constant factor of its first-nonzero value as `n` grows further
  — then `(*)` fails at the level of individual terms not vanishing, and
  no summability argument, block-halving-based or otherwise, can rescue
  it. This is the terminal kill condition for the whole document, not just
  (M3).
- **K3 (kills the practical value of this whole document even if `(*)`
  is eventually true).** If, on inspection, establishing `(*)` by any
  available means turns out to require smuggling in the very per-history
  uniform decay that section 0's balance-false finding already falsifies —
  i.e., if no honest aggregate-only argument can be constructed and every
  attempt reduces to assuming what is already known to be false — then this
  document has contributed nothing beyond restating the open ratio-decay
  question in heavier notation, and should be recorded as killed on those
  grounds rather than kept open indefinitely.

## 6. Controls

1. `P(C_n(r))` as used in `(*)` must equal `|H_r(n)| / 2^n` exactly as
   already defined and tracked in `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md`
   section 4 — no silent redefinition of `H_r(n)` or of the measure.
2. Any non-increasing-in-`j` check, index-alignment check, or extended
   `k`-search produced under V3/V4/V5 must be computed by re-reading or
   re-running existing `block_halving.py`/`flip_pairing.py` code and logs
   already in this directory, not by inventing a new statistic, so a later
   reader can tell a re-analysis or extension of old data from a new
   experimental claim.
3. The Borel-Cantelli step (M1) itself requires no simulation or census to
   verify as a piece of mathematics — it is a two-line classical lemma —
   and no computational "check" of it is proposed; only `(*)`'s hypothesis
   needs empirical/analytic support, and that boundary must stay explicit
   in any writeup that builds on this document.

## 7. What this does not claim

- Does **not** claim PT2 (period-2 exclusion) for all configurations.
  Measure-zero is compatible with a nonempty exceptional set of
  configurations that do exhibit the defect; a measure-theoretic argument,
  even if it fully succeeds, closes a strictly weaker question than the
  project's actual target and does not substitute for it.
- Does **not** claim independence of per-row or per-level events at any
  point. The entire reason (M1)/Borel-Cantelli was chosen over a coupling
  or mixing-based large-deviation bound is that BC1 needs no such
  assumption; independence is never invoked in section 2 or 3.
- Does **not** claim the deterministic forced continuation map has any
  intrinsic randomness. All probability statements are over the choice of
  the finite source word under the uniform product measure, pushed through
  a fixed deterministic map, per section 1.
- Does **not** claim the block-halving `k` stays bounded past the measured
  range `n=11..18`. Section 3's chain states this as the open hypothesis
  `(*)` rests on, and K1 is built specifically to fire if it fails.
- Does **not** claim `(*)` itself holds. Both routes offered to it (M2,
  borrowing an unproven counting-line bound; M3, the block-halving chain,
  conditional on `k` staying bounded) are open, and this document runs
  neither and extends neither.
- Does **not** claim `P(ever)= 0`. Section 3.5 states explicitly that BC1
  gives only the weaker "finitely often" conclusion, and that closing the
  gap to "ever" would require the full DLP/RW nonexistence claim
  (`H_r(n) = emptyset` for all `n`), which is out of scope here.
- Does **not** claim any new numeric result. Every number cited above
  (`0.4`, `0.4062`, `13/32`, `k<=3`, the `99->54->28->18` and
  `6->6->6->6` trajectories, `H_r(n)` empty through `n=13`) is quoted from
  already-existing documents in this directory, not measured here.

## 8. Whether determinism already closes this route

No, not by itself. Section 1's warning is real and does rule out any
mechanism that needs per-row independence or a uniform per-history mixing
rate — which is exactly why no i.i.d.-coin-flip or uniform-coupling
argument is proposed anywhere above. But Borel-Cantelli's first lemma
(section 2) is independence-free by construction, and the block-halving
chain (section 3, M3) is an *amortized* statement over `k`-blocks, not a
per-step or per-trajectory one, so it is not automatically falsified by
the balance-false finding either — a flat run of length up to `k` is
explicitly compatible with it. It is merely *threatened* by it in the one
specific, checkable way K1 names (does `k` stay bounded as `n` grows). The
honest status is: open, with a named and checkable risk, not closed by
the deterministic-forcing objection.

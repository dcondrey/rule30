# Where this session's spectral work lands in the R1..R7 register: R7, not R1

Session 2026-09-05. Every claim below is quoted from the file named, read this
session, not carried over from a summary.

## Short answer

**It maps to R7, tightly, and to R1 only through R7.** The de Bruijn/window
construction is R7's own machinery, and the vacuity found this session is an
independent rediscovery of R7's already-recorded blocker on a different state
space. It is **not** a new obstruction, and it says nothing directly about R1.

## R7: three exact correspondences

**1. The construction is R7's, already characterized.** `PATH.md:1417-1419`:

> The one formalization that does have real cycle structure (a sliding-time-window
> SFT/de-Bruijn graph) **is not new — it is the R7 ladder automaton**, already
> characterized under **obstruction F** (`RESULTS-ladder-rung1.md`; row 7), with
> a verdict already on record.

So a De Bruijn adjacency matrix over a sliding window is not an alternative to
R7; it *is* R7's encoding.

**2. The blocker is named, and the second half is exactly what I proved.**
`PATH.md:587` gives R7's status as STALLED with:

> Blocker is a **state-count wall plus the free-boundary escape**, not compute.

The vacuity result in `RESULTS-WINDOW-SPECTRAL-RELAXATION.md` — the free
incoming `(h,F)` cell can always be steered onto the target, at every width,
because `h' = h XOR a XOR 1` with `a` depending only on the left parent — **is a
free-boundary escape.** Same mechanism, different state space (RW `(h,F)` cells
rather than the ladder's columns).

**3. R7 already recorded the reason widening fails.** `PATH.md:299-301`:

> Do NOT re-run at larger R or k, and do NOT raise the Diff bound Q — both
> directions are now measured closed by the same mechanism, **constraint and
> freedom growing together.**

"Constraint and freedom growing together" is precisely the `w`-independence of
`lambda_max = phi`: each extra window level adds a constraint *and* an extra
free boundary cell, and they cancel exactly. R7 measured this; this session
proved it for the RW window.

## The number 4 is the same 4 in all four places

`RESULTS-ladder-rung1.md:118-123` gives the ladder automaton's state counts:

```
R=1->2:     428 ->    1445   ratio 3.376
R=2->3:    1445 ->    5574   ratio 3.857
R=3->4:    5574 ->   22087   ratio 3.963
R=4->5:   22087 ->   88136   ratio 3.990
R=5->6:   88136 ->  352329   ratio 3.998
```

Converging to exactly **4**. That is the same 4 as:

| where | appearance |
|---|---|
| R7 ladder automaton | `4^R` states — the state-count wall |
| Fibonacci/fiber bound | fiber factor `2^n/4^k` |
| this session's relaxation | the free cell ranges over `4 = \|{(h,F)}\|` values |
| null transfer matrix | `phi/4` — "uniform over 4 states, subject only to no-11" |

**The state-count wall and the fiber factor are one quantity seen from two
sides.** The ladder needs `4^R` states precisely because the fiber factor is
`4^{-k}` and nothing compresses it — corroborated independently by exact DFA
minimization achieving **zero** collapse (`RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md`:
minimized sizes `5, 17, 65, 257, 1025, 4097, 16385, 65537 = 4^(h+1)+1`) and by
the proved `k_dia(L) = L` in `RESULTS-DIAGONAL-MEMORY.md` ("a sufficient
statistic for RW survival cannot forget, because the diagonal does not").

Note also `PATH.md:304-306`: the one constraint that reaches the unmodelled
region is the full 1-pin at the boundary column, which "prunes 58% and **flips
no verdict**, and which **costs the Rule 90 soundness control**." Consistent
with `RESULTS-ladder-rung1.md:118-123`, where the pin cuts states 1.9x-7.5x and
every verdict stays NONEMPTY.

## R1: no direct mapping, and claiming one would be a type error

`PATH.md:295` describes R7 as "per-period exclusion by omega-automata,
**mechanizing R1**", with two decidable modes per `(p,k)` (`PATH.md:317-320`):

- **mode (i)** emptiness of `S_k(p)` — proves `Thm(p)` outright. **Provably
  dead** (limitation theorem; `plain_{R,k}(w)` nonempty for every `R,k,w`).
- **mode (ii)** inclusion `S_k(p) ⊆ {col_{-1} eventually periodic ...}` —
  **this is R1's implication itself**, mechanized. Untouched.

So R1 is reachable from here only *through* R7 mode (ii). The Fibonacci/fiber
apparatus does not touch R1 directly: it lives on the rotated wedge over words
`{1,2}^n`, whereas R1 is about columns of the genuine lone-seed diagram. This
session already recorded one instance of exactly that type mismatch —
`phi/4` (a rotated-wedge per-row survival eigenvalue) versus the zero-set
density (measured **0.500362** at `T = 200000`) — and asserting a second one
would repeat it.

**What can honestly be said about R1:** the wall this session hit is the wall
mode (ii) would have to climb, since mode (ii) is an inclusion check on the same
ladder automaton whose states grow `4^R`. That is evidence about the *cost* of
mechanizing R1, not evidence about R1's truth.

## Consequence for what to do next

- **Do not build a De Bruijn/window automaton for this.** It is R7's encoding,
  its verdict is on record (all `p = 2..8` NONEMPTY, verdict uniform in `R`, `k`
  and `Q`), and `PATH.md:298-299` explicitly says not to re-run at larger `R`,
  `k` or `Q`.
- **Do not spend compute on R7 mode (i).** Closed by a proved limitation
  theorem.
- R7 mode (ii) is untouched but inherits the `4^R` wall.
- The unblocked work remains where the previous handoff put it: **R1 directly**
  (the general-finite-row zero-set obligation, A8), and the split argument
  identified in `RESULTS-FIB-FIBER-UNIFICATION.md`.

  **Corrected 2026-09-05.** This bullet previously read "the bulk is fine, the
  obstruction is the small-`S_k` tail". That framing was **withdrawn** the same
  day (commit `cc22299`, correction recorded in
  `RESULTS-WINDOW-SPECTRAL-RELAXATION.md` and
  `RESULTS-FIB-FIBER-UNIFICATION.md`): the per-step failure is *not* confined to
  a small-population tail — it is falsified entrywise, weighted-for-every-weight,
  and at every population floor tested (violations at `S_k` up to at least 255).
  A per-step ceiling was always the wrong object. The live target is the
  **product**: the induction needs `S_need / S_0 < 2^-n`, i.e. a geometric mean
  below `1/phi = 0.61803`, not a uniform per-step bound. Scored against a
  pre-registered kill condition over 24 cells `n = 10..24`, both tails, the kill
  did **not** fire: max geometric mean `0.5987` (`n=12, c=2`). See
  `RESULTS-PRODUCT-GEOMETRIC-MEAN.md`. That pass rests on a *fitted*, not proved,
  slope separation (`log_phi(D_peak) ~ 0.398n` against `m' ~ 0.217n`, fitted
  `n <= 24`).

## Correction to my own framing earlier this session

`RESULTS-WINDOW-SPECTRAL-RELAXATION.md` presents the vacuity result as a kill of
"the naive width-`w` window truncation". That stands, but it understated the
prior art: the free-boundary escape was **already named as R7's blocker** in
`PATH.md:587` before this session. The result is a proof of a mechanism that was
already recorded as measured. Logged here rather than by rewriting that file, so
the sequence stays auditable.

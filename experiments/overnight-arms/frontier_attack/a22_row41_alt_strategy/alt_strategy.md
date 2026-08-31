# a22 — row 41 alt-trace fiber, alternative strategy after Lemma S is dead

Read in full before this: `a5_row41_fiber_uniform/row41_fiber_uniformity.md`
(Lemma S, shallow-locality of the pin parity, refuted) and
`docs/rule30/RESULTS-alt-trace-fiber.md` (survivor automaton, `{1,4}`
wallpaper). This document does **not** repeat the shallow-locality
truncation attempt. It does three things: (A) an algebraic decomposition of
the pin-parity quantity that isolates exactly where Rule 30's nonlinearity
enters and explains why a naive GF(2) generating-function argument is a
dead end in its linear form; (B) a reframing of the open question as a
**streaming/register compression** question, which is strictly more general
than Lemma S and is *not* refuted by a5's argument; (C) a precise statement
of the finite-left-support lemma the `{1,4}` wallpaper forces any proof to
use. **Verdict: no proof, no new exclusion. One concrete reframing (B) that
survives a5's kill, one algebraic fact (A) that explains why it's hard, one
sharpened lemma statement (C).**

---

## A. The pin-parity quantity is linear-plus-a-genuine-quadratic-form, not linear

The survivor step is `o[m] = u[m] OR v[m]` and the quantity that decides
survival is `parity(o) = XOR_m o[m]`, `m = 0..T-1`. Over GF(2), `a OR b = a
XOR b XOR (a AND b)` termwise, so summing over `m`:

```
parity(o) = parity(u) XOR parity(v) XOR corr(u, v),   corr(u,v) := XOR_m (u[m] AND v[m])
```

**Verified** (`bilinear_decomp_check.py`, read-only reuse of a5's
`band_automaton.forced_step`/`seed_state`, which is read-only reuse of the
repo probe): this identity reproduces the actual pin/rho drive bit on every
substep, `kseed=10` to 8 pairs (8792 checks) and `kseed=12` to 16 pairs
(33628 checks), both phases, 0 mismatches.

`parity(u)` and `parity(v)` are **GF(2)-linear** functionals of the state —
exactly the kind of quantity a rational generating function over
`GF(2)[[x]]` handles natively (a linear recurrence in the coefficients has a
rational g.f.; this is the standard toolkit for *additive* CA like Rule 90 —
Martin–Odlyzko–Wolfram 1984, "Algebraic properties of cellular automata" —
where the local rule is GF(2)-affine and the whole space-time pattern is a
2D linear recurrence over GF(2), decidable by linear algebra / the
transfer-matrix method).

`corr(u,v)` is **not** linear in the state; it is a genuine bilinear form
(the same-index GF(2) dot product of the two frontier vectors). This is the
*entire* Rule-30-specific content of the map: Rule 90's version of this
automaton (a5 §6, `forced_step_90`) replaces OR by a bare projection
(`g(a,b)=b`), which has no AND term and no `corr(u,v)` at all — its pin
quantity is 100% linear, hence tractable by exactly the linear methods that
don't touch Rule 30. This is *why* Theorem A / Theorem C / Lemma D in a5 are
proved to hold verbatim for Rule 90 (§6 of a5's doc): every claim proved
there is a claim about the **linear part only**, `parity(u) XOR parity(v)`,
or about vanishing (Theorem C, which only needs the OR/AND-vs-projection
distinction not to matter on an all-zero region — `0 OR 0 = 0 AND 0 = 0`
either way). Nothing in a5 touched `corr(u,v)` because Lemma S was posed as
a windowed-determinism question on the raw state, not as a question about
this specific bilinear term.

**Conclusion of (A):** a *linear* GF(2) generating-function / transfer-matrix
argument, run naively on `L_(T+1) = v XOR parity(o)`, is not a new strategy —
it is exactly the strategy that Martin–Odlyzko–Wolfram already show applies
only to additive rules, and a5 §6 already demonstrates empirically that
every structural fact provable by such linear methods here is Rule-90-blind.
This is a **known-dead-end restatement**, in research-mode Part 0 terms: it
is not worth spending a test on. The open content is entirely inside
`corr(u,v)`, a quadratic (degree-2 Reed–Muller) form on the frontier bits.
A genuine generating-function argument would have to be one for the
*Hadamard product* (coefficientwise AND) of two GF(2) power series, which
does not have a rational or even algebraic closure in general — Hadamard
products of algebraic series are famously not algebraic (this is the
classical obstruction; cf. the general failure of Hadamard-product closure
for algebraic/automatic power series, in contrast to ordinary product and
sum). So (1) as posed in the brief is not a free lunch; it correctly
identifies the right object (`corr(u,v)`) but the "does it admit a g.f.
argument" question reduces to a question already known to be hard in
general, not a shortcut.

## B. Reframing that is NOT killed by Lemma S: streaming compression, not windowed compression

Lemma S asked: is `parity(o[g..T-1])` a function of a **bounded raw window**
`u[g..g+M), v[g..g+M)` of the *current* state? a5 killed this (unbounded
active width, explicit witness pairs agreeing on every window up to
`M = aw-2` and disagreeing on the very next pin parity).

That is a narrower question than the one that actually matters for
uniformity. What matters is whether there is **any** finite-state predictor
at all — i.e. a DFA reading the `rho`-stream online, maintaining a bounded
register `R` (not a window into the raw frontier), updated by a fixed
transition function at each rho/pin substep, such that `R` alone determines
the next pin-parity bit. Call this:

> **LEMMA S′ (streaming compressibility).** There is a constant `M` and a
> finite-state transducer `(Q, |Q| <= 2^M, delta, phi)` reading the rho-bit
> stream online (one bounded-size state per substep, updated only from the
> previous state and the current rho bit) such that `phi(state)` equals the
> next pin-parity bit, for every state reachable from a finite (left-depth-`d`)
> seed, for every `d`.

**Why S′ is strictly weaker than (harder to kill than) S**, and why a5's
argument does not touch it: Lemma S's refutation works by exhibiting two
*raw states* that agree on a window but differ in a *tail cell outside the
window* with a nonzero OR-partner, forcing different `corr`. A streaming
automaton is never asked to reconstruct that tail cell from a window of the
*current* raw state — it could instead have already folded that cell's
contribution into `R` back when that cell was first emitted (every cell is
emitted exactly once, at the step it becomes the shallow-most new entry).
Concretely: `corr(u,v) = XOR_m u[m] AND v[m]`, and every summand `u[m] AND
v[m]` is *available at the substep where `u[m]` is created* if `v[m]` (one
step older) is already known — which it is, since `v` is literally `u` from
the previous substep. So a register `R := R XOR (new_u_bit AND
old_partner_bit)` maintained incrementally, one bit per substep, computes
`corr` exactly, with **register size 1**, *if* the only content of state
that matters for future correlation is this running total. The catch,
identical to Kill 2's finding, is that `corr` restarts fresh at every `T`
(it's over `m = 0..T-1`, the *whole* current frontier, not an
incrementally-extended window) — so a naive single running register does
NOT compute the version of `corr` needed at the *next* `T` without
re-summing all `m`, because `u` and `v` are not append-only: `u` at time
`T+1` is the *entire* `parity(o[0..m-1])` prefix-scan of `o`, not `u` at
time `T` with one bit appended. This is exactly why the map is not an
append-only stream in the naive sense, and it is the concrete obstacle any
attempt at S′ must clear — but note it is a *different* obstacle from
Lemma S's (tail sensitivity to unseen raw bits), so a5's kill does not
transfer. **This lemma is open, unattempted here beyond this framing, and is
the recommended next target.** A finite-state search for it (brute-force
enumeration of transducers up to some `|Q|`, tested against the same
`out_kseed10.txt`-style witness generation a5 already has code for) is
concrete future work but was not run in this pass (budget).

## C. The exact finite-left-support property the wallpaper forces you to use

The `{1,4}` wallpaper member (`RESULTS-alt-trace-fiber.md`, "left-periodic
members" section) is a state whose forced orbit survives every pin check
forever, with a left half that is spatially 7-periodic **all the way to
depth infinity** — it never has an all-zero deep segment at any depth. This
is the single fact that rules out any invariant/potential argument that
does not use left-*finiteness*, and a5's Theorem C already isolates the
correct discriminator:

> **Theorem C restated as the discriminator.** A state is reachable from a
> finite left-depth-`d` seed **iff** (necessary, not sufficient — this
> direction is what Theorem C proves) `u_T[m] = 0` for all `m < (T-d)/2`,
> i.e. the deep segment of the frontier is *identically zero* below a
> threshold that advances at rate `1/2` per rho/pin pair. The wallpaper
> member violates this for every `d` (no `m`-threshold below which it is
> ever zero), which is exactly why it is not a left-finite counterexample.

The precise lemma that remains needed, combining (B) and (C):

> **LEMMA (target, combining S′ and the zero-prefix constraint).** Restrict
> attention to frontier pairs `(u,v)` possessing a growing all-zero deep
> prefix (Theorem C's constraint, for *some* `d`, not fixed in advance).
> Show that `corr(u,v)` — equivalently, the pin-parity bit — cannot equal 1
> forever along the forced orbit. Equivalently: the "active" (non-zero-prefix)
> segment of the frontier, which by Kill 2 grows by exactly 1 cell per
> rho/pin pair, cannot sustain `corr = 1` on every pin substep indefinitely.

This is *not* a locality claim (S and S′ are about compressibility; this is
a claim about the actual infinite-time behavior of `corr` restricted to the
zero-prefixed reachable set) and is not refuted by anything in a5 — a5's
Kill 1/Kill 2 are about compressibility of the *predictor*, not about
whether the predicted quantity is eventually forced to 0. This is the
sharpest form of "Claim(d) for every d" the repo currently has: a statement
purely about the bilinear form `corr` restricted by the zero-prefix
constraint, with the linear terms (`parity(u)`, `parity(v)`) and Rule-30/90
distinction cleanly separated out by part (A).

## What this does NOT do

* No new exclusion beyond the register's `d <= 24`. No orbit was extended.
* Lemma S′ is stated, not proved or disproved. No transducer search was run.
* The Hadamard-product non-closure remark in (A) is a general fact about
  algebraic power series, cited as the reason the naive g.f. idea in the
  brief's point (1) doesn't shortcut anything; it is not itself a proof
  about this specific `corr(u,v)`.
* Row 41 status is unchanged: **OPEN**.

## Known-result check (brief's point 2)

Parity-of-count / quadratic-form-of-digit-string sequences do have a
tractable literature (Rudin–Shapiro sequence: parity of the number of `11`
occurrences in binary expansion, a quadratic GF(2) form, and it is
2-automatic — Allouche–Shallit, *Automatic Sequences*, ch. 3). But that
tractability rests on the quadratic form's window being of **bounded width
in the input's own digit expansion** (adjacent-pair count). Here `corr(u,v)`
ranges over a window whose width is the *entire active region*, proved
unboundedly growing in a5 §5 (Kill 2). That is the structural disanalogy
that blocks importing the Rudin–Shapiro toolkit directly: it is exactly
Lemma S′'s open question, restated as "is this specific unbounded-width
quadratic form nonetheless computable by a bounded automaton," which is
known to hold for *some* unbounded-width quadratic forms (Rudin–Shapiro is
one, cast differently) and known to fail for others. No existing theorem
found that settles this particular form either way; this is reported as a
literature check that came back open, not as a citation that closes
anything.

## Reproduction

```bash
cd experiments/overnight-arms/frontier_attack/a22_row41_alt_strategy
uv run python bilinear_decomp_check.py 10 8     # 8792 checks, 0 mismatches
uv run python bilinear_decomp_check.py 12 16    # 33628 checks, 0 mismatches
```

Both read-only import `a5_row41_fiber_uniform/band_automaton.py`, which
read-only imports the repo probe. No file outside this directory was
written. Paid model-provider calls: $0.

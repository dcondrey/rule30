# NEGATIVE-NAMES-MISSING-LEMMA — missing lemma: **shallow-locality of the pin parity**, i.e. "there is a constant `M` such that the pin parity `parity(o[g..T-1])` of a survivor state is a function of its front-anchored width-`M` window". FALSE: by tail sensitivity of the OR-word parity plus the unbounded growth of the active region (no constant `M` survives), and witnessed on the reachable set by explicit seed pairs at two seed radii, both phases.

Row 41, alternating-trace fiber survivor automaton.  Attack on the
uniformity gap (`docs/rule30/RESULTS-alt-trace-fiber.md`, register row 41).
Nothing here proves P1, P2 or P3, and nothing here excludes the alternating
trace at any depth the register does not already record.

---

## 0. What was attempted, and the one-sentence outcome

Obstruction H says per-`d` certificates can never reach uniformity by
themselves, so the assignment was to find structure in the closed-form
survivor automaton `L_(T+1) = v XOR parity(o_1..o_T)` that is provably the
same at every `d`: an invariant, a lasso, or a bounded state count.

Such a structure exists and is exhibited below (Theorem A, Lemma D): in
time-anchored coordinates the survivor map is a fixed second-order
recurrence with no dependence on `d`, on `T`, or on the phase, and it is
locally determined from its deep end.  **The structure is real and it is
`d`-uniform.  It is also blind to the kill condition, provably and by a
measured margin, and it holds verbatim for Rule 90.**  So the uniformity gap
is not closed and this route does not close it.

---

## 1. PROVED and VERIFIED: the deep-anchored normal form (Theorem A)

Index the reconstruction frontier by **time** rather than by depth.  Write

```text
u_T[m] := x(m, -(T-m))   for m = 0..T-1,        u_T[T] := c_T
```

so `u_T[0] = x(0,-T) = L_T` is the forced output and `u_T[T]` is the trace
bit.  In these coordinates the probe's frontier pair `(A, B)` is
`(u_T, u_(T-1))`, the probe's convention `B_0 := c_(T-1)` is exactly the
shallow slot `u_(T-1)[T-1]`, and the whole survivor map is

```text
o[m]        = u_T[m] OR u_(T-1)[m]                      m = 0..T-1
u_(T+1)[m]  = parity( o[0..m-1] )                       m = 0..T
u_(T+1)[m+1]= u_(T+1)[m] XOR ( u_T[m] OR u_(T-1)[m] )   (same thing)
```

with `u_(T+1)[0] = 0` automatically (the new forced output vanishes), and the
kill condition at a pinned step is `parity(o) = u_(T+1)[T] = 1`, the
**shallow-most** entry.

This is a change of coordinates on the register's already-recorded closed
form, not a new theorem about Rule 30.  Its content is that the resulting
recurrence carries no `d`, no `T` and no phase: the parameter that the
certificate ladder is indexed by has disappeared from the map.

**Verification** (`band_automaton.py --validate`, output `out_kseed10.txt:1`).
200 random `rho` drives of length 40, both phases, every step, four identities
against the repo's verified probe (`experiments/rule30/alt_trace_fiber_probe.py`,
read-only): `parity(o)` equals `_or_parity`; the successor equals `_wf_step`
re-read deep-anchored, for the general drive `v` (entries offset by
`v XOR parity(o)`); the forced drive gives new output `0`; and the
reconstructed outputs match `left_from_rho`.  **PASS.**

## 2. PROVED and VERIFIED: the deep-anchored truncation is vacuous (Theorem C)

The obvious way to get a bounded state count is to truncate to `m < M`.  It
is available — the recurrence reads only indices `< m` — and it is worthless.

**Theorem C.**  On any orbit surviving to time `T` from a knee seed of left
depth `d`, `u_T[m] = 0` for every `m < (T-d)/2`.

*Proof, exact, no gap.*  The rotated rule gives
`x(t,-(j+1)) = x(t+1,-j) XOR (x(t,-j) OR x(t,-(j-1)))`.  Survival means
`x(0,-j) = 0` for `d < j <= T`.  Induction on `t`: if `x(t,-j) = 0` on
`d+t < j <= T-t` then the three row-`t` terms vanish for
`d+t+1 < j <= T-t-1`, so `x(t+1,-j) = 0` there.  Setting `j = T-m`, `t = m`
gives the claim. ∎

**Corollary.**  For every fixed band height `M` the deep-anchored truncation
`u_T[0..M-1]` is eventually the all-zero fixed point.  Its lasso is trivial
and decides nothing.  **The "bounded state count" reading of the uniformity
target is retired in its natural coordinates.**

**Verification** (`--cone 10`, `out_kseed10.txt:3-5`).  All `2^10` `rho`-seeds
per phase (left depth `d = 20` for phase `01`, `d = 21` for phase `10`), every
surviving state up to 24 rho/pin pairs: 6792 states checked, **0 violations**.

## 3. PROVED and VERIFIED: the correct finite-state object leaks (Lemma D)

Let `g` be the joint front `min{m : u_T[m] = 1}` over the pair.  Below `g` the
OR-word vanishes, so `u_(T+1)[m] = parity(o[g..m-1])`.

**Lemma D.**  The successor's values on the absolute interval `[g, g+M)` are a
function of `(u_T, u_(T-1))` on `[g, g+M-1)` alone.

**Why this is not an autonomous automaton, and this is the whole finding.**
The front advances (`g' = g` or `g+1`, rate `1/2` per substep).  A
front-anchored width-`M` window therefore determines the successor only on a
width-`M-1` window once the front moves: the window **leaks one cell per front
advance**.  It buys a finite look-ahead, not an invariant.

**Verification** (`--window 10 24`, `out_kseed10.txt:8`).  376,832 checks over
all `2^10` seeds per phase, 8 steps each, `M = 2..24`: **0 contradictions**.

## 4. KILL 1: Lemma S is false, by tail sensitivity and by witnesses

**The argument, which needs no measurement.**  The pin parity is

```text
parity( o[m] : g <= m <= T-1 ),      o[m] = u_T[m] OR u_(T-1)[m].
```

Take any tail index `m*` outside the window with `u_(T-1)[m*] = 0`.  Flipping
`u_T[m*]` flips `o[m*]`, hence flips the pin parity, and leaves the width-`M`
window untouched.  So no function of `2M` window bits computes the pin parity
unless the window happens to determine every tail cell whose OR-partner is
`0`.  §5 then finishes it: the active region grows by one cell per rho/pin
pair without bound, so no **constant** `M` can survive.

The measurement's job is therefore narrow and it is the job the argument
cannot do alone: to show that such tail pairs actually occur among states
**reachable from finite seeds**, which is the only set the uniformity target
cares about.

**Exhaustiveness scope, stated precisely.**  All `2^k` `rho`-seeds of length
`k`, both phases, taken at the knee (`T = d`, with `d = 2k` for phase `01`
and `2k+1` for phase `10`) — the identical seed set the register's
`forced_orbit` measurement uses — over the first 48 rho/pin pairs of the
parameter-free forced continuation.  `k = 8` and `k = 10` were both run.
Nothing is claimed for seeds outside this set, and nothing is claimed for
`d > 24`; no certificate ladder was extended.

Write `H(M)` for the largest `h` such that the first `h` pin parities are a
function of the width-`M` window over that set.  Measured (`out_kseed10.txt:11-58`,
`out_kseed8.txt`): `H(M) <= 1` for every `M` up to `aw - 2`, where `aw` is the
maximum active width over the seed set (20 and 21 at `k = 10`; 16 and 17 at `k = 8`).  Every row prints
a witness pair; e.g. `k = 10`, phase `01`, `M = 18`: seeds `0000000000` and
`1111111000` share their width-18 window and disagree on the very first pin
parity.  **Those witness pairs are the load-bearing output of this section.**

**What the table does NOT show, stated so nobody quotes it.**  At the knee
`T = d`, so the front sits at index `0` and `aw` equals the state length.
`M = aw` is therefore the whole state, and the jump of `H` to the cap at
`M = aw - 1` is a restatement of that fact, not a discovered threshold.  Do
not read a step function into it.

What survives the objection is the within-class behaviour just below the top:
the mean within-class deviation of the pin rate from `1/2` is 0.077 at
`M = 2` and still only 0.4805 at `M = 18`, where **5 of 308 classes remain
mixed** — one cell short of the entire state and locality still fails.
Near-determinism is not determinism.

**Past the knee, where the scales do separate, the reachable set is too thin
to test.**  Advancing `2^12` seeds by 5 rho/pin pairs (`--window 12 34
--offset 5`, `--coverage 12 --offset 5`, `out_offset5.txt`, `out_coverage.txt`)
gives window, active width and state length as three distinct scales
(`aw = 27..29` against state length 34).  But only 180 (phase `01`) and 142
(phase `10`) states survive, and from `M = 16` upward **no window class
contains two distinct full states** — every class is one state reached by
several seeds.  `H(M)` there is measuring coverage, not locality, and is
reported as such.  This is a limitation of the measurement, not evidence for
Lemma S.

## 5. KILL 2, measured: the deciding window grows without bound

`--growth 10`, `out_kseed10.txt:59-68`, all `2^10` seeds, phase `01`:

```text
pair  survivors  active width (min/mean/max)
   0        512   17 / 20.55 / 21
   1        268   18 / 21.60 / 22
   2        187   19 / 22.66 / 23
   3        115   20 / 23.57 / 24
   4         67   23 / 24.66 / 25
   5         31   25 / 25.94 / 26
   6         15   27 / 27.00 / 27
   7         15   28 / 28.00 / 28
```

The active width grows by exactly `1` per rho/pin pair (front at `(T-d)/2`,
shallow end at `T`, so width `(T+d)/2`).  This is the half of Kill 1 that
needs no sampling: the region the pin parity reads is unbounded along any
surviving orbit, so **no constant `M` satisfies Lemma S**, whatever the
reachable set looks like at any single time.

Separately, this says something about the register's obstruction-A exemption
for row 41, and it is a different quantity from the one the register measures
(the register's exemption is about certificate levels `k(d) ~ d` colliding
within one cone-return time, a statement about ladder termination, not about
state counts).  Row 41 does escape the `O(log t)` wall: the two anchors
separate at rate `1/2`, not logarithmically.  But linear separation still
gives an exponential state count.  **The exemption from obstruction A does not
by itself repair obstruction H.**

## 6. Rule 90 filter — the structure fails it

`--rule90 10`, `out_kseed10.txt:71-75`.
`ensemble_filter.center_column("90", 20000)`: zero ones at `t > 0`, so Rule
90's lone-seed centre is eventually periodic, as the filter requires.

Rule 90 rotated is `x(t,x-1) = x(t+1,x) XOR x(t,x+1)`, i.e. `g(a,b) = b`, so
`o[m] = u_(T-1)[m]` and the normal form of §1 holds with the OR replaced by a
projection.  Lemma D's fixed-anchor determination was run on both:

```text
rule 30 fixed-anchor determination (Lemma D): 22400 checks, 0 contradictions -> HOLDS
rule 90 fixed-anchor determination (Lemma D): 22400 checks, 0 contradictions -> HOLDS
```

**The deep-anchored normal form, Theorem C's vanishing, and Lemma D all hold
verbatim for Rule 90.**  Every structural fact found in this cycle is
therefore Rule-90-blind and proves nothing on its own.  The only
Rule-30-specific ingredient in the object is the pin parity — and §4 is the
measurement that the structure cannot see it.

## 7. Single-column sensitivity filter

No new statistic of the lone-seed space-time diagram is introduced here, so
`discriminator.py`'s overwrite test has no argument to take.  The quantities
measured (`H(M)`, active width, mixed-class fraction) are functionals of the
fiber over a **prescribed** centre column — the object is *defined* by
conditioning on column 0 being `(01)^inf` or `(10)^inf`, which is precisely
the modification the discriminator applies as its perturbation.  The filter
is passed by construction, in the same sense as register rows 25/26.  This is
a statement about relevance, not about strength: relevance was never the
problem here.

## 8. The missing lemma, stated so it can be attacked or refused

> **LEMMA S (shallow-locality of the pin parity).**  There is a constant `M`
> and a function `phi: {0,1}^M x {0,1}^M -> {0,1}` such that for every
> survivor state `(u_T, u_(T-1))` reachable from a finite seed,
> `parity(o[g..T-1]) = phi(u_T[g..g+M), u_(T-1)[g..g+M))`, where `g` is the
> joint front.

With Lemma S, Lemma D turns the survivor automaton into a genuine finite
automaton on `4^M` states, its lasso structure is decidable, and Claim(d) for
every `d` reduces to one emptiness check — the uniformity target, closed.

**Lemma S is false as stated**: by §4's tail-sensitivity argument together
with its reachable-set witnesses for every `M` below the active width, and by
§5's unbounded active width, which alone rules out any constant `M`.  Any
repair must therefore either (i) anchor at the shallow end
instead, where the map is not autonomous, or (ii) supply a compression of the
active region that the OR-word's parity respects — which is a statement
about Rule 30's nonlinearity, not about the automaton, and is the same
obligation the register already records at rows 31 and 41.

This document does not supply either, and does not claim a step "under an
appropriate uniformity/composition/descent lemma" — the point of the document
is that the lemma such a step would need is Lemma S, and Lemma S is measured
false rather than merely unproved.

## 9. What a reader must not over-read

* **No new exclusion.**  No `d` beyond the register's `d <= 24` is certified
  here, and none was attempted.  The seeds used are `k = 8, 10` (`d = 16, 20,
  21`), strictly inside the recorded range, and they are diagnostics for the
  invariant hunt, exactly as the brief required.
* **§1 is a coordinate change, not a theorem about Rule 30.**  The closed form
  it re-expresses is the register's, already proved.
* **§2 and §3 are proved, but they are proved for Rule 90 too.**  Do not
  quote Lemma D as progress on P1.
* **§4's witnesses and §5's table are measurements over a stated finite set**,
  not proofs about all `d`.  The refutation of Lemma S rests on the
  tail-sensitivity argument plus unbounded active width; the measurements show
  the failure occurs on the reachable set rather than only in principle.  Lemma
  S was the only bridge on offer here; this is not a proof that no finite
  invariant of any kind exists.
* **§4's `H(M)` table is not a threshold discovery.**  At the knee `M = aw` is
  the whole state, and past the knee the reachable set thins to the point where
  window classes hold one state each.  Quote the witnesses and the mixed-class
  counts, not the jump.
* **The row 41 status is unchanged: OPEN.**  This cycle removes one candidate
  bridge (finite-state truncation of the survivor automaton, in every
  anchoring tried) and quantifies why it fails.  It does not kill row 41, and
  it does not advance it.
* The `{1,4}` wallpaper member's infinite-left seed still shows any proof must
  use left-finiteness; nothing here changes that, and the forced map studied
  here is parameter-free precisely because left-finiteness has already been
  spent to fix the front.

## 10. Reproduction

From this directory:

```bash
uv run python band_automaton.py --validate               # Theorem A
uv run python band_automaton.py --cone 10                # Theorem C
uv run python band_automaton.py --window 10 24           # Lemma D + Kill 1
uv run python band_automaton.py --growth 10              # Kill 2
uv run python band_automaton.py --rule90 10              # Rule 90 filter
uv run python band_automaton.py --window 8 24            # Kill 1 at k = 8
uv run python band_automaton.py --window 12 34 --offset 5    # past the knee
uv run python band_automaton.py --coverage 12 --offset 5     # coverage caveat
```

Saved outputs: `out_kseed10.txt` (validate, cone, window, growth, rule90),
`out_kseed8.txt`, `out_offset5.txt`, `out_coverage.txt`.  Everything ran
locally in a few minutes total.  Paid model-provider calls: $0.

**Fence, verified not asserted.**  `git status --porcelain -- .` over
`13-rule30` shows exactly one tracked modification, `docs/rule30/PATH.md`,
which was already modified before this session began (mtime 13:48, predating
the first write here) and was not touched.  The only new path is this
directory.  The single side effect outside it is a refreshed
`experiments/rule30/__pycache__/alt_trace_fiber_probe.cpython-311.pyc`,
written by importing the probe; no source file outside this directory was
created or modified.  The repo probe
`experiments/rule30/alt_trace_fiber_probe.py` is imported read-only and is the
source of every ground-truth comparison.

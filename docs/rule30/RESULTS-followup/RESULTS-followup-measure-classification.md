# Follow-up: panel Direction 2 ("point-specific omega-limit classification") vs R8

## Status

**Verdict: DUPLICATE-OF-R8**, modulo one factual correction to the panel's
own Rule-90 screen. No new theorem, no new open problem. Everything
executable here is either PROVED (elementary, given below) or MEASURED
(explicitly labeled).

Working directory for this follow-up:
`experiments/overnight-arms/roundtable_followup/measure_classification/`
(script: `rule90_omega_limit.py`). `PATH.md` was read, not touched.

## What the panel proposed, and what R8 already says

Panel Direction 2, verbatim object:

> `Omega(e) := ∩_{N≥0} closure{F^t e : t≥N}`, `M_e := {μ : μ is F-invariant
> and supp(μ) ⊆ Omega(e)}`. Classification target: for all `μ ∈ M_e`,
> `μ[x_0=1] = 1/2`, plus uniqueness of the one-site marginal (or the weaker
> Cesàro statement).

`e` is a single **row** (an element of `{0,1}^Z`, the lone-seed initial
configuration), `F` is the CA **global map** (not a shift), and `Omega(e)`
is the classical omega-limit set of a point under a continuous self-map of
a compact space — this is exactly the object studied by Host-Maass-Martínez
(DCDS 2003), Pivato (DCDS 2005), and Sablik (ETDS 2007), which R8 already
cites verbatim as "known inputs" and "every published rigidity theorem
requires algebraic/bipermutative structure ... Rule 30 is left-permutative,
nonlinear, outside all of them, and Pivato's survey names the nonlinear
case as an open gap" (`PATH.md`, R8 paragraph 2).

R8's object, verbatim:

> `Y` = closure of the vertical (time) shifts of the lone-seed diagram in
> `{0,1}^{Z^2}`. ... every vertical-shift-invariant measure on `Y` assigns
> the centre cell density 1/2.

`Y` lives in `{0,1}^{Z^2}` (full 2D spacetime diagrams), and the dynamics
is the **vertical shift** `σ_v` (shift the diagram one row in time), not
`F` directly.

### Are these the same object?

They are different spaces (`{0,1}^Z` acted on by `F`, vs `{0,1}^{Z^2}`
acted on by `σ_v`), but they are tied together by the standard
"spacetime-diagram" (trajectory) embedding, which is exactly why R8 chose
the shift formulation in the first place:

1. **Intertwining.** Let `π₀ : Y → {0,1}^Z` be the row-0 projection. Because
   every point of `Y` is (a limit of) an actual spacetime diagram generated
   by iterating `F`, `π₀(σ_v y)` (row 1 of `y`) equals `F(π₀(y))` (row 0
   pushed one step by `F`). So `π₀` intertwines `(Y, σ_v)` with
   `({0,1}^Z, F)`. Pushing forward any `σ_v`-invariant measure on `Y` under
   `π₀` gives an `F`-invariant measure on `{0,1}^Z`, and the pushforward's
   centre-cell marginal equals the original's centre-cell marginal (they're
   literally the same coordinate, row 0 site 0 in both pictures).

2. **Where the pushforward lands.** `Y` is defined as the closure of the
   forward orbit of one specific spacetime diagram `D` (the lone-seed
   diagram) under `σ_v`. A standard fact about orbit closures of a single
   point under a continuous map on a compact space: every invariant
   probability measure on `closure{T^n x : n≥0}` is supported on `ω(x)`
   (non-recurrent transient points of a single orbit carry no invariant
   mass unless they are themselves periodic, and periodic points already
   lie in their own omega-limit set). Applying this with `x=D`, `T=σ_v`:
   every `σ_v`-invariant measure on `Y` is supported on `ω(D)` under the
   vertical shift, and its row-0 image under `π₀` is supported on `π₀(ω(D))
   ⊆ ω(e)` under `F` — i.e. supported on `Omega(e)` as the panel defines
   it. So R8's classification claim, if proved, **implies** the panel's
   Direction-2 claim by direct pushforward.

3. **The converse (lifting).** Conversely, any `F`-invariant measure `ν` on
   `{0,1}^Z` supported on `Omega(e)` can be lifted to a `σ_v`-invariant
   measure on the corresponding spacetime-diagram space by the standard
   natural-extension / suspension construction (deterministically generate
   row `t+1` from row `t` via `F`, `ν`-a.e.); this lift is supported on `Y`
   because `Omega(e)`-supported rows only ever generate spacetime diagrams
   in the closure of the lone-seed orbit. So the two families of invariant
   measures are in essentially bijective correspondence via projection and
   lift.

**Conclusion on (1):** Direction 2, read literally, is a *lower-dimensional
restatement* of R8's classification target, using the "naive"/classical
configuration-space formulation (`F` acting directly on `{0,1}^Z`) instead
of R8's spacetime-shift embedding. R8 deliberately moved to the shift
formulation because the classical `F`-invariant-measure literature
(Host-Maass-Martínez, Pivato, Sablik) is blocked for Rule 30 by the
bipermutativity requirement — and Direction 2's `M_e`/`Omega(e)` machinery
*is* that classical formulation, restricted from "all invariant measures on
the full shift" down to "measures supported on one seed's omega-limit set."
That restriction (single-seed orbit closure, not the whole space) is the
one place Direction 2 narrows the classical target — and R8 makes the
identical narrowing move (`Y` = closure of *the lone-seed diagram's* orbit,
not all of `{0,1}^{Z^2}`). The two routes narrow the same classical problem
in the same way, in two different but equivalent representations. This is
DUPLICATE, not a genuine variant: no new mathematical content, no new
technique implied, and it inherits the same "controlling what `Y`/`Omega(e)`
contains may require knowing the column" circularity R8 already names as
its honest risk.

## Checking the panel's Rule-90 screen (point 2)

The panel's stated screen: *"For Rule 90, `Omega(e)` is the singleton
`{0^∞}` and the classification is trivially false (`0 ≠ 1/2`)."* This
conflates "the centre **column** is eventually zero" (true, and already the
exact fact R8's own filter cites) with "the **whole configuration**'s
omega-limit set is the single point `0^∞`" (false). Rule 90 from a lone
seed produces the growing Sierpinski/Pascal-mod-2 triangle: only the exact
centre column collapses to 0; the rest of the configuration keeps
generating fresh nonzero structure forever, so the *point* `e`'s orbit does
not converge to the zero configuration in the product topology.

Checked in `rule90_omega_limit.py` (exact big-integer bitmask simulation,
cross-checked against the closed form `x_t(n) = 1 iff (n+t)` even and
`C(t, (n+t)/2)` odd, the last decided exactly via Kummer/Lucas:
`C(t,k)` odd iff `k & (t-k) == 0`):

- **Probe 1 (PROVED, elementary, matches known fact).** Centre column
  `x_t(0)`: `C(t, t/2)` is odd only when `t=0` (submask condition forces
  `t/2 ∈ {0}` when `t` itself has more than one structure... concretely:
  `k=t/2` is a submask of `t=2k` never holds for `k>0`). Verified by
  simulation for `t=0..4096`: `x_t(0)=1` at `t=0`, `0` for all `t≥1`.
  This is the fact R8's own filter already relies on ("degenerate invariant
  measures from the eventually-zero centre column") — it is not new.

- **Probe 2 (PROVED via the closed form, and numerically confirmed for
  `k=1..40`, i.e. `t` up to `~1.1×10^12`).** Column `n=1`:
  `x_t(1) = 1` at every `t = 2^k − 1`. This holds for *arbitrarily large*
  `t`, so coordinate 1 of the configuration keeps returning to 1 forever;
  the sequence of full configurations `x_t` does **not** converge to the
  all-zero point. Hence `Omega(e) ≠ {0^∞}`. **The panel's stated screen is
  factually wrong as written.**

- **Probe 3 (PROVED analytically, and numerically confirmed for
  `W=1..64`).** At `t = 2^m` exactly, `k=(n+t)/2` must be a submask of the
  single-bit number `2^m`, forcing `k∈{0,2^m}`, i.e. `n∈{-2^m,2^m}`. So
  `x_{2^m}(n)=0` for every `n` with `|n|<2^m` — the row is *exactly* zero
  on the window `(-2^m,2^m)`. As `m→∞` this window swallows any fixed
  finite window, so `x_{2^m} → 0` in the product topology along this
  explicit subsequence. **`0^∞ ∈ Omega(e)`, but as one recurrent point
  among (infinitely) many, not as the whole set.** (Numerical run matched
  this exactly: `W=1→t=2, W=2→t=4, W=4→t=8, ..., W=64→t=128`, i.e. `t=2W`
  as predicted by `t=2^m`, `W=2^{m-1}`.)

**Correction to record:** `Omega(e)` for Rule 90 is not a singleton; it is
a nontrivial closed shift-orbit-closure-like set (structurally the
well-known Pascal-triangle-mod-2 / Rowland–Yassawi-type object, the exact
"linear rules" case R8 already cites as solved in the literature) that
contains `0^∞` as one point among a rich recurrent family. **The
classification claim is still false for Rule 90**, but for the reason R8
already states, not the panel's reason: `F(0)=0` is a genuine fixed point,
`0 ∈ Omega(e)` (proved above), so `δ_0` (point mass at the all-zero
configuration) is a valid, degenerate element of `M_e`, and
`δ_0[x_0=1] = 0 ≠ 1/2`. This is word-for-word the mechanism R8's filter
paragraph already names ("its `Y` carries degenerate invariant measures
from the eventually-zero centre column"). The panel's screen reaches the
right verdict (classification fails for Rule 90) by an incorrect argument
(wrong claim about what `Omega(e)` is), which happens not to matter for the
pass/fail outcome but would matter for anyone trying to build a general
argument on "Omega(e) is trivial for degenerate rules" — it is not, in
general; only one point of it is degenerate.

## Points 3 and 4

Given (1) and (2): this is R8 restated in a different, less powerful
representation (no access to the shift/subshift machinery R8's embedding
was chosen to enable), with an incidentally incorrect Rule-90 justification
that does not change the bottom line. There is no genuinely new
formulation here to attempt a cheap uniqueness argument or counterexample
against — doing so would just be re-deriving R8 under a different name. No
false progress is manufactured; no new claim is added to the route
inventory. `PATH.md` R8 already contains everything correct in Direction 2
and is the record to keep pointing at.

## Repo-discipline labels

- Probe 1 (centre column eventually zero): PROVED (elementary, restates a
  fact already used by R8).
- Probe 2 (off-centre column recurs to 1 at `t=2^k-1`, arbitrarily late):
  PROVED via the closed form (Kummer/Lucas), spot-checked numerically for
  `k=1..40`.
- Probe 3 (`0^∞` is a genuine limit point of the orbit, not merely close to
  it): PROVED via the closed form (exact zero window at `t=2^m`),
  numerically confirmed for small `W`.
- Overall route verdict: **DUPLICATE-OF-R8** (equivalent classification
  target under a projection/lift between the two representations), with a
  documented factual error in the panel's own Rule-90 screen that does not
  change the pass/fail outcome of that screen.

# Followup: entropy/Garden-of-Eden on the ray map (P1, direction 1)

Status: **KILLED as a route to P1.**  Not because it fails the Rule 90 screen
in the usual way that screen kills things (no version of the measured
mechanism, controlled or not, ever produces a growing effect for Rule 30 that
Rule 90 lacks, so the screen has nothing to filter either way) but because,
once made precise, it collapses into the already-open ladder question from
`RESULTS-ladder-rung0.md`/`RESULTS-ladder-rung1.md` with no new leverage, its
central inference (entropy drop => non-surjective => Garden-of-Eden for the
one lone-seed point) is invalid on its own terms, and a controlled
fixed-output-length multi-depth measurement (section 3.3) found no
accumulating or rule-specific compression at all — an earlier, uncontrolled
version of that measurement (retracted in section 3.3) had suggested one.

Code: `experiments/overnight-arms/roundtable_followup/entropy_garden_of_eden/`
(`verify_inv.py`, `cylinder_growth.py`, plus the ad hoc depth-2/3 extension
reproduced in section 3.3).  Modal: $0.  Paid model-provider calls: $0.

## 0. Required reading, and what it established going in

`PATH.md` section 0 (Rule 90 filter): any argument that would also apply to
Rule 90 proves nothing, because Rule 90 is left-permutive and its lone-seed
centre column *is* eventually periodic. Section 7.3 obstruction A (`O(log t)`
wall: trace-anchored analysis reaches only `~2.4 log2(t)` into a diagram
whose relevant column is at distance `Theta(t)`), obstruction C (single-column
blindness: P1 is a statement about one column, a density-zero object, and no
functional continuous under density-zero modification can decide it), and
obstruction F (free boundary of a fixed-depth strip: `plain(R+1) subseteq
pin(R) subseteq plain(R)`, proved in rung 1, so tightening a strip's boundary
buys strictly less than one column and the escape relocates rather than
dying) are the three obstructions this proposal explicitly claims to evade.

`RESULTS-ladder-rung0.md` and `RESULTS-ladder-rung1.md`: the existing Buchi
automaton, built on the exact same leftward inverse transduction used here,
proves period-1 and the zero-tail case (calibration) but stays NONEMPTY for
period 2 at every right depth `R` tested up to 7, with every witness verified.
Rung 1 additionally *proves* the sandwich lemma (Corollary 2): the boundary
pin is exactly the one-column extendability condition, so it can only ever
find, one column early, an emptiness that plain depth would find anyway, and
it never does (the accepting tail system grows as `~R^2.75` bisimulation
classes against a `4^R` raw encoding, for both the plain and pin variants,
with matching exponents to `0.02` — the measured shadow of the sandwich).
PATH.md flags a "depth-3 escape family" claim as unsubstantiated (no code
artifact); it is not relied on here.

## 1. Making T_w precise (the load-bearing step)

The panel's stated recursion, `u_{t,i-1} = u_{t+1,i} XOR (u_{t,i} OR
u_{t,i+1})`, cannot be a map from one row `rho_t` to the next row `rho_{t+1}`
taken alone: the right-hand side already needs `u_{t+1,i}`, a value that lives
in the row being produced. As literally written it is circular, not merely
truncated.

**The fix**, which is exactly what this repo's ladder machinery already uses
(`experiments/rule30/inverse_trace_probe.py`, `ladder.py`'s `step_window`):
treat each spatial column `x` as a *full time trace* `col_x : t -> {0,1}`, and
let the inverse recursion move in `x` (spatial, leftward), consuming two
time-shifted values of the *same* column plus one value of its right
neighbour, to produce the next column at every `t` simultaneously:

```text
Rule 30:  col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))
Rule 90:  col_{x-1}(t) = col_x(t+1) XOR col_{x+1}(t)
```

This is `verify_inv.py`. Verification against ground-truth brute-force
simulation of the lone-seed diagram, chaining the reconstruction (feeding a
just-reconstructed column back in as the new center, using no fresh ground
truth after the first step — i.e. genuinely iterating T_w on its own output):

```text
rule=30 depth=1..5, T=60: 0 mismatches (59..285 cell checks per depth)
rule=90 depth=1..5, T=60: 0 mismatches (59..285 cell checks per depth)
```

Also checked the two closed-form identities PATH.md states (constant centre
`c_t=1 => l_t=0`; the general reduction `c_t=1 => l_t = 1 XOR c_{t+1}`,
`c_t=0 => l_t = c_{t+1} XOR r_t`) against the code, independent of lone-seed
data: both hold exactly. **T_w, correctly formalized, is confirmed identical
to the pin/INV machinery already in this repo — it is not a new map.**

## 2. Fixing R and "entropy"

The panel's `R` ("one-sided subshift of light-cone rays, support in `[0,t]`")
is ill-posed as a stationary one-sided subshift over `{0,1}` for the reason
given in the task brief: `rho_t` and `rho_{t+1}` have different supports and
are not two points of the same shift space under the usual shift map.

**The fix used here.** Once columns are the right unit (section 1), the
natural object is a subshift over the *uncountable* alphabet `A = {0,1}^N`
(each symbol is a whole column time-trace), where a point is a sequence
`(c_0, c_1, c_2, ...) in A^N` and the local rule `c_{x-1} = F(c_x, c_{x+1})`
plays the role of a sliding-block map running backward in the spatial index.
`A` is compact (Tychonoff) so this is a legitimate compact shift space, but
computing its topological entropy requires a generating partition, and the
only natural one available is to *also* cut each column at a finite time
horizon `n` — i.e., entropy of this object is inherently computed from finite
`(x,t)`-cylinders, exactly like the ladder's finite-depth-`R`, finite-`t`
window. **The panel's claim that this evades truncation and obstruction A
("no truncation; entropy is global on `{0,1}^N_0`") is therefore false as
stated**: making "entropy of R" computable reintroduces the same double
truncation (spatial depth `D`, time length `n`) the ladder already uses.  This
is not a minor technicality; it is the reason the measurement in section 3
below is *the same kind of object* as rung 0/1's state counts, not a
genuinely different, truncation-free invariant.

Concretely, `cylinder_growth.py` defines, for depth `D=1` (columns 0 and 1)
and window length `n`: `R(D,n)` = all binary matrices `b[x][t]`, `x in {0,1}`,
`t in [0,n)`, respecting the only structural constraint at this truncation
(`b[1][t]=0` for `t<1`; column 0 has no wedge constraint since `x=0<=t`
always). `R_w(n) subseteq R(1,n)` restricts column 0 to be exactly `p`-periodic.
`T_w` is applied to get `col_{-1}`, and the image is the induced multiset of
length-`(n-1)` outputs.

## 3. MEASURED: does the image shrink relative to the domain?

All numbers below are **MEASURED**, finite `n` (4 to 15), finite `p` (1, 2),
exhaustive enumeration (not sampled) at each `(rule, p, n)` — full command
output reproduced from `cylinder_growth.py` and its depth-2/3 extension.

### 3.1 Depth 1 (immediate left column)

```text
rule p  n   #w   #c1    domain   image   ratio     ambient
30   1  4   2    8      16       4       0.2500    128
30   1  12  2    2048   4096     1024    0.2500    8388608
30   2  4   4    8      32       7       0.2188    128
30   2  12  4    2048   8192     1087    0.1327    8388608
90   1  4   2    8      16       8       0.5000    128
90   1  12  2    2048   4096     2048    0.5000    8388608
90   2  4   4    8      32       8       0.2500    128
90   2  12  4    2048   8192     2048    0.2500    8388608
```

Growth-rate (log2 image_size per unit `n`, i.e. the base of the exponential,
which is the actual entropy-relevant quantity — a shrinking *ratio* at fixed
base is a bounded prefactor loss, not an entropy drop):

```text
rule=30 p=1: slopes = 1.000, 1.000, 1.000, 1.000   (full rate, constant 4x loss)
rule=30 p=2: slopes = 0.858, 0.890, 0.931, 0.961    (rising toward 1.000)
rule=90 p=1: slopes = 1.000, 1.000, 1.000, 1.000   (full rate, constant 2x loss)
rule=90 p=2: slopes = 1.000, 1.000, 1.000, 1.000   (full rate, exactly, all n)
```

Rule 30 `p=1` and Rule 90 (`p=1` and `p=2`) show a *constant*-factor loss
(one or two bits, independent of `n`) — not a growing entropy gap. Rule 30
`p=2` is the only cell showing a ratio that keeps shrinking with `n`, and even
there the exponential-rate slope is *rising toward 1.0*, i.e. trending toward
no rate drop as the window widens, consistent with a polynomial (not
exponential) prefactor correction — exactly the "`R^2.75` against `4^R`"
shape rung 1 already reported, not a new, sharper phenomenon.

### 3.2 Rule 90 screen, stated plainly

By Lemma 1' of `RESULTS-ladder-rung1.md`, Rule 90's extendability condition
is vacuous — its inverse map is an unconditional bijection in the free
variable, with no OR to saturate. On the section 3.1 data: Rule 30 `p=1`
shows a *constant* 4x loss and Rule 90 `p=1` a *constant* 2x loss —
qualitatively the same shape, neither growing. The only cell that looks
different is Rule 30 `p=2`, and there the exponential-rate slope is rising
*toward* 1.0, not falling away from it. **The honest statement is not "the
screen is passed" but "no accumulating drop was measured for either rule at
this window size, so the discriminating question the screen asks is moot
here."** Section 3.3's controlled depth test resolves this more sharply: the
apparent Rule-30-specific effect disappears entirely once the measurement is
done correctly.

### 3.3 Controlled depth-accumulation test (fixed output length)

The first version of this test (chaining `T_w` and comparing image size
against `2^{n-d}` at each depth `d`) is **retracted**: comparing against a
denominator that itself shrinks with `d` makes near-saturation almost
arithmetically forced and reads the yardstick, not the image, and it also
never enforced the seed-compatibility wedge on the *reconstructed* columns
(`col_{-k}(t) = 0` for `t < k`), so it was counting images of a map not
actually restricted to `R`. Both defects are fixed in
`depth_accumulation.py`: output length `L` is held **fixed** across all
depths `d = 1..5` (input length `n = L + d` grows to compensate), every
intermediate reconstructed column is checked against its own wedge condition
and discarded if it fails, and only surviving chains are counted. This makes
counts directly comparable across `d` with no denominator games.

```text
rule=30 p=1 L=8:  d=1..5 distinct = 128, 64, 32, 16, 8   (halves every d)
rule=30 p=2 L=8:  d=1..5 distinct = 128, 64, 32, 16, 8   (halves every d)
rule=90 p=1 L=8:  d=1..5 distinct = 128, 64, 32, 16, 8   (halves every d)
rule=90 p=2 L=8:  d=1..5 distinct = 128, 64, 32, 16, 8   (halves every d)
(L=10 reproduces the same halving, one step later, for all four cases)
```

`distinct / survivors` (the loss *conditional on* wedge-admissibility) is
**flat** in `d` for every `(rule, p)` cell — 0.5 from `d=2` on for three of
the four, exactly 0.25 for all `d` in the fourth (Rule 90, `p=2`) — with no
trend in either direction. The halving of the raw `distinct` count with
depth is fully explained by the wedge condition itself (`col_{-d}` loses one
more leading admissible time-step's worth of freedom for each unit of `d`,
a purely geometric light-cone fact with no dependence on the rule or on
periodicity), not by anything dynamical, and it is **identical between
Rule 30 and Rule 90 and between `p=1` and `p=2`** to within the flat
conditional ratio above.

**Corrected conclusion: there is no measured accumulating, rule-specific, or
periodicity-specific entropy drop.** The one asymmetry section 3.1 seemed to
show (Rule 30 `p=2`'s shrinking ratio) does not survive a properly controlled
multi-depth measurement — once the wedge is enforced at every level and the
yardstick is held fixed, Rule 30 and Rule 90 look the same, and both look
like "constant conditional loss per level," not "compounding loss." This
removes ground for the proposal's mechanism entirely, independent of
section 4's logical objection: there is no evidence the image shrinks
relative to the domain as depth grows, for either rule.

## 4. Is the central inference even valid? No.

Independent of what section 3 measures, the argument's logical step is
broken. "`h(T_w(R)) < h(R)` therefore `T_w` is non-surjective on `R`" is fine
as stated (a strict entropy drop across an infinite, well-defined subshift
does force non-surjectivity in the standard sense). The failure is the next
step: **non-surjectivity of `T_w` on the bulk space `R` says nothing about
whether one specific point — the actual lone-seed ray — lies in the excluded
part.** This is exactly `PATH.md` obstruction C, restated one level up: P1 is
a statement about a single orbit (a measure-zero, "density-zero" object in
the space of all rays, just as a single column is density-zero in the space
of all 2D configurations), and a bulk/counting invariant like topological
entropy is by construction insensitive to what happens on any particular
point or even any countable/measure-zero set of points. A subshift can have
entropy strictly less than the full shift and still contain (or exclude) any
specific point you like; entropy alone decides nothing about membership of
one named element. To close this gap the proposal would need to show, in
addition to a bulk entropy drop, that the *specific* lone-seed ray lies in
the non-image — which is a single-orbit question no different in kind from
the one the whole ladder program (rung 0/1) is already stuck on, and which
entropy, being a statistical quantity, cannot address by construction.

So even where section 3 found a real (if non-accumulating) compression
[Rule 30, `p=2`, depth 1], the conclusion "hence no infinite backward
`T_w`-orbit of the actual `rho` can hit `delta_0`" does not follow from it.

## 5. Relation to the sandwich lemma: same mechanism, not an evasion

Item 5's question — does the escape family surviving at every finite `R` in
the ladder correspond to a specific non-surjectivity witness of `T_w`, making
the Garden-of-Eden claim demonstrably false — has a direct answer from
existing repo results plus section 3.3 here:

* Rung 0/1 already exhibit, at every tested `R` up to 7, an actual verified
  witness lasso for period-2 escape (NONEMPTY with `verify_witness` passing
  every time). Each such witness is, by construction, a point of `plain(R)`
  (equivalently `pin(R)` by Corollary 2) — i.e., a concrete element that a
  literal Garden-of-Eden claim (no such element exists at any depth) would
  have to exclude, and does not.
* Section 3.3's controlled depth test found the conditional survival ratio
  flat in depth for both rules, with the raw halving fully explained by the
  wedge condition rather than by anything dynamical. That is the
  entropy-language echo of Corollary 2/3 (`plain(R+1) subseteq pin(R)
  subseteq plain(R)`, and the pin only ever buys, one column early, an
  emptiness depth would find anyway): nothing here shows the image shrinking
  *relative to the domain* as depth grows, so there is no sense in which
  "the escape mechanism operating at a bounded strip" (named directly in the
  task's framing of rung 0/1) has been closed off by moving to an unbounded
  ray. The mechanism this proposal offers has no measured teeth at all, let
  alone teeth sharp enough to reach where the ladder's own boundary pin
  could not.

**Conclusion for item 5: this is the same escape mechanism as rung 0/1, seen
through an entropy lens, not a distinct or unboundedly-stronger one.**
Dropping finite state does not evade obstruction F; the free boundary simply
relocates from "the last modelled column" to "the last column for which
entropy was measured," which is exactly the same relocation phenomenon rung
1 proved in Corollary 2/3.

## 6. Verdict

**KILLED**, on three independent grounds, any one of which is sufficient:

1. **Ill-posed as stated, and the necessary fix collapses it into the
   existing open ladder question** (section 2), with no new leverage —
   "entropy" computed honestly requires exactly the finite `(depth, time)`
   truncation the proposal claims to avoid (obstruction A is not evaded).
2. **The central inference is invalid**: entropy is a bulk/statistical
   invariant of the whole ray space `R` and cannot, even granting a genuine
   drop, decide membership of the one specific lone-seed point (obstruction C
   is not evaded; if anything the proposal is a fresh instance of it).
3. **The one controlled multi-depth computation obtained (section 3.3, fixed
   output length, wedge enforced at every level) found no accumulating,
   rule-specific, or periodicity-specific drop at all** — the conditional
   survival ratio is flat in depth for Rule 30 and Rule 90 alike, at
   `p=1` and `p=2` alike, and the raw halving is fully explained by the
   light-cone wedge condition itself. This directly contradicts the
   accumulation the argument needs, and what little asymmetry the
   uncontrolled section 3.1 measurement seemed to show does not survive the
   controlled version.

**The Rule 90 screen itself never gets to fire** (section 3.2, 3.3) — no
version of the measured mechanism (controlled or not) produces a growing,
rule-specific drop for Rule 30 that Rule 90 lacks, so there is nothing here
that would incorrectly exclude Rule 90's actually-periodic centre column. A
screen with nothing to filter is not a point in the proposal's favor; it is
one more sign the mechanism has no measured content, on top of grounds 1-2
above.

**Nothing here bears on Wolfram's Problem 1.** No per-period exclusion was
obtained or attempted to be claimed. What was established: `T_w`, correctly
formalized, is identical to this repo's existing pin/INV machinery (new
independent verification, section 1); the panel's `R` requires a specific
fix to be well-posed, and the fixed version is a finite-cylinder construction
no different in kind from the ladder (section 2); an uncontrolled single-depth
measurement showed an ambiguous, possibly-shrinking ratio for Rule 30 `p=2`
(section 3.1) that a controlled fixed-output-length, wedge-enforced multi-depth
test then showed to be an artifact — no accumulating or rule-specific drop
was found once measured correctly (section 3.3); and the proposal's logical
bridge from bulk entropy to single-orbit existence is broken regardless,
independent of any of the above (section 4).

## Reproduction

```sh
cd experiments/overnight-arms/roundtable_followup/entropy_garden_of_eden
uv run python verify_inv.py           # section 1
uv run python cylinder_growth.py      # section 3.1/3.2
uv run python depth_accumulation.py   # section 3.3 (the controlled test)
```

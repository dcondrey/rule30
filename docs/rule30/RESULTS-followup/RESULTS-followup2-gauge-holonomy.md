# Gauge-holonomy plaquette defect kappa(x,t): verification of the LLM-panel spark

Status: **KILLED**. Kill condition pre-registered by the triage agent fired
exactly as predicted, and is now a proof, not a guess: kappa is the zero
function by algebraic identity for every left-permutive rule, Rule 30
included, independent of any periodicity assumption. The nonzero regime
exists only when a periodic continuation is force-fed into one of the two
paths, and there it equals, cell for cell, the pre-existing local-consistency
check already catalogued as obstruction D in `PATH.md` section 7.3. Nothing
new survives.

Code: `experiments/overnight-arms/roundtable_followup2/gauge_holonomy/kappa_probe.py`
(read-only reuse of `experiments/rule30/inverse_trace_probe.py`'s
`evolve_once_packed` and the algebraic identity behind `reconstruct_left_column`,
plus `RULE_30`/`RULE_90` from `periodicity_bridge_probe.py`).
Raw output: `kappa_probe_results.json` in the same directory.

## 1. Making kappa(x,t) precise

The spark's "reconstruct-left-then-evolve vs evolve-then-reconstruct-left
around a spacetime diamond" is under-specified as written (a single diamond
`{(t,x-1),(t,x),(t,x+1)} -> (t+1,x)` only supports one direction of
computation). The only reading that produces two genuinely different routes
to the *same* target cell uses **two** diamonds sharing an edge, targeting
`s(t+1,x-1)`:

* **Path A ("reconstruct-then-evolve")**: evolve the triple one step
  forward directly: `s(t+1,x-1) = forward(s(t,x-2), s(t,x-1), s(t,x))`.
* **Path B ("evolve-then-reconstruct")**: evolve the diamond at column `x`
  forward to get `s(t+1,x)` and `s(t+1,x+1)`, then evolve one more step to
  get `s(t+2,x)`, then apply the left-permutive **inverse** identity at
  column `x`, one time step later, to solve back for `s(t+1,x-1)`:
  `s(t+1,x-1) = s(t+2,x) XOR (s(t+1,x) OR s(t+1,x+1))` (Rule 30) —
  this is exactly `reconstruct_left_column`'s formula
  (`inverse_trace_probe.py:135-160`) applied one row later.

`kappa(x,t) := PathA(x,t) XOR PathB(x,t)`.

**This resolves the ambiguity the task asked about, and it resolves in favor
of the kill condition, not against it.** The Rule 30 forward rule is
`s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))`; the "inverse" used in Path B
is nothing but this same equation solved for the left argument, holding the
other two fixed. For any left-permutive rule, `forward(., M, R)` is a
bijection in its first argument by definition, and `inverse(., M, R)` **is
defined to be its inverse function**. So `inverse(forward(L, M, R), M, R) = L`
is not a fact about Rule 30's dynamics; it is the definition of "inverse"
applied to the definition of "forward". Path B, unwound, computes exactly
`inverse(forward(PathA-value, s(t+1,x), s(t+1,x+1)), s(t+1,x), s(t+1,x+1))`,
which collapses to `PathA-value` by the identity above with no reference to
Rule 30, periodicity, or the lone seed at all. **This is the missing
composition law obstruction (D) appearing at the definitional level, before
any computation is needed**: Path A and Path B are the same map read forwards
and backwards, so the forward rule alone forces agreement, for any
left-permutive rule, unconditionally.

## 2. PROVED: kappa is the zero function, exhaustively, for both rules

`algebraic_identity_check()` enumerates all `2^5 = 32` bit assignments to the
5 cells that fully determine the two-plaquette footprint
(`s(t,x-2..x+2)`), derives every other cell used by Path A/B via the forward
rule itself (no free variable is left unconstrained — this is what "internally
consistent with the forward rule" means), and checks `kappa` on all 32 cases.

Result: **0/32 nonzero for Rule 30, 0/32 nonzero for Rule 90.** Since this is
a complete enumeration over the entire input space that determines kappa (not
a sample), this is a **proof by exhaustion**, matching the closed-form
argument in section 1: `kappa == 0` identically, for both rules, by
construction.

(An earlier draft of the script had two orthogonal indexing bugs — feeding
Path B a spurious free variable that didn't correspond to any real cell, and
giving Rule 90's inverse a spurious dependence on the middle cell that Rule
90's forward rule never has — that each produced a false nonzero rate before
being caught and fixed; the corrected script's 0/32 result is what's reported
here, and the fixes are visible in the file's git-free diff history in this
run.)

## 3. MEASURED: confirmed on the true lone-seed diagrams (no periodicity assumed)

`measured_true_diagram_check` simulates lone-seed Rule 30 and Rule 90 out to
`t=400`, `|x|<=60`, and evaluates kappa at 2000 random interior `(x,t)`
pairs directly from the real diagrams (still no periodicity assumption
anywhere — this is item 2 of the task). Result: **0/2000 nonzero for both
rules.** This is exactly what section 2's proof predicts and adds no new
information beyond confirming the harness is wired correctly; it is reported
as MEASURED (a finite check) even though the proved identity already makes
the outcome certain for every `(x,t)`, everywhere, not just these 2000
samples.

**The triage kill condition has now fired as a proof, not a suspicion**: "the
only way to get a nonzero kappa is to smuggle in an assumed periodic
continuation" is correct, and section 1 shows *why* it must be correct —
Path A and Path B are definitionally the same computation.

## 4. MEASURED: the periodic-p injection, and what it actually measures

Per the task's item 3, `periodic_injection_check` builds a nonzero kappa on
purpose: Path A still reads the **true** lone-seed diagram, but Path B's
three future-column inputs are replaced by an assumed period-`p=2` centre
trace (`[0,0]` and `[0,1]` tested) wherever the column index in Path B's
formula equals the centre column `x=0` (and its neighbor `x=-1`, which feeds
Path B's `s(t+1,x+1)` term when `x=-1`). This is the smuggled assumption the
kill condition names.

Result at `p=2`, `steps=200`, `|x|<40` (14578 samples per word):

| period word | kappa nonzero | kappa nonzero **without** a local mismatch between the assumed value and the true value at the injected cell |
|---|---|---|
| `[0,0]` | 154 / 14578 | **0** |
| `[0,1]` | 141 / 14578 | **0** |

Every single nonzero kappa coincides exactly with a cell where the assumed
periodic value disagrees with the true simulated value. There are **zero**
cases of a nonzero kappa that isn't just that disagreement showing up. This
is precisely the "circular... exactly the missing-composition-law
obstruction D" the kill condition predicted: kappa under a periodicity
assumption is not a new derived quantity, it is a renaming of "does the
assumed value equal the true value here", cell by cell.

**On "summing kappa over a fundamental temporal cylinder" (task item 3,
second half):** since kappa's support is exactly the injected-cell mismatch
set, summing kappa over any region (cylinder or not) is exactly counting how
many of the injected cells in that region are wrong. There is no cancellation
structure, no parity trick, and no Stokes-theorem-style global constraint
hiding in the sum — a sum of an indicator function over disagreement points
is an occupancy count, not a boundary term of an exact form. Gluing time into
a cylinder (identifying `t` and `t+p`) does not change this: it would only
add one more term to the same disagreement count, at the seam. This adds
**nothing** beyond what the existing ladder already checks locally, cell by
cell (`PATH.md` row 55, `RESULTS-ladder-rung1.md`). It is a rename, not a new
route.

## 5. MEASURED/computational: the Rule 90 screen, and why the spark's stated reason is not the real one

Task item 4 asked to verify the spark's Rule 90 "gut check": *"Rule 90's
reconstruction is affine-linear, so its plaquette curvature should be
identically zero."* Computationally confirmed (section 2: 0/32 for Rule 90).

But the *reason* given in the spark is wrong, and this matters for the
verdict: **Rule 90's kappa is not zero because Rule 90 is affine-linear.
Rule 30's kappa is equally zero, and Rule 30 is not affine-linear.** Both are
zero for the same reason given in section 1 — Path A and Path B are the same
computation for *any* left-permutive rule, linear or not, by the definition
of "inverse". Affine-linearity is irrelevant to the vanishing; it would only
matter if one were trying to distinguish Rule 30 from Rule 90 by this
statistic, and section 2 shows the statistic can't distinguish them because
it is identically zero for both. This is the Rule 90 filter (`PATH.md`
obstruction B / section 0) applying in its strongest form: not "this argument
happens to also hold for Rule 90", but "this quantity is the zero function
for the entire left-permutive class by construction, so it was never capable
of being about Rule 30 specifically."

## 6. Does this bypass the O(log t) wall? No — task item 5

It does not, and the reason is visible directly in section 4's construction.
The only way kappa is ever nonzero is by comparing an *assumed* value at the
centre column at some time `t` against the *true* simulated value at that
same `t`. Computing "the true value at time `t`" for the true lone-seed
diagram is exactly the reach problem obstruction A already names: reading it
off requires either brute-force simulation to time `t` (no shortcut) or a
triangular-inverse reconstruction from boundary data, which is the mechanism
already shown to reach only `~2.4 log2(t)` diagonals
(`RESULTS-diagonal-periodicity.md`, `PATH.md` 3.1, section 7.3 obstruction
A). "Summing over a fundamental temporal cylinder" does not relax this: the
cylinder still needs the true centre value at every time inside it to know
whether kappa is zero there, and if the cylinder's time extent is meant to
reach the depth at which a claimed period `p` would first be tested (i.e.
`t` on the order of the ladder's current search depth), certifying kappa
there needs exactly the same depth of reach as everything else in section
7.3's register — not less. The spatial width of the cylinder does not need
to grow with `p`, but the **temporal reach needed to know the true value
being compared against does**, and that is the same wall under a new name,
confirmed directly by the injection experiment's own construction (Path A
needed the *true* diagram at exactly the times/positions being compared).

## Verdict

**KILLED**, on the triage agent's own pre-registered kill condition, now
established as an exhaustive proof rather than a suspicion:

1. kappa(x,t), made precise as the only two-path reading the spark supports,
   is the zero function for every left-permutive rule (Rule 30 and Rule 90
   both checked, 0/32 exhaustively) as a direct consequence of what
   "reconstruct" and "evolve" mean for a left-permutive rule — not a
   property of Rule 30's dynamics, the lone seed, or any periodicity claim.
2. The only way to get a nonzero kappa is to inject an assumed periodic
   continuation into one of the two paths, at which point kappa reduces
   exactly (0 counterexamples in 29156 injected samples across two period
   words) to a rename of "is the assumed value locally wrong here" — this
   *is* obstruction D, the missing composition law, already catalogued in
   `PATH.md` section 7.3.
3. Summing kappa over a "fundamental temporal cylinder" produces an
   occupancy count of local mismatches with no Stokes-theorem cancellation
   structure; it adds nothing beyond the existing ladder's local consistency
   check (`PATH.md` row 55).
4. The Rule 90 screen passes, but for the general reason (obstruction B, in
   its strongest form: the statistic vanishes for the whole left-permutive
   class by construction), not the spark's stated reason (affine-linearity),
   which is a red herring — Rule 30's kappa vanishes too, and Rule 30 is not
   affine.
5. The claimed bypass of the `O(log t)` wall (obstruction A) does not
   materialize: certifying kappa away from the trivial injected-mismatch
   case requires the true centre-column value at the same depth the wall
   already governs.

This route does not advance P1, P2, or P3. No part of it should be retried
without a fundamentally different definition of kappa that is not, by
construction, the identity function composed with its own inverse.

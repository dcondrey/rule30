CLEAN DEAD END — no specific-sequence Ore-height/order uniformity route for
A051023 exists that both (a) is not just a restatement of the closed generic
question and (b) is suppliable from Rule-30-specific facts currently on hand
(OR-latch pin, `deg f_t = 2t-1`, a6's measured rank data). Two independent
obstructions, neither computational, both stated below. Row 46 stays OPEN;
this arm closes nothing in it and adds no new obligation.

Read in full before writing this: `a6_row46_ore_uniform/row46_ore_uniformity.md`,
`a20_bridy_verification/bridy_verification.md`, and
`automaticity/ore_check.py`. Also consulted: `docs/rule30/PATH.md` row 43 (ANF
degree law) and its OR-latch section (§1), `docs/rule30/overnight/RESULTS-automaticity.md`,
`docs/rule30/ARM6-binary-kernel.md`.

---

## 0. The question this arm was asked

Row 46's remaining obligation (Lemma L) asked for a bound on Ore
order/height as a function of state count `k`, uniform over the whole class
of 2-automatic sequences. a20 closed that generically: both halves are false,
by explicit counterexamples (`x^n` for height, Bridy's Artin-Schreier series
`G_n` — identical to a6's own witness family — for order). The class-level
question is dead, full stop, not reopened here.

The question actually left open, per the task brief: could a
**sequence-specific** argument, using facts true of A051023 in particular
(not true of an arbitrary automatic sequence), still bound Ore
order/height for A051023 — sidestepping the generic worst case the way a
tighter promise for one particular sequence always could?

## 1. First obstruction: the bound would still be indexed by `k`, and `k` is exactly what's unknown

Any statement of the form "if A051023 is 2-automatic with `k` states, then its
Ore height is `<= H(k)`" — no matter how much tighter `H` is made by using
Rule-30-specific structure instead of Bridy's worst-case `k*2^(k+1)` — is
still a `k`-indexed conditional. Nothing about proving H(k) small changes
that indexing. Two independent reasons this kills the route outright, not
just weakens it:

**1a. Even a perfect bound still requires an unbounded search over `k`.**
Non-2-automaticity of A051023 is the statement `AND_k` "not `k`-state
automatic", for every finite `k`. A single finite Ore-relation-absence
certificate at order `n`, height `d`, computed from `N` prefix terms, only
excludes state counts `k` small enough that `H(k) <= d` is forced (a6's
Theorem U, transported through whatever `H` is used — see a20 §7 for the
worked exchange rate with Bridy's `H`). Making `H` polynomial instead of
exponential changes the *rate* at which the required prefix length `N(k)`
grows with `k` — it does not remove the fact that `N(k)` must be evaluated
at every `k` and the ladder never terminates. This is Obstruction H
(finite-prefix data bounds a complexity function, never the infinite
statement) restated at the level of the bound itself rather than at the
level of one computation. A22's Rule-30-specific `H`, however good, is still
on the wrong side of Obstruction H. a20 §7's own table makes the point
concrete even for the *published, worst-case* bound: 32000 terms excludes
only `k<=7`, a billion bits excludes only `k<=20`. A specific-sequence bound
tighter by a large constant factor moves those numbers, it does not remove
the AND-over-`k`.

**1b. A `k`-free bound is not just hard to find, it is definitionally
unavailable.** The order half of Lemma L, before a20's refutation, was
already the good case: order `<= m_span` (a6 §4), linear in the kernel-span
dimension, no exponential in sight. That did not close row 46, because
`m_span` is still a stand-in for the automaton's state count, and asserting
"`m_span` is finite" is *definitionally equivalent to* "A051023 is
2-automatic" (a finite-dimensional 2-kernel span over `F_2` is one of the
standard equivalent definitions of automaticity, the one a6 uses
throughout). So a `k`-free — meaning state-count-free — order bound would
have to either (i) smuggle in automaticity as a hypothesis, which is
circular since automaticity is P1's negation, or (ii) bound the order using
some quantity independent of the (nonexistent, if P1 is true) automaton
entirely, which is a different kind of statement — not an Ore-uniformity
statement at all, but a direct non-automaticity proof by another method
(kernel-element distinctness, subword complexity, etc — see §3). There is no
third option. This is a structural fact about what "order `<=` bound" means,
not a claim that no one has found the right Rule-30 fact yet.

## 2. Second obstruction: the named Rule-30 facts do not have the right index structure to feed a Bridy-style bound, at any tightness

Independently of §1, check whether the OR-latch pin or the ANF degree law
could even in principle supply a number to plug into the Frobenius-degree-
growth mechanism that produces Bridy's bound (a20 §1, the `B_i` iterated
product, `deg B_i ~ 2^i * deg(A^{-1})`). They cannot, because they are
statements about different index variables:

- **The 2-kernel / Ore relation is about base-2 dilation in `t`.** The object
  being bounded is degree growth in `x` under the substitution `x -> x^{2^i}`,
  i.e. under sampling `a(2^i * t + r)` for residues `r`. This is multiplicative
  structure in the time index.

- **The OR-latch pin is a relation under time shift by exactly 1**, between
  two *different space columns* (`s(t,x)=1 => s(t,x-1) = NOT s(t+1,x)`), not
  a relation between `a(t)` and any dilate `a(2^i t + r)` of the same
  (centre) column. It is additive in `t` and cross-column; the kernel
  machinery is multiplicative in `t` and single-sequence. There is no known
  translation between the two, and none is supplied by PATH.md §1.

- **`deg f_t = 2t-1` (row 43) is the F2-algebraic degree of the map from a
  finite window of the input row to the next centre bit**, i.e. a statement
  about dependence on *initial-condition bits* at fixed time `t`, along one
  trajectory. It carries no base-2 content in `t` at all — `t` is just which
  fixed Boolean function of the seed is being asked about, not an argument
  being dilated. Row 43 itself states the scope limit that applies here
  verbatim: "It implies NOTHING for P1 or P2" (`PATH.md` line ~622, cross-
  checked against `overnight/RESULTS-anf.md`). This arm did not need to
  re-derive that; it is prior art, cited, not re-verified.

Neither fact is *about* the quantity Bridy's mechanism needs (degree growth
of the hypothetical automaton's transition matrix under repeated Frobenius
twisting). Retrofitting either into that role would require a new theorem
connecting CA local dynamics to automaton transition-matrix structure that
does not exist in this repo and was not attempted or found in the literature
sweep this arm's siblings (a6, a12, a17, a20) already ran. Absent that
theorem, "use a Rule-30-specific fact to sharpen `H`" has no fact to use.

## 3. What the task's literal question about a6's own data resolves to: no, and why not just "not yet"

The task asked directly: does a6's *measured* GF(2) rank-growth data already
suggest a bound or obstruction for A051023, distinct from the closed generic
claim? Checked directly against `overnight/RESULTS-automaticity.md` lines
47-48 and `a6_row46_ore_uniform/row46_ore_uniformity.md` §3: every number a6
ever computed on A051023 is a **nullity-0 result** — order `<=12` to height
570, order 0 to height 3999, order 1 to height 2665, all at `N=32000`, all
"no relation found." a6 says this explicitly of its own instrument: "nullity
`>0` never proves that a relation exists, only that none is excluded" (a6 §1).

Nullity-0 exclusion data cannot suggest a bound on the height of a relation
that would exist, because it is evidence about the *absence* of relations in
the searched region, not about the *shape* of one that might exist outside
it. There is no growth curve to extrapolate — a6 never found a nonzero
relation on A051023 to measure the growth of. This is not "the data is too
small to see the trend yet"; it is that the recorded quantity (nullity
against no relation) is structurally the wrong kind of number to carry a
trend about relation shape. So: no, and the answer does not improve with
more compute in this direction, only with more `N`, which §1 already shows
does not close the AND-over-`k`.

## 4. Where a genuine specific-sequence attack on A051023's automaticity does live, and why it is out of this arm's scope

A `k`-free, non-Ore route to non-automaticity exists in principle and is
already staged in this repo: **2-kernel element distinctness**.
`a(t) := A051023(t)`; if infinitely many of the dilates `{a(2^i t + r) :
i>=0, 0<=r<2^i}` are pairwise distinct as sequences, `a` is not 2-automatic
directly (Eilenberg), no Ore relation, no height bound, no `k`-indexing
problem at all — because the statement is "the kernel is infinite," which
sidesteps needing to bound anything as a function of a finite `k` that may
not exist. `docs/rule30/ARM6-binary-kernel.md` already runs exactly this:
distinct 128-bit residual prefixes measured through depth 12 (`8191`
residuals), GF(2) rank growing alongside, both consistent with (not proving)
an infinite kernel. That arm is open, live, and is the correct home for
further specific-sequence work on A051023 — it is not this arm's fence, and
extending it is explicitly out of scope here (task brief restricts this
document to the Ore-height uniformity question and to writing only inside
`a22_row46_specific_uniformity/`).

## 5. Verdict

**Clean dead end**, stated without hedging, on the Ore-order/height
uniformity route specifically:

1. A sequence-specific Ore-height bound for A051023, however tight, remains
   `k`-indexed and therefore subject to the same AND-over-`k` / Obstruction H
   wall a20 §7 already quantifies for the generic bound — tightening the
   constant moves the numbers in that table, it does not close the ladder.
2. A `k`-free order/height bound is definitionally unavailable without either
   assuming automaticity (circular) or abandoning the Ore framing for a
   different non-automaticity method.
3. The two Rule-30-specific facts named in the task brief (OR-latch pin,
   `deg f_t = 2t-1`) are indexed on variables (space-column shift; fixed-`t`
   dependence on seed bits) that do not match the variable Bridy's mechanism
   needs (base-2 dilation degree growth in `t`), so neither can be
   retrofitted into an `H(k)` bound without a new, currently nonexistent,
   connecting theorem.
4. a6's own measured data on A051023 is exclusively nullity-0 (no-relation)
   data and is structurally incapable of suggesting the shape of a bound on
   a relation that was never found.

Row 46 status: unchanged, OPEN. No new obligation is added to it by this
arm. The live specific-sequence thread for A051023, for anyone picking this
up next, is kernel-element distinctness in `ARM6-binary-kernel.md`, not
Ore-height uniformity.

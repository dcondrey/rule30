# Ball-fission topology: verification of the LLM-panel spark

Status: **KILLED**, on three independent grounds that stack. The
pre-registered single-column-blindness gate fires as predicted, but it is
not even the first thing that kills this route: the literal reading of the
spark's own definition proves, by an exact algebraic lemma verified on both
rules, that "fission" (a connected component of 1s splitting into two or
more pieces) is *impossible*, for Rule 30 and for Rule 90 alike, in the
unperturbed lone-seed diagram. The premise is false before any periodicity
argument or any column-substitution test is needed.

Code: `experiments/overnight-arms/roundtable_followup3/ball_fission_topology/fission.py`
(main simulation, both readings, kill-condition test) and
`analyze_components.py` (component-locality / spatial-extent breakdown).
Raw output: `results.json`, `component_locality.json` in the same directory.

## 1. Making "connected component of 1-cells in its backward light cone" precise

The spark under-specifies the adjacency relation, the same failure mode
flagged for `kappa(x,t)` in `RESULTS-followup2-gauge-holonomy.md` section 1.
Two honest, non-equivalent readings were implemented, because the text
supports both and they give different (and differently informative)
answers.

**Reading 1 (causal-edge graph, cell-level, the literal reading).** Build a
graph `G` whose vertices are every 1-valued lattice site `(t,x)` in the
diagram. Add an edge `(t,x)-(t+1,x')` iff `|x-x'|<=1` **and**
`diagram[t][x]==1` **and** `diagram[t+1][x']==1` — i.e. an edge exists only
where an actual 1-to-1 causal dependency of the radius-1 rule holds. "The
connected component of cell `c=(t0,x0)` in its backward light cone" is then
the connected component containing `c` in the induced subgraph restricted
to `t<=t0`. This is the only reading that uses no adjacency not already
implied by the words "backward light cone" and "connected component of
1-cells": no free choice of same-row adjacency, no arbitrary window.

**Reading 2 (same-row spatial run / domain tracking, the charitable
reading).** At each time `t`, identify maximal runs (intervals) of
consecutive 1s in that row — these are the "domains" or "balls" the spark's
baseball framing evokes. A run `A` at time `t` and a run `B` at time `t+1`
are linked if `A`'s causal footprint (each cell reaches `x-1..x+1`)
overlaps `B`'s interval. **Fission** = a run at `t` whose footprint touches
`>=2` runs at `t+1`, none of which has any other parent (a clean 1-parent
split). **Merge** = symmetric, `>=2` parent runs feeding one child.
**Annihilation** = a run with zero children. This is the reading that
actually matches the spark's own "annihilate vs. fission" language and is
the one worth testing the premise against on its own terms.

Both are implemented in `fission.py` (`causal_component_trace` /
`verify_every_one_has_a_parent` for Reading 1, `run_events` for Reading 2)
and computed for real lone-seed Rule 30 and Rule 90 diagrams, `steps=300`,
half-width `320` (comfortably beyond the light cone at `t=300`).

## 2. PROVED: Reading 1 gives exactly one component, always, for both rules — fission is definitionally impossible

**Lemma.** For Rule 30 (`s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))`) and
for Rule 90 (`s(t+1,x) = s(t,x-1) XOR s(t,x+1)`), every output cell with
value 1 has at least one causal parent among `{x-1,x,x+1}` at time `t`
with value 1.

*Proof.* Rule 30: if `s(t+1,x)=1`, either (a) `s(t,x-1)=1` and the OR term
is 0 (so `x,x+1` are both 0 — parent is `x-1`), or (b) `s(t,x-1)=0` and the
OR term is 1 (so at least one of `x,x+1` is 1 — that is a parent). The case
`s(t,x-1)=1` and OR-term`=1` gives XOR`=0`, not output 1, so it never
arises. Rule 90: if `s(t+1,x)=1` then exactly one of `s(t,x-1),s(t,x+1)` is
1 (XOR), which is the parent. In both cases the base case (`t=0`, the
single seed) trivially has one component. By induction: every 1-cell at
`t+1` is linked by a real graph edge to at least one 1-cell at `t`, so
every 1-cell in the entire diagram is connected, through a chain of such
edges, back to the single seed cell. Hence **the whole diagram's 1s form
exactly one connected component, at every time, for every rule of this
exact radius-1 shape (any output-1 forced to credit at least one 1-valued
neighbor), independent of what the rule computes when that condition
holds.** &#8718;

**Computational confirmation** (`verify_every_one_has_a_parent`,
`causal_component_trace`, both rules, `t` up to 300): **0 parent-lemma
violations** for Rule 30 and for Rule 90, and the running component count
under Reading 1 is **1, at every sampled `t`, for both rules**
(`results.json` → `premise_check.rule30/rule90.reading1_final_component_count
== 1`, `parent_violations == 0`).

This is stronger than a measurement: it is a proof, and it is
**rule-independent** — it says nothing whatsoever separates Rule 30 from
Rule 90 under this reading, because the reason is a graph-theoretic fact
about growing induced subgraphs of a fixed diagram (existing connected
material can only merge with more material or stay the same as more of a
static graph is revealed; a fixed connected piece cannot un-connect without
an edge being removed, and no edge is ever removed here) composed with the
parent lemma above. **Under the literal reading of the spark's own words,
"fission" cannot happen, for any rule of this shape, ever.** The premise is
false before periodicity, before Rule 90, before the column-blindness gate.

## 3. MEASURED: Reading 2 (domain tracking) does not show the claimed asymmetry either

Task item 2 asked to verify, separately from the kill condition, whether
"Rule 90 only ever lets components merge/annihilate under XOR, while Rule
30's OR term creates genuine splits." Measured directly
(`run_events`, both rules, `t=0..300`):

| rule | fissions (clean 1-parent splits) | merges (`>=2`-parent) | annihilations (0-child) | creations (0-parent) |
|---|---:|---:|---:|---:|
| Rule 30 | 1937 | 4984 | **0** | 0 |
| Rule 90 | 2409 | **0** | 2394 | 0 |

This is the **opposite** of the premise's stated direction under the only
operational definition of "fission" that gives the spark's
"annihilate-vs-split" language content: Rule 30 shows **zero**
annihilations and thousands of merges, while Rule 90 shows thousands of
"clean fissions" by this counting and zero merges. The reason is not a
topological property of XOR vs. OR: Rule 90's lone-seed pattern is the
classic Pascal's-triangle-mod-2 / Sierpinski structure, nonzero only on
cells with `x+t` even, so within a single row its 1s are almost always
isolated singletons separated by 0s — a parity/sparsity artifact of
additive CA structure, not a splitting mechanism. A single isolated 1 at
time `t` causally touches up to two output positions at `t+1`
(`x-1,x+1` under Rule 90's rule, since the middle term is absent), which
this counting scheme registers as a "clean fission" purely because Rule 90
has no middle-cell dependency, not because a connected structure divided.
Conversely Rule 30's OR term keeps the interior of the light cone densely
packed with 1s (few gaps), so touching runs at `t+1` routinely have more
than one parent, registering as "merges," not because two colliding
defects fused, but because the diagram is locally dense.

**Honest scope**: this measurement genuinely tests item 2's question and
the answer is "no, this premise as stated does not hold" — the direction is
reversed and the mechanism is a sparsity artifact of Rule 90's known
checkerboard support, not a real annihilation-only vs. fission-capable
dichotomy. It should be reported as a real, checked negative result, not
buried.

## 4. MEASURED: the pre-registered single-column-blindness gate

Per the task's item 3: take the true Rule 30 lone-seed diagram, overwrite
column 0 (`x=0`) only, at every `t`, with a periodic word, leaving every
other cell exactly as computed by real forward evolution (no re-simulation,
including the deliberate local inconsistency at `x=-1,0,+1` this creates,
per the gate's own specification). Recompute both readings' statistics on
the substituted diagram and compare to the unmodified baseline.
`full_width = 641` columns, `column0_fraction_of_columns ≈ 0.00156`.

**Reading 1 (exact component count):**

| word | final component count | delta from baseline (1) | max `|x|` reached by any *non-dominant* component | non-dominant component sizes |
|---|---:|---:|---:|---|
| baseline (unmodified) | 1 | — | — | — |
| `[0,1]` (period 2, alternating) | 37 | +36 | **1** | all size 1 |
| `[0,1,1]` (period 3) | 7 | +6 | **1** | sizes 2,2,2,2,4,4 |
| `[0,0]` (period 2, constant 0) | 45 | +44 | **300** (full range) | two macroscopic halves (23008, 22519 cells) + tiny debris |

**Reading 2 (event counts), delta from baseline (1937 fissions / 4984
merges / 0 annihilations / 0 creations):**

| word | Δfissions | Δmerges | Δannihilations | Δcreations |
|---|---:|---:|---:|---:|
| `[0,0]` | −2 | −64 | +46 | +41 |
| `[0,1]` | −1 | +25 | +19 | +18 |
| `[0,1,1]` | −3 | +31 | +15 | +12 |

**Interpretation, and why this is column-blindness in the strong sense, not
a survival.**

For every *non-constant* periodic word tested (`[0,1]`, `[0,1,1]`), every
single extra Reading-1 component is confined to `|x|<=1` — the immediate
spatial neighbors of the one column that was overwritten — and does not
grow with `t` even out to `t=300` (`component_locality.json`: x-ranges are
literally `(0,0)`, `(1,1)`, `(-1,-1)`, `(-1,1)`; t-ranges are single points
or spans of 1-2). These are exactly what the local-consistency check
already catalogued as obstruction D (`PATH.md` section 7.3,
`RESULTS-followup2-gauge-holonomy.md` section 4): the substitution makes
column 0 briefly disagree with what the true forward rule would compute
from its (also-substituted) neighbors, that disagreement creates one or two
extra size-1/size-2 components exactly at the disagreement site, and
nothing else in the diagram is touched. The Reading-2 event deltas are of
the same character and the same size: single- or double-digit changes out
of totals in the thousands (≈0.05-1.3%), i.e. **`O(1/W)`-scale**, exactly
the threshold the gate specifies.

The one word that produces a *large*, non-local effect — `[0,0]`, constant
zero — is a different and unrelated phenomenon, not a survival of the
fission-topology claim. Forcing column 0 to identical 0 at every `t`
removes every edge that could ever cross `x=0` in the causal graph (an edge
requires both endpoints to be 1, and column 0 is now never 1), which
severs the left half-plane from the right half-plane into two
approximately-equal-size components by a **generic graph cut-vertex
argument**: this happens for *any* radius-1 rule (Rule 30 or Rule 90,
identically — not tested but immediate from the same argument, since
neither rule's forward map ever creates an edge whose column-0 endpoint has
value 1 if that endpoint is forced to 0), and it happens for *any*
all-zero substitution, **periodic or not** — a single one-time zeroing of
column 0 forever after would sever the diagram exactly the same way. It
carries no information about whether the true column-0 sequence is
periodic, and it does not discriminate Rule 30 from Rule 90. It is a
column-severing artifact wearing periodicity's clothes, not a probe of P1
or P2.

**Conclusion for the gate**: for the reading of "fission" that behaves like
a genuine structural statistic (non-constant words), the quantity moves
only by the exact local-mismatch artifact obstruction C predicts, and never
propagates past the immediate neighbor columns even over 300 time steps —
this is the `O(1/W)` (here closer to `O(1)`, i.e. a *fixed*, non-growing
number of cells regardless of window) column-blindness obstruction firing
exactly as specified. For the one word that does move the statistic
globally, the mechanism is a generic disconnection artifact unrelated to
periodicity or to either rule's specific dynamics.

## 5. Verdict

**KILLED**, on three independent, stacking grounds:

1. **The premise is false by proof, under the literal reading of the
   spark's own definition (Reading 1)**: the parent lemma of section 2
   forces exactly one connected component of 1-cells at all times, for
   Rule 30 and for Rule 90 alike (0 violations, both rules, `t<=300`).
   "Fission" as literally defined cannot occur, for either rule, ever — not
   a periodicity-dependent fact, not a Rule-30-specific fact, a fact about
   any radius-1 rule whose output-1 always credits at least one 1-valued
   neighbor.
2. **Under the charitable operational reading (Reading 2), the claimed
   asymmetry does not hold and is empirically reversed**: Rule 30 shows
   zero annihilations and thousands of merges; Rule 90 shows thousands of
   "clean fissions" and zero merges under this counting — driven by Rule
   90's known checkerboard sparsity, not by any splitting mechanism (item 2
   of the task, checked and reported honestly as a real negative result).
3. **The pre-registered single-column-blindness gate fires exactly as
   predicted for the only version of the statistic that isn't already
   dead by (1)**: overwriting column 0 with a non-constant periodic word
   moves Reading 1's component count and Reading 2's event counts by a
   fixed, tiny, strictly-local amount (`|x|<=1`, not growing with `t` out
   to 300 steps) — a local-mismatch artifact of the same shape as
   obstruction D, not a signal about periodicity. The one word (`[0,0]`)
   that produces a large, non-local change does so by a generic
   graph-cut-vertex mechanism that requires no periodicity and does not
   distinguish Rule 30 from Rule 90.

**Is the underlying fission-vs-annihilation observation real, even though
it doesn't save this construction?** No, not in the form the spark states
it. Section 3's direct measurement finds the opposite empirical direction
from what the spark's baseball/Merkle-Boner framing claims, and the
mechanism behind the observed asymmetry (Rule 90's parity sparsity) has
nothing to do with topological fission — it is a restatement of the
already-known fact that Rule 90 is supported only on `x+t` even, not a new
finding about OR vs. XOR collision dynamics. The one true, defensible
statement in this vicinity — that Rule 90's dynamics is affine/superposable
and Rule 30's is not — was already the content of the Rule 90 filter
(`PATH.md` section 0 / obstruction B) and of the gauge-holonomy followup's
section 5 finding that affine-linearity is a red herring for vanishing
statistics; it gains nothing new here.

This route does not advance P1, P2, or P3. No part of it should be retried
without a fundamentally different definition of "connected component" that
(a) is not provably always-1 by the parent lemma of section 2, and (b) does
not reduce, under column substitution, to a local-mismatch or graph-cut
artifact.

## Reproduction

```sh
cd experiments/overnight-arms/roundtable_followup3/ball_fission_topology
uv run python fission.py            # premise check + kill-condition test -> results.json
uv run python analyze_components.py # component locality / size breakdown -> component_locality.json
```

Modal: $0. Paid model-provider calls: $0.

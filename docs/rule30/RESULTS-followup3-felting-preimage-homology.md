# Felting-preimage-homology: verification of the LLM-panel spark

Status: **KILLED**. The pre-registered kill condition fires, but for a
strictly stronger and more general reason than the one triage suspected: the
compatibility graph, made precise, is a forest for a pure graph-theoretic
reason (a length-graded node set with a canonical truncation map to a unique
parent), true for *any* local update rule whatsoever, not only for
left-permutive ones and not specifically because of Rule 30's OR-pin. It is
therefore rule-agnostic in the strongest possible sense: it never had a
chance to distinguish Rule 30 from Rule 90, because it never uses the update
rule's identity at all, only that it is deterministic and has finite
propagation speed. Measured exhaustively for Rule 30 and Rule 90 to depth
`k=40`: forest, 0 cycles, both rules, identical shape.

Code: `experiments/overnight-arms/roundtable_followup3/felting_preimage_homology/compat_graph.py`
(primary construction, right half pinned to the true seed) and
`compat_graph_freeright.py` (robustness check, right half existentially
free). Raw output: `results.json` in the same directory.

## 1. Making the compatibility graph precise

The spark gives two under-specified pieces: what a "left-half configuration
... consistent with the observed prefix" is, precisely, and what a
"one-step-consistent extension" edge is. The most literal reading of the
spark's own words is adopted here, because it is the only reading that
assigns a concrete, checkable meaning to *both* nouns the spark uses
("configurations on cells `{-t,...,-1}`" and "extensions of each other")
without inventing structure the spark didn't ask for:

**Node**, level `k`: a word `w ∈ {0,1}^k`, read as a candidate initial
condition on cells `-1,...,-k` at `t=0` (`w[i-1]` = candidate value of
`s(0,-i)`), that is **consistent**: when the full initial row is built as

```text
s(0,0)  = 1                (the true one-cell seed)
s(0,-i) = w[i-1]           for i = 1..k
s(0,x)  = 0                otherwise (x > 0 or x < -k)
```

and evolved forward under the rule, the resulting centre column agrees with
the *true* lone-seed centre `a_0,...,a_{k-1}` for all `k` steps this IC can
determine.

**Edge**: `w` (level `k`) to `w'` (level `k+1`) iff `w'` restricted to its
first `k` coordinates equals `w` (i.e. `w'` keeps every cell `w` fixed and
adds exactly one new cell, `-(k+1)`), and `w'` is itself a consistent node.
This is the literal reading of "one-step-consistent extension": one new cell
added, one new time-step of centre column checked, nothing else changed.

**Padding is not an extra assumption.** Filling `x < -k` with 0 does not bias
the result: by finite propagation speed, `s(t,0)` for `t <= k-1` depends only
on the initial row restricted to `[-(k-1), k-1]`, a window entirely inside
`w`'s domain (`-1..-k`) union the known true right half (`x>=0`). Cells past
`-k` are outside every light cone used to check `a_0,...,a_{k-1}`, so their
padded value is a don't-care, not a hidden hypothesis. This is verified
directly by the monotonicity lemma below, not merely asserted.

**Why this is the most charitable reading, and what the alternative is.**
A different formalization is possible: fix a finite window width `W` and
build a de-Bruijn/SFT-style transition graph on width-`W` words as `t`
increases (nodes = admissible windows at depth `t`, edges = valid
one-step-in-time transitions). That construction is a real, previously
studied object in this repo — it is exactly the `plain_R`/`pin_R` automaton
underlying the R7 ladder (`RESULTS-ladder-rung1.md`, `PATH.md` section 7.3
obstruction F). It genuinely has cycles (any walk on a finite state graph
run forever must loop), and its cycle/lasso structure has already been
characterized: `plain(R+1) ⊆ pin(R) ⊆ plain(R)` at every `R` (Corollary 2/3),
the phase slip "relocates to the free boundary rather than dying," and mode
(i) of the corresponding search (row 7) never returns empty at any depth —
verdict uniform across a 5,500x range of raw sizes. If that is what the spark
meant, it is not a new construction, it has already been run at scale, and
its verdict is already recorded: it does not decide P1. The construction
below is the literal, non-duplicate reading of the spark's own text (a
graph on *initial-condition prefixes*, not on *sliding time-windows*), and it
is examined on its own terms rather than assumed to reduce to the ladder.

## 2. PROVED: the graph is a forest, for a reason that has nothing to do with Rule 30

**Lemma (monotonicity of consistency).** If `w'` of length `k+1` is
consistent, then its truncation `w = w'[:k]` (length `k`) is consistent.

*Proof.* Consistency of `w'` means the IC built from `w'` reproduces
`a_0,...,a_k`. In particular it reproduces `a_0,...,a_{k-1}`. By finite
propagation speed, `a_0,...,a_{k-1}` depend only on the initial row on
`[-(k-1),k-1]`, which is identical between the `w'`-IC and the `w`-IC (they
agree on cells `-1..-k`, and `-(k+1)` — the one coordinate they differ on —
lies outside `[-(k-1),k-1]`). So the `w`-IC reproduces `a_0,...,a_{k-1}`
too, i.e. `w` is consistent. **QED.** (Confirmed computationally:
`truncation_mismatches: 0` over all 80 edges at `k=40`, both rules — every
edge really is the truncation map, never something else.)

**Theorem (forest).** The compatibility graph, at any depth, is a forest —
in fact a single tree rooted at the empty word — regardless of the update
rule.

*Proof.* By construction, every edge into a level-`(k+1)` node `w'` comes
from `w' → w'[:k]`, a single deterministic function of `w'` (there is only
one way to drop the last coordinate of a fixed string). So every non-root
node has **exactly one** candidate parent, and the lemma above guarantees
that candidate parent is itself a valid node whenever `w'` is a node. Hence
every non-root node has exactly one parent edge, level 0 has one root (the
empty word: the seed alone, trivially consistent with `a_0`), and a graph
with unique parents and one root is a tree by definition. Cycles, and hence
any nonzero `H1`, are structurally impossible. **This argument never
mentions Rule 30's forward rule, the OR, or the pin.** It only uses
determinism and finite propagation speed, so it holds verbatim for Rule 90,
Rule 90's own inverse, or literally any local update rule on `Z`.

This is the pre-registered kill condition, confirmed, but sharpened: triage
suspected the pin (a Rule-30-specific, though rule-agnostic-by-construction,
mechanism at the OR-latch) would force acyclicity. The pin is not needed at
all here — the acyclicity is forced one level up, by the fact that
"left-half configurations graded by length with an extension relation" is,
as a piece of pure combinatorics, always a rooted forest. The pin's role (see
section 4) is instead to explain *how many* nodes survive at each level, not
*whether* the graph has cycles.

**MEASURED, exhaustively to `k=40`, both rules** (`compat_graph.py`,
`forest_check`): total nodes `= 2k+1`, edges `= 2k`, `n_edges == total_nodes
- n_roots` exactly (the exact combinatorial signature of a forest),
`multi_parent_nodes = 0`, `truncation_mismatches = 0`,
`cyclomatic_number_if_connected_as_forest = 0` — at every one of `k = 1..40`
for Rule 30 and Rule 90 both. Since the theorem above is a proof, not a
sample, this is confirmation of the mechanism rather than new information,
exactly as with the analogous checks in the two prior follow-up reports.

## 3. Rule-90 explicit check (task item 3)

Run identically, with `rule90(a,b,c) = a XOR c` in place of Rule 30's OR
latch, no other code path changed. Result: forest, `k=1..40`, identical
combinatorial signature (`total_nodes=2k+1`, `edges=2k`, `0` cyclomatic
number at every level) — see `results.json`, key `"rule90"`. This is the
vacuity confirmation the task asked for: the acyclicity is not merely "also
true for Rule 90 by coincidence," it is produced by the *same* proof for
both rules, because the proof never inspects which rule is in use.

## 4. A second, independent kill: the node set itself is too thin to hold a cycle

Section 2's forest proof holds for *any* edge relation built by extension —
it does not depend on how permissive the node-consistency test is. But a
skeptical reading of section 1's node definition deserves to be checked
directly, because it is the more exploitable weak point: the base
construction pins the right half (`x>0`) to the *true* seed configuration
(all zero beyond the origin) and only lets the left half vary. That is a
choice, not forced by the spark's text, and a tighter node-consistency test
could in principle produce a graph so sparse that "it's a forest" is true
only because there was almost nothing to connect — a second, independent
way to be vacuous, on top of section 2's structural one.

So this was checked directly rather than assumed away.
`compat_graph_freeright.py` redefines a node at level `k` as a left-half word
`w` for which **some** right-half completion `v` (not necessarily the true
one) reproduces `a_0,...,a_{k-1}` — a strictly larger, existentially
quantified node set (the true-seed choice is one witness among many, so
every original node survives here too). The truncation lemma of section 2
is unaffected by this change (its proof never inspects the right-half
values, only that parent and child agree on it up to level `k-1`'s light
cone, which holds under existential quantification with the same witness).
Measured directly (`nodes_with_free_right`, `k=1..8`, brute force over all
`2^k` left times `2^k` right combinations):

| k | Rule 30 survivors | Rule 90 survivors | `2^k` |
|---|---:|---:|---:|
| 1 | 2 | 2 | 2 |
| 2 | 2 | 4 | 4 |
| 3 | 2 | 8 | 8 |
| 4 | 4 | 16 | 16 |
| 5 | 4 | 32 | 32 |
| 6 | 4 | 64 | 64 |
| 7 | 4 | 128 | 128 |
| 8 | 6 | 256 | 256 |

Two things follow from this table, and both close the objection:

1. **Rule 90's free-right node set is the *entire* binary tree at every
   level** (`survivors == 2^k` exactly, `k=1..8`): right-half freedom always
   suffices to make any left half consistent, because Rule 90's centre value
   is an affine function of the boundary and the right half alone has full
   rank over it. This is the maximally permissive case obtainable from this
   construction, and it is *still* a forest, trivially (the full binary
   tree is the largest possible tree on length-graded binary words) —
   confirmed by direct truncation check, `0` violations. So even the most
   generous plausible node set for the rule most naturally suited to
   admitting one does not produce a cycle; there was never a permissiveness
   knob available that could.
2. **Rule 30's free-right node set grows slightly (`2,2,2,4,4,4,4,6,...`)
   but stays exponentially thinner than `2^k`**, and remains a forest by the
   same truncation check (`0` violations, `k=1..8`). So the base
   construction's thinness (section 1) was a real restriction relative to
   this variant, but relaxing it changes the node *count*, not the
   acyclicity verdict — exactly as predicted by section 2's proof, which
   never used how the node set was chosen.

**Conclusion of this section: the forest verdict is doubly robust.** It
holds under the tightest plausible node definition (right half pinned to
truth, section 2) and under the loosest plausible one that still matches
the spark's words (right half existentially free, this section, including
the degenerate case where literally every word is a node). No node-set
choice available inside the spark's own vocabulary — "left-half
configurations... consistent with the observed prefix" — produces a cycle,
because the truncation argument that forbids them is a property of the
*extension* relation, not of which words pass the consistency filter.

## 5. The base construction's node count is a rule-invariant "broom," independently of section 4

The tightest node definition (right half pinned to the true seed, section 1)
was also examined for its own sake, since in principle branching could have
been rule-sensitive in an interesting way even though it cannot produce a
cycle either way (section 4 already forecloses that regardless of which
node set is used). It is not rule-sensitive.

**MEASURED, both rules, `k=1..40`:** exactly 2 nodes survive at every level,
and they are always

```text
level k:  (0,0,...,0)          "spine": the true left half (all zero)
          (0,0,...,0,1)        "leaf": true left half, except the single
                                        farthest cell (-k) flipped to 1
```

confirmed by direct enumeration (`broom_shape_holds_k1_40: True` for both
rules in `results.json`). In graph terms this is a "broom": one infinite
spine (the true configuration, which trivially always survives) with a
single length-1 pendant edge re-sprouting at every level and dying exactly
one level later. The mechanism is immediate and, again, rule-agnostic: a
lone perturbation at cell `-k` is outside every light cone used up through
level `k` (so both its values survive there, by the same finite-propagation
argument as section 2) and enters the light cone for the very first time at
level `k+1`, where — for both Rule 30 and Rule 90, checked exhaustively —
it changes the centre value relative to the truth and is killed on the spot.
Nothing about this depends on the OR-pin, on left-permutivity, or on which
of the two rules is running; it is a restatement of "a deterministic rule
with finite propagation speed detects a single defect exactly when the
defect's light cone first reaches the observation point," which is equally
true of Rule 90 (the rule whose whole point, per `PATH.md` section 0, is
that it must NOT distinguish itself from Rule 30 for any argument to survive
the filter). This closes off the obvious follow-up question ("even if it's
a forest, could its *shape* still encode something P1-relevant?") with a
measured no: the shape is the same trivial broom for both rules to `k=40`.

**Bits-bound note (task's pointer to `PATH.md` 9.1), for completeness.** Even
setting the forest proof aside, any scalar read off this graph up to depth
`k` (node count, branching profile, "cycle count" had one existed) is a
quantity computed from a bounded initial segment of a length-graded
structure — exactly the shape flagged in `PATH.md` section 9.1: a quantity
of the form `f^k(m_0)` on a bounded per-level alphabet carries at most
`O(log(nodes at depth k))` bits about the whole orbit, independent of how
far `k` is pushed. Here that bound is moot because the exact value (forest,
broom) is already known in closed form for all `k`, but it is worth
recording that even a hypothetical nonzero invariant surviving to some large
measured `k` would not, by itself, certify anything at `k=infinity` — the
same wall that already retired the geometric/spectral column-blind family
(`PATH.md` section 0.1, obstruction C) and the finite-certificate family
(obstruction H) would apply here too.

## 6. Does either rule's version look different at all? No — explicit comparison

| quantity | Rule 30 | Rule 90 |
|---|---|---|
| forest (cyclomatic number) at every `k=1..40`, right pinned | 0 | 0 |
| forest (cyclomatic number) at every `k=1..8`, right free | 0 | 0 |
| nodes at level `k`, right pinned | `2` (all `k>=1`) | `2` (all `k>=1`) |
| nodes at level `k`, right free | `2,2,2,4,4,4,4,6,...` | `2^k` (every word) |
| mechanism | finite propagation speed + unique truncation | finite propagation speed + unique truncation |

The only column where the two rules differ at all is node *count* under the
free-right variant (Rule 90's affine structure admits every word; Rule 30's
does not) — and section 4 already showed that difference is irrelevant to
the question asked, since neither count produces a cycle. Per `PATH.md`
section 0 ("does this argument fail for Rule 90?"), the acyclicity result
itself is not merely a control that passed — it is the whole verdict: the
construction was incapable of separating the two rules on the cycle
question before any code ran, because its acyclicity proof (section 2)
never uses the update rule.

## Verdict

**KILLED.** The pre-registered kill condition (graph is a forest by
construction) is confirmed, exhaustively, for `k` up to 40 on both rules,
and is now a proof rather than a suspicion:

1. The compatibility graph, formalized as the literal reading of the spark
   (left-half prefixes at `t=0`, graded by length, edges = one-cell
   extensions), is a rooted tree for *any* deterministic, finite-propagation-
   speed rule — a fact about grading-by-length-with-canonical-truncation, not
   about Rule 30's pin. This is a **stronger** kill than the one triage
   proposed: it does not even need left-permutivity or the OR-latch.
2. Confirmed computationally to `k=40` for both Rule 30 and Rule 90:
   `n_edges == n_nodes - n_roots` exactly, zero multi-parent nodes, zero
   truncation mismatches, zero cyclomatic number, at every level.
3. Checked directly rather than assumed away: the acyclicity is not an
   artifact of an overly restrictive node definition. Loosening the base
   construction's node set to its most permissive form consistent with the
   spark's words (right half existentially free rather than pinned to the
   true seed) still produces a forest for both rules, `k=1..8`, including
   the maximally-permissive degenerate case for Rule 90 (every word is a
   node — the full binary tree, still a tree).
4. The one remaining rule-sensitive-looking quantity available from this
   construction — the branching/node-count profile under the tighter,
   right-pinned node set — was checked honestly rather than assumed dead on
   the forest argument alone, and is *also* identical (the "broom": true
   configuration plus a one-level dying perturbation leaf) for both rules to
   `k=40`, for the same rule-agnostic causal reason.
5. The interesting alternative formalization (a finite-window sliding-time
   SFT/de-Bruijn graph, which does have real cycle structure) is not a new
   construction: it is the R7 ladder automaton already characterized in
   `PATH.md` section 7.3 obstruction F and `RESULTS-ladder-rung1.md`, with a
   verdict already on record (constraint and freedom grow together at every
   `R`; row 7 never returns empty; does not decide P1).

No part of this route advances P1, P2, or P3. Nothing here should be
retried without a fundamentally different node/edge definition that escapes
both (a) the length-graded-tree triviality proved in section 2 and (b) prior
coverage of the sliding-window alternative in the R7 ladder work.

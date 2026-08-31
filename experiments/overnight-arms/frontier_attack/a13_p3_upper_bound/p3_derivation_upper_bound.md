# R9 / arm A13 (INVERTED target): NEGATIVE. No `o(n^2)` resolution derivation family for `c_n` was found. What was obtained is a machine-checked **constant-factor** improvement, of exact length `n^2/2 + n` for rule 30 and `n^2/4 + n` for rule 90, 2.95x shorter than the `O(n^2)` row-simulation baseline PATH.md R9 asserts, verified step by step at `n = 4..128` and in closed form to `n = 200`; and, in the same sentence as that result, a proof-complexity bound of any kind does NOT resolve Wolfram's Turing-machine formulation of Problem 3, since systems with extension simulate fast algorithms.

The missing lemma is named exactly, in section 8: a block-summary clause family
`S_B`, one per dyadic spacetime block `B` of the light cone, with
`|S_B| = o(area(B))`, together with a resolution derivation of `S_B` from the
`S_{B'}` of `B`'s children plus `B`'s local axioms in `o(area(B))` steps, and a
derivation of `c_n` from `S_root` in `o(n^2)` further steps.  Which condition
each measurement kills, and how, is section 8.

Status: measurement plus four derivation families, no theorem about Rule 30.  Every
resolution step reported below was verified mechanically by a checker in this
directory.  Nothing here is a lower bound; the lower-bound side is
`../a4_p3_resolution/`.  No proof artifact is produced and nothing here
contains `sorry`.

---

## 0. What was run

| artifact | what it establishes |
|---|---|
| `p3_core.py` | Light-cone CNF, a resolution checker that replays and re-verifies **every** step, and four derivation families.  Gates: centre column against `experiments/rule30/center_column.py` (OEIS A051023) and `experiments/overnight-arms/common/rule30.py` to `n=512`; encoding soundness and exactness of the off-cone-parent substitution at every band. |
| `p3_tables.py`, `derivations.json`, `derivations.log` | Mechanically counted, every-step-checked lengths of all four families plus block doubling at `k = 2,4,8,16`, rules 30 and 90, `n = 4..128`. |
| `p3_slice_ladder.py`, `slice.json` | Bit-parallel size of the antecedent-minimal backward slice, `n = 16..8192`, three antecedent-choice policies, validated against the explicit set. |
| `p3_closed_form.py`, `closedform.log` | Exact closed forms for the best family, checked for every even `n` in 2..200.  This is the guard against reading the finite-size log-log fit as sub-quadratic. |
| `p3_minlength.py`, `minlen.log`, `minlen.json` | Exhaustive search over the clause space for any derivation shorter than the best family, at tiny `n`.  Minimizes **tree** cost. |
| `p3_optimal_witness.py`, `optimal_witness.log` | Reconstruction of the minimum tree-like derivation at `n = 2,3`.  This is what found the best family; it confirms `min_tree == backward family` at both `n`. |
| `p3_drup_trap.py`, `drup.json`, `drup.log` | Why a SAT solver's proof length is the wrong instrument here. |

Interpreter: `/Volumes/A/researchpapers/.venv/bin/python` (python-sat lives
there, not in the default `uv` environment).

## 1. The formalization, pinned

Variables: one per cell of `D_n = {(t,x) : |x| <= min(t, n-t)}`, the backward
diamond of `(n,0)` intersected with the forward light cone of the lone seed.
`|D_n| = n^2/2 + n + 1` for even `n`, verified to `n=200`.

Axioms: the unit `{s(0,0)}`; for every cell with `t >= 1`, the full truth-table
clause set over its **in-diamond** parents (8 clauses per rule-30 cell, 4 per
rule-90 cell, fewer at the boundary).  Parents outside the diamond lie outside
the forward light cone, are identically 0, and are substituted as constants.
That substitution is exact and is checked, not assumed (`gate_encoding`).

Target: the unit clause asserting the true value of `s(n,0)`.  Length of a
derivation = number of resolution steps.

This is character-for-character the convention of
`experiments/rule30/proof-complexity/mus_probe.py` and of the sibling arm
`a4_p3_resolution`, so the numbers compose.  The identical convention is used
for rule 90, or the control comparison would be void.

**Independent replication.** This arm's baseline was implemented from scratch
and reproduces the sibling arm's counts exactly: 24, 96, 384, 1536, 6144,
24576 for rule 30 and 16, 64, 256, 1024, 4096, 16384 for rule 90 at
`n = 4..128`.

## 2. Measured derivation lengths, every step machine-checked

`derivations.log`, rule 30:

```text
     n    cells   baseline   sliced  backward  bwd+slice  base/n2  slic/n2   bwd/n2  bwd/cells
     4       13         24       20        12         14   1.5000   1.2500   0.7500     0.9231
     8       41         96       91        40         58   1.5000   1.4219   0.6250     0.9756
    16      145        384      285       144        179   1.5000   1.1133   0.5625     0.9931
    32      545       1536     1342       544        810   1.5000   1.3105   0.5312     0.9982
    64     2113       6144     5304      2112       3136   1.5000   1.2949   0.5156     0.9995
   128     8321      24576    19436      8320      11485   1.5000   1.1863   0.5078     0.9999
```

rule 90:

```text
     n    cells   baseline   sliced  backward  bwd+slice  base/n2  slic/n2   bwd/n2  bwd/cells
     4       13         16       12         8          8   1.0000   0.7500   0.5000     0.6154
     8       41         64       40        24         24   1.0000   0.6250   0.3750     0.5854
    16      145        256      144        80         80   1.0000   0.5625   0.3125     0.5517
    32      545       1024      544       288        288   1.0000   0.5312   0.2812     0.5284
    64     2113       4096     2112      1088       1088   1.0000   0.5156   0.2656     0.5149
   128     8321      16384     8320      4224       4224   1.0000   0.5078   0.2578     0.5076
```

The four families:

* **baseline** — row simulation: derive the unit clause of every diamond cell
  in topological order from all read parents.  `1.5 n^2` (rule 30), `n^2` (rule 90).
* **sliced** — antecedent-minimal: rule 30's OR latch means that when
  `s(t,x)=1` the child is determined without `s(t,x+1)`, so whole subtrees can
  be dropped.  Retains only the backward slice.
* **backward** — the best family, below.  `n^2/2 + n` and `n^2/4 + n`.
* **bwd+slice** — backward elimination restricted to the slice.

## 3. The best family: backward elimination, and how it was found

The exact minimum **tree-like** derivation length was computed at `n = 2,3` by
Dijkstra over the clause space (`p3_optimal_witness.py`; cost of a resolvent =
cost of its two parents + 1).  The optimum is 4 at `n=2` and 7 at `n=3`,
against a baseline of 6 and 13.  Reconstructing the optimal derivation shows a
mechanism the baseline does not use: **it derives no intermediate unit clause
at all.**  It starts from the target cell's firing clause and resolves each
ancestor variable away against that ancestor's own firing clause, deepest
first, until only the seed literal remains:

```text
{~(2,-1),(2,0),(2,1),(3,0)} + {~(1,-1),~(1,0),~(1,1),~(2,0)} on (2,0)
   => {~(1,-1),~(1,0),~(1,1),~(2,-1),(2,1),(3,0)}
... + {~(1,0),~(1,1),~(2,1)} on (2,1)  => {~(1,-1),~(1,0),~(1,1),~(2,-1),(3,0)}
... + {~(1,-1),~(1,0),(2,-1)} on (2,-1) => {~(1,-1),~(1,0),~(1,1),(3,0)}
... + {~(0,0),(1,-1)} on (1,-1)         => {~(0,0),~(1,0),~(1,1),(3,0)}
... + {~(0,0),(1,0)} on (1,0)           => {~(0,0),~(1,1),(3,0)}
... + {~(0,0),(1,1)} on (1,1)           => {~(0,0),(3,0)}
... + {(0,0)} on (0,0)                  => {(3,0)}
```

Generalized (`p3_core.derive_backward`) this is exactly one resolution step per
ancestor cell.  Closed form, verified for every even `n` in 2..200
(`closedform.log`):

```text
  |D_n|            = n^2/2 + n + 1
  rule 30 backward = n^2/2 + n  =  |D_n| - 1
  rule 90 backward = n^2/4 + n
```

This is a **2.95x** constant-factor improvement over the row-simulation
baseline PATH.md R9 names, and 3.88x for rule 90.  It is not sub-quadratic.

**Do not read "optimal" as more than it is.** The search minimizes *tree* cost,
and `min_DAG <= min_tree`, so `EXHAUSTED: none shorter` at cap `= |bwd| - 1`
excludes no shorter DAG derivation: a DAG that reuses a subderivation has tree
cost above its DAG length and would not be enumerated.  What is established is
"no shorter **tree-like** derivation exists" — at `n = 2,3` for rule 30, and at
`n = 2,3,4` for rule 90 (section 10).  The DAG question is open and belongs to
the lower-bound arm.

## 4. The trap this arm nearly walked into: finite-size exponents

The least-squares log-log fit over `n = 4..128` reads **1.8935** for the rule 30
backward family and **1.8165** for rule 90.  Both quantities have the exact
quadratic closed forms above.  A six-band ladder manufactures a sub-quadratic
exponent for `n^2/2 + n`.  This is ARM7's named failure mode ("reporting a
subquadratic empirical exponent as if it implied `poly(log n)` work") firing on
this arm's own data, and it is the reason the closed form is checked to `n=200`
rather than the fit being reported.

The same discipline applied to the slice ladder, where no closed form is
available, requires a long ladder.  `slice.json`, `n = 16..8192`:

```text
rule 30 n=8192  diamond=33562625  best slice=28061755  fill=0.8361
        fitted exponent 1.9907    local slope (top 3 bands) 2.0002
rule 90 n=8192  diamond=33562625  best slice=16785409  fill=0.5001
        fitted exponent 1.9708    local slope (top 3 bands) 1.9989
```

Rule 30's antecedent-minimal slice is a near-constant **0.83** fraction of the
diamond out to `n = 8192`.  That independently corroborates the stored GMUS
probe's 76-82% fill (`RESULTS-proof-complexity-probe.md`, `n <= 256`) on a
ladder 32x longer, by a method that shares no code with it.  Rule 90's slice is
exactly the even-parity sublattice, `(n/2+1)^2`, fill `-> 1/2`.

## 5. Block doubling, actually built, is strictly worse

Rows 19, 21, 22, 23 and 24 all proposed a dyadic block state with an assumed
`O(1)` merge.  The derivation-length setting lets that story be built and
counted rather than named.  `derive_kstep` derives units only on rows divisible
by `k`; for each such target the `k`-step composed clause over its row-`(t-k)`
ancestors is **derived** from the one-step axioms by resolving every
intermediate cell variable away, and every one of those steps is counted.
Length as a multiple of the best family (`derivations.log`):

```text
rule 30   k=1 (row simulation) 2.95x
   k=2   n=4:1.83x  n=8:2.70x  n=16:3.28x  n=32:3.62x  n=64:3.80x  n=128:3.90x
   k=4             n=8:2.50x  n=16:4.06x  n=32:4.97x  n=64:5.47x  n=128:5.73x
   k=8                        n=16:3.83x  n=32:6.74x  n=64:8.32x  n=128:9.15x
   k=16                                   n=32:6.50x  n=64:12.08x n=128:14.99x

rule 90   k=1 (row simulation) 3.88x
   k=2   n=4:1.75x  n=8:2.83x  n=16:3.70x  n=32:4.28x  n=64:4.62x  n=128:4.80x
   k=16                                   n=32:6.61x  n=64:12.44x n=128:15.62x
```

Monotone in `k` and monotone in `n` at fixed `k`, on both rules: coarser blocks
cost strictly more, up to 15x worse at `k=16, n=128`.  The reason is structural
and is the seam named in section 8: distinct cells carry distinct variables, so
a composed clause built for one block is a clause about that block only and is
never reused by another.  Self-similarity of the Rule 30 diagram does not
become clause-level reuse in a fixed-seed CNF.

## 6. The sandwich over this encoding

The sibling arm `a4_p3_resolution` computes `mu(n)`, the size of the smallest
sufficient cell set (SMUS), exactly at small `n`, and proves a leaf-counting
bound: any resolution derivation of `c_n` has length `>= mu(n) - 1` (every step
has fan-in 2, so a derivation DAG containing `k` distinct axiom leaves needs at
least `k-1` steps).  `mu(n)` is theirs; the upper bounds are this arm's.

| rule 30 `n` | leaf bound `mu-1` (theirs) | best derivation (here) | window |
|---|---|---|---|
| 4 | 8 | 12 | 1.50x |
| 6 | 16 | 24 | 1.50x |
| 8 | 32 | 40 | 1.25x |

The sibling arm recorded `UB/LB = 3.00` at these `n` against the row-simulation
baseline.  The backward family **cuts the known window over this encoding from
3.00x to 1.25-1.50x**.  Consequence, stated as the conditional it is: no
`o(n^2)` derivation exists over this encoding unless `mu(n)` is itself
sub-quadratic.  Two independent measurements say it is not — this arm's slice
fill 0.83 to `n = 8192`, and the stored GMUS probe's 76-82% to `n = 256` — and
neither is a proof (obstruction H: finite data cannot establish an infinite
statement; `mu(n)` itself is exact only to `n = 8`).

## 7. The Rule 90 filter, and what it actually showed

The task's filter expected a large gain on rule 90, whose cells have
closed-form binomial-parity values.  Measured: rule 90 gets a factor of
**2** over rule 30 and **no exponent gain at all** — `n^2/4 + n` against
`n^2/2 + n`, both exactly quadratic.  Scoped precisely: *these families* give
rule 90 no sub-quadratic derivation.  This is not a claim that none exists.

The reason is the most transferable finding in this document, and it qualifies
the reading of the stored probe.  Rule 90's GMUS is a sparse
`n^{log2 3} ~ n^1.585` odd-binomial set whose fill fraction *vanishes*
(0.415 -> 0.103).  A small sufficient axiom set does not yield a short
resolution derivation, because that skeleton telescopes only under a parity
argument, which is exactly the Tseitin regime resolution is classically bad at.
**Axiom-subset size and derivation length decouple**, demonstrated on the
control.  The stored probe's own aside — rule 90's `n=256` GMUS extraction
stalling in CDCL parity reasoning while rule 30's did not — is consistent with
this and now has a reason attached.

Second filter result, in the opposite direction: Rule 30's OR nonlinearity, the
one structure that lets antecedents be dropped, makes the best family
**worse**, not better (`bwd+slice` 11485 against `backward` 8320 at `n=128`),
because each dropped antecedent costs a specialisation step that exceeds the
cells it saves.  The nonlinearity gives no derivation-length leverage either.

## 8. The missing lemma, stated as a missing lemma

Nothing below is claimed to hold.  This is the exact statement that a
sub-quadratic family would need and that could not be derived.

> **BLOCK-SUMMARY LEMMA (not proved, not assumed).**  There is a family of
> clause sets `S_B`, one for each dyadic spacetime block `B` of `D_n`, with
>
> (i) `|S_B| = o(area(B))`;
> (ii) `S_B` derivable in resolution from `B`'s local axioms together with the
>      `S_{B'}` of `B`'s four children in `o(area(B))` steps;
> (iii) `c_n` derivable from `S_root` in `o(n^2)` further steps.

Which condition each measurement kills, and how:

* **(i) fails for both instantiations that could be built.**  Taking `S_B` to
  be the unit clauses of the retained cells gives `|S_B| = 0.83 * area(B)`,
  measured to `n = 8192`, a constant fraction with local slope 2.0002.  Taking
  `S_B` to be the composed firing clauses of the block's top row gives one
  clause per top-row cell whose width is the block's full row-`(t-k)` ancestor
  span.
* **(ii) fails monotonically in composition depth.**  Built and counted at
  `k = 2, 4, 8, 16` over `n = 4..128`: every `k > 1` is strictly worse than
  `k = 1`, and worse as `k` grows, on both rules (section 5).
* **The structural reason both fail** is one line, and it is obstruction D
  restated in this setting: a clause is a set of literals over specific cell
  variables, distinct cells have distinct variables, so a summary clause for
  one block is never a clause for any other.  Geometric self-similarity of the
  Rule 30 diagram cannot become clause reuse in a fixed-seed CNF.  Any
  sub-quadratic family must therefore find summaries whose *size* shrinks, not
  summaries that repeat.

No phrase of the form "under an exact composition law (derivable ...)" appears
in this document, and none of the three conditions is assumed anywhere in the
code.

## 9. Obstruction checks

**Obstruction G — arbitrary-input measures versus a single fixed point.**
Executed, with numbers.  P3 fixes the input to the lone seed and varies only
`n`.  Circuit size, decision-tree depth, sensitivity and algebraic immunity are
measures of a function of variable inputs and are identically zero on a
one-point domain, which killed rows 63-66.  Derivation length is not such a
measure: with the input fixed to the lone seed, the measured length is 4 at
`n=2`, 12 at `n=4`, 8320 at `n=128`, with exact closed form `n^2/2 + n`,
strictly increasing in `n`.  A quantity obstruction G kills would be constant
in `n` here.  It is not.  The framing evades G, exactly as PATH.md 7.3 says row
9 was built to.

**Obstruction D — the missing composition law.**  Addressed by construction
order, in the order the task required: the baseline was built and counted
mechanically first; the candidate families were built concretely and counted
for the same `n`; the derived unit was checked against
`experiments/rule30/center_column.py` at every band; and no asymptotic claim is
made that is not backed either by a verified closed form or by a ladder to
`n = 8192` with its local slope reported.

**Obstruction H — finite data cannot establish an infinite statement.**  The
`mu(n)` sandwich is exact only to `n = 8`; the tree-optimality of the backward
family is established only at `n = 2,3` (rule 30) and `n = 2,3,4` (rule 90);
rule 30's `n = 4` search hit its cap (see section 10).  None of these becomes an asymptotic statement.  The closed
forms in section 3 are the only unconditional claims here, and they are claims
about the constructions, not about the minimum.

**Wolfram's Problem 3.**  Stated in the same sentence as every result above: a
proof-complexity upper or lower bound over this encoding does not resolve
Wolfram's Turing-machine formulation of Problem 3, because proof systems with
extension simulate fast algorithms, so nothing measured here transfers to the
prize question.

## 10. Walls hit, and the instrument that had to be discarded

**The DRUP trap.**  The obvious way to measure "achieved derivation length" is
to run a CDCL solver on `F_n AND (wrong-value unit)` and count its proof
lemmas.  That instrument is void here, and spectacularly so.  `drup.log`:

```text
rule 30 n=128 UNSAT=True  DRUP lemmas=0  level-0 forced literals=8321  ...
rule 90 n=128 UNSAT=True  DRUP lemmas=0  level-0 forced literals=4225  ...
```

The formula is refuted by unit propagation at decision level 0, so CDCL learns
nothing and emits a **zero-length** proof at every `n` tested.  Reporting that
as a derivation length would have produced a spurious `O(1)` "upper bound" out
of nothing — obstruction D in a new costume.  The honest number is the
expansion of the single implicit RUP step into resolution inferences, which is
the level-0 propagation chain: 8321 forced literals for rule 30 at `n=128`,
exactly `|D_n|`, and 4225 for rule 90, exactly the even-parity sublattice
`(n/2+1)^2` — which is precisely this arm's rule 90 slice size, arrived at by a
second route.  Solver proof length is not resolution derivation length for this
family, and no number in this document comes from a solver's lemma count.

**The minimum-length search wall.**  Exhaustive tree-cost search, asking at
each `n` whether anything strictly shorter than the backward chain exists
(`minlen.log`):

```text
rule 30 n=2  backward=4   search<=3:  EXHAUSTED: none shorter   settled=145
rule 30 n=3  backward=7   search<=6:  EXHAUSTED: none shorter   settled=6039     7.5s
rule 30 n=4  backward=12  search<=11: WALL (node cap)           settled=32001  1490.8s
rule 90 n=2  backward=3   search<=2:  EXHAUSTED: none shorter   settled=40
rule 90 n=3  backward=3   search<=2:  EXHAUSTED: none shorter   settled=78
rule 90 n=4  backward=8   search<=7:  EXHAUSTED: none shorter   settled=17238   26.8s
```

So the backward family is tree-optimal at `n = 2,3` for rule 30 and at
`n = 2,3,4` for rule 90.  Rule 30's `n = 4` band is where the instrument stops:
the search is `O(settled^2)` in Python, and the 32,000-clause cap is reached
after 1491 s without exhausting the space.  The cap is on settled nodes, not
wall time, so the wall is reproducible.  Tree-optimality for rule 30 at
`n >= 4` is left open.  The search is `O(settled^2)` in Python and this is where it stops.
Obstruction H applies to the whole of section 3: two exhausted bands buy a
statement about `n = 2` and `n = 3`, and nothing asymptotic, ever.

## 11. What a reader must not over-read

1. **This is a constant factor, not an exponent.**  `n^2/2 + n` is `Theta(n^2)`.
   The inverted kill condition in R9 — a sub-quadratic derivation family — did
   **not** fire.  No mechanism candidate for the Arm 3 tournament is produced.
2. **Nothing here is a lower bound.**  The `mu(n)` sandwich is the sibling
   arm's lemma applied to this arm's constructions, exact only to `n = 8`, and
   the conclusion in section 6 is conditional on `mu(n)` not being
   sub-quadratic, which is measured and not proved.
3. **"Optimal" means tree-optimal at `n = 2,3`.**  A shorter DAG derivation at
   those `n`, or any shorter derivation at `n >= 4`, is not excluded.
4. **The 1.89 and 1.82 fitted exponents in section 4 are artifacts** of a
   six-band ladder on exact quadratics.  Quote the closed forms, never the fit.
5. **The rule 90 statement is about these families**, not about rule 90.
6. **Everything is relative to one encoding.**  A different CNF for the same
   question, or a stronger proof system, is a different problem; systems with
   extension in particular simulate fast algorithms, which is why none of this
   touches Wolfram's Problem 3.

## Reproduction

```sh
cd experiments/overnight-arms/frontier_attack/a13_p3_upper_bound
V=/Volumes/A/researchpapers/.venv/bin/python
$V p3_core.py                                     # gates
$V p3_tables.py --ns 4 8 16 32 64 128 --out derivations.json
$V p3_slice_ladder.py --out slice.json
$V p3_closed_form.py
$V p3_drup_trap.py --ns 4 8 16 32 64 128 --out drup.json
$V p3_optimal_witness.py
$V p3_minlength.py --ns 2 3 4 --node-cap 32000 --out minlen.json   # ~25 min
```

Modal: $0.  Paid model-provider calls: $0.

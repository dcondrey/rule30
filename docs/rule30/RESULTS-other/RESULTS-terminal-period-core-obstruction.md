# Terminal-period attempt: sparse cores, eventual exclusions, and an unclosed return mechanism

Date: 2026-09-09.

**Deliverable (c): a precise obstruction report. The terminal-period theorem
is not proved, and no right-realizable counterexample is exhibited.** The 24
rung-4 refutations yield 15 sparse patterns that are uniformly forbidden
sufficiently late under an alternating centre. These give new all-period
necessary conditions, but their complete avoidance graph still admits the
primitive family

```text
rho_k = 00001 00001 (001)^(k+2),      h_k = 16+3k,      k>=0.
```

This is an exact counterexample to the proposed **criterion**, not to the
terminal-period theorem. Its first member is itself excluded by a new
finite cone at prefix length 51. A concrete missing step is an **unbounded periodic
return lemma** controlling arbitrarily many two-zero gaps between visits to
the four-zero-gap region. Neither the recorded cones nor pumping in their
finite avoidance graph supplies that lemma.

The [rung-4 report](RESULTS-ladder-rung4-q420-periodic-obstructions.md) is the
input classification. Evidence labels retain the repository convention:
`U` uniform proof, `R` reduction, `C` finite certificate, `M` measurement,
`K` counterexample to a stated mechanism.

| Finding | Evidence |
|---|---|
| All 24 original DRUP proofs traced to independently UNSAT input supports | `C`, 34,810 checked additions |
| Deletion-minimal sample cores contain 4–8 observations; 15 distinct normalized masks | `C/M`, new CNF/DRUP certificates; 134 deletion witnesses |
| Sparse cores imply eventual forbidden masks, uniformly over periods and onsets | `U`, reset the cone before the occurrence |
| Consecutive zero-gap block `33` is eventually impossible | `U/C`, h4 core plus `11` exclusion |
| Both registered finite-factor criteria fail | `K/U/C`, explicit graph returns and unbounded primitive families |
| Regression accepts exactly the four known necklaces through h=15 | `C`, all 4,720 necklaces, zero mismatches |
| Two graph-derived h16 words are not right-realizable | `C/K`, shortest canonical prefixes 24 and 51, new DRUP proofs |
| Terminal-period theorem; periodic branch of q=420; aperiodic branch | **Open** |

## 1. Registration and what was computed

[REGISTRATION.md](../../experiments/rule30/terminal-period/REGISTRATION.md)
and [FACTOR-REGISTRATION.md](../../experiments/rule30/terminal-period/FACTOR-REGISTRATION.md)
record the candidates and kill conditions before their graph calculations.

The first candidate was that the seven frozen factors plus the 24 certified
prefixes admit only `01`, `001`, `00001`, `0000101` as primitive periodic
words. The strengthened candidate adds the normalized sparse cores as
eventual restrictions. In each case an explicit exceptional periodic label
on a graph return kills the criterion. A graph survivor is not treated as
an actual right extension.

There was **no necklace census beyond h=15**. Higher-period words below were
derived from graph returns to check a proposed uniform criterion. Testing
longer members of a displayed family is not used to infer its all-k claim:
that claim follows from the two exact return paths.

The old JSON records counts and the 24 residual necklaces, rather than an
explicit row for every necklace. Two implementations regenerated precisely
the existing range. The full 4,720-row regression is now persisted in
[input-verification.json](../../experiments/rule30/terminal-period/input-verification.json).
The arithmetic is 4,692 frozen-factor exclusions + 24 cone exclusions +
4 realizations = 4,720; thus there are **4,716 excluded necklaces**.

## 2. What the 24 cores actually share

For each saved CNF, the extraction reconstructs every clause from its
space-time coordinate and the scalar Rule 30 truth table. It performs two
different operations:

1. Trace RUP conflict reasons backward through the saved DRUP proof to an
   UNSAT subset of original clauses. Independently solve that subset again.
2. Hold every original transition clause fixed, remove all rho observation
   units, and delete observations in increasing sample order whenever
   UNSAT persists. Recheck every retained observation's necessity, saving
   and forward-replaying a SAT initial row for its deletion.

The second result is **inclusion-minimal in the observation assumptions**,
relative to the full transition base. It is not minimum cardinality, and
the first result is not claimed to be a clause-minimal MUS. Different
deletion orders can select different cores. Consequently distinct selected
masks refute only literal identity of these selected templates, not every
possible shared mechanism.

Each selected core also has a **new** CNF/DRUP certificate. The frozen
checker verified all 93,035 new proof additions and rechecked the persisted
files. All 134 single-deletion initial rows were replayed with the unchanged
`numeric_rho`. A separate audit confirmed that each new CNF contains exactly
the old transitions and its selected observation units: no hidden pins,
spatial wrap, temporal wrap, or periodic farther columns.

Write `N` for the original shortest infeasible canonical prefix, `a` for the
first selected sample, and `P` for its normalized mask. A question mark
means that sample is unprescribed. All indices are zero based.

| rho necklace | N | a | P |
|---|---:|---:|---|
| `0001` | 32 | 23 | `1?0?1?0?1` |
| `00001001` | 32 | 4 | `1???00??1????0???????0??1??1` |
| `000010001` | 18 | 6 | `0??0?0?1?0?1` |
| `0001000101` | 18 | 7 | `1???0?1???1` |
| `00001000101` | 31 | 11 | `0????????????0?1?0?1` |
| `00001001001` | 30 | 7 | `1????0??1??1????0??1??1` |
| `00001010001` | 22 | 6 | `1??????0?1??00?1` |
| `000010000101` | 24 | 9 | `1????0??0???1?1` |
| `000010001001` | 21 | 9 | `0??0?0?1?0?1` |
| `000100010101` | 20 | 9 | `1???0?1???1` |
| `0000100001001` | 39 | 9 | `1?????????0??1???00????0??1??1` |
| `0000100010001` | 22 | 10 | `0??0?0?1?0?1` |
| `0000101010001` | 46 | 15 | `0????????????0?1???1????????1?1` |
| `00001000010001` | 14 | 2 | `0??0?0?1?0?1` |
| `00001001001001` | 36 | 10 | `1????0??1?????1????0??1??1` |
| `00001010001001` | 14 | 4 | `1??0??1??1` |
| `00010001000101` | 22 | 11 | `1???0?1???1` |
| `00010001010101` | 22 | 11 | `1???0?1???1` |
| `000010001000101` | 26 | 15 | `0?0?1?0?1?0` |
| `000010001001001` | 24 | 12 | `0??0?0?1?0?1` |
| `000010001010001` | 24 | 12 | `0??0?0?1?0?1` |
| `000010010000101` | 15 | 4 | `1???0???1?1` |
| `000010100010001` | 15 | 4 | `1???0?1???1` |
| `000010101010001` | 39 | 12 | `0????0?1??????????0?0?1???1` |

There are 15 distinct masks, of span 9–31, with first selected index 2–23.
Six cores share `0??0?0?1?0?1`; five share `1???0?1???1`. These are concrete
shared structures, beyond a similarity in proof sizes.

Every core retains the final sample. This is forced by minimality of the
original infeasible prefix: deleting that sample alone leaves the saved
feasible predecessor. The terminal value is one in 23 cases, but it is
**zero** for `000010001000101`. An explanation requiring every contradiction
to be triggered by a terminal one is therefore false.

Plain unit propagation does not refute any of the 24 original cones. Their
selected DRUP input supports have 172–4,550 clauses, all meet column 1, and
reach as far as columns 7–30 depending on the case. Every support contains
OR-sensitive clauses. These facts rule out identifying the recorded proofs
with a single immediate pin conflict; they are not proof-complexity lower
bounds or claims that every clause in a support is indispensable.

Exact clause IDs, sample indices, proof hashes, truth-table histograms,
and initial rows are in
[core-results.json](../../experiments/rule30/terminal-period/core-results.json).

## 3. The uniform consequence: eventual masks, not fresh-onset masks

**Lemma (`U`).** Suppose a free-initial-row cone with alternating centre is
UNSAT when only samples `rho_(a+d)=e_d`, for `d` in a finite set containing
zero, are prescribed. Then its normalized mask cannot occur at any start
`p>=a` in any actually driven rho.

**Proof.** Start that same cone at macro time `p-a`. Its initial row is the
actual right row at that time, an allowed assignment because the initial
cells are free. The shift is by an even number of original time steps, so
the centre phase remains zero. An occurrence of the mask would satisfy all
selected units and all transitions, contradicting UNSAT. This applies
after any eventually alternating onset. ∎

Thus every actual tail `rho[23:]` avoids all 15 masks, and every eventually
periodic rho must avoid them at every cyclic phase. This is an all-h
consequence of finite certificates.

The prehistory cannot simply be discarded. For h4 the selected observations
are `[23,25,27,29,31] = [1,0,1,0,1]`. But the fresh initial right row

```text
10110010000000110
```

produces `100010001` in nine samples under the unchanged `numeric_rho`.
This is a concrete counterexample to forbidding the normalized h4 mask at
a fresh onset. After sample 23 it is forbidden. Together with `11`, its
four wildcards must be zero, so **two consecutive gaps of three zeros
between ones are eventually impossible**, uniformly in period.

The OR mechanism is explicit. For the even row `a_j=x(T0+2n,j)`, two
updates at the boundary give

```text
b_1 = a_1 OR a_2,
b_2 = a_1 XOR (a_2 OR a_3),
rho_(n+1) = 1 XOR (b_1 OR b_2)
          = NOT(a_1 OR a_2 OR a_3).
```

A sampled one therefore forces the preceding three right cells to zero.
The cores combine repeated such constraints with the reachable rows under
the intervening alternating drive. This identifies a common OR-dependent
framework; it does not yet classify all possible returns of the farther
right tail.

## 4. Why the infeasible prefix lengths are nonmonotone

The repeated mask `0??0?0?1?0?1` has span 12. Its six source cores have
first selected indices `6,9,10,2,12,12`, producing the recorded prefix
lengths `18,21,22,14,24,24`. The h14 certificate supplies its strongest
listed threshold, namely two samples of prehistory. Once that threshold
is available, the varying canonical positions of this same pattern
explain all six prefix obstructions. The h4 contradiction uses a different
mask and a longer sufficient prehistory, 23 samples.

There is also a phase inequality. For a fixed unrealizable primitive word
of period h, let `N_r` be its first infeasible prefix length at rotation r.
A forbidden prefix at phase `r+1` is a suffix of a prefix one symbol longer
at phase r. Hence

```text
N_r <= N_(r+1)+1,       max_r N_r - min_r N_r <= h-1.
```

Across different words there is no monotonicity principle in h. Here the
cores demonstrate recurring sparse patterns and different positions; the
nonmonotonic numbers alone would not have demonstrated a uniform bound.
The selected prehistories are sufficient thresholds, not claimed optimal.

## 5. Exact pumping obstructions to both candidate criteria

The first graph, from the 31 original factors, has 355 states. Its single
recurrent component has 337 states, 466 internal edges, and 129 branching
states. At suffix `0101010`, the labels

```text
A = 0010001010101010,       B = 10
```

both return to the same state. They give the primitive family
`00010001(01)^(k+4)` of periods `16+2k`. The h4 eventual mask excludes this
family, demonstrating a real gain from core extraction.

For the stronger graph, wildcard expansion is pruned using already
forbidden words. Every omitted completion already contains a forbidden
factor, so this preserves the exact intersection language. The 31 original
factors and 15 eventual masks reduce to **45 irredundant concrete factors**.
Two independent constructions agree on the graph: 557 states and 718 edges.
Its single recurrent component has **287 states, 350 internal edges, and
63 branching states**.

At suffix `0100100100`, state 116 in the persisted graph, both labels

```text
A = 0010000100100100,       B = 100
```

return to state 116. Their exact state paths are

```text
A: 116,140,164,189,215,241,266,288,312,338,362,292,317,343,71,91,116
B: 116,71,91,116
```

Therefore `AB^k` is a closed walk for every integer `k>=0`, proving cyclic
avoidance for all k. Moving its final `00` to the front gives exactly

```text
rho_k = 00001 00001 (001)^(k+2).
```

Algebraically the rotation uses `00(100)^k=(001)^k00`. Its cyclic gap word
is `4,4,2,...,2`, with `k+2` twos. The adjacent `4,4` pair occurs exactly
once, so any rotation preserving the word fixes its unique position.
Consequently its minimal period is `16+3k`, not a shorter divisor.

This is a uniform, explicit proof that the **selected 24 cores**, even
after the valid eventual normalization, do not entail the target theorem
through factor avoidance. Exact factors, graph states, paths, and the
4,720-case regression are in
[core-factor-results.json](../../experiments/rule30/terminal-period/core-factor-results.json).

## 6. Actual cone checks of the two graph witnesses

| Criterion that accepts it | Primitive rho | First infeasible canonical prefix |
|---|---|---:|
| Original 31 factors | `0001000101010101` | 24 |
| Original factors plus all 15 eventual masks | `0000100001001001` | 51 |

The second forbidden prefix is exactly

```text
000010000100100100001000010010010000100001001001000
```

Its cone has 101 initial right cells, 5,151 variables and 40,051 clauses;
the new DRUP proof checks 10,961 additions. Its 50-sample predecessor is
SAT. One exact 99-cell initial right row, listed from column 1 rightward, is

```text
011011100011100111001111101010010010001010000010011101000101110001010100101001001011111110011011100
```

The unchanged `numeric_rho` reproduces that predecessor. Independent Z3
cones agree on both feasibility boundaries. The other graph witness has
a 152-addition DRUP refutation, and its 23-sample predecessor is likewise
forward verified. These are checks of specified graph-derived words, not
a classification at h16.

Both words would have neighbour period 32, which does not divide 420,
**if realizable**. Both are UNSAT, so **neither is a q=420 witness**.
See [factor-cone-results.json](../../experiments/rule30/terminal-period/factor-cone-results.json)
and [core-factor-cone-results.json](../../experiments/rule30/terminal-period/core-factor-cone-results.json).

A bounded follow-up minimized only the already-refuted 51-sample cone.
Its nine selected observations give the mask
`0?????0??1????????0???0??1??1????00`, with span 35 and prehistory 16.
It rejects `rho_0` but **misses every `rho_k` with k>=1**. This is also a
uniform statement: the phases were checked for k=1 through 10; for k>=10,
the intervening `(001)` run has length at least 36, so a 35-sample window
meets at most one marked `0000100001` block. All such windows already occur
at k=10. Thus one more local mask does not establish the required induction.

This additional sparse core is solver-checked with nine forward-replayed
single-deletion witnesses; unlike the original 24 sparse cores, it has
**no separate DRUP proof**. Its parent complete-prefix refutation does.
The claim that its mask misses the family is a direct string/graph check,
independent of that extra UNSAT claim. See
[h16-selected-core.json](../../experiments/rule30/terminal-period/h16-selected-core.json)
and [h16-family-mask-results.json](../../experiments/rule30/terminal-period/h16-family-mask-results.json).

## 7. The named missing step

**Unbounded periodic return.** The graph can stay in its two-zero-gap
return for arbitrarily many repetitions before making the `4,4` excursion.
To exclude this family uniformly, an argument must control that return
in the actual Rule 30 right extension for every repetition count. Equal
suffix states only certify avoidance of the selected factors; they do not
identify the sets of feasible right-cone frontiers. The UNSAT h16 word is
an explicit nonliftable graph cycle.

A pumping induction would need a justified operation that deletes or
inserts such a return while preserving actual right-realizability in the
required direction, or an OR-dependent quantity that forces failure for
every cyclic return. No such compatibility lemma follows from these cores.
Other deletion orders, additional patterns, or a stronger abstraction are
not excluded by this failure. The displayed family does not claim to exhaust
the residual graph cycles; excluding it alone would not complete the theorem.

There is a separate **temporal-period lifting gap**. For each fixed strip
width W and periodic rho of period h, a realizing strip has a finite graph
with at most `2h*2^W` row-and-phase states and therefore a periodic strip
realization. Its period and exterior drive can change with W. Passing to
arbitrarily wide strips does not justify a common time period for the full
right half-plane. Thus torus orbit counts cannot fill the return gap.

For a fixed infinite rho, compactness says it is realizable exactly when
every finite prefix cone is SAT. This guarantees a finite obstruction for
each unrealizable word, but supplies no common bound over all primitive
periods. Full proofs of these distinctions are in
[structure-notes.md](../../experiments/rule30/terminal-period/structure-notes.md).

## 8. Rule 90, verification, and reproduction

The unchanged `controls.rule90_control(6)` passes at T=2,4,6: the leftward
map is bijective and the displayed tori are forward correct. The OR reset
above is absent: Rule 90 instead gives
`rho_(n+1)=1 XOR a_1 XOR a_3`.

Indeed Rule 90 realizes every infinite rho. Its n-th sample has the form
`x(0,2n+1) XOR H_n(x(0,1),...,x(0,2n))`: the rightmost initial variable
has coefficient one along its unique ancestral path. Fix the even initial
cells arbitrarily and choose odd cells recursively. Thus none of these
consistent sparse sample constraints can yield a Rule 90 cone refutation.
The argument uses Rule 30's nonlinear OR constraints, not just causality
or periodicity.

The 25 frozen ladder/rung1/rung2 tests pass. The frozen exact language through
length 10 was recomputed; all four positive tori were reconstructed and
forward checked, including `numeric_rho` replays. All original recorded
source and certificate hashes match. No frozen engine was modified;
`ladder.py` retains SHA-256
`589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.
An independent artifact audit checks the exact sparse CNF subsets, all 134
deletion rows, the graph and return paths, and every necklace again in
[output-verification.json](../../experiments/rule30/terminal-period/output-verification.json).

From the repository root, in this order:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/terminal-period/verify_inputs.py
PYTHONDONTWRITEBYTECODE=1 uv run --with python-sat python experiments/rule30/terminal-period/core_analysis.py
PYTHONDONTWRITEBYTECODE=1 uv run python experiments/rule30/terminal-period/factor_graph.py
PYTHONDONTWRITEBYTECODE=1 uv run python experiments/rule30/terminal-period/core_factor_graph.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/terminal-period/factor_cone_check.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with z3-solver --with python-sat python experiments/rule30/terminal-period/factor_cone_check.py --core
PYTHONDONTWRITEBYTECODE=1 uv run --with python-sat python experiments/rule30/terminal-period/h16_selected_core.py
PYTHONDONTWRITEBYTECODE=1 uv run python experiments/rule30/terminal-period/h16_family_mask_check.py
PYTHONDONTWRITEBYTECODE=1 uv run python experiments/rule30/terminal-period/verify_outputs.py
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy --with pytest python -m pytest experiments/rule30/ladder/test_ladder.py experiments/rule30/ladder/test_rung1.py experiments/rule30/ladder-rung2/test_rung2.py -q
```

The main new artifacts occupy approximately 16 MB, including the proofs.

## 9. Honest scope

This attempt establishes sound all-period necessary restrictions and
identifies exactly why the registered finite criteria fail. It proves
neither the terminal-period theorem nor its negation. It does not establish
right-realizability of any member of the residual family, including those
with h>=19. No stabilization inference or prime-pattern argument is used.

No fixed-radius observation is used to decide eventual periodicity of an
unknown configuration. The masks are necessary consequences of finite
driven cones, valid along the entire tail after their proved thresholds.
If a future finite avoidance graph actually had only the four simple
recurrent cycles, it would prove the stronger statement that every driven
rho is eventually one of them. This graph has a branching recurrent
component, so that stronger conclusion is unavailable too.

**R7's q=420 gap remains open, in both the periodic and aperiodic branches.**
A proof of the requested terminal-period theorem would retire the periodic
branch because 4,6,10,14 divide 420. That theorem alone would still leave
the aperiodic neighbour case unresolved. No assertion about P1, P2, or P3
follows from this obstruction report.

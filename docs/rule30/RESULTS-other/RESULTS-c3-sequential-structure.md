# C3 has an eight-state diagonal comparator; source-state closure remains open

Date: 2026-09-09. Overnight Task 5.

**The full-affine edge comparison has an exact minimal eight-state sequential
machine when its input is the pair of dependency diagonals. Generating those
diagonals from the source remains the unresolved part.** Exact source-order
minimization gives growing finite lower bounds for raw edges, but no
unbounded-state theorem and no obstruction of comparable size for C3's
existential predicate.

| Finding | Level |
|---|---|
| Relative affine permutation gives an eight-state diagonal comparator | `U`, group identity; `C`, complete transition/minimality check |
| Raw boundary edge needs 13,207 source-order residual states at n=22 | `C`, exact minimization of its entire truth table |
| A subcube consisting only of hard-core words needs up to 60 states at n=22 | `C`; raw edges, not survival-restricted edges |
| Raw H has at most two residual states in the measured lengths through 22 | `C`; not a uniform bound |
| Neither finite growth nor high degree establishes unbounded sequential memory | logical limitation; the overnight prompt's stronger inference is unavailable |
| C3, source-state closure, and legal-row reachability | **Open** |

## 1. Exact uniform machine

Use `constant_tail_zero_prefix_bitsliced.zero_prefix_bitsliced_graph` as the
definition, including all `(alpha,beta,gamma)` coordinates and the forced
symbol. For adjacent zero-prefix scenarios, call their newest-cut affine
permutations `A,B` in the eight-element group `D8`. Their initial boundary
permutations agree. A paired diagonal letter supplies fixed-left local
permutations `L_x,L_y` and updates

```
A' = L_x A,       B' = L_y B.
```

Store just `h=B A^(-1)`. Then

```
h' = L_y h L_x^(-1),       initial h = identity,
edge present iff h != identity.
```

This is closed on eight states for arbitrary diagonal length. Equality of
the full affine maps already forces equality of the forced symbols, for
either fixed tail; that coordinate is checked, not silently discarded.
The complete 16-letter transition table is in `diagonal-machine.json`.
All eight states are reachable, and exact Moore refinement distinguishes
all eight. The update agrees with the full pair of affine maps on all
`8*8*16 = 1,024` cases. The equality output is emitted after the final
diagonal letter, so no terminal comparison is omitted.

This construction is a consequence of the already known D8 structure,
not a new explanation of why C3 should hold. The input consists of the
**already constructed** scenario diagonals. The frozen forcing routine
builds and extends those diagonals using a growing boundary. No reduction
of that generator to this eight-state comparator is established. Confusing
these inputs would repeat the sibling Psi local/composite error.

## 2. Exact source-order minimization

For fixed `n,tail,j`, read `W_0,...,W_(n-1)` once and emit one bit at the end:

```
E_j(W) = [j in raw S_j(W)]
H_j(W) = [some k>=j belongs to raw S_j(W)].
```

These raw functions are defined before survival filtering, as in the
degree audit. Length, query row and read position are supplied for free.
At cut `d`, two prefixes can share a deterministic state exactly when
their residual truth tables over the last `n-d` symbols agree. Thus the
number of distinct residuals is an exact minimum **at that cut**, even for
machines whose transition rule depends on the read position. It is not the
minimal size of one uniform DFA spanning all lengths.

`minimize.py` computes full truth tables from the imported bit-sliced
forcing kernel, reduces residuals bottom-up, and independently checks the
reduction by direct residual-table comparison at small sizes. It never
minimizes an observed sample of source words.

| n | max E residual states | max E on HC subcube | max H residual states |
|---:|---:|---:|---:|
| 4 | 3 | 2 | 1 |
| 6 | 6 | 2 | 2 |
| 8 | 14 | 3 | 1 |
| 10 | 37 | 4 | 1 |
| 12 | 84 | 8 | 2 |
| 14 | 229 | 9 | 1 |
| 16 | 668 | 13 | 1 |
| 18 | 1,854 | 22 | 1 |
| 20 | 4,949 | 34 | 1 |
| 22 | 13,207 | 60 | 2 |

The run covers every length 1–18, then 20 and 22, both tails and every
`0<=j<n`. The largest full-cube entry is tail 2, row 2, cut 17 at n=22.
Consequently no deterministic machine with fewer than 13,207 states can
compute **that raw edge in that read order**, even with the length and
position available. An algorithm computing all sensitivity sets must
handle this edge, but a different read order, extra passes, or a different
output protocol is not ruled out by this experiment.

This lower bound also has explicit witnesses, not only a state count.
`n22-distinguishable-prefixes.npz` stores 13,207 actual 17-symbol prefixes
and their distinct 32-bit residual truth tables over the remaining five
symbols. For any two rows, any set bit in the XOR of their tables gives a
common suffix that separates the prefixes. `witness.py` independently
recomputes just the two relevant forcing scenarios and constructs this
certificate; its encoding and SHA-256 are in `n22-witness.json`.

For the HC column, even source positions are fixed to symbol `2` and odd
positions vary freely. Every assignment is hard-core, so this is a genuine
independent-bit subcube; no reject-state complexity or arbitrary off-domain
extension is being counted. These are still **raw** functions: a lower
bound on them is not automatically a lower bound after restricting to
legal surviving rows.

## 3. Why neither tempting conclusion follows

The large edge counts do not transfer through the OR to `H_j`. The existing
length-52 witness is rechecked on its entire two-variable hard-core subcube:
`H_49=1 XOR z_49*z_51` with position 50 fixed to symbol 2. It is non-affine,
but itself has a two-state sequential implementation. The small H counts
through 22 therefore cannot justify a uniform affine law or a uniform
state bound, and the degree-52 counterexample cannot kill bounded state.

Conversely, growth across finitely many lengths does not prove growth for
all lengths. It excludes each state budget below the attained finite
maximum for the stated function and model. The prompt's proposed leap
from a growing measured sequence to a limitation theorem for **all**
bounded-state descriptions is not valid. The one-million-state cutoff was
not hit; the requested finite experiment ends at the listed lengths, with
the all-length question expressly unresolved.

The concrete remaining task is a source-level recurrence for `H_j` with
survival and the entering affine phase retained, or an explicit family of
pairwise distinguishable source prefixes at unbounded lengths. Neither
has been produced here. No automaticity, Christol, or uniform-measure route
is inferred from these data.

## 4. Controls and reproduction

There are 5,616 independent scalar scenario/row comparisons through n=5
and 62 comparisons with the exact frozen hard-core graph. These include
the source/extension seam and all legal rows up to the graph's returned
survival length. The alpha-only witness `21212122`, tail 2, row 2 again has
support `{1,2,3,5,6,7}`.

The Rule 90 kernel is source-independent on 1,032 checked full support
rows through n=5, both tails. The existing Rule 30 permutation calibration
passes through n=4. This is a kernel comparison, not a transplanted
Rule 90 endpoint-language theorem. The separate unchanged rung-2 Rule 90
control passes in the Task 3 artifact. As a sequential-computation control,
n-input AND has at most two residual states at every measured length,
despite degree n. No averaged statistic or fixed-window P1 proof is used.

```
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/c3-sequential/minimize.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/c3-sequential/diagonal_machine.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/c3-sequential/witness.py
```

The JSON records complete layer profiles, truth-table hashes and imported
kernel hashes. P1 and C3 remain open.

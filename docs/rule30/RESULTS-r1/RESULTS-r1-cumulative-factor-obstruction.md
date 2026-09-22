# The cumulative factor return obstruction

Date: 2026-09-09. Evidence: **C** (exact finite avoidance graph and strip
sets), **U/C** (all-length accepted loop family), **R** (remaining
realization obligation). This is an intermediate result, not an R1
proof or kill.

## 1. Registered mechanism and kill condition

Combine the certified necessary eventual factors from
`terminal-period/core-factor-results.json`, both subsequent terminal
cone checks, the uniform 56-sample family-seam word, and all eleven
certified shortest prefixes for `k=0,...,10` from that family. Build the
exact finite prefix-suffix avoidance graph.

If every recurrent strongly connected component is a simple cycle,
every infinite path is eventually periodic. Since every actual
alternating-centre rho tail is a path in this graph, that would prove
the period-two instance of R1. If branching survives, extract actual
return paths rather than extrapolating a necklace census.

The kill condition does **not** fire. One branching recurrent component
survives.

## 2. Exact counts and independent checks

| Quantity | Count |
|---|---:|
| Input factor records, with provenance | 59 |
| Distinct factors | 58 |
| Factors after substring redundancy removal | 57 |
| Avoidance graph states | 1,088 |
| Avoidance graph edges | 1,406 |
| Recurrent components | 1 |
| States in the recurrent component | 811 |
| Internal edges in the recurrent component | 1,028 |
| Branching states in the recurrent component | 217 |

The old core graph contributed 45 minimal factors. All twelve distinct
new family boundary/seam factors survive substring reduction. The old
factor-cone word `000100010101010100010001` is redundant because it
contains `100010001`. The core-cone word duplicates the new family's
`k=0` boundary. The inherited maximum normalization burn-in is 23 rho
samples; the new exact-prefix cone words themselves can be excluded
at any alternating-centre onset.

The graph is built twice, by the frozen fast failure-link construction
and the independent frozen prefix-suffix construction; all states and
edges agree exactly. Iterative Kosaraju and a separate Tarjan
implementation give identical full SCC partitions. All four known
realized primitive words `01`, `001`, `00001`, `0000101` survive.
Increasing graph-state counts after adding factors reflect the longer
suffix memory, not an enlargement of the accepted language.

Every retained CNF/proof hash in the added-factor manifests is checked.
The already independently checked cone certificates are inputs here;
their large DRUP files are not re-proved by the graph calculation.
The complete graph, factor provenance, source hashes, and SCC state
lists are saved in
`experiments/rule30/r1-isolated-column/cumulative-factor-results.json`.

## 3. Shortest extracted return family

Among all branching vertices, take a shortest return after each of its
two outgoing edges and minimize the sum of the two return lengths.
The selected common state has suffix `0101010` (state 54), with

```text
A = 00100001010101010    (length 17)
B = 10                   (length 2).
```

The exact return traces are

```text
A: 54,75,97,108,133,159,186,214,242,269,178,205,169,196,224,252,39,54
B: 54,39,54.
```

**U/C.** Every word `A B^k`, every cyclic repetition of such a word,
and every infinite concatenation of the two returns avoids all 58
distinct factors. This follows from concatenating the checked paths
at their common safe state; it is not an inference from finitely many
values of `k`.

The canonical periodic family is

```text
rho_k = 00001 (01)^(k+4) 0001,       h_k = 17+2k, k>=0.
```

It has one four-zero gap, one three-zero gap, and `k+4` one-zero gaps
per period. The unique four-zero gap proves the stated period is
minimal: a nontrivial repetition would repeat that gap. If realizable,
it would fail to be a `q=420` witness only for `k=2,9,44`, corresponding
to `h=21,35,105`, the odd divisors of 210 at least 17. No member is
claimed realizable.

The smallest novel necklace among the separately inspected shortest
return candidates is already length 16:

```text
rho = 0000100001010001                 (gaps 4,4,1,3)
common suffix = 00010000101000
A = 1000010000101000                   (length 16)
B = 01000010000101000                  (length 17).
```

This is a precisely specified extracted candidate, not a claim that
all shorter or equally short graph cycles have been classified anew.

## 4. The direct gap-one seam test survives

The shortest-return family spends an arbitrarily long time in the
known realizable gap-one regime `(01)^infinity`. Its exceptional
return consists of a three-zero gap followed by a four-zero gap.
Reuse the sound width-20 strip relation from the family-seam proof:
all exterior bits are allowed independently at each microstep, so
every actual right half-plane projects to a strip path. Starting
with all odd rows, put

```text
G(X) = B_01(X),          E(X) = B_000100001(X).
```

The descending gap-one image sets stabilize after eleven blocks at
1,288 rows. The complete cardinality sequence is

```text
524288,24332,5400,2579,2114,1767,1598,1422,1361,1310,1291,1288,1288.
```

The excursion has 1,076 possible endpoint rows. Subsequent gap-one
returns have counts

```text
j=0,...,22:
1076,888,602,641,664,667,904,983,1055,1092,1107,1112,
1138,1164,1181,1213,1228,1247,1260,1264,1267,1267,1267.
```

The entire return set at index 22 equals the set at index 20; the
index-21 set is distinct. Thus the return sets enter a two-cycle of
cardinality 1,267. There is no extinction in this relaxation, even
after arbitrarily many further gap-one returns.

Two implementations agree on every stable-row integer, every return
count, and the exact repeat indices. The independent implementation
constructs all 4,194,304 width-20 transitions from individual scalar
Rule 30 truth-table entries. Return-set hashes and the complete
1,288-row stable set are retained in the two
`cumulative-family-gap1-strip*.json` artifacts.

The previous family's width-20 failed-return argument therefore does
not automatically transfer to this excursion. A larger spatial depth,
repeated-excursion analysis, or a different invariant remains possible.
A nonempty relaxed return image establishes no full realization and
does not by itself establish an infinite path with repeated excursions.

## 5. Rule 90 and honest scope

The width-8 Rule 90 version has all 128 odd rows in its gap-one stable
set and all 128 rows after the excursion and every return. Unchanged
`controls.rule90_control` also passes at `T=2,4,6,8,10`. The certified
Rule 30 forbidden factors are not imposed as if they held for Rule 90;
their OR-specific cone proofs are the source of the nonlinear
restriction.

The recurrent SCC contains all known periodic regimes and still has
217 branching vertices. Excluding the single displayed family would
not eliminate that entire component. The exact unresolved component
obligation is to exclude every infinite observable-branching path by
a sound right-extension argument, or to realize one such path. The
finite graph overapproximates realizability and supplies neither
conclusion on its own.

This work does not predict a neighbour from bounded centre history.
It tests a necessary language of a fully specified alternating centre,
with every imported normalization onset stated above. The graph and
strip calculations are exact finite certificate/criterion evaluations,
not a census used as an asymptotic proof.

## 6. Reproduction

From the repository root:

```sh
uv run python experiments/rule30/r1-isolated-column/cumulative_factor_graph.py
uv run python experiments/rule30/r1-isolated-column/verify_cumulative_family_strip.py
```

Both commands verify saved outputs without changing frozen inputs.
The graph script's `--write` flag creates its output on a first run;
the strip verifier's `--write` creates its independent verification
artifact. R1 and P1 remain open at this intermediate step.

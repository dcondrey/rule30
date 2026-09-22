# Axis-first canonical CNF

Date: 2026-09-09. Evidence **U/C**; this only changes representations.
It does not prove or kill R1.

`direct_dfa_axis_canonical.add_axis_canonical(synth)` returns fresh
clauses and sets `synth.axis_size_selectors[R]`. Construct the existing
`LeanSynthesis` with `symmetry=False`; the helper replaces the previous
whole-alphabet discovery convention. It rejects installation when the
complete old naming family is already present.

For the selected `R`, the helper imposes exactly:

1. Sources below `R` have axis-symbol `0,2` targets below `R`.
2. Every state `v` in `1,...,R-1` has an incoming axis edge from a source
   below `v`.
3. Each first appearance of target `v>=2` is preceded by an appearance
   of target `v-1` in the flattened first-`R` axis rows.

One-hot `R` selectors choose exactly one size. The first two conditions
make the axis-reachable set exactly `0,...,R-1`; the third fixes its
breadth-first discovery names. Rows at states `q>=R` remain free.
Simultaneously permuting all transitions and all output tables preserves
every represented cell value.

The existing N5 lean parameter base has 385 variables and 223 clauses
without the old naming convention. The new helper adds five variables
and 113 clauses, giving 390 variables and 336 clauses before ground
gates or composed-output conditions are installed.

The regression exhausts every padded binary axis table through three
states, checking every possible `R` against an independent queue-based
discovery traversal:

| Core states | Labelled axis tables | All size checks | Accepted with R=1,2,3 |
|---:|---:|---:|---|
| 1 | 1 | 1 | 1 |
| 2 | 8 | 16 | 4,4 |
| 3 | 243 | 729 | 81,36,45 |

Every table is also renamed to an accepted representation. Across all
tables, 21,420 paired-digit words of length at most three preserve
their complete state trajectory under the permutation. These finite
checks calibrate the symbolic renaming argument; they are not its
all-length proof. The existing Rule 90 model survives the renaming,
passes its exact full-diagram gate check, and agrees on 1,024 explicit
coordinates.

Independent audit also passes every complete four-symbol padded core
through three states, including all 177,147 N3 transition tables and
531,441 size-selector SAT queries. It checks every table has a valid
renaming, the selected size is unique, odd-symbol transitions remain
unconstrained, and 2,834,352 renamed transition entries obey conjugacy.
The independent Rule 90 check covers 4,096 coordinates and its exact
gate closure. These results are in `direct-dfa-axis-naming-independent.json`.

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_axis_canonical.py
```

The result is `direct-dfa-axis-canonical-regression.json`. Repeating the
command compares against the saved result without replacing it. No new
synthesis run was launched by this module. The complete catalog and
its guard semantics are specified in
`docs/rule30/RESULTS-r1-canonical-axis-partition.md`.

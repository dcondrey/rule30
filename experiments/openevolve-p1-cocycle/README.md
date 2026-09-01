# OpenEvolve P1 cocycle potential search

This experiment uses OpenEvolve as a conjecture generator for the exact
period-two defect/restart cocycle.  It does **not** evolve finite Rule 30
seeds and it runs no SAT instances.

The proved primary component is the principal survivor rank.  The evolved
function proposes a secondary nonnegative tuple `D(F)`.  It is tested on the
exact rank-preserving transitions where a lexicographic measure

```text
(principal_rank(P), D(F))
```

would otherwise stall.  The candidate grammar excludes offsets, widths,
lookup tables, negative constants, subtraction, branches, and loops.

The generated `cocycle_features.json` is a finite discovery suite, not a
proof.  Even a perfect candidate must be translated back into a uniform
Boolean-ring inequality before it has mathematical force.

The first finite-perfect expression is retained in `candidate_lex2.py` as a
negative control.  It passed all ten plateau edges through width 15 and was
then falsified by the external width-18 edge recorded in
`cocycle_features_n18.json`.

Run the eight-iteration smoke search with:

```bash
./run_smoke.sh
```

After inspecting that calibration run, launch the 24-iteration discovery
search with:

```bash
./run_search.sh
```

# OpenEvolve search for a P1 cocycle delay potential

Date: 2026-09-01

Status: **HARNESS VALIDATED AND SEARCH RUN.  THE BEST OPENEVOLVE PROGRAM
ORDERS 8 OF 10 DISCOVERY PLATEAUS.  A FINITE-PERFECT FOLLOWUP EXPRESSION IS
FALSIFIED BY A NEW WIDTH-18 PLATEAU.  NO UNIFORM RANK OR PERIOD-TWO THEOREM
IS PROVED.**

The experiment is in `experiments/openevolve-p1-cocycle/`.  It used the
vendored OpenEvolve 0.3.2 installation already retained for the P3 experiment.
The eight-iteration smoke run and 24-iteration discovery run made model calls
through the configured OpenRouter endpoint.  Their complete checkpoints,
program databases, metrics and logs are retained under
`openevolve_output_smoke/` and `openevolve_output_search/`.

## 1. Exact target

The defect/restart cocycle has exact state

```text
F_m = (symbolic frontier S_m, previous forced rho, survivor indicator P_m)
```

and the already-proved update

```text
P_(m+1) = P_m K_m,
rank(P_(m+1)) <= rank(P_m).
```

Strict rank descent fails because some `K_m` are absorbed on the survivor
class.  The search target was therefore a nonnegative tuple `D(F)` such that

```text
(rank(P_m), D(F_m)) > (rank(P_(m+1)), D(F_(m+1)))      (1)
```

lexicographically whenever `rank(P_m)>0`.  Rank already handles every strict
rank drop, so the evaluator scores `D` only on exact rank-preserving edges.
If one formula satisfied (1) uniformly in `n,m`, the product order on
`N x N^k` would be well founded and every finite-width survivor chain would
terminate.

This target avoids finite-seed fitness entirely.  The experiment runs no SAT
instances and enumerates no seed assignments.

## 2. Anti-overfitting grammar and exact data

`build_dataset.py` derives every state from
`defect_restart_cocycle.advance`.  It exposes 66 nonnegative algebraic
statistics of the exact current state: ANF term/degree/support statistics for
`P_m`, the previous rho, the pin, obstruction and good-factor polynomials,
plus aggregate statistics of both symbolic frontier rows.  It does not expose
the seed width or macro offset.

Evolved functions may return a tuple of at most four arithmetic expressions.
Imports, loops, branches, comparisons, assignments, lookup tables,
subtraction, negative numbers and large constants are rejected by an AST
gate.  The permitted operations are `+`, `*`, `//`, `%`, `min`, `max` and
`abs` on the recorded nonnegative features.

The initial discovery artifact contains:

| split | widths | rank-preserving edges |
|---|---|---:|
| training | `2,3,5,6,7,8,9,11,13,14` | 3 |
| holdout | `4,10,12,15` | 7 |

The holdout deliberately contains the length-four restart lift and the
length-ten closure collision.  Widths 16 and 17 were generated afterward;
both die after seven macros and contain no plateau, so they are vacuous tests.

## 3. OpenEvolve results

The first smoke prompt failed to list the available feature vocabulary.  Its
eight proposals merely recombined `factor_terms`; four also violated the
grammar.  The seed remained best, at `0/3` training and `2/7` holdout edges.
This was treated as a harness defect, not a negative mathematical result.

After adding the exact feature families and failed-edge directions to the
feedback, the 24-iteration search improved on its first two proposals.  Its
best retained function is

```python
return (
    state["obstruction_terms"],
    state["frontier_b_terms"],
    state["factor_terms"],
)
```

It passes all three training edges, five of seven holdout edges, and the
restart control.  It fails:

```text
n=4,  offset 3: (0,18,3)  -> (0,27,3)
n=10, offset 7: (15,695,18) -> (26,715,31).
```

The second failure is inside the recorded closure-collision chain.  A separate
archive member crosses that collision but passes only one of three training
and three of seven holdout edges.  The failures of the two candidates are
true reversals, so concatenating their tuples does not repair them.

## 4. Finite-perfect conjecture and external falsifier

`expression_census.py` then enumerated the same short-expression grammar
deterministically.  On the original ten edges it found

```text
D(F) = (
  max(obstruction_span, previous_rho_quadratic),
  pin_weight mod 9
).                                                       (2)
```

Equation (2) passed all ten edges, including both controls.  It is retained
as `candidate_lex2.py`, explicitly as a falsified overfitting control.

The next nonvacuous exact width is 18.  Its symbolic chain took about 111
seconds to construct and contains

```text
n=18, offset 7: rank partition [5,5,0].
```

The first coordinate of (2) ties at 22.  Although the raw pin weight decreases
from 4214 to 4129, its residue wraps upward:

```text
(22, 4214 mod 9) = (22,2)
(22, 4129 mod 9) = (22,7).
```

Thus (2) reverses on the first new plateau and is false.
`cocycle_features_n18.json` records the complete exact external chain and is
loaded by all future evaluations.

After adding this edge, the unrestricted census again obtains a finite-perfect
pair only by using a residue:

```text
(
  max(obstruction_span, pin_quadratic),
  obstruction_terms mod 12
).
```

When `%` is disabled, none of the 17,147 enumerated raw, quotient, pairwise
sum/product/min/max, or small positive weighted expressions forms a one- or
two-component lexicographic separator for all eleven edges.

## 5. Consequence

OpenEvolve is operational on the exact P1 cocycle and can find meaningful
partial summaries quickly.  The run also demonstrates the central danger of
a finite evaluator: phase residues manufacture perfect rankings until a later
plateau wraps them.  A perfect finite fitness value is therefore not evidence
of a well-founded invariant unless each operation has a uniform symbolic
monotonicity argument.

The useful negative result is narrower:

> No one- or two-component expression in the recorded 17,147-expression
> nonmodular grammar orders all eleven exact rank plateaus through width 18.

This is a finite grammar exclusion, not a Rule 30 theorem.  A defensible next
evolution must mutate proof templates or locally checkable recurrence
identities, not arbitrary numerical feature expressions.  In particular,
modular coordinates should be excluded unless the candidate simultaneously
supplies an invariant range that proves wraparound impossible.

## 6. Reproduction

From the repository root:

```bash
cd 13-rule30/experiments/openevolve-p1-cocycle
./run_smoke.sh
./run_search.sh
python3 expression_census.py
python3 expression_census.py --no-mod
```

Those launchers now include the stored width-18 external edge.  The preserved
2026-09-01 checkpoints are the authoritative original runs.  To reconstruct
the original ten-edge evaluator rather than start the strengthened search,
set `RULE30_P1_INCLUDE_EXTERNAL=0`.

Regenerating the expensive external holdout is optional:

```bash
python3 build_dataset.py \
  --external-width 18 \
  --output cocycle_features_n18.json
```

The stored OpenEvolve runs and external JSON make routine re-evaluation
instant; regeneration is needed only to audit the symbolic source chain.

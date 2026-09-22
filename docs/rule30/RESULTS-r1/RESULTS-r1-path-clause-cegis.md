# Deterministic path clauses for automatic-diagram synthesis

Date: 2026-09-09. Evidence: **U** (sound refinement rule), **C**
(independent clause replay), **M** (one capped performance comparison).
This is an intermediate implementation improvement. R1 and P1 remain
open; the run below ended UNKNOWN.

## 1. The class and the unchanged final test

The comparison uses the same complete five-state MSB automatic-diagram
predicate as the existing direct synthesis run: temporal clock length
4, spatial output-label clock length 14, canonical state numbering,
a nonzero Rule 30 centre clock, and the proved complete 111-bit
aperiodicity witness encoding. Both runs start with the same centre
constraints at times 1 through 7, the same 224 actual local gates, and
the same 1,108 previously collected actual-coordinate constraints.

Every proposed model still goes through unchanged `check_centre` and
`check_gates`, which examine their exact finite all-coordinate product
closures. A candidate is accepted only if these closures validate the
whole right half-plane and its exact automatic aperiodicity witness
also checks. Changing the refinement encoding does not replace that
final test with a sample of coordinates.

## 2. A single clause replaces a ground unrolling

For a failed local gate, evaluate the candidate's four MSB coordinate
paths at `(t,x-1)`, `(t,x)`, `(t,x+1)`, and `(t+1,x)`. Each path starts
at root state zero. Record every selected transition variable and the
signed output-assignment literal at its final state. Under the one-hot
transition constraints, the conjunction of those literals forces the
same four coordinate outputs in any later candidate. If the outputs
violate the frozen Rule 30 truth table, negate the conjunction and add
that single clause.

**U:** every actual diagram in the specified automaton class satisfies
this clause. Deterministic path induction proves the implication, and
the final four-bit contradiction is checked against the unchanged
ladder `FWD`. A centre failure is handled the same way, with its
required clock-assignment literal included.

There are at most `4N` distinct selected transition variables in a
candidate core, regardless of coordinate magnitude. A full four-site
gate cut consequently has at most `4N+4` literals. No ground-state or
ground-output variables are introduced for the new cut.

The implementation safely strengthens the cut by deleting unnecessary
output-site assignments. It tests deletion against all eight ordinary
valid truth-table rows, without making assumptions about aliases
between candidate output variables. It then keeps paths only for the
remaining sites. Because no alias relation was used, changing an
unguarded discarded path cannot invalidate the implication. All four
original paths are nevertheless retained in the artifact for replay.

## 3. The 180-second comparison

| Quantity | Existing ground constraints | Path clauses |
|---|---:|---:|
| Initial variables | 19,396 | 19,396 |
| Initial clauses | 233,140 | 233,140 |
| Candidate models examined | 2 | 13 |
| New failed-coordinate refinements | 33 | 196 |
| Final variables | 19,902 | 19,396 |
| Final clauses | 239,404 | 233,336 |
| Elapsed seconds | 180.31 | 180.17 |
| Outcome | UNKNOWN | UNKNOWN |

The first path-backend candidate appeared at 123.26 seconds. Ten
candidates had been processed by 164.80 seconds. The initial solve
therefore consumed most of the budget; subsequent path refinements
were substantially cheaper in this run. The largest saved clause
has 18 literals, including at most 14 distinct transition literals.

This is one performance comparison, not a parameter census or a
controlled statistical benchmark. The cut strengths differ: one full
coordinate equation excludes every invalid assignment at that
coordinate, whereas one path clause excludes its certified implication
cube. Raw cut counts are not equal measures of eliminated models.
The path run also retained native proof logging so an eventual UNSAT
answer could be checked without rerunning the search. Neither capped
UNKNOWN answer is evidence that the class is empty.

## 4. Independent replay and Rule 90

The independent verifier does not call the producer's path extractor,
cube minimizer, or clause constructor. It rebuilds the base formula,
checks the imported source hash, reconstructs paths from the integer
coordinates, validates their signed variable assignments, checks each
remaining output cube against frozen `FWD`, and reconstructs every
clause and the final CNF.

The completed replay checks:

| Item | Count |
|---|---:|
| Exact candidate aperiodicity inequalities | 13 |
| Imported actual-coordinate constraints | 1,108 |
| Path clauses | 196 |
| Coordinate paths | 781 |
| Individual transition steps | 5,468 |
| Ordinary truth-table row checks | 1,560 |

All checks pass. Among the eight invalid Rule 30 output quadruples,
the ordinary cube minimizer retains three sites in six cases and all
four sites in two cases. For Rule 90 it retains three sites in all
eight cases and always discards the irrelevant centre input. Unchanged
`controls.rule90_control(6)` passes at periods 2, 4, and 6.

The implication method is generic and can refine either rule; the
different ordinary truth tables supply the required nonlinear content.
An UNSAT result would require both this clause replay and an accepted
DRUP proof against the final CNF. The current run has no UNSAT result
and claims no proof artifact of one.

## 5. Artifacts and reproduction

Producer:
`experiments/rule30/r1-zero-set-attack/construction/direct_dfa_path_cegis.py`.
It imports the existing synthesis predicate and exact coordinate
checker read-only. Run artifact:
`direct-dfa-path-R30-N5-T4-q14-complete111.json` in the same directory.
The baseline is
`direct-dfa-R30-N5-T4-q14-msb-complete111-canonical.json`.

Independent verification:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_direct_dfa_path.py experiments/rule30/r1-zero-set-attack/construction/direct-dfa-path-R30-N5-T4-q14-complete111.json
```

Its saved result is
`direct-dfa-path-R30-N5-T4-q14-complete111-independent-check.json`.
To make a separate fresh performance run, use a new output filename:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_path_cegis.py --seconds 180 --batch 32 --import-base experiments/rule30/r1-zero-set-attack/construction/direct-dfa-R30-N5-T4-q14-bits88-batch32.json --output direct-dfa-path-R30-N5-T4-q14-repeat.json
```

No frozen engine or terminal-period machinery was edited. No full
Rule 30 counterdiagram was found in this run.

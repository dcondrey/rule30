# Binary automatic construction with unrestricted eventual centre period

The first broader binary run is **M / UNKNOWN**, not an R1 proof or
counterdiagram. It used 180.008860 seconds of solver time and saved 7,190
parameter models and 190,251 new necessary Rule 30 gate clauses. Every
model passed the exact eventual-centre/aperiodic-masked-neighbour predicate;
each then failed an actual Rule 30 gate. The five-state class remains live.

## Exact class and mechanism

The class consists of padded five-state binary MSB coordinate automata,
with an output lookup depending additionally on `t mod 4` and `x mod 14`.
The number four is a lookup phase count, **not a prescribed centre period**.
The centre may have any eventual period represented by the automaton.
There is no condition on its early values. The right half-plane extends
uniquely to a full Rule 30 diagram using left permutivity if every local
gate succeeds.

The uniform predicate is proved in
`docs/rule30/RESULTS-r1-automatic-full-predicate.md`. For a reachable
time-axis core of size `R`, use `H=2^R` and
`P=2^R*lcm(1,...,R)`. Exact endpoint pairs compare all coarse times
`n,n+P`, `n>=H`. The composed centre labels must agree on every pair;
at least one pair must have both centre labels zero and distinct
neighbour labels. This is equivalent to eventual periodicity of the
centre and aperiodicity of `(1-centre)*neighbour`. A successful model has
a safe centre onset `4H` and period dividing `4P`; no minimal-period
claim is made.

Axis-first naming replaces the old whole-alphabet naming. There are
exactly 21,091 canonical reachable axes through five states, with counts
`1,4,45,816,20225`. Every one is constrained before solving. Per-phase
spanning forests express both centre equality and the zero-centre
neighbour inequality exactly. This is a finite complete predicate for
this automatic class, not a finite-window predictor from centre history.

The mechanism's success condition is full all-coordinate Rule 30 closure
of a model satisfying that predicate. Its finite-class kill condition is
UNSAT with a checked proof of the exact final CNF. A time cap establishes
neither condition.

## Input reuse and measured outcome

The new base has 2,069 variables and 439,246 clauses: 224 ordinary seed
gate equations, the axis naming clauses, exact composed outputs, and all
catalogue predicates. There are no clock variables or early centre
equations. From the independently audited shared checkpoint, the importer
regenerated 728,441 ordinary gate cuts exactly, using only the preserved
transition/output variable IDs. It discarded 2,379 centre cuts and all
162,590 old observation cuts. No old clock constraint survives.

The imported base has 1,167,339 clauses. The final pool has 1,357,337
clauses and the same 2,069 variables. One CaDiCaL195 solver was retained
through 7,190 conflict-budget calls, with 219,129 conflicts. All 190,251
new gate paths and their forcing truth-table cubes were replayed before
saving. Independent replay subsequently passed in
`direct-dfa-general-R30-N5-T4-q14-cadical180-independent-check.json`:
7,190 models, 118,954 endpoint pairs, 475,816 centre equalities,
1,610,560 seed gates, 190,251 new cuts, 761,004 paths, and 4,077,791
path steps. The rebuilt final CNF SHA-256 is
`a7a4b4dc6c2241bd4e018f5247a11fe20a174fbfab564d70c951dba7528c5f82`.

The artifact is
`direct-dfa-general-R30-N5-T4-q14-cadical180.json.gz`, compressed SHA-256
`ef30c3465f7126a5af91012a33111fb1301036a41f96e5c30199dd61cb9aceea`.
Its canonical uncompressed JSON hash is
`ec658c44c45242c7468f821fb63cd1c16eb5e38cc81dbd111a65086e6a9c7134`.
The complete earlier gate source remains a hash-identified provenance
dependency; its large arrays are not duplicated in this artifact.

Of the 7,190 candidates, 366 have an eventually zero centre and 6,824
have a nonconstant eventual centre. Reachable axis sizes are two for 28
models, three for 577, four for 1,273, and five for 5,312. These are
diagnostics of failed parameter models, not realised Rule 30 diagrams.

## Checks and Rule 90 control

The complete two-state, two-phase, two-spatial-class comparison covers
all 32,768 parameter assignments: the independent MSB classifier and SAT
predicate agree, accepting 720. A four-phase comparison checks another
32,768 assignments, accepting 622. The latter samples output labels
deterministically and is not called exhaustive.

The full 21,091-record predicate accepts the actual five-state Rule 90
lone-seed model after renaming. Its exact masked-neighbour witness is at
times 127 and 319, with centre values zero and neighbour values one and
zero. The full coordinate gate closure and 16,384 scalar forward cell
checks pass. The Rule 90 control is therefore preserved by the automatic
predicate; the Rule 30 OR gates supply the rule-specific constraint.

Independent catalogue checking covers all endpoint relations, all 366,953
saved endpoint witnesses, and every pre-final pair record. Independent
axis-naming SAT checks cover all 177,147 labelled three-state four-symbol
cores and all three size selectors. Every accepted core has a unique
reachable size and every core has a valid renaming. Forest equivalence
has exhaustive graph/label checks through five vertices.

```
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_general_observation.py
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_axis_naming_independent.py
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_canonical_axis_catalog.py
uv run --with python-sat --with ijson python experiments/rule30/r1-zero-set-attack/construction/verify_general_gate_import.py
uv run --with ijson python experiments/rule30/r1-zero-set-attack/construction/verify_general_result_independent.py
uv run --with python-sat --with ijson python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_general_cadical.py --gate-source experiments/rule30/r1-zero-set-attack/construction/direct-dfa-lean-path-R30-N5-T4-q14-shared-900.json.gz --seconds 180 --conflict-chunk 2000 --output direct-dfa-general-R30-N5-T4-q14-cadical180.json.gz
```

Use a fresh output filename when repeating the solve. The outcome remains
an unfinished construction search. It establishes neither R1 nor P1 and
does not exclude larger automata or other lookup phase counts.

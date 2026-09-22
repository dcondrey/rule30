# Memory-two temporal pair graphs: two certified exclusions

Date: 2026-09-09. Evidence: `C` for the stated finite certificate classes,
`U/R` for their exact extension semantics. This does not prove or kill R1.

The intended mechanism was a right-surjective temporal-pair language with
two closed walks sharing a starting vertex and having different sampled
neighbour words. Arbitrary concatenation of the walks would encode an
aperiodic selector. Exact right-surjectivity would then extend each
adjacent-column path to the right repeatedly; left permutivity completes
the diagram on the left. The kill condition for a proposed graph is a
finite source path with no right lift.

Here a temporal symbol is `(L_t,M_t)`, encoded `2L_t+M_t`. A graph vertex
remembers two consecutive symbols. An edge `E_p(a,b,c)` records an
overlapping triple, with time phase `p mod 2`. Both constituent source
updates must admit a right input according to Rule 30. There are exactly
72 possible phase-labelled edges. Enabled edges must have successors.

Two cyclic words have centre `01`, equal lengths `B`, and the same first
two neighbour bits, so they start at the same graph vertex. Their even
neighbour samples must differ somewhere. These are finite cycle conditions,
not assumed realizability of arbitrary switching between known tori.

For exact right-surjectivity, a subset state retains the source vertex,
time phase, and all possible pairs of current/next right bits. There are at
most `2*12*15=360` nonempty states. Every source edge filters both local
updates and the target triple. An empty subset supplies a finite unliftable
path. Absence of empty subsets gives a lift for every finite source prefix;
the finitely branching tree of lifts has an infinite path by compactness.
This argument uses no online or memoryless choice of right extension.

Each counterexample adds a conditional existential finite-lift constraint:
if all its source edges remain selected, fresh right bits must satisfy all
source updates and all target edges. This is necessary for every genuinely
right-surjective graph. Consequently a verified UNSAT result after these
refinements soundly excludes the specified graph/cycle class.

| B | Refinements | Final variables | Final clauses | Result |
|---:|---:|---:|---:|---|
| 6 | 28 | 174 | 474 | UNSAT, DRUP checked |
| 10 | 23 | 167 | 483 | UNSAT, DRUP checked |

The limits were 60 seconds and 1,000 refinements per run. Neither limit was
reached. All counterexamples have three or four source symbols. Exact
paths and the candidate graph that each refutes are retained in the JSON
reports. The smallest recorded example is phase zero, symbols `0,2,0`;
its meaning depends on the stored candidate graph, so it is not a universal
Rule 30 forbidden path.

Independent replay checked all 256 and 200 possible right-bit assignments
across the respective stored cuts. With source edges enabled, the actual
CNF simplifies to exactly the frozen Rule 30 equations and required target
edge units for every assignment. This checks the cut semantics for every
remaining graph assignment. It also reconstructs both final CNFs exactly,
verifies their hashes and DRUP proofs, and rechecks graph inclusion with
explicit sets of right-bit pairs rather than bit masks.

**Rule 90 control (`U/C`).** The full graph has 128 edges and passes exact
inclusion with 64 reached subset states. Any temporal pair has the right
extension `N_t=L_t XOR M_(t+1)`. The two centre-`01` neighbour cycles
`000000` and `001000` share their first two symbols and differ on the zero
set. Thus this construction mechanism admits the expected Rule 90
counterdiagram; it does not incorrectly prove R1 for Rule 90.

Reproduction, from the repository root:

```sh
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/memory2_pair_extension.py --rule90-control
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/memory2_pair_extension.py --length 6 --seconds 60 --iterations 1000
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/memory2_pair_extension.py --length 10 --seconds 60 --iterations 1000
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_memory2_pair_extension.py
```

The proof checker is the family-seam audit's DRAT-trim, located by
`experiments/rule30/r1-isolated-column/drat_trim.py` (`$RULE30_DRAT_TRIM`,
then `/tmp/rule30-family-seam-drat-trim/drat-trim`, then `PATH`; pinned
build recipe in `docs/rule30/RESULTS-family-seam.md`). Frozen `ladder.py` is imported read-only and
its recorded SHA-256 is asserted before every run. No frozen engine changed.

The result excludes only memory-two phase-two temporal pair graphs with
the specified equal-length observable cycle pairs. It does not exclude
other lengths, other temporal memories, spatially typed graphs, or
nonsofic right-surjective languages. An aperiodic full diagram need not
admit a finite graph presentation. No asymptotic inference follows from
these two UNSAT certificates.

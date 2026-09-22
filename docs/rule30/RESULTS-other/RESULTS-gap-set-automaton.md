# The gap-set automaton closes; its recurrent language exceeds the four tori

Date: 2026-09-09. Overnight Task 3.

**The complete width-24 subset graph closes at 15,424 states. It does not
prove the terminal-period theorem.** It does give exact, uniform exclusions
for two specified infinite families. Adding 177 distinct proof-certified
forbidden words still leaves branching recurrent components. Surviving
paths throughout this report are candidates, not Rule 30 realizations.

Artifacts and reproducible programs are in
`experiments/rule30/gap-set-automaton/`. The frozen strip and cone engines
are imported unchanged.

## 1. A sound graph, including arbitrary onsets

Retain columns 1 through W at a time when the alternating centre is zero
and the sampled right bit is one. The initial row universe U is all odd
W-bit rows. Gap g acts by the frozen block relation for `0^g 1`, with both
exterior-bit choices retained at every elementary update. Its image of a
set S is denoted T_g(S).

Every actual right half-plane with that centre trace projects into this
relation. At any one in an eventual gap sequence, its row belongs to U.
Consequently an empty iterate from U excludes that gap continuation at
every sufficiently late onset. Including U is essential: exploration only
from the four known stable regimes would not cover arbitrary realizations.
The exploration also includes those four regimes as regression seeds.

States are exact sorted sets, identified by their complete byte strings;
no approximate hashing or sampled rows identify states. Every discovered
state has all four outgoing transitions computed. Empty images lead to
the dead state. The cap was 100,000 discovered states at each width.

| Width | Nonempty set states | Transitions checked | Maximum discovery depth | Branching recurrent SCC sizes |
|---:|---:|---:|---:|---|
| 20 | 3,209 | 12,836 | 27 | 549, 39 |
| 24 | 15,424 | 61,696 | 38 | 560, 349, 169 |

Both explorations close below the cap. All transitions are replayed using
the independently implemented, frozen scalar truth-table relation, not
only the images encountered near the start. The stored growth curves
record the complete runs. SCCs use every edge, including cross edges.

The stable sets for gaps `(1)`, `(2)`, `(4)`, `(4,1)` have sizes
`1288,670,1021,252` at width 20 and `6321,2045,5923,1585` at width 24.
Their exact sets and convergence counts agree between both implementations.
The unchanged rung-2 Rule 90 control passes. In the strip control, each of
the four gap blocks fixes the entire odd-row universe for Rule 90 at width
8. This tests the forced-trace construction; it makes no automaticity claim
about Rule 90's lone-seed centre.

## 2. Uniform classifications of three cyclic families

The closed graph gives an all-length calculation, rather than a census of
short necklaces. Add an absorbing dead state, so each T_g is a function
on the finite node set. Compute its powers as **whole functions** until
`T_g^(a+p)=T_g^a`. Function composition then proves this identity for every
later exponent. For each remaining exponent class, iterate the composite
`T_g^m T_e` from U to death or repetition. This decides survival of
`(e,g^m)^infinity` for every integer m>=0 in this strip.

| Cyclic gap family | Width-24 classification for all m>=0 | Repeated function: onset a, period p |
|---|---|---|
| `(2,4^m)` | survives at m=0 and every m>=3; excluded at m=1,2 | T_4: 17, 2 |
| `(4,2^m)` | survives only at m=0; excluded for every m>=1 | T_2: 16, 1 |
| `(3,1^m)` | excluded for every m>=0 | T_1: 40, 2 |

These finite function identities and verdicts are in `families.json`.
At width 20 the first two classifications agree; `(3,1^m)` survives only
at m=0. The respective power onsets/periods are `(12,1)`, `(10,1)`, `(25,2)`.

By soundness, **no actual eventually periodic rho can have cyclic gap word
`(4,2^m)` for m>=1 or `(3,1^m)` for m>=0**. The latter does not exclude a
single transient gap 3, nor every periodic word containing gap 3. Conversely,
the survival of `(2,4^m)` for all m>=3 is a uniform limitation of this width,
not a construction of infinitely many Rule 30 traces.

## 3. Unrestricted-cone checks and certified pruning

Each branching SCC contains many return cycles. The program records up to
100 distinct primitive, rotation-normalized representatives at each width.
This catalogue is explicitly **not all cycles** in a branching component.
Every catalogue entry receives an independent unrestricted-cone attempt.

| Width | Catalogue entries | Certified exclusions | Unresolved | Known torus necklaces |
|---:|---:|---:|---:|---:|
| 20 | 100 | 89 | 8 | 3 |
| 24 | 100 | 66 | 30 | 4 |

The width-20 catalogue cap omits one known necklace; the separate exact
regression still checks all four. Counts are per catalogue entry, so entries
at different widths may overlap.

The frozen cone encoder specifies actual Rule 30 updates with the forced
alternating centre, and no artificial finite spatial boundary. For a
candidate's periodic rho word, prefixes of 32, 64 and 128 samples are
queried, stopping at a certified contradiction. Each initial query has a
one-second solver budget. Satisfiable witnesses are replayed with the
unchanged `numeric_rho`; timeout is recorded as unknown. UNSAT results have
CNF and DRUP files independently checked by `drat-trim`. A separate Z3
attempt is recorded, including timeouts; it is not required to agree within
its time limit for the checked DRUP proof to be valid.

There are 155 newly checked exclusions. The stored CNF and proof files are
losslessly gzipped, with compressed and original SHA-256 hashes. All 36
relevant existing cone certificates are also regenerated against the frozen
encoder, hash-checked and proof-checked: 11 finite family-seam cases, its
uniform seam word, and 24 periodic-neighbour cases. Their original files
remain unchanged.

Every certified finite rho word is forbidden at every onset in an actual
trace. To exploit that stronger consequence, `refine.py` intersects the
width-24 graph with an avoidance automaton, retaining matches across gap
boundaries. The 177 distinct certified words reduce to 168 after removing
words that already contain a shorter forbidden word. The avoidance machine
has 8,747 states; its reachable product with the strip closes at 18,739 states
and 74,956 transitions. An independent literal-substring/longest-suffix
implementation verifies every product edge and all-state reachability.

The product retains three branching recurrent SCCs, of sizes
`1172,376,349`, as well as the four known necklaces. Extra states record
forbidden-word history; their number need not decrease when the accepted
language decreases. This combination of existing and new certificates
**still does not establish the terminal-period theorem**. Repeating the
whole-function power calculation on this product gives exactly the same
three all-m classifications and power onsets/periods as the width-24 strip.
In particular, `(2,4^m)` survives for every m>=3 even after all 177 certified
words are forbidden. This is a proved limitation of the combined model.

## 4. A concrete residual family and its limits

The uniform width-24 survivor `(2,4^m)` for m>=3 gives a specific target
beyond a generic appeal to larger strips. Separate, longer-budget cone
runs for m=3 and m=4 use 15 seconds per query at 32, 64, 128 and 256 samples.
Both have replayed SAT witnesses through 64 samples; both are **unknown**
at 128 and 256. The initial rows and exact queries are in
`selected-cones.json`. Finite SAT does not imply infinite realizability.

The corresponding rho periods are `h=3+5m`, hence 18 and 23 in these two
examples. Each cyclic word has one gap 2, so its minimal rho period is h.
In a full alternating-centre diagram the forced left neighbour is rho on
even times and one on odd times; its zeros exclude an odd period, giving
minimal period 2h. For m>=3, h cannot divide 210: it is coprime to 5, and
the only divisor of 42 congruent to 3 modulo 5 is 3. Thus an actual
realization of any such candidate would escape a forced period of 420 for
that neighbour. No such realization, or survival at all R7 ladder depths,
is established here.

## 5. Reproduction and remaining obligation

From the project directory, with NumPy, SciPy, python-sat and z3-solver
available (the current environment uses `uv run --no-project`):

```
python experiments/rule30/gap-set-automaton/explore.py --widths 20 24
python experiments/rule30/gap-set-automaton/verify.py --width 20
python experiments/rule30/gap-set-automaton/verify.py --width 24
python experiments/rule30/gap-set-automaton/cones.py --width 20 --timeout 1 --checker /path/to/drat-trim
python experiments/rule30/gap-set-automaton/cones.py --width 24 --timeout 1 --checker /path/to/drat-trim
python experiments/rule30/gap-set-automaton/prior_certificates.py --checker /path/to/drat-trim
python experiments/rule30/gap-set-automaton/pack.py --widths 20 24
python experiments/rule30/gap-set-automaton/refine.py --width 24 --cones experiments/rule30/gap-set-automaton/prior-cones.json experiments/rule30/gap-set-automaton/cones-w20.json experiments/rule30/gap-set-automaton/cones-w24.json
python experiments/rule30/gap-set-automaton/verify_refinement.py
python experiments/rule30/gap-set-automaton/families.py
python experiments/rule30/gap-set-automaton/verify_artifacts.py
```

Packing verifies an exact round trip and records the new archive hash in
the transition verification manifest. The verifier reads both original
and delta-encoded subset archives. Solver timeouts are machine-dependent;
the archived checked UNSAT proofs carry the exclusion claims.

`verify_artifacts.py` additionally checks the exact initial universes,
reachability from the declared seeds, all four infinite positive-control
paths from U, compressed proof hashes, every stored finite SAT witness,
and graph/manifest provenance. The selected-family cone run is reproduced by
adding `--width 24 --timeout 15 --samples 32 64 128 256 --input
experiments/rule30/gap-set-automaton/selected-family.json --output
experiments/rule30/gap-set-automaton/selected-cones.json` to `cones.py`, along
with the checker path.

The terminal-period theorem needs a sound argument eliminating the extra
recurrent language, or a genuine non-torus realization refuting it. Neither
closure of a permissive strip nor a finite SAT prefix supplies that step.
P1 remains open.

# Exact observation cuts without a witness circuit

Date: 2026-09-09. Evidence: **U** (conditional observable criterion and
shared-selector equivalence), **C** (independent finite closure and
clause replays), **M** (capped search runs). This is an intermediate
construction tool. No Rule 30 counterdiagram or R1 proof is claimed.

## 1. An exact observation condition for each proposed core

The direct MSB bound proved in
`RESULTS-r1-msb-automatic-period-bound.md` permits removal of the long
existential witness circuit from automatic-diagram synthesis. For a
fixed transition core, take its time-axis binary transitions and
compute every endpoint pair

```text
(q(n),q(n+P)), n>=H,
H=2^N, P=2^N*lcm(1,...,N).
```

An exact finite MSB addition product computes this entire relation,
with an actual integer witness for each pair. It depends only on
transitions, not output labels. For each centre-clock phase, fold
each endpoint through the fixed low-coordinate suffix specifying
that phase and spatial coordinate 1. The neighbour on this phase
is aperiodic exactly when some folded endpoint pair has unequal
output labels. This is the proved eventual-period bound, not an
inference from observing a long nonperiodic prefix.

For a centre clock with finitely many zero phases, the masked vector
is aperiodic if and only if at least one of those scalar phase
signals is aperiodic. If all scalar signals were eventually periodic,
the maximum of their onsets and the least common multiple of their
periods would make the vector eventually periodic.

Thus, conditioned on the proposed core transitions, the exact
observation requirement is an OR over eligible phase/output-state
pairs: the phase clock is zero and the two labels differ.

## 2. Why the conditional cuts preserve the construction class

The time-axis reachable state set is closed under symbols with spatial
bit zero. All low suffix symbols before the final spatial bit 1 stay
on this axis. Guarding all four outgoing transitions of its reachable
states therefore fixes the endpoint relation and every folded output
pair, including the final transition that may leave the axis. Negate
those selected transition literals and add the eligible pair selectors
as one disjunction. Selector implications encode the zero clock and
unequal labels.

If all original endpoint pairs are diagonal, every folded pair is
diagonal regardless of the final suffix. Fixing just the two time-axis
transitions per reachable state already excludes that core from the
aperiodic class.

Every accepted automatic counterdiagram satisfies every such cut.
Conversely, for a fixed core the observation condition exactly
characterizes its aperiodic masked output labelings. The finite
all-coordinate Rule 30 and centre checkers remain unchanged; output
aperiodicity alone is never accepted as a diagram.

The lean parameter formula retains the necessary mixed-clock condition
and the same canonical numbering. It initially uses only the 224
actual-coordinate seed gates and seven centre equations. Local failures
are refined with the independently audited deterministic path clauses
from `RESULTS-r1-path-clause-cegis.md`.

For this fixed class the gate checker's full product has at most
`5^4 * 2^3 * 4 * 14 = 280000` states: four automaton states, three
two-valued coordinate differences, and the two output-label residues.
Consequently its configured 500,000-state cap cannot truncate any
candidate gate check in this class. This is an exact state-space bound,
not a claim about the largest coordinate tested by direct simulation.

## 3. First complete-class lean run

The class remains five MSB states, temporal output clock 4, and spatial
output-label clock 14. The previous 111-bit circuit was already complete
for this class; replacing it by the exact observation criterion changes
the encoding, not the intended construction class.

| Quantity | First lean run |
|---|---:|
| Seed variables / clauses | 1,988 / 20,982 |
| Candidate models | 14,095 |
| Necessary path clauses | 47,060 |
| Exact observation refinements | 12,205 |
| Final variables / clauses | 122,042 / 440,394 |
| Search seconds | 180.31 |
| Result | UNKNOWN, time cap |

An independent verifier uses a different endpoint-relation construction,
replays every path without the producer's helpers, and reconstructs the
entire final CNF. It checks 1,163 distinct time-axis tables, 241,032
endpoint pairs, 187,040 coordinate paths, and 877,020 individual
transition steps. All 14,095 candidate observations, all 47,060 path
cuts, and all 12,205 observation cuts pass. Unchanged
`controls.rule90_control(6)` also passes.

The full semantic artifact is compressed without loss:

```text
direct-dfa-lean-path-R30-N5-T4-q14.json.gz
raw JSON bytes: 412733513
gzip bytes:      12783970
raw SHA-256: 86cea9b7e19b88de6f0228c18f7c77fa2e6455c76f0b52ec8f99b94400caeee5
```

The raw file was removed only after independent verification and an
exact decompression-hash check. The `.provenance.json` sidecar retains
both raw and compressed hashes. Every model, path, clause, endpoint
witness, and refinement order remains in the compressed artifact.

## 4. Shared selectors and semantic continuation

All pair selectors have a core-independent meaning:

```text
selector(phase,a,b) => clock(phase)=0 and output(phase,1,a)!=output(phase,1,b).
```

They may therefore be shared across observation cuts. At five states
and four phases there are at most `4*binomial(5,2)=40` selectors.
This sharing is existentially equivalent to separate copies: OR all
eligible copies to obtain a shared assignment; conversely copy the
shared assignment into every occurrence. All implications and guarded
disjunctions remain satisfied. No exclusivity between selectors is
required.

The shared base additionally requires at least one of the 40 selectors.
An aperiodic zero-phase observable must distinguish at least two raw
output states on that phase, so this is a necessary condition. It does
not assert those states are reachable; the exact observation test is
still required.

The continuation rebuilds every prior refinement from its audited
semantic record under the shared variable names, rather than reusing
old selector identifiers. All 47,060 path and 12,205 observation
refinements are retained. With the raw-output necessity condition,
the rebuilt base has only 2,028 variables and 80,353 clauses.

The 180-second shared continuation ended UNKNOWN after 25,571 additional
candidates. Its totals are 39,666 candidates, 173,742 path cuts, and
32,996 observation cuts. The final formula has 2,028 variables and
227,762 clauses. An independent semantic-import and full-clause replay
passes, including 3,935 distinct time-axis tables, 682,399 endpoint
pairs, 691,641 coordinate paths, and 3,280,916 transition steps.
Unchanged Rule 90 controls pass again.

The shared checkpoint is
`direct-dfa-lean-path-R30-N5-T4-q14-shared-resume.json.gz`, with raw
SHA-256
`4b0d3bec497969cb9b2b3ceb8c5d79abb3c7d1eb38088446b7bffbdbd9c2ce39`.
Its raw JSON is 1,301,052,417 bytes, retained losslessly in 37,101,534
compressed bytes. A longer continuation starts from this audited
checkpoint, retaining all refinements and keeping SAT learning within
the longer run. No conclusion follows from a resource cap.

The subsequent single 900-second Glucose process also ended UNKNOWN,
after 900.8199 seconds. It retained SAT learning throughout that run
and examined 148,808 additional candidates. Its cumulative totals are
188,474 candidates, 730,820 path cuts, and 162,590 observation cuts,
with 2,028 variables and 914,165 final clauses. Producer replay checks
all path clauses; their maximum width is 21, including at most 17
distinct transition guards. Independent full semantic replay passes:
13,093 distinct axis tables, 3,474,756 endpoint pairs, 2,916,143
coordinate paths and 14,095,903 transition steps. It rebuilds the
complete final CNF, preserves every semantic import, and reruns the
unchanged Rule 90 controls successfully.

This checkpoint is
`direct-dfa-lean-path-R30-N5-T4-q14-shared-900.json.gz`: 5,845,848,783
raw JSON bytes are retained in 163,362,027 compressed bytes. Its raw
SHA-256 is
`30c54e28324f4690d7c8d3d71678666233cb650d30d2561eb61383e208609d5c`,
and its compressed SHA-256 is
`5ca9a07276238be2320f5d29ff8f5e34906e78eef5fe5bc975adb72626fdef46`.
The complete model/path/observation pool remains available for semantic
continuation. These counts are measurements, not a class exclusion.

## 5. Controls, scope, and reproduction

The endpoint-relation implementation was checked on all 252 labelled
time-axis transition tables with one through three states and a root
leading-zero self-loop. All 1,978 binary output labelings agree with
the independently implemented exact MSB classifier. A Rule 90 control
shows that a conditional observation cut accepts the actual aperiodic
output labels while rejecting constant labels on the same core.
The independent verifier additionally compares complete endpoint-pair
sets, using a different construction, on every one of those 252 tables.

The observation logic is intentionally rule-generic. The actual frozen
Rule 30 truth table enters through the local gate equations and their
path refutations. The method therefore passes Rule 90 as a construction
control and does not purport to prove a rule-generic version of R1.

Sources and artifacts are under
`experiments/rule30/r1-zero-set-attack/construction/`:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_observation.py
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_direct_dfa_lean.py experiments/rule30/r1-zero-set-attack/construction/direct-dfa-lean-path-R30-N5-T4-q14.json.gz
```

The shared semantic continuation is launched with:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_lean_path_cegis.py --seconds 180 --batch 32 --shared-selectors --raw-output-prune --resume experiments/rule30/r1-zero-set-attack/construction/direct-dfa-lean-path-R30-N5-T4-q14.json.gz --output direct-dfa-lean-path-R30-N5-T4-q14-shared-resume.json.gz
```

Use a new output filename for a new search run; existing artifacts are
not overwritten. Any future UNSAT claim requires a checked DRUP proof
against the reconstructed final CNF as well as semantic replay of all
cuts. An UNKNOWN result establishes neither unrealizability nor a
counterdiagram. R1 and P1 remain open at this intermediate stage.

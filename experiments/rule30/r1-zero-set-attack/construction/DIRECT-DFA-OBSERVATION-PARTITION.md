# Exact output-label partitions for the direct automatic construction

Date: 2026-09-09. Evidence `U/R/C`. This is a synthesis mechanism, not an
R1 proof or a realized Rule 30 counterdiagram.

For a fixed `N`-state MSB core, let `d_b(q)=delta_(b,0)(q)` and let `q(n)`
be its state after reading `n` from the root. The root has a leading-zero
self-loop. Use the audited direct-MSB bounds

```text
H=2^N,   P=2^N*lcm(1,...,N).
```

Compute the exact finite relation

```text
E = { (q(n),q(n+P)) : n>=H }.
```

**Output partition lemma (`U`).** An output function `tau` defines an
eventually periodic sequence if and only if `tau(a)=tau(b)` on every
edge `(a,b)` of `E`. Equivalently, such output functions are constant on
each connected component of the undirected equality graph. This is the
direct-MSB period theorem applied simultaneously to every possible output
labeling of the same fixed core. The transition table is fixed in this
statement; it is not inferred from a bounded sequence prefix.

`endpoint_pairs` computes `E` by the exact MSB addition product. It retains
the two core states, a carry into the already read high digits, the digit
position in `P` after an arbitrary common leading-zero prefix, and the
significant length of `n` capped at `N+1`. Terminal carry zero and length
`N+1` mean exactly `n+P` and `n>=H`. Every edge has explicit integer
witnesses, checked by separate scalar core evaluation. The full closure
is regenerated from the transition table; its sorted-state hash is saved.

For the diagram's clock `T=2^a`, fix a residue `r`. Appending the low
coordinate suffix `(r,1)` to a state defines `f_r(q)`. Hence

```text
s(T*n+r,1) = g(r, 1 mod q, f_r(q(n))).
```

The zero-set neighbour is aperiodic exactly when at least one residue has
clock value zero and labels some folded edge `(f_r(a),f_r(b))` differently.
This leaves every output label and the centre clock free. It requires no
prescribed valuation, substitution, or sparse-pulse neighbour word.

## Conditional synthesis constraint

For a proposed core, compute the states reachable on the time axis and
the exact folded-edge list. Condition on that core's four outgoing
transition values at each axis-reachable state. All low suffix digits
before its last digit have spatial bit zero and stay in this set. The
last digit has spatial bit one, and its outgoing transition is fixed by
the same condition. No transition from the final state is needed.

Under this condition, require the exact finite disjunction

```text
some r,a,b:
    centre_clock[r]=0
    AND g(r,1 mod q,f_r(a)) != g(r,1 mod q,f_r(b)).
```

Fresh selectors encode the disjunction with ordinary CNF clauses. If the
condition is false, choosing every selector false makes the refinement
vacuous. If the condition is true, it is precisely the required aperiodic
output-label condition, so the cut preserves every possible countermodel.

The optional shared-selector encoding uses one selector for each
`(phase, unordered output-state pair)` across every observation cut.
Its meaning is always the same: that phase has clock zero and those
two output labels differ. Setting every eligible shared selector true
simultaneously satisfies every guarded disjunction that was satisfiable
with separate selectors. Thus sharing introduces no stronger condition
and bounds selector variables by `T*N*(N-1)/2`, at most 40 for `N=5,T=4`.
The default separate-selector mode is retained for reproducing older runs.
The equivalence has explicit maps in both directions: OR every old copy
to obtain the shared value, and copy a shared value into every old
occurrence. Both maps preserve all eligibility implications and guarded
disjunctions for every primary-variable assignment, uniformly in the
number of cuts.

The shared-mode base constraint additionally requires the OR of all these
eligible pair selectors. This is a necessary condition independent of the
core: an aperiodic zero-clock residue cannot have a constant raw output
lookup. It is not sufficient, because distinct labels might occur only on
unreachable states. `observe` therefore remains the exact test.
`add_raw_output_nonconstant` creates all selectors before refinement;
each later observation cut adds only its one guarded disjunction.

For `N=5,T=4,q=14`, the canonical core has 385 variables and 284 clauses.
The 40 shared selectors and global disjunction give 425 variables and 405
clauses. With the existing seven centre equations and 224 seed gates, the
base has exactly 2,028 variables and 21,103 clauses. Every subsequent
observation or sparse path cut adds no variables. Shared insertion uses
direct clause-membership checks instead of copying the growing full CNF.

If every edge of the unfurled relation `E` is diagonal, no output function
can be aperiodic. In that case only the two time-axis transitions at each
reachable state need to be fixed to exclude the core. The low suffix and
all output labels are irrelevant to this special case.

The implementation is `direct_dfa_observation.py`. `LeanSynthesis` reuses
the parameter table and actual-coordinate CNF methods from
`direct_dfa_synthesis.py`, but omits the 111-bit existential observation
circuit. Its `observe` function returns either an exact aperiodicity
witness or the endpoint relation needed by `add_observation_cut`.
The sparse gate-path backend can use this API independently of how local
Rule 30 constraints are encoded.

## Verification and control

The exact relation criterion agrees with the independently implemented
direct-MSB classifier for all 1,978 output labelings of all 252 padded
transition tables with one through three states (unreachable states are
allowed in this regression). Counts are `2,32,1944` output labelings and
`1,8,243` transition tables at the respective sizes.

The known five-state Rule 90 core has axis-reachable states `{0,2,3}`.
Its addition product has 334 states and 667 transitions and produces
exactly the pairs `(2,2),(2,3),(3,2),(3,3)`. For `T=2`, the two folded
edges are phase zero `(3,4)` and phase one `(0,3)`. The actual Rule 90
labels distinguish the latter. The witness `n=63`, `H=32`, `P=1920`
gives actual times 127 and 3967, with neighbour values one and zero.

Changing all output labels to zero makes the observable eventually
periodic. The generated conditional cut rejects those labels for the
same core and accepts the original Rule 90 labels. This control uses
115 variables and 290 clauses. The unchanged frozen Rule 90 dynamics
and exact five-state source model remain the positive control; the
generic automaticity theorem is not being used as a Rule 30 argument.

Reproduce:

```sh
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_observation.py
```

The resulting `direct-dfa-observation-regression.json` retains exact
endpoint witnesses, closure hash, folded edges, counts and control result.
No bound on the number of synthesis iterations is inferred from these
regressions. A successful construction still requires independent full
Rule 30 gate closure and centre-clock verification.

The separate/shared equivalence has additional exhaustive finite replay:
43,008 primary assignments over 69 families of three simultaneous cuts,
including both explicit assignment maps on all 13,248 satisfiable cases.
The raw-output condition matches its direct Boolean meaning on all 256
assignments of a small instance. One hundred actual observation cuts
match an independent slow clause-construction reference exactly, including
fresh-clause lists and variable numbering. The actual Rule 90 core remains
SAT with the raw-output prerequisite, with the same times 127 and 3967
distinguished above. These are finite checks supporting the uniform
assignment-map argument, not an inference from tested sizes.

```sh
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_shared_observation_selectors.py
```

Exact counts and the example separating raw nonconstancy from actual
aperiodicity are in `direct-dfa-shared-selector-equivalence.json`.

## Recorded persistent CaDiCaL portfolio

The 900-second continuation of the independently audited shared checkpoint
remained **M / UNKNOWN**. It retained one CaDiCaL195 solver across 118,103
budgeted calls, with 156,999 conflicts. The final pool has 2,028 variables
and 438,558 clauses, with 157,769 saved parameter models, 269,881 exact
path cuts, and 147,680 observation cuts. Relative to the shared checkpoint,
114,684 new models failed the exact observation criterion and 3,419
reached the centre/gate check. All 269,881 path cuts were replayed against
their deterministic coordinate paths and the Boolean truth table before
saving. This does not exclude the five-state class.

```
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_lean_cadical.py --resume experiments/rule30/r1-zero-set-attack/construction/direct-dfa-lean-path-R30-N5-T4-q14-shared-resume.json.gz --seconds 900 --conflict-chunk 2000 --output direct-dfa-lean-path-R30-N5-T4-q14-shared-cadical900.json.gz
```

The saved artifact's compressed SHA-256 is
`3b68b193cb1d533bfb98757f1e4c163260bc5967d1d7936d17ef85e87218ac5d`;
the canonical uncompressed JSON hash is
`4ee37dc5f4fb1cb2b8676921b5d55be2899735b9b2b974b5c0e6464229357279`.
The command above requires a fresh output path when repeating a run.

The measured repeated-axis bottleneck motivates the independently checked
symbolic composition described in `DIRECT-DFA-COMPOSED-OBSERVATION.md`.
That formulation represents the final spatial transition symbolically
and needs only the time-axis core as a guard. It is a change of exact
encoding, with no new mathematical assumption about Rule 30.

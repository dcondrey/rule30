# Exact observation clauses with only time-axis guards

Evidence: **U**, conditional on the independently proved direct MSB
period bound; **C** for the finite implementation checks; **M** for solver
bottleneck counts. This changes the encoding of the existing automatic
candidate class. It does not prove R1 or produce a Rule 30 counterdiagram.

Let the coordinate DFA have transition function `delta` and output lookup
`g[p][s][q]`, with time clock `T=2^a`. The neighbour residue subsequence is
`u_p(n)=s(T*n+p,1)`. Its upper binary digits use only the time-axis
transitions `delta(q,0)` and `delta(q,2)`. Its final `a` digits have spatial
bit zero except in the last digit. Define, once for all candidate cores,

```
V[p,q] = g[p][1 mod spatial][delta(q,2*(p mod 2)+1)].
```

The SAT encoding uses two conditional equivalence clauses for every
possible target of this one-hot transition. Thus `V` has exactly the
stated value for every primary assignment. It is not a relaxation.

Fix a proposed time-axis core on its reachable states. Its exact MSB
addition closure gives all endpoint pairs `(q(n),q(n+P))`, `n>=H`, where
`H=2^N` and `P=2^N*lcm(1,...,N)`. Propagate each pair through the upper
`a-1` suffix bits of phase `p`, leaving the final spatial-one transition
unevaluated. Call the resulting pair `(q,r)`. The residue is aperiodic if
and only if at least one such pair satisfies `V[p,q] != V[p,r]`.

Consequently the zero-set observation condition is exactly

```
OR over p and pre-final pairs (q,r): clock[p]=0 AND V[p,q]!=V[p,r].
```

Guard this condition only by the proposed time-axis transitions. These
transitions preserve both the reachable axis set and every pre-final pair.
The odd-symbol transitions remain arbitrary: their entire effect is
already represented by `V`. This proves the guarded condition necessary
for every genuine aperiodic observation and sufficient for aperiodicity
whenever its guard holds. Global implication-only pair selectors are
sound by setting every eligible selector true simultaneously.

For `N=5,T=4`, the composition requires 20 value variables, 40 pair
selectors, and 321 clauses, all allocated once. Each later observation
refinement adds at most one clause and no variables. With the existing
2,028-variable shared-selector checkpoint preserved, this gives 2,088
variables. Old observation clauses may remain: they are independently
necessary conditions. Neither a solver timeout nor a finite collection
of failed candidate cores excludes the whole five-state class.

## Implementation checks

`verify_composed_observation.py` exhausts every padded two-state,
two-phase core and every clock/output assignment. The independent direct
MSB classifier and SAT encoding agree on all 8,192 assignments across
128 cores: 480 aperiodic assignments accepted, 7,712 periodic assignments
rejected. Every accepted model also has its composed-value variables
checked by direct lookup.

A separate deterministic four-phase regression changes the unguarded odd
transitions and all clock/output labels for 4,096 three-state assignments
over 64 reference axes. All agree with the independent MSB classifier;
897 are aperiodic and accepted. This exercises the upper suffix digit
that is absent from the exhaustive two-phase comparison.

The actual five-state Rule 90 diagram passes the composed clauses, full
coordinate gate closure, centre closure, and 16,384 scalar forward cell
checks. The exact aperiodicity witness compares neighbour times 127 and
3,967, corresponding to coarse `n=63`, `H=32`, `P=1920`. Giving the same
core constant output labels is rejected. Thus the mechanism continues to
accept the required Rule 90 control; only the Rule 30 local-gate clauses
can rule out that analogue.

```
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_composed_observation.py
```

## Measured reason for changing the encoding

Streaming the audited shared checkpoint found 39,666 parameter models:
6,670 passed the observation test and 32,996 failed it. Those 32,996 old
observation cuts have distinct full guards but only 2,714 distinct guarded
time-axis tables. This is a finite diagnostic of repeated irrelevant
spatial-transition choices, not evidence that all five-state cores fail.

An intermediate phase-sensitive guard passed 1,230,848 exhaustive changed
core/label checks but is superseded by the exact symbolic composition.
Its artifacts are retained; no running solver was modified mid-run.

```
uv run --with ijson python experiments/rule30/r1-zero-set-attack/construction/diagnose_observation_guards.py experiments/rule30/r1-zero-set-attack/construction/direct-dfa-lean-path-R30-N5-T4-q14-shared-resume.json.gz --output experiments/rule30/r1-zero-set-attack/construction/direct-dfa-observation-guard-diagnostic.json
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_phase_sensitive_observation.py
```

The intended 180-second composed baseline did not reach the solver. An
import assertion incorrectly required an already-present all-diagonal
clause to be fresh. That bookkeeping case is fixed and explicitly covered
by `verify_composed_checkpoint_import.py`. Before restart, the run was
superseded by the complete automatic predicate allowing any eventual
centre period. `direct-dfa-composed-baseline-not-run.json` records this
without a SAT/UNSAT claim.

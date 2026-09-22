# The ternary three-state centre obstruction

Date: 2026-09-09. Evidence: **U** (exact predicate reduction), **C**
(independently reconstructed CNF and checked DRUP), **K** (the specified
automatic construction class is excluded). **R1 and P1 remain open.**

No padded three-state, base-three paired-digit automaton with output
lookup periods three in time and seven in space can describe a Rule 30
right half-diagram whose centre is eventually periodic and whose right
neighbour is aperiodic on the centre-zero set. The centre's eventual
period and onset are unrestricted inputs to this statement; bounds on
them follow from the finite automaton theorem.

## 1. Exact class

An unknown three-state DFA reads paired ternary digits of `(t,x)` from
most significant to least significant, with a leading-`(0,0)` self-loop
at its initial state. Its output is

```text
s(t,x) = g[t mod 3][x mod 7][DFA_state(t,x)],   t,x>=0.
```

All transitions and binary lookup entries are free. All Rule 30 gates
at `t>=0,x>=1` must hold. There is no centre clock variable, no prescribed
centre word, and no centre equality imposed at any early time. The
whole-alphabet state naming convention preserves representations by
renaming reachable states and normalizing unused rows.

The right half-diagram would extend uniquely to the left by the inverse
Rule 30 relation. Infinite initial support is allowed. The conclusion
therefore excludes this complete automatic ansatz for a generic diagram
counterexample, rather than only excluding lone-seed or finite-support
inputs.

## 2. Uniform exact observation predicate

Let `A(q,d)=delta(q,3d)` be the time-axis table. For each phase `p`, define
two output labellings on its three states:

```text
C[p,q] = g[p][0][delta(q,3p)],
R[p,q] = g[p][1][delta(q,3p+1)].
```

They are respectively the centre and right-neighbour values at time
`3n+p` after the axis has read `n`. The final paired digits are exactly
`(p,0)` and `(p,1)`.

The [arbitrary-radix automatic-period theorem](RESULTS-r1-radix-automatic-period-bound.md)
gives the conservative bounds `H=27,P=162` for every state labelling.
The exact finite addition product enumerates all endpoint pairs
`(q(n),q(n+162))` with `n>=27`.

**U:** The centre is eventually periodic exactly when, at each phase,
`C[p,a]=C[p,b]` on every endpoint pair. The resulting centre agrees
at shift 486 at every actual time at least 81. This is a consequence
of the automaton structure, not an externally imposed onset or period.

Define the masked neighbour by `m_t=(1-c_t)r_t`. Its phase labelling is
`(1-C[p,q])R[p,q]`, on the same three-state axis. Under the centre
equalities, a masked endpoint mismatch is exactly

```text
C[p,a]=C[p,b]=0 and R[p,a]!=R[p,b].
```

Therefore a centre equality on every endpoint pair, together with one
such mismatch, is equivalent to an eventually periodic centre and an
aperiodic masked neighbour. When the centre is eventually periodic,
mask aperiodicity is equivalent to aperiodicity of the chronological
neighbour sequence restricted to centre-zero times: a common temporal
period groups those times into repeated finite blocks. An eventually
empty zero set cannot satisfy the mismatch condition.

All 6,561 possible padded ternary axis tables are covered. Each one
receives guarded centre-equality clauses and a guarded disjunction of
zero-centre/unequal-right selectors. The centre and right compositions
are encoded exactly by one-hot transition gates. Exactly one full-axis
guard matches a candidate table. This is complete observation elimination
for the specified class, without a finite witness horizon.

## 3. Refutation and independent checks

The clean seed formula has 609 variables and 83,355 clauses. It includes
84 actual Rule 30 gates and no early centre equations. From the earlier
[narrower ternary test](RESULTS-r1-ternary-automatic-construction.md),
14,314 ordinary gate implicants transfer: each independently forces a
specific invalid Rule 30 tile. Every earlier centre cut and every
clock-based observation condition is discarded. The imported base has
609 variables and 97,667 clauses.

The new run returned UNSAT within its 60-second cap. It examined 2,266
candidates and recorded 64,716 new gate implicants. Its final formula
has 609 variables and 162,372 distinct clauses. The reported run time
is 30.7924 seconds. The producer's DRUP check passes.

The independent verifier rebuilds every expected clause separately,
including all compositions, selectors, axis conditions, seed gates,
imports and new refinements. It uses an independently directed endpoint
construction and its own ternary coordinate evaluator. Exact counts are:

| Check | Count |
|---|---:|
| Axis tables | 6,561 |
| Endpoint pairs | 40,979 |
| Candidate models | 2,266 |
| Candidate centre-pair equalities | 52,425 |
| Candidate seed gates | 190,344 |
| Imported / new gate cuts | 14,314 / 64,716 |
| Coordinate paths | 316,120 |
| Individual transition steps | 1,016,734 |
| Frozen truth-row cube comparisons | 632,240 |

The final CNF matches exactly, and an independent DRUP rerun returns
VERIFIED. SHA-256 values are:

```text
result: 5c931ce2f3e9c935e4bcc57a131e7d70453f9b57cf28f0c31fa09bbf4023f82e
CNF:    c194dcd6b520578430a0735966cc54bf3e62da2793debf0a238e354b028a94aa
DRUP:   dd01b14ac8116cffaa92a63094d5d116fd0f909f327f89283612139b131ba85d
```

## 4. Controls, reproduction and scope

The observation reduction is deliberately rule-independent. The actual
Rule 30 distinction enters through frozen OR-saturated gates. The
generic gate checker accepts the existing binary Rule 90 diagram in
its original radix. The unchanged `controls.rule90_control(6)` passes
again at periods two, four and six. No ternary presentation of the
binary Rule 90 spike sequence is assumed.

Artifacts are in `experiments/rule30/r1-zero-set-attack/construction/`:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_ternary_epcentre_independent.py
```

This reproduces the complete saved-clause and DRUP verification. The DRUP
replay needs DRAT-trim, located by
`experiments/rule30/r1-isolated-column/drat_trim.py`: `$RULE30_DRAT_TRIM`,
then `/tmp/rule30-family-seam-drat-trim/drat-trim`, then `drat-trim` on
`PATH`; the pinned build recipe is in `RESULTS-family-seam.md` section 8.
A new search, under a new output name, uses

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_ternary_epcentre_synthesis.py --seconds 60 --batch 32 --output fresh-any-epcentre.json
```

The obstruction is specific to three core states, radix three, and the
stated lookup periods. It does not bound the automaton size of general
Rule 30 diagrams, exclude nonautomatic diagrams, or decide R1. No finite
sample is being extrapolated to arbitrary time: the finite certificate
refutes a complete, explicitly bounded representation class.

# Exact observation reduction with an odd time-lookup factor

Date: 2026-09-09. Evidence: **U** (uniform observation reduction), **C**
(complete finite axis catalog and independent replay), **M** (a bounded
construction run ended UNKNOWN). **No class refutation, R1 proof, or R1
counterdiagram is claimed here.**

The automatic-diagram construction can use time lookup period 40 and
space lookup period 8 without prescribing any centre period or onset.
This lookup directly represents the known period-40, width-eight Rule 30
ether. The exact observation formula for three core states is small:
1,360 variables and 4,733 clauses before any ordinary Rule 30 gates.

## 1. Mechanism and stopping condition

The proposed representation is

```text
s(t,x) = g[t mod 40][x mod 8][DFA_state(t,x)],   t,x >= 0,
```

where an unknown three-state DFA reads paired binary digits from most
significant to least significant. The initial state has a leading-zero
self-loop. All lookup bits and transitions are free. A candidate would
need to pass all Rule 30 gates at `t>=0,x>=1`, an eventually periodic
centre, and an aperiodic masked neighbour `(1-c_t)r_t`.

The first diagnostic computes the entire finite observation catalog,
builds its clauses, and checks existing diagrams and controlled output
labellings. The catalog computation has a 60-second cap. A subsequent
single construction run has a separate 60-second cap. It refines unknown
automatic diagrams by exact ordinary Rule 30 gate violations. Any accepted
construction must pass the complete full-coordinate gate product; a class
refutation needs an independently checked final-CNF proof.

## 2. Uniform odd-modulus lift

Write an even lookup period as `T=2^a d`, with `d` odd and `a>=1`.
Let `A(q,b)=delta(q,2b)` be the reachable binary time-axis automaton,
with `R` states. At time `t=2^a n+r`, where `0<=r<2^a`, augment its
state after reading `n` by the residue `n mod d`:

```text
(q,s) --b--> (A(q,b), (2s+b) mod d).
```

This is a padded MSB automaton with at most `R*d` states. Its initial
state is `(0,0)`. The actual lookup phase is `2^a*s+r`. Reading the
upper `a-1` bits of `r` through `A`, followed by paired last digit
`(r mod 2,0)` or `(r mod 2,1)`, gives the centre or right-neighbour
observation. For each fixed `r`, both observations and their masked
product are binary output labellings of this same augmented automaton.

The [uniform MSB period theorem](RESULTS-r1-automatic-period-bound.md)
therefore supplies

```text
H = 2^(R*d),    P = H*lcm(1,...,R*d).
```

An output labelling is eventually periodic exactly when it agrees at
shift `P` for every coarse time at least `H`. The finite addition product
enumerates exactly the pairs of augmented states attained at `(n,n+P)`
for `n>=H`. Since `d<=R*d`, the period `P` is divisible by `d`, so the
two augmented endpoint states have the same residue component.

**U:** The centre is eventually periodic if and only if its two composed
outputs agree on every such endpoint pair, for every low word `r`.
This covers every centre period and onset that can occur in this
representation class. When the equalities hold, a masked mismatch is
exactly two zero centre outputs with unequal right-neighbour outputs.
At least one such mismatch is equivalent to masked aperiodicity.

The resulting actual-time bounds are `2^a H` and `2^a P`. For `T=40`
and `R<=3`, safe bounds are onset 262,144 and period 94,466,211,840.
They are consequences of the finite representation, not hypotheses
restricting the unknown centre clock. Interleaving the finitely many
low-word sequences preserves the stated equivalences. For an eventually
periodic centre, mask aperiodicity is equivalent to aperiodicity of the
chronological neighbour sequence on the centre-zero set.

## 3. Complete three-state catalog and exact clauses

Axis-first state naming covers every representation by simultaneous
renaming of transitions and outputs. There are 50 canonical reachable
binary axes of size at most three. The catalog records every exact
endpoint pair and its witness.

| Reachable axis states | Augmented states | Axes | Endpoint pairs | Folded nontrivial pairs | Maximum addition-product states |
|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 1 | 5 | 0 | 552 |
| 2 | 10 | 4 | 55 | 50 | 6,168 |
| 3 | 15 | 45 | 1,396 | 1,476 | 32,552 |
| Total | | 50 | 1,456 | 1,526 | |

After the upper low bits are folded, write `C[p,q]` and `V[p,q]` for
the centre and right outputs after the final paired digit. Their exact
one-hot transition compositions use symbol `2*(p mod 2)+x` for `x=0,1`.
For each axis guard and phase, endpoint equality needs only a spanning
forest of the folded endpoint graph. Under those equalities, a masked
mismatch exists on the graph exactly when a zero-centre forest edge has
unequal `V` endpoints. Thus the same forest suffices for both parts of
the predicate; no endpoint condition is weakened.

The concrete observation-only formula has these counts:

| Component | Count |
|---|---:|
| Raw transition and lookup variables, including true constant | 997 |
| Raw clauses | 50 |
| Axis naming clauses | 21 |
| Exact composition and selector clauses | 1,920 |
| Forest edges over all axis records | 1,346 |
| Guarded observation clauses | 2,742 |
| Total variables / clauses | 1,360 / 4,733 |
| Clock variables / early centre equations / seed gates | 0 / 0 / 0 |

The constructor is separate from the earlier power-of-two-only synthesis
constructor. It installs the common DFA parameters and reuses only the
ordinary ground-gate methods. No existing solver source or active search
semantics was modified.

The prepared gate-refinement backend adds 640 actual Rule 30 equations,
at `t=0..39,x=1..16`, giving 4,301 variables and 30,412 clauses. Later
ordinary gate implicants use only the 997 original parameter variables.
The subsequent bounded run is recorded below.

## 4. Independent replay and controls

**C:** An independent implementation reconstructs all 50 augmented
endpoint relations by a coarse-prefix graph and a fixed-low-digit dynamic
program. It checks all 1,456 pairs and exact witnesses, and all 1,526
folded pairs. It inspects 1,967 coarse states and 118,800 low-digit states.
All sets agree with the producer. This check enumerates dynamic-program
states rather than exponentially many low words.

The separate constructor and clause integration also pass independent
source review, and their saved regression reproduces the stated 1,360
variables and 4,733 clauses. The residue augmentation is deterministic
inside the catalog; it does not introduce unknown full-diagram states
beyond the original three-state core.

The known Rule 30 ether starts from ring-eight row integer 7, with
bit zero at spatial coordinate zero. Frozen Rule 30 updates return to
that row first at time 40. Its direct lookup presentation passes the
full-coordinate gate product, using 2,560 product states; 1,920 scalar
cells are also checked. The observation classifier correctly reports
both centre and masked neighbour periodic.

The initial control retained the binary Rule 90 construction with its
five full core states and three reachable axis states. Repeating its output lookup at periods
40 and 8 preserves all 16,384 checked coordinates. The exact Rule 90
gate product accepts it in 5,075 states. The lifted observation predicate
accepts its periodic centre and aperiodic masked neighbour, with actual
endpoint times 524,287 and 94,466,736,127: the centres are both zero and
the neighbours are respectively one and zero. The observation CNF also
accepts this fixed Rule 90 model after its axis states are renamed first.
The unchanged `controls.rule90_control(6)` passes all three cases.

Subsequent exact minimization gives a stronger positive control for the
original three-state class itself. Merge the old states into
`{0},{2,4},{1,3}`. The quotient transition rows are

```text
0: [0,2,1,0]
1: [2,1,1,0]
2: [2,2,2,2]
output: [1,0,0]
```

The projection commutes with all 20 old transitions and preserves all
10 old phase/state outputs, so it preserves every coordinate value.
All three quotient states are reachable. State zero is distinguished by
its output; states one and two are distinguished by suffix symbol three.
Thus this ordinary constant-output Moore automaton is minimal. No
minimality claim is made when extra lookup clocks are allowed.

The quotient passes 16,384 scalar comparisons, the full Rule 90 gate
product in 4,660 states, and the exact R1 observation predicate. It also
passes the complete three-state depth-three prefix formula below. Its
proof and checks are in `direct_dfa_rule90_minimal.py` and
`direct-dfa-rule90-minimal.json` under the construction directory.
Therefore the earlier three-state Rule 30 tests already concern a class
containing an actual Rule 90 counterdiagram; the control did not require
enlarging that class.

As a separate observation-only calibration, a three-state padded model
with zero centre and a Thue–Morse right output satisfies the predicate;
replacing its right labels by constants makes the same core fail it.
That model is not asserted to satisfy Rule 30 gates. The reduction is
rule-independent; any future Rule 30 conclusion must enter through its
OR-saturated local truth table.

## 5. Bounded construction result

After independent review of the observation reduction and the concrete
backend, one CaDiCaL195 run examined this exact class for 60 seconds.
It ended **UNKNOWN**, at a measured 60.0134 seconds. It rejected 2,171
candidate descriptions and recorded 42,441 ordinary gate implicants.
The final formula has the same 4,301 variables and 72,810 distinct
clauses. The solver recorded 56,812 conflicts and 1,357,869 decisions.

Every candidate passed the exact eventual-centre/aperiodic-mask predicate
and failed an actual Rule 30 gate. The gate check has the complete finite
bound 207,360 states; it does not truncate a temporal simulation.
Producer replay reconstructs all 42,441 cuts, with maximum clause width
16 and at most 12 distinct transition guards. All models and coordinate
paths are retained in
`direct-dfa-odd-phase-R30-N3-T40-q8-cadical60.json.gz` under the construction
directory. Lossless decompression is verified against the original JSON.

Independent replay **passes**. It reconstructs the entire base and final
CNF, all 2,171 candidate observations, 578,896 centre endpoint equalities,
2,171 masked witnesses, 1,389,440 frozen seed gates, and all 42,441 cuts.
The cut replay covers 169,764 coordinate paths, 1,006,977 transitions,
and 339,528 frozen valid-row comparisons. The unchanged Rule 90 controls
pass again. Exact SHA-256 values are:

```text
raw JSON:  2d1ec5622b81e8fad7b70b2aa61deec1da1b2ac5fcaf4ea1dac82c812fc96c5e
gzip:      b909bdd5f977ae175efde0c2ae129826ed5612640f8c4ac86f3f88d214a8c1e9
final CNF: 5c0c17c43e611f21ca70a0223097b5b2c69da079537da2a6cb1c309d13185ebb
```

These are measurements of one construction run. UNKNOWN gives no class
exclusion, and the surviving formula is not a realizable diagram. No
finite computation here is presented as an asymptotic result about Rule 30.

The exact lifted relation was subsequently cached by the immutable axis
table and lookup period. Candidate output labels are not cached. Replay
of all 2,171 saved observations reproduces the original JSON values,
and every source gate implicant is rebuilt before resuming the formula.
No clause or representation restriction changes.

A 300-second continuation from that exact 72,810-clause checkpoint also
ended **UNKNOWN**, at 300.0144 seconds. It added 18,550 candidate records
and 324,759 gate implicants. Its final formula has 4,301 variables and
397,235 distinct clauses. The cache records 20,680 hits and 41 misses.
The previous source artifact remains a hash-provenanced dependency;
the new gzip stores every new model and path rather than duplicating the
old arrays. Its name is
`direct-dfa-odd-phase-R30-N3-T40-q8-cadical300.json.gz`.

Independent cumulative replay **passes**: 20,721 models, 367,200 gate
cuts, 5,382,856 centre endpoint equalities, 13,261,440 frozen seed gates,
1,468,800 coordinate paths, 8,975,895 transitions, and 2,937,600 frozen
truth-row comparisons. It verifies every dependency hash, clause-stream
hash, and intermediate formula boundary, then reconstructs the complete
397,235-clause formula. The unchanged Rule 90 controls pass again.

```text
continuation raw JSON: 1bd28076145a5a6086af499184afbab884003eb09a346109592ae963ac817db6
continuation gzip:     2e498aed95ae1d064e8a1f74ac346ab852d4b078433ec724b7e0eaee4cf73806
continuation CNF:      79d1e234e6a796bc04af4e51ec9fdd87137ed77374316d04bf32b67030db6f91
```

This continuation supplies a larger certified necessary-clause pool,
without an UNSAT proof or a realizable Rule 30 diagram.

## 6. Reproduction and scope

Run from the repository root:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_odd_phase_observation.py
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_odd_phase_observation_independent.py
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_odd_phase_encoding.py
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_odd_phase_result_independent.py
uv run --with ijson python experiments/rule30/r1-zero-set-attack/construction/verify_odd_phase_result_independent.py experiments/rule30/r1-zero-set-attack/construction/direct-dfa-odd-phase-R30-N3-T40-q8-cadical300.json.gz --stream
```

These reproduce the observation JSON exactly, except for the producer's
recorded elapsed time, and perform no synthesis search. To start a new
bounded construction run under a distinct output name:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_odd_phase_cadical.py --seconds 60 --batch 32 --output fresh-odd-phase.json
```

The complete gate-product
bound for a future three-state, time-40, space-eight candidate is
`3^4*8*40*8=207360`; a cap at least that large completes the exact check.

This establishes a feasible exact finite encoding for a distinct
automatic construction class. It proves neither existence nor absence
of a Rule 30 member with the required observation. It does not imply
that a generic R1 counterdiagram, if one exists, must be automatic.

## 7. Keeping the time axis small while enlarging the full core

**U, representation observation:** Total core size and reachable
time-axis size can be bounded separately. Let the full paired-digit DFA
have `N>=3` states, but require its reachable time axis to have some
`R` in `{1,2,3}`. Rename those `R` states first in their binary discovery
order. Constrain their `delta(_,0)` and `delta(_,2)` transitions to one of
the same 50 canonical axes. Every odd-symbol transition from an axis
state, every transition from a remaining state, and every output label
remain arbitrary. In particular, off-axis transitions may return to the
axis; forbidding those returns would narrow the intended class.

The exact observation catalog and onset/period bounds are unchanged by
`N`. At `x=0` the whole digit path stays on the time axis. At `x=1` every
spatial digit before the final one is zero, so the path leaves the axis
only at its final digit. Its final state may be any of the `N` states,
but the composed right output is still a binary labelling of the same
`R` axis states, and hence of the same `5R` augmented states. Extra
off-axis transition structure affects the other columns and the Rule 30
gate obligations, without changing this observation theorem.

Only `C[p,q]` and `V[p,q]` for `q<3` are needed. With selectors for
`R=1,2,3`, the observation-only counts for this proposed formulation are

```text
variables = 364 + 4*N^2 + 320*N,
clauses   = 3209 + 496*N + 2*N^2*(N-1).
```

The clause count includes `12*N-15` axis-naming clauses, `480*N+480`
composition/selector clauses, and the same 2,742 catalog clauses.
These are counts from the specified construction, not measurements of
an enlarged search. The separation argument and both count formulas
also pass independent symbolic review.

| Full states | Maximum axis states | Observation variables | Observation clauses | Complete gate-product bound |
|---:|---:|---:|---:|---:|
| 3 | 3 | 1,360 | 4,733 | 207,360 |
| 4 | 3 | 1,708 | 5,289 | 655,360 |
| 5 | 3 | 2,064 | 5,889 | 1,600,000 |

Adding a fourth full state is the smallest state-count enlargement of
the original class. The three-state Rule 90 quotient above already lies
in the original class. A four-state presentation can split its dead
state and send the initial state's spatial-one exit to the new dead
copy. All four full states are then reachable, while the time axis still
has three states; projection to the minimal quotient proves that it
describes the same Rule 90 diagram.
Allowing an arbitrary finite number of off-axis states would require
the union over `N`; a result for one fixed `N` cannot settle that union.

Old ordinary gate implicants could be transferred to a larger core by
rebuilding each coordinate path with its new transition/output variable
IDs. Their numeric literals cannot simply be copied: changing `N`
changes the variable numbering. The old observation or state-naming
constraints would not be imported as gate facts.

## 8. Prepared four-state prefix encoding

The proposed `N=4,R<=3,T=40,q=8` class is implemented in
`direct_dfa_offaxis_encoding.py`. Complete axis-naming calibration covers
all 16,384 labelled four-state time-axis tables and 49,152 exact-size SAT
queries. The canonical acceptances for `R=1,2,3` are 4,096, 1,024, and
720. Every one of the 11,488 labelled axes with at most three reachable
states survives the prescribed renaming. Fresh naming clauses contain
no odd-symbol transition variables. Independent source review passes.

The observation formula has 1,708 variables and 5,289 clauses. Adding
640 ordinary seed gates gives 5,384 variables and 44,914 clauses. The
[uniform prefix theorem](RESULTS-r1-uniform-prefix-gates.md), at suffix
depth three, adds 20 prefix types and 840 guarded gate equations. The
complete prepared formula has 7,956 variables and 74,395 clauses. A
candidate still needs the full 655,360-state gate product to pass.

The actual three-state Rule 90 quotient and the reachable four-state
presentation both satisfy the corresponding complete observation,
ordinary-gate and prefix formulas. Their exact scalar prefix checks
cover 630 and 840 gates respectively; full gate closures use 4,660 and
7,740 states. The period-40 Rule 30 ether satisfies the four-state
ordinary and prefix gates and its full-coordinate check. The unchanged
`controls.rule90_control(6)` passes again. These are positive controls,
not inferred Rule 30 realizations of an aperiodic observation.

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_rule90_minimal.py
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_offaxis_encoding.py
```

After the setup and controls passed review, a single 300-second
four-state construction diagnostic ended **UNKNOWN**, at 300.008955
seconds. It checked 6,129 candidate descriptions and recorded 169,416
ordinary gate implicants. Every candidate satisfied the exact R1
observation and the uniform depth-three prefix conditions, then failed
an actual Rule 30 gate. The final formula has 7,956 variables and
243,508 distinct clauses. Producer replay passes all cuts, with maximum
clause width 19 and at most 15 distinct transition guards.

The complete artifact is
`direct-dfa-offaxis-R30-N4-R3-T40-q8-depth3-cadical300.json.gz`; it retains
every new model and coordinate path. Independent full-pool replay now
passes all 6,129 models and 169,416 cuts: 159,112 endpoint pairs,
1,272,896 centre equalities, 3,666,055 scalar prefix gates, 3,922,560
ordinary seed gates, 677,664 coordinate paths, 4,148,196 transition
steps, and 1,355,328 frozen truth-table comparisons. The reconstructed
CNF SHA-256 is
`939941d17b03646bd4fbbebad98f1549230ce1c70c49b0088da9b5c4c631aad9`.
The unchanged Rule 90 controls pass. There is no enlarged-class
existence or exclusion claim.

Exact diagnostics of this saved pool give an eventual-zero centre for
280 of 6,129 candidates; 5,849 have a nonzero eventual centre period.
The classification uses the audited lifted endpoint left projection and
the proved automatic-period bounds, rather than a numerical tail window.
Of all candidates, 6,098 already have a saved failed gate contained in
one depth-four suffix block. Complete depth-four checks on the remaining
31 reject another 25 and accept six. Thus exactly 6/6,129 pass the
depth-four necessary criterion. All six have nonzero centre periods and
still fail a later ordinary Rule 30 gate.

The six source candidate indices are `383,409,448,2287,2299,2348`.
Their smallest saved failing suffix depths are respectively
`5,5,7,5,5,5`. Representative depth-four failures are candidate zero at
`(t,x)=(3,23)`, with tile values `(1,0,0;0)`, and candidate five at
`(44,7)`, with `(0,0,0;1)`. Both disagree with the frozen Rule 30 table.
The complete depth histogram and witnesses are saved in
`direct-dfa-offaxis-N4-R3-depth3-pool-diagnostic.json`.

Adding all depth-four prefix gates to the existing depth-three formula
requires 9,176 additional variables and 114,176 additional clauses for
4,200 guarded gates. The combined clean base has 17,132 variables and
188,571 clauses. The measurements identify a concrete bottleneck for
the next encoding and do not establish an asymptotic Rule 30 claim.

```sh
uv run --with ijson python experiments/rule30/r1-zero-set-attack/construction/diagnose_offaxis_pool.py
```

## 9. Continuation with depth-four necessary gates

**Mechanism and kill condition, stated before the run:** retain all
169,416 recorded ordinary gate implicants in the same four-state class,
then add the depth-four uniform prefix equations and the 50 odd-phase
OR-tail clauses from `direct_dfa_odd_or_tail_prune.py`.
The latter are necessary because an eventually zero Rule 30 centre
forces its right neighbour to be eventually constant by OR monotonicity.
No centre clock, period, onset, off-axis return restriction, or new state
bound is imposed. The run stops after 300 seconds, a verified UNSAT
result, or a candidate passing the complete 655,360-state gate product.
An UNKNOWN checkpoint is not a class exclusion.

For clarity, the OR-tail clause for a selected axis uses the **left
projection of every exact endpoint pair, including diagonal pairs**.
Folding each of the eight low suffixes gives every composed centre
output that occurs after the certified onset, with its actual phase
`8*s+r`. Their disjunction is therefore equivalent to the centre tail
containing a one. If that disjunction fails, then `c_t=0` throughout
the tail and the Rule 30 gate at column one gives
`r_(t+1)=r_t OR s(t,2)`. This binary monotone sequence becomes constant,
contradicting the imposed aperiodicity of the masked neighbour. This
necessity uses OR and is not applied to Rule 90. The clause adds no
auxiliary variables and does not prescribe a centre word.

`direct_dfa_offaxis_resume.py` regenerates every source coordinate path
and checks the source's compressed and uncompressed hashes before
allocating the new depth-four auxiliary variables. The expected search
base has 17,132 variables and 357,734 clauses. Its exact Rule 90 control
passes all 4,200 reachable depth-four gates, the complete gate product,
the R1 observation, and SAT with the control parameters fixed. The
Rule 30-only OR-tail prune is not applied to Rule 90.

The continuation ended **M / UNKNOWN** after 300.403703 seconds. It
checked 50 candidate descriptions and retained 712 new ordinary cuts,
of which 711 add distinct clauses. Each description passed the exact
observation and the depth-four necessary criterion, then failed an
actual Rule 30 gate. The final formula has 17,132 variables and 358,445
clauses. Producer replay passes every new cut, with maximum clause
width 17 and at most 13 distinct transition guards. The source replay
also regenerates all 169,416 old cuts and reproduces all 6,129 old exact
observations before adding the new auxiliaries.

The full checkpoint is
`direct-dfa-offaxis-R30-N4-R3-T40-q8-depth4-cadical300.json.gz`.
Its uncompressed SHA-256 is
`758f6ce1cf715f7bf93e7d5acce79e1e75f31a636d9c215d81ca7f837889d421`;
its compressed SHA-256 is
`82c5c14c3b7a2e7efd5187c04d7c55e1ad4b6224d83ba950738e3d7c995426b4`.
The 7,581,553 uncompressed bytes are preserved in 216,663 compressed
bytes, together with the exact source dependency. Decompression and both
hashes reproduce. Independent replay of this new segment is pending;
the source depth-three segment has passed it. No UNSAT certificate or
full Rule 30 diagram was obtained.

A further **M** diagnostic of these 50 saved descriptions, without new
synthesis, rejects all 50 at the complete depth-five necessary check.
Their minimum saved failing suffix depths are five for 44 descriptions,
six for one, and seven for five. All 712 saved failures have suffix
depth at least five. Exact failures and the complete histogram are in
`direct-dfa-offaxis-N4-R3-depth4-pool-diagnostic.json`. This identifies
the next finite obstruction in this checkpoint; it does not infer that
any fixed depth settles the full automatic class or R1.

```sh
uv run --with ijson python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_offaxis_resume.py --seconds 300
uv run --with ijson python experiments/rule30/r1-zero-set-attack/construction/diagnose_offaxis_depth4_pool.py
```

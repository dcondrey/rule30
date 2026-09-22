# Direct automatic Rule 30 construction: exact synthesis framework

Date: 2026-09-09. This is an intermediate construction attempt. No R1
counterdiagram has passed the all-coordinate check in the recorded runs.

The searched diagram is defined at every `t>=0,x>=0` by a deterministic
finite automaton reading synchronized binary digits of `(t,x)` from most
significant to least significant. Its core transition table is unknown.
The output lookup additionally uses `t mod T,x mod q`. The root is state
zero and `delta_(0,0)(0)=0`, so common leading-zero padding has no effect.
This is not a factor of a fixed Rule 90 or Rule 150 source. Different
spatial coordinates can define infinitely many different temporal columns.

The candidate centre agrees with an unknown `T`-periodic clock from time
one onward. The initial centre value is allowed to differ. Only local
updates at `x>=1` are checked; every successful quadrant has a unique left
completion by Rule 30's inverse formula

```text
s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1)).
```

Thus an all-coordinate SAT certificate with an aperiodic zero-set neighbour
would supply a full formal counterdiagram, with no assumption of periodic
farther columns or a finite strip boundary.

## Exact gate closure (`U/C`)

To check a gate, synchronize the five nonnegative coordinates `t,t+1` and
`x-1,x,x+1`. Read their binary digits from the most significant end while
tracking the four core states for the left, middle, right and next-time
cells. Track the three differences between the coordinate prefixes too:

```text
d_t in {0,1},   d_minus in {-1,0},   d_plus in {0,1}.
```

A new digit changes each difference by `d -> 2d + bit_difference`.
Leaving its listed range makes the required final difference impossible:
no suffix of two equal-length binary numbers can repair it. Terminal
differences `(1,-1,1)` mean exactly the desired coordinates and imply
`x>=1`. The tracked time/spatial residues supply the output lookup phases.

Every reached product state retains an actual integer witness. Conversely
every actual gate has an equal-width padded binary representation in this
product. Closure and truth-table agreement therefore check all gates, not
only a bounded rectangle. A failure supplies a concrete `(t,x)` and its
four output values. The centre uses a smaller one-variable product,
including a flag that excludes only `t=0` from the clock condition.

`direct_dfa_check.py` implements this finite product. It has been
independently audited. Its Rule 90 positive control uses the exact
five-state radius-one binary renormalization of the lone-seed diagram:
113 gate-product states, 16 terminal states, 380 transitions, and four
centre-product states. A separate scalar source calculation agrees at
16,384 coordinates. The full finite closure is retained in
`direct-dfa-rule90-control.json`.

## Observation certificate and its bounds (`U/R`)

For `T=2^a` and a fixed residue `r`, the neighbour subsequence
`u_r(n)=s(T*n+r,1)` has an `N`-state MSB automaton. Its transitions while
reading `n` are `delta_(bit,0)`; the fixed low coordinate suffix `(r,1)` is
folded into the output function. The spatial lookup causes no extra state
factor, because the observed coordinate is always one.

The independently audited automatic-period bounds are documented in
`docs/rule30/RESULTS-r1-automatic-period-bound.md` and its direct-MSB
strengthening. The original encoding safely reversed an `N`-state MSB
machine to at most `M=2^N` LSD states and used

```text
H=2^M,  P=2^M*lcm(1,...,M).
```

The improved encoding uses the direct-MSB theorem with `M=N`. In either
case a single exact inequality `u_r(n) != u_r(n+P)` at `n>=H` proves that
subsequence aperiodic. Selecting a residue whose centre clock is zero
makes it a zero-set neighbour certificate. No sampled Rule 30 trace is
declared aperiodic merely because one mismatch was observed: the theorem
requires the independently defined finite automaton at every time.

The original witness-bit cap was explicit and not claimed complete. The
improved encoding uses `L+4N^2` bits, where `L=P.bit_length()`, which is
complete. Write `n=2^L*m+r`. Addition of `P` changes the high part from `m`
to `m+c`, `c in {0,1}`. The synchronized MSB product of these two high
inputs retains two core states, prefix difference zero or one, and whether
`m>0`, at most `4N^2` states. Replace a high path by a shortest path with
the same endpoint and positivity flag, keeping the low `L` digits. Both
outputs and the condition `n>=H` are preserved. Hence any inequality has
a witness within the stated bit cap. This argument has been independently
audited; it is not extrapolation from a witness search.

## Synthesis and controls

The SAT variables are the unknown transition table, output lookup, centre
clock, and a binary witness to the observation inequality. Transition
choices and intermediate core states use one-hot encodings. A ripple
adder encodes `n+P` exactly, including its carry bit. Every SAT parameter
assignment is checked by the all-coordinate products above. Failing
coordinates add necessary actual Rule 30 equations. Batches of up to 32
failing terminal states reduce repeated product traversals.

Canonical state numbering is a sound symmetry reduction. Enumerate
reachable states by first discovery from the root, scanning outgoing
symbols in order. Whenever a transition first targets state `v>=2`, an
earlier transition has already targeted `v-1`. All unused states can have
transitions normalized to zero. This is a relabelling of the same diagram;
no clock rotation or complementation is assumed. Checks cover all 128
padded two-state transition tables and 600 deterministic random tables
with three through eight states.

For Rule 30 the complete run additionally requires at least one clock
one. If the eventual centre were all zero, then
`r_(t+1)=r_t OR s(t,2)`, so `r` is eventually nondecreasing and cannot be
aperiodic. A clock zero already follows from the observation selector.
This pruning is deliberately not applied to the Rule 90 control.

The frozen Rule 90 five-state model satisfies the same observation CNF.
Its clock is `T=2,q=1`, distinct from the Rule 30 search clock `T=4,q=14`.
For the original bound, the solver found `n=8589934591,r=1`, giving actual
times `17179869183=2^34-1` and `1240417074208453515280383`. The exact Rule 90
formula gives neighbour values one and zero there. The direct-MSB control
also passes with the new bound and canonical numbering. Exact reversal
of the control's residue subsequences yields one state for the constant
even subsequence and three for the aperiodic odd subsequence. All controls
are callable from `verify_direct_dfa.py`.

## Recorded intermediate runs

| Core states | Observation encoding | Coordinate cuts | Outcome |
|---:|---|---:|---|
| 3 | reversed bound, 26-bit witness | 81 | UNSAT, DRUP verified |
| 3 | complete direct-MSB predicate, 42-bit witness | 81 | UNSAT, DRUP verified |
| 5 | reversed bound, 88-bit witness | 685 | UNKNOWN at 60 seconds |
| 5 | same predicate, batches of 32, resumed cuts | 1,108 | UNKNOWN at 180 seconds |
| 5 | complete direct-MSB predicate, canonical numbering | 1,141 | UNKNOWN at 180 seconds |
| 5 | same complete predicate, CaDiCaL195 portfolio | 1,422 | UNKNOWN at 180 seconds |

The first final CNF has 2,092 variables and 15,305 clauses. Its proof is
independently rechecked. The complete three-state predicate uses `H=8,P=48`
and 42 witness bits; its 2,236-variable, 16,150-clause formula is also
DRUP-verified, using the same 81 coordinate cuts. This genuinely excludes
the specified three-state, `T=4,q=14` automatic class.
The original batched partial CNF has 19,097 variables
and 230,089 clauses; it is not an UNSAT certificate. All saved CNFs are
reconstructed from the source and exact counterexamples. The batch run
retains 23 candidate models; separate scalar evaluation checks all 423
new failing coordinates and 20,703 previously imposed constraints.

The complete direct-MSB five-state run uses `H=32,P=1920`, 111 witness
bits, canonical state numbering, and the nonzero-clock condition. Its
19,902-variable, 239,404-clause formula remained UNKNOWN at the cap. Its
two saved parameter models supply 33 additional failing coordinates;
separate scalar replay checks those and 2,248 preceding constraints.
No result from a resource-limited run is extrapolated to the whole class.
The complete predicate does cover the specified five-state, `T=4,q=14`
automatic class; the unresolved SAT result provides no exclusion of it.
The CaDiCaL195 portfolio retained one solver across 1,099 conflict-budget
chunks, reaching 2,180,085 conflicts. Its 24,930-variable, 301,356-clause
formula remained UNKNOWN at 180 seconds. Independent scalar replay checks
the 281 new failing coordinates from its 15 saved models and 18,852 prior
constraints. This is solver progress, not a mathematical exclusion.

Reproduce the saved controls and artifacts:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_check.py
uv run --with python-sat python experiments/rule30/r1-zero-set-attack/construction/verify_direct_dfa.py
```

The source `direct_dfa_synthesis.py --help` documents the explicit resource
limits, bound mode, batched cuts, and import/resume options. A SAT result
still requires the independently checked full product closure and the
automatic observation theorem before being reported as an R1 kill. The
current finite exclusions and UNKNOWN results do not prove R1 or P1.

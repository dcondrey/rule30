# Exact all-coordinate gate closure for automatic countermodels

Date: 2026-09-09. Evidence: **U** (encoding equivalence), **C**
(independent finite regressions). This is an intermediate construction
tool. It neither proves R1 nor supplies a counterdiagram.

The previous automatic-model searches often satisfied every gate in one
uniform prefix depth and failed at the next carry. This encoding imposes
the entire finite coordinate-checking graph at once. Its size depends on
the chosen coordinate automaton, not on a maximum time or spatial window.

## 1. Model and exact coordinate relation

The model is

```
U(t,x) = g[t mod T, x mod q, Q(t,x)],  t,x >= 0,
```

where Q is an N-state deterministic automaton reading equally padded
binary coordinate pairs from most significant to least significant digit.
Its start state has a zero-pair self-loop. The centre is column zero;
ordinary Rule 30 gates are required at every t>=0 and x>=1. A valid right
half-plane and its centre reconstruct all left columns by the unchanged
inverse rule. Eventual centre periodicity and neighbour aperiodicity are
separate obligations, imposed by the previously audited exact observation
predicate when this gate encoding is used in a construction search.

For a local gate, retain the four core states at coordinate prefixes for
`(t,x-1), (t,x), (t,x+1), (t+1,x)`. Retain also the prefix differences

```
(dt,dm,dp) in {0,1} x {-1,0} x {0,1}
```

and the middle coordinate's residues modulo T and q. Appending digits
`(tb,tnb,xmb,xb,xpb)` replaces the differences by

```
(2*dt+tnb-tb, 2*dm+xmb-xb, 2*dp+xpb-xb).
```

Keep the edge exactly when the new differences remain in their allowed
ranges. A difference outside these ranges cannot be repaired by a later
suffix. Conversely, the equally padded representations of any actual
local gate remain inside these ranges and end at `(1,-1,1)`.
Thus the closure from the all-zero prefix recognizes precisely the
coordinate quadruples requiring a gate. There are at most `8*N^4*T*q`
joint states. The eight difference types have respectively 6,0,12,6,2,0,4,2
digit edges in the implementation's displayed order, totaling 32.

## 2. Horn encoding and proof of equivalence (U)

Allocate an existential Boolean R for each joint state. Assert the initial
R. For every geometric digit edge, impose forward closure under the four
unknown core transitions. A direct enumeration of all source and target
four-tuples is unnecessary: update the left core coordinate, then the
middle, right, and next-time coordinates in four stages. Each intermediate
flag represents the complete hybrid four-tuple, retaining the correlation
between coordinates already updated and coordinates still to be updated.
The elementary clause is

```
active(hybrid) AND delta(old,symbol)=new  => active(next_hybrid).
```

The fourth stage enters the target R relation. Each active terminal tuple
implies all eight truth-table clauses of the required Rule 30 gate, with
the exact time and spatial residues of its four outputs.

**Soundness.** Fix any satisfying parameter assignment. The initial flag
and the staged implications force every actually reachable joint tuple
active, by induction on digit length. Its terminal truth-table clauses
therefore impose the correct gate at every actual coordinate.

**Completeness.** Fix any parameter assignment satisfying every actual
gate. Set R to its least reachable joint relation. On each digit edge,
set each intermediate relation to the successive exact images of its
source R relation under the processed coordinates. The fourth image is
contained in the target R relation. These assignments satisfy all closure
clauses and all terminal gates. Extra existential flags therefore impose
no restriction on the model class.

This proof covers arbitrary coordinate size. It does not claim that a
fixed-radius observation of the centre determines its neighbour.

The optional `collapse_time=True` first **equates every time output table
to phase zero** and then uses phase modulus one in the closure. It is
equivalent only within that explicitly equated-table class; it must not be
used silently to discard a time clock. Spatial residues remain present.

## 3. Implementation and checks (C)

Implementation:
`experiments/rule30/r1-zero-set-attack/construction/direct_dfa_gate_closure.py`.
It is a new helper; no frozen engine was changed.

The producer compared the encoding's SAT projection with the existing
complete checker on all 512 padded two-state, clock-free parameter tables
for each rule. Rule 30 accepts 147 and rejects 365; Rule 90 accepts 145
and rejects 367. The actual minimal three-state Rule 90 lone-seed model
also satisfies the complete closure.

The independent verifier derives the coordinate-prefix relation separately,
replays representative coordinates directly, and checks 69,907 SAT
projections. This includes all 128 padded two-state transition cores and
256 output labelings at T=2,q=2 for both rules: 2,473 Rule 30 assignments
and 835 Rule 90 assignments are accepted. It also checks odd T=3 with
q=2, rejects unequal output tables when time collapse is requested, and
accepts the actual three-state Rule 90 model at T=3,q=2 while rejecting
18 perturbed output labelings. The unchanged Rule 90 controls pass.

Run:

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_gate_closure.py
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_gate_closure_independent.py
```

The adjacent `direct-dfa-gate-closure-regression.json` and
`direct-dfa-gate-closure-independent-check.json` retain the exact counts.

## 4. Mechanism, kill condition, and scope

This helper permits a finite SAT search for an infinite automatic diagram.
A SAT assignment is useful only after the independent all-coordinate
checker and exact observation predicate both pass; the resulting diagram
then still needs an explicit description and aperiodicity proof. Verified
UNSAT excludes only the exact automaton/clock class encoded. A timeout
excludes nothing. Neither result may be extrapolated to all automaton
sizes, arbitrary diagrams, or the lone-seed orbit.

The mechanism's immediate kill condition is a disagreement between its
SAT projection and the independent coordinate checker; the completed
regressions found none. The Rule 90 counterdiagram remains admitted, as
required. R1 remains the active research target.

# Ternary automatic-diagram construction test

Date: 2026-09-09. Evidence: **U** (exact certificate reductions),
**C** (controls and parameter elimination), **M** (resource-limited
search if no certificate is obtained). R1 and P1 remain open.

## 1. Specified class and mechanism

The candidate is a three-state deterministic automaton reading paired
base-three digits of `(t,x)` from most significant to least significant.
Its initial state has a leading-`(0,0)` self-loop. The cell value is

```text
s(t,x) = g[t mod 3][x mod 7][DFA_state(t,x)],  t,x >= 0.
```

The output lookup table, all nine-symbol transitions, and the centre
clock of period dividing three are unknown. Centre equality is required
for every `t>=1`. A zero clock phase must have an aperiodic neighbour
observation. The all-zero Rule 30 clock is omitted using the existing
monotone-neighbour argument; a clock with no zero phase cannot satisfy
the observation condition.

The whole-alphabet canonical state numbering preserves the represented
class: number reachable states in breadth-first discovery order, then
normalize unreachable rows before completing the numbering. No canonical
condition is imposed on the time-axis subautomaton by itself.

The finite search mechanism has two exact parts: eliminate all periodic
observable output labellings for every possible time-axis table upfront,
then refine failed all-coordinate Rule gates by deterministic path
clauses. The success condition is an independently verified full Rule 30
diagram and an exact aperiodicity certificate. An independently checked
UNSAT proof would exclude this particular automatic class. The diagnostic
cap is 60 seconds; a cap gives UNKNOWN, not an exclusion.

## 2. Complete observation elimination

Write `delta_axis(q,d)=delta(q,3*d)`. There are exactly
`3^(3*3-1)=6561` labelled three-state ternary axis tables with the
required initial zero self-loop. Unreachable states are included.

For each such table, the independently checked
[arbitrary-radix theorem](RESULTS-r1-radix-automatic-period-bound.md)
uses `H=27` and `P=162`. Its finite addition product enumerates exactly
all pairs `(q(n),q(n+162))` for `n>=27`.

At actual time `t=3n+p` and spatial position one, the final paired digit
is `(p,1)`, of symbol number `3p+1`. Introduce the exact composed lookup

```text
V[p,q] = g[p][1][delta(q,3p+1)].
```

One-hot transition gates define every `V` without choosing the final
transition in advance. Shared selectors assert a zero clock phase and
an inequality between two `V` values. For each axis table, a clause
guarded by all its transition choices requires at least one selector
corresponding to an unequal endpoint pair. Exactly one full axis guard
matches any complete candidate transition table. Consequently these
6,561 clauses are equivalent to aperiodicity of at least one zero-phase
neighbour subsequence. They impose no numerical witness horizon.

The initial formula has 603 variables and 9,539 clauses, including the
complete observation conditions, 84 actual seed gates and five centre
equations. Gate refinements add no variables.

## 3. Finite class refutation

The search returned UNSAT in 14.0591 seconds, after 594 candidates and
14,458 recorded path cuts. The final formula has 603 variables and
23,995 distinct clauses; two recorded refinements repeat existing clauses.
The producer rebuilds every saved path record and verifies the final
DRUP proof with DRAT-trim. Independent replay of the actual upfront
observation formula passes all 6,561 axis clauses, all 40,979 endpoint
pairs, and all 81 composed-value/selector clauses. Independent replay
of the saved gate cuts and final CNF also passes: 594 candidate
observations, 49,896 candidate seed gates, 14,458 cuts, 57,400 coordinate
paths, 166,021 transition steps and 114,512 frozen truth-row cube
comparisons. The final CNF rebuilds exactly, and the independent
DRUP rerun returns VERIFIED.

The saved result is `direct-dfa-base3-N3-T3-q7.json`. Its final CNF and
DRUP proof are in `direct-dfa-path-certificates/`, with SHA-256 values

```text
CNF:  ad6aa1d16c8c6dc57edb0657c134cc0e71330ac4e2d106f3f6403995070d07f8
DRUP: 47fc3b2ffaf8f85c92d02d69fd09b0a28abed02f78677779123b9042bce44e59
```

The certificate refutes the complete class specified in section 1,
including arbitrary infinite right support within that class. It does
not extrapolate to larger automata, another radix or clock, or arbitrary
Rule 30 diagrams.

## 4. Exact gates and path clauses

The gate product retains four automaton states, three paired-coordinate
prefix differences, and the time and spatial residues. In any radix,
the differences for `(t+1)-t`, `(x-1)-x`, and `(x+1)-x` must remain in
`{0,1}`, `{-1,0}`, and `{0,1}`, respectively. Once a prefix difference
leaves its interval, no later digits can restore the required difference.
The product therefore covers every gate at `t>=0,x>=1` exactly.

For this class its complete state space is at most
`3^4 * 2^3 * 3 * 7 = 13608`. The checker uses this bound directly, so
there is no smaller closure cap that could silently truncate validity.
The centre product separately checks every positive time.

For each failed coordinate, retain the chosen transition literals on
the candidate's actual ternary paths, and the necessary signed output
literals. Ordinary frozen Rule 30 truth-table rows determine which
output coordinates are needed for the invalid tile. Negating this
conjunction gives one necessary clause. The output-cube reduction does
not assume accidental equalities between terminal automaton states.
Centre failures also retain the differing clock assignment. These are
the same independently reviewed logical implications as the binary
path-clause method, with actual ternary coordinate paths.

## 5. Controls and reproduction

The generic-radix gate checker verifies a ternary presentation of the
spatial checkerboard pattern and also the existing binary Rule 90
control diagram in its original radix. The saved checkerboard closure has 336 states, 42
terminal gates and 3,024 product transitions; 6,561 explicit coordinates
agree with spatial parity. Twelve deterministic random ternary models
provide another 8,748 gate-coordinate comparisons against an independent
coordinate evaluator. Those comparisons are calibration, not the proof
of all-coordinate closure.

The existing binary Rule 90 control passes through the generic checker,
with 113 product states and 16 terminal gates. The unchanged
`controls.rule90_control(6)` passes at periods two, four and six.
No finite ternary presentation of the Rule 90 spike sequence is asserted.
For a ternary aperiodic output-only control, the radix theorem uses parity
of the number of ternary digits equal to two; its exact mismatch is at
20 and 38. Ternary digit-sum parity would instead be periodic and is not
used as an aperiodicity control.

All implementation files are new, under
`experiments/rule30/r1-zero-set-attack/construction/`. Frozen Rule 30
engines remain unchanged.

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_radix_check.py
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_ternary_synthesis.py --seconds 60 --batch 32 --output direct-dfa-base3-N3-T3-q7.json
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_ternary_result_independent.py
```

The synthesis protects existing result files; use a new filename for
a new search. Any claimed positive or negative certificate still
requires independent saved-artifact replay. A full diagram obtained
in this class may have infinite initial support on both sides. It
would test the generic diagram version of R1, not constitute a
lone-seed Rule 30 counterexample by itself.

# Uniform prefix gates for automatic counterdiagram synthesis

Date: 2026-09-09. Evidence: **U** (necessary-condition theorem), **C**
(finite encoding checks). This is a synthesis improvement, not a proof or
kill of R1.

## Mechanism and stopping condition

The existing search checks one candidate automatic space-time field at
all coordinates, then adds clauses from its failing coordinate paths.
Here one gate constraint represents every coordinate with a given
reachable high-digit prefix state and clock residues. This shares an
ordinary Rule gate across infinitely many high-coordinate prefixes.

A finite suffix depth supplies necessary constraints only. The stopping
condition for reporting a counterdiagram remains the exact all-coordinate
gate checker together with the independently proved R1 observation test.
An UNSAT certificate excludes only its stated automatic model class.

## Uniform necessary-condition theorem (`U`)

Let

```text
U(t,x) = g[t mod T, x mod q, Q(t,x)],
```

where Q is a padded paired-binary-digit MSB automaton with initial state
0 and delta(0,00)=0. Let To and qo be the odd parts of T and q. Define
the exact prefix-reachable set

```text
R = {(Q(t,x), t mod To, x mod qo) : t,x >= 0}.
```

It is the least set containing (0,0,0) and closed under the four maps

```text
(a,u,v) -> (delta(a,2b+c), (2u+b) mod To, (2v+c) mod qo).
```

Choose d so that 2^d is divisible by both T/To and q/qo. For a member
(a,u,v) of R, append d paired low digits representing (i,j), with
0<=i,j<2^d. Its output is

```text
V_(a,u,v)(i,j) =
  g[(2^d*u+i) mod T, (2^d*v+j) mod q,
    delta*(a, paired_d_digits(i,j))].
```

This formula is exact: if (t,x) witnesses membership in R, then the
displayed value equals U(2^d*t+i,2^d*x+j). Changing t or x to another
representative with the same odd residue changes neither full clock
residue, because the missing power of two divides 2^d.

Consequently every valid Rule 30 field satisfies, for every member of R,
every 0<=i<2^d-1 and 1<=j<2^d-1,

```text
V(i+1,j) = V(i,j-1) XOR (V(i,j) OR V(i,j+1)).
```

All four cells lie inside one low-digit block, and the spatial centre
is at least one. Thus no carry or boundary gate has been silently
identified with an internal gate.

The CNF introduces one reach flag for each possible triple. It requires
the initial flag and closure under each selected transition. Flags may
describe a closed superset of R. Every satisfying assignment therefore
includes R. Conversely a valid field can choose exactly R, so the
existential flags do not exclude any valid field. Deterministic suffix
state circuits and output multiplexer circuits implement the displayed
formula; each ordinary eight-row truth-table constraint is guarded by
its prefix reach flag.

The union over all sufficiently large d is complete for ordinary gates:
any fixed t>=0,x>=1 is an internal gate of the block with zero high
prefix once 2^d>max(t+1,x+1). No finite d is claimed complete.

## Finite implementation checks (`C`)

The producer checks all 32,768 padded two-state transition/output models
with T=q=2 at d=2. SAT projection onto the actual transition and output
variables agrees exactly with a scalar check over all exact reachable
prefixes: 2,597 accepted and 30,171 rejected. The formula has 127 variables
and 563 clauses. These are counts for this necessary-condition encoding,
not counts of full diagrams.

The existing five-state actual Rule 90 diagram passes both the scalar
checks and CNF at (T,q,d)=(2,1,2),(4,14,2),(4,14,3). Rule 90 uses its own
unchanged local truth table. A positive Rule 30 argument still requires
the OR-specific gates; prefix grouping itself is rule independent.

For N=5,T=4,q=14 there are 35 possible prefix triples. Depth two adds
210 guarded gates, 940 circuit variables and 11,570 clauses after the
reachability encoding. Depth three adds 1,470 gates, 4,220 circuit
variables and 57,970 clauses. The reachability encoding is shared.

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_prefix_gate_encoding.py
```

Implementation: `construction/direct_dfa_prefix_gates.py`; counts:
`construction/direct-dfa-prefix-gate-encoding-regression.json`, under
`experiments/rule30/r1-zero-set-attack/`.

Independent odd-period review uses the full residues modulo 40 and 8,
without assuming the odd-part reduction. On 4,352 two-state models it
agrees with CNF projection: 2,039 accepted and 2,313 rejected; 48,764
full-residue states and 34,552 distinct gate tuples were checked. The
actual Rule 90 diagram also passes at T=40,q=8,d=3. Reproduce with
`construction/verify_prefix_odd_independent.py`.

## Bounded synthesis diagnostics (`M`)

The following runs use the complete centre-EP/masked-neighbour-aperiodic
predicate. They retain the ordinary all-coordinate gate checker and add
only necessary ordinary gate clauses after each candidate. All three
ended **UNKNOWN**, without a valid full diagram or an UNSAT proof.

| Full states | T | q | Suffix depth | Seconds | Candidates | New gate records | Final variables | Final clauses |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 4 | 14 | 3 | 60.0783 | 145 | 4,531 | 6,324 | 502,427 |
| 3 | 40 | 8 | 3 | 60.2622 | 1,849 | 45,640 | 5,984 | 91,949 |
| 5 | 4 | 14 | 4 | 60.2284 | 121 | 3,656 | 19,444 | 693,873 |

Every saved candidate satisfies its exact observation predicate and
uniform-prefix constraints, and fails an actual Rule 30 gate. Independent
replay rebuilt every formula, checked all candidate observations, and
checked every saved path/cube clause. The independently reconstructed
final CNF SHA-256 values, in table order, are

```text
e7f821c09a14eec28dbf0ed3e9bbc79f650fe9a8caa68781959bb7363e58be99
d9b9a34bf144e90dfbe4fe6e208d5b68145627f005ec3e7d3540f5670ec99f9e
179f2ca9e684e051f086ec0dc97f45f7d859daced0384f221f9945d9aa2bae7f
```

The old binary 180-second pool's 7,190 candidates all fail these shared
constraints: 7,188 at depth two and the remaining two at depth three.
The later canonical-clause pool's 5,576 candidates also all fail: 5,547
at depth two and 29 at depth three. These are finite diagnostics of
the encoding's pruning strength. They do not exclude the searched class
and do not substitute for a uniform proof.

```sh
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_prefix_cadical.py --kind binary --depth 3 --seconds 60 --output fresh-prefix-binary-d3.json.gz
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_prefix_cadical.py --kind odd --depth 3 --seconds 60 --output fresh-prefix-odd-d3.json.gz
uv run python experiments/rule30/r1-zero-set-attack/construction/direct_dfa_prefix_cadical.py --kind binary --depth 4 --seconds 60 --output fresh-prefix-binary-d4.json.gz
```

Saved pools are `direct-dfa-prefix-R30-N5-T4-q14-d3-60.json.gz`,
`direct-dfa-prefix-R30-N3-T40-q8-d3-60.json.gz`, and
`direct-dfa-prefix-R30-N5-T4-q14-d4-60.json.gz`, under the construction
directory. The independent checker is
`construction/verify_prefix_results_independent.py`.

## Scope

This construction concerns the full coordinate range of a specified
automatic model. It makes no bounded-window prediction of a neighbour
from centre history and does not infer an asymptotic statement from a
finite census. No R1 proof or kill has been obtained.

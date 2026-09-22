# The temporal-pair Markov extension obstruction

Date: 2026-09-09. Evidence: **U** (certificate framework and cycle
reduction), **C** (finite classifications and checked refutations).
This does not prove or kill R1.

The strongest result below is uniform: an alternating-centre observed
pair graph with temporal memory at most two cannot support the desired
aperiodic zero-set language together with full right extension, even
through an arbitrary sequence of different spatial graph types.

## 1. A finite certificate would construct a full diagram

Let a phase-labelled graph have vertices `s=(b,c)` and edges
`E_p(s,s')`, where `p=t mod 2`. Its paths specify adjacent temporal
columns. A right extension chooses a whole sequence `d_t`, requiring

```text
c_(t+1) = b_t XOR (c_t OR d_t),
E_p((c_t,d_t),(c_(t+1),d_(t+1))).
```

**U:** If every infinite graph path admits such an extension that is
again a graph path, one can repeatedly extend rightward and obtain an
entire right half-plane satisfying Rule 30. The already determined
columns agree at every stage. Left columns can then be reconstructed
from the exact inverse rule, giving a full diagram. This statement
preserves complete temporal correlations; it does not refresh exterior
bits independently at different times.

Two equal-length graph cycles based at the same vertex, with the same
periodic first-column word and different second-column words on its
zero phases, would supply an aperiodic zero-set trace: concatenate the
cycles according to any explicit aperiodic binary sequence. Distinct,
equal-length observable blocks preserve nonperiodicity, because an
eventually periodic concatenation would make its aligned block sequence
eventually periodic. This is a constructive sufficient certificate for
the broad diagram version of an R1 kill; finite left support is not
part of this framework.

## 2. Exact right-surjectivity check

At a source pair vertex `s`, retain the set `D subset {0,1}` of all
possible current right bits. Reading a source edge `s -> s'` updates
this set to

```text
D' = {d' : exists d in D,
      F30(b,c,d)=c' and E_p((c,d),(c',d'))}.
```

Start with both right-bit choices. An empty reachable set is an exact
finite obstruction to lifting that source path. If no empty set is
reachable, every finite source prefix has a compatible right extension;
finite branching gives an infinite extension by Koenig's lemma. This
is a complete finite check for the specified graph, including possible
extensions that need arbitrarily long future information.

The search requires every selected edge to have a successor edge.
Discarding vertices with no infinite continuation loses no infinite
path language, so this condition does not restrict the meaningful
certificate class.

## 3. Smallest failure and phase-independent classification

The largest pair graph permitted by the local pin already fails. Its
shortest unliftable path is

```text
(b,c) = (1,0), (0,0), (0,0),
or b=100, c=000.
```

The middle-column rule forces `d_0=1, d_1=0`. But the next pair
`(c,d)` violates the pin at time zero: a right-column 1 cannot fall to 0
while its left neighbour is 0.

Exhausting all 4,095 nonempty subgraphs of the 12 pin-legal transitions
gives 2,287 distinct nonempty graphs after removing dead vertices.
Exactly five are right-surjective. Using pair strings as vertices, their
edge sets are:

```text
{00->00}
{01->01, 10->10}
{00->00, 01->01, 10->10}
{00->00, 11->00}
{00->00, 01->01, 10->10, 11->00}.
```

Every path in these graphs is eventually constant. This completely
excludes the phase-independent, one-step pair-graph certificate class,
without a temporal-period cutoff.

## 4. Two temporal phases: online and exact offline certificates

The next search allowed separate unknown edge sets at phases 0 and 1.
It required two observable cycles of lengths 4, 6, and 8 with common
initial pair and first-column word `01` repeated.

The online sufficient certificate assigns `W_p(e,d)`, permitting a
right-bit choice after seeing one source edge. Every selected edge must
have a choice, and every selected choice must extend along every next
source edge. This stronger strategy condition was refuted first.

The exact offline search then discarded `W`. Each candidate graph was
checked by the complete subset construction above. For an unliftable
source path, the next SAT instance says: either remove a source edge,
or provide an entire compatible right-bit path. The fresh right bits
are existentially chosen separately for each obstruction. Thus these
refinements impose no online-strategy restriction. Nonblocking edges
ensure every enabled finite source path has an infinite continuation,
which makes every refinement necessary for right-surjectivity.

| Cycle length | Online variables / clauses | Offline refinements | Final offline variables / clauses | Result |
|---:|---:|---:|---:|---|
| 4 | 161 / 503 | 29 | 111 / 282 | UNSAT |
| 6 | 166 / 523 | 22 | 94 / 233 | UNSAT |
| 8 | 171 / 543 | 21 | 99 / 256 | UNSAT |

All six refutations have independently checked DRUP certificates.
The final CNFs also rebuild exactly from their recorded graph constraints
and counterexample paths. Another agent independently reviewed the
subset construction and conditional refinement encoding.

## 5. Why length four suffices for this specific graph class

**U:** For a phase-2, memory-one pair graph under the prescribed centre
`01`, sample the neighbour at the centre-zero times. Its two-step graph
has vertices 0 and 1 and only possible edges

```text
0->0, 0->1, 1->0.
```

The missing edge `1->1` follows from the Rule 30 pin at both microsteps.
An infinite path in this two-vertex graph can be aperiodic only if all
three edges are present: without `0->0`, its recurrent nonconstant part
alternates deterministically; without either crossing edge, every
infinite path is eventually constant. If all three edges are present,
the two closed walks `0->0->0` and `0->1->0` lift to length-four
microstep cycles with common initial pair and different zero-phase
neighbour words. They are precisely the witness already excluded by the
length-four offline certificate.

Consequently the exact length-four refutation excludes every aperiodic
zero-set path in this phase-2, memory-one, right-surjective graph class.
This conclusion does not extrapolate the table and does not apply to
graphs with hidden states or longer memory.

### Any centre period p: two macros suffice for this witness test

For a fixed centre word of period `p`, sample the pair graph every `p`
steps. Its only boundary state is the neighbour bit, so the resulting
macrograph has two vertices. Label each macro edge by the neighbour
word on the centre-zero phases during that macro; every label has the
same length.

**U:** If this labelled graph has an aperiodic observable path, it has
two equally long closed walks of length two macros, based at one vertex,
with different observable words. To prove the contrapositive, consider
the strongly connected component eventually visited by an infinite
path. A one-vertex component cannot have two different loop labels,
since repeating each loop twice would give the required witness. In a
two-vertex component, both crossing directions exist. Parallel edges
with different labels would also give different two-step return words,
by using one fixed return edge. Thus every directed edge type has one
label. With no self-loop, the path alternates and its labels are
periodic. With a self-loop labelled `A`, and crossing labels `C,D`, the
absence of two-step witnesses requires `AA=CD`. Equal label lengths
give `A=C=D`; any loop at the other vertex must have this same label.
The observable path is then constant at macro scale. This proves the
claim, including all transients between components.

The search therefore only needs cycle length `2p` for a memory-one
observed pair graph. Two additional exact offline runs gave:

| Centre word | Complete witness length | Refinements | Variables / clauses | Result |
|---|---:|---:|---:|---|
| `0111` | 8 | 57 | 219 / 554 | UNSAT |
| `0001` | 8 | 86 | 310 / 821 | UNSAT |
| `00111` | 10 | 125 | 432 / 1,151 | UNSAT |
| `011` | 6 | 41 | 161 / 403 | UNSAT |

All four final CNFs rebuild exactly and have checked DRUP refutations.
Longer witness cycles would be redundant for these graph classes.
The `00111` and `011` tests each had a declared 60-second/1,000-refinement
cap and stopped by refutation after about 0.013 and 0.003 seconds,
respectively, before the separate final proof check. They were selected
because the earlier zero-initial driven-halfline measurements did not
lock under these drives. Those measurements are not asymptotic claims;
these refutations exclude only the stated memory-one extension class.

### Alternating centre: arbitrary spatial types are also excluded

There is a stronger symbolic explanation for the alternating case.
Any aperiodic sampled-neighbour path in its two-vertex macrograph
requires the edge `0->0`, as shown above. That edge is a two-microstep
closed walk in the original graph, so repeating it gives an admitted
path with centre `01` and sampled neighbour `rho=000...`.

Suppose every path in this observed graph has a full Rule 30 right
extension, possibly by passing through different graph types at each
successive column. The repeated zero-sample path must then also extend.
But the existing [five-zero theorem](RESULTS-ladder-rung3-io-and-aperiodicity-audit.md)
forbids five consecutive zero samples under the alternating centre,
for arbitrary right-tail data. Its short proof is the forced two-step
chain `011 -> 001 -> 010 -> 000 -> first bit 1`.

**U:** This contradiction excludes every such certificate with a
phase-2, memory-one observed pair graph. The sequence of right-extension
types need not be spatially periodic or finite, and the target types
need not themselves have memory one. The essential limitation is the
observed graph's repeatable zero macro-loop together with full-path
right extension. It does not exclude a richer observed graph whose
additional state forbids long zero runs.

### Memory two: the same obstruction is uniform

The obstruction also excludes observed graphs whose vertices retain two
consecutive pair symbols and whose edges specify triples. No cycle-length
bound or restriction on the subsequent spatial graph types is needed.

**U:** Restrict the observed paths to centre `01`, and write a neighbour
triple as its three successive bits. The pin permits exactly

```text
phase 0: 000, 001, 010, 110,
phase 1: 000, 001, 011, 100, 101.
```

At an even time, retain both neighbour bits in the macro. The three
possible macrovertices are `A=00`, `B=01`, and `C=11`, with sampled
labels `0,0,1`. The only possible macroedges are

```text
AA, AB, AC, BA, BB, CA, CB.
```

These seven edges cannot be selected independently: they are obtained
by joining one permitted triple at each phase. In particular,

```text
CB present and BA present  =>  BB present.
```

Indeed, `CB` requires the phase-1 triple `101`, whereas `BA` requires
the phase-0 triple `010`. Together these two triples give `BB`.

If a zero-labelled cycle exists, its infinite repetition is an admitted
path with `rho=0` forever. Full-path right extension contradicts the
five-zero theorem. Therefore `AA`, `BB`, and the joint pair `AB,BA`
are forbidden in every extendible observed graph.

Consider a recurrent component containing `B`. Since `BB` is absent,
it must leave by `BA`. A return from `A` directly through `AB` gives
the forbidden all-zero two-cycle. The only other possible return must
pass through `C` and use `CB`; together with `BA` this forces `BB`,
again a contradiction. Thus `B` belongs to no recurrent component.
The remaining vertices `A,C` have only the crossing cycle `A<->C`.
Every infinite observed path is consequently eventually alternating in
its sampled neighbour, of period two.

**C:** The independent checker exhausts all `2^9=512` selections of the
legal observed triple edges. They give 80 distinct macrographs. Of the
512 selections, 232 admit a zero-labelled cycle. Among the other 280,
263 have no directed cycle, and 17 have exactly `A<->C` as their
recurrent edge set. The proof above, rather than an extrapolation in
memory or cycle length, establishes the uniform statement. These are
observed-language constraints only: the checker does not assert that
the 17 remaining graphs have full right extensions.

This explains why adding a second temporal symbol to the extension
search cannot yield an aperiodic certificate. It also shows why the
known `rho=(001)^infinity` torus needs additional observed state: its
memory-two local language admits a spurious indefinitely repeated zero
path. No contradiction is being asserted for the torus itself.

## 6. Rule 90 control and reproduction

Replacing the local rule with unchanged ladder Rule 90 passes the same
online certificate test. Its witness uses the full 32 phase-labelled
edges, with neighbour cycles `0010` and `0000` over centre `0101`.
The independent projection check reaches eight nonempty subset states.
The saved control has 201 variables and 647 clauses. Thus the certificate
framework can construct the expected additive countermodels; Rule 30's
OR/pin restrictions cause the refutations above.

From the repository root, recheck saved proofs without modifying them:

```sh
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --length 4 --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --length 6 --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --length 8 --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --length 4 --cegis --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --length 6 --cegis --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --length 8 --cegis --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --centre 0111 --length 8 --cegis --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --centre 0001 --length 8 --cegis --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --centre 00111 --length 10 --cegis --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_sat.py --centre 011 --length 6 --cegis --verify-existing
uv run python experiments/rule30/r1-isolated-column/markov_extension_census.py
uv run python experiments/rule30/r1-isolated-column/memory2_observed_graph_audit.py
```

Each saved-proof check also reruns the Rule 90 positive control and
checks both local truth tables against the unchanged ladder engine.
The engine SHA-256 is checked before use. The certificate directory is
`experiments/rule30/r1-isolated-column/markov-extension-certificates/`.
The memory-two observed-graph check also runs the unchanged
`controls.rule90_control` at `T=2,4,6,8,10`: every inverse map is
bijective and every constructed full-period torus verifies. Rule 90
allows all 16 observed triple edges and has no five-zero prohibition,
so the symbolic exclusion fails at its required OR/pin steps.

## 7. Honest scope

This work provides an exact finite certificate framework and refutes the
pair-graph classes specified above. It constructs no Rule 30 countermodel,
proves no general impossibility of a branching temporal law, and makes
no claim about arbitrary hidden-state graphs, temporal memory above two,
other centre words, or global cylinder horseshoes. R1 remains open.

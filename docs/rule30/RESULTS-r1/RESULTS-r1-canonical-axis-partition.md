# Complete finite observation partition after canonicalizing the time axis

Date: 2026-09-09. Intermediate construction machinery; **R1 remains open**.

The five-state binary construction's observation condition can be expressed
with **21,091 axes**, after choosing state names by time-axis
discovery order. This eliminates repeated observation refinements for that
fixed class. It does not decide the remaining Rule 30 gate constraints.

## 1. Canonicalization (`U`)

The two-dimensional MSB core has `N` states and transitions indexed by
paired binary digits `2*t_digit+x_digit`. Its time-axis transitions are
symbols `0,2`. Let `A` be the states reachable from state zero using only
these symbols, and let `R=|A|`.

Name states in `A` by breadth-first discovery, visiting symbols `0,2` in
that order. They become exactly `0,...,R-1`. Name the remaining core states
arbitrarily and permute every transition target and every output table by
the same bijection. All coordinates of the resulting diagram are
unchanged. Thus this is a class-preserving choice of representation.

This convention must **replace** the earlier canonicalization that visits
all four paired symbols together. Conjoining two incompatible naming
conventions would require a new proof and is not justified here.

For a fixed `R`, flatten the `R` rows of the two-symbol axis table. Its
initial zero transition is zero. A canonical table has two properties:

1. First appearances of targets occur in increasing target order.
2. Every target `v>0` appears before its own source row `v` is processed.

These properties characterize precisely the reachable breadth-first
tables. The second property implies reachability inductively from a
smaller source state; the first fixes the discovery names. Conversely,
breadth-first discovery has both properties.

The catalog generator recursively permits an existing target or the next
undiscovered target. It rejects a row whose source has not yet been
discovered and requires all `R` states to have been discovered at the end.
This is a finite exhaustive generation, with no appeal to measured counts
for its completeness.

## 2. CNF requirements for using the catalog

One possible exact encoding selects `R` from `1,...,N`. Conditional on it:

* Axis transitions from a source below `R` have targets below `R`.
* For every `v` with `0<v<R`, some axis transition from a source below `v`
  targets `v`.
* A transition targeting `v>=2` requires an earlier flattened transition
  targeting `v-1`.

These constraints are imposed only on the first `R` source rows. Axis
transitions at other core states remain free. Closure and the incoming
conditions prove that the actual axis-reachable set has exactly size `R`;
the first-appearance conditions give the catalog's naming convention.

Existing actual-coordinate Rule 30 path clauses remain necessary under
this change: their proof never used a naming convention. They may be
rebuilt using their semantic variable names. Literal numbers must not be
assumed stable if the new selector allocation changes numbering.

## 3. Exact observation clause (`U/C`)

For each canonical axis table use its own `R`-state bounds from the
[automatic-period lemma](RESULTS-r1-msb-automatic-period-bound.md):

```text
H_R=2^R,
P_R=2^R lcm(1,...,R).
```

The exact addition product lists all pairs of core states reached by
`n,n+P_R` for `n>=H_R`. In the period-four construction the observation at
`(4n+p,1)` appends two paired binary digits. The first has spatial digit
zero, so it is folded through the fixed axis table. The second is held
symbolically using the globally composed value

```text
V[p,q] = output[p,1,delta(q,2*(p mod 2)+1)].
```

For each distinct folded pair `a,b`, a shared selector can be true exactly
when phase `p` of the centre clock is zero and `V[p,a] != V[p,b]`.
Existential selector implications suffice: the clause below forces one to
be true when required. The exact clause for the axis is

```text
(some fixed axis transition differs)
OR (some eligible zero-phase folded pair has unequal composed outputs).
```

The guard fixes only the first `R` source rows' two axis transitions. The
catalog axis is reachable and closed, so this already fixes the actual
time-axis core, whatever transitions other states have. Final spatial-one
transitions and output labels remain free through `V`.

For the one matching canonical axis, the clause is equivalent to an
aperiodic zero-phase residue sequence. Every other guard releases its
clause. A finite interleaving is eventually periodic exactly when all its
residue sequences are, so this is also equivalent to aperiodicity of the
whole zero-set observation. All clauses together give the complete
observation condition for the stated finite construction class.

## 4. Computed catalog and checks (`C`)

| Reachable axis states | Canonical axes | Exact endpoint pairs | Largest addition product | Axes with no possible aperiodic output |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 18 | 1 |
| 2 | 4 | 11 | 78 | 2 |
| 3 | 45 | 282 | 227 | 6 |
| 4 | 816 | 9,206 | 549 | 24 |
| 5 | 20,225 | 357,453 | 1,250 | 131 |

Total: 21,091 axes and 366,953 endpoint pairs. The last column counts axes
whose folded-pair set is empty; it is not a count of Rule 30 models.

The independent breadth-first canonicalizer agrees with the generator on
every padded labelled binary and ternary table through three states. The
labelled table counts are `1,8,243` in base two and `1,32,6561` in base
three. The ternary canonical reachable counts are `1,24,2268`.

The complete binary catalog took 12.905 seconds on this run. Each record
contains its transitions, period/onset bounds, full endpoint relation with
exact integer witnesses, and folded pairs. The raw JSON-lines SHA-256 is

```text
7be472a0fb73fd918ab560862e8d1cb3b91b55128d62a8e134997865a0848ab9
```

Files:

* [Generator and canonicalizer](../../experiments/rule30/r1-isolated-column/canonical_axis_catalog.py)
* [Canonicalization regression](../../experiments/rule30/r1-isolated-column/canonical-axis-regression.json)
* [Complete catalog](../../experiments/rule30/r1-isolated-column/canonical-axis-b2-N5-T4.jsonl.gz)
* [Hash and count manifest](../../experiments/rule30/r1-isolated-column/canonical-axis-b2-N5-T4.jsonl.manifest.json)

```sh
uv run python experiments/rule30/r1-isolated-column/canonical_axis_catalog.py --build
```

The endpoint checker and its arbitrary-radix extension have independent
finite-product audits and unchanged Rule 90 controls. A new SAT encoding
of the axis naming constraints still requires its own independent audit
before using a result as a certificate.

## 5. Scope

This is exact finite parameter elimination within an automatic-diagram
ansatz. It is not a bounded-history predictor of the neighbour from the
centre, and it asserts no finite bound on general Rule 30 diagrams. No
Rule 30 counterdiagram, R1 proof, or R1 kill follows from the catalog alone.
No frozen engine was edited.

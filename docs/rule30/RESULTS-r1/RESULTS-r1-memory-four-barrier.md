# The observed memory-four barrier

Date: 2026-09-09. Evidence: **U** (finite-graph reduction),
**C** (complete finite certificate-class checks). This is an intermediate
restriction on a construction method; it neither proves nor kills R1.

## 1. Mechanism and kill condition

Fix an alternating centre `c=(01)^infinity`. A temporal-pair graph of
memory `m` permits phase-labelled windows of `m+1` consecutive pair
symbols `(c_t,r_t)`. On the observed boundary, the centre is fixed, so
each edge is specified by its phase and its `m+1` neighbour bits.

Suppose every infinite path in this observed graph has a full Rule 30
right extension. The extension may use different graph types of
arbitrary memory at successive spatial columns. Every such path must
obey the already certified eventual forbidden factors for
`rho_n=r_(2n)`.

The test enumerates every selection of the pin-legal observed edges,
forms its exact two-step macrograph, and examines each recurrent
strongly connected component. A component admitting a certified
forbidden factor is eliminated. The kill condition for this graph
class is that every remaining component has periodic observable paths.
This is a finite proof-criterion evaluation, not a census of temporal
necklaces or finite Rule 30 cones.

The scan caps were 60 seconds. Memory three completed in 0.051 seconds;
memory four completed in 0.375 seconds. No memory-five scan was run.

## 2. Why the test is uniform

**U — Recurrent forbidden factors.** If a factor occurs on a finite
path inside a recurrent component, one may precede it by arbitrarily
many closed walks in that component. Hence it occurs arbitrarily late
in an admitted infinite graph path. This contradicts full-path
realizability even when the imported factor theorem has a finite
burn-in. The maximum inherited burn-in is 23 macrosteps; no claim that
all factors are forbidden at time zero is needed.

**U — Exact periodic-label criterion.** For each vertex `v` of a
strongly connected component, run two independent synchronous walks
from `v`, retaining one Boolean flag that records a mismatch of their
observable labels. Reaching `(v,v,mismatch)` is exactly a pair of
equal-length closed walks with different observable words. Their
arbitrary concatenations would encode an aperiodic observable path.

Conversely, suppose no such pair exists. Fix a nonempty closed walk
at `v` with observable word `u`. For any other closed walk with word
`w`, the two equally long closed walks with words `u^|w|` and
`w^|u|` agree. Thus `w` is a prefix of `u^infinity`. Every finite
path from `v` can be closed back to `v`, so every infinite path from
`v` has observable word exactly `u^infinity`. An arbitrary infinite
finite-graph path eventually remains in one recurrent component.
Its observation is therefore eventually periodic.

This argument checks the observation itself. It does not infer
periodicity from absence of ordinary unlabelled graph branching.

## 3. Complete counts

The pin permits a neighbour transition with `r_t=1` only when
`r_(t+1)=1-c_t`. At memory three this gives seven legal quadruples
at each phase. At memory four it gives ten legal five-bit words at
phase zero and twelve at phase one. All subsets are checked.

| Observed memory | Legal phase edges | Edge selections | Acyclic | Every recurrent component forbidden | Only periodic surviving components | Live branching component |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 14 | 16,384 | 8,013 | 7,523 | 848 | 0 |
| 4 | 22 | 4,194,304 | 1,993,111 | 1,916,178 | 285,015 | 0 |

Memory three has four even-time macrovertices, namely neighbour words
`000,001,010,110`, and 640 distinct induced macrographs. Memory four
has seven macrovertices, the legal phase-zero four-bit neighbour words,
and 51,200 distinct induced macrographs.
Edges are obtained by joining the exact overlapping microstep windows;
the two phase-edge sets are not treated as independent macroedges.

The memory-three elimination only uses the factors
`00000`, `101001`, `010010001`, and `100010001`. Both scans read the
complete 57-factor list from `cumulative-factor-results.json`, whose
SHA-256 is
`bf773b8333368a0c65df55f3c9b8fcb620292bab259a32c751593d63e95679fd`.
The provenance and proof scope of these factors are recorded in
[the cumulative-factor report](RESULTS-r1-cumulative-factor-obstruction.md).

## 4. Reproduction and scope

The scripts and data are in `experiments/rule30/r1-isolated-column/`:

```sh
uv run python experiments/rule30/r1-isolated-column/memory3_observed_factor_audit.py
clang++ -O3 -std=c++17 experiments/rule30/r1-isolated-column/memory4_observed_factor_scan.cpp -o /tmp/rule30-memory4-factor-scan
uv run python -c 'import json; print("\n".join(json.load(open("experiments/rule30/r1-isolated-column/cumulative-factor-results.json"))["minimal_factors"]))' | /tmp/rule30-memory4-factor-scan
uv run python experiments/rule30/r1-isolated-column/observed_memory34_independent.py
uv run python experiments/rule30/r1-isolated-column/memory34_rule90_control.py
```

The memory-three producer compares a rebuilt result with its saved
artifact without overwriting it. The memory-four scanner writes its exact result to stdout;
the saved count and provenance record is
`memory4-observed-factor-audit.json`.

Combined with the existing memory-one and memory-two exclusions,
these checks exclude every phase-two observed temporal-pair SFT
certificate of memory at most four with an aperiodic zero-set path
and full-path right realizability. This applies even when the
subsequent extension types are arbitrary. It does not exclude hidden
states, memory at least five, other centre words, or nonsofic temporal
languages. In particular it does not decide realizability of the
branching component in the cumulative factor-avoidance graph.

The factor exclusions use Rule 30's OR saturation. They cannot be
imported into Rule 90, which has a full right-extension language and
realizes the all-zero sampled word. Independent replay passes in
`observed_memory34_independent.py` and its JSON artifact. That verifier
regenerates the overlapping microstep words, uses Tarjan components,
and tests label consistency on gcd-defined cyclic classes rather than
the producer's paired-return search. It reproduces all counts above.
The separate frozen-table control finds all 32 and 64 phase edges
legal for Rule 90 at memories three and four, respectively. Its full
temporal-pair graph extends by `N_t=L_t XOR M_(t+1)` and admits the
all-zero sampled trace. The unchanged `controls.rule90_control(6)`
passes at periods two, four, and six.

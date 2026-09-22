# R1 intermediate result: the Cantor return gap

Date: 2026-09-09. Evidence: **U** (exact infinite-row block identities),
**C** (frozen local checks), **R** (a return mechanism is still missing).
**No R1 proof or counterdiagram is obtained.**

There are two explicit continuous Rule 30 inverse branches between
proper closed subsets of right rows. They carry arbitrary binary spatial
data and have different initial neighbours. The following driven step
lands in a third set disjoint from the starting set, so these branches
do not provide the repeated choices needed for an aperiodic temporal
zero-set trace.

## 1. Exact positive construction (`U`)

Use the driven maps `G_a(x)_i=x_(i-1) XOR (x_i OR x_(i+1))`, with
`i>=1` and prescribed `x_0=a`. Number three-cell blocks by `n>=0` and
define closed Cantor sets

```text
S = { x : (x_(3n+1),x_(3n+2),x_(3n+3)) = (a_n,1-a_n,0) },
Y = { y : (y_(3n+1),y_(3n+2),y_(3n+3)) = (1,1,e_n) }.
```

Both data sequences `a` and `e` are arbitrary infinite binary sequences.
The OR term gives, at every block including the first,

```text
G_0(x)_(3n+1 .. 3n+3) = (1,1,1 XOR a_n XOR a_(n+1)).
```

Consequently `G_0(S)=Y`. For each target `e`, choose `a_0=b` freely and
recursively set

```text
a_(n+1) = 1 XOR a_n XOR e_n,
a_n = b XOR (n mod 2) XOR e_0 XOR ... XOR e_(n-1).
```

For each fixed `b=0,1`, this defines a continuous inverse branch from
`Y` onto `S_b={x in S:a_0=b}`. The inverse is continuous because each
finite source prefix depends on only a finite target prefix. The sets
`S_0,S_1` are disjoint and relatively clopen in `S`; each maps onto all
of `Y`, and their initial neighbour bits differ. This is an all-length
construction, not an inference from sampled rows.

The branches differ at both first cells of every three-cell block and
agree at the last cell. They do not differ at only finitely many sites.

## 2. The exact return failure (`U`)

Apply the next boundary bit one. For every `y in Y`,

```text
G_1(y)_(3n+1 .. 3n+3) = (b_n,0,0),
b_0=0,   b_(n+1)=1-e_n.
```

Thus `G_1(Y)=Z_0`, where `Z_0` is the closed set of all these rows with
arbitrary `b_1,b_2,...`. In particular,

```text
(G_1 o G_0)(S) = Z_0,    Z_0 intersection S = empty.
```

The disjointness already follows from the first block: `Z_0` starts
`000`, whereas a row in `S` starts `010` or `100`. A return at this
two-step scale is therefore impossible for this proposed starting set.
A longer return through other sets, or a different closed construction,
has not been supplied or excluded.

This is compatible with the
[full-cylinder covering obstruction](RESULTS-r1-cylinder-cover-obstruction.md).
Its dense eventually checkerboard targets never occur in `Y`, whose
blocks always begin with two ones. Moreover, `Y` and `S` are different
sets: having two inverse branches between them does not imply a
horseshoe on either set.

## 3. Checks, control and scope

The unchanged ladder truth tables verify every two-data-bit assignment
in both displayed block identities: 12 and 24 cell updates. An additional
finite calibration checks both inverse branches for every eight-bit
target, 512 branches and 12,288 forward cell updates. These checks
calibrate the symbolic identities; their finite length is not the proof.

Rule 90 fails the saturating first-block gate: for `a_0=0,1`, its first
output bits are respectively one and zero, whereas Rule 30 gives one
in both cases. The construction therefore uses OR saturation.

```sh
uv run python experiments/rule30/r1-isolated-column/cantor_branch_gate.py
```

Exact counts and engine hash are saved in
[`cantor-branch-gate.json`](../../experiments/rule30/r1-isolated-column/cantor-branch-gate.json).

Arbitrary spatial data and positive spatial entropy do not establish
aperiodicity of the neighbour as a function of time. The missing step is
an invariant return structure that permits repeated independent branch
choices with distinguishable temporal observations. This report makes
no such claim, and establishes neither a realization nor a refutation
of R1.

## 4. Further exact return gates (`U`, `C`)

The entire set S cannot return into S at any microtime t≥2 under any
finite prescribed boundary drive. Choose constant data a in S. Its
spatial tail is `010` or `100` repeated, which Rule30 sends first to
the all-one tail and then to the all-zero tail. The latter remains
zero outside the advancing boundary cone. No row in S has an eventually
zero tail. This excludes an invariant return of the entire S; it does
not exclude a suitable proper subset.

There is also an immediate four-step gate for every such subset. Write
a row of Z_0 in blocks `(b_n,0,0)`, with b_0=0, and put B=G_1∘G_0.
Direct substitution gives

```text
B(Z_0), block 0:       (1,b_1,b_1),
B(Z_0), block n>=1:    (0,(1-b_n)b_(n+1),b_n XOR b_(n+1)).
```

The later blocks never belong to `{010,100}`. A first coordinate zero
would require the block `010`; its middle coordinate one forces
`b_n b_(n+1)=01`, which makes its final coordinate one. Thus
`B(Z_0) intersection S` is empty, and no subset of the original S can
return to S after four driven microsteps.

For the six fixed even times below, a complete spatial-language check
strengthens this. It computes the actual Rule30 cone above every data
window that can influence one output block and retains precisely the
windows whose output block lies in `{010,100}`. Overlapping windows
form a finite directed graph. These constraints apply to every block
sufficiently far from the driven left boundary.

| Microtime | Data window length | Allowed windows | Recurrent vertices / edges | Possible periodic data tails |
|---:|---:|---:|---:|---|
| 2 | 3 | 4 | 2 / 2 | `01` and its shift |
| 4 | 5 | 0 | 0 / 0 | none |
| 6 | 5 | 14 | 4 / 4 | `0011` and its shifts |
| 8 | 7 | 40 | 4 / 4 | `0011` and its shifts |
| 10 | 9 | 104 | 0 / 0 | none |
| 12 | 9 | 170 | 0 / 0 | none |

Each recurrent strongly connected component is a simple directed cycle.
Every infinite path in a finite graph eventually stays in one recurrent
component; here its labels are then periodic. Consequently, at each of
these six specified times, every possible source in S that returns to
S has eventually periodic spatial data. There are only countably many
such right rows. Therefore no Cantor subset K of S can satisfy
`B^p(K) subset K` for p=1,...,6, and in particular no two-branch Cantor
return certificate inside S exists at those times. Boundary conditions
can only further restrict this necessary spatial language.

This is an all-length conclusion about each of six finite-radius spatial
constraints, **not** an extrapolation to untested return times. It does
not exclude longer returns, a union of different row languages, or a
different inverse-branch construction.

The certificate enumerates all 1,224 data windows over the six times,
checks 160,064 cell updates with unchanged `FWD[30]`, and independently
recomputes the same cones with the Boolean formula `l XOR (c OR r)`.
Each graph's strongly connected components are checked twice, by two-pass
graph traversal and by full transitive closure. The exact allowed words,
edges, cycles, and controls are in `cantor-return-languages.json`.

The identical S-return test under Rule90 has one two-cycle at each of
these six times (allowed-window counts 2,8,8,32,128,128). Thus this
particular short-return source class is also too restrictive for Rule90;
its exclusion is not a proposed mechanism for R1. The unchanged
`controls.rule90_control(6)` additionally passes.

```sh
uv run python experiments/rule30/r1-isolated-column/cantor_return_languages.py
```

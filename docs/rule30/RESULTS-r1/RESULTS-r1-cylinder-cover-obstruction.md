# R1 intermediate result: the cylinder-cover obstruction

Date: 2026-09-09. Evidence: **U** (uniform proof), **C** (exact inverse
gate and frozen controls), **K** (the specified construction is excluded).
**R1 and P1 remain open.**

For any finite prescribed centre word, two disjoint initial right-row
cylinders cannot both map onto a set containing the same nonempty target
cylinder. This excludes the proposed two-branch, full-cylinder horseshoe
at every prefix length and return time. The mechanism is a Rule 30 inverse
reset: every eventually checkerboard target has at most one preimage,
and these targets meet every cylinder.

## 1. Exact statement

Let `X = {0,1}^{N>=1}`, and let `[u]` denote the initial-prefix cylinder
specified by the finite binary word `u`. The empty prefix gives `X`.
For a prescribed boundary bit `a`, define

```text
G_a(x)_i = x_(i-1) XOR (x_i OR x_(i+1)),  i >= 1, x_0 = a.
```

Let `H = G_(a_(p-1)) o ... o G_(a_0)` for any `p>=1` and any drive word.
There do not exist disjoint cylinders `[u_0]`, `[u_1]` and a nonempty
cylinder `[v]` such that

```text
[v] subseteq H([u_0]) intersection H([u_1]).
```

The theorem does not require `[u_0]` and `[u_1]` to lie inside `[v]`.
In particular, it excludes that stronger arrangement, even before asking
for distinguishable neighbour observation blocks.

## 2. The inverse reset (`U` plus a four-state `C` gate)

From a target row `y` and a right input pair `(x_i,x_(i+1))`, Rule 30
determines the next pair to its left:

```text
x_(i-1) = y_i XOR (x_i OR x_(i+1)).
```

Encode a pair `(l,c)` as `2*l+c`, in the order `00,01,10,11`.
The backward maps for target bits zero and one are

```text
f_0 = [0,2,3,3],   f_1 = [2,0,1,1].
```

For a spatial output word `y_i...y_(i+3)=1010`, the corresponding
composition is

```text
f_1 o f_0 o f_1 o f_0 = [1,1,1,1].
```

Thus the output block forces `(x_(i-1),x_i)=01`, independently of
`(x_(i+3),x_(i+4))`. Once this pair is fixed, the deterministic inverse
recurrence determines every input cell to its left. The word `1010` is
a shortest reset word: no output word of length at most three resets all
four states. The other length-four reset word is `0010`, resetting to
pair `11`. This minimality is only a four-state automaton statement.

**Unique-preimage lemma (`U`).** If `y` is eventually spatially alternating,
then for each boundary bit `a`, it has at most one preimage under `G_a`.
Any existing preimage is eventually the same checkerboard tail.

*Proof.* Arbitrarily far to the right, `y` contains the block `1010`.
Each such block fixes an inverse pair and hence the entire input prefix
to its left. Two putative preimages therefore agree on every finite
prefix. Moreover, at each sufficiently large index `i` with `y_i=1`, the
reset gives `x_(i-1)=0` and `x_i=1`. These pairs cover the whole tail, so
that tail agrees with `y`. The prescribed boundary may prevent the
preimage from existing, which does not affect uniqueness. QED.

A direct frozen-engine check confirms the phase: ordinary Rule 30 fixes
both spatial checkerboards, since `F(1,0,1)=0` and `F(0,1,0)=1`.

**Composition lemma (`U`).** The same at-most-one-preimage statement holds
for `H`, for every eventually alternating target. Apply the previous
lemma to the last step. Its unique possible predecessor is itself
eventually alternating, so the preceding step also has at most one
predecessor. Induction through the finite drive proves the claim.

**Cover obstruction (`U`).** Every cylinder `[v]` contains an eventually
alternating row: append either checkerboard after `v`. If two disjoint
source cylinders both covered `[v]`, such a row would have two distinct
`H`-preimages, contradicting the composition lemma. QED.

## 3. Why covering would have been a valid construction gate

Had two disjoint compact subcylinders of `[v]` both covered `[v]` under a
periodic return map, repeated inverse choices and compactness would give
an orbit for any binary itinerary. If the two branches forced distinct
equal-length zero-set observation blocks, a suitable aperiodic itinerary
would give an aperiodic zero-set neighbour. The failed step is the
covering condition, uniformly, rather than the compactness argument.

For comparison, covering itself has an exact finite verification method
at any fixed drive length `p`: the `p`-step cone is a finite input/output
transducer, retaining the last `2p` initial bits in the bulk, with a finite
startup for the prescribed left boundary and source prefix. Determinizing
its possible input states along output prefixes decides whether an output
prefix has a lift. A reachable empty subset supplies a finite failed
target prefix; if no empty subset is reachable, compactness supplies a
lift of every infinite target. This uses consistent initial rows and all
intermediate Rule 30 tiles. It does not refresh exterior bits separately
at different times. The uniform reset proof makes a search for two
full-cylinder covers unnecessary.

## 4. Rule 90 control (`U` and `C`)

For Rule 90 the driven equation is `y_i=x_(i-1) XOR x_(i+1)`. Given any
infinite target `y` and any boundary `a`, choose `x_1` freely and then set

```text
x_(i+1) = y_i XOR x_(i-1),  i >= 1.
```

Both choices work, and give exactly two preimages. Consequently, with
constant zero boundary, the disjoint cylinders `[0]` and `[1]` each map
onto `X` in one step. Their time-zero neighbour bits differ. Rule 90
therefore passes precisely the covering gate that Rule 30 fails. Its
inverse pair maps are permutations, so no composition has a reset word.
The distinction uses Rule 30's OR saturation.

The verifier checks the two inverse maps against the unchanged ladder
truth tables, all 30 nonempty binary words of length at most four for
each rule, and all 64 six-cell Rule 30 inputs for the output word `1010`.
Exactly four such inputs survive, all with initial pair `01`.
For Rule 90 it checks both inverse branches for all 256 eight-bit target
words and both boundary bits: 1,024 branches and 8,192 frozen forward
cell updates. These finite checks calibrate the symbolic infinite-row
recursion. The unchanged `controls.rule90_control(6)` also passes.

Run from the repository root:

```sh
uv run python experiments/rule30/r1-isolated-column/cylinder_cover_obstruction.py
```

The exact maps, reset witnesses, counts and frozen engine hash are in
[`cylinder-cover-obstruction.json`](../../experiments/rule30/r1-isolated-column/cylinder-cover-obstruction.json).

## 5. Honest scope

This is a uniform obstruction to full-cylinder covering branches for
any finite driven Rule 30 map. It is stronger than a finite prefix or
return-time census. It is compatible with the previously established
[periodic cylinders](RESULTS-r1-periodic-cylinders.md), whose return
images are **contained in** their source cylinders: containment does not
supply two covering inverse branches.

A horseshoe on a proper closed subset remains outside this theorem:
its relative target cylinders may exclude every eventually alternating
row. The result does not exclude aperiodic neighbours under periodic
centres, and does not impose finite-left support on any diagram. It
neither proves nor kills R1. No bounded centre-history determination,
fixed-radius observable invariant, or finite-window decision about an
unknown eventually periodic word is asserted.

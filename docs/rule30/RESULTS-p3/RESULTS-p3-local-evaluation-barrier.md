# A quadratic barrier for literal lazy center evaluation

Date: 2026-09-13. Status: an all-length theorem for an explicit local
derivation model, with an exact certificate checker. **Not a P3 lower bound.**

Plain lazy evaluation cannot provide the missing single-seed shortcut.
Even if it memoizes every cell, chooses its evaluation order adaptively, and
short-circuits every local Boolean inference as soon as possible, it needs
quadratically many distinct cell inferences. The statement concerns one
generation at a time; it leaves dyadic jumps, exact seed-specific identities,
and other algorithms open.

This closes a concrete alternative to the previously measured
[Hashlife approach](RESULTS-hashlife-center.md) without rerunning Hashlife,
compression probes, or a scaling benchmark. The repository's operational P3
target remains one uniform `o(n)` algorithm on binary input n; see the
[scope audit](P3-SCOPE-AUDIT.md).

## 1. The permitted facts and inference rule

Write u(t,x) for the singleton-seed Rule 30 cell at time t and position x.
The evaluator may use these facts for free:

```text
u(0,x) = 1[x=0],
u(t,x) = 0 when |x|>t,
u(t,-t) = u(t,t) = 1.
```

The last facts follow inductively from `f(0,0,1)=f(1,0,0)=1` and the
quiescence identity `f(0,0,0)=0`.

For every other cell, the permitted inference is the one-generation gate

```text
u(t,x) = f(u(t-1,x-1),u(t-1,x),u(t-1,x+1)),
f(l,c,r) = l XOR (c OR r).
```

The evaluator can determine parents in any adaptive order and omit any
parents once the local truth table fixes the result. Memoized parents cost
no second inference. However, the inference must be valid for every setting
of its unexamined parent bits. An additional identity relating distinct
seed-reachable cells is not an instance of this inference rule.

A **local derivation** is the resulting acyclic graph, with a node for each
distinct cell whose value is used. Every nonfree node carries a subset of its
three parents and a truth-table certificate that their values force its
output. All facts and preprocessing needed by the query belong to this graph.
The size charged below counts only distinct nonfree nodes. This gives the
evaluator full credit for memoization and free boundary recognition.

## 2. Every local inference has two distinct necessary directions

**Local certificate lemma.** Every partial assignment forcing the value of
f specifies l and at least one of c,r.

Proof: if l is unspecified, flipping it flips f while holding c,r fixed, so
the value is undetermined. If only l is specified, choosing `(c,r)=(0,0)`
or `(1,0)` gives opposite outputs. Hence a forcing partial assignment must
specify the left parent and at least one other parent. Conversely an OR
value of one can be certified by either one-valued OR parent; an OR value
of zero needs both. The proof allows every local decision-tree policy, not
only the usual left-first program.

The verifier exhausts the complete 27-element set of partial assignments
`{unknown,0,1}^3`. This is a complete local certificate, independent of the
query horizon or of a sample of Rule 30 rows.

## 3. Quadratic growth in the upper half of the query cone

**Theorem.** For every n>=0, every local derivation of u(n,0) in the above
model contains at least

```text
(k+1)(k+2)/2 distinct nonfree inferences,
k = floor((n-1)/2).
```

For n=0 the expression is zero. As n grows it is `n^2/8+O(n)`.

Proof: let S_j be the positions of all used cells at time n-j. Every
dependency changes position by at most one, so `S_j` is contained in `[-j,j]`.
When `j<=k`, we have `n-j>j`: every site of S_j is strictly inside the seed
cone, and no initial, exterior, or edge fact applies.

The root gives `S_0={0}`. For a nonempty S_j in this strict interior, the
local lemma forces every position in

```text
S_j - 1 = {x-1 : x in S_j}
```

into S_(j+1). This set has |S_j| elements. Let m be the largest position of
S_j. The node at m also needs its center or right parent, at position m or
m+1. Either lies strictly to the right of the largest position m-1 in
`S_j-1`. Consequently

```text
|S_(j+1)| >= |S_j|+1.
```

Induction gives `|S_j|>=j+1` for `0<=j<=k`. These time layers are disjoint,
and all their nodes are nonfree. Summing proves the bound. No assumptions
about independence, randomness, or values along the singleton orbit enter
the argument.

This is a quadratic lower bound on the number of individual local cell
inferences. It is also a time lower bound for the literal evaluator that
executes one such inference per operation. A bit-parallel batch operation,
a multi-generation identity, or a different uniform algorithm is not charged
by silently expanding it into these operations; its own construction and
cost need separate analysis.

The bound survives a stronger hypothetical boundary oracle. If every cell
within distance w(n) of either seed-cone edge is supplied for free, replace
k by `max(-1,floor((n-w(n)-1)/2))`. For w(n)=o(n), the local inference count remains
quadratic. Thus adding finitely many explicitly solved edge stripes cannot
make this evaluator sublinear.

## 4. Why the theorem is not a fixed-sequence lower bound

Rule 90 gives an exact adversarial control. Its gate `l XOR r` satisfies the
same local lemma, so the identical geometric proof gives the same quadratic
local derivation bound for its singleton center query.

But that center bit equals zero for every n>0. To prove this, write its
evolution as the sum of left and right shift operators over F_2. At each
binary digit of n, the Frobenius identity leaves a choice of displacement
`+2^j` or `-2^j`. For n>0, the largest such power is greater than the sum of
all smaller powers present. No resulting displacement can be zero, so no
term contributes to the center. The n=0 value is one. This gives an exact
algorithm using at most O(log n) work even when reading and validating the
whole binary input.

Thus the theorem cannot establish the prize claim: it excludes a derivation
system that also misses a known exact shortcut. Its use is sharper than a
runtime fit: every possible evaluation policy within that system is already
covered, at every horizon.

## 5. The precise diagonal jump that escapes the local rule

There is an exact way to batch the forced-left chain. For any 0<=L<=t, put

```text
P_L(t,x) = XOR_(j=1)^L [
  u(t-j,x-j+1) OR u(t-j,x-j+2)
].
```

Repeatedly substituting the local recurrence gives

```text
u(t,x) = u(t-L,x-L) XOR P_L(t,x).
```

This identifies the required aggregate exactly; it does not posit an
undefined seam correction. It also shows how strong its computation would
have to be. For n=2m the maximal free-endpoint center jump has

```text
u(2m,0) = 1 XOR P_m(2m,0),
```

while for n=2m+1 it has

```text
u(2m+1,0) = P_(m+1)(2m+1,0).
```

The first endpoint is the known left edge `(m,-m)`; the second is the known
exterior cell `(m,-m-1)`. Therefore the whole jump parity is already the
target bit, up to a known constant. Replacing the gate chain by an oracle
for this parity simply restates the center query. There is also a concrete
construction-cost consequence. Suppose the parity algorithm first obtains
local parent facts sufficient to determine each individual OR term, using
M nonfree cell inferences. Starting from the known endpoint, at most L
additional gate inferences recover the entire forced-left chain and the
original query. Thus

```text
M + L >= (k+1)(k+2)/2,
```

and M remains quadratic. Avoiding the chain nodes while separately evaluating
all its OR terms therefore cannot provide a sublinear shortcut either.

What could change the result is an independently executable composition law
for these parities or a different aggregate, using cancellations or actual
seed-reachable relations without producing the individual parent facts.
No such law or complexity bound is established here. This is the exact
boundary between a new algorithm and an uncharged diagonal-parity oracle.

## 6. Exact verifier and bounded controls

The verifier accepts an arbitrary supplied local derivation graph; it does
not consult or trust a policy label. It checks:

- every seed, exterior, and edge fact;
- each inference against all completions of its unexamined parents;
- all parent coordinates and values, and strict temporal descent;
- reachability of every charged node from the requested center;
- the layer expansion argument and distinct-node lower bound.

The saved run checked all 27 local partial assignments for each of Rules30
and90, 242 finite-set instances of the elementary expansion inequality, and
14 complete derivations for the single horizon n=17: six parent orders and
one cache-aware adaptive order for each rule. Their answers matched a
separate whole-row control. A missing left dependency, a false boundary
value, and a false center value were each rejected. The run took about
0.03 seconds. These controls test the verifier; they are not the source of
the all-length bound or an empirical exponent estimate.

An independent review reproduced the 54 local partial-assignment checks,
validated the saved arbitrary derivation and the n=0,1,2 boundary cases,
and checked both the geometric proof and the `M+L` diagonal argument.

Files:

- [Verifier and arbitrary-policy derivation interface](../../experiments/rule30/p3_local_evaluation_barrier.py)
- [Complete local certificate and bounded controls](../../experiments/rule30/p3-local-evaluation-barrier.json)

To reproduce these small checks:

```sh
uv run --offline --no-project python experiments/rule30/p3_local_evaluation_barrier.py --output /tmp/p3-local-evaluation-barrier.json
```

To validate a separate local derivation, use the `--derivation PATH` option.
The JSON format is documented by the saved `example_derivation`: each node
stores its time, position, value, and the indices of its queried parents.

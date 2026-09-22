# Exact original-variable counting across a spatial cut

Date: 2026-09-11. **The proposed cumulative inequality is still unproved and
unrefuted.** This continuation supplies a new exact counting engine, a proof
of its chronological-ancestry invariant, and complete continuation trees for
seven specified original history classes. It does not improve the existing
necessary upper bound `epsilon <= 1.4176025745...` when `c=1`.

The methodological gain is that these trees can be counted without listing
the originals or listing every intermediate endpoint. For example, the
length-35 class with history `000111000` contains 2,248,825,019,423,562
originals. Its entire continuation tree has 161 nonempty history classes.
The new engine counts all of them, and all paths terminate by the twentieth
successful update. This is an exact **finite, restricted** result. It is not
mortality for all original words of length 35, much less for all lengths.

All words are auxiliary reconstruction states. No singleton-seed reachability
is asserted. The focused period-two/P1 question remains open; these results
do not address arbitrary periods or P2.

## 1. An exact seam identity with every guard retained

Fix original length r, and let x range over the same m=2r-1 free original bits
throughout. The original high bit a_0 is the constant one. For a chronological
tape alpha, maintain Boolean functions

- K_alpha(x), whose satisfying assignments are exactly C_r(alpha);
- W_alpha(x), a symbolic word of length r+|alpha| which is the actual endpoint
  whenever K_alpha(x)=1.

Values of W_alpha away from K_alpha=1 have no mathematical meaning. They may
be kept as formal Boolean values, but never become new original assignments.
Initially K_empty=1 and W_empty is the original legal word.

Take any cut k with 1<=k<=L, where L is the current length, and a prescribed
next scalar s. Scan the first k symbols from the actual origin state (0,0,0).
Call the resulting pair at site k-1 `(p_u,p_v)`. Independently require the
output pair at site L-1 to be `(s,s)`. For each site i, right-to-left transport
of a proposed output pair `(u_i,v_i)` is

\[
 u_{i-1}=u_i\oplus(v_i\lor a_i),\qquad
 v_{i-1}=v_i\oplus(a_{i-1}\lor b_i).                 \tag{1}
\]

Apply (1) for i=L-1,...,k. It yields the uniquely required pair `(q_u,q_v)`
at site k-1. Define

\[
 K_{\alpha s}
 =K_\alpha\,[p_u=q_u]\,[p_v=q_v].                    \tag{2}
\]

The new symbolic word consists of the forward outputs on sites 0,...,k-1,
the right-transported outputs on sites k,...,L-1, and the appended symbol
`3-s`.

**Exact ancestry theorem.** For every r, every finite tape, and every sequence
of legal spatial cuts, (2) and this word construction preserve both invariants
above. In particular,

\[
 \boxed{|C_r(\alpha s)|
   =\sum_{x\in\{0,1\}^{2r-1}}
       K_\alpha(x)[p_u(x)=q_u(x)][p_v(x)=q_v(x)].}       \tag{3}
\]

**Proof.** For a fixed input symbol and its preceding input high bit, one
scan step is a bijection on its two incoming accumulator bits. Solving its
two XOR equations gives exactly (1). Thus the actual left scan and the scan
ending in `(s,s)` describe the same full bulk output if and only if their
pairs agree at the cut. Agreement is equivalent to the successful guard
with emitted scalar s. Intersecting this condition with K_alpha keeps every
earlier guard. On that intersection the joined output is the actual output,
including the prescribed appended symbol. Induction starting with the legal
original variables proves the claim. Summing its indicator proves (3).

This specializes the existing arbitrary-cut composition viewpoint to a
single successful update and makes its original-variable bookkeeping explicit.
It is an identity, not an information estimate. The two seam equalities need
not be independent, and may already follow from K_alpha. Changing the cut
does not supply any fresh completion or weaken a chronological guard.

## 2. Exact Boolean decision diagrams

The native engine represents K and every word bit by a reduced ordered binary
decision diagram. There are exactly m original variables; later birth cells
and history bits introduce no variables. Shannon decomposition, a unique-node
table, and Boolean AND/OR/XOR operations implement (1)-(2). Garbage collection
retains K and every current word field. Operation-cache eviction changes no
Boolean function.

Counting includes every skipped original variable. If a node at variable level
i has children at levels j_0,j_1, its count below level i is

\[
 2^{j_0-i-1}c_0+2^{j_1-i-1}c_1.
\]

Terminal levels are m, with terminal counts zero and one; the root's count
is multiplied by 2 to the power of its level. This counts assignments over
the fixed original domain, rather than assignments to a new current frontier.

Both possible next scalars are explored at every nonempty continuation node.
A tree is complete only when every such branch either has been explored or
has zero original assignments. At a node alpha,

\[
 |C_r(\alpha)|-|C_r(\alpha0)|-|C_r(\alpha1)|
\]

is the number of originals whose next update fails. These differences are
nonnegative and sum to the entire root weight for each completed tree.

The implementation supports 1<=r<=63 and histories of at most 60 symbols.
These are computational limits, not restrictions on the identity (3).
Counts use unsigned 128-bit integers, sufficient for at most 125 free original
bits. The candidate comparison uses an exact shifted threshold, avoiding
overflow in the product `|C|*2^D`. No floating-point estimate certifies a count
or inequality.

## 3. Complete, selected original-history trees

The saved computation obtains the following complete trees. N and D include
the prescribed nine-symbol prefix. Maxima in a row need not occur on the same
tape. The first two rows are controls reproducing earlier endpoint results.

| r | Prescribed prefix | All original ancestors at root | Nonempty tree nodes | Maximum N | Maximum D |
|---:|:---|---:|---:|---:|---:|
| 22 | `000111111` | 14,955,516 | 10 | 17 | 14 |
| 24 | `000111000` | 380,628,720 | 15 | 20 | 15 |
| 29 | `000111000` | 667,110,554,910 | 34 | 17 | 11 |
| 32 | `000111000` | 36,977,226,550,344 | 83 | 18 | 13 |
| 35 | `000111000` | 2,248,825,019,423,562 | 161 | 20 | 13 |
| 29 | `000111111` | 792,254,285,262 | 36 | 19 | 13 |
| 32 | `001110000` | 38,168,795,487,780 | 75 | 17 | 12 |

Every listed node passes `|C_r(alpha)|*2^D <= 2^(2r-1)`. Empty descendant
classes satisfy it trivially, so this checks every finite continuation of
each listed root. It supplies no conclusion about other nine-symbol roots
at the same r, other r, or a uniform rate as D grows.

Two selected complete original counts have an additional endpoint-fiber check:

| r | Full prescribed tape | D | Exact original ancestors |
|---:|:---|---:|---:|
| 32 | `000111000011100000` | 13 | 8,839,609,056 |
| 35 | `000111000011000000` | 13 | 1,239,750,743,616 |

For r=32 all these originals reach the same endpoint after the first nine
successful updates:

```text
30312121310303131021322121310303203030303
```

For r=35 they reach exactly two such endpoints, with the indicated weights:

```text
21320303203103210321032222121310303203030303   293998812408
21320303203103210321030322121310303203030303   945751931208
```

Each weight is independently recomputed from original prefixes using the frozen
oracle, without the BDD engine, its seam construction, or a copied accepting
signature. The oracle also replays an explicit original representative through
the entire target tape. All originals in a given nine-update endpoint fiber
then share its deterministic continuation. The two r=35 weights sum exactly
to the whole BDD count; the endpoint classes are disjoint. The artifact retains
the representatives, independent count records, and all tree-node counts.

These are compressed exact counts. Billions or trillions of originals were
not individually replayed.

## 4. Maintained verifier and limits

- [guarded_history_bdd.cpp](../../experiments/rule30/guarded_history_bdd.cpp)
- [guarded_history_bdd.py](../../experiments/rule30/guarded_history_bdd.py)
- [guarded-history-bdd.json](../../experiments/rule30/guarded-history-bdd.json)

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/guarded_history_bdd.py
```

The wrapper compiles the native source in a temporary directory. It checks
exact membership and endpoint words against `panel/cert33.py` on all 170 legal
originals of lengths 1-4, using both extreme initial cut positions. This small
regression validates the new symbolic engine; it is not another run of the
old length-12 census. It also checks empty-prefix handling and that an
interrupted prefix count cannot be mislabeled complete.

For r=22 and r=24, every earlier endpoint weight is independently recomputed
with the frozen oracle, and every resulting history count is compared with
the new complete tree. A separate common-graph transfer computation checks
all seven nine-symbol root counts. Each four-term uint64 sum is checked for
overflow beforehand; summing the whole array in uint64 would be unsafe at the
larger original lengths and is not done. The three new selected endpoint
fibers are independently counted as described above.

Native caps are two million nodes per BDD manager, four million simultaneously
live nodes, three million operation-cache entries with exact eviction, 5,000
tree nodes, 60 history symbols, and normally 35 seconds per invocation. A cap
is explicitly incomplete. The default wrapper has a 120-second overall budget
and writes its completed artifact only after every required verification
passes. Source hashes include the unchanged frozen oracle. No GPU, paid
compute, or singleton-seed generation is used.

Several spatial cuts exhausted the native caps before constructing the
length-35 root. Cut 11 completes it; this affects computational complexity
only. A separate attempted root `(r=35, prefix=001111111)` was not completed
by the exploratory runs and has no asserted ancestor count or mortality bound.
Partial counts at shorter prefixes must not be reported as counts of that root.

## 5. What this continuation did not establish

The new counter operates on the unrestricted original variables, repairing
the practical limitation of investigating only fixed-high or fixed-low
families. Nevertheless, none of these selected trees improves the earlier
length-24 obstruction to stronger exponents. The length-24 count
55,885,140 at D=15 remains the strongest obtained restriction on epsilon
when c=1; see the [weighted endpoint report](RESULTS-weighted-history-endpoints.md).

Equation (3) alone gives no bound on how much information its successive
intersections acquire. In particular, it does not justify charging a new bit
to each repeat. The documented plateaus, synchronization after r successes,
and switch-dependent refilling remain obstacles to such an argument.

Thus the all-length positive-rate information bound, finite-frontier
mortality for arbitrary legal auxiliary starts, and the resulting exclusion
of eventual period two in the center column all remain unresolved. The new
work is an exact counting mechanism and restricted certificates, not a proof
of the research target.

# A real block jump, with its boundary construction charged

Date: 2026-09-13. **An exact fused section compiler and a Q^k core jump are
implemented. They do not give a sublinear Rule 30 algorithm.** Unlike the
previous evaluator's loop over single input bits, this compiler handles an
entire input block as one finite-state transduction of the shared word
expression. Its cost includes the block states it constructs.

The crucial limitation is proved for this particular implementation: taking
one giant block in its explicit-context recursive protocol costs at least
quadratic bit work on the actual query. This is not a lower bound against
compressed contexts, different query quotients, or general algorithms.

## 1. Exact block action and section

Let U be a chronological word in A,B,C, represented by the existing SLP.
For b>=1 and 0<=x<2^b, the compiler computes

```
action(U,b,x)  = U(x) mod2^b,
section(U,b,x)= U|_x,
```

where x denotes the b input bits in low-to-high order. The defining identity
for every higher tail z is

```
U(x+2^b z) = action(U,b,x) + 2^b section(U,b,x)(z).       (1)
```

On one generator, the block action is its exact integer formula followed
by truncation. For b>=2, its section depends only on the two highest input
bits in that block: if these two bits represent the ordinary integer
0,1,2,3, respectively, the sections are A,B,C,C. The raw automaton memory
stores the last two **input** bits and has forgotten its starting state.
The one-bit case uses the original section table.

At a concatenation UV, the exact recursion is

```
y = action(U,b,x),
action(UV,b,x)  = action(V,b,y),
section(UV,b,x)= section(U,b,x) section(V,b,y).           (2)
```

The second child receives the first child's complete ordered output block.
The compiler does not replace it by a parity, a new zero block, or a guessed
independent completion. Structural induction proves (1)-(2).

An action-only final call avoids constructing a section that the answer
will never use. A general center query consumes the singleton input in
blocks, starting with a block whose low bit is1 and continuing with zero
blocks, and reads the appropriate bit of the final action.

## 2. One call computes any finite number of Q updates

The [bulk-core proof](RESULTS-p3-bulk-core-formula.md) establishes the literal
word identity

```
(U A^k)|_(0^(2k)) = A^k Q^k(U).                        (3)
```

The method `BlockSections(arena).q_jump(node,k)` therefore constructs A^k
by binary concatenation, takes one block section of U A^k at width2k and
input zero, and removes the first k output letters by SLP length metadata.
There is no loop over k core updates in this method. It computes the exact
word Q^k(U), with the full chronological boundary retained. All prefix
cutting, expression construction, and transduction work is recorded.

This is a real executable bulk operation, rather than an unevaluated symbol
for Q^k. It can nevertheless perform many recursive calls internally.

## 3. What the compiler costs

For a fixed block width b and an input graph with s reachable nodes, there
are at most s*2^b distinct node/input-context pairs for each of action and
section. Memoization visits only needed pairs and constructs no initial
2^b-entry quotient table. This bounds the number of recursive contexts;
it is not a unit-cost bit-time bound. Each explicit block integer can have
b bits, and arithmetic, hashing/comparison, graph allocation, and lookup
must be charged in the chosen machine model.

The implementation records action and section requests, distinct contexts,
leaf actions, their operand-bit sum, grammar nodes, and prefix cuts. It
also avoids a hidden large zero allocation: it builds a b-bit truncation
mask only if the actual result overflows b bits. Reading the two highest
input bits also returns A immediately when the explicit value is too short
to reach them.

As a control, the compiler computes Q^k(A^L)=A^L for
L=2^40+3 and k=2^36+7 using86 grammar nodes and one explicit leaf action.
It creates no L-letter word, 2k-bit zero buffer, or enormous modulus. This
known fixed family shows that the implementation really can skip a huge
number of updates on a compressible input. It is not a Rule 30 center
shortcut.

## 4. Why one giant block is still expensive on the actual query

Specify the protocol carefully: an SLP is evaluated recursively by (2),
its boundary values are explicit binary integers, and leaf transitions
are evaluated by their exact A/B/C bit operations. The only skips are
memo hits for identical node, width, and input value. A direct formula for
an arbitrary power or a lazy compressed boundary representation would be
a different algorithm and is outside the following result.

**Proposition.** Evaluating A^n on the singleton1 with one block of width
n+1 by this protocol requires Omega(n^2) bit work.

Proof. Let r=floor(n/2). Before each of the first r leaf transitions,
the input is A^t(1), 0<=t<r. Its highest one is at position2t and it has
not yet been truncated. These input values are all distinct. Consequently
no earlier same-context memo entry can skip those transitions. Their
materialized input sizes sum as

```
sum_(t=0)^(r-1) (2t+1) = r^2.
```

Their bit shifts and Boolean operations therefore require Omega(n^2)
work, even if leading zeros are omitted. This argument is independent of
the word's binary parenthesization.

The Q^k jump has the same problem. If U begins with C, then the first i
letters of U A^k send zero to a value with highest one2i-1, for1<=i<=k.
This follows because C(0)=3 and every later A/B/C raises the highest one
by two. Before the width2k truncation is reached, the compiler must process
k distinct leaf contexts of total size Omega(k^2). Although a section-only
call does not need the last leaf's action, it must compute all preceding
prefix actions; U A^k has more than k letters, so this does not remove
the first k charged transitions.

There is a related exact restriction on full-output rewrites.
If a C-headed word U has length L, the highest one of U(0) is2L-1.
For any positive word V in A,B,C, delete its leading A-run. If the
remaining word has length m and begins with B, its zero output has highest
one2m-2; if it begins with C, that index is2m-1. An all-A word outputs
zero. Therefore V(0)=U(0) forces the remaining word to be C-headed with
exactly m=L. In particular, no positive-word rewrite preserving the full
zero output can shorten this core below L. This allows new leading A
letters and is stronger than assuming a length-preserving rewrite.

Consequently, length-preserving contextual pair rewrites do not cure the
giant-block cost: they retain the C head and the same support growth.
This is a restriction on full-output positive words and on the specified
explicit-context compiler. It does not exclude a shorter shared graph,
inverse letters, query-only rewrites, or an algorithm that avoids computing
the full zero output.

## 5. Bounded measurements, with the wide work visible

The directed controls use n=8,17,32 and block widths1,2,4,8,n+1. At n=32:

| Block width | Outer blocks | Distinct action contexts | Distinct section contexts | Leaf operand-bit sum | Grammar nodes |
|---:|---:|---:|---:|---:|---:|
| 1 | 33 | 250 | 246 | 15 | 205 |
| 2 | 17 | 214 | 186 | 54 | 125 |
| 4 | 9 | 218 | 190 | 244 | 78 |
| 8 | 5 | 209 | 181 | 739 | 51 |
| 33 | 1 | 63 | 0 | 839 | 9 |

Fewer outer blocks and fewer grammar nodes do not establish a speedup:
the one-block version materializes wider intermediate boundary values.
The operand-bit column counts distinct leaf evaluations only; dictionary,
nonleaf-context, and graph work is additional. No fitted exponent or
unrestricted lower bound is inferred from these finite counts.

The compiler proves that the exact bulk identity can be executed with
complete boundaries. Its cost identifies the next missing ingredient:
constructing and consuming those boundaries implicitly, with a proved
total cost below n, instead of storing the intervening row fragments in
wide integers. No such implicit-boundary algorithm is supplied here.

## 6. Reproduction

- [Compiler and exact verifier](../../experiments/rule30/p3_fused_section_blocks.py).
- [Saved contexts, query counts, and controls](../../experiments/rule30/p3-fused-section-blocks.json).

The checks include558 independent local section/tail cases,24 ordered-word
cases,30 Q-jump comparisons with literal updates,15 center-query variants
against independent row evolution, three actual Q-jump lower-bound
controls, and the huge compressed fixed-family control. The universal
conclusions follow from the recursion and support proofs, not these
finite instances. No paid compute, old census, or long-prefix generation
was used.

```
uv run --offline --no-project python experiments/rule30/p3_fused_section_blocks.py
```

Problem 3 remains open.

# Conditional pair rewriting on the actual section query

Date: 2026-09-13. Status: exact contextual identities and a finite-state SLP
rewriter proved and implemented. The tested rewrite schedule costs more than
the unrevised evaluator; no sublinear algorithm is established.

There are nontrivial cancellations inside the ordered section words. For
example, on every input congruent to 1 modulo 4, the chronological pair BC
has exactly the same full output as AA. On every input congruent to 2
modulo 4, AC equals BA. These are conditional identities; applying them
without the boundary condition is false.

The [dyadic section evaluator](RESULTS-p3-dyadic-sections.md) supplies the
states A,B,C and lists words in chronological order: in UV, U acts first.
This report retains that convention throughout.

## 1. Exact identities with a retained boundary

Recall

```text
A(x)=G(x),
B(x)=G(x) XOR1,
C(x)=G(x) XOR(3-2*(x AND1)),
G(x)=x XOR((x<<1) OR(x<<2)).
```

In particular C(x)=B(x) whenever x is odd. The genuinely two-letter
identities include:

| Incoming input condition | Equal chronological pairs |
|---|---|
| x=1 mod4 | AA = BC = CC |
| x=2 mod4 | AC = BA |
| x=2 mod8 | AA = CB = CC; AB = CA |

Every equality holds for all higher input bits, not merely for the displayed
small integer representative. The corresponding conditional rewrites may
therefore be used within a longer word, provided the condition is checked
at that word position.

For one illustrative derivation, direct substitution gives

```text
AC(x) XOR BA(x)
  = 2*x_0 XOR 4*(1 XOR x_0 XOR x_1).
```

All higher differences vanish. Consequently AC=BA exactly when the two low
input bits are x_0=0,x_1=1. The other identities are certified by the complete
small boundary table below, using the finite propagation lemma.

The conditions are necessary to the stated use. At input0,

```text
AC(0)=3, BA(0)=7;
BC(0)=6, AA(0)=0;
CB(0)=12, AA(0)=0.
```

Thus these are not unconditional group relations.

## 2. Why a finite table proves an all-tail identity

**Finite propagation lemma.** If two binary inputs differ only at positions
at most d, their images under any one of A,B,C differ only at positions at
most d+2. Also, the outputs of A,B,C on a common input can differ only at
positions 0 and 1.

Proof: output bit j of G reads only input bits j,j-1,j-2. The additional
state corrections occur only at bits 0 and 1 and depend only on bit 0. This
proves both statements directly.

Consequently any two length-two state words, applied to the same input,
have identical outputs at every position j>=4. Their four low output bits
depend only on the four low input bits, by triangularity. To certify a pair
identity for all x=r mod8, it therefore suffices to check the two inputs
r and r+8. Higher tails cannot affect the check or produce an unexamined
higher difference.

The verifier evaluates all nine pairs on all 16 four-bit inputs, for 144
evaluations. For each of the eight retained input residues, it groups pairs
whose two outputs agree and chooses the lexicographically first pair in each
group, using A<B<C. The table contains 72 entries. This is a complete
classification of the nine candidate pairs with this retained boundary,
not a claim about arbitrary longer-word rewrites.

## 3. The boundary is computed, not guessed

Suppose the current prefix P sends the remaining seed input 0 to an integer
whose residue modulo8 is r. The residue can be propagated through each state
using its exact map modulo8. A pair W may then be replaced by its table
representative W'. The table theorem gives

```text
W(P(0)) = W'(P(0)).
```

The entire subsequent context receives the same input. In particular, all
later boundary residues and the requested output bit remain valid. This
preserves the actual prefix condition instead of choosing a fresh boundary
independently for each pair.

As a concrete example, after processing the seed bits 1000, the n=8 query
contains the exact word

```text
ABCCABCC.
```

One left-to-right pass on its actual zero input rewrites it to

```text
ABAAABCB,
```

with the same full output 6428. The first CC is encountered after AB has
produced residue 1, so its replacement by AA is one of the genuine pair
cancellations. The last CC becomes CB by the simpler odd-input identity.
The pass creates an internal run of A states without expanding a spacetime
row or assuming that arbitrary generator words are interchangeable.

## 4. A single pass works directly on the compressed graph

The implementation uses the existing SectionSLP node interface. Its method

```text
PairNormalizer(arena).normalize(node, incoming_zero=0)
```

returns a node with the same output on every input having the specified
residue modulo8. The default handles the actual remaining zero tail.

The pass is a finite transducer. Its state consists of an incoming residue
r in 0,...,7 and either no pending letter or one pending A,B,C. There are 32
states. The first letter of a pair is buffered. On the second, the transducer
emits the canonical pair and updates r by the original pair's exact map
modulo8. An unpaired final C is replaced by B only at an odd incoming
residue.

For a concatenation node, first transduce its left child, then transduce its
right child with the resulting residue and pending letter. Memoization keys
include the node and the complete transducer state. Concatenating the two
outputs gives an exact transformed SLP. Thus a shared input subgraph may
produce different outputs in different boundary contexts; it is never
silently reused under the wrong residue.

For an input SLP with s reachable nodes, one pass has at most 32s distinct
transduction subqueries and creates O(s) output nodes, with a fixed constant.
No expanded-word scan or iteration to an assumed normal form is required.
Arithmetic on node identifiers and concatenation lengths must also be
charged in the selected machine model. The implementation records all
transduction, section, and concatenation work.

The simple query experiment applies exactly one pass after each consumed
seed bit. This is correct because the transformed word has the same full
output on its zero tail; sectioning at another zero preserves the remaining
output tail. The schedule still makes n successive section advances.

## 5. Paid result of the bounded test

The hypothesis tested was that this constant-state contextual pass could
reduce section-graph work enough to cover its own construction. The results
do not support that schedule:

| Query n | Baseline distinct section subqueries | Rewritten section subqueries | Added transduction subqueries | Baseline / rewritten constructed nodes |
|---:|---:|---:|---:|---:|
| 8 | 36 | 32 | 69 | 32 / 50 |
| 17 | 113 | 105 | 201 | 99 / 179 |
| 32 | 246 | 234 | 412 | 205 / 401 |

At n=32, the pass performs 28 genuine pair cancellations beyond C=B on odd
inputs, but 234+412=646 distinct subqueries exceed the baseline 246. All
concatenation requests are recorded separately as well. Counting only the
decrease in section subqueries would hide the dominant new work.

This is finite evidence against the every-step schedule, not a proof that
the identities cannot help another exact algorithm. Their useful deliverable
is a sound contextual rewrite operation that can be composed with separate
query-specific pruning. No larger benchmark or fitted exponent was run.

## 6. Exact verification and files

The saved checks include 144 independent raw-memory pair evaluations,
288 conditional high-tail checks, 1936 short-word SLP transduction controls,
three guarded-rewrite counterexamples, and the three center-query comparisons
against independent whole-row evolution. These are small implementation
controls. The finite propagation proof and the complete boundary table
provide the all-length identities.

Independent review checked the all-tail propagation argument, pending-letter
and residue semantics, cache keys, final-letter guard, linear-in-grammar
construction bound, and paid negative comparison. No gap was found.

- [Contextual SLP rewriter and verifier](../../experiments/rule30/p3_observable_rewrite_pairs.py)
- [Exact table, guarded falsifiers, and paid counts](../../experiments/rule30/p3-observable-rewrite-pairs.json)

```sh
uv run --no-project python experiments/rule30/p3_observable_rewrite_pairs.py --output /tmp/p3-observable-rewrite-pairs.json
```

The remaining task is an exact query operation that exploits such identities
without paying for n sequential section advances or a linear ordered seam.
This implementation supplies a legitimate graph rewrite, not that missing
sublinear algorithm. P3 remains open.

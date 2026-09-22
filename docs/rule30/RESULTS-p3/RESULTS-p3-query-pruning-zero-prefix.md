# Exact zero-input prefix deletion in the P3 section graph

Status: **a query-specific graph rewrite and its all-length correctness are
proved and implemented.** The rewrite removes a known generator prefix
without expanding it. On the actual singleton query it removes about half
the generator word by the time the center bit is reached, but the evaluator
still makes `n-1` sequential zero-section advances. No sublinear algorithm
or unrestricted lower bound follows.

## 1. The query and the sound rewrite

Use the three exact binary transducers from the
[dyadic section report](RESULTS-p3-dyadic-sections.md):

```text
A=(A,C),        B=(A,C) swap,        C=(B,C) swap.
```

Generator words are chronological: in `UV`, `U` acts first. Their actions
on nonnegative integers are

\[
\begin{aligned}
G(x)&=x\mathbin{\mathrm{XOR}}((x\ll1)\mathbin{\mathrm{OR}}(x\ll2)),\\
A(x)&=G(x),\\
B(x)&=G(x)\mathbin{\mathrm{XOR}}1,\\
C(x)&=G(x)\mathbin{\mathrm{XOR}}(3-2(x\mathbin{\&}1)).
\end{aligned}
\]

The singleton center bit is `c_n=bit_n(A^n(1))`. After consuming its first
input bit `1`, the exact section is `C^n` and the remaining input is zero.
For any finite word `U` and any `q>=0`,

\[
 (A^qU)(0)=U(0),                                          \tag{1}
\]

because `A(0)=0`. Thus a syntactically known **initial** run of `A` may be
deleted for this query, at every output precision. This preserves the
whole output on the given zero input; it does not assert equality of the
two complete maps on arbitrary inputs.

Store generator words as a straight-line program of concatenations. Each
node can retain its expanded length and the length of its initial `A` run.
For a concatenation, the latter is the left run length, plus the right run
length exactly when the left child is all `A`. These metadata require a
constant number of operations per constructed node. A known initial run
is removed by an exact suffix cut down the concatenation tree, retaining
the untouched subtrees. No letters in a long run need be visited.

## 2. Exact prefix length on every actual seed section

Let `S_(n,j)` be the length-`n` generator word obtained by sectioning `A^n`
along the actual seed prefix `1 0^(j-1)`, with `n>=1` and `j>=1`.

**Theorem.** For `1<=j<=2n`, `S_(n,j)` has exactly

\[
 q_j=\left\lfloor\frac{j-1}{2}\right\rfloor               \tag{2}
\]

initial copies of `A`. Its first non-`A` letter is `C` when `j` is odd
and `B` when `j` is even. For `j>=2n+1`, the complete section word is
`A^n`.

**Proof.** Every generator raises the highest nonzero bit of a positive
input by exactly two: `G` creates the new highest bit from `x<<2`, and
the corrections defining `B,C` affect only bits zero and one. Starting
from zero, initial `A` letters leave zero fixed. The first non-`A` letter
sends zero to `1` for `B`, or `3` for `C`. Hence, for a length-`n` word
with `q` initial `A` letters, its zero image has highest bit

\[
 2(n-q-1)+\delta,\qquad
 \delta=0\text{ for a first }B,\quad\delta=1\text{ for a first }C.
                                                               \tag{3}
\]

On the actual seed,

\[
 S_{n,j}(0)=\left\lfloor\frac{A^n(1)}{2^j}\right\rfloor.
\]

Since the highest bit of `A^n(1)` is exactly `2n`, its shifted value has
highest bit `2n-j` for `j<=2n`. Equating this with (3) gives
`j=2q+2-delta`, which proves (2) and the stated head letter. After the
entire nonzero output has been consumed, the zero image is zero. A word
containing any `B` or `C` has positive zero image by the same argument,
so the section word must then be `A^n`. It remains `A^n` under further
zero sections. QED.

This argument proves the syntactic run exactly on the actual seed path;
it does not infer it from a bounded sample of section words.

## 3. An exact pruned query evaluator

Build `C^n` directly by binary powering of concatenation. At seed-prefix
length `j`, retain the canonical suffix `U_(n,j)` obtained by removing the
initial `A` run from `S_(n,j)`. Its zero output agrees with the full
section by (1). To move one input bit farther:

1. Compute the exact zero section `U_(n,j)|_0` on the shared expression.
2. Delete its initial `A` run with the metadata and suffix cut.

This preserves the canonical invariant. In fact, the section of an
initial `A^q` on a zero input is still `A^q`, and it emits only zeros to
the next factor. Thus sectioning the shortened word, then deleting its
new initial `A` run, gives exactly the shortened next full section.

Equation (2) makes this transition especially precise: from a `C`-headed
stage it erases no letter and becomes `B`-headed; from a `B`-headed stage
it erases exactly one `A` and becomes `C`-headed, until the terminal empty
word is reached. At the center query the latter terminal case has not
yet occurred.

At stage `j=n`, return the root toggle of the canonical word. The current
input bit is zero, so that toggle is precisely `c_n`. Handle `n=0`
separately by returning one. Induction above proves the evaluator for
every nonnegative `n`, without a supplied row, precomputed orbit, or
unpaid table.

The exact expanded canonical length is

\[
 |U_{n,j}|=n-\left\lfloor\frac{j-1}{2}\right\rfloor,
 \qquad
 |U_{n,n}|=\left\lfloor\frac n2\right\rfloor+1.            \tag{4}
\]

The code performs exactly `n-1` zero-section advances and deletes exactly
`floor((n-1)/2)` letters before answering. In the shared expression, an
exponentially long initial run can nevertheless be removed in logarithmic
construction work: the directed control `A^(2^50+7) CBCA` constructs
61 grammar nodes and deletes the whole prefix in two cut requests,
without expanding any of its letters. This is an exact illustration of
the rewrite; it is not asserted to be a new fast center-query family.

## 4. What cannot be erased on the same grounds

Equality on zero input is not preserved when an arbitrary left context
is attached. For example, `A(0)=0`, but `BA(0)=7` while `B(0)=1`.
The preceding `B` supplies the nonzero input one to `A`.

There is an equally small counterexample **inside an actual singleton
center query**. For `n=4`, after consuming the prefix `100`, the section
word is `ACAC`. Removing the initial `A` is sound and leaves `CAC`.
The remaining query is bit one:

\[
 \operatorname{bit}_1(CAC(0))=\operatorname{bit}_1(50)=1=c_4.
\]

Erasing its interior `A` instead gives

\[
 \operatorname{bit}_1(CC(0))=\operatorname{bit}_1(12)=0.     \tag{5}
\]

This is the first center-query failure of a single interior-`A` deletion
from the canonical seed sections: the verifier checks every available
deletion for `n=1,2,3`. At `n=3`, the final canonical word `CA` does
contain an interior `A`, but its deletion preserves that root-bit query.
The distinction is the actual input and the requested observable, not
the generator's name alone.

## 5. Paid cost and maintained checks

The initial grammar has `O(log n)` height and size. Sectioning preserves
its tree shape, and suffix cuts only prune it, so a nontrivial prefix
cut takes `O(log n)` grammar operations. Metadata are maintained when a
node is constructed. A section advance has the elementary `O(n)` bound
obtained by traversing the expanded binary tree; all advances and cuts
therefore take `O(n^2)` grammar operations and at most `O(n^2)` stored
nodes. Deterministic comparison-tree dictionaries give the same
`O(n^2 log n)` word-operation upper bound as the original evaluator.
Python's dictionaries are an implementation choice, not an assumption of
deterministic constant-time hashing in that stated bound.

Reducing expanded length need not reduce the number of distinct shared
nodes. At the directed `n=32` control, pruning constructs 215 nodes
versus 205 without pruning, although it reduces distinct section
subqueries from 246 to 225. Prefix cuts themselves cost work and can
change the available sharing. These finite counters justify neither an
asymptotic improvement nor a claim of monotone graph-size reduction.

The [verifier](../../experiments/rule30/p3_query_pruning_zero_prefix.py)
checks twelve fresh pruned queries through time 33 against both the
existing section evaluator and independent scalar spatial evolution.
It also checks 30 complete seed sections through their all-`A` terminal
states, the large compressed-prefix deletion, and the actual counterexample
(5). The [artifact](../../experiments/rule30/p3-query-pruning-zero-prefix.json)
retains the paid counters, section words, witnesses, and hashes of both
code sources. No old census or large prefix dataset is rerun.

```sh
uv run --offline --no-project python experiments/rule30/p3_query_pruning_zero_prefix.py
```

This establishes a sound rewrite under the exact query context. An
additional operation would still have to skip the linear sequence of
remaining section advances, with its own construction cost charged, to
meet the current sublinear P3 target.

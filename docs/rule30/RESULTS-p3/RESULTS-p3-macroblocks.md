# Paid macroblocks for a singleton-center query

Status: **a uniform `O(n²/log²(n+2))` word-RAM upper bound is proved**, with
all table construction charged. A matching-order lower bound is proved only
for the explicitly defined exhaustive fixed-size macrotable tiling model
below. Neither statement is a Turing-machine bound or a resolution of P3.

The block-table idea is established prior art. Grandjean and Jachiet's
Theorem 3 proof and Appendix §11 explicitly simulate cellular automata by
tabulating blocks in both space and time. This report supplies the exact
singleton-query geometry, paid construction, optimized block aspect ratio,
and a narrow model barrier; it makes no algorithmic novelty claim.
[Grandjean–Jachiet, arXiv:2206.13851v2, §8.2 and §11](https://arxiv.org/pdf/2206.13851v2).

## 1. Computation model and precise target

The target is the center bit at time `n` of Rule 30 started from a singleton
at spatial position zero. Its input is `n` in canonical binary notation.
Use a word RAM with `Theta(log(n+2))`-bit words, enough constant-factor
headroom for addresses and counters; bounded-word Boolean operations,
shifts, arithmetic, and indexed array access have unit cost. Reading the
input and choosing the block size are charged.

No word contains a complete length-`Theta(n)` row. There is no prior orbit
cache or free `n`-dependent advice. The algorithm constructs its lookup
table anew from the fixed eight-entry Rule 30 rule on every query.
The cost of constant indexed access is a model assumption; it must not
be carried over to an ordinary Turing tape without a separate simulation
analysis. See the [P3 scope audit](P3-SCOPE-AUDIT.md).

## 2. The exact macrotable

For a time jump `t>=1`, one table entry takes **`4t` input bits** and
returns their central **`2t` bits after `t` ordinary updates**. The
input interval shrinks by two cells per update, so it needs no exterior
boundary data. The table has

\[
 E(t)=2^{4t}
\]

entries. Building each entry by literal scalar simulation performs exactly

\[
 \sum_{i=1}^{t}(4t-2i)=3t^2-t
\]

Rule 30 evaluations. Thus constructing and storing the whole table takes
`O(t²2^(4t))` word operations and `O(2^(4t)+t)` words. Each result fits
in one word under the parameter choice in §4.

Divide the spatial row into aligned blocks

\[
 [2tj,\,2t(j+1)-1],\qquad j\in\mathbb Z,
\]

packed with increasing spatial positions in increasing bit positions.
To advance block `j` by `t` steps, form a `4t`-bit key from the right
half of block `j-1`, all of block `j`, and the left half of block `j+1`.
If their words are `L,M,R`, the key is

\[
 (L\mathbin{\gg}t)
 \mathbin{|}(M\mathbin{\ll}t)
 \mathbin{|}\bigl((R\mathbin{\&}(2^t-1))\mathbin{\ll}3t\bigr).
\]

This takes three indexed reads and a fixed number of bounded-word
operations, followed by one table lookup and one output write. The
three input blocks are needed only to extract a width-`4t` window;
the table does not redundantly index all six halves.

## 3. Exact geometry of the requested center

At time `s`, retain only

\[
 I_s=[-R_s,R_s],\qquad R_s=\min(s,n-s).             \tag{1}
\]

Outside the seed's forward cone, every cell is the known quiescent zero.
Outside the target's backward cone, no cell can affect the requested
answer. Retain every packed block that intersects `I_s`, masking its
bits outside that interval to zero.

**Why boundary masking is correct.** For any required output position
`x in I_(s+t)`, its earlier dependencies lie in `[x-t,x+t]`, which is
contained in the previous target cone `[-(n-s),n-s]`. Dependencies outside
`[-s,s]` are known zero; all others lie in `I_s` and were retained exactly.
Extra outputs in partial boundary blocks may depend on discarded data,
but those outputs are masked away before the next layer. Induction over
the time jumps proves the retained values are exact.

Write `n=qt+delta`, where `0<=delta<t`. At jump `ell`, the radius is
`min(ell*t,n-ell*t)`. A radius `R` intersects exactly

\[
 \left\lfloor\frac R{2t}\right\rfloor+
 \left\lceil\frac R{2t}\right\rceil+1
\]

aligned blocks. Summing for `ell=1,...,q` gives the **exact lookup count**

\[
 Q(n,t)=\left\lfloor\frac{q^2}{4}\right\rfloor+q+
       \mathbf1_{\delta>0}\left\lceil\frac q4\right\rceil.\tag{2}
\]

For completeness, at the first `floor(q/2)` layers the count is `ell+1`.
At later layers it is `q-ell+1`, with one extra block exactly when
`delta>0` and `q-ell` is even. The base sum is `floor(q²/4)+q`, and
there are `ceil(q/4)` extra layers.

At time `qt`, only `[-delta,delta]` remains relevant. Pack these
`2delta+1` bits, using `O(t)` bounded-word operations, and perform the
remaining `delta` updates on this shrinking `O(t)`-bit cone. It fits in
one word and costs `O(t)` operations. This also handles `q=0`, using
the known initial singleton. No generation-alignment assumption is made.

## 4. Uniform paid upper bound

Handle `n=0` directly. Otherwise choose

\[
 t=\max\left(1,\left\lfloor\frac{\log_2 n}{4}\right\rfloor\right).
\]

For `n>=16`, the table has at most `n` entries; the smaller cases have
constant cost. Combining the charged preparation and (2) gives

\[
 T(n)=O\left(t^2 2^{4t}+\frac{n^2}{t^2}+\frac nt+t+\log n\right)
     =O\left(\frac{n^2}{\log^2(n+2)}\right).        \tag{3}
\]

The preparation term is `O(n log²n)` and is asymptotically smaller than
the displayed bound. The table uses `O(n)` words; two contiguous row
arrays with explicit coordinate offsets use `O(n/t)` words. The total
space is `O(n)` words, or `O(n log(n+2))` bits. There is no hash-table
assumption. Ordinary integer divisions used in the geometry may instead
be implemented by `O(log²n)` bounded-word steps per time layer; the
resulting `O(n log n)` overhead is still absorbed in (3).

This is a stronger RAM upper bound than the `O(n²/log n)` construction
recorded in the earlier [self-composition audit](AUDIT-natal-alsaadi-self-composition.md).
It improves a fine-grained baseline, not the repository's P3 target
`o(n)` charged Turing-machine time. Its present choice of table size
already costs `Omega(n)` entries to initialize; the full dense tiling
cost is much larger.

## 5. Optimal aspect ratio and a narrowly scoped barrier

Consider the following **exhaustive fixed-size macrotable tiling model**:

1. For each input `n`, choose one output width `b>=1` and time jump `t>=1`.
2. Construct an explicit entry for every one of the `2^(b+2t)` binary
   input windows, each giving `b` outputs after `t` steps. Store one output
   word per directly indexed entry and initialize every entry, as in the
   maintained implementation.
3. At every complete time boundary `t,2t,...`, materialize every spatial
   block intersecting the retained interval (1), at least one table
   lookup per block. No query quotient or symbolic omission replaces
   these cuts.
4. Charge the full table construction and every lookup. All computation
   uses the same uniform bounded-word RAM model.

**Restricted-model theorem.** Every such algorithm has worst-case charged
work `Omega(n²/log²n)`. This is a barrier for this representation, not
a lower bound for Rule 30 computation in general.

**Proof.** Fix a sufficiently large input `n`. If its charged work is at
least `n²`, the required lower bound already holds at this input.
Otherwise the explicit table alone requires `2^(b+2t)<n²` writes,
which implies `b+2t<2 log2 n`. In particular `b,t=O(log n)` at this input.
For `Theta(n/t)` time boundaries between `n/4` and `3n/4`, the retained
interval has width at least `n/2`. Each such boundary requires
`Omega(n/b)` materialized blocks. Hence the lookup count is
`Omega(n²/(bt))`. Finally,

\[
 8bt\le(b+2t)^2,
 \qquad (b+2t)^2-8bt=(b-2t)^2.                  \tag{4}
\]

This proves the bound at every sufficiently large input, with uniform
constants. No regularity assumption on `b(n),t(n)` or on the time
function is needed.

At a fixed key length `b+2t`, the product `bt` is maximized when `b=2t`.
This explains the aspect ratio used above. It optimizes the area replaced
per lookup under this boundary-size constraint, not every possible
preprocessing tradeoff.

Compressed tables, adaptive block sizes, sparse query dependency graphs,
Hashlife-style shared subcomputations, and algebraic shortcuts are outside
this lower-bound model. The theorem cannot rule them out. In particular,
it provides no variable-input hardness argument for the fixed singleton
sequence.

## 6. Prior art and what was actually added

Natal and Al-saadi prove the one-output self-composition upper bound
`O(n²/log n)` and explicitly assume unit-cost indexed memory. They do
not prove this is a ceiling for generic simulation.
[Published paper, Theorem 8 and §5](https://content.wolfram.com/sites/13/2025/10/34-3-1.pdf).

Grandjean and Jachiet already tabulate `Q^(3ell)->Q^ell` time-jump
transitions, paying for the table before lookup. Their result concerns
RAM implementations of operations on logarithmic-size operands; the same
local construction can be tiled over larger diagrams. Our bound is a
specialization of that established principle. The exact count (2), the
`b=2t` choice, and the restricted theorem in §5 are proved here rather
than attributed to their paper.
[Theorem 3 proof sketch and Appendix §11](https://arxiv.org/pdf/2206.13851v2).

The [maintained verifier](../../experiments/rule30/p3_macroblocks.py) and
[artifact](../../experiments/rule30/p3-macroblocks.json) check all 4,368
entries of the microtables for `t=1,2,3` using two independent rule forms.
They also check 48 small query/control pairs through time 47, including
every residual for `t=2,3`, five fresh-table wrapper calls, 1,032 exact
geometry cases, and the aspect-ratio identity. Only the tiny independent
reference checks use a whole-cone integer. Production code stores bounded
words in direct indexed arrays. No existing large prefix was regenerated,
and no empirical runtime exponent is used as a proof.

The remaining P3 question is whether a uniformly constructible,
query-specific representation can avoid these dense intermediate cuts
with all its construction and access costs charged in the target
Turing-machine model. The macrotable calculation does not answer it.

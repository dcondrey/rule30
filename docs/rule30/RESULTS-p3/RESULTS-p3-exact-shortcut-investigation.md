# Exact shortcut investigation: sections, arithmetic, and global linearization

Date: 2026-09-13. **The requested exact sublinear Rule 30 algorithm has not
been found.** This investigation implements and tests specific mechanisms
that could skip evolution. It constructs an exact section-based query
algorithm, derives exact composition and Newton identities, and refutes
several precisely stated accelerations. None of these results proves
Problem 3, a general lower bound, or any new center-period exclusion.

The operational target is one finite program receiving binary n and
returning the singleton center bit c_n in total o(n) work, with construction,
precision, and preprocessing paid. See the [scope audit](P3-SCOPE-AUDIT.md).
The auxiliary Z-frontier and endpoint arguments from P1 are not substituted
for the actual singleton trajectory here.

The follow-up [contextual graph-rewriting investigation](RESULTS-p3-contextual-query-rewriting.md)
finds and implements sound nonlinear pair cancellations, query-specific
prefix/suffix pruning, and finite-precision power reduction. These do
simplify the exact expression, but their tested schedules have not supplied
a sublinear query or an improved asymptotic bound.

## 1. Four concrete routes and their outcomes

| Mechanism | Exact result | What remains unproved |
|---|---|---|
| Binary sections of a 2-adic map | Three exact transducer states; a shared-expression query evaluator constructed from n; isometric conjugacy to every odd affine map excluded | An operation skipping many section advances with sublinear total work |
| Time-block aggregation along diagonals | Associative affine and complete two-bit actions; the proposed overlapping summaries collide on actual singleton histories | A summary retaining the ordered internal driving history cheaply |
| Nonlinear binary decimation | Equal radius-eight center windows, index lengths, and residues mod4 require opposite answers in both doubling branches | A richer, constructible state with a valid all-length doubling law |
| Global Newton solve | Exact adjacent-correction residual identity; uniform precision doubling fails; four explicit logarithmic schedules are incorrect | A fast linear solve and a proved small convergence schedule for the center |

The negative results have different quantifiers. The affine-conjugacy
obstruction and Newton adjacent-error family are all-length mathematical
arguments. The decimation and diagonal-summary results are exact finite
counterexamples to universally quantified proposed identities. Newton's
four schedule witnesses refute four complete algorithms. None is an
asymptotic measurement of Rule 30 hardness.

## 2. An exact evaluator and the specific operation that is missing

In right-edge coordinates,

\[
 G(x)=x\mathbin{\mathrm{XOR}}
       ((x\ll1)\mathbin{\mathrm{OR}}(x\ll2)),
 \qquad c_n=\operatorname{bit}_n(G^n(1)).
\]

Reading the input from low bits to high bits gives exactly three states:

\[
 A=(A,C),\quad B=(A,C)\,\mathrm{swap},\quad
 C=(B,C)\,\mathrm{swap},\qquad A=G.
\]

Here swap complements the current output bit. For generator words written
in chronological application order, their sections obey

\[
 (UV)|_b=(U|_b)(V|_{b\oplus p(U)}),
\]

where p(U) is its root-bit toggle. The
[implemented evaluator](../../experiments/rule30/p3_dyadic_sections.py)
constructs A^n with O(log n) initial expression nodes and evaluates the
needed sections using exact sharing. This is a correct query algorithm at
every n. It still takes exactly n section advances and pays for all
additional expression nodes, so it is not the sought shortcut.

For n>=1, define

\[
 \operatorname{jump0}(U,m)=p(U|_{0^m}).
\]

Then the exact center query becomes

\[
 c_n=\operatorname{jump0}(A^n|_1,n-1).
\]

This isolates an actual computational operation, rather than a proposed
summary whose transitions have not been defined. Its unresolved composition
requirement is equally explicit:

\[
 (UV)|_{0^m}
  =(U|_{0^m})\left(V|_{\operatorname{prefix}_m(U(0^\infty))}\right).
\]

The second factor consumes the first factor's **ordered output prefix**.
Its parity alone is insufficient. A successful accelerator would construct
and consume the necessary information implicitly, prove the identity it
uses at all lengths, and charge o(n) total work. No such accelerator is
supplied by the current implementation.

Two tempting simplifications are now excluded. Dyadic seed return depths
are 4 at time4 and 6 at time8. A prefix-compatible bijective conjugacy to
an odd affine 2-adic map would force the second depth to be5. Also, full
sections along the actual seed have distinct zero-tail outputs before the
center is reached, so literal cycle detection cannot skip that interval.
Neither result excludes bulk manipulation of unequal sections or a smaller
query-specific quotient. Proofs and exact controls are in the
[section report](RESULTS-p3-dyadic-sections.md).

## 3. What the alternative constructions taught us

The [diagonal action investigation](RESULTS-p3-aggregate-affine-blocks.md)
does obtain a four-element affine monoid for a fixed diagonal's time
blocks. Its exact last-reset formula is useful once the drivers are given.
But equal overlapping block actions and equal entering/leaving values need
not determine the next diagonal's action. Retaining the **complete joint
action on two unknown bits** repairs all one- and two-step blocks; an
actual three-step singleton witness defeats that repair. The witness even
has the same next entering bit and different next departing bits. This
tests chronological information directly, instead of assuming independent
marginal summaries compose.

The [nonlinear decimation investigation](RESULTS-p3-decimation-window.md)
tests a different possible escape. At n=1863 and n=2011, all seventeen bits
c_(n-8)..c_(n+8) agree, the binary lengths agree, and n mod4 agrees. Yet
(c_(2n),c_(2n+1)) is (1,0) versus (0,1). Hence arbitrary nonlinear functions
of exactly those supplied arguments cannot provide either doubling law.
A correct fixed-radius law would admit a genuine one-branch recursive
query, and that conditional algorithm is implemented and validated on
Thue–Morse. The witness does not exclude larger states or later-only laws.

The [global Newton investigation](RESULTS-p3-global-newton.md) treats the
space-time diagram as one nonlinear system. If a is its current reference
and v is the next linearized solve, its exact residual is

\[
 v_{t+1,i}+F(v_t)_i
   =(v_{t,i}+a_{t,i})(v_{t,i+1}+a_{t,i+1}).
\]

Unlike ordinary power-series multiplication, this product is at the same
time index. Adjacent errors first present at time m can survive at time
m+1 after Newton correction, so there is no general doubling of temporal
precision. On the actual singleton, the four proposed schedules
k=A ceil(log2(n+1)), A=1,2,3,4, fail respectively at n=6,21,40,50. The
residual identity remains an exact, computable certificate; evaluating its
whole cone currently costs too much. No lower bound on the best possible
Newton variant is proved.

## 4. Chaos is compatible with an exact fast query

As a positive control, consider the binary Champernowne sequence obtained
by concatenating the binary representations of 1,2,3,... . It is a known
normal sequence, as discussed by Pincus and Singer in
[their primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC3511067/).
It is the digit itinerary of its corresponding real number under
x -> 2x mod1. This shift representation alone is not the shortcut.

The explicit concatenation permits a paid shortcut. The first k digit-length
blocks occupy

\[
 S(k)=\sum_{j=1}^k j2^{j-1}=(k-1)2^k+1.
\]

For a zero-indexed digit n, locate k with S(k-1)<=n<S(k), set
r=n-S(k-1), and extract the bit at position k-1-(r mod k) from the integer
2^(k-1)+floor(r/k). All integers used have O(log(n+2)) bits; even a simple
schoolbook implementation takes O(log^3(n+2)) bit work. It never constructs
the first n digits or queries an infinite-precision constant.

The [control report](RESULTS-p3-chaotic-query-control.md) and its
[implementation](../../experiments/rule30/p3_chaotic_query_control.py)
check this on literal short concatenations and huge-index block boundaries.
This is known arithmetic used as a positive control, not a new Rule 30
result. It prevents sensitivity, nonperiodicity, or statistical complexity
from being mistaken for a reason exact shortcuts are impossible. For Rule
30 we still lack the equivalent explicit indexing law.

## 5. Reproducibility and disposition

Each linked result includes its exact verifier and a saved JSON artifact.
The section and Newton arguments were checked against independent row or
truth-table implementations. The decimation witness was independently
recomputed through its largest required time4023; the diagonal witness
requires only time28. No old frontier census, large kernel survey, GPU job,
paid computation, or long prefix extension was run.

This work narrows specific candidate algorithms and leaves an executable
section representation on which to test a nonsequential jump. It does not
justify claiming that an exact sublinear algorithm exists, that none can
exist, or that a path to completing P3 has been established.

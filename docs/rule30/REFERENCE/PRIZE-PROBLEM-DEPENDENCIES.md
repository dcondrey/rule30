# Rule 30: a dependency map of smaller proof problems

Date: 2026-09-10. P2 research targets revised 2026-09-11.

This roadmap organizes the repository's exact results into sufficient proof
routes for the three [official Rule 30 problems](https://rule30prize.org/).
It distinguishes proved reductions, unproved sufficient lemmas, and useful
partial milestones. A more specific target need not be easier than the
original problem. Equivalent formulations do not count as newly established
decay or complexity bounds.

Write `x^t=F^t(delta_0)`, `c_t=x_0^t`, `z_t=1-2c_t`, and
`A(T)=sum_(0<=t<T)c_t`. All prize conclusions concern this single seed.

| Problem | Exact working target | Most developed route here |
|---|---|---|
| P1: no eventual period | For every p>=1 and T>=0, some t>=T has c_(t+p)!=c_t | Exclude prescribed periodic traces by finite-origin reconstruction |
| P2: density one-half | A(T)-T/2=o(T) | Prove accumulated cancellation of ordered temporal block sums |
| P3: no sublinear exact query | No fixed uniform correct algorithm computes c_n in o(n) total work | Find an exact scale summary, then prove its cost or expose its obstruction |

The P3 convention follows the repository's
[scope audit](P3-SCOPE-AUDIT.md). The
[official announcement](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/)
has a mismatch between its prose and displayed asymptotic predicate. An
eventual pointwise Omega(n) lower bound is stronger than the operational
no-o(n) target used here; a formal submission must state which it proves.

## 1. P1: exclude periodic tails, one structural class at a time

For a fixed p, define the number of mismatches

\[
Q_p(T)=\#\{0\le t<T:c_{t+p}\ne c_t\}.
\]

Then P1 is exactly `Q_p(T)->infinity` for every p>=1. This only asks for
infinitely many mismatches for each p, not a positive density of mismatches.

### P1.1. Remove the unknown onset [proved reduction]

If a period starts at time T, let y=F^T(delta_0). Its center trace is
periodic from time zero. Thus the stronger theorem

\[
\operatorname{Tr}_0(y)\ne\operatorname{Tr}_0(F^p y)
\quad\text{for every nonzero finite }y\text{ and every }p\ge1
\]

would prove P1. One may instead restrict y to actual seed iterates, but must
then preserve that restriction in the proof. Support grows with the onset T;
checking a bounded support size cannot remove the onset quantifier.

Source: [eventual-period reduction](RESULTS-eventual-period.md).

### P1.2. Exclude constant tails [proved]

The published [zero-tail note](paper/zero-tail-note.tex), including the
constant-one classification, excludes eventual constant traces of nonzero
finite rows. This completes the p=1 case.

### P1.3. Exclude alternating tails [open, with exact reductions]

After constants are removed, period two means an alternating trace. The
[alternating-trace reconstruction](RESULTS-alt-trace-fiber.md) shows that
mortality of every legal finite Z-frontier suffices to exclude it.

The episode results divide this into more concrete tasks:

| Task | Status | Role |
|---|---|---|
| Compose arbitrary episodes with every seam and survival guard retained | Proved | Follow a complete history without admitting false continuations |
| Count exact inverse fibers, including guarded versions | Proved | Describe possible ancestors of a continuation |
| Prove repeat descent and exact phase-switch resets | Proved | Account for local resource loss and refills |
| Bound cumulative repeats by a finite function of the initial length | Open | Turn the local laws into mortality |

Sources: [composition](RESULTS-variable-length-episode-composition.md),
[episode and inverse-fiber analysis](RESULTS-episode-memory-and-repeat-budget.md),
[reset law](RESULTS-repeat-budget-phase-reset.md).

The useful sufficient target is

\[
\forall r\ge1\;\exists B(r)<\infty\;\forall\text{ successful prefixes from
legal length-}r\text{ starts},\quad D\le B(r),
\tag{P1-B}
\]

where D counts repeated adjacent emitted scalars. The proved bound

\[
r+N+1\le2^{D+1}(r+2)
\]

then gives the finite survival horizon

\[
N\le2^{B(r)+1}(r+2)-r-1.
\]

The sharp conjecture B(r)=r-1 is unnecessary. The
[repeat lower-bound report](RESULTS-repeat-budget-lower-bound.md) includes
the alternating-run input and the proof of this implication.

One concrete certificate format for P1-B is a nonnegative potential
Phi(history), bounded initially by B(r), satisfying

\[
\Phi(hs)\le\Phi(h)-\mathbf1_{s=\operatorname{last}(h)}
\tag{P1-C}
\]

on every accepted extension; the first emission has no repeat charge.
Such a potential may retain the initial length, ordered history, and seam
information. Its formula must be independently computable or verifiable;
defining it as the number of future repeats would assume the missing result.
This is a sufficient proposed certificate, not a proved potential.

The existing local rank cannot do this because switches produce unbounded
refills. Merely counting compatible original ancestors cannot do it either:
`C_3(0)=C_3(00)` has eight elements, and
`C_6(101)=C_6(1011)=C_6(10111)` has 36. Longer amortization or additional
information is required for that particular approach.
[Exact counterexamples](RESULTS-fixed-origin-history-count.md).

### P1.4. Extend the reconstruction argument to every period [open]

Period-two mortality is a partial theorem, not P1. For each primitive
nonconstant binary word w, the next tasks are:

1. Derive its phase-driven reconstruction and prove the correspondence with
   finite-origin traces, including every boundary constraint.
2. Identify a finite-origin obstruction or prove mortality for the required
   reconstruction states.
3. Supply an induction or parameterized proof covering all primitive w.

The horizon may depend on w and the initial frontier size. There is no need
for one small numerical bound independent of period, but there must be a
theorem covering all periods. The distinct period-three cases `001` and
`011` provide the next finite targets; see the
[period-three fiber report](RESULTS-period3-fiber.md).

## 2. P2: turn temporal block imbalance into a quantity that loses energy

P2 does not require full statistical independence, normality, or a stationary
thermal bath. There are two routes below. The direct temporal route does not
require first solving the spatial-potential problem.

### P2.1. Reduce all times to complete dyadic shells [proved equivalence]

For N=2^k, use the actual temporal word z_N,...,z_(2N-1), and define

\[
M_k=\max_{0\le u\le N}\left|\sum_{r<u}z_{N+r}\right|.
\]

Then P2 holds if and only if M_k=o(N). The maximum retains excursions inside
a shell; checking only dyadic endpoint densities is insufficient.
[Proof](RESULTS-p2-p3-cross-review-2026-09-03.md).

### P2.2. Replace the maximum by ordered block energies [proved equivalence]

Let b_(k,j,a) be the sum on aligned block a of length 2^j inside the shell.
Put

\[
E_{k,j}=\sum_a b_{k,j,a}^2,\qquad H_k=\sum_{j=0}^{k}E_{k,j}.
\]

The [sharpened energy inequalities](RESULTS-p2-coarse-energy-and-or-pairing.md)
give

\[
\mathrm{P2}\iff H_k=o(N^2)\iff\max_j E_{k,j}=o(N^2).
\]

Thus any proved bound H_k=O(N^(2-epsilon)), epsilon>0, would suffice.
This is an exact reformulation with useful algebra, not a proof of decay.

### P2.3. Obtain cancellation at a flexible sub-shell scale [primary open target]

Define

\[
D_{k,j}=\sum_a(b_{k,j,2a}-b_{k,j,2a+1})^2,\qquad
V_{k,j}=\frac{E_{k,j}}{N2^j}.
\]

The following are proved deterministic identities and bounds:

\[
E_{k,j+1}=2E_{k,j}-D_{k,j},\qquad
V_{k,j+1}=(1-\delta_{k,j})V_{k,j},\quad
\delta_{k,j}=\frac{D_{k,j}}{2E_{k,j}},
\]

\[
\frac{M_k}{N}\le\sqrt{V_{k,j}}+2^{j-k}.
\]

If E is zero, every later energy is zero. Otherwise delta lies in [0,1].
The primary target retains the full range of possible cutoffs:

\[
\boxed{\exists j_k\le k:\quad k-j_k\longrightarrow\infty,
\qquad V_{k,j_k}\longrightarrow0.}
\tag{P2-F}
\]

This is equivalent to P2, by the
[ordered-energy analysis](RESULTS-p2-ordered-energy-audit.md). It requires
only L_k=2^(j_k)=o(N), without a square-root cutoff, a fixed power saving,
or a uniform waiting time between losses. A cutoff selected after measuring
the discrepancy verifies a finite representation; it is not a construction
of the missing all-scale seed estimate.

For a rational diagnostic that does not impose a cutoff schedule, use

\[
F_k=\min_{0\le j\le k}\bigl(V_{k,j}+4^{j-k}\bigr).
\]

Then P2 is equivalent to F_k->0, since a minimizing scale makes both
nonnegative terms small. The [flexible-scale audit](RESULTS-p2-flexible-scale-audit.md)
proves `(M_k/N)^2/2<=F_k<=5M_k/N` and implements this diagnostic across
every available level. This is the same proof target, not a new seed theorem.

One sufficient method is to accumulate arbitrarily many levels below a
sub-shell cutoff with delta>=eta for a fixed eta>0. More generally use the
exact product `V_(k,j)=product_(i<j)(1-delta_(k,i))`; full loss at one level
is allowed, and uniformly large individual losses are not necessary.
Individual zero-loss levels occur on the actual seed. Failure of a
sign-diversity certificate does not rule out this exact loss criterion.

No predetermined sublinear cutoff schedule captures every balanced sign
sequence: cancellation can occur later while still below shell length.
The [flexible-scale audit](RESULTS-p2-flexible-scale-audit.md) proves this
for every prescribed schedule and gives explicit controls.
Any chosen schedule therefore requires an additional seed-specific proof.

### P2.4. A fixed-window recurrence [optional stronger target]

Find an integer ell>=1 and constants 0<eta<1, C>=0, independent of k and j, such that on
every actual seed shell, whenever j+ell<=k/2,

\[
\boxed{V_{k,j+\ell}\le(1-\eta)V_{k,j}+C2^{-j}.}
\tag{P2-C}
\]

Equivalently, the exact telescoped energy identity makes this

\[
\boxed{\sum_{s=0}^{\ell-1}2^{-s-1}D_{k,j+s}
       \ge\eta E_{k,j}-CN.}
\]

In words: substantial energy at a coarse temporal scale must produce
contrast within ell merges, apart from an O(N) remainder. This retains
ordered blocks and allows individual merges to have no loss. It is a
stronger-than-necessary sufficient target, not an observed or proved seed law.

The k/2 cutoff and fixed ell are optional restrictions in this candidate.
They must not replace P2-F as the primary target or become reasons to
reject later cancellation. This recurrence remains worth pursuing only
if the seed supplies a mechanism for these particular uniform constants.

Why it suffices: iterate at j=0,ell,2ell,... up to
`j*=ell floor(k/(2ell))`. Starting from V_(k,0)=1 gives a geometrically
contracted initial value plus a convolution of two decaying geometric
sequences, so V_(k,j*)->0 uniformly as k grows. Also 2^(j*-k)->0. The
prefix bound then gives M_k/N->0 and proves P2.

A proof must derive P2-C, or a weaker accumulated-loss statement, from the
actual seed's causal geometry. Finite integer calculations can falsify or
suggest constants; an induction or telescoping certificate must establish
the inequality for all scales. An exact evolution on temporal means alone
is already [known not to close](RESULTS-p2-temporal-mean-nonclosure.md).

### P2 representations and the seed obligation

Temporal energy, opposite-sign matching, and the queue accumulator describe
one cancellation route. They are not three independent seed mechanisms.
For maximum prefix imbalance M, equal-rank sign pairing has distance at
most 2M-1 and leaves only the total imbalance unmatched. Thus freely
optimized matching is equivalent to the discrepancy target. A useful
matching proof must control a radius and unmatched count from seed
information, including collections of deficient neighborhoods, rather
than choose the radius from the unknown M.

The [matching/energy bridge](RESULTS-p2-matching-energy-bridge.md) gives
direct quantitative conversions, for equal blocks of length L:

\[
U_{L-1}/N\le\sqrt{V_L},\qquad
V_L\le U_R/N+2R/L.
\]

It also identifies the exact total Hall deficiency as a maximum over
collections of intervals with disjoint expanded neighborhoods. Controlling
only the largest deficit by o(N) is insufficient: many bounded deficits can
sum to a linear matching loss. With R>=1 and R=o(N), bounding the sum of the
largest positive and negative single-interval deficits by o(R) is sufficient,
by an explicit packing factor. That estimate remains unproved for the seed.

A proposed new estimate must identify a property of F^t(delta_0) that is
preserved or propagated from the singleton initial condition and then
explain how it controls the uncentered energy or matching deficits.
Universal identities and finite seed measurements do not provide that
causal implication. Restricting a proof to observed local patterns also
needs a theorem that those restrictions hold at all relevant future scales.

The [seed-geometry obstruction](RESULTS-p2-seed-geometry-audit.md) makes this
requirement concrete. At a late seed age, alternative finite rows can retain
both exact moving edge strips forever, a growing recent center history, and
the entire right half at the observation cut, while prescribing an arbitrary
macroscopic future center block. They are not singleton evolutions. Hence
those cut data alone cannot replace the interior's connection to time zero;
a successful certificate must impose an additional origin constraint.
The same report identifies an exact one: for endpoints [-n,n], maximal
finite ancestry depth n characterizes the singleton row. The quantity
`n-d_fin(y)` is invariant, but no cancellation consequence of its vanishing
has been proved.

The spatial current route below is an alternative algebraic starting point.
Its two terms may cancel jointly; separate bounds are sufficient, not
mandatory. Nonlocal compensating observables and increasing observation
windows remain available despite the bounded-window obstructions.

### P2 alternative: spatial cancellation, followed by current cancellation

The proved identity is

\[
A(T)-T/2=P_T+\sum_{t<T}(K_t-1/2),\qquad
P_t=\sum_{m\ge0}(x_{4m+1}^t-x_{4m+3}^t).
\]

The local integer charge defining K is
`q_i=2x_i(x_(i+1) OR x_(i+2))+x_(i+1)x_(i+2)` and
`K=sum_m(q_(4m)-q_(4m+2))`.
[Definitions and proof](RESULTS-quarter-wave-current-target.md).

This route has two separate open obligations:

1. Prove P_t=o(t). A first partial theorem would improve the coefficient
   1/4 in the elementary bound to `|P_t|<=kappa t+C`, kappa<1/4.
   Ultimately, certificates `|P_t|<=epsilon_h t+C_h`, epsilon_h->0,
   with C_h independent of t, suffice. Alternatively prove decay of spatial
   quarter-wave window variance at lengths L(t)=o(t), using the
   [exact spatial loss identity](RESULTS-seed-loss-certificate-search.md).
2. Prove `sum_(t<T)(K_t-1/2)=o(T)`. There is no established estimate closing
   this step. Spatial cancellation alone does not prove it.

Separate bounds are sufficient, but not individually necessary: the two
terms can cancel each other. The all-phase
[observation theorem](RESULTS-local-phase-observation-theorem.md) explains
why a finite list of balanced local statistics alone cannot propagate the
needed spatial property over all inputs. Additional seed restrictions or
larger-scale information must justify any such propagation argument.

## 3. P3: separate exact representation from the cost of evaluating it

### P3.1. Fix the indexed problem and charge all work [established scope]

The input is the canonical binary representation of n, with only
Theta(log n) bits; the initial row is fixed. A single finite algorithm must
return c_n exactly for every n. All n-dependent preprocessing, summary
construction, arithmetic, and memory access must be charged in its model.
Fixed finite tables are allowed; an uncharged family of tables growing with
n is not a uniform algorithm.

For a machine M and canonical m-bit inputs define

\[
W_M(m)=\max_{2^{m-1}\le n<2^m}T_M(n).
\]

Then `T_M(n)=o(n)` if and only if `W_M(m)=o(2^m)`, because n and 2^m differ
by at most a factor of two in this range. A no-sublinear theorem therefore
needs, for every correct uniform M, some epsilon_M>0 and infinitely many m
with W_M(m)>=epsilon_M 2^m. A lower bound for one chosen algorithm is weaker.

### P3.2. The lower-bound milestones [all open for the required index function]

| Smaller restricted target | What a proof would establish | What remains |
|---|---|---|
| Exclude every finite-state machine reading the binary index | No finite-state digit predictor | More general algorithms may still be fast |
| Exclude every polylog(n)-time exact query | No logarithmic-power shortcut | Fractional-power algorithms remain |
| Exclude every O(n^alpha) query for every fixed 0<alpha<1 | No fixed power saving | Bounds such as n/log n remain sublinear |
| Exclude every o(n) uniform query | The operational positive answer to P3 | State the precise model and asymptotic predicate |

These are nested partial results, not a known method for proving the next
one. Even nonexistence of a finite-state digit predictor would imply P1,
so it is not automatically an easier prerequisite to solve first.

Our [ANF theorem](overnight/RESULTS-anf.md) concerns a different function:
the time-t output as a function of 2t+1 variable initial cells. Its degree
2t-1 for t>=3 does not lower-bound evaluation on the one fixed seed. The actual index
function has only m variable bits and degree at most m; the desired effort
bound concerns internal computation after those bits have been read.

A route through circuits, proof systems, or boundary descriptions must prove
a quantitative bridge covering all relevant uniform algorithms. Simulation
overhead must preserve the target threshold. For example, a bound weaker than
linear by a logarithm cannot exclude all o(n) algorithms. No such bridge is
currently supplied by the episode or ANF results.

### P3.3a. Current exact constructive components [source-reviewed]

The record chain `r30-p3-itinerary-conjugacy-coding` ->
`r30-p3-actual-b-query-center` fixes the actual singleton observer.
`r30-p3-two-time-rise-reset-b-high` and
`r30-p3-two-time-rise-reset-c-center` evaluate its two-time high field from
the full actual midpoint, with different origin equations. The interior
pause and predecessor-language certificate are
`r30-p3-rise-chain-transparency-pause` and
`r30-p3-rise-chain-transparency-language`.

These are representation and guarded evaluation steps, not implications
establishing P3. The missing constructor is
`r30-p3-implicit-boundary-investigation-open-guard-construction`.
It must retain ordered run ends: the actual time-0/time-4 collision
`r30-p3-rise-chain-transparency-control-nonclosure` refutes rise-only
causal closure. A uniform constructor still needs a separate o(n) bound
on all charged work. Exact finite-width powering and supplied grammar
transduction retain their narrower all-input correctness and cost scopes.
See [the current report](RESULTS-p3-implicit-boundary-investigation.md)
and [rise-chain certificate](RESULTS-p3-rise-chain-transparency.md).

### P3.3. A constructive route to a negative answer

An exact shortcut can be sought through these separate subproblems:

1. **Sufficient summary.** Define a state S_n from which c_n is exactly
   decoded. Prove that it preserves every boundary dependency needed for
   its future use.
2. **Binary-index extension.** Give exact maps from S_m to S_(2m) and
   S_(2m+1), starting from a fixed base state. Prove correctness by induction
   on the bits of the requested index.
3. **Construction bound.** Bound the cost of those maps, the size of their
   operands, and the final decoding, including all preprocessing.
4. **Sublinear total cost.** Prove a recurrence with a genuinely sublinear
   solution in the declared computational model.

For example, a one-branch recurrence

\[
T(n)\le T(\lfloor n/2\rfloor)
       +C n^\alpha(\log n)^b,
\qquad 0<\alpha<1,\ b\ge0,
\]

gives T(n)=O(n^alpha(log n)^b)=o(n). If each extension costs only a
polylogarithm, the whole query remains polylogarithmic. These are sufficient
algorithm templates, not known Rule 30 algorithms. Two independent half-size
recursive calls, an exponentially large summary, or uncharged precomputation
can destroy the desired bound.

The existing exact composition laws are models of the required proof
discipline, but their prescribed-trace frontier states have not been shown
to provide these index-doubling summaries of the actual seed.

## 4. What would count as a negative solution?

| Problem | Sufficient negative certificate | Examples that do not suffice |
|---|---|---|
| P1 | Actual seed times T,p and an all-future proof c_(t+p)=c_t for t>=T | A long finite match; a periodic background; an immortal abstract frontier without seed provenance |
| P2 | Actual seed times T_j->infinity and epsilon>0 with abs(A(T_j)-T_j/2)>=epsilon T_j | A failed variance inequality; a large spatial potential alone; a large nonzero Walsh coefficient |
| P3 | One uniform exact algorithm with proved o(n) charged work | Approximation; finite runtime fits; subquadratic but superlinear work; a query given an expensive uncharged table |

For P2, persistent positive limsup of M_k/2^k or H_k/2^(2k) would also
disprove the target by the proved equivalences. Failure of a merely
sufficient condition is different from failure of an equivalent condition.

## 5. Dependencies and practical order

P3, in the no-sublinear sense, implies P1: an eventually periodic sequence
has a fixed finite prefix and cycle, allowing exact queries in O(log n)
time by reducing the binary index modulo its fixed period. P2 alone does
not imply P1 (`010101...` is balanced). P1 and P2 together do not imply P3:
Thue-Morse is a nonperiodic balanced sequence with a logarithmic-time
population-parity query.

The immediate research tasks suggested by the repository are:

1. **P1:** search for a history-dependent cumulative repeat certificate;
   accept any finite initial-length bound before trying to optimize it.
2. **P2:** prove the flexible-scale target P2-F from an explicit consequence
   of the singleton initial condition. Treat P2-C and weighted sign diversity
   as optional sufficient certificates, and matching/queue methods as
   representations of the same route. The invariant must retain more origin
   information than the exact edges and recent history in the proved
   competing-row construction. See the [gap repairs](RESULTS-p2-gap-repairs.md)
   for the corrected targets and verification scope.
3. **Independent partial result:** improve the spatial quarter-wave
   coefficient below 1/4 with an all-time seed certificate.
4. **P3:** require a concrete exact index-summary construction or an explicit
   restricted lower-bound target before expanding the computational search.

The one-paper plan can present the proved composition, inverse-fiber,
phase-reset, ANF, and phase-observation results in full, and use this map to
state the remaining obligations. The conditional arrows are research goals;
they should remain visibly separate from the paper's proved theorems.

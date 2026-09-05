# Fresh-session prompt for the Rule 30 Prize Problems

Research state summarized through commit `2f53439` on branch
`research/ancestry-lemma`. Copy the text below into a fresh coding/research
session. It is intentionally more detailed than a normal resumption note so
that the next session does not reconstruct the same reductions or repeat dead
experiments.

---

You are taking over a proof-oriented investigation of Wolfram's three Rule 30
Prize Problems. Work autonomously toward an actual all-length proof,
refutation, or exact algorithm. Do not spend the session surveying the topic
or accumulating more finite evidence.

This prompt is the resumption state, not an invitation to reconstruct it.
Treat every identity and reduction stated below as already derived and saved.
Open its cited proof report only when you need to verify a hypothesis or use
the exact notation in a new proof. Your first mathematical contribution must
start at an explicitly named open arrow below.

## Repository and branch

Use the existing worktree if it is present:

```text
/Volumes/A/researchpapers/r30-lemma/13-rule30
```

The required branch is:

```text
research/ancestry-lemma
```

Begin with `git worktree list`, `git status --short --branch`, and
`git log --oneline -12`. Preserve all pre-existing changes. Do not work in a
different worktree merely because the shell starts there. Commit coherent
advances often. Before each commit, inspect the diff and run only the focused
checks needed for files you changed.

The latest completed branch steps summarized here are:

```text
22181cf  recalibration of failed finite conjectures
4df82e1  draft of the public transducer-orbit question
2f53439  TP3-011 versus TP2 closure asymmetry and the TP3-011 rank obstruction
```

Do not recreate those notes, rerun their computations, or redraft the public
question. If later commits exist, inspect them before choosing a target and
treat them as superseding this baseline.

Use these names without exception:

```text
PP1, PP2, PP3       Wolfram Prize Problems 1, 2, and 3
TP2                 temporal period two
TP3-011             temporal period-three necklace represented by 011
TP3-001             temporal period-three necklace represented by 001
```

Never use bare `P2` or `P3` where it could mean either a Prize Problem or a
temporal period. Rename ambiguous new files, headings, and commit messages
before committing.

## Mathematical setup and exact prize targets

Rule 30 acts on binary configurations by

```text
F(x)(i) = x(i-1) XOR (x(i) OR x(i+1)).
```

Let `delta_0` be the configuration containing one `1` at the origin and zero
elsewhere, and let

```text
c_t = F^t(delta_0)(0)
```

be its center column.

The official questions are:

1. **PP1:** Is `(c_t)` nonperiodic? In this archive the intended target is
   non-eventual-periodicity.
2. **PP2:** Does the frequency of each bit in `(c_t)` tend to `1/2`?
3. **PP3:** Does computing `c_n` from the digit representation of `n` require
   at least linear effort?

All three are open. No file in this repository proves a prize result.

PP3 has a statement-level ambiguity. The announcement's prose suggests an
`Omega(n)` lower bound or exclusion of `o(n)` algorithms, but its displayed
predicate negates the existence of even an `O(n)` machine. These are not
equivalent. The repository's conservative operational convention is:

```text
Try to exhibit a uniform exact machine computing c_n in o(n) work.
For a positive lower bound, state a precise Turing-machine predicate and do
not claim a prize solution without organizer clarification.
```

The input is the canonical binary encoding of `n`, so an `Omega(n)` bound is
exponential in ordinary input length. Arbitrary-row complexity is not the
same problem.

## Non-negotiable research discipline

There is a standing prohibition on another finite census, horizon sweep, GA
adversary search, or SAT extension whose purpose is to accumulate passing
cases. Prior sessions preregistered such runs as non-closing, and they were
non-closing.

A bounded computation is permitted only when it decides a specifically
stated symbolic claim or searches for a counterexample that would change the
next proof step. Write the claim and the consequence of either outcome before
running it. Stop on the first decisive counterexample. A finite range with no
counterexample is not an output and does not increase confidence in an
unbounded claim.

Be aggressive about proof work, not about evidence volume. Do not stop after
one attractive invariant fails. Within the selected target, move immediately
through these modes while a precise next statement remains:

```text
direct identity/proof
-> contrapositive or dual formulation using the complete saved state
-> exact no-go theorem for the failed representation class
-> next weaker prize-sufficient target that retains the lost information.
```

Do not respond to a counterexample by increasing a radius, horizon, number of
features, or solver budget. Respond by identifying the transported datum that
the false claim omitted. Do not stop with “a composition law should exist” or
“standard automata methods apply”; either write the law/method and prove its
hypotheses or mark that arrow open and pivot.

Use the archive's evidence labels literally:

```text
U = uniform all-length theorem or identity
R = uniform reduction to a named open theorem
C = finite exact certificate or bounded decision
K = exact counterexample
M = measurement only
I = inference or heuristic
```

Do not turn `C`, `M`, or `I` into a theorem by rhetoric. No progress
percentages and no bar charts. Report named open unbounded lemmas. In the
current TP2 reduction chain their number is one; equivalent reformulations do
not create independent lemmas. If nothing advances, say “No progress this
session” and record the precise obstruction. That is preferable to a new
finite table.

Every proposed proof must answer all of these questions before implementation:

1. What exact uniform statement is being proved?
2. By what already-proved implication does it advance PP1, PP2, or PP3?
3. Does it use Rule 30's nonlinear `OR`, the lone-seed orbit, and finite
   support where required, or would it also falsely prove the claim for Rule
   90?
4. What is the complete state at the composition seam?
5. What information is discarded, and which archived counterexample shows
   that discarding it is safe or unsafe?
6. Is the proposed lemma genuinely stronger than the conclusion, or merely
   the conclusion restated in new coordinates?

Use Rule 90 with finite row `{-1,1}`, whose center is eventually zero, as the
standing discriminator against rule-generic PP1 arguments.

## Completed-work ledger: reuse it, do not reproduce it

The following work is complete at its stated level. Re-deriving, remeasuring,
or independently rediscovering one of these items is not progress:

```text
PP1:
- bit-exact Rule 30 ground truth and Rule 90 controls;
- same-orbit reduction for every proposed temporal period;
- exclusion of eventually constant-zero and constant-one traces;
- alternating TP2 fiber, Gray/OR macro, four-state phi rule, D8 carry group;
- rotated Peel identity, 13-element inverse-lift monoid, rank descent;
- reduction of the remaining TP2 question to SEP;
- binary-wedge high-bit elimination and deterministic (Q_n,Psi_n);
- the exact unbounded phase/diagonal update written as equations (1)-(4) below;
- the six-route exhaustion ledger: projected support, deterministic halving,
  queue ancestry, dyadic hard-core lock, Peel/Craig induction, and
  Cartier/rationality have already reached a uniform result, exact kill, or
  explicitly isolated unbounded lemma;
- TP3-011 factor monotonicity, equality-subgraph refinement, residual SFT;
- exact UNSAT of the already specified four-state phase-aware additive rank.

PP2:
- equivalence with dyadic-shell maximal discrepancy;
- equivalence with subcubic integrated shell energy;
- exact (length,D,A,I) concatenation law;
- dyadic-tree energy, Walsh, XOR-autocorrelation, and van der Corput bounds;
- all existing finite center, discrepancy, energy, spectrum, and ANF data;
- the diagnosis that the missing object is the actual seed-specific nonlinear
  scale seam, not another observable identity.

PP3:
- deterministic fuel instrumentation and naive baselines;
- arbitrary-input ANF, circuit, ROBDD, proof-system, and 2-kernel probes;
- ordinary spacetime quadtree/ARM7 and arbitrary-input observational/ARM8 work;
- exact query-oriented one-dimensional Hashlife with Rule 90 control;
- the diagnosis that none of these gives a fixed-sequence lower bound and that
  ordinary Hashlife identity does not give a Rule 30 sublinear algorithm.
```

Before starting any proposal, search `docs/rule30/EXPERIMENT-ATLAS.md` and the
`RESULTS-*` files for its mechanism and write a one-sentence novelty boundary:

```text
Existing result X already proves/blocks ______.
The new lemma begins at the still-open arrow ______ and escapes obstruction Y
because it retains/uses ______.
```

If you cannot fill this in precisely, do not start the proposal. Reuse stored
code, tables, witnesses, and checkers as regression material; do not regenerate
them.

## Priority ladder

Unless the user supplies a different target, use this order. It ranks exact
leverage, not the importance of the prizes, and it makes no claim that any
open prize has a high absolute probability of solution.

1. **PP1 through the weakest TP2 separator `(SEP)`.** This is the archive's
   deepest exact reduction and keeps the real hard-core/terminal predicates.
   Work on the complete ordered carried state or prove a valid quotient of it.
   Do not assume the proof state must be finite. A new invariant, normal form,
   well-founded order, or transducer-section argument is useful only if its
   update is derived for every word and it separates both `c=2` and `c=3`.
2. **The `(PSI)` relaxation only when there is a concrete algebraic move beyond
   equations `(1)`–`(4)`.** It is cleaner but stronger and has low prior
   weight. Give it no extra confidence because its finite instances pass. If
   the growing diagonal cannot be quotiented, prove the exact no-go class or
   return to `(SEP)` with the discarded hard-core and terminal data.
3. **PP2 through the actual-shell seam and integrated energy `(6)`.** The
   observable algebra is finished; attack only the missing seed-specific seam
   and all-scale estimate.
4. **Full-period PP1 through the R1 zero-set obligation** if a genuinely
   period-dependent right-neighbor cocycle is available. This has greater
   payoff than TP2 but less developed exact state; never substitute a bounded
   strip or finite period ladder.
5. **PP3 only with a written new congruence/composition or a written
   fixed-sequence lower-bound bridge.** Without one of those, PP3 work will
   repeat an archived representation census.

TP3-011 is a secondary PP1 laboratory, not the default path. Return to it only
with a nonadditive all-length termination mechanism that is visibly outside
the already rejected additive SFT rank class. Do not open TP3-001 until
TP3-011 closes or yields a new exact obstruction.

## Current exact state of PP1

For any finite configuration `x`, eventual temporal period `p` gives a row
`y=F^T(x)` on the same forward orbit satisfying

```text
Tr_0(y) = Tr_0(F^p(y)),
Tr_0(y)_t = F^t(y)(0).
```

Thus the universal statement

```text
Tr_0(y) != Tr_0(F^p(y))
for every nonzero finite y and every p >= 1
```

is sufficient for PP1. It is stronger than necessary because PP1 starts from
`delta_0`. Same-orbit is load-bearing: one-cell trace injectivity is false for
arbitrary pairs.

Eventually all-zero and eventually all-one center traces have already been
excluded. The Rule-30-specific latch is

```text
c_t = 1  =>  l_t = 1 XOR c_(t+1),
l_t = c_(t+1) XOR (c_t OR r_t),
```

where `l_t=s(t,-1)` and `r_t=s(t,1)`. Under an eventually periodic center,
column `-1` is eventually periodic exactly when `r_t`, restricted to times
with `c_t=0`, is eventually periodic. This is the full-period R1 zero-set
route. It remains open.

If choosing this full-PP1 route, start at the zero-set obligation itself. Do
not rederive the latch, retry the rightward determination cascade, use a
bounded run-of-ones wedge, enlarge a fixed-depth strip, or restart the finite
period automaton ladder; those continuations are already killed. New content
would need an exact period-dependent return/cocycle law that determines the
right-neighbor values on the center zero-set while retaining the unbounded
gaps and phase that defeated those routes.

### TP2: the most developed nonconstant-period rung

The immediate universal target is

```text
Tr_0(y) != Tr_0(F^2(y)) for every nonzero finite y.       (TP2)
```

The two alternating phases reduce to `0101...`. The proved reduction chain is

```text
TP2 counterexample
  => alternating Gray/OR frontier with hard-core endpoint
  => inverse-terminal cut of finite Peel rank
  => rank-zero hard-core endpoint
  => first infinite shifted cut with tail c^omega, c in {2,3}
  => endpoint-derived source orbit meets the inverse-terminal hard-core image.
```

The single exact open separator is

```text
O_c intersect I(HC_omega) = empty, c in {2,3}.            (SEP)
```

Here is a self-contained definition. Let `A={0,1,2,3}` and
`B=(3,2,1,0)`. Define `g_s:A->A` by the four rows

```text
s=0: (0,3,2,3)
s=1: (1,2,3,2)
s=2: (3,1,1,1)
s=3: (2,0,0,0).
```

For `a in {0,1,2}`, define the one-sided sequential transducer `T_a` by

```text
T_a(x)_0 = a,
T_a(x)_j = g_(x_j)(T_a(x)_(j-1)), j>=1.
```

For a finite word `u=a_1...a_m`, set

```text
T_u = T_(a_m) o ... o T_(a_1),
O_c = {T_u(c^omega): u in {0,1,2}*}.
```

Define `phi:A^2->A` by rows

```text
(0,1,3,2)
(3,2,1,0)
(3,2,0,1)
(3,2,1,0).
```

Let

```text
HC_omega = {e in {1,2}^N : e contains no 11}.
```

For `e in HC_omega`, define the inverse-terminal word `I(e)=(r^t_0)_(t>=0)`
by

```text
r^0_i = B(e_i),
r^1_i = phi(e_i,r^0_(i+1)),
r^t_i = phi(r^(t-2)_(i+1),r^(t-1)_(i+1)), t>=2.
```

Then `(SEP)` asks whether the finite transducer orbit of `c^omega` is
disjoint from the inverse-terminal image of the hard-core subshift. For a
definition check,

```text
I(2^omega) = (12)^omega,
T_0(2^omega) = 0311... .
```

Proving `(SEP)` closes TP2 only. It does not exclude higher temporal periods
and does not by itself solve PP1.

### The deterministic binary-wedge relaxation

A cleaner but stronger sufficient statement is the binary-wedge horizon

```text
M_c(n) <= n+1,
```

equivalently: no binary word `f` of length `2n+2` satisfies

```text
P^n(I_G(f)) = c^(n+2), c in {2,3},
```

where `I_G` is inverse Gray code. This drops the original hard-core junction
and terminal-pull predicates, so its failure would not refute `(SEP)`.

Affine `D8` triangularity already eliminates all continuation choices. For
each binary source `W in {1,2}^n` there is one forced binary continuation
`Q_n(W)` of length `n+2`. If `G_n=P^n o I_G`, define

```text
Psi_n(W)_j = 1 + H(G_n(W Q_n(W))_j) + L(G_n(W Q_n(W))_j)
```

over `F_2`. The binary-wedge claim is exactly

```text
Psi_n(W) is never constant.                              (PSI)
```

There is no remaining existential suffix. This is an exact coordinate
reduction, not independent evidence for the conjecture.

The newest-cell affine phase has the form

```text
A_(alpha,beta,gamma)(h,l)
  = (h+alpha, l+beta*h+gamma).
```

It emits both the forced continuation and defect bit:

```text
q       = 2-alpha,
Psi bit = alpha + beta*(1+alpha) + gamma.                (1)
```

For a four-state symbol `x=(H,L)`, define

```text
lambda(x) = (H OR L, 1+L, H OR L).
```

Affine phases compose as

```text
(alpha,beta,gamma) ->
(alpha+a, beta+b, gamma+g+b*alpha).                      (2)
```

After `(1)` forces `q`, the dependency diagonal updates by

```text
D'_0 = B(q),
D'_1 = phi(previous_endpoint,D'_0),
D'_k = phi(D_(k-2),D'_(k-1)), k>=2.                     (3)
```

Equations `(1)`–`(3)` are the exact phase-carrying sequential law already
derived. They are not a bounded composition: the newly transformed ordered
diagonal grows. The smallest exact state currently justified is

```text
(previous binary endpoint,
 ordered dependency word over {0,{1,3},2}).              (4)
```

The quotient `{1,3}` is exact. No smaller closed quotient is proved. A total
affine phase, endpoint, fixed prefix/suffix, two-ended window, or SFT legality
state does not determine the next transformed diagonal. Prefix and suffix
recursions fail without carried phase even after reversal and complementation.

The legitimate symbolic target is therefore one of:

1. starting from equations `(1)`–`(4)`, prove a genuinely new identity that
   quotients the growing ordered dependency word to an exact bounded phase and
   then proves `Psi_n` nonconstant;
2. prove by a uniform distinguishability argument—not another bounded
   collision search—that no bounded phase quotient of a precisely specified
   class can close;
3. retreat to the weaker hard-core rotated-wedge/late-pull statement and use
   the hard-core junction and terminal `12a` information discarded by
   binary-wedge.

Do not rederive equations `(1)`–`(4)`, retry phase-free prefix or suffix
recursions, rerun the two-ended annotation search, or apply TP3 local-factor
ranking before a fixed TP2 graph has been proved. Do not claim that equations
`(1)`–`(3)` already solve `(PSI)`. If taking option 3, do not rerun the existing
late-row CNFs or source-word censuses; the new content must be an all-length
argument using the two predicates that the binary-wedge relaxation discarded.

### Temporal period three

TP3 has two primitive necklaces. `TP3-011` and `TP3-001` must be treated
separately.

For TP3-011, the boundary-free interior transducer acts synchronously on a
fixed finite core. Equality-subgraph refinement proves an all-length
lexicographically nonincreasing local-factor vector. A hypothetical immortal
dual orbit eventually lies in the positive-entropy SFT

```text
{w in {0,1,2}* : w avoids 01, 11, and 220}.
```

Word length is not bounded and grows on alternating endpoint types. One exact
phase-aware nonnegative additive-rank class on the four-state SFT product is
UNSAT; this rules out that rank class only. TP3-011 remains open.

Do not rerun the equality-subgraph calculation, the residual-language word
census, or the four-state additive-rank synthesis. A continuation must begin
with a genuinely different all-length termination mechanism, such as a proved
nonadditive/positional rank that explains growth, or it must record a new exact
structural obstruction and leave TP3-011. Merely adding factor length or
another local weight class repeats completed work.

TP3-001 has two free boundary phases, probably needs a larger frontier state,
and is untouched. A proof of TP3-011 alone would not exclude temporal period
three and would not solve PP1. Do not start TP3-001 merely because TP3-011 has
partial structure; first obtain a proof or a stated structural obstruction
for TP3-011.

## Current exact state of PP2

Put

```text
x_t = 2*c_t-1,
S(N) = sum_(0<=t<N) x_t.
```

PP2 is exactly `S(N)=o(N)`. For each dyadic shell define

```text
M_k = max_(0<=u<=2^k)
      |sum_(2^k<=t<2^k+u) x_t|.
```

The dyadic-shell lemma is an exact equivalence:

```text
PP2  <=>  M_k/2^k -> 0.                                 (5)
```

Define shell prefixes and integrated energy by

```text
S_k(u) = sum_(0<=r<u) x_(2^k+r),
I_k    = sum_(u=1)^(2^k) S_k(u)^2.
```

Because `I_k <= 2^k M_k^2` and `I_k >= M_k^3/8`, there is a second exact
equivalence:

```text
PP2  <=>  I_k=o(2^(3k)).                                (6)
```

This is currently the weakest exact scalar target. For a signed word `w`, let

```text
D(w) = total signed sum,
A(w) = sum of prefix sums,
I(w) = sum of squared prefix sums.
```

The summary `(length,D,A,I)` composes exactly under concatenation:

```text
n(uv) = n_u+n_v,
D(uv) = D_u+D_v,
A(uv) = A_u+n_v*D_u+A_v,
I(uv) = I_u+n_v*D_u^2+2*D_u*A_v+I_v.                   (7)
```

Thus the PP2 observable already has an associative composition law. The open
problem is not `(7)`; it is constructing exact dyadic pieces of the actual
lone-seed Rule 30 spacetime with a seam state strong enough to propagate them
and then proving the subcubic bound.

A valid scale state `Q_k` must:

1. be constructed from the actual lone-seed orbit;
2. compose exactly to scale `k+1` with an explicit nonlinear seam;
3. determine or bound `M_k` or `I_k`;
4. give `o(2^k)` discrepancy or `o(2^(3k))` integrated energy uniformly;
5. retain scale and absolute phase unless an identity proves cancellation.

Useful stronger sufficient routes, not equivalent statements, are:

```text
subquadratic dyadic-tree block energy,
k*W_k/2^k -> 0 for time-index Walsh maximum W_k,
sum_h |C_k(h)| = o(2^(2k)/k^2) for XOR autocorrelations.
```

There is also an exact ordinary-shift bridge. With `z_t=(-1)^(c_t)` and

```text
C_N(h)=sum_(t=0)^(N-1-h) z_t*z_(t+h),
```

the hypothesis

```text
C_N(h)/N -> 0 for every fixed h>=1                     (8)
```

implies PP2 by van der Corput. In Rule 30 language, `(8)` says that the
center defect between `F^t(delta_0)` and `F^(t+h)(delta_0)` has limiting
density `1/2`. Temporal-period exclusion only proves, at best, that such a
defect cannot vanish forever; PP2 needs quantitative cancellation.

Do not use Bernoulli initial-condition independence, almost-everywhere
ergodicity, horizontal densities, or a generic invariant measure to bridge
to the lone seed. The lone seed is a measure-zero orbit. The orbit-closure
rigidity target may also be too strong because all-zero or checkerboard fixed
points may lie in the closure. Universal local additive conservation laws
are blocked by fixed configurations; bounded rational searches through width
12 are not an all-width theorem.

The preferred PP2 openings are the following missing arrows, not blank-slate
versions of earlier experiments:

1. **Moment-decorated actual-shell seam.** Start with `(7)` and the stored
   ARM7/Hashlife obstructions. New content must be an exact composition for
   the reachable lone-seed seam plus a uniform subcubic estimate. Do not
   rebuild an ordinary dyadic quadtree, full row-block Hashlife, or another
   compression census.
2. **Quantitative complete defect state.** The local two-orbit defect recurrence,
   Walsh identities, and finite spectra already exist. New content must be an
   all-scale norm/cancellation theorem for the complete seed-derived seam, not
   another derivative calculation or a larger spectrum.
3. **Seed-specific boundary flux.** Universal local conservation laws and
   endpoint-only telescopes have already failed. A new coboundary must depend
   explicitly on the lone-seed cone, absolute scale/phase, and its two moving
   edges, and its telescoping identity must be proved symbolically before any
   evaluation.

Reject a proposed PP2 route if it discards the nonlinear seam or silently
switches from the designated orbit to an ensemble.

## Current exact state of PP3

PP3 is a fixed-sequence query problem. ANF degree, sensitivity, decision-tree
depth, ROBDD size, circuit size, proof size, or dependence on most cells for
an arbitrary input row does not lower-bound the cost of the function
`n -> c_n`. A fixed output bit can be hardwired nonuniformly; the required
algorithm is uniform over all `n`.

Exact one-dimensional Hashlife already implements the archived power-of-two
center queries without first materializing the whole spacetime triangle. On
the Rule 90 control its memoized advance calls grow polylogarithmically. For
Rule 30 the measured call count is superlinear over the archived finite range.
This kills the literal full-row-block identity quotient as a proposed
sublinear algorithm. It is not a lower bound on other algorithms and its
horizon must not be extended for evidence.

The coherent constructive target is an exact reachable observational quotient
with all four ingredients:

```text
a canonical state of poly(log n) or o(n) size
+ exact dyadic composition including the nonlinear seam
+ exact extraction of c_n
+ a proof that total charged work is o(n) in the stated machine model.
```

The quotient may merge only states proved equivalent in every parent context
reachable in the lone-seed query. Raw Hashlife identity retains too much;
arbitrary-input ROBDDs retain the wrong state space. Kill a candidate as soon
as its canonical seam provably needs `Omega(n)` bits or one composition touches
`Omega(n)` entries.

Do not implement another generic Hashlife, quadtree compressor, fixed variable
order ROBDD, 2-kernel census, ANF expansion, proof-size proxy, or evolutionary
program search. For a constructive route, write the new reachable-state
equivalence relation and prove its congruence/composition law first; only then
implement it. For a lower-bound route, write the explicit bridge from the
fixed sequence to the chosen uniform machine model before invoking any
complexity measure.

A positive PP3 result must instead lower-bound every correct uniform machine
in a precise model. Nonperiodicity, nonautomaticity, expansion of one formula,
large certificates, a fitted runtime exponent, and incompressibility language
do not supply that bridge. No such lower-bound bridge is currently known in
the archive.

## Failed extrapolations that must govern confidence

The following conjectures passed substantial exact ranges and then failed or
were found circular:

1. `M_c(n)<=n` passed through `n=14` and failed at `n=15` with
   `M_3(15)=16`.
2. The two-step fan-out retreat cover failed at queue length `5`.
3. A two-ended annotation passed complete held-out lengths `11` and `12` and
   failed at `13`; the missing information was in the interior queues.
4. The actual-language ancestry-depth-two cap survived endpoint lengths
   through `26` and failed at endpoint length `64` with depth `4`.
5. Nonfinal alpha support passed 370,944 held-out cases and was then proved to
   restate its desired conclusion at `j=n` because the witness interval was
   empty.
6. For TP3-011, “every left three-cell block is nonzero” passed three blocks
   and failed at the fourth.

Consequently:

```text
M_c(n)<=n+1 / nonconstant Psi_n: low prior weight;
bounded phase for (Q_n,Psi_n): very low until a closed update is written;
hard-core rotated wedge / three late rows: structurally better because it
retains real source predicates, but finite UNSAT instances add no weight;
SEP: the correct open theorem, not evidence for itself.
```

Other mechanism classes already have exact obstructions: fixed-radius
additive energy, bounded frontier summaries, raw dyadic period mismatch,
bare holonomy defects, static DFA-rank contraction, a literal final local
patch, single backward defects, arbitrary-queue pivot counts, pointwise scale
derivatives, and ever-larger bounded SAT/GA tables. Their shared failure is
loss of a growing ordered dependency diagonal carrying binary scale and
absolute `D8` phase.

Do not rename one of these mechanisms and retry it without identifying a new
load-bearing hypothesis that escapes its exact counterexample.

## Targeted source routing

Do not reread the entire archive. This prompt contains the current state.
Read `START-HERE.md` once to detect superseding commits, then open only the
capsule and exact predecessor reports for the target you select. Search the
atlas by mechanism rather than reading it sequentially:

```text
docs/rule30/START-HERE.md
docs/rule30/EXPERIMENT-ATLAS.md
```

Do not read `PATH.md` chronologically unless resolving a collision; it is the
exhaustive register, not the resumption document.

For every PP1/TP2 continuation, read only these three compact ledgers first:

```text
experiments/rule30/p1-period2-invariant/PROOF-STATE-CAPSULE.md
experiments/rule30/p1-period2-invariant/RECALIBRATION-FAILED-FINITE-CONJECTURES.md
experiments/rule30/p1-period2-invariant/RESULTS-SIX-ROUTE-EXHAUSTION.md
```

If attacking `(SEP)` directly, then read only the exact state/conjugacy reports
you will use:

```text
experiments/rule30/p1-period2-invariant/RESULTS-ROTATED-PEEL-IDENTITY.md
experiments/rule30/p1-period2-invariant/RESULTS-CONSTANT-TAIL-QUEUE.md
experiments/rule30/p1-period2-invariant/RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md
experiments/rule30/p1-period2-invariant/RESULTS-CONSTANT-TAIL-FRONTIER-GRAPH.md
experiments/rule30/p1-period2-invariant/RESULTS-ENDPOINT-EVENT-BRIDGE.md
```

If attacking `(PSI)`, read:

```text
experiments/rule30/p1-period2-invariant/RESULTS-TP3-011-VS-TP2-CLOSURE.md
experiments/rule30/p1-period2-invariant/RESULTS-BINARY-WEDGE-HIGH-ELIMINATION.md
```

Read the following only if you deliberately retreat from `(PSI)` to the
weaker source-constrained statement:

```text
experiments/rule30/p1-period2-invariant/RESULTS-DLP-ROTATED-WEDGE.md
experiments/rule30/p1-period2-invariant/RESULTS-LATE-PULL-DIAGONAL.md
```

For the public automata formulation, read but do not post:

```text
experiments/rule30/p1-period2-invariant/DRAFT-PUBLIC-QUESTION.md
```

That question is already drafted. Do not rewrite or post it unless the user
explicitly requests that action.

For TP3-011, also read:

```text
experiments/rule30/p1-period2-invariant/RESULTS-TP3-011-SFT-RANK.md
```

For PP2, read:

```text
docs/rule30/RESULTS-p2-p3-cross-review-2026-09-03.md
docs/rule30/RESULTS-p2-time-index-walsh.md
```

For PP3, read:

```text
docs/rule30/P3-SCOPE-AUDIT.md
docs/rule30/RESULTS-hashlife-center.md
docs/rule30/REFUTATION-nersissian-log-query.md
docs/rule30/CLAIM-AUDIT-deva-dual-flow.md
```

Read `docs/rule30/FACT-INDEX.md` for exact reusable identities. Consult the
specific `RESULTS-*` proof report before citing any compact summary as a
publication claim.

## Work order for this session

1. Verify branch, status, and whether commits newer than the baseline above
   alter this handoff.
2. Search the atlas/result titles for the proposed mechanism and write the
   novelty-boundary sentence required above. Do not perform a general survey.
3. Choose exactly one named theorem or algorithmic target. If no fresh
   preference is supplied, PP1/TP2 has the most developed exact state, PP2 has
   the weakest exact prize-equivalent scalar target, and PP3 is viable only
   with a concrete new quotient/composition or lower-bound bridge.
4. Write the implication DAG from the chosen target to the Prize Problem.
   Mark every unproved arrow. If the candidate is only a rung, say so.
5. Begin at the last saved exact identity, not at its derivation. Work
   symbolically first. Preserve full seam, phase, and ordered state
   until an exact quotient identity is proved.
6. Use computation only for a decisive symbolic check under the standing
   restriction. Do not extend a horizon after a pass.
7. If you prove a uniform statement, add a human-readable derivation and an
   independent checker where appropriate. If you falsify it, preserve the
   smallest exact counterexample and explain which information it exposes.
8. Update the appropriate result note and compact index only after the claim
   level is clear. Commit each coherent theorem, counterexample, obstruction,
   or corrected handoff separately with `PP1`, `PP2`, `PP3`, `TP2`,
   `TP3-011`, or `TP3-001` in the message as appropriate.
9. Continue autonomously while a concrete safe proof step remains. Stop at a
   good mathematical boundary: a proof, an exact obstruction, or a precise
   account of the unbounded carried state and why the plausible quotients
   fail.

Do not declare a target exhausted merely because its first representation
fails. Exhaust the precise symbolic consequences of the failure, then use the
priority ladder. Conversely, do not keep a dead representation alive by
adding parameters. Aggressiveness means fast falsification, immediate reuse of
the saved exact state, and persistence across mathematically distinct proof
moves.

## Anti-hallucination acceptance gates

Use no unverified step in a claimed result. Every load-bearing assertion must
have at least one of:

```text
- a displayed derivation from the Rule 30/local transducer tables;
- an exact citation to a proof in a named repository file and section;
- a finite-state certificate whose state graph represents words of all
  lengths, together with an independent verifier;
- or a cited primary-source theorem whose hypotheses are checked one by one.
```

A long finite orbit, solver UNSAT at finitely many lengths, fitted exponent,
absence of a collision, or agreement among agents is never a load-bearing
assertion. Do not invent a literature theorem, standard lemma, recurrence,
symmetry, or boundary condition. If an external result is needed and its exact
statement is not locally available, verify it from the primary source. The
archive specifically flags the Jen 1986 novelty premise as unread; do not
silently strengthen or rely on it.

Before using the word “solved,” run the corresponding audit:

```text
PP1: the proof covers the lone seed for every eventual period and every
     preperiod; closing TP2, TP3-011, or any finite list of periods is not PP1.
PP2: the proof is an all-N asymptotic statement for the lone-seed center;
     dyadic endpoints, an ensemble, and finite bias data are insufficient.
PP3: the algorithm is uniform and exact for every canonical binary n and has
     fully charged o(n) work, or the lower bound quantifies over every machine
     in an explicit model; one derivation/representation is insufficient.
```

For any intermediate lemma, substitute its exact quantifiers into the whole
implication DAG and check that no hypothesis is the desired conclusion in
disguise. Recheck boundary indices, empty witness intervals, finite-support
use, and both tail/phase cases. These are where this archive's most convincing
false proofs failed.

The desired output is not a plausible conjecture. It is one of:

```text
- a complete, independently checkable solution of PP1, PP2, or PP3;
- an all-length lemma that closes a named arrow in a prize-aligned proof DAG;
- an exact obstruction that permanently closes a broad proof or algorithm
  class and identifies the next state that must be carried;
- or an honest report that no unbounded lemma advanced.
```

In the final report, lead with what is proved or not proved, name the remaining
open unbounded lemmas, list commits, and state explicitly whether any Prize
Problem or only a temporal-period rung was closed.

---

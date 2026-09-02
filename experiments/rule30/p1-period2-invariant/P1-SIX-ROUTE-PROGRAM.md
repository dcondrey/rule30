# P1 six-route exhaustion program

Date started: 2026-09-01

Status: **EXHAUSTION GATE COMPLETE 2026-09-01.**  Each route now has an
all-length proof component, an exact structural kill/subsumption, or one
unbounded irreducible lemma.  This status does not claim P1 or period two.

Objective: pursue each currently credible P1 program to one of three terminal
outcomes: a uniform proof consumed by P1, an exact structural kill of the
stated mechanism, or a rigorously isolated irreducible lemma with all tested
bounded substitutes recorded as insufficient.

## Evidence gate

Finite survival, SAT, rank, or random-search results never close a route.
Every terminal result must be one of:

1. an all-length algebraic/automata proof;
2. an exact parametric counterfamily or one exact counterexample to a
   universal mechanism;
3. an equivalence reduction whose remaining quantified lemma is stated
   without hidden finite bounds.

## Route ledger

| Route | Exact success target | Current state | Next admissible move |
|---|---|---|---|
| Projected diagonal support | Prove the tail-2 `(alpha,beta)` and tail-3 `(alpha,gamma)` change at some `k>=j` on every required row | **IRREDUCIBLE FULL-QUEUE CONTRAPOSITIVE**; endpoint telescopes, bounded defect states, and local edge monotonicity are killed | Prove the contrapositive from the complete ordered scenario queues or an equivalent unbounded leading-term/ancestry quotient; no further width sweep is admissible |
| Deterministic halving | Prove `s_c(W)<=ceil(n/2)+1+s_2(L)` for `n>=4` | **IRREDUCIBLE PREFIX-IMPLICATION FORM**; scalar gaps, raw embedding, and parent-continuation-only morphs are killed | Prove uniformly that parent legality through `h+r` implies left-half/tail-2 legality through `r`, by triangular elimination retaining the free left half |
| Queue ancestry / distance | Prove `d(r)->infinity`, equivalently constant-frontier orbit disjointness from infinite hard-core terminals | **PULL RAY AND TEMPORAL ANCESTRY PROVED; ONE MARKED STATE LIVE**. Pull depths satisfy `h_i>=floor(i/2)+1`. The one-chain feature bound passes 4,115,168 held-out queues; the stronger exclusion of raw state `3` at zero remaining reserve passes 1,697,191 newly seeded queues | Prove preservation of `pull-depth+[raw=3]<=initial feature reserve` under the marked raw scan; this gives `#pulls<=2|R|`. Alternatively exclude unbounded depth under eventual actual pull gaps `{2,3,4,5}`. Fixed-factor ranks through width five are killed |
| Dyadic hard-core lock | Prove every ultimately dyadic cut with an infinite hard-core endpoint is the exceptional eventually-`2` family, then apply reachability separation | **SUBSUMED AS A STANDALONE ROUTE**; finite core reachability has finite Peel rank, which descends exactly to rank zero | Prove the rank-zero finite-support separator through one of the first three routes. Classifying infinite-rank dyadic cuts is unnecessary; separated-doubling control is retained only as a diagnostic |
| Peel-recursive Craig induction | Express the next separator as a Peel pullback of its predecessor plus an exact restart/boundary state | **LITERAL PULLBACK EXHAUSTED**; `P(S_H)` re-enters `S_(H-1)` only at the all-`2` endpoint | The exact section `F(2e)=g(e_0)F(e)` forces an unbounded defect position. Prove an indexed restart separator, equivalently the stronger shell lemma `C(m,m)` apart from its two explicit exceptions |
| Cartier `S(0)` rationality | Prove the center generating series is nonrational, equivalently the center is not eventually periodic | **GENERIC ROUTE EXHAUSTED**; `S(0)` is exactly P1, infinite Cartier kernel is stronger, finite-prefix and generic Ore induction bridges are killed | Only a Rule-30-specific all-size nonsingular Hankel-minor family (exact P1) or infinite residual family (stronger) remains; no such family is known |

## Recorded cross-route result

The dual-colex fan-out law `2,1,0^m,1 -> 1^(m+1),2` is uniform, but it does
not merge the deterministic-halving and queue-distance routes.  All frozen
logarithmic gap ranks fail and queue `21101` has two retreats with no fan-out
block anywhere in its orbit.  See `RESULTS-FANOUT-GAP-ANCESTRY.md`.

The displayed parametric fan-out family is abstract-queue admissible but not
hard-core endpoint-derived: its inverse endpoints are `2131`, `21213`, or
begin `2120`.  This weakens it as an obstruction to an actual-endpoint proof,
although the separate invariant queue `21101` still kills fan-out-only
retreat ancestry in the stronger mortality route.

The mixed resource `#1+#zero-runs` repairs that specific fan-out defect on
all registered evidence.  More importantly, colex origins expose a stronger
prefix-Hall conjecture, while the exact rightmost-pivot suffix language
reduces every nonfirst retreat to one productive `1 0^m 2` pull.  A retreat
always creates suffix `102`, so every later pull is the literal rewrite
`102->0021` on the ballistic ray `p-t=N-3`.  The weakest remaining queue
lemma is the bottom-feature crossing bound on that one ray; see
`RESULTS-MIXED-ORIGIN-RETREAT.md` and `RESULTS-PULL-RAY.md`.
The appended-coordinate parent forest weakens this further: infinitely many
pulls force one chain of unbounded pull-depth, so a one-chain feature bound
already suffices; see `RESULTS-PULL-ANCESTRY-DEPTH.md`.
For the original alternating-center application, the actual-right
`00000` prohibition gives the weaker sufficient target of excluding an
eventually syndetic pull ray with gaps in `{2,3,4,5}`.

Center-controlled reversal of the physical right half alternates the new
edge between word ends and gives a uniform descent on the `1 -> 0` phase.
The complementary phase resets it; all symmetric two-step factors and all
64 simple two-half lexicographic repairs fail by length four.  See
`RESULTS-ADAPTIVE-REVERSE-FOLD.md`.

The final route-by-route disposition and recommended continuation order are
in `RESULTS-SIX-ROUTE-EXHAUSTION.md`.

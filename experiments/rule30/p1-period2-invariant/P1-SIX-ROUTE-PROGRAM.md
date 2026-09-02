# P1 six-route exhaustion program

Date started: 2026-09-01

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
| Projected diagonal support | Prove the tail-2 `(alpha,beta)` and tail-3 `(alpha,gamma)` change at some `k>=j` on every required row | **LIVE**; complete through length 23, no proof | Derive the contrapositive from the full ordered zero-prefix queue; bounded defect annotations are killed |
| Deterministic halving | Prove `s_c(W)<=ceil(n/2)+1+s_2(L)` for `n>=4` | **LIVE**; held-out through length 64 | Retain the exact residual boundary mode. Scalar/logarithmic fan-out gap contraction is now killed |
| Queue ancestry / distance | Prove `d(r)->infinity`, equivalently constant-frontier orbit disjointness from infinite hard-core terminals | **IRREDUCIBLE TWO-LEMMA FORM**; retreat windows are disjoint and phase-gap Hall reduces exactly to at most one eventless retreat | Prove the one-zero-free-epoch lemma, then prove repeated creation of matched phase gaps requires unbounded initial ancestry. `#1+1`, fan-out-only cover, and scalar/log gap ranks are killed |
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

Center-controlled reversal of the physical right half alternates the new
edge between word ends and gives a uniform descent on the `1 -> 0` phase.
The complementary phase resets it; all symmetric two-step factors and all
64 simple two-half lexicographic repairs fail by length four.  See
`RESULTS-ADAPTIVE-REVERSE-FOLD.md`.

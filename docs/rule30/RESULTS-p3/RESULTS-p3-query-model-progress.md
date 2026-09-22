# Exact P3 results for three specified computation models

Date: 2026-09-13. **Problem 3 remains open.** This investigation proves two
restricted obstructions and supplies a paid implementation of a stronger
generic RAM simulation bound. None is an unrestricted lower bound for the
singleton center sequence, and none is a sublinear Turing-machine algorithm.

The input is the canonical binary representation of `n`, the seed is fixed,
and `c_0=1`. Every query must include its own construction and preprocessing
cost. The [scope audit](P3-SCOPE-AUDIT.md) distinguishes the official
inequivalent asymptotic formulations; the operational shortcut target remains
one uniform exact `o(n)` algorithm.

The subsequent [constructive shortcut investigation](RESULTS-p3-exact-shortcut-investigation.md)
implements ordered binary sections and tests nonlinear decimation, coupled
time-block actions, and global Newton iteration. It has not obtained a
sublinear algorithm; its new statements retain their precise model limits.

## 1. Completed results and their limits

| Result | Exact conclusion | Scope limitation |
|---|---|---|
| [Lazy local inference](RESULTS-p3-local-evaluation-barrier.md) | At least `(k+1)(k+2)/2` distinct nonfree cell inferences, `k=floor((n-1)/2)`, for every horizon | Only one-generation truth-table deductions, with memoization and free seed-cone boundaries |
| [Fixed digit actions](RESULTS-p3-digit-action-obstruction.md) | No fixed two-generator action of a nilpotent group of class at most three computes every singleton center query | A state-identity obstruction, not a bound on arbitrary algorithms or memory |
| [Paid macroblocks](RESULTS-p3-macroblocks.md) | Uniform `O(n²/log²(n+2))` word-RAM work, including a newly constructed table | Constant indexed access is charged under the stated RAM model; no improved Turing-machine bound follows |

The first bound follows from a complete local certificate lemma: each used
interior cell requires its left parent and at least one other parent. At
successive time layers, the rightmost used cell forces one new position
beyond the shifted parent set. For the first half of the query cone this
gives at least `1,2,3,...` nonfree cells. Evaluating the OR correction terms
of a diagonal jump separately still has quadratic cost: appending only a
linear number of local gates reconstructs a derivation subject to the same
bound. Rule 90 satisfies this local lower bound but has an easy singleton
center formula, explicitly preventing an unrestricted P3 interpretation.

The second obstruction concerns the actual binary index. Recursively define
`u_0=0`, `v_0=1`, `u_(j+1)=u_jv_j`, and `v_(j+1)=v_ju_j`. Their actions
agree in every group of nilpotency class at most `j`, by induction in the
lower central series. Yet the indices `10u_3=617` and `10v_3=662` have
independently recomputed values `c_617=1` and `c_662=0`. Equal actions cannot
produce these different answers from the same length-dependent initial
state and decoder. A class-four extension is separately recorded using two
existing exact archives; those larger witness bits were not regenerated.

The third result uses `t` time steps and `2t` output cells per lookup. Its
table has `2^(4t)` entries, each built with exactly `3t²-t` scalar Rule 30
evaluations. Choosing `t=max(1,floor(log2(n)/4))` makes the paid preparation
`O(n log²n)`; the retained singleton-query diamond costs `O(n²/log²n)`
lookups. The report also proves a matching lower bound inside its explicitly
exhaustive fixed-macrotable tiling architecture. Adaptive or compressed
representations are outside that lower bound.

Two-dimensional table simulation is prior art in Grandjean and Jachiet,
[§8.2 and Appendix 11](https://arxiv.org/pdf/2206.13851v2). The contribution
here is its explicit singleton-query implementation and geometry, plus the
precisely restricted model analysis. It is not a claim of a new generic
simulation method. The earlier [self-composition audit](AUDIT-natal-alsaadi-self-composition.md)
has been corrected: its `O(n²/log n)` upper bound was incorrectly described
as a ceiling on generic methods.

## 2. The remaining algorithmic obligation

These results identify specific assumptions a new shortcut must avoid.
Selecting fewer individual local deductions cannot beat the first theorem.
Batching a dense cone with one exhaustive macrotable cannot beat the third
model's bound. Replacing the ordered index history by the small nilpotent
group action in the second theorem loses information that the actual answer
needs.

The exact diagonal identity provides a concrete aggregate to work with:

\[
P_L(t,x)=\bigoplus_{j=1}^{L}
 \left(u(t-j,x-j+1)\lor u(t-j,x-j+2)\right),
\qquad
u(t,x)=u(t-L,x-L)\oplus P_L(t,x).
\]

For the center, a maximal jump reaches a known edge or exterior cell.
Consequently its complete parity is already `c_n` up to a known bit; treating
that parity as an oracle supplies no algorithm. A useful next construction
must instead evaluate such aggregates collectively, with a proved composition
law and charged cost, or give another exact query-specific representation.
The present work proves neither such a law nor a bound for one. The recent
RW/auxiliary-frontier cocycles have not been identified with this actual
singleton query and cannot be transferred by notation alone.

## 3. Reproducible exact checks

- [Local inference verifier](../../experiments/rule30/p3_local_evaluation_barrier.py)
  accepts arbitrary supplied derivation DAGs; its artifact checks every local
  partial assignment, all seven tested policies for each of Rules 30 and 90,
  and rejection of three corrupted certificates.
- [Digit-action verifier](../../experiments/rule30/p3_digit_action_obstruction.py)
  retains both independently evolved short witnesses and separately identified
  cache-supported values, with no silent fallback between those statuses.
- [Macroblock verifier and algorithm](../../experiments/rule30/p3_macroblocks.py)
  checks 4,368 complete microtable entries, 48 tiny query cases, five paid
  wrapper calls, and 1,032 geometry cases.

The universal conclusions come from the stated inductions and cost arguments.
The bounded checks validate their local premises and implementations. No paid
compute, GPU job, long-prefix regeneration, or repeated compression census
was performed.

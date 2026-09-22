# Exact affine time blocks and the missing diagonal seam information

Status: **an exact constant-size time-composition law is proved, and two
specific proposed spatial closure laws are refuted on the singleton orbit.**
The coupled two-bit repair closes at time-block lengths one and two, then
fails at length three. These statements neither supply a faster center
algorithm nor exclude other query-specific summaries or settle P3.

This is a directed repair test of the aggregate route in the
[local-evaluation report](RESULTS-p3-local-evaluation-barrier.md), not a
repeat of the full-output [Hashlife probe](RESULTS-hashlife-center.md) or
an arbitrary-input quotient-size experiment. The issue is whether a small,
exact action on a time block also contains enough information to construct
the neighboring block action.

## 1. An exact four-element time-block monoid

Let `u(t,x)` be the singleton Rule 30 evolution, with `u(0,0)=1` and
all other initial cells zero. Set

\[
 d_k(t)=u(t,k-t).
\]

Thus `k` measures distance from the moving left edge and the requested
center bit is `d_n(n)`. All operations in the next formulas are over
`GF(2)`. The local Rule 30 equation gives

\[
 d_k(t+1)=(1+d_{k-1}(t))d_k(t)+d_{k-2}(t)+d_{k-1}(t).       \tag{1}
\]

Fix the **actual** two driving traces `d_(k-2),d_(k-1)` on the time
interval `[a,a+L)`. Regarding only the entering value of `d_k` as an
unknown `z`, their induced action is affine:

\[
 S_k(a,L)(z)=Pz+Q,\qquad (P,Q)\in\{0,1\}^2.                \tag{2}
\]

The four possible actions are identity, flip, constant zero, and constant
one. They compose exactly by

\[
 (P_2,Q_2)\circ(P_1,Q_1)=(P_2P_1,\;P_2Q_1+Q_2),          \tag{3}
\]

and in particular

\[
 S_k(a,L+M)=S_k(a+L,M)\circ S_k(a,L).                      \tag{4}
\]

This is a statement about induced actions under fixed driving traces;
varying `z` does not assert a different singleton trajectory. In the
collision witnesses below every driving trace, seam endpoint, and actual
output used for comparison comes from the same genuine singleton orbit.

There is also an exact last-reset formula. Write
`u_j=d_(k-2)(a+j)` and `v_j=d_(k-1)(a+j)`. If `v_j=0` throughout,

\[
 P=1,\qquad Q=\bigoplus_{j=0}^{L-1}u_j.
\]

Otherwise let `tau` be the **last** index with `v_tau=1`. Then

\[
 P=0,\qquad Q=1+\bigoplus_{j=\tau}^{L-1}u_j.               \tag{5}
\]

Indeed, that step resets the current value to `1+u_tau`; subsequent
steps only add the later `u_j`. This locates the exact information needed
from the driving histories: the last reset and a suffix parity. Neither
quantity is supplied for free by the input `n`.

## 2. The affine summaries do not close in the spatial direction

Consider the proposed rule that would determine `S_(k+1)(a,L)` from

\[
 K_k=\bigl(S_{k-1}(a,L),S_k(a,L),
 d_{k-1}(a),d_k(a),d_{k-1}(a+L),d_k(a+L)\bigr).            \tag{6}
\]

Such a translation-invariant rule does not exist, even on actual singleton
contexts with the **same time interval**. On `[4,6)`, the contexts `k=6`
and `k=7` both have

\[
 K_k=((0,0),(0,0),0,0,0,0),
\]

but their next actions are respectively

\[
 S_7(4,2)=(0,0),\qquad S_8(4,2)=(1,1).                   \tag{7}
\]

The actual traces at times `4,5,6` are

| Column | Trace |
|---|---|
| `d4` | `111` |
| `d5` | `010` |
| `d6` | `010` |
| `d7` | `000` |
| `d8` | `110` |

Length two is the minimum possible temporal block length for this failure.
For `L=1`, `S_k=(P,Q)` recovers its two drivers:
`v=1+P` and `u=Q+v`. Given the retained entering bit `z=d_k(a)`, the next
action is exactly `(1+z,v+z)`. Thus the one-step case always closes.

Adding the diagonal index and the block phase still does not repair (6).
For `k=17,L=2`, compare `a=9` and `a=13`, which have the same phase modulo
two. Both keys are

\[
 ((1,1),(0,1),1,1,0,1),
\]

while `S18(9,2)=(0,0)` and `S18(13,2)=(0,1)`. This is a precise
nonclosure claim for these retained data. It is not a claim that retaining
the full absolute time, with unrestricted computation from it, is useless.

## 3. A full coupled two-bit action repairs only the shortest blocks

Instead of independent one-bit summaries, retain the **complete joint
action** on two adjacent unknown entering bits `(x,y)=(d_k,d_(k+1))`.
With the actual two left drivers `(u,v)=(d_(k-2),d_(k-1))` fixed, one step is

\[
 (x,y)\longmapsto
 \bigl((1+v)x+u+v,\;(1+x)y+v+x\bigr).                    \tag{8}
\]

Both right-hand sides use the old values. Define `J_k(a,L)` as the full
four-entry table obtained by composing (8) over the block, ordered by
inputs `00,01,10,11` and with outputs encoded as `2x+y`. These actions
retain nonlinear coupling and compose exactly as functions on four
states. They require four two-bit entries; this is stronger data than
two independent affine marginals.

The corresponding proposed spatial closure retains two overlapping joint
actions and all endpoints of their three-column seam:

\[
 \mathcal K_k=\bigl(J_{k-1},J_k,
 (d_{k-1},d_k,d_{k+1})(a),
 (d_{k-1},d_k,d_{k+1})(a+L)\bigr).                        \tag{9}
\]

**Exact finite closure for `L=1,2`.** For either of those fixed lengths,
(9) determines `J_(k+1)` for every locally consistent block, including
arbitrary driving data, not only the singleton. Here is a complete finite
proof domain. Choose the two left driving words
`U=(d_(k-3)(a+j))` and `V=(d_(k-2)(a+j))`, each of length `L`, and three
initial seam bits. Equation (1) then determines the entire three-column
seam. There are `2^(2L+3)` possibilities. The exact verifier lists all
32 and 128 possibilities and finds that their keys (9) are all distinct.
Consequently the key uniquely determines the history and the next action.
This exhaustive finite identity proves precisely these two lengths.

**Actual singleton failure at `L=3`.** On the same interval `[6,9)`,
the contexts `k=3` and `k=8` both have

\[
 J_{k-1}=(1,0,0,0),\qquad J_k=(3,3,1,1),
\]

and their seam endpoints both read

\[
 (d_{k-1},d_k,d_{k+1}):\quad (0,0,1)\longmapsto(0,1,1).
\]

Nevertheless,

\[
 J_4(6,3)=(3,3,3,3),\qquad J_9(6,3)=(3,2,2,2).           \tag{10}
\]

The retained full joint actions have lost the ordering of an interior
change. The actual seam traces make the missing information explicit:

| Context | `d_(k-1)` | `d_k` | `d_(k+1)` | `d_(k+2)` |
|---|---|---|---|---|
| `k=3` | `0000` | `0101` | `1111` | `0101` |
| `k=8` | `0000` | `0011` | `1111` | `0110` |

The entering bit of the next unsummarized column `d_(k+2)` also agrees,
being zero in both contexts. Its **actual departing bit differs**, one
versus zero. Thus this collision affects the genuine seed continuation,
not merely unused inputs to a formal action. Combining this witness with
the finite closure proof shows that length three is the first possible
failure for (9).

The stronger same-diagonal, same-phase control also fails. With
`k=29,L=4`, compare `a=16` and `a=24`. Both have

\[
 \mathcal K_k=((3,3,3,3),(2,2,2,2),(0,0,0),(1,1,0)),
\]

but their next actions are `(1,0,0,0)` and `(0,0,0,0)`. This last witness
concerns full actions; unlike (10), it does not assert matching actual
entering bits on the additional, unsummarized column.

## 4. Cost and precise consequence for the aggregate route

Once the driving traces are explicit, an affine block action costs `O(L)`
bit operations and constant auxiliary storage to construct. A coupled
two-bit action also costs `O(L)` with a larger constant. Two already
constructed actions compose in constant time. Using a balanced composition
tree changes parallel depth, but still requires `Theta(L)` generators
and combination operations if those generators are supplied separately.

Equations (3) and (8) therefore justify time-block composition, but not a
fast uniform procedure to obtain its inputs from `n`. In particular, the
collisions disprove using (6), or its coupled repair (9), as the proposed
spatial construction rule. Obtaining every driving bit by individual
one-generation local evaluation remains subject to the separate
[local-evaluation barrier](RESULTS-p3-local-evaluation-barrier.md).

An exact method retaining different or larger seam data, or constructing
the aggregate without termwise local evaluation, remains possible. No
lower bound on all finite summaries, no growing-width induction, and no
unrestricted P3 hardness statement follows from these four witnesses.

## 5. Maintained exact checks

Run:

```sh
uv run --offline --no-project python experiments/rule30/p3_aggregate_affine_blocks.py
```

The [verifier](../../experiments/rule30/p3_aggregate_affine_blocks.py) uses
literal numbered-rule truth-table updates in ordinary spatial coordinates
to check the diagonal recurrence and the four fixed witnesses. It also
checks all 64 affine associativity triples, the last-reset identity on all
341 driver-word pairs through length four, all splits of the eight directed
blocks, and the complete 160 short coupled histories described above.
Its longest singleton control ends at time 28. The
[artifact](../../experiments/rule30/p3-aggregate-affine-blocks.json) retains
the traces, both short closure tables, and the verifier's source hash.
This is bounded exact hypothesis discrimination, not a new orbit census.

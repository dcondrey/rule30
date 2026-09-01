# Frontier-graph theorem for the constant-tail cocycle

Date: 2026-09-01

Status: **QUEUE MORTALITY IS NOW EXACTLY A DISTANCE-DIVERGENCE THEOREM IN A
UNIFORM FAMILY OF FINITE DIRECTED GRAPHS.  THE TERMINAL SET IS PROVABLY THE
FIBONACCI-SIZED SET OF HARD-CORE INVERSE-CONE DIAGONALS.  DISTANCE DIVERGENCE
IS NOT YET PROVED, SO PERIOD-TWO MORTALITY AND P1 REMAIN OPEN.**

The solver-free checker is `constant_tail_frontier_graph.py`.

## 1. Stack the changing formulas

Fix a survival horizon `h` and stack the first `h+1` queue rows over a common
input column.  Write their vertical frontier as

```text
v=(v_0,...,v_h) in {0,1,2,3}^(h+1).
```

If the next normalized symbol of the original queue is `a in {0,1,2}`, the
queue scan recurrence gives the next vertical frontier `T_a(v)` exactly:

```text
w_0 = a,
w_j = g_(v_j)(w_(j-1)),             1 <= j <= h.    (1)
```

This follows by induction up the new column: `w_(j-1)` is the next input
symbol in row `j-1`, while `v_j` is the scan state immediately to its left in
row `j`.  Thus no bounded-window approximation is involved.

Define the labeled directed graph

```text
G_h = ({0,1,2,3}^(h+1), {v --a--> T_a(v): a in {0,1,2}}).  (2)
```

The fixed leading tail `c` puts the stack at

```text
C_h(c)=(c,...,c).                                    (3)
```

Reading the remaining symbols of a normalized queue follows the
correspondingly labeled path in `G_h`.

Each graph edge is also an exact inverse-Peel lift.  Directly from the
definition of `g`,

```text
P(T_a(v))_j = phi(w_j,w_(j+1)) = v_(j+1),
P(T_a(v)) = sigma(v).                               (4)
```

Thus a path of fixed length `d`, followed consistently as the height tends to
infinity, produces a cut `x` with

```text
P^d(x)=c^omega,  P^(d+1)(x)=0^omega,                (5)
```

because `phi(2,2)=phi(3,3)=0`.  This identifies bounded frontier distance
with the finite-Peel-rank collision isolated by the earlier rotated-triangle
and rank-zero reductions.

## 2. Identify the terminal frontiers exactly

Let `HC_(h+1)` be the words of length `h+1` over `{1,2}` avoiding `11`, and
let `I(e)` be the complete inverse-terminal-cone diagonal of `e`.  Define

```text
A_h={I(e): e in HC_(h+1)}.                           (6)
```

The right boundary of a stack surviving `h` updates is a hard-core endpoint
word `e` of length `h+1`.  Applying the local inverse-cone recurrence down
that boundary shows that its vertical terminal frontier is `I(e)`.  Conversely
the same recurrence fills the finite triangular corner between `I(e)` and
`e`; because every adjacent endpoint pair is legal, each of its `h` boundary
decoders succeeds.  Therefore

> A queue `R` with leading tail `c` survives at least `h` updates if and only
> if its suffix labels a path in `G_h` from `C_h(c)` into `A_h`.

This is an all-h equivalence, not a finite census.

The terminal map is injective: the finite triangular map `I` has the explicit
inverse `terminal_cone` (equivalently, the right-permutive local rule solves
each successive triangular cell uniquely).  The number of hard-core words of
length `h+1` satisfies the usual two-state recurrence, hence

```text
|A_h|=|HC_(h+1)|=F_(h+3).                            (7)
```

This proves the Fibonacci terminal count uniformly.  It is adjacent to, but
not the same indexed quantity as, the minimized language DFA's observed
`F_(h+4)` accepting-state count; that latter count belongs to the DFA's
representation rather than to the terminal-frontier set itself.

## 3. The exact remaining graph theorem

Let `d_h^any(c)` be directed distance in `G_h` from `C_h(c)` to `A_h`.  A
path of length `d` reads the `d` symbols after the fixed leading tail, so the
shortest surviving arbitrary normalized queue has length

```text
m_h^any(c)=1+d_h^any(c).                             (8)
```

There is a second, numerically different metric.  Every successful queue
update enters the invariant ternary language avoiding `20`, `22`, and `011`.
Take the product of `G_h` with the five-state suffix DFA for those factors and
let `d_h^SFT(c)` be its source-to-terminal distance.  Then

```text
m_h^SFT(c)=1+d_h^SFT(c)                              (9)
```

is the shortest queue in the regular language `L_h(c)` from the language
cocycle.  The two finite sequences need not agree: the unconstrained shortest
word can contain one of the three forbidden factors.

Their divergence is nevertheless equivalent.  An immortal invariant queue
is also an arbitrary one.  Conversely, the first successor of any immortal
arbitrary queue is an immortal queue in the invariant SFT.  Therefore the
strong queue-mortality theorem is exactly either pair of limits

```text
d_h^any(c) -> infinity  <=>  d_h^SFT(c) -> infinity,
for c=2,3.                                             (10)
```

Either statement is sufficient for the constant-tail separator and hence
for the remaining period-two rung.  It is stronger than the original
seed-derived statement because its initial middle word is arbitrary.

Indeed, an immortal queue of length `n` would survive every horizon and give
a bounded distance sequence.  Conversely, if either sequence is bounded,
finite branching of the ternary prefix tree gives a single finite word
occurring in every corresponding survival language, hence an immortal queue.

Both minimum sequences are nondecreasing for a uniform reason: survival for
`h+1` steps implies survival for `h` steps.  They need not increase at every
step, as the exact plateaus below demonstrate.  The missing proof is that
neither can eventually stabilize.

There is an intrinsic graph proof of this nesting.  Let `pi_h` delete the
last coordinate of a height-`h+1` frontier.  Formula (1) and prefix
compatibility of the inverse cone give

```text
pi_h T_a = T_a pi_h,
pi_h(C_h(c)) = C_(h-1)(c),
pi_h(A_h) = A_(h-1).                                (11)
```

Thus these graphs and terminal sets form an inverse system, and projecting a
path at height `h+1` gives the same labeled path at height `h`.

The projection has more structure.  After the first input, restrict to the
invariant cylinder whose first coordinate lies in `{0,1,2}`.  Split a
height-`H` frontier as `(v,z)`, where `z` is its last coordinate.  If the
projected edge sends `v` to `w` and `t` is the last coordinate of `w`, the
lifted edge is

```text
(v,z) -> (w,K_t(z)),
K_0=(0,1,3,2),
K_1=K_3=(3,2,1,0),
K_2=(2,3,1,0).                                     (11a)
```

Every `K_t` is a permutation, and these permutations generate the eight
elements

```text
(0,1,2,3), (0,1,3,2), (1,0,2,3), (1,0,3,2),
(2,3,0,1), (2,3,1,0), (3,2,0,1), (3,2,1,0),
```

which form `D8`.  Hence each added frontier coordinate is a four-sheeted
permutation cover of the preceding graph.  The expanding formula is not
discarding that coordinate: it transports it reversibly by a `D8` phase
determined by the projected path.  A distance proof must therefore control
the accumulated cover monodromy; a scalar rank that assumes fiber collapse
cannot work.

This is literally the same eight-element affine group as the boundary
permutations in `RESULTS-EVENTUAL-CONSTANT-TAIL.md`.  In coordinates
`(alpha,beta,gamma)` for

```text
(h,l) -> (h+alpha,l+beta*h+gamma),
```

the four fiber generators are

```text
t=0: (0,1,0),   t=1 or 3: (1,0,1),   t=2: (1,1,0). (11b)
```

Their path product uses the already proved three-bit law

```text
(a,b,g) after (A,B,G)=(a+A,b+B,g+G+b*A).            (11c)
```

For a fixed queue suffix `u`, let `M_H(u)` be this product along its projected
path at height `H-1`.  If `x=T_u(c^omega)`, the cover law gives the exact
coordinate formula

```text
x_(H-1)=M_H(u)(c).                                  (11d)
```

Consequently the inverse-limit collision asks for one finite `u` and one
infinite hard-core `e` satisfying

```text
I(e)_(H-1)=M_H(u)(c) for every H.                   (11e)
```

For a fixed word `u=(u_1,...,u_d)`, the complete projected frontier does have
an exact finite driver, but its size depends exponentially on `d`.  Put
`r^(0)=u` and update one vertical coordinate by

```text
s_0=c,
s_k=g_(s_(k-1))(r_k),
D_c(r)=(s_1,...,s_d).                               (11f)
```

Then the rightmost coordinate of `D_c^j(u)` is exactly `x_j`.  Thus the
height sequence and `M_H(u)` are finite-state for each fixed `u`, with at most
`4^d` driver states; the earlier dyadic cascade theorem makes their eventual
periods powers of two.  There is no fixed state bound uniform in `d`, which is
why this does not itself prove (11e).  The sharpened target is to show that no
ultimately dyadic driver output from (11f) can also be the complete
inverse-cone diagonal of an infinite hard-core endpoint.

Equivalently, on the one-sided space `X={0,1,2,3}^omega`, extend (1)
coordinate by coordinate and put

```text
O_c={T_u(c^omega): u in {0,1,2}^*},
A=I({infinite hard-core endpoint words}).            (12)
```

The arbitrary-queue distance theorem in (10) is exactly the topological
language separation

```text
O_2 intersect A = O_3 intersect A = empty.           (13)
```

If a fixed orbit word lies in `A`, all of its finite projections are
accepted and the distances are bounded by its length.  Conversely, if the
distances fail to diverge, some bound `D` works at every height.  There are
only finitely many words of length at most `D`; projection nesting (11) and
the pigeonhole principle yield one word accepted at arbitrarily large
heights, hence at every height and therefore in `A`.  This supplies the exact
compactness step—what remains unproved is the disjointness in (13).  By the
one-step SFT image theorem, restricting `u` to invariant queue words gives an
equivalent emptiness problem.

Together with (5), failure of (10) would produce one finite-Peel-rank
inverse-terminal cut over an infinite hard-core endpoint—the exact remaining
aperiodic collision, not a new loophole.  Conversely the prior rank descent
and first-infinite-tail reduction turn any such period-two counterexample
into one of these two bounded-distance modes.

This is the promised unbounded graph-theoretic target.  It does not claim
that a fixed graph or fixed-width metric captures the active cone; the graph
height grows with the formula.

## 4. A tempting first-defect induction is uniformly false

It is natural to hope that one graph edge can move the first illegal symbol
of the decoded endpoint only a bounded distance.  That would turn the graph
distance into an immediate ranking.  The hope fails for an all-length reason.

Let `e` be any finite hard-core endpoint word beginning in state `1`, and put
`y=I(e)`.  Then `y_0=B(1)=2`.  Form

```text
v = 0 . P(y).
```

Right-permutivity of `phi` and equation (4) give exactly

```text
T_2(v)=y.
```

The endpoint decoded from `v` is illegal at its first coordinate, because
cut symbol `v_0=0` decodes to endpoint state `3`.  The endpoint decoded from
`T_2(v)` is the arbitrary hard-core word `e`.  Consequently a single
inverse-Peel lift can postpone the first endpoint defect by an arbitrarily
large amount.  This does not produce a path from the constant source, but it
rules out any induction using only the first defect and one-edge Lipschitz
control.  A successful metric must retain the source ancestry or a comparable
global grammar.

The Fibonacci count in (7) likewise measures the target family but does not
separate that family from the source orbit.  Zeckendorf coding is potentially
only a change of coordinates unless it also supplies a monotone law for the
full frontier transformations.

## 5. Exact finite audit

Breadth-first search in (2), both bare and in product with the invariant SFT,
and checked against literal queue evolution, gives

```text
h:              1  2  3  4  5  6  7  8  9 10 11 12
m_h^any(2):     1  3  5  5  5 10 10 10 10 16 16 18
m_h^any(3):     2  3  5  5  5 10 10 10 12 12 15 16
m_h^SFT(2):     1  3  5  5  5 10 10 10 10 17 18 18
m_h^SFT(3):     2  3  5  5  5 10 10 10 13 14 15 16
|A_h|:          3  5  8 13 21 34 55 89 144 233 377 610
```

The four minimum rows are finite evidence only.  Equations (4), (7),
(8)-(13), and the graph construction are uniform theorems.

This frontier version is substantially smaller operationally than repeatedly
constructing and minimizing the full language DFA.  It also exposes the
actual geometry: the source is one constant vertical column, while the target
is a thin family of inverse-cone diagonals indexed by the hard-core endpoint
language.

## 6. Reproduction

From `13-rule30/`:

```bash
uv run python \
  experiments/rule30/p1-period2-invariant/constant_tail_frontier_graph.py \
  --max-horizon 12
```

The script constructs all `F_(h+3)` terminal diagonals, searches the exact
frontier graph, reconstructs a shortest queue and endpoint witness, and then
checks that queue against the literal growing cocycle for all `h` updates.  It
also compares graph acceptance with every normalized queue through suffix
length six at horizons one through five; that bounded comparison is a
regression guard for the uniform column and terminal-frontier proofs above.
Height projection is independently checked on every frontier through height
six.  The four-sheeted cover law is checked on every edge through height six,
and the generated permutation group is closed exactly to the displayed eight
elements.  The affine generator coordinates and literal path products are
independently checked on every ternary word through length four and heights
two through five.  The `4^d` vertical driver is matched to literal frontier
columns for every ternary word through length four and height six.

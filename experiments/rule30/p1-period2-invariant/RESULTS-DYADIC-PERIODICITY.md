# Dyadic periodicity mismatch: exact graph audit

Date: 2026-09-01

Status: **THE ZERO-RAY CASCADE HAS ONLY DYADIC EVENTUAL PERIODS, BUT THE
PROPOSED ACCEPTANCE MISMATCH IS FALSE.  NO MORTALITY OR PERIOD-TWO THEOREM IS
PROVED.**

The solver-free checker is `dyadic_periodicity_analyzer.py`.  It uses only
finite transformation closure, functional-graph SCC decomposition, and an
exact recurrence for the inverse terminal cone.  It runs no SAT instance and
contains no finite-width clause search.

## 1. Three graphs that must be distinguished

Write `Q={0,1,2,3}` for the two-bit carry codes and let `sigma` swap their
bits.  The exact carry permutations

```text
tau_0 = (0,1,3,2)
tau_1 = (2,3,1,0)
tau_2 = (3,2,1,0)
tau_3 = (3,2,1,0)
```

are the rows of `FORWARD`, so feeding symbol `q` sends carry `s` to
`tau_q(s)` and passes `sigma(tau_q(s))` upward.

The raw labelled carry graph has one SCC, `Q`, and simple cycles of lengths
`1,2,3,4`.  In particular,

```text
0 --1--> 2 --0--> 3 --3--> 0                         (1)
```

is a simple odd cycle.  Thus the unrestricted statement that the `feed`
transition graph has only power-of-two cycles is false.  The true dyadic
statement concerns the more constrained triangular cascade on a zero input
ray.

For a word `u=(q_1,...,q_m)`, compose the `m` feed generators and apply them
to `000...`.  At spatial layer `t`, their internal symbols form a word
`z(t) in Q^m`.  Define `T_m` by starting with `s_0=0` and setting

```text
s_i = tau_(z_i)(s_(i-1)),
(T_m z)_i = sigma(s_i).                               (2)
```

The emitted cut symbol is `s_m`.  Hence the infinite cut `A_u(000...)` is
the output sequence of the finite functional graph `T_m` from initial state
`u`.

## 2. The dyadic cascade theorem

For an already-updated preceding coordinate `r`, the fiber map on the next
old symbol is

```text
h_r(q) = sigma(tau_q(sigma(r))).                      (3)
```

The four maps, in image-tuple notation, are

```text
h_0=(0,1,3,3)  h_1=(3,2,2,2)
h_2=(2,3,1,1)  h_3=(1,0,0,0).
```

Their transformation monoid has exactly the following 13 elements:

```text
(0,0,0,0) (0,1,1,1) (0,1,2,3) (0,1,3,3)
(1,0,0,0) (1,1,1,1) (1,1,3,3)
(2,2,2,2) (2,3,1,1) (2,3,3,3)
(3,2,2,2) (3,3,1,1) (3,3,3,3).
```

Direct composition by each generator closes this list.  The cyclic SCCs of
every listed transformation have length one or two; the checker prints each
one.  This finite multiplication table supplies the fiber lemma used below.

**Theorem (dyadic zero-ray cascade).** Every periodic orbit of `T_m` has
length a power of two.  Consequently, for every finite word `u`, the cut
`A_u(000...)` is ultimately periodic with minimal eventual period a power of
two.

**Proof.** Induct on `m`.  The projection deleting the last coordinate
intertwines `T_m` with `T_(m-1)`.  Let a periodic orbit of `T_m` project to an
orbit of period `p`.  By induction, `p` is a power of two.  During one turn
around that projected orbit, the last coordinate is acted on by a composition
of the fiber maps (3), hence by one of the 13 monoid elements.  Its return
cycle has length `l in {1,2}`.  The full orbit therefore has length `p*l`,
again a power of two.  The base `T_0` has period one.  An arbitrary initial
state eventually enters a periodic orbit, and an output period divides its
state period.  QED.

The exhaustive SCC census through `m=8` is a check of the theorem, not its
basis.  Its cycle lengths are `1,2,4`; the 13-element fiber lemma makes the
induction uniform in `m`.

## 3. Exact inverse-terminal graph

The acceptance side does not use the same graph.  Put

```text
B(r)       = tau_3^(-1)(r),
phi(l,r)   = tau_(sigma(l))^(-1)(r).                  (4)
```

If `U_k` denotes inverse-feeding a terminal `3` starting at coordinate `k`,
then for its input row `y`,

```text
(U_k y)_j = y_j                 for j<k,
(U_k y)_k = B(y_k),
(U_k y)_j = phi(y_(j-1),y_j)    for j>k.              (5)
```

Let `e` be the endpoint word and let `x` be its inverse-terminal cut.  Define
arrays

```text
Z_0[k] = B(e_k),
Z_1[k] = phi(e_k,B(e_(k+1))),
Z_t[k] = phi(Z_(t-2)[k+1], Z_(t-1)[k+1])  (t>=2).    (6)
```

Induction down the triangular sequence
`U_(H-1),...,U_1,U_0` gives the exact identity

```text
x_t = Z_t[0].                                          (7)
```

The checker compares (6) literally with the original forward/inverse cone
code on all 21,844 arbitrary endpoint words through length seven.

When `e` has spatial period `p`, (6) is a finite functional graph on pairs of
`p`-vectors:

```text
G_p(U,V) = (V,W),
W_k = phi(U_(k+1 mod p), V_(k+1 mod p)).              (8)
```

Cycle detection in (8), followed by exact divisor testing of its output
block, gives minimal periods without a horizon heuristic.  For primitive
cyclic hard-core endpoints, the first values are:

| endpoint period | number of necklaces | inverse-cut periods |
|---:|---:|---|
| 1 | 1 | `2` |
| 2 | 1 | `28` |
| 3 | 1 | `28` |
| 4 | 1 | `28` |
| 5 | 2 | `310` (both) |
| 6 | 2 | `276` (both) |
| 7 | 4 | `728` (three), `1316` (one) |
| 8 | 5 | `1016` (one), `5200` (four) |
| 9 | 8 | `1962` (three), `2025` (four), `8370` (one) |
| 10 | 11 | `310` (six), `25000` (five) |

This rigorously reproduces the observed odd factors for the displayed
nonconstant periodic endpoints.  It is a finite census, not an all-period
theorem.

## 4. The acceptance premise has a uniform counterfamily

The sole period-one hard-core endpoint is

```text
e = 2222....
```

Equations (4)-(8) give

```text
inverse_terminal(e) = 121212....,
terminal_cone(121212....) = 222222....                 (9)
```

and the cut in (9) has minimal period two.  It passes every pin and forces
`rho=0` forever.  This is the same accepted point already recorded in
`RESULTS-CORE-INTERPOLANT.md`.

The exception is not isolated.  From (6), `Z_t[k]` depends only on endpoint
coordinates

```text
k + floor(t/2), ..., k+t.                             (10)
```

This follows immediately by induction in (6).  Therefore every hard-core
endpoint that is eventually all `2` has an inverse-terminal cut eventually
equal to `1212...`: once `t>=2N`, the dependency interval (10) lies beyond an
endpoint prefix of length `N`.  There are infinitely many such endpoints,
and their cuts are distinct because the terminal-cone map is bijective on
every prefix.

Thus the proposed assertion that an infinite accepted cut must traverse a
cycle with an odd prime factor is false, even after replacing one exceptional
point by an eventual-period formulation.  The accepted language contains an
infinite ultimately-period-two subfamily.

## 5. Why the topological contradiction does not follow

The proved and refuted statements are now:

```text
reachable zero-ray cuts  -> eventual period 2^k        PROVED
all accepted cuts        -> eventual period with odd factor  FALSE
```

In particular, the reachable and accepted period spectra overlap at period
two.  Period information alone cannot decide whether their languages
intersect.  Even a proof that all other accepted cycles have odd factors
would leave the entire eventually-`1212` acceptance family to exclude.
Moreover, showing that an intersection is finite would not prove it empty;
mortality requires empty intersection.

The exact remaining obligation is unchanged:

> Prove that the orbit of `000...` under all finite positive feed-generator
> words is disjoint from the inverse-terminal hard-core language.

The dyadic theorem is a useful restriction on that orbit, but it is not the
missing separator.  A successful continuation must distinguish the actual
dyadic orbit from the accepted ultimately-period-two family, rather than
separate only their possible period integers.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/dyadic_periodicity_analyzer.py
```

The default run constructs exact cascade SCCs through width eight and exact
accepted periodic orbits through primitive endpoint period ten.  These bounds
are diagnostics only; the cascade theorem is the symbolic induction in
Section 2, while (9)-(10) are uniform counterexamples to the proposed
acceptance premise.

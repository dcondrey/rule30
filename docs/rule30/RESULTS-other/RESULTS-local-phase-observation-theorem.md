# Finite local statistics can hide every rational spatial phase

**Status:** an exact all-length theorem for periodic inputs. This strengthens
[the quarter-wave atom theorem](RESULTS-quarter-wave-atom-propagation.md).
It is not a result about the lone-seed orbit and does not settle P1, P2, or P3.
The circulation argument is a general tool; its literature priority has not
been established.

## 1. A general constructive observation lemma

Let \(H\) be a binary cellular automaton with radius \(R\), and set
\(n=2R+1\). Fix a phase order \(q\ge2\), a nontrivial \(q\)th root of
unity \(\zeta\), and a ring length \(N\) divisible by \(q\) with
\(N>4R\). Regard

\[
Q_H(x;\zeta)=\sum_{j=0}^{N-1}\zeta^j H(x)_j
\]

as its unique ordinary complex multilinear polynomial on the binary cube.
Suppose it has a nonzero coefficient on a monomial with support \(B\) and
degree \(d>k\). Then there is **one periodic binary row** \(w\) such that:

* Every binary \(k\)-block occurs equally often at every phase modulo \(q\),
  and all \(2^k\) blocks have equal frequencies within each phase.
* \(Q_H(w;\zeta)\ne0\).

The first property implies zero nontrivial \(q\)-phase Fourier sums for
every observable on \(k\) consecutive cells. It is stronger than merely
requiring a zero coordinate Fourier coefficient. The hypotheses are about an
ordinary polynomial; GF(2) degree cannot be substituted without a separate
survival argument.

### Proof by an explicit mixed difference

Use the phase-expanded de Bruijn graph with vertices
\((b_0\cdots b_{n-2},a)\), \(a\in\mathbb Z/q\mathbb Z\), and edges

\[
(b_0\cdots b_{n-2},a)
\longrightarrow(b_1\cdots b_{n-1},a+1).
\]

For \(S\subseteq B\), let \(x^S\) be the period-\(N\) row with ones exactly
at \(S\). Its \(N\) consecutive windows give an integer circulation
\(C(x^S)\) on this graph, assigning to an edge its number of occurrences
with the designated phase. Define the signed integer circulation

\[
v=\sum_{S\subseteq B}(-1)^{d-|S|}C(x^S).
\tag{1}
\]

For each fixed phase \(a\) and \(k\)-block \(u\), the count

\[
\sum_{j\equiv a\; (q)}\mathbf1_{x_j\cdots x_{j+k-1}=u}
\]

is an ordinary multilinear polynomial of degree at most \(k\). Its mixed
difference (1) therefore vanishes. This holds **separately at each phase**,
without complex cancellation between phases.

The output functional on an edge weights the output of its centered local
map by \(\zeta^a\). Its value on \(v\) is \(\zeta^{-R}\) times the
specified nonzero coefficient of \(Q_H\). Thus the output functional does
not vanish on \(v\).

Let \(u_e=1\) on every edge. This is an integer circulation; its output
Fourier sum vanishes because \(\sum_{a=0}^{q-1}\zeta^a=0\). Pick an integer
\(M>\max_e|v_e|\). The flow \(v+Mu\) is strictly positive. The graph is
strongly connected: a path may append any prescribed ending word after a
long enough prefix, and its length can be chosen in any residue class modulo
\(q\). It therefore admits a single Euler tour with these multiplicities.
Start that tour at phase zero and read its overlapping bits as \(w\).

The tour length is divisible by \(q\), and its output Fourier sum is the
nonzero number \(\zeta^R B(v)\). Every \((k\text{-block},a)\) count is
exactly \(M2^{n-k}\), since (1) has zero such counts. Finally,

\[
\sum_e v_e=N\sum_{S\subseteq B}(-1)^{d-|S|}=0,
\]

so the period supplied by the construction is exactly \(Mq2^n\). A crude
general choice is \(M=N2^d+1\). This is one Eulerian row, not a mixture of
periodic rows. Its minimal period may divide the supplied period.

## 2. Rule 30: one row exposes every nontrivial phase frequency

**Theorem.** Fix \(q\ge2\), \(t\ge3\), and \(k<2t-1\). There is one
periodic binary row \(w\), with a supplied period

\[
p=Mq2^{2t+1},\qquad M=1+\lceil3/q\rceil
=\begin{cases}3,&q=2,\\2,&q\ge3,\end{cases}
\tag{2}
\]

such that:

1. Every \(k\)-block occurs exactly \(M2^{2t+1-k}\) times in **each** phase
   modulo \(q\).
2. For **every** nontrivial \(q\)th root of unity \(\zeta\),
   \(\sum_{j=0}^{p-1}\zeta^j(F^t w)_j\ne0\).

Thus the uniform spatial-phase measure of this row has zero spectral atoms
at all nontrivial \(q\)-phase frequencies for every \(k\)-cell observable,
while its time-\(t\) coordinate observable has a nonzero atom at every one of
those frequencies. The same row works simultaneously for all of them.

### The ordinary coefficient survives at every root of unity

Write \(n=2t+1\) and \(d=2t-1\). The established
[all-length ANF theorem](overnight/RESULTS-anf.md) states that for \(t\ge3\)
the center function has GF(2) degree \(d\), with unique top monomial
\(\prod_{r=-t+2}^{t}x_r\).

On an auxiliary ring with \(N>4t\), choose \(B=\{2,\ldots,2t\}\).
The monomial supported on \(B\) fits into exactly three output light cones,
centered at \(t,t+1,t+2\). Let their ordinary integer coefficients be
\(c_0,c_1,c_2\). Integer multilinear coefficients reduce modulo two to ANF
coefficients. Therefore

\[
c_0\text{ is odd},\qquad c_1,c_2\text{ are even}.
\tag{3}
\]

Its coefficient in the weighted output is

\[
\zeta^t(c_0+c_1\zeta+c_2\zeta^2).
\tag{4}
\]

For every root of unity, the factor in parentheses is \(1+2z\) for some
\(z\in\mathbb Z[\zeta]\). It cannot vanish: otherwise \(-1/2\) would be
an algebraic integer, whereas a rational algebraic integer is an integer.
No assumption that \(\zeta\) is primitive is needed. This is an ordinary
integer-to-cyclotomic argument, not substitution of a complex number into
an identity asserted only over GF(2).

### A smaller flow makes the period bound explicit

In (1), all edge windows not containing \(B\) have mixed difference zero.
The only surviving window starts are \(0,1,2\). At each start, the map from
\(S\subseteq B\) to its binary edge word is injective, so it contributes
only \(+1\) or \(-1\) to any edge multiplicity. The three consecutive
starts assign at most \(\lceil3/q\rceil\) contributions to one phase.
Hence

\[
|v_e|\le\lceil3/q\rceil.
\]

The choice in (2) makes every edge strictly positive. It is independent of
\(\zeta\), so a single Euler tour works for every nontrivial \(q\)th root.

More explicitly, because each iterated Rule 30 center function is balanced
under uniform inputs, the output one-counts by phase satisfy

\[
\#\{j\equiv a\pmod q:(F^t w)_j=1\}
=M2^{n-1}+
\sum_{r=0}^2c_r\mathbf1_{a\equiv t+r\pmod q}.
\tag{5}
\]

This gives a directly checkable integer certificate before taking Fourier
transforms. Each input has exactly uniform local phase statistics, but its
future coordinate distinguishes those phases.

## 3. What this does and does not distinguish

The exact law \(\deg_{\mathbb F_2}f_t=2t-1\) is specific to Rule 30 and
separates it from additive Rules 90 and 150, whose iterated GF(2) degrees
remain one. **The general failure of local phase-observation closure is not
exclusive to nonlinear GF(2) rules.**

For example, Rule 90 sends \(00001111\) to \(10011001\): the input quarter
sum is zero and the output sum is \(2-2i\). More generally, at
\(t=2^m-1\), Rule 90 outputs the parity of \(2^m\) distinct initial bits.
The ordinary multilinear polynomial of that parity has a unique top monomial
of degree \(2^m\), with coefficient \((-2)^{2^m-1}\). On a sufficiently
large ring, a weighted spatial sum retains that monomial from one translated
output. The general lemma therefore gives all-width phase-observation
counterexamples for Rule 90 as well. Boolean linearity and ordinary real
polynomial degree are different notions here.

The Rule 30 result concerns arbitrary periodic inputs; it does not rule out
a finite collection with additional structure specific to the lone seed,
nor a nonlocal representation. The actual seed may satisfy spectral
restrictions absent from these other inputs. Establishing those restrictions
remains a separate problem.

This theorem makes the logical scope of local spectral arguments precise.
It is not a proof of chaotic mixing, entropy generation, computational
irreducibility, or any of the three prize conjectures. Its publishable novelty
must be checked against work on periodic realizations of block frequencies,
symbolic dynamics, and local observation of factors.

## 4. Exact finite verification

The independent integer verifier constructs the signed three-cube flow,
checks conservation at every vertex and zero phase-specific counts at every
width through \(k\), realizes one Euler word, re-counts all its \(n\)-blocks,
and compares scalar Rule 30 evolution with cyclic packed-integer evolution.
It also checks (5) using an integer Mobius transform of the local truth table.

At \(t=3\), \(k=4\), the coefficients are \((c_0,c_1,c_2)=(1,2,0)\):

| Phase order \(q\) | Supplied period | Output one-counts by phase |
|---:|---:|---|
| 2 | 768 | \(194,193\) |
| 3 | 768 | \(129,130,128\) |
| 4 | 1024 | \(130,128,128,129\) |
| 5 | 1280 | \(128,128,128,129,130\) |

For each example every input four-block has the same count in each phase:
24 when \(q=2\), and 16 otherwise. The nonzero output Fourier statements
follow exactly from (3), not from floating-point eigenvalues.

Reproduce:

```sh
uv run python experiments/rule30/local_phase_observation_certificate.py
```

[Verifier](../../experiments/rule30/local_phase_observation_certificate.py)
and [exact certificate](../../experiments/rule30/local-phase-observation-certificate.json).

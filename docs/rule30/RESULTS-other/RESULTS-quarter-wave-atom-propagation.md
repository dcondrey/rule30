# Quarter-wave atoms can be hidden from every fixed local observation width

**Status:** exact periodic counterexamples and an all-length obstruction for
arbitrary input rows. Neither result proves nor disproves P1, P2, or P3 for
the lone seed.

The sufficient spectral criterion in
[the skew-product report](RESULTS-quarter-wave-skew-product.md) remains valid:
zero coordinate spectral mass at quarter frequencies for every actual spatial
cluster measure implies the quarter-wave potential is sublinear. The issue
here is propagation of that premise. **Absence of a coordinate atom need not
survive even one Rule 30 step.** Adding any fixed finite collection of local
observables cannot give a universal, temporally preserved version of that
premise.

## 1. An exact one-step example

For a binary periodic word (w) of period (p), with (4\mid p), put

\[
Q(w)=\sum_{j=0}^{p-1}i^j w_j.
\]

Let \(\mu_w\) be uniform spatial phase on the periodic configuration. For the
coordinate observable \(h(x)=x_0\), its spectral mass at each of the spatial
eigenvalues \(i,-i\) is

\[
\sigma_{h,\mu_w}(\{i\})
=\sigma_{h,\mu_w}(\{-i\})=\frac{|Q(w)|^2}{p^2}.
\]

This is the finite Fourier formula; it also holds if \(p\) is a multiple of
the minimal period. Using centered bits changes only the zero-frequency
coefficient.

Rule 30 on cyclic words gives

\[
w=00001111\quad\longmapsto\quad Fw=10011000.
\]

The four phase classes contain equal input one-counts, hence \(Q(w)=0\).
The output ones are at positions \(0,3,4\), so

\[
Q(Fw)=2-i,\qquad
\sigma_{h,F_*\mu_w}(\{\pm i\})=\frac5{64}.
\]

Although \(F\) commutes with the spatial shift, the spectral measure of
\(h\) under \(F_*\mu\) is the spectral measure of **\(h\circ F\)** under
\(\mu\). Commutation does not identify this with the spectral measure of
\(h\) under \(\mu\). The period-eight shift system already contains a
quarter-periodic eigenfactor; the coordinate initially fails to detect it.
Rule 30's nonlinear observable detects it at the next step.

## 2. All-length finite-observation obstruction

**Theorem.** Fix any \(k\ge1\), and any \(t\ge3\) such that \(2t-1>k\).
There is a binary periodic row \(w\), of a period divisible by four, such
that:

1. For every real observable \(\phi\) depending on \(k\) consecutive cells,
   \(\sum_j i^j\phi(\sigma^j w)=0\). Equivalently, each such observable has
   zero spectral mass at both quarter frequencies under \(\mu_w\).
2. \(Q(F^t w)\ne0\). The output coordinate has a nonzero quarter atom.

The row is allowed to depend on \(k,t\). The theorem does not exhibit one row
invisible at every finite width: all cylinder observables together detect the
whole spatial eigenfactor.

### 2.1 A surviving ordinary multilinear coefficient

We use the established all-length theorem in
[RESULTS-anf.md](overnight/RESULTS-anf.md): for \(t\ge3\), the center output
\(f_t\), as an algebraic normal form over \(\mathbb F_2\), has degree
\(d=2t-1\), and its unique degree-\(d\) monomial is

\[
M_t=\prod_{r=-t+2}^{t}x_r.
\]

This fact must be transferred to an **ordinary integer multilinear
polynomial**, not evaluated over complex numbers inside \(\mathbb F_2\).
Every Boolean function has a unique integer multilinear representation on
the Boolean cube, obtained by the integer Mobius transform. Reducing those
integer coefficients modulo two gives its algebraic normal form. Thus the
integer coefficient of \(M_t\) is odd, while every other degree-\(d\)
coefficient is even. Integer coefficients of higher degree may exist; they
do not affect the coefficient considered below.

Take a ring of length \(N>4t\), with \(4\mid N\), and consider the ordinary
complex multilinear polynomial

\[
Q_t(x)=\sum_{j=0}^{N-1}i^j(F^t x)_j.
\]

The fixed monomial \(\prod_{r=2}^{2t}x_r\) fits into exactly three output
light cones, centered at \(t,t+1,t+2\). Their integer coefficients are
\(c_0,c_1,c_2\), where \(c_0\) is odd and \(c_1,c_2\) are even, by the
unique top monomial theorem. Its coefficient in \(Q_t\) is consequently

\[
i^t c_0+i^{t+1}c_1+i^{t+2}c_2
=i^t+2z\ne0\qquad(z\in\mathbb Z[i]).
\]

The last inequality holds because a Gaussian unit is not divisible by two.
Therefore \(Q_t\) has ordinary multilinear degree at least \(d>k\).
In contrast, every real or complex linear combination of quarter-wave sums
of \(k\)-cell observables has degree at most \(k\) on this ring. Allowing
separate real and imaginary parts does not change that degree bound.

### 2.2 From nonmembership to one periodic row

Let \(n=2t+1\). Form the finite directed graph whose vertices are
\((v,a)\), with \(v\) a binary word of length \(n-1\) and
\(a\in\mathbb Z/4\mathbb Z\). For every binary \(n\)-block
\(b=b_0\cdots b_{n-1}\), there is an edge

\[
(b_0\cdots b_{n-2},a)
\longrightarrow(b_1\cdots b_{n-1},a+1).
\]

Let \(C\) be its real circulation space: incoming and outgoing total
weights agree at each vertex. Define the real linear constraint map \(A\)
by collecting the real and imaginary parts of

\[
A_u(v)=\sum_{(b,a)} i^a
  \mathbf1_{b_0\cdots b_{k-1}=u}\,v_{(b,a)}
\quad(u\in\{0,1\}^k),
\]

and define the complex output functional

\[
B(v)=\sum_{(b,a)}i^a f_t(b)\,v_{(b,a)}.
\]

Suppose \(B\) vanished on \(C\cap\ker A\). Finite-dimensional real linear
algebra would give \(B=L A\) on \(C\), for a real-linear map \(L\) into
\(\mathbb C\): a functional vanishing on the kernel factors through the
constraint map. Apply this identity to the circulation traced by every
binary period-\(N\) row on the ring from Section 2.1. The constraints are
quarter-wave sums of \(k\)-block indicators, whereas the output is
\(i^{-t}Q_t(x)\), because the edge starts \(t\) cells left of its output
center. This contradicts the ordinary multilinear degree distinction.

Hence there is \(v\in C\cap\ker A\) with \(B(v)\ne0\). All defining
matrices have integer entries after splitting real and imaginary parts.
Their nullspace has a rational basis, so \(v\) can be chosen rational and
then scaled to integer entries.

The constant edge flow \(u_e=1\) is a circulation and satisfies
\(A(u)=B(u)=0\): for each fixed block, summing the four phase weights gives
\(1+i-1-i=0\). Choose an integer \(M>\max_e|v_e|\). Then

\[
q=v+Mu
\]

is a strictly positive integer circulation with \(A(q)=0\) and
\(B(q)\ne0\). The graph is strongly connected: from any vertex one may
append an arbitrary sufficiently long word ending in a prescribed target
word, choosing the length in the required residue class modulo four.
Thus the directed multigraph with edge multiplicities \(q_e\) has one
Euler tour, which we start at a vertex of phase zero. Reading its overlapping
binary blocks produces **one** periodic
binary row, not a mixture of rows. The tour returns to its starting phase,
so its length is divisible by four. Its constraints give all the required
zero input quarter sums, while its output sum is the nonzero number
\(i^t B(q)\). This proves the theorem.

## 3. What stronger premise is preserved

There is a correct distinction between a spectral property of one observable
and a spectral property of the entire spatial system. If a shift-invariant
measure \(\mu\) has **no quarter eigenfunctions at all** in \(L^2(\mu)\),
then neither does \(F_*\mu\). Indeed, pullback

\[
U_F:L^2(F_*\mu)\to L^2(\mu),\qquad U_F\psi=\psi\circ F,
\]

is an isometry intertwining the spatial shifts. Any nonzero quarter
eigenfunction in the image measure would pull back to one in the original
measure. Full weak mixing is more than this argument needs.

Equivalently, requiring zero quarter spectral projection for **every**
cylinder observable is sufficient, since cylinder functions are dense in
\(L^2(\mu)\). The theorem above shows why no fixed finite observation width
can replace this universal premise for arbitrary input rows.

This is a failure of invariance for fixed-width cylinder atom-absence. It is
not an obstruction to every finite-state or nonlocal representation, and it
does not exclude a finite collection whose additional structure is specific
to the lone-seed orbit.

This preservation fact cannot be applied directly to the lone seed's
time-dependent spatial windows. Their limiting measures are not obtained
by taking a single fixed shift-invariant initial measure and pushing it
forward before the spatial limit. The actual seed cluster measures still
require a separate argument. The example and theorem here leave the
seed-specific criterion in the skew-product report intact.

## 4. Exact finite checks

The verifier checks the period-eight example and constructs periodic rows
containing each pair \((k\text{-block},\text{phase})\) exactly once. Such rows
have stronger input balance than the theorem needs: all blocks through
length \(k\) have the same counts in each phase class. Scalar and packed
integer Rule 30 updates agree for every checked step.

| \(k\) | Output time | Input period | Output quarter sum |
|---:|---:|---:|---:|
| 1 | 3 | 8 | \(2-i\) |
| 2 | 3 | 16 | \(-2i\) |
| 3 | 3 | 32 | \(-1+i\) |
| 4 | 3 | 64 | \(-2-5i\) |
| 5 | 4 | 128 | \(5-2i\) |
| 6 | 4 | 256 | \(9+4i\) |
| 7 | 5 | 512 | \(-5+8i\) |
| 8 | 5 | 1024 | \(18+15i\) |

The integer Mobius transform also checks the surviving ordinary polynomial
coefficient independently at \(t=3,4,5,6\). The three contributing integer
coefficients are respectively \((1,2,0),(1,2,-8),(-1,2,-4),(-5,-4,0)\).
These finite checks validate explicit witnesses and the indexing; the
all-length theorem rests on the proof above and the established ANF theorem.

Reproduce without writing files:

```sh
uv run python experiments/rule30/quarter_wave_atom_propagation.py
```

Exact data: [quarter-wave-atom-propagation.json](../../experiments/rule30/quarter-wave-atom-propagation.json).
Verifier: [quarter_wave_atom_propagation.py](../../experiments/rule30/quarter_wave_atom_propagation.py).

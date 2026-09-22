# Fibonacci interpolation: fixed columns and the moving center

Date: 2026-09-14

The supplied notebook's Fibonacci interpolation is a valid fixed-column
identity. **Every center query lies among the initial samples it requires.**
The identity therefore supplies no reduction of the center query. Separately,
its exponentially growing integer-polynomial degree does not force
exponential center computation: support indices above the requested time can
be discarded throughout the exact support recurrence. This gives a
polynomial algorithm, without improving the known direct evolution bound.

This supplements the preserved [2026-09-03 query audit](REFUTATION-nersissian-log-query.md).
It does not claim a new interpolation or truncation method, a computational
lower bound, or a solution of any Rule 30 prize problem.

## 1. Primary sources and coordinates

The [supplied Wolfram Cloud notebook](https://www.wolframcloud.com/obj/90ec1460-afdd-4dfe-a2d4-90cd535694ae)
was read through its [public notebook download](https://www.wolframcloud.com/download/90ec1460-afdd-4dfe-a2d4-90cd535694ae)
on 2026-09-14, without executing Mathematica. Its section on the right-column
recurrence contains Definition 5, `r30Column`, and Theorem 3 (Fibonacci
dependency). It attributes its companion framework to T. Nersissian,
*Unified Theory of Deterministic Cellular Automata*,
[DOI 10.5281/zenodo.21306383](https://doi.org/10.5281/zenodo.21306383).
The downloaded notebook does not state a separate publication date. The
author's [support-recurrence question](https://mathematica.stackexchange.com/questions/318912/rule-30-finding-a-closed-formula-for-the-s-m-subset-recurrence)
was also read on 2026-09-14; it explicitly seeks a fast construction of the
support sets. We audit the displayed formulas, not uninspected claims in the
companion paper.

For the singleton evolution \(x_t(i)\), put

\[
R_k(t)=x_t(t-k).
\]

The displayed right-column recurrence is

\[
R_k(t+1)=R_k(t)+R_{k-1}(t)+R_{k-2}(t)
               +R_{k-1}(t)R_{k-2}(t)\pmod2,
\]

with \(R_k(0)=1\) exactly at \(k=0\), and negative columns zero. In these
coordinates **the center is \(R_t(t)\)**. The support question uses the shifted
index \(m=k+1\), giving its equivalent identity \(c(t)=b(t+1,t)\).

## 2. What the Fibonacci interpolation proves

Lift the recurrence to ordinary integer addition and multiplication. The
resulting integer-valued polynomials satisfy

\[
P_0(t)=1,\quad P_1(t)=t,\quad P_k(0)=0\ (k\ge1),\qquad
\Delta P_k=P_{k-1}+P_{k-2}+P_{k-1}P_{k-2}.
\]

Their reductions modulo 2 are \(R_k\). Each polynomial has positive leading
coefficient. For \(k\ge2\), the product has degree at least either summand's
degree; any tie adds positive leading coefficients. Discrete integration
increases degree by one and preserves positive leading coefficient. Thus

\[
d_0=0,\quad d_1=1,\quad d_k=d_{k-1}+d_{k-2}+1,
\qquad d_k=F_{k+2}-1.
\]

Set \(F=F_{k+2}\). Ordinary interpolation at nodes \(0,\ldots,F-1\) gives,
for integer \(t\ge F\),

\[
P_k(t)=\sum_{r=0}^{F-1}\lambda_r(t)P_k(r),\qquad
\lambda_r(t)=(-1)^{F-1-r}\binom tr
                         \binom{t-r-1}{F-1-r}.
\]

These weights are **integers**, so replacing each \(P_k(r)\) by its parity
is valid. Substituting \(p=F-r\) gives exactly the notebook's displayed
weight

\[
\binom{t-1}{F-1}\binom Fp
\frac{(-1)^{p+1}tp}{F(t-F+p)}.
\]

Hence the fixed-column identity is sound; rational-looking weights do not
invalidate its reduction modulo 2. It determines a column from at most
\(F\) initial values, without proving that this many values are necessary.

For the center, \(k=t\), and

\[
F_{t+2}\ge t+1>t\qquad(t\ge0).
\]

The inequality follows from the Fibonacci recurrence and the initial cases.
Consequently **no center query meets the reconstruction condition
\(t\ge F_{k+2}\)**. The required initial list contains its target \(R_t(t)\).
Extending the Lagrange polynomials to the initial nodes does not help:
\(\lambda_r(t)=\mathbf1_{r=t}\) there. That extension merely returns the
already supplied target sample. This is a domain obstruction to this
particular center reduction, not a restriction on every possible use of the
integer lift.

## 3. Exact support cutoff and its paid algorithm

Over \(\mathbb F_2\), let \(f_m\) indicate the question's finite support set
\(S_m\). Its recurrence is

\[
f_1=\mathbf1_0,\quad f_2=\mathbf1_1,\qquad
f_m=I(f_{m-1}*f_{m-2}+f_{m-1}+f_{m-2}),
\]

where \(I\) raises the integer index by one and \(*\) is parity convolution
under bitwise OR. Let \(\pi_n\) discard indices above \(n\). Then

\[
\pi_nI f=\pi_nI\pi_nf,\qquad
\pi_n(f*g)=\pi_n((\pi_nf)*(\pi_ng)).
\]

Indeed, increment never decreases an index, and \(a\mathbin{\mathrm{OR}}b
\ge\max(a,b)\). Thus high discarded coefficients cannot return to the
retained interval. Induction preserves exactly \(f_m(0),\ldots,f_m(n)\) at
every stage. All terms in the final Lucas evaluation of \(c(n)\) have index
at most \(n\), so this cutoff preserves the answer for every \(n\).

An explicit implementation uses Boolean tables of length
\(L=2^{\lceil\log_2(n+1)\rceil}<2(n+1)\). Zero entries above \(n\) are
restored after every advance. The subset-zeta transform \(Z\) satisfies

\[
Z(f*g)=(Zf)(Zg),\qquad Z^2=1\quad\text{over }\mathbb F_2.
\]

Three transforms and a pointwise Boolean expression therefore implement one
advance in \(O(L\log L)\) Boolean butterfly and table operations. There are
exactly \(n-1\) advances for \(n\ge1\). The total is
**\(O(n^2\log(n+1))\) scalar Boolean/table operations and \(O(n)\) logical
table bits**, plus index management. The supplied Python implementation
uses ordinary indexed byte arrays; this count does not make its
arbitrary-precision index operations free. Charging \(O(\log(n+1))\) per
index operation gives the conservative polynomial bound
\(O(n^2\log^2(n+1))\) for its bit arithmetic in an indexed-memory model.
Nothing here asserts sublinear work in a Turing-machine P3 model.

This is not an improvement over the usual quadratic Boolean work for local
evolution through time \(n\). It shows why the exponential degree of the
**integer** lift cannot by itself establish exponential work for a center
query. The prior audit's sharper zeta/prefix-sum identity already identifies
the transformed recurrence with the original rotated evolution; we do not
rerun its checks.

The claimed cost of a supplied masked-block evaluator remains separate from
constructing those blocks. This cutoff proves neither a uniformly small
block representation nor a fast jump between support rows.

## 4. Lucas submasks cannot replace the cutoff

The final query uses only indices \(r\preceq n\), but that smaller set is
not safe during construction: increment can carry a discarded index into a
retained one. At the single directed query \(n=4\),

\[
S_1,\ldots,S_5=\{0\},\{1\},\{1\},\{2\},\{2,3,4\}.
\]

The cutoff \(r\le4\) preserves these rows and gives \(c(4)=1\). Filtering
each row instead to submasks of \(4\), namely \(\{0,4\}\), erases \(S_2\)
and every later row, incorrectly giving zero. This rejects that intermediate
filter only; it does not prohibit more elaborate query-specific summaries.

## 5. Exact verifier and limits

[Verifier](../../experiments/rule30/p3_fibonacci_interpolation_audit.py)
and [artifact](../../experiments/rule30/p3-fibonacci-interpolation-audit.json)
are independent of the earlier implementation. They check the complete
eight-entry Rule 30 truth table, bounded exact polynomial instances of the
degree induction, integer Lagrange weights and reconstruction, and linear/
bilinear basis identities for zeta and cutoff. The only physical trajectory
is a fresh four-step truth-table calculation validating the carry witness.
The cutoff algorithm is called only at that same \(n=4\).

```sh
uv run --offline --no-project python experiments/rule30/p3_fibonacci_interpolation_audit.py
```

The all-length statements follow from the proofs above; the finite controls
check their implementation and indexing. No previous support census,
large prefix, or old verifier is rerun. Source hashes include this report,
the new source, and the preserved prior audit. The artifact also records the
SHA-256 of the primary notebook bytes read on the stated retrieval date;
verification itself does not download or execute that notebook.

# Exact defect-frequency bounds and the remaining parity obstruction

Date: 2026-09-10. **Exact certificates; no solution of P1, P2, or P3.**

The proposed invariant frequency LP has a sharp answer: the maximum `11`
density is **2/5**, and the maximum one-density is **3/5**, for every block
size k>=3. These bounds already follow from triple consistency and
one-bit time stationarity. They do not converge to 1/4 and 1/2 as k grows.
A periodic Rule 30 orbit attains both bounds at every refinement.

The same algebra, with the time change retained, also yields a deterministic
bound for the actual lone seed:

\[
\sum_{t=0}^{T-1} D_t\le \frac{2T^2+4T-6}{5},\qquad T\ge1,
\]

where D_t counts adjacent `11` pairs in the entire finite-support row.
This controls total defects in spacetime, not the parity of their
intersections with a Green-function mask.

## 1. Exact preimages and the scope of frequency constraints

For f(p,q,r)=p XOR (q OR r), direct enumeration gives

```
f^-1(11)  = {0010, 0011, 0100, 1001}
f^-1(111) = {00100, 01001, 10010, 10011}.
```

For any shift-invariant measure P_t, the exact evolution equations are

\[
P_{t+1}(11)=P_t(0010)+P_t(0011)+P_t(0100)+P_t(1001),
\]
\[
P_{t+1}(111)=P_t(00100)+P_t(01001)+P_t(10010)+P_t(10011).
\]

Consequently, the proposed compressed expression
`P_t(00100)+P_t(01001)+P_t(1001)` for the second equation is valid:
the last two five-block probabilities sum to P_t(1001). It still requires
five-block data; it is not a closed constraint on sixteen four-block
variables.

Spatial consistency alone does not give a fractional upper bound on the
next row's `11` density. On the periodic lattice,

```
(001)^Z -> (111)^Z -> (000)^Z.
```

Thus the one-step maximum is 1. Imposing P_{t+1}=P_t is a substantive
additional restriction. It is justified for invariant measures, not for
each row of the lone-seed orbit. Moreover, full-lattice spatial frequencies
of every nonzero block in a finite-support row are zero. Frequencies
normalized to the expanding occupied window instead have boundary terms.

## 2. A solver-free certificate for the stationary LP

Write the stationary triple probabilities, in lexicographic order, as

```
(a,b,c,d,e,f,g,h) = (P000,P001,P010,P011,P100,P101,P110,P111).
```

Spatial consistency gives

```
e=b,    g=d,    c=b+f-d.
```

The current one-density is b+f+d+h. The next one-density, obtained by
summing the four output-one preimages, is

```
b+c+d+e = 3b+f.
```

One-bit time stationarity therefore gives d+h=2b. Normalization becomes
1=a+5b+2f, while P(11)=2b and P(1)=3b+f. In particular,

\[
\boxed{5P(11)+2P(000)+4P(101)=2},
\]
\[
\boxed{5P(1)+3P(000)+P(101)=3}.
\]

Nonnegativity proves P(11)<=2/5 and P(1)<=3/5. This is an exact algebraic
certificate, independent of the floating-point LP solver.

Both bounds are attained by the uniform measure on the five shifts of
the periodic configuration (00111)^Z. Its Rule 30 evolution is

```
00111 -> 11100 -> 10011 -> 01110 -> 11001 -> 00111.
```

These five rows are precisely the five spatial shifts. Their uniform
measure is invariant under both spatial translation and Rule 30, has
P(11)=2/5 and P(1)=3/5, and supplies consistent cylinder probabilities
of every length. No enlargement of this stationary block LP can exclude
it. The all-zero invariant measure attains the lower bound P(11)=0.

This does not refute lone-seed density 1/2. It refutes the proposed claim
that spatial consistency and time invariance force the LP maximum toward
the fair-Bernoulli value 1/4. Seed-specific restrictions would be additional
information.

## 3. Retaining the time change gives a seed-specific count bound

Without time stationarity, set
delta_t=P_{t+1}(1)-P_t(1). The same calculation gives

\[
5P_t(11)+2P_t(000)+4P_t(101)=2-3\delta_t,
\]
\[
5P_t(1)+3P_t(000)+P_t(101)=3-2\delta_t.
\]

For a finite-support binary row define:

- n: number of ones; n': number after one Rule 30 update;
- r: number of runs of ones;
- D: number of `11` pairs;
- H: number of `101` blocks;
- U: number of length-three windows containing at least one one.

All windows are counted on the zero-padded infinite lattice. Counting runs
and the isolated zero gaps between them gives

```
D=n-r,    U=n+2r-H,    n'=3r-2H.
```

For the last identity, the OR part has n+r ones, and its intersection
with the left-parent one set has n-r+H ones. The XOR output therefore
has n+(n+r)-2(n-r+H)=3r-2H ones.

Eliminating r proves the exact finite integer identity

\[
\boxed{5D+4H=2U-3(n'-n)}.
\]

For the lone seed, all ones at time t lie in [-t,t], so U_t<=2t+3.
Summing the identity through time T-1 telescopes the time difference:

\[
5\sum_{t<T}D_t+4\sum_{t<T}H_t
=2\sum_{t<T}U_t-3(n_T-1)
\le2T^2+4T-3(n_T-1).
\]

For T>=1 the three distinct positions -T, -T+1, and T are one, hence
n_T>=3. Dropping the nonnegative H term proves

\[
\boxed{\sum_{t<T}D_t\le(2T^2+4T-6)/5}.
\]

The first T lightcone rows have total area T^2. Thus this is an upper
bound 2/5+O(1/T) on their total defect count divided by lightcone area.
It is neither a per-row bound nor a center-column frequency theorem.

## 4. The geometric projection uses a trinomial kernel

Use the conventions and exact residual decomposition from
[the edge-response report](RESULTS-duhamel-left-edge-thue-morse.md).
Put A(z)=z^-1+1+z. The correct Rule 150 kernel is

\[
G(n,j)=[z^j]A(z)^n\quad\text{over GF(2)}.
\]

It is not the proposed binomial coefficient binom(n,-j) modulo two.
Already G(1,j) is nonzero at all three positions -1,0,1. Also

```
A(z)^3 = z^-3 + z^-2 + 1 + z^2 + z^3   over GF(2),
```

so ordinary Pascal-triangle support counts cannot be imported without
accounting for cancellations. A source location contributes to the center
at time t precisely when G(t-1-s,-j)=1.

For the residual R_t, the mandatory left-edge source must first be
removed. Define Q^0=0 and Q^s=N^s XOR e_-s for s>=1, where
N_j^s=x_j^s*x_(j+1)^s. Let

\[
V^t=\bigoplus_{s<t}L^{t-1-s}Q^s,\qquad R_t=V^t_0.
\]

For h=2^k, Frobenius gives three translates,
L^h=S^-h+I+S^h. Therefore the correct recursion is

\[
R_{t+h}=R_t\oplus V^t_{-h}\oplus V^t_h
\oplus\bigoplus_{s=t}^{t+h-1}(L^{t+h-1-s}Q^s)_0.
\]

The last term contains fresh defects. Even the old part involves three
translates combined by XOR, not a union with a single shifted copy. This
identity supplies no cancellation estimate without further control of
those terms.

## 5. Sparse sources can still produce linear parity discrepancy

A density bound does not say which mask sites are occupied. Nor does
the absence of exact dyadic self-similarity imply cancellation of signs.
The following forced-source example isolates that gap; its sources are
**not claimed to be realizable nonlinear Rule 30 defects**.

For any prescribed bits r_t with r_1=0, take

\[
Q_j^s=\mathbf1_{j=0}(r_{s+1}\oplus r_s),\qquad s\ge1,
\quad Q^0=0.
\]

Each row has at most one source, inside the seed lightcone. Since
G(n,0)=1 for all n, their projected residual telescopes to r_t.
Choose

\[
r_t=\theta(t)\oplus\mathbf1_{\{t\text{ is a square}\}}.
\]

Then r_1=0, r_2=1 and r_4=0, so even the simplest doubling symmetry
fails. Yet the proposed center signs have discrepancy

\[
\sum_{t=1}^T(-1)^{\theta(t)+r_t}
=T-2\lfloor\sqrt T\rfloor.
\]

This shows that sparse forcing plus the exact Rule 150 mask can coexist
with linear discrepancy. To rule it out for Rule 30, one must use the
specific nonlinear feedback Q^s=N(x^s) XOR e_-s. The total-count bound
in Section 3 does not encode that feedback's parity consequences.

The outstanding P2 target remains a bound o(T) on the signed sum for
the actual lone seed. Neither stationary block extrema nor a spacetime
defect-count estimate provides such a bound by itself.

The [weighted-mask follow-up](RESULTS-defect-mask-flux.md) derives the exact
spatial current, proves its mask-variation cost, and shows explicitly why
reducing this certificate modulo two recovers only the original update rule.

## 6. Reproducibility

Run from the repository root:

```
uv run python experiments/rule30/defect_frequency_polytope.py
```

The verifier enumerates both preimage sets, checks the periodic witness,
and solves the stationary LPs for k=3,...,10. It also checks the witness
against each constraint matrix using exact integer cylinder counts.
The finite-row identity passes all 32,766 binary rows of widths 1–14.
The telescoped identity and seed bound pass every prefix through T=1024;
the cumulative defect count there is 261,648.

These computations cross-check the displayed algebraic proofs. The LP
output is numerical evidence for the implementation; the identities and
the periodic witness establish sharpness for every k>=3 without a solver.

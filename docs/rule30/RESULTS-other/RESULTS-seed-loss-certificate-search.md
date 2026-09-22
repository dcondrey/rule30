# Actual-seed search for a spatial loss certificate

This continuation tests the missing accumulated-loss estimate on the lone
seed, rather than assuming a stochastic model for its rows. It produces
an exact counterexample to one proposed uniform loss constant and a
reproducible finite census. It does not prove a uniform seed loss bound,
the quarter-wave estimate P_t=o(t), or P1, P2, or P3.

## 1. The exact quantity being tested

For the positive row x_1^t,...,x_t^t, extended by zero, set

\[
B_{L,j}=\sum_{r=0}^{L-1}i^r x_{j+r}^t,\quad
E_{t,L}=\sum_{j\ge1}|B_{L,j}|^2,\quad
V_{t,L}=\frac{E_{t,L}}{tL^2}.
\]

The boundary energy Q and contrast D are

\[
Q_{t,L}=\sum_{j=1}^{L}|B_{L,j}|^2,\qquad
D_{t,L}=\sum_{j\ge1}|B_{L,j}-i^L B_{L,j+L}|^2.
\]

The [exact finite-row recursion](RESULTS-finite-gap-mps-and-variance.md) is

\[
E_{t,2L}=4E_{t,L}-2Q_{t,L}-D_{t,L},\qquad
\delta_{t,L}=\frac{2Q_{t,L}+D_{t,L}}{4E_{t,L}},\qquad
V_{t,2L}=(1-\delta_{t,L})V_{t,L}.
\]

Every nonzero finite positive row has 0<delta<1. The missing property is
sufficient loss across growing scales before L becomes comparable to t.

## 2. An exact seed counterexample to a uniform quarter loss

At t=20 the seed's positive row is

```text
01111011101100010001
```

At L=4, direct integer sums give

\[
(E_{20,4},E_{20,8},Q_{20,4},D_{20,4})=(21,67,3,11).
\]

In particular,

\[
\boxed{\delta_{20,4}=17/84<1/4.}
\]

This disproves the proposed inequality delta>=1/4 for every seed row and
every dyadic scale 4<=L<=sqrt(t). It does not disprove an eventual version,
a smaller constant, or an accumulated-loss inequality allowing exceptions.

## 3. The finite census

Every integer time 16<=t<=8192 and every dyadic scale
4<=L<=floor(sqrt(t)) was checked: 35,509 row/scale cases. The exact minima
over these finite ranges are:

| L | Time attaining the recorded minimum | Minimum delta |
|---|---:|---:|
| 4 | 20 | 17/84 |
| 8 | 77 | 87/241 |
| 16 | 390 | 750/1951 |
| 32 | 1155 | 17469/46664 |
| 64 | 5259 | 33619/84280 |

The time-20 case was the only strict violation of delta>=1/4 in this
census. All cases satisfy delta>=1/8. Neither observation supplies a
bound outside the enumerated range. No random-walk model, fitted
confidence interval, or asymptotic extrapolation is used.

The [verifier](../../experiments/rule30/quarter_wave_seed_loss_scan.py)
generates the seed by exact packed-bit evolution, calculates all energies
as integers, compares losses as rational numbers, and independently checks
the time-20 witness by scalar window sums. The complete summary is in the
[JSON record](../../experiments/rule30/quarter-wave-seed-loss-scan.json).

```bash
uv run python experiments/rule30/quarter_wave_seed_loss_scan.py \
  --output experiments/rule30/quarter-wave-seed-loss-scan.json
```

## 4. What a uniform certificate would actually buy

Here is a sufficient theorem template, not an established seed property.
Suppose some eta>0 and t_0 satisfy, for every seed time t>=t_0 and every
dyadic 4<=L<=sqrt(t),

\[
2Q_{t,L}+D_{t,L}\ge4\eta E_{t,L}.
\]

Choose J=floor(log_2(sqrt(t))) and L_*=2^J. Iterating from L=4 to L_*
uses J-2 inequalities and gives

\[
V_{t,L_*}\le (1-\eta)^{J-2}V_{t,4}
\le C_\eta t^{\frac12\log_2(1-\eta)}.
\]

The existing deterministic window estimate then yields

\[
|P_t|\le
C'_\eta t^{1+\frac14\log_2(1-\eta)}+\sqrt t.
\]

For example, a proof with eta=1/8 would give exponent
1+(1/4)log_2(7/8), approximately 0.95184, on the first term. The finite
census does not prove this hypothesis. Accumulated loss on a sufficiently
large subset of scales would also suffice; imposing the same constant at
every scale is stronger than necessary.

## 5. What the accompanying exact analysis changes

The [atom-propagation report](RESULTS-quarter-wave-atom-propagation.md)
proves a separate all-length obstruction: for any fixed block width k,
there is a periodic input with zero quarter-frequency spectral projection
for every k-cell observable, but with a nonzero coordinate projection
after sufficiently many Rule 30 steps. The proof uses a surviving ordinary
multilinear coefficient and an exact phase-indexed circulation. Thus a
generic finite list of vanishing local projections cannot be propagated
indefinitely. This statement does not rule out additional seed-specific
constraints or representations.

The [coherence analysis](RESULTS-quarter-wave-coherence-barrier.md) supplies
a universal finite-support floor for delta and a quantitative consequence
of small contrast. Its geometric floor is too small to close the seed
estimate on sublinear scales. Thus positivity of loss is not the missing
certificate; a quantitatively stronger consequence of the seed's history
is required.

The [sparse-origin search](RESULTS-quarter-wave-sparse-coherence.md) gives
one exact example of using the initial zeros: a closed periodic prefix
excludes maximal positive imbalance for every origin with at most two
ones at times n=1 modulo 4 beyond n=9. The conclusion concerns exact
maximality; extending it to a fixed fractional imbalance is an unresolved
step, so it supplies no sublinear seed estimate.

The spatial estimate remains an intermediate target. Even proving it
would leave the accumulated-current term in

\[
A(T)-T/2=P_T+\sum_{t<T}(K_t-1/2)
\]

uncontrolled. There is no claim here of a solution to the center-column
density or nonperiodicity problems.

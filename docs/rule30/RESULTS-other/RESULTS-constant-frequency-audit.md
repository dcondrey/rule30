# Constant-frequency models and the Rule 30 center column

Date: 2026-09-15. **An elementary exclusion of a specified model class;
no prize problem solved.** The calculation below rejects a single
thresholded oscillator at every frequency. It does not reject arbitrary
formulas involving mathematical constants, a complicated observation of
a rotation, or an oscillator model beginning after an unknown transient.

## 1. A precise version of the frequency proposal

Let `c_t=(F^t(delta_0))_0`, including `c_0=1`. Consider

\[
c_t=\mathbf 1\{\cos(2\pi\alpha t+\beta)\ge q\}
\quad(t\ge0),
\]

where alpha, beta and q are arbitrary real constants. A sine, an amplitude
and an offset give the same model class after adjusting the parameters
(with constant-output cases treated separately).

**This formula cannot generate the Rule 30 center column, for any choice
of its constants.** No frequency fitting or numerical approximation to
alpha is needed for the exclusion.

### Proof by finite block counts

More generally let `c_t=g(theta+t alpha mod 1)`, where g is binary and
constant on the arcs obtained by removing at most two boundary points
from the circle. Permit arbitrary values at those boundary points.

For a length-m block, the m translates of the boundary set have at most
2m distinct points. Between those points, every coordinate of the block
is constant. With k>0 distinct points there are k open arcs and k singleton
boundary cells, so at most 2k<=4m different blocks are possible. If there
are no boundary points, there is just one block. Rational rotation rates,
coincident boundaries, and threshold equality do not increase this bound.

The actual first 29 Rule 30 center bits are

```text
11011100110001011001001110101
```

They contain 21 distinct length-five blocks. Since 21>4*5, this finite
prefix contradicts the proposed formula at every alpha, beta and q.

For the conventional half-open interval coding, the stronger bound is
2m: with the consistent `[a,b)` convention, every boundary has the same
block value as the arc immediately on its right, even when boundaries
coincide. The first 15 Rule 30 bits already contain all eight triples,
exceeding 2*3. The 29-bit certificate avoids needing that endpoint
convention. All 32 length-five blocks occur by prefix length 120.

This is a finite witness excluding an entire specified family of infinite
formulas. It is not a finite-prefix proof of center nonperiodicity.

### Reproduction

The standard-library verifier
[constant_frequency_audit.py](../../experiments/rule30/constant_frequency_audit.py)
compares independent scalar truth-table and packed-bit Rule 30 generators
through 1,024 bits. Its
[artifact](../../experiments/rule30/constant-frequency-audit.json)
records the block witnesses and prefix thresholds.

```sh
uv run --no-project python experiments/rule30/constant_frequency_audit.py
```

## 2. Physical units and constants that encode a sequence

Rule 30 specifies cells and discrete updates, with no physical duration or
distance assigned to either. A frequency in hertz requires an additional
choice of seconds per update. Dimensionful physical constants therefore
do not determine a frequency for the bare automaton without a model
connecting those units. A dimensionless physical constant could occur in
a proposed identity, but the identity would still require a derivation.

Every binary sequence can also be encoded as a real constant:

\[
R_{30}=\sum_{t\ge0}c_t2^{-(t+1)}.
\]

P1 is equivalent to irrationality of this particular number. P2 concerns
the limiting proportion of its binary digits equal to one. Defining this
constant provides neither property. Likewise, identifying digits of some
independently defined constant with c_t would require proof of the
identification and a separate account of the relevant digit properties
and computation costs.

## 3. The exact frequency already supplied by the local rule

The [quarter-wave current report](RESULTS-quarter-wave-current-target.md)
provides a more substantive frequency connection. For finite rows define

\[
P(x)=\sum_{m\ge0}(x_{4m+1}-x_{4m+3}),
\qquad q_i(x)=2x_i(x_{i+1}\lor x_{i+2})+x_{i+1}x_{i+2},
\]
\[
K(x)=\sum_{m\ge0}(q_{4m}(x)-q_{4m+2}(x)).
\]

Then the exact integer identity is

\[
x_0=P(Fx)-P(x)+K(x).
\]

The weights are `sin(pi*i/2)` on the positive half-line: a spatial
wavelength of four cells. They cancel the neighboring terms of the
linear part of Rule 30 while keeping the nonlinear correction K.
This is a spatial projection, not a temporal oscillator formula for c_t.

On the singleton orbit, telescoping gives

\[
\sum_{t<T}(c_t-\tfrac12)
=P(x^T)+\sum_{t<T}(K(x^t)-\tfrac12).
\]

Separate sublinear bounds on both terms would prove P2. Neither estimate
is established; the two terms can also cancel each other, so requiring
separate bounds is stronger than the exact identity requires.

The [spectral criterion](RESULTS-quarter-wave-skew-product.md) makes one
partial target precise: absence of coordinate spectral atoms at spatial
frequencies plus/minus 1/4 in every specified singleton accumulation
measure suffices for `P(x^t)=o(t)`. It leaves the accumulated-current
estimate open. Full mixing or a flat spectrum is unnecessary for this
partial target.

## 4. What the audit changes

The useful question is whether singleton ancestry forces cancellation
in this exact spatial projection or its nonlinear current. Searching
named constants for a numerical fit does not supply that estimate.
The [origin audit](RESULTS-p2-seed-geometry-audit.md) shows why retaining
the actual singleton origin matters: other finite rows can share both
moving edge tapes, a prescribed central history, and the current right
half while producing an arbitrary specified future center block.

The older [frequency-domain note](ARM4-frequency-domain.md) reports
Berlekamp--Massey complexity over GF(2). Those finite values constrain
short linear recurrences over that field. They do not by themselves
exclude general real-frequency models or nonlinear digit formulas.
The block-count proof above supplies its own model-specific exclusion.

All three prize problems remain open in this audit.

The [fundamental-frequency follow-up](RESULTS-fundamental-frequency-search.md)
classifies the bounded one-sided linear extraction weights: the quarter-wave
choice is the only one with a unit-modulus temporal multiplier, and that
multiplier is 1 (zero temporal frequency). A fixed-candidate search over
1,048,576 cached center bits, with disjoint-block peak checks, identifies
no convincing persistent temporal frequency. This is finite evidence,
not an absence-of-lines theorem.

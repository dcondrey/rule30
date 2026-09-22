# Actual-orbit decoder causality: an exact return-period criterion

Date: 2026-09-13. **There is an exact all-length criterion for whether a
two-input-digits-to-one-output-digit decoder is even well-defined on the
actual even-time seed orbit.** The criterion is not proved to hold at
every depth. A bounded exact test finds no collision through six output
digits. No finite-state decoder or P3 speedup is established.

A continuous decoder with unrestricted input delay does exist by the
nested orbit periods. The open point here is the specified rate of one
output digit per two input digits, followed by the separate algorithmic
and reconstruction requirements.

The [verifier](../../experiments/rule30/p3_actual_orbit_decoder_causality.py)
and [artifact](../../experiments/rule30/p3-actual-orbit-decoder-causality.json)
use one12-digit residue orbit for256 steps, charging3072 local digit
transitions. These are exact finite-prefix return computations, not a
regenerated center prefix or a fitted transducer.

## 1. The restricted question

Let K be the [itinerary automaton](RESULTS-p3-itinerary-conjugacy.md),
with fixed initial state C, and let0 denote its infinite zero input.
Seek a causal decoder D satisfying only

```
D(K^(2L)(0)) = K^L(0)  for every L>=0.             (1)
```

After2k input digits, the decoder must have determined its first k
output digits. Internal memory may be unbounded. This restriction to
actual seed points is essential: the
[all-input two-to-one intertwiner](RESULTS-p3-digit-pair-renormalization.md#4-no-total-intertwining-decoder-with-or-without-causality)
is already refuted by fixed points of the first-pair permutation.

Let P_m be the primitive period of0 under K modulo4^m. K is a prefix
permutation, so the finite orbit is a cycle from its first point. Thus

```
K^a(0) = K^b(0) mod4^m  iff  a=b mod P_m.         (2)
```

Moreover P_m divides P_(m+1). Each P_m is a power of two. To see the
latter without a group-theory assumption, use compatibility with binary
prefixes, inherited from the isometric ABC conjugacy. Once a binary
prefix returns, its next bit is either fixed by that return or toggled;
the lifted orbit period is therefore the same or twice as large.
Starting at the empty prefix gives a power of two at every precision.
In particular P_1=2 and all P_m are even.

## 2. Necessary and sufficient prefix consistency

Fix k. Two even-time input points have equal2k-digit prefixes exactly
when their indices L differ by a multiple of

```
S_k = P_(2k)/gcd(P_(2k),2) = P_(2k)/2.           (3)
```

Their prescribed k-digit outputs agree exactly when their indices
differ by a multiple of P_k. Therefore the prescribed prefix function
is well-defined if and only if

```
P_k divides S_k.                                  (4)
```

Since these are powers of two and P_k divides P_(2k), (4) is equivalent
to the particularly simple strict inequality

```
P_(2k) > P_k.                                    (5)
```

If (5) fails, use the two actual indices L=0 and L=P_(2k)/2. The fine
input prefixes both equal zero modulo4^(2k), but the target prefix at
the latter index is nonzero modulo4^k. This is a concrete collision of
actual inputs and excludes every decoder with the stated timing,
regardless of the number of its internal states.

There is an unconditional qualitative conclusion. The periods P_m are
unbounded: if all divided some fixed power P, the congruences
K^P(0)=0 modulo every4^m would imply K^P(0)=0 in Z_2. Conjugacy would
then give C^P(0)=0, contrary to its positive width. Therefore, for each k,
the finite precision

```
M(k) = min {m: P_m >= 2*P_k}                      (4a)
```

exists. An actual input prefix of length M(k) uniquely determines its
prescribed k-digit output by the same divisibility argument. Compatible
extension defines a continuous decoder on the actual even-orbit closure
with this possibly large delay. Thus generic continuity is already
available; the specific quantitative question in (5) is M(k)<=2k.

If (5) holds for every k, the resulting finite-prefix functions are
compatible: whenever a longer input prefix is realized by a seed point,
its prescribed output reduces to the already determined shorter output.
They therefore define a continuous causal map with the specified
two-input-digits/one-output-digit timing on the closure of the actual
even-time orbit. They can also be extended to a total
causal map by assigning arbitrary consistent outputs on input prefixes
outside that closure. This extension need not satisfy an all-input
intertwining identity.

Thus (5) at all depths is both necessary and sufficient for existence
of a causal map with possibly unbounded memory satisfying (1). It says
nothing about a finite-state realization or efficient construction of
the prefix functions. Looking up an input's index in a whole period is
not a free operation.

There is also an essential direction issue. D maps already available
doubled-time fine data to half-time coarse data. That operation alone
does not reconstruct an arbitrary requested fine digit from a shorter
coarse computation. Even an efficiently realized D would need an exact
inverse or suitable query reconstruction rule, with its additional
information and cost charged, before yielding an index-halving algorithm.

## 3. An equivalent inequality for power-of-two returns

Define

```
alpha_s = v_4(K^(2^s)(0)),  s>=0,                 (6)
```

where v_4 counts the number of leading zero base-four digits. These
valuations are finite: Phi is injective and C^L(0) has positive width
for every L>0. In particular alpha_0=0. Equation (2) gives

```
alpha_s = max {m>=0: P_m divides2^s},             (7)
```

with P_0=1. Consequently, (5) for all k is equivalent to

```
alpha_s <= 2*alpha_(s-1)+1  for every s>=1.        (8)
```

Indeed a plateau P_k=P_(2k)=2^s is precisely the existence of an integer
k with alpha_(s-1)<k and2k<=alpha_s. Such a k exists if and only if
alpha_s>=2*alpha_(s-1)+2. If this inequality occurs, k=alpha_(s-1)+1
and L=0,2^(s-1) supply the collision just described.

Equation (8) is an exact new formulation of the causal-decoder question;
it is not established here as a universal inequality. Even a proof of
it would establish only the existence of the causal map described above,
leaving its state complexity, evaluation cost, and useful query readout
to be proved separately.

## 4. Bounded exact observation

The saved residue orbit gives these complete first-return periods:

| m | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P_m | 2 | 8 | 16 | 32 | 64 | 64 | 64 | 256 | 256 | 256 | 256 |

At depth12 no return occurs by256, so the power-of-two property gives
P_12>=512. Thus (5) holds for k=1,...,6, including k=6 where only this
lower bound is needed. The same bounded orbit gives

```
s       = 0,1,2,3,4,5,6,7,8,
alpha_s = 0,1,1,2,3,4,7,7,11.
```

These observations satisfy (8) at the checked exponents. Neither the
next valuation nor the all-length inequality is inferred from them.

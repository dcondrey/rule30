# Two conditional affine scans and a local Gray basis

Date: 2026-09-14. **The itinerary map B can be evaluated by two consecutive
prefix scans, each affine in the field it updates when the other field is
fixed. A pointwise Gray-code basis gives an equivalent two-field update and
a local readout of every requested bit.**

This is a direct consequence of the already saved
[bitplane equations](RESULTS-p3-bitplane-temporal-squaring.md), made explicit
here. It corrects an overly strong interpretation of the nonaffine half in
the [staggered factorization](RESULTS-p3-staggered-affine-field.md): that
nonaffinity concerns its particular choice of the fixed old field. It does
not require one intrinsically nonaffine half in every coordinate system.
The two halves below remain jointly nonlinear, and their control fields
change along the actual orbit. No faster temporal powering or P3 algorithm
is proved.

The [verifier](../../experiments/rule30/p3_two_affine_scans.py) and
[artifact](../../experiments/rule30/p3-two-affine-scans.json) check the local
identities, both boundaries, inverse formulas, and bounded exact comparisons
with the original itinerary transducer. No orbit or capacity census is
needed for the all-length statements.

## 1. Direct bitplanes: compute the high field, then the low field

All additions and multiplications in the formulas below are over F2.
Write an input digit of Y as D_i+2H_i and its output under B as P_i+2Q_i.
The original output-driven equations are

```
P_i = D_i + (P_(i-1) OR Q_(i-1)),
Q_i = H_i + (Q_(i-1) OR D_i),
(P_-1,Q_-1)=(1,0).                              (1)
```

The second equation does not use P. Thus first compute the entire high
field using

```
Q_i = H_i + D_i + (1+D_i) Q_(i-1), Q_-1=0.       (2)
```

With Q fixed, compute the low field using

```
P_i = D_i + Q_(i-1) + (1+Q_(i-1)) P_(i-1),
P_-1=1.                                         (3)
```

Equations (2) and (3) are simply the expansion x OR y=x+y+xy in (1).
They preserve the fixed B boundary. The second scan uses exactly the high
field produced by the first scan.

For fixed D, the map H->Q in (2) is affine on every finite prefix and on
the whole one-sided field. For fixed Q, the map D->P in (3) is likewise
affine. Each is bijective on prefixes: its current input enters with
coefficient1, and all other dependence is on previous outputs. Their local
inverse equations are

```
H_i = Q_i + D_i + (1+D_i) Q_(i-1),
D_i = P_i + Q_(i-1) + (1+Q_(i-1)) P_(i-1).       (4)
```

To invert the complete update, recover D from the supplied P,Q by the
second equation, then recover H by the first. Only adjacent supplied
output digits are used. These are all-input identities; no seed ancestry
or assumption about reset locations is required.

Each forward scan has a Boolean carry acted on by one of four affine maps:
identity, flip, reset to0, or reset to1. This allows exact aggregation of
**supplied** control blocks. It does not construct those blocks across
successive B times.

## 2. A local Gray-code representation

Define two binary fields

```
U_i=D_i, Z_i=H_i+D_i.                            (5)
```

This is a pointwise linear bijection, with D=U and H=Z+U. It neither
requires an inverse prefix scan nor adds an auxiliary history. Write the
output fields as U'=P and Z'=Q+P.

There is an exact factorization in the opposite order. First update U,
holding the old Z fixed:

```
U'_i = U_i + Z_(i-1) + (1+Z_(i-1)) U'_(i-1),
Z_-1=0, U'_-1=1.                                (6)
```

Then update Z, holding the newly produced U' fixed:

```
Z'_i = Z_i + U'_i(1+U'_(i-1)) + U'_i Z'_(i-1).
                                                     (7)
```

At the origin equation (7) uses the auxiliary values
U'_-1=Z'_-1=0, giving Z'_0=Z_0+U'_0. Equivalently one may use both
auxiliary values1, since they enter only through their sum. This is a
separate boundary convention for the second scan; it does not alter any
produced U'_i at i>=0. In particular it must not be mixed with
U'_-1=1,Z'_-1=0 in (7).

Here is a direct proof, retaining the output boundary of (1). Rewriting its
high equation gives

```
Q_i = Z_i + U'_i Q_(i-1).                        (8)
```

Indeed if Q_(i-1)=0, both sides reduce to H_i+D_i. If Q_(i-1)=1,
(1) forces U'_i=1+D_i, and substitution again gives equality. Hence

```
U'_i OR Q_i = U'_i OR Z_i,
```

because the additional term in (8) is masked whenever U'_i=1. Substituting
this identity at the preceding digit in the low equation proves (6).
Finally Z'_i=Q_i+U'_i and Q_(i-1)=Z'_(i-1)+U'_(i-1) prove (7) for
i>=1. At i=0, Q_-1=0 gives its stated origin equation directly.

Both halves are again affine in the field being updated. Their inverses
are local once the controlling field and output are supplied:

```
U_i = U'_i + Z_(i-1) + (1+Z_(i-1)) U'_(i-1),
Z_i = Z'_i + U'_i(1+U'_(i-1)) + U'_i Z'_(i-1).   (9)
```

To invert the full update, use the second formula to recover Z, then the
first to recover U. Use the same separate origin conventions as in the
forward scans.

## 3. Exact actual initial condition and marked readout

The actual zero ray has U=Z=0. Equations (6)-(7) send it to U'=Z'=1,
which decodes to the exact whole ray B(0)=1^infinity. Applying the fixed
two-scan map N times therefore gives precisely the fields of B^N(0),
with no fresh completion or freely chosen time boundary.

Every digit bit has a local readout:

```
low(digit_i B^N(0))  = U_i^(N),
high(digit_i B^N(0)) = Z_i^(N)+U_i^(N).           (10)
```

In the established [actual-B center formula](RESULTS-p3-actual-b-query.md),
for h>=1 and e in{0,1}, set N=h+1+e. Then

```
c_(2h+e) = U_(h-1)^(N) + e Z_(h-1)^(N).         (11)
```

The cases c_0=c_1=1 remain separate. Both center parities are represented
by the same zero initial fields and the same fixed update; the high-bit
readout in (11) adds no prefix reconstruction or future-time query.

## 4. What has and has not been simplified

For a supplied prefix of m digits, either representation evaluates one B
step using two O(m) Boolean-operation scans and constant carry memory in
addition to its O(m) input/output storage. The Gray transformation and
readout cost constant work per digit. Materializing the actual fields
through N times still costs O(Nm) Boolean work; for (11), m=h and N is of
order h, so this gives the usual quadratic work in the center time.
Index handling and representation costs are additional implementation
costs, not free operations on arbitrarily large indices.

Conditional affinity does not make the entire map affine. The coefficients
of the second scan use the field constructed by the first, and the next
time step uses both newly constructed fields. For example the root Gray
rule is U'_0=U_0+1, Z'_0=Z_0+U_0+1, but higher digits already use products
between fields in (6)-(7). More decisively, the two-fine-digit inputs
0,1,2,3 have B outputs5,14,15,0, whose XOR is4; this violates an affine
rectangle identity and remains a violation under the linear Gray change.

Products of the affine scan operators can be written with their complete
ordered control history. A binary product tree reduces their dependency
depth. It does not by itself reduce the work required to produce the
control fields, align their spatial blocks, or evaluate both child
products. No factor-refactorization identity eliminating this actual
history dependence is proved here. Freezing a control field and powering
its operator would address a different supplied-context problem.

The result supplies an exact simpler representation and local observable,
and corrects a coordinate-specific obstruction. It provides neither an
all-scale dyadic closure nor an improved P3 complexity bound.

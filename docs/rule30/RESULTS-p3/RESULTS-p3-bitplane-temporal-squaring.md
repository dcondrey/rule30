# Exact B squaring and a persistent decimation correction

2026-09-14. This concerns the itinerary map B used in the exact singleton
query formula in [the actual-B report](RESULTS-p3-actual-b-query.md).
The two-step map admits one spatial scan with a two-digit output memory.
The next square does not reduce to the same kernel on alternate digits,
even away from the origin on the actual orbit of zero. Both statements
are exact. They do not rule out a more structured nonlocal correction or
provide an asymptotic query algorithm.

## 1. Boundary and notation

Digits are written low first. For Y=B(X), write an input digit as
a_j+2b_j and its output as p_j+2q_j. The output-driven B automaton gives

```
p_j = a_j XOR (p_(j-1) OR q_(j-1)),
q_j = b_j XOR (q_(j-1) OR a_j),
(p_-1,q_-1)=(1,0).
```

The virtual origin is part of the map. It must not be replaced by the
boundary of A or C. Put L=B^-1. Its local inverse is

```
a_j = p_j XOR (p_(j-1) OR q_(j-1)),
b_j = q_j XOR (q_(j-1) OR a_j).
```

Let i(e,d) denote this inverse digit function given the previous output e:
i(0,d)=-d mod4; i(1,d)=d-1 mod4; i(2,d)=i(3,d)=3-d.

## 2. An exact two-step kernel and forward scan

Put R=L^2. At a position j>=1, denote the current input to R by (p,q),
the preceding digit by (u,v), and the two-back digit by (r,s). At j=1,
the two-back digit is the prescribed virtual pair (1,0). Define

```
F = (s AND u) XOR ((1 XOR v) AND (r OR s)),
T = s OR (u XOR r).
```

Then the output pair of R is exactly

```
a = p XOR F,
b = q XOR (T AND (a XOR v)).                         (1)
```

At j=0 its rule is instead (a_0,b_0)=(p_0,q_0 XOR1), because the
root permutation of B is addition by1 modulo4. This origin rule is
not obtained by extending the bulk with an invented second virtual digit.

To prove (1), compose the two local inverses. The resulting digit is

```
R(r,u,p) = i(i(r,u), i(u,p)),                         (2)
```

where r,u,p now denote full digits. Substitution of the two Boolean inverse
equations gives (1). The verifier checks all64 assignments to these three
digits against (2), and checks all4 root and16 second-digit assignments
against two complete inverse scans. Since these exhaust the local inputs,
the certificate is an all-length identity, not a sampled trajectory claim.

Equation (1) can be solved in the same order for B^2. Given the original
input pair (a,b), compute

```
p = a XOR F,
q = b XOR (T AND (a XOR v)),                          (3)
```

where F,T use the previous two already computed output pairs. Initialize
(p_0,q_0)=(a_0,b_0 XOR1). This gives one O(m) Boolean-operation scan of
m digits, with constant working memory besides input and output. It avoids
materializing the intermediate B row; it does not reduce the order of
the work for many temporal iterations.

## 3. The second square retains the intervening digits

For five consecutive input digits d0,...,d4 at a bulk location, composition
of (2) gives

```
L^4(Y)_j = R(R(d0,d1,d2), R(d1,d2,d3), R(d2,d3,d4)). (4)
```

This holds without an origin convention for j>=4. Earlier positions are
handled by composing the exact origin and second-digit rules above. The
verifier checks the1024 five-digit assignments against four independent
inverse scans, including all boundaries of the corresponding prefix.

The tempting decimation replacement

```
L^4(Y)_j = R(d0,d2,d4)                               (5)
```

is false. Its failure can persist arbitrarily far from the origin on an
actual B orbit. Directly in the original binary coordinates, set

```
B0(x)=x XOR ((x<<1) OR (x<<2)) XOR1,
H(x)=(x>>2) XOR ((x>>1) OR x).
```

Eight B0 steps give25712. Its complete H orbit enters a four-cycle after
three steps, proving the infinite itinerary identity

```
Y=B^8(0)=003(0332)^infinity.
```

Applying L^4 returns B^4(0)=(03)^infinity. Starting at j=7, the four
successive bulk windows and outputs are:

| Window d0...d4 | Exact (4) | Decimated (5) | XOR error |
|---|---:|---:|---:|
|03320|3|2|1|
|33203|0|3|3|
|32033|3|2|1|
|20332|0|3|3|

The exactly closed four-cycle repeats these windows forever. Thus no
correction confined to a finite origin prefix can repair (5) on this
actual input. Here the correction itself is periodic and easy to describe;
the result does not exclude a useful nonlocal correction scheme.

## 4. The coefficient that a recursive correction must preserve

Any fixed inverse temporal block has a triangular affine action on its
current digit once the preceding input history is fixed:

```
a=p XOR c,
b=q XOR (d AND p) XOR e.
```

For (1), c=F, d=T, e=T AND(F XOR v). If a second block has coefficients
(c_bar,d_bar,e_bar) on the transformed preceding history, their composition
has coefficients

```
c_new = c XOR c_bar,
d_new = d XOR d_bar,
e_new = e XOR e_bar XOR (d_bar AND c).                (6)
```

This follows by direct substitution. The barred history is the actual
transformed history, including its boundary, rather than a fresh independent
stream. Formula (6) specifies a correction that an exact squaring scheme
must compute. No bound on the construction cost or compressed size of
those histories has been proved here.

## Exact verifier

[p3_bitplane_temporal_squaring.py](../../experiments/rule30/p3_bitplane_temporal_squaring.py)
uses its own digit-permutation inverse and its own original-coordinate
B0 and H maps; it imports no primary itinerary engine. It records the
64 local assignments, origin cases, fixed radius-four checks, complete
actual orbit and periodic discrepancies in
[p3-bitplane-temporal-squaring.json](../../experiments/rule30/p3-bitplane-temporal-squaring.json),
with source hashes. Run with the approved runner:

```
uv run --offline --no-project python experiments/rule30/p3_bitplane_temporal_squaring.py
```

No original-frontier census, center-prefix regeneration, or degree-growth
scan is involved. P3 remains open.

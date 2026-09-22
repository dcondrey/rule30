# Gamma powers return to BCCA; a sparse family fails on the marked query

Date: 2026-09-14. **Gamma powers have an exact simple form, but the proposed
family consisting of one C and one A power does not supply the successive
returns. It already gives the wrong singleton center bit at n=6.** The
correct second return is a conjugate of BCCA, the action already left open
by the existing powering method. This is a targeted candidate failure,
not a general obstruction to embeddings or fast Rule30 queries.

Words are chronological. A,B,C below are the itinerary actions; the
subscript0 distinguishes the original binary actions. Lowercase a means
A inverse. Gamma is the fixed-boundary embedding from the
[return-class report](RESULTS-p3-itinerary-return-classes.md).

## 1. All powers of Gamma, with the coordinates kept explicit

In original coordinates A0 commutes with multiplication by2. Since
Gamma0(x)=2 A0^-1(x), it follows that

```
Gamma0^k(x)=2^k A0^-k(x),
Gamma A=A Gamma.                                   (1)
```

The formula in itinerary coordinates is different. Let
H(x)=(x>>2) XOR((x>>1) ORx), and let Phi record the successive low-two-bit
H outputs. For every2-adic x,

```
Gamma0^2(x)=4 A0^-2(x),
H(4y)=A0(y),
H(Gamma0^2(x))=A0^-1(x).
```

The first itinerary digit of Gamma0^2(x) is0. The remaining itinerary is
that of A0^-1(x), so

```
Gamma^2(z)=4 A^-1(z),
Gamma^(2r)(z)=4^r A^-r(z), r>=0.                  (2)
```

For the second identity, A fixes digit0 and has section A there, hence
commutes with prefixing a zero digit. Thus A^-1 commutes with the factor4
in the first identity. This proves the formula for all r by induction.
It is not inferred from a finite list of Gamma powers.

There is a direct finite certificate as well. The verifier closes all
reachable states for Gamma A=A Gamma and Gamma^2=4a, comparing every
input digit and every successor. The latter comparison includes the
one-digit output delay and the original zero boundary. It therefore
checks the identities on every infinite tail.

The query cost of(2) is explicit. Digits below r are zero. A requested
digit j>=r is digit j-r of A^-r(z). One inverse A step uses the current
and previous supplied digits, with virtual previous digit0 at the origin.
Consequently this request needs at most r+1 input digits, in positions
max(0,j-2r),...,j-r, and O((r+1)^2) local Boolean operations after those
digits are supplied. Acquiring the input digits remains part of any
algorithm using this identity. Neither the input action nor its queried
digits are supplied for free.

## 2. The correct second return is the existing W

The first embedding identity is Gamma CA=B^2 Gamma. The root four-cycle
of B gives its exact first return

```
W=BCCA,
B^4(4z)=4 W(z).                                   (3)
```

Define D2 by chronological word a W A=aBCCAA, or ordinary composition
D2=A composed with W composed with A^-1. Using(2) and(3),

```
Gamma^2 composed with D2 = B^4 composed with Gamma^2,
Gamma^2(D2^m(0))=B^(4m)(0), m>=0.                (4)
```

The zero input is preserved because A and Gamma fix zero. These are
full-action embedding identities with the specified input boundary.
But W=A^-1 composed with D2 composed with A; equivalently, the
chronological word A D2 a is W. Introducing D2 has not reduced the unresolved return
action. Positive A and inverse A in that conjugacy, and any resulting
extra queried digits, must be retained in its evaluation cost.

A coordinate pitfall deserves an explicit control. The adjacent word
aB is the map x XOR1 in the original binary coordinates. Its itinerary
conjugate is not a finite-support digit permutation: aB(0)=1^infinity,
because A^-1 fixes zero and B loops on zero with output1. Thus rewriting
D2=(aB) C^2 A^2 does not produce a free low-digit correction in itinerary
coordinates. Evaluating through Phi to use the original low-bit flip
would also have to be charged.

## 3. A precise sparse-return candidate and an actual center falsifier

A tempting extension of the first identity is

```
E_k=C A^(2^k-1),
Gamma^k composed with E_k
  = B^(2^k) composed with Gamma^k.                (5)
```

It is valid at k=1. If it remained true, the embedded return would always
have one C and one power node, rather than a growing sequence of return
letters. This would still need an evaluation-cost argument. In fact(5)
already fails at k=2 on zero, including the actual coupled marked query.

Compute in original coordinates, where
A0(x)=x XOR((x<<1) OR(x<<2)), B0(x)=A0(x) XOR1. Then

```
B0^t(0), t=0,...,4: 0,1,6,27,100,
E2(0)=A0^3(C0(0))=221,
Gamma0^2(E2(0))=4 A0(C0(0))=52.                 (6)
```

The cancellation in the second line of(6) uses Gamma0^2=4 A0^-2 and
the final two A0 actions in the chronological word. The two original
values have H prefixes

```
actual:    100,111,100,
candidate: 52,51,55.
```

The low bit of itinerary digit2 is therefore0 for the actual B^4(0)
and1 for the proposed replacement. The
[actual-B query theorem](RESULTS-p3-actual-b-query.md) identifies precisely
this observable with c6: its exponent is4, digit position2, and requested
bit0. A separate literal Rule30 row calculation from the singleton seed
confirms c6=0. Thus restricting(5) to the required diagonal observable
does not save this candidate.

## Exact verification and scope

[p3_gamma_power_returns.py](../../experiments/rule30/p3_gamma_power_returns.py)
has its own elementary digit maps and literal Rule30 truth-table oracle.
It saves the two complete finite transducer certificates, directed Gamma
power controls, the exact first-return section, and the n=6 witness in
[p3-gamma-power-returns.json](../../experiments/rule30/p3-gamma-power-returns.json).
It hashes the established dependencies without rerunning their saved
return checks. No growing return closure, original census, or long center
prefix is generated.

The outcome is specific: Gamma powers are exact and usable with charged
local inverse queries; the sparse family(5) is false even for the actual
singleton observable; the correct D2 action returns to W. A different
controlled return family or an efficient evaluator for W remains open.

```
uv run --offline --no-project python experiments/rule30/p3_gamma_power_returns.py
```

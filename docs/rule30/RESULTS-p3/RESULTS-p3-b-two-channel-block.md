# Exact two-channel blocking of the actual B orbit

Date: 2026-09-14. **One dyadic step halves both the B-power time index
and the requested digit index exactly, by retaining two coupled fields.**
The blocked update is an eight-carrier transducer on a16-symbol alphabet.
Its primary output does not read the current complementary high bit,
but that bit can affect the next carrier. Actual seed rays prove that
the complementary field cannot simply be discarded or recovered from
an unphased finite spatial window of the primary field.

This is a constructive single blocking step, not an all-scale closed
renormalization or a sublinear query algorithm. A correction depending
on the time or root phase is not excluded. The
[verifier](../../experiments/rule30/p3_b_two_channel_block.py) and
[artifact](../../experiments/rule30/p3-b-two-channel-block.json) preserve
the entire local table and the exact small seed-ray certificates.

## 1. A bijective split and the marked-query reduction

Use the [itinerary B automaton](RESULTS-p3-itinerary-conjugacy.md), with
its fixed initial state B for every time step. Pair consecutive fine
digits and define

```
P_j = high(z_(2j)) + 2*low(z_(2j+1)),
Q_j = low(z_(2j))  + 2*high(z_(2j+1)).            (1)
```

No information is discarded. The inverse is

```
z_(2j)   = low(Q_j)  +2*low(P_j),
z_(2j+1) = high(P_j) +2*high(Q_j).                (2)
```

Let S denote this split, and define the two-field update
F=S composed with B squared composed with S inverse. Then

```
(P^(L),Q^(L)) = F^L(0,0) = S(B^(2L)(0))          (3)
```

for every L>=0. The boundary of each F update is the fixed chronological
carrier BB, not a freely chosen completion. Equation (3) retains the
actual zero ancestry at every step.

Odd exponents need no additional output observer. Since B(0)=1^infinity
(the single state B loops on input0 with output1), its split is the
constant field pair(2,1). For N=2L+r, r in{0,1}, define

```
(P_r^(L),Q_r^(L)) = F^L(I_r),
I_0=(0^infinity,0^infinity),
I_1=(2^infinity,1^infinity).
```

Then(P_r^(L),Q_r^(L))=S(B^N(0)). Both initial conditions are exact
seed-derived states. The r=1 case is not a new free boundary choice.

For a requested fine digit2j+d, where d is0 or1, and requested bit e,
equation (2) gives

```
bit_e(digit_(2j+d)(B^(2L+r)(0)))
  = bit_d(Q_r^(L)_j)  if d=e;
  = bit_d(P_r^(L)_j)  if d!=e.                    (4)
```

Thus one requested bit becomes one requested bit at half the time and
half the spatial index. The new update F acts on both fields. Applying
the same generic blocking construction again need not return to the
same eight-carrier family, and no such closure is asserted here.

## 2. Exact local equations with chronological carriers

Let s be the first B scan's current state and t the second scan's current
state. Both belong to{A,B,C}. Put

```
eps(A)=0, eps(B)=eps(C)=1,
c(A)=c(B)=0, c(C)=1,
psi(0)=A, psi(1)=B, psi(2)=psi(3)=C.
```

For the current input pair write P=p0+2p1, Q=q0+2q1. The first fine
digit is q0+2p0. Its intermediate and final bits are

```
u0 = q0 XOR eps(s),
u1 = p0 XOR (c(s) OR q0),
Q'low = u0 XOR eps(t),
P'low = u1 XOR (c(t) OR u0).
```

The updated states after this fine digit are

```
s1=psi(u0+2u1), t1=psi(Q'low+2P'low).
```

Process the second fine digit p1+2q1 with those states:

```
v0 = p1 XOR eps(s1),
v1 = q1 XOR (c(s1) OR p1),
P'high = v0 XOR eps(t1),
Q'high = v1 XOR (c(t1) OR v0).
```

The next block's carrier is

```
(s2,t2)=(psi(v0+2v1), psi(P'high+2Q'high)).       (5)
```

These are the ordinary one-digit ABC equations, applied first in time
and then to the next spatial digit. They prove the blocked rule on all
input tails. The verifier independently compares (5) with two complete
serial state passes for every pair in each reachable carrier.

From the fixed boundary BB, precisely these eight carriers suffice:

```
BB, BC, CA, CB, AB, CC, AC, AA.
```

The complete128 symbol edges remain inside this set. Each carrier's
16-symbol input/output table is a permutation, consistent with the
bijective block encoding of the prefix permutation B squared. No
ambient independence of P and Q is assumed for actual orbit claims;
checking the full local alphabet establishes an all-input rule that
can then be applied to the specified initial pair(0,0).

## 3. What is triangular, and where feedback remains

For each fixed carrier, P' is independent of q1, the current high bit
of Q. Also

```
Q'low = q0 XOR eps(s) XOR eps(t),
Q'high = q1 XOR R(s,t,p0,p1,q0),                  (6)
```

where R is explicitly given by (5). Thus the current complementary
high bit is merely toggled by a function of the other current bits and
the carrier. It can nevertheless change(s2,t2), and therefore influence
the next block. Ignoring this successor dependence would create a false
autonomous update.

In fact there is no all-input factor retaining only(P,low(Q)), regardless
of how its carrier states are lumped. From BB, input blocks(0,0) and(0,2)
have the same retained input and both emit retained output(1,0), but
their successors are BC and CA. Supply the same next block(0,0): their
retained outputs are respectively(1,0) and(0,1). The required successor
equivalence is therefore impossible. Equivalently, fine inputs0 and8
have identical entire retained input fields and different retained
B-squared output fields. This witness concerns arbitrary inputs;
neither input's actual seed ancestry is assumed.

The complete primary permutations make the remaining coupling visible.
Entries list P' at P=0,1,2,3:

| Carrier | low(Q)=0 | low(Q)=1 |
|---|---|---|
| BB | 1,2,3,0 | 1,2,3,0 |
| BC | 1,2,3,0 | 0,3,2,1 |
| CA | 0,1,2,3 | 1,0,3,2 |
| CB | 2,1,0,3 | 1,2,3,0 |
| AB | 2,1,0,3 | 2,1,0,3 |
| CC | 2,1,0,3 | 0,3,2,1 |
| AC | 3,0,1,2 | 2,1,0,3 |
| AA | 0,1,2,3 | 0,1,2,3 |

At the initial BB carrier the rule simplifies, for all16 inputs, to

```
P'=P+1 mod4,
Q'low=q0,
Q'high=q1 XOR ((1-q0)*(1 XOR p0 XOR p1)).         (7)
```

Starting from the actual zero boundary, the successive root pairs are
(0,0),(1,2),(2,2),(3,2),(0,0). In particular the primary root digit
does implement the desired exponent halving for every L. This exact
root law alone does not establish closure of the higher digits.

## 4. Exact actual-orbit feedback and local-slaving obstructions

The required rays have small complete spatial state certificates:

```
B^2(0) = 2^infinity,
B^4(0) = (03)^infinity,
B^6(0) = (2332)^infinity,
B^8(0) = 003(0332)^infinity.                     (8)
```

These are identities of entire actual rays. The verifier closes the
zero-input cascade state orbit at each of these four specified powers,
using102 local digit transitions in total. It retains every initial
state, transient, and periodic seam. The conclusions are not inferred
from a matching finite output prefix.

Splitting (8) gives

| Macro time L | Primary field P^(L) | Complementary field Q^(L) |
|---:|---|---|
| 1 | 1^infinity | 2^infinity |
| 2 | 2^infinity | 2^infinity |
| 3 | (31)^infinity | (23)^infinity |
| 4 | 0(13)^infinity | 01(30)^infinity |

First, Q cannot evolve autonomously under a single time-independent map,
even one allowed to inspect its entire input field. The identical fields
Q^(1)=Q^(2)=2^infinity would have to yield the different successors
Q^(2)=2^infinity and Q^(3)=(23)^infinity. An update supplied an additional
time or root phase is outside this claim.

Second, the primary feedback occurs at an actual reachable carrier. At
position1, macro rows L=1 and L=4 both enter in carrier BC with P=1.
Their respective Q values are2 and1. Equation (5) produces primary
outputs2 and3. Thus the dependence on low(Q) in the table is used by
the actual zero orbit; it is not solely an artifact of arbitrary inputs.

Third, Q cannot be a single unphased local function of a fixed finite
window of P across the actual orbit. P^(3) and P^(4) agree at every
position j>=1, while Q^(3) and Q^(4) differ at every j>=2. For any
fixed finite window radius, choose j far enough from0 that both windows
lie in the common P tail. They are identical and would have to give the
same Q value, a contradiction. A sequential decoder that remembers the
root phase, or a rule explicitly supplied the time phase, is not refuted.

There is a narrower phase-aware obstruction as well. At macro times0
and16, both the root phase and the time modulo16 coincide. Direct exact
evaluation of eight bits for the original binary generator
B_0(x)=x XOR((x<<1) OR(x<<2)) XOR1 gives B_0^32(0)=128 modulo256. Four
itinerary digits, computed using12 additional local Boolean updates,
are0002. Thus the split at macro time16 has initial P digits00 and
initial Q digits02. At macro time0 these prefixes are00 and00. Hence
a causal decoder of Q whose first two output digits depend only on
the first two P digits and the common root/time phase cannot work.
This test uses256 original Boolean updates; it does not construct a
large seed prefix. A decoder allowed lookahead, a different supplied
time phase, or more time information is not excluded by this witness.

The same rays locate the error in dropping Q and identifying P^(L)
with B^L(0). At L=4 the exact difference is

```
P^(4) XOR B^4(0) = 0(23)^infinity.               (9)
```

It is nonzero at every position after0, so the correction is not confined
to any finite boundary strip. It is still a compressed periodic field
in this example; no claim about all later correction complexity follows.

## 5. Remaining constructive issue

Equations (3)-(5) give the requested exact single-level change of scale
with both time and spatial index halved, keeping the original time
boundary and selected-bit readout. They expose a concrete partially
triangular coupling rather than assigning independent coarse histories.

The unresolved requirement for a fast recursion is a controlled family
under further blocking, or a phase-aware representation of the second
field whose total cost remains small. The failures in section4 exclude
only the stated ways of deleting that field. Keeping both full fields
indefinitely, while allowing the blocked alphabet and carriers to grow
without a bound, does not establish an acceleration.

The [inverse temporal-squaring kernel](RESULTS-p3-bitplane-temporal-squaring.md)
provides a complementary local description. Its temporal decimation
error is a different comparison from (9); neither is substituted for
the other in this certificate.

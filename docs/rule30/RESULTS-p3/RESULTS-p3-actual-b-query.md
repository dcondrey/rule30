# Both singleton-center parities are single B-power digit queries

Date: 2026-09-14. **The inverse-prefix recurrence cancels on the actual
singleton query. Both even and odd indices reduce to one specified bit
of one digit of an itinerary B power.** For h>=1 and e in {0,1},

```
c_(2h+e) = bit_e(digit_(h-1)(B^(h+1+e)(0))).        (1)
```

Here bit0 is the low bit, bit1 the high bit, and digits are numbered
from0. The boundary values are c0=c1=1. Formula(1) is an all-length
identity; it is not a conjecture inferred from finite center data.

The [evaluator and verifier](../../experiments/rule30/p3_actual_b_query.py)
reuse the exact [power-section engine](RESULTS-p3-power-node-sections.md)
without modifying it. The [artifact](../../experiments/rule30/p3-actual-b-query.json)
records finite implementation controls and construction costs. The
evaluator still advances through h-1 digit positions, so this result
does not establish a sublinear P3 algorithm.

## 1. An all-input boundary identity

Use A0,B0,C0 for the original binary maps and A,B,C for their conjugates
under the [itinerary map Phi](RESULTS-p3-itinerary-conjugacy.md). Write

```
G(x)=x XOR((x<<1) OR(x<<2)),
B0(x)=G(x) XOR1,
C0(x)=G(x) XOR(3-2*(x mod2)),
H(x)=(x>>2) XOR((x>>1) ORx),
R(x)=x>>1,
F(x)=2x+(x mod2).
```

F duplicates the first binary bit. Its two exact identities are

```
C0 composed with F = F composed with B0,
H composed with F = R composed with B0.            (2)
```

For the first identity, the binary sections of C0 are

```
C0(2x)=1+2B0(x),    C0(2x+1)=2C0(x).
```

B0 and C0 agree on odd x. Splitting according to x mod2 therefore
gives C0(F(x))=F(B0(x)), since B0 flips the low bit.

For the second identity, let x_j be the jth input bit. Bit0 of HF(x)
is x1 XOR(x0 ORx0)=x1 XORx0, which is bit1 of B0(x).
For j>=1, bitj is x_(j+1) XOR(x_j ORx_(j-1)), which is bitj+1 of
B0(x). This proves the equality at every bit, including arbitrary
higher tails. The verifier checks complete local boundary and generic
bulk truth tables; the translation of the bulk formula proves all
remaining positions.

Starting from0, equations(2) imply

```
C0^L(0)=F(B0^L(0))=2B0^L(0)+(L mod2),
H(C0^L(0))=R(B0^(L+1)(0)),                       (3)
```

for every L>=0. The first equality is also the familiar first-two-bit
seed boundary relation: A0^L(1)=1+2C0^L(0), hence
A0^L(1)=1+2(L mod2)+4B0^L(0). Its use here is to realize the marked
itinerary query without a separate inverse-prefix computation.

## 2. Cancel the prefix recurrence with the next B time

Let sigma be base-four right shift and
J=Phi composed with R composed with Phi^(-1). The exact local formula
from the [branch-transport report](RESULTS-p3-local-branch-transport.md) is

```
J(z)_j = high(z_j)
         +2*(low(z_(j+1)) XOR 1[z_j!=0]).         (4)
```

In particular low(J(z)_j)=high(z_j); evaluating that low bit requires
only the current digit. Since Phi H=sigma Phi, equations(3) give

```
J(C^L(0))=B^L(0),
sigma(C^L(0))=J(B^(L+1)(0)).                     (5)
```

These also follow from the guarded JC=BJ relation and J^2 C=sigma;
no false commutation of J with C or assertion J^2=sigma is needed.

The earlier exact singleton reduction is

```
c_(2h)=high(digit_(h-1)(C^(h+1)(0))),
c_(2h+1)=low(digit_h(C^(h+1)(0))).
```

The first line of(5) converts the even readout directly to the low bit
of B^(h+1). The second line converts the odd readout to the high bit of
B^(h+2) one digit earlier. This proves(1).

For comparison, reconstructing C^L from B^L at the same time uses

```
q0=L mod2,
q_(t+1)=high(b_t) XOR(low(b_t) ORq_t),
```

where b_t is digit t of B^L(0) and q_t is the low bit of digit t of
C^L(0). That recurrence is exact, but unnecessary for the requested
odd bit: it equals high(b'_(h-1)) in the next iterate B^(L+1)(0).
The extra action is included in the initial power exponent, not
implemented by reading every digit of the previous B output.

The related cancellation `(CA)^k(0)=J(B^(2k+1)(0))` is proved in the
branch-transport report. In particular its low-bit readout is one high
bit of B^(2k+1), removing the corresponding Gamma inverse observer.

## 3. Implemented evaluator and remaining cost

For n>=2 the evaluator constructs the single power node B^(h+1+e),
takes h-1 zero sections, and reads bit e of its root output on0.
Every section uses the complete root orbit and preserves the ordered
return and remainder. No B^L(0) integer, complete itinerary, or
length-L generator word is constructed at initialization. The exponent
and all subsequently constructed expression nodes are charged.

The saved controls compare n=8,17,32 with the original C-power
evaluator and an independent Rule30 row engine; n=0,1,2,3 check the
boundary conventions. The artifact retains node counts, distinct
section contexts, permutation work, exponent-operand bit counts, and
logical metadata size. These are exact construction statistics, not
complete bit-operation or wall-time complexity estimates. Allocation,
interning, hashing, and integer operations remain part of the cost.

| Query n | B advances | B nodes | Original C advances | Original C nodes |
|---:|---:|---:|---:|---:|
| 8 | 3 | 13 | 3 | 13 |
| 17 | 7 | 30 | 8 | 32 |
| 32 | 15 | 94 | 15 | 92 |

These three directed comparisons do not show a uniform node-count
improvement. The verifier also checks28 local truth-table rows, nine
specified integer boundary inputs, and six specified iterate identities
through an independent digit automaton and itinerary encoding.

The new query uses h-1 advances for both parities. It saves one advance
at odd n relative to the C formula and removes the inverse-prefix
observer from the same-time B-query route.
It does not prove that the constructed return expressions remain
small, nor that these h-1 advances can be skipped.

At the first B section, its root four-cycle gives

```
(B^(4k+s))|0=(BCCA)^k prefix_s(BCCA), 0<=s<4.
```

The exponent divides by4 while the return word has four letters.
Likewise converting CA^k back to B^(2k+1) removes an observer but
increases that exponent. These identities do not supply a measure
that simultaneously decreases the requested position, return-action
description, and total construction work. That bulk-query operation
remains the missing step; no shrinking-index complexity theorem is
claimed.

```
uv run --offline --no-project python experiments/rule30/p3_actual_b_query.py
```

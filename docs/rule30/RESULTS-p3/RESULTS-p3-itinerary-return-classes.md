# The first itinerary return classes: a precise obstruction and guarded reductions

Date: 2026-09-13. **The four first returns of K_C^2 cannot be replaced by
single ABC states, or powers of those states, using same-depth rooted-tree
conjugacies. Three branches admit exact reductions of marked zero-input
queries, and CA embeds into the even-input component of B^2 with a one-bit
delay.** A recursion with decreasing query cost remains unresolved.
No shrinking-index powering algorithm is claimed.

The [verifier](../../experiments/rule30/p3_itinerary_return_classes.py) and
[artifact](../../experiments/rule30/p3-itinerary-return-classes.json) retain
small exact first-return trees, independent arithmetic prefix permutations,
and every boundary guard used in the query reductions. These are targeted
algebraic certificates, not a census of singleton trajectories.

## 1. The exact returns and the proposed closure

Use the [itinerary automaton](RESULTS-p3-itinerary-conjugacy.md). State g
emits P_g(d), then enters psi(P_g(d)), where

```
P_A=(0,3,2,1), P_B=(1,2,3,0), P_C=(3,2,1,0),
psi(0)=A, psi(1)=B, psi(2)=psi(3)=C.
```

Words remain chronological: CA means apply K_C and then K_A. Suppress
the K subscript when writing a word action. Direct section composition
gives

```
C^2|_0=CA,  C^2|_1=CB,  C^2|_2=BC,  C^2|_3=AC.   (1)
```

The root action of C^2 is the identity, so each of these is the return
map used after dividing a C exponent by two at the corresponding digit.
The question is whether these maps return to a fixed simple family,
including the cost and effect of any conjugators.

CA and AC are cyclic-rotation conjugates, as are CB and BC. There are
therefore two relevant conjugacy classes at this first stage. Neither
class is conjugate to a power of a single original state A,B,C by an
automorphism preserving every rooted-tree level.

## 2. An exact obstruction to CA being B in different coordinates

CA and B have the same root four-cycle, and both have two eight-cycles
on two-digit prefixes. They differ at the next level:

| Action | Cycles on three-digit prefixes |
|---|---|
| CA | four cycles of length16 |
| B | two cycles of length32 |

This is proved by a compact first-return calculation. Follow the root
four-cycle starting at0. Its return words are

```
B:  R_B=BCCA,        root permutation(3,2,1,0);
CA: R_D=CBCCBCAA,    root permutation(2,3,0,1).     (2)
```

Each return permutation has two cycles of length2, represented by0 and1.
The next returns and their root permutations are

| Parent return | Representative | Twice-return section | Root permutation |
|---|---:|---|---|
| R_B | 0 | BCBCACAA | (3,0,1,2) |
| R_B | 1 | CBCCCACB | (3,0,1,2) |
| R_D | 0 | CACABCCCBCBCCAAA | (1,0,3,2) |
| R_D | 1 | CCACACBCABCBCBCB | (3,2,1,0) |

The first two permutations are four-cycles, giving2 cycles of length
4*2*4=32. Each of the last two has two two-cycles, giving4 cycles of
length4*2*2=16. The arithmetic verifier independently reproduces the
full64-point permutations; no finite-depth match is promoted to an
infinite equality.

In particular,

```
(CA)^16 fixes every three-digit prefix;
B^16 fixes no three-digit prefix, and B^16(0)=32 mod64. (3)
```

Any rooted-tree, prefix-compatible conjugacy would induce conjugate
permutations at every finite level, preserving cycle lengths. Equation
(3) therefore excludes every such conjugacy between CA and B, regardless
of the conjugator's amount of memory.

There is even no total prefix-compatible map Gamma in the direction

```
Gamma composed with CA = B composed with Gamma,    (4)
```

without an injectivity assumption. At depth3, the sixteenth iterate of
(4) would put every Gamma image at a fixed point of B^16; none exists.
The same argument excludes a same-time intertwiner of the CA zero orbit
into any B orbit at this precision. It does not exclude reverse factors
or identities for only a selected observable bit.

The other candidate class already differs from A at depth2:

```
A:  cycle lengths1,1,2,2,2,2,2,4;
CB: cycle lengths1,1,2,4,4,4.                       (5)
```

CA/AC have root cycle type(4), which among powers of A,B,C requires an
odd power of B. Such a power still has two32-cycles at depth3. CB/BC
have root type(2,1,1), which requires an odd power of A; such powers
retain the cycle lengths in (5). Even and negative powers introduce no
exception to these root and cycle-type arguments. Thus the entire
single-generator-power conjugacy proposal fails for all four returns.

These obstructions concern same-depth rooted-tree conjugacies, not
arbitrary homeomorphisms that change prefix depth. A guarded equality on
a restricted invariant input class is also different and can be useful.

## 3. Three valid marked-query reductions

### BC collapses to a power of B under the correct input guard

B and C agree on every input with odd low bit: on root digits1 and3
they have the same output digit and the same following state. Thus their
actions agree on every higher tail in those two cylinders.

If x is even, B(x) is odd. Therefore BC(x)=B^2(x). Both maps preserve
the entering even parity, so induction gives

```
(BC)^k(x)=B^(2k)(x) for every even x and k>=0.     (6)
```

In particular this holds on the zero input. Similarly,

```
(CB)^k(x)=B^(2k)(x) for every odd x and k>=0.      (7)
```

The parity is the low binary bit of the base-four input digit. Equations
(6)-(7) are full-output identities on their stated invariant cylinders,
not guesses based on matching a few iterates. They do not assert the
whole-space conjugacies excluded above. Note also that (6) doubles the
B exponent; it does not by itself preserve an exponent-halving gain.

### CB on zero becomes CA with one fewer queried digit

CB fixes the initial digit0 and has section CA there. Consequently

```
(CB)^k(0)=4*(CA)^k(0),  k>=0.                     (8)
```

The root digit is0, and digit j>=1 on the left is digit j-1 of the CA
orbit at the same exponent. This is an exact reduction of the queried
index, with no new input boundary or phase assumption.

### AC on zero becomes CA with a local change of observable

Write D=CA and E=AC. In ordinary function-composition notation,
D=A composed with C and E=C composed with A. Hence
E=A^(-1) composed with D composed with A. Since A(0)=0,

```
(AC)^k(0)=A^(-1)((CA)^k(0)).                      (9)
```

The inverse of the output-driven automaton is local in its supplied
output digits. If y=(CA)^k(0), then digit j of the left side is obtained
from p=y_(j-1), d=y_j, with the virtual p=0 when j=0:

```
-d mod4       if p=0;
d-1 mod4      if p=1;
3-d           if p=2 or3.                         (10)
```

Thus this particular conjugacy needs two adjacent CA digits, rather than
a new pass through the entire prefix. Its input remains the known zero
ray. The number of requested bits has increased, however. A recursive
algorithm using this reduction must account for those queries and their
possible sharing; no uniform bound follows merely from the locality of
one use of (10).

### CA embeds into the even component of B^2 with one bit of delay

There is a further positive relation that the preceding obstruction does
not prohibit. Write D=CA. A concrete four-state map Gamma satisfies

```
Gamma composed with D = B^2 composed with Gamma,
Gamma(0)=0.                                        (11)
```

For input base-four digits y_j, put y_(-1)=0 and define

```
(Gamma(y))_j = high(y_(j-1))
             +2*(low(y_j) XOR 1[y_(j-1)!=0]).      (12)
```

The state is just the previous input digit. Gamma maps Z_2 bijectively
onto its even-input component and delays one binary bit. It is not a
same-depth bijection of the entire rooted tree, so it does not contradict
section2. In particular (11) gives

```
Gamma((CA)^k(0))=B^(2k)(0).                       (13)
```

Here is an all-length derivation. Temporarily use A_0,B_0,C_0 for the
original binary generators before the itinerary conjugacy. Their binary
sections give

```
B_0^2(2x)=2*(C_0 composed with A_0)(x).
```

Let L(x)=2*A_0^(-1)(x). Then

```
B_0^2 composed with L = L composed with (A_0 composed with C_0).
```

Conjugating by Phi proves (11) for Gamma=Phi composed with L composed
with Phi^(-1). This expression is used to prove the identity, not as an
algorithm requiring either itinerary conversion. Indeed H(Lx)=x>>1,
and Lx mod4=2*low(x). If y=Phi(x), write u_j=low(y_j) and v_j=high(y_j).
The local H recurrence gives the bit at spatial position2 at time j-1
as u_j XOR(u_(j-1) OR v_(j-1)). These formulas produce exactly (12).

The verifier also proves (11) directly by a complete finite Mealy
bisimulation between the two compositions. Every input digit at every
reachable joint state is checked, including each successor. This
independently certifies equality on all infinite tails.

The inverse and its query cost are explicit. For z=Gamma(y), z is even,
and with a_(-1)=0,

```
high(y_j) = low(z_(j+1));
a_j=low(y_j)=high(z_j) XOR(a_(j-1) OR low(z_j)).   (14)
```

These reconstruct y uniquely from every even z, proving the claimed
bijection onto that component. In particular a high-bit query for
(CA)^k(0) becomes one low-bit query for B^(2k)(0), at the next digit.
A low-bit query instead requires the actual unary recurrence through
digits0,...,j of that B orbit, unless a separately constructed aggregate
can answer it. The implementation retains and charges those prefix
updates. It does not treat the coefficients as independent or supplied
for free.

This is an exact useful embedding into a larger marked family. The
exponent has doubled, the high-bit query index has increased by one, and
the low-bit case introduces a prefix observable. Those costs prevent
(11) alone from establishing the sought shrinking-index recursion.

## 4. Scope and verification

Equations (6), (8), and (9)-(10) reduce three zero-input return branches
to CA or a power of B while preserving their exact meaning. Equations
(11)-(14) give a further exact embedding for CA. They do not close a
recursion that reduces the remaining exponent and requested-observable
cost. The finite permutation obstruction identifies why a same-depth
replacement by B fails, while the embedding demonstrates why that
obstruction must not be overextended to other marked representations.

The verifier saves the four first sections, the two small return trees,
the directed prefix permutations, both odd-input cylinder identities,
all16 cases of the adjacent-digit inverse rule,32 guarded power controls,
and12 marked zero-input controls. Full-output finite checks use separate
arithmetic digit permutations. It also retains the complete Gamma
bisimulation,64 inverse-prefix controls, and four power/readout controls.
The all-length positive conclusions are
proved by section composition, the invariant parity guards, and the
explicit conjugacy. The negative conclusion uses an exact finite
conjugacy invariant, not an assertion that finite matching is sufficient.

```
uv run --offline --no-project python experiments/rule30/p3_itinerary_return_classes.py
```

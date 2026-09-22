# An exact affine field inside the actual B update

Date: 2026-09-14

The itinerary B update factors into two successive field updates. **The
second is affine in its entire input field when the other field is supplied.**
It has a local inverse and an exact compiler on a supplied, aligned pair
grammar. A staggered coordinate map turns this factorization into a closed
two-field evolution with one fixed actual initial condition.

The first field update remains nonlinear. Constructing its actual outputs,
and constructing aligned grammars through many iterations, are still paid
tasks. This is not a polylogarithmic center algorithm or an all-scale
renormalization theorem.

## 1. Definitions and the fixed boundary

Use the itinerary B map and the bijective split from the
[two-channel blocking report](RESULTS-p3-b-two-channel-block.md). For a fine
base-four ray Y, digits are low first, and

    P_j = high(Y_(2j)) + 2 low(Y_(2j+1)),
    Q_j = low(Y_(2j))  + 2 high(Y_(2j+1)).

Thus Y_(2j)=Qlow+2Plow and Y_(2j+1)=Phigh+2Qhigh. Write

    R=P(BY), V=Q(BY), R_j=a+2b, Q_j=q0+2q1.

The previous B-output odd digit is c+2h, where
c=R_(j−1).high and h=V_(j−1).high. At j=0 the actual B boundary is
**(c,h)=(1,0)**. It is not replaced by a completed spatial predecessor.

The one-digit B equations, for input a0+2a1 and output b0+2b1, are

    b0 = a0 XOR(previous_b0 OR previous_b1),
    b1 = a1 XOR(previous_b1 OR a0).

They determine the chronological scan on every finite prefix and every
infinite tail.

## 2. The affine half and its local inverse

**Theorem.** Given Q and R, the complete field V=Q(BY) is
$N_R(Q)$, where

    Vlow  = q0 XOR(c OR h),
    Vhigh = q1 XOR[a OR(b XOR Vlow)],                 (1)
    c_next=b, h_next=Vhigh.

For proof, B's even output digit is Vlow+2a. Its root toggle gives the
first line. The odd input's low bit is
Phigh=b XOR(Vlow OR a). Its output high bit is consequently
q1 XOR[a OR(b XOR(Vlow OR a))]. The outer OR with a masks the extra
inner a, giving the second line. This retains the entire chronological
seam.

Over $\mathbb F_2$, put

    A_j = (1+c)(1+a),
    K_j = q1 + a + (1+a)(b+q0+c).

Then the unknown carry obeys

    h_next = A_j h + K_j.                            (2)

The coefficients A_j depend only on the supplied R field; K_j is affine
in the current Q digit. Induction therefore proves that $N_R$ is affine
in the **whole Q field**, for every fixed R. Affine means
$N_R(U+W)=N_R(U)+N_R(W)+N_R(0)$, not necessarily linear.

The inverse is local when R and V are supplied:

    q0 = Vlow XOR(c OR previous_Vhigh),
    q1 = Vhigh XOR[a OR(b XOR Vlow)].                 (3)

Only the current digits and their immediately preceding supplied bits are
read. Thus $N_R$ is a bijection on every finite prefix, compatible with
all longer tails.

Equation (2) also gives an exact last-reset formula. A_0=0 because c=1
at the boundary. If ell is the last index at or before j with A_ell=0,
then

    V_j.high = XOR_(s=ell..j) K_s.                   (4)

This formula does not supply ell or the intervening fields for free.
No bounded reset spacing is assumed.

## 3. The nonlinear half, exact inverse, and full factorization

Define $M_Q(P)=P(BY)$. Its direct scan is

    a = Plow XOR(h OR q0),
    v0 = q0 XOR(c OR h),
    b = Phigh XOR(v0 OR a),
    h_next = q1 XOR(a OR Phigh), c_next=b.           (5)

These equations use the same boundary (1,0). They follow by applying the
two B digit equations to the even digit and then the odd digit. In
particular they do not obtain R by solving for arbitrary extra history.

For fixed Q, $M_Q$ is also a bijection. Given R, first compute
$V=N_R(Q)$ and then recover P locally:

    Plow  = Rlow XOR(previous_Vhigh OR Qlow),
    Phigh = Rhigh XOR(Vlow OR Rlow).                 (6)

Together (1) and (6) are exactly the local inverse of B, so both inverse
directions hold on all prefixes. The full split update is therefore

    (P,Q) --> (R,V)=(M_Q(P), N_(M_Q(P))(Q)).          (7)

Unlike N at fixed R, M at fixed Q need not be affine. With two coarse
cells, Q=00, and P encoded low-first as the integer 0,1,2,3, its outputs
are respectively 10,15,12,13. Their XOR is 4, contradicting the affine
rectangle identity. This is an arbitrary-input algebraic control, not a
claim that those four inputs occur in the actual zero orbit.

Even this special nonlinear map has a simple exact scan: if Q is identically
zero, the entering B root toggle stays 1. With one carry c initially zero,

    Rlow=Plow XOR c, Rhigh=Phigh XOR1,
    c_next=(Plow XOR c) OR Phigh.                    (8)

Its carry XORs Plow when Phigh=0 and resets to1 when Phigh=1. No invariance
of the zero-Q condition under the full actual evolution is asserted.

## 4. One actual initial condition and the marked query

The staggered coordinate map

    T(Y)=(U=Q(Y), R=P(BY))

is a bijection by (6). Equations (7) prove the all-length conjugate update

    T(BY) = (V, M_V(R)),  V=N_R(U).                 (9)

The actual initial ray Y=0 gives **T(0)=(0-infinity,2-infinity)**,
because B(0)=1-infinity. Iterating (9) once means one B action; iterating
it twice means B squared. No time-halving is claimed for a single use of
(9).

For a requested fine digit 2j+d and bit e, the original split gives

    bit_e(Y_(2j+d)) = bit_d(Q(Y)_j) if d=e,
                     bit_d(P(Y)_j) if d!=e.         (10)

To express both time parities using the single seed above, put

    U^(L)=Q(B^(2L)0), R^(L)=P(B^(2L+1)0).

The pair is T(B^(2L)0), so its macro-update is exactly two applications
of (9). Combining (10) with the
[actual singleton B-query theorem](RESULTS-p3-actual-b-query.md) yields

    c_(4m)   = high(R^(m)_(m−1)),       m>=1;
    c_(4m+1) = high(U^(m+1)_(m−1)),     m>=1;
    c_(4m+2) = low(U^(m+1)_m),          m>=0;
    c_(4m+3) = low(R^(m+1)_m),          m>=0.

The remaining c0=c1=1 are direct boundary values. This halves the
marked spatial index in a coupled representation while retaining both
fields and the full B-squared update. It does not bound the construction
cost through repeated scales.

## 5. Conditional compilation without expanding a supplied repeat

For a finite query prefix, suppose a grammar for the **aligned pairs**
$(Q_j,R_j)$ is supplied. Its nodes are digit pairs, concatenations, and
integer repeats. Alignment is part of the supplied object; producing it
from two separate grammars is an additional charged task.

The N transducer has four boundary contexts (c,h). Each input node has
a four-entry state transformation. At a concatenation, the actual output
state of the left child supplies the right child's state. At a repeat,
the child's transformation has an orbit of at most four states. Its
finite prefix and cycle determine an output grammar containing a repeat
of the cycle block and the actual remainder. No copy-count expansion is
needed.

The [compiler](../../experiments/rule30/p3_staggered_affine_field.py)
caches each (input node,boundary context). For s input nodes there are
at most 4s compiled contexts. A repeat context adds at most nine output
nodes, so **at most 36s+1 output nodes** suffice, including the empty node.
Metadata construction and four-entry map compositions are charged too.
This is O(s) structural work on integer lengths and exponents; their bit
arithmetic, interning, and storage access are not constant-cost assertions.
For example, with at most L bits per integer, ordinary arithmetic can
charge O(L squared) per multiplication or general division. A marked
output query follows the retained grammar and charges its node visits
and index-operand widths. The saved index-operand counter is partial
instrumentation: grammar-length operands, storage addressing, and the
arithmetic implementation also cost work. It is not a total bit-work count.

The verifier includes one 101-digit repeat-count control on a supplied
constant pair (Q,R)=(0,0). Its N output is the constant digit3, and no
expanded input or output field is constructed. This checks the new
compiler's repeat semantics; it is not an actual B-power construction.
The earlier [repeat transduction report](RESULTS-p3-itinerary-repeat-transduction.md)
already makes the distinction between compressed input repetition and
compressed iteration.

For the actual problem, R itself is produced by the nonlinear M half,
and subsequent aligned pair grammars must be constructed. The factorization
does not prove that their size remains small, nor that many alternating
M/N steps can be jumped. Supplying those histories would hide the
remaining computation.

## 6. Actual zero-run failure and its exact scope

The previous two-channel certificate proves the entire actual ray

    B^8(0)=003(0332)-infinity.

One additional B scan is enough to derive a new complete ray. The prefix
003 emits110 and leaves state A. The first0332 block then emits0102 and
leaves C; every subsequent0332 block emits3013 and returns to C. Hence

    B^9(0)=1100102(3013)-infinity,
    P(B^9(0))=200(32)-infinity.                     (11)

This refutes the proposed all-spatial avoidance of 00 in P of odd B
powers: the actual R digits at positions1,2 are zero. Nevertheless its
carry coefficients are A1=0,A2=1,A3=0. Thus this witness has only one
consecutive nonreset step. **It does not refute a maximum-two-block gap
between actual resets**, and no such gap theorem is proved here.

Nor can positivity of a finite H state supply a general reset guarantee:
H(13)=12 and H(12)=13, so the itinerary of13 is (10)-infinity and its P
field is identically zero. This is an exact counterexample to that broader
argument, without asserting that13 is an actual odd B-zero core.

## 7. Verification and scope

The [source](../../experiments/rule30/p3_staggered_affine_field.py) and
[artifact](../../experiments/rule30/p3-staggered-affine-field.json) retain
complete local factorization, affine carry, and inverse checks; directed
word and marked-index algebra controls; the two-cell nonaffinity witness; the closed B9 transport;
and all four grammar boundary contexts. The old B8 artifact is read and
its source hashes checked, without regenerating that orbit. The new ray
proof closes its repeated-state seam, rather than extrapolating a prefix.

    uv run --offline --no-project python experiments/rule30/p3_staggered_affine_field.py

All universal statements follow from the local equations and induction.
No center prefix, larger orbit census, or repeated blocking census is run.
The main P3 marked-query construction remains open.

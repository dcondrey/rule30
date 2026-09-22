# Compact incoming-digit profiles and a finite-group closure obstruction

Date: 2026-09-14. **The complete nine-counter action has an eight-bit
Heisenberg representation, and its full incoming-digit repair needs only
42 bits. Both compose exactly on supplied words. But no fixed finite-group
word annotation can close the spatial column update homogeneously and
retain its endpoint on the actual B zero orbit.** The last assertion is
an all-length theorem, not a failure inferred from one small profile.

The constructive compression and the obstruction delimit different
operations: aggregating a supplied temporal word is exact and cheap;
repeatedly constructing the next actual column needs a representation
that can grow, vary with position, or leave this group-annotation model.
No unrestricted P3 lower bound follows.

## 1. Eight counters encode both phase-indexed actions

Use the counters in the
[four-period carry report](RESULTS-p3-four-period-central-carry.md), with
the first position of a word assigned odd time. Retain

```
(U,V,W,C,D,Wdec,A,F0),                            (1)
```

and the word length modulo4. The omitted ninth counter is
`K=(floor(length/2) mod2)+C`. For an arbitrary initial nine-counter state,
the full action adds the zero-initialized counter values in(1), together
with exactly four cross terms:

```
W     additionally receives U_word*V_initial;
Wdec  additionally receives C_word*D_initial;
A     additionally receives C_word*V_initial;
F0    additionally receives D_word*U_initial.    (2)
```

This follows directly from the update equations: the relevant base
counters are translated, and no upper counter enters another upper
counter. Thus the zero-state values determine the entire action;
these are not independent marginals or a restriction to zero probes.

Put `Fbar=F0+U*D`, and arrange the eight bits as

```
p=(U,C),       q=(V,D),
Z=[[W,Fbar],[A,Wdec]].                           (3)
```

For chronological first/second actions at the same global phase, the
group product is

```
(p,q,Z) star (p',q',Z')
   = (p+p',q+q',Z+Z'+p'*q^T).                   (4)
```

This is the eight-bit block Heisenberg group. It is represented by
5-by-5 upper triangular matrices with blocks of sizes2,1,2:

```
[[I2,p,Z], [0,1,q^T], [0,0,I2]].
```

Chronological composition uses the second matrix times the first,
which explains the ordering p' q^T in(4). Associativity follows by
bilinearity, and every element has fourth power identity.

Changing the starting phase is an explicit involutive automorphism.
Let `S=[[1,0],[1,1]]` and `J=[[0,1],[1,0]]`. Then

```
R(p,q,Z)=(S*p,S*q,S*Z*S^T+U*J).                (5)
```

In the original coordinates this says

```
C_odd=U+C,       D_odd=V+D,
A_odd=W+U+A,
F0_odd=U+U*V+W+F0,
Wdec_odd=W+Wdec+A+F0+U*D.                       (6)
```

For example A sums `c_t*V_(t-1)+c_t`; adding its odd and even sums gives
W+U. The last equation follows by separating the full ordered area W
into odd/odd, even/even and the two cross-parity areas. Alternatively,
all of(5)-(6) follow by the append induction certified below.

An annotation is therefore `(h,n)` with h the eight Heisenberg bits
and n the length modulo4. Its concatenation is

```
(h,n) * (h',n') = (h star R^(n mod2)(h'), n+n' mod4).              (7)
```

A single supplied digit z has `c=1[z!=0]`, `d=1+high(z)`, and annotation
`p=(c,0),q=(d,0),Z=0,n=1`. Equations(4)-(7) supply an ambient finite
group of1024 elements; no claim that all are reached by supplied words
is needed. They reconstruct both starting-phase
affine maps, including K and the outgoing phase. The representation
uses ten bits including n, rather than two unrestricted affine matrices.
Its exponent divides8, as also follows from the earlier counter-action
proof. All lengths here describe supplied words; no trajectory is reset.

## 2. The full incoming-digit profile has an exact 42-bit construction

For a temporal driver word w and entering physical digit s, define T_s(w)
by the chronological recurrence

```
x_0=s,
x_t= -x_(t-1) mod4       if w_t=0;
     x_(t-1)+1 mod4      if w_t=1;
     3-x_(t-1)           if w_t=2 or3.
```

The output word is x_1...x_N. This is the actual next-column construction
when s=0, including its ordered output boundary. The endpoint permutation
is already determined by the first three input-annotation counters:

```
rho_w(a,b)=(a+U,b+V*a+W+U+U*V).                (8)
```

Retain the input annotation h(w) and all four output annotations
`h(T_s(w))`, s=0,1,2,3. They share the same length modulo4, so the
complete augmented profile needs `8*(1+4)+2=42` bits. Equation(8)
supplies the endpoint permutation without another stored matrix.

The exact concatenation rule is

```
T_s(uv)=T_s(u) concatenated with T_(rho_u(s))(v).                 (9)
```

Consequently each output annotation composes using the actual endpoint
rho_u(s), and (7) handles the phase at the cut. The implementation uses
five fixed-size annotation products per supplied letter: one input
annotation and four output annotations. It constructs no output-history
lists in its streaming profile builder. Its cost is O(N) fixed-bit work
and fixed-size working state for a supplied N-letter word. Input
construction and access costs remain charged.

These profiles are group annotations too. They embed in the product of
the input annotation group and the wreath product of four output
annotation groups by the D8 endpoint action. Thus concatenation is
associative and invertible. The profile exponent divides16: the endpoint
permutation has order dividing4. After four copies it fixes the incoming
states, and each accumulated annotation has length0 modulo4, placing it
in the exponent4 Heisenberg subgroup. The fourth power of that complete
four-copy action is therefore identity. The bound is attained by the
virtual letter1, whose complete profile has order16.
The supplied-repeat helper reduces a repeat exponent modulo16, charging
the arithmetic on that exponent. This statement concerns the fixed
profile, not B powers or the construction of another physical column.

## 3. The complete repair still fails to close on the saved actual boundary

Take the actual virtual driver `v=1^32`. Its first three physical output
columns, read at fine times1,...,32, are the saved words z0,z1,z2, with

```
z0=(1230)^8,
z1=(12130300)^4,
T_0(v)=z0,       T_0(z0)=z1,       T_0(z1)=z2.    (10)
```

The virtual driver represents the fixed physical boundary1; it is not
an interior column. Every displayed output uses initial physical digit0
and the original B zero ancestry.

Both v and z0 have the IDENTITY complete42-bit profile. In particular,
their own annotations agree, every incoming digit returns to itself,
and each of the four transduced words has the identity full affine
annotation in both starting phases. Their length32 also agrees.

Nevertheless z0 has the identity profile and z1 does not. The latter's
incoming-0 output is z2, whose zero-initialized nine-counter annotation is

```
(U,V,W,C,D,Wdec,A,F0,K)=(0,0,1,0,0,0,0,0,0).
```

Therefore even the full four-incoming-digit profile, supplemented by
the exact common length and initial phase, cannot determine its next
profile by one homogeneous update. The checker compares the complete
old affine actions as well as their compact representations. This is
not merely a collision of one scalar readout.

## 4. No fixed finite-group annotation can supply that homogeneous closure

The small witness has an all-length explanation covering every fixed
finite incoming-profile level.

**Theorem.** Let Psi map digit words homomorphically into a fixed finite
group G. For each N, allow an arbitrary map F_N:G->G and an arbitrary
endpoint readout r_N:G->{0,1,2,3}. Suppose the following contract holds
on the actual words

```
w_(-1)=1^N,       w_j=T_0(w_(j-1)) for j>=0:

Psi(w_(j+1))=F_N(Psi(w_j)),
r_N(Psi(w_j))=last digit of T_0(w_j).             (11)
```

The contract includes the virtual root and all actual subsequent
columns. The map and readout are homogeneous in the spatial column
index j; they may depend arbitrarily on N. Then such Psi,F_N,r_N do not
exist.

**Proof.** Let m be the exponent of G and choose N=4m. Homomorphic
aggregation gives

```
Psi(1^N)=identity,
Psi((1230)^m)=identity.
```

But w_0=(1230)^m. Equation(11) therefore forces F_N(identity)=identity,
and every subsequent actual word also has identity annotation. The
readout at w_(-1) is0, since T_0(1^N) ends in0. The same r_N must
therefore give0 at every subsequent column. It follows that every
digit of B^N(0) is0.

This contradicts the original-coordinate B_0 zero orbit. For every
positive integer N, its highest set bit is2N-2: B_0(0)=1, and the
shift-by-two term creates an uncancellable new highest bit at every
subsequent step. Thus B_0^N(0) is positive. The exact itinerary map is
injective and fixes0, so B^N(0) cannot be the zero ray. QED.

The proof uses neither off-orbit closure nor a common update/readout
across different lengths. Homomorphic word aggregation, a fixed finite
group, and spatial homogeneity are essential assumptions. It does not
exclude a representation that grows with N or depth, nonhomomorphic
summaries, position-dependent updates/readouts, or another algorithm.
The contradiction concerns exact physical endpoint recovery; an
arbitrary separately supplied position-dependent computation is not
being treated as a group readout.
The contract also requires every spatial column at each fixed N.
Correctness only at the one column coupled to a marked singleton query
need not satisfy(11), so that narrower task is not excluded.

## 5. The unbounded profile family and its explicit construction cost

There is an exact parameterized repair, but its naive size is explicit.
At depth k, retain the annotation of the input word and the annotations
of every word obtained with each sequence of up to k incoming digits.
These form a four-branch tree with

```
8*(1+4+...+4^k)+2 = 8*(4^(k+1)-1)/3+2 bits.    (12)
```

All nodes share length modulo4. Prefix nodes supply the endpoint
permutations needed to route the incoming-digit paths at a concatenation
cut. Thus concatenation acts exactly on the tree. A single actual column
update selects its incoming-0 subtree, consuming one available level.
This is a description of the all-depth algebra, not an enumeration of
the trees. Explicit construction needs O(4^k) stored nodes and a
comparable number of annotation operations per concatenation.

The finite-group theorem prohibits replacing this entire growing family
by one fixed group annotation satisfying(11). It does not prove that
the trees must be materialized. A useful next construction must show
how their actual shared structure can be obtained from the constant
root word1^N with a controlled size and evaluation cost. The present
package gives no such bound and claims no shrinking marked-query work.

## 6. Exact checks

The [verifier](../../experiments/rule30/p3_heisenberg_column_profiles.py)
checks4096 complete counter-append contexts, phase reversal and group
identities, and the complete old affine actions on a spanning set.
It verifies four-incoming profile concatenation and repeat contracts
on directed supplied words, including the saved actual words. No
growing-depth profile survey or new period census is performed.
The [artifact](../../experiments/rule30/p3-heisenberg-column-profiles.json)
retains the full incoming-profile witness and source hashes.

The finite-group theorem is proved independently of these controls and
was independently audited. Its positivity and itinerary facts are
established in the [actual-period report](RESULTS-p3-autonomous-profile-bound.md)
and [itinerary report](RESULTS-p3-itinerary-conjugacy.md).

```
uv run --offline --no-project python experiments/rule30/p3_heisenberg_column_profiles.py
```

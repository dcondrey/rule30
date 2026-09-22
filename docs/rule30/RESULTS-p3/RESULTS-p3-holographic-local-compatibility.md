# Local compatibility of the Pfaffian route under independent edge bases

Date: 2026-09-14. **No assignment of independent invertible complex binary
bases to the edges makes every uncontracted four-leg equality tensor
and an incident Rule30 constraint tensor matchgate signatures.** The
gate's four edges must all meet four-leg equality tensors. This is an
all-basis local obstruction to the stated unblocked construction. It
also extends to every positive uniform temporal blocking depth in the
coarse bulk, with full neighborhood and equality tensors retained. It
does not exclude boundary pinning, different block contractions, gadgets,
or a sublinear P3 algorithm.

The question was whether interference in a tensor contraction could
replace the ordered-history computation. A prerequisite for the standard
construction fails before any large network is built. No spacetime census
or approximate tensor truncation is involved.

## 1. Exact model and the required identities

Use the four-leg tensors, with fixed leg order,

```
E=|0000>+|1111>,
T(a,b,c,y)=1[y=a XOR(b OR c)].
```

E expresses equality of the four occurrences of an interior spacetime
variable. Allow a different invertible complex 2-by-2 matrix B_e on
every edge. Transform its equality leg by B_e and its gate leg by
B_e^(-T), preserving the contraction. Each transformed local tensor
must be a matchgate signature. The bases may differ even among edges
of the same spatial or temporal type.

Such a signature has either even or odd support parity. At arity four
the even quadratic relation, in this order, is

```
f0000*f1111-f1100*f0011+f1010*f0101-f1001*f0110=0.
```

There is the corresponding relation on odd coordinates. These parity
and Grassmann--Plucker conditions are standard necessary matchgate
identities; see [Cai and Choudhary's primary paper](https://pages.cs.wisc.edu/~jyc/papers/matchgate-holograph.pdf).
The proof below only needs their necessity. In particular, failure of
parity alone suffices to reject a transformed gate.

## 2. The independent-leg equality classification

Suppose E'=(B_1 tensor ... tensor B_4) E has pure parity eta. Write
Z=diag(1,-1) and K_i=B_i^(-1) Z B_i. Then

```
(K_1 tensor ... tensor K_4) E=(-1)^eta E.          (1)
```

Every K_i is an invertible traceless involution. Flatten (1) into a
matrix with legs12 as rows and legs34 as columns. The right side has
column space span{|00>,|11>}. The left side's column space is spanned
by the two independent product vectors

```
K_1|0> tensor K_2|0>,  K_1|1> tensor K_2|1>.
```

They span that column space because K_3 tensor K_4 preserves the
independence of |00>,|11>. A nonzero product vector in span{|00>,|11>}
must be proportional to one of those two basis vectors: the associated
diagonal 2-by-2 matrix has rank one. Therefore K_1,K_2 are monomial
with matching orientation, either both diagonal or both antidiagonal.
The row space gives the same conclusion for K_3,K_4. Repeating with
the split13|24 forces one common orientation on all four matrices.

If the K_i are **diagonal**, each is Z or -Z and each B_i is monomial.
E' is then supported on exactly one complementary pair of binary words.
That pair has one support parity, since its length is even. Precisely
one nonzero complementary-pair product remains in the quadratic
matchgate relation for that parity. It cannot vanish. This excludes
the diagonal case, including all possible zero-entry bases.

If the K_i are **antidiagonal**, the two rows of B_i are their respective
left eigenvectors for +1 and -1. Thus, with nonzero parameters,

```
B_i=D_i H diag(alpha_i,1),
H=[[1,1],[1,-1]],
```

where D_i is diagonal and nonsingular. For example, writing the rows
as(a_i,b_i),(c_i,d_i), one has c_i/d_i=-a_i/b_i;
choose alpha_i=a_i/b_i and D_i=diag(b_i,-d_i).

Remove the harmless diagonal row scalings and put A=product_i alpha_i.
The equality coefficient at a word of weight k is A+(-1)^k. Pure
parity therefore requires A=1 for even support, A=-1 for odd support.
These tensors also satisfy their parity's matchgate quadratic: all
four complementary-pair products have a common value and alternate
in sign. Restoring the row scalings multiplies each such product by
the same nonzero factor.

This proves the complete classification under four independent bases.
In particular, each incident edge of a matchgate equality tensor must
use a Hadamard-phase basis, even though its phase is unconstrained
individually. No uniqueness theorem for tensor decompositions is assumed;
the two elementary matrix flattenings supply the argument.

## 3. The homogeneous case as a checked corollary

Write B=[[a,b],[c,d]]. The transformed equality coefficient at any word
of Hamming weight k is

```
f_k=a^(4-k)*c^k+b^(4-k)*d^k.
```

First suppose all four entries are nonzero. Set alpha=a/b and gamma=c/d.
Invertibility gives alpha!=gamma.

For **even** support parity, f_1=f_3=0 implies

```
alpha^3*gamma=-1,  alpha*gamma^3=-1.
```

Dividing yields alpha^2=gamma^2. Since alpha!=gamma, gamma=-alpha;
substitution gives alpha^4=1.

For **odd** support parity, f_0=f_2=f_4=0 implies

```
alpha^4=-1,  alpha^2*gamma^2=-1,  gamma^4=-1.
```

Again alpha^2=gamma^2 and gamma=-alpha, this time with alpha^4=-1.

Thus every nonzero-entry candidate has the form

```
B=D H diag(alpha,1),
H=[[1,1],[1,-1]],  alpha^8=1,
```

where D is nonsingular diagonal. Indeed choose D=diag(b,-d).
Conversely these bases give a pure parity equality tensor; for D=identity
its coefficients are alpha^4+(-1)^k. They satisfy the four-leg quadratic
relation as well. Nonsingular diagonal row scaling preserves both parity
and that homogeneous relation.

Zero entries do not add candidates. Odd support is impossible if any
entry vanishes, by f_0=f_4=0 and invertibility. For even support, f_1=f_3=0
then forces B to be diagonal or antidiagonal. In either case the only
nonzero equality coordinates are 0000 and 1111. Their product is nonzero,
violating the displayed even quadratic relation.

This recovers section2 when all four bases coincide. Its eighth-root
restriction is specific to that homogeneous specialization; independent
edge phases need not be roots of unity.

## 4. None of the independent bases gives the gate pure parity

For each admitted edge basis,

```
B_i^(-T)=(1/2) D_i^(-1) H diag(alpha_i^(-1),1).
```

The outside diagonal matrix and scalar do not change support. Thus gate
parity is precisely the parity of the Walsh transform H^(tensor4) V,
where

```
V(s)=product_(i:s_i=0) alpha_i^(-1) * T(s).
```

Every weight is nonzero, so V and T have identical support. Let X flip
one binary coordinate, and Z=diag(1,-1). Since H X=Z H, the Walsh
transform of V has pure parity eta if and only if

```
X^(tensor4) V=(-1)^eta V.
```

In particular, the support of V would have to be closed under bitwise
complement. But T(0000)=1 and T(1111)=0. The first equality is Rule30 on
input000; the second follows because input111 produces0 rather than1.
This violates the required support symmetry. The transformed gate has
both parities for every admitted basis, proving the claim.

The complement witness is independent of every edge phase and diagonal
scaling. It does not even need a constraint on the product of the four
phases entering this gate. Those edges may come from four different
equality tensors. This avoids fitting unknown complex bases.

## 5. Every positive uniform temporal blocking depth also fails in the bulk

The equality argument has an all-arity necessary version. Let m>=3 and
E_m=|0^m>+|1^m>. If independent binary edge bases transform E_m into
a matchgate, each edge basis must again be D_i H diag(alpha_i,1).
To prove this, apply the conjugated parity equation to any chosen pair
of legs versus the other m-2 legs. Both vectors on the latter side
remain independent, including when m=3. The same two-dimensional
column-space argument forces each pair of K_i to have matching
monomial orientation. Overlapping pairs link all m legs.

The diagonal orientation would leave just one complementary support
pair s,complement(s). For odd m this already violates parity. For even
m>=4 use the general matchgate identity, with positions where a and b
differ listed in increasing order,

```
sum_i (-1)^i f_(a XOR e_i)*f_(b XOR e_i)=0.
```

Set a=s XOR e_1 and b=complement(s) XOR e_1. The sum runs over all
m positions. Its i=1 term is nonzero. Every other term flips two
positions of s, giving neither s nor its complement because m>=4,
so all those terms vanish. This is a contradiction. This form of the
identity is [Cai and Gorenstein, Theorem2.1](https://theoryofcomputing.org/articles/v010a007/v010a007.pdf).
The argument uses the actual support positions; it assumes no invariance
under arbitrary leg permutations or bit-flip changes of matchgate
coordinates. The antidiagonal orientation forces the stated Hadamard
form exactly as in section2. Necessity is all that is needed below.

Now fix any integer temporal block depth t>=1. Represent each coarse
Rule30 update by its exact t-step Boolean function on the full nominal
2t+1-bit input neighborhood and one output bit. Denote its constraint
tensor by T_t. Retain all these input occurrences; each interior coarse
variable then has a COPY_(2t+2) equality tensor. Require that every
edge of the selected coarse gate meets such an uncontracted equality
tensor, and that all those tensors are transformed into matchgates.

The all-arity lemma forces a Hadamard-phase basis on every edge of T_t.
The Fourier-parity argument from section4 therefore requires its
original support to be closed under simultaneous bit complement.
But for every t>=1,

```
Rule30^t(all-zero input)=0,
Rule30^t(all-one input)=0.
```

Both constant infinite configurations become all zero after one step,
and all zero remains all zero. The same calculation holds on the finite
shrinking dependency cone. Thus T_t contains its all-zero input/output
assignment and does not contain the complementary all-one assignment.
No independent invertible binary bases can make this uniformly
coarsened bulk tensor network a matchgate network.

This is a proof for every finite t, not a search over blocking depths.
It leaves different contractions, grouping neighboring variables into
larger alphabets, eliminating unused legs, and seed-specific boundary
reductions outside its scope. A blocking depth comparable to the entire
finite query can remove every full interior gate; that situation is
not covered by the bulk premise. The theorem does not say that every
representation of a finite Rule30 computation fails.

## 6. Verification and limits

The [verifier](../../experiments/rule30/p3_holographic_local_compatibility.py)
checks the local Rule30 relation against its independent Wolfram-code
truth table. It then works exactly in the four cyclotomic fields for
root orders1,2,4,8, covering all eight homogeneous canonical roots and
all their algebraic conjugates. It checks the dual contraction convention, equality
parity and the quadratic relation, and explicit nonzero gate coefficients
of both parities. It independently checks the weighted Walsh formula.
Two additional rational controls use genuinely different phases2,3,5
and either1/30 or-1/30, with independent diagonal row scalings. Both
give matchgate equality tensors and mixed-parity gates. These controls
retain the distinction between independent phases and the special
eighth-root homogeneous list. The
[artifact](../../experiments/rule30/p3-holographic-local-compatibility.json)
records the witnesses. The all-basis conclusion rests on the flattening
classification and support argument, rather than on a numerical search.

The all-arity extension has a sparse exact checker for its single-term
matchgate-identity witness and a two-case check of the constant-background
update. Its universal time-depth conclusion uses the induction above;
the checker does not enumerate truth tables of larger blocked rules.

This rejects independent binary bases in the unblocked network at a
Rule30 gate whose four edges meet uncontracted COPY4 tensors. A pinned
boundary variable or a tensor whose legs have already been contracted
can have different arity and is not silently covered. Grouped variables,
gadgets, and other algebraic contraction methods need separate analyses.
No network planarity assertion or global complexity lower bound is used.

As a control against interpreting this as computational hardness, the
same complement-support argument rejects the Rule90 gate when encoded
with the same unused middle-input leg and COPY4 convention. Rule90's
separate linear shortcuts remain valid. Failure of this local tensor
representation does not imply failure of other algorithms.

Even passing these local conditions would not itself settle P3: a generic
Pfaffian algorithm has a cost in the size of the explicit network, while
the requested target charges all construction and demands o(n) total
work. [Morton's primary treatment](https://arxiv.org/abs/1101.0129) describes
the circuit-size-dependent Pfaffian construction. No implicit small
Pfaffian or cheap singleton marked query has been constructed here.

```
uv run --offline --no-project python experiments/rule30/p3_holographic_local_compatibility.py
```

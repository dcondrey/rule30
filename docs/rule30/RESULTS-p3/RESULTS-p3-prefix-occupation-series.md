# Ordered prefix-action series and paid Cartier queries

Date: 2026-09-14. **An ordered integer polynomial retains the complete incoming-digit
prefix action and has an exact column-update equation. Its Cartier even/odd
recursion halves a supplied prefix length in the same eight-element permutation
alphabet.** The maintained query routine charges the coefficient work: without
an additional compressed-input contract it still reads N leaves. This establishes
no new complexity bound for the singleton marked query.

There are two exact counterexamples to shortcuts within this construction.
Evaluating the polynomial at1, even retaining its full integer occupation matrix
and endpoint permutation, fails to close the next column on saved actual
histories. Replacing its Hadamard equation by an ordinary rational inverse already
fails at the first two letters of the actual boundary construction. These specify
operations that an improved representation must preserve.

## 1. The ordered polynomial and its exact composition

Use the actual temporal column transducer from the
[incoming-profile report](RESULTS-p3-heisenberg-column-profiles.md). For a supplied
word w=w_1...w_N and an entering physical digit s,

```
x_0=s,     x_t=M_(w_t)(x_(t-1)),     T_s(w)=x_1...x_N,
M_0(x)=-x mod4,   M_1(x)=x+1 mod4,   M_2(x)=M_3(x)=3-x.       (1)
```

The actual boundary construction uses s=0 in every column, starts with the
virtual word1^N, and iterates T_0. The virtual word is a boundary, not an
interior column. No current predecessor is substituted for this ancestry.

Write M_d also for its4-by-4 permutation matrix acting on column vectors. Put

```
R_0=I,   R_t=M_(w_t)...M_(w_1),
A_w(z)=sum_(t=1..N) z^(t-1) R_t.                              (2)
```

Coefficients lie in integer matrices. This polynomial retains every ordered
prefix permutation, on all four entering digits. It determines the original
sequence of action matrices through R_t R_(t-1)^(-1); the distinction between
input digits2 and3 is unnecessary for(1).

For a chronological concatenation u then v,

```
R_uv=R_v R_u,
A_uv=A_u+z^|u| A_v R_u.                                      (3)
```

This follows by separating prefixes at the cut. Consequently

```
A_(u^r)=A_u sum_(k=0..r-1) (z^|u| R_u)^k.                    (4)
```

In particular A_(1^N)=M_1 sum_(k=0..N-1)(z M_1)^k. It can be written as
`M_1 (I-(z M_1)^N)(I-z M_1)^(-1)` in formal power series. The apparent
inverse here is legitimate because its constant term is I, and the numerator
makes the result a polynomial. This supplied geometric expression has a short
construction from N. Its degree and integer occupation counts are not killed by
the finite exponent of the underlying permutation group.

Equations(2)-(4) describe exact ordered data and expression construction.
They do not make arbitrary polynomial expansion or coefficient extraction free.

## 2. The column update is a Hadamard prefix-product equation

For entering digit s define four scalar selector polynomials

```
E_d(z)=e_d^T A_w(z)e_s
      =sum_(t=0..N-1) 1[x_(t+1)=d] z^t.                     (5)
```

Let Q_t be the action of the first t letters of T_s(w), including Q_0=I, and
Q(z)=sum_(t=0..N) Q_t z^t. Then

```
Q=I+z sum_(d=0..3) M_d (E_d Hadamard Q),
A_(T_s(w))=(Q-I)/z.                                         (6)
```

The Hadamard product multiplies coefficients at the same index, entrywise
against the scalar selector. Thus the coefficient equation is exactly
`Q_(t+1)=M_(x_(t+1)) Q_t`. It has a unique polynomial solution by forward
induction; N=0 gives Q=I. The final coefficient also retains the outgoing
permutation. Every entering digit s is treated with its own ordered selectors.

This is a growing, characteristic-zero closure. It lies outside the fixed
finite-group theorem because A_w has arbitrarily many coefficients. The
unpaid operation in a compressed implementation is constructing or querying
the solution of(6) after repeated spatial column updates. Calling that operation
a single expression node is not a complexity bound.

## 3. Exact Cartier halving, with the order preserved

The matrices in(1) generate

```
D8={x -> epsilon*x+a mod4 : epsilon in{+1,-1}, a in{0,1,2,3}}.
```

For a general supplied D8-letter sequence g_0,g_1,... let E_g be its one-hot
selector series, indexed from0. Write C_0 and C_1 for the even and odd Cartier
operators: C_i(sum a_t z^t)=sum a_(2t+i) z^t. The paired selector is

```
F_h=sum_(b*a=h) (C_0 E_a) Hadamard (C_1 E_b).                 (7)
```

Here b*a means b after a. The coefficient at k selects exactly
`h=g_(2k+1) g_(2k)`. There are eight possible output letters, regardless of the
number of halvings. For a finite word, only complete pairs enter F.

Let Q^even(z)=sum Q_(2k)z^k and Q^odd(z)=sum Q_(2k+1)z^k. Then

```
Q^even=I+z sum_h h(F_h Hadamard Q^even),
Q^odd=sum_a a((C_0 E_a) Hadamard Q^even).                     (8)
```

Indeed a pair advances Q_(2k) by g_(2k+1)g_(2k), and its odd intermediate
prefix advances it only by g_(2k). This proves both equalities coefficient by
coefficient, including a final unpaired letter. The original entering state is
retained because these are full permutation matrices. Once applied to(5),
there is no fresh boundary initialization at a pair cut.

The implemented `CartierQuery` recursively queries one coefficient Q_N using
(7)-(8), without constructing all Q_t. With an ordinary one-hot coefficient
oracle its exact work is N leaf labels,8N selector calls and N constant-size
group compositions, including multiplication by the identity at the requested
cut. The active recursion uses O(log N) stack frames. Thus the recursion halves
the index but does not by itself halve the total work. Costs of obtaining the
input selector coefficients, and integer index arithmetic, remain charged.
On a word RAM with O(log N)-bit words and constant-cost supplied coefficient
access this is O(N) work; it is not a sublinear query algorithm.

A separate `SuppliedPeriodicQuery` makes the stronger input contract explicit.
Given a nonempty period of P letters, it prepares its prefix products in P
group compositions. For N=qP+r it returns

```
Q_N=Q_r (Q_P)^q.                                           (9)
```

Every D8 element has order dividing4, so a query then needs at most four group
compositions, plus reading N, division by P, and residue arithmetic. The verifier
exercises an81-bit N without expanding the repetition. The supplied P-letter
period and its preparation are paid; neither its discovery nor the construction
of the next actual column's period is supplied by this theorem.

In particular(7) builds products of adjacent action letters in a supplied
series. It does not prove that these paired selectors can be shared or updated
cheaply across successive T_0 constructions. Equation(6), with its retained
prefix products, is still required for that operation.

## 4. Full integer occupation counts still lose necessary order

The specialization O_w=A_w(1) is a4-by-4 integer occupation matrix. Entry(d,s)
counts the times that the output of T_s(w) equals d. Also retain N and R_w.
These counts grow with N, so the finite-group theorem alone does not exclude
their closure.

Nevertheless there is an exact actual-boundary collision. Use only the saved
32-by-3 zero-orbit artifact from the
[autonomous-profile report](RESULTS-p3-autonomous-profile-bound.md). For times1
through32 its column words are z_0,z_1,z_2, with

```
v=1^32,                z_0=(1230)^8,
z_1=(12130300)^4,
T_0(v)=z_0,   T_0(z_0)=z_1,   T_0(z_1)=z_2.                 (10)
```

The two inputs v and z_1 have the same length32, the same starting phase and
entering digit0, the same endpoint I, and the same complete integer matrix:

```
O_v=O_(z_1)=[[8,8,8,8],[8,8,8,8],[8,8,8,8],[8,8,8,8]].     (11)
```

Their outputs have different endpoints:

```
R_(T_0(v))=R_(z_0)=I,
R_(T_0(z_1))=R_(z_2): (0,1,2,3) -> (2,3,0,1).              (12)
```

Thus `(N,O_w,R_w)` has no homogeneous next-column update even on these saved
actual histories and the required virtual boundary. This checks all four
incoming occupation profiles, not only the zero probe. Additional word
statistics, column-dependent annotations and the ordered series itself are
outside the counterexample. No new orbit was generated to obtain it.

## 5. An ordinary rational inverse is already wrong at length2

At the first two virtual boundary letters11, the actual output is12.
Therefore its selectors are E_1=1,E_2=z and the other selectors vanish.
Replacing Hadamard products in(6) by ordinary multiplication would give

```
Q_wrong=(I-z B-z^2 C)^(-1),
[z^2]Q_wrong=B^2+C,       but Q_2=C B.                       (13)
```

Here B=M_1 and C=M_2. Each column of the wrong coefficient sums to2, whereas
each column of the correct permutation matrix sums to1. This is an exact
nonnegative-integer discrepancy. Coefficients0 and1 agree, so length2 is the
first possible failure. Formula(13) refutes that ordinary-inverse substitution;
it does not refute more structured rational-series solvers.

## 6. Verification and remaining task

The [exact verifier](../../experiments/rule30/p3_prefix_occupation_series.py)
and its [artifact](../../experiments/rule30/p3-prefix-occupation-series.json)
check the complete64-entry D8 multiplication table, supplied-word cuts and
all four incoming states, the finite Hadamard and Cartier identities, every
requested prefix of the directed control words, the charged periodic query,
and both counterexamples. Actual data are read from the existing32-by-3
artifact; no period census, larger center prefix or growing profile family is
computed. Source and report hashes are recorded.

The remaining construction problem is precise: represent and evaluate the
iterated solutions of(6), or their paired selectors in(7), with a proved total
cost bound for the actual marked query. The series identities and supplied-input
queries establish that contract's algebra; they do not establish its compressed
construction cost or settle P3.

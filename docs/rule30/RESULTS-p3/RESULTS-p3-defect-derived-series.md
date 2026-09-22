# Exact commutator propagation and unbounded derived length of the defect groups

Date: 2026-09-14. **Proved on complete maps:** a local commutator propagates
a bit flip by two places. It gives explicit finite defect groups of
arbitrarily large derived length, rules out virtual solvability of the
full group, and yields an exponential dimension requirement for faithful
characteristic-two matrix models of those finite groups. With the stated
Tits-alternative dependency, the full group has no faithful finite-dimensional
matrix representation over any field.

These concern the **complete group action**, not the cost of one requested
singleton bit. They prove neither a sublinear P3 algorithm nor an unrestricted
lower bound. No literature-priority claim is made for the classification
consequences; the commutator proof and witnesses below are explicit.

Verifier: [p3_defect_derived_series.py](../../experiments/rule30/p3_defect_derived_series.py).
Artifact: [p3-defect-derived-series.json](../../experiments/rule30/p3-defect-derived-series.json).

## 1. Definitions and the complete-map identity

Use **ordinary composition**, with the rightmost map applied first, and
[g,h]=g h g^(-1) h^(-1). Let

\[
A(x)=x\mathbin{\mathrm{XOR}}((2x)\mathbin{\mathrm{OR}}(4x)),\qquad
\tau_j(x)=x\mathbin{\mathrm{XOR}}2^j.
\]

A is the original binary A0, not the itinerary-coordinate map. Its
coefficient formula is

\[
y_i=x_i+(x_{i-1}\lor x_{i-2}),\qquad x_{-1}=x_{-2}=0.       \tag{1}
\]

All coefficient sums are over F2. This triangular rule is invertible on
infinite binary inputs. In particular, changing y_(j+1) leaves the inverse
bits x_0,...,x_j unchanged and toggles x_(j+1).

For every j>=0,

\[
\boxed{[A\tau_j A^{-1},\tau_{j+1}]=\tau_{j+2}.}             \tag{2}
\]

**Proof.** Put gamma_j=A tau_j A^(-1) and write y=A(x). Toggling x_j
changes only three output coordinates:

\[
\begin{array}{c|ccc}
\text{coordinate}&j&j+1&j+2\\ \hline
\text{change}&1&1+x_{j-1}&1+x_{j+1}.
\end{array}                                                \tag{3}
\]

This is the Boolean derivative of OR in each of its arguments. Replacing
y by tau_(j+1)y leaves x_(j-1) unchanged and toggles x_(j+1), by (1).
Consequently

\[
\gamma_j\tau_{j+1}=\tau_{j+2}\tau_{j+1}\gamma_j.
\]

Both gamma_j and tau_(j+1) are involutions. Multiplying by them on the
right gives (2). At j=0 the coefficient x_(-1) in (3) is zero; the same
argument applies. At every other coordinate the two maps agree without
truncation, so this proves equality on every infinite input.

## 2. Explicit witnesses inside finite defect windows

Retain the boundary group D from the
[reset-group normal form](RESULTS-p3-automaton-group-identification.md):

\[
\sigma(x)=4\lfloor x/4\rfloor+((x-1)\bmod4),\qquad
D=\langle\tau_0,\sigma\rangle\cong D_8.
\]

It contains tau_1=sigma^2, and [tau_0,sigma]=tau_1, so tau_1 is in D'.
Define

\[
K_m=\langle A^s D A^{-s}:0\le s\le m\rangle,\qquad
H^{(0)}=H,\quad H^{(d+1)}=[H^{(d)},H^{(d)}].
\]

Every K_m is a finite 2-group acting within its first 2m+2 bits, by the
existing complete-map localization theorem. No enumeration of that group
is needed here.

First, (2) inductively proves

\[
\tau_j\in K_m\quad(0\le j\le2m+1).                         \tag{4}
\]

The cases j=0,1 hold in D. For j>=2, tau_(j-2) belongs to K_(m-1),
so A tau_(j-2) A^(-1) belongs to K_m; tau_(j-1) also belongs to K_m.
Their commutator is tau_j. This proves (4) by induction on j, for every
window containing that index.

The stronger derived-series statement is

\[
\boxed{\tau_j\in K_m^{(d)}
 \quad\text{if } d\ge1,\ m\ge d-1,\ 2d-1\le j\le2m+1.}   \tag{5}
\]

For d=1, the j=1 case is the D' identity above; all j>=2 follow from
the same commutator used in (4). Suppose (5) holds at d, and take
m>=d and 2d+1<=j<=2m+1. Then

\[
\tau_{j-2}\in K_{m-1}^{(d)},\qquad
\tau_{j-1}\in K_m^{(d)}.
\]

Conjugation by A sends K_(m-1) into K_m, and hence sends its dth
derived subgroup into K_m^(d). Applying (2) to these two members gives
tau_j in K_m^(d+1), proving the induction.

In particular,

\[
\tau_{2m+1}\in K_m^{(m+1)}\setminus\{1\},\qquad
\boxed{\operatorname{dl}(K_m)\ge m+2.}                     \tag{6}
\]

Here derived length is the least d with K_m^(d)=1. At m=0 the bound is
the exact derived length 2 of D8. Already K_1 is not metabelian: its
second derived subgroup contains tau_3. The general statement does not
claim that m+2 is the sharp length for every m.

## 3. Neither the kernel nor the full group is virtually solvable

The established normal form is

\[
G=\langle A,D\rangle=N\rtimes\langle A\rangle,\qquad
N=\langle A^s D A^{-s}:s\in\mathbb Z\rangle,
\]

where N is a locally finite 2-group and G/N is infinite cyclic. Equation
(6) proves N is not solvable: it contains finite subgroups of unbounded
derived length.

If N had a solvable subgroup of finite index, its normal core C would
also be solvable and of finite index. The finite quotient N/C is a
2-group: lift a finite generating set of the quotient into N; those
lifts generate a finite 2-group mapping onto it. Thus N/C is solvable.
An extension of a solvable group by a solvable group is solvable, giving
a contradiction. Therefore N is not virtually solvable. Intersecting any
hypothetical finite-index solvable subgroup of G with N shows that G is
not virtually solvable either.

This settles the specific structural question left by the earlier
noncommutation witness. The kernel does not become an abelian or bounded
solvable collection of correction terms at larger windows.

## 4. Exponential matrix dimension in characteristic two

For every field F of characteristic 2, a faithful representation
K_m -> GL_d(F) must satisfy

\[
\boxed{d\ge2^{m+1}+1.}                                    \tag{7}
\]

Here is a self-contained representation argument. Every action of a
finite 2-group P on a nonzero finite-dimensional F-space has a nonzero
fixed vector. Induct on |P|. A nontrivial finite 2-group has a central
involution z. Its matrix satisfies (z-I)^2=0, so W=ker(z-I) is nonzero
and P-invariant. On W the action factors through P/<z>, to which the
induction applies. Repeating the fixed-vector result on successive
quotient spaces gives a complete invariant flag with trivial actions on
its one-dimensional factors. Thus the image lies, in a suitable basis,
in the upper unitriangular group UT_d(F).

Let J be the strictly upper triangular matrix algebra. Its ideals satisfy
J^a J^b subset J^(a+b), so

\[
[1+J^a,1+J^b]\subseteq1+J^{a+b}.
\]

Consequently UT_d(F)^(s) is contained in 1+J^(2^s), and it is trivial
when 2^s>=d. Its derived length is at most ceil(log_2 d). Faithfulness
and (6) require ceil(log_2 d)>=m+2, equivalent to (7).

Thus no fixed matrix dimension over characteristic 2 faithfully encodes
all complete defect windows. This does not bound the size of a
nonfaithful observer that computes only one bit, compressed matrix
evaluation, or representations with other operations.

## 5. The full group is not linear over any field

There is also a qualitative any-field corollary, using an explicitly
external theorem. Every torsion-free subgroup of G intersects the torsion
group N trivially, so its projection to G/N=Z is injective. It is therefore
cyclic. In particular G has no nonabelian free subgroup.

The Tits alternative states that a finitely generated group of matrices
over a field either has a nonabelian free subgroup or is virtually
solvable. G is finitely generated and satisfies neither conclusion, so
it has no faithful finite-dimensional matrix representation over any
field. This is an application of the theorem, not a claim to prove it
in the finite verifier. The original characteristic-zero and positive-
characteristic statements appear as Theorems 1 and 2 of
[Tits, *Free Subgroups in Linear Groups* (1972)](https://perso.univ-rennes1.fr/serge.cantat/Documents/Tits-Alternative.pdf);
in positive characteristic the finitely generated locally finite quotient
in Theorem 2 is finite. The all-field finitely generated formulation is
also directly implied by Theorem 1.1 of the primary research paper
[Breuillard, *A Strong Tits Alternative*](https://arxiv.org/abs/0804.1395).

The conclusion concerns representing the entire group faithfully by
fixed finite matrices. It does not exclude matrix algorithms for a
specific orbit, a marked observable, or matrices of growing size.

## 6. Relevance and verification limits

The original singleton query uses a particular ordered norm product,
not arbitrary elements of every K_m. Theorems (6) and (7) therefore do
not prove that this query needs exponential state, linear time, or any
other general resource lower bound. They prevent using a fixed solvable
full-group normal form or a faithful fixed-matrix action as an unproved
shortcut. A fast algorithm specialized to B^N(0) remains possible and
unconstructed. Period-two exclusion and the other prize problems are
unaffected.

The verifier checks the complete local Boolean derivative cases, then
480 directed finite-input commutators at j=0,1,2,3 using an inverse
verified against the independent raw binary Mealy recursion. It checks
the D8 base identities with untouched higher bits, and constructs small
proof DAGs for five specified derived-subgroup witnesses. These DAGs
check containment bookkeeping, not finite group closures. The all-window
conclusions use (2) and the symbolic index ranges in (4)-(5); the
characteristic-two and Tits consequences use the proofs above.

No old frontier census, singleton center prefix, growing group census,
GPU computation or paid compute is run. Earlier reports and artifacts
are preserved. Run:

```
uv run --offline --no-project python experiments/rule30/p3_defect_derived_series.py
```

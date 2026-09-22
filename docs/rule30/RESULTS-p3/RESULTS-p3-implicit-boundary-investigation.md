# P3: finite-core powering and implicit boundary actions

Updated: 2026-09-14. **P3 remains open. The exact reductions below have
not produced a uniform sublinear algorithm for the singleton center bit,
or a lower bound for arbitrary algorithms.** Both center parities reduce
to one specified itinerary B-power digit. Dyadic blocking halves both
indices while retaining two coupled fields, but construction and evaluation
under repeated blocking remain unbounded by any sublinear cost proof.
Both fine-bitplane updates can be made conditionally affine. Constructing
their changing control fields remains part of the temporal computation.

The separate inverse-prefix observer cancels exactly. The surviving
Cartier correction has a local formula and exact supplied-history
aggregation rules; obtaining its required history remains necessary.
Fixed finite-group annotations cannot provide the stated homogeneous
spatial closure. Growing representations are still possible. The working
section evaluators continue to advance linearly many digit positions.

This continues the [bulk-jump implementation](RESULTS-p3-bulk-query-jumps.md).
The question was whether its expensive explicit boundary states could be
replaced by a cheaper exact object. The results distinguish finite-integer
orbits, full ordered word actions, and the final requested bit.

## 1. An all-length finite-core period theorem

For the exact integer core

\[
 H(x)=(x\gg2)\mathbin{\mathrm{XOR}}((x\gg1)\mathbin{\mathrm{OR}}x),
\]

bit j at the next time is

\[
 x_{j+2}\mathbin{\mathrm{XOR}}(x_{j+1}\mathbin{\mathrm{OR}}x_j).
\]

The two bits above it drive a unary reset or toggle. Reading coordinates
from the highest bit downward gives an exact cycle-lifting construction.
On an upper cycle of period P, a reset produces a unique extension of
the same period. Without a reset, odd driver parity doubles the period;
even parity gives two extensions of the same period. This retains phase
and both actual driving columns.

The new spacing argument restricts those doublings. The first is possible
at width four, the second no earlier than width nine, and subsequent
doublings are at least seven columns apart. Therefore every eventual
cycle of a nonnegative integer of width at most w has period dividing

\[
 P_w=\begin{cases}
 1,&0\le w\le3,\\
 2^{\lfloor(w+5)/7\rfloor},&w\ge4.
 \end{cases}
\]

This is an all-width upper bound, not a fitted growth rate. The
[finite-core powering report](RESULTS-p3-triangular-core-power.md)
gives the spacing proof and exact verifier. Its independent lower bound
is also uniform: a positive width-w cycle of period P requires

\[
 w\le4^P-1.
\]

To prove the latter, represent successive spatial columns by ordered
pairs of complete P-bit temporal words. Every target pair has a unique
predecessor. A path leaving the exterior pair (0,0) cannot revisit a pair,
so it contains at most the other 4^P-1 states. This does not constrain a
moving center query merely by proving facts about eventual fixed-width
cycles.

The top-down reset analysis gives a common safe transient bound
T_w=(w-1)P_w for w>=1, with T_0=0. Consequently

\[
 H^{T_w+P_w}(x)=H^{T_w}(x),\qquad 0\le x<2^w.
\]

For k>=T_w, one may replace k by
T_w+((k-T_w) mod P_w). This is an exact uniform fast-forward rule for
a supplied finite integer. The bound can be exponential in w, and the
integer, transient, and phase computations are charged. It is not an
o(n) center-query algorithm.

The [complete period-four column certificate](RESULTS-p3-period-four-column-certificate.md)
sharpens the third doubling: it first occurs at width30. The graph checks
all256 ordered pairs of four-periodic columns, retains every temporal
seam, and closes its entire97-node positive component. Every positive
integer has eventual primitive period1 at widths1--3, period2 at widths4--8,
period4 at widths9--29, and period8 at width30; there is one cycle up to
phase at each of these widths. The unary return argument excludes hidden
higher-period continuations before the listed leaves. Combining the
width30 anchor with the seven-column separation gives the stronger bound
P_w=2^floor((w-9)/7) for w>=30. This improves a constant in the exponential
bound, with no new asymptotic P3 conclusion or assumption about the query's
transient.

## 2. Two shortcuts fail on the actual center query

The existing reduction uses x=C^(h+1)(0), followed by H updates and a
bit-zero or bit-one readout. These values are genuine singleton-query
cores, not arbitrary states selected to cause failure.

| Attempted shortcut | Exact witness | Wrong readout |
|---|---|---|
| Reduce time modulo the eventual period from the initial state | At n=11, x=C^6(0)=3204 has transient 2 and period 4; the query needs H^5 | bit0(H^5(x))=0, but bit0(H^1(x))=1 |
| Extend a correctly phased eventual cycle backward through the transient | At n=18, x=C^10(0)=820716 has transient 10 and period 4; the query needs H^8 | bit1(H^8(x))=0, but the extrapolated bit1(H^12(x))=1 |

Thus knowing the cycle and its phase is insufficient when the query lies
before that cycle. No claim is made that every large query lies in the
transient, or that no other algorithm can handle it cheaply.

The periodicity theorem concerns the integer zero-output quotient H.
It does not assert that the ordered Q words, their complete maps, or
their unrelated input histories become equal at the same times.

## 3. Two other exact ways to represent a boundary

The [section reward construction](RESULTS-p3-section-reward-action.md)
computes a demanded section's root toggle by composing a low-prefix
permutation together with a reward bit for every incoming prefix. It
works directly on a shared word expression. At fixed precision this
really skips an enormous expanded word, but at precision m its explicit
table contains 2^m contexts. The construction cost cannot be omitted.

Its actual-core counterexample also sharpens the missing information:
two chunks of Q(C^9) have identical letter counts and identical complete
low-two-bit permutations, yet different next-bit rewards at the same
incoming residue. The ordered reward cannot be reconstructed from that
permutation and the counts alone.

The [zero-corridor calculation](RESULTS-p3-zero-corridor-jump.md) supplies
a different exact bulk identity: a specified triangular region of
chronological zero guards makes the two-step recurrence linear, allowing
binomial and dyadic jumps. A single zero column does not suffice. An
actual C^5 core has that column permanently zero and still violates the
unguarded four-step jump through an explicit quadratic residual. Reading
the full triangular guard certificate costs quadratic work; cheap guards
are proved only for special closed-cycle controls.

## 4. The actual coupled query, rather than a generic finite core

The actual input to H is not arbitrary: its length and iteration count
are coupled in H^h(C^(h+1)(0)). This relation must survive any change of
coordinates. The exact itinerary transformation does retain it:

\[
 \Phi(x)=\sum_{t\ge0}(H^t(x)\bmod4)4^t,\qquad
 \Phi H=\operatorname{shift}_4\Phi,\qquad \Phi(0)=0.
\]

Right-permutivity makes Phi a bijective base-four isometry. Its action
on every A/B/C generator has an explicit three-state realization. The
states have digit permutations

| State | Outputs on input digits 0,1,2,3 |
|---|---|
| A | 0,3,2,1 |
| B | 1,2,3,0 |
| C | 3,2,1,0 |

After emitting digit d, the next state is A if d=0, B if d=1, and C
otherwise. The transition uses the actual **output** digit, which makes
this different from the original input-driven section machine.

The [itinerary report](RESULTS-p3-itinerary-conjugacy.md) proves the
conjugacy, gives a constructive inverse, and retains the exact local
HC error that led to the transformation. For every nonempty chronological word U,
one zero section in this new automaton is literally Q(U). Thus the
same core can be advanced without the old two binary sections followed
by a cut and an append. Every concatenation still feeds its actual
left-child output into the right child.

The [quaternary evaluator](../../experiments/rule30/p3_quaternary_section_query.py)
constructs the initial C power by binary concatenation and executes
these sections on the shared word graph. Since Phi(0)=0, this algorithm
does not first construct an unknown original integer and translate its
entire itinerary. Its [saved controls](../../experiments/rule30/p3-quaternary-section-query.json)
give:

| Query n | Core section advances | Grammar nodes | Distinct section contexts | Composed permutation entries |
|---:|---:|---:|---:|---:|
| 8 | 3 | 17 | 19 | 52 |
| 17 | 8 | 38 | 52 | 136 |
| 32 | 15 | 90 | 125 | 344 |

All queries agree with independent row evolution; 42 complete core-word
comparisons agree with literal Q updates. The n=32 earlier core evaluator
constructed 437 nodes. This is a finite implementation improvement,
not a fitted asymptotic bound. The new evaluator still makes a linear
number of section advances. The table counts operations and contexts;
integer identifiers, lengths, allocation, and dictionary work retain
their bit costs. There are also sixteen constant leaf-permutation entries.

There is a second constructive property of the new machine. Its input
state transformations form an eight-element monoid. Consequently one
pass over an arbitrary repeated block W^m requires at most three distinct
block transductions: one transient block and a cycle of at most two.
The [repeat-transduction report](RESULTS-p3-itinerary-repeat-transduction.md)
gives the exact construction and charges its grammar operations. This
skips expansion of a repeated **input block**, not an arbitrary number
of repeated applications of the machine. Keeping those two counts
distinct is essential to the P3 cost question.

The generic right-permutative itinerary construction is a standard
symbolic-dynamics principle; the report distinguishes it from this
explicit simultaneous A/B/C realization and its implemented query.
No claim that an equivalent coordinate system alone solves P3 is made.

## 5. Multi-iterate returns: exponent division is exact, closure is missing

The continuation tests repeated **machine iterations**, which the
one-pass repeated-input rule does not handle by itself. For an action U
with root-digit orbit d,p(d),...,p^(q-1)(d), let R be the ordered product
of its sections around that complete orbit, and let S_r be the product
of its first r sections. Then

```
(U^(qk+r))|d = R^k S_r,  0<=r<q<=4.
```

The [power-node evaluator](RESULTS-p3-power-node-sections.md) implements
this identity without expanding the exponent. In particular
`(C^(2k))|0=(CA)^k`. A directed 100-bit exponent control needs only nine
nodes including a separate fixed-power control. This is one section,
not an enormous completed center query. The n=32 query still uses15
advances and constructs92 nodes, compared with90 in the earlier
concatenation evaluator. There is no claimed monotone or asymptotic
improvement. The expanded return word grows by the same factor by which
the exponent is divided; whether the needed compressed descriptions
remain cheap is the unresolved issue.

The [return-class investigation](RESULTS-p3-itinerary-return-classes.md)
proves real reductions with their boundary costs:

- On even inputs, `(BC)^k=B^(2k)`; the parity guard is invariant.
- `(CB)^k(0)=4*(CA)^k(0)`.
- `(AC)^k(0)=A^(-1)((CA)^k(0))`; that inverse readout uses two adjacent
  digits with the stated origin value.
- A four-state injective map Gamma sends the whole CA action into the
  even component of B squared: `Gamma CA=B^2 Gamma`, with Gamma(0)=0.
  A complete23-state composition check verifies all92 edges. Its high-bit
  readout is local; its direct low-bit inverse has a unary prefix
  recurrence. Section6 shows that one additional B action absorbs this
  recurrence, eliminating a separate inverse-prefix computation.

The last relation doubles the exponent again. It does not supply a
shrinking-time recursion. It also demonstrates why a failed conjugacy
test should not discard every larger representation: CA is not conjugate
to B by any same-depth prefix bijection, since their depth-three cycles
have lengths16 and32 respectively, but the delayed embedding above is
valid. These are distinct mathematical statements.

Two other proposed closures now have exact counterexamples. The
[reset-language report](RESULTS-p3-reset-token-languages.md) proves an
explicit bijection from every even-digit input under K squared to the
language `low(z_(j+1))=1[z_j=0]`, with even initial digit. But K fourth
does not return even streams to themselves: `200 -> 203` is a shortest
witness. A complete state/phase certificate gives the actual ray
`K^8(0)=00202(2013)^infinity`. Its eventual cycle escapes even the union
of those two languages with any fixed alphabet permutation, finite
prefix, and tail shift. The exact22-state reset recognizer also proves
that the actual `K^4(0)=(02)^infinity` has no universal two-pass reset
substring. Arbitrary larger token families remain untreated.

The [digit-pair report](RESULTS-p3-digit-pair-renormalization.md) refutes
all eight possible uniform injective pair embeddings by exact second-digit
seams. Its stronger global decoder obstruction has no memory assumption:
K exchanges the rays `(12)^infinity` and `(21)^infinity`, but K has no
fixed point. Thus no total map D can satisfy `D K^2=K D`. This obstruction
does not apply to a map defined only on the actual seed orbit.

For that actual orbit, the
[causality report](RESULTS-p3-actual-orbit-decoder-causality.md) proves
that an unrestricted-delay continuous index-halving decoder exists.
A decoder producing k digits from2k input digits exists precisely when
`P_(2k)>P_k` for every k, where P_m is the exact zero-orbit period modulo
4^m. Equivalently its return depths must satisfy
`alpha_s<=2*alpha_(s-1)+1` at every s. These quantitative inequalities
are **unproved**; the saved check covers only six output depths. Even
a proof would give neither cheap evaluation nor the inverse readout
needed to reconstruct a requested fine digit from a shorter computation.

## 5a. The known reset-group structure retains the ordered correction

The [catalogue identification](RESULTS-p3-automaton-group-identification.md)
matches the original binary machine exactly with automaton2369, using
only the renaming (a,b,c)=(C0,B0,A0). Grouping two input bits makes its
section independent of the starting state. Established reset-automaton
theory therefore applies: the generated group is N semidirect Z, where
N is locally finite. The direct specialization proves N is a locally
finite2-group and gives explicit finite support after one common
conjugation. This is an application of a known theorem, not a new group
classification or a consequence of the finite controls alone.

The cyclic degree chi sends each original generator to1, counts signed
letters, and is preserved by every section. Thus every section of B0^N
still has degree N. Inverse cancellations cannot shorten it below N
ordinary signed letters; this does not restrict compressed powers or
their evaluation cost.

The [strengthened precision rule](RESULTS-p3-precision-filtration.md)
uses the section-closed subgroup of even degree. Every element in that
subgroup has fourth power fixing three bits. Iterating this local fact
gives, for h>=1,

```
g^(2^[h-floor((h-1)/3)])=identity modulo2^h.
```

For an even-degree base g, the exponent improves to
`2^[h-floor(h/3)]`. A separately proved uniform fixed prefix may also
be removed from the required precision. The maintained helper now uses
these bounds and retains the previous rule for comparison. The initial
marked exponent is still smaller than the resulting modulus, so this
does not give a sublinear query bound. The optional degree condition is
on the base of the power, not merely on its exponent.

With tau(x)=x XOR1, the normal form of B0^N retains the ordered product

```
tau Ad_A(tau) ... Ad_A^(N-1)(tau) A^N,
Ad_A^j(tau)=A^j composed with tau composed with A^(-j).
```

All compositions here are ordinary. The positive conjugates are finite
prefix permutations, but their support grows with N. Since A^N fixes0,
evaluating this ordered correction at0 already evaluates B0^N(0).
The group theorem supplies no cheap collection rule for that product.
In particular, neither local finiteness nor noncontraction settles the
marked-query cost. Sorting the correction into even and odd conjugation
indices fails directly at the marked query n=5: it replaces B0^4(0)=100
by96 and changes the requested itinerary bit. The precision verifier
retains this control with the ordered product intact.

## 5b. The exact correction groups have unbounded derived length

The [commutator theorem](RESULTS-p3-defect-derived-series.md) adds a direct
all-length structural constraint. In original binary coordinates, put
tau_j(x)=x XOR2^j. With ordinary composition and commutator ghg^-1h^-1,

```
[A tau_j A^-1, tau_(j+1)] = tau_(j+2) for every j>=0.
```

The proof uses the three affected output bits of A under an input flip,
and the triangular inverse; it includes the boundary j=0. For the finite
window group K_m generated by Ad_A^s(D8), 0<=s<=m, it produces
tau_(2m+1) in the (m+1)st derived subgroup. Thus K_m has derived length
at least m+2, and the locally finite kernel N is not virtually solvable.
Neither is the full group G=N semidirect Z.

Every faithful characteristic-two representation K_m→GL_d requires
d>=2^(m+1)+1: finite2-groups are unitriangular in characteristic2, and
the derived series of d-by-d unitriangular matrices terminates by
ceil(log_2 d). The report also derives that G is not linear over any field
using the cited Tits alternative. Its cyclic quotient and torsion kernel
exclude nonabelian free subgroups, whereas G is not virtually solvable.

These are statements about faithful representations of the complete
group action. They exclude a fixed solvable full-group normalization and
faithful fixed-matrix powering, but give no work lower bound for the
particular marked B orbit. A nonfaithful observer or growing representation
with cheap access remains outside the conclusion.

## 5c. A nonlinear commutator family does admit a compact evaluator

The [balanced defect normal form](RESULTS-p3-balanced-defect-normal-form.md)
provides a constructive simplification beyond those representation
restrictions. With ordinary composition, define

```
E_0=tau_0,    E_(d+1)=[A E_d A^-1,E_d].
```

The complete map E_d toggles only bit2d. For d>=2 its exact guard is:
the first2d-4 bits vanish and the next two bits agree. All other inputs
are fixed. This follows by induction from a proved arbitrary-guard
commutator identity, not an extrapolation of word evaluations. Only
eight prefixes of length2d activate the gate.

More generally, start with any gate T_(p,f) that flips bit p by an
arbitrary function of its lower p bits. After
d>=max(2,floor(p/2)+1) of the same balanced steps, the entire action is
identity if f(0)=0, and otherwise the canonical gate at bit P=p+2d:
zeros through bit P-5, followed by an equal pair. This convergence bound
is sharp for p>=3. The proof retains the complete product of inverse-time
guards; its vertical zero column forces the whole lower-p prefix to
vanish. Evaluation of the initial guard at zero is charged. Afterward,
the zero-input marked query needs only binary index arithmetic.

The literal word has length (7*4^d-4)/3 in A,A^-1,tau_0. Its normal
form instead tests a supplied guard in O(d) Boolean work. On zero input,
the marked query is simply bit_k(E_d(0))=1[k=2d], requiring only
O(log(d+2)+log(k+2)) bit work, with d and k supplied in binary.

Conjugation retains the unresolved computation exactly:

```
(A^j E_d A^-j)(0)=4^d A^j(1),
bit_(j+2d)((A^j E_d A^-j)(0))=c_j.
```

Thus this simplification alone does not reduce the singleton index j.
Nor may adjacent cancellation be used for arbitrary residual pairs.
Although every A-conjugate of E_d for d>=3 fixes odd inputs, putting
F_i=A^i E_2 A^-i gives `[F_3,F_1](A^8(1))=102465` instead of102849,
changing the actual center bit8. The saved actual row, an exact support
bound, and an independent Mealy checker certify this complete-output
control. No occurrence of that particular residual uncancelled in the
actual norm is asserted.

The same report also tests residuals that do occur in a specified
six-swap even/odd collection of P_8. Omitting either of two nonadjacent
corrections while retaining the others changes the actual n=14 marked
answer. A different correction can be pruned: its discrepancy disappears
after five H steps, with an exact local-cone proof for every common
higher tail. Thus ordered collection admits some guarded erasures and
requires other corrections even in this one actual product. The
independent [collection verifier](../../experiments/rule30/p3_dyadic_norm_collection.py)
retains both outcomes. A costed collection rule for the whole ordered
norm remains missing.

The [parallel-pair extension](RESULTS-p3-parallel-defect-pair.md) supplies
a larger closed family. A gate toggling bits p,p+1 by two functions of
the lower p bits remains such a parallel pair after the commutator,
shifted to p+2,p+3. Its exact two-coefficient update is proved on all
inputs. Through d iterations, a single shared inverse orbit replaces
the exponential recursive evaluation tree by d+1 paid original-guard
calls and d(d+1)/2 local pair updates, with inverse passes, bit access,
and output costs retained.

At zero input the coefficients obey `(a,b)->(a,b*(1+a))`, an idempotent
update. Every positive depth therefore has a direct marked query after
one paid initial-guard evaluation and binary index comparisons. This
works without a proof that the complete two-gate action collapses to a
single gate. The report retains explicit depth-three and depth-four
controls where the second gate is still needed. This is a costed
evaluator for that expression family; no collection of the entire
actual norm into the family has been established. Adjacency matters:
starting instead with G(x)=x XOR5 gives a first commutator K with
K(0)=28 and K(28)=16. Its complete five-bit action is not an involution,
so it cannot be represented by the same parallel independent-flip rule.

## 5d. Actual block pruning needs a guard, and the guard has a compact action

All maps in this subsection use the original binary coordinates.

The [actual block-pruning audit](RESULTS-p3-actual-norm-block-pruning.md)
tests deleting the whole left factor in
P_(2m)=P_m Ad_A^m(P_m). At N=8 this replaces B^8(0)=25712 by
A^4 B^4(0)=25636 and changes both actual marked answers, c13 and c14.
The discrepancy is permanent: after a finite transient the two complete
H orbits stay two phases apart on a proved four-cycle. Their highest
disagreement has a common zero immediately above it at every time, so
the required reset never occurs. This is an exact all-future obstruction
for the specified deletion, not a claim about all decompositions.

There is a positive conditional block rule. If the supplied initial bits
w through2w-1 alternate1,0,1,0,..., then H^w forgets all2^w possible
lower prefixes, with every higher tail unrestricted. Put z=x>>2w.
The complete remaining action is B^w(z) when z mod2=w mod2, and C^w(z)
otherwise. An induction carries the actual alternating guard through
each H step and retains the new tail's B or C action.

For the two marked output bits even those powers need not be evaluated.
Writing a=bit0(z), b=bit1(z), q=w mod2, r=floor(w/2) mod2 gives

```
bit0 H^w(x)=a XOR q,
bit1 H^w(x)=b XOR q XOR (r AND (1 XOR a XOR q)).
```

The [guarded evaluator](../../experiments/rule30/p3_prefix_synchronization.py)
reads the w supplied guard bits and those two tail bits, then uses this
formula without any temporal expansion. Obtaining or verifying that
length-w guard from an implicit input remains charged.

The [actual applicability theorem](RESULTS-p3-actual-alternating-guard.md)
now closes the proposed use on the whole observer: the guard holds only
at center times4 and6. For every N>=2, two fixed edge coordinates of
B^N(0) both equal N mod2, as certified by
32->56->50->55->50 and64->112->100->111->100 under H.
The full guard requires the opposite parity at edge6 for even queries
N>=6, and at edge5 for odd queries N>=4. The remaining even N=5 case
also fails. Thus this particular whole-query shortcut is unavailable
asymptotically; shorter guarded blocks and other patterns have not been
classified by this result.

The audit also retains the total-time accounting. Deleting P_m from
P_N gives A^m B^(N-m)(0), whose marked observation is still a query at
the original final time after an explicit two-bit modification of an
earlier singleton row. A smaller source exponent by itself therefore
does not supply a faster recurrence for the center bit.

## 6. The inverse-prefix obstacle cancels on the actual query

The 2026-09-14 continuation identifies the prefix recurrence as an
existing part of the automaton itself. For input digits z_j=p_j+2q_j,
the observer

```
a_j=q_j XOR(a_(j-1) OR p_j),  a_(-1)=0
```

is exactly the high bit of the next B output at position j. It need
not be computed by scanning an already constructed B orbit: when the
input is B^L(0), its requested value is simply a high-bit query on
B^(L+1)(0). The [observer report](RESULTS-p3-gamma-observer-grammar.md)
proves this for every supplied input stream, and separately implements
an optional aggregate on repetition grammars with construction charged.
Its three-state aggregate profile is not closed under another action;
the report retains an exact even-input witness and does not assert that
that witness is an actual seed point.

There is a compatible local transport

```
J(z)_j=high(z_j)+2*(low(z_(j+1)) XOR1[z_j!=0]).
```

The [transport report](RESULTS-p3-local-branch-transport.md) proves that
J is the itinerary conjugate of deleting one original binary bit.
On the even component, `Gamma^(-1)=J B`; therefore

| First return | Exact output on zero |
|---|---|
| `(CA)^k` | `J(B^(2k+1)(0))` |
| `(CB)^k` | `4*J(B^(2k+1)(0))` |
| `(BC)^k` | `B^(2k)(0)` |
| `(AC)^k` | `J(B^(2k)(0))` |

These formulas hold for every k>=0, including their origin conditions.
The changed B exponents and any adjacent digit requests remain charged.
The correct shift identity is `J^2 g=sigma` for each generator g;
`J^2=sigma` is false and is not used as a shortcut.

Most directly, the [actual B-query report](RESULTS-p3-actual-b-query.md)
proves, for h>=1 and e in{0,1},

```
c_(2h+e)=bit_e(digit_(h-1)(B^(h+1+e)(0))),
c_0=c_1=1.
```

Both center parities are single-digit readouts. The proof uses exact
boundary identities for F(x)=2x+(x mod2): `C_0 F=F B_0` and
`H F=R B_0`, where R deletes one original bit. It then transports the
actual seed orbit through Phi. No hypothetical independence or extension
to a fresh orbit replaces those boundaries.

The new implementation constructs the initial B power directly and
uses h-1 zero sections. Its n=17 control uses7 advances and30 nodes,
compared with8 and32 for the previous power-node C query. At n=32 it
uses15 advances and94 nodes, compared with15 and92. All seven controls
agree with independent row evolution. These are finite implementation
comparisons, not a scaling law. The substantive removal is the extra
observer in the same-time B reconstruction route; the earlier C query
already had a direct readout.

There is also an all-length boundary on one proposed closure mechanism.
The [autonomous-profile theorem](RESULTS-p3-autonomous-profile-bound.md)
proves that B's actual zero-orbit period P_m modulo4^m satisfies
`P_m>=m+1`. Exact autonomous temporal summaries that recover the last
digit at every depth j<=m, for every time, must have at least P_m states
at some such depth. Thus a uniformly bounded finite profile cannot close
this entire iteration problem. This counts possible temporal states,
not computational steps or spatial-transducer memory, and does not
exclude growing descriptions or algorithms restricted to the actual
coupled singleton queries.

## 7. An exact dyadic step, with its complementary field retained

The [two-channel blocking report](RESULTS-p3-b-two-channel-block.md)
defines a bijective split S of consecutive itinerary digits:

```
P_j=high(z_(2j))+2*low(z_(2j+1)),
Q_j=low(z_(2j))+2*high(z_(2j+1)).
```

The conjugate F=S B^2 S^(-1) is an explicit transducer with eight
reachable chronological carriers and sixteen input symbols. Its complete
128-edge table closes on those carriers. For N=2L+r, r in{0,1},

```
S(B^N(0))=F^L(I_r),
I_0=(0^infinity,0^infinity), I_1=(2^infinity,1^infinity).
```

The second seed follows from B(0)=1^infinity. It is not an independently
chosen boundary. A fine bit e at digit 2j+d becomes bit d of Q_j if
d=e, and bit d of P_j otherwise. This halves the time exponent and
spatial query index in a single exact step, without an extra prefix
observer. The rule acts on both fields; neither field is supplied for
free.

The local primary output ignores the current high bit of Q, but that
bit can change the next carrier and hence the next primary output.
A two-block witness disproves the all-input factor that simply deletes
that bit. Actual seed rays also rule out an autonomous Q evolution or
an unphased finite-window recovery of Q from P. For example,

```
B^8(0)=003(0332)^infinity,
P(B^8(0))=0(13)^infinity,
B^4(0)=(03)^infinity.
```

Their discrepancy continues throughout the tail, rather than stopping
in an origin strip. These are complete closed spatial-orbit certificates,
not extrapolations from matching prefixes. They leave a phase-aware or
otherwise structured complementary field open.

The [temporal-squaring report](RESULTS-p3-bitplane-temporal-squaring.md)
also gives a one-pass B^2 scan with a two-digit output memory and a
separate, exact origin rule. A proposed next square that skips the
intervening digits has a nonzero periodic error on the same actual
B^8 ray. Its triangular coefficient composition retains a cross term
evaluated on the transformed preceding history. A shared formal
expression for that history is not yet a cheap evaluation of it.

The [all-length cocycle calculation](RESULTS-p3-nilpotent-history-cocycle.md)
makes that correction explicit. Under inverse iteration L=B^(-1), let
p_t,q_t be the current digit's bits and v_t the high bit of its preceding
digit at matching time t. Then, over F2,

```
q_N=q_0+p_0+p_N+sum_(t<N)p_t+sum_(t<N)v_t*p_t.
```

This telescopes an ordered double sum to one neighboring-history
correlation. Squaring the block retains the same transformed middle
prefix for every coefficient and entering-digit probe. The implemented
shared evaluator uses N*m digit updates and (N-1)*m signature
compositions on a nonempty supplied m-digit prefix. Its O(N*m) cost
is explicit: the correlation has not been made free by writing a
logarithmic-depth formula.

The [Gamma-power calculation](RESULTS-p3-gamma-power-returns.md) gives a
different exact way to organize embeddings. In itinerary coordinates,

```
Gamma^(2r)(z)=4^r A^(-r)(z), r>=0.
```

The inverse action and acquisition of its queried digits remain charged.
The proposed sparse return family consisting of chronological word
`C A^(2^k-1)` is false at k=2, even for the actual marked observable.
Its embedded original value is52, whereas B0^4(0)=100. Their second H
iterates have different low bits, giving the wrong center bit at n=6.
The correct second embedded return is a conjugate of BCCA, so it does
not remove the existing ordered-return problem.

### The staggered factorization keeps one field affine

The [staggered-field report](RESULTS-p3-staggered-affine-field.md)
factors one B action into two invertible field updates:

```
(P,Q) -> (R,V)=(M_Q(P),N_R(Q)).
```

For fixed R, N_R is affine in the entire Q field and has a local inverse.
Write R_j=a+2b, Q_j=q0+2q1, and let c be the previous R high bit and h
the previous V high bit. The exact scan is

```
Vlow=q0 XOR(c OR h),
Vhigh=q1 XOR[a OR(b XOR Vlow)],
c_next=b, h_next=Vhigh.
```

The actual boundary is (c,h)=(1,0). In F2 the carry has the form

```
h_next=(1+c)(1+a)h + q1+a+(1+a)(b+q0+c).
```

This proves affineness by induction without declaring the coefficients
free to construct. Conversely, supplied R and V recover Q from their
current and immediately preceding digits. The complementary map M_Q
is invertible but need not be affine, even when Q is identically zero.

Staggering the fields preserves the actual evolution and removes the
need to choose separate time-parity seeds:

```
T(Y)=(Q(Y),P(BY)),
T(BY)=(N_R(U),M_(N_R(U))(R)) when T(Y)=(U,R),
T(0)=(0^infinity,2^infinity).
```

The report derives all four center-index residues from this fixed seed.
Two staggered steps still mean two B actions. For a supplied grammar
of aligned pairs (Q_j,R_j), an N pass needs at most four boundary
contexts per input node and at most 36s+1 output nodes for s input
nodes. Concatenations and repeats retain the actual seam state.
Alignment, grammar construction, and integer arithmetic remain charged;
this bound does not control repeated M/N evolution.

A closed scan of the already certified B8 ray also gives the complete
actual ray B9(0)=1100102(3013)^infinity and P(B9(0))=200(32)^infinity.
Thus odd B powers do not have an all-spatial prohibition on consecutive
zero R digits. This witness does not disprove a maximum-two-block reset
gap. Neither such a gap theorem nor a cheap construction of the actual
coefficient fields has been established.

The [two-affine-scan report](RESULTS-p3-two-affine-scans.md) makes an
important qualification explicit: the nonaffinity of M_Q is specific to
that choice of fields. The already saved fine-bitplane equations allow
both halves to be conditionally affine. For input D+2H and output P+2Q,
first scan

```
Q_i=H_i+D_i+(1+D_i)Q_(i-1), Q_-1=0,
```

then scan

```
P_i=D_i+Q_(i-1)+(1+Q_(i-1))P_(i-1), P_-1=1.
```

Each map is affine in the field being updated when its controlling field
is fixed, and each has a local inverse. The report also gives an exact
opposite-order factorization in the pointwise Gray basis U=D, Z=H+D,
with the distinct scan boundaries retained. It starts from U=Z=0 and
decodes every requested bit locally. This removes any need for a prefix
observer in that representation; it does not remove the feedback between
the fields. The complete map is nonaffine even on two fine digits.
These statements follow from the existing local equations and refine
their interpretation. Explicit evolution still uses O(Nm) Boolean work
for N passes of m digits. No cheaper construction of the actual ordered
control history follows from conditional affinity alone.

### Two-time high queries use a last rise and a range parity

The [two-time rise-reset report](RESULTS-p3-two-time-rise-reset.md)
proves a cancellation within the actual two-step composition. For old
bitplanes D,H, let Z=D+H, A=low(BY), and q=high(B²Y). Mark the rising
edges of A with rho_0=A_0 and rho_i=A_i(1+A_(i-1)) for i>=1. With
q_-1=Z_-1=0, the exact high-field scan is

```
q_i=Z_i+(1+rho_i)q_(i-1)+rho_i(1+Z_(i-1)).
```

The proof multiplies the two complementary weighted-shift factors and
uses the fact that rho has no consecutive ones. A rise resets the carry;
therefore, after the last rise k<=i, q_i is 1 plus the parity of Z from
max(0,k-1) through i. With no rise it is the prefix parity of Z.
The zero padding in rho is distinct from B's scan boundary A_-1=1.

The corresponding C² identity retains two origin corrections. It starts
with q_0=H_0 and q_1=Z_1+H_0, then uses the same scan from site2 onward.
Its last-rise query searches only positions k>=2; absent such a rise,
the answer is H_0 plus the parity of Z from1 through i.

Both center parities can use these high-only queries:

| Requested bit | Actual old input Y | Actual intermediate low field A | Position |
|---|---|---|---|
| c_(2h) | C^(h-1)(0) | low(C^h(0)) | h-1 |
| c_(2h+1) | B^h(0) | low(B^(h+1)(0)) | h-1 |

Here h>=1; c_0=c_1=1 are separate. The even case's initial high carry is
(h-1) mod2. The derivation uses the established actual B/C center
identities, so it does not require a final low-field observer.

This reduces the final high query to an actual last rise and a parity
range, but does not construct those quantities cheaply across many time
steps. Nor does it close the full continuation on rising edges alone:
when Z=0 and A_0=1, the next high field is constant1 while the next Gray
field equals the complete A. This occurs at actual zero-orbit times0
and4. The old one-pass B² kernel already costs O(m) on a supplied
m-digit prefix; the new cancellation is not an asymptotic improvement
over it. No shrinking total-work recurrence has been established.

## 7a. A local correction for exact two-column Cartier reduction

The [parity-string Cartier report](RESULTS-p3-parity-string-cartier.md)
now eliminates the intervening odd-time state from the local correction
formula. Write a digit's low and high bits in that order. At an even time,
let (p,q) and (a,b) be two adjacent updated digits, and put c=p OR q.
All arithmetic in the following formulas is over F2:

```
g=c*(1+b+a*q),
f=c+a*(1+q),
E=a*b+c*(a OR b)+a*q.
```

If the next digit was (A,B) two time steps earlier, its updated value is

```
A'=A+g,
B'=B+E+g+f*(A+g).
```

These are exact local formulas, including the transported column seam.
The report proves the positive-time prefix-sum identity underlying them
and keeps the origin separately. Their combined physical action agrees
with the already proved B^2 scan; it is not a separate faster algorithm.
A supplied even-time row suffices for
each local correction; no separate odd-time carry is needed. Constructing
that row and summing E are still algorithmic obligations. In particular,
this two-column formula does not on its own halve the spatial query
index or prove closure under arbitrarily many doublings.

Two actual-orbit controls specify what cannot be discarded. In the saved
32-step three-digit cycle, the lifted first-column carry and the next
column's two cumulative linear fields return to zero, while the XOR of E
is1. An independent four-digit calculation gives B^32(0)=0002 modulo4^4.
Thus E is not a difference of endpoint potentials on those retained
states, even with time phase modulo32. This cycle is outside the marked
center-query diagonal; a cancellation restricted to that diagonal is
not refuted. The cycle itself is periodic, so its nonzero correction
also does not establish costly evaluation.

Nor does the finite set of local actions automatically close as a new
coarse alphabet. At actual times2 and4, the first two digits are22 and03;
both give (g,f,E)=(0,1,1). After two more updates their pairs are03 and23,
which give different signatures. A phase-aware or richer representation
remains possible. The exact verifier checks the complete local table,
the transported physical readout, and these bounded actual witnesses.

The [four-period central-carry calculation](RESULTS-p3-four-period-central-carry.md)
provides a positive reduction when the upstream history has a certified
even period P and its one-period action on the next digit is a four-cycle.
Across four driver periods, the second downstream column's cumulative
linear coordinates return, and its central increment can be computed
from a single upstream period. Both the local correction and the ordered
interaction between periods are included. No downstream history needs
to be constructed for this full-cycle observable.

The required counters admit fixed-size affine updates, so a supplied
concatenation/repetition grammar can also be aggregated by exact
composition and powering. For these counter actions, every even-length
word has order dividing4; every odd-length word, including its phase
change, has order dividing8. The proof separates translated base counters
from upper counters depending linearly on them. Repeat annotations can
therefore reduce their exponents modulo4 or8. These are identities of
the counter annotation, not of B or of the physical driver history.
This closes evaluation of that supplied
history, not construction of the histories needed at further spatial
depths. The annotation itself cannot support a homogeneous next-column
update: the actual length32 words at columns0 and1 have identical
complete annotation maps, yet their next-column words have different
annotations. Length, phase, and entering digit are equal in this witness.
Richer or column-dependent profiles remain possible.
The theorem requires the periodicity and four-cycle premises;
it is not an evaluation formula for an arbitrary partial period or the
general marked diagonal. The actual control with P=8 predicts the same
nonzero 32-step return above.

## 7b. Incoming-digit profiles and the limit of finite group annotations

The [Heisenberg profile calculation](RESULTS-p3-heisenberg-column-profiles.md)
compresses the complete counter action to eight group coordinates and
length modulo4. The first three coordinates already recover the
incoming-digit endpoint permutation. Retaining the input annotation and
all four transduced annotations therefore gives an exact42-bit profile.
Concatenation routes each second-word input through the actual first-word
endpoint. Both time phases and the ordered central products are retained.
This is an implemented compression of the whole action, not an inference
from matching zero-state outputs alone.

The repair still does not close under another column update. At length32,
the actual virtual word1^32 and its first physical output(1230)^8 have
identical complete profiles. Their next-column profiles differ. All four
incoming digits, both phases, and the common length are included in this
check; the source reuses the saved actual orbit.

There is also an all-length obstruction covering every fixed finite-group
annotation of this form. Suppose word aggregation is a homomorphism into
a fixed finite group of exponent m, and a homogeneous spatial update and
endpoint decoder recover all actual columns at length N. Those two maps
may depend on N. At N=4m, the virtual word1^N and its first output(1230)^m
both annotate to the identity. The spatial update must then fix that
identity at every later column, and the endpoint decoder must give0
everywhere. This contradicts B^N(0) being a nonzero ray, which follows
from positivity of B0^N(0) and the exact itinerary bijection.

This rules out the stated fixed-group homogeneous construction, including
every fixed incoming-profile depth. It does not exclude growing groups,
nonhomomorphic annotations, position-dependent updates, or a method
restricted to the marked diagonal. A full depth-k profile tree has
8*(1+4+...+4^k)+2 bits before sharing; an exact column step selects its
incoming-0 subtree and consumes one level. Constructing and evaluating a
suitable unbounded representation with sublinear total work remains open.

## 7c. Integer occupation counts and the ordered prefix-action series

The [prefix-action series investigation](RESULTS-p3-prefix-occupation-series.md)
tests a representation that retains unbounded integer data. For a supplied
temporal word w, let R_t be its complete incoming-digit permutation after
t letters. The polynomial

```
A_w(z)=sum_(t=1..|w|) z^(t-1) R_t
```

retains every ordered prefix action. It composes by
`A_uv=A_u+z^|u| A_v R_|u|`. The actual next-column letter selectors are
matrix entries of this polynomial. Their prefix products satisfy a unique
linear equation using coefficientwise products. An exact Cartier step
pairs consecutive letters in their chronological order and stays within
the eight-element D8 permutation alphabet. These are supplied-series
operations; constructing successive spatial columns is still required.

Setting z=1 gives complete integer occupation counts, but loses necessary
order even after retaining the final permutation and length. The saved
actual words1^32 and(12130300)^4 have the same occupation matrix and endpoint.
Their next-column words have different endpoint permutations. Thus merely
lifting the old counters from bits to integer occupation counts does not
close the update. The full polynomial distinguishes these words.

The maintained coefficient-query routine charges its input access: for an
ordinary coefficient oracle, halving the prefix index still visits all
N driver positions. A separately supplied periodic driver supports a fast
large-index query after its period is read and composed. Neither operation
constructs the required actual driver for free. Replacing coefficientwise
multiplication by ordinary series multiplication is already wrong on the
actual virtual prefix11; no ordinary rational inverse solves that equation.

## 7d. A local braid completion fails; endpoint interchange retains a defect

The [braid audit](RESULTS-p3-braid-interchange-audit.md) proves that no
Yang–Baxter map on any hidden set, even an infinite one, can have
M_a(b) as its first visible output for every pair under a surjective
pointwise projection. The first coordinate of the braid equation at
visible pair(0,1) would require an identity action among M_0,...,M_3,
and none exists. This precise hypothesis leaves blocked, restricted-context
and parameter-dependent constructions open.

The genuine D8 Hurwitz interchange does preserve a temporal endpoint.
On the first actual driver pair(1,2), however, it changes the intermediate
output1 to3. In the next spatial column that becomes a high-bit flip at
every later time, not a disappearing boundary error. No invertible
boundary change independent of the current driver can carry this flip
through another column: M_2=M_3 would force M_0=M_1. The exact controls
read the existing actual-column artifact. Neither endpoint interchange
nor these model exclusions give a faster marked query.

## 8. Scope of a proposed multiplicative transport shortcut

An independent route sought a product that transports through each
local tile and can be powered without expanding the digit word. For
the specified homogeneous equation

```
L_g M_d=M_e L_psi(e), e=P_g(d),
```

the [group classification](RESULTS-p3-multiplicative-transport.md)
forces all four M_d equal when all seven symbols are invertible. The
[finite-dimensional extension](RESULTS-p3-finite-dimensional-transport.md)
allows arbitrary singular D-dimensional digit matrices while retaining
invertible L_g. A common-row-space reduction proves that every product
then depends only on length and its first at most D-1 digits. This is
an induction over every dimension and field, not a finite matrix search.

The [rank-one extension](RESULTS-p3-rank-one-transport.md) permits singular
state transports under an explicit nonannihilation premise. Products
either vanish after two digits or retain only their first digit and
length. Its Boolean version is proved separately.

These theorems exclude the stated product-only encoding. They do not
exclude arbitrary tensor networks, position-dependent local laws,
growing or implicit dimensions, singular transports selecting a proven
reachable language, or a decoder supplied additional time information.
Matrix dimension is not a runtime lower bound. In particular these
classifications do not resolve P3.

A different algebraic proposal also has a complete local test. The
[holographic compatibility report](RESULTS-p3-holographic-local-compatibility.md)
classifies even four independent invertible complex binary bases making
an uncontracted four-leg equality tensor a matchgate signature. Each
edge basis must be Hadamard with nonzero diagonal row and column factors.
Under the dual bases, Rule30's gate fails the necessary support parity:
its support contains0000 but not its complement1111. The argument applies
when all four gate edges meet uncontracted four-leg equality tensors.
The proof includes zero-entry bases; its exact verifier uses rational
and cyclotomic arithmetic. This rejects independent bases on that
unblocked network, not contracted boundaries, blocked gadgets, or
arbitrary Pfaffian algorithms. A Rule90 control shows explicitly that
failure of this representation does not establish computational hardness.
The equality classification extends to every arity at least3. Since
both constant Rule30 inputs produce0 after any positive number of
updates, the same obstruction survives every finite uniform temporal
blocking depth in the full coarse bulk. It does not cover blocking a
whole finite query until no full interior gate remains.
Even a successful local construction would still need a sublinear bound
for the charged network construction and marked-query evaluation.

## 8a. A genuine truncated trajectory does not acquire Newton doubling

The [prefix-Newton theorem](RESULTS-p3-prefix-newton-tail.md) gives an exact
formula for a natural proposed algebraic acceleration. In moving polynomial
coordinates let r_t be the true row, L=1+X+X^2, and retain only the first
m rows in P_m. For every m>=1, its exact global Newton update is

```
Newton(P_m)=P_m+T^m r_m/(1+T L).
```

The correction begins at time m, so its coefficientwise products with the
earlier reference vanish. Newton therefore appends r_m correctly and then
evolves it by the additive rule L. Its first incorrect full row is exactly
m+1: the difference has coefficient1 at X^(2m+1), since the two highest
bits of every positive-time true row are11. This is an all-length statement
about genuine singleton truncations, independently checked against a
physical-coordinate truth-table Newton solve.

The exhibited error is away from the center in general. The theorem does
not bound center-only convergence or the particular repeated Newton
iterates in the older experiment. It rules out the claimed full-row
precision doubling from a correct truncated prefix, while leaving other
preconditioners and an actual finite algebraic-series certificate open.

## 8b. Actual Newton convergence and the limit of an algebraic compiler

The [Newton error-wedge theorem](RESULTS-p3-newton-error-wedge.md) concerns
the successive approximations initialized from the singleton alone. After
k complete rounds their error at time t, in moving index j, satisfies

```
support(error at round k, time t) is contained in [2k,2t-k].
```

The exact error equation has a linear part shifting by0,1,2 and an adjacent
old-error product. The product removes two possible error columns at one
edge and one at the other; a double induction proves the displayed interval.
Consequently every center bit at time n<2k is correct, and a complete row
is correct when2n<3k. The implemented sufficient center schedule is
floor(n/2)+1 rounds, with n=0 handled directly. These are upper bounds on
rounds sufficient, not lower bounds on rounds necessary. The materialized
implementation still costs O(n^3) scalar work, so this convergence theorem
does not accelerate the query beyond direct simulation.

A possible way to avoid materialization was to compile each linearized solve
from an automatic or algebraic reference. The
[automatic-reference counterexample](RESULTS-p3-automatic-reference-newton.md)
rules out that general closure claim even with the correct singleton and
the finite light cone. Its reference is the full interval0 through2t,
except for zero rows at positive powers of2. Both a digit automaton and an
explicit algebraic series describe it. The unique Newton solution remains
inside the cone but has a nonautomatic, nonalgebraic spacetime series.

The proof retains the high boundary exactly. On times2^m+1, an adjusted
solution row F_m has lowest nonzero coefficient at index6 and obeys
F_(m+1)=L F_m up to errors whose lowest index grows exponentially in m,
where L=1+X+X^2. A finite digit automaton would impose one eventual period
P in m at every fixed spatial precision. This conflicts with the nonzero
lowest coefficient of (L^P+1)F_m. The contradiction uses no fitted kernel
or finite state-count extrapolation.

This reference is prescribed, not an actual Newton iterate. In particular,
the first actual reference has the more specific rational series
1/(1+T L). Its next solve might admit special structure excluded from the
generic argument; no finite Cartier certificate was found for it here.
Nonautomaticity of a full spacetime array also does not give a lower bound
for arbitrary coefficient algorithms or for its center diagonal.

The [left-edge cancellation](RESULTS-p3-newton-left-edge-gain.md) strengthens
the actual error interval to [2k,2t-k-1] for every k>=3. Two specified
adjacent round-2 errors have disjoint period-four phases; their product is
identically zero, so the next round removes one additional edge column.
The existing support induction preserves that gain at all subsequent
rounds. This improves some sufficient whole-row schedules; the sufficient
center schedule is unchanged.

## 8c. Constructed periods for actual Newton strips

The [strip Floquet theorem](RESULTS-p3-newton-strip-floquet.md) gives an
exact distant-time evaluator for the actual initialized approximations.
At spatial precision j+1, let Q(j) be the least power of2 at least j+1.
The kth round has a pure temporal period dividing

```
P_1(j)=Q(j), P_k(0)=1,
P_k(j)=Q(j) P_(k-1)(j-1) for k>=2,j>=1.
```

The forcing term is folded into the constant coefficient v_0=1. The
resulting lower unitriangular matrix needs only the previous round's
coefficients through j-1. Over one constructed reference period its
monodromy U satisfies U^Q(j)=I. The evaluator generates that full reference
period from the singleton, then applies powers of U and the ordered
remainder phase. Its total work is polynomial in j and log(t+1) for each
fixed round k. No later reference, orbit table or free preprocessing is
assumed; independent scalar controls include very large binary timestamps.

This is a true bulk evaluation for a fixed strip, but j=n for a center
query and the sufficient round count grows with n. The theorem therefore
does not meet the sublinear P3 work requirement. Nor does a polynomial
period bound for each fixed round prove a finite digit automaton for the
joint unbounded time and space indices.

The [autonomous triangular-CA counterexample](RESULTS-p3-triangular-ca-automaticity.md)
shows that even a fixed two-layer affine system with an additive bottom
layer and a finite seed need not have automatic spacetime. A single
particle moves between a stationary marker and a marker moving at speed1;
its speed2 reflections give successive origin times T'=3T+2, hence
T_k=3^k-1. The accepted binary word lengths have irrational density, which
is impossible for a regular language. This is an all-length elementary
proof, with an independent local routing checker.

This example is not Rule30 or a Newton iterate. It excludes automaticity
from the general triangular architecture alone, leaving the special
reference L^t unresolved. It also has an O(log^2(t+2))-bit-work origin
query: test whether t+1 is a power of3. Thus the same example explicitly
separates failure of finite digit-automaton methods from query hardness.

## 8d. Fibonacci interpolation does not leave the center's initial data

The [new primary-source audit](RESULTS-p3-fibonacci-interpolation-audit.md)
checks the notebook's integer lift and its exact Lagrange weights. For a
fixed right-edge column k, the lift has degree F_(k+2)-1, so its first
F_(k+2) samples determine later values. At the center k=t, however,
F_(t+2)>t for every t. The requested sample is always inside that initial
list. Thus this particular interpolation does not reduce any center
query, even before its construction cost is considered.

The exponentially large integer degree is not a computational lower
bound either. In the support-set recurrence, OR cannot decrease either
operand's index and increment raises it. Discarding support indices above
n at every stage therefore preserves c(n) exactly. An explicit paid
implementation takes n-1 support advances, with polynomial table work;
the existing subset-zeta conjugacy gives the ordinary rotated evolution.
Filtering those intermediate rows to final Lucas submasks is instead
unsound: the exact n=4 carry witness loses the true answer1. The report
retains an independent four-step verifier and distinguishes Boolean table
operations from total bit work.

Fomin's [current support-wave release, v6](https://zenodo.org/records/22646809)
(2026-09-07) uses the same center formula. Its fixed moving-front automaton
does not supply the required interior support memberships, and its supplied
window evaluator still advances one support row at a time. This review
does not turn the absence of repeated window states into a lower bound on
compressed or query-specific algorithms. No sublinear construction follows
from either reviewed formula.

## 9. Precise outcome

There are now exact algorithms for the coupled quaternary query,
finite-core powering, and weighted section aggregation, together with
explicit failures of the proposed shortcuts. The universal identities
and period bounds do not establish improved asymptotic singleton-query
time or a lower bound for general P3 algorithms.

The remaining issue is to evaluate the specified B-power digit at
sublinear total cost. Its readout requires no independent inverse-prefix
observer. Dyadic blocking halves the two indices, but a uniform bound
on the construction and evaluation of the resulting coupled rules is
missing. The staggered factorization supplies a compiler for supplied
paired grammars. A fine-bitplane or local Gray representation makes both
half-updates conditionally affine, but their changing control fields and
any required alignment still have to be constructed. Two-time cancellation
further reduces both center parities to a high-only last-rise/range-parity
query. Constructing its actual control and parity data at sublinear total
cost remains open. In the separate
section representation, B's first return is
BCCA: dividing the exponent by4 expands that return word to four letters.
Neither identity alone gives a shrinking-cost recursion. The two wrong
center bits above remain controls for a proposed period-based shortcut.
The Gamma candidate adds a third, independently checked wrong marked bit.
The Cartier formula identifies a local correction that can be evaluated
without an odd-time observer, but no sublinear method for its required
accumulated value has been established. Returning the compressed endpoint
state is insufficient to infer that this accumulated value vanishes.
No P1 or P2 exclusion follows.

The linked reports retain exact verifiers and saved artifacts.
The universal conclusions use induction, temporal-column reconstruction,
or complete local truth tables; bounded orbit controls are labeled as
such. No paid compute, GPU, long singleton prefix, or old frontier census
was used.

# Exact R1 countermodel predicate for automatic diagrams

Date: 2026-09-09. **Reduction and construction machinery; R1 remains open.**

Within the chosen automatic-diagram ansatz, the centre's eventual period
and onset can both remain unspecified. The same finite endpoint relation
used to certify an aperiodic neighbour also decides eventual periodicity
of the centre. This removes the earlier prescribed-centre-clock restriction.

## 1. Model and uniform reduction (`U/R`)

Let a two-dimensional radix-`b` MSB core define

```text
U(t,x) = g[t mod T, x mod q, state(t,x)],
T=b^a, a>=1.
```

Its initial state has a paired-zero self-loop. Here `T` is a **lookup
modulus**, not an assumed temporal period of column zero. Let `R` be the
number of core states reachable using time-axis symbols `(digit,0)`.
For a time-axis state `s`, let `Q(n)` be the state after reading `n`.

For each residue `p<T`, append the `a` paired low digits of `(p,0)` or
`(p,1)`. This defines two binary output functions on the same `R` states:

```text
C_p(Q(n)) = U(Tn+p,0),
V_p(Q(n)) = U(Tn+p,1).
```

The zero-set mask is the third output function

```text
M_p(s) = (1-C_p(s))*V_p(s).
```

No product automaton is needed for `M`: all three outputs label the same
time-axis core. Put

```text
H=b^R,
P=b^R lcm(1,...,R),
E={(Q(n),Q(n+P)): n>=H}.
```

The [arbitrary-radix period lemma](RESULTS-r1-radix-automatic-period-bound.md)
and the exact addition product give the following equivalence:

**The centre is eventually periodic and its zero-set neighbour is not
eventually periodic if and only if both conditions hold:**

1. For every phase `p` and every `(s,t)` in `E`, `C_p(s)=C_p(t)`.
2. For some phase `p` and some `(s,t)` in `E`, both centre labels are zero
   and `V_p(s) != V_p(t)`.

*Proof.* A sequence is eventually periodic if and only if each of its
finitely many residue subsequences is. Apply the period lemma separately
to the centre output functions `C_p`. It gives exactly condition 1.
Apply it to the mask functions `M_p`. The mask is aperiodic exactly when
one endpoint pair has unequal mask labels. Under condition 1, those mask
labels differ exactly when their common centre label is zero and their
neighbour labels differ, which is condition 2. For an eventually periodic
centre, eventual periodicity of the mask is equivalent to eventual
periodicity of the neighbour on the centre's zero set. One can take a
common multiple of the centre and mask periods to see this directly. QED.

The centre certificate consequently has safe onset `T*H` and a period
dividing `T*P`. These are consequences of the model and finite predicate;
neither is imposed as a guessed onset or claimed to be minimal.

For the ternary three-state model with lookup modulus three, the safe
bounds are onset 81 and period 486. For the binary five-state model with
lookup modulus four, they are onset 128 and period 7,680. Smaller reachable
axis cores have their own smaller bounds.

## 2. Exact shared Boolean encoding (`U/C`)

Only the final low spatial digit of `x=1` is nonzero. Fold the upper `a-1`
low time digits through a fixed axis table. Retain the last step using two
globally composed Boolean values at a pre-final core state `s`:

```text
C[p,s] = g[p,0,delta(s,b*(p mod b))],
V[p,s] = g[p,1 mod q,delta(s,b*(p mod b)+1)].
```

One-hot transition selectors encode both identities exactly. A shared
selector for `(p,s,t)` may be true only when

```text
C[p,s]=C[p,t]=0 and V[p,s] != V[p,t].
```

Conditional on the fixed axis table, impose centre equality for every
folded endpoint pair and require at least one of its eligible selectors.
For a nonmatching axis, its guard releases these constraints. Both the
centre equalities and the eligible-selector disjunction may use a spanning
forest of each phase's undirected endpoint graph. Equality on the forest
is equivalent to equality on all edges, making the centre label constant
on each component. On a component with centre label zero, the neighbour
labels differ on some original edge if and only if they differ on some
forest edge: either condition says they are nonconstant on that component.
Thus the replacement preserves the full predicate and uses at most `R-1`
pairs per phase.

Together with complete axis coverage, these clauses are equivalent to the
two conditions in section 1. The
[canonical binary catalog](RESULTS-r1-canonical-axis-partition.md) supplies
21,091 reachable axes through five states. The ternary three-state backend
can instead use all 6,561 padded labelled axis tables directly.

## 3. Which earlier constraints transfer

All ordinary Rule 30 gate clauses remain necessary. A gate implicant that
fixes actual coordinate paths and raw output labels also remains necessary:
its proof does not use an external clock or any centre assumption.

The new base must omit the old fixed-clock variables and their constraints,
early centre equations, centre-violation cuts, clock-based aperiodicity
selectors, and any raw-output pruning expressed using that old clock.
Only ordinary gate cuts may be imported without a new semantic argument.
Rebuild by semantic variable names, or independently verify the identical
parameter allocation before reusing literal numbers.

This is a deliberately broader class. Previous UNSAT results for a centre
fixed from time one do not automatically exclude it.

## 4. Verification and scope

The reduction has been independently checked against the common-core
output functions and arbitrary-radix period theorem. The equation-specific
CNF and every imported cut still require independent reconstruction. Any
successful candidate also needs exact all-coordinate Rule 30 gates, actual
forward verification, the frozen ladder check, and the unchanged Rule 90
control before it can be reported as a counterdiagram.

Rule 90's genuine lone-seed diagram satisfies the abstract predicate: its
centre is eventually zero and its neighbour is aperiodic. The acceptance
predicate must admit it when paired with Rule 90 gates. Rule 30's OR enters
through its different gate constraints, including any separately proved
Rule-30-only prune; the automaticity lemma itself is rule-independent.

No finite list of automatic classes exhausts all Rule 30 diagrams. Even a
fully certified counterdiagram with an infinite-support initial row would
have to be distinguished from the original lone-seed statement. No proof
or kill of R1 is asserted by this reduction alone.

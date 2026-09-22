# Rank-one local transport retains only the first digit

Date: 2026-09-14. **Replacing invertible digit matrices by rank-one
matrices does not rescue a nonannihilating local transport invariant.**
Every product of the digit matrices either vanishes after two letters,
or depends only on the first digit and the word length. This holds over
every field and also for Boolean rank-one relations. The transport
matrices themselves may be singular.

The [exact verifier](../../experiments/rule30/p3_rank_one_transport.py)
and [artifact](../../experiments/rule30/p3-rank-one-transport.json)
check the finite incidence certificate and explicit examples. The
theorem below is an all-length classification under stated premises,
not an empirical search through matrix dimensions. It rules out the
specified product-only marked-query representation; it is not a P3
lower bound or a claim about all tensor-network constructions.

## 1. The local transport equation

Use the output-driven [itinerary automaton](RESULTS-p3-itinerary-conjugacy.md):

```
P_A=(0,3,2,1), P_B=(1,2,3,0), P_C=(3,2,1,0),
psi(0)=A, psi(1)=B, psi(2)=psi(3)=C.
```

For every state g and input digit d, let e=P_g(d). Consider

```
L_g M_d = M_e L_psi(e).                            (1)
```

This equation composes in the actual spatial order. If d0...d_(m-1)
is an input word, its chronological output is e0...e_(m-1), and its
final state is h, then

```
L_g M_d0 ... M_d(m-1) = M_e0 ... M_e(m-1) L_h.
```

The right boundary h is retained. Discarding or freely inverting it
is a separate assumption, not a consequence of(1).

## 2. Classification over an arbitrary field

**Theorem.** Suppose the four M_d are nonzero rank-one square matrices
over a field, (1) holds on all12 edges, and all12 products L_g M_d
are nonzero. Then the M_d have representations

```
M_d=u_d v^T,       u_d!=0, v!=0,
v^T L_g=kappa_g v^T,   kappa_g!=0.
```

Writing t_d=v^T u_d, exactly one of the following holds.

1. All t_d=0. Every product of at least two digit matrices is zero.
2. All t_d have one common value t!=0, and all kappa_g are equal.
   Every nonempty word has

```
M_d0 ... M_d(m-1) = t^(m-1) M_d0.                (2)
```

No assumption that the L_g are invertible is needed. Invertibility of
the L_g would automatically supply the nonzero-product premise.

**Proof of the common row line.** Write initially M_d=u_d v_d^T.
On a nonzero edge, the row line on the left of(1) is span(v_d^T).
The right row line depends only on the emitted e, being
span(v_e^T L_psi(e)). Inputs that can emit the same e therefore have
the same row line. The complete preimage sets are

```
e=0: {0,3};   e=1: {0,2,3};
e=2: {1,2};   e=3: {0,1,2}.
```

Already the first three connect all four digits. Choose a common
nonzero row v^T, absorbing its scalar normalizations into the u_d.
Since each of A,B,C occurs as psi(e), equation(1) now implies
v^T L_g=kappa_g v^T with kappa_g nonzero. Equality of the remaining
column factors gives

```
L_g u_d = kappa_psi(e) u_e,
kappa_g t_d = t_e kappa_psi(e).                   (3)
```

Because P_B is a four-cycle and all kappa values are nonzero, one
zero t_d forces all four to be zero. If none is zero, apply the
following finite cancellation argument to the scalar form of(3).
This argument works in any group for invertible symbols L_g,M_d:

```
B3=C3 gives L_B=L_C.
B0=C0 then gives M_1=M_3.
B2=C0 gives M_2=M_0.
A2=A0 gives L_A=L_C.
A0=B0 gives M_0=M_1.
```

Thus all kappa values and all t values coincide. Finally the product
of rank-one matrices is

```
u_d0 (v^T u_d1) ... (v^T u_d(m-1)) v^T,
```

which proves both cases and(2).

## 3. Boolean rank-one relations

The same conclusion holds over the Boolean semiring when each M_d
is a nonempty rectangle u_d v_d^T, each L_g is any Boolean relation,
and every side of(1) is nonempty. Here a Boolean product uses OR of
ANDs, not addition of integer path counts.

On a nonempty edge, the set of nonzero columns on the left is exactly
the support of v_d. On the right it is the support of v_e^T L_psi(e).
The same preimage connections force all v_d to one common Boolean
row v. The equations then give v L_g=v and L_g u_d=u_e. Consequently

```
t_d=v u_d=v L_g u_d=v u_e=t_e.
```

The B four-cycle forces a common t in{0,1}. If t=0, all products of
length at least two are empty. If t=1, every nonempty product is M_d0.
This includes rank-one matrix units as a special case. No invertibility
is imposed on the Boolean relations.

## 4. Why the nonannihilation premise matters

There are nontrivial solutions satisfying that premise. In dimension4,
take u_d to be the dth coordinate vector, v^T=(1,1,1,1), and L_g to
be the permutation matrix sending u_d to u_Pg(d). Then M_d=u_d v^T
satisfies every edge of(1), but M_d M_f=M_d: the representation retains
only its first digit.

Singular transport matrices do not evade the theorem: append an unused
zero coordinate to this example and make every L_g zero there. All12
edge products remain nonzero, and the same collapse holds. An example
of the other case takes dimension5, u_d the first four coordinate
vectors, v the fifth coordinate vector, and L_g acting as the root
permutation on the first four coordinates and fixing the fifth. Every
local edge is nonzero, although every product of two digit matrices
vanishes.

If annihilation is allowed, the local equation can become vacuous.
Take every L_g=0 and choose arbitrary rank-one M_d, such as the four
2-by-2 matrix units. All12 equations are0=0, although matrix products
can now distinguish adjacent symbols. This example supplies no update
rule: both sides of the proposed transport have been erased.

A useful field-valued refinement is that the theorem applies whenever
all16 pair products M_d M_f are nonzero and at least one local edge is
nonzero. To see this, define S to be the emitted digits e for which
M_e L_psi(e) is nonzero. For each g the image of L_g on
U=span(u_0,...,u_3) is precisely span(u_e:e in S), because P_g is a
permutation. If S is nonempty, every row v_f is nonzero on that image:
v_f u_e is nonzero for every e by the pair-product assumption.
Therefore v_f L_psi(f) is nonzero for every f, so S is all four
digits. The main nonannihilation premise follows.

Degenerate transports whose zeros select restricted input languages
remain outside this classification. To use one for the actual singleton
query, its surviving language, boundary information, and decoding must
be established separately. Merely satisfying a zero local equation is
not a computation of the observable.

## 5. Exact scope of the query obstruction

Under the theorem, any readout supplied only with the product in(2),
the length, and the requested position receives identical data for
words of the same length and first digit. It cannot recover a later
marked digit bit on all inputs. The two words00 and01, read low digit
first, already have identical matrix products and different low bits
at position1. Fixed boundary vectors or a readout depending on the
marked position cannot distinguish them.

Additional data depending on the actual interior, other marked tensor
insertions, varying-rank matrices, or a family restricted to actual
seed-reachable words are different proposals. The theorem does not
silently grant or rule out those additions. It also does not show that
the actual singleton query lacks a fast algorithm.

The verifier checks all12 transport edges in the three nonannihilating
examples over both integer and Boolean arithmetic, all16 pair products,
the output-preimage connectivity, and the degenerate example. It does
not search over dimensions or unknown matrix entries.

```
uv run --offline --no-project python experiments/rule30/p3_rank_one_transport.py
```

# Exact finite-width H cycles through the first period-eight lift

Date: 2026-09-14. **Every positive finite H orbit eventually has primitive
period1 at widths1–3, period2 at widths4–8, period4 at widths9–29, and period8
at width30. In each of these widths there is exactly one cycle up to temporal
phase.** In particular the first period-eight width is exactly30.

This is a complete temporal-column certificate, covering every initial
integer of the stated widths. It does not enumerate those integers or infer
their behavior from a selected one-hot input. The
[verifier](../../experiments/rule30/p3_period_four_column_certificate.py) and
[artifact](../../experiments/rule30/p3-period-four-column-certificate.json)
contain the complete256-node period-four graph and the four terminal lifts.
No period-eight graph is generated.

The result sharpens the constants in the earlier
[triangular cycle bound](RESULTS-p3-triangular-core-power.md). It supplies no
asymptotic improvement for P3 and makes no global novelty claim about the
known periodic flank of Rule30.

## 1. The exact finite graph

Use

```
H(x)=(x>>2) XOR ((x>>1) OR x).
```

Positive width is invariant. On a periodic orbit, three successive spatial
columns from high to low satisfy

```
z(t+1)=u(t) XOR (v(t) OR z(t)).                  (1)
```

Represent a four-periodic column by the integer whose bit t is its value at
time t, with t read modulo4. The graph has256 vertices (u,v). There is an
edge (u,v)->(v,z) exactly when (1) holds at all four times. Equivalently,

```
u(t)=z(t+1) XOR (v(t) OR z(t)).                  (2)
```

Every target pair (v,z) has exactly one predecessor, so enumerating the256
target pairs constructs every edge. An independent forward construction
tries the two entering values z(0), executes four ordered updates, and
retains the word only if its last update returns to z(0). Thus the finite
certificate retains the temporal seam and verifies every outgoing list.

Two zero columns lie above the highest one. The positive branch from (0,0)
is therefore (0,15), where15 is the constant-one column. The zero self-loop
does not belong to a positive-width path. Width counts columns starting
with that highest one.

## 2. Complete rooted component

The rooted nonzero component has97 vertices and no repeated vertex on or
between its paths. Its complete branching and termination data are:

| Width already present | Pair (u,v) | Possible next columns |
|---:|---|---|
| 3 | (15,0) | 5,10 |
| 8 | (5,0) | 6,9 |
| 8 | (10,0) | 3,12 |
| 29 | (13,0), (7,0), (14,0), (11,0) | None |

Every other reachable pair has exactly one outgoing edge. There is one
rooted path at each width1–3, two at each width4–8, and four at each width9–29.
The certificate checks that the paths at each width are temporal rotations
of one another, and that their primitive periods are respectively1,2,4.

For example, one complete width29 cycle, in chronological order, is

```
466434654, 421327336, 467256710, 420189862.
```

The artifact may start the same cycle at a different temporal phase. Its
high-to-low temporal columns and all four integer updates are checked.

At all four leaves the immediate driver v is zero and u has odd parity
over its four times. Equation (1) therefore gives z(t+4)=1-z(t).
Duplicating the already fixed upper four-periodic columns and trying both
entering bits produces eight width30 paths. They are the eight phases of
one primitive period-eight cycle. The checker verifies the complete eight
integer updates, without enumerating any additional temporal pairs.

## 3. Why this classifies every initial state

There are two logically separate claims to justify: the graph lists all
four-periodic columns, and a higher-period cycle cannot occur before the
listed leaves. The first is exactly (2). The second follows from the
ordered unary return map and does not follow from the graph count alone.

Suppose the upper spatial prefix on any cycle has primitive period P.
Over those P updates the next bit has one of three return maps:

* If v contains a1, the return is constant. Every periodic continuation is
  the unique P-periodic continuation; a longer cycle cannot avoid the reset.
* If v is zero and the parity of u over P is even, the return is identity.
  Both possible continuations are P-periodic.
* If v is zero and that parity is odd, the return toggles. Both continuations
  have period2P and differ by a shift of P times.

Start with the highest one, which is fixed. Until a period greater than4
first occurs, every upper prefix appears in the complete period-four
graph. The first two toggles are already represented by its phase branches
at widths4 and9. A further toggle to8 requires a pair with no four-periodic
continuation. The exhaustive rooted component has such pairs only at
width29, so it cannot occur earlier, and it must occur upon extension to
width30. This proves both the absence of hidden higher periods and the
claimed unique cycles.

Finally every finite-width integer orbit enters a cycle because the state
space is finite, and its highest one remains fixed. Consequently the
classification of cycles gives the stated eventual periods for **all**
positive initial integers of each width. Nothing here places the queried
time after the transient.

## 4. A stronger constant in the all-width period bound

The earlier triangular theorem proves that all periods are powers of two
and that, after a doubling to period at least4, successive doublings are
separated by at least seven spatial coordinates. The certified third
doubling occurs at width30. Thus a cycle of primitive period2^q with q>=3
requires

```
w >= 30+7(q-3) = 7q+9.                         (3)
```

An all-width upper bound is therefore

```
P_w = 1                           for 0<=w<=3,
      2                           for 4<=w<=8,
      4                           for 9<=w<=29,
      2^floor((w-9)/7)             for w>=30.    (4)
```

The zero state is fixed. Combined with the proved transient bound
mu<=(w-1)P for positive width, (4) also supplies the uniform iterate identity

```
H^(T_w+P_w)=H^T_w on [0,2^w),
T_w=max(w-1,0)*P_w.                             (5)
```

Every smaller-width period divides P_w, and its transient is at most T_w,
which justifies the ambient-width statement. This refines an exponential
bound by a constant factor. It proves no increasing all-length spacing law,
no polynomial bound on the period, and no faster construction of an actual
singleton query. The earlier normal-form implementation is unchanged.

## 5. Verification and scope

The maintained verifier checks256 inverse edges against1024 scalar time
equations; independently reconstructs all256 outgoing lists by the two
possible entering bits; closes the entire97-node rooted component; checks
every leaf's odd parity; verifies the phase classes at all29 permitted
widths; and checks124 whole-integer cycle edges across those representatives
and the unique width30 lift. The full graph, rather than a fitted trajectory
or sampled set of initial states, is the certificate for the quantified
statements above.

```
uv run --offline --no-project python experiments/rule30/p3_period_four_column_certificate.py
```

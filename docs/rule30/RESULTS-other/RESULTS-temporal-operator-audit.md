# Spatial matrices, growing frontiers, and the correct temporal operator

**Status.** The proposed four-state matrix multiplications are correct for
their stated recurrence. They do not identify that recurrence with the
guarded auxiliary Z dynamics. The proposed fixed-length temporal matrix
also omits an essential feature: successful frontiers grow even after their
original ancestors synchronize. The corrected operator formulation below
does not prove mortality or period-two exclusion.

This audit proves a scan-memory obstruction, verifies small exact examples,
and states the correct zero-product criterion. It concerns auxiliary legal
frontiers and asserts no singleton-seed ancestry.

## 1. What the proposed matrices actually compute

For the recurrence

```
y = u XOR (v OR x),        (u,v) -> (x,y),
```

the supplied matrices A_0,A_1 correctly label transitions by the spatial
output y. With the proposed state order 00,01,10,11, they satisfy

```
M=A_0 A_1,
M^2 = [[0,1,0,1], [0,0,0,0], [0,0,0,0], [0,1,0,1]],
M^3=M^2.
```

Thus M^n=M^2 for every n>=2. This is an exact algebraic observation about
successive spatial output labels of that recurrence.

Its recurrence after the first symbol is

```
y_i = x_(i-1) XOR (y_(i-1) OR x_i).
```

The middle variable is a preceding **output**. It is not a direct scan of
three old-row bits under the usual overlap convention, which would shift
the old input pair (u,v) to (v,x). Nor has a coordinate identification with
the specified auxiliary Z scan been supplied. The same Boolean expression
does not by itself identify the boundary conditions or the dynamical system.

In particular, the chronological scalar alpha_t is a terminal value of a
whole Z update. It is not the output at every spatial cell of that update.
For example, the genuine successful update

```
32 --0--> 303
```

has bulk output `30`, whose low bits are `10`. Requiring all spatial low
outputs to equal the terminal scalar 0 would discard this valid trajectory.

## 2. The exact deterministic Z scan requires its third memory bit

The actual cell input is x=2a+b, and the scan memory is (u,v,p), where p
is the preceding input high. The update is

```
v' = v XOR (p OR b),
u' = u XOR (v' OR a),
memory' = (u',v',a),        emitted symbol = 2u'+v'.
```

It starts at (0,0,0). Original legality restricts the first input to 2 or 3.
The terminal guard for scalar s requires u=v=s, with either terminal p.
In particular (u,v)=(0,1) fails, rather than emitting scalar 1.

**Explicit lost-memory witness.** Prefixes `20` and `22` both emit `21`
and leave (u,v)=(0,1). Their memories are respectively (0,1,0) and (0,1,1).
The same next symbol can therefore change survival itself:

```
202 --1--> 2132,
222 fails its guard, with bulk output212.
```

Appending 0 instead also shows that the terminal scalar is not determined
by the retained pair:

```
200 --1--> 2132,
220 --0--> 2103.
```

All four originals are legal, and the full updates are independently
checked against frozen `panel/cert33.py`.

**Deterministic memory lower bound.** Every one of the eight memories occurs
after a legal prefix:

| Prefix | Memory (u,v,p) |
|---|---|
| `201` | 000 |
| `32` | 001 |
| `20` | 010 |
| `22` | 011 |
| `30` | 100 |
| `2` | 101 |
| `200` | 110 |
| `3` | 111 |

After a memory (u,v,p), the guard-success indicators for the four possible
next symbols 0,1,2,3 are exactly

```
(1-u, 1-u, u XOR v XOR p, 1 XOR u XOR v).
```

These determine u from the first entry, v from the fourth, and p from the
third. Thus all eight memories have different one-symbol continuation
languages. A deterministic direct cell scan retaining the same quaternary
input convention requires at least eight states after legal prefixes,
even if it only reports guard success.

### Qualification: memory states are not linear dimension

The preceding result does not exclude every four-dimensional matrix
representation or every alternative encoding. Indeed let

```
A=(-1)^u, B=(-1)^(u XOR v), C=(-1)^(u XOR v XOR p),
phi=(1,A,B,C).
```

The exact cell maps for symbols 0,1,2,3 send phi respectively to

```
(1,C,A,A), (1,-B,A,A), (1,-A,-C,C), (1,-A,B,-B).
```

The terminal success indicator is (1+B)/2. This is a signed linear
representation of the one-update guard with eight possible feature vectors,
not a four-state nonnegative path-count model. It does not provide a
chronological multi-update representation by replacing cell symbols with
terminal scalar labels. The verifier checks all 32 local cases.

## 3. Synchronization does not fix frontier length

Each successful update appends `3-s`, so a frontier of L quaternary cells
becomes a frontier of L+1 cells. After n successes from original length r,
the current length is r+n.

The proved [synchronization theorem](RESULTS-weighted-history-endpoints.md)
says that after r successful updates the prescribed tape determines a
single endpoint. That endpoint has length 2r; its next successful update
has length 2r+1. The theorem identifies different ancestors' current words;
it does not make those words stop growing.

The smallest exact example is

```
original3 --1--> 32 --0--> 303 --failure.
```

Here r=1, so synchronization is already achieved at `32`. It still grows
on its next success. Also, `303` fails with terminal bulk pair (0,1), giving
a concrete control for the correct scalar-one guard.

## 4. The exact temporal matrices are rectangular

Let W_L be all legal length-L frontiers, of cardinality

```
M_L = 2^(2L-1).
```

Use row-vector conventions and define

```
U_L^(s)[w,z] = 1 iff Z(w)=(z,s),
w in W_L,                  z in W_(L+1).
```

The actual guard and appended birth are included in the entry definition.
This matrix has M_L rows and M_(L+1)=4M_L columns. Consequently a
chronological tape of length N uses the correctly typed product

```
U_r^(alpha_1) U_(r+1)^(alpha_2) ... U_(r+N-1)^(alpha_N).
```

It maps original length-r words to actual length-(r+N) endpoints and retains
every intermediate guard. Its nonzero rows are precisely C_r(alpha).
Because Z is deterministic, each surviving row has one endpoint. Summing
its columns over original rows gives the original endpoint weights used
in the [merger accounting](RESULTS-split-encoder-obstruction.md).

Writing U_L=U_L^(0)+U_L^(1), finite-frontier mortality is exactly

```
for every r there exists N such that
U_r U_(r+1) ... U_(r+N-1) = 0.
```

The equivalence uses the finite number of original length-r words: if each
dies, take the maximum of their finite lifetimes. This reformulates the
open theorem; no such all-r vanishing bound is proved here.

One may instead keep a fixed basis of **original** words, as the existing
guarded counting code does. Then the successive guard predicates depend on
the evolving, growing trajectory. Fixed original variables do not justify
a single time-independent finite-width update matrix with two fixed guard
projections.

## 5. Zero products, cycles, and the relevant quantifiers

For one prescribed infinite auxiliary tape at fixed r, if every finite
chronological product is nonzero, the nested finite original classes
C_r(alpha[:N]) have nonempty intersection. Thus some ordinary finite
original realizes that entire tape. Proving such nonvanishing at **every**
depth would be a mortality counterexample; a finite observation does not
establish it.

No finite-state cycle is required for such a trajectory. The exact graph
on all finite frontiers is already acyclic because every edge increases
length. An infinite surviving trajectory would be an infinite path in this
infinite graph. The finite-graph argument converting arbitrarily long paths
into a cycle does not apply without a proved finite quotient.

If all lengths are combined in an infinite graded vector space, mortality
would make the resulting operator locally nilpotent: every finitely
supported vector is eventually killed. Global nilpotence would demand one
exponent killing all original lengths and is already impossible. The
proved [all-depth spatial theorem](RESULTS-history-transfer-mixing.md)
supplies successful finite histories of every depth at sufficiently large
original lengths. Thus arbitrarily long finite histories coexist logically
with the conjecture that every fixed finite original dies.

## 6. Alternating auxiliary tapes are already bounded

The chronological auxiliary scalars are not the Rule 30 center-column bits.
The sufficient mortality route must handle arbitrary auxiliary scalar tapes.
It does not reduce period-two center exclusion to an alternating auxiliary
tape.

For an alternating auxiliary tape, D=0. The already proved repeat lower
bound immediately gives

```
r+N+1 <= 2(r+2), hence N <= r+3.
```

In particular, the correct chronological product for an alternating tape
of length r+4 is zero on all original length-r words. This is a consequence
of the existing theorem, not a new period-two exclusion. The missing case
is unrestricted tapes whose repeats accumulate across switches.

## 7. Exact verifier and scope

```
uv run --no-project python experiments/rule30/temporal_operator_audit.py
```

The [verifier](../../experiments/rule30/temporal_operator_audit.py) and
[artifact](../../experiments/rule30/temporal-operator-audit.json) check the
proposed matrix products, all 32 actual scan transitions, all 28 pairs of
distinct memories, the signed guard representation, and the explicit
length-changing and guard counterexamples. Forty attempted updates agree
with the frozen oracle. Source hashes and scope flags are retained.

The default has a ten-second wall cap and completed in under a second.
No old census, spatial-orbit extension, seed regeneration, or paid/GPU
compute was used. The frozen oracle is unchanged. The temporal operator
identities above are exact formulations, not a claim to have proved their
unrestricted vanishing.

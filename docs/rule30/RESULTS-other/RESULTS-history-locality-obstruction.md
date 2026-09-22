# Cumulative history information: exact defects and a locality obstruction

Date: 2026-09-11.

**The unrestricted counting inequality, every unrestricted positive-rate
variant, finite-frontier mortality, and period-two exclusion remain open.**
This investigation establishes a new uniform limitation on a counting proof:
for a fixed tape and sufficiently large original length, every assignment to
any bounded number of original bits occurs in its exact ancestor class.
Consequently, predicates involving only a fixed number of original bits cannot
provide a uniform information budget, even when nonlinear predicates and
overlapping supports are allowed.

There is also a positive, finite coding result. The difficult length-24 class
with 15 repeats admits a count certificate using six disjoint blocks of at
most eleven original bits. Its product bound is 3,857,168,160, below the
required 2^32. This succeeds where fixed coordinate deletion and independent
affine-equation counting failed. The uniform theorem explains why its block
size cannot simply be held constant in a general proof.

All statements concern legal auxiliary Z frontiers, with the original length
fixed in each ancestor class and every chronological guard imposed. No
singleton-seed reachability or P2 claim is made.

## 1. The four attacks and their outcomes

1. **A quantity retaining the full defect pattern.** The complete ordered
   defects have the exact nonlinear update below. Counting their population,
   even with arbitrary fixed phase offsets, fails: a genuine switch creates
   arbitrarily many defects from a state with no real-cell defects.
2. **Exact guarded composition.** A fixed original suffix acts bijectively on
   each appropriate temporal-column slice. Combined with the established
   all-depth connectivity, this proves the gap-completion theorem below.
3. **The difficult complete history.** Nonlinear block constraints give an
   exact finite certificate paying for all 15 repeats of the known length-24
   witness. No independence assumption or deletion of original variables is
   used.
4. **A weaker positive rate.** Bounded-arity support constraints are now ruled
   out as a uniform sufficient mechanism for *any* c>0 and epsilon>0. This
   refutes a class of proof mechanisms, not the desired counting bound.

## 2. Exact transport of all ordered defects

Let w be an actual image of length R, with previous scalar q. Use inward
coordinates A_d,B_d, zero-extended at d>=R. Extend the phase reference to d=0:

```
c_q(d) = q XOR ((d-1) mod 2),
X_d = A_d XOR c_q(d),    Y_d = B_d XOR c_q(d).
```

Thus X_0=q, Y_0=0 and X_1=Y_1=0. For a successful next scalar s, let
delta=q XOR s, and use primes for defects measured against the *new* phase.
For every d>=2 put c=c_s(d). The exact laws are

```
X'_d = X'_(d-1)
       XOR ((c XOR Y'_(d-1)) AND ((1-c) XOR delta XOR X_(d-2))),

Y'_d = Y'_(d-1)
       XOR ((c XOR delta XOR X_(d-1))
            AND ((1-c) XOR delta XOR Y_(d-2))).                 (1)
```

These retain the entire ordered defect sequence. They hold across switches
and in the virtual zero region; that region is not a supply of new bits.

**Proof.** Substitute A_d=X_d XOR c_q(d), and likewise for B, in the exact
backward equations from the
[episode-composition report](RESULTS-variable-length-episode-composition.md).
Use `a OR b = 1 XOR ((1 XOR a) AND (1 XOR b))` and
`c_s(d-1)=1-c`, `c_q(d-2)=c XOR delta`. Cancellation gives (1).
The actual birth values initialize the recurrence. This is an identity on
actual successful edges, not a replacement for the original guard.

The following closed family rejects the defect-population proposal. The
underlying two-update family was already proved in the
[phase-reset report](RESULTS-repeat-budget-phase-reset.md):

```
3 2^(4k-1)  --0-->  (30)^(2k)3  --1-->  (3210)^k32,    k>=1.    (2)
```

At the middle state, X_d=Y_d=0 for every real depth 1<=d<R. At the last
state, all real Y defects still vanish, while

```
{d : X_d=1, 1<=d<R'} = {3,4,7,8,...,4k-1,4k}.                  (3)
```

Consequently no rank

```
Phi_q(w) = C_q + SUM_(1<=d<R) (X_d + Y_d)
```

with fixed finite phase constants can be nonincreasing on every successful
switch: it would require C_0>=C_1+2k for every k. The same obstruction holds
for fixed nonnegative depth weights whose sum over the displayed depths
diverges. This does not exclude a more elaborate function of the full ordered
profile or a quantity that retains additional history. It shows why merely
replacing the first-defect height by the number of defects does not repair
the reset problem.

## 3. A uniform gap-completion theorem for original histories

Fix a tape alpha of length n>=1. Use the established common transfer graph
T_n, whose S_n=2*4^n vertices record

```
q = (A_0,A_1,B_1,...,A_n,B_n).
```

Reading an original symbol `(a,b)` supplies `A'_0=a,B'_0=b` and updates

```
B'_j = B_j XOR (A_(j-1) OR B'_(j-1)),
A'_j = A_j XOR (B'_j OR A'_(j-1)).                             (4)
```

The accepting pair sigma(alpha),sigma(alpha)+1 specifies the *complete*
chronological guard history; its only free coordinate is terminal A_0.
The [transfer theorem](RESULTS-cumulative-history-transfer.md) establishes
that original-word paths ending at this pair are exactly C_r(alpha).

**Fixed-symbol bijection.** For any input symbol `(a,b)` and any h in {0,1},
its map from the slice A_0=h to the slice A'_0=a is a bijection.

Indeed, given the target slice, set old A_0=h and reconstruct in increasing j:

```
A_j = A'_j XOR (B'_j OR A'_(j-1)),
B_j = B'_j XOR (A_(j-1) OR B'_(j-1)).                           (5)
```

Each old pair is determined uniquely. Both slices have 4^n elements.
Composing these bijections proves the corresponding statement for any fixed
nonempty original suffix S: for either prescribed incoming high bit h, the
map is a bijection onto the slice whose high bit is the last high bit of S.

Set

```
L_n = 2(S_n-1) = 4^(n+1)-2.
```

The [all-depth connectivity theorem](RESULTS-history-transfer-mixing.md)
proves that T_n is strongly connected and its zero vertex has a self-loop.
Every vertex can therefore reach every other in **each exact length g>=L_n**:
go to zero in at most S_n-1 edges, wait there, then go to the destination in
at most S_n-1 edges.

**Gap-completion theorem.** Let P be any fixed nonempty legal original
prefix, S any fixed original suffix, and g>=L_n. There is a word G of length
g such that

```
P G S belongs to C_(|P|+g+|S|)(alpha).                           (6)
```

**Proof.** Reading P from its true origin vertex gives a definite column x.
If S is empty, choose either accepting vertex y. If S is nonempty, choose
the accepting vertex with its required terminal high bit. The fixed-suffix
bijection supplies its unique preimage y in, say, the incoming-high-zero
slice. An exact length-g path from x to y supplies the symbols of G.
The completed original word ends at the fully guarded accepting pair, proving
(6). P and S remain exactly the prescribed words. No intermediate guard is
discarded.

This is an existence theorem about *original inputs*. It does not let an
already chosen original trajectory replace its current predecessor or repair
a failed guard by choosing a fresh completion.

## 4. Full projections and the obstruction to bounded arity

At original length r, index the m=2r-1 free bits as

```
x_0=b_0,    x_(2i-1)=a_i,    x_(2i)=b_i,   1<=i<r.
```

**Full-projection theorem.** Fix n>=1 and k>=0. For every length-n tape
alpha and every

```
r >= 1+(k+1)L_n,                                               (7)
```

the projection of C_r(alpha) onto *any* set J of at most k free original
bits is all of `{0,1}^J`.

**Proof.** Assign arbitrary values to the chosen bits. They touch at most k
of the r-1 non-origin sites. If there were no untouched run of L_n sites,
there would be at most k+(k+1)(L_n-1)=(k+1)L_n-1 non-origin sites altogether.
This contradicts (7). Choose L_n untouched consecutive sites as G. Complete
all sites outside G arbitrarily, respecting the selected bits and a_0=1.
The gap-completion theorem fills G without changing any selected bit. The
result is a member of the same C_r(alpha). Repeating this construction for
each assignment proves surjectivity.

Different assignments may use different original completions. The original
length and the tape are fixed throughout the assertion. This proves full
*support* of the projections, not uniform marginal probabilities and not
statistical independence.

For a set C, let its k-arity envelope be the intersection of **all** predicates
that hold everywhere on C and depend on at most k of the original free bits.
Under (7), every such predicate must be identically true, because every
assignment to its support occurs. Hence

```
k-arity-envelope(C_r(alpha)) = all legal original length-r words. (8)
```

Overlapping supports, position-dependent predicates and arbitrary nonlinear
truth tables do not alter (8). In particular, a nontrivial predicate valid on
C_r(alpha) must involve at least `floor((r-1)/L_n)` original bits whenever
that lower bound is positive. This is a bound on **support size**, not
polynomial degree: a parity equation may involve many bits and have degree one.

For any proposed fixed k,c>0,epsilon>0, choose n so large that
`epsilon*(n-1)>log_2(c)`, take alpha=0^n, and choose r satisfying (7).
The class is nonempty and D=n-1. Its k-arity envelope has size 2^m, which
exceeds `c*2^(m-epsilon*D)`. Thus **no counting upper bound obtained solely
from bounded-arity universally valid support predicates can establish the
desired positive-rate estimate uniformly**.

The same argument applies to an arity bound k(alpha) depending only on the
tape: after fixing alpha, r can still exceed the threshold in (7). Thus a
successful support-predicate method must allow its arity to grow with the
**original length**, even at a fixed temporal depth.

The actual class can still be much smaller than its envelope. This theorem
does not refute the estimate for the actual |C_r(alpha)|, nor adaptive
encodings, unbounded-support constraints, weighted marginal arguments, or
factorizations with auxiliary states. In particular, a small-state spatial
automaton can impose constraints of large support on the original bits;
it is not ruled out by the arity theorem.

The verifier obtains sharper exact gap lengths at four small depths:

| Tape length n | Graph vertices | Least all-pairs exact path length |
|---:|---:|---:|
| 1 | 8 | 3 |
| 2 | 32 | 6 |
| 3 | 128 | 9 |
| 4 | 512 | 13 |

For example, for **every r>=1+6(k+1)**, every assignment to any k original
free bits occurs in C_r(00). Once all pairs have paths of length E, an
arbitrary initial edge followed by such a path supplies length E+1; induction
supplies every larger length. The table is a finite graph certificate; no
formula for arbitrary n is inferred from its values. The general theorem
uses L_n above.

## 5. A successful nonlinear code for the difficult finite history

Use the complete original class

```
r=24, alpha=00011100001111111100, D=15, m=47.
```

Its previously independently established count is 55,885,140. The
[encoding obstruction](RESULTS-history-encoding-obstruction.md) showed that
fixed coordinate deletion cannot retain only 32 bits and that there are at
most six independent affine equations on the class.

For a contiguous interval I of original free-bit indices, let P_I be the
exact projection of this class onto I. Choose the following disjoint
partition; intervals are half open:

| I | Number of bits | Projection size |
|:---|---:|---:|
| [0,5) | 5 | 2 |
| [5,16) | 11 | 219 |
| [16,17) | 1 | 2 |
| [17,28) | 11 | 453 |
| [28,37) | 9 | 108 |
| [37,47) | 10 | 90 |

Reading the six projected values is injective on original words because the
blocks partition all original bits. Therefore

```
|C_24(alpha)| <= 2*219*2*453*108*90
              = 3,857,168,160 < 2^32 = 2^(47-D).               (9)
```

This is a concrete nonlinear code: index each block value in its allowed
set, then encode the six indices in mixed radix. The product is below 2^32,
so a 32-bit label suffices. **No product-distribution or independence
assumption is needed.** The Cartesian product is an overestimate of the
class, which is the required direction.

Overlapping windows give a smaller envelope. Intersect the exact allowed
patterns on every width-k contiguous free-bit window, retaining agreement
on overlaps. A finite dynamic program gives:

| Window width k | Exact size of this envelope |
|---:|---:|
| 1 | 2,199,023,255,552 |
| 2 | 927,712,935,936 |
| 3 | 193,273,528,320 |
| 4 | 26,491,944,960 |
| 5 | 11,638,652,832 |
| 6 | 6,462,124,236 |
| 7 | 2,947,869,792 |

Seven-bit windows suffice for the one-bit estimate on this history; widths
through six do not suffice using this particular envelope. Three-bit windows
already suffice for epsilon=1/2, since their envelope count U satisfies
`U^2*2^15 <= 2^94` exactly.

These certificates concern the entire original class, not selected members.
All eight previously documented plateau repeats are therefore included.
The upper bounds certify information acquired earlier that remains available
during later repeats; they do not assert new filtering at each repeat.

The contrast at the earlier prefix is instructive. For the same r and tape
`000111000`, whose exact class has 380,628,720 originals, **every contiguous
four-bit window has every pattern**. Its width-four envelope is still the
entire 2^47 cube. Thus even in this one history, substantial information can
reside in correlations invisible at a selected local scale. Section 4 turns
this phenomenon into an all-length obstruction for every fixed arity.

## 6. Verification and the remaining mathematical obligation

Run:

```sh
uv run --no-project python experiments/rule30/history_locality_certificate.py
```

The [verifier](../../experiments/rule30/history_locality_certificate.py),
[predicate exporter](../../experiments/rule30/history_locality_certificate.cpp)
and [artifact](../../experiments/rule30/history-locality-certificate.json)
provide:

* All 128 local truth-table cases for (1), plus independent full scans of
  five instances of the uniform family (2)-(3).
* Complete graphs through temporal depth four, all fixed-symbol inverse
  checks, and the exact all-pairs path exponents in the table.
* 128 constructed legal originals, including every assignment to three
  scattered bits in a length-25 C_25(00) control. The unchanged frozen oracle
  checks all 408 successful original updates and every guard.
* The two exact original-variable predicates, generated with the maintained
  guarded BDD engine. A separate Python reader validates their reduced graph
  structure, recounts their satisfying assignments and computes the allowed
  projections by existential traversal. The envelope dynamic program retains
  overlaps, and the disjoint-block product uses integers only.
* 112 original representatives of projected patterns, independently replayed
  for 1,624 successful updates with the frozen oracle. These representative
  checks supplement the symbolic predicate proof; they do not stand in for
  a census or independently prove the projection exclusions.

The completed local run took approximately 1.3 seconds. Compiler and counter
subprocesses have external wall timeouts. The source hashes are saved. No
original-frontier census, seed regeneration, paid computation, or modification
of the frozen oracle was performed.

The missing statement is still a uniform control of **total** chronological
information as D grows. The new obstruction says that retaining only
bounded-arity support information is insufficient; the finite code says that
nonlinear information can pay for the established plateau without charging
each repeat separately. A proof must control the required growing scale, or
use a different global quantity. Neither control is proved here.

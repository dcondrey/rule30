# The exact guarded-history transfer has minimal MPO bond dimension four

Date: 2026-09-13. **An exact representation theorem and an upper-compression
certificate are proved.** The spatial transfer for chronological history
counts has a nonnegative matrix product operator with bond dimension four,
at every temporal depth. A rank-four minor shows that four is necessary in
the stated physical ordering.

This does not give a uniform bound on the bond dimension of its iterated
messages, a useful compressed count certificate, or a mortality theorem.
The cumulative counting inequality and period-two exclusion remain open.

All history counts retain the original length and every chronological guard.
The columns are exact counting separators for auxiliary frontiers; no
singleton-seed reachability is assumed.

## 1. Exact transfer and physical ordering

Use the column coordinates

```text
q = (A_0,z_1,...,z_n),       z_j=(A_j,B_j),
q' = (A'_0,z'_1,...,z'_n).
```

The normalized spatial transfer is

```text
P_n(q,q') = (1/4) * #{x in {0,1,2,3}: delta(q,x)=q'}.
```

Each of its four labeled edges chooses one **original** input symbol. The
local cascade is

```text
B'_j = B_j XOR (A_(j-1) OR B'_(j-1)),
A'_j = A_j XOR (B'_j OR A'_(j-1)).
```

At level zero, A'_0 is the new original high bit and B'_0 is its low bit.
The latter is summed out. Chronological guards and transported births remain
in the exact acceptance indicator g_alpha; they are not separately imposed
at the right end of each application of P_n.

For original length r the desired probability is

```text
|C_r(alpha)| / 2^(2r-1)
  = (1/2) SUM_(beta=0,1) (P_n^(r-1) g_alpha)(o_beta).
```

The two o_beta are the legal origin columns from the
[transfer theorem](RESULTS-cumulative-history-transfer.md).

## 2. Four bond states suffice

The direct eight-state separator would remember

```text
(p,u,v)=(A_(j-1),A'_(j-1),B'_(j-1)).
```

The next layer uses these bits only through

```text
t=u,       e=p OR v.
```

Thus use four bond states sigma=(t,e). For old physical pair x=(a,b) and
new pair y=(c,d), define the nonnegative local tensor

```text
W_(sigma,tau)(x,y) = 1 exactly when
    d = b XOR e,
    c = a XOR (d OR t),
    tau = (c, a OR d);
otherwise W=0.
```

For fixed sigma and x there is exactly one y and one tau. This tensor
therefore propagates the complete local relation, including its shared
latent bond, without an independence approximation.

At the original-high boundary, put

```text
L_(t,e)(a,a')
  = (1/4) * 1[t=a'] * #{b in {0,1}: e=a OR b}.
```

In bond order `(0,0),(0,1),(1,0),(1,1)`, its four rows are

| (a,a') | Boundary row L |
|---|---|
| (0,0) | (1/4,1/4,0,0) |
| (0,1) | (0,0,1/4,1/4) |
| (1,0) | (0,1/2,0,0) |
| (1,1) | (0,0,0,1/2) |

The right boundary is one in each bond state. Hence

```text
P_n(q,q')
  = SUM_(sigma_0,...,sigma_n)
      L_(sigma_0)(A_0,A'_0)
      PRODUCT_(j=1..n) W_(sigma_(j-1),sigma_j)(z_j,z'_j).
```

**Proof.** The bond invariant is exactly
`sigma_j=(A'_j,A_j OR B'_j)`. Substitution in W gives the original cascade
at every level. The left boundary counts precisely the original low-bit
choices compatible with that invariant. In particular, the weight 1/2 when
A_0=1 preserves the multiplicity of two OR-masked original choices. No
weight is introduced at later temporal layers. Summing the final bond imposes
no additional constraint. This proves the equality for every n.

This does not contradict the
[eight-memory scan obstruction](RESULTS-temporal-operator-audit.md). That
result scans the four-symbol original frontier. Here each physical site
contains an old and new **temporal-column** pair; the separator and the
direction of contraction are different.

## 3. Four is also necessary

At depth n=2, matricize the operator by placing

```text
(A_0,z_1; A'_0,z'_1)
```

on the row side and `(z_2;z'_2)` on the column side. Symbols below encode
each pair by 2A+B. Select these four rows:

```text
(0,0;0,0), (0,2;1,0), (0,0;1,2), (0,2;0,2),
```

and these four columns:

```text
(0;0), (1;0), (0;2), (1;2).
```

The resulting submatrix of 4P_2 is exactly the 4-by-4 identity. This can be
checked by the four original-symbol transitions at each selected entry;
the explicit full-column implementation gives the same minor.

Any MPO crossing this cut factors the matricization through its bond space,
so its bond dimension is at least the ordinary matrix rank, namely four.
For n>2, fix the old pairs above two and sum their new pairs. The local
deterministic continuation contracts P_n to P_2. This acts entirely on the
suffix side of the cut and cannot increase its rank, so the lower bound
persists at every greater depth.

At n=1, cut directly after (A_0,A'_0). Using rows
`(0,0),(0,1),(1,0),(1,1)` and columns
`(z_1,z'_1)=(0,0),(1,0),(0,2),(1,2)`, the selected matrix of 4P_1 is

```text
1 1 0 0
0 0 1 1
0 2 0 0
0 0 0 2
```

Its determinant is -4. Thus four is minimal at every n>=1, with the
original-high boundary treated as the first physical site. The lower bound
holds even if signed coefficients are allowed. This is an operator-rank
result, not an asymptotic claim about the rank of repeated messages.

## 4. Exact action on nonnegative MPS messages

Write a nonnegative matrix product message as

```text
f(q') = ell(A'_0) B_1(z'_1) ... B_n(z'_n) rho.
```

The matrices may depend on the temporal position, tape, and spatial horizon.
The leaf g_alpha has bond dimension one: each physical factor is the
indicator for its prescribed pair, and ell(A'_0)=rho=1.

Applying P_n produces an exact expanded message E whose bond is at most
four times the previous bond. Its coefficients are

```text
ell_E(a)_((sigma,i))
  = SUM_(a') L_sigma(a,a') ell(a')_i,

E_j(x)_((sigma,i),(tau,h))
  = SUM_y W_(sigma,tau)(x,y) B_j(y)_(i,h),

rho_E_((tau,h)) = rho_h.
```

All coefficients are nonnegative. The original normalization appears only
in ell_E. An additional factor 1/4 per temporal site would be incorrect.

Starting from the leaf, b exact applications therefore give the elementary
upper bound `bond dimension <=4^b`. This is not a claim of necessary
exponential growth. Nor does the constant operator bond prove that useful
upper messages can remain at fixed bond.

There is also an exact simplification from the
[inverse-front theorem](RESULTS-inverse-message-front.md). After b spatial
steps, when n>=b+1, the message factors into a correlated prefix of b+1
temporal pairs and a deterministic pinned tail. That tail has bond dimension
one. The high bit A_(b+1) is also pinned, so the effective correlated physical
dimensions are

```text
2, 4, ..., 4, 2,
```

with b full pairs between A_0 and the final free low bit. Across the cut
after pair j the ordinary matrix rank is at most

```text
min(2*4^j, 2*4^(b-j)),       0<=j<=b.
```

These dimension bounds also give a constructive **nonnegative** MPS upper
bound: use identity tensors to retain complete prefix and suffix assignments,
and place the original nonnegative coefficient table at a central physical
site. Consequently, for b>=1,

```text
maximum required bond <= 2*4^floor(b/2).
```

For b=0 the leaf has bond one. If A_0=1 is fixed only after all transfers,
for the final legal-origin contraction, the analogous bound is `2^b`.
This restriction must not be imposed prematurely on intermediate messages:
the spatial transfer also evaluates columns with A_0=0.

At fixed original length r, take b=r-1. The correlated core has at most
r pairs, and these upper bounds are independent of larger tape depth n.
They retain every later guard through the tail compatibility indicator;
they do not prove that this compatibility must eventually fail. Ordinary
cut rank can prove lower bounds on exact MPS bond, but need not equal the
minimum bond when all factors are required to be nonnegative. No exponential
lower bound on actual message ranks is asserted here.

## 5. A local certificate for upper compression

Suppose E is an expanded exact MPS with nonnegative matrices E_j(x), left
row ell_E(a), and right column rho_E. Propose a smaller nonnegative MPS

```text
F(q) = ell_F(A_0) B_1(z_1) ... B_n(z_n) rho_F.
```

For each cut j choose a nonnegative simulation matrix S_j with dimensions

```text
(expanded bond at cut j) by (compressed bond at cut j).
```

The following componentwise inequalities are sufficient:

```text
rho_E <= S_n rho_F,
E_j(x) S_j <= S_(j-1) B_j(x)    for every j and physical symbol x,
ell_E(a) S_0 <= ell_F(a)         for a=0,1.             (1)
```

**Certificate theorem.** If (1) holds, then E(q)<=F(q) for every full column.

**Proof.** Induct backward on suffix vectors. The right inequality starts
`e_n<=S_n f_n`. If this holds at cut j, nonnegativity gives

```text
e_(j-1) = E_j(x) e_j
        <= E_j(x) S_j f_j
        <= S_(j-1) B_j(x) f_j
         = S_(j-1) f_(j-1).
```

Multiplying by ell_E and using the left inequality completes the proof.
The same simulation matrix is used for every occurrence of a latent bond;
no separate maximizer is chosen for different downstream assignments.

Applied after each exact MPO expansion, these certificates inductively
majorize the true guarded message. The final MPS can be evaluated exactly
at the two legal origins. It becomes a count certificate only if that root
value meets the required `c*2^(-epsilon*D)` probability bound.

All proposed coefficients and inequalities can be checked with rational
arithmetic. When the candidate compressed tensors and boundaries are fixed,
the displayed feasibility constraints are linear in the unknown S_j.
Learning or numerical factorization could propose those tensors; it cannot
replace the certificate. Failure to find S_j excludes that particular local
simulation certificate, not every upper MPS of the same bond dimension.

For a uniform theorem one must additionally give a parametrized family and
prove its inequalities and root estimate for arbitrary r,n,alpha. Checking
finitely many tensor tables does not provide that quantification.

## 6. Why this remains a distinct candidate class

A bond state carries information through the entire temporal column. Even a
two-state nonnegative MPS can impose parity on arbitrarily many sites, using
identity and swap matrices and selecting the final parity at the boundary.
Thus a fixed bond is not the same restriction as a bounded-support predicate,
a single retained window, or a sum of nonnegative local bag functions.
The previous message obstructions do not automatically exclude this class.

That distinction is a reason to test the certificate, not evidence that the
needed compression exists. The concrete next discriminator is whether a
small nonnegative bond and matrices S_j certify an upper message that meets
a saved difficult history's threshold. Exact expansion, identity compression,
and a deliberately invalid compression provide controls for the checker;
they are not themselves a new counting result.

## 7. Exact verification

Run:

```text
uv run --offline --no-project --with numpy python experiments/rule30/guarded_history_mpo.py
```

The [implementation](../../experiments/rule30/guarded_history_mpo.py) and
[artifact](../../experiments/rule30/guarded-history-mpo.json) record:

* sixteen local eight-to-four quotient tensor identities and five boundary
  identities;
* all 17,472 operator entries at temporal depths one through three, with
  672 labeled original-symbol edges;
* 2,061 exact column comparisons for MPS application to selected guarded
  tape indicators;
* the rank-four identity minor at depth two and determinant-minus-four
  minor at depth one;
* two valid majorant certificates, two deliberately invalid boundary
  certificates, rejection of floating and malformed certificates, and
  128 direct pointwise comparisons.

The saved run completes in under one second; its precise time is recorded
in the artifact. Arithmetic is exact: the
implementation uses T=4P and applies the corresponding normalization once
per spatial transfer. The majorant checker admits integers and rational
fractions. These checks validate exact expansion and the stated
certificate orientation. They do not demonstrate a useful reduction of bond
dimension on a difficult history or a new counting inequality.

No original-frontier census, public-data regeneration, model training, GPU,
or paid compute was needed.

## 8. Bounded comparison with the window relaxation

The separate [rank verifier](../../experiments/rule30/message_mps_rank_audit.py)
and [artifact](../../experiments/rule30/message-mps-rank-audit.json) certify
154 cut ranks for selected exact and width-three relaxed messages at depth
seven. Integer row elimination gives the rational rank; a matching nonzero
minor modulo a verified prime supplies an independent lower certificate.

For the tape `0010011`:

| Spatial transfers b | Minimal ordinary exact MPS bond of h_b | Minimal ordinary exact MPS bond of the width-three upper message |
|---:|---:|---:|
| 6 | 11 | 15 |
| 8 | 17 | 24 |

In these finite examples the relaxation is itself harder to represent as
an exact ordinary MPS than the true message. Both true original-origin
counts are zero: these ranks concern the function on all columns, not a
positive surviving ancestor fiber. They give neither an asymptotic rank
law nor the minimal nonnegative ranks.

The same verifier checks a global parity function with nonnegative MPS
bond two whose proper-window envelope is identically one. This is an
auxiliary representation example, not an asserted Rule 30 message. It
supports the distinction in section 6 without assuming that the actual
guarded messages have an equally small representation.

## 9. A global-maximum shortcut is false

The new representation suggests checking whether

```text
max_q (T_n^b g_alpha)(q) <= 2^b,       n>=b+1.          (2)
```

This would imply the desired one-bit estimate for every r>=n: apply it at
b=n-1 and then use that P cannot increase the maximum. But (2) is false.
The verifier records two small exact witnesses:

| Tape | b | Column q | Exact h_b(q) | Proposed ceiling |
|---|---:|---:|---:|---:|
| `11` | 1 | 25 | 4 | 2 |
| `000` | 2 | 21 | 6 | 4 |

For the first witness, q is `(A_0=1; z_1=0,z_2=3)`. Its four labeled
successors are `6,6,7,7`, exactly the two accepting columns for `11` with
their multiplicities. The second witness has six accepting two-symbol
paths, all recorded in the artifact.

There is an all-length version of the first observation. If alpha begins
with one, its first required pair is 3. Choose old A_0=1 and old first pair
0. Then every input symbol produces the first required pair: the high
boundary masks the input low bit, and the new low bit one masks the input
high bit. Every later old pair can be uniquely inverse-completed from the
common target pairs. Thus there is a column q with `P_n g_alpha(q)=1` for
every such tape. No factor below one can hold at this first spatial step
uniformly over columns.

These witnesses concern unrestricted **temporal columns inside the exact
counting transfer**, not arbitrary replacements for the original legal
frontiers. Neither is one of the two legal origin columns at the indicated
depth. They refute (2), not the actual original-origin count inequality.

## 10. A bounded exact compression attempt on the width-three obstruction

The [deterministic suffix verifier](../../experiments/rule30/deterministic_mps_quotient_probe.py)
implements one concrete exact compression and saves its
[artifact](../../experiments/rule30/deterministic-mps-quotient-probe.json).
Each row has at most one outgoing edge for each physical symbol. Working
backward, multiply each outgoing weight by its child's normalization, divide
the nonzero weights by their gcd, and merge identical normalized rows.

This procedure has an exact nonnegative simulation certificate. If a state
i merges into class c_i with scale s_i, put `S[i,c_i]=s_i`, using a zero
row for a zero residual. The normalized row construction gives

```text
E_j(x) S_(j+1) = S_j B_j(x),
rho_E = S_n rho_B,       ell_B = ell_E S_0.
```

The equality version of section 5 proves that every column value is
preserved. This is an all-length construction for such deterministic
integer-weighted MPS, not an inference from the finite probe.

For the guarded leaf, a stronger restriction persists: each row accepts
only **one** physical symbol across the whole alphabet, with unit weight.
For a fixed MPO bond the map from old physical pair to new pair is a
permutation, so expansion preserves this property. Quotienting only merges
identical point-mass suffixes; it cannot introduce the general branching
needed to represent many suffixes with one latent state. It is a narrow
subclass of nonnegative MPS compression.

The bounded probe used `alpha=0^22`, original length r=41, a 20-second work
budget, and a 4,096-state cap on the expanded bond. It completed b=11
spatial transfers. Its largest compressed bond was 1,392; the next expansion
would construct 5,568 states, so the probe stopped at its cap. All completed
layers matched a separate sparse inverse recurrence; 468,098 local and
boundary simulation equalities passed in the main probe. Separate small
controls checked another 1,432 equalities and 2,728 column evaluations.

At b=11 the exact normalized global maximum is

```text
max_q P_22^11 g_(0^22)(q) = 64,435 / 2^21.
```

Stochasticity preserves this ceiling under all further spatial transfers.
It therefore supplies the valid, but inadequate, bound

```text
|C_41(0^22)| <= 64,435 * 2^60.
```

The desired one-bit threshold is `2^60`: this certificate leaves a factor
64,435 gap. The exact requested count was not computed. The true origin
counts at the completed original lengths 1 through 12 are zero, which must
not be substituted for the requested length 41.

The probe rules out continuing this particular exact suffix-mixture
calculation under the declared cap. It does not prove a lower bound against
general MPS compression, and it does not refute the counting inequality.
Increasing that cap alone is not the proposed next step. A useful follow-up
needs compressed states representing multiple compatible suffixes and a
nonnegative domination certificate that still meets the origin threshold.

**Subsequent results:** [shared-prefix sweeps](RESULTS-shared-prefix-mps.md)
and [nonnegative conic factorization](RESULTS-disjoint-cone-mps.md) introduce
and verify such shared branching, though they do not complete this MPS
count. An independent [guarded UNSAT certificate](RESULTS-constant-zero-history-certificate.md)
now proves the benchmark's exact value `C_41(0^22)=empty`. The
[reference-message theorem](RESULTS-reference-message-compression.md)
separately identifies the remaining issue as controlling accumulated error
under transfers, rather than small final-stage bond dimension alone.

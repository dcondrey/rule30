# The repeat budget: an exact phase rank and its reset law

Date: 2026-09-09. Based on commit `3b2b34c`.

There is now a concrete nonlinear rank that pays for every repeated scalar.
Its failure across episodes is also exact: switches reset its defining
height, and returns to the same phase increase the rank by elapsed time.
An explicit family makes the refill arbitrarily large.

Two other candidate classes have uniform impossibility certificates:
phase-dependent additive scan ranks on actual second images, separately in
both sectors; and arbitrary unit-drop ranks built from inverse-branch counts,
phase, sector and actual length, even on third images.

**The cumulative repeat budget remains unproved and unrefuted. P1/P2 and
unrestricted Z mortality remain open.** The results concern the legal finite
frontiers defined in [the composition report](RESULTS-variable-length-episode-composition.md),
not an asserted collection of frontiers from the original lone-seed orbit.

## 1. A nonlinear rank for repeated scalars

Let w be an actual image of a successful Z update, of length R. Write q
for its most recent terminal scalar. In inward depth coordinates,

```
(A_0,B_0)=(1,1 XOR q),    (A_1,B_1)=(q,q).
```

Extend the frontier by zero at original indices k<0. Equivalently, set
`A_d=B_d=0` for d>=R. These are virtual cells, not new input choices. The
zero extension agrees with the scan's fixed zero memory on the left.

Put `c_q(d)=q XOR ((d-1) mod 2)` for d>=1. Define H_q(w) to be the largest
integer h>=0 such that

```
A_d=c_q(d) for 1<=d<=h+1,
B_d=c_q(d) for 1<=d<=h.
```

This is a static first-defect statistic, computed directly from the current
word. If d_A and d_B are the first depths where A and B respectively differ
from c_q, then `H=min(d_A-2,d_B-1)`. It is not a definition in terms of future
survival or future repeats.

**Phase-rank theorem.** Set

```
rho_q(w)=R-1-H_q(w).
```

Then rho is a nonnegative integer. Whenever the next successful scalar is
again q,

```
H_q(Zw) >= H_q(w)+2,
rho_q(Zw) <= rho_q(w)-1.                              (1)
```

**Proof.** H>=0 follows from A_1=q. H>=R would require the two virtual cells
A_R and A_(R+1) to equal opposite alternating bits, whereas both are zero.
Thus H<=R-1, proving nonnegativity.

The exact backward equations, including the virtual zero region, are, for d>=2,

```
A_d' = A_(d-1)' XOR (B_(d-1)' OR A_(d-2)),
B_d' = B_(d-1)' XOR (A_(d-1) OR B_(d-2)).              (2)
```

For another q, the birth pattern gives
`A_1'=B_1'=q`, `A_2'=B_2'=1 XOR q`, and `A_3'=q`, even when H=0.
Continuing in increasing depth in (2), the required old fields lie in the
known A-range through H+1 and B-range through H. Each relevant OR joins
complementary alternating bits, hence equals one. This supplies the new
A-range through H+3 and B-range through H+2. Length increases by one while
H increases by at least two, proving (1).

This gives a uniform rank for a constant episode without expressing it as
a sum of local counts. It works equally for `00` and `11`.

## 2. Switches reset the height exactly

For actual image states, every scalar-one state has A_2=0, including the
virtual-cell small-length case. Indeed, a first successful one forces
`A_2'=1 XOR (1 OR A_0)=0` independently of the old frontier. Thus q=1
implies H_q>=1.

**Reset theorem.** On any successful switch from an actual image,

| Switch | New height | Change in rho |
|---|---:|---:|
| `0→1` | 1 | H_old |
| `1→0` | 2 | H_old−1 |

**Proof.** For `0→1`, (2) gives `A_2'=B_2'=0` and `A_3'=0`. The new
phase-one pattern requires A_3'=1, so H_new=1. For `1→0`, the old A_2=0
gives `A_2'=B_2'=1`, `A_3'=B_3'=0`, and `A_4'=0`. The phase-zero pattern
requires A_4'=1, so H_new=2. The rank change is always
`1+H_old-H_new`. The zero-extension convention includes `32→303`; no
small-length exception is needed here.

At each `0→1` arrival rho therefore equals `R-2`; at each `1→0` arrival
it equals `R-3`. If two arrivals are to the same phase and separated by
ell successful updates, then

```
rho_later - rho_earlier = ell.                        (3)
```

This is an exact law across variable-length episodes. The local rank
increases at these returns. For example, seed `20001` has successive
`0→1` arrivals `21321032` and `2132221032`, with rho increasing from 6 to 8.

The refill is unbounded, not just occasionally positive. For every k>=1,

```
3 2^(4k-1)  --0-->  (30)^(2k)3  --1-->  (3210)^k32.  (4)
```

Here exponents mean word repetition. The two formulas follow by direct
scan: the first row emits alternating `30`, and the next scan repeats
`3210`. At the switch source, R=4k+1 and H=R-1, so rho=0. At the target,
H=1 and rho=4k. These are genuine two-update histories from finite legal
frontiers. They do not violate the repeat budget: their scalar tape is `01`.

There is also an exact accounting identity. For states after emissions
1 through N, let D count repeated adjacent scalars. At each repeat put
`e=H_new-H_old-2>=0`; at each switch put `J=1+H_old-H_new`. Then

```
rho_N = rho_1 - D - SUM_repeat e + SUM_switch J.        (5)
```

This exposes the missing issue for an argument using this rank: the switch
refills need a cumulative bound. The proved descent within episodes supplies
no such control. Indeed, the abstract cycle of (phase,height) values

```
(0,2) --0--> (0,4) --1--> (1,1) --1--> (1,3) --0--> (0,2)
```

obeys every repeat and reset rule, with R increasing at each edge. Starting
at R>=5 keeps rho nonnegative forever, while two repeats accrue per cycle.
This is a sequence of abstract statistics, not a claimed Z trajectory. It
proves that the displayed local laws alone do not imply a finite repeat
budget; additional realizability information is essential.

## 3. Additive scan ranks fail on actual second images

Let M_0 be all legal finite frontiers, and M_j=Z^j(M_0). The frozen exact
image-language construction gives a 25-state DFA for M_2. These are actual
two-step images, not words admitted only by a terminal-pattern relaxation.
Also M_(j+1) is contained in M_j, so continuing an M_2 state stays in M_2.

For each fixed sector beta, consider the entire family of real-valued ranks

```
Phi_q(w) = C_q + SUM_i omega(q,h_i,w_i) + tau(q,h_final),
```

where h_i is the exact three-bit scan memory immediately before reading
w_i. All weights, constants and terminal terms are free and may differ
between the two sectors. Require

```
Phi_q(w) >= 0,
Phi_q(w)-Phi_s(Zw) >= [q=s],                          (6)
```

for every applicable word in M_2 with sector beta and preceding scalar q.
The target scalar s and appended symbol are included exactly. No initial
upper bound such as `Phi<=r-1` is imposed.

**Theorem.** No such weights exist, in either sector.

The all-word inequalities have a finite equivalent formulation. Track the
input-domain DFA, input scan memory, output scan memory for descent, and
terminal-phase pattern. Retain only vertices reachable from a legal first
symbol and able to reach an accepted endpoint. For each graph introduce
shortest-path variables p_v and inequalities

```
p_v <= first-edge cost,
p_v <= p_u + edge cost,
p_v + terminal cost >= 0.
```

Telescoping proves sufficiency. Conversely, if every accepted word has
nonnegative total cost, a reachable negative cycle with an accepted exit
is impossible. Shortest-path distances are then finite and provide the p_v.
This proves equivalence, rather than merely giving sufficient LP conditions.

The descent edge cost is `omega(q,h_i,x)-omega(s,h_o,y)`. The terminal cost
contains C_q−C_s, both terminal tau terms, the output scan's cost of reading
the appended `3-s`, and `-[q=s]`.

| Sector | Finite inequalities | Variables | Nonzero rational certificate terms |
|---:|---:|---:|---:|
| 0 | 3,462 | 1,606 | 152 |
| 1 | 3,480 | 1,618 | 104 |

Each certificate is a nonnegative rational combination of valid inequalities
that cancels every variable and yields `0>=1`. A solver-free checker
regenerates the graph rows, uses a separate local Boolean scan implementation,
and verifies every multiplier and cancellation exactly.

The limitation of this class is concrete: the sector-one certificate uses
only phase-zero nonnegativity and `0→0` descent. Thus this additive template
cannot even certify the constant-zero termination already proved by (1).
Its failure is not evidence against the repeat-budget conjecture or against
more general nonlinear ranks.

## 4. Even nonlinear functions of inverse counts and length are insufficient

For an actual image word of length R>=3, define N_up and N_down by counting
indices `1<=i<R-2` at which `a_i != a_(i-1)` and respectively
`(b_i,b_(i+1))=(0,1)` or `(1,0)`. These omit the appended symbol and the
separate origin factor. The preceding report's inverse product formula
simplifies exactly to

```
number of legal Z-predecessors = 2^(1+q+N_up) * 3^N_down. (7)
```

Each interior rise contributes a factor two, each fall a factor three;
the other admissible blocks contribute one. The origin contributes two
and the terminal high bit contributes 2^q.

There is a stronger obstruction than the earlier examples of nonmonotone
counts. Put `p=32010110`. For every k>=0 the following complete histories
exist:

| Initial frontier | First four scalars | Last transition | Counts at both endpoints |
|---|---|---|---|
| `p 0^k 101200` | `1100` | phase 0, length 17+k to 18+k | (2,5) |
| `p 0^k 2010101` | `0011` | phase 1, length 18+k to 19+k | (3,4) |

Both have sector one; the repeat source is an actual third image.

**All-length certificate.** Scanning p through four cascaded bulk updates
leaves all four memories at `(0,0,0)`. A zero at this point emits a zero in
every row and returns all four memories unchanged. Thus inserting any number
of zeros preserves all subsequent scan values, terminal guards and appended
symbols, inserting that same zero block in each genuine successor. Rows
three and four end in two zero symbols just before the insertion cut. The
new interior triples and both seams therefore preserve the crossing counts.
The two base histories and this finite loop prove both families for all k.

Consequently **no nonnegative rank depending only on
`(N_up,N_down,q,beta,R)` can drop by at least one at every repeat of either
specified phase**, even on third images. Fixing the counts, phase and sector,
the corresponding family forces `Phi(R+1)<=Phi(R)-1` for every R above its
threshold, contradicting nonnegativity. The same argument excludes strict
descent in any well-founded order. It does not exclude an arbitrary strictly
decreasing nonnegative real function such as 1/R.

This is an infinite chain of projected statistics supplied by different
finite starting frontiers. It is not an immortal frontier trajectory. A rank
retaining further spatial order, initial-length information, or history is
outside this obstruction; sufficiently older image domains are also not
settled by this third-image construction.

## 5. Verification and current boundary

Code and certificates are under `experiments/rule30/repeat-budget-rank/`.
From the project root:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python -S experiments/rule30/repeat-budget-rank/verify.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/repeat-budget-rank/phase_height.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/repeat-budget-rank/branch_pump.py
```

The first command checks the rational impossibility certificates without
Z3, NumPy or SciPy. The phase checker verifies the height, repeat descent,
switch resets, return identity and accounting balance against the frozen
engines. The branch checker verifies the exact four-layer loop, checks
22 four-update histories with insertions through length 1000, and compares
(7) with 491 distinct images obtained by exhaustive predecessor enumeration.
Source hashes and concrete witnesses are recorded in the JSON artifacts.

These are all-length theorems with finite implementation checks. None bounds
the total switch refill in (5), and none refutes `D<=r-1`. The work identifies
which state information these candidate ranks discard and gives an exact
formula for the replenishment a cumulative argument using this rank must
account for.

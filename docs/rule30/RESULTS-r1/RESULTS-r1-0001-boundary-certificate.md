# Driven 0001: an exact boundary certificate with one unresolved bit

**Status:** an invariant union of three four-cell prefix cylinders for a
periodically driven right half-line. The zero-initial trajectory enters
this union at time eight. No eventual lock, mismatch upper bound, or
Rule 30 prize result is proved.

The [older driven-halfline report](RESULTS-lock-driven-halfline.md#3-k1-fired-58-of-69-drives-do-not-lock)
measures a period-four neighbour under drive 0001. The
[R1 inventory](../../experiments/rule30/p1-period2-invariant/RESULTS-R1-ZERO-SET-INVENTORY.md)
also records periodic outputs for this drive under several prefixes. Those
remain finite observations. The certificate here proves only the smaller
phase constraint stated below. A targeted search of those reports and the
R1 result documents found no earlier statement of this three-state table;
no literature-priority claim is made.

## 1. Domain, timing, and finite certificate

Use Rule 30 on sites i>=1 with prescribed boundary c_t=s(t,0):

\[
s(t+1,i)=s(t,i-1)\mathbin\oplus
          (s(t,i)\mathbin\lor s(t,i+1)),\qquad
c=(0001)^\infty.
\]

The initial right row is all zero. No rule equation is imposed at site zero,
and no left half-plane or left PIN condition is assumed. Strings below list
sites 1,2,... from left to right. Let

```text
A = 0010,    B = 0011,    C = 0111.
```

At a block time divisible by four, suppose the first four right cells form
one of these words. Let (a,b) be the current cells (s(t,5),s(t,6)). The next
four drive values are 0,0,0,1. Their exact effect is:

| Current prefix | Condition on (a,b) | Prefix four steps later | Neighbour values during the four steps |
|---|---|---|---|
| A | 01 | B | 0011 |
| A | 00, 10, or 11 | A | 0011 |
| B | 00 | A | 0011 |
| B | 01, 10, or 11 | C | 0011 |
| C | 00 | B | 0111 |
| C | 01, 10, or 11 | A | 0111 |

**Complete finite proof.** In four radius-one updates, the returned first
four cells and the four neighbour observations depend only on the initial
first eight cells and the prescribed drive. The literal eight-entry Rule 30
truth table, evaluated on all three prefixes and all sixteen possible
four-bit exterior words, gives the table: **48 complete cones**. A second
packed implementation agrees on every returned prefix and every observation.
The calculation also verifies that exterior cells seven and eight cancel
from this table. Cells beyond eight cannot influence these outputs.

Thus [A] union [B] union [C] is mapped into itself by the four-step driven
map, for every infinite continuation. Iterating this inclusion proves the
all-time assertion. At each iteration the actual tail is used; no independence
or free choice of future exterior values is asserted.

For the zero-initial trajectory, pack site i into bit i-1. Its full finite
right rows at times 0,...,8 are exactly

```text
0, 0, 0, 0, 1, 3, 5, 13, 20.
```

The row at time eight therefore starts A=0010. Independent scalar and packed
evolution verify these eight entrance steps. No longer simulation is used
to justify the invariant.

## 2. One free zero-phase bit remains

Write r_t=s(t,1). For every k>=2 define e_k=1 when the prefix at time 4k
is C, and e_k=0 when it is A or B. The certificate proves

\[
\boxed{(r_{4k},r_{4k+1},r_{4k+2},r_{4k+3})=(0,e_k,1,1).}
\tag{1}
\]

Also e_k e_(k+1)=0, since C cannot be followed by C. Two of the three
centre-zero phases are fixed; only the phase 4k+1 remains unresolved.

This is not an autonomous three-state evolution: its transition still reads
cells five and six. Nor is e an autonomous binary evolution. Treating those
two exterior cells as independently selectable at successive blocks would
enlarge the dynamical system and would not describe the zero-initial orbit.
The observed period-four lock would require e to be eventually constant;
the no-adjacent-ones property would then force that constant to be zero.
No proof of this property of the actual e is supplied.

The [observer-collision certificate](RESULTS-r1-0001-observer-collision.md)
now refutes one proposed closure: the eight-cell prefix seen at time eight
admits two finite continuations with identical first five observer samples
and different sixth samples. The [onset-basin certificate](RESULTS-r1-0001-onset-basin.md)
extends entry to this invariant to specified nonzero initial right prefixes
and all drive phases, without proving periodicity of the residual bit.

## 3. Exact period-multiple mismatch reduction

Keep the period-multiple quantifier in the
[origin-preserving mismatch target](RESULTS-r1-periodic-realization-scope.md#4-consequence-for-the-zero-set-obligation).
For any q>=1 and N, define

\[
M_{4q}(N)=\#\{8\le t<N:c_t=0,\ r_{t+4q}\ne r_t\}.
\]

Equation (1) gives the exact identity

\[
\boxed{M_{4q}(N)=\sum_{\substack{k\ge2\\4k+1<N}}
                   \mathbf1\{e_{k+q}\ne e_k\}.}
\tag{2}
\]

Thus an o(log N) upper bound for this drive at some fixed period multiple
reduces to an o(log K) shift-mismatch bound for e at some fixed q. Neither
bound is established. Nonzero mismatch counts at q=1 would not exclude a
successful bound at another q. An eventual period q of e would make (2)
bounded, but eventual periodicity is stronger than the proposed sublogarithmic
target.

The logarithmic lower bound from the cited report applies after adjoining a
compatible finite-left history and enforcing the centre equation. It cannot
be imposed on this independently driven half-line without those hypotheses.

## 4. The zero boundary at time zero is a real scope distinction

Here c_0=0, so this is not the actual singleton centre, whose first bit is
one. The right row stays zero through time three. Shifting this driven
experiment by three steps gives the equivalent right-half experiment with
zero initial right row and boundary (1000)^infinity, beginning with a one.
That delayed injection / phase rotation does not repair centre compatibility:
if the left row is also initially zero, PIN at the new time zero requires
l_0=1 XOR c_1=1, but l_0=0. It already fails its first left pin.

Accordingly, this certificate is a control and an exact reduction for the
specified driven family. It proves no assertion for arbitrary finite
prefixes before the periodic drive, the actual singleton centre, or the
eventual-period candidates satisfying the left PIN.

## 5. Reproduction

```sh
uv run --no-project python experiments/rule30/r1_0001_boundary_certificate_audit.py \
  --output experiments/rule30/r1-0001-boundary-certificate-audit.json
```

The [standard-library verifier](../../experiments/rule30/r1_0001_boundary_certificate_audit.py)
contains no imports from the earlier driven-halfline implementations. Its
scalar cone calculation shrinks the available row at each step, so no
artificial exterior boundary enters the checked cone. The
[JSON record](../../experiments/rule30/r1-0001-boundary-certificate-audit.json)
retains every exterior assignment, returned prefix, and observation, together
with the zero-initial entrance states. Only these bounded checks are run.

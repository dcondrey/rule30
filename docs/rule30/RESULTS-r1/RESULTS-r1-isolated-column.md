# R1: the isolated-periodic-column obstruction

Date: 2026-09-09.

**Intermediate result. R1 remains open. No proof of P1 and no Rule 30 killing
diagram is claimed. The active task continues until a proof or a kill of R1;
this report is not its final deliverable.** The attempted construction was a travelling spatial
data channel with a periodic centre and a non-eventually-periodic neighbour
on the centre's zero set. It fails for a uniform reason: **any such killing
diagram must have exactly one eventually periodic spatial column**. A rigid
spacetime translation supplies a second one and therefore cannot work.

The smallest local failure of the proposed period-two channel is the
two-data-bit rise `01`, with complete physical cone

```text
00010 -> 011 -> 1.
```

The required return value was zero. OR-saturation turns the proposed freely
chosen data into a monotone sequence: only constants and one spatial domain
wall survive. This is an exact obstruction to the attempted construction,
not a finite census used to infer an asymptotic claim.

| Statement | Evidence |
|---|---|
| Two eventually periodic boundary columns force the intervening finite strip eventually periodic | `U`, elementary deterministic finite-state proof |
| An R1-killing Rule 30 diagram has exactly one eventually periodic spatial column | `U/R`, finite-strip lemma plus the pin/pass identity |
| No rigid travelling-wave diagram can kill R1, for any temporal period or spatial displacement | `U/K`, uniform obstruction to this construction class |
| Interleaved period-two data channel satisfies its translation identity iff its data avoid `01` | `U/C`, symbolic identity; all eight Boolean triples checked independently |
| Rule 90's actual lone seed has exactly one eventually periodic column | `U/C`, explicit all-scale formulas; numerical regression to t=4096 |
| R1, existence of a Rule 30 isolated-periodic-column diagram, and P1 | **Open here** |

The finite-state lemma is elementary; no literature novelty is claimed.
Its use here is to close a proposed countermodel construction and identify
the specific hypothesis that a replacement construction must avoid.

The subsequent [periodic-cylinder result](RESULTS-r1-periodic-cylinders.md)
proves that finite right prefixes can force periodic neighbours for every
infinite tail. It refutes the proposed global no-periodic-cylinder premise;
it does not refute R1 or establish that all right rows enter those basins.

## 1. The exact obligation retained after reading the route map

Write `c_t=s(t,0)`, `l_t=s(t,-1)`, `r_t=s(t,1)`, and define the masked
zero-set observation

```text
z_t = (1-c_t) r_t.
```

For eventually periodic `c`, eventual periodicity of its zero-set sampled
neighbour is equivalent to eventual periodicity of `z`. Periods can always
be enlarged to a common multiple of the period of `c`. Thus the live R1
obligation permits an arbitrary multiplier:

```text
c_(t+p)=c_t eventually
  => there exist h>=1 and T such that
     c_t=0 => r_(t+hp)=r_t for every t>=T.
```

Requiring `h=1` is a stronger target. The existing 7-by-4 torus, independently
rechecked here, has rows

```text
0000001
1000011
0100110
1111101
```

With the leftmost displayed coordinate designated column zero,
`c=0101`, `r=0011`, `l=1101`, and the zero-set samples are `01`, all repeated.
All **28 cyclic local updates** are correct. This prior witness refutes
same-period inheritance for arbitrary diagrams; it does not refute R1.

There is a second quantifier distinction. PATH's literal kill condition
allows an arbitrary full diagram. A kill of that diagram-wide assertion
would obstruct the proposed general route; it would not logically refute
the remaining implication restricted to finite rows or the lone-seed orbit.
The finite-support hypothesis is required in the Jen/Kopra conclusion used
by the P1 chain. It cannot be applied to arbitrary infinite-left examples.

The original a7 infinitely-often assertion is already settled by the prior
five-zero theorem. The stronger aperiodicity requirement remains

```text
for every h>=1 and N, some n>=N satisfies rho_(n+h) != rho_n.
```

These distinctions are established in the
[rung-3 audit](RESULTS-ladder-rung3-io-and-aperiodicity-audit.md), not new
claims of this arm. The terminal-period family excluded in the previous
[seam report](RESULTS-family-seam.md) settles neither this assertion nor R1.

## 2. The periodic-enclosure lemma (`U`)

**Lemma.** In a binary radius-one cellular automaton, suppose columns `a<b`
are eventually periodic. Let `L` be a common period and choose a time `T`
after which both boundary columns have that period. Put `m=b-a-1`.
Every intervening column is eventually periodic with period `L*d`, for
some `1<=d<=2^m`, after at most `L*(2^m-1)` further steps.

**Proof.** At times `T+nL`, retain the entire `m`-bit row between the two
boundary columns. Its next `L` updates are determined by that row and by
the two specified boundary words. The same deterministic map on `2^m`
states is used at each strobe. Its trajectory has a preperiod `mu` and
cycle length `d`, with `mu+d<=2^m`. Repeating the same boundary inputs
also repeats the intermediate rows within every `L`-step block. Therefore
the whole strip is `L*d`-periodic after time `T+mu*L`. For `m=0` the
interior is empty and the assertion is vacuous. ∎

The boundary columns are **assumed actual, eventually periodic columns**.
No argument here obtains them from a bounded window of centre history, or
replaces an unconstrained exterior by a periodic one. This distinction is
the exact point on which the obstruction rests.

## 3. The isolated-periodic-column obstruction (`U/R`)

**Proposition.** If a Rule 30 diagram has eventually periodic centre and
some other eventually periodic column, its zero-set neighbour is eventually
periodic.

**Proof.** If the other column is at `a>0`, apply the lemma between columns
zero and `a`. Column one is either that boundary itself or lies inside the
periodic strip. Hence `r` and therefore `z` are eventually periodic.

If `a<0`, the same argument makes `l` eventually periodic. The exact Rule 30
identity is

```text
l_t = c_(t+1) XOR (c_t OR r_t),
z_t = (1-c_t) (l_t XOR c_(t+1)).
```

The second equality is the pin/pass identity restricted to centre-zero
times. The right side is a function of eventually periodic sequences, so
it is eventually periodic. ∎

**Necessary condition for a kill.** A full diagram with eventually periodic
`c` and non-eventually-periodic `z` has exactly one eventually periodic
spatial column: column zero. All columns at nonzero positions must fail
eventual periodicity.

This is not the missing R1 theorem. The attempted positive inference stops
at the exact step

```text
periodic c  ?=>  another periodic column at some finite nonzero distance.
```

That implication has not been proved. Assuming it would assume a sufficient
replacement for the original obligation. The finite-state lemma gives no
reason for an unconstrained farther column to become periodic.

## 4. Why every rigid travelling-wave countermodel fails (`U/K`)

The proposed ansatz was an actual diagram satisfying, eventually,

```text
s(t+p,j) = s(t,j-q),        p>=1, q an integer,
```

with a periodic centre and a spatial data stream intended to make the
neighbour aperiodic. No finiteness or locality assumption on the initial
data is needed for the following obstruction.

For `q!=0`, set `j=0`:

```text
s(t,-q) = c_(t+p).
```

The centre's eventual periodicity therefore supplies a second eventually
periodic column. Section 3 excludes an aperiodic zero-set neighbour. For
`q=0`, every column is already eventually `p`-periodic. Thus **no rigid
spacetime translation, at any displacement or period, can fire R1's kill**.

This is a fundamental obstruction within the stated ansatz. It is not an
obstruction to non-rigid defects, changing scales, or a full diagram with
an isolated periodic centre. Nor does it assert that periodic centres in
general imply a rigid translation.

## 5. Exact failure of the proposed data lane (`U/C/K`)

The first concrete test used the right-moving comoving map

```text
H30(y)_i = F30(y)_(i+1) = y_i XOR (y_(i+1) OR y_(i+2)),
y_(2n)=0,  y_(2n+1)=u_n.
```

The translation gate was `H30^2(y)=y`, equivalent to
`F30^2(y)_i=y_(i-2)`. Under that gate, even-time centre samples would be
zero; a full periodic centre would also require checking its odd-time
samples. The construction was rejected at the translation gate, before
claiming that the latter condition held.

Direct Boolean calculation gives

```text
H30^2(y)_(2n)   = (1-u_n) u_(n+1),
H30^2(y)_(2n+1) = u_n XOR ((1-u_(n+1)) u_(n+2)).
```

Consequently the translation identity holds **if and only if**
`u_(n+1)<=u_n` at every position. The even outputs prove necessity; the
same inequalities make every odd correction vanish, proving sufficiency.
A bi-infinite binary sequence with this property is constant or has one
`1 -> 0` interface. A spatial domain wall is not globally periodic, but
either ray is eventually constant; it cannot transmit the required
non-eventually-periodic data past a fixed column.

The smallest forbidden data pattern is the two-bit rise `01`:

| u_n u_(n+1) | H30^2(y)_(2n) |
|---|---:|
| 00 | 0 |
| 01 | 1 |
| 10 | 0 |
| 11 | 0 |

Its complete physical cone is `00010 -> 011 -> 1`, contradicting the
required original value zero. Minimality is **within this ansatz**: a
single data bit cannot witness a rise; two adjacent bits suffice. Five
physical cells are the complete two-step dependency window of `H`.
No minimality among other R1 constructions is asserted.

Both formulae were independently checked on all **eight** assignments to
`(u_n,u_(n+1),u_(n+2))`. A separate 32-word check of `H30^2(y)=y` gives
20 legal de Bruijn edges. The only recurrent vertices are `0000`, `0101`,
and `1010`, forming the zero cycle and checkerboard two-cycle. These exact
small checks validate the construction's failure; larger comoving-period
counts are unnecessary after section 4 and are not used as evidence here.

## 6. Rule 90 control: the obstruction leaves the real countermodel intact

The finite-strip lemma is rule-generic. Therefore it **cannot itself be
a proof of R1**. Its completed use here is a limitation on countermodel
constructions. The genuine Rule 90 lone seed satisfies the resulting
necessary condition exactly.

**Proposition (`U`).** The Rule 90 lone-seed centre is eventually zero,
and every fixed nonzero spatial column is not eventually periodic.

**Proof.** Represent a row over GF(2) by a Laurent polynomial. The row at
time `t` is `(X+X^(-1))^t`. The centre coefficient is zero for odd `t`;
for positive even `t=2v`, it is `binomial(2v,v)`, which is even. Thus the
centre is one at time zero and zero thereafter.

Fix `a=|j|>0`. For each `n` with `2^(n-1)>=a`, the cell at column `j`
is one at time `2^n-a`. By reflection it suffices to take `j=a`; its
coefficient is `binomial(2^n-a,2^(n-1))`, which is odd. Indeed, the binary
factorization `(1+X)^t=product_(b:bit_b(t)=1)(1+X^(2^b))` shows that this
coefficient is the highest binary bit of `t`.

For `0<=v<2^n-a`,

```text
(X+X^(-1))^(2^n+v)
 = (X^(2^n)+X^(-2^n)) (X+X^(-1))^v.
```

The two shifted supports miss `j`. Hence the entire interval
`2^n <= t <= 2^(n+1)-a-1` is zero at column `j`. There are infinitely
many ones and arbitrarily long zero intervals, incompatible with any
eventually periodic binary sequence. ∎

In particular, column one is one **exactly** at `t=2^n-1`, `n>=1`.
For odd `t=2v+1`, its coefficient is `binomial(2v+1,v+1)`, odd exactly
when the binary expansions of `v` and `v+1` have no common one-bit; this
is equivalent to `v=2^k-1`. Even times give zero by parity.

The numerical control checks times **0 through 4096**, columns **-16
through 16**, including **286** complete or horizon-truncated zero blocks
and the exact column-one support. The all-scale conclusion comes from the
symbolic proof, not those observations. The unchanged
`controls.rule90_control(6)` passes at `T=2,4,6` as well.

The specific lane calculation also changes under Rule 90:

```text
H90(y)_i = y_i XOR y_(i+2),
H90^2(y)_(2n)=0,
H90^2(y)_(2n+1)=u_n XOR u_(n+2).
```

Its rigid two-step return would force `u=0` globally. The actual Rule 90
lone seed does not satisfy that rigid-return hypothesis. Neither this
lane failure nor periodic enclosure rejects the real Rule 90 diagram.

## 7. Verification, filters, and reproduction

All computation is in the new directory
[r1-isolated-column](../../experiments/rule30/r1-isolated-column/).
[verification.json](../../experiments/rule30/r1-isolated-column/verification.json)
contains the exact truth tables, graph edges, torus rows, control windows,
and frozen-source hashes.

As a finite calibration of the strip implementation, both rules were
checked for interior widths `0,...,5`, boundary periods `1,...,3`, every
pair of boundary words, and every initial strip row:

| Rule | Stroboscopic maps | Initial rows across maps | One-step evaluations | Bound violations |
|---|---:|---:|---:|---:|
| 30 | 504 | 5,292 | 14,364 | 0 |
| 90 | 504 | 5,292 | 14,364 | 0 |

The uniform strip lemma is proved in section 2; these are bounded
implementation checks, not its proof by extrapolation. The scalar Rule 30
and Rule 90 tables are checked against unchanged `ladder.FWD` and `INV`.

No bounded centre-history predictor is proposed. The strip is closed only
after assuming a second actual periodic boundary; supplying that boundary
from the centre alone remains unresolved. No spatially averaged statistic
or proposed P1-deciding quantity is introduced, so there is no geometric
statistic to run through the single-column-sensitivity discriminator.
The analysis does not evade that filter by changing a normalization.

A source wording issue was also checked but is **not counted as an R1
obstruction**: the front lemma tracks the rightmost discrepancy, not the
number of discrepancies. The all-zero row and a lone one differ after
one update at `{-1,0,1}` under Rule 30, not at one site. The source's
subsequent “leftmost” corollary needs “rightmost.” The finite-speed local
indistinguishability argument and the requirement for a nonlocal P1
certificate remain intact; this arm does not pursue fixed-radius closure.

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run --with numpy python experiments/rule30/r1-isolated-column/verify.py
```

The symbolic derivations were reviewed independently by separate agents.
The check script and report are new; PATH, the previous reports, and the
frozen engines were not edited. In particular, `ladder.py` retains
SHA-256 `589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.

## 8. Honest scope and the named unresolved step

**Fundamental within the attempted class:** a rigid travelling diagram
with periodic centre cannot have an aperiodic zero-set neighbour, at any
period or displacement. A construction using a second fixed periodic
column as an enclosing boundary has the same obstruction. The period-two
interleaved channel additionally fails at the exact `01` data seam.

**Unresolved outside it:** whether Rule 30 admits a full diagram with an
isolated eventually periodic centre and a non-eventually-periodic masked
neighbour; and whether the finite-support/lone-seed hypothesis rules out
such isolation. No bounded test here decides either question.

The missing step is therefore **isolated-column realization or exclusion**,
not stronger checking of a periodic enclosure. No R1 kill was obtained;
the program is not redirected to the cascade fallback. No P1, P2, P3, or
new q=420 conclusion follows.

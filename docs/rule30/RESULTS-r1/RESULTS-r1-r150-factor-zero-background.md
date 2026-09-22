# Rule 150 source and the necessary zero-background theorem

Date: 2026-09-09. Evidence: **U** (uniform symbolic results), **C**
(independent finite calibrations), **R** (remaining construction problem).
This is an intermediate result. It proves neither R1 nor its kill
condition. The subsequent
[doubling-latch theorem](RESULTS-r1-doubling-latch-recurrence.md) uses this
necessary condition to exclude the whole stated finite-factor class.

## 1. The source has a suitable bounded-gap aperiodic neighbour (U)

Let `z(t,x)` be the lone-seed Rule 150 diagram on the full integer line.
Over `F_2`, its row polynomial is

\[
 (u^{-1}+1+u)^t.
\]

The characteristic-two squaring identity gives, for every `t>=0` and
integer `x`,

\[
 z(2t,2x)=z(t,x),\qquad z(2t,2x+1)=0,
\]
\[
 z(2t+1,2x)=z(t,x),\qquad
 z(2t+1,2x+1)=z(t,x)\oplus z(t,x+1).
\]

The centre therefore satisfies `z(t,0)=1` for all time. If
`r_t=z(t,1)`, then

\[
 r_{2n}=0,\qquad r_{2n+1}=1\oplus r_n,
 \qquad r_t=v_2(t+1)\pmod 2.
\]

In particular,

\[
 r_{4n+1}=1,\qquad r_{4n+3}=r_n.
\]

The ones have gaps at most 4. The sequence is not eventually periodic:
an odd eventual period would transfer every sufficiently late even-index
zero to the odd indices, contradicting the infinitely many ones at
`4n+1`. If `2q` were an eventual period, applying it at sufficiently late
odd indices and using `r_(2n+1)=1 xor r_n` would make `q` an eventual
period. Removing all powers of 2 from a proposed period yields the
impossible odd case.

Thus copying or complementing the source neighbour on target times
`4n+3`, while fixing the target centre to zero at those times, would
produce an aperiodic restriction of the target neighbour to the target
centre's zero set. This remains conditional on constructing an actual
Rule 30 factor with those properties.

The source does not itself kill R1: its centre is constantly 1, so its
centre's zero set is empty. It also does not satisfy Rule 30's OR pin.

## 2. Precise factor class and mechanism

Fix any finite radius `R`. A candidate in the class considered here is
a lookup family

\[
 s(t,x)=\phi_{t\bmod4,\,x\bmod14}
       \bigl(z(t,x-R),\ldots,z(t,x+R)\bigr),
 \tag{1}
\]

such that `s` is an actual Rule 30 diagram for every `t>=0` and every
integer `x`. The lookup may depend arbitrarily on the full local source
window. No rule for other source initial conditions is assumed.

Define its zero-input background by

\[
 B(t,x)=\phi_{t\bmod4,\,x\bmod14}(0,\ldots,0).
\]

All-zero source windows occur arbitrarily far outside the finite source
cone, at every time and every spatial residue. Equation (1)'s actual
Rule 30 updates there therefore imply that `B` itself is a Rule 30
diagram, with time period dividing 4 and space period dividing 14.

**Theorem (U).** If `s` is not identically its background `B`, then
`B` is identically zero. This holds for every finite radius `R`; it is
not an extrapolation from radius-1 or radius-2 synthesis.

The mechanism is the position of the leftmost discrepancy from the
background in moving coordinates. Its range grows with the full defect
cone. An infinite sequence of sparse, scaled source rows bounds that
position; OR saturation then forces a zero diagonal in the background.
The period-4/space-14 arithmetic forces this background to be all zero.
This theorem is a necessary restriction on a construction. Excluding
finite Rule 30 replicators over that zero background requires the separate
doubling-latch theorem cited above.

## 3. Proof of the necessary zero-background theorem (U)

### 3.1. A finite nonempty initial discrepancy and its rightmost front

Let

\[
 D_t=\{x:s(t,x)\ne B(t,x)\}.
\]

The source initially consists of a single 1, so `D_0` is contained in
`[-R,R]`. It is nonempty: otherwise determinism would give `s=B` for all
future times. Set `b=max D_0`.

Rule 30 is left-permutive. At the position immediately to the right of
the rightmost discrepancy, only the left input differs; the two outputs
there differ. All still farther outputs agree. Consequently

\[
 \max D_t=b+t\qquad\hbox{for every }t\ge0.
 \tag{2}
\]

In particular, the discrepancy never becomes empty.

### 3.2. Scaled source rows force the leftmost seed copy to survive

Let `L=2^m>2R`, with `m>=2`. For any integer `n>=1`, repeated squaring
gives

\[
 z(nL,x)=
 \begin{cases}
 z(n,x/L),&L\mid x,\\
 0,&L\nmid x.
 \end{cases}
\]

The extremal source cells at `-nL` and `nL` are 1, and all source ones
at this time are separated by at least `L`. The output discrepancy is
therefore a union of disjoint finite clusters, one around each source
1. The relative cluster profile lies in `[-R,R]` and depends only on
the source cell's spatial residue modulo 14: the time phase is 0 and
each source cell is isolated from all the others. Call this profile
`P_a`, where `a` is that spatial residue. Some profiles could initially
be empty; their nonemptiness must be proved.

By (2), the target discrepancy at `b+nL` exists. It lies in the cluster
centred at the rightmost source cell `nL`, because every other cluster
ends at most at

\[
 nL-L+R<nL-R\le nL+b.
\]

Thus `P_(nL mod14)` contains relative offset `b`, for every `n>=1`.
Taking `n=13`, which is `-1 mod14`, proves that `P_(-L mod14)` contains
that offset. At time `L`, the source row has ones at `-L,0,L`, so this
same profile occurs around its leftmost seed. Hence

\[
 \min D_L\le -L+b.
 \tag{3}
\]

The use of scaled times `13L` closes the possible disappearing-left-copy
loophole. Spatially dependent lookup tables need not treat positive and
negative seed positions alike; (2) supplies the needed nonemptiness.

### 3.3. The moving leftmost discrepancy stabilizes

Set

\[
 \lambda(t)=\min D_t+t.
\]

The radius-one propagation bound makes `lambda(t)` nondecreasing. By
(3), `lambda(2^m)<=b` for every sufficiently large `m`. Since these times
are unbounded, monotonicity bounds the entire sequence above by `b`.
It is integer valued and bounded below by `min D_0`, so it eventually
stabilizes at an integer `A`.

Use moving coordinates

\[
 S^K(t,x)=s(t,x-t),\qquad B^K(t,x)=B(t,x-t).
\]

Their common update is

\[
 K(a)_x=a_{x-2}\oplus(a_{x-1}\lor a_x).
\]

For all sufficiently large `t`, the leftmost discrepancy between these
two rows is exactly at `A`. The two positions to its left agree, so the
difference in the next output at `A` is

\[
 \delta_{t+1}(A)=
 \bigl(1-B^K(t,A-1)\bigr)\delta_t(A).
\]

Both discrepancies displayed here equal 1. Therefore
`B^K(t,A-1)=0` for every sufficiently large `t`. The background in moving
coordinates is time-periodic with period dividing 28, so this fixed
zero column holds for every time.

### 3.4. Period arithmetic propagates the zero to the whole background

The laboratory time period 4 gives

\[
 B^K(t+4,x)=B^K(t,x-4).
\]

A fixed zero column at `x=A-1` therefore forces, at each time, zeros
at every position in that residue class modulo `gcd(4,14)=2`. Thus one
entire spatial parity class is zero at all times. At a position `x` in
that parity class, the `K` update reduces to

\[
 B^K(t+1,x)=B^K(t,x-1),
\]

because positions `x-2` and `x` are zero. Its left side is zero, so the
opposite parity class is also zero. Hence `B^K`, and therefore `B`, is
identically zero, proving the theorem.

## 4. Rule 90 filter and independent verification (C)

The proof's front-to-zero step is specific to the OR rule. For Rule 90,
the moving update is `K_90(a)_x=a_(x-2) xor a_x`; a leftmost discrepancy
persists independently of the intervening background bit. For example,
the triples `010` and `011` both map to 1 under Rule 30, but map to 0
and 1 under Rule 90. Thus persistence does not force a zero diagonal in
Rule 90.

An independent verifier uses scalar truth-table evolution of Rule 150
through time 255. It checks 131,584 instances of the four dyadic
identities, 256 centre/valuation identities, and 64 instances of the
phase-3 self-copy. These are finite calibrations; the all-time identities
and aperiodicity follow from section 1's symbolic proof.

For the final parity step, it checks all 128 assignments to the other
parity class of a 14-cell row. Only the all-zero assignment preserves
the zero parity after the Rule 30 moving update; all 128 preserve it
under Rule 90. The unchanged `controls.rule90_control(6)` is also run:
its `T=2,4,6` checks all pass.

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/r1-r150-factor/verify_uniform_lemmas.py
```

The exact output is
[uniform-lemmas-verification.json](../../experiments/rule30/r1-r150-factor/uniform-lemmas-verification.json).
The mathematical front argument was independently audited before this
report was finalized. The scripts do not modify the frozen engines.

## 5. Remaining obligation and scope (R)

For this exact factor class, synthesis may soundly fix every zero-source
lookup value to 0. A successful nontrivial factor would start from an
actual finite Rule 30 configuration, and the full orbit would reproduce
separated finite output clusters at the scaled source times. This theorem
alone does not exclude such a finite replicator; the
[dyadic population corollary](RESULTS-r1-doubling-latch-recurrence.md)
supplies that additional step and excludes this entire factor class.

The Rule 150 reset retains a seed at the centre of every dyadic row.
Thus the earlier Rule 90 argument based on an entirely periodic central
reset profile cannot simply be reused. The proof above handles the
retained finite defect and yields the necessary zero-background condition
used by that additional argument.

No bounded history of the proposed periodic centre is used to determine
its neighbour. No averaged geometric statistic is proposed. The
nonlocal quantity is the position of the leftmost discrepancy in the
entire expanding finite support, and its bound uses infinitely many
scaled times proved symbolically. The result neither proves R1 nor
constructs its required periodic-centre/aperiodic-zero-set-neighbour
counterexample.

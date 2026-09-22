# An all-length error wedge for the actual Newton iterates

Date: 2026-09-14. **Proved:** after \(k\) complete Newton rounds initialized
from the singleton row alone, every center bit at a time \(n<2k\) is exact.
This concerns the actual sequence of Newton approximations. It improves the
previous sufficient schedule of \(n\) rounds to \(\lfloor n/2\rfloor+1\)
rounds for a center query, but gives no sublinear algorithm or lower bound
on the number of rounds required. Problem 3 remains open.

Verifier: [p3_newton_error_wedge.py](../../experiments/rule30/p3_newton_error_wedge.py).
Artifact: [p3-newton-error-wedge.json](../../experiments/rule30/p3-newton-error-wedge.json).
The older [Newton experiment](RESULTS-p3-global-newton.md) is preserved and
its saved schedule is not rerun.

## 1. The initialized sequence and its error equation

Use moving coordinates \(r_{t,j}=u_{t,t-j}\), so the actual row polynomial

\[
r_t(X)=\sum_{j\ge0}r_{t,j}X^j
\]

has support in \([0,2t]\), and its coefficient at \(j=t\) is the center
bit. All additions below are over \(\mathbb F_2\). Spatial products marked
\(\odot\) are coefficientwise; multiplication by \(X\) shifts indices.

Let \(a^{(0)}_0=1\) and \(a^{(0)}_t=0\) for \(t>0\). Each complete Newton
step uses its entire previous approximation as reference and solves forward
from the correct initial row, exactly as in the older report. Write
\(e_t=a_t+r_t\) for its old error and \(d_t=v_t+r_t\) for its new error.
The old report's exact error equation, in these coordinates, is

\[
d_0=0,\qquad d_{t+1}=J(a_t)d_t+X(e_t\odot Xe_t),                 \tag{1}
\]

where

\[
J(a)d=(1+X+X^2)d+X(a\odot Xd+d\odot Xa).
\]

At a single output index \(j\), this is

\[
d'_{j}=d_j+(1+a_{j-2})d_{j-1}+(1+a_{j-1})d_{j-2}
                   +e_{j-1}e_{j-2}.                            \tag{2}
\]

Negative indices are zero. No assumption on the support or values of the
reference \(a_t\) is needed for the following support argument.

## 2. The error-wedge theorem

For every round \(k\ge0\) and time \(t\ge0\),

\[
\boxed{\operatorname{supp}(a^{(k)}_t+r_t)
                  \subseteq[\,2k,\;2t-k\,].}                  \tag{3}
\]

An interval with its lower endpoint above its upper endpoint is empty.
The equivalent physical-coordinate interval is \([k-t,t-2k]\).

**Proof.** Round zero satisfies (3) because the singleton cone is
\([0,2t]\); its time-zero error is zero. Suppose round \(k\) satisfies
(3). Induct on time to prove the statement for round \(k+1\), starting
with its zero error at time zero. At time \(t\), put \(L=2k\) and
\(U=2t-k\). The old error has support in \([L,U]\); the induction in time
places the new error in \([L+2,U-1]\).

The three shifts in \(J(a_t)d_t\) are by zero, one and two, so this term
has support in \([L+2,U+1]\). Multiplication by arbitrary coefficients
of \(a_t\) can only remove terms. The adjacent-product source in (2)
also has support in \([L+2,U+1]\): it requires both \(j-1\) and \(j-2\)
to belong to \([L,U]\). Consequently the new error at time \(t+1\) has
support in

\[
[L+2,U+1]=[\,2(k+1),\;2(t+1)-(k+1)\,],
\]

which closes both inductions. The same argument covers empty intervals.

The contraction is asymmetric. One Newton round removes two moving-index
columns from the low end of the possible error cone and one from the high
end. It does not double temporal precision.

## 3. Exact center and whole-row schedules

The center at time \(n\) has moving index \(j=n\). It lies below the error
wedge whenever \(n<2k\). The entire row is exact whenever the wedge is
empty, that is, \(2n<3k\). Therefore, for \(n\ge1\), sufficient schedules
are

\[
k_{\rm center}(n)=\lfloor n/2\rfloor+1,\qquad
k_{\rm row}(n)=\lfloor2n/3\rfloor+1.                           \tag{4}
\]

At \(n=0\), return the seed bit 1 without a Newton solve. These are proved
upper bounds, not claims that the first error reaches the wedge boundary
or that a smaller schedule cannot work.

The verifier supplies a callable `newton_center(n)`: construct the
singleton-only approximation through time \(n\), perform the first
schedule in (4), and read the center of its last row. Its finite window
has two spare cells on each side of the complete causal cone, so truncation
does not alter the query or the proof. No true later row is supplied to the
algorithm. The local Newton formula and (3) prove its correctness for every
input \(n\); verification does not rerun the old numerical schedule.

This is not a fast P3 algorithm. In the materialized scalar implementation,
one round visits \(n(2n+5)\) cells. The resulting sufficient center schedule
uses \(O(n^3)\) scalar cell work and \(O(n^2)\) stored bits. Packed shifts,
allocation, counters and operand sizes remain charged under the
[P3 query model](P3-SCOPE-AUDIT.md). Direct simulation already has a better
materialized work bound. The useful result here is a universal convergence
invariant for the actual iterates, not an implementation improvement over
direct simulation.

## 4. What the leading edge still needs

At the lowest possible error index of round \(k\ge1\), equation (2)
reduces exactly to

\[
e^{(k)}_{t+1,2k}=e^{(k)}_{t,2k}
 +e^{(k-1)}_{t,2k-1}e^{(k-1)}_{t,2k-2}.                       \tag{5}
\]

Thus this edge is a prefix parity of the two preceding error columns.
It is not an independent finite-state recurrence: updating the next
column still involves coefficients of the actual reference approximation.
No rule is proved that obtains those histories or their requested parity
in sublinear total work. In particular, (3) supplies neither a lower bound
on the center convergence rate nor a logarithmic-round guarantee.

## 5. Exact validation and finite consistency

The new verifier checks (2) against independently constructed Boolean
truth-table derivatives for all 512 choices of reference, actual and
updated triples. It separately checks the six symbolic monomials of (2)
against the arbitrary-endpoint interval template in the proof, and
rejects two corrupted support templates. The latter check verifies the
local all-length induction step; it is not a finite fit to iterates.

It then reads the already saved 33 diagnostics, rounds 0 through 32 on
horizon 128, and checks that each recorded first wrong row and first wrong
center is consistent with (3). Those observations are finite consistency
checks only. The new artifact hashes the report, verifier and saved
dependency. The older files are not modified, and no center census,
schedule extension or orbit regeneration is performed.

```
uv run --offline --no-project python experiments/rule30/p3_newton_error_wedge.py
```

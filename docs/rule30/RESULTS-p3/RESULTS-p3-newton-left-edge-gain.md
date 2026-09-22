# One extra left-edge column for the actual Newton iterates

Date: 2026-09-14. **Proved:** for every actual initialized Newton round
k>=3, its error at time t has moving-index support inside

```
[2k, 2t-k-1].                                               (1)
```

This improves the upper endpoint of the
[existing error wedge](RESULTS-p3-newton-error-wedge.md) by one column.
The new input is an exact period-four cancellation in round 2, preserved
through every later round by the previous support induction. It improves
some sufficient whole-row schedules by one round. The center schedule is
unchanged, and this is not a P3 algorithmic improvement.

The earlier report and verifier remain unchanged.

## 1. Reverse coordinates and the first reference

Retain the actual initialized sequence a^(k): the zeroth approximation is
the singleton row at time zero and zero at every positive time. Let r be
the actual Rule 30 trajectory. In moving coordinates r_(t,j)=u_(t,t-j),
reverse each row about its left edge and write

```
R_(t,h)=r_(t,2t-h),       A^(k)_(t,h)=a^(k)_(t,2t-h).
```

Negative h are zero. These are the same finite rows and initial conditions;
no reference is reset. The actual left-edge recurrence is

```
R'_(h)=R_(h-2)+(R_(h-1) OR R_h).                             (2)
```

The first Newton approximation is L^t, L=1+X+X^2, whose coefficients are
symmetric under this reversal. Its first four coefficients are

```
A^(1)_(t,0)=1,
A^(1)_(t,1)=b0,
A^(1)_(t,2)=b0+b1,
A^(1)_(t,3)=b0*b1,                                         (3)
```

where b0 and b1 are the two low bits of t. One proof is the Frobenius
factorization of L^t; equivalently the four rows in (3) close exactly under
multiplication by L, starting from the singleton.

The true first four coefficients obey

```
R_(t,0)=1 for all t,
R_(t,1)=1 for t>=1,
R_(t,2)=0 and R_(t,3)=t mod2 for t>=2.                       (4)
```

This follows directly from (2), with the initial rows through time 2.
The two highest bits 11 force the next bit to zero; the following bit then
toggles. These are all-time edge identities, not an extrapolated periodic row.

## 2. Two adjacent round-2 errors never occur together

In reverse coordinates the exact Newton update at reference A is

```
V'_h=V_(h-2)+(1+A_h)*V_(h-1)
       +(1+A_(h-1))*V_h+A_(h-1)*A_h.                        (5)
```

For the second Newton round, V_0=1 always and V_1=1 from time 1 onward.
Put z_t=V_(t,2), y_t=V_(t,3). Substitution of (3) into (5) gives, for t>=1,

```
z_(t+1)=(1+b0)*(z_t+b0+b1),
y_(t+1)=1+(1+b0*b1)*z_t+(1+b0+b1)*y_t.                     (6)
```

The omitted forcing product in the second line is identically zero:
`(b0+b1)*b0*b1=0`. The initial values are

```
(z_1,y_1)=(1,0),   (z_2,y_2)=(0,0),   (z_3,y_3)=(1,1).
```

For every t>=3, the following complete phase table is invariant under (6):

| t modulo 4 | z_t | y_t | round-2 error at h=2 | round-2 error at h=3 |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 |
| 2 | 0 | 1 | 0 | 1 |
| 3 | 1 | 1 | 1 | 0 |

The error columns use (4). At times 0,1,2 both errors are zero, because the
second round gives those complete rows correctly; this is also checked
from the initial four-bit recurrence. In particular the periodic formula
for the h=3 error is asserted only from time 3 onward.

Consequently, writing e^(2) for the round-2 error in reverse coordinates,

```
e^(2)_(t,2) * e^(2)_(t,3)=0 for every t>=0.                  (7)
```

This is an exact forbidden adjacent-error pattern of these two specified
columns. It is not a claim that all errors in round 2 are isolated.

## 3. The extra column persists through all subsequent rounds

The error equation in reverse coordinates is

```
d'_h=d_(h-2)+(1+A_h)*d_(h-1)
       +(1+A_(h-1))*d_h+e_(h-1)*e_h.                        (8)
```

The old wedge already makes the round-3 errors at h=0,1,2 zero. At h=3,
(8) therefore reduces to

```
d'_(3)=(1+A^(2)_(t,2))*d_(3)
            +e^(2)_(t,2)*e^(2)_(t,3).
```

Its source vanishes by (7), and its initial value is zero. Hence the
round-3 error at h=3 is zero for every time. Together with the old low-end
bound, round 3 has support inside `[6,2t-4]` in moving coordinates.

Now repeat the earlier support induction. If round k has error support
`[L,U]=[2k,2t-k-1]`, the next round's error at the previous time lies in
`[L+2,U-1]`. Its derivative term and adjacent-product source both lie in
`[L+2,U+1]` at the next time. This is exactly
`[2(k+1),2(t+1)-(k+1)-1]`. Thus (1) holds for every k>=3, including the
empty-interval cases.

The entire row is therefore exact whenever `2n<3k+1`, with k>=3. A
sufficient whole-row choice is

```
k=floor((2n-1)/3)+1, provided this k is at least 3.           (9)
```

Equivalently use `max(3,ceil(2n/3))` for n>=3; n=0,1,2 need respectively
zero, one, and two rounds. Compared with the old whole-row schedule,
(9) saves a round when n is a positive multiple of 3 and the k>=3 condition
holds. The center readout still needs the unchanged sufficient condition
`n<2k`; no center convergence gain follows from removing this high-index
column.

## 4. Exact checks and limits

The [verifier](../../experiments/rule30/p3_newton_left_edge_gain.py) and
[artifact](../../experiments/rule30/p3-newton-left-edge-gain.json) retain all
64 local truth-table derivative cases, all four additive-reference phase
edges, the time-0-through-2 controls, and every edge of the invariant table.
They check the zero-source boundary with either value of its reference
coefficient. These finite tables certify the all-length induction.

The verifier only reads the saved initialized-round diagnostics from
[p3-global-newton.json](../../experiments/rule30/p3-global-newton.json).
No old rounds, schedules, complete Rule 30 rows, or larger center prefix
are recomputed. All relevant report/source/data hashes are recorded.

Those saved diagnostics also already refute the suggested universal lower
bound that the first wrong row is at least 2k: round 2 first errs at row 3,
round 4 at row 7, and round 7 at row 12. These are finite counterexamples
to that exact statement, not an asymptotic convergence conclusion. The
single fixed-column cancellation (7) supplies no bound on general error
adjacencies and no sublinear round schedule.

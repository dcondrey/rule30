# Preregistration: reflected-half overlay audit

Date: 2026-09-01

## Question

Fold a Rule 30 row at the center and encode the cell pair at distance `i` as

```text
q_i=(L_i,R_i)=(x(-i),x(i)).
```

Test whether any reflection-symmetric overlay made from

```text
X=L XOR R,  A=L AND R,  O=L OR R
```

is a closed local factor of the exact folded evolution.  If it is, search its
complete local table for a period-two boundary obstruction.  If it is not,
identify the smallest ordered refinement that is closed and compare it with
the existing four-state carry normal form.

## Frozen checks

1. Derive the radius-one four-state folded rule and check it against literal
   Rule 30 on all `4^3=64` folded neighborhoods.
2. Check the alternating-center boundary pins:

   ```text
   c_t=0 => X_t(1)=1,
   c_t=1 and c_(t+1)=0 => O_t(1)=1.
   ```

3. Exhaust every nonempty subset of `{X,A,O}` and decide local closure by
   exact same-projected-neighborhood/different-projected-output collisions.
4. Exhaust two-coordinate refinements drawn from `{L,R,X,A,O}` and report
   the inclusion-minimal closed encodings.
5. Compare the ordered OR-latch encoding `(L,O)` with the carry input action
   `c'=c XOR O`, `d'=d XOR (c OR L)`.  Record whether the literal input
   quotient is exactly `2~3`, as predicted by the OR latch.

## Interpretation gate

A symmetric overlay that is not closed is not a proof coordinate by itself.
The missing mismatch orientation must be retained as a cocycle.  A closed
ordered encoding is useful only if it is smaller than, or gives a new
monotone quotient of, the already-known `D8` carry action.  Finite row-density
measurements are outside this audit and will not be used as a theorem.


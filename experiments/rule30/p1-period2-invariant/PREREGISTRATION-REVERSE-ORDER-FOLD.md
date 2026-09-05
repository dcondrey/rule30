# Preregistration: reverse-order (antidiagonal) fold

Date: 2026-09-01

## Question

For the single-seed Rule 30 triangle, read the left half from center to its
outer edge but read the right half in the opposite order, from its outer edge
back to the center.  At time `t` encode

```text
Q_t(i)=(A_t(i),B_t(i))=(x_t(-i),x_t(t-i)),  0<=i<=t.
```

This differs from the ordinary reflected fold `(x_t(-i),x_t(i))`.  Test
whether the reverse ordering exposes a smaller closed factor or a useful
two-ended boundary constraint for an alternating center trace.

## Frozen checks

1. Derive and exhaustively check the interior update

   ```text
   A_(t+1)(i)=f(A_t(i+1),A_t(i),A_t(i-1)),
   B_(t+1)(i)=f(B_t(i),B_t(i-1),B_t(i-2))
   ```

   wherever all displayed parents lie in the old row.

2. Verify directly on single-seed rows that the two endpoints are

   ```text
   Q_t(0)=(c_t,1),       Q_t(t)=(1,c_t).
   ```

   Thus they are bit-transposes, and a period-two center would prescribe a
   period-two pair at both ends of a word whose length grows by one.

3. Exhaust every nonempty symmetric projection from `X=A XOR B`,
   `N=A AND B`, and `O=A OR B` for closure under the four-site interior
   stencil.  Record exact collisions for every nonclosed projection.

4. Identify every inclusion-minimal closed projection drawn from
   `{A,B,X,N,O}`.  A projection is strategically new only if it retains less
   than one literal side or couples the two sides through a closed quotient.

5. Compare the reversed-right recurrence with the already proved physical
   shear.  State explicitly whether this coordinate is conjugate to the
   inverse-terminal queue or merely analogous to it.

## Interpretation gate

The two paired cells are separated by `t`, so a visual correlation is not a
local spatial invariant.  A symmetric overlay that is not closed cannot be
used as a proof state without restoring the missing orientation.  Temporal
or whole-triangle reversal is not included in this audit; it would depend on
a chosen finite horizon and would not commute with forward Rule 30 evolution.

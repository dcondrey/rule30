# Preregistration: center-controlled reversal

Date: 2026-09-01

## Coordinate

Let `u_t=(x(t,0),...,x(t,t))` be the physical right half of the single-seed
triangle, including the center and the right characteristic edge.  Encode

```text
E_c(u) = u             if c=0,
         reverse(u)    if c=1,
```

where `c=u[0]` is the center bit.  Under the hypothetical alternating center
trace, the orientation reverses on every time step.

The same finite-word map can be studied independently of the single-seed
orbit: inputs have the prescribed center at the appropriate end and have
right-edge bit one.  The next center is externally pinned to `1-c`.

## Frozen checks

1. Check literal Rule 30 rows against the encoded update

   ```text
   T_c(w)=E_(1-c)( right_step(E_c^-1(w),1-c) ).
   ```

2. Verify that the newly created right-edge bit occurs at the beginning of
   `T_0(w)` and at the end of `T_1(w)`.  Thus the growth/reset alternates
   between the two ends.

3. Remove just that newly created edge bit and compare the inherited
   length-`n` output with the length-`n` input.  Exhaust all four word orders
   (lex/colex and `0<1`/`1<0`) separately in each phase through length 14.
   If one comparison is uniformly strict, construct a finite synchronous
   comparison automaton to prove it for all lengths.  Otherwise print the
   first exact counterexample to every order.

4. Test ordered pairs of comparisons, allowing the phase-zero descent to pay
   for a phase-one increase, by comparing the exact two-step macro after
   deleting its two new edge cells.  Again exhaust all lex/colex orders and
   report exact counterexamples or an all-word automaton proof.

5. Also retain the left half in center-to-edge order and form the adaptive
   folded pair

   ```text
   Q_t(i)=(x(t,-i),x(t,i))     when c_t=0,
          (x(t,-i),x(t,t-i))   when c_t=1.
   ```

   Under an alternating trace beginning with zero, verify that its XOR word
   has zero at both endpoints at every phase.  Test whether XOR, AND, OR, or
   their joint symmetric encoding closes under the two-step maps that return
   to a fixed phase.  Interior nonclosure is enough to reject a quotient.

6. State the scope precisely.  Center-controlled reversal is a coordinate
   change on a physical half-row.  It is not automatically a conjugacy to the
   four-state inverse-terminal queue; any transfer to the queue must be an
   explicit theorem rather than a visual analogy.

## Success criterion

A useful result is an all-word one-step or two-step descent in which boundary
growth is least-significant often enough to prevent indefinite resets.  A
bounded pattern seen only on the actual single-seed prefix is exploratory and
will not be treated as a period-two proof.

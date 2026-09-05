# Radius-two Bellman energy audit

Date: 2026-09-01

Status: **THE POSTED RADIUS-TWO LINEAR SYSTEM IS UNSAT.**  It has no rational
weights `W`, `P`, `S`, and `U`; consequently it supplies neither an
all-length invariant nor a period-two mortality proof.

## 1. Exact solver result

The literal `N=7` script did not print because its only output branch is
guarded by `sol.check() == sat`.  With the same constraints and Z3's alternate
exact linear-rational engine, the result is `unsat`.

The proposed optimized script is also `unsat`, in under one second with Z3
4.16.0.  This is not caused by the number of constraints.  In fact, the
contradiction below uses only peel words of length at most five and one
length-three hard-core word, so it is contained in both posted systems.

## 2. Solver-independent rational contradiction

Write the asserted gaps as

```text
D(q)   = 2 (q_0 & 1) + E(peel(q)) - E(q) >= 0,
I(rho) = E(init(rho)) - wt(rho)                 >= 0.
```

Exact coefficient collection gives the polynomial identity

```text
 16 I(101)
+  4 D(01303)
+    D(1312)
+ 14 D(1303)
+  8 D(0312)
+ 10 D(0231)
+  2 D(0123)
+ 15 D(231)
+    D(022)
+    D(012)
+  6 D(003)
+  2 D(000)
+ 14 D(02)
+  2 D(00)
+ 16 D(0)
- 16 U(empty)
= -2.
```

Every displayed coefficient of an asserted inequality is nonnegative, and
`U(empty)=0`.  If the posted constraints held, the left side would therefore
be nonnegative.  The identity says it is `-2`, a contradiction.  All
coefficients of all 16 `W` variables, four `P` variables, four `S` variables,
and five `U` variables cancel exactly over the rationals.

This is a Farkas certificate, not a bounded counterexample or a numerical
tolerance result.  The checker constructs every affine expression from the
posted definitions and verifies both complete symbolic cancellation and the
constant `-2` with Python `Fraction` arithmetic.  It separately asks Z3's
`qflra` tactic to check the posted optimized system.

## 3. Locality issue

For words of length at least three, put

```text
f(a,b) = peel(a,b).
```

Then the global gap has the weighted-path form

```text
D(q_0...q_(m-1))
  = A(q_0,q_1)
    + sum B(q_i,q_(i+1),q_(i+2))
    + C(q_(m-2),q_(m-1)).
```

Radius two makes `A`, `B`, and `C` local, but it does not by itself make every
arbitrary-length path sum nonnegative.  A valid uniform certificate would
also need a finite-state flux `V(a,b)` satisfying endpoint inequalities and

```text
B(a,b,c) + V(a,b) - V(b,c) >= 0
```

for every triple.  This would telescope for all lengths.  Likewise, the
hard-core initialization lower bound needs its own two-state flux certificate;
checking seed lengths through eight is not, by itself, an all-length proof.

The present system fails before either lifting question arises.

## 4. Consequence

There are no exact fractions to hardcode in an unbounded verifier.  The
claimed chain

```text
wt(rho) <= E(init(rho)) <= 2 wt(L(rho))
```

cannot be derived from the posted constraints, so the reconstructed-tail
density bound, hard-core isolated-pulse theorem, period-two theorem, and Rule
30 Prize Problem 1 all retain their previous status.

At least one mathematical input must change before another synthesis is
meaningful: the definition of `peel`, the encoding `init`, the direction or
coefficient of the Bellman inequality, or the domain on which peel words are
required to satisfy it.

## 5. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/bellman_radius2_audit.py
```

Expected output:

```text
posted radius-2 QF_LRA system: UNSAT
exact Farkas certificate: -2 >= 0 (contradiction)
maximum peel-word length in certificate: 5
only hard-core initialization in certificate: 101
```

# Exact local seam law for the deterministic binary-wedge map

Date: 2026-09-02

Status: **the phase-to-`(Q, Delta)` decoder is now an all-length identity.
The source-interval `Join` law producing the required phase profile remains
open, so the nonconstant period-two exclusion and P1 remain open.**

## Result

For the `j`th forced output, let

```text
A_j=(a_j,b_j,g_j): (h,l) -> (h+a_j,l+b_j h+g_j)
```

be the exact entering affine `D8` phase.  Define its adjacent ordered
holonomy by

```text
D_j=A_j^-1 o A_(j+1)=(x_j,y_j,z_j).
```

Then the complete deterministic output map has the exact decoder

```text
Q_n(W)_j = 2-a_j,

Delta_j(W)
  = x_j + z_j + y_j(1+a_j+x_j)                 over F_2.       (1)
```

Thus every adjacent output defect is isolated at one explicit seam.  The
absolute entering phase cannot be discarded: two assignments with the same
holonomy `(x,y,z)=(0,1,0)` have opposite defects,

```text
(a,b,g,x,y,z) = (0,0,0,0,1,0) -> Delta=1,
(a,b,g,x,y,z) = (1,0,0,0,1,0) -> Delta=0.             (2)
```

Equation (2) excludes every phase-free seam decoder, regardless of grammar.

## Paper proof

The forced binary input to `A=(a,b,g)` has bits `(h,l)=(1+a,a)`, hence

```text
psi(A)=a+b(1+a)+g.
```

If `D=(x,y,z)=A^-1 o A'`, then `A'=A o D`, so affine composition gives

```text
A'=(a+x,b+y,g+z+bx).
```

Substitution in `psi(A)+psi(A')` cancels `b`, `g`, and the two copies of
`bx`, leaving exactly (1).  This derivation uses only Boolean-ring
identities and holds for every adjacent phase pair.

## Machine checks

The CEGIS grammar contains only typed Boolean AST nodes for constants,
variables, XOR, and AND.  It enumerated 3,525 distinct functions through
operator cost five.  Five rejected candidates received their first literal
counterexamples; the survivor was

```text
(((((1^a)^x)&y)^x)^z)
```

which is (1).  Z3 5.1.0 returned `UNSAT` for the survivor differing from the
unsimplified group-composition target on any Boolean assignment.

An independent inverse-cone implementation then checked exact agreement on:

- all 1,022 binary words of lengths 1 through 9;
- all 9,216 binary splits of those phase profiles, using left-deep,
  right-deep, and balanced recursive folds;
- the width-15 sharp binary-wedge saturator; and
- eight archived bounded-summary/charge/rank-zero obstruction words.

The finite nonzero-`Delta` census is `128/128`, `256/256`, and `512/512` at
lengths 7, 8, and 9.  This is regression evidence only; formula (1) does not
prove that some seam is nonzero at every length.

## What remains

The phase profile `A_0,...,A_(n+1)` is still computed by the full exact
recurrence.  Splitting that already-known profile is associative and (1)
places one correction at each chosen seam, but this is not yet closure under
splitting the source word.

The next synthesis question is precise:

> Find a recursive interval summary retaining ordered ancestry, scale, and
> entering/exiting `D8` phase, with an associative `Join` that derives the
> phase profile without invoking the full recurrence.

That `Join`, not the now-solved five-operator decoder, is the proper object
for cvc5/OpenEvolve.  A candidate must reproduce (1) at every join and must
survive the archived closure collisions before receiving any horizon score.

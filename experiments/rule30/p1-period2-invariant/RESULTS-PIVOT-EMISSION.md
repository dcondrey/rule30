# Symbolic pivot/emission audit

Date: 2026-09-01

Status: **THE PROPOSED TIME-ORDERED PIVOT ARGUMENT IS KILLED.  The linear
hard-core mortality theorem remains open.**

## 1. Indexing and the exact one-row expansion

For an even-phase rho seed, the feeds of column `-1` are

```text
v_(2k)   = 1 XOR rho_k,
v_(2k+1) = 1.
```

Thus a seed of length `n` reaches frontier depth `T=2n`, not `T=n`.  If
`(T,A,B)` is the current frontier, define

```text
o_j = A_j OR B_(j-1),
B_0 = (T-1) mod 2.
```

The exact next row and emitted fixed-tail bit are

```text
C_1       = v_T,
C_(j+1)   = v_T XOR XOR_(ell=1)^j o_ell,
L_(T+1)   = C_(T+1)
          = v_T XOR XOR_(j=1)^T
              (A_j XOR B_(j-1) XOR A_j B_(j-1)).       (1)
```

Equation (1) is correct, but it is an ANF in the *frontier bits*.  Those
frontier bits are already nonlinear functions of rho.  The product term is
therefore not generally quadratic in the seed variables.

Writing the seed variables one-based and reducing exactly on the no-`11`
domain gives the first emissions

```text
L_1 = 1 + rho_1,
L_2 = rho_1,
L_3 = 1 + rho_2,
L_4 = 0,
L_5 = 1 + rho_2 + rho_3,
L_6 = rho_3,
L_7 = 1 + rho_3 + rho_4,
L_8 = rho_2 rho_4.                                  (2)
```

In particular, `L_4=rho_1 rho_2` before hard-core reduction and is identically
zero afterward.  There is no fresh linear seed pivot in that row.

These early `L_j` are coordinates of the reconstructed initial tail, not
post-knee zero constraints.  Finite support constrains `L_j=0` only after the
actual left depth.  Consequently no pivot is "consumed to maintain zero" while
the seed frontier itself is being constructed.

## 2. What the inverse-Gray kernel actually says

For zero-based positions and suffix XOR `P`,

```text
K = P^T P,
K_(i,j) = (min(i,j)+1) mod 2.
```

For width six this is

```text
1 1 1 1 1 1
1 0 0 0 0 0
1 0 1 1 1 1
1 0 1 0 0 0
1 0 1 0 1 1
1 0 1 0 1 0
```

Hence `K` is symmetric, not the lower-triangular all-ones matrix displayed in
the proposed pivot argument, and

```text
K_(i,i) = (i+1) mod 2 = 1,0,1,0,... .              (3)
```

It nevertheless has full rank because `P` is invertible.  Full rank of the
static bilinear form does not identify its Gaussian pivots with consecutive
emission times and does not imply that each scalar emission consumes a new
rho variable.  Equations (2) and (3) trigger Kill Condition 1 for the proposed
derivation.

## 3. Correct macro form through `T=n+2`

To remove the row/macro ambiguity, let macro `T=n` mean the first complete
zero/pin pair after a length-`n` seed.  Write `R_v(T,A,B)=(T+1,C,A)` for the
one-row polynomial map (1).  The frontier entering the post-knee calculation
is explicitly

```text
S_seed(0)   = (0, empty, empty),
S_seed(k+1) = R_1(R_(1+rho_(k+1))(S_seed(k))),
(2n,A^(0),B^(0)) = S_seed(n).                       (4)
```

Thus every bit below is an ANF in precisely `rho_1,...,rho_n`.  Let `S` be
the shallow-to-deep left shift, let `e_0` be the shallow boundary bit, and pad
all words with deep zeros.  At macro state `(A^(m),B^(m))`, where the row depth
is `2(n+m)`, put

```text
V_m = e_0 + S B^(m),
X_m = A^(m) OR V_m,
C_m = P X_m,
Y_m = C_m OR S A^(m),
D_m = P Y_m.                                        (5)
```

The forced next boundary bit and the two fixed-tail emissions are

```text
rho_(n+m+1)     = 1 + (C_m)_0,
L_(2(n+m)+1)    = 0,
L_(2(n+m)+2)    = epsilon_m = 1 + (D_m)_0.           (6)
```

Here rho is numbered one-based, consistently with (2).  Survival requires

```text
epsilon_m = 0,
rho_(n+m) rho_(n+m+1) = 0,                          (7)
```

and then `(A^(m+1),B^(m+1))=(D_m,C_m)`.  Equations
(4)--(7), iterated for `m=0,1,2`, are the explicit symbolic expansion through
macro `T=n+2`.  They involve only the initial `rho_1,...,rho_n`, because the
new rho bit in (6) is forced rather than free.

The formulas at `m>0` are interpreted on assignments satisfying all earlier
conditions (7); the displayed ANFs are harmlessly defined on failed paths as
well.

The OR products are explicit without shorthand:

```text
(C_m)_0 = XOR_j (A^(m)_j + V_(m,j) + A^(m)_j V_(m,j)),

epsilon_m = 1 + XOR_j
  (C_(m,j) + (S A^(m))_j + C_(m,j)(S A^(m))_j).     (8)
```

There is an exact place for `K`, but it is a frontier correlation rather than
a `(2n+2) x n` seed-evaluation matrix.  If `G=P^-1` and
`e_j=(j+1) mod 2`, then (8) becomes

```text
epsilon_m = 1 + e^T X_m + 1^T A^(m)
                + X_m^T K G(S A^(m)).               (9)
```

Both arguments of the `K` pairing change nonlinearly under (4).  Rank `K=w`
alone gives no affine-image obstruction for their reachable values.

## 4. First nonlinear post-knee specialization

For `n=4`, reduce modulo
`rho_1 rho_2=rho_2 rho_3=rho_3 rho_4=0`.  The three requested post-knee
macros are

```text
macro T=n:
  rho_5     = 1 + rho_3 + rho_2 rho_4
  epsilon_0 = 1 + rho_2 rho_4
  no-11     = rho_4 + rho_2 rho_4

macro T=n+1:
  rho_6     = 1 + rho_4 + rho_2 rho_4
  epsilon_1 = 1 + rho_4
  no-11     = 1 + rho_3 + rho_4

macro T=n+2:
  rho_7     = rho_3
  epsilon_2 = rho_3
  no-11     = rho_3.                               (10)
```

The legal seed `rho=0101` in shallow-to-deep order has
`rho_2=rho_4=1`; its quadratic term cancels the constant in `epsilon_0`, so
the first post-knee pin passes.  It also passes the next three macros and dies
at the fifth, agreeing with the retained exhaustive result.  Thus the
cross-term can enable finite survival; it is not forced to produce a one as
soon as a presumed linear degree count reaches `n`.

Already by the initial row `T=15`, the unrestricted ANF of `L_16` has degree
eight in the rho variables.  Referring to the entire reachable cross-term as
a quadratic vector in rho loses these higher-degree substitutions.

## 5. Rule 90 control

For Rule 90 the rotated recurrence contains `A_j XOR B_(j-1)` in place of
`A_j OR B_(j-1)`.  The product term is absent from the local polynomial; the
Boolean value `A_j B_(j-1)` does not itself become identically zero.  With
this wording correction, the Rule 90 exemption is sound and the symbolic
frontier remains linear in rho.

## 6. Reproduction and conclusion

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/pivot_emission_audit.py \
  --seed-length 4 --post-macros 3 --initial-rows 8
```

The checker verifies the kernel rank/diagonal through width 16 and the exact
symbolic recurrence against every hard-core seed through length eight.

The proposed `Im(K)+v_T` target lemma is therefore not established by the
kernel identity and cannot be used in its current form.  A viable uniform
argument must analyze the nonlinear moving-endpoint recurrence (4)--(9), not
static pivot exhaustion.  No seed surviving `2n+2` macros was found here, so
this audit does not refute linear hard-core mortality itself.

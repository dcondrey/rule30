# Interval annihilators and the matched-extension mechanism

Date: 2026-09-01

Status: **A GENUINE UNIFORM SHIFT MECHANISM IS PROVED FOR THE MATCHED
EXTENSION BRANCH.** The `n=10` and `n=12` six-point survivor classes are the
same rank-six local annihilator state with a period-three tail, and all
future observables are conjugate by a two-macro shift. A rank-five unmatched
branch appears at `n=13`; classifying such defect/restart states remains the
missing step for uniform mortality.

No seed assignment is enumerated in this audit.

## 1. The correct state is the survivor indicator

Let the ordered pin and hard-core generators at macro `m` be
`epsilon_m,q_m`. For an interval of macros `[a,a+H)`, define

```text
P_(n;a,H) = product_(m=a)^(a+H-1) (1+epsilon_m)(1+q_m)       (1)
```

in the Boolean hard-core quotient

```text
B_n = F_2[rho_1,...,rho_n]
      / <rho_i^2+rho_i, rho_i rho_(i+1)>.
```

`P_(n;a,H)` is an idempotent indicator, not an arbitrary Bezout cofactor. A
polynomial `f` is forced to zero on this interval class exactly when

```text
f P_(n;a,H) = 0.                                      (2)
```

Thus the annihilator of `P` is the exact algebraic state of the surviving
class. The highlighted cofactor
`rho_6rho_9(1+rho_4)` is one element of such an annihilator; it is not by
itself enough to identify the state or its successor.

The size of the represented class is recovered without evaluating seeds. In
a finite Boolean function ring, it is the rank of the multiplication map

```text
mu_P : B_n -> B_n,    f |-> fP.                       (3)
```

All ranks below are computed by exact GF(2) elimination on (3).

## 2. Uniform matched-extension lemma

Let `S` be a seed frontier. Write the one-row inverse-Gray update as `R_v`
and put

```text
z = parity_or(S),
r = 1+z.                                               (4)
```

Here `r` is the next forced rho bit. Adding a new seed bit `b` applies

```text
E_b(S) = R_1(R_(1+b)(S)),                              (5)
```

whereas one forced post-knee macro applies

```text
F(S) = R_1(R_z(S)).                                    (6)
```

If the appended bit is matched, `b=r`, then `1+b=z`, so (5) and (6) are
literally the same pair of row maps:

```text
b=r  ==>  E_b(S)=F(S).                                 (7)
```

This proves, for every `n` and `H`, not merely the measured cases,

```text
M_n P_(n+1;0,H) = M_n P_(n;1,H),                       (8)
M_n = 1 + rho_(n+1) + r_0^(n).
```

`M_n` is the Boolean indicator that the appended bit equals the first forced
bit of the shorter frontier. Iterating (7) through `s` matched appended bits
shifts every later forced rho, pin, and hard-core observable by `s` macros.

This is the exact action of `R_v` that the cofactor automaton was missing. It
acts on the full annihilator interval plus a match condition, not on a lone
cofactor motif.

## 3. The rank-six period-three state

For `n=10`, after eight surviving macros, the compact annihilator
presentation is

```text
rho_5=rho_6=rho_7=rho_9=rho_10=0,
rho_8=1,
rho_4 + rho_2rho_4=0.                                 (9)
```

There are six remaining Boolean points. As matched bits are appended, the
fixed tail extends as

```text
position:  8 9 10 11 12 13 14
value:     1 0  0  1  0  0  1.                       (10)
```

The left core and its six choices do not change. Denoting this state by
`A_n`, exact quotient identities give

```text
A_11 = A_10 rho_11,
A_12 = A_11,
A_13 = A_12 (1+rho_13),
A_14 = A_13 rho_14.                                  (11)
```

The equality `A_12=A_11` is in the hard-core quotient: `rho_11=1` already
forces `rho_12=0`. In particular,

```text
P_(12;0,6)
  = P_(10;0,8) rho_11(1+rho_12).                      (12)
```

On (12), for every `m=0,...,6`, the audit proves

```text
rho_m^(12)     = rho_(m+2)^(10),
epsilon_m^(12) = epsilon_(m+2)^(10),
q_m^(12)       = q_(m+2)^(10).                        (13)
```

Every difference in (13), multiplied by `P_(12;0,6)`, reduces to literal
zero. Thus the apparent `n=10`/`n=12` repetition is a true two-macro
conjugacy, not merely a similar cofactor.

## 4. Exact match/defect decomposition

Applying (8) along the diagonal classes gives:

| extension | destination interval | total rank | matched rank | defect rank |
|---|---:|---:|---:|---:|
| `10 -> 11` | `H=7` | 6 | 6 | 0 |
| `11 -> 12` | `H=6` | 6 | 6 | 0 |
| `12 -> 13` | `H=5` | 11 | 6 | **5** |
| `13 -> 14` | `H=4` | 11 | 11 | 0 |

At each line the destination indicator is partitioned exactly as

```text
P_destination = M P_destination + (1+M)P_destination, (14)
```

and the two summands multiply to zero. The first is the interval-shifted
matched component from (8); the second is the mismatch defect.

The `12 -> 13` defect is not algebraic noise. It has rank five and the
following compact local presentation, called `B_13`:

```text
rho_4=rho_5=rho_7=rho_8=rho_10=rho_11=rho_12=0,
rho_6=rho_9=rho_13=1.                                 (15)
```

The five points are exactly the five arbitrary hard-core assignments of
`rho_1,rho_2,rho_3`, followed by the fixed tail in (15). At the next length,

```text
B_14 = B_13 (1+rho_14),                               (16)
```

and all rank-six and rank-five branches are matched. Equivalently, the full
rank-eleven indicator satisfies

```text
P_(14;0,4) = P_(13;0,5)(rho_13+rho_14).                (17)
```

Equation (17) says `rho_14=1+rho_13` on the entire class.

## 5. Both states force the terminal pin

The terminal signatures are:

| state | terminal macro | rank | `epsilon` | `q` | forced rho |
|---|---:|---:|---:|---:|---:|
| `A_10` | 8 | 6 | 1 | 1 | 1 |
| `A_11` | 7 | 6 | 1 | 1 | 1 |
| `A_12` | 6 | 6 | 1 | 1 | 1 |
| `A_13` | 5 | 6 | 1 | 1 | 1 |
| `B_13` | 5 | 5 | 1 | 0 | 1 |
| `A_14` | 4 | 6 | 1 | 1 | 1 |
| `B_14` | 4 | 5 | 1 | 0 | 1 |

The obstruction branch changes which `q` is active, but it does not escape:
`epsilon=1` identically on both local states.

## 6. Affine law for a mismatched appended bit

The mismatch itself has an exact frontier formula. Relative to the matched
macro successor:

1. flipping the first feed complements every bit of the first added row;
2. the successor `B` row therefore differs by the all-ones word; and
3. the successor `A` defect is

```text
delta_0 = 0,
delta_j = sum_(ell=1)^j (1 + Shift(A)_ell).            (18)
```

The OR nonlinearity cancels in (18) because

```text
((1+C) OR A) + (C OR A) = 1+A.                        (19)
```

The implementation verifies (18) as exact ANF at frontier depths 8, 20, and
24. This reduces the unmatched transition to an affine inverse-Gray defect,
but the defect still depends on the full incoming `A` word. A bounded local
quotient for (18) has not yet been proved.

## 7. What remains for uniform mortality

The matched branch is now solved uniformly: it is a literal macro shift.
The remaining proof obligation is narrower:

> Classify the interval-annihilator states produced by mismatched extensions
> and by restarts after skipped failed emissions, and exhibit a well-founded
> rank that bounds consecutive good macros across those states.

This wording matters. The `0xa` seed is a *matched* two-bit extension of its
shorter prefix, but it skips an earlier failed pin before beginning its
length-four survival run. Therefore match/defect alone is not the whole
state; the automaton must use interval indicators `P_(n;a,H)` rather than
only prefix ideals `J_H=P_(n;0,H)`.

The evidence now supports a finite-state program with two explicit pieces:

```text
(local annihilator type, interval/restart phase),
```

not a DAG of raw cofactors. The rank-six `A` state and rank-five `B` state are
the first exact entries in that dictionary.

## 8. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/interval_annihilator_audit.py \
  --json \
    experiments/rule30/p1-period2-invariant/interval-annihilator-n10-n14.json

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/verify_interval_annihilator.py \
  experiments/rule30/p1-period2-invariant/interval-annihilator-n10-n14.json
```

The artifact records every compact generator, exact indicator identity,
match/defect component, principal rank, alignment residue, terminal target,
and mismatch formula. The standalone verifier reconstructs the compact
indicators, all component products, and all ranks from monomial masks.

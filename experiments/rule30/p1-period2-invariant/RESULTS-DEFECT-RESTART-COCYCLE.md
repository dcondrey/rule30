# Exact defect/restart cocycle

Date: 2026-09-01

Status: **THE FULL SYMBOLIC COCYCLE AND ITS ADVANCE, RESTART, AND EXTENSION
SPLITS ARE EXACT.  PRINCIPAL RANK IS CONSERVED BY BRANCH PARTITION BUT IS NOT
STRICTLY CONTRACTING.  NO WELL-FOUNDED UNIFORM RANK OR PERIOD-TWO THEOREM IS
PROVED.**

The generator is `defect_restart_cocycle.py`; the independent artifact
checker is `verify_defect_restart_cocycle.py`.  Both are solver-free and
enumerate no seed assignments.

## 1. The exact evolving state

Work in the Boolean hard-core quotient

```text
B_n = F_2[rho_1,...,rho_n]
      / <rho_i^2+rho_i, rho_i rho_(i+1)>.
```

At macro offset `m`, let `S_m` be the complete symbolic frontier, let
`r_(m-1)` be the previous forced rho polynomial, and let `P_m` be the
indicator of the current survivor class.  The cocycle state is

```text
F_m = (S_m, r_(m-1), P_m).                            (1)
```

The frontier recurrence determines the next pin obstruction `epsilon_m`,
the new hard-core obstruction `q_m`, the forced rho, and `S_(m+1)`.  Put

```text
K_m = (1+epsilon_m)(1+q_m).                           (2)
```

The exact formula morph is

```text
P_(m+1) = P_m K_m.                                    (3)
```

Equations (1)-(3) are a closed operator for every `n` and `m`.  The closure
is not finite-dimensional: `S_m` gains two symbolic frontier coordinates per
macro, exactly retaining the expanding information that a fixed formula
loses.

## 2. Uniform partition lemma

For any Boolean indicator `P` and Boolean factor `K`, define

```text
P_good = P K,
P_out  = P (1+K).                                     (4)
```

Then, identically in every Boolean ring,

```text
P = P_good + P_out,
P_good P_out = 0.                                     (5)
```

The first identity is distributivity; the second is `K(1+K)=0`.  In the
finite Boolean function ring `B_n`, the principal rank of an indicator is the
number of represented hard-core points.  Hence the disjoint split gives

```text
rank(P) = rank(P_good) + rank(P_out).                  (6)
```

Consequently (3) is strictly rank-contracting **if and only if** the removed
component `P_m(1+K_m)` is nonzero.  This is an exact criterion, but it does
not say that a nonzero removed component exists at every macro.

## 3. Restart is a second instance of the same split

For an interval beginning at `a`, write

```text
P_(n;a,H) = product_(m=a)^(a+H-1) K_m.
```

Suppose the interval after offset `a` is good for `H` macros, without
requiring offset `a` itself to pass.  Applying (4) to its preceding macro
gives the exact restart operator

```text
P_(n;a+1,H)
  = P_(n;a,H+1)
    + P_(n;a+1,H)(1+K_a).                             (7)
```

The first summand continues through offset `a`.  The second fails at `a` and
then begins a new good interval at `a+1`; it is precisely the restart class.
The summands are disjoint and their ranks add.

Equation (7) makes “skipping a failed emission” an explicit algebraic branch,
not an informal exception to an induction.

## 4. Seed extension is the third exact split

Let `M_n` indicate that appended bit `rho_(n+1)` equals the first forced rho
of the length-`n` frontier.  The uniform matched-extension identity gives

```text
M_n P_(n+1;a,H) = M_n P_(n;a+1,H).                    (8)
```

Therefore every destination interval has the disjoint decomposition

```text
P_(n+1;a,H)
  = M_n P_(n;a+1,H)
    + (1+M_n)P_(n+1;a,H).                             (9)
```

The first branch is the shifted matched interval; the second is the affine
mismatch defect.  Their principal ranks again add.  The retained exact
extension controls are:

| extension | longer interval | destination / matched / defect rank |
|---|---|---|
| `2 -> 3` | `[1,5)` | `1 / 1 / 0` |
| `3 -> 4` | `[0,4)` | `1 / 1 / 0` |
| `10 -> 11` | `[0,7)` | `6 / 6 / 0` |
| `11 -> 12` | `[0,6)` | `6 / 6 / 0` |
| `12 -> 13` | `[0,5)` | `11 / 6 / 5` |
| `13 -> 14` | `[0,4)` | `11 / 11 / 0` |

Thus matched extension is rank-preserving, while an unmatched branch can add
a separate defect component to the longer destination.

## 5. Exact restart mechanism behind `0xa`

The smallest endpoint-peel obstruction is now explained without enumerating
seeds.  At length two,

```text
P_(2;2,4) = rho_2.                                    (10)
```

This entire rank-one class is a restart after offset one:

```text
rank P_(2;2,4)                  = 1,
rank P_(2;1,5)                  = 0,
rank P_(2;2,4)(1+K_1)           = 1.                  (11)
```

Two matched extensions apply (8) twice.  The exact interval indicators are

```text
P_(2;2,4) = rho_2,
P_(3;1,4) = rho_2,
P_(4;0,4) = rho_2 rho_4.                              (12)
```

On the hard-core domain, `rho_2 rho_4` is the unique seed `0xa`.  Thus the
length-four survival spike is not created by a mismatch.  It is a shorter
restart interval lifted into prefix position by two perfectly matched
appends.  Any induction state omitting the restart phase necessarily misses
this mechanism.

## 6. Strict contraction and a small compressed cocycle both fail

The exact advance-rank traces are:

```text
n=4:   8,1,1,1,1,0
n=10:  144,72,28,11,11,6,6,6,6,0
n=12:  377,146,94,41,26,13,6,0.                      (13)
```

Every equality in (13) is a literal absorbed-generator step:
`P_(m+1)=P_m`, not merely two classes of equal cardinality.  Hence principal
rank is nonincreasing but not strict.

Adding the period-three tail phase still does not close the state.  At
`n=10`, offsets five and eight have

```text
same exact rank-six indicator,
same offset modulo 3,
offset 5 successor = the same rank-six indicator,
offset 8 successor = 0.                               (14)
```

The artifact retains the shared 14-term degree-five indicator, both exact
good factors, and both successors.  Equation (14) is a closure collision for

```text
(survivor indicator, offset mod 3).
```

It proves that even the complete survivor class plus the observed tail phase
does not determine its next morph.  Some additional frontier driver is
essential.

## 7. Consequence

The requested adaptive operator has been built.  Its algebraic structure is
a conservative branch partition:

```text
advance:    current = survivor + removed,
restart:    future  = continuous + restart,
extension:  longer  = matched + mismatch defect.     (15)
```

This is a useful uniform intermediate lemma: it identifies exactly where
degrees of freedom go.  It does **not** prove convergence.  Absorbed
generators yield self-loops, matched extension preserves rank, restarts can be
lifted into new prefix survivors, and the driver required for deterministic
closure still grows with the frontier.

A genuine mortality proof now needs a well-founded rank on a symbolic
compression of the full driver in (1), strong enough to charge arbitrarily
long absorbed runs and restart lifts.  Defining the charge as “distance to a
future nonabsorbed generator” would be circular: proving that this distance
is always finite is already the mortality problem.

The period-two theorem remains open.

## 8. Boundary-collision interpretation and next operator

The boundary-value formulation is compatible with the exact cocycle, but
three evidence levels must remain separate.

1. Rowland's right-diagonal theorem is rigorous: every fixed right-cone
   diagonal of a finite row is purely periodic with a power-of-two period.
2. The penetration estimate `~2.4 log2(t)` in
   `docs/rule30/RESULTS-diagonal-periodicity.md` is an exact computation over
   the recorded range, not a proved asymptotic law.  In particular, the
   stronger claim that the right boundary exerts no constraint on the centre
   for every time does not follow from that estimate alone.
3. The exact "one new bit" statement is a closure deficit: advancing a
   fixed finite fibre requires the next outer bit.  It is not a theorem that
   Rule 30 loses one bit of entropy or predictability at every step.  The
   entropy census in `docs/rule30/RESULTS-followup-entropy-gardenofeden.md`
   instead records bounded-prefactor losses in the tested languages.

The left-side obstruction is the exact ladder sandwich

```text
plain(R+1) subset pin(R) subset plain(R).             (16)
```

Thus a fixed-depth boundary pin relocates the unresolved phase slip rather
than closing the dynamics.  A bilateral adaptive state must retain that
unresolved information.  The minimal honest specification is

```text
C_T = (L_T, S_T, P_T, R_T),                           (17)
C_(T+1) = U_(L_T,R_T)(C_T),                           (18)
```

where `L_T` and `R_T` are exact boundary modes, `S_T` is the symbolic
active-core frontier, and `P_T` is the survivor indicator.  Every newly
exposed seam bit remains in `S_T` unless an exact boundary relation eliminates
it.  Merely attaching two periodic phases to `P_T` would not make (18)
closed: the collision (14) already shows that the same complete indicator
and tail phase can have different successors when their symbolic drivers
differ.

The resulting uniform theorem target is therefore:

> Construct a closed symbolic compression of `(L_T,S_T,P_T,R_T)` and a
> well-founded measure `mu` such that
> `mu(U_(l,r)(C)) < mu(C)` for every admissible boundary-mode pair `(l,r)`.

The right-diagonal modes can parameterize inputs to this operator, but they
cannot by themselves supply the required decrease across the growing
unresolved interface.  Proving either symbolic elimination of every fresh
seam bit or strict descent despite retaining those bits is the outstanding
obligation.

## 9. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/defect_restart_cocycle.py \
  --json \
    experiments/rule30/p1-period2-invariant/defect-restart-cocycle.json

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/verify_defect_restart_cocycle.py \
  experiments/rule30/p1-period2-invariant/defect-restart-cocycle.json
```

The standalone verifier reconstructs every Boolean product, all 21 advance
partitions, all six extension splits, the restart lift, every principal rank,
and the closure collision directly from recorded monomial masks.

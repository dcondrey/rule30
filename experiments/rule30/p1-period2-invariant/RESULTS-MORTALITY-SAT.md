# Variable-seed mortality certificates and triangular correlations

Date: 2026-09-01

Status: **OPEN.  No period-two theorem was proved.**  The hybrid experiment
produced exact variable-input certificates through finite seed lengths and a
new full-rank formula for inverse-Gray correlations.  Neither result is a
uniform argument in the seed length.

## 1. Exact mortality formula

For seed length `n` and post-seed horizon `H`, `mortality_sat.py` constructs
a CNF `M(n,H)`.  Its only unconstrained semantic inputs are the `n` rho bits.
The formula asserts:

- the seed has no `11`;
- its exact two-row frontier is built by the registered recurrence;
- every future zero phase has a zero new deep-left output;
- every future pinned phase has a zero new deep-left output; and
- the consequently forced rho bits continue to have no `11`.

For a frontier `(T,A,B)`, one one-row step is encoded bit for bit as

```text
C_1 = v,
C_(j+1) = C_j XOR (A_j OR B_(j-1)),
B_0 = (T-1) mod 2.
```

At a forced zero phase, constraining the deepest `C` bit to zero determines
`v`, and the next rho bit is `NOT v`.  At the following pin phase `v=1`, and
the new deepest bit must again be zero.  Consequently:

> `M(n,H)` is SAT exactly when some hard-core seed of length `n` survives at
> least `H` post-seed macrosteps.

This is a variable-seed UNSAT statement, unlike the earlier fixed-seed P3
instances whose outputs were forced by unit propagation.

## 2. Independent semantic validation

For every `n <= 16`, every threshold from `H=0` through one beyond the direct
maximum was compared with independent integer-transducer enumeration.  SAT
held exactly through the maximum and UNSAT held at the next step in all 95
threshold checks.  Every SAT model was decoded to a seed and replayed.  With
the post-seed deep-left constraints removed, the registered `H=2n+2` control
remained SAT.

Direct exhaustive enumeration was then extended to every Fibonacci-language
seed through `n=24` (121,393 seeds at `n=24`), with cap 512 and no cap hit:

| `n` | maximum survival | first witness | death | `n` | maximum survival | first witness | death |
|---:|---:|---:|---|---:|---:|---:|---|
| 1 | 2 | `0x0` | pin | 13 | 5 | `0x480` | hard-core |
| 2 | 1 | `0x2` | pin | 14 | 4 | `0x1120` | pin |
| 3 | 1 | `0x0` | hard-core | 15 | 5 | `0x2120` | pin |
| 4 | 4 | `0xa` | pin | 16 | 6 | `0x1028` | pin |
| 5 | 3 | `0xa` | pin | 17 | 6 | `0x4940` | pin |
| 6 | 2 | `0x2a` | pin | 18 | 8 | `0x24a0` | pin |
| 7 | 2 | `0x40` | pin | 19 | 8 | `0x4aaa8` | hard-core |
| 8 | 4 | `0x50` | hard-core | 20 | 7 | `0x20940` | pin |
| 9 | 3 | `0x0` | hard-core | 21 | 10 | `0x41400` | hard-core |
| 10 | 8 | `0x80` | hard-core | 22 | 12 | `0xa80a8` | pin |
| 11 | 7 | `0x480` | hard-core | 23 | 11 | `0xa80a8` | pin |
| 12 | 6 | `0x480` | hard-core | 24 | 10 | `0xa80a8` | pin |

Thus the preregistered `H(n)=2n+2` bound survives every finite test through
24, but the maximum is not constant: it reaches 12 at `n=22`.  This retires
the earlier hope that a small universal post-knee bound would be visible.

## 3. Proof-certificate outcome

Glucose proof traces for the primary `M(n,2n+2)` instances were independently
RUP-checked through `n=11`.  The proof at `n=12` grew to 105,998 raw lines
(65,543 additions, maximum width 154), and checking was stopped after five
minutes under the registered proof-growth kill condition.

After observing that padding the horizon obscures the actual obstruction, an
exploratory sweep certified the shortest UNSAT instance
`M(n, maximum(n)+1)`.  These traces were independently checked through
`n=17`; the next trace was stopped when it reached 13 MiB.  Representative
profiles are:

| `n` | death horizon | additions | deletions | maximum width |
|---:|---:|---:|---:|---:|
| 1 | 3 | 2 | 27 | 1 |
| 4 | 5 | 21 | 68 | 12 |
| 8 | 5 | 250 | 92 | 32 |
| 12 | 7 | 5,263 | 1,277 | 90 |
| 16 | 7 | 15,224 | 5,552 | 132 |
| 17 | 7 | 22,878 | 14,801 | 130 |

The checker deliberately retains proof clauses named by deletion lines.  This
is sound: each retained clause was first RUP-checked, and adding an already
derived consequence can only strengthen later unit propagation.  It also
avoids depending on a producer's duplicate-deletion convention.

The result is useful but negative for the intended proof language.  The
observed proofs have neither bounded width nor bounded size, and no small
repeated induction is visible.  This does not prove that a short resolution
family is impossible; it shows that generic CDCL did not discover one.

## 4. Exact triangular correlation lemma

Let `P` be inverse Gray code on a width-`w` Boolean vector, with zero-based
indices:

```text
(P x)_k = XOR_(j >= k) x_j.
```

Then for all `x,y` over `F_2`,

```text
<P x, P y> = x^T K_w y,
(K_w)_(i,j) = (min(i,j)+1) mod 2.                 (1)
```

Indeed, the `(i,j)` entry of `P^T P` counts the indices
`k <= min(i,j)`.  Since `P` is unit triangular, it is invertible, so

```text
rank(K_w) = w.                                    (2)
```

The even- and odd-output-position pieces have ranks `ceil(w/2)` and
`floor(w/2)`.  `quadratic_probe.py` checked (1), both split versions, and all
three ranks on every pair through width 8 (87,380 word pairs total).

This identifies the exact algebra hidden in the earlier survival parity
`corr(u,v)`: it is a structured triangular quadratic form, not an arbitrary
global correlation.  But (2) is also an obstruction.  Its separable bilinear
rank grows with frontier width, so it cannot be replaced by a fixed number of
linear parity pairings.

## 5. Fixed quadratic closure also fails

A deliberately generous 37-bit candidate retained:

- `T mod 16`;
- even/odd parity and both endpoint bits of `A,V,C,S`;
- all 20 even/odd inverse-Gray correlations between unordered pairs from
  `A,V,C,S`;
- and, outside those 37 bits, the previous rho bit required by `no 11`.

Here `V=1|(B<<1)`, `C=I(A|V)`, and `S=A<<1`.  On legal hard-core finite-seed
paths it has an equal-depth closure collision:

```text
T = 32, previous rho = 0

origin (seed length, seed, follow, state)
  (15, 0x200, 1, (32,1431655765,984962389))
  (15, 0xa20, 1, (32,1431655765,716879189))
```

The current 37-bit summaries agree; both states force rho 1, pass the pin,
and preserve `no 11`; their successor quadratic summaries differ.  Therefore
this natural finite triangular-correlation algebra does not close.  The
result does not exclude a non-closed quadratic rank or an invariant involving
the full unbounded triangular form.

## 6. What remains worth trying

The hybrid attempt changes the best target but does not solve it.  The useful
next statement is now:

> **Linear hard-core mortality.**  Prove that every hard-core rho seed of
> length `n` dies within `2n+2` forced macrosteps.

Such a theorem would uniformly exclude alternating center traces after the
already-checked bilateral reduction.  The finite results suggest two more
specific instruments:

1. extract a parameterized interpolant or inductive clause from the *shortest*
   death instances, using frontier position relative to the deep boundary;
2. retain the full triangular form but seek a well-founded spatial statement
   about its moving endpoint, rather than compressing it to finitely many
   parity bits.

Finite UNSAT through `n=24` is not evidence enough to state the linear bound
as a theorem.

## 7. Reproduction

From this directory, with the repository's `python-sat` environment:

```bash
uv run --project ../../sygus-p3 python mortality_sat.py \
  --validate --max-validate 16

uv run --project ../../sygus-p3 python mortality_sat.py \
  --direct --max-n 24 --out mortality-direct-n24.json

uv run --project ../../sygus-p3 python mortality_sat.py \
  --threshold-sweep --max-n 17 --proof-dir mortality-threshold-proofs

uv run --project ../../sygus-p3 python quadratic_probe.py \
  --max-width 8 --max-seed 16 --max-follow 32

uv run --project ../../sygus-p3 python verify_drup.py \
  mortality-threshold-proofs/threshold-n17-h07.cnf \
  mortality-threshold-proofs/threshold-n17-h07.drup
```

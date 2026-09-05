# Why a finite-width spectral/transfer-matrix bound cannot prove `H_r(n) = 0`

Date: 2026-09-05.  Written because the idea was proposed again and is
seductive.  It is a *correct observation* attached to an *impossible
conclusion*.  Recording the refutation so it is not re-derived a fourth time.

## The proposal

Build a De Bruijn transition matrix for the hard-core constraint, compute its
dominant eigenvalue `lambda_max`, and conclude that `lambda_max < 2` at any
finite width `w` gives geometric collapse, hence extinction, hence a proof for
all `n` by finite certificate.

## 1. The spectral radius is `phi`, in closed form, and it is already known

The hard-core language on the RW alphabet `{1,2}` (no two adjacent 1s) has
transfer matrix `[[0,1],[1,1]]`.  Computed:

```text
spectral radius = 1.618033988750
golden ratio    = 1.618033988750   identical to 1e-12
phi/4           = 0.404508
```

`phi/4 = 0.4045` is exactly the decay constant this project already recorded,
and already explained: `phi^k` is hard-core (Fibonacci) language growth, `4^k`
is the forced-symbol alphabet.  **A width-`w` numerical eigenvalue computation
returns a constant we have in closed form.**  It is not new information.

## 2. `lambda_max < 2` is not an extinction condition.  It is vacuous here

`phi = 1.618 < 2` already.  So the proposed success criterion **fires
immediately, at every width, and always would** — while `H_r(n) = 0` remains
unproven.  A criterion that cannot fail is not a certificate.

The arithmetic: if surviving words grow like `lambda^n`, then `lambda < 2` says
the *fraction* of `{1,2}^n` surviving tends to 0.  It says nothing about the
*count*, which still diverges whenever `lambda > 1`.  Extinction of a
nonnegative integer count needs `lambda < 1`.  Here `lambda = phi > 1`, so the
hard-core constraint alone makes the population **grow**, not collapse.  All
of the extinction must come from the other constraints, which is precisely the
part a hard-core transfer matrix does not model.

## 3. The bound is tight exactly where it is useless

Real `D_k` from the brute-force census (`overnight_c2_even.log`, `n=24`,
`c=2`) against the hard-core transfer-matrix bound:

| k | transfer-matrix bound | actual `D_k` | ratio |
|---:|---:|---:|---:|
| 1..9 | 2,3,5,8,13,21,34,55,89 | 2,3,5,8,13,21,34,55,89 | **1.000** |
| 10 | 144 | 116 | 0.806 |
| 11 | 233 | 75 | 0.322 |
| 12 | 377 | 33 | 0.088 |
| 13 | 610 | 14 | 0.023 |
| 14 | 987 | 3 | 0.003 |

The bound is **exactly achieved** for `k < k_star`, where the population is
manifestly nonzero, and is off by 300x by `k = 14`, where extinction actually
happens.  A transfer-matrix upper bound is therefore tight precisely where it
proves nothing and hopeless precisely where the result lives.  No refinement of
the eigenvalue changes this: the departure at `k_star` is the whole phenomenon,
and it is exactly what the transfer matrix cannot see.

## 4. It is three recorded dead ends at once

* **(a) Transfer-matrix domination.**  Already tested to destruction:
  `RESULTS-TRANSFER-DOMINATION-CHECK.md` shows entrywise domination by
  `M = [[0,1/4],[1/4,1/4]]` is FALSE pointwise, worst case needing 1.75-4x.
* **(b) First moment via the forced-symbol map.**  REFUTED in
  `MEMO-PHI-OVER-4-FIRST-MOMENT.md`: the map is not equidistributed, its image
  saturates, and past `k ~ n/2` the required bound is `< 1`, impossible.  A
  spectral bound is a first-moment bound.
* **(f) Object conflation.**  The proposed script applies Rule 30 to a bit
  window and forbids `11` in the *output*.  `H_r(n)` is about
  `literal_extension`'s forced continuation over `{1,2}` with a `12a` terminal
  pull.  Different objects, as in `RESULTS-FIB-ABSENT-M8-M9-M10.md`.

## 5. The structural reason no fixed-`w` certificate can work

Verified this session against the source: `append_dependency_edge` recomputes
every array position from scratch on every call (appending 10 symbols rewrites
all 20 earlier positions).  The recursion has **genuinely unbounded memory with
no local mixing**.  A width-`w` transfer matrix is by construction a bounded-
memory model.  It cannot represent an unbounded-memory recursion at any finite
`w`, so no finite-width certificate closes `n -> infinity` for this object.

This is the same wall three independent representations already hit.

## What would actually be needed

Not a larger `w`.  A bound on the *departure* `Fib(k+1) - D_k` past `k_star`,
which is the regime-2 question and is pseudorandomness-flavoured.  The
first-moment route to it is closed by (b).  Nothing on the backlog currently
reaches it.

## Reproduction

`/private/tmp/.../scratchpad/hardcore_spectrum.py`, or four lines:

```python
import numpy as np
print(max(abs(np.linalg.eigvals(np.array([[0,1],[1,1]], float)))))  # 1.618033988750
```

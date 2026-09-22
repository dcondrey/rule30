# Orbit-only local boundary corrections: refuted wherever the lone seed repeats a window, vacuous above

Date 2026-09-19. Pre-registration `PREREGISTRATION.md` (committed before any
script existed). Simulator `orbit_current.c`, analysis `horizon.py`, log
`horizon.log`, record `horizon.json`. Registered outcome A held. This proves
nothing about P2; it closes the orbit-only local form of route 3 on the
measured data.

## 1. The class and the question

`RESULTS-quarter-wave-current-collision.md` excludes the time-independent
boundary correction

```text
K_t - rho = h(W_r(t+1)) - lambda * h(W_r(t)),   W_r(t) = x^t[-r..r],    (1)
```

for `r <= 5` from two hand-found witness pairs, with no search. Here the
search runs over the first `T = 2^20` lone-seed rows, `K_t` computed from
`q_i` directly on the full row.

- E1 (every `lambda`, `rho`): a repeated pair `(W_r(t), W_r(t+1))` with
  unequal `K` refutes (1) at radius `r`.
- E2 (`lambda = 1`, the telescoping case P2 needs): along the orbit (1) forces
  `h(W_r(t)) = h(W_r(0)) + sum_(u<t) K_u - rho t`, so each return of a window
  fixes `rho`; two returns fixing different `rho` refute (1) for every `rho`,
  and one return with `rho != 1/2` refutes the centred case.

## 2. Result

| quantity | lone seed | null model |
|---|---:|---:|
| `r_pair` (E1, all `lambda, rho`) | 18 | 18 |
| `r_one` (E2, `lambda = 1`, all `rho`) | 18 | 18 |
| `r_half` (E2, `lambda = 1`, `rho = 1/2`) | 19 | 19 |
| birthday radius `r_b` (uniform model) | 19 | 19 |

So (1) is refuted for every `h`, `lambda` and `rho` at every `r <= 18`. At
`r = 19` there is no repeated pair and one window return; it refutes only the
centred case `lambda = 1`, `rho = 1/2`, and leaves every other `rho` and
every `lambda != 1` unrefuted. At `r >= 20` no window repeats in `t < 2^20`,
so `h` is a free function of time along the data and (1) is satisfiable
trivially. Outcome C, a radius with enough repeats to test (1) and no
refutation, did not occur; `r = 19` is the one-return edge case above.

The distinct-window and horizon matches below are birthday statistics and
would match for any sequence of well-spread windows. The quantity that a
real orbit-only identity would move is how often the currents agree at a
repeated pair `(W_r(t), W_r(t+1))`. It matches the null:

| `r` | orbit: repeats with equal `K` / repeated pairs | null |
|---:|---:|---:|
| 8 | 1,309 / 693,180 | 1,368 / 693,278 |
| 9 | 326 / 304,025 | 359 / 304,346 |
| 10 | 89 / 91,546 | 90 / 91,820 |
| 11 | 24 / 23,877 | 28 / 24,250 |
| 12 | 7 / 5,966 | 4 / 6,104 |
| 13 | 2 / 1,479 | 0 / 1,547 |
| 14..18 | 0 / 463 | 0 / 524 |

(Counts are adjacent entries in `(W_r(t), W_r(t+1), K_t)` sort order within
one repeated pair class, `repeated_pairs - killing_pairs` in `horizon.json`;
from `r = 12` almost every class has two members.)

The distinct-window count `D_r(T)` matches the uniform expectation at every
radius, the largest relative gap being `6.0e-4` at `r = 9` (453,607 against
453,333; null 453,482). Radii 0 to 7 see every window. So the lone-seed
centre windows repeat exactly as often as independent uniform windows do, and
outcome B (more repeats than chance) did not occur.

The two recorded witnesses (radius 5, times 20 and 31; radius 2, times 29
and 41) are found by the same search.

## 3. What this closes

On this data the orbit-only local class has no intermediate regime. Below
about `log2 T` the windows repeat, and the repeats refute (1) for every `h`,
`lambda` and `rho` (through `r = 18`; `r = 19` only at `rho = 1/2`); above it the windows along the orbit are pairwise
distinct and (1) constrains nothing. A correction of the form (1) that
survives must use radius growing at least like `log2 T`, at which point the
window is a time label and the identity carries no locality. Because the
repeat statistics match the uniform model, there is no hidden reuse of centre
windows for a local correction to exploit, and the current agreement rate at
repeated pairs confirms it directly. The route-3 lever "an identity
valid only on lone-seed rows" is left with terms that depend on history or
sum over the growing half-row, the forms (1) does not cover.

Finite evidence: the horizon is measured at `T = 2^20` only; the dichotomy is
an observation about this `T`, and the match to the uniform model is
statistical, not a theorem.

## 4. Gates and a disclosed change

- G1: `c_t` equals `shell-maximum-o-n/center_sim.c` on all `2^20` bits.
- G2: `c_t = P_(t+1) - P_t + K_t` (record `aec10b5b09559ca1`) at every `t`,
  with `K` from `q_i`, not from the identity.
- G3: an independent set-based evolution with the literal Rule 30 table
  reproduces `P, K, W_31, c` for `t < 4096`; both witnesses are found.
- G4: the null model's horizons are within 2 of `r_b` (they equal 18, 18, 19).

The null model was changed after pre-registration and before the first
analysis run: the registered "i.i.d. windows and currents" would pair two
independent windows in E1, doubling the collision entropy and making the
null horizon about half of `r_b` by construction. The null used pairs each
uniform radius-32 row with its own one-step Rule 30 image, which has the
orbit's one-step dependence and no time structure; currents are the orbit's,
permuted (seed 20260919).

## 5. Reproduction

From this directory:

```sh
cc -O3 -march=native -o orbit_current orbit_current.c && ./orbit_current 1048576 orbit.bin   # 26 MB, not committed, about 20 s
uv run --no-project --with numpy python horizon.py --output horizon.json > horizon.log   # about 90 s
```

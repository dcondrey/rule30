# P2 routes 2 and 3: no twisted conservation law through window 11, and the digit-coupling residual is the whole window

Date 2026-09-19. Pre-registration `PREREGISTRATION.md` (committed before either
script existed). Scripts `twisted_conservation.py` (log
`twisted-conservation.log` and, through `m = 11`, `twisted-conservation-m11.log`,
records `twisted-conservation.json`, `twisted-conservation-m11.json`),
`digit_residual.py` with `column_sim.c` (log `digit-residual.log`, record
`digit-residual.json`). Both registered expectations held; neither result
proves or refutes P2.

## 1. T3 (route 3): Rule 30 has no spatially twisted local additive conservation law, windows 1 to 11

For every window `m = 1..11` and every twist `omega` of order
`p in {1, 2, 3, 4, 6, 8}`, the solution space of

```text
rho(y_0..y_(m-1)) - rho(x_1..x_m) = J(x_0..x_m) - omega * J(x_1..x_(m+1))
```

has density dimension exactly `2^(m-1)`, the trivial twisted coboundaries
(66 of 66 rows, excess 0; `m = 11` from the extension run, which repeats
every control and every row below it). The rank is exact over `GF(1000000009)` with
`omega` of order `p`; a rank mod a prime above `q` is at most the rank over
`Q(omega)`, so a trivial count mod `q` certifies the trivial count exactly.
`p = 1` reproduces the catalog record
`r30-bco-no-local-additive-conserved-density` (window 12 there). Controls, all
34 as expected: Rule 30 untwisted `2^(m-1)`; Rule 184 untwisted
`2^(m-1) + 1` (particle number); Rule 204 `2^m` at `p = 1, 3, 4`; and Rule 236
at `p = 4` with excess 1, 2, 3 at `m = 2, 3, 4`, a genuine twisted law, so
the instrument detects one when it exists. A scan of all 256 elementary rules
at `m <= 4` found such laws for 134 (rule, `p`) pairs, none for Rule 30.

The twists cover every periodic weight of period 1, 2, 3, 4, 6 or 8, the
quarter-wave `sin(pi i / 2)` included: a conserved `sum_i w_i rho(window_i)`
with `w` of period `P` stays conserved when the row is shifted, and the
`P` shifted identities are a Vandermonde system in the frequency components,
so each `sum_i omega^i rho(window_i)` with `omega^P = 1` is conserved on its
own. Every primitive root of each order was also run explicitly
(`verify_twisted.py`, gate G1: 108 (root, window) rows through `m = 9`, all
trivial), so the reduction does not rest on Galois conjugacy.

Alignment gate G2 (`verify_twisted.py`, log `verify-twisted.log`): random
combinations of the solver's null space are conserved under direct summation
of `sum_i omega^i rho(window_i)` on 40 random finite rows before and after
one step, for the Rule 236 twisted law (`p = 4`, `m = 3, 4`, both primitive
roots), Rule 184 and Rule 30, while a random `rho` is not. The equation the
solver builds is the conservation law it claims to be.

What this closes. A route-3 identity of the quarter-wave shape,
`x_0 - 1/2 = Phi(x^(t+1)) - Phi(x^t) + (boundary terms)` with
`Phi = sum_i omega^i rho(window_i)`, needs the interior current to vanish.
That is a universal twisted conservation law, and none exists for Rule 30 at
these windows and twists. So the interior current is unavoidable: the
quarter-wave current `K` is not an artifact of choosing the linear density
`x_i`. A route-3 identity with boundary terms only on the cone edges must use
a growing window, history, or an identity that holds only on the lone-seed
rows. The last is not excluded in general: a sum that vanishes on the orbit
rows alone need not decompose into local equations. Its local form is now
excluded on the measured data. Record
`r30-p2-orbit-window-horizon-refuted-or-vacuous`
(`experiments/rule30/p2-orbit-window-horizon/RESULTS.md`) searches the first
`2^20` lone-seed rows for a fixed-radius correction
`K_t - rho = h(W_r(t+1)) - lambda h(W_r(t))` and refutes it for every `h`,
`lambda` and `rho` at every radius `r <= 18`; at `r = 19` only the centred
case `lambda = 1, rho = 1/2` falls, and at `r >= 20` no window repeats, so
the identity is satisfiable there only because the data cannot test it. So no
fixed-radius orbit-only route-3 identity gains any support from these rows:
every radius they can test is refuted, bar the `r = 19` residue of `lambda
!= 1` and `rho != 1/2`. That leaves less than it once did. Record
`r30-p2-clocked-window-horizon-refuted-or-vacuous`
(`experiments/rule30/p2-clocked-window-horizon/RESULTS.md`) extends the
refutation to corrections clocked by `t mod p`, for the periods 1 to 8, 12
and 16, at every radius where the lone seed repeats a phase-matched centre
window.
Record `r30-p2-history-window-horizon-refuted-shape-independent`
(`experiments/rule30/p2-history-window-horizon/RESULTS.md`) refutes a
correction reading the last `d` windows of radius `r` whenever
`r + d - 1 <= 18`, for the measured depths `d <= 13`, and shows the
radius-18 refutation holds for every support shape inside that
neighbourhood: off-centre window, masked or sparse subset, weighted sum,
parity, or a half-row sum truncated to it. So history is covered, and so is
any sum confined to radius 18. For an unclocked correction what is still
untouched is then exactly an `h` reading a cell outside `[-18, 18]`: an
untruncated half-row sum, or a window growing past radius 18. A clocked one
keeps more, since the kill reaches only the last radius at which a
phase-matched repeat exists and that radius falls with the period, to
`r_pair = 15` at `p = 8` and `p = 16`; above it the rows cannot test the
identity rather than supporting it. A window that grows with `t` but stays inside radius
18 is covered at every `t`, and a single `h` applied to windows of different
widths at different times is a time-dependent family, vacuous on finite data.

Not covered: windows above 11, twists not a root of unity of these orders, non-additive or temporally twisted (`Phi(Fx) = lambda Phi(x)`)
invariants.

## 2. T2 (route 2): the digit-coupling residual covers the whole window and is balanced on the orbit

Over GF(2), `c_(t+L) = c_t XOR x^t_(-L) XOR x^t_L XOR R_j(x^t)`, `L = 2^j`.
Gate: at `L = 1` the orbit residual equals `c_t AND x^t_1` at every
`t < 2,099,199` (Rule 30 is Rule 150 plus `x_0 x_1`), and the simulator's
centre column matches `center_sim.c` on all 2,099,200 bits.

Exact truth tables (uniform inputs on `[-L, L]`):

| `L` | `Pr[R_j = 1]` | cells with zero influence | influence of `x_L` | smallest nonzero influence |
|---:|---:|---|---:|---|
| 1 | 0.2500 | `-1` | 0.5 | 0.5 (cells 0, 1) |
| 2 | 0.5000 | `-2` | 0.75 | 0.25 (cells 0, 1) |
| 4 | 0.4844 | `-4` | 0.9375 | 0.0625 (cell 3) |
| 8 | 0.5000 | `-8` | 0.9961 | 0.0039 (cell 7) |

`x_(-L)` never matters (left permutivity); every other cell does. The
residual region is the whole window, not `o(L)` cells.

Orbit, shells `k = 14..20`, `j = 3..10`: `|sum_t (-1)^(R_j)| / sqrt(N)` is at
most 2.61 (`k = 19`, `j = 5`) against the registered 4, and the residual
density is 0.497 to 0.505. The registered kill fires on both halves: the
linear part `x_(-L) XOR x_L` explains none of the lag-`L` correlation, and
the residual carries all of it.

A structural reading, stated as observation, not registered. The influence
of `x_L` on `R_j` approaches 1 while the cells just left of it approach 0
(cell 7 at `L = 8`: 0.004). So `F^L(x)_0` barely depends on the right end of
its window and `R_j` is close to `x_L` XOR a function of cells `-L+1..L/2`.
The Rule 150 linearization puts `x_L` in the wrong place. This is the known
asymmetry of Rule 30 (information moves right at speed 1 through the
permutive left input and leftward only through the OR), and it means a
route-2 coupling should be written in the left-permutive form
`c_(t+L) = x^t_(-L) XOR G_L(x^t_(-L+1..~L/2))`, with `G_L` again a full
nonlinear function. It does not rescue route 2 in this form.

## 3. What changed

- **Proved (finite, exact):** no twisted local additive conserved density of
  window `<= 11` for any periodic weight of period 1, 2, 3, 4, 6 or 8; no
  cell of `(-L, L]` is free of the residual for `L = 1, 2, 4, 8`.
- **Measured:** the lag-`2^j` residual is balanced on the orbit to
  `2.61 sqrt(N)` through `k = 20`, `j = 3..10`.
- **Open, unchanged:** P2; routes 2 and 3 in any form using growing windows,
  history, or orbit-only identities. The cross-review's section 6.1 reduction
  (route 1 = routes 2 and 3 through the cross term) stands, and both local
  forms of those routes now fail at the parameters above.

## 4. Reproduction

From this directory:

```sh
uv run --no-project --with numpy python twisted_conservation.py --mmax 10     # about 3 minutes
uv run --no-project --with numpy python verify_twisted.py                     # about 1 minute
cc -O3 -march=native -o column_sim column_sim.c && ./column_sim 2099200 columns.bin   # 48 MB, not committed
uv run --no-project --with numpy python digit_residual.py --columns columns.bin
```

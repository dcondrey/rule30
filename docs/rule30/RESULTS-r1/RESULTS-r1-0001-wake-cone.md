# Driven 0001: the residual bit is a global cancellation, not a shielded one

Date: 2026-09-15. **Status: negative structural result for the driven
family. `b_k = 0` (equivalently the period-four lock of the right neighbour)
remains observed, not proved, and this note shows it cannot be proved by any
bounded-width prefix invariant. No prize result.**

Setting as in [the boundary certificate](RESULTS-r1-0001-boundary-certificate.md):
Rule 30 on sites `i >= 1`, zero initial row, boundary `c_t = s(t,0)`,
`c = (0001)^infinity`. The certificate proves
`(r_(4k), r_(4k+1), r_(4k+2), r_(4k+3)) = (0, e_k, 1, 1)` with `e_k = 1`
exactly when the four-cell prefix at time `4k` is `C = 0111`, i.e.

    e_k = s(4k, 2).

The observed lock is `e_k = 0` for all `k >= 2` (to `t = 60,000` in the
certificate's own check; to `t = 4096` in every run here). This note asks
what kind of proof that statement can have.

## 1. The wake is a periodic boundary layer, a chaotic interior, and a period-doubling front

`r1_0001_wake_probe.py` (numpy, `T = 2048`): column `x` has eventual time
period 4 for `x = 1, 2, 3`, period 8 for `x = 4, ..., 11`, and no period
`<= 1024` for `x >= 12` on `[x+64, T-x]` (re-checked at `T = 4096`). The
density of ones on `[1, t]` is `0.488, 0.477, 0.488, 0.503` at
`t = 256, 512, 1024, 2047`. The rightmost one sits at `t - 3`. In the
comoving frame `s(t, t-d)` the front is nested rather than periodic: periods
`1, 1, 1, 1, 2, 2, 2, 2, 4, 8, 8, 16, 32, 32, 64, 64, 64` for `d = 0..16`
and none `<= 64` beyond. The nested front is not new: in the comoving frame
`f(t,d) = s(t, t-d)` Rule 30 is the triangular system
`f(t+1,d) = f(t,d) XOR (f(t,d-1) OR f(t,d-2))`, so every right diagonal is
purely periodic with a power-of-two period, the known right-cone
periodicity of `PATH.md` row 34 (Rowland 2006 Lemma 2; killed as a route
because the ordered depth is only `~2.4 log2 t`). It holds verbatim for a
driven half-plane. So the near-boundary periodicity is a boundary layer of
width eleven sitting against a chaotic zone; it is not part of a
space-time periodic tiling.

## 2. No prefix cylinder invariant of width 4 to 22 closes

`r1_0001_closure_probe.py` (`T = 4096`). Let `R_L` be the set of width-`L`
prefixes `s(4k, 1..L)` seen at block times `8 <= 4k < T - 8`. The
certificate's construction generalises to: `R_L` is an invariant if the
four-step driven map returns every `p in R_L` into `R_L` for every one of
the 16 exterior words on cells `L+1..L+4`. That fails at every width:

| `L` | `|R_L|` | escaping (prefix, exterior) pairs / total | distinct escapes |
|---|---|---|---|
| 4 | 1 | 4 / 16 | 1 |
| 8 | 2 | 16 / 32 | 3 |
| 11 | 4 | 20 / 64 | 4 |
| 12 | 6 | 25 / 96 | 5 |
| 16 | 27 | 15 / 432 | 5 |
| 19 | 104 | 139 / 1664 | 25 |
| 22 | 275 | 930 / 4400 | 155 |

For `L <= 10` the sets `R_L` (size 2) are complete by the period-8
structure of section 1, so those failures are exact, not sampling
artefacts: exterior words that never occur at block times in the real orbit
would break the boundary layer if they did occur. Beyond `L = 11` the set
grows by roughly a factor `1.5` per column, so widening the window enters
the chaotic zone without ever closing. Every prefix in every `R_L` has
`s(4k, 2) = 0`.

## 3. The residual bit depends on a positive fraction of the chaotic light cone

`r1_0001_cone_probe.py` traces the backward dependency of `s(4k, 2)`
through the actual orbit with the OR mask applied exactly: `s(t+1, x)` reads
`(t, x-1)` and `(t, x)` always and `(t, x+1)` only when `s(t, x) = 0`.

| `k` | `t = 4k` | max width of masked cone | cells in cone |
|---|---|---|---|
| 16 | 64 | 41 | 1,093 |
| 64 | 256 | 173 | 18,723 |
| 256 | 1024 | 693 | 296,072 |
| 512 | 2048 | 1369 | 1,168,818 |
| 1000 | 4000 | 2657 | 4,443,945 |

The masked cone has width `~0.66 t` and size `~0.28 t^2`. The mask removes
about one third of the unmasked light cone and nothing more. The value
`s(4k, 2) = 0` is therefore the output of a computation over
`Theta(t^2)` cells of the chaotic zone at every block time, not a locally
shielded quantity.

## 4. Consequence

`e_k = 0` is not a bounded-certificate statement. A proof must exhibit a
global property of the whole driven configuration (an exact identity or
invariant of the driven response `s(t, x) = F_(t,x)(c_0, ..., c_(t-1))`)
that forces the zero at phase `4k`, and the chaotic interior gives no local
handle on it. That is the same shape as the Rule 30 prize problems
themselves, so this sub-target is not smaller than P1 in kind; it is P1's
difficulty transplanted into a driven half-plane. The reduction
`M_(4q)(N) = sum 1{e_(k+q) != e_k}` of the certificate stands, and the
finite lock remains strong evidence, but no route to proving it through
prefix invariants exists at any width, and the earlier description of this
target as a small first piece of the mismatch mechanism was too optimistic.

Reproduction (numpy required, `T` as the single argument):

```sh
uv run --no-project --with numpy python experiments/rule30/r1_0001_wake_probe.py 2048
uv run --no-project --with numpy python experiments/rule30/r1_0001_closure_probe.py 4096
uv run --no-project --with numpy python experiments/rule30/r1_0001_cone_probe.py 4096
```

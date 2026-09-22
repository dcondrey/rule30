# Referee: the two `[U]` lemmas of `RESULTS-RIGHT-SEED-MARGIN.md`

Date 2026-09-16. Checker `referee.py` (log `referee.log`, exit 0, 0 failures, 0.7 s), written
from the definitions in section 1 of the results document and Lemmas 1, 2 of
`RESULTS-FORWARD-HALVING-LEMMA.md`; imports nothing from P1. Mutation tests (a wrong
reconstruction rule, a wrong `l` convention) break the prefix check on 48/60 and 60/60 pairs;
the bit-packed exhaustive path agrees with the scalar evolution on 505 sampled rows.

## Verdict 1: prefix lemma (section 1). HOLDS.

Every step checked, none refuted.

1. Induction shape. Write `A_T` for "pin through `T`", `B_T` for "`W` agrees with `xhat`
   through `T`". The proof shows `A_(T-1) => (a_T <=> b_T)` where `a_T` is the pin at `T` and
   `b_T` is `W_T = xhat_T`, then uses `A_(T-1) <=> B_(T-1)`. Since `A_T = A_(T-1) and a_T` and
   `B_T = B_(T-1) and b_T`, this gives `A_T <=> B_T` in both directions: when `A_(T-1)` fails
   both sides are false, when it holds both reduce to `a_T <=> b_T`. The base `T = 1` is
   `W_1 XOR y_1 = 1` against `xhat_1 = l_0 = 1 - y_1`, which agrees. Valid.
2. "The right (left) half-line has seen only the pin through `T-1`." `s(T-1, +-1)` reads
   `s(t,0)` only for `t <= T-2`. Valid under `A_(T-1)`.
3. Pin equation at `T`. `T-1` odd: `s(T,0) = s(T-1,-1) XOR 1` must be 0, so `s(T-1,-1) = 1 =
   l_(T-1)`. `T-1 = 2k`: `s(T,0) = s(T-1,-1) XOR rho_k` must be 1, so `s(T-1,-1) = 1 - rho_k =
   l_(T-1)`. Valid.
4. Lemma 2 applied to `W`. Lemmas 1 and 2 are stated for an arbitrary seed `x` on all of
   `i <= -1`; `W` padded by zeros is such a seed; `g = g_(T-1,1)`. Their inductions were
   re-derived and are correct (the OR term at `m = 1` reads the boundary constant).
5. "The reconstructed row obeys the same identity by construction." The reconstruction
   relation `col_(m+1)[t] = col_m[t+1] XOR (col_m[t] OR col_(m-1)[t])` is the Rule 30 relation
   `col_m[t+1] = col_(m+1)[t] XOR (col_m[t] OR col_(m-1)[t])` solved for the left neighbour
   (XOR is invertible), and `col_0[t] = t mod 2`. So by induction on `t` the reconstructed
   array is exactly the driven left half-line with the infinite seed `xhat`, for all `m, t`,
   and in particular `s(t,-1) = col_1[t] = l_t`. Lemma 2 at `(T-1, 1)` on that seed is the
   claimed identity with the same `g`. The step is justified. (Numeric: 60 seeds, `M = 200`,
   the driven evolution from `xhat_1..xhat_200` reproduces `col_m[t]` on the whole triangle
   `m + t <= 200` and `s(t,-1) = l_t` for `t <= 199`.)
6. Cancellation. With `W_m = xhat_m` for `m <= T-1`, `g` takes the same argument on both
   sides, so `s(T-1,-1) = l_(T-1)` iff `W_T = xhat_T`. Valid.
7. Finiteness of `y`. Not used: the driven right half-line and the plain evolution are
   defined for any `y`, and nothing bounds the light cone by the seed width. Finiteness of
   `W` is not used either. The hypotheses are stronger than the proof needs; not a defect.

Remark, not an objection: consequence (ii) reads a zero run as maximal (`xhat_(a+z+1) = 1`),
otherwise the loss time is later than `a + z + 1`. The check below uses maximal runs.

Numeric check (from scratch). 300 random pairs, `w_R` in `1..16`, `xhat` to `M = 200`:
100 random `W` of width `5..60`, 100 `W = xhat_1..xhat_a` with `a` in `1..60`, 100 such
truncations with one flipped bit. The first `t` with `s(t,0) != t mod 2` under plain Rule 30
with no boundary equals `min{m : W_m != xhat_m}` in 300 of 300; max `m*` 62; longest zero run
of `xhat` entered by a truncation 6.

## Verdict 2: eventually periodic traces are safe (section 7). HOLDS.

Every step checked, none refuted. Two gaps in the write-up, both closable in one clause and
neither affecting the conclusion:

- `P` must be even. The proof takes `P` from column `-1` and then needs column 0 (period 2)
  to be `P`-periodic for the base of the column induction. If `rho` is eventually constant 0,
  `l` is eventually all ones with minimal period 1, and `P = 1` breaks the base case. The fix
  is `P := 2p` for `p` a period of `rho`, which is what `l_(2k) = 1 - rho_k`, `l_odd = 1`
  gives directly; the proof should say so.
- `W = 0` has no leftmost 1. The argument needs `W != 0`, or the leftmost 1 of the whole
  configuration. `W = 0` loses the pin by `t = 2` for every `y` (`s(1,-1) = 0` but `l_1 = 1`),
  so the lemma holds there too.

Steps:

1. Column `-1` equals `l` for all `t`: forced by the pin equation (step 3 above) once the pin
   holds forever, with `rho_k = s(2k,1)` the driven trace. Valid.
2. Same `t_0` at every column. `s(t,-m-1) = s(t+1,-m) XOR (s(t,-m) OR s(t,-m+1))` reads times
   `t` and `t+1` of the two columns to the right; for `t >= t_0` both are `>= t_0`, so
   `P`-periodicity from `t_0` passes to column `-m-1` from the same `t_0`. The preperiod does
   not grow with `m`. Valid.
3. Left edge speed exactly 1. With the leftmost 1 at `e` and zeros to its left, cell `e-1`
   becomes `0 XOR (0 OR 1) = 1` and cell `e-2` becomes `0 XOR (0 OR 0) = 0`, as do all cells
   further left. So `s(t, -w_L - t) = 1`, `s(t, i) = 0` for `i < -w_L - t`, hence
   `s(t,-m) = 0` for `t < m - w_L` and `s(m - w_L, -m) = 1`. Valid.
4. Contradiction. For `m >= w_L + t_0 + P`, times `m - w_L - P >= t_0` and `m - w_L` differ by
   `P` and carry 0 and 1. Valid.
5. Finiteness of `y`: not used.

Numeric check (from scratch). Seeds `0x0020` and `0x00a0` (bit `j` = `s(0,j+1)`): `rho_k =
s(2k,1)` is `(01)^omega` through `k = 4000` for both. For `0x0020`, `xhat` is period 7 from
`m = 1`, word `1000000`, longest zero run 6. All `2^20` left rows on cells `-20..-1` evolved
directly (plain Rule 30, 64 rows per word, exact array) against `0x0020`: 1,048,576 of
1,048,576 lose the pin by `t = 44`; maximum loss time 22, attained only by
`W = xhat_1..xhat_20` (`0x04081`, ones at `m = 1, 8, 15`), whose next disagreement is
`xhat_22 = 1`. Loss-time histogram is `2^(20-t)` rows at `t = 1..20` and one row at 22, and
the direct loss time equals `min{m : W_m != xhat_m}` on all `2^20` rows; `22 <= 20 + 7`.

## Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --no-project --with numpy python crosscheck/verify-0916/margin/referee.py > crosscheck/verify-0916/margin/referee.log 2>&1
```

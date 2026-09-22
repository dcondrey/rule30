# The halving lemma of the forward form, and the bijection of its survivors with rho prefixes

Date: 2026-09-16. Checker `forward-boundary/halving_lemma_check.py`, log
`forward-boundary/halving_lemma_check_k0-9.log` (exit 0, every check PASS, `k = 0..9`).
Proves the halving asserted (not proved) by `forward_survivor_census.py` and recorded in
`RESULTS-FORWARD-BOUNDARY-CENSUS.md` section 2b and `PROOF-STATE-CAPSULE.md` section 2.

**`[U]` Let the left half-line `i <= -1` run Rule 30 forward with boundary `s(t,0) = t mod 2`
and seed `x_m = s(0,-m)`, and let `C_k = s(2k,-2) XOR s(2k,-1)` be the period-two condition
`(L1)` at even step `k`. Then `C_k` is a function of `x_1, ..., x_(2k+2)` alone and is affine
with coefficient 1 in `x_(2k+2)`: `C_k = x_(2k+2) XOR G_k(x_1, ..., x_(2k+1))`. Hence for each
`k` and each assignment of `x_1..x_(2k+1)` exactly one value of `x_(2k+2)` satisfies `C_k = 1`,
the partial seeds on `-(2k+2)..-1` satisfying `C_0 = ... = C_k = 1` number exactly `2^(k+1)`,
and they are in bijection with the `2^(k+1)` words `(rho_0, ..., rho_k)`, `rho_j = 1 - s(2j,-1)`,
through a triangular map with unit diagonal. For words of width exactly `w` the count after
conditions `0..k` is `2^(w-2-k)` for `k <= floor((w-3)/2)`, and the first step at which halving
can fail is `k = floor((w-1)/2)`, the step whose new coefficient-1 bit is the fixed leftmost 1
(even `w`) or the fixed 0 beyond it (odd `w`). `[C]` The halving, the level count and the
distinctness of the `rho` prefixes are checked exhaustively for `k = 0..9` (`2^20` seeds at
`k = 9`); the light cone is checked on 2048 sampled seeds per `k` under random padding here
and exhaustively to length 12 by the referee's `crosscheck/verify-0916/halving/`. Nothing
here bounds the free phase; it identifies the controllable phase exactly and says that its
survivors are precisely "the source `W` is free", the endpoint form's premise (the
identification `rho_u <-> e_u = (1 - rho_u, rho_u)` is identity I2 of
`RESULTS-FORWARD-ENDPOINT-DICTIONARY.md`, not a consequence of the lemmas here).**

## 1. Objects

Rule 30 on `i <= -1`: `s(t+1,i) = s(t,i-1) XOR (s(t,i) OR s(t,i+1))`, with `s(t,0) = t mod 2`
read as the right neighbour of column `-1` and never updated. Seed `x_m = s(0,-m)`, `m >= 1`.
`(L1)` at step `k` is `C_k = 1`; by the rule at `i = -1`, `s(2k+1,-1) = s(2k,-2) XOR (s(2k,-1)
OR 0) = C_k`, so `C_k = 1` is exactly "column `-1` is 1 at time `2k+1`", the pin's odd-time
obligation `l_(2k+1) = 1` (`RESULTS-FORWARD-BOUNDARY-CENSUS.md` section 1).

## 2. Two lemmas and the theorem

**Lemma 1 (light cone).** `s(t,-m)` depends only on `x_1, ..., x_(m+t)`.
Induction on `t`: `s(t+1,-m)` reads `s(t,-m-1)`, `s(t,-m)`, `s(t,-m+1)`, which by hypothesis
depend on `x_1..x_(m+1+t)`. (For `m = 1` the right neighbour is the boundary constant.)

**Lemma 2 (left-permutivity along the diagonal).** There are functions `g_(t,m)` with
```text
s(t,-m) = x_(m+t) XOR g_(t,m)(x_1, ..., x_(m+t-1)).
```
Induction on `t`: `t = 0` is `s(0,-m) = x_m`. For the step,
`s(t+1,-m) = s(t,-m-1) XOR (s(t,-m) OR s(t,-m+1))`; the first term is
`x_(m+1+t) XOR g_(t,m+1)(x_1..x_(m+t))` by hypothesis, and the OR term depends only on
`x_1..x_(m+t)` by Lemma 1. So `s(t+1,-m) = x_(m+t+1) XOR g'(x_1..x_(m+t))`.

**Theorem (halving).** `C_k = s(2k,-2) XOR s(2k,-1) = x_(2k+2) XOR G_k(x_1..x_(2k+1))` with
`G_k = g_(2k,2) XOR x_(2k+1) XOR g_(2k,1)`, by Lemma 2 at `(t,m) = (2k,2)` and `(2k,1)`.
Therefore:

1. For fixed `x_1..x_(2k+1)`, exactly one `x_(2k+2)` gives `C_k = 1`.
2. Level `L = 2k+2` (partial seeds on `-L..-1` with `C_0 = ... = C_k = 1`) has exactly
   `2^(L/2)` members: level 2 has two (`x_2 = 1 XOR x_1`), and level `2k+2` extends each
   level-`2k` member by a free `x_(2k+1)` and a forced `x_(2k+2)`, because `C_0..C_(k-1)`
   do not read `x_(2k+1), x_(2k+2)` (Lemma 1). This is the factor 2 that
   `forward_survivor_census.py` asserts at every level; its docstring's `2^(L/2+1)` is a
   typo for `2^(L/2)`.
3. **Bijection with rho prefixes.** On level `2k+2`, `x_2, x_4, ..., x_(2k+2)` are determined
   by `x_1, x_3, ..., x_(2k+1)`, and `rho_j = 1 - s(2j,-1) = 1 XOR x_(2j+1) XOR g_(2j,1)(x_1..x_(2j))`
   is affine with coefficient 1 in `x_(2j+1)` given the earlier bits. So
   `(x_1, x_3, ..., x_(2k+1)) -> (rho_0, ..., rho_k)` is triangular with unit diagonal, hence a
   bijection of the `2^(k+1)` survivors onto all `2^(k+1)` binary words of length `k+1`.
4. **Width-`w` words.** With `x_w = 1` and `x_m = 0` for `m > w`, condition `C_k` forces a
   free bit iff `2k+2 <= w-1`, so the survivor count after `C_0..C_k` is `2^(w-1-(k+1))`
   for `k <= floor((w-3)/2)`, and the first `k` at which halving is not guaranteed is
   `floor((w-1)/2)`. `RESULTS-FORWARD-BOUNDARY-CENSUS.md` section 2 counts conditions
   survived (its table's first column is one condition), so its `2^(w-1-k)` after `k`
   conditions is `2^(w-2-k)` here after `k+1` and the two agree; its stop `floor((w-2)/2)`
   names the last guaranteed halving for even `w` and is one short for odd `w`
   (`N_9 = 128, 64, 32, 16, 10` halves through four conditions).

## 3. Result of the check

`halving_lemma_check.py 9`: for `k = 0..9`, over all `2^(2k+2)` seeds: (LC) six random padding
bits beyond `-(2k+2)` never change `C_k` (2048 samples per `k`); (H) every prefix
`x_1..x_(2k+1)` has exactly one completing `x_(2k+2)`; (B) the level count is `2^(k+1)`,
column `-1` is 1 at every odd time `<= 2k-1` on every survivor, and the `rho` prefixes of the
survivors are pairwise distinct. All PASS, exit 0.

## 4. Reading

The controllable phase is now a theorem, not a census, and it says what the endpoint form
assumes: after `k+1` conditions the survivors are exactly parametrized by a free `rho`
prefix of length `k+1`, one symbol per condition. In the endpoint form this is the source
`W in {1,2}^n` being free while everything else is forced, so the two forms agree on where
the freedom sits. What the lemma does not touch is the free phase, `C_k` for
`k >= floor((w-1)/2)` on a width-`w` word, where every `C_k` is a fixed function of the
`w-1` free bits with no new coefficient-1 variable; that phase is `4` to `11` even steps on
`w = 12..30` (8 at `w = 12`, 11 at `w = 30`, not monotone) and it is the object a proof must
bound. Under the hard-core condition the right half imposes it is `1` to `8` on `w <= 40`
(`RESULTS-FORWARD-SURVIVOR-W40.md`), and that is the `(PT2)`-relevant statistic. The single-flip picture of
`RESULTS-FLIP-PAIRING.md` ("a flip at any depth but the first three source symbols is a
fresh coin on every forced level") is the same statement in the endpoint coordinates.

## 5. Scope

Uniform proof, no restriction on `k` or `w`. The exhaustive check is a check of the
coordinate bookkeeping to `k = 9`. `RW`, `(SEP)`, `(PT2)` untouched.

## 6. Reproduction

```sh
uv run --no-project --with numpy python forward-boundary/halving_lemma_check.py 9   # 30 s
```

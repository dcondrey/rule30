# Proof of lemma `driven-lhp-column-minus-one-aperiodic`, structural-inductive form

**Scope correction, 2026-09-15:** the aperiodicity theorem below is
unaffected, but the later discussion calling the literal PIN-Pi horn
open is superseded. The boundary `c=110^infinity` passes every pin test
in the zero-initial LHP and is eventually constant. Its full centre glue
fails. See [the exact counterexample and repaired scope](../../../../../docs/rule30/RESULTS-r1-periodic-realization-scope.md).

Date: 2026-09-03.  Output directory:
`/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-structural/`.
Finite checks: `verify_driven_lhp.py`, log `verify_driven_lhp.log` (same directory), all
gates `PASS`, total mismatches 0 in 4.2 s.  Every numbered check `G1..G7` cited below is a
line of that log.

## 0. Verdict and scope

**Proved, uniformly in all parameters (level `U`).**

1. **Theorem 1** (the lemma).  For every finite `y`, every eventually periodic boundary word
   `c`, and under the nondegeneracy hypothesis `(ND)` of section 1, the column
   `l_t = LHP_y(c)(t,-1)` is not eventually periodic.
2. **Theorem 2** (stronger, the screening's observation (1) made a theorem).  For every finite
   `y` and every boundary word `c` whatsoever, if `LHP_y(c)` satisfies `(ND)` then no two
   distinct columns `x_1 < x_2 <= 0` of `LHP_y(c)` are both eventually periodic.  With `c`
   eventually periodic this says no column `x <= -1` is eventually periodic.  This is Jen 1986
   Theorem 2b (at most one eventually periodic column of a finite Rule 30 configuration)
   transferred to the driven half-plane; it is labelled as that, not as a discovery.
3. **Consequence (a)** (Proposition A).  If the true centre column `c*` is eventually periodic
   then `Z = {t : c*_t = 0}` is infinite and `r*|Z` is not eventually periodic.  Hence
   `R1 <=> P1` as propositions (Corollary A.1).
4. **Consequence (b)**, in the form that is actually a theorem (Proposition B): for a word `c`
   with `c_0 = 1`, `c = c*` if and only if the rule at `x = 0` holds at every `t` with `l` from
   `LHP_seed(c)` and `r` from `RHP_seed(c)`; the rule at `x = 0` is the pin at one-times and the
   coupling at zero-times, and both half-planes are consistent with every `c`.

**Two corrections to the lemma text**, neither of which is a gap in the proof.

- *Hypothesis.*  "Nonzero finite `y`" must be read as `(ND)`: `y(x) = 1` for some `x <= -1`, or
  `c_t = 1` for some `t`.  With `y` zero on `x <= -1` and `c = 0^omega` the driven half-plane is
  identically zero and `l = 0^omega` is periodic, so the lemma is false without `(ND)`; the
  lemma's own proof text assumes "`c` has infinitely many ones", which an arbitrary eventually
  periodic `c` need not satisfy.  `(ND)` is exactly the right hypothesis, and it holds in the
  intended application (`c*_0 = 1`).
- *Clause (b)-must.*  "Any proof of P1 must use the coupling at the zero-times" is not a
  theorem and is not proved here.  Its only mathematical content is the negation of
  `(PIN-Pi)` (there exists an eventually periodic `c` with `c_0 = 1` whose driven left half-plane
  satisfies the pin at every one-time), which is OPEN and is currently screened in the opposite
  direction (`uc/r1-r1zero-screen-pin-pi-no-periodic/lock_search_T32768_p8.log`: `CONFIRMED
  LOCKS 0`; `pin_tree_L48.log`: `atcap=0` for every tail).  If `(PIN-Pi)` is ever proved, P1
  follows from the pin alone and clause (b)-must is false.  Section 7 gives the defensible
  statement.

**What this lemma does not do.**  It implies none of `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)`,
P1.  Theorems 1 and 2 hold verbatim for Rule 90 (section 8), so by obstruction B they are
limitation theorems about the route R1, not proof routes.

## 1. Definitions

**Rule.**  `f(a, b, c) = a XOR (b OR c)`, applied as `s(t+1, x) = f(s(t, x-1), s(t, x), s(t, x+1))`.
The only properties of `f` used in sections 2 to 5 are

```text
(F0)  f(0, 0, 0) = 0
(F1)  f(0, 0, 1) = 1
(LP)  f(a, b, c) = a XOR g(b, c) with g(b, c) = b OR c     (left permutivity)
```

`(F0)`, `(F1)` are read off the definition.  Rule 90 (`g(b, c) = c`) satisfies all three.

**Driven left half-plane.**  Let `y : Z -> {0,1}` have finite support and let `c = (c_t)_{t >= 0}`
be any binary word.  `LHP_y(c)` is the array `s(t, x)`, `t >= 0`, `x <= 0`, defined by

```text
s(0, x) = y(x)                                   x <= -1
s(t, 0) = c_t                                    t >= 0
s(t+1, x) = f(s(t, x-1), s(t, x), s(t, x+1))     x <= -1, t >= 0
```

The recursion at `(t+1, x)` with `x <= -1` reads only positions `x-1, x, x+1 <= 0`, so it is
well defined and, by induction on `t`, `LHP_y(c)` is the unique array satisfying the three
displayed lines.  `LHP_seed(c)` means `y = delta_0` (zero on `x <= -1`).  `RHP_y(c)` is the
mirror object on `x >= 0`: `s(0, x) = y(x)` for `x >= 1`, `s(t, 0) = c_t`, and the same rule at
`x >= 1`, reading `x-1 >= 0`.  Write `l_t = s(t, -1)` and `r_t = s(t, 1)`.

**Nondegeneracy.**  `(ND)`: `LHP_y(c)` is not identically zero.  Equivalently, `y(x) = 1` for
some `x <= -1` or `c_t = 1` for some `t >= 0`: if `y` is zero on `x <= -1` and `c = 0^omega`
then every row is zero by induction on `t` (`(F0)` below); conversely a `1` in `y` on
`x <= -1` is a `1` in row `0`, and `c_t = 1` is a `1` in row `t`.

**Eventually periodic.**  A sequence `(u_t)_{t >= 0}` is eventually `P`-periodic from `T` if
`u_{t+P} = u_t` for all `t >= T`; eventually periodic if this holds for some `P >= 1`, `T >= 0`.
If `u` is eventually `p`-periodic from `T` it is eventually `kp`-periodic from `T` for every
`k >= 1` (apply the identity `k` times).

**Restriction to a set.**  For an infinite set `Z = {z_1 < z_2 < ...}` of times and a sequence
`u`, `u|Z` is the sequence `k -> u_{z_k}`; "`u|Z` eventually periodic" means this indexed
sequence is eventually periodic.  Lemma 7 converts an index period into a time period.

## 2. The ordered object: the moving edge

For each `t` let `S_t = {x <= 0 : s(t, x) = 1}` and, when `S_t` is nonempty, `m_t = min S_t`.

**Lemma 1 (finite support).**  `S_t` is finite for every `t`.

*Proof.*  Induction on `t`.  `S_0` is contained in `supp(y) union {0}`, finite.  If `S_t` is
finite with `m = m_t` (or `S_t` empty), then for `x <= -1` with `x + 1 < m` (or any `x <= -1`
when `S_t` is empty) all three arguments of `f` at `(t+1, x)` are `0`, so `s(t+1, x) = 0` by
`(F0)`.  Hence `S_{t+1}` is contained in `[m - 1, 0]` (or in `{0}`), finite.  QED.

**Lemma 2 (the edge moves left by exactly one cell per step).**  Suppose `S_t` is nonempty and
`m = m_t`.  Then `S_{t+1}` is nonempty and `m_{t+1} = m - 1`; explicitly `s(t+1, m-1) = 1` and
`s(t+1, x) = 0` for all `x < m - 1`.

*Proof.*  `m <= 0`, so `m - 1 <= -1` and the driven recursion applies at `(t+1, m-1)`.  Its
arguments are `s(t, m-2) = 0`, `s(t, m-1) = 0` (both below the minimum of `S_t`) and
`s(t, m) = 1`; by `(F1)`, `s(t+1, m-1) = 1`.  For `x < m - 1` all three arguments `s(t, x-1)`,
`s(t, x)`, `s(t, x+1)` are at positions `< m`, hence `0`, and `(F0)` gives `s(t+1, x) = 0`.
QED.

This case analysis covers `m = 0` (then `s(t, 0) = c_t = 1` is the only one and the argument
reads `c_t` at `x + 1 = 0`) and `m <= -1` alike; nothing about `c_{t+1}` enters, because the
overwritten cell `x = 0` is never the cell `m - 1 <= -1`.

**Corollary 2.1 (edge law).**  Under `(ND)` some `S_t` is nonempty; let
`t_0 = min{t : S_t nonempty}` (if `y` is nonzero on `x <= -1` then `t_0 = 0`; otherwise `t_0`
is the first `t` with `c_t = 1`, since by Lemma 1's induction `S_t` stays empty until then)
and `a = m_{t_0} <= 0`.  Then for every `t >= t_0`:

```text
m_t = a - (t - t_0),   s(t, m_t) = 1,   s(t, x) = 0 for all x < m_t.          (EDGE)
```

*Proof.*  Induction on `t >= t_0` using Lemma 2 for the step; the base is the definition of
`a`.  QED.

`(EDGE)` is the ordered object of the structural argument: the map `t -> m_t` is a strictly
decreasing bijection from `[t_0, infinity)` onto `(-infinity, a]`.  Each column `x <= a` is
visited by the edge exactly once, at time `t_0 + (a - x)`, and is identically zero before that
time.

Finite gate: `G2a` checks `(EDGE)` at every `t <= 40` for all `64` initial words `y` on
`x = -1..-6` and all `256` period-8 drives, both rules (`32766` nondegenerate runs, `0`
violations); `G2b` for `1000` random `(y, c)` with aperiodic `c` at `T = 200` (`0` violations);
`G2c` gates the integer kernel against an explicit cell array (`123041` cells, `0` mismatches).

## 3. The column-to-column invariant: periodicity is transported leftward

**Lemma 3 (back-solve).**  For all bits `a, b, c`, if `d = f(a, b, c)` then
`a = d XOR g(b, c)`.

*Proof.*  From `(LP)`, `d XOR g(b, c) = a XOR g(b, c) XOR g(b, c) = a`.  Exhaustive over the 8
triples and both rules: `G1`, `0` mismatches.  QED.

Applied to the driven recursion at `(t+1, x)`, `x <= -1`:

```text
s(t, x-1) = s(t+1, x) XOR ( s(t, x) OR s(t, x+1) ).                          (BS)
```

**Lemma 4 (one step of the invariant).**  Let `x <= -1` and `P >= 1`, `T_0 >= 0`.  If columns
`x` and `x+1` of `LHP_y(c)` are eventually `P`-periodic from `T_0`, so is column `x-1`.

*Proof.*  For `t >= T_0`, using `(BS)` at `(t+P+1, x)`, then periodicity of column `x` at the
times `t+P` and `t+P+1` (both `>= T_0`) and of column `x+1` at time `t+P`, then `(BS)` at
`(t+1, x)`:

```text
s(t+P, x-1) = s(t+P+1, x) XOR ( s(t+P, x) OR s(t+P, x+1) )
            = s(t+1, x)   XOR ( s(t, x)   OR s(t, x+1) )
            = s(t, x-1).
```

QED.

**Corollary 5 (whole half-plane).**  If columns `0` and `-1` of `LHP_y(c)` are eventually
`P`-periodic from `T_0`, then every column `x <= 0` is eventually `P`-periodic from the same
`T_0`.

*Proof.*  Let `S(k)` be "columns `-k` and `-k+1` are eventually `P`-periodic from `T_0`",
`k >= 1`.  `S(1)` is the hypothesis.  `S(k)` implies `S(k+1)` by Lemma 4 with `x = -k`.  By
induction `S(k)` holds for all `k >= 1`.  QED.

The invariant transported column to column is "`P`-periodic from `T_0`", with `T_0` unchanged
at every step; the step is `(BS)`, which is the decoupled (left-permutive) form of the rule.
Finite gate: `G3` reconstructs columns `-2..-61` from columns `0, -1` by `(BS)` on `40` random
drives at `T = 300` (`505200` cells, `0` mismatches).

## 4. Theorem 1

**Theorem 1.**  Let `y` be finite, `c` eventually periodic, and `(ND)` hold.  Then
`l_t = LHP_y(c)(t, -1)` is not eventually periodic.

*Proof.*  Suppose `c` is eventually `p`-periodic from `t_c` and `l` eventually `q`-periodic from
`t_l`.  Put `P = pq` and `T_0 = max(t_c, t_l)`.  Column `0` is `c`, eventually `P`-periodic
from `t_c <= T_0`, and column `-1` is `l`, eventually `P`-periodic from `t_l <= T_0`; by
Corollary 5 every column `x <= 0` is eventually `P`-periodic from `T_0`.

By `(ND)` and Corollary 2.1 the edge law `(EDGE)` holds from some `t_0` with edge origin `a`.
Let `T_1 = max(T_0, t_0)` and `x* = m_{T_1} - P = a - (T_1 - t_0) - P`; then `x* <= -1`.

- For `T_1 <= t < T_1 + P`: `m_t = m_{T_1} - (t - T_1) > m_{T_1} - P = x*`, so `x* < m_t` and
  `s(t, x*) = 0` by `(EDGE)`.
- At `t = T_1 + P`: `m_t = m_{T_1} - P = x*`, so `s(T_1 + P, x*) = 1` by `(EDGE)`.

Column `x*` is eventually `P`-periodic from `T_0 <= T_1`, so `s(T_1 + P, x*) = s(T_1, x*) = 0`.
This contradicts `s(T_1 + P, x*) = 1`.  QED.

In words: periodicity of two adjacent columns is transported to every column by `(BS)`; the
edge visits each far-left column exactly once after being zero there for a full period, which
no periodic column can do.  Only `(F0)`, `(F1)`, `(LP)` were used.

Finite instances (not proof steps): the 172 screened drives of
`uc/r1-r1zero-screen-driven-lhp-column-minus-one-aperiodic/driven_lhp_aperiodic_T131072_deep1048576.log`
(`FINAL: l eventually periodic in 0/172`), and two instances outside that family in `G7`,
`c = 0^omega` with `y = {-1}` and with `y = {-3, -1}` at `T = 4096`: no eventual period
`q <= 256` with onset `<= T/2`, longest shift-agreement run `19` at the random null `20.0`,
edge violations `0`.

## 5. Theorem 2: no two eventually periodic columns at any distance

**Theorem 2.**  Let `y` be finite, `c` any binary word, and `(ND)` hold for `LHP_y(c)`.  Then
there are no `x_1 < x_2 <= 0` such that columns `x_1` and `x_2` are both eventually periodic.
In particular, if `c` is eventually periodic, no column `x <= -1` of `LHP_y(c)` is eventually
periodic.

*Proof.*  Suppose columns `x_1 < x_2 <= 0` are eventually periodic; take a common period `P`
and a common onset `T_0` (product of the two periods, maximum of the two onsets).  Let
`d = x_2 - x_1 >= 1`.

*Step 1: the strip between them is eventually periodic.*  If `d = 1` there is nothing to show.
If `d >= 2`, let `sigma_t = (s(t, x_1+1), ..., s(t, x_2-1))` in `{0,1}^{d-1}`.  For
`x_1 < x < x_2` the recursion at `(t+1, x)` reads positions `x-1 >= x_1` and `x+1 <= x_2`, so
`sigma_{t+1} = G(sigma_t, s(t, x_1), s(t, x_2))` for a fixed map `G`.  For `t >= T_0` the two
boundary bits are functions of the phase `phi_t = (t - T_0) mod P`.  Hence
`omega_t = (sigma_t, phi_t)` satisfies `omega_{t+1} = H(omega_t)` for a fixed self-map `H` of
the finite set `Omega = {0,1}^{d-1} x Z/P`, for all `t >= T_0`.  Among
`omega_{T_0}, ..., omega_{T_0 + |Omega|}` two coincide, `omega_i = omega_j` with
`T_0 <= i < j`; then `omega_{t + (j - i)} = omega_t` for all `t >= i` by induction on `t`.  So
every interior column is eventually `(j - i)`-periodic from `i`.

*Step 2: two adjacent eventually periodic columns.*  Columns `x_1` and `x_1 + 1` are now both
eventually periodic (`x_1 + 1` is interior if `d >= 2`, and is `x_2` if `d = 1`).

*Step 3: the sub-half-plane.*  The array `s'(t, x') = s(t, x' + x_1 + 1)` for `x' <= 0` is
`LHP_{y'}(c')` with `y'(x') = y(x' + x_1 + 1)` (finite) and `c'_t = s(t, x_1 + 1)`: the three
defining lines of section 1 hold for it because the driven recursion of `LHP_y(c)` at
`x <= x_1 <= -1` is the same recursion.  It satisfies `(ND)`: by `(EDGE)` the cell
`(t_0 + (a - x_1 - 1), x_1 + 1)` is `1` if `x_1 + 1 <= a`, and the cell `(t_0, a)` with
`a <= x_1` is `1` otherwise.  Its boundary `c'` is eventually periodic (Step 2) and its column
`-1` is column `x_1`, eventually periodic (hypothesis).  Theorem 1 applied to `LHP_{y'}(c')`
gives a contradiction.  QED.

Step 1 is rule-independent; Steps 2 and 3 use Theorem 1.  Prior art: Jen 1986 Theorem 2b and
Jen 1990 Proposition 3 prove "at most one eventually periodic column" for finite
configurations of the full plane; Theorem 2 is that statement for the driven half-plane and is
labelled validation of known structure.  The screening's observation that columns `-1..-8`
are all aperiodic in every drive (`periodic single columns among -1..-8: 0` in the log cited
in section 4) is an instance.

## 6. Consequence (a): R1's conclusion is refuted by R1's hypothesis

**Lemma 6 (the true left half-plane is the driven one).**  Let `s*` be the Rule 30 spacetime
diagram of the lone seed and `c*_t = s*(t, 0)`.  Then `s*(t, x) = LHP_seed(c*)(t, x)` for all
`t >= 0`, `x <= 0`, and `s*(t, x) = RHP_seed(c*)(t, x)` for all `t >= 0`, `x >= 0`.

*Proof.*  Induction on `t`.  At `t = 0` both arrays are `delta_0` on `x <= 0` (resp. `x >= 0`).
If they agree on row `t` (for `x <= 0`), then for `x <= -1`,
`LHP(t+1, x) = f(LHP(t, x-1), LHP(t, x), LHP(t, x+1)) = f(s*(t, x-1), s*(t, x), s*(t, x+1)) = s*(t+1, x)`
since `x+1 <= 0`; and `LHP(t+1, 0) = c*_{t+1} = s*(t+1, 0)`.  The right half-plane is the
mirror argument with `x-1 >= 0`.  QED.  Finite gate: `G4a` (`16793603` cells, `0` mismatches),
`G4b` (`8394753` cells, `0` mismatches), `T = 4096`.

**The rule at `x = 0`.**  `c*_{t+1} = l*_t XOR (c*_t OR r*_t)`.  Hence

```text
c*_t = 1  =>  l*_t = 1 XOR c*_{t+1}                    (PIN)
c*_t = 0  =>  r*_t = c*_{t+1} XOR l*_t                 (COUPLING)
```

`(PIN)` is `(BS)` at `x = 0` with the OR saturated; `(COUPLING)` is `(BS)` at `x = 0` on the
zero set.  Finite gate: `G4c`, `2028` one-times and `2068` zero-times to `T = 4096`, `0`
violations each.

**Lemma 7 (eventually periodic sets).**  Let `c` be eventually `p`-periodic from `t_c` and
`Z = {t : c_t = 0} = {z_1 < z_2 < ...}` infinite.  Let `k_p = |Z intersect [t_c, t_c + p)|`.
Then `k_p >= 1` and there is `k_0` with `z_{k + k_p} = z_k + p` for all `k >= k_0`.
Consequently, if `(u_{z_k})_k` is eventually `q`-periodic in `k` from `k_1`, then with
`Q = qp` and `t_r = max(z_{k_0}, z_{k_1})`: `u_{z + Q} = u_z` for every `z in Z` with
`z >= t_r`, and `z + Q in Z` for every such `z`.

*Proof.*  If `k_p = 0` then by periodicity `Z intersect [t_c, infinity)` is empty and `Z` is
finite, contrary to hypothesis.  The map `t -> t + p` is an order-preserving bijection from
`Z intersect [t_c, infinity)` onto `Z intersect [t_c + p, infinity)`: it maps into it because
`c_{t+p} = c_t = 0`, and every `t' >= t_c + p` in `Z` is the image of `t' - p >= t_c`, which is in
`Z` because `c_{t'-p} = c_{t'} = 0`.  Let `z_{k_0}` be the least element of `Z` that is `>= t_c`.
Listing both sets in increasing order, the first is `z_{k_0}, z_{k_0+1}, ...` and the second is
`z_{k_0 + k_p}, z_{k_0 + k_p + 1}, ...` (the second set omits exactly the `k_p` elements of `Z`
in `[t_c, t_c + p)`).  An order-preserving bijection between two increasing enumerations maps
the `i`-th element to the `i`-th element, so `z_{k_0 + i} + p = z_{k_0 + k_p + i}` for all
`i >= 0`.  For the consequence: for `k >= max(k_0, k_1)`, `z_{k + q k_p} = z_k + qp = z_k + Q`
(apply the first identity `q` times) and `u_{z_{k + q k_p}} = u_{z_k}` (apply the index
periodicity `k_p` times).  QED.

**Proposition A.**  Suppose `c*` is eventually `p`-periodic from `t_c`.  Then

1. `Z` is infinite, and
2. `r*|Z` is not eventually periodic.

*Proof.*  By Lemma 6, `l* = LHP_seed(c*)(., -1)`, and `(ND)` holds because `c*_0 = 1`.  By
Theorem 1, `l*` is not eventually periodic.

(1)  If `Z` were finite, then for all `t` beyond `max Z` we would have `c*_t = 1` and by
`(PIN)` `l*_t = 1 XOR c*_{t+1}`, which is eventually `p`-periodic because `c*` is.  Contradiction.

(2)  Suppose `(r*_{z_k})_k` is eventually `q`-periodic from `k_1`.  By Lemma 7 there are `Q = qp`
and `t_r` with `r*_{z+Q} = r*_z` for all `z in Z`, `z >= t_r`.  Let `T = max(t_c, t_r)` and
`t >= T`.  Since `Q` is a multiple of `p` and `t, t+1 >= t_c`: `c*_{t+Q} = c*_t` and
`c*_{t+Q+1} = c*_{t+1}`.  Two cases.

- `c*_t = 1`: then `c*_{t+Q} = 1`, and `(PIN)` at `t` and at `t+Q` gives
  `l*_{t+Q} = 1 XOR c*_{t+Q+1} = 1 XOR c*_{t+1} = l*_t`.
- `c*_t = 0`: then `t in Z`, `t + Q in Z`, and `(COUPLING)` at `t` and at `t+Q` gives
  `l*_{t+Q} = c*_{t+Q+1} XOR r*_{t+Q} = c*_{t+1} XOR r*_t = l*_t`.

So `l*` is eventually `Q`-periodic from `T`, contradicting Theorem 1.  QED.

**Corollary A.1 (R1 is P1).**  Let `(R1)` be the proposition "if `c*` is eventually periodic
then `r*|Z` is eventually periodic" and `(P1)` the proposition "`c*` is not eventually
periodic".  Then `(R1) <=> (P1)`.

*Proof.*  `(P1) => (R1)`: the antecedent of `(R1)` is false.  `(R1) => (P1)`: if `c*` were
eventually periodic, `(R1)` would give `r*|Z` eventually periodic and Proposition A(2) would
give the opposite.  QED.

So the register's row 1 equivalence "column `-1` eventually periodic `<=>` `r*|Z` eventually
periodic, assuming `c*` eventually periodic" (`PATH.md` section 2) is an equivalence between
two statements that are both false under that assumption.  The zero-set obligation cannot be
discharged; under R1's hypothesis it is provably violated, and the violation lives entirely in
the left half-plane, which by Lemma 6 is a function of `c*` alone.

## 7. Consequence (b): what the constraints on a candidate word are

**Proposition B (assembly).**  Let `c` be a binary word with `c_0 = 1`, `l = LHP_seed(c)(., -1)`,
`r = RHP_seed(c)(., 1)`.  The following are equivalent:

1. `c = c*`;
2. `c_{t+1} = l_t XOR (c_t OR r_t)` for every `t >= 0`;
3. `(PIN)` holds at every `t` with `c_t = 1` and `(COUPLING)` holds at every `t` with
   `c_t = 0`.

*Proof.*  `(2) <=> (3)` is the case split on `c_t`.  `(1) => (2)` is Lemma 6 together with the
rule at `x = 0`.  `(2) => (1)`: glue `LHP_seed(c)` and `RHP_seed(c)` along their common column
`0` into an array `S` on all of `Z x Z_{>= 0}`.  `S(0, .) = delta_0`.  At `(t+1, x)` with
`x <= -1` and with `x >= 1`, `S` satisfies the Rule 30 recursion by construction of the two
half-planes; at `x = 0` it satisfies it by (2).  So `S` is a Rule 30 diagram from the lone seed;
by uniqueness of forward evolution `S = s*`, and `c = S(., 0) = c*`.  QED.

Finite gate: `G5`, all `2^12` words with `c_0 = 1` at `T = 12`: exactly `1` satisfies (2) for
all `t < 12`, and it is `c*[:13]`.  (For information, `77` satisfy the pin alone at `T = 12`.)

**Corollary B.1.**  `(P1)` holds if and only if no eventually periodic `c` with `c_0 = 1`
satisfies (3).  Both `LHP_seed(c)` and `RHP_seed(c)` exist for every `c` and satisfy the Rule 30
recursion at every cell off column `0`; the only constraints on `c` are those of (3).

This is the defensible content of clause (b): the constraint set on a candidate periodic word
is exactly `(PIN)` on one-times (a self-constraint of the left half-plane) plus `(COUPLING)` on
zero-times (which reads the right half-plane through `r`).  Nothing here says that a P1 proof
must use `(COUPLING)`; whether `(PIN)` alone already excludes every eventually periodic `c` is
`(PIN-Pi)`, open.  What Theorem 1 adds to the picture is negative: the mechanism R1 hoped for
(make `l` periodic, then invoke two adjacent periodic columns) is unavailable, because `l` is
aperiodic for every eventually periodic drive, whether or not `(COUPLING)` holds.

## 8. Rule 90 and the obstruction audit

**Rule 90.**  Sections 2 to 5 used only `(F0)`, `(F1)`, `(LP)`; Rule 90 satisfies all three, so
Theorems 1 and 2 hold for the Rule 90 driven half-plane with the same proof.  `G6`:
`LHP_seed(1 0^omega)` for Rule 90 has `l_t = [t = 2^j - 1]` through `T = 4096`, aperiodic, edge
violations `0`; this is the mirror of a1's computation and an instance of the Rule 90 Theorem 1.
Lemma 6, Lemma 7 and Proposition B are also rule-independent.  Proposition A uses `(PIN)`, a
Rule 30 fact, only to handle the finite-`Z` case and the one-times; its Rule 90 analogue
(with `l_t = c_{t+1} XOR r_t` at every `t`) holds with the same proof.  So every statement in
this file is a limitation theorem: it constrains what R1 can be, and it is not a route to P1.

| Obstruction | Status for this lemma |
|---|---|
| A, `O(log t)` wall | Not applicable: nothing is propagated from the trace into the diagram; the edge law `(EDGE)` reaches distance `t` exactly because it is a statement about the support boundary, not about determined interior cells. |
| B, Rule 90 filter | Passed in the only sense available: Theorems 1, 2 hold for Rule 90 too (section 8, `G6`), so they are explicitly not a proof route and are recorded as a limitation theorem. |
| C, single-column blindness | Not applicable: the statement is about one column and is decided by it. |
| D, missing composition law | Not applicable: the composition law is `(BS)`, written out and gated (`G1`, `G3`). |
| E, measure-zero single orbit | Not applicable: no measure; the lone-seed diagram is handled exactly by Lemma 6. |
| F, free boundary of a fixed-depth strip | Evaded: Corollary 5 transports the invariant through every column, infinite depth; the contradiction is at column `x*`, arbitrarily far left. |
| G, arbitrary-input measures | Not applicable. |
| H, finite data | Not applicable: every step is a derivation; the log lines are gates on identities and instances, not evidence for the theorem. |

## 9. Finite checks, one line each (`verify_driven_lhp.log`)

| Line | What it gates | Result |
|---|---|---|
| `G1` | Lemma 3, all 8 triples, Rules 30 and 90 | `0` mismatches |
| `G2a` | Corollary 2.1 `(EDGE)`, exhaustive `y` on `x = -1..-6` and period-8 drives, `T = 40`, 2 rules | `32766` runs, `0` violations |
| `G2b` | `(EDGE)`, random `y` (width `<= 24`), random aperiodic `c`, `T = 200`, 2 rules | `1000` runs, `0` violations |
| `G2c` | integer kernel vs cell-array reference | `123041` cells, `0` mismatches |
| `G3` | Corollary 5's mechanism `(BS)`, columns `-2..-61` from `0, -1`, 40 drives, `T = 300` | `505200` cells, `0` mismatches |
| `G4a`, `G4b` | Lemma 6, `T = 4096` | `16793603` and `8394753` cells, `0` mismatches |
| `G4c` | `(PIN)`, `(COUPLING)` on the true diagram, `T = 4096` | `2028` and `2068` checks, `0` violations |
| `G5` | Proposition B, all `2^12` words, `T = 12` | exactly `1` solution, equal to `c*[:13]` |
| `G6` | Rule 90 instance of Theorem 1 | `l_t = [t = 2^j - 1]`, no period `q <= 256`, `0` edge violations |
| `G7` | Theorem 1 instances with `c = 0^omega`, `y = {-1}` and `{-3,-1}`, `T = 4096` | no period `q <= 256`, run `19` vs null `20.0`, `0` edge violations |

Reproduce: `cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant && uv run python uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-structural/verify_driven_lhp.py`.

## 10. Register consequence (for the maintainer; no file outside this directory was edited)

`PATH.md` row 1 (R1, OPEN, "best route") should read: equivalent to P1 (Corollary A.1);
under its own hypothesis the zero-set obligation is provably violated inside the left
half-plane (Proposition A), so no property of `c` or of the right half-plane can discharge it;
a P1 proof by this route is a proof that no eventually periodic `c` with `c_0 = 1` satisfies
`(PIN)` at all one-times and `(COUPLING)` at all zero-times (Corollary B.1), with `l` aperiodic
for every such `c` (Theorem 1) and every column `x <= -1` aperiodic (Theorem 2).  The lemma's
clause "(b) any proof of P1 must use the coupling" should be struck: its content is
`NOT (PIN-Pi)`, which is open and screened the other way.

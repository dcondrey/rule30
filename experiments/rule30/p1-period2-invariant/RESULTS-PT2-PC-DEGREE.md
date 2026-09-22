# Refutation degree of the alternation systems is the full seed width

Date: 2026-09-16.

**`[C]` Polynomial-calculus refutation degree equals the axiom floor at every
one of the 266 (placement, generator set) pairs through `w = 14`, and its
per-width maximum is `n = w-2`, the number of free seed bits, at every
`w = 4..14`. A refutation must load a generator of degree `n` and then closes
at that degree, in both generator sets, so the direct-seed `F2` certificate
route named at `RESULTS-PT2-PANEL-2026-09-15.md` section 2 is closed for
polynomial calculus as it was for Nullstellensatz: the degree grows as `w-2`
on the measured range in both proof systems. The panel's staircase
`0,0,0,1,1,1,2,2,2,3,3` counted multiplier degree only. The axiom floor alone,
which lower-bounds every proof system with degree-bounded lines, is `n` at
every `w = 4..27` (floor-only computation past `w = 14`). `(SEP)` and `(PT2)`
at `PROOF-STATE-CAPSULE.md:48` are untouched.** Scripts: `pt2_pc_degree.py`
(record `pt2_pc_degree.json`), the independent `pt2_pc_degree_crosscheck.py`
(record `pt2_pc_degree_crosscheck.json`), and `pt2_pc_floor_probe.py`.

## 1. Systems and measures

Placements are the panel's: width `w`, support `[a, a+w-1]` with `a` in
`[-w, 1]`, tight (`x_a = x_b = 1` substituted), free interior bits
`n = w-2`, centre `c_t = Tr_0(y)_t` as a multilinear polynomial over `F2` in
the free bits, `g_t = c_t + (t mod 2)`, `h*` the first `h` at which
`g_0..g_h` have no common zero (`RESULTS-PT2-PANEL-2026-09-15.md:24-31`). Both
generator sets refute the same ideal in `B_n = F2[x]/(x_i^2 + x_i)`:
`S_g = {g_0..g_(h*)}` and `S_D = {c_0, c_1+1, D_0..D_(h*-2)}`, `D_t = c_t + c_(t+2)`.

Four degrees per system, `ml` the multilinear reduction:

- axiom floor: least `d` at which the generators of degree `<= d` alone have
  no common zero. Every refutation in any proof system whose lines have
  degree `<= d` uses only those generators, so it lower-bounds all of the
  following.
- `ns_mult`: least `d` with `sum ml(h_g g) = 1`, `deg h_g <= d`. This is the
  panel's `nullstellensatz_degree` (`pt2_panel_C_anf_cert.py`,
  `solve_certificate`); it counts multipliers only.
- NS degree: least `d` with `1` in `span{ml(m g) : m a monomial, deg m + deg g <= d}`,
  the Nullstellensatz degree in `F2[x]` with Boolean axioms, where the product
  `m g` has degree `deg m + deg g` before reduction.
- PC degree: least `d` with `1` in `Cl_d(S)`, the smallest subspace of the
  degree-`<= d` multilinear polynomials that contains the generators of degree
  `<= d` and contains `ml(x_i p)` for every `p` in it with
  `deg ml(x_i p) <= d`. This is the polynomial-calculus refutation degree over
  `F2` with Boolean axioms: a refutation multilinearizes line by line without
  raising degree, and `x_i^2 m` reduces via `(x_i^2 + x_i) m` at the same
  degree. The closure is computed as the fixed point of
  `V <- V + sum_i ml(x_i (V cap M_i(d)))` with `M_i(d)` the span of the
  monomials of degree `< d` and the degree-`d` monomials divisible by `x_i`;
  multiplying a basis of `V` alone is wrong, since two basis vectors whose
  degree-`d` parts are not divisible by `x_i` can sum to one whose part is
  (control C1 below is exactly such a case).

One further quantity was measured and discarded: the least `d` with `1` in
`span{ml(m g) : deg ml(m g) <= d}`. Reduction can drop `deg ml(m g)` below
`deg g`, so this admits a generator that no degree-`d` line may load, and it
falls below the PC degree at 66 of the 266 pairs, always by exactly one. The
smallest case is `n = 2`, `S = {x1x2 + x2 + 1, x1 + 1}`: `ml(x1 (x1x2 + x2 + 1)) = x1`,
so `1 = x1 + (x1 + 1)` with reduced products of degree 1, while the only
degree-`<= 1` generator `x1 + 1` is satisfiable, so floor and PC degree are 2.
Both implementations found this independently. It is not the degree of any
proof system and is kept in the records only as `ns_full`.

## 2. Result

Per-width maxima over placements; PC and floor coincide in both systems at
every width, NS is given for `S_g / S_D`. `w = 1..3` have `n <= 1` and every
degree 0.

| `w` | `n` | placements | `h*` max | PC = floor | NS | `ns_mult` | placements at PC `= n` |
|---|---|---|---|---|---|---|---|
| 4 | 2 | 6 | 4 | 2 | 2 / 2 | 1 | 2 |
| 5 | 3 | 7 | 5 | 3 | 3 / 3 | 1 | 2 |
| 6 | 4 | 8 | 7 | 4 | 4 / 4 | 1 | 1 |
| 7 | 5 | 9 | 9 | 5 | 6 / 5 | 2 | 4 |
| 8 | 6 | 10 | 8 | 6 | 6 / 6 | 2 | 3 |
| 9 | 7 | 11 | 15 | 7 | 7 / 7 | 2 | 4 |
| 10 | 8 | 12 | 10 | 8 | 9 / 9 | 3 | 5 |
| 11 | 9 | 13 | 11 | 9 | 10 / 10 | 3 | 3 |
| 12 | 10 | 14 | 12 | 10 | 11 / 10 | 3 | 4 |
| 13 | 11 | 15 | 15 | 11 | 12 / 12 | 4 | 2 |
| 14 | 12 | 16 | 15 | 12 | 13 / 13 | 4 | 5 |

Per placement: PC degree equals the axiom floor at all 266 pairs; `S_g` and
`S_D` have the same PC degree at 117 of the 133 placements; NS exceeds PC by
0, 1 or 2 everywhere. Largest values seen: PC 12, NS 13, `ns_mult` 4,
generator degree 12, all at `w = 14`.

Floor only, `w = 15..27` (`pt2_pc_floor_probe.py --wide 15 20` and
`--wide 21 27`, one implementation, no closure, record
`pt2_pc_floor_probe_wide.json`): the per-width maximum axiom floor is again
`n` at every width, `13..25`, with `h*` maxima `16, 18, 17, 19, 21, 21, 22,
28, 24, 24, 25, 35, 35`. Since the floor lower-bounds the degree of any
refutation whose lines are degree-bounded, the maximal refutation degree is
at least `w-2` at every `w = 4..27` in every such system, not only in the two
measured.

Reading. The degree of a refutation is set entirely by the lowest-degree
subfamily of generators that is already unsatisfiable; once those are
admitted, degree-`d` polynomial calculus needs nothing above them. The
generator `g_t` has degree `n` exactly when its top coefficient, the parity of
its truth table over the `2^n` free assignments, is 1, so "floor `= n`" says
that the even-weight alternation constraints of the placement always leave a
survivor and only an odd-weight `g_t` kills it. That is an exact
reformulation of the measurement, not a mechanism: eleven widths, no proof.

`pt2_pc_floor_probe.py` looks for a mechanism at the 121 placements with
`n >= 2` and finds none of the simple ones. Full degree is not monotone in
`t`: at 23 placements `deg g_t` falls back below `n` after first reaching it,
`(9,-9)` running `-1,-1,1,1,1,2,3,3,4,5,7,7,6,7,6,7` over `t = 0..15`. The
light-cone bound, `deg g_t = n` only if `t >= max(b-1, -a)`, holds at all 807
`(placement, t <= h*)` pairs but is not sharp: 60 pairs at or past that time
have degree below `n`. Floor `= n` is not even "some generator has full
degree": at `(5,-1)`, `(6,-3)`, `(9,-6)`, `(13,-9)` and `(13,-6)` full-degree
generators exist, a later generator of degree `n-1` completes the kill, and
the floor is `n-1`. The common-zero set `Z` of the even-weight generators at
the 35 floor-`= n` placements is a single seed at 14 of them, equals
`V_(h*-1)` at 21, is never all-ones and alternating once; its left part
`x_a..x_0` takes at most three values per `a` across all widths, the variation
sitting entirely in the right part. What is stable is where the full floor
sits. For `w >= 10` and `a >= -8` the death time `h*(w,a)` does not depend on
`w` (`a: h*` is `-8:8, -7:10, -6:10, -5:9, -4:4, -3:6, -2:3, -1:8, 0:0, 1:2`),
and floor `= n` is carried by the fixed offsets `a = -5` at every `w = 7..14`,
`a = -7` at every `w = 9..14`, `a = -6` at `w = 10, 11, 12, 14`, plus sporadic
far-left placements with large `h*`: `(9,-9)` 15, `(12,-10)` 11, `(14,-11)`
13, `(14,-9)` 15. Since floor `= n` needs a full-degree generator at some
`t <= h*`, hence `h*(w,a) >= max(a+w-2, -a)`, that block can carry the full
floor only through `w = 16`, `19` and `18` respectively; past that, growth as
`w-2` needs far-left placements whose death time keeps pace, `h* >= n/2` at
the least. That is what happens at `w = 15..27`: `a = -5` never holds the full
floor again, `a = -7` only at `w = 15`, `a = -6` at `w = 15, 16, 18`, and from
`w = 19` the full floor sits only at `a` in `[-24, -8]`, at 6 to 11 placements
per width, with `h*` up to 35. The `w`-independence of `h*(w,a)` persists for
`a >= -7` through `w = 27` and breaks at `a = -8`: 8 for `w <= 14`, 15 at
`w = 15..17`, 17 at `w = 18..27`. The largest death times, `h* = 35` at
`(26,-20)` and `(27,-20)`, sit inside the support rather than at its far-left
end.

## 3. Controls

- C1, closure fixture, `n = 4`, `d = 2`, `S = {x1x2 + x3x4 + x2, x1x3 + x3x4 + x4}`:
  `x1x3 + x1x4 = ml(x1 (p + q))` is in `Cl_2(S)` (dimension 5), not in
  `span(S)`, and not in the basis-only closure. Both implementations.
- C2, induction principle `IND_m` (Buss and Pitassi 1998), `S = {x_1 + 1}`,
  `{x_i x_(i+1) + x_i}`, `{x_m}`: PC degree 2 for every `m = 2..12`; NS
  degree `2,2,3,3,3,3,4,4,4,4,4`, non-decreasing and above 2 from `m = 4`,
  the known `Theta(log m)` separation. Both implementations. `ns_mult` is
  `1,1,1,1,2,2,2,2,2,2,2`.
- C3, the checked-in panel: 88 placements at `w <= 11`, `h*` maximum 15 only
  at `(9,-9)`, per-width maximum `ns_mult(S_g)` equal to `0,0,0,1,1,1,2,2,2,3,3`,
  and every placement matching `pt2_panel_C_run_w11.log` on `n`, `h*`, `dNS_g`
  and `dNS_D`. Both implementations.
- Invariants asserted on every pair: floor `<=` PC `<=` NS, `ns_mult <=` NS,
  and `1 in Cl_n(S)`, the closure at full degree computed directly for every
  placement in the cross-check and for `n <= 7` in the primary, with `PC <= n`
  and monotonicity of `Cl_d` in `d` covering the rest.

## 4. Independent cross-check

`pt2_pc_degree_crosscheck.py` shares no code with the primary or the panel:
it simulates each of the `2^n` seeds as an integer row and collects truth
tables bit by bit, stores polynomials as `numpy` coefficient vectors over the
monomial index, runs bit-packed `GF(2)` elimination, and computes
`V cap M_i(d)` by stacking bases (Zassenhaus) rather than by a projection
kernel; every ANF it uses is re-evaluated at all `2^n` points against the
simulated table. On the 117 placements it completed, `w <= 13`, the two
records agree on `n`, `h*`, floor, `ns_mult`, `ns_full` and PC for both
systems, 1,170 fields, 0 mismatches. Its pre-cancellation NS variant, which
admits `ml(m g)` when every `|t cup m|` over terms `t` of `g` is `<= d`, has
the same per-width maxima as PC and exceeds PC only at `(9,-3)` and `(9,-1)`
in `S_D`, 7 against 6.

## 5. Scope

Finite, `w <= 14`, 133 placements, both generator sets, one variable set (the
raw seed bits). The kill is of bounded-degree certificate families over those
bits in either proof system on this range; a change of variables, or a
certificate system that is not degree-bounded (resolution width, cutting
planes), is not measured. Nothing here touches `(SEP)`; `(PT2)` is the
all-width statement these finite refutations do not reach. The exact question
left is whether the death time keeps pace with the width: the floor reaches
`n` at `(w,a)` only if `h*(w,a) >= max(a+w-2, -a) >= (w-2)/2`, so the `w-2`
growth continues exactly as long as some placement dies late enough. On the
range the margin is wide, `h*` maxima `16..21` against a requirement of
`7..9` at `w = 15..20` and `22..35` against `10..13` at `w = 21..27`, but the
only uniform statements about alternation
death times are the bounded left-depth certificates (`docs/rule30/FACT-INDEX.md`,
alternating trace excluded through left depth 24), and no growth law for `h*`
is proved or attempted here.

## 6. Reproduction

From the repository root:

```sh
uv run --no-project python \
  experiments/rule30/p1-period2-invariant/pt2_pc_degree.py 14 \
  experiments/rule30/p1-period2-invariant/pt2_pc_degree.json
uv run --no-project --with numpy python \
  experiments/rule30/p1-period2-invariant/pt2_pc_degree_crosscheck.py 13 \
  experiments/rule30/p1-period2-invariant/pt2_pc_degree_crosscheck.json
uv run --no-project python \
  experiments/rule30/p1-period2-invariant/pt2_pc_floor_probe.py
uv run --no-project python \
  experiments/rule30/p1-period2-invariant/pt2_pc_floor_probe.py --wide 15 20
uv run --no-project python \
  experiments/rule30/p1-period2-invariant/pt2_pc_floor_probe.py --wide 21 27
```

The floor probe imports the primary's generator construction, reproduces `h*`
and floor from the record at all 121 placements with `n >= 2` and on its fast
path at every `w = 14` placement, and runs in about two seconds per mode
through `w = 20`. `--wide 21 27` costs 1.9, 4.1, 8.9, 19.6, 43, 107 and 255 s
per width, doubling with each width, 7.3 min in all; the per-width JSON for
`w = 15..27` is `pt2_pc_floor_probe_wide.json`.

The primary is pure standard library and exits 0 in 140 s single-core, of
which `w = 14` is 122 s; `w <= 11` completes in about one second. The
cross-check exits 0 in 314 s, 248 s of it at `w = 13`, and declines `w = 14`
under its own 15-minute budget since each width costs about 4.8x the last. Both print the per-width table and the controls and exit nonzero
on any control or invariant failure. The checked-in `.json` files are the
records; the `.log` files beside them are ignored by the global git config.

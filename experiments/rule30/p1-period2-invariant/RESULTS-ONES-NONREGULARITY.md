# Non-regularity of L_1(c) along 1^m: closed form, separating suffixes to level 17, and the exact gap

Date: 2026-09-16. Pre-registration `PREREGISTRATION-ONES-NONREGULARITY.md`
(written before the run). Scripts and logs in `nonregularity/`:
`ones_closed_form.py` (log `ones_closed_form.log`, 16 lines, rc=0) and
`ones_separation.py` (log `ones_separation.log`, rc=0). Kernel `psi_kernel.py`
(`Endpoint`, `CONE`, `BOUNDARY`); oracle `crosscheck/source-residuals/oracle_1m.py`
(`in_L1`). Every number below names its log line.

**`[U]` Closed form: after `sym^m` (`sym` in `{1, 2}`) the Endpoint holds
`T[m-1][d] = sym` if `m + d` is even and `sym XOR 3` otherwise, for every
`-m <= d <= m-1`; the proof is two `CONE` entries per symbol plus induction on
`m`, and the transducer reading `(sym, sym XOR 3)` returns to its state after one
period (`ones_closed_form.log` lines 1 to 8), `[C]` verified cell by cell for
`m <= 200` (lines 9, 10). Corollary `[U/C]`: `1^m` lies in neither `L_1(2)` nor
`L_1(3)` for any `m >= 1`, and `2^m` lies in `L_1(2)` iff `m` is even and in
`L_1(3)` iff `m` is odd (lines 11 to 14). `[U]` Reduction: after `1^m` every
later column is a window of one `m`-independent triangle `U(j, e)`, `e = d + m`,
and the cut of `1^m v s` is the cell `U(q, 2m + q)`, `q = |v|`: the suffix reads
the periodic column `q` at position `2m + q`, so the length `m` is observed as a
position, not as content (`[C]` 6048 triples against the oracle,
`ones_separation.log` line 3). `[U]` For `v` ending in `2` the membership is
`f_v(m) = [F(Pi_m^{-1}(1,0)) = 0]` with `Pi_m` the `D8` product of column
`q-1` over `[-q, 2m+q)`, `f_3 = 1 - f_2` exactly (line 4), and `m, m'` are
separated iff the stretch `D` of column `q-1` between the two cut positions
satisfies `F' + beta(Pi_m)(h' + 1) = 1` for `(h', F') = D^{-1}(cell 2)`: always
when `D` moves cell `3` to cell `2`, never when it fixes cell `2`.
`[C]` Certified separating family: for every level `a = 4..17` an explicit
suffix `A[a]` of length `a` (`2112`, `21112`, `212112`, `2111112`, ...,
`22111111211111112`) with `f_c(m + 2^a) != f_c(m)` for ALL `m >= 0` and both
`c`, proved by a tower recurrence plus an exhaustive check over one period
(lines 67 to 94), and a table over residues mod 16 for `a <= 3` (lines 5 to 66).
Hence every pair `m != m'` with `m != m' (mod 2^18)` is Nerode-separated, and any
DFA for `L_1(c)` has at least `2^18 = 262144` states, up from the measured 1100.
`[C]` The rule `v(m, m', c)` separates all 4032 `(m, m', c)` with
`1 <= m < m' <= 64` under the `Endpoint` oracle alone, with `|v| <= 5`
(line 95). `[K]` The pre-registered kill fired in its second clause: the closed
form yields no separating family for all pairs. The naive family `2 1^(a-2) 2`
fails at `a = 6, 10, 11, 12, 13, 14, 15, 16, 17` (lines 71 to 93); the
one-period maps `Phi_k` of the columns along `2 1^k` are `(1,0,1), (1,1,0), id,
z, (1,0,1), z, (1,0,0), z, z, id, (0,1,0)` for `k = 0..10` with the tower period
stalling at `k = 2` and `k = 9` (lines 97 to 108); among the candidates with at most two inner `2`s
the certified count falls `3, 1, 1, 0` at `a = 14..17` and level 17 needs a
three-`2` suffix, 6 of 105 (lines 93, 94). No induction closes, so the theorem
"`L_1(c)` is not regular" is NOT proved; what stands is the `2^18` bound, and
the exact gap is section 2.8.**

## 1. Objects

`L_1(c) = {W in {1,2}^* : the s in {1,2} with cut_0(W s) = c exists and is
admissible after W}`, `c in {2, 3}`; `s = 1` after a final `1` is inadmissible
(`oracle_1m.py`, `in_L1`). `1^m` is not hard-core (factor `11`), so it probes the
wide language; `2^m` is the control.

Endpoint coordinates (`psi_kernel.py`): after `e_0 .. e_u` the state holds
`T[u][d]` for `-u-1 <= d <= u`, with `column[i] = T[u][-i]` (`i = 0..u+1`) and
`diagonal[k] = T[u][k]` (`k = 0..u`); `T[u][-u-1] = e_u`, `T[u][-u] =
BOUNDARY[e_u] = e_u XOR 3`, `T[u][d+1] = CONE[T[u-1][d]][T[u][d]]` for
`-u <= d < u`. `CONE = ((0,1,3,2), (3,2,1,0), (3,2,0,1), (3,2,1,0))`. The cut of
`W s` with `|W| = n` is `T[n][n]`. The "column" and the "anti-diagonal" of the
older documents are the two halves `d <= 0` and `d >= 0` of the same column
`T[u][.]`.

Affine model. A cell `x` is the point `(h, F) = (H(x), E(x))` of `F_2^2`,
`E = 1 + H + Lo`: `0 -> (0,1)`, `1 -> (0,0)`, `2 -> (1,0)`, `3 -> (1,1)`. The
letter of `x` is the affine map `(alpha, beta, gamma) = (1 + (1+h)F, h + F, 0)`
acting by `(h, F) -> (h + alpha, F + beta h + gamma)`: `0 -> (0,1,0)` (the
shear `sigma`), `1 -> (1,0,0)` (the translation `tau`), `2 -> (1,1,0)` (`tau
sigma`), `3 -> (1,0,0)` (`tau` again: this is the masking `CONE[1] = CONE[3]`).
Composition (`g_1` then `g_2`) is `(alpha_1 + alpha_2, beta_1 + beta_2, gamma_1 +
gamma_2 + alpha_1 beta_2)`; the group is `D8`, the centre is `z = (0,0,1)`
(cell `x -> x XOR 1`). `CONE[x][y]` equals the letter of `x` applied to `y` for
all 16 pairs (`ones_separation.log` line 2). This is the `(H, E)` transducer of
`RESULTS-PSI-ANCESTRY-LAW.md` section 4, re-derived here rather than copied.

The triangle `U`. For a suffix `v = v_1 .. v_q` put

```text
U(-1, e) = 1 + (e mod 2)                          e >= 0
U(j, -j-1) = v_{j+1},   U(j, -j) = v_{j+1} XOR 3   0 <= j < q
U(j, e+1) = CONE[U(j-1, e)][U(j, e)]              e >= -j
```

The tower `(U(0,e), ..., U(q-1,e))` at position `e` determines the tower at
`e+1` given `e mod 2`, and every step is a permutation of the fibre, so the
tower is purely periodic from `e = 0`. `f_v(m) = [1^m v in L_1(c)]` is the
membership function, `v_2(n)` the 2-adic valuation, and a suffix is
"anti-periodic at `A`" if `f_c(m + A) = 1 - f_c(m)` for all `m >= 0` and both `c`.

## 2. Result

### 2.1 Closed form on `sym^m`, with proof

For `sym in {1, 2}` and `m >= 1`, after `sym^m`:

```text
T[m-1][d] = sym            if m + d is even
          = sym XOR 3      if m + d is odd,        -m <= d <= m-1,
```

i.e. `column[i] = sym` iff `m - i` is even (`i = 0..m`) and `diagonal[k] = sym`
iff `m + k` is even (`k = 0..m-1`). Both halves alternate, the phase is the
parity of `m`, and nothing else about `m` is stored.

Proof by induction on `m`. Base: `T[0][-1] = sym`, `T[0][0] = BOUNDARY[sym] =
sym XOR 3` (log lines 1, 5). Step: `T[m][-m-1] = sym` and `T[m][-m] = sym XOR
3` by construction; for `-m <= d < m` the recurrence reads `T[m-1][d]`, which by
the hypothesis is `sym XOR 3` when `m + d + 1` is even and `sym` when it is odd,
so the two entries

```text
CONE[sym XOR 3][sym] = sym XOR 3      (T[m][d] = sym,       m + d + 1 even)
CONE[sym][sym XOR 3] = sym            (T[m][d] = sym XOR 3, m + d + 1 odd)
```

carry the alternation to `d + 1`. Those entries are `CONE[2][1] = 2`,
`CONE[1][2] = 1` (lines 2, 3, 6, 7): the two-letter transducer reading `(sym,
sym XOR 3)` from state `sym XOR 3` emits `(sym, sym XOR 3)` and returns to
`sym XOR 3` (lines 4, 8). The virtual left parent `3` of column 0 never enters
because the stored range is `d <= u`. The kill's first clause ("the transducer
state does not return over a period") did not fire. Cell-by-cell agreement with
`Endpoint` for `m <= 200`, both symbols: lines 9, 10.

Corollary. The last column of `sym^m s` reads `m` periods of `(sym, sym XOR 3)`
from the state `s XOR 3`, so `cut(sym^m s) = P_sym^m(s XOR 3)` with `P_1 =
CONE[2] o CONE[1] = (0 1)(2)(3)` and `P_2 = CONE[1] o CONE[2] = (0)(1)(2 3)`
(lines 11, 12). Hence `cut(1^m 1) = 2` (inadmissible after a `1`), `cut(1^m 0)
= 3` (not binary), `cut(1^m 2) in {0, 1}`: `1^m` is in neither language;
`cut(2^m 1) = 2` for even `m` and `3` for odd `m` with `2` admissible after `2`:
`2^m in L_1(2)` iff `m` even, `in L_1(3)` iff `m` odd. Verified for all `s` and
`m <= 200` (lines 13, 14). This is the period 1 and 2 of the prefix
memberships recorded in `RESULTS-SOURCE-RESIDUALS.md`, now derived.

### 2.2 Reduction: the suffix reads a position in an `m`-independent column

Lemma. After `1^m v`, `T[m+j][d] = U(j, d + m)` for `0 <= j < q` and
`-(m+j)-1 <= d <= m+j`. The cut of `1^m v s` is `U(q, 2m + q)` where column `q`
is built from the symbol `s`.

Proof. Induction on `j`. Column `m + j` of the Endpoint has boundary
`(v_{j+1}, v_{j+1} XOR 3)` at `d = -(m+j)-1, -(m+j)` and reads column `m+j-1`
over `-(m+j) <= d < m+j`; for `j = 0` that column is `T[m-1][d] = 1 + ((m + d)
mod 2) = U(-1, d + m)` by 2.1 (`d + m in [0, 2m-1]`), for `j >= 1` it is
`U(j-1, d + m)` by the hypothesis (`d + m >= -j`, inside the domain of
`U(j-1, .)`). The two recurrences coincide under `e = d + m`. The cut is
`T[m+q][m+q] = U(q, 2m + q)`. Triangle memberships equal oracle memberships on
all 6048 `(m, v, c)` with `m <= 24`, `|v| <= 6` (line 3).

So the Endpoint state after `1^m v` is the window `[-q, 2m + q)` of column
`q - 1` of `U`, and the only `m`-dependence is the window's right end. The
cell the probe reads is `U(q, 2m + q)`: a periodic column sampled at a
position that advances by two per unit of `m`. The measured horizon-`q` class
counts `1, 4, 16, 32, ..., 1024` (`drive_classes_1100.log` lines 1, 2) are the
periods of these columns.

### 2.3 Membership as a function of the letter product; the separation criterion

Column `q` starts at `U(q, -q) = s XOR 3` and reads column `q-1` over `[-q,
2m+q)`, so `U(q, 2m+q) = Pi_m (s XOR 3)` with `Pi_m` the product (in `D8`) of
the letters of column `q-1` over that window. `Pi_m` is a bijection of the four
cells, so exactly one `s` gives cut `c`: `s_c(m) = Pi_m^{-1}(c) XOR 3`. In
coordinates `XOR 3` is `(h, F) -> (h + 1, F)`, `c = 2` is `(1, 0)`, `c = 3` is
`(1, 1)`; the admissible symbols are `{1, 2} = {F = 0}` after a final `2` and
`{2} = {(1, 0)}` after a final `1`. Therefore

```text
v ending in 2:   f_c(m) = [F(Pi_m^{-1}(c)) = 0]
v ending in 1:   f_c(m) = [Pi_m(1) = c]           (cell 1 = (0,0))
```

Complement. `Pi_m^{-1}` is affine with linear part `(h, F) -> (h, F + beta h)`,
which fixes `(0, 1)`, so `Pi_m^{-1}(1,1) = Pi_m^{-1}(1,0) + (0,1)` and
`f_3 = 1 - f_2` for every `v` ending in `2` (line 4: all such `v` of length
`<= 7`, `m < 128`). One suffix separates for both `c` at once.

Criterion. For `m < m'`, `Pi_{m'} = D Pi_m` with `D` the product of the
`2(m' - m)` letters of column `q-1` over `[2m + q, 2m' + q)`. Writing `Pi_m =
(alpha, beta, gamma)` and `D^{-1}(1,0) = (h', F')`, one has `F(Pi_m^{-1}(h,F))
= F + beta (h + alpha) + gamma`, so for `v` ending in `2`

```text
f(m') != f(m)   iff   F' + beta(Pi_m) (h' + 1) = 1 .
```

In particular the stretch separates whenever `D(3) = 2` (the two letters
`(2, x)` with `x != 0` do this for `m' = m + 1`), never when `D(2) = 2`, and
in the remaining cases `h' = 0` exactly when `beta(Pi_m) = F' + 1`, i.e.
`beta = 1` for `D(1) = 2` and `beta = 0` for `D(0) = 2`. This is the sense in
which the position of the window is observable: what separates two lengths
is the content of column `q-1` between the two cut positions, and that
content is a fixed periodic word read at `2m + q`.

### 2.4 Certificates and the anti-periodic family

Certificate for one suffix `v` ending in `2` and one level `a`:

1. Tower recurrence: the least even `P` with `tower(P) = tower(0)` over
   columns `0..q-1`. Then `U(j, e + P) = U(j, e)` for all `e >= 0`, `j < q`.
2. `Phi` = product of column `q-1`'s letters over `[0, P)`. The two-letter
   blocks `R_i` at `(2i + q, 2i + q + 1)` have period `P/2` in `i >= 0`, `Pi_m
   = R_{m-1} ... R_0 Pi_0`, and `Pi_{m + P/2} = Phi_m Pi_m` with `Phi_m` a
   cyclic rotation of `Phi`, hence conjugate to it. So `L = (P/2) ord(Phi)` is
   a period of `Pi_m` and of `f_c`.
3. Exhaustive check `f_c(m + 2^a) != f_c(m)` for all `m < L` and both `c`,
   which by 2 holds for all `m >= 0`.

A disconfirming run at step 3 is one `m < L` with equal memberships; that is
what the naive family shows at its failing levels. Certified suffixes
(`ones_separation.log` lines 67 to 94; candidates were `2 1^n 2`, `2 1^i 2 1^j
2`, `2 1^i 2 2 1^j 2` with `n = a - 2`, widened to `2 1^i 2 1^j 2 1^k 2` when
none certifies, first certified taken; `|A[a]| = a`):

| `a` | `A[a]` | column period `P` | `Phi` | `L` | `2 1^(a-2) 2` | log |
|---|---|---|---|---|---|---|
| 4 | `2112` | 32 | `z` | 32 | same | 67, 68 |
| 5 | `21112` | 64 | `(1,0,0)` | 64 | same | 69, 70 |
| 6 | `212112` | 128 | `(1,0,0)` | 128 | fails (`Phi = id`, `L = 64`) | 71, 72 |
| 7 | `2111112` | 256 | `(1,0,1)` | 256 | same | 73, 74 |
| 8 | `21111112` | 512 | `z` | 512 | same | 75, 76 |
| 9 | `211111112` | 1024 | `z` | 1024 | same | 77, 78 |
| 10 | `2211111112` | 2048 | `(1,0,0)` | 2048 | fails (`Phi = id`) | 79, 80 |
| 11 | `21111121112` | 4096 | `(1,0,1)` | 4096 | fails (`P = 2048`) | 81, 82 |
| 12 | `221111111112` | 8192 | `(1,0,0)` | 8192 | fails | 83, 84 |
| 13 | `2111112111112` | 8192 | `(1,1,0)` | 16384 | fails (`Phi = id`) | 85, 86 |
| 14 | `21211111111112` | 16384 | `(1,1,0)` | 32768 | fails | 87, 88 |
| 15 | `211121111111112` | 65536 | `z` | 65536 | fails | 89, 90 |
| 16 | `2111211111111112` | 131072 | `z` | 131072 | fails (`Phi = id`) | 91, 92 |
| 17 | `22111111211111112` | 262144 | `(1,0,0)` | 262144 | fails (`P = 65536`) | 93, 94 |

The mechanism is not one mechanism: `Phi = z` gives anti-period `P/2`
directly (central, all rotations equal); `ord(Phi) = 4` gives `Phi_m^2 = z`
and anti-period `P`; the non-central involutions `(1,0,0)` and `(1,0,1)` give
anti-periodicity only through the correlation between the rotation `Phi_m` and
`beta(Pi_m)` of 2.3, which the exhaustive check certifies but no argument
explains. At level 17 none of the 30 candidates with at most two inner `2`s certifies; the search
widened to the 105 words `2 1^i 2 1^j 2 1^k 2`, of which 6 certify (line 93).

### 2.5 The table for `a <= 3`

Every suffix of length `<= 3` has membership period `L` dividing 16 (lines 5
to 32: `L in {2, 4, 16}`), so `f_v(m)` depends on `m mod 16`. The covering sets
`C_2 = (21, 22, 121, 122, 211, 222)` and `C_3 = (21, 22, 121, 122, 212, 222)`
give 16 distinct 6-bit signatures for `c = 2` and `c = 3` (lines 33 to 66; no
set of five suffices, the search is exhaustive over the 14 suffixes). For `a
<= 3` the residues of `m` and `m'` mod 16 differ, and `v(m, m', c)` is the first
suffix of `C_c` whose bit differs between the two signatures.

### 2.6 The rule and its verification

```text
v(m, m', c):   a = v_2(m' - m);   a <= 3: table 2.5;   4 <= a <= 17: A[a].
```

On all `1 <= m < m' <= 64` and both `c` (4032 triples) the rule separates
under the `Endpoint` oracle of `oracle_1m.py`, never through the triangle, with
`|v| <= 5`; usage `21:1536, 22:1280, 121:448, 122:384, 211:64, 212:64,
222:64, 2112:128, 21112:64` (lines 95, 96). A disconfirming run is a triple
with `1^m v` and `1^{m'} v` both in or both out of `L_1(c)`.

### 2.7 What is proved

Theorem (finite bound, all `m`). For `c in {2, 3}` and all `m != m'` with `m
!= m' (mod 2^18)`, the prefixes `1^m` and `1^{m'}` are Nerode-inequivalent for
`L_1(c)`. Every DFA for `L_1(c)` has at least `2^18 = 262144` states.

Proof. `a = v_2(m' - m) <= 17`. If `a <= 3`, 2.5. If `4 <= a <= 17`, `m' = m
+ 2^a (2t + 1)` and `A[a]` is anti-periodic at `2^a` for all `m`, so `f(m') =
1 - f(m)` after an odd number of flips. The `2^18` prefixes `1^0 .. 1^(2^18 -
1)` are pairwise separated.

This supersedes the finite bound 1100 of `RESULTS-SOURCE-RESIDUALS.md`
(`drive_classes_1100.log` lines 1, 2), which was a count of signatures among
`m <= 1100`; the statement here holds for every `m`.

### 2.8 The gap, exactly

Claim not proved: `L_1(c)` is not regular. Along `1^m` this is equivalent to
the membership periods `L_v` being unbounded over suffixes `v`: if `L_1(c)`
were regular the DFA state after `1^m` would be eventually periodic in `m` with
some period `p`, every `f_v` is purely periodic (2.4 step 2), and a purely
periodic sequence that is eventually `p`-periodic has minimal period dividing
`p`; conversely unbounded `L_v` (each `L_v` is a power of two, being a tower
period times `1, 2, 4`) gives infinitely many Nerode classes among the `1^m`,
since finitely many classes would make `m -> class(1^m)` eventually periodic
and bound every `L_v`. So the missing statement is:

    (G) for every `a` there is a suffix `v` with `f_v` not `2^a`-periodic.

Two sub-steps are open.

(G1) Tower period unbounded along some suffix family. Lemma `[U]`: along
`2 1^infinity`, the tower period is bounded iff some column `U(j, .)`, `j >=
1`, is ground on `e >= 0` (ground = the closed form `1` if `e + j + 1` even
else `2`). Proof: column `j` is ground on the light cone `[-j-1, j-2]` (the
closed form is a fixed point of the recurrence and column `j` reads column
`j-1` one position behind; lines 97 to 107 verify this and that every column
`j <= 10` is non-ground beyond it), so if all columns had period dividing `2Q`
then column `j >= 2Q + 1` would be ground on a full period, hence everywhere;
conversely a ground column feeds a ground column above it. Local form: column
`j+1` is ground iff column `j` has no cell `0` and no cell `2` at positions `e
= j + 1 (mod 2)`, because `CONE[x][1] = 2` iff `x != 0` and `CONE[x][2] = 1`
iff `x in {1, 3}`. No invariant is known that forbids this configuration; the
per-period counts of `0`-cells `1, 1, 8, 6, 15, 30, 57, 112, 246, 522, 532`
(lines 97 to 107) are positive but follow no rule.

(G2) Observability. Even with (G1), the probe sees the column below only
through its letters, and cells `1` and `3` emit the same letter `tau`
(masking); the tower can differ at two positions without the difference
reaching the cut. The certificates say it always does through level 17, and
no argument says why.

Witness `[K]` that no uniform mechanism exists: the one-period maps along
`2 1^k`, `k = 0..10`, are `(1,0,1), (1,1,0), id, z, (1,0,1), z, (1,0,0), z, z,
id, (0,1,0)` with column periods `4, 8, 32, 32, 64, 128, 256, 512, 1024, 2048,
2048` (line 108): identities at `k = 2` and `k = 9` stall the tower, the
orders run `2, 4, 1, 2, 2, 2, 2, 2, 2, 1, 2`, and no period or self-similarity
is visible. The anti-periodic suffix at each level had to be found by search,
the two-`2` families give nothing at level 17, and the three-`2` family that
does (6 of 105) has no more structure than the ones before it. An induction on
`a` would need an
invariant carried by the column of `A[a]` that determines `(P, Phi)` of the
column of `A[a+1]`; the data above shows there is no such invariant of bounded
size within the families tried. Of the killed mechanism classes in
`PROOF-STATE-CAPSULE.md` section 5, none was renamed or retried: the
certificates here are exhaustive checks at fixed `a`, not bounded quotients,
linearisations or rank counts.

## 3. Reading

The closed form on `1^m` is as simple as a closed form can be: an alternating
column with its phase, period 2, no preperiod. That is exactly why `1^m` is a
good probe of the wide language: the whole content of `m` is the length of an
alternating window, and the suffix reads it as a position in a periodic column
whose period doubles per suffix symbol. The doubling is certified level by
level for all `m` up to anti-period `2^17`, but it is not one mechanism: the
one-period map of the top column takes every conjugacy class of `D8` as the
suffix grows, including the identity, which stalls the tower and is why
`2 1^(a-2) 2` fails at `a = 6, 10, 11, ...`. A proof of non-regularity through
`1^m` needs either an invariant that keeps the tower period growing (G1 in its
local form: no column of `2 1^infinity` is ever free of `0`-cells and of
`2`-cells at the wrong parity) together with an observability argument through
the `CONE[1] = CONE[3]` masking (G2), or a different prefix family with a
uniform column structure. The alternating family of
`RESULTS-ALTERNATING-FAMILY.md` has period 28 on `(12)^k` and is the natural
next candidate, since its columns are computed there and any defect family is
the same kind of tower.

Nothing here bears on P1: the pre-registration classes this as a no-go
theorem for finite-state certificates of the run language, and the outcome is
that the no-go theorem is proved only at the finite bound `2^18`, with the
obstruction to the infinite bound named exactly.

## 4. Scope

- Closed form: all `m >= 1` (proof), checked `m <= 200`. Corollary: all
  `m >= 1` (proof), checked `m <= 200`.
- Reduction lemma: all `m`, `v` (proof); checked `m <= 24`, `|v| <= 6`.
- Complement `f_3 = 1 - f_2`: all `v` ending in `2` (proof); checked `|v| <= 7`,
  `m < 128`.
- Certificates `A[4..17]`: all `m >= 0`, both `c` (finite proof per level).
  Table mod 16: all `m` (finite proof).
- Separation of all pairs `m != m' (mod 2^18)`: all `m` (theorem 2.7).
  Separation of all pairs `m < m' <= 64`: also checked by the oracle.
- Not proved: non-regularity; separation of any pair with `m = m' (mod 2^18)`.
- `2^m`: closed form and membership only. Its Nerode classes were not
  pursued; `2^m` is realizable only to length 4 (`00000` forbidden), so it is
  a control on the closed form, not a probe.
- Candidate families for `A[a]` were `2 1^n 2`, `2 1^i 2 1^j 2`, `2 1^i 2 2 1^j
  2` (and three-inner-`2` words at level 17). The anti-periodic suffixes
  listed in the abstract are the first certified in that order, not the only
  ones (at `a = 7`, 7 of 10 candidates certify; at `a = 16`, 1 of 28).
- Runtime: `ones_closed_form.py` under one second; `ones_separation.py 64 17`
  209 s, of which level 17 is 177 s (log lines 93, 109).

## 5. Reproduction

From `experiments/rule30/p1-period2-invariant`:

```text
uv run --no-project python nonregularity/ones_closed_form.py 200
uv run --no-project python nonregularity/ones_separation.py 64 17
```

Both exit 0 iff every check passes. `ones_separation.py MMAX AMAX` verifies
all pairs `m < m' <= MMAX` and certifies levels `4..AMAX`; `AMAX = 13` runs
in about two seconds. Logs: `nonregularity/ones_closed_form.log`,
`nonregularity/ones_separation.log`.

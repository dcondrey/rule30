# The single-flip dependency law: (P1) and (P2) are exact and uniform, and the pre-registered kill fires at n = 4, so no step-by-step fresh-token mechanism exists

Date: 2026-09-16. Pre-registration `PREREGISTRATION-DEPENDENCY-LAW.md` (written before the
run). Scripts and logs in `charge-injection/dependency-law/`: `propagation_law.py`
(`propagation_law_n1-10.log`), `dependency_laws.py` (`dependency_laws_n1-14.log`,
`dependency_laws_n18.log`, `dependency_laws_tight_n17.log`), `tight_word_he.py`
(`tight_word_he.log`). Kernel `psi_kernel.py`, forced run `seam_history_inheritance.run`
(wide grammar, `maxrows n + 4`). `cut()`, `deps()` and `max_matching()` are the probe's
functions (`charge-injection/injection_probe.py`, `greedy_rules.py`), copied verbatim.

**The kill fires, at the first non-trivial scale. `[K]` On `W = 1212`, `c = 2` (`n = 4`, run 2,
forced `22`) the single-flip dependency sets are `D_0 = {1, 2, 3}` and `D_1 = {1, 3}`, the
maximum matching of steps into `2`-positions saturates (2 = run), and step 1 has no
`2`-position outside `D_0`: (L-fresh) fails on a word whose matching saturates
(`dependency_laws_n1-14.log` line 98; at `c = 3` the witness is `2121`, line 102). It is not a
small-`n` accident: (L-fresh) fails on 77 of the 371 `c = 2` words with a run at `n = 14`
and on 458 of 2819 at `n = 18`, all of them saturating; (L-nested) on 47 and 216 (lines 28,
`dependency_laws_n18.log` line 2). So the injection of run steps into `2`-tokens that
inequality (12) needs exists only globally, by Hall, and no argument of the shape "forced
step `j` reads a `2` that steps `0 .. j-1` did not need" exists. On the tight word
`12212121212121212` the maximum matching is 8 for 10 steps `[C]` (previously bounded only by
the greedy `-3`): the flip of `e_1`, the first `2` of the `22` factor, perturbs no cell of
any column from 17 on, and the flip of `e_0` none from column 3 on (`tight_word_he.log`
lines 32 to 33), so two of the ten steps depend on no `2` that is not already charged, and
steps 2 to 9 all read only `2`s that steps 0 and 1 already read (`dependency_laws_tight_n17.log`
lines 2 to 11). (L-order) `[C]`: of six fixed orders, only "steps by ascending
`|D_j cap 2-positions|`, oldest unused `2` within a step" reaches the maximum matching on
every word tested (`n <= 14`, `n = 18`, and 8 on the tight word); each of the other five
falls below the maximum on a named word, the oldest-unused rule on exactly two words at
`n = 18`. That order needs every `D_j` before it charges the first step, so it is a global
choice and does not rescue (Q). Part 1 is positive and uniform. (P1) `[U]`: flipping `e_i`
flips `H_i(d)` at every depth and flips `E_i(d)` iff `beta_i(d)` is odd, hence column `i`'s
letter `b` flips exactly where `beta_i` is even and `a = (1-H) E` becomes `H (E + beta)`; the
state perturbation is the shear `S^beta` applied to `(1, 0)`. (P2) `[U]`: at every later
column the `H` channel is `F2`-linear in the previous column's `a`-perturbation, the `F`
channel is bilinear with explicit coefficients, the pair (unperturbed, perturbed) runs a
fixed 16-state product transducer, perturbations vanish above the light cone
`d < u - 2i - 1`, and a perturbation changes between zero and nonzero only at a perturbed
input letter, because each letter acts as a bijection on the four states. All eleven
identities hold on 3,579 endpoint sequences `W` and `W Q_c(W)`, every binary `W` with
`n <= 10`, both `c`, up to 2.4 million cells per identity
(`propagation_law_n1-10.log` lines 11 to 12). `RW`, `(SEP)`, `(PT2)` untouched.**

## 1. Objects

Triangle `T[u][d]` read off `psi_kernel.Endpoint`: after appending `e_0 .. e_u`,
`column[k] = T[u][-k]` for `k = 0 .. u+1` and `diagonal[k] = T[u][k]` for `k = 0 .. u`, so
column `u` lives on depths `[-u-1, u]` with `T[u][-u-1] = e_u`, `T[u][-u] = e_u XOR 3`,
`T[u][d+1] = CONE[T[u-1][d]][T[u][d]]` (`propagation_law.triangle` asserts all three against
`CONE` and `BOUNDARY` on every sequence it builds). `(H, Lo) = (x >> 1, x & 1)`,
`E = 1 + H + Lo`; the quotient of a cell is `(a, b) = ([x == 0], [Lo(x) == 0]) =
((1-H) E, H XOR E)`. Column `u` is the Moore machine with state `(h, F) = (H_u(d), E_u(d))`,
input the quotient of column `u-1` at the same depth, step `h' = h + 1 + a`,
`F' = F + h b`, initial `(1 - H(e_u), 0)` at `d = -u`
(taken from `RESULTS-PSI-ANCESTRY-LAW.md` section 4, where it is verified on all 16
argument pairs; re-verified by the referee's `crosscheck/verify-0916/dependency/check_moore.py`;
not re-derived in this document).
`beta_i(d) = #{d' in [-i, d) : Lo(T[i-1][d']) = 0}`, with `beta_i(-i-1) := 0` and
`beta_0 := 0`. A single flip is `e_i -> 3 - e_i`; `d` prefixed to a quantity is its change
mod 2 under the flip.

`cut_j(W') = Endpoint(W' Q[:j]).peek(Q[j])[1][n] = T[n+j][n]` of the sequence `W' Q[:j+1]`;
`D_j(W) = {i < n : cut_j(W with W_i flipped) != c}` with the forced prefix `Q` of `W` held
fixed. The matching is between steps `0 .. run-1` and `{i in D_j : W_i = 2}`. The three
laws are as pre-registered: (L-fresh) every step `j` has a `2`-position in `D_j` outside
`D_0 u .. u D_(j-1)`; (L-nested) for `j >= 1`, `D_j cap 2pos` is not a subset of
`D_(j-1) cap 2pos`; (L-order) a fixed order saturates whenever the maximum matching does.
Orders: steps forward, reverse, or by ascending `|D_j cap 2pos|` (ties by `j`), and within a
step the oldest (smallest index) or newest unused `2`. Kill: (L-fresh) fails on a word whose
maximum matching saturates.

## 2. Result

### 2.1 (P1), first-column propagation `[U]`

Let the flip be at `e_i`. Columns `u < i` are unchanged (triangularity; check `P0`). Both
binary symbols have `E = 0`, so the flip changes the initial state of column `i` from
`(h_0, 0)` to `(h_0 + 1, 0)` and leaves the input word of column `i` (the quotient of column
`i-1`) unchanged. Each letter `(a, b)` acts on `Z_2^2` affinely: `(h, F) -> (h + 1 + a,
F + b h)`, whose linear part is the shear `S_b : (h, F) -> (h, F + b h)`. Shears commute and
square to the identity, so the linear part of the word read on `[-i, d)` is `S^beta_i(d)`,
and the difference of the two trajectories at depth `d` is `S^beta (1, 0) = (1, beta_i(d)
mod 2)`. Hence

```text
(P1.H)  dH_i(d) = 1                       for every d in [-i-1, i]
(P1.E)  dE_i(d) = beta_i(d) mod 2
(P1.b)  db_i(d) = 1 + beta_i(d) mod 2      (b = h + F flips where beta is even)
(P1.a)  a_i'(d) = H_i(d) (E_i(d) + beta_i(d)),  i.e.  da_i(d) = E_i(d) + H_i(d) beta_i(d)
```

Checked on every cell of column `i` for every flip position `i` of every sequence: 386,346
cells per identity, zero failures (`propagation_law_n1-10.log` line 11).

### 2.2 (P2), propagation into columns `i+1 .. n+j`: what is uniform `[U]`

For `u > i` the initial state of column `u` is unchanged, and `h_u(d) = h_u(-u) + (d + u) +
sum_{d' in [-u, d)} a_{u-1}(d')` is affine in the input `a`-letters. So

```text
(P2.H)   dH_{i+1}(d) = #{d' in [-(i+1), d) : da_i(d') = 1} mod 2,   dH_{i+1}(-(i+2)) = 0
(P2.Hc)  dH_{i+1}(d) = sum_{d' in [-i, d)} (E_i(d') + H_i(d') beta_i(d'))  mod 2
(P2.Hu)  dH_u(d)     = #{d' in [-u, d) : da_{u-1}(d') = 1} mod 2     for every u > i
```

(the `d' = -(i+1)` term of (P2.H) is the source cell `e_i`, whose `a = [e_i == 0] = 0` on
both sides, so (P2.Hc) drops it). The `F` channel is exact but bilinear: from
`F' = F + h b`,

```text
(P2.E)   dE_{i+1}(d+1) = dE_{i+1}(d) + H_{i+1}(d) db_i(d) + dH_{i+1}(d) b_i(d) + dH_{i+1}(d) db_i(d)
                       with db_i(d) = 1 + beta_i(d),  dE_{i+1}(-(i+2)) = dE_{i+1}(-(i+1)) = 0
```

and the emitted letters of the perturbed column, from `a = (1 - h) F`, `b = h + F`:

```text
(P2.prod)  da = (1 + h) dF + dh (F + dF),   db = dh + dF,
           dh' = dh + da_{u-1},   dF' = dF + h db + dh b + dh db
```

so the pair (unperturbed column, perturbed column) at every `u > i` is one run of a fixed
16-state transducer on state `(h, F, dh, dF)`, uniform in `n`, `u`, `i`. Two structural
consequences: (P2.cone) `(dh, dF)(u, d) = 0` for `d < u - 2i - 1`, since `(u, d)` depends
only on cells `(u', d')` with `d' - u' <= d - u` and the source cell has `d' - u' = -2i - 1`;
and (P2.ext) the perturbation of column `u` changes between zero and nonzero from depth `d`
to `d+1` only if `(da, db)(u-1, d) != 0`, because for a fixed letter the step is a bijection
of the four states (an element of `D8`), so equal inputs send unequal states to unequal
states and equal states to equal states. A perturbation is therefore extinguished only by
another perturbation arriving from the left, and re-lit only the same way.

Checks (`propagation_law_n1-10.log` line 11): `P2.H` and `P2.E` 379,188 cells, `P2.Hc`
347,871, `P2.Hu` and `P2.cone` 2,401,548, `P2.prod` and `P2.ext` 2,084,994 cell-steps, zero
failures, over all 3,579 sequences `W` and `W Q_2(W)`, `W Q_3(W)` with `|W| <= 10` (line 12
`ALL PASS`). The script tests (P2.ext) in its cell form (the input cell differs), which is
weaker than the letter form stated above (cells `1` and `3` give the same letter); the
letter form follows from (P2.prod) and the per-letter bijection and is tested directly in
`crosscheck/verify-0916/dependency/check_p1p2_n11.log`, `check_p1p2_n12.log` (zero failures). A disconfirming run would have printed the first `(check, S, i, d)` with both
columns.

What is not uniform, and cannot be made so by this route: (P2.E) needs the unperturbed
profiles `H_{i+1}(d)` and `b_i(d)`, and through (P2.prod) the coefficient `(1 + h)` feeds the
`F` perturbation back into the `a` channel, so from column `i+2` on both channels depend on
the whole unperturbed column, which is the growing input word of section 5 of
`RESULTS-PSI-ANCESTRY-LAW.md` and the F2-linearisation row of the capsule's kill list. The
membership `i in D_j` is `(dh, dF)(n+j, n) != 0`, a bit of that iterated product transducer,
and no bounded-window statement about it is claimed.

### 2.3 (L-fresh), (L-nested), the matching, `n <= 14` `[K]` / `[C]`

`dependency_laws_n1-14.log` lines 2 to 29, every hard-core `W` with `run >= 1`, both `c`.
"Kill" counts words on which (L-fresh) fails and the matching saturates.

| `n` | `c = 2` words | sat | fresh fails | kill | nested fails | `c = 3` words | sat | fresh fails | kill | nested fails |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 1 | 1 | 0 | 0 | 0 | 4 | 2 | 2 | 0 | 2 |
| 4 | 5 | 5 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 |
| 5 | 2 | 2 | 0 | 0 | 0 | 6 | 6 | 2 | 2 | 2 |
| 6 | 9 | 9 | 1 | 1 | 1 | 10 | 10 | 0 | 0 | 0 |
| 7 | 14 | 13 | 5 | 4 | 5 | 19 | 17 | 11 | 9 | 10 |
| 8 | 18 | 18 | 12 | 12 | 10 | 21 | 19 | 5 | 3 | 1 |
| 9 | 24 | 24 | 0 | 0 | 0 | 41 | 36 | 11 | 6 | 11 |
| 10 | 47 | 47 | 8 | 8 | 8 | 64 | 62 | 13 | 11 | 13 |
| 11 | 98 | 98 | 12 | 12 | 9 | 98 | 98 | 29 | 29 | 19 |
| 12 | 140 | 140 | 36 | 36 | 12 | 137 | 137 | 25 | 25 | 22 |
| 13 | 209 | 209 | 36 | 36 | 24 | 269 | 269 | 42 | 42 | 21 |
| 14 | 371 | 371 | 77 | 77 | 47 | 380 | 380 | 84 | 84 | 57 |
| 18 | 2819 | 2819 | 458 | 458 | 216 | 2625 | 2625 | 327 | 327 | 168 |

First witnesses, in enumeration order (`n` ascending, then lexicographic with `1 < 2`):

- Kill, `c = 2` (line 98): `W = 1212`, run 2, forced `22`, `D_0 = {1, 2, 3}` (`2`-positions
  `{1, 3}`), `D_1 = {1, 3}` (`2`-positions `{1, 3}`), matching 2. Step 1 reads exactly the two
  `2`s step 0 read.
- Kill, `c = 3` (line 102): `W = 2121`, run 2, forced `22`, `D_0 = D_1 = {0, 1, 2, 3}`,
  matching 2.
- (L-nested) fails first on the same `1212` at `c = 2` (line 106) and on `121` at `c = 3`
  (line 110: `n = 3`, run 4, forced `2122`, `D_j = {1, 2}` for all four steps, matching 1,
  which is the known `c = 3` slack and also the first non-saturating word, line 172).
- The matching at `c = 2` saturates on every word `n <= 14` except one: `2222121` at `n = 7`,
  run 4, forced `2221`, matching 3 (line 166), inside the `[22 in W]` term of (12); the probe's
  table started at `n = 8` and did not see it. At `c = 3` it is short at `n = 3, 7, 8, 9, 10`
  and saturates at `n = 11 .. 14` (column `sat`), as the probe reported.
- At `n = 18` (`dependency_laws_n18.log` lines 2 to 3) the matching saturates on every word,
  both `c`. This was "not computed" in `RESULTS-CHARGE-INJECTION-PROBE.md`; it is now `[C]`.
  First kill witness there: `121212121212121221`, `c = 2`, run 8, nine `2`s, matching 8,
  (L-fresh) failing at step 2 (line 68).

### 2.4 The tight word at `n = 17` `[C]`

`dependency_laws_tight_n17.log` line 1: `W = 12212121212121212`, `c = 2`, run 10, forced
`2122122121`, nine `2`s, maximum matching 8, short by 2. (L-fresh) and (L-nested) both fail
first at step 2. The `D_j` (lines 2 to 11) agree with `greedy_rules_n8-18.log` lines 2 to 11
and with the independent full-triangle computation of `tight_word_he.py` (matrix, lines 3
to 20 of its log). Greedy minus run: forward/oldest and forward/newest `-3`, the other four
orders `-2`, which is the maximum. At `c = 3` the run is 0 (line 12).

Why 8: `tight_word_he.log` lines 32 to 33. The flip of `e_0` (the leading `1`) perturbs no
cell of any column `u >= 3`; the flip of `e_1` (the first `2` of `22`) perturbs no cell of any
column `u >= 17`, the column of the first forced symbol. By (P2.ext) both perturbations were
cancelled by their own downstream images and cannot return. So eight `2`s are reachable by
ten steps, and steps 2 to 9 read only `2`s inside `D_0 u D_1 = {2, 4, 6, 8, 10, 12, 14, 16}`
(lines 2 to 11 of the `n17` log: every `fresh` list from step 2 on is empty).

### 2.5 (L-order) `[C]`

Per-order first word on which the order falls below the maximum matching
(`dependency_laws_n1-14.log` lines 30 to 79, `dependency_laws_n18.log` lines 4 to 43):

| order | first word below the maximum, `n <= 14` | at `n = 18` |
|---|---|---|
| forward, oldest (the probe's rule) | `12212`, `c = 3`, `n = 5` (line 42) | `122121212122121212` and `222121212122121212`, `c = 2`, run 6, forced `212222`, matching 6: the only two failures (lines 137 to 151) |
| forward, newest | `1222121`, `c = 2`, `n = 7` (line 30) | 12 words at `c = 2`, 4 at `c = 3` (lines 2 to 3) |
| reverse, oldest | `2222`, `c = 2`, `n = 4` (line 58) | 2 words at `c = 3` (line 3) |
| reverse, newest | `2212`, `c = 2`, `n = 4` (line 46) | none (lines 2 to 3) |
| size ascending, newest | `1222121`, `c = 2`, `n = 7` (line 66) | none |
| size ascending, oldest | none (no `below-max` witness; lines 2 to 29 report 0 at every `n`) | none (lines 2 to 3); 8 = maximum on the tight word |

So the pre-registered alternative "by `|D_j|` ascending" with the oldest unused `2` repairs
both `n = 18` failures of the oldest-unused rule and reaches the maximum matching on every
word tested. It is a fixed order in the sense of the pre-registration, and it is not a
mechanism: it sorts the steps by the size of sets that are known only after all `D_j` have
been computed, which is a global (Hall-type) choice, the opposite of a step-by-step law. A
disconfirming run is a word on which `greedy(size, oldest) < matching`; none appeared in
the 1,992 (word, `c`) pairs with a run at `n <= 14` or the 5,444 at `n = 18`.

### 2.6 The `(H, E)` description of the tight word's ten steps

`tight_word_he.py` builds one triangle of `S = W Q` and its seventeen single-flip variants;
`D_j` is the set of `i` whose flip perturbs `(n + j, n)`. The cut perturbation matrix
(`tight_word_he.log` lines 3 to 20; `.` none, `H` only `dh`, `E` only `dF`, `B` both):

```text
        j: 0123456789
  i= 0 (1): ..........
  i= 1 (2): ..........
  i= 2 (2): .BHHB.....
  i= 3 (1): ...BB.....
  i= 4 (2): .HEBEEH...
  i= 5 (1): EHEEHH....
  i= 6 (2): BBEHEEH.E.
  i= 7 (1): EEEEEHBEEH
  i= 8 (2): .BHBBHBEEE
  i= 9 (1): BE.BEEEEE.
  i=10 (2): B..EEEBHEH
  i=11 (1): ...HBBEB.B
  i=12 (2): HHEBE.B.EE
  i=13 (1): EBHHB.BB.B
  i=14 (2): EEBHHEH.HH
  i=15 (1): E.EHEHBBBH
  i=16 (2): .BHEBBH...
```

Per step, the profiles `h_{n+j}(d)`, `F_{n+j}(d)` on `[-(n+j)-1, n]`, the input quotient of
column `n+j-1`, and the perturbation strip of every source flip are at lines 50 to 298 (step
`j` at line `50 + 25 j`). The cut cell is `(h, F) = (1, 0)` at every step (`c = 2`). The
binding step 7 (`u = 24`, `Q[7] = 1`, lines 225 to 248):

```text
  a_23(d), d = -24..17:   000000000010000000000101011110100010000000
  b_23(d):                101010100110001010001101011110101010010101
  h_24(d), d = -25..17:  0101010101011010101010110011111001011010101
  F_24(d):               0011001100001111111111100001010000110001100
  flip i= 6 (2)       :  .....................................BBHB..
  flip i= 7 (1) in D_j:  .....................................BBHHEE
  flip i= 8 (2) in D_j:  ..................................HEEEEEEEE
  flip i= 9 (1) in D_j:  ..................................HHBB.EBHE
  flip i=10 (2) in D_j:  ..............................BBEE..BB.EE.H
  flip i=11 (1) in D_j:  ..............................BB....BBHB.EB
  flip i=12 (2)       :  ............................BHEH.HB.BEEBB..
  flip i=13 (1) in D_j:  ...............................BHE.HEHHEEBB
  flip i=14 (2)       :  .....................EEEH..BHEEEBBHHE......
  flip i=15 (1) in D_j:  .......................BEEBHEEHH..HHEEEEEBB
  flip i=16 (2)       :  ....................H.......BHE.HEBB.......
```

(rows for `i = 0 .. 5` are all `.`). In words, what the steps read:

- Every source flip lives, in column `n + j`, inside the light cone `d >= j + n - 2i - 1`
  (P2.cone), so the top of its window moves down one depth per step and the cut `d = n`
  leaves the cone of position `i` after step `2i + 1`. The early positions drop out earlier
  than that: position 2 is read at steps 1 to 4 (cone allows 5), 3 at steps 3 and 4 (cone 7),
  4 at 1 to 6 (cone 9), 5 at 0 to 5 (cone 11), 6 at 0 to 6 and 8 (cone 13) (lines 34 to 48).
  Each early exit is a cancellation by the image of the same flip one column to the left
  (P2.ext), and position 1 is cancelled completely before column 17 (line 33).
- The late positions are never squeezed out by the cone (`2i + 1 >= 25` for `i >= 12`), so
  their membership is decided at the bottom of the column: at step 7 the flips of 12, 14, 16
  are still present in column 24 on `d <= 15`, `d <= 11`, `d <= 10` respectively but have been
  cancelled on the last depths up to the cut, while at steps 6 and 8 the same flips reach
  the cut again (matrix rows 12, 14, 16). Position 16, the last symbol, is read at steps 1
  to 6 only, even though its cone reaches every step.
- So step 7 reads the middle band of the source: the run `1 2 1 2 1` at positions 7 to 11
  (positions 7, 8, 9 through the `F` channel only, 10 through `h` only, 11 through both) and
  the two `1`s at 13 and 15 (both channels). Its only `2`-dependencies are 8 and 10, both
  already read before it: 8 by steps 1 to 6, 10 by steps 0 and 3 to 6. Steps 8 and 9 read
  only positions inside 6 to 15 and 7 to 15, with the late `2`s 12 and 14 back in, again
  nothing new. The early defect `22`
  at 1, 2 is read only through position 2 at steps 1 to 4 and never through position 1.
- There is no step at which a new `2` becomes readable after step 1: the reachable set is
  fixed at `{2, 4, 6, 8, 10, 12, 14, 16}` by the end of step 1, and the remaining eight steps
  permute their windows over it. That is the obstruction on the tight word, made explicit.

## 3. Reading

The pre-registration named one kill and it fired at `n = 4`, so the verdict on (Q) is the
obstruction, not a mechanism. A proof of inequality (12) by charging each forced step to a
distinct `2` it single-flip-depends on cannot proceed step by step: on `1212` (and on 77 of
371 saturating words at `n = 14`) the later step depends on no `2` the earlier one did not,
and the injection has to be found globally, by Hall, after all dependency sets are known.
Worse for that route, on the sole slack-zero word of (12) at `c = 2` the dependency-respecting
matching is 8 for 10 steps (and on its sibling `22212121212121212`, run 10, ten `2`s, it is 9,
Hall deficiency 1, the only other non-saturating `c = 2` word at `n = 17`;
`crosscheck/verify-0916/dependency/check_laws_n6-17.log`): the `+[22 in W]` token of (12) does not cover the deficit,
because the first `2` of the `22` is forgotten by the triangle before any forced column is
reached, and a second step is also free. Any charging proof of (12) must charge two steps of
the tight word to something they do not single-flip-depend on. This is a new `[C]`
obstruction to the proof shape the probe proposed, sharper than the kill.

Part 1 is the positive residue. (P1) and (P2) put the single-flip perturbation in closed
form as far as it is closed: the `H` channel is linear in the previous column's
`a`-perturbation at every column, the first column's perturbation is the shear power
`S^beta (1, 0)`, and the two structural facts (P2.cone) and (P2.ext) explain the shape of the
strips in section 2.6: windows bounded above by the cone and cut at the bottom by
cancellations. Neither gives a bounded-state description of `i in D_j`; the `F` channel and
its feedback into `a` carry the full unperturbed column, which is the same growing-word
obstruction that (PSI) meets. Nothing here is a renamed retry of a killed mechanism class:
no bounded quotient, no linearisation beyond the `H` channel identity that is exact, no
additive energy.

The (L-order) result is empirical and should be read as such: one greedy order finds a
maximum matching on every word tested. It is a statement about maximum matchings of these
particular bipartite graphs, not a step-by-step law, and it is not used for anything.

## 4. Scope

Finite and single-implementation: (P1), (P2) exhaustive on all binary `W`, `n <= 10`, and
their forced continuations for both `c` (the identities are uniform derivations, the check is
their gate); the laws on all hard-core `W`, `n <= 14` and `n = 18`, both `c`, wide grammar;
the tight word at `n = 17`. `D_j` is single-flip dependency with the forced prefix held
fixed, as in the probe; a joint dependency on `e_1` together with other flips is not
excluded by the silence of the single flip. The maximum matching is exact (augmenting
paths). Nothing about `RW`, `(SEP)` or `(PT2)` is touched. The pre-registration named
`n <= 16`; this document ran `n <= 14` and `n = 18` (and `n = 17` on the tight word only).
The referee's sweep in `crosscheck/verify-0916/dependency/` covers `n = 15, 16, 17, 19`
exhaustively and 300 sampled words at `n = 21`: every word saturates, the size-ascending
order reaches the maximum everywhere, and (L-fresh) fails on 94 (`c = 2`) and 125 (`c = 3`)
of the words with a run at `n = 15`, and on 204 and 160 at `n = 16`
(`check_laws_n6-17.log`).

## 5. Reproduction

From `experiments/rule30/p1-period2-invariant`:

```sh
uv run --no-project python charge-injection/dependency-law/propagation_law.py 10 > charge-injection/dependency-law/propagation_law_n1-10.log      # 7 s
uv run --no-project python charge-injection/dependency-law/dependency_laws.py all 14 > charge-injection/dependency-law/dependency_laws_n1-14.log
uv run --no-project python charge-injection/dependency-law/dependency_laws.py n18 > charge-injection/dependency-law/dependency_laws_n18.log      # add only22 to restrict to words with a 22 factor; not needed
uv run --no-project python charge-injection/dependency-law/dependency_laws.py word 12212121212121212 > charge-injection/dependency-law/dependency_laws_tight_n17.log
uv run --no-project python charge-injection/dependency-law/tight_word_he.py > charge-injection/dependency-law/tight_word_he.log
```

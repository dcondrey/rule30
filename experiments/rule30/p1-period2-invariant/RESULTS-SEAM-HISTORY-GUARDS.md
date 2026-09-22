# Finite history cannot supply the guarded seam

Date: 2026-09-15.

**Two uniform lemmas, run inheritance `(L1)` and seam-equals-inheritance
`(L2)`, make every finite-history version of `(SEAM)` either refuted by an
explicit orphan at run `D_n(c)` or vacuous, so the next step at
`RESULTS-RW-GUARDED-SEAM-DESCENT.md:134-137`, "prove (SEAM) using stronger
history information", collapses to `RW` itself: the only guard that works is the
full constant cut, `RW`'s own hypothesis. A uniform-in-`n` guard at any level
`m` is equivalent to `sup_n D_n(c) < m`, strictly stronger than `RW` (section
5). `RW`, `(RW-alpha)`, `SEP` and `PT2` remain open, the live obligation
unchanged.** Scripts: `seam_history_inheritance.py`,
`seam_history_crosscheck.py`, `seam_history_narrow_growth.py`.

## 1. Notation

Scale `n`, tail `c` in `{2,3}`, source `W` in `{1,2}^n`. `Q_c(W)` is the forced
continuation, row `u` taking the unique binary symbol with `H(P^n I(WQ)_u)=1`
(`RESULTS-BINARY-WEDGE-HIGH-ELIMINATION.md:47-70`); `rho_c(W)` counts leading
rows whose cut cell is `c` while the continuation stays admissible;
`D_n(c) = max_W rho_c(W)` is the deepest of `RESULTS-RW-LINEAR-SLACK.md:44-58`;
`Sh_c(W) := W[1:] . Q_c(W)[:2]` needs `rho_c(W) >= 2`. Hard-core is
`RESULTS-CORE-CRAIG-MORPH.md:61`, grammar `HC = 2 HC union 12 HC`
(`RESULTS-RANK-ZERO-REDUCTION.md:117-121`); narrow also forbids `22222`, wide
constrains only the junction suffix. `I(e)` is the inverse-terminal cut by its
diagonal recurrence (`RESULTS-DYADIC-PERIODICITY.md:120-126`), `P` the Peel
(`RESULTS-ROTATED-PEEL-IDENTITY.md:14-17`), `P(I(sigma e)) = sigma^2 I(e)` the
rotated identity (same file, 19-38). `(SEAM)` is `P^(n-k) I(vW) = c^(2k)` at
`RESULTS-RW-GUARDED-SEAM-DESCENT.md:84`, four-guard version refuted at 92-120.

## 2. The two lemmas `[U]`

**`(L1)` run inheritance.** If `rho_c(W) >= 2` then `Q_c(Sh_c W) = Q_c(W)[2:]`
and `rho_c(Sh_c W) = rho_c(W) - 2`. By the light cone, `I(e)_t` reading only
`e[ceil((t-1)/2) .. t]` by induction from the recurrence, `Sh_c W` at
`e[n+1 .. 2n+1]` has as forcing equations the scale-`n` equations at rows `u+2`;
admissibility transfers since rows `0,1` are covered by `rho >= 2`.

**`(L2)` seam equals inheritance.** For `vW'` admissible with `W'[-3:]`
hard-core, `P^(n-1) I(vW') = (c,c)` iff `rho_c(vW'[:-2]) >= 2` and
`Sh_c(vW'[:-2]) = W'`: the seam cells are run cells `0,1` of `S = vW'[:-2]`,
both `c` exactly when `W'[-2:]` are `S`'s `H`-forced symbols with passing pins.

## 3. Orphan bound and run floor `[U]`

**`(C1)`.** A seam-passing `v` forces `rho_c(W') + 2 = rho_c(vW'[:-2])`, at most
`D_(n-1)(c)`, so every `W'` with `rho_c(W') > D_(n-1)(c) - 2` is an **orphan**
with no seam-passing prepend; `k=2` is two `k=1` steps by identity (1) of the
report. `(L1)` further gives `D_n(c) >= D_(n-1)(c) - 2` uniformly, each
`rho >= 2` parent having an in-grammar child: proved, not observed. Only
strictness is computed, at 54 of the 60 rows `n=4..18` over both grammars and
tails `[C]`; the six exceptions are narrow `c=3` at `n=4,10,11`, narrow `c=2`
at `n=18`, wide `c=2` at `n=13` and wide `c=3` at `n=4`, five still carrying
top orphans.

The equivalence of universally quantified `(SEAM)` with `RW` is a triviality,
not a theorem: `RW => (SEAM)` is vacuous, no constant old cut arising, while
`(SEAM) => RW` is the report's descent at 84-90 plus an unstated `n<=3`/`k=0` base.

## 4. Exhaustive census, scales 3..18 `[C]`

Entries are `D_n(c)` with `(top-orphans / deepest words)` at that depth.

| n | narrow c=2 | narrow c=3 | wide c=2 | wide c=3 |
|---|---|---|---|---|
| 7 | 4 (3/3) | 4 (5/5) | 4 (5/5) | 4 (10/10) |
| 8 | 3 (3/3) | 3 (3/3) | 3 (9/9) | 6 (3/3) |
| 9 | 2 (6/6) | 8 (3/3) | 4 (4/4) | 8 (6/6) |
| 10 | 4 (4/4) | 6 (1/3) | 5 (6/6) | 7 (4/4) |
| 11 | 3 (5/5) | 4 (2/5) | 6 (4/4) | 7 (12/12) |
| 12 | 5 (5/5) | 5 (3/3) | 9 (2/2) | 8 (1/1) |
| 13 | 5 (2/2) | 5 (3/3) | 7 (11/12) | 9 (3/3) |
| 14 | 5 (7/7) | 5 (5/5) | 10 (4/4) | 8 (8/8) |
| 15 | 7 (2/2) | 4 (12/12) | 9 (10/10) | 8 (9/9) |
| 16 | 6 (2/2) | 6 (3/3) | 10 (3/3) | 10 (18/18) |
| 17 | 10 (2/2) | 5 (3/3) | 11 (10/10) | 10 (6/6) |
| 18 | 8 (1/2) | 8 (2/2) | 12 (16/16) | 11 (12/12) |

The wide columns are the control, reproducing the deepest columns of
`RESULTS-RW-LINEAR-SLACK.md:44-58` at every `n=7..17` and its section 9.4 at
`n=18`; the four-guard witnesses
of `RESULTS-RW-GUARDED-SEAM-DESCENT.md:98-101` reproduce too, cuts `3333231`
and `222213000`, runs `4`, seams `31` and `33`. Levels at `n=16` wide `c=2`:

```text
0: 1625/40996   1: 493/13942   2: 237/6266   3: 93/2315   4: 26/1252
5: 14/510       6: 4/131       7: 5/89       8: 0/24      9: 0/8   10: 0/3
```

Zero above `D_15(2) - 2 = 7` as `(C1)` forces, and at `n=18` zero above
`D_17(2) - 2 = 9` (`10:0/2 11:0/16 12:0/16`); parents sharing a child at `n=16`:
2332 wide `c=2`, 2447 wide `c=3`. The narrow-grammar maximum hard-core orphan run
equals `D_n(c)` at every `n=5..18`, both tails, so an `m`-guarded seam lemma is
false **for every amount of history an admissible word attains**, vacuous for
`m > D_n(c)`. The `n=18` run asserted `(L1)` on 84,744 pairs, `(L2)` on 4,642
words over 9,022 seam evaluations finding 581 seams, and completed 60 deepest
orphans to `RW` length.

Four `n=16` orphans `[K]`: `r=0`, length 34, in grammar, terminal `12a` pull, no prepend.

| grammar, c | `f` | cut | lead | seams |
|---|---|---|---|---|
| wide, 2 | `1122212122122122222121222212122121` | `222222222213220102` | 10 | `23`, `23` |
| wide, 3 | `1111112122211122221212121212122121` | `333333333312111110` | 10 | `32`, `32` |
| narrow, 2 | `1222212122122122122122121212122121` | `222222333101111312` | 6 | `32` |
| narrow, 3 | `1222122212212122212221212121212121` | `333333122330132322` | 6 | `13` |

The deepest `n=18` orphans, length 38, same guards: wide `c=2`
`W=111211112211221212`, cut `22222222222232023122`, run 12; wide `c=3`
`W=111212111112221212`, cut `33333333333221200332`, run 11; narrow `c=2`
`W=121212121212121221`, cut `22222222000220002031`, run 8; narrow `c=3`
`W=121212222121221212`, cut `33333333233000003312`, run 8.

## 5. Route eliminated, the uniform guard, and scope

Struck: the guarded-seam family, any lemma forcing a seam-passing prepend from
grammar, terminal pull, and the first `m` constant cut cells, at every `m` an
admissible word attains, `n <= 18`.

The uniform-in-`n` version is closed by the lemmas, not by the census. Call
`(G_m)` the guard at level `m`: at every scale `n >= n0`, every admissible `W'`
with `rho_c(W') >= m` has a seam-passing prepend. By `(C1)` such a `W'` has
`rho_c(W') <= D_(n-1)(c) - 2`, so `D_n(c) >= m` forces
`D_n(c) <= D_(n-1)(c) - 2`, and with the `(L1)` floor `D_n(c) = D_(n-1)(c) - 2`
exactly. From `n0` the run then falls by two per scale until `D_n(c) < m`, and
once `D_(n-1)(c) < m` the guard forbids `D_n(c) >= m` again; conversely
`D_n(c) < m` at every large `n` makes `(G_m)` vacuous. So, given `(L1)`, `(L2)`
and `(C1)`, a uniform guard at level `m` is equivalent to `sup_n D_n(c) < m`,
which is `(RW-alpha)` of `RESULTS-RW-LINEAR-SLACK.md:87-89` at `alpha = 0`: it
implies `RW` at every `n >= m-2`, a run below `m <= n+2` never reaching
`n+r+2`, while `RW` is consistent with the measured `D_n(c)` near `0.6 n` and
implies no constant bound. The lead of the first draft is therefore a closing
reduction, not a route. `(G_m)` fails at any `n >= n0` with `D_n(c) >= m` and a
strict floor, the top word being an orphan by `(C1)`; the exact runs refute
every `(m, n0)` with `m <= 14`, `n0 <= 34` for narrow `c=2` (`D_34(2) = 14`,
floor 11), `m <= 13` for narrow `c=3` (`D_34(3) = 13`, floor 11), and through
the wide table `m <= 12`, `n0 <= 18` for `c=2` and `m <= 14`, `n0 <= 20` for
`c=3` (`RESULTS-RW-LINEAR-SLACK.md` 4 and 9.4). Narrow `D_n(2)` for
`n = 16..34` is `6,10,8,7,6,7,7,9,10,10,8,9,10,10,11,12,13,13,14` and `D_n(3)` is
`6,5,8,6,8,8,9,8,8,11,10,9,10,11,13,11,13,13,13` (`seam_history_narrow_growth.py`,
exact over the 2,921,225 narrow sources at `n=34`); the floor is tight only at
`c=2`, `n = 18, 26` and `c=3`, `n = 19, 31`. Extended 2026-09-16 to
`n = 35..38` (`seam_history_narrow_sub5.py`, `RESULTS-NARROW-SUB5.md`):
`D_n(2) = 13, 13, 13, 13` and `D_n(3) = 14, 13, 15, 16`, exact over 16,182,480
narrow sources at `n = 38`, floor strict throughout, which refutes `(m, n0)`
additionally for `m <= 13`, `n0 <= 38` at `c=2` and `m <= 16`, `n0 <= 38` at
`c=3`. Only `D_n(c)` bounded would rescue
a uniform guard, and it has no support: the near-alternating family `(12)^*`
with at most two defects has maximum run between 2 and 11 over `n = 8..58` in
both grammars and tails with no trend (same script, part 2). A correction to
the first draft's wording: `D_n >= D_(n-1) - 2` with `D_n >= 0` forces the floor
to be strict at infinitely many `n`, not `D_n` to increase; increase infinitely
often needs `D_n` unbounded, which is measured, not proved.

Scope: the orphan census is finite, `n <= 18`, and the narrow runs to `n = 34`
are maxima only; `(L1)`, `(L2)`, `(C1)`, the run floor and the equivalence of
a uniform guard with a bounded run are uniform. The equivalence remark is narrow-language; published wide `RW`
admits sources with `11` in `W[-3:]`, blocked by condition 1 whatever the seam
cells do, counted as grammar-only orphans, nonzero only in the wide rows and at
most 6 (`n=10`, `c=2`). Completion to `RW` length is exhibited, not argued: that
needs `rho <= n+r-1` for three free pull symbols. `RW`, `(RW-alpha)`, `SEP` and
`PT2` are untouched.

## 6. Reproduction

From the repository root:

```sh
uv run --no-project --with numpy python \
  experiments/rule30/p1-period2-invariant/seam_history_inheritance.py 18
uv run --no-project --with numpy python \
  experiments/rule30/p1-period2-invariant/seam_history_crosscheck.py
uv run --no-project --with numpy python \
  experiments/rule30/p1-period2-invariant/seam_history_narrow_growth.py 34 58
```

The census runs in about 9 s at `n=18` (2.4 s at `n=16`) asserting `(L1)` and
`(L2)` on everything it enumerates; the crosscheck re-derives the four
witnesses and the `n=7` control through `guarded_rw_seam_audit.py`'s
independent `(H,E)` kernel; the narrow growth probe reuses the census kernel
and takes about 270 s, 140 s of it at `n=34`.

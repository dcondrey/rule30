# Composition charge (12) holds exhaustively on hard-core sources through length 30

Date: 2026-09-16. Pre-registered in `PREREGISTRATION-HC-COMPOSITION-CHARGE.md`
before the run. Script `seam_history_hc_charge.py`, record
`seam_history_hc_charge.json`, log `seam_history_hc_charge.log`.

**`[C]` The inequality (12) of `RESULTS-EVENTUAL-CONSTANT-TAIL.md` section 8,
`s_2(W) <= #2(W) + [22 in W]` and `s_3(W) <= #2(W) + 3` for hard-core `W`,
exact through `|W| = 22` before, has no violation at any of the 5,581,494
hard-core words of length 23 to 30, both tails. The minimum slack is 4..9
(`c = 2`) and 7..11 (`c = 3`) on the new range and never returns to 0 after
the recorded tight case at `n = 17`. The kill did not fire; (12) stays a
falsifier-backed target, not a proved charge, and nothing here touches `RW`,
`(SEP)` or `(PT2)`.**

## 1. What was computed

`s_c(W)` was taken as `rho_c(W)` from `seam_history_inheritance.run` over the
wide grammar with `maxrows = 2n+2`: the number of leading forced rows whose
cut cell equals `c` while the continuation stays hard-core across the
junction. Sources are enumerated through the same trie with the no-`11`
clause only, `F(n+2)` words at length `n`. The identification with the
recorded `s_c` was gated, not assumed: at every `n = 1..22` and both `c` the
maximum `rho` equals the recorded row of `RESULTS-EVENTUAL-CONSTANT-TAIL.md`
271-275 (44 values), `rho` equals the recorded sharp values on `121` (`c=3`,
4), `12212121212121212` (`c=2`, 10) and `122212222222221212122` (`c=2`, 12),
and the minimum slack is `>= 0` throughout. The gate passed before any new
length was reported. Slack `0` occurs only at `(n,c) = (1,2)` (the empty run),
`(3,3)`, `(4,2)` on `1212`, and `(17,2)`; `(4,2)` was not noted in the earlier
record.

## 2. Result, `n = 23..30`

`D` is the maximum `s_c` over hard-core words; `min` the minimum slack; `W`
the first word attaining it with its run and bound; `seam` whether a prepend
`v = 1`, `v = 2` passes the literal seam `P^(n-1) I(vW) = (c,c)`.

| `n` | words | `c=2`: `D` | min | `W` (`rho`/bound) | seam | `c=3`: `D` | min | `W` (`rho`/bound) | seam |
|---|---|---|---|---|---|---|---|---|---|
| 23 | 75,025 | 13 | 4 | `12121221212222212222212` (13/17) | no, no | 13 | 7 | `12221222212222221221212` (13/20) | no, no |
| 24 | 121,393 | 11 | 4 | `122121212121212121212122` (10/14) | no, no | 11 | 9 | `121212121212212222122121` (8/17) | no, no |
| 25 | 196,418 | 10 | 6 | `1212121212121212121212221` (8/14) | v=1 | 11 | 8 | `1212212122122221212122212` (11/19) | no, no |
| 26 | 317,811 | 10 | 9 | `12121212121212122122122121` (6/15) | no, no | 13 | 8 | `12122121222221221212221222` (13/21) | no, no |
| 27 | 514,229 | 11 | 7 | `121212121222122121212122121` (9/16) | no, no | 11 | 10 | `121212121222221221221212121` (9/19) | both |
| 28 | 832,040 | 12 | 8 | `1212212121212222121212122121` (9/17) | no, no | 14 | 9 | `1212122222212212221222121222` (14/23) | no, no |
| 29 | 1,346,269 | 13 | 8 | `12122122121222222221212212212` (13/21) | no, no | 12 | 9 | `12121222221212121221221212212` (12/21) | no, no |
| 30 | 2,178,309 | 13 | 7 | `121212121221221222221212212212` (13/20) | no, no | 13 | 11 | `121212221212122121212121222221` (10/21) | no, no |

No word has slack 0 at any `n >= 18`. The full slack histogram per `(n,c)` is
in the record.

The same quantity in the three source grammars, `narrow` (no `11`, no
`22222`; `seam_history_narrow_growth.log`), hard-core (this run) and `wide`
(all `2^n` sources; `uc/r1-injection/census_rate_table_n3-33.log`), written
`narrow / hard-core / wide`:

| `n` | `c=2` | `c=3` |
|---|---|---|
| 23 | 9 / 13 / 16 | 8 / 13 / 16 |
| 24 | 10 / 11 / 14 | 8 / 11 / 16 |
| 25 | 10 / 10 / 16 | 11 / 11 / 16 |
| 26 | 8 / 10 / 15 | 10 / 13 / 15 |
| 27 | 9 / 11 / 17 | 9 / 11 / 19 |
| 28 | 10 / 12 / 21 | 10 / 14 / 17 |
| 29 | 10 / 13 / 19 | 11 / 12 / 16 |
| 30 | 11 / 13 / 18 | 13 / 13 / 19 |

The inclusions `narrow <= hard-core <= wide` hold at every entry, as they
must. On `n = 24..30` the hard-core maximum is at most `floor(n/2)` for both
tails; the wide maximum exceeds it by 3 to 9, so the deepest wide runs on
this range are carried by sources that contain `11`.

## 3. Reading

An exhaustive extension of the falsifier range from 22 to 30, with the
margin widening rather than closing. It does not prove (12): the pointwise
certificate families for it are the killed rows "Pointwise scale
derivative/matching" and the intervention hierarchy of
`RESULTS-SCALE-TELESCOPING.md` section 2, and this run adds no certificate.
What it adds is data a symbolic attempt has to respect: the minimum-slack
words are, with two exceptions, seam orphans (no prepend passes the literal
seam), and the hard-core maximum run sits at or below `n/2` from `n = 24`
while the wide one does not. `D_n^HC(c) <= 14` through `n = 30`.

## 4. Scope

Finite, `n <= 30`, hard-core sources, both tails, one implementation gated
against the earlier independent census only on `n <= 22`. No statement about
the narrow-grammar deepest run beyond `n = 34`, about `sup_n D_n(c)`, or
about the counting-line constant is made or changed.

## 5. Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --no-project --with numpy python seam_history_hc_charge.py 30 seam_history_hc_charge.json
```

Exit 0 on gate pass and no kill, 2 on a gate failure, 1 on a kill. 142 s
single core, of which `n = 30` is 56 s; the count of words per length grows
by the golden ratio, so each further length costs about 1.6x the last.

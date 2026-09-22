# E1-E5 audit: there is no E1-E5 preregistration to score, and one claim in `RESULTS-EXTINCTION-MARGIN.md` is overstated

Date 2026-09-05. Read-only audit. `RESULTS-EXTINCTION-MARGIN.md` was **not
modified**; findings are recorded here per `TASKLIST-20260904-R1.md` E2.

## 1. The claimed scoring obligation does not exist

A prior status note listed as open: "Task 4 / E1-E5 extinction margin: data
collected but **NOT scored against the prereg**."

**Verified: there is no E1-E5 preregistration.** `E1-E5` appears in exactly four
places repo-wide (three prior status notes plus
`RESULTS-PRODUCT-GEOMETRIC-MEAN.md:194`). Its definition is
`TASKLIST-20260904-R1.md` lines 74-78, and those five entries are **audit and
re-derivation tasks**, not a comparative experiment:

| | task | kind |
|---|---|---|
| E1 | re-derive margins `n=10..18` from `literal_extension` | re-derivation |
| E2 | audit every numeric claim in `RESULTS-EXTINCTION-MARGIN.md` | audit |
| E3 | are the max-survival words a structured family? | descriptive |
| E4 | if so, exclude that family by an exact argument | the theorem fragment |
| E5 | why is the margin tail-dependent? | descriptive |

No task, metric, baseline, strong-outcome or kill condition is stated for any of
them. There is nothing to score, and **no preregistration is being written now**:
the margin data has already been seen (min 5 at `n=12`; the full table below), so
any kill condition authored at this point would be written after the curve.
`RESULTS-PRODUCT-GEOMETRIC-MEAN.md:193-195` already made the correct call —
"reported as measured; scoring against the E1-E5 preregistration is not done
here". That line should read "no such preregistration exists" rather than
implying one is pending. **The margin table is descriptive, un-preregistered
data. It is fine as data and must not be reported as a passed test.**

## 2. E2: the numeric claims, audited against the extended range

`RESULTS-EXTINCTION-MARGIN.md` was written 2026-09-04 from six points,
`n = 10..18`, `r=0`, `c=2`. Data now runs to `n=24` both tails
(`RESULTS-PRODUCT-GEOMETRIC-MEAN.md`) and to `n=30` for `c=2`
(`docs/rule30/overnight/LEDGER-20260905.md`, where the same quantity is called
`gamma`). **`gap` and `gamma` are the same object**: both are
`(n+2) - max_survival_row` at `r=0`. The two tables agree in every shared cell
(`n=17..24`, both `c`), which is the cross-check for the transcription below.

| claim | verdict on the extended range |
|---|---|
| the six-point table `n=10..18`, `c=2`: gaps `7, 5, 6, 8, 8, 8` | **holds.** `n=10..16` independently recomputed via `overnight_census.run()`; `n=17,18` read from `overnight_c2_*.log` |
| "the gap does not shrink toward 0 as `n` grows" | **holds, and strengthens.** `c=2` continues `10, 11, 10, 12, 9, 12` at `n=19..24` and reaches `14` at `n=30`; global minimum over every measured cell is `5`, at `n=12` |
| "the last three points sit at a stable 8" | **true in range, and the plateau ends.** `n=19` breaks it upward |
| "max-survival-row grows roughly linearly with slope close to 1" | **overstated.** Least-squares slope on its own six points is **0.726**, not ~1; over `n=10..24` it falls to **0.561** (`c=3`: 0.484 and 0.731) |

The last row is the one correction, and it runs **in the document's own favour**:
a max-survival slope below 1 against a target growing at exactly 1 is precisely
why the margin widens rather than closing. The document understated its own
evidence by describing the slope as ~1 while its table already implied ~0.73.

Margins used (source: `RESULTS-PRODUCT-GEOMETRIC-MEAN.md`, cross-checked against
the ledger's `gamma` table):

```
 n      10  12  14  16  17  18  19  20  21  22  23  24
 c=2     7   5   6   8   8   8  10  11  10  12   9  12
 c=3     5   6   8   8   9   9   8   8   7  10   9  10
 min     5   5   6   8   8   8   8   8   7  10   9  10
```

## 3. What is still open, and what is not

- **E1** is effectively satisfied for `n=10..16` (recomputed from
  `literal_extension` via `overnight_census.run()`) and `n=17..24` (read from the
  census logs with the code path verified). No further re-derivation is needed.
- **E2** is closed by section 2.
- **E5**'s premise — "`c=2` rising, `c=3` flat" — **is not supported** on the
  extended range. Both tails fluctuate: `c=2` runs `7,5,6,8,8,8,10,11,10,12,9,12`
  and `c=3` runs `5,6,8,8,9,9,8,8,7,10,9,10`. The ledger separately retracted a
  claimed climb in `gamma` as an even-`n` artifact. Do not spend further
  effort explaining a tail asymmetry that the data does not show.
- **E3/E4: re-verified 2026-09-05 and both are negative.** See
  `RESULTS-E3-MAXSURVIVAL-WORD-STRUCTURE.md`. `RESULTS-FIBER-EXTREMAL-FAMILY.md`
  answers E3 for the forced *continuations* (no parametrized family, `n=10..16`);
  the separate claim in `RESULTS-EXTINCTION-MARGIN.md` that the max-survival
  *source words* "share a long common suffix, differing mainly in their first one
  or two symbols" is **false** on 13 of the 18 cells `n=10..18`, both tails: on
  `c=2` the free prefix length runs 6,2,1,13,5,14,3,6,18 for `n=10..18`, and at
  `n=18,c=2` the 16 finalists share no common suffix at all. E4 therefore has no family to exclude, and the "suffix window near
  the append point" proof route in `RESULTS-EXTINCTION-MARGIN.md` step 1 should
  not be attempted in that form.

**Nothing here is evidence that `gap(n) >= g_min > 0` for all `n`.** That
implication — which would give `H_r(n) = 0` outright — is stated correctly as
unestablished in `RESULTS-EXTINCTION-MARGIN.md` and remains so. The range is
`n <= 30`; obstruction H applies.

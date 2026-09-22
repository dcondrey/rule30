# Extremal sources are not a bounded-period family

Date: 2026-09-06. Script: `extremal_word_family_dump.py`.

Status: **KILL CONDITION FIRED. The smallest periods of the extremal hard-core
sources GROW with `n`: at `n=8` the extremal set contains words of period 1 and
5, by `n>=13` the smallest period present is 9 or more, and at `n=17,18` the
smallest periods are 15 and 11 against lengths 17 and 18, i.e. no real
periodicity at all. The single-defect shape `2^a 1 2^b` disappears entirely for
`n >= 12`. The finite-list-of-periodic-rays shape does not survive this
measurement.**

Evidence level: `K` (exhaustive over hard-core words, `n = 8..18`, both tails).

## 1. Validation before the claim

Survival is computed with the repo's own `forced_trace` and
`hard_core_extension_length`. The per-`n` maxima this dump finds are identical
to `constant_tail_scale.EXPECTED_MAXIMA` for both tails across the whole range
`n = 8..18`:

```text
c=2:  3 2 4 4 5 5 7 7 10 10 9      (n = 8..18)
c=3:  3 8 6 4 5 5 5 6  6  5 9
```

So the extremal sets below are the registered extremal sets, not a re-derived
approximation.

## 2. The table

`source periods` lists the distinct smallest periods present in the extremal
set, `ap` meaning no period shorter than the word.

```text
  n  c  surv #extremal         source periods #1-defect     cont periods
  8  2     3         8             ap,1,5,6,7         4                2
  8  3     3         3                  3,5,7         0                2
  9  2     2         6               ap,3,7,8         0             ap,1
  9  3     8         5             ap,4,5,6,7         1                7
 10  2     4         7               ap,7,8,9         0             ap,3
 10  3     6         4                  7,8,9         0                4
 11  2     4         7           ap,5,6,7,8,9         1               ap
 11  3     4         9          ap,3,4,8,9,10         0             ap,1
 12  2     5         8              8,9,10,11         0              2,3
 12  3     5         3                ap,7,10         0                3
 13  2     5         2                  11,12         0                3
 13  3     5         5             9,10,11,12         0                4
 14  2     7         3               10,12,13         0                1
 14  3     5        15       ap,7,10,11,12,13         0           ap,3,4
 15  2     7         2                  ap,13         0               ap
 15  3     6         7          ap,6,10,11,13         0                5
 16  2    10         2                  ap,11         0                7
 16  3     6         3               12,13,14         0                4
 17  2    10         2                  15,16         0                8
 17  3     5        24 ap,10,11,12,13,14,15,16         0             ap,3
 18  2     9         8      ap,11,14,15,16,17         0                7
 18  3     9         2                  ap,16         0                7
```

## 3. Reading it

**Sources.** A period of `n-1` or `n-2` on a length-`n` word is not periodicity;
it is the tautology that some suffix matches some prefix. Discounting those, the
genuinely short periods (1, 3, 4, 5, 6) are present only up to `n=11`, and from
`n=12` onward the smallest period in the extremal set climbs with `n`
(8, 9, 10, 11, 13, 11, 15, 10, 11). That is the pre-registered kill: the
extremal sources are not prefixes of periodic sequences of bounded period.

**Single defect.** `2^a 1 2^b` accounts for 4 of the 8 extremal words at
`n=8, c=2`, one word at `n=9, c=3` and one at `n=11, c=2`, and **none at all**
for `n >= 12`. So that shape is a small-`n` coincidence, not a family.

**Continuations.** These behave better than the sources: continuation periods
stay small (2, 3, 4, 5, 7, 8) and only occasionally go aperiodic. If anything in
Observation 4.3's hypothesis survives, it is the statement about extremal
*continuations*, not extremal sources. That is a materially weaker claim and it
is not what the finite-ray argument needed.

## 4. A discrepancy that was mine, not the paper's

An earlier version of this file reported 24 words attaining `max-surv` at
`n=17, c=3`, outside the "between 2 and 18" band of the paper's Observation 4.3,
and flagged it as a counting-convention gap in the paper. **That flag was
wrong.** It came from defining the extremal set per tail. The paper's
`max-surv(n)` is the maximum over words *and* tails jointly. Recomputed that
way:

```text
 n  global max  #attaining  source periods            #1-defect  tails
 8       3          11      ap,1,3,5,6,7                  4      [2,3]
 9       8           5      ap,4,5,6,7                    1      [3]
10       6           4      7,8,9                         0      [3]
11       4          16      ap,3,4,5,6,7,8,9,10           1      [2,3]
12       5          11      ap,7,8,9,10,11                0      [2,3]
13       5           7      9,10,11,12                    0      [2,3]
14       7           3      10,12,13                      0      [2]
15       7           2      ap,13                         0      [2]
16      10           2      ap,11                         0      [2]
17      10           2      15,16                         0      [2]
18       9          10      ap,11,14,15,16,17             0      [2,3]
```

Every count lies in `[2, 18]`. Observation 4.3's count claim is correct as
stated, and this file's earlier objection to it is withdrawn.

**The kill in section 3 survives the definition change.** Under the joint
definition the genuinely short periods (1, 3, 4, 5, 6, 7) still occur only
through `n = 11`; from `n = 12` the smallest period present climbs with `n`
(7, 9, 10, ap, ap, 15, 11), and periods of `n-1` or `n-2` are not periodicity.
Single-defect words account for 4 of 11 at `n = 8`, one at `n = 9`, one at
`n = 11`, and **none for `n >= 12`**. So "extremal sources are prefixes of
purely periodic hard-core sequences of bounded period, or single-defect words"
is false under either definition of the extremal set.

## 5. What dies and what does not

Dies: "extremal sources are prefixes of purely periodic hard-core sequences of
bounded period, or single-defect words", and with it the plan to reduce
extinction to a finite list of periodic rays carrying a finite automaton or a
one-dimensional recurrence.

Does not die: `gamma(n) >= 1` itself, which is untouched here; and the weaker
observation about extremal continuations sitting in low-period orbits, which
this measurement supports rather than refutes.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/extremal_word_family_dump.py \
  --first 8 --last 18
```

Roughly a minute; `Fib(n+2)` words times an `O(n^2)` forced trace. Per-word
detail lines (source, continuation, failure symbol) are printed for the first
three extremal words of each `(n, c)`.

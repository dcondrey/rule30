# E3 re-verification: the max-survival *words* are not a suffix-indexed family

Date 2026-09-05. Read-only over `late_pull_diagonal_sat.py`; one new
throwaway script (scratchpad, reproduction inlined in section 5), no existing
file modified. Run log for `n=11,13,15,17,18` kept as
`maxsurv_words_20260905.log` (`n=10..16` even was run interactively and is
reproduced by the same command). `r=0`, both tails.

Motivated by the inherited-claim rule: E3 was recorded as "addressed in
`RESULTS-FIBER-EXTREMAL-FAMILY.md` (another session), not re-verified"
(`RESULTS-EXTINCTION-MARGIN-AUDIT.md` §3). It is addressed only in part, and
the part `RESULTS-EXTINCTION-MARGIN.md` actually leans on is **false**.

## 1. The two documents characterise different objects

`RESULTS-FIBER-EXTREMAL-FAMILY.md` §3 answers E3 for the **continuations**:
the forced output strings reaching `k_max(n,tail)`. Its verdict is a clean
negative — no parametrized family fits `n=10..16`.

`RESULTS-EXTINCTION-MARGIN.md` makes a separate structural claim about the
**source words**:

> The finalist words at each `n` (the ones achieving max survival) share a
> long common suffix, differing mainly in their first one or two symbols —
> consistent with survival depth being governed mostly by a suffix window
> near the append point.

That sentence is the sole stated motivation for its proposed proof route
("attempt a direct argument ... why a forced continuation cannot stay
hard-core past roughly `(source length) - 8` rows"). It was never checked.

## 2. `k_max` and `max_survival_row` are the same quantity

`RESULTS-FIBER-EXTREMAL-FAMILY.md`'s `k_max` (last depth with `D_k>0`, via
`continuation_image_analysis.d_k_table`) and `RESULTS-EXTINCTION-MARGIN.md`'s
`max survival row` (first hard-core violation in `literal_extension`'s output,
seam with `w[-1]` included) agree on **all fourteen** cells `n=10..16`, both
tails, and the recomputation in section 3 reproduces `fiber_full_analysis.json`
exactly on each: same finalist count, same longest common suffix, same residual
set. Two independent code paths, so the fibers at `k_max` in that JSON **are**
the max-survival source words. The identity is established by agreement on
every cell, not traced symbolically through `d_k_table`; the disconfirmation in
section 3 does not rest on it, since every cell there is recomputed directly.

## 3. Measured: shared-suffix length of the max-survival word set

Independent recomputation (script in section 5), `r=0`, every `n` from 10 to 18
and both tails, nothing read from the prior JSON. `free` = source length minus
the longest common suffix, i.e. how many leading symbols the finalists differ in.

```
 n   c   maxsurv  gap   #words   common suffix   free
10   2      5      7       6         4 / 10        6
10   3      7      5       4         8 / 10        2
11   2      6      7       4         9 / 11        2
11   3      7      6      12         0 / 11       11
12   2      9      5       2        11 / 12        1
12   3      8      6       1        12 / 12        0
13   2      7      8      12         0 / 13       13
13   3      9      6       3        11 / 13        2
14   2     10      6       4         9 / 14        5
14   3      8      8       8         1 / 14       13
15   2      9      8      10         1 / 15       14
15   3      8      9       9         0 / 15       15
16   2     10      8       3        13 / 16        3
16   3     10      8      18         0 / 16       16
17   2     11      8      10        11 / 17        6
17   3     10      9       6        14 / 17        3
18   2     12      8      16         0 / 18       18
18   3     11      9      12        13 / 18        5
```

Two cross-checks fall out of this table for free. Every `gap` entry at even `n`
and at `n=17,18` reproduces `RESULTS-EXTINCTION-MARGIN-AUDIT.md` section 2
independently, both tails; and every `n=10..16` row reproduces
`fiber_full_analysis.json` cell for cell. The odd-`n` `c=2` gaps 7 (`n=11`),
8 (`n=13`) and 8 (`n=15`), and the `c=3` gaps 6, 6, 9, are new: the audit's
table sampled only even `n` below 17. They change nothing. The minimum over
the whole range is still 5, still at `c=3, n=10` and `c=2, n=12`.

**Verdict: DISCONFIRMED.** "Differing mainly in their first one or two symbols"
holds at 5 of the 18 measured cells (`n=10,c=3`; `n=11,c=2`; `n=12,c=2`;
`n=13,c=3`; and `n=12,c=3` trivially, a single finalist). It fails at the other
13, and it fails without a pattern.

On the extinction document's own grid, `c=2`, the free prefix runs
**6, 2, 1, 13, 5, 14, 3, 6, 18** for `n=10..18`. The claim holds at `n=11,12`
and nowhere else. At `n=13`, `n=15` and `n=18` the shared suffix is 0 or 1,
meaning the finalists agree on essentially nothing; `n=18` is the document's
own last cited point and its strongest case for the gap, and there the 16
finalists share **no common suffix at all**. `c=3` behaves no better: free
prefix 2, 11, 0, 2, 13, 15, 16, 3, 5, with three cells at zero shared suffix.

The finalist set has no stable size either, ranging from 1 to 18 words with no
trend in `n`, and the parity of `n` matters more than its size: `c=2` collapses
at odd `n` while `c=3` collapses at even `n=14,16`. Nothing here is consistent
with survival depth being governed by a suffix window near the append point.

## 4. Consequence for E4

E4 was "exclude the max-survival family by an exact argument". There is no
family to exclude, on either side of the map: the continuations do not
unify (`RESULTS-FIBER-EXTREMAL-FAMILY.md` §3) and the source words are not
suffix-indexed (§3 here). The "suffix window near the append point" reading
of the survival mechanism is not supported by the data it was drawn from,
so `RESULTS-EXTINCTION-MARGIN.md`'s step 1 should not be attempted in that
form. Its own §"Derivation attempt" already closed the generic
finite-monoid route and asked for "a specific candidate word family";
this document says the obvious source of one is empty.

What survives untouched: the **gap** measurements themselves
(`RESULTS-EXTINCTION-MARGIN-AUDIT.md` §2, `n<=30`), which are descriptive
data and do not depend on any structure claim about the finalists.

## 5. Reproduction (~9 min for the full `n=10..18` table, both tails)

```sh
cd experiments/rule30/p1-period2-invariant
env PYTHONPATH=. uv run python - 10 11 12 13 14 15 16 17 18 <<'PYEOF'
import sys
from itertools import product
from late_pull_diagonal_sat import literal_extension

def winners(n, tail, residue=0):
    rows = n + residue + 2
    best, wins = -1, []
    for w in product((1, 2), repeat=n):
        cont = literal_extension(w, tail, rows)
        prev, fail = w[-1], None
        for i, v in enumerate(cont):
            if v not in (1, 2) or (prev == 1 and v == 1):
                fail = i; break
            prev = v
        s = rows if fail is None else fail
        if s > best: best, wins = s, [w]
        elif s == best: wins.append(w)
    return best, rows, [''.join(map(str, w)) for w in wins]

def suffix_len(ws):
    m, i = min(map(len, ws)), 0
    while i < m and len({w[-1-i] for w in ws}) == 1: i += 1
    return i

for n in map(int, sys.argv[1:]):
    for c in (2, 3):
        best, rows, ws = winners(n, c)
        sl = suffix_len(ws)
        print(n, c, best, rows - best, len(ws), sl, len(ws[0]) - sl)
PYEOF
```

## 6. What this does not claim

Range is `n<=18`, `r=0`; obstruction H applies. Does not claim the finalists
are unstructured — only that they are not the *suffix-indexed* family
`RESULTS-EXTINCTION-MARGIN.md` asserted, which is the specific structure its
proof route needed. A different invariant of the finalist set remains open;
the residual sets in §3 are the data to look at, and `n=10,c=2`'s
`{112111, 121112, 122111, 212111, 221112, 222111}` is not obviously free
or hard-core-constrained (it contains `11` internally, and is 6 of the 64
length-6 words). Not preregistered: this is an audit of an existing claim,
not a comparative experiment.

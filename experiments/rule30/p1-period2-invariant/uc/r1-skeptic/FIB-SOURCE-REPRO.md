# fib_source_check.py: L7 headline number does not reproduce

Ran 2026-09-03 as part of finishing the L7-PERIODIC-SOURCE-CAP thread.

BACKLOG.md rows (section 1 and 6) cite this exact script for the claim
"held to n=40: max run - 0.6n = 2.6 at n=9, pattern 2212."

Current output:

```
hard-core Fibonacci factors tested: 0; max (run - 0.6n) = 0.0 at None
```

Cause: the script builds `w` by the substitution `1->12, 2->1` from seed
`1`. In the resulting word, `"11"` recurs with gap 3-5 (checked over the
first 4000 characters: min gap 3, mean 4.2, max gap 5). The hard-core filter
`"11" not in f[n-1:]` therefore rejects every windowed factor for every
`n` in the tested range 4..100 -- the word this script generates is not a
source of hard-core factors at all, so the loop body that would compute
`run - 0.6n` never executes, and `best` stays at its zero initializer.

The `pattern 2212` cited in BACKLOG.md is length-4 periodic and does not
occur as a Fibonacci-word factor of a hard-core window at any tested n --
it looks like output from the OTHER family test (`periodic_family.py`,
purely-periodic sources), mis-filed under this script's row.

This is not a proof-relevant regression (nothing here bears on P1/SEP
either way); it is a broken citation in the ranked backlog table. The
row's "held to n=40" status is not currently reproducible from the script
it names. Needs one of: point the row at `periodic_family.py`'s actual
output, fix `fib_source_check.py`'s word construction if a genuine
Fibonacci-factor test was intended, or retire the row.

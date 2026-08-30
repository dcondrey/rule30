# Agent 1: right-wedge boundary enforcement

**Verdict: the constraint was already imposed.  Confirmed live, changes no
verdict.  This corrects `RESULTS-ladder-rung0.md` section 4, which named it
the one remaining candidate on the false premise that the encoding "never
touches" it.**

## The constraint is in `ladder.step_window`

```python
ax = abs(x)
if t < ax:  ...require 0
elif t == ax: ...require 1
```

`abs(x)` covers positive `x`, so `col_x(t) = 0` for `t < x` -- i.e.
`c_x(t) = 0` for `x > t` -- is enforced on every modelled column, together
with the edge one at `t = x`.  `ladder.verify_witness` re-checks the same
loop over all columns.  Nothing about it is new, and it was already active in
every rung-0 number.

The real gap is narrower than section 4 stated: columns strictly to the right
of `R` are not modelled at all, so no constraint reaches them.  That gap is
what Agent 2 turns out to occupy.

## Confirmation run: disable it and the language grows

`wedge_right=False` drops the check for `x > 0` only.  Identical parameters
otherwise, Q = 1.  Log: `wedge.log`.

| w | R,k | states, wedge ON | states, wedge OFF | ratio |
|---|---|---:|---:|---:|
| 01 | 2,2 | 472 | 653 | 1.38 |
| 01 | 3,2 | 1,817 | 2,613 | 1.44 |
| 01 | 4,2 | 7,194 | 10,197 | 1.42 |
| 100 | 2,2 | 514 | 725 | 1.41 |
| 100 | 3,2 | 1,955 | 2,901 | 1.48 |
| 100 | 4,2 | 7,716 | 11,349 | 1.47 |
| 1100 | 2,2 | 555 | 789 | 1.41 |
| 1100 | 3,2 | 2,092 | 3,157 | 1.51 |
| 1100 | 4,2 | 8,173 | 12,309 | 1.51 |

The right wedge prunes a consistent 29-34% of the state space, so it is not
vacuous.  **Every verdict is NONEMPTY with or without it**, at every
`(w, R, k)` tested.  No `p >= 2` flips.

## Conclusion

Nothing to implement and nothing to add.  The measurement's value is that it
retires the section-4 recommendation and relocates the unconstrained region
to `x > R`, which is where Agent 2 acts.

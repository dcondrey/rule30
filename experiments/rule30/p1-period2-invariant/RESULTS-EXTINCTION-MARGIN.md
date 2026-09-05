# Does the hard-core extinction row stay a bounded margin behind the target?

Date: 2026-09-04

Status: **suggestive pattern from 6 data points, not a proof.** Two prior
directions (matrix domination, aggregate-ratio domination) were tested and
falsified as stated (`RESULTS-TRANSFER-DOMINATION-CHECK.md`); this is a
third, more promising angle found while looking at the actual last
survivors directly instead of statistics of the population.

## Observation

For each `n` (r=0, c=2), find the maximum row index any source word's
`literal_extension` continuation survives hard-core (before violating
`{1,2}` membership or hitting `11`), and compare it to the target row count
`n+r+2` needed for an `H_r(n)` candidate to even be possible.

| n | target rows (n+2) | max survival row | gap |
|---|---|---|---|
| 10 | 12 | 5 | 7 |
| 12 | 14 | 9 | 5 |
| 14 | 16 | 10 | 6 |
| 16 | 18 | 10 | 8 |
| 17 | 19 | 11 | 8 |
| 18 | 20 | 12 | 8 |

The gap does not shrink toward 0 as `n` grows in this range; the last three
points sit at a stable 8. Max-survival-row itself grows roughly linearly
with slope close to 1 (not saturating at a fixed constant, which was the
first, simpler hypothesis this disproved — checked at n=17,18 specifically
to rule that out).

The finalist words at each `n` (the ones achieving max survival) share a
long common suffix, differing mainly in their first one or two symbols —
consistent with survival depth being governed mostly by a suffix window
near the append point, though clearly not a *fixed-length* window given the
gap's mild growth.

**2026-09-05 disconfirmed:** the common-suffix claim above is false on 13 of
18 cells n=10..18, both tails, recomputed directly from `literal_extension`.
At n=18, c=2 (this document's own last cited point) the 16 finalists share
no common suffix at all. See `RESULTS-E3-MAXSURVIVAL-WORD-STRUCTURE.md`.
Step 1 below should not be attempted in its stated form.

## What would need to be true for this to become a proof

If `gap(n) = (n+r+2) - max_survival_row(n)` is bounded below by any fixed
positive constant `g_min > 0` for all `n` (not just these six points), then
`H_r(n) = 0` for every `n` follows immediately: no word's forced
continuation can reach the target length, so no `H_r(n)` candidate exists,
full stop — no statistical or asymptotic argument needed, no degree-`n`
obstruction to route around.

This has not been established. It is an extrapolation from 6 points across
`n=10..18`. The two likely next steps, in order of cost:

1. **Cheaper first: attempt a direct argument**, not more computation. The
   finalist words' shared-suffix structure suggests looking at
   `literal_extension`'s forcing recursion algebraically (the same
   row-permutation / triangularity facts used in
   `endpoint_restart_cocycle.py` and the prereg's collapse lemma) for why a
   forced continuation cannot stay hard-core past roughly
   `(source length) - 8` rows. If the mechanism killing survival is a fixed
   local obstruction that recurs with bounded period (as
   `endpoint_restart_cocycle.py` found for a related object — an exact
   four-phase restart law), a similar periodic-defect argument might apply
   directly to `literal_extension`'s recursion, without needing more data.
2. **More expensive: extend the census.** `n=19,20` would cost roughly
   20-40 minutes combined at the observed per-`n` cost growth (~4x per +2
   n); `n=22` well over an hour. Only worth doing if a direct argument
   doesn't pan out, since more points cannot themselves prove the bound is
   universal.

## Derivation attempt (2026-09-04, dead end, recorded so it isn't retried)

Traced `literal_extension`'s backward-solve chain (invert `append_dependency_edge`'s
`cone_local` fold from the target `tail` back to the forced `value`) down to
its generating permutations `G_s = FORWARD[swap(s)]` for `s in {0,1,2,3}`.
These generate a group of exactly 8 elements (D4, computed directly from
`dyadic_periodicity_analyzer.FORWARD`/`swap`) — the *same* 8-element
structure already identified project-wide as the proved D8 affine action
in `PROOF-STATE-CAPSULE.md` section 3, "already fully used, not a shortcut
left to try." Confirms the connection is real, but it reconnects to
already-mined territory rather than opening new ground: the group itself
being finite doesn't reduce the dependency window (composition of
permutations is invertible, so it cannot generically "forget" earlier
symbols) — `endpoint_restart_cocycle.py`'s four-phase restart law worked
because it found an exact periodic pattern for one *specific* word family
(`2^m p_r`), not because the group forgets history in general. No analogous
family was found for `literal_extension`. **Do not retry the generic
"reduce to the known finite monoid" argument** without a specific candidate
word family to test it against; that argument alone does not distinguish
this route from the ones already killed by the full-degree `Psi_n` result.

## What this does not claim

Does not establish `H_r(n)=0` beyond what the exhaustive census already
showed (`n<=16`, `RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`). Does not
rule out the gap eventually shrinking to 0 or going negative at some larger
`n` outside the tested range. Supersedes the "bounded-suffix / saturating
max-survival-row" hypothesis, which n=17,18 directly falsified.

## Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python - <<'PYEOF'
from itertools import product
from late_pull_diagonal_sat import literal_extension

def max_survival(n, tail, residue):
    target = n + residue
    rows = target + 2
    best = -1
    for w in product((1, 2), repeat=n):
        cont = literal_extension(w, tail, rows)
        prev = w[-1]
        fail_at = None
        for i, v in enumerate(cont):
            if v not in (1, 2) or (prev == 1 and v == 1):
                fail_at = i
                break
            prev = v
        survived = rows if fail_at is None else fail_at
        best = max(best, survived)
    return best, rows

for n in (10, 12, 14, 16, 17, 18):
    best, rows = max_survival(n, 2, 0)
    print(n, rows, best, rows - best)
PYEOF
```

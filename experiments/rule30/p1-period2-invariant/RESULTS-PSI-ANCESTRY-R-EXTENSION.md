# S1'/S2 for the r=1,2 rows: exact constant-Psi_{n,r} counts and hard-core+12a check

Date: 2026-09-04

Status: setup steps closed per `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md`
section 3. Empty result, as expected there. This is not the section 4
measurement (`|H_r(n)|/2^n` decay); that remains open.

## S1' — exact constant-Psi_{n,r} counts, r=1,2, n<=17

`psi_ancestry_r.py` generalizes `psi_kernel.psi`'s H=1-forcing recursion from
continuation length `n+2` (r=0) to `n+2+r`. At `r=0` this is checked to
reproduce `psi_kernel.psi` exactly (`--check-r0`, verified through n=9),
which is control #2 from the prereg's section 5.

Reproduction: `uv run python psi_ancestry_r.py --max-source 17`
(log: `psi_ancestry_r_20260904.log`, ~79s).

| n | r=1 constant | r=2 constant |
|---|---|---|
| 1-4 | 0 | 0 |
| 5 | **2** | 0 |
| 6 | **3** | 0 |
| 7-17 | 0 | 0 |

r=1's n=5,6 counts (2, 3) match r=0's exactly (`RESULTS-PSI-ANCESTRY-LAW.md`
section 6), including the witness words. r=2 has zero constant words at
every measured n, including 5 and 6. No n>=7 hit for either r, so the
prereg's "check immediately" clause does not fire.

## S2 — hard-core + 12a-terminal check on every constant word found

Every constant-`Psi_{n,r}` word from S1' (r=0's existing n=5,6 table and
r=1's n=5,6 above; r=2 contributed none) checked against
`late_pull_diagonal_sat.literal_witness(word, c, r)` for `c in {2,3}`:

```
r=0 n=5: 12121, 22121           -> literal_witness False for both c
r=0 n=6: 111222, 112122, 211222 -> literal_witness False for both c
r=1 n=5: 12121, 22121           -> literal_witness False for both c
r=1 n=6: 111222, 112122, 211222 -> literal_witness False for both c
```

Zero RW witnesses among the constant-Psi candidates, for both `r=0` and
`r=1`, at both target states. `r=2` has no candidates to check.

## Reading

S1'/S2 are empty, matching the prereg's stated expectation and consistent
with `r=0`'s existing empty count. Per the prereg section 4, this alone is
not evidence for or against RW (an empty census is not a proof, same
caveat as always). The actual pre-registered target is unstarted: measure
`|H_r(n)| / 2^n` (hard-core+12a-terminal-survivable population, independent
of the constant-Psi question checked here) and look for decay with `n`.
That measurement needs `H_r(n)`'s two independent constructions per the
prereg's control #1, not yet built.

## Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python psi_ancestry_r.py --max-source 17
```

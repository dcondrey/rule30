# r1-skeptic, second pass (2026-09-03): scripts and logs

All scripts run as `cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/<script>`.
No file outside this directory was written; no pre-existing file was edited.
Files from the first pass of this lens (census_*.json/log, rw_bitsliced.py, rw_sat.py,
periodic_family.py, suffix_growth.py, state_survival.py, quotient_multiplicity.py,
kill_split.py, fourstate_nearmiss.py, e_only_*.py and their logs) are read, not modified.

| script | log | what it measures |
|---|---|---|
| `counting_threat.py` | `counting_threat.log` | From the complete census JSONs (n = 7..33): max_k N_k/2^(n-k) (all k and k >= 2), the deepest-level ratio, sup_k N_k 2^(lambda k - n) for lambda = 1.1, 1.2, 1.3, and the state-halving margin log2 Q_n - deepest (Q_n exact for n <= 20 from the first-pass logs, extrapolated at 1.775^n beyond). |
| `nearmiss_extract.py` | `nearmiss_extract.log` | Extracts and displays, on `psi_kernel`, the four-state (diagonal-form) near-misses counted by the first pass: n = 21, c = 3 (one violation in 23 columns, 12a ending), n = 22, c = 3 (two violations), n = 27, c = 2 (three violations, 12a ending). |
| `state_level_hits.py` | `state_level_hits_validate.log`, `state_level_hits_n12-14.log`, `state_level_hits_n18-30.log`, `state_level_hits_n31.log`, `state_count_n25-28.log` | Per level k the number of distinct forced-process states D_k, the number passing the E-pin, the hard-core condition, and both, and the largest fiber; pooled by absolute level and by offset from the deepest level. Also Q_n = D_0 exactly for n <= 28. State extraction validated against `quotient_multiplicity.quotient_column` (n = 6..9). |
| `bwh_suffix_cylinder.py` | `bwh_suffix_cylinder.log` | RW census of the cylinder of sources ending in the n = 15 BWH+ extremal suffix `211212112`, n = 15..31, both c. |
| `sturmian_sources.py` | `sturmian_sources.log` | RW admissible runs of all length-n factors of the Fibonacci word under both letter maps, n = 8..64, both c. |
| `null_estimates.py` | `null_estimates.log` | Independence-null arithmetic in states (Q_n ~ 1.44 * 1.765^n, p = 0.405 per column): expected counterexamples beyond n = 33, expected distance-1 near-misses, failure probability of the state-halving lemma, and the null probability of the observed record runs. |
| `census_one.py` | `census_n34_c2.log`, `census_n34_c3.log` (+ `census_n34_c{2,3}.json`) | Complete RW census at n = 34 for one c per process; prints whether SOURCE-HALVING (N_k <= 2^(n-k)) and STATE-HALVING (deepest <= log2 Q_n) hold. Kill test of the two lemmas at the first n beyond the first pass. |

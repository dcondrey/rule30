# r1-hardcore: scripts and logs

All scripts run as `cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant && uv run python uc/r1-hardcore/<script>`.
No file outside this directory was modified.

| script | log | what it measures |
|---|---|---|
| `forced_symbol_census.py` | `forced_symbol_census_n8-12.log` | all 2^n binary prefixes: survivor counts under E only, hard-core only, both (RW), both plus no-22222; joint law of (previous symbol, forced symbol, E ok) per level; forced-one density. Kernel gated against `psi_kernel.psi` on 1,022 prefixes (n <= 9). |
| `rw_restricted_margin.py` | `rw_restricted_margin_n6-16.log`, `rw_restricted_margin_HC_n17-24.log`, `rw_restricted_margin_R5_n17-28.log`, `rw_restricted_margin_R11_n17-32.log`, `rw_restricted_margin_R13_n17-36.log`, `rw_restricted_margin_R13_n37-44.log`, `rw_restricted_margin_R13rev_n16-32.log` | RW deepest-run census with the prefix AND the forced continuation restricted to finite-type supersets of the actual right trace language R: HC (no 11), R5 (no 11, 00000), R11, R13 (all recorded minimal forbidden factors through length 13). R13rev is an orientation control. |
| `level_balance.py` | `level_balance.log` | R13_n equals `right_trace_forbidden.realized_language(n)` for n <= 11; exact balance of the first E constraint on {1,2}^n, HC_n, R13_n. |
| `deep_survivors.py` | `deep_survivors_R13_n26-36.log`, `deep_survivors_R13_n37-42.log` (also `deep_survivors_R13_n28-36.log`, an earlier run without the E+R5 column) | on R13 prefixes: deepest run under E only, E+HC, E+R5, E+R13; the attainers and their common suffix; every prefix with E-only run >= 0.4n together with the index at which its forced word leaves R13. |

Symbol convention throughout: endpoint symbol 1 is rho bit 1, symbol 2 is rho bit 0 (`constant_tail_actual_frontier.endpoint_bits`), e_0 earliest.

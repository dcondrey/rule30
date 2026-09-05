# r1-hardcore, second pass (2026-09-03): scripts and logs

All scripts run as `cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant && uv run python uc/r1-hardcore/<script> [args]`.
No file outside this directory was modified; the first-pass files listed in `INDEX.md` were not edited.
Symbols: endpoint 1 is rho bit 1, endpoint 2 is rho bit 0, `e_0` earliest (repository convention, `constant_tail_actual_frontier.endpoint_bits` with `right_trace_realizable`).

| script | log | what it measures |
|---|---|---|
| `r_exact_sat.py` | `r_exact_sat_m1-30.log`, `r_exact_sat_m1-50.log` (in flight when this index was written; lengths print as they complete) | exact actual-right trace language `R_m` by one CaDiCaL query per candidate extension on the minimal light cone; gated against `right_trace_forbidden.realized_language` for `m <= 10` and the recorded counts through 13. Writes `r_exact_language.json` (237 minimal forbidden factors through length 30, the 3908 words of `R_30`). |
| `hf_make_reversed_json.py` | (none; writes `r_exact_language_reversed.json`) | time-reversed factor list, orientation control |
| `hf_lang_survival.py` | `hf_lang_survival_smoke_n13-16.log` (gates: `psi_kernel.psi` on 1022 prefixes; `BIN=HC` reproduces the 1292 fully hard-core forced continuations at `n = 16`; joint columns reproduce `rw_restricted_margin` and `rw_margin`), `hf_lang_survival_R13_n17-40.log`, `hf_lang_survival_R13_n41-46.log`, `hf_lang_survival_R11_R5_HC_n13-26.log`, `hf_lang_survival_Rexact30_n13-40.log`, `hf_lang_survival_Rexact30rev_n13-36.log`, `hf_lang_survival_R13prefix_HC_R5_n13-34.log` | for every prefix in a finite-type superset `L` of `R`: the first forced step at which the H-forced continuation (no E-pin, no `c`) leaves `L` (LANG-only), the E-only and joint (E + LANG) first failures for `c = 2, 3`, survivor counts `N_k`, the killing forbidden factor, and the independence null `k = h n / (1 - h)` (LANG-only) and `h n / (2 - h)` (joint) |
| `hf_periodic_families.py` | `hf_periodic_families_R13_p12_n13-60.log`, `hf_periodic_families_Rexact30_p12_n13-60.log` | every primitive periodic bit pattern of period `<= 12` lying in `L`, every rotation, `n = 13..60`: LANG-only survival of the forced continuation; a pattern surviving `n + 2` steps would kill HF-L outright (none does) |

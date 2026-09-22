# Arm 3, run 1 — instrument validation and a baseline exponent

Sealed tournaments over `crosstalk-lab run`, one per n-point, 64 committed
hidden cases each, `fuel_consumed` as the effort proxy. Reports and inputs are
in `experiments/rule30/`.

## Result

| candidate | alpha_hat | R^2 | fuel/case @ n=531 | @ n=4031 |
|---|---|---|---|---|
| naive byte-array simulation (baseline) | 1.9980 | 1.00000 | 2.04e7 | 1.17e9 |
| 64-bit bit-parallel simulation | 1.9676 | 0.99998 | 5.05e5 | 2.72e7 |

Fitted over n in {531, 1031, 2031, 4031}.

**What this is.** The instrument recovers the known O(n^2) exponent to three
decimal places with R^2 = 1.00000. That is validation of the measurement, not a
finding about rule 30.

**What the bit-parallel candidate is not.** The lab reports it as the tournament
winner because the challenge minimises raw fuel, and it wins by roughly 40x. Its
exponent is 1.968: that is a constant-factor win, and the dip below 2 is
small-n overhead, not reducibility. Checked rather than asserted: refitting on
the two largest points alone gives 1.985 for the bit-parallel candidate against
1.999 for the naive one, so the fitted exponent climbs toward 2 as n grows. The
row is ~17 words at n=531 and ~126 at n=4031, so per-row loop overhead is the
dominant small-n term. Reporting it as
progress on Problem 3 would be exactly the misreading the pre-registration was
written to prevent. **No exponent improvement was found**, which is the expected
outcome, since no sub-quadratic algorithm for the center column is known.

**Chance floor, observed.** The `constant` candidate (`solve(n) = 1`, 406 bytes)
scored accuracy 0.53125 on a one-bit output and was rejected on
`all_cases_correct`. With 64 cases the floor is 2^-64; with the five cases a
casual setup would use, a guesser wins one run in 32.

## Defect found and fixed: the reproduction gate was a wall-clock coin flip

The first N=2000 tournament failed with `baseline was not independently
verified: accuracy differs: primary=1 reproduction=0.234375`, while the primary
and reproduction evaluators were given identical `SandboxConfig`.

Root cause: `src/engines/sandbox.rs` set `store.set_epoch_deadline(1)` against a
free-running one-tick-per-second epoch incrementer. A call therefore received
somewhere in (0, 1] seconds of wall clock depending on its phase relative to the
ticker. Once a single case approached that budget, the second (reproduction)
pass died partway through the case list, and the run was reported as a
determinism failure. The evaluator's whole contract is bit-identical
reproduction under `deterministic: true`, so a free-running wall-clock interrupt
as the *binding* constraint made the gate flaky precisely in the expensive-
candidate regime the lab exists to measure.

Fix: derive the deadline from the operator's `timeout_secs` plus one tick of
phase slack, leaving fuel as the deterministic bound and the epoch deadline as a
liveness backstop. After the fix, N=2000 reproduces exactly (primary and
reproduction fuel agree to the unit at every point above).

No regression pin. Three behavioural tests were written and all three pass
against the pre-fix code, so none of them pins the defect: two synthetic busy
loops were folded away by Cranelift, and the aged-manager test refuted its own
hypothesis. `tests/sandbox_tests.rs` keeps only a derivation test asserting the
deadline scales with `timeout_secs`, carrying a FIXME saying it does not reach
the call site. The fix stands on the empirical handle above, not on a test.

Still open, not fixed here:

- `resource_limit_hit` does not distinguish fuel exhaustion from an
  epoch-deadline abort, so a wall-clock kill is still indistinguishable from a
  deterministic one in the report.
- `cpu_fuel_limit` is a budget for the **whole case list**, not per case:
  `evaluate_i64_cases_with_timeout` threads `remaining_fuel` through the loop and
  breaks with `resource_limit_hit` when it reaches zero. Reported "fuel/case"
  above is therefore the aggregate over 64, which is sound for the fit but means
  a candidate whose cost varies sharply with n inside a band cannot be rejected
  per case.

## Table-lookup cap

Landed after the run: the challenge file takes an optional
`max_candidate_bytes`, enforced against the baseline and every candidate, capped
in turn by the 32 MiB transport limit. Without it `MAX_WASM_BYTES` alone admits
~2.7x10^8 tabulated bits, enough to pass every band run so far. The bands used
here were fitted before the cap existed and no table candidate was submitted, so
the run stands; every future band sets the cap to 64 KiB.

Still not enforced: the n >= 10^6 decision bands from the pre-registration.
Points here top out at n=4031.

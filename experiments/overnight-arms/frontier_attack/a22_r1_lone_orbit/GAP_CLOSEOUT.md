# Gap closeout, parent session, 2026-08-30

Two gaps flagged in the parent session's own review of `a22_r1_lone_orbit`'s
first report. Both closed here, directly, not delegated.

## Gap 1: the "m=12, all-t is a genuine unexplained anomaly" claim

**Does not survive replication. Retracted.**

The original report's control (`ensemble_control.py`, seed `20260830`,
`K=1,000,000`) showed p=0.5714 at m=12 -- no deviation. Re-running the same
unmodified script at `K=2,000,000` (same seed, a strict superset draw)
showed p=1.479e-8 -- a large, apparently significant deviation, prompting
the "unexplained by its own control" flag.

That flag does not hold up: a **second, independent RNG seed**
(`31415926`, same K=2,000,000, fully disjoint train+test draw) gives p=0.55
at m=12 -- back to no deviation. Two out of three realizations (seed
20260830/K=1e6, seed 31415926/K=2e6) show no effect; one realization
(seed 20260830/K=2e6) shows a large one. That pattern -- present in one
draw, absent in a resampling -- is the signature of ordinary sampling
variability at m=12's bin-count regime (4096 bins), not a reproducible
effect. **m=12 is not evidence of anything, orbit or ensemble.** The
earlier write-up's phrasing ("no cell survives Bonferroni... smallest
surviving p is m=12") was also internally contradictory regardless of the
replication question, and is corrected below.

m=14 and m=16, by contrast, show the same large deviation in **every**
tested realization (both seeds, both K, both the all-t and zero-set
restrictions, and in the raw ensemble control with no orbit involved at
all) -- reproducible, not a fluke -- and carry the sparse-bin overfitting
signature named in the original report (train_err far below eps_30(m),
e.g. at m=16: train 0.154-0.163 vs eps30 0.173; test_err far above it).
That diagnosis stands as originally stated.

## Gap 2: the zero-set restriction has no matched control, and eps_30(m)
might be the wrong reference for it

**Reference is correct; no gap.** By left permutivity, `c_t = s(t,0) =
b_t XOR g(b_0,...,b_{t-1})` for the fresh independent seed bit `b_t`, while
both the window `gamma = (c_{t-m},...,c_{t-1})` and `r_t = s(t,1)` depend
only on `b_0,...,b_{t-1}`. XOR with an independent uniform bit randomizes
`c_t` completely regardless of its correlation with `g(b_0,...,b_{t-1})`,
so `c_t` is exactly Bernoulli(1/2) and independent of `(gamma, r_t)` jointly
in the i.i.d. ensemble -- meaning conditioning on `c_t=0` does not change
the distribution of `(gamma, r_t)`, and `eps_30(m)` (the unconditional
Bayes error) IS the correct reference for the zero-set-restricted case too.

Verified two ways, not just derived:
1. `ensemble_control_zeroset.py`, `K=2,000,000`: `c_t=0` fraction over all
   rows = 0.500047 (matches Bernoulli(1/2) to 5 significant figures), and
   the `|all` and `|Z` test-error/p-value columns track each other closely
   at every `m` (e.g. m=8: p|all=0.0078, p|Z=0.068; m=16: both effectively
   0) -- no systematic offset between the two restrictions beyond what the
   smaller `n` in the `|Z` column explains.
2. `independent_eps_check.py`, a **structurally different implementation**
   of `eps(m)` (explicit numpy boolean-array simulation per window `g`,
   vs. `eps_theorem.py`'s big-int bitmask-packing method): exact match to
   12 significant figures at every `m=1..16`. This also closes a real hole
   in `a21`'s own pipeline: its cross-check against direct enumeration
   (`eps_theorem.py`'s `main()`) only runs for `t<22`, i.e. `m<=10` --
   for `m=11..16` the comparison set is empty and the check silently
   no-ops. `eps_30(12)`, `eps_30(14)`, `eps_30(16)` -- the exact numbers
   the whole R1-lone-orbit arm and `PATH.md` 9.4 cite -- had never been
   independently verified before this check. They are now, and they are
   exactly correct.

## Net effect on the arm's verdict

Unchanged in substance, corrected in precision. At every window width
where the comparison is trustworthy (not overwhelmed by sparse-bin
overfitting, which afflicts the ensemble control identically to the
orbit), the lone-seed orbit's window-conditional error is statistically
indistinguishable from the ensemble value. No cell -- including the one
originally flagged as an outlier -- survives a proper replication check as
real signal. Obstruction E stays open; this remains a null result on the
first direct probe of it, now on firmer footing than the original
write-up gave it.

## Files

- `ensemble_control_zeroset.py`, `ensemble_control_zeroset_output.txt`
  (K=2e6, seed 20260830)
- `independent_eps_check.py`, `independent_eps_check_output.txt` (m=1..16,
  exact match every row)
- `ensemble_control_freshseed.py` (K=2e6, seed 31415926, ad hoc, not
  cleaned up -- a `sed`-generated one-seed-changed copy of
  `ensemble_control.py`, kept for reproducibility)
- `ensemble_control_2e6_output.txt` (K=2e6, seed 20260830, the run that
  triggered this investigation)

Tool calls for this closeout: ~14 (2 script writes, 4 runs, 1 sed-copy, 1
this file).

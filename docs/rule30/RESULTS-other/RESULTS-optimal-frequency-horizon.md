# Optimal-kernel frequency at 2^29 cached bits: no coherent line

Date: 2026-09-16. **Finite diagnostic at one derived frequency. No spectral
line, no absence theorem, and no prize result.**

The [bilateral current report](RESULTS-bilateral-frequency-current.md) derives
`alpha_* = acos(-1/3)/(2*pi) = 0.3040867...` as the exact minimizer of the
bilateral kernel's spatial decay modulus, `rho_* = 1/sqrt(3)`, and probes it on
the first 2^20 cached center bits. That probe read 0.1% of the available cache.
This extends the same frequency, unchanged and unfitted, to 2^29 bits.

`alpha_*` is optimal for the extraction kernel, not for Rule 30. It is the
cheapest frequency to read with this family of Green functions; nothing predicts
that the center column carries energy there.

## Pre-registration

Fixed before the run, in
[`optimal_frequency_horizon_probe.py`](../../experiments/rule30/optimal_frequency_horizon_probe.py):
dyadic prefixes `2^12..2^29`; 32 disjoint blocks of `2^24` with the global phase
retained; statistic `S_N = mean_(t<N) (2*c_t-1)*exp(-2*pi*i*alpha_* t)`, reported
as `sqrt(N)*|S_N|`, which is `O(1)` under square-root cancellation and grows like
`sqrt(N)` under a coherent line.

* **Kill.** `sqrt(N)*|S_N|` bounded along the ladder with block phases spread:
  no line above the `2^(-29/2) = 4.3e-5` noise scale.
* **Positive.** `|S_N|` flat at a positive value across three or more doublings,
  with the 32 block phases concentrating well above the `1/sqrt(32) = 0.177`
  resultant length expected of uniform phases.

## The kill condition fired

Over 18 rungs `sqrt(N)*|S_N|` stays in `[0.28, 0.96]`, mean 0.655, median 0.662,
against the Rayleigh reference for an incoherent sign sequence (mean
`sqrt(pi)/2 = 0.886`, median `sqrt(log 2) = 0.833`). The log-log slope of
`|S_N|` is `-0.5233`, where `-0.5` is exact cancellation and `0` a coherent line.

```text
N          |S_N|       sqrt(N)|S_N|
2^20       8.118e-04   0.831
2^24       1.538e-04   0.630
2^27       3.458e-05   0.401
2^29       4.048e-05   0.938
```

At the horizon the seeded random `+-1` control gives `sqrt(N)|S_N| = 2.153`,
larger than the center column's 0.938; the binary oscillator at the same
frequency gives `0.63661977`, matching `2/pi` to eight digits.

The 32 disjoint blocks are the sharper statement, being independent where the
nested prefixes are not. Their phases are uniform: resultant length 0.097
against the 0.177 uniform reference, Rayleigh `p = 0.74`. Normalized block
amplitudes have median 0.993, and the largest single block, `4.750e-04`, is 11.7
times the full-horizon coefficient. The blocks cancel each other rather than
reinforcing.

**Any persistent line at `alpha_*` has amplitude below about `4e-5`**, against
about `1e-3` at `2^20`: the noise scale fell from `9.77e-4` to `4.31e-5`, the
`sqrt(512)` the horizon bought. This measures the finite
horizon only. A null coefficient excludes nothing: the conditional in the
bilateral report runs one way, a *nonzero* limiting coefficient at irrational
`alpha_*` would exclude eventual periodicity, and its absence at any finite
horizon implies nothing about the infinite orbit.

## What the numbers rest on

The cache is the Wolfram Data Repository billion-bit center column; the file's
SHA-256 matches its recorded checksum. Of the 2^29 bits used, **2^20 are
re-derived here from the singleton seed** by packed 64-bit row evolution, cell by
cell against the cache, a 128-fold increase over the previous 8,192-bit check,
alongside the helper's 8,192-bit big-integer check and 257-bit scalar check. The
remaining 511/512 of the horizon is not independently recomputed, and at this
scale that provenance gap, not the arithmetic, is the dominant risk: regenerating
2^29 center bits is an `O(T^2)` evolution and is not feasible here.

Two independent checks of the arithmetic: the nine rungs shared with the earlier
probe reproduce exactly under this script's different implementation (chunked
accumulation with exact dyadic starting phases rather than one whole-array pass),
and the 32 block coefficients average to the full coefficient within `1e-12`.

```sh
uv run --offline --no-project python experiments/rule30/optimal_frequency_horizon_probe.py
```

The [probe record](../../experiments/rule30/optimal-frequency-horizon-probe.json)
stores every rung, both controls, the 32 blocks, the circular statistics, the
payload digest and the script and helper hashes.

# P2 density: Mersenne lead and seed-specific Walsh status

Date: 2026-09-09. Evidence: **M** (exact finite computation), **R/U** for
the sufficient reductions inherited from `RESULTS-p2-time-index-walsh.md`.
No new asymptotic bound is proved. The result is seed-specific wherever the
lone-seed centre column is used; no a.e. statement is inferred.

The cheap lead from arXiv:2604.00165 concerns the full-row support difference
`epsilon(m)=|S_m^(30)|-|S_m^(22)|`, not the centre column. Exact bit-parallel
evolution gives the following Mersenne values:

| m | epsilon(m) | Rule 30 support | Rule 22 support |
|---:|---:|---:|---:|
| 1 | 0 | 3 | 3 |
| 3 | 0 | 6 | 6 |
| 7 | 0 | 12 | 12 |
| 15 | -2 | 22 | 24 |
| 31 | -9 | 39 | 48 |
| 63 | -18 | 78 | 96 |
| 127 | -60 | 132 | 192 |
| 255 | -115 | 269 | 384 |
| 511 | -242 | 526 | 768 |
| 1023 | -500 | 1036 | 1536 |

The pattern is a finite diagnostic about full-row support. It contains no
centre-column Walsh coefficient and gives no implication for P2. It is
dropped as an attack route. Reproduce with

```sh
uv run python experiments/rule30/p2_mersenne_lead.py
```

For the actual lone-seed centre trace, the existing exact time-index Walsh
implementation was run for shells `k=1,...,12` (length through 4096). The
largest shell had signed shell discrepancy `dc=-56`, maximal Walsh magnitude
`W_12=240`, maximal aligned restriction `68`, maximal prefix discrepancy `65`,
and dyadic tree energy `54856`. These values are measurements only. They do
not bound later shells. Reproduce with

```sh
uv run python experiments/rule30/p2_time_index_walsh_probe.py \
  --min-k 1 --max-k 12 --json
```

The exact reductions remain valid: `k W_k/2^k -> 0` is sufficient for the
seed-specific density statement, as is the tree-energy condition
`(k+1)H_k/2^(2k) -> 0`. No Rule 30 estimate establishing either condition was
found. The Walsh code retains overlaps; it does not use independence.

The measure-theoretic route is explicitly excluded. Hedlund balance gives
an exactly one-half single-site marginal at each time under the uniform
Bernoulli ensemble, while the lone seed is a single measure-zero orbit.
This marginal statement alone is not an almost-everywhere time-average
theorem. No transfer from the ensemble to the seed is made.

## Ladder reached and remaining gap

**Correction: no rung of the requested ladder was reached.** Rung 2 asks
for a proof that `k W_k/2^k -> 0`; reproducing the existing implication
from that unproved condition to P2 does not reach it. The measurements
establish no asymptotic claim. Rungs 1 through 5 remain unproved here.

The permitted Christol pivot was inspected through the repository's Topal
refutation. Its implication chain is sound, but no proof that the actual
Rule-30 centre sequence is non-2-automatic was obtained here; the published
Topal computation confuses Frobenius dilation with Cartier decimation. Thus
that pivot yields no completed result in this run. Rule 90 controls are not
used as evidence for the seed estimate: its centre is eventually zero and
serves only as a control against rule-generic reasoning.

Scope: all displayed support, Walsh, and energy numbers are finite exact
computations. They establish neither a limit nor a liminf/limsup statement.

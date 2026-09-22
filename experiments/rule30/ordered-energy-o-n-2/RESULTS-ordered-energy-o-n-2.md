# The seed's dyadic tree energy to k=28 sits at the random-sign scale

Status: **computed over shells `k = 8..28`. No ladder statement changed;
"Ordered energy o(N^2)" stays conjectured.** The per-level energies were not
new: `experiments/rule30/p2-cross-science-explore.json` has stored every
`E_(k,j)` for `k <= 28` since at least 2026-09-17, and the fixed-window work
reads them. What was never written down is `H_k` itself past `k = 20` and the
three facts in §2. What this run adds beyond tabulation is a second code path:
it re-derives those stored arrays from the payload and agrees exactly at every
`k = 8..28`, where they had been independently cross-checked only through
`k = 12`. The first version of this document claimed to extend a table the
repository already held; that claim is withdrawn.

## 1. What is measured and why it is the right quantity

`E_(k,j)` is the sum of squared aligned block sums of length `2^j` over shell
`k`, and `H_k = sum_(j<=k) E_(k,j)`. `H_k/N^2 -> 0` is equivalent to P2
(`f0855dca62da0be9`), and `M_k^2 <= (k+1) H_k` is proved (`861b69c6da1d2689`),
so a bound on `H_k` is a bound on the shell maximum. The node's success
criterion is any `H_k = O(N^(2-eps))`.

**Control.** The published `H_k` at `k = 8, 10, 12, 14, 16, 18, 20`
(`RESULTS-p2-time-index-walsh.md:256-264`) reappear exactly as integers, from
this code over the same payload, and the sum of the stored `E` arrays in
`p2-cross-science-explore.json` equals this run's `H_k` at every `k = 8..28`.
That second agreement is independent of the stored code but not of the payload:
both read the same `10^9`-bit cache, which is itself verified against a
regenerated centre column only on its first 8192 bits, re-derived here on every
run.

The shell is read in chunks of `2^22` bits. Every aligned block no longer than a
chunk lies inside one, so its square is accumulated there and only the chunk
totals are folded for longer blocks. Exact integer arithmetic; memory stays
near one chunk at every `k`, which is what makes `k = 28` cost 1.8 s rather
than the 2 GB the unchunked fold needs.

## 2. Result

| `k` | `H_k` | `H_k/((k+1)N)` | `H_k/N^2` | `max_j E/N^2` | `argmax j` |
|---:|---:|---:|---:|---:|---:|
| 8 | 1,768 | 0.7674 | 0.02698 | 0.004456 | 2 |
| 9 | 8,840 | 1.7266 | 0.03372 | 0.01031 | 9 |
| 10 | 10,256 | 0.9105 | 0.009781 | 0.001221 | 5 |
| 11 | 16,560 | 0.6738 | 0.003948 | 0.0004883 | 0 |
| 12 | 54,856 | 1.0302 | 0.00327 | 0.0003242 | 7 |
| 13 | 162,796 | 1.4195 | 0.002426 | 0.0003534 | 13 |
| 14 | 291,952 | 1.188 | 0.001088 | 0.0001955 | 13 |
| 15 | 441,968 | 0.843 | 0.0004116 | 3.263e-05 | 8 |
| 16 | 1,230,080 | 1.1041 | 0.0002864 | 2.951e-05 | 15 |
| 17 | 3,542,192 | 1.5014 | 0.0002062 | 3.469e-05 | 17 |
| 18 | 3,907,312 | 0.7845 | 5.686e-05 | 3.875e-06 | 11 |
| 19 | 9,135,532 | 0.8712 | 3.323e-05 | 2.047e-06 | 12 |
| 20 | 23,676,184 | 1.0752 | 2.153e-05 | 1.552e-06 | 16 |
| 21 | 36,929,140 | 0.8004 | 8.397e-06 | 4.777e-07 | 2 |
| 22 | 94,700,640 | 0.9817 | 5.383e-06 | 3.076e-07 | 18 |
| 23 | 266,135,284 | 1.3219 | 3.782e-06 | 6.127e-07 | 23 |
| 24 | 419,260,944 | 0.9996 | 1.49e-06 | 7.305e-08 | 23 |
| 25 | 942,367,060 | 1.0802 | 8.37e-07 | 5.137e-08 | 24 |
| 26 | 2,297,383,448 | 1.2679 | 5.101e-07 | 4.732e-08 | 26 |
| 27 | 3,639,099,780 | 0.9683 | 2.02e-07 | 8.988e-09 | 26 |
| 28 | 7,330,540,080 | 0.9417 | 1.017e-07 | 4.16e-09 | 25 |

Three exact facts over this range:

- **`H_k/((k+1)N)` stays in `[0.674, 1.727]`**, minimum at `k = 11` and maximum
  at `k = 9`. `(k+1)N` is the expected value of `H_k` for independent fair
  signs, so the seed's dyadic energy sits at the random-sign scale, a factor of
  about `N/log N` below the `o(N^2)` threshold the node needs. At `k = 28` that
  factor is `H_k/N^2 = 1.017e-7`.
- **`H_k/N^2` strictly decreases at every step from `k = 9` to `k = 28`.** The
  only non-decrease in range is `k = 8 -> 9`.
- **The whole-shell block dominates exactly at `k = 9, 13, 17, 23, 26`**, where
  `argmax j = k` and so `max E = E_(k,k) = D_k^2`. Those are the shells with the
  largest signed sums relative to `N`; `k = 17` is the shell that sets the
  shell-maximum frontier and `k = 23` carries the largest `|D_k|` in range, 6566.

## 3. What it does not buy

The data sits comfortably inside the success criterion at every `k` measured,
and that is exactly why it proves nothing: the criterion is asymptotic, and a
bound `H_k = O(N^(2-eps))` is a statement about every `k`, which no finite table
reaches. Staying at the random-sign scale through `k = 28` is the behaviour a
proof would have to explain, not evidence that one exists. The band's width is
itself informative in the other direction: `H_k/((k+1)N)` moves by a factor of
2.6 across the range with no trend, so there is no fitted constant here to
quote, and none is quoted.

Complete shells stop at `k = 28` because the only centre-column cache holds
`10^9` bits; `k = 29` needs `2^30`.

## 4. Files

`dyadic_energy.py` (`dyadic_energy.log`). It re-verifies the payload alignment,
asserts the seven published controls, and writes no tracked artifact. Logs are
hidden by the global ignore; `git add -f` to commit them.

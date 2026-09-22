# The aligned-block profile of the Rule 30 shells matches the exact random-walk law, and the half-seam coupling changes sign

Date 2026-09-20. Pre-registration `PREREGISTRATION-aligned-block-seam.md`,
written before `seam_profile.py` existed, with the screen bands calibrated
against the iid control before any Rule 30 number was read. Script
`seam_profile.py`, record `seam-profile.json`, log `seam-profile.log`. Source is
the same 10^9-bit centre column `shell_screen.py` reads, with the same 29-bit
witness check. Neither screen proves or refutes P2.

## 0. What was not already recorded

`RESULTS-shell-maximum-o-n.md` records `M_k`, `D_k` and `I_k` exactly for the
complete shells `k = 10..28`. Three quantities the route-1 reduction needs were
recorded at no `k` anywhere in the repository: the prefix area `A`, the
decomposition of a shell's integrated energy at its half boundary, and the
aligned-block profile

```text
L(K, j) = sum over the 2^(K-j) aligned blocks B of length 2^j in shell K of |D(B)|
```

which record `r30-p2-route1-reduces-to-adjacent-block-cross-term` shows route 1
must control. `shell_stats` returns `length, M, u_star, D, I` and no area;
`p2_dyadic_shell_probe.py` has the exact four-coordinate law but its
`ShellRecord` carries no area field and its `main()` stops at `--max-k 18`.

## 1. Control on the measurement itself

`seam_profile.py` is an independent second implementation: it accumulates
`(n, D, A, I)` by the four-coordinate law over 2^24-bit chunks rather than by
`shell_screen.py`'s inline carry. It reproduces the recorded `M`, `u_star`, `D`
and `I` exactly at every complete shell `k = 10..28`, and aborts on the first
mismatch. It also re-checks the law itself exhaustively over all 3969 pairs of
signed words of lengths 0..5 before using it, and asserts at every `k` that the
two half summaries compose to the whole shell and that `I_u + X_k + I_v = I_(k+1)`.

## 2. Aligned-block profile (screen S1)

Normalizing by the exact mean absolute displacement of a simple random walk of
`n = 2^j` steps, `m_j = n C(n, n/2) / 2^n`, put `r(K, j) = L(K, j) / (2^(K-j) m_j)`.

At `K = 28`:

| `j` | blocks | `r(28, j)` | `L/2^28` |
|---:|---:|---:|---:|
| 0 | 268435456 | 1.0000 | 1.000000 |
| 4 | 16777216 | 1.0002 | 0.196418 |
| 8 | 1048576 | 1.0001 | 0.049824 |
| 12 | 65536 | 1.0026 | 0.012498 |
| 16 | 4096 | 0.9984 | 0.003112 |
| 20 | 256 | 1.0172 | 0.000793 |
| 24 | 16 | 1.0366 | 0.000202 |
| 28 | 1 | 0.0838 | 0.000004 |

`r(K, 0) = 1` identically and is structural, not a measurement: `L(K, 0) = 2^K`
and `m_0 = 1`. The screen therefore excludes `j = 0` and does not count it. This
is a reporting correction, not a narrowing of the registered screen: `|r - 1|`
is exactly 0 there, so no `j = 0` entry could ever have fired the kill or moved
the maximum. The first run counted the 19 structural entries, one per shell, and
reported 155 pairs where 136 were measurements; the control counts fall from 93
to 78 the same way. No verdict and no maximum changes.

Over the registered range, every `K = 10..28` and every `1 <= j <= K - 12` (at
least 4096 blocks), 136 pairs: **`max |r - 1| = 0.0225`, so S1 is not refuted.**
The iid control over the same construction gives 0.0196 over 78 pairs. The deviation shrinks with
block count exactly as sampling predicts: at `j = 4`, `r` is 1.0741 at `K = 10`
and 1.0002 at `K = 28`.

The consequence for route 1: on the measured shells
`L(K, j)/2^K = m_j 2^(-j) r(K, j)`, which is `sqrt(2/(pi 2^j))` to within 2.3%.
The triangle-inequality branch needs `L(K, j) = o(2^K)`, and the measured
profile satisfies that for any `j` growing with `K`. **The data does not kill
that branch.**

## 3. Half-seam decomposition (screen S2)

For the halves `u`, `v` of shell `k+1`, `X_k = I_(k+1) - I_u - I_v
= 2^k D_u^2 + 2 D_u A_v`. The first summand depends on `u` alone, so the only
genuine coupling between the halves is `Y_k = 2 D_u A_v`.

The sign of `Y_k` over `k = 10..28` is

```text
- + - + - - 0 + - + - - + + - - - - -
```

**not constant, so S2 is not refuted.** The zero at `k = 16` is exact and not a
rounding artefact: the first half of shell 16, `t` in `[65536, 98304)`, has
signed sum exactly `D_u = 0`, verified by a direct independent read of the same
bits. The second half has `-356`, which is `D_16`.

`s_k = X_k / I_(k+1)` runs from `-0.737` (`k = 12`) to `+0.828` (`k = 22`) and
`a_k = A_k / 2^(3k/2)` from `-0.464` to `+1.042`. Both are reported without a
screen: the iid control shows neither concentrates, and a band on either would
fire on the null (pre-registration section 5).

## 4. Controls

| control | S1 `max \|r-1\|` | S1 | S2 signs | S2 |
|---|---:|---|---|---|
| centre column | 0.0225 | not refuted | `{-1, 0, +1}` | not refuted |
| iid `+-1` | 0.0196 | not refuted | `{-1, +1}` | not refuted |
| all-ones | 79.2170 | **refuted** | `{+1}` | **refuted** |
| iid `P(+1) = 1/2 + 1/k` | 5.6663 | **refuted** | `{+1}` | **refuted** |

The all-ones control is the one the concatenation law cannot distinguish from
any other signed word, and it fails both screens, so neither screen is an
identity in disguise. The biased control fails S1 by a factor of 57 over the
band, which fixes what S1 measures: **it is a bias screen at the aligned-block
level.** The centre column passing it says the shells carry no block-level bias
through `K = 28`; it does not say anything about P2, which the biased control
satisfies while failing S1.

## 5. What changed

- **Proved (exhaustive over the stated range, machine-checked):** `A_k` for
  `k = 10..28`; the half-seam decomposition of `I_(k+1)` for `k+1 = 11..28`;
  `L(K, j)` for `K = 10..28` and all `j`. `D_u = 0` exactly for the first half
  of shell 16.
- **Not refuted, over `k = 10..28` only:** S1, the aligned-block square-root law
  at every depth with at least 4096 blocks; S2, the sign of the half-seam
  coupling is not constant.
- **Open, unchanged:** P2, and the shell-maximum ladder statement `M_k = o(2^k)`.
  Nothing here bounds `M_k`. The triangle-inequality branch of route 1 survives
  the data rather than being supported by it: a finite profile satisfying
  `L = o(2^K)` at each measured `K` is not the uniform statement that branch
  needs, and section 6.1 of the cross-review holds regardless that the only
  place Rule 30 can enter route 1 is an estimate of the cross term, which is
  not produced here.

## 6. Reproduction

From this directory:

```sh
uv run --no-project --script seam_profile.py --kmax 28 --out seam-profile.json
```

Measured with `/usr/bin/time -l` on two runs: 10.74 s and 9.53 s real, peak
resident 2,116,304,896 and 2,121,973,760 bytes. Both runs produce identical
`seam-profile.json`, controls included, since every control is seeded from
`SEED = 20260920`.
`--no-controls` skips the three control passes. `*.log` is globally gitignored,
so committing `seam-profile.log` needs `git add -f`.

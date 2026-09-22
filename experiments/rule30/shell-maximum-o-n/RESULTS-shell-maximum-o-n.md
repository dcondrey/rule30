# Shell maximum o(N): criterion, finite screens, controls

Ladder statement: 'Shell maximum o(N)' (P2). Status on entry: conjectured.

## 0. Pre-registration (written 2026-09-19 before any screen ran)

### 0.1 What cannot be a success criterion

`M_k = o(2^k)` is an asymptotic statement. No finite computation proves it,
and no finite computation refutes it: any finite list of values
`M_12..M_28` is consistent both with `M_k/2^k -> 0` and with
`limsup M_k/2^k > 0`. Its status stays **conjectured** whatever runs here.

### 0.2 Success criterion at the finite level

The criterion is split into falsifiable screens `H`. Each has the form
"for every `k >= k0`, `M_k <= B(2^k)`" with `B(N) = o(N)`, so each `H`,
if true for all `k`, proves the ladder statement and hence P2. Each is
killed by one shell `k` in the checked range with `M_k > B(2^k)`, where
the witness is the prefix length `u*` attaining the maximum and anyone can
re-add the `u*` signed bits.

| id | bound `B(N)` | kill fires if |
|---|---|---|
| H1 | `1.0 sqrt(N)` | some `k in [10,28]` has `M_k > sqrt(N)` |
| H2 | `2.0 sqrt(N)` | same with `2 sqrt(N)` |
| H3 | `3.0 sqrt(N)` | same with `3 sqrt(N)` |
| H4 | `sqrt(2 N ln ln N)` (LIL envelope) | same |
| H5 | `N^(3/4)` | same |
| H6 | `I_k <= N^(5/2)` (energy form, weakest) | same with `I_k` |

Range: `k = 10..28` complete shells, plus the partial shell `k=29` truncated
at the end of the 10^9-bit external cache (a partial maximum is a LOWER
bound on `M_29`, so it can kill an upper-bound screen but never support one).

A surviving screen means only "not refuted on `k <= 28`". Nothing is
extrapolated past the range.

### 0.3 Null-model screen (validation, not P2 progress)

H7: the normalized shell maxima `M_k/sqrt(2^k)`, `k=10..28`, are a sample
from the law of `max_{0<=s<=1}|W(s)|` for standard Brownian motion (the
large-`N` limit for an iid fair +-1 walk). Kill: one-sample KS p < 0.01.
Pseudorandomness of the centre column is long known empirically, so a
survival is validation; a kill would be a finding.

### 0.4 Controls (each must behave as stated, or the pipeline is broken)

| control | expected |
|---|---|
| all-zero Rule 30 fixed point (`x_t = -1`) | `M_k = N` exactly; H1..H6 all killed |
| Rule 90 single seed centre | `M_k = N` exactly if the centre is 0 for all `t >= 1`; H1..H6 killed |
| shell-balanced sawtooth (`+1` for `N/2`, `-1` for `N/2` per shell) | every shell endpoint sum 0, yet `M_k = N/2`; H1..H6 killed. Shows endpoint densities are insufficient |
| iid fair +-1, seed 0 | H1..H5 behave as a random walk would; H7 survives |
| iid with `P(+1) = 1/2 + 1/k` in shell `k` | `M_k ~ 2N/k = o(N)` (P2-type statement TRUE) yet H1..H4 killed: the screens are sufficient, not necessary |

### 0.5 Data provenance (reproduced, not inherited)

Three independent sources, compared bit-for-bit on every overlap before
any number is used:

1. `center_sim.c` (this directory): new light-cone-trimmed bit-parallel
   simulator, 2^23 bits, itself checked against
   `experiments/rule30/center_column.py`.
2. The repository band cache
   `experiments/overnight-arms/frontier_attack/a25_checkerboard_growth_extended/cache/band30_T33554432.bin`,
   bit 15 of each little-endian uint32 row, 2^25 bits.
3. The Wolfram Data Repository file
   `experiments/overnight-arms/frontier_attack/a20_deep_simulation/ref/wdr_billion.bin`,
   payload offset 239, MSB-first, 10^9 bits.

## 1. Result

Status: **NEITHER PROVED NOR REFUTED. The ladder statement stays conjectured.**
Run: `cc -O3 -march=native -o center_sim center_sim.c && ./center_sim 8388608 center.bin`
(about 4 minutes), then `uv run --with numpy python shell_screen.py --sim center.bin`,
log `shell-screen.log`, full integers in `shell-screen.json`. Omitting `--sim`
rewrites `shell-screen.json` without the `center_sim` cross-check.

### 1.1 Sources agree

All three sources agree on every overlapping bit: the WDR file against the
band cache on 2^25 bits (0 mismatches), against `center_column.py` on 2^16
bits (0), and against the new `center_sim.c` on 2^23 bits (0). The WDR
bytes holding the first 2^29 bits (complete shells `k <= 28`) hash to
`c46e9665...ece`, identical to `used_payload_sha256` in
`experiments/rule30/dyadic-lag-drift.json`. The first 29 bits match the
A051023 witness.

### 1.2 Shell integers, `k = 10..28` (computed, exact)

`u*/N` is where the first maximum sits; `D = S_k(N)` is the shell endpoint sum.

| `k` | `M_k` | `u*/N` | `D_k` | `M_k/N` | `M_k/sqrt(N)` | `I_k/N^2` |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 36 | 0.428 | 0 | 3.52e-2 | 1.125 | 0.242 |
| 11 | 25 | 0.360 | 4 | 1.22e-2 | 0.552 | 0.064 |
| 12 | 65 | 0.986 | 56 | 1.59e-2 | 1.016 | 0.100 |
| 13 | 183 | 0.883 | 154 | 2.23e-2 | 2.022 | 0.964 |
| 14 | 249 | 0.525 | 112 | 1.52e-2 | 1.945 | 1.248 |
| 15 | 180 | 0.238 | -64 | 5.49e-3 | 0.994 | 0.249 |
| 16 | 367 | 0.976 | -356 | 5.60e-3 | 1.434 | 0.437 |
| 17 | 889 | 0.927 | 772 | 6.78e-3 | 2.456 | 1.375 |
| 18 | 330 | 0.578 | 104 | 1.26e-3 | 0.645 | 0.084 |
| 19 | 1006 | 0.840 | 638 | 1.92e-3 | 1.389 | 0.473 |
| 20 | 1198 | 0.618 | -152 | 1.14e-3 | 1.170 | 0.325 |
| 21 | 940 | 0.305 | 194 | 4.48e-4 | 0.649 | 0.060 |
| 22 | 3049 | 0.903 | 2268 | 7.27e-4 | 1.489 | 0.715 |
| 23 | 6654 | 1.000 | 6566 | 7.93e-4 | 2.297 | 1.455 |
| 24 | 5288 | 0.825 | 3872 | 3.15e-4 | 1.291 | 0.556 |
| 25 | 6374 | 0.998 | -6082 | 1.90e-4 | 1.100 | 0.113 |
| 26 | 14660 | 1.000 | 14598 | 2.18e-4 | 1.790 | 0.973 |
| 27 | 14700 | 0.945 | -12486 | 1.10e-4 | 1.269 | 0.223 |
| 28 | 8303 | 0.514 | 1096 | 3.09e-5 | 0.507 | 0.047 |
| 29 (partial, first 463,129,088 of 2^29) | >= 44301 | | | >= 8.25e-5 | >= 1.912 | |

Rows 12..24 reproduce the cross-review's `M_k` and `I_k` tables exactly.
Rows 25..28 and the partial row 29 are new. On every complete shell the
deterministic inequalities `M^3/8 <= I_k <= N M^2` hold (asserted in the run).

### 1.3 Screens

| id | bound | verdict on `k = 10..28` (+ partial 29) | witness |
|---|---|---|---|
| H1 | `sqrt(N)` | **refuted** | first at `k=10`: `M=36 > 32`; 14 complete shells plus partial 29 (the JSON's 15 `killing_k` entries) |
| H2 | `2 sqrt(N)` | **refuted** | `k=13` (`183 > 181.0`), `k=17` (`889 > 724.1`), `k=23` (`6654 > 5792.6`) |
| H3 | `3 sqrt(N)` | not refuted | largest ratio `2.456` at `k=17` |
| H4 | `sqrt(2 N ln ln N)` | **refuted** | `k=17`: `889 > 804.1` |
| H5 | `N^(3/4)` | not refuted | |
| H6 | `I_k <= N^(5/2)` | not refuted | largest `I_k/N^2 = 1.455` at `k=23` |
| H7 | Brownian `sup|W|` law, KS | not refuted (validation) | `n=19`, `D=0.155`, `p=0.71` |

Refuted means: that uniform bound is false on the actual orbit, so no proof
of P2 can go through it. The smallest constant `C` with `M_k <= C sqrt(2^k)`
on every complete shell `k = 10..28` is `889/sqrt(2^17) = 2.4555`, and the
partial `k=29` shell does not raise it. Any proposed `C sqrt(N)` law with
`C < 2.4555` that is claimed from any `k0 <= 17` on, and the plain LIL envelope, is dead on recorded data.

H3, H5, H6 surviving is not evidence for P2 beyond `k = 28`. H7 surviving says
only that 19 normalized shell maxima look like Brownian `sup|W|` draws, which
is what pseudorandomness predicts; it is not a finding.

### 1.4 Controls

| control | range | observed | screens killed |
|---|---|---|---|
| all-zero Rule 30 fixed point | `k = 10..24` | `M_k/N = 1` | H1..H6 |
| Rule 90 single-seed centre | `k = 10..12` | 0 ones at `t >= 1` in 8192 steps, `M_k/N = 1` | H1..H6 |
| shell-balanced sawtooth | `k = 10..24` | endpoint sums 0, `M_k/N = 1/2` | H1..H6 |
| iid fair, seed 0 | `k = 10..24` | `M_24/N = 2e-4` | H1 only |
| iid `P(+1) = 1/2 + 1/k` | `k = 10..24` | `M_24/N = 0.083` (about `2/k`) | H1..H6 |

Each control behaved as registered, so the pipeline does detect linear
shell maxima. The last control has `M_k = o(N)` (true P2-type
statement) and still kills every screen: the screens are sufficient, not
necessary, and a refuted screen says nothing against P2 itself. The sawtooth
confirms the scope note that endpoint densities alone are insufficient.
The registration under-predicted this control: it said "H1..H4 killed", and
H5 and H6 die too, because at `k=24` the observed `M_24/N = 0.083` exceeds
`N^(-1/4) = 0.0055` by about 15x.

## 2. What changed

- **Proved:** nothing new. The equivalence to P2 is the cross-review's
  analytical lemma; this run machine-checks only its two finite
  inequalities on the 19 real shells.
- **Refuted (finite, exact witnesses):** H1, H2, H4. Any uniform bound
  `M_k <= C sqrt(2^k)` with `C < 2.4555`, and `M_k <= sqrt(2 N ln ln N)`,
  are false on the single-seed orbit.
- **Computed:** `M_k`, `I_k`, `D_k`, `u*` for `k = 10..28` from three
  agreeing sources; `M_29 >= 44301`.
- **Open:** `M_k = o(2^k)` itself, and the weaker candidate laws H3, H5, H6.
- **Ladder statement 'Shell maximum o(N)':** unchanged, conjectured. The
  data can now also reject any proposed proof whose bound is below the
  recorded `k = 17` value.

## 2a. Rejection frontier (computed, `frontier.py` -> `frontier.json`)

For each start shell `k0`, the smallest constant that a bound claimed "for
all `k >= k0`" must carry to survive the recorded shells. Below the frontier
the bound is refuted, with the named shell as the exact witness. At or above
it the bound is only not refuted. Rows for `M` include the partial shell 29,
which is valid because its value is a lower bound on `M_29`; the energy column
uses complete shells only.

| `k0` | `M_k <= C sqrt(N)` needs `C >=` | `M_k <= c sqrt(2N ln ln N)` needs `c >=` | `M_k <= N^alpha` needs `alpha >=` | `I_k <= C N^2` needs `C >=` |
|---:|---:|---:|---:|---:|
| 10..13 | 2.4555 (k=17) | 1.1055 (k=17) | 0.5781 (k=13) | 1.4549 (k=23) |
| 14..17 | 2.4555 (k=17) | 1.1055 (k=17) | 0.5762 (k=17) | 1.4549 (k=23) |
| 18..23 | 2.2974 (k=23) | 0.9763 (k=23) | 0.5522 (k=23) | 1.4549 (k=23) |
| 24..26 | 1.9120 (k=29 partial) | 0.7805 (k=29 partial) | 0.5323 (k=26) | 0.9728 (k=26) |
| 27..29 | 1.9120 (k=29 partial) | 0.7805 (k=29 partial) | 0.5322 (k=29 partial) | 0.2232 (k=27), 0.0470 (k=28) |

Use: a proposed proof step that yields, say, `M_k <= N^0.55` from `k=10` on,
or `M_k <= 2 sqrt(N)` from any `k0 <= 23`, is false on the orbit and can be
rejected by re-adding the witness shell's signed bits. Frontier values for
`k0 >= 24` rest on at most five shells and say little. None of these numbers
is an asymptotic estimate: the frontier shows what the data rejects, not what
holds past `k = 28`.

## 3. Files

- `center_sim.c`: independent light-cone-trimmed simulator (2^23 bits in the check).
- `shell_screen.py`: cross-check, screens, KS, controls.
- `frontier.py`, `frontier.json`, `frontier.txt`: rejection frontier from `shell-screen.json`.
- `shell-screen.json`: the run (all integers). `shell-screen.log` is the console copy; `*.log` is globally gitignored, so a commit needs `git add -f`.

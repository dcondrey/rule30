# The period-two left obligation as a forward boundary-observer problem, and its exact census to width 18

Date: 2026-09-16. Script `forward-boundary/forward_boundary_census.py`, log
`forward_boundary_census_w2-18.log`. No pre-registration; first run of a new
formulation.

**`[C]` With the centre column pinned to `s(t,0) = t mod 2`, the left
half-plane is Rule 30 on the half-line `i <= -1` run forward from its row at
time 0 with that boundary, and the period-two hypothesis restricted to the
left side is one sentence: the two rightmost cells differ at every even time,
`s(2k,-2) != s(2k,-1)` for all `k` (equivalently, column `-1` is 1 at every
odd time). `(PT2)` follows if no finite word satisfies it forever; the right
half-plane only adds that the even-time column-1 word is hard-core. Over all
`2^(w-1)` words of width `w` (leftmost cell 1), the number surviving `k` even
steps is exactly `2^(w-1-k)` for `k <= floor((w-2)/2)`, one bit of the seed
per even step, and then decays slowly: the maximum number of even steps
survived is `M(w) = 8, 7, 8, 7, 14, 11, 13, 15, 12, 15, 16` at `w = 8..18`,
between `w - 4` and `w + 2`, so the free-running phase after the controllable
one lasts 7 to 9 even steps on this range. A period-two counterexample needs
`M = infinity`. The forward map is exactly two-to-one on the full sequence
space; restricted to finite-width rows the in-degree is 0, 1, or 2 (correction,
2026-09-17, `r-structure/theory-s3/refute-backward-tree.md`), the two backward
choices differing only in the boundary-adjacent cell but not both always
closing to a finite width (see section 1 below). Nothing here
proves anything; it states the obligation without the reconstruction, the
four-state alphabet, the cut or the forcing, and gives it an exact census
instrument that reaches width 18 in seconds.**

## 1. Derivation

At the centre, `c_(t+1) = l_t XOR (c_t OR r_t)` with `l_t = s(t,-1)`,
`r_t = s(t,1)`. With `c_t = t mod 2`: at odd `t`, `0 = l_t XOR 1`, so
`l_t = 1`; at even `t`, `1 = l_t XOR r_t`, which defines `r_t = 1 - l_t` and
constrains nothing on the left. The left half-line's own rule at `i = -1`
gives `l_(2k+1) = s(2k,-2) XOR (l_(2k) OR 0)`, so `l_(2k+1) = 1` iff
`s(2k,-2) != s(2k,-1)`. The left half-plane evolves autonomously given the
boundary column, so the condition is a property of the initial left word
alone. Conversely a left word satisfying it forever, together with a finite
right word whose even-time column 1 equals `1 - l_(2k)`, is a period-two
counterexample; `BWH+` (capsule section 2) is the statement that the left
condition alone already fails at every scale.

Two-to-one: given row `t+1` on `i <= -1` and the boundary, choosing
`l_t = s(t,-1)` determines `s(t,-2) = s(t+1,-1) XOR (l_t OR c_t)`, then
`s(t,-3)` from `s(t+1,-2)`, and so on leftward; both choices give a preimage
(possibly infinite). This is the left-permutivity of Rule 30 read backwards.

## 2. Census

`N_w(k)` is the number of width-`w` words surviving `k` even steps.

| `w` | words | `M(w)` | first argmax | `N_w(k)`, `k = 0, 1, ...` |
|---|---|---|---|---|
| 8 | 128 | 8 | `10000001` | 64 32 16 5 3 1 1 1 0 |
| 9 | 256 | 7 | `100010101` | 128 64 32 16 10 10 8 0 |
| 10 | 512 | 8 | `1101111010` | 256 128 64 32 19 8 8 2 0 |
| 11 | 1,024 | 7 | `11110101010` | 512 256 128 64 32 20 2 0 |
| 12 | 2,048 | 14 | `110100010101` | 1024 512 256 128 64 25 10 8 6 6 6 3 3 3 0 |
| 13 | 4,096 | 11 | `1000010000001` | 2048 1024 512 256 128 64 22 13 3 3 1 0 |
| 14 | 8,192 | 13 | `11011100100101` | 4096 2048 1024 512 256 128 77 45 24 14 4 2 2 0 |
| 15 | 16,384 | 15 | `110101001101010` | 8192 4096 2048 1024 512 256 128 70 30 22 13 9 6 6 6 0 |
| 16 | 32,768 | 12 | `1000000100010101` | 16384 8192 4096 2048 1024 512 256 117 65 22 14 10 0 |
| 17 | 65,536 | 15 | `10100000010000001` | 32768 ... 256 147 94 52 27 ... 0 |
| 18 | 131,072 | 16 | `100010011000010101` | 65536 ... 512 237 144 83 ... 0 |

The exact halving `N_w(k) = 2^(w-1-k)` holds while the seed bit at position
`-(2k+1)` or `-(2k+2)` is still arriving at the boundary (the leftmost cells
reach column `-1` at speed one, and left-permutivity makes the observer's
bit an affine function of the newest arriving seed bit); it stops at
`k = floor((w-2)/2)`, after which the word is free-running. The full logs
carry every `N_w(k)`.

## 2b. Survivor-only branching to width 30

`forward_survivor_census.py` (log `forward_survivor_census_w2-30.log`)
builds level `L` (even) as the set of partial seeds on positions `-L..-1`
satisfying `(L1)` at steps `0 .. L/2 - 1`, by extending level `L - 2` with
two bits and filtering. At every level exactly half of the four-fold
extension survives (asserted through `L = 30`): the condition at step `k`
depends on positions `-(2k+2)..-1` and, by left-permutivity along the
diagonal, is affine with coefficient 1 in the bit at `-(2k+2)`, so that bit
is forced by the ones to its right. Width-`w` words are the level-`L` seeds
with leftmost 1 at `-w` (`L = w` rounded up to even), run on as finite seeds.

| `w` | words past the controllable phase | `M(w)` | free-phase profile | first argmax |
|---|---|---|---|---|
| 12 | 25 | 13 | 25 10 8 6 6 6 3 3 3 0 | `110100010101` |
| 16 | 117 | 11 | 117 65 22 14 10 0 | `1000000100010101` |
| 20 | 455 | 17 | 455 253 144 105 67 50 29 15 15 0 | `11010001010101000001` |
| 24 | 1,993 | 19 | 1993 1056 529 320 202 97 54 40 4 0 | `101001001011011000010101` |
| 26 | 4,067 | 20 | 4067 2057 1071 517 258 154 40 4 2 0 | `11100110110110011001101010` |
| 28 | 8,075 | 22 | 8075 4010 1939 937 425 160 95 69 14 6 0 | `1100000011100001010101000001` |
| 30 | 16,485 | 25 | 16485 8266 4004 1959 961 415 162 62 28 8 4 4 0 | `100001011001011001001101111010` |

`M(w)` for `w = 12..30`: 13, 10, 12, 14, 11, 14, 15, 13, 17, 16, 19, 20, 19,
19, 20, 20, 22, 23, 25 (`M` here counts even steps from time 0 and is one
less than the full census's count, which included step 0). The free phase
after the controllable one halves the survivors per even step for about
`log2` of their number, then flattens into plateaus of 2 to 6 words; its
maximum length grows from 8 at `w = 12` to 11 at `w = 30`. So even after the
whole seed has arrived, the boundary observer behaves like a fresh coin for
several steps, and the structured survivors appear only in the last few.
Cost: `2^(w/2)` seeds per width; width 40 is about a million.

## 3. Reading

This is the archive's period-two left obligation with nothing added and
nothing reconstructed: `(L1)` forever for some finite word is equivalent to a
counterexample's left half. Its census is the forward twin of the
constant-cut run `D_n(c)`: the controllable phase is exactly one bit per even
step, and the free-running tail is what the proof must bound. On `w <= 18`
the tail is 7 to 9 even steps, with survivor plateaus (`6, 6, 6`; `3, 3, 3`)
that are the structured survivors seen everywhere else. The instrument
scales: only `2^(w-1-k)` words survive the controllable phase, so a search
that branches only on survivors reaches widths in the forties with the
same cost as this census at 18. What the formulation invites that the
cascade does not: the map on finite rows is a two-to-one expanding system
and the condition is a cylinder condition on its orbit; the question is
whether any finite (eventually zero) initial row has an orbit that stays in
the cylinder, which is the shape of a "rational point in a Cantor set"
question for a specific expanding map. `RW`, `SEP`, `PT2` untouched.

Later the same day: the halving is proved (`RESULTS-FORWARD-HALVING-LEMMA.md`), and the
dictionary `RESULTS-FORWARD-ENDPOINT-DICTIONARY.md` shows the `(L1)`-only statistic here is
not the `(PT2)` one: the argmax seeds have `11` in `rho` at most widths, and the hard-core
census (`RESULTS-FORWARD-SURVIVOR-W40.md`, Table 2) is the archive's `D_n(c)` up to one scale
and two steps.

## 4. Reproduction

```sh
uv run --no-project --with numpy python forward-boundary/forward_boundary_census.py 18    # 20 s
```

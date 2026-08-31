# Arm 9: factor complexity, pre-registered before running

Follows the literature search this session ran against Question A (Rule 30
Prize Problem 1, non-periodicity of the center column, OEIS A051023).
Allouche-Shallit-Yassawi, arXiv:2104.13072, catalog every published
non-automaticity technique; ARM6 already ran the kernel-finiteness test
(Theorem 1 in their survey) to depth 12 with no small-kernel collapse. Their
Theorem 17 (Cobham) is the one technique in that survey that requires no
algebraic or substitutive presentation of the sequence and has not been run
against A051023 anywhere in the literature or this project: a k-automatic
sequence has factor complexity `p(n) = O(n)`. Eventual periodicity implies
automaticity for every base, so a proof that `p(n)` is NOT `O(n)` would prove
non-automaticity, which would prove non-periodicity (Problem 1). This is
cheaper to test than a transcendence proof and distinct from the kernel
search.

## 1. Exact target

`p(n)` = the number of distinct length-`n` substrings (factors) occurring in
the center column `A051023`. Computed exactly (not sampled) via a suffix
automaton over the generated prefix, using the standard fact that each SAM
state represents a contiguous range of substring lengths
`(len(link(state)), len(state)]`, all with the same right-extension set, so
summing "which states' ranges cover `n`" over all `n` gives `p(n)` for every
`n` from 1 to the prefix length in one linear pass (difference array over
state length-ranges, then prefix sum). No sampling, no truncated window.

## 2. Positive control

Thue-Morse (2-automatic, `t(n) = parity of popcount(n)`) run through the
identical pipeline. Its factor complexity is known in closed form (Brlek
1989; de Luca-Varricchio) and is linear: `p(1)=2`, and for `n>=2`,
`p(n) = 3*2^r + 4s - 2` where `n - 1 = 2^r + s`, `0 <= s < 2^r` (there are
different equivalent normalizations in the literature; this project does not
take Brlek's formula on trust -- it is checked against this project's own
brute-force count below, not asserted from memory). Control passes iff the
SAM-computed `p(n)/n` ratio for Thue-Morse stays bounded (does not set new
highs) across the measured range, matching Cobham's theorem for a sequence
already known to be automatic.

## 3. Correctness gate on the SAM implementation itself

Before trusting the SAM output on either sequence: brute-force count of
distinct length-`n` substrings via a Python `set` on the first `N<=2000`
bits, cross-checked against the SAM's `p(n)` for every `n<=N`, both
sequences, zero mismatches required. This is the earned test -- it verifies
non-obvious correctness of a from-scratch suffix-automaton implementation,
not a passthrough.

## 4. Pre-registered kill condition / strong outcome, stated before running

**This cannot prove non-periodicity from finite data, exactly as ARM6 could
not prove non-automaticity from finite data.** The asymptotic claim (`p(n)`
is or is not eventually `O(n)`) is never decided by any finite prefix. What
CAN be measured honestly:

- **Kill condition (evidence against automaticity at this scale):** the
  ratio `p(n)/n`, evaluated at the largest `n` reached, is strictly higher
  than at every smaller checkpoint measured so far (i.e. still visibly
  growing, no plateau), while the Thue-Morse control's ratio is flat or
  decreasing over the same range. This does not prove `p(n) != O(n)`; it is
  the same class of statement ARM6 made ("any exact representation needs at
  least this much state, at this depth").
- **What would NOT be evidence for periodicity/automaticity:** `p(n)/n`
  plateauing within the reachable range. Cobham's bound is asymptotic; a
  plateau at `n` in the thousands or millions says nothing about the limit.
  State this explicitly in the results regardless of outcome.
- **Strong outcome, explicitly out of reach here:** an actual proof needs
  `p(n)` unbounded relative to `n` for ALL `n`, which requires an inductive
  combinatorial argument this arm does not attempt. This arm is a
  measurement, not that argument.

## 5. Reproduction

```bash
cd /Volumes/A/researchpapers/13-rule30
uv run python experiments/rule30/factor_complexity_probe.py --n 2000000
```

Ground truth: `experiments/rule30/center_column.py:center_column` (read-only
import, unmodified). Thue-Morse control generated in-file by direct
definition (parity of popcount), not imported from `automaticity_probe.py`
to avoid coupling this arm's correctness to that file's control generator.

Results filled in below after the run.

## 6. Correction to the checkpoint design (recorded before final results)

The first implementation swept `k` up to a large fraction of a FIXED `n` and
found `p(k)/k` declining as `k -> n`. That is not evidence of anything: it is
the trivial ceiling `p(k) <= n-k+1` binding as `k` approaches the total
generated length, unrelated to the sequence's real complexity. Corrected
design: fix several small `k`, sweep `n` upward, and watch whether `p(k, n)`
(distinct length-`k` factors in the first `n` symbols) plateaus (consistent
with a small true `p(k)`, as Cobham requires for an automatic sequence) or
keeps climbing with no sign of leveling off.

A second, unrelated problem surfaced during the corrected run: the pinned
ground-truth generator (`experiments/rule30/center_column.py`) grows one
Python big integer over all `n` steps, which costs `Theta(n^2)` machine-word
operations with a poor constant (a single bignum op on a growing `t`-bit
integer at every step `t=1..n`) -- at `n=5*10^6` this pegged a CPU at 100%
for 35+ minutes with zero output and was killed. This is the same
`Theta(n^2)` shape as Prize Problem 3 itself (no sub-quadratic algorithm for
the center column is known to anyone), so it cannot be fixed asymptotically,
but `a3_p2_orbit_closure/band_census.py`'s bit-packed `uint64`-word kernel
does the identical `Theta(n^2)` work with a far better constant (word-
parallel shifts via numpy, the same lever already used for the R7/P2 arms
this session). Read-only reused here via `_band_series("30", steps,
wmax=1)`, extracting the center bit. Cross-checked bit-for-bit against the
pinned `center_column` at `n=20000`: 0 mismatches, both correctness gates
(brute-force distinct-factor count, and fast-vs-pinned generator) pass
before any number below is trusted.

## 7. Results

Thue-Morse control (2-automatic, known linear factor complexity): `p(k)`
plateaus IMMEDIATELY, by `n=100000` already at its final value, and stays
flat out to `n=3000000` for every `k` tested (8, 12, 16, 20, 24) --
`p(24)=76`, nowhere near its `2^24` ceiling. This is exactly the signature
Cobham's theorem predicts and the control passes cleanly.

Rule 30, same pipeline, `n` up to 3,000,000:

| k | p(k) at n=1e5 | n=3e5 | n=1e6 | n=3e6 | ceiling 2^k | status at n=3e6 |
|---:|---:|---:|---:|---:|---:|---|
| 8 | 256 | 256 | 256 | 256 | 256 | full saturation (immediate) |
| 12 | 4096 | 4096 | 4096 | 4096 | 4096 | full saturation (immediate) |
| 16 | 51114 | 64821 | 65536 | 65536 | 65536 | full saturation (reached by n=1e6) |
| 20 | 95252 | 260800 | 644259 | 988257 | 1048576 | 94.2% and still climbing, no plateau |
| 24 | 99639 | 297179 | 970864 | 2746622 | 16777216 | 16.4%, undersampled (n < 2^24), uninformative |

**Verdict, stated plainly and not oversold.** At every `k` where this arm has
enough data to judge (`k<=20`), Rule 30's center column shows NO plateau
below its ceiling -- it either already realizes every one of the `2^k`
possible length-`k` patterns (`k<=16`) or is still climbing toward that
ceiling with no sign of leveling off (`k=20`). `k=24` is simply undersampled
(`n=3*10^6 < 2^24 approx 1.7*10^7`) and gives no information either way.

**This is NOT evidence of non-automaticity, and the reasoning for why not is
the whole point of stating it carefully:** full or near-full saturation of
the pattern space for small-to-moderate `k` is equally consistent with a
large-period periodic (hence trivially automatic) sequence -- a periodic
sequence with period `P >> 2^k` can realize every length-`k` pattern too.
The clean discriminator Cobham's theorem actually offers requires `k` large
enough, RELATIVE TO THE SEQUENCE'S OWN STATE COUNT, that an automatic
sequence's linear bound `p(k) <= Ck` would visibly separate from `2^k` --
and that requires probing `k` in the range of several dozen or more, which
in turn requires `n >> 2^k`, i.e. `n` in the range of `10^10`-`10^13` for
`k=30..40`. That is not reachable by ANY bit-packed simulation, fast or
slow, because it is bounded by the same `Theta(n^2)` wall as Prize Problem 3
-- this arm's own speedup (from the `Theta(n^2)`-with-bad-constant pinned
generator to the `Theta(n^2)`-with-good-constant bit-packed one) closes a
factor-of-tens-to-hundreds gap, not the polynomial-degree gap that would be
needed to reach informative `k`.

**What this arm actually establishes:** the factor-complexity route (ASY
survey, Theorem 17/Cobham) is confirmed to have no near-term computational
path to a useful answer, for a reason specific to this sequence (its
apparent complexity saturates the exponential ceiling far too fast for any
reachable `n` to separate "large-period automatic" from "genuinely
unbounded"). This is a negative result about the ROUTE, not about Problem 1.
No row status elsewhere in this project changes.

## 8. Reproduction

```bash
cd /Volumes/A/researchpapers/13-rule30
uv run python experiments/rule30/factor_complexity_probe.py --n 3000000 \
  --validate-n 20000 --checkpoints 100000 300000 1000000 3000000
```


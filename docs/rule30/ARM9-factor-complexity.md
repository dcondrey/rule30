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

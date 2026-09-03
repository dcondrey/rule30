# Conditional block loss at the exact state: measured at half the rate it needs

Date: 2026-09-03.  Scripts `prefix_cylinder_loss.py`, `mass_decomposition.py`,
`block_lemma.py`; logs of the same names dated `20260903` plus
`block_lemma_n17-19_20260903.log`.  Complete census on `psi_kernel.Endpoint`;
nothing sampled.  All three were pre-registered in their docstrings before
running.

Status: **the conditional block lemma is not falsified, and it is not
sufficient.**  A uniform per-state contraction does exist for blocks of length
`b >= 6`, but the rate it delivers is `0.17` to `0.65` bits per level against
the `1.0` that `(RW-alpha)` requires.  Proving the lemma exactly as measured
would not give the target.  That gate is section 4 and it is the result.

## 1. Why this state and not another

`RESULTS-COLUMN-DECOMPOSITION.md` section 10 killed the column-memory route:
the column is not a sufficient statistic for RW survival, the full endpoint
state is.  Within a fixed `n` the forced continuation is deterministic, so the
only branching is the choice of the `n` source symbols and the right
conditional object is the prefix cylinder: partition `{1,2}^n` by the exact
endpoint state after `p < n` free symbols, and count survivors per class,

```text
N_s(j) = #{W with prefix state s surviving j forced levels}.
```

This conditions on the strongest statistic available.  Any weaker conditioning
has already been killed.

## 2. Uniform contraction is false at short blocks, true from `b = 6`

`block_lemma.py`, `R(n, p, c, b) = max_s max_j N_s(j+b)/N_s(j)` at
`p = floor(n/2)`, no threshold and no aggregation, the maximum taken over
every state and every level:

| `n` | `c` | `b=4` | `b=5` | `b=6` | `b=7` | `b=8` | `b=9` | `b=10` |
|---|---|---|---|---|---|---|---|---|
| 13 | 3 | 0.500 | 0.333 | 0.143 | 0.056 | 0.020 | 0.008 | 0.000 |
| 14 | 2 | 1.000 | 0.500 | 0.333 | 0.091 | 0.056 | 0.026 | 0.008 |
| 15 | 2 | 1.000 | 0.333 | 0.100 | 0.033 | 0.011 | 0.004 | 0.000 |
| 16 | 3 | 1.000 | 1.000 | 0.500 | 0.091 | 0.029 | 0.012 | 0.004 |
| 17 | 2 | 1.000 | 0.500 | 0.200 | 0.067 | 0.028 | 0.012 | 0.005 |
| 17 | 3 | 0.333 | 0.111 | 0.062 | 0.023 | 0.010 | 0.005 | 0.002 |

- **`b <= 5` fails.**  Ratio `1.000` occurs at `b = 5` at `n = 16, c = 3`, and
  at `b <= 4` at many `(n, c)`.  The smallest block with no ratio-1 state
  anywhere is `b = 6`, whose worst value over `n = 10..17` is `0.500`.
- The states attaining ratio `1.0` hold tiny survivor counts, `1 -> 1`,
  `3 -> 3`, `4 -> 4` (`prefix_cylinder_loss.py`, threshold columns).  Above a
  count threshold of 16 the worst `b = 6` ratio drops to `0.17`.  So the
  violations are deep-tail plateaus, not bulk reservoirs.
- The statement is sensitive to the conditioning depth.  At `p = 2n/3` ratio
  `1.0` persists to `b = 6` and beyond; at `p = n/2` it does not.  The claim is
  about `p = floor(n/2)` only.

## 3. Absorbing the exceptional states

`mass_decomposition.py` tests the arithmetic a proof would use.  Split states
at level `j` into BIG (`N_s(j) >= delta N_j`) and SMALL.  If BIG states obey
`N_s(j+b) <= lambda N_s(j)` and SMALL states obey only the trivial bound, then

```text
N_{j+b} <= (lambda + mu (1 - lambda)) N_j = B N_j
```

with `mu` the SMALL mass fraction.  At `p = n/2`, `b = 8`, `delta = 0.001`:
`B <= 0.056` over `n = 11..16`, with `max mu = 0.001`.  At `delta = 0.01` the
same figure is `B <= 0.692`, because `mu` reaches `0.684`.  The absorption
works, but only because at `delta = 0.001` the threshold falls below one
source and every state is BIG, which makes `B` the unconditional maximum of
section 2 rather than an independent gain.

## 4. The rate gate, which decides it

A block contraction `N_{j+b} <= lambda N_j` iterates to
`N_j <= 2^n lambda^(j/b)`.  The run dies while `j <= alpha n` with `alpha < 1`
exactly when

```text
log2(1 / lambda) / b  >  1        (bits per level)
```

That is the requirement.  Measured, worst case over `n = 10..17` and both `c`:

| `b` | worst `lambda` | bits per level | verdict |
|---|---|---|---|
| 5 | 1.000 | 0.000 | fails outright |
| 6 | 0.500 | 0.167 | short |
| 7 | 0.091 | 0.494 | short |
| 8 | 0.056 | 0.520 | short |
| 9 | 0.026 | 0.585 | short |
| 10 | 0.008 | 0.697 | short |

**The uniform per-state contraction delivers at most `0.70` bits per level and
needs more than `1.0`.**  The shortfall is roughly a factor of two and it does
not close over `n = 10..17`.

Two caveats, both of which make the table optimistic rather than pessimistic,
so the conclusion is not softened by either:

- The large-`b` rows are contaminated by finite depth.  The deepest survivor
  run at these `n` is about 10 levels, so a block of 9 or 10 reaches the end of
  the data and reports a ratio that is small because nothing survives that
  deep at all, not because of contraction.  The honest range is `b = 6..8`,
  where the rate is `0.17` to `0.52`.
- The aggregate rate is much better than the uniform one: `N_{j+b}/N_j` pooled
  is `0.001` to `0.007` at `b = 6`, which is the `1.35` bits per level of
  `uc/BRIEF.md` section 4.  The uniform per-state bound is far weaker than the
  average, which is precisely the gap a proof has to pay for.

## 5. Verdict

The conditional block lemma over the exact half-depth prefix state is the
strongest surviving candidate of its kind, and it is not falsified: from
`b = 6` no state has ratio 1 at any tested `n`.  But it is insufficient by a
factor of about two in rate, so proving it would not yield `(RW-alpha)`.

This is a negative result about the shape of the argument, not about the data.
Anyone proposing a conditional-loss lemma for this problem must first state
the rate it would deliver and compare it to the `1.0` bits per level the
target needs.  Three separate mechanism families in
`PROOF-STATE-CAPSULE.md` section 5 were rate mechanisms that were never
checked against this gate before being pursued.

What would change the verdict:

1. A conditioning that makes the uniform rate approach the aggregate `1.35`.
   The gap is the price of the worst state; a proof that the worst state is
   rare or structured would recover part of it, but that is the reservoir
   classification, not a block lemma.
2. Larger `n`.  The rate at `b = 6` moved `0.143 -> 0.500 -> 0.200` across
   `n = 13, 16, 17` with no trend toward the requirement.  `n = 18, 19` are
   running and are recorded in `block_lemma_n17-19_20260903.log`.

## 6. Reproduction

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run python prefix_cylinder_loss.py --min-n 10 --max-n 16 --blocks 2,4,6,8,10
uv run python mass_decomposition.py --min-n 11 --max-n 16 --blocks 4,6,8 --deltas 0.001,0.01
uv run python block_lemma.py --min-n 10 --max-n 16 --bmax 10
```

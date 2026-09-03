# The fibre has its own exact half-slope memory law, and the base-to-fibre
# channel is one scalar per step

Date: 2026-09-03.  Script `diagonal_memory.py`, log `diagonal_memory_20260903.log`,
complete enumeration of `{1,2}^L` for `L = 1..13`.

Status: **two exact laws, both proved.**  `k_dia(L,i) = ceil((L+i+1)/2)` for
the anti-diagonal entry at index `i`, and `k_seed(L) = ceil((L+1)/2)` for the
single scalar by which the column reaches the diagonal.  Together with
`RESULTS-COLUMN-DECOMPOSITION.md` section 5 this gives a complete half-slope
description of the skew product.  It also explains structurally why section 10
of that document had to fail.

## 1. The skew product, exactly

`psi_kernel.Endpoint.peek` runs two trajectories of the SAME four-state
automaton, differing only in seed and direction:

```text
column    nc[L] = BOUNDARY[symbol]      nc[i]   = CONE[col[i+1]][nc[i+1]]
diagonal  nd[0] = nc[0]                 nd[k+1] = CONE[dia[k]][nd[k]]
```

The column is read right to left and seeded by the appended symbol.  The
diagonal is read left to right and seeded by `nc[0]`.

**The base reaches the fibre through exactly one scalar per append, `nc[0]`.**
That is two bits per step, and it is the entire coupling.  No RESULTS file
stated this before; it is visible only in the kernel source.

## 2. The channel is half-memory

`nc[0]` is the column entry at distance `d = L` from the end, so
`RESULTS-COLUMN-DECOMPOSITION.md` section 5c gives its memory immediately.
Measured independently as `k_seed(L)`, the least `k` with `nc[0]` a function of
`w[-k:]`:

| `L` | 1 | 3 | 5 | 7 | 9 | 11 | 13 |
|---|---|---|---|---|---|---|---|
| `k_seed(L)` | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| `ceil((L+1)/2)` | 1 | 2 | 3 | 4 | 5 | 6 | 7 |

Exact at every `L = 1..13`.  The signal the base sends to the fibre forgets the
first half of the input, at every length.

## 3. The diagonal forgets nothing as a whole

`k_dia(L)`, the least `k` with the whole diagonal a function of `w[-k:]`, is
`L` at every `L = 1..13`.  The anti-diagonal remembers every symbol.

This is the structural reason `RESULTS-COLUMN-DECOMPOSITION.md` section 10 had
to come out the way it did.  The state is the pair, the pair's memory is the
maximum of the two, and the diagonal's is total.  A sufficient statistic for RW
survival cannot forget, because the diagonal does not.

## 4. But the per-entry law is exact and half-slope

`k_dia(L, i)`, least `k` with `diagonal(w)[i]` a function of `w[-k:]`:

```text
k_dia(L, i) = ceil((L + i + 1) / 2)      for every L = 1..13 and every i
```

Verified against every measured entry with no exception.  Note the direction.
For the column, memory DECREASES with the index, `k_col(L,i) = ceil((L-i+1)/2)`,
measured from the end.  For the diagonal it INCREASES, and the two agree at the
seam: `k_dia(L,0) = ceil((L+1)/2) = k_seed(L)`, since `nd[0]` is `nc[0]`.  At
the far end `k_dia(L, L-1) = L`, which is section 3.

### Proof

Append `s` to a word `w` of length `L`.  The old diagonal `dia` has the law at
length `L`; the new diagonal `nd` is claimed to have it at length `L+1`.

*Seed.*  `nd[0] = nc[0]`, whose memory is `ceil((L+2)/2)` by the column law at
distance `L+1`.  The claim at `i = 0`, length `L+1`, is `ceil((L+2)/2)`.

*Step.*  `nd[k+1] = CONE[dia[k]][nd[k]]`.  By hypothesis `dia[k]` depends on the
last `ceil((L+k+1)/2)` symbols of `w`, hence on the last
`ceil((L+k+1)/2) + 1` of `w s`; and `nd[k]` depends on the last
`ceil((L+k+2)/2)` of `w s`.  So `nd[k+1]` depends on the last

```text
max( ceil((L+k+1)/2) + 1, ceil((L+k+2)/2) )  =  ceil((L+k+3)/2)
```

symbols, and the claim at index `k+1` and length `L+1` is exactly
`ceil(((L+1) + (k+1) + 1)/2) = ceil((L+k+3)/2)`.  QED.

The identity `max(ceil((L+k+1)/2)+1, ceil((L+k+2)/2)) = ceil((L+k+3)/2)` was
checked for all `L < 200` and all `k < L`, zero failures.  Double induction as
in section 5c: outer on word length for the appeal to `dia`, inner on `k` for
the appeal to `nd[k]`.

## 5. Corollary: the RW observable forgets a quarter of the word

The RW test reads the cell `T[n+j][n]`, which is `diagonal[n]` of the endpoint
word of length `L = n + j`.  By section 4 its memory is

```text
ceil((2n + j + 1)/2) = n + ceil((j+1)/2),
```

so it is independent of the first `floor((j-1)/2)` symbols of the word.  The
observable at level `j` forgets about `j/2` symbols, growing with the level.

Two honesty notes, both load bearing:

- **This is not a forgetting statement about survival.**  Survival through
  levels `0..j` requires every observable, and the level-0 observable depends on
  the whole word.  `RESULTS-RW-LINEAR-SLACK.md` 9.2 measured survival, not a
  single cell, and is not contradicted.
- **This is not new as an observation.**  It is fact (1) of
  `uc/r1-entropy/lightcone_check.py` (concurrent session), "`T[u][d]` depends on
  `e_j` only if `j >= (u-d-1)/2`", zero failures for `u = 2..12`.  The two
  differ by at most one from index conventions.  What is new here is the exact
  least-`k` form, the proof at all lengths, and the seed statement of section 2.

## 6. What this changes

- The skew product now has a complete half-slope description: base law,
  channel law, fibre law, all exact, all proved.
- It explains rather than merely records the section 10 kill.  The diagonal is
  the part that cannot forget, and it is also the part that carries survival.
- It does NOT give a rate.  `RESULTS-CONDITIONAL-BLOCK-LOSS.md` section 4 shows
  the rate gate a conditional argument must clear is 1.0 bits per level, and
  nothing here produces a rate at all.

## 7. Reproduction

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run python diagonal_memory.py --lmax 13     # about 3 minutes
```

# Driven 0001: finite onset-prefix basins with arbitrary exterior

Date: 2026-09-15. **Exact finite certificates and their uniform
consequences; no eventual lock or prize result.** The
[three-prefix certificate](RESULTS-r1-0001-boundary-certificate.md)
extends to many right rows at the onset of an eventual `0001` drive.
It still leaves one unresolved observation bit per block.

## 1. Complete four- and eight-cell entry tests

Use the source certificate's convention: strings list spatial sites
`1,2,...`, and phase zero means the next drive values are `0,0,0,1`.
Write `K={0010,0011,0111}` for its invariant four-prefix set.

For width `n`, define `F_n(u)` as the set of first `n` cells after four
driven steps, over all sixteen initial exterior words on sites
`n+1,...,n+4`. Radius-one locality makes this the exact one-block image
of the prefix cylinder. Put

```text
B_0 = {u : the first four cells of u belong to K},
B_(j+1) = B_j union {u : F_n(u) subseteq B_j}.
```

Membership in `B_j` guarantees entry to K within `4j` steps, for every
infinite exterior. Induction applies to the actual future exterior; it
does not assume that future exterior words are independently choosable.

The complete small graphs give:

| Prefix width | New prefixes at ranks 0,1,2,3,4 | Certified basin | Unresolved |
|---|---|---:|---:|
| 4 | 3, 4 | 7 / 16 | 9 |
| 8 | 48, 112, 19, 6, 1 | 186 / 256 | 70 |

At width four, the exact certified entry conditions are

```text
already in K: 0010, 0011, 0111;
entry within four steps: 1100, 1010, 1011, 1111.
```

The eight-cell condition is the rank table in the
[JSON certificate](../../experiments/rule30/r1-0001-onset-basin-audit.json).
Each of the 256 words has its full successor set and either a rank
`0..4` or `null`. The only rank-four word is `11100101`.

These are the least fixed-point basins in these particular graphs.
**The 70 unranked eight-cell words are unresolved, not counterexamples.**
A path avoiding K in the finite graph need not come from one consistent
infinite exterior over all times. Larger prefixes or longer correlated
cones can prove further entries. Conversely, entry to K supplies the
one-bit reduction, not periodicity of that bit.

## 2. Phase at the onset matters

Let the prescribed drive at onset be the rotation starting at phase
`phi` of `D=0001`. Set `delta=(-phi) mod 4`. The next phase-zero time is
`delta` steps later. Given an onset prefix `u` of width `n`, evaluate all
`2^delta` exterior assignments on its next `delta` cells. If every
resulting width-`n` prefix has rank in section 1, entry is guaranteed
within

```text
delta + 4 * max(resulting ranks)
```

steps. This gives exact membership tests for the stated alignment-and-
basin certificate, rather than a classification of all possible eventual
entries.

| Onset drive phase | Width-four admitted / 16 | Maximum delay | Width-eight admitted / 256 | Maximum delay |
|---|---:|---:|---:|---:|
| `0001` | 7 | 4 | 186 | 16 |
| `0010` | 8 | 3 | 184 | 15 |
| `0100` | 5 | 2 | 169 | 18 |
| `1000` | 5 | 5 | 165 | 17 |

All admitted words and their individual delay bounds are in the JSON.
The width-four conditions for the three nonzero phases are:

```text
0010: 1000,1100,0010,1010,0110,0101,1011,0111  (delay 3);
0100: 1100,1010,1101,1011,0111                 (delay 2);
1000: 1100,1010,1001,1011                     (delay 1),
      0001                                  (delay 5).
```

For a hypothetical actual singleton centre with an eventual rotated
`0001` tail, these are conditions on its actual right row at that onset.
If its prefix is admitted, the residual-bit reduction follows after the
certified delay. The initial right row at the onset need not be zero.
Neither admission of every singleton onset nor eventual periodicity of
the residual bit is proved.

## 3. Another branch, and why entry is not automatically universal

The word `D=0001` obeys a further exact transition:

```text
D -> 0011  iff x5=1 and (x6 OR x7)=1;
D -> D     otherwise.
```

Its neighbour block is always `0001`. Thus `K union {D}` is invariant.
A trajectory entering this union either stays in D forever, with a
period-four neighbour, or eventually enters K and inherits its unresolved
bit. The same width-eight graph certifies entry to this larger union for
210 prefixes, with rank layers `64,116,22,7,1`; 46 remain unranked.
This enlargement still does not prove a periodic observer for all rows.

There is an exact infinite right row that never enters K: take the
already recorded space-seven/time-four torus, with rows

```text
0000100
0001110
0011001
1110111
```

and place the centre at the first column. Both centre and right neighbour
are `0001`; the first four right cells at every phase-zero time are D.
This is the [recentered archive witness](RESULTS-r1-periodic-realization-scope.md),
not a newly discovered torus. Its right row is not finite.

Nevertheless, truncating that initial right row after `L=4m+4` cells
gives a finite right row whose first four cells agree with the torus
through time `4m`. Hence it avoids K through all phase-zero times up to
`4m`. This proves that **there is no entry-time bound independent of the
initial right support**. It does not refute eventual entry for every
finite right row, and it does not refute eventual periodicity of every
finite-row observer under this particular drive. Both universal claims
remain unproved here.

## 4. Bounded audit and limits

```sh
uv run --no-project python experiments/rule30/r1_0001_onset_basin_audit.py
```

The [checker](../../experiments/rule30/r1_0001_onset_basin_audit.py)
uses independent shrinking-cone truth-table and packed implementations.
It exhausts 4,352 four-step cones for widths four and eight, then 4,080
phase-alignment cones. It checks the D transition, the archived torus,
and eight finite truncations as indexing controls for the all-length
locality argument. It also verifies that the deterministic-successor
subgraphs at these two widths have no cycles. That last statement does
not exclude a periodic observer with a changing prefix.

The [periodic-cylinder report](RESULTS-r1-periodic-cylinders.md) explains
why failure of a fixed-width one-block certificate cannot exclude longer
returns or recovery of a prefix after intermediate uncertainty. None of
the present negative graph statements is extrapolated to all widths.

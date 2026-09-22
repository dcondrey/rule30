# Single-interval deficits on the seed: first measurement, and two exact facts

Status: **computed over shells `k = 10..24`. No ladder statement changed; the
matching deficit target stays conditional.** `D_+(R)` and `D_-(R)`, the
quantities this node's target is about, had never been computed on the Rule 30
seed at any `(k, R)`. The only stored deficit was the single `k=20`, `R=1024`
neighborhood certificate; the only other `D_±` in the tree belongs to a
24-symbol artificial word.

## 1. Method and the two assumptions it rests on

`d_+([a,b)) = #{+1 in [a,b)} - #{-1 in [a-R, b+R)}`, clipped to the shell. With
`P` the prefix count of `+1` and `Q` of `-1`,

    d_+([a,b)) = f(b) - g(a),  f(b) = P_b - Q_min(N,b+R),  g(a) = P_a - Q_max(0,a-R)

so one pass with a running minimum of `g` gives the exact maximum over every
`a < b`. That is `O(N)`, not the `O(N^2)` the defining formula suggests.
Clipping is done by clamping the prefix index rather than special-casing the
ends, which matters: the stored certificate's expanded interval clips on the
right.

**Control.** The scan must return `D_+ = 814` at `k=20`, `R=1024`, against the
stored `neighborhood_certificate`. It does. A scan that mishandles the clipping
does not.

**Alignment re-verified, not inherited.** Every seed number here depends on the
payload being read at bit offset 239, bitorder `big`. That constant was
discovered once by an offset scan and has been copied since. The scan re-derives
it on every run against 8192 freshly regenerated centre-column bits and refuses
to proceed otherwise.

## 2. `D_+ + D_-` saturates at exactly the shell's signed sum

For `R` past a shell-dependent point, `D_+ + D_- = |sum z|` **exactly**, at
every one of the fifteen shells `k = 10..24`:

| `k` | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `\|sum z\|` | 0 | 4 | 56 | 154 | 112 | 64 | 356 | 772 | 104 | 638 | 152 | 194 | 2268 | 6566 | 3872 |
| plateau | 0 | 4 | 56 | 154 | 112 | 64 | 356 | 772 | 104 | 638 | 152 | 194 | 2268 | 6566 | 3872 |

The smaller of the two deficits reaches zero and the larger holds at the global
imbalance. So at fixed `k` the target quantity is eventually constant in `R` and
`D_sum/R -> 0` trivially; all the content is in where the decay happens, not
whether it does.

## 3. Where the decay happens sits near `sqrt(N)`

First dyadic `R` with `D_+ + D_- <= R`:

| `k` | 16 | 18 | 20 | 22 | 24 |
|---|---|---|---|---|---|
| `R*` | 512 | 512 | 2048 | 4096 | 4096 |
| `sqrt(N)` | 256 | 512 | 1024 | 2048 | 4096 |
| ratio | 2.0 | 1.0 | 2.0 | 2.0 | 1.0 |

Across all fifteen shells the ratio stays within `[0.707, 2.828]`, a factor of
four band around `sqrt(N)`. **The ratio is quantized**: `R*` is measured on a
dyadic grid and `sqrt(N) = 2^(k/2)`, so the ratio can only be a power of
`sqrt(2)`, and the band is four grid steps wide. The honest statement is that
`R*` tracks `sqrt(N)` to within the grid's own resolution on every shell
measured, and nothing finer.

This is the scale at which `898a681ea2f86cc5` kills `R ~ sqrt(N)` as a
canonical schedule, by an artificial word showing square-root-scale matching
restrictions are strictly stronger than P2. The measurement does not revive that
schedule; it records that the seed's own crossover sits there.

## 4. The `++++----` mechanism is present on the seed, and it is radius-dependent

`c261e82b523850c9` refutes "bounding the largest single-interval deficit bounds
the total deficiency" with a 24-symbol periodic word at `R=1`, where three
bounded deficits sum. Whether that mechanism occurs on the real seed was
unmeasured, and the one stored point suggested it does not: at `k=20`, `R=1024`
the maximizing collection is a single component, so `Delta_+ = D_+ = 814`.

Across the stored `U_R` rows it does occur, and the split is by radius. Writing
`Delta_+ = (U_R + sum z)/2`:

| `k` | `R` | `U_R` | `D_+` | `Delta_+` | single interval attains it |
|---|---|---|---|---|---|
| 16 | 8 | 5728 | 429 | 3042 | no |
| 16 | 32 | 1720 | 410 | 1038 | no |
| 16 | 128 | 360 | 358 | 358 | yes |
| 18 | 128 | 1328 | 225 | 612 | no |
| 18 | 512 | 104 | 0 | 0 | yes |
| 20 | 8 | 90522 | 1515 | 45337 | no |
| 20 | 128 | 8126 | 1384 | 4139 | no |
| 20 | 512 | 2230 | 1083 | 1191 | no |
| 20 | 1024 | 1476 | 814 | 814 | yes |

At small radius the collection maximum exceeds the best single interval by up to
a factor of 30 (`k=20`, `R=8`: 45337 against 1515). So the kill's mechanism is
real on the seed, not an artifact of the constructed word, and the single-interval
target is only equivalent to the collection target near and above the crossover.
The stored `k=20` point was taken exactly at that shell's crossover, which is why
it reads as single-component.

## 5. The packing bound is slack by two to three orders of magnitude

`U_R <= K_(N,R) (D_+ + D_-)` with `K_(N,R) = 1 + floor((N-1)/(2R+1))` is the
explicit packing factor this node's success criterion asks for. Measured against
the actual `U_R`, the bound is loose by 32x at `k=12`, `R=64`; 256x at `k=16`,
`R=128`; 449x at `k=18`, `R=128`; and 1858x at `k=20`, `R=8`. The slack grows
with `k` at fixed `R`. A proof of the single-interval bound would therefore still
not deliver the collection bound at realistic constants through this inequality,
which is worth knowing before anyone spends a session proving it.

## 6. Scope

Exact over `k = 10..24` and `R = 2^j`, `3 <= j <= k-2`, and nothing past it.
`D_±` are exact; `Delta_±` exist only at the nine `(k,R)` rows where a stored
`U_R` does, and are derived from it rather than recomputed. **The radius in the
target statement is one a prover gets to choose, so a fixed dyadic grid is not
evidence for or against any schedule**, and `D_sum/R` at a grid point is not a
counterexample to `D_+ + D_- = o(R)`. The crossover trend is fifteen points on a
quantized grid, not a law. Shells are read from a gitignored payload that no
script in this chain regenerates.

## 7. Files

`seed_deficit_scan.py` (`seed_deficit_scan.log`). It re-verifies the payload
alignment on every run, asserts the `D_+ = 814` control, and writes no tracked
artifact. Logs are hidden by the global ignore; `git add -f` to commit them.

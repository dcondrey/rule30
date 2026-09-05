# Single-flip pairing on the RW survivor levels

Date: 2026-09-03.  Script `flip_pairing.py`; logs `flip_pairing_20260903.log`
(pairing census, `n = 9..16`, both `c`) and `flip_pairing_profile_20260903.log`
(death profile, `n = 12..16`).  Complete census on `psi_kernel.Endpoint`;
nothing sampled.  The survivor counts reproduce `RESULTS-CLUSTER-ANATOMY.md`
section 3 exactly (`512/214/112/53/23/6/6/6/6` at `n = 9, c = 3`).

Status: **KILLED.  Single source flips are not a pairing between survivor
levels.  A flip at any depth but the first three source symbols is a fresh
coin on every forced level, so the fraction of level-`j` survivors with a
partner decays like `0.4^j` and the depth of the nearest partner is
unbounded.  Unconditional per-level balance is itself false at deep levels.**

## 1. Pre-registration

The full-degree result (`RESULTS-PSI-ANCESTRY-LAW.md` section 10) kills every
bounded-arity seam law for the `E` defect but not injection arguments.  The
missing fact behind a halving bound `N_{j+1} <= N_j / 2` is that the `E`
constraint is balanced on every survivor level, not merely on average.  An
injection would pair each source passing level `j` with one failing `E` at
level `j`.  The endpoint-flip cocycle (`RESULTS-ENDPOINT-FLIP-COCYCLE.md`)
says one endpoint flip rewrites the inverse cut only on `[k, 2k+1]`; the
proposal was to use those flips as the pairing on the RW survivor set.

Setting.  `W in {1,2}^n`; for `j >= 0`, `e_{n+j}` is `H`-forced.  `S_j` is
the set alive at level `j` (forced cell `T[n+j'][n] = c` and hard-core forced
symbol for all `j' < j`).  `D_j` is the strict `E`-failure set at `j` (alive,
forced symbol hard-core, forced cell has the wrong `E`); `Dall_j` is every
death at `j`, hard-core kills included.  For `W in S_{j+1}` and `i < n`, the
flip `W' = W` with `e_i` toggled is a valid partner if `W' in D_j` and the
forced symbol at level `j` agrees; `delta = n-1-i` is the flip depth.

Strong outcome: every `W in S_{j+1}` has a partner at bounded `delta`, and the
flip graph `S_{j+1} -> D_j` has a matching saturating `S_{j+1}`.  Kill: a
level where a fixed fraction of `S_{j+1}` has no partner, or the required
`delta` grows with `n`, or the maximum matching falls short.

## 2. Result: all three kill conditions fire

Coverage (fraction of `S_{j+1}` with at least one valid partner), strict
definition, both `c` pooled by range:

| level `j` | `n = 11` | `n = 12` | `n = 13` | `n = 14` | `n = 15` | `n = 16` |
|---|---|---|---|---|---|---|
| 0 | 0.87, 0.92 | 0.94, 0.96 | 0.95, 0.95 | 0.95, 0.96 | 0.96, 0.97 | 0.98, 0.98 |
| 1 | 0.41, 0.59 | 0.51, 0.51 | 0.57, 0.62 | 0.60, 0.60 | 0.64, 0.66 | 0.65, 0.67 |
| 2 | 0.27, 0.27 | 0.32, 0.39 | 0.27, 0.30 | 0.30, 0.36 | 0.33, 0.38 | 0.31, 0.37 |
| 3 | 0.10, 0.11 | 0.17, 0.22 | 0.16, 0.19 | 0.12, 0.17 | 0.11, 0.14 | 0.14, 0.22 |
| 4 | 0.00, 0.13 | 0.00, 0.06 | 0.00, 0.10 | 0.03, 0.10 | 0.04, 0.09 | 0.07, 0.08 |
| 5 and deeper | 0 | 0 | 0, 0.15 | 0 | 0.04, 0.19 | 0, 0.08 |

Each cell lists the two `c` values in ascending order.  The deep rows are
the sparse survivor sets (`20` to `255` sources) where the strict coverage
is `0` at most levels and never above `0.19`.

- **Coverage is a fixed fraction short at every level `j >= 1`**, roughly
  halving per level, and does not improve with `n` at fixed `j`.  Level 0 is
  the only level near 1, and even there it is not 1 (`23722/24909` matched at
  `n = 16, c = 3`).
- **Maximum matching never saturates.**  At `n = 16, c = 3`: `23722/24909`,
  `6029/10412`, `1260/3977`, `333/1698`, `46/625`, `0/234` for `j = 0..5`.
  No injection by single flips exists at any level.
- **The nearest partner is at unbounded depth.**  The maximum over survivors
  of the minimal `delta` is `n-1` or `n-2` at levels 0..3 for every `n`
  (`15` at `n = 16`).  The histogram of minimal `delta` at `n = 16, j = 0`
  is `3751, 5296, 4277, 2797, 2001, 1797, 1246, 998, 722, 462, 377, 267,
  216, 104, 22, 1` for `delta = 0..15`: the whole source length is used.
- Relaxing the pairing (any same-level death, hard-core kills included; or
  dropping the forced-symbol agreement) raises coverage by at most `0.1` and
  leaves every conclusion unchanged (`lenient` and `freeH` columns).
- Counting distinct endpoint states instead of sources (`states` columns)
  changes nothing: at `n = 16, c = 3, j = 3`, `86` of `340` states have any
  name with a partner.

**Unconditional balance is false.**  Against strict `E`-failures,
`|S_{j+1}| <= |D_j|` fails at many levels for both `c` (list per `(n, c)` in
the log summary).  At level 0 it must fail for one of the two `c`, since
`S_1(c) = D_0(3-c)` exactly (`24909 / 24540` at `n = 16`).  Against all
deaths it holds on the bulk levels but fails at the deep ones: `n = 16,
c = 3` has `99 -> 54 -> 28 -> 18` at `j = 7, 8, 9`; `n = 10, c = 3` has
`22 -> 14 -> 12`; `n = 9, c = 3` has the known `6 -> 6 -> 6 -> 6` plateau.
Whatever pairs survivors with failures, per-level halving is not a true
statement of the finite data; only the average rate (`0.4` per level,
`RESULTS-RW-LINEAR-SLACK.md`) is.

## 3. Mechanism: a flip is a fresh coin on every level

Death profile (`flip_pairing_profile_20260903.log`, `n = 16, c = 3`).  For
`W in S_{j+1}` and each single flip at depth `delta`, the probability that
`W'` is still alive at level `j`:

```text
j=1  delta=0..15:  0.36 0.42 0.40 0.39 0.42 0.40 0.40 0.41 0.40 0.39 0.41 0.43 0.45 0.59 0.83 0.98
j=2                0.15 0.19 0.14 0.17 0.20 0.15 0.19 0.16 0.17 0.18 0.17 0.23 0.24 0.46 0.79 0.98
j=3                0.06 0.07 0.06 0.06 0.06 0.06 0.06 0.07 0.08 0.07 0.07 0.13 0.18 0.43 0.76 0.98
j=4                0.00 0.04 0.02 0.04 0.00 0.00 0.02 0.01 0.02 0.02 0.03 0.08 0.18 0.33 0.73 0.98
```

and the level at which `W'` dies, pooled over all flips: `0: 0.52, 1: 0.20,
2: 0.08, 3: 0.04, ...` at every `j`.

- For `delta <= n-4` (every source symbol except the first three) the
  profile is flat at `0.4^j`: the flip kills at level 0 with probability
  `1/2`, at level 1 with probability `0.2`, and so on, independent of where
  the flip is.  A single source flip toggles the `E` bit of every forced
  level as an independent coin.  This is the full-degree fact seen from the
  source side.
- The only flips that preserve the earlier levels are `e_0, e_1, e_2`
  (`0.98, 0.8, 0.5`), and they preserve them because they change nothing:
  `e_0` leaves `W'` alive at every level with probability `0.98`, so it does
  not toggle the target either.  (This is the low bit-0 influence of
  `BACKLOG.md` L10 and the invisible first-bit flip of the alternating
  source, seen again.)
- Hence a level-`j` survivor has a partner only if one of its `n-3` coin
  flips happens to survive levels `0..j-1` and fail at `j`, probability
  about `0.6 * 0.4^j` per flip.  Coverage at fixed `j` is therefore
  `1 - (1 - 0.6 * 0.4^j)^(n-3)`, which is what the table shows, and keeping
  it near 1 at level `j` needs `n` exponential in `j`.  "Bounded distance
  from the target row" is not a property the pairing can have.

The compact-influence interval `[k, 2k+1]` of the cocycle is a statement
about the inverse cut `I(e)` along the diagonal.  The RW constraint lives on
the row `T[u][n]` across the columns `u = n, ..., 2n+3`, and every one of
those cells sees every source symbol through the column integrals of
`uc/BRIEF.md` section 2.  The bounded interval does not project to a bounded
set of constrained levels.

## 4. Disposition

- Closest killed row in `PROOF-STATE-CAPSULE.md` section 5: "One backward
  source defect" (single-coordinate relaxations remain UNSAT; branched and
  global obstruction).  This is the same fact measured as an involution on
  the survivor set rather than as a relaxation.  Also the
  `diagonal-permutation-cylinder` row of `BACKLOG.md` ("nearly every survivor
  is isolated"), now quantified per level.
- What would still be an injection route: a pairing that is not a fixed
  coordinate flip, i.e. one that rewrites the source by an amount depending
  on the state (a phase-decorated map).  Capsule section 6 item 4 already
  names that as the target; this result says the decoration cannot be
  "which coordinate", it must be "which state".
- Rank of what is left: the average per-level rate `0.4` is measured and
  stable; no per-level, per-state, or per-flip halving law is available in
  the finite data.

## 5. Reproduction

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run python flip_pairing.py --min-n 9 --max-n 16 > flip_pairing_20260903.log      # 20 s
uv run python flip_pairing.py --profile --min-n 12 --max-n 16 > flip_pairing_profile_20260903.log
uv run python block_halving.py --min-n 9 --max-n 18 > block_halving_20260903.log    # 90 s
```

## 6. What per-level statement is true: block halving and the counting constant

Script `block_halving.py`, log `block_halving_20260903.log`, `n = 9..18`,
sources and distinct endpoint states.  Since per-level halving is false,
the weakest form still worth an injection is block halving: the least `k`
with `N_{j+k} <= N_j / 2` at every level.

| `n` | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|
| least `k`, sources (`c = 2`, `c = 3`) | 1, 4 | 1, 3 | 1, 2 | 2, 2 | 1, 2 | 3, 2 | 2, 1 | 1, 2 | 2, 1 | 2, 1 |
| least `k`, states | 1, 4 | 1, 3 | 1, 2 | 2, 2 | 1, 2 | 2, 2 | 2, 1 | 1, 2 | 1, 1 | 2, 1 |

`k <= 3` for every `n >= 11` with no growth; the `4` and `3` at `n = 9, 10`
are the small plateaus.  Block halving is a true statement of the data, but
it is too weak on its own: halving over `k` levels is rate `1/k` bits per
level, and `(RW-alpha)` needs rate at least `1`.

The counting form of `(RW-alpha)` is `N_j <= C 2^(n - lambda j)`, and the
least constant `C(n, lambda) = max_j N_j 2^(lambda j - n)` over the levels is:

| `lambda` | 1.0 | 1.1 | 1.2 | 1.3 | 1.35 |
|---|---|---|---|---|---|
| `C(9, 3)` | 3.00 | 5.22 | 9.09 | 15.83 | 20.89 |
| max `C(n, c)` over `n = 10..18` | 1.00 | 1.22 (`n = 11, c = 3`) | 1.98 (`n = 11, c = 3`) | 3.22 | 4.59 (`n = 18, c = 2`) |
| `C(n, c) = 1` on how many of the 18 cases, `n = 10..18` | 18 | 16 | 14 | 5 | 1 |

- **The line `N_j <= 2^(n - j)` is crossed only at `n = 9, c = 3`**
  (levels 7 and 8, the `6, 6, 6, 6` plateau, `C = 3`).  For every other
  `(n, c)` from 9 to 18 the survivor chain lies under the slope-1 line from
  `2^n` with constant 1, and under slope 1.1 except at `n = 10, 11, c = 3`.
  The three earlier known violations of the naive bound
  (`uc/BRIEF.md` section 4: `(3,3,1), (4,2,2), (7,3,4)`) and this one are
  all below `n = 10`.
- `N_j <= 3 * 2^(n - j)` holds on all data and suffices for `(RW)`, since
  `C < 4` gives `N_{n+2} < 1`.  The constant `3` is tight at `n = 9` and
  slack (`1.0`) everywhere else through `n = 18`.
- At slopes `1.3` and above the constant is driven by the deepest plateau
  (`argmax` at the last nonzero level) and fluctuates between `1.0` and
  `3.2` with no trend in `n` (`3.22` at `n = 11`, `2.25` at `n = 16`,
  `3.03` at `n = 18`, all `lambda = 1.3`).  The average rate `1.35` is not
  a uniform rate; the uniform rate the data supports is between `1.0` and
  `1.2`.

This narrows the counting target without proving anything: the statement
to prove is `N_j <= 3 * 2^(n - j)` for all `n, j`, or equivalently that no
survivor plateau of size above `3 * 2^(n - j)` exists.  The only plateau
that comes close in the data is one endpoint state with six source names at
`n = 9`.

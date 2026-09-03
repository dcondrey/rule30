# Cluster anatomy: survivors that die together are one endpoint state with many names

Script `cluster_anatomy.py`, log `cluster_anatomy_20260902.log`.  Complete
finite computation on the validated kernel (`psi_kernel.py`); nothing sampled.

## 1. Question

Two clusters were on record without an explanation.  In RW at `n = 9, c = 3`
six survivors persist through `k = 5..8` and die together (BACKLOG.md
section 8, `half-survivor-step`).  In BWH+ at `n = 15, c = 3` eighteen
sources reach the 16-cell plateau and die together, which
`RESULTS-BINARY-WEDGE-HORIZON.md` section 5 called "a synchronized phase
catastrophe".  What do the members share at the death level?

## 2. Answer

Everything.  In every cluster examined the members carry the identical
endpoint state (full `column` and `diagonal` of `psi_kernel.Endpoint`)
already at `k = 0`, before any forced step.  The forced orbit is a function
of that state alone, so the members are one orbit under several source
names.  "Dying together" is the fibre of the source-to-state map, not a
coincidence of distinct orbits.

| cluster | members | distinct states at `k = 0` | shared source bits | death |
|---|---|---|---|---|
| RW `n = 9, c = 3`, depth 8 | 6 | 1 | `...222122` (all 6 hard-core prefixes of length 3 followed by 2; the 2 non-hard-core ones map to another state and die at `k = 2`) | forced `e = 1` gives `E = 0`, need 1 |
| BWH+ `n = 15, c = 3`, depth 16 | 18 | 1 | `.....2211212112` (18 of 32 prefixes; the other 14 map to 3 other states, dying at 0 and 6) | forced `e = 1` gives `E = 0`, need 1 |
| RW `n = 12, c = 2`, depth 9 | 2 | 1 | `.11122211121` | forced `e = 2` gives `E = 1`, need 0 |
| RW `n = 16, c = 3`, depth 10 | 18 | 2 (fibres of 8 and 10) | two suffixes, `112122211122` and `111221121` | forced `e = 2` gives `E = 0`, need 1 |

In every case the killer is the `E`-miss of the forced symbol (the `H`-forced
symbol exists, as 9.5 of `RESULTS-RW-LINEAR-SLACK.md` requires), never a
missing forced symbol and never hard-core alone.  At `n = 9` the forced
symbol is also a hard-core `11`, but the `E`-miss already kills.  The
`T[u][n]` trajectory is `c` throughout the plateau by construction; the
death-level window, `|Z|`, `|W2|` and diagonal are identical across a fibre
because the state is.

## 3. The state census: sources versus distinct states

Counting survivors by distinct endpoint state instead of by source
(`--census 16`, entries `sources/states/max-fibre` per level):

```text
n=9  c=3: 512/232/8 214/84/8 112/40/8 53/16/6 23/6/6 6/1/6 6/1/6 6/1/6 6/1/6
n=12 c=2: 4096/1329/16 1607/451/18 752/187/18 278/72/18 119/29/18 33/12/7 14/5/4 6/2/4 2/1/2 2/1/2
n=16 c=3: 65536/13382/46 24909/4325/52 10412/1787/39 3977/688/32 1698/291/32 625/116/24 234/49/18 99/19/16 54/8/16 28/5/10 18/2/10
```

The `half-survivor-step` kill (`6, 6, 6, 6` at `n = 9, c = 3`, ratio 1.0)
reads `1, 1, 1, 1` in states: one orbit.  The plateaus are always a single
state or two.

The number of distinct states at `k = 0` is `39, 73, 129, 232, 410, 742,
1329, 2376, 4265, 7560, 13382` for `n = 6..16`, successive ratio `1.77`
against `2` for sources; the mean fibre at `n = 16` is `4.9`.  The
per-level survival ratio in states is `0.32, 0.41, 0.39, 0.42, 0.40, 0.42,
0.39, 0.42` at `n = 16, c = 3`, the same `~0.4` as in sources: fibres are not
concentrated on survivors.  `(Q_n, Psi_n)` from `psi()` is coarser than the
endpoint state (`3398` versus `4265` values at `n = 14`) and is not by itself
a sufficient statistic for the orbit; the full `column` is.

## 4. What this settles and what it does not

- The "synchronized phase catastrophe" of `RESULTS-BINARY-WEDGE-HORIZON.md`
  section 5 is the fibre of one state.  Retire that phrase.
- Reconciles with 9.2 of `RESULTS-RW-LINEAR-SLACK.md` ("no effective
  forgetting"): inside a fibre the prefix is forgotten completely; across
  fibres of a fixed suffix, survival halves per prefix bit.  9.2 measured the
  second; this measures the first.  Same map as the near-alternating `Psi`
  kernel of BACKLOG.md section 16.
- It does not give a proof route.  The state space grows like `1.77^n`, the
  survival rate per level in states matches the rate in sources, and the
  survivor counts at the deepest levels are 1 or 2 states either way.  Any
  entropy argument can be run on states instead of sources, which removes
  the `2^n` overcount but not the `0.4` per-level rate that is the actual
  target.

## 5. Reproduction

```sh
uv run python cluster_anatomy.py --extra --census 16   # about 3 minutes
```

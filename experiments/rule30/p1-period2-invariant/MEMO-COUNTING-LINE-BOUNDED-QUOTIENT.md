# Memo: bounded-quotient check for the `N_j <= C*2^(n-j)` counting line

Date: 2026-09-04. Scope: BACKLOG.md section 17, the `counting line` row
(`N_j <= C 2^(n-j)`, empirically `C=3` tight at `n=9`, target `C<4` for
`(RW)`). Question asked: does the recursion generating `N_j` reduce to a
bounded finite-state (Myhill-Nerode) process, the way `H_r(n)`'s bounded-state
question is being checked elsewhere today, so that `C<4` could become a
proven eigenvalue/automaton bound instead of an exhaustive-to-`n=18` census?

## What `N_j` is

From `block_halving.py`/`flip_pairing.py`: `W` ranges over binary sources in
`{1,2}^n`. Each `W` produces a forced continuation via `psi_kernel.Endpoint`
(the same `H`-forced/`E`-defect kernel used throughout this directory). `W`
is "alive at level `j`" if, for every `j' < j`, the forced cell at column `n`
equals the target `c` and the forced symbol is hard-core (no `11` at the
junction). `N_j = |S_j|` is the count of length-`n` sources alive through
level `j`. The state carried forward per source is `psi_kernel.Endpoint`'s
`(column, diagonal)` pair, which is the *entire* history-dependent state:
column `i` depends on `endpoint[:i+1]` (see `psi_kernel.py` docstring), so it
is triangular/full-length by construction, not a fixed-width summary.

## Check performed

`counting_line_quotient_check.py` (new, this task) reuses
`flip_pairing.census()` (untouched) to get, for `n=9..15` and both `c`, the
raw `Endpoint` key and the forced `(sym, cell, hardcore)` sequence per source.
For each level `j` it counts, among survivors `S_j`:

- `raw`: distinct raw `Endpoint` states (`keys`) — already tracked as the
  "states" column in `block_halving.py`.
- `sig`: distinct **future-behavior classes**, i.e. distinct forced
  `(sym, cell, hardcore)` sequences over the next `W=8` levels. This is the
  actual Myhill-Nerode quotient of interest: two sources with different raw
  states but identical forward behavior would still support a bounded
  automaton; `raw` alone would not detect that.

Both are stronger checks than needed for a lower bound on the true minimal
quotient size, since `sig` only requires 8 levels of look-ahead, not the full
future.

## Result: no bounded state found (negative)

At every fixed level `j`, both `raw` and `sig` counts grow with `n` at
essentially the same rate as `N_j` itself, with no sign of saturation:

```text
j=0 sig count:  n=9..15 -> 188, 350, 596, 1075, 1911, 3338, 5807
j=0 raw count:  n=9..15 -> 232, 410, 742, 1329, 2376, 4265, 7560
```

Ratio `sig(n+1)/sig(n)` is consistently ~1.7-1.85, i.e. exponential growth in
`n`, not convergence to a constant. The same pattern holds at every checked
`j=0..5` and both `c=2,3` (full table in the script's stdout; representative
rows also below). If a bounded finite-state process existed, `sig` would
plateau to a fixed integer as `n` grows for fixed `j`; instead it tracks
`N_j` up to a slowly-shrinking-but-nonzero ratio (`sig/N_j` falls from ~0.37
at `n=9,j=0` to ~0.18 at `n=15,j=0`, a much slower decay than the exponential
growth of `sig` itself).

```text
n=15 c=2: j=0:N=32768,sig=5807  j=1:N=12134,sig=2204  j=2:N=4829,sig=902
          j=3:N=1680,sig=323  j=4:N=727,sig=134  j=5:N=272,sig=47
```

Conclusion: **no bounded Myhill-Nerode quotient exists** for the process
generating `N_j`. The number of behaviorally-distinct residual states at any
fixed level grows exponentially in `n`, so no fixed-size transfer
matrix/automaton can replace the empirical `C<4` census with a proven
eigenvalue bound the way a bounded-state reduction would for `H_r(n)`. This
is consistent with, and sharpens, two already-recorded negative results in
this directory:

- "Fixed finite quotient of the frontier" (`PROOF-STATE-CAPSULE.md` section
  5): a fixed quotient collides same-summary/different-future sources.
- The single-flip pairing kill (`RESULTS-FLIP-PAIRING.md`,
  `flip_pairing.death_profile`): a flip at any source position beyond the
  first three symbols has the *same* ~`0.4^j` effect on later survival
  regardless of how far back it is, which is itself the signature of
  unbounded memory — a genuinely finite-state/bounded-window process would
  make a sufficiently old flip invisible (probability of unaffected outcome
  -> 1), not flat.

The `C<4` counting-line target therefore has no available shortcut via a
computable finite-state eigenvalue argument. It remains exactly what BACKLOG
section 17 already says: an empirical census (`C=3` tight at `n=9`, held
through `n=18`), not a theorem, and no structural reduction found here closes
that gap. Any future proof of `C<4` will have to argue directly about the
unbounded-state process (e.g. via the dependency-diagonal/pushdown angle
proposed in BACKLOG section 18, or a genuine induction on the full `Endpoint`
state), not via a bounded automaton spectral radius.

## Artifacts

- `counting_line_quotient_check.py` — the check script (new; reuses
  `flip_pairing.census`, does not modify it or any restricted file).
- Full run log for `n=9..15`, both `c`: reproduce with
  `PYTHONDONTWRITEBYTECODE=1 uv run python counting_line_quotient_check.py --min-n 9 --max-n 15`.

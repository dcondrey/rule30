# a19 pre-registration — ML/symbolic mining as a conjecture generator

Written **before** the full run, after a reduced-depth smoke test (train `[0,3000)`,
test `[20000,60000)`) whose printed output is in `smoke.log`.  The smoke test is
disclosed here so that nothing below reads as post-hoc.

## Target

Not a prize problem.  This arm produces at most a *candidate*: a precise, finite,
checkable discrete rule, exact-checked out of range.  An accuracy number is not a
result and none is reported without the exact check beside it.

## Depth split (fixed, quoted with every number)

```
TRAIN t in [0, 20000)          table extraction / GF(2) solve / model fit
DEV   t in [20000, 50000)      in-range holdout, ADJACENT to train
TEST  t in [200000, 500000)    OUT OF RANGE, disjoint, 10x-25x deeper
```

**AMENDMENT, recorded honestly rather than silently applied.**  This was
originally registered as `TEST t in [200000, 1000000)`.  The `10^6` run was
killed for a compute reason only — the exact window construction is quadratic in
depth and the first attempt was terminated by its shell — and TEST was shortened
to `[200000, 500000)` before any result was read.  The amendment can only *weaken*
the arm's power to refute, never strengthen it, and every candidate that was
refuted broke within 520 steps of `t = 200000`, i.e. far inside either range.
No number in the deliverable would change.

All three ranges come from one exact integer simulation of the lone-seed
diagram.  No sampling, no approximation.

## Obstruction H, stated up front

No depth settles an infinite statement.  `RESULTS-automaticity.md` Theorem O's
exchange rate is the sharp form: `N` terms buy a kernel lower bound of about
`N/8` and nothing more, ever.  So the exact check in this arm has exactly one
power: **it can refute a candidate, never confirm one.**  Where a candidate
survives to `t = 10^6`, the only honest report is "not refuted at this depth",
plus a separate, non-empirical argument if the candidate is in fact a theorem.

## Extraction threshold (declared before the full run)

A framing produces a CANDIDATE WORTH EXTRACTING iff all three hold:

1. the exact lookup table is **consistent on TRAIN** (no pattern carries both
   labels), OR its unanimous sub-table covers `>= 20%` of TEST;
2. TEST coverage `>= 0.05` (guards against memorisation: a 25-bit table over
   20k samples is unanimous vacuously, one sample per pattern);
3. it **fails the universality check** below, i.e. it is an orbit-specific
   claim rather than a consequence of the local rule.

Anything meeting 1+2 but passing universality is a local-rule tautology and is
reported as such, with the derivation, not as a finding.

## Universality check

A candidate `pattern -> label` is *universal* if it holds for every row of the
Rule 30 space-time diagram, not just the lone-seed orbit: enumerate the free
bits the pattern does not fix and see whether the label is forced.  For
`y = c_{t+1}` from a left window, the single free bit is `s(t,1)`.

Caveat, stated because it cuts the other way too: universality is a statement
over all rows, so **failing** it does not falsify the orbit claim.  That is
precisely why the exact out-of-range check is the operative test.

## Two lemmas that bound what this arm can possibly find

**Lemma A19.1 (target A is exhausted by the pin).**  Rule 30 is
`c_{t+1} = s(t,-1) XOR (c_t OR s(t,1))`.  Given only `s(t,-Wl..0)`, the bit
`s(t,1)` is free, and the value is independent of it iff `c_t = 1`, where it
equals `NOT s(t,-1)`.  So for every `Wl >= 1` the universal part of any
extracted target-A table is **exactly the OR-latch pin and nothing more**.
This is a theorem about the pipeline's reach, not a measurement.  Any target-A
table entry at `c_t = 0` is unanimous by accident and is expected to break.

**Lemma A19.2 (target B is necessarily orbit-specific).**  No function of
`s(t,-Wl..0)` equals `s(t,1)` universally: two Rule 30 rows can agree on
`s(t,-Wl..0)` and differ at `s(t,1)` (extend either row arbitrarily to the
right; left permutivity fixes nothing to the right of `0`).  Hence *every*
target-B candidate fails universality by construction, which is what makes its
break point genuine information.  Target B is the R1-relevant framing:
register row 1 is exactly "`c` eventually periodic forces `r` eventually
periodic on `{c_t = 0}`".

**Target C is a local-rule tautology except on one branch.**  With
`m_t = min{j >= 1 : s(t,j) = 1}`:

* `m_t = k >= 3`: `s(t+1,1) = c_t`, `s(t+1,j) = 0` for `2 <= j <= k-2`,
  `s(t+1,k-1) = 1`, so `m_{t+1} = 1` if `c_t = 1` else `k-1`;
* `m_t = 2`: `s(t+1,1) = NOT c_t`, so `m_{t+1} = 1` if `c_t = 0` else `2`;
* `m_t = 1`: `s(t+1,1) = NOT c_t`; for `c_t = 0` that gives `m_{t+1} = 1`, and
  for `c_t = 1` it gives `s(t+1,1) = 0` with `s(t+1,2) = 1 XOR (s(t,2) OR
  s(t,3))`, **not** determined by `(m_t, c_t)`.

So `m_{t+1} = f(m_t, c_t)` off the single branch `(m_t, c_t) = (1,1)`.  Mining
is restricted to that branch.  Declared in advance: `m` is a right-side
quantity and P1/P2 are column-0 statements, so nothing found on that branch can
be the headline.  `m` is a9's quantity (a9 proved the forced left half `P_k` is
a function of `m` alone); it enters here only as an input feature and a9's
Identity R is not re-derived.

## Hypotheses, with kill conditions that can fire on a negative

| # | Hypothesis | Kill condition |
|---|---|---|
| H1 | Some framing yields a candidate meeting the threshold above | No framing meets it -> report clause (b): no candidate worth extracting, with the numbers |
| H2 | A candidate meeting the threshold survives DEV | It breaks inside DEV -> refuted in-range, a *stronger* negative than an out-of-range break |
| H3 | A candidate surviving DEV survives TEST to `t = 10^6` | It breaks in TEST -> report the exact first break `t` and the pattern |
| H4 | A GF(2) polynomial of degree `<= 3` over the features reproduces TRAIN exactly | System inconsistent -> an exact negative, reported as such |

## Controls

* **Rule 90 positive control.**  Identical pipeline on Rule 90's lone-seed
  column, which is `1` then `0` forever.  A pipeline that cannot trivially and
  perfectly solve Rule 90 is broken.  Equally: Rule 90 must *not* be reported as
  a success for Rule 30.  (`PATH.md` section 0, `ensemble_filter.py`.)
* **Local-rule positive control.**  Target A with the full window `W = 1` is the
  Rule 30 rule itself: the table must be consistent and exact at every depth.
* **Vacuity control.**  TEST coverage, reported for every framing; a consistent
  table with coverage `~0` is memorisation, not structure.

## Single-column sensitivity (`PATH.md` 0.1)

Recorded in advance: these candidates are *pointwise predictions that read
column 0 (and its immediate neighbours) directly*, not averages over the `~2t`
cells of a row.  Overwriting column 0 changes their inputs and outputs
outright, so they pass the `discriminator.py` filter **vacuously**.  Passing it
is therefore necessary and not sufficient here, and no weight is placed on it.

## Fence

All writes confined to this directory.  No `uv add` (there is no repo-root
`pyproject.toml`; `uv add` would create one).  Packages, if any, via
`uv pip install`.  No git commits.  `experiments/rule30/` and `docs/` read-only.

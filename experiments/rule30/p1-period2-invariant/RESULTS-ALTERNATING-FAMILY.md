# The alternating source family: closed form for zero defects, none for one

Date: 2026-09-16. Scripts and logs in `alternating-family/` (`alt_family.py`,
`one_defect.py`, `one_defect2.py`, `one_defect3.py`, `one_defect4.py`; record
`one_defect2_kE.json`). Kernel `psi_kernel.py` (`Endpoint`, `psi`). No
pre-registration: this is the first look at a family, with the expected
outcome stated beforehand in the session as "a closed form on periodic
sources and a phase-shift law for one defect". The first half held, the
second did not.

**`[C]` For the pure alternating sources `W = (12)^k`, `k = 2..60`, the endpoint
state has a closed form: the anti-diagonal after `W` is the window
`D[2k-4 : 4k-4]` of one sequence `D` of period 28 (block
`0303 0300 0312 0311 1230 0323 2120`), and the column grows by one prepended
pair per `k` with the pair sequence of period 14 in `k`
(`03 03 03 00 13 02 13 11 32 00 23 23 21 00`) over a fixed bottom. `(21)^k`
obeys the same laws with a rotation of the same period-28 block and the same
14-cycle of pairs rotated. On this family the forced continuation's cut run is
`k_E <= 3` (`c = 2`) and `<= 5` (`c = 3`) at every `k <= 60`, so `(PSI)` holds
on it with the whole scale to spare. One inserted symbol destroys this. For
`W = (12)^a 2 (12)^b` the column's prepend law fails exactly for
`1 <= b < a`, with the disturbance retreating two entries per period from the
front and healing at `b = a`, after which the column is again a period-14
pair stack, but with a different 14-cycle; the anti-diagonal never returns to
window form: for every `a <= 40` and `b <= 95` it is not a factor of the
period-28 sequence and the shift-by-two law fails at every `b >= a`; at `a = 5, 10, 20`
no shift of at most 6 relates consecutive periods. The cut run on the
one-defect family is at most 11 through `n = 271` (3,124 words, `a <= 45`,
`b <= 70`, plus `a <= 40`, `b <= 95`), against the need `n + 2`, and for fixed
`a` it has no period of length at most 40 in `b`. So the phase a proof by
induction on defects would carry does not exist even for one defect: the
defect's history lives in the anti-diagonal, which is rewritten in full at
every step thereafter, while the column forgets it after as many periods as
the prefix had.**

## 1. Objects

`Endpoint` (psi_kernel.py) holds a column and an anti-diagonal over
`{0,1,2,3}`. Appending `s` recomputes the column from the top,
`new_column[i] = CONE[column[i+1]][new_column[i+1]]` seeded by `BOUNDARY[s]`,
and the anti-diagonal from the seed `new_column[0]`,
`new_diagonal[j+1] = CONE[diagonal[j]][new_diagonal[j]]`; the cut cell is
`new_diagonal[n]`. `CONE = ((0,1,3,2), (3,2,1,0), (3,2,0,1), (3,2,1,0))`,
`BOUNDARY = (3,2,1,0)`; every row of `CONE` is a permutation. `psi(W)` gives
the H-forced continuation of length `n + 2` and the low-bit word; `k_E(c)` is
the first forced step at which the cut's low bit leaves `c`, and `(PSI)` is
`k_E(c) < n + 2` for both `c` (`PROOF-STATE-CAPSULE.md` section 2). The
sources `(12)^k` are realizable (`10101...` avoids every recorded forbidden
factor); `1^k` and `2^k` are not (`11` and `00000` are forbidden), so the
alternating family is the simplest reachable one.

## 2. Zero defects: the closed form

For `k = 2..60` (`alt_family.log`):

- Anti-diagonal: `diag((12)^k) = D[2k-4 : 4k-4]` with `D` periodic of period
  28, block `0303030003120311123003232120`. Consecutive `k` drop two symbols
  at the old end and append four at the young (cut) end.
- Column: `col((12)^(k+1)) = p_k + col((12)^k)` with `p_k` the pair sequence
  `03 03 03 00 13 02 13 11 32 00 23 23 21 00` repeated (period 14 in `k`,
  no preperiod from `k = 2`), over the fixed bottom `0003030300212`.
- `(21)^k`: block `1112300323212003030300031203`, a rotation of the `(12)`
  block; pairs `11 32 00 23 23 21 00 03 03 03 00 13 02 13`, the same
  14-cycle rotated.
- Cut runs: `k_E(2)` takes values 0 to 3 and is periodic in `k` with period
  28 from `k = 10` (`k = 10..23` equals `k = 38..51`); `k_E(3)` takes values
  0 to 5 and has no period of length at most 28 on `k <= 60`.

This matches, and identifies with the endpoint process, the finite census of
`RESULTS-DYADIC-PERIODICITY.md` (endpoint periods 2, 3, 4 give inverse-cut
period 28) and its proved dependency cone (`Z_t[k]` depends on endpoint
coordinates `k + floor(t/2) .. k + t`), which is the window `[2k-4, 4k-4]` in
these coordinates. The identification is made here for the first time; the
earlier document works on an infinite periodic endpoint, this one on the
finite prefix and its column.

What a proof of the closed form needs, not done here: the append acts on the
anti-diagonal as a fixed 4-state transducer (`RESULTS-PSI-ANCESTRY-LAW.md`
section 5, transition monoid `D8`), so "window shifts by two per period" is
the statement that the transducer over one period of `D`, with the seed the
column supplies, returns to its state; that is a finite check on one period
plus an induction on the number of periods, and the same for the column
chain over one period of pairs. The cut runs then follow from at most six
further transducer passes, each again over a periodic object; `(PSI)` on the
pure family would be a computer-checked theorem. It is written up here as
verified structure, not as a proof. Done the same day in
`RESULTS-PSI-ALTERNATING-PROOF.md`: the closed form is one period-28 sequence `D` with
`T[2k-1][d] = D[(2k+d) mod 28]` (the "bottom" here is `D[12..0]`, not a separate object),
and `k_E(2) <= 3`, `k_E(3) <= 6` for every `k >= 2`; the bound 5 above is a `k <= 60`
artefact, `k_E(3) = 6` first at `k = 144`.

## 3. One defect: the column heals, the anti-diagonal does not

`W = (12)^a 2 (12)^b`, the simplest reachable perturbation (inserting a `1`
creates `11`). Grid `a = 2..45`, `b = 0..70` (`one_defect2.log`) and
`a = 2..40`, `b = 0..95` (`one_defect3.log`).

Column. The prepend law `col(a, b) = pair + col(a, b-1)` fails exactly for
`1 <= b < a` (990 of 990 such cells fail, no other cell does). The failing
entries form a front segment that retreats two per period: at `a = 10` the
differing positions span `(0, 18), (2, 15), (0, 13), (0, 11), (0, 9), (1, 7),
(0, 5), (0, 3), (0, 1)` at `b = 1..9` and none at `b = 10`; at `a = 30` the
span is `(0, 58)` at `b = 1` and `(0, 1)` at `b = 29`. For `b > a` the
prepended pairs are again periodic with period 14 in `b`, but the 14-cycle is
not a rotation of the pure family's at any `a <= 40`.

Anti-diagonal. `diag(a, b)` is a factor of the period-28 sequence for no
`(a, b)` with `a <= 40`, `b <= 95` (`one_defect3.log`; the `a <= 45`, `b <= 70` grid ran no factor test). At `a = 5, 10, 20` and `b = a..a+35` (`one_defect4.log`) no shift `sigma <= 6` satisfies
`diag(a, b+1)[: L - sigma] = diag(a, b)[sigma :]`, and the number of leading
symbols consecutive diagonals share is 0, 2 or 4 in a 14-periodic pattern.
Sample at `a = 5`:

```text
b=5  230303211232323030312
b=6  00323030303212003121212
b=7  3232120323030303030321200
b=8  321200303112030300031203120
b=9  12003030300321212031230303030
```

The material is the pure family's (`030303`, `121212`, `3232`), rearranged
in full every period. The mechanism is the chain: the seed `new_column[0]`
of every anti-diagonal pass is read off the column, the pass runs end to end,
and once the seeds leave the pure family's cycle the whole line changes.

Cut runs. Maximum `k_E` over both tails: 8 on `a <= 24`, `b <= 24` (575
words; at `(3, 22)`, `(8, 23)`, `(13, 20)`), 11 on `a <= 45`, `b <= 70` (3,124 words; histogram 1: 1591, 2: 748,
3: 397, 4: 199, 5: 98, 6: 42, 7: 27, 8: 13, 9: 2, 10: 5, 11: 2; argmax
`(9, 41)` and `(18, 65)`, `n = 101` and `167`), 11 on `a <= 40`, `b <= 95`.
For fixed `a` and `b >= a` the sequence `b -> k_E` has no period of length at
most 40 (`b <= 95`), and `k_E` is not a function of `(a mod m, b mod m)` or
`(a mod m, (b - a) mod m')` for `m, m' in {14, 28, 56}` (every residue class
with more than one member disagrees, 598 of 784 at `m = 28`).

Gap in the grids: `a` starts at 2. The single word at `n = 17` that meets the
charge bound of `RESULTS-EVENTUAL-CONSTANT-TAIL.md` (12) with zero slack,
`1 22 (12)^7` at `c = 2` (run 10 against nine `2`s), is this family at
`a = 1`, `b = 7`: the extremal one-defect sources put the defect first and
alternate afterwards. Rerun with `a` from 0 (`one_defect2_a0.py`, log
`one_defect2_a0.log`, whose settled-regime section aborts at `a = 0` and is
not needed): over `a = 0..45`, `b = 0..70` the maximum `k_E` is 13, attained
only at `(a, b) = (1, 7)`, that word; the prepend law still fails at every
`1 <= b < a` (`RESULTS-CHARGE-INJECTION-PROBE.md`).

## 4. Reading

The question posed here was whether the reconstruction map has a
closed form on the alternating family with one defect, so that an induction
on defects could carry a finite phase. The answer is: closed form with zero
defects (section 2), no finite phase with one (section 3). The column does
carry a finite phase after a defect, but only after a transient exactly as
long as the prefix before the defect, and the anti-diagonal never does. This
is the smallest exact instance of the archive's diagnosis (capsule section
5: "a growing ordered dependency diagonal stores phase in long gaps"), and it
agrees with `RESULTS-COLUMN-DECOMPOSITION.md`: the merge and memory mechanism
is the anti-diagonal, not the column.

For `(PSI)`: the pure family is provable and has slack `n - 3` or more; the
one-defect family has slack at least `n - 9` through `n = 271` and no
residue structure to prove it from. Two defects would inherit the aperiodic
anti-diagonal of one. A proof on the family therefore needs a bound on the
cut run that does not go through periodicity of the state, which is the
same object every route in the capsule is missing. What is new is the
negative form: even the smallest reachable perturbation of the one source
whose state is periodic leaves nothing periodic to induct on.

## 5. Scope

Finite: `k <= 60` for the pure families, the two one-defect grids above, one
implementation (`psi_kernel.py`, not independently re-implemented here; the
pure-family laws are consistent with the independently derived dependency
cone of `RESULTS-DYADIC-PERIODICITY.md`). No pre-registration. `(PSI)`,
`RW`, `SEP`, `PT2` untouched.

## 6. Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --no-project python alternating-family/alt_family.py      # 2 min
uv run --no-project python alternating-family/one_defect.py      # 1 min
uv run --no-project python alternating-family/one_defect2.py alternating-family/one_defect2_kE.json   # 4 min
uv run --no-project python alternating-family/one_defect3.py     # 8 min
uv run --no-project python alternating-family/one_defect4.py     # seconds
```

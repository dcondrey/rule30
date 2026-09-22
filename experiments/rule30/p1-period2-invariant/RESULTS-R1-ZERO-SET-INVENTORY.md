# R1 (zero-set obligation): inventory of `uc/r1-r1zero/`, and what it does and does not establish

Date: 2026-09-04 (late).
Everything below was re-derived against the real code; nothing is relayed
from a prior document.

## What is in `uc/r1-r1zero/`, and what each run actually showed

All logs are from 2026-09-03; all completed (elapsed lines present). None
crashed. In particular the three `lhp_lock_search*` logs are small because the
searches **found nothing**, not because they died: each carries a `runs=`
count, a violation rate, and an `elapsed` line.

| file | what it ran | outcome |
|---|---|---|
| `forward_pair_law.py` | exhaustive 16-case check of the forward `(H,E)` law; lone seed `T=2000` | 0 failures on all three checks (3996+3996+1023) |
| `driven_halfplane.py` | 23 primitive words `p=1..6`, 2 prefixes, `T=4096`; RHP `r|Z`, LHP `l`, pin violations; **includes Rule 90 controls** | `r|Z` eventually periodic in **10/44** drives; LHP `l` in **0/44** |
| `prefix_dependence.py` | 9 words, 11 prefixes each, `T=16384`, `q<=1024` | strongly word-dependent: `0001`,`0011`,`0111` periodic 11/11; `01` 1/11; `011`,`00101` **0/11** |
| `drive01_deep.py` / `drive01_long.py` | period-two drive to `T=65536` / `T=524288`, `q<=4096` | **no eventual period found**; `r|Z` density flat at ~0.214 across 16 blocks, all four prefixes |
| `pin_survival.py` / `pin_survival2.py` | pin-survival horizons over `Pi`-leaves, `L` up to 36 | max survival 13-35 depending on tail; `atcap=0` everywhere (cap 400 never reached) |
| `comoving_columns.py` | comoving column scan to `T=32768` | (log present, 13 KB; not re-derived) |
| `lhp_lock_search.py` / `_y.py` | 231 primitive words `p<=7` x 61 prefixes, `T=2048`; also `p<=4` at `T=8192` | **0 lock candidates** in every run; second-half pin-violation rate **0.4993-0.5001** against a null of 0.5; longest violation-free tail 14, 9, 65 |

## Two identities, re-verified

`scratchpad/verify_lhp_closure.py`, lone seed, `T=400`, full LHP window
`x in [-400,-1]`:

```
pin   c_t=1 -> l_t = NOT c_(t+1)      : 207 tests, 0 failures
pass  c_t=0 -> l_t = c_(t+1) XOR r_t  : 193 tests, 0 failures
LHP reconstructed from c alone vs true LHP: 0 mismatches
```

The third line is the structural fact worth stating plainly, and it is stronger
than the pin alone:

> **The entire left half-plane `x <= -1` is a function of the centre column `c`
> and the LHP's own `t=0` data.** No knowledge of `r` is required. This is
> because Rule 30's stencil is `{x-1,x,x+1}`, so evolving `x <= -1` needs only
> `x = 0`, which is `c`.

Consequently the pin is a **self-consistency condition on `c` together with the
LHP initial data** — it never mentions `r`. That is why `lhp_lock_search` is
the right instrument, and it is also exactly why its result is weaker than it
looks.

## The over-read to avoid, and the lemma that blocks it

The tempting reading of "0 lock candidates over 14091 runs, violation rate
0.5001" is: *a periodic `c` cannot sustain the pin, therefore `c` is not
eventually periodic.* **That reading is wrong**, for two independent reasons.

1. **`lhp_lock_search` fixes the LHP initial data to all zeros.** It varies the
   prefix of `c` and the periodic word, never the left half. It therefore
   probes one initial-data family, not the space of finite rows.

2. **`docs/rule30/RESULTS-eventual-period.md` already proves the blocking
   lemma** ("PROVED finite-prefix lemma"): for any finite desired trace
   `tau_0..tau_N` and any compatible right prefix, left permutivity supplies a
   unique `L_1..L_N`, and zero padding gives a finite row matching that trace
   through time `N`. So *no contradiction can depend on a bounded number of
   centre symbols independent of support size*. Pin survival must grow with
   support radius `w`, and the same document's SMT table shows it does:
   `H(p=2,w) = 6,6,6,6,8,9,9,14` for `w=1..8`. (`H` there is the maximum
   *periodic-prefix* horizon under full Rule 30 consistency — SAT through `H`,
   UNSAT at `H+1` — not a pin-only horizon. Full consistency subsumes the pin,
   so `H` upper-bounds any pin-only survival horizon.)

   The `lhp_lock_search` tails (9, 14, 65) must **not** be compared to `H`
   numerically: they count pin violations only, they are measured over a
   window `[T/2, T)` rather than from `t=0`, and the 65 is a run ending at the
   window's right edge, so it is a truncation artefact rather than a horizon.
   The two measurements are different objects. The argument above does not
   need them to agree — it needs only that `lhp_lock_search` varies the prefix
   and the word while holding the left half fixed at zero.

**Verdict: `lhp_lock_search`'s zero-lock result adds no exclusion beyond the
existing `H(p,w)` table.** It should not be cited as evidence against eventual
periodicity. Its real content is a calibration: at LHP-init zero the pin fails
at the null rate 1/2, i.e. a periodic drive buys no pin advantage at all.

## Why the lone-seed version of R1's probe is trivial (and so cannot be the target)

`scratchpad/direct_lone_seed_period.py`, `T=20000`, **0.1 s**: for the lone
seed, no period `p <= 64` has any onset `<= T/2`. Eventual periodicity of the
*lone-seed* centre column with bounded period and bounded onset is refuted by
computing `c` directly; the pin, the LHP reconstruction and the SAT grid are all
strictly more expensive ways to learn less. Any probe whose statement is
lone-seed-specific is therefore not worth building. **The target must quantify
over all finite rows** (equivalently, over support radius `w`), which is what
the `H(p,w)` table and the `n<=29` SAT grid already do.

This retires seed task 34 as stated ("assume `c` periodic with period `p`, test
whether `r` on `{c_t=0}` is forced periodic, start at small `p`") in its
lone-seed form. The general form is item R1-b below.

## The R1 forcing hypothesis is already answered, and the answer is NO

R1 needs: `c` eventually periodic `=>` column `-1` (or `+1`) eventually
periodic, which then contradicts Jen 1990 Prop. 3 / Kopra Thm 3.5.

`prefix_dependence_T16384.log` and `drive01_long_T524288.log` answer the
right-hand version directly, in the driven-RHP model:

- word `01` (period 2): **no** eventual period `q <= 4096` at `T = 524288`, for
  all four prefixes, with `r|Z` density flat at 0.214.
- words `011` and `00101`: 0/11 prefixes periodic.
- words `0001`, `0011`, `0111`: 11/11 prefixes periodic.

So a periodic `c` **does not force** `r|Z` periodic. Whether it does depends on
the word. A proof of R1 therefore cannot run through a forcing argument on the
driven right half-plane alone; it must use global consistency (a real diagram
constrains `c`, `r` and the LHP simultaneously, and the driven model does not).

Note the direction of this result: it is a **negative for the cheap route**, not
a refutation of R1 itself. R1 concerns genuine Rule 30 diagrams from finite
seeds, and the driven RHP with an arbitrary prefix is not one.

## Rule 90 filter (seed task 35), applied explicitly

Rule 90's centre column from `{-1,1}` is identically 0 (periodic) while
`r_t = 1` iff `t = 2^j - 1` (aperiodic), so R1's implication is FALSE for
Rule 90 and any rule-generic argument is wrong.

- **Pin-based arguments: PASS the filter.** Rule 90 has no OR, so `c_t = 1`
  saturates nothing and there is no pin. Moreover the filter's degenerate case
  is handled correctly rather than accidentally: with `c` identically 0 the pin
  has *no tests to fail* (`ones = 0`), so a pin argument is vacuous exactly
  where the statement is false. `RESULTS-eventual-period.md` records the same
  behaviour on the SMT side (the Rule 90 row `{-1,1}` is retained at every
  horizon rather than manufacturing UNSAT).
- **Driven-RHP forcing arguments: moot.** They are dead on Rule 30's own
  evidence above, before the filter is needed.
- `driven_halfplane.py` already carries the Rule 90 control inline and
  reproduces `ones at t = [1,3,7,15,31,63,127,255,511,1023,2047,4095]`, i.e.
  `2^j - 1`. **Any future probe must take the step function as a parameter and
  be run against `rule90_step` before a Rule 30 positive is believed.**
  `r1zero_lib.rule90_step` already exists; use it.

## Seed task 36: does `phi/4` say anything about the density of `{c_t = 0}`?

**No — the types do not match. One line, as pre-agreed, and then stop.**

`phi/4 = 0.404508` is the leading eigenvalue of the transfer matrix
`[[0,1/4],[1/4,1/4]]` governing **per-row survival in the rotated wedge** over
the `H`-population, an object defined on words of length `n` in a truncated
combinatorial construction. Problem 2 is a statement about the **symbol density
of the true lone-seed centre column**, measured at
**0.500362 over `T = 200000`** (10.6 s) — consistent with 1/2 and unrelated to
0.404508.

Caution for anyone tempted by `drive01_long`'s `|Z| = 262144 = T/2`: that is
`T/2` **by construction**, because the drive imposes `c = (01)^inf`. It is not
evidence about the real centre column's density.

## VALIDATION (not a finding): `H(2,w) >= w`, confirmed constructively to `w = 300`

**This is a corroboration of a lemma already proved in the repo, not a new
result.** The finite-prefix lemma in `docs/rule30/RESULTS-eventual-period.md`
states it directly: for any finite desired trace `tau_0..tau_N` and any
compatible right prefix, left permutivity supplies a unique `L_1..L_N` and zero
padding gives a finite row matching the trace through time `N` — a row of
support radius `~N`. So `H(2,N) >= N` follows with no measurement at all, and
the same document already draws the operational conclusion in words ("no
contradiction can depend only on `p` or on a bounded number of centre symbols
independent of support size"). What the run below adds is an implementation
check, a numerical reach of `w = 300`, and a Rule 90 control. It is labelled
validation so an expected result is not later mis-cited as a discovery — the
failure mode behind several prior retractions.

The practical call it settles is still worth stating: **do not spend SMT
compute on `w = 9,10,11`.**

The measurement looked like "extend the `H(p,w)` table to
`w = 9,10,11` and see whether it plateaus". **That measurement is void: a
plateau cannot occur, and the reason is the same finite-prefix lemma used above
to retire `lhp_lock_search`.** Applied to `H` itself: truncate `(01)^inf` at
`N`, pick any compatible right prefix, let left permutivity supply `L_1..L_N`,
zero-pad. That is a finite row of support radius `~N` whose centre trace matches
`(01)^inf` through time `N`. Hence `H(2,w) >= w` for every `w`, and `H` is
unbounded.

Measured constructively rather than argued, in **0.04 s**
(`uc/r1-r1zero/h_horizon_lower_bound.py`, log alongside). The construction
prescribes the trace, takes the **empty** `t=0` right half, derives
`s(0,-1..-D)` by left permutivity, and then evolves the resulting finite row
with the ordinary Rule 30 evaluator — so the derivation is never trusted, only
the measured horizon:

```
rule 30, trace (01)^inf, empty right half:
   D   support radius w   true horizon H   H - w
   4                  1                6       5
   8                  7                8       1
  16                 16               17       1
  32                 31               32       1
  64                 64               65       1
 128                127              130       3
 200                199              200       1
 300                300              302       2
```

`H - w` stays in `{1,2,3,5}` out to `w = 300`, so empirically
`H(2,w) = w + O(1)`, not merely `>= w`. This is a **lower bound** on the table's
`H(2,w)` (the table maximises over all rows of radius `w`, this family has
support in `[-w, 0]` only), and it is consistent with every published cell:
`H(2,1) = 6` is reproduced exactly, and `H(2,7) >= 8` sits under the table's 9.
It extends the reach of the **lower bound** by a factor of ~37 at zero SMT
cost. It does **not** extend the table: `H(2,300)` is not a table value, since
the table maximises over all rows of radius `w` and this family does not.

**Consequences.**

1. The plateau branch is closed; there is no uniform horizon bound to find.
2. A kill condition of the form `H(2,w) > w + c` is the wrong test. The one
   drafted earlier (`c = 8`) would not even have fired on the
   existing data: `H(2,8) = 14` against `w + 8 = 16`.
3. Each `w` still yields a genuine exclusion — no row of radius `<= w` has an
   eventually period-2 centre trace — but the horizon needed grows at least
   linearly in `w`, and no finite `w` covers all finite rows. **Extending the
   SAT/SMT grid cannot close R1 or the `p=2` exclusion.** A structural theorem
   is required, exactly as `RESULTS-eventual-period.md` already concluded in
   words; this supplies the quantitative version.

**Rule 90 filter, applied to this validation itself.** The same construction, run
under `rule90_step`, also gives `H - w` in `{1,3}` out to `w = 299` (control in
the same log). So the unboundedness is a **left-permutivity fact, not a Rule 30
fact** — both rules are left-permutive. That is the correct reading: this result
is a negative about the *method*, and it must not be cited as saying anything
about Rule 30 specifically. It fails the Rule 90 filter as a positive argument,
by design — which is the expected outcome for a left-permutivity lemma, and a
check that the instrument is reporting honestly.

## What is genuinely open on R1 after this inventory

- **R1-a. CLOSED** — `H(2,w) >= w`, see above. It was drafted as
  the highest-value open measurement and it turned out to be answerable for
  free. Do not spend SMT compute on `w = 9,10,11`.
- **R1-b.** The general-finite-row form of the zero-set obligation: over all
  finite rows (not the lone seed), is `r|Z` forced periodic by a periodic `c`?
  The driven-RHP evidence above says local forcing fails; the open question is
  whether diagram-global consistency restores it.
- **R1-c.** `comoving_columns_T32768.log` (13 KB) was not re-derived and is
  the only substantive `r1-r1zero` artefact still unaudited.

## Files

All three are committed under `uc/r1-r1zero/`, beside the code they audit:

- `verify_lhp_closure.py` — the pin and pass identities, and the LHP-closure
  fact. Run: `env PYTHONPATH=. .venv/bin/python3 uc/r1-r1zero/verify_lhp_closure.py`
- `direct_lone_seed_period.py` — the 0.1 s direct lone-seed exclusion that
  retires seed task 34.
- `h_horizon_lower_bound.py` with `h_horizon_lower_bound.log` — the
  `H(2,w) >= w` construction and its Rule 90 control.

Each is a few lines, self-checking (every construction is re-measured with the
plain Rule 30 evaluator), and referenced from this document, so none of them is
unowned tooling. Their outputs are transcribed above in full.

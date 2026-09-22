# (Lock) refuted: a 0-initial half-line does not lock under a periodic centre drive

Status: **(Lock) is FALSE at measurement strength in its drive-universal and
its finite-support-initial-state forms, `w = 01` being the headline witness.
The proposed proof mechanism is separately dead: the Rule 90 lone seed is a
*literal* counterexample to (Lock)'s analogue.  The seed-specific (Lock) is
not refuted, but it has lost this route to a proof.  No `Thm(2)`, no P1.**

Date: 2026-09-07.  Code: `experiments/rule30/lock-driven-halfline/`.
Pre-registration: `PREREG.md` in that directory, written before the sweep.
Modal: $0.  Paid model-provider calls: $0.

| # | Claim | Level |
|---|---|---|
| 1 | The lone seed's entire right half-plane is a deterministic function of the centre column alone: no fiber, no free boundary | `U`, validated bit-exactly |
| 2 | 58 of 69 periodic drives (`p <= 8`) leave `col_1` with no period `<= Qmax`, `w = 01` among them, stable to `T = 100,000`, `Qmax = 20,000` | `M`, kill `K1` |
| 3 | Rule 90 does the same (0 of 21 lock), so non-locking is not an OR phenomenon | `M`, kill `K2` |
| 4 | The **actual** Rule 90 lone seed has `col_0` eventually periodic (period 1) and `col_1` with no period `<= 20,000` | `M` on a real orbit |
| 5 | 11 drives *do* lock, at `p in {3,4,8}` only; `p = 2` is not among them | `M` |

## 1. The one good thing here, and it is structural

Rule 30 is `x_i(t+1) = x_{i-1}(t) XOR (x_i(t) OR x_{i+1}(t))`, so the half-line
`i >= 1` needs only `x_0` as its left boundary.  With the seed's own initial
data (`x_i(0) = 0` for `i >= 1`):

> **The entire right half-plane of the lone-seed diagram is a deterministic
> function of the centre column.**  There is nothing to quantify over.

This is genuinely not the ladder and not `RESULTS-alt-trace-fiber.md`.  That
arm drives *leftward* and enumerates *right halves* (`W = 10, 12`), finding
left-periodic members and concluding "any proof must again use left-finiteness
of the seed".  Here the right half is pinned to the seed's zeros and the
evolution is forward.  Obstruction F (free boundary) does not apply.

*Validation `V1`, the gate:* driving the half-line with the **true** centre
column reproduces the true lone-seed `col_1`, `col_2`, `col_3` bit for bit, to
`T = 3000`, rules 30 and 90.

## 2. Prior art, found before claiming novelty

The `w = 01` case is **not new**.  `a7_ladder_realizability` builds `X(k,01)`
with `s(0,x) = 0` for `x >= 1`, which is the same zero-initialised right half
driven by an alternating centre, and measured exactly this non-locking as its
unproved *i.o. lemma*.  Independent cross-validation of the two
implementations: density of `col_1 = 1` on the centre zero set

```text
this harness, T = 100,000 :  0.2145
a7, independent code       :  0.2132 - 0.2168
```

What is new here is the generalisation to all periodic drives, the clean
zero-initial form, the deeper horizon, and the Rule 90 control.

## 3. `K1` fired: 58 of 69 drives do not lock

Primitive nonconstant necklaces, `c(t) = w[t mod p]`, `T = 50,000`,
`Qmax = max(512p, 4096)`, 20% transient discarded, at least 10 repetitions
required before a period is accepted.

| `p` | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| words | 1 | 2 | 3 | 6 | 9 | 18 | 30 |
| locked | 0 | 1 | 3 | 0 | 0 | 0 | 7 |
| **no lock** | **1** | 1 | 0 | 6 | 9 | 18 | 23 |

The 11 locks are sparse and structured -- `w = 001` (period 21), the three
`p = 4` words (periods 4, 8), seven `p = 8` words (period 8) -- and `p = 2` is
not among them.  Doubling check, as pre-registered:

```text
w=01     T= 20,000 Qmax= 4,096 -> none    T= 50,000 Qmax=10,000 -> none    T=100,000 Qmax=20,000 -> none
w=011    same                              same                             same
w=00111  same                              same                             same
```

For `w = 01` the derived `col_{-1}` likewise has no period `<= 20,000` at
`T = 100,000`, and `col_1 = 1` still occurs on the centre zero set at
`t = 99,992`.

## 4. `K2` fired, and worse: Rule 90's real orbit is the counterexample

The proposed mechanism was that the OR makes the drive alternate between
sticky-`OR` and `NOR`-reset steps and thereby forces a finite attractor, with
Rule 90 linear and not locking, so the filter passes.  The first half fails.

* Rule 90, same harness: **0 of 21** drives lock (`p <= 6`).  So "does not
  lock" is shared by both rules and separates nothing.
* Decisive, and not a counterfactual: the **actual Rule 90 lone seed** has
  `col_0` eventually periodic with period 1 and `col_1` with no period
  `<= 20,000`.  That is a real orbit of a real rule sitting in exactly the
  configuration (Lock) declares impossible -- one eventually periodic column
  next to an aperiodic neighbour, entirely consistent with Kopra's width-2
  theorem.

So (Lock) cannot be a driven-half-line lemma.  Any true version must be
strictly Rule-30-specific in a way that the OR-sticky/NOR-reset picture does
not supply, because that picture predicts locking and the measurement says
otherwise.

## 5. What survives

* The seed-specific (Lock) is **not** refuted.  A periodic word need not be
  realisable as a Rule 30 centre column, and the counterexamples here are
  drives, not seeds.  This was recorded in the pre-registration before the run.
  What is gone is the proof strategy: one cannot get (Lock) from a general
  statement about periodically driven half-lines.
* `(Lock) + Kopra => P1` remains a valid implication.  It is the hypothesis
  that is now unsupported, not the inference.
* Side effect for R7: the `w = 01` object is a mode-(ii) witness for every
  `q <= 20,000` at every `R`, by rung 2's splice lemma -- but at *measurement*
  strength, exactly a7's i.o. lemma again.  It does not upgrade
  `RESULTS-ladder-rung2-periodic-realizability.md`, whose `q` not divisible by
  420 result is proof-strength from finite tori.  The two are complementary:
  proof for most `q`, measurement for all small `q`.

## 6. Honest scope

Non-locking is measured, never proved: "no period `<= 20,000` at
`T = 100,000`" is not aperiodicity, and this is obstruction H.  The kill is
therefore of a *proposal*, at the strength the pre-registration set in advance
(`K1`: no period `<= Qmax`, stable under doubling `T`).  Nothing here bears on
P1, P2 or P3.  The structural fact in section 1 is exact and is the piece
worth keeping.

## Reproduction

```sh
cd experiments/rule30/lock-driven-halfline
uv run python -c "from driven import *; T=3000; tr=lone_seed_cols(T,30,4); \
  print(run_halfline(lambda t: tr[0][t],T,30,3)==tr[1:])"     # V1 gate
uv run python sweep.py --rule 30 --pmin 2 --pmax 8 -T 50000
uv run python sweep.py --rule 90 --pmin 2 --pmax 8 -T 50000
```

# R7 rung 2: the half-plane extension exists.  Mode (i) of the ladder is dead for every period; mode (ii) rests on one named lemma

**VERDICT — MODE (i): limitation theorem PROVED, unconditional, uniform in `R`
and `k` and in the tail word, machine-verified with exhaustive safety scope.
MODE (ii): NOT CLOSED.  MISSING LEMMA: `col_1(t) = 1` for infinitely many `t`
in the zero set of `col_0`.**

That single i.o. statement closes mode (ii) for `q = 1` and every odd `q` at
once.  Nothing below is conditional on an unstated lemma: Theorem A is
unconditional, and Theorem B carries its hypothesis in its own statement.

Date: 2026-08-30.  Code and outputs in this directory.  Nothing outside it was
written; nothing was committed.  Modal: $0.  Paid model-provider calls: $0.

Rung 1 (`docs/rule30/RESULTS-ladder-rung1.md` §6) named the remaining gap:

> **MISSING: realizability.**  One needs, at every `R`, an infinite letter word
> realizing an alternating `col_0` together with an aperiodic `col_{-1}`.

and `PATH.md` R7 sharpened it: *does any finite `R` kill the phase slip, or
does it extend to a full half-plane?*  **It extends to a full half-plane.**
The object is exhibited below, in closed form, for every left depth `k` and
every eventually periodic target word simultaneously.

---

## 1. The construction

Fix a left depth `k >= 1` and a target tail word `w` of length `p`.  Put
`T0 = 2k + 1`.  Define an initial row `s(0, .)` on `Z` by

```text
s(0,x) = 0                for x >= 1            (the ladder's right wedge)
s(0,0) = 1                                       (the seed cell)
s(0,x) = 0                for -2k <= x <= -1     (matches the lone seed)
s(0,x)  free              for x <= -(2k+1)
```

and choose the free bits greedily, one per time step, by the rule in Lemma P
below: for `t >= T0`, set `s(0,-t)` so that `col_0(t) = w[(t - T0) mod p]`.
Everything is then determined.  Call the resulting spacetime diagram `X(k,w)`.

**Lemma P (left permutivity, flip form).**  For rule 30 and rule 90,

```text
s(t,x) = s(0, x-t) XOR H_t(s(0, x-t+1), ..., s(0, x+t))
```

so flipping `s(0,-t)` flips `s(t,0)` and changes no `s(t',0)` with `t' < t`.

*Proof.*  Induction on `t`.  `t = 0` is trivial with `H_0 = 0`.
`s(t+1,x) = s(t,x-1) XOR g(s(t,x), s(t,x+1))` with `g = OR` (rule 30) or
`g(a,b) = 0`, `s(t+1,x) = s(t,x-1) XOR s(t,x+1)` (rule 90).  By hypothesis
`s(t,x-1) = s(0,x-1-t) XOR H_t(...)`, and `s(t,x)`, `s(t,x+1)` depend only on
`s(0, >= x-t)`.  Collecting the rest into `H_{t+1}` gives the claim. ∎
*Verified:* `test_lemma_permutivity_flip`, 40 random configurations per rule,
every `t <= 12`, flip present at `t` and absent at every `t' < t`.

Hence the greedy choice is well defined and never disturbs an earlier decision.
**The centre column of `X(k,w)` is the lone-seed centre for `t < T0` and equals
`w` repeated for `t >= T0`** — so it is eventually `w`-periodic, with onset
`T0 = 2k+1`, which the ladder's Buchi construction guesses.

**Lemma W (the wedge is automatic).**  Every ladder wedge/edge check on a
column `x in [-k, R]` reads a cell `s(t,x)` with `t <= |x|`.  Such a cell
depends only on `s(0, [x-t, x+t]) ⊆ s(0, [-2k, 0])` when `x < 0`, and only on
`s(0, [0, 2x])` when `x >= 0`.  Both ranges are fixed at their lone-seed values
by the display above, whatever the free bits are.  So

```text
col_x(t) = 0   for t < |x|,     col_x(|x|) = 1,     for every x in [-k, R],
```

holds in `X(k,w)` for **every** choice of free bits and every `R`. ∎
*Verified exhaustively:* `test_lemma_wedge_automatic_exhaustive`, both rules,
`k = 1,2,3`, all `2^8` assignments of the first eight free bits, all
`x in [-k, 6]` — 1,536 configurations, zero deviations.

### Implementation

By diagonals.  With `D_j(u) = s(u, u-j)`,

```text
D_j(u+1) = D_j(u) XOR (D_{j-1}(u) OR D_{j-2}(u))    [rule 30]
D_j(u+1) = D_j(u) XOR  D_{j-2}(u)                    [rule 90]
col_x(t) = D_{t-x}(t),      D_j ≡ 0 for j < 0,   D_0 ≡ 1.
```

`D_j` is a prefix XOR of a function of `D_{j-1}, D_{j-2}`, so `D_j(0)` — the
free bit `s(0,-j)` — enters every entry by XOR, and the greedy choice at step
`j` is one XOR.  `O(T^2)` time, `O(T)` memory (`realize.py`).

*Independent check:* `rowsim` re-derives the same columns by a plain
row-by-row simulation on a window wide enough that no light cone reaches its
boundary.  **0 mismatches** for `x in [-k-2, 13]`, `T = 2000`, in every case
reported here (`test_construction_matches_row_simulation` covers both rules,
`k = 1,2,3`, `w in {01, 0011, 1}`, `T = 300`).

---

## 2. THEOREM A (unconditional): the ladder's mode (i) is nonempty at every `R` and `k`, for every tail word

> For every rule in {30, 90}, every `k >= 1`, every `R >= 1` and every finite
> word `w`, the diagram `X(k,w)` supplies a letter word
> `t -> (col_{R-1}(t), col_R(t))` that satisfies **every** constraint the R7
> ladder imposes in mode (i): the inverse transduction (exactly — the columns
> are the real ones), the light cone and both edges on `x in [-k, R]`
> (Lemma W), the right wedge on positive `x` (Lemma W), and "centre eventually
> `w`-periodic" with onset `2k+1` (Lemma P).
>
> Hence `plain_{R,k}(w) != ∅` for every `R` and `k`.  **No emptiness verdict in
> mode (i) is ever obtainable, at any depth, for any period.**  In particular
> the depth-3 escape family of rung 0 is not a depth artifact: it is the
> shadow of an actual half-plane, and the phase slip survives to `R = ∞`.

The `R7` rung-1 question — *does any finite `R` kill the slip, or does it
extend to a full half-plane* — is answered: **the half-plane.**

**Corollary A' (the pin too).**  `X(k,w)` carries a genuine `col_{R+1}`
obeying the forward rule at `x = R`, so by rung-1 Lemma 1 its projection
satisfies the boundary pin.  `pin_{R,k}(w) != ∅` for every `R, k`.  This is
recorded as a corollary of rung 1, not as an independent measurement.
*Verified anyway:* `pin_violations = 0` at every `R <= 16` in all 184 rule-30
cases of the sweep, over `8,207`-`13,925` pin antecedents each at `R <= 12`,
`T = 20000`.

### Machine verification, and why it is exhaustive rather than a sample

`ladder_check.py` drives `ladder_copy.py` — a byte-identical copy of
`experiments/rule30/ladder/ladder.py`, which was not modified — with the
letter word read off `X(k,w)`.  `ladder.step_window` performs a wedge or edge
check only while `cnt < P.saturate = R + 2k + 1`; past that it performs none.
**So feeding `saturate + 8` letters decides every safety constraint the ladder
imposes, not a sample of them.**  The Buchi condition is settled by Lemma P.

One detail that the exhaustiveness rests on, stated so it is not implicit:
`ladder.successors` clamps its counter (`cnt+1 if cnt < saturate else cnt`)
while `ladder_check.py` increments unconditionally.  The two agree on every
step with `cnt < saturate`, and they can differ only at `cnt >= saturate`,
where `step_window` sets `sat = True` and performs no check at all.  So the
driver fires exactly the same set of checks as the automaton, and no check is
skipped by the difference.

`rule 30, k = 2, w = 01, q = 1, T = 20000` (`log_ladder_w01_k2.txt`):

| R | saturate | letters fed | rejected at | centre mismatches | `col_-1` mismatches | pin antecedents | pin violations |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 6 | 14 | None | 0 | 0 | 8,207 | 0 |
| 2 | 7 | 15 | None | 0 | 0 | 11,790 | 0 |
| 3 | 8 | 16 | None | 0 | 0 | 9,654 | 0 |
| 4 | 9 | 17 | None | 0 | 0 | 13,925 | 0 |
| 5 | 10 | 18 | None | 0 | 0 | 7,103 | 0 |
| 6 | 11 | 19 | None | 0 | 0 | 12,132 | 0 |
| 7 | 12 | 20 | None | 0 | 0 | 10,083 | 0 |
| 8 | 13 | 21 | None | 0 | 0 | 10,735 | 0 |
| 9 | 14 | 22 | None | 0 | 0 | 10,144 | 0 |
| 10 | 15 | 23 | None | 0 | 0 | 9,307 | 0 |
| 11 | 16 | 24 | None | 0 | 0 | 10,919 | 0 |
| 12 | 17 | 25 | None | 0 | 0 | 9,963 | 0 |

"centre mismatches" and "`col_-1` mismatches" compare the ladder's own derived
`c_val` / `m1_val` against the construction's columns at the correct delay:
zero, so the ladder is reading the object we think it is.

**Sweep** (`sweep.py`, `log_sweep.txt`, `out_sweep.json`): rules 30 and 90,
`k = 1..8`, `R = 1..16`, all **23 primitive binary necklaces of length
`p <= 6`**, `T = 4000`.

```text
cases: 368   failures: 0
```

Zero ladder rejections, zero derived-column mismatches, zero pin violations,
in all 368.

---

## 3. Calibration: the construction reproduces every decided case

These were run **before** `w = 01`, as the disconfirming gate.  They are
validation against results this repo already holds, not discovery.

| case | prediction from the repo | measured |
|---|---|---|
| `w = 1`, `k = 2` | rung 0: mode (ii) EMPTY at `p = 1`, so `col_{-1}` must be eventually periodic here; register row 26: the all-one trace forces the checkerboard left half | `col_{-1} ≡ 0` from `t = 9`; minimal eventual period **1**; `Diff_q` events **0** for `q = 1..8`; late row `x in [-4,0]` is `1,0,1,0,1` — the checkerboard |
| `w = 0`, `k = 2` | rung 0: mode (ii) EMPTY at `w = 0, R = 2`; on this tail `col_{-1} = col_1`, so `col_1` must be eventually constant | `col_1 ≡ 1` from `t = 9`; `col_{-1}` minimal eventual period **1**; `Diff_q` events **0** for `q = 1..8` |
| both, mode (i) | rung 0: "mode i NONEMPTY and mode ii EMPTY" at `p = 1` | mode (i) accepted at every `R <= 16`, `k <= 8`; `Diff_1` fails.  Exactly that split |

The `w = 0` row is the one that could have fired: `col_1` is a column the
construction does not control, and rung 0's EMPTY verdict forces it to be
eventually constant.  It is.  `test_p1_calibrations_reproduce_rung0` pins both.

**Rule 90 control.**  Lemma P and Lemma W hold verbatim for rule 90, so the
construction works there too — 184 rule-90 cases, zero failures.  This is the
control in its correct form, and it is not a defect: it is the measured
content of register row 5.  The ladder's mode-(i) constraint set uses nothing
beyond left permutivity, and both rules are left permutive, so mode (i)
cannot separate them.  Rule 90's boundary condition is vacuous (rung-1
Lemma 1'), so the pin check is skipped for rule 90 rather than applied from
rule 30 — applying rule 30's pin to rule 90 destroys the control instead of
testing it, which the first run of `sweep.py` reproduced as 184 spurious
failures before the repair.

---

## 4. Mode (ii): what is measured, and the exact missing lemma

For `w = 01` with onset `T0`, write the tail phase by `t - T0`.  Directly from
the forward rule at `x = 0`:

```text
t - T0 odd   (col_0(t)=1, col_0(t+1)=0):   col_{-1}(t) = 0 XOR (1 OR *)      = 1
t - T0 even  (col_0(t)=0, col_0(t+1)=1):   col_{-1}(t) = 1 XOR (0 OR col_1(t)) = NOT col_1(t)
```

So `col_{-1}` is pinned to `1` on the odd phase and is the complement of
`col_1` on the even phase — the even phase being exactly the **zero set of the
centre column**.  Two consequences.

* `col_{-1}` can never be eventually `0`, so the only way `Diff_1` fails is
  `col_{-1} ≡ 1` eventually.
* For **every odd `q`**, `t` and `t-q` lie in opposite phases, so
  `col_{-1}(t) != col_{-1}(t-q)` exactly when the even-phase one has
  `col_1 = 1`.

> **MISSING LEMMA (i.o.).**  `col_1(t) = 1` for infinitely many `t` with
> `col_0(t) = 0`, in `X(k, 01)`.

**THEOREM B (conditional, hypothesis in the statement).**  *Assume the i.o.
lemma.*  Then `col_{-1}` of `X(k,01)` has infinitely many `q`-diffs for every
odd `q`, so `S_{R,k}(01, q) != ∅` for every `R`, every `k` and every odd `q`;
with the analogous even-`q` statement it extends to the bounded-universal mode
`S(1..Q)` for every `Q`.  The R7 ladder then decides nothing about `p = 2` in
either mode, at any depth, with or without the pin, at any `Q` — a complete
limitation theorem.  **Without the i.o. lemma, Theorem B is not proved and is
not claimed.**

**The failure branch is explicit.**  If the i.o. lemma is false then
`col_{-1} ≡ 1` eventually, whence `col_{-2} ≡ 0`, `col_{-3} ≡ 1`, ... — the
time-constant, space-alternating checkerboard, which is precisely rung-1
Lemma 4's collapse state `((1,1),(0,0)) <-> ((0,0),(1,1))`.  So the two rungs
meet: the only way this construction fails to close mode (ii) is by landing on
the state rung 1 already proved is the unique attractor of time-2-periodic
tails.

**Where the gap lands.**  The i.o. lemma is a statement about `col_1` on the
zero set of an eventually periodic `col_0` — the same object as register row 1
(R1: "show `c` eventually periodic forces `r` eventually periodic on
`{c_t = 0}`"), which the register lists as the best open route.  The mode-(ii)
limitation theorem and R1 are aimed at the same zero set from opposite sides.
This is a structural observation about where the difficulty sits, not a
reduction and not a proof of either.

### Finite-horizon measurements (evidence, not proof)

`rule 30, k = 2, w = 01`:

| horizon `T` | smallest eventual period of `col_{-1}` searched | found | `col_1 = 1` on the centre zero set | last such `t` |
|---:|---:|---|---|---:|
| 20,000 | `q <= 512` | **none** | 2,137 / 9,996 (density 0.2138) | 19,991 |
| 50,000 | `q <= 4096` | **none** | 5,357 / 24,996 (density 0.2143) | 49,999 |

`Diff_q` event counts at `T = 50000`, `q = 1..8`:
`10714, 10713, 10713, 10711, 10712, 8928, 10712, 10712`.
At `T = 20000`, `q = 1..16`:
`4274, 4274, 4274, 4272, 4273, 3585, 4273, 4273, 4273, 690, 4272, 4272, 4272, 4268, 4271, 2895`.

**Period-detection scope of the sweep.**  "No eventual period" below means *no
eventual period `q <= 256` detected on `t in [T0+4, 4000]`* — with a tail of
about 3,990 samples, a period near the top of that range is tested against only
~15 repetitions, so a long-period collapse would read as "none".  The `w = 01`
robustness run below (`q <= 1024`, `T = 20000`) and the `T = 50000`,
`q <= 4096` run have far more margin; the sweep does not.

Across the sweep (368 cases, `T = 4000`, search to `q <= 256`) the two `p = 1`
words always give `col_{-1}` of minimal eventual period 1 with `Diff_1 = 0`,
and the `p >= 2` words give no eventual period `<= 256` with `Diff_1` counts of
850-2,960 — **with three exceptions**, all rule 30:

```text
rule 30, k = 2, w = 0001   col_-1 minimal eventual period 4   (Diff_1 = 1995)
rule 30, k = 5, w = 0011   col_-1 minimal eventual period 4   (Diff_1 = 1993)
rule 30, k = 7, w = 0011   col_-1 minimal eventual period 4   (Diff_1 = 1991)
```

**These matter and are not swept under.**  They show that the construction does
*not* automatically produce an aperiodic `col_{-1}`: for those `(k, w)` the
left half collapses to something eventually 4-periodic, which is exactly what
the i.o. lemma has to exclude, and which no argument given here excludes.  They
do not touch Theorem A (mode (i) needs no `Diff`), and they do not touch
`q = 1` even in their own cases, since `Diff_1` still fires ~10,000 times at
`T = 20000`; they kill only `q = 4` for those particular witnesses.

**All three are escapable by phase** (`log_collapse_phases.txt`; the sweep
fixes phase 0, and `k` enters the construction only through the onset
`T0 = 2k+1`, so the free parameter here is the transient, which is exactly what
the Buchi onset guess quantifies over).  At `T = 20000`, search to `q <= 2048`:

| `k`, `w` | phase 0 | phase 1 | phase 2 | phase 3 |
|---|---|---|---|---|
| 2, `0001` | period 4, `Diff_4 = 0` | none, `Diff_4 = 4` | none, `Diff_4 = 3` | none, `Diff_4 = 8` |
| 5, `0011` | period 4, `Diff_4 = 0` | none, `Diff_4 = 2` | period 4, `Diff_4 = 0` | none, `Diff_4 = 5` |
| 7, `0011` | period 4, `Diff_4 = 0` | none, `Diff_4 = 2` | none, `Diff_4 = 1` | none, `Diff_4 = 5` |

So the construction does supply a `q = 4` witness for those words after all,
at a different phase.  **Read that with care**: the surviving `Diff_4` counts
are 1 to 8 events over 20,000 steps.  That is a thin margin, it is finite
horizon, and it is not evidence that those diffs recur forever — it only says
the collapse is not forced by `(k, w)`.  What the table does establish is that
the "individual configuration collapses" phenomenon is a property of the
*transient*, not of the target word.

For the target case `w = 01` no collapse occurs at any `k = 1..8` for either
rule.  A dedicated robustness run (`log_w01_robust.txt`, rule 30,
`k in {1..8, 10, 12, 16}`, both alternating phases, `T = 20000`, search to
`q <= 1024`) gives, in all **22** configurations: **0** wedge/edge violations
on `x in [-k, 9]`, **no** eventual period `<= 1024` for `col_{-1}`, and
`col_1 = 1` on the centre zero set with density `0.2132`-`0.2168`, the last
occurrence within 10 steps of the horizon end in every one.  The split between `p = 1` and `p >= 2` that rung 0 measured inside the
automaton appears here inside single explicit configurations, with the three
collapses above as the honest exception list.

The stable density near 0.214 and the last-occurrence times sitting at the end
of every horizon are consistent with the i.o. lemma and prove nothing about
it.

---

## 5. Honest scope — what a reader must not over-read

* **`X(k,w)` has infinite support to the left.**  It is not the lone seed and
  it is not a finite configuration.  Theorem A says nothing whatever about
  Wolfram's Problem 1, and it does not exhibit a Rule 30 *finite-seed* diagram
  with an alternating centre column.  What it exhibits is an element of the
  ladder's over-approximation.
* **Theorem A is a statement about the method, not about Rule 30.**  It says
  the R7 constraint set is satisfiable at every depth; the ladder remains
  sound, its EMPTY verdicts would still be theorems, and it simply can never
  return one in mode (i).
* **`w = 1` does not contradict Jen 1990 Prop. 3 / Kopra 2023 Thm 3.5.**
  `X(2,1)` has `col_0 ≡ 1` and `col_{-1} ≡ 0` eventually — two adjacent
  eventually periodic columns — because the configuration is infinite to the
  left.  Register row 26 is the reason: no *finite* row has a constant-one
  trace, and the constant-one trace forces exactly the checkerboard left half
  that the construction reproduces.  **Consequently the Jen/Kopra finisher may
  not be invoked to conclude that `col_{-1}` of `X(k,01)` is aperiodic.**  That
  route was checked and is closed; the i.o. lemma of §4 is what remains, and it
  is not obtainable from the finisher.
* **The construction is rule-independent.**  It works for rule 90 verbatim.
  That is the explanation of Theorem A, not a flaw in it, and it means nothing
  proved here can be upgraded into a Rule-30-specific statement by adding depth.
* **It is not the `RESULTS-alt-trace-fiber.md` wallpaper.**  That member has
  nonzero initial cells at `x = 1` and `x = 4`, which violates the ladder's
  right wedge, so it is not a ladder witness; and its left half is spatially
  7-periodic, so its `col_{-1}` is time-periodic and it could not settle mode
  (ii) either.  `X(k,w)` has an all-zero right half by construction and is
  proved, not empirical.
* **Nothing here re-derives the depth-3 escape family**, and nothing here uses
  the stroboscopic map or the alternating-trace survivor automaton.  Theorem A
  explains why that family survived every depth increase; it does not restate it.
* **The `T = 50000` aperiodicity numbers are finite-horizon.**  They pin a
  regression, they do not establish that `col_{-1}` is aperiodic.  The three
  collapsing cases in §4 are the concrete demonstration that the construction
  gives no aperiodicity for free: at `(k, w) = (2, 0001)` and `(5, 0011)` and
  `(7, 0011)` the constructed `col_{-1}` really is eventually 4-periodic.  Do
  not read Theorem A as producing aperiodic neighbours.

## 6. What this retires

Rung 0 retired depth; rung 1 retired the pin and the `Q` axis, and falsified
tail-language stabilization.  Rung 2 retires **mode (i) entirely, for every
period, unconditionally**, and reduces mode (ii) from "realizability at every
`R`" — three ingredients, two in hand — to **one infinitely-often statement
about one column on one zero set**.  Any further R7 work that is not an attack
on that i.o. lemma is spending compute on a decided question.

## Reproduction

```sh
cd experiments/overnight-arms/frontier_attack/a7_ladder_realizability
uv run python realize.py -w 1  -k 2 -T 800   --verify-T 400  --qmax 64     # calibration
uv run python realize.py -w 0  -k 2 -T 800   --verify-T 400  --qmax 64     # calibration
uv run python realize.py -w 01 -k 2 -T 50000 --verify-T 2000 --qmax 4096
uv run python ladder_check.py -w 01 -k 2 -T 20000 --rmax 12 -q 1
uv run python sweep.py --kmax 8 --pmax 6 --rmax 16 -T 4000
for K in 1 2 3 4 5 6 7 8 10 12 16; do for P in 0 1; do \
  uv run python realize.py -w 01 -k $K --phase $P -T 20000 --qmax 1024 --rmax 8; done; done
for KW in 2:0001 5:0011 7:0011; do for P in 0 1 2 3; do \
  uv run python realize.py -w ${KW##*:} -k ${KW%%:*} --phase $P -T 20000 --qmax 2048; done; done
uv run --with pytest --with numpy python -m pytest test_realizability.py -q  # 7 passed
```

Files: `realize.py` (construction), `ladder_check.py` (drives the untouched
ladder engine), `sweep.py`, `test_realizability.py`, `ladder_copy.py`
(byte-identical copy of `experiments/rule30/ladder/ladder.py`), logs
`log_*.txt`, machine-readable `out_*.json`.

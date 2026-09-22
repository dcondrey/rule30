# Uniform no-go theorem for end windows plus total queue phase

Date: 2026-09-02

Status: **AN ALL-LENGTH COUNTEREXAMPLE FAMILY RULES OUT EVERY FIXED
TWO-ENDED QUEUE WINDOW, EVEN WHEN IT IS AUGMENTED BY LENGTH, COMPLETE
ENDPOINT/EVENT DATA, AND THE EXACT TOTAL `D8` ACTION.  THE FULL ORDERED QUEUE
REMAINS CLOSED.  `(SEP)`, TP2, PP1, PP2, AND PP3 REMAIN OPEN.**

Evidence level: `U/K` (uniform table derivation and an infinite exact
counterexample family).

## 1. Novelty boundary and scope

`RESULTS-HOLONOMY-DEFECT-CLOSURE.md` already gives finite transition
collisions for an anchored phase profile and for the first natural
depth-one two-ended repair.  It does not prove that every fixed end-window
radius fails.

The new statement begins at that open quantifier.  It escapes dependence on
a larger census by using two exact neutral blocks of the Rule 30 inverse-cone
transducer.  It rules out the entire state class

```text
fixed left/right queue windows
+ queue length
+ previous and emitted endpoint/event data
+ exact total D8 word action.                            (1)
```

It does **not** rule out every conceivable bounded quotient, and it does not
prove queue mortality.  The families below are legal in the invariant queue
SFT but are not asserted to be diagonals derived from hard-core endpoint
prefixes.  Its role in the PP1/TP2 proof DAG is therefore an exact no-go
branch in the stronger arbitrary-queue route:

```text
end-window/total-phase induction  --X-->  closed transition system

complete ordered queue or a proved lossless ancestry quotient
  --> O_c intersect I(HC_omega) = empty                  (SEP, OPEN)
  --> TP2 exclusion                                      (OPEN)
  -/-> full PP1 without all other temporal periods.
```

## 2. The neutral blocks

For a normalized queue input symbol `a in {0,1,2}`, let `h_a` be its exact
permutation of the scan state.  From the local `phi` table,

```text
h_0=(0,1,3,2),
h_1=(3,2,1,0),
h_2=(2,3,1,0).                                         (2)
```

Both `h_0` and `h_1` are involutions.  Therefore the distinct blocks

```text
00, 11
```

have the same total action, namely the identity.  They leave every entering
scan state equal after the block, so any common suffix is scanned identically.
They are nevertheless not interchangeable under the next queue update.
Writing `q(3)=1` for the exact normalization and leaving `0,1,2` fixed, the
two relevant entering-state rows are

```text
enter 1:  scan(00)=11,  scan(11)=21;
enter 3:  scan(00)=21,  scan(11)=01.                  (3)
```

The two output-block actions in each row of (3) differ.  Because every
`h_a` is a permutation, multiplying both by common prefix, suffix, and
boundary actions cannot erase that difference.

This is the transported datum omitted by (1): **which identity block occurs
at an interior position**.  Its present total action is trivial, but the
sequential scan exposes it one row later.

## 3. Legal families for both constant tails

Let `k` be odd.  For tail `2`, define

```text
R^0_k = 2 1^k 00 2 1^k,
R^1_k = 2 1^k 11 2 1^k.                              (4)
```

Both words avoid the invariant forbidden factors `20`, `22`, and `011`.
The prefix `1^k` carries scan state `2` to state `1`, so (3), first row,
applies.  Each neutral block returns to state `1`; the following `2` sends it
to `3`, and the odd suffix `1^k` sends it to final scan state `0`.  Both
queues end in normalized symbol `1`, hence have previous endpoint `2`; final
state `0` legally emits endpoint `1`.  Thus both perform the same legal `A`
event.

For tail `3`, let `k = 2 (mod 4)` and define

```text
S^0_k = 3 1^k 00 (01)^k,
S^1_k = 3 1^k 11 (01)^k.                             (5)
```

Their nonleading words again avoid `20`, `22`, and `011`.  Since `k` is
even, `1^k` leaves the entering state at `3`, so the second row of (3)
applies.  Put `J=h_1 o h_0=(3,2,0,1)`.  The literal four-state cycle gives

```text
J^k(3)=2 when k = 2 (mod 4).                          (6)
```

Both queues therefore finish in scan state `2`.  They end in normalized
symbol `1`, so previous endpoint `2` legally emits endpoint `2`; both perform
the same `B` event.

Equations (2), (3), and (6) are complete finite-table calculations and hold
for every stated `k`.  No maximum word length is involved.

## 4. All-window nonclosure theorem

For radius `r>=0`, define `Sigma_r(R)` to contain

```text
the queue length and fixed tail;
the first r and last r queue symbols;
the previous endpoint, final scan state, emitted endpoint, and event;
the exact total D8 action of every nonleading queue symbol.       (7)
```

> **Theorem.** For every finite `r`, `Sigma_r` is not a transition
> congruence on the legal invariant queues, for either tail `2` or tail `3`.

**Proof.** Choose an odd `k>=max(1,r)` in (4).  The two queues have equal
length and equal `r`-symbol end windows.  Their middle blocks have the same
identity action, so their total actions agree.  Section 3 shows that all
endpoint/event data in (7) agree and both updates are legal.  During the
update, the emitted rows differ only inside the two-cell middle block:
common prefixes reach the same entering state, the neutral blocks have the
same exit state, and common suffixes therefore agree.  Hence the successor
end windows still agree.  The first row of (3) and cancellation in the group
show that the successor total actions differ.  Thus equal `Sigma_r` states
have unequal successor `Sigma_r` states.

For tail `3`, choose `k>=max(2,r)` with `k=2 (mod 4)` and repeat the argument
with (5), (6), and the second row of (3).  QED.

The theorem remains true if a state adds any data determined by the fields
in (7), such as the current invariant-SFT suffix state or a residue of the
queue length.  It does not cover an unrelated interior statistic that
explicitly distinguishes the two neutral blocks.

## 5. Consequence for the remaining proof search

The exact composition seam is still the complete ordered normalized queue,
or an ancestry object proved to preserve the placement of neutral interior
blocks.  Increasing a fixed endpoint window cannot repair the loss, even
when the exact current `D8` phase and all boundary decisions are supplied.

The prize-sufficient target remains the single open separator

```text
O_c intersect I(HC_omega) = empty,  c in {2,3}.       (SEP)
```

A continuation should use the complete queue to prove pull-token
nonreusability, a scale-aware gap descent, or the actual syndetic pull-ray
exclusion.  The present theorem closes only the bounded end-window/phase
representation class; it closes no temporal-period rung.

## 6. Independent verification

The checker verifies the local involutions and scan rows, the complete
two-state/four-state residue cycles used for arbitrary `k`, and concrete
instances for every requested window:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_queue_window_phase_no_go.py \
  --max-window 64
```

The loop over windows is a regression check for the formulas, not the source
of the all-window quantifier; that quantifier is supplied by (2)--(6).

## 7. Follow-up: four escapes tried against the exact mechanism (2026-09-06)

The theorem's mechanism is the collapse of `00`/`11` to the same `D8` group
element. Four escapes were tried, each judged by whether it specifically
avoids asking a group-collapsed summary to predict the future:

- **A finer congruence that keeps the whole intermediate scan trace, not
  just its final `D8` element.** Resolved 2026-09-06, and it closes the
  family rather than escaping it. Zero class merges through `L=18`
  (3,015,168 exhaustive legal words, `RESULTS-SYNTACTIC-MONOID-QUOTIENT.md`),
  and then proved injective for **every** length in two finite checks on the
  action table (`RESULTS-SYNTACTIC-MONOID-INJECTIVITY-PROOF.md`). This is
  the escape the theorem's own final paragraph anticipates ("an unrelated
  interior statistic that explicitly distinguishes the two neutral blocks"),
  and the proof shows the only statistic of this shape that distinguishes
  them is the literal block: the right congruence is the identity, so the
  block monoid is free and admits no finite quotient at any radius. The
  no-go's `D8` collapse is the `sig_B` special case of that fact.
- **A paired/relative invariant over two synchronized copies.** Killed for
  both tested constructions — divergence width grows without saturation
  under tail 3, and tail-2 pairs die before divergence develops. See
  `RESULTS-PAIRED-DIVERGENCE-INVARIANT.md`.
- **A monotone Lyapunov potential not built from a finite quotient at all.**
  Killed for every tested candidate; all were artifacts of the queue's
  fixed +1-symbol-per-step growth rather than real dynamical signal. See
  `RESULTS-LYAPUNOV-POTENTIAL-SEARCH.md`.
- **The existing zero-prefix greedy counting lemma** (`s_2(W)<=n`,
  `s_3(W)<=n+1`, `RESULTS-SCALE-TELESCOPING.md`), which is a monotone count
  over the whole word rather than a bounded transition congruence and so
  was never in this theorem's scope: extended empirically (length 23
  exhaustive, length 2000 adversarial/random, zero counterexamples), still
  unproved. See `RESULTS-ZERO-PREFIX-LEADING-TERM-EXTEND.md`.

The syntactic-trace quotient is the one live structurally-new lead; it is
not proved for all `L`, only verified exhaustively to `L=18`.

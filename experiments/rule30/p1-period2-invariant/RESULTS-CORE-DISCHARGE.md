# Reverse carry cascades and the factor-discharge obstruction

Date: 2026-09-01

Status: **A UNIFORM FIXED-HORIZON CASCADE LEMMA IS PROVED, BUT THE LOCAL
DISCHARGING ROUTE IS KILLED AT RADIUS SEVEN.**  No mortality or period-two
theorem is proved.

## 1. Exact reverse macro

Let `q_1,...,q_T` be an even frontier's aligned symbols, read
shallow-to-deep, and encode a carry `(c,d)` by `2c+d`.  For input symbol `q`,
the forward deep-to-shallow action is the permutation `tau_q` from
`carry_transducer.py`.  Its emitted symbol is the bit-swap of the new carry.

When a seed bit `rho` is appended, the prescribed carry at the shallow end of
the old word is

```text
f_rho = (1-rho,rho).                                (1)
```

Indeed the first new row has shallow feed `C_1=1-rho`, while the pinned row
has `D_1=1`; the last shallow recurrence gives `D_2=rho`.  Since every
`tau_q` is a permutation, start at (1) and read the old word
shallow-to-deep, applying `tau_q^(-1)`.  Before each inverse action, the
bit-swap of the current carry is the corresponding successor symbol.  The
carry left at the deep end is exactly the pair of newly reconstructed tail
bits.

Thus one append is an exact reverse subsequential transduction.  The
successor word consists, shallow-to-deep, of terminal symbol `3`, the emitted
symbols along the old word, and the bit-swap of the final deep carry.
`core_discharge.py` checks this construction against the independent integer
`append_macro` recurrence on all 4,370 arbitrary even frontiers through depth
six.  The preceding permutation argument is independent of depth.

## 2. Exact fixed-horizon composition

For a fixed hard-core word `rho_0,...,rho_(H-1)`, compose `H` reverse macros.
A symbol passes through a vector of `H` carries.  The shallow terminal `3`s
initialize a finite triangle, the arbitrary old frontier is then streamed
through the vector, and the final deep carries are flushed through a second
finite triangle.  The resulting `H` carry codes are exactly the `H` emitted
tail pairs.

Consequently, for every fixed `H`, all possible length-`H` label blocks over
arbitrary frontier width are recognized by a finite cascade with at most
`4^H` carry vectors.  This statement quantifies over frontier width; it is
not a width sweep.  The implementation cross-checks 4,247 arbitrary
frontier/rho instances through `H=5` against repeated `append_macro`.

The construction is useful as an exact finite-horizon verifier, but its state
space grows with `H`.  It supplies no horizon-independent quotient.

## 3. Radius-seven discharging is false

Encode an append label as `(rho,e_1,e_2)`, where `e_1,e_2` are its two new
tail bits.  The exact seed-generated frontier

```text
n=22, seed=0x24a28
```

has seven forced continuation bits `0000000`; every pin passes and every
emitted pair is `00`.  Therefore the legal length-seven factor `0000000`
appears in the label language.  A factor-only de Bruijn approximation of
radius seven contains the corresponding self-loop.  Its per-edge charges are

```text
7(e_1+e_2)-2             = -2,
2(e_1+e_2+rho)-1         = -1.                       (2)
```

So (2) gives negative cycles for both the coefficient-seven density charge
and the second weaker balance charge.

The first weaker balance has charge `2(e_1+e_2)-rho`.  It is killed by the
seed-generated control

```text
n=26, seed=0x892512,
forced rho=01010101,
emitted pairs=00^8.
```

Its two overlapping length-seven factors form the alternating two-cycle;
the cycle has negative total charge because each rho-one edge contributes
`-1` and each rho-zero edge contributes zero.

These witnesses do not falsify either global weaker balance inequality.
Repeating a locally legal factor need not be a globally seed-generated
frontier orbit.  They prove that a certificate retaining only the allowed
label factors of radius seven cannot establish the balances.  Increasing the
factor radius would again be horizon growth and is outside the registered
certificate class.

## 4. Consequence

The reverse cascade is a genuine uniform-in-width lemma and explains how to
make any fixed-horizon factor computation complete.  The negative cycles show
why that completeness does not become a mortality proof: global
seed-generated compatibility is lost when legal blocks are spliced.

The linear hard-core mortality theorem, both weaker global balances, the
period-two theorem, and Prize Problem 1 remain open.  A next proof must retain
an unbounded compatibility object or establish a symbolic induction in the
horizon.

## 5. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/core_discharge.py
```

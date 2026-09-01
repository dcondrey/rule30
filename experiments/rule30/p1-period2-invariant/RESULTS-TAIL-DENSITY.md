# Reconstructed-tail density and active-core audit

Date: 2026-09-01

Status: **OPEN.  The coefficient-seven density bound survives its registered
finite falsifier, but no uniform density proof was obtained.**  The primary
phase/`rho`/`D8` potential is killed by an exact negative cycle.  A new exact
uniform reduction removes the growing deep-zero padding and conjugates the
full frontier to a length-`+1` active-core transducer; mortality of that core
remains to be proved.

## 1. Density candidate and exact finite falsification

For a no-`11` word `rho_0,...,rho_(n-1)`, let `L_1,...,L_(2n)` be the
successive deepest outputs of the exact alternating-fiber reconstruction.
The registered candidate is

```text
7 wt(L_1...L_(2n)) >= 2n-2.                         (D)
```

Exhaustive enumeration of all Fibonacci-many hard-core words through
`n=24` finds no counterexample.  The minimum weights are

```text
1,1,1,2,2,2,2,2,3,3,4,4,4,4,5,5,5,6,6,6,6,7,7,7.
```

The minimum slack `7 wt(L)-2n+2` is zero only at `n=8`, on chronological
word `01010100`.  This is finite falsification data only.  It is not an
induction and is not used to claim (D) for arbitrary `n`.

The coefficient seven has an exact sharp control.  On a cyclic row of width
seven, Rule 30 sends

```text
1000000 -> 1100001 -> 0010011 -> 1111110 -> 1000000.
```

In the registered reconstruction alignment, `rho=0101...` emits
`L=1000000...`.  Thus a valid proof may force positive density, but it may
not demand more than the period-seven infinite-left wallpaper supplies.

## 2. The registered finite potential is impossible

The primary observer retained

```text
(n mod 7, previous rho, exact D8 action of the aligned frontier word)
```

and charged a seed extension by

```text
7 * (number of its two new L-ones) - 2.
```

Its exact reachable edge alphabet through length 16 has a 14-edge negative
cycle.  Every edge in the cycle is a legal no-`11` seed-prefix extension,
emits `00`, and has charge `-2`, so the total charge is `-28`.  The complete
frontiers and chronological extension bits are printed by
`tail_density.py`.

The cycle splices edges belonging to different full frontiers.  It therefore
does **not** disprove (D).  It proves that no potential on this observer can
certify (D): summing

```text
cost(edge) + Phi(destination) - Phi(source) >= 0
```

around the cycle would give `-28 >= 0`.  Per the preregistered kill condition,
the observer was not enlarged with another bounded endpoint window or D8
lookahead.

## 3. Uniform deep-zero/core conjugacy

There is a useful exact reduction that retains the whole ordered state.  For
an even frontier `(T,A,B)`, form its fixed-width aligned word

```text
q_j = (A_j,B_(j-1)),  j=1,...,T,
```

over the four-letter alphabet, and reverse it so that the deep end is read
first.  Starting with carry `(c,d)=(0,0)`, one letter `q=(a,b)` performs

```text
c' = c XOR (a OR b),
d' = d XOR (c OR a),
emit (d',c').                                        (1)
```

After the last input, emit the shallow terminal letter

```text
(c XOR d,1).                                         (2)
```

The exact forced macro satisfies the word identity

```text
reverse(q(successor)) = 0 . Transduce(reverse(q(state))) . terminal.   (3)
```

The leading zero in (3) is the newly forced deep zero.  A leading zero read
from zero carry emits zero and leaves the carry zero.  Consequently all
leading deep zeros can be stripped.  If `v` is the remaining active core,
then every pin-passing forced macro is exactly

```text
v -> G(v) = Transduce(v) . 3,                        (4)
```

so the active length grows by one, not two.  Moreover,

```text
pin passes       iff c XOR d = 1,
next forced rho  = 1 XOR c.                          (5)
```

Equations (3)--(5) are all-length identities, not observations.  Equation
(3) follows directly by reading the two inverse-Gray sweeps deep-to-shallow:
their two running XOR carries are exactly `(c,d)`, (1) emits the successor
aligned symbol, (2) is the shallow boundary symbol, and the two prescribed
deep outputs contribute the single aligned zero.  Equation (5) follows
because final `c` is the parity of the input OR-word and the first bit of
(2) is the pin.

The implementation independently constructs the integer successor with
`wf_step` and checks (3)--(5) on all 511 pin-passing reachable macros from
hard-core seeds through length 12.  Those checks validate the implementation;
the preceding carry derivation proves the identity uniformly.

This quotient is stronger than the killed `D8` summary: it removes only a
provably inert zero prefix and retains the complete arbitrary-length core.
It also exposes why a regular additive cost failed.  The length-four witness
begins

```text
22230123 -> 303001213 -> 3122230123,
```

the same exact circulation recorded by the ordered-boundary-operator audit.
A successful argument on (4) must therefore be non-additive, stack-like, or
an exact full-word induction.

## 4. Two weaker balances remain conjectural

Exploration suggested the pointwise inequalities

```text
2 wt(L) >= wt(rho),
2 (wt(L)+wt(rho)) >= n.
```

Together they would imply `6 wt(L) >= n`, already enough to exclude an
eventually-zero reconstructed tail.  Both survive exhaustive hard-core
enumeration through `n=24`.  Separate exact SAT falsification found no
counterexample through `n=40`, but no proof artifact from that exploratory run
is retained here.  They are recorded only as candidate lemmas.  No
parameterized certificate or human proof was found, and the display must not
be cited as a result.

## 5. Consequence and next obligation

The active-core conjugacy is a genuine uniform intermediate lemma, but it is
not mortality.  An immortal finite-left candidate would become an
arbitrary-length orbit of (4), ending in `3` at every step, whose final carry
always has unequal bits and whose forced bits from (5) avoid `11`.  Excluding
such an orbit is exactly the remaining obligation.

Thus neither (D), the period-two theorem, nor Prize Problem 1 is proved here.
The next proof attempt should act on the whole word in (4), preferably by a
well-founded non-additive decomposition of the `2/3`-merging transducer.  It
must retain the infinite-left period-seven wallpaper as a control: that
wallpaper has no finite deep-zero prefix and therefore is not represented by
a finite active core.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/tail_density.py \
  --max-length 24 --core-max-seed 12
```

The command reproduces every minimum, the exact cyclic wallpaper, all
reachable core-conjugacy cross-checks, and the complete negative observer
cycle.

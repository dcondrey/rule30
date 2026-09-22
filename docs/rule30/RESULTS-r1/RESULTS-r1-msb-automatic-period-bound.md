# A direct period bound for MSB automata

Date: 2026-09-09. Evidence: **U** (symbolic theorem, independently
audited), **C** (exact finite addition product), **C/M** (exhaustive
small-machine regression and scalar controls). This is an intermediate
construction tool. R1 and P1 remain open.

## 1. The bound does not require reversal

Let an `N`-state deterministic binary-output automaton read integers
from most significant to least significant bit. The root must have
a leading-zero self-loop. The output of the empty word defines the
value at zero. Unreachable or equivalent states need not be removed
before applying the following conservative bound.

**Theorem (U).** Put

```text
H = 2^N,                 P = 2^N * lcm(1,...,N).
```

Its output sequence `u` is eventually periodic if and only if

```text
u(n+P) = u(n) for every n>=H.
```

In particular, an exact mismatch above `H` proves aperiodicity of
this independently defined automatic sequence. The original MSB
state count is used directly; no `2^N` reversal-state count is needed.

The proof also establishes the more informative restriction

```text
a+b <= N
```

when the least period of the eventual tail is `2^a*b`, with `b` odd.

## 2. Pure-tail residual states

Suppose `u` is eventually periodic with least tail period
`p=2^a*b`. Extend its eventual tail to a purely periodic sequence
`v` on all nonnegative integers. For each residue `r mod p`, define
the residual function on finite binary words

```text
f_r(w) = v(2^|w|*r + val(w)).
```

Minimize the original DFAO for the proof only. Write `n<=N` for its
state count. For every residue `r`, choose a sufficiently large
positive prefix integer `x` congruent to `r mod p`. All integers
obtained by appending digits to `x` are past the onset, so the state
reached after reading `x` has residual function exactly `f_r`.
Consequently the distinct `f_r` form a subset `Q_tail` of `M<=n`
states of the minimized original automaton. This subset is closed
under both transitions, since

```text
delta_d(f_r) = f_(2r+d).
```

Every sufficiently large prefix integer reaches a state in `Q_tail`.

If `f_r=f_s`, take a suffix length `ell` with `2^ell>=p` and
`ell>=a`. Equality on all suffixes of this length compares two
shifts of `v` on at least `p` consecutive arguments. Minimality of
`p` implies `p | 2^ell(r-s)`, and therefore `b | (r-s)`. Thus
different residues modulo `b` always give different residual states.

## 3. The 2-adic exponent consumes states too

For `k>=0`, put an equivalence relation `E_k` on `Q_tail` by

```text
q E_k q' iff delta_w(q)=delta_w(q') for every word w of length k.
```

These are equalities of successor **states**, not merely their
current output bits. `E_0` is equality and the relations increase.
They obey

```text
q E_(k+1) q' iff delta_0(q) E_k delta_0(q')
                 and delta_1(q) E_k delta_1(q').
```

Hence a plateau is permanent: `E_k=E_(k+1)` implies equality at
all later levels.

At level `a`, `E_a` has exactly `b` classes, indexed by `r mod b`.
Residues equal modulo `b` become identical modulo `p` after `a`
appended digits. Conversely, residues unequal modulo `b` still have
unequal successor residuals, by Section 2 and invertibility of 2
modulo `b`.

If `a>0`, the period `p/2` is not a period of `v`. Choose `j` such
that `v(j) != v(j+p/2)`, and write

```text
j = 2^(a-1)*r + z,             0<=z<2^(a-1).
```

After appending the `(a-1)`-digit word of value `z`, states `f_r`
and `f_(r+b)` have unequal output bits. They are therefore not
`E_(a-1)`-equivalent, although they are `E_a`-equivalent. There
can have been no earlier plateau. All `a` increases from `E_0`
to `E_a` are strict, each reducing the number of classes by at
least one. Thus

```text
M >= a+b.
```

For `a=0`, the same inequality is already Section 2. This proves
`a+b<=N`. In particular `a<=N-1`, `b<=N`, and `p` divides the
stated conservative `P`.

## 4. Bounding the onset directly

There are `n-M` states outside the closed set `Q_tail`. A path
reading a canonical positive prefix cannot repeat a state while
remaining outside this set. Repeating the intervening nonempty
digit block would give arbitrarily large positive prefix integers
ending in that same outside state, contradicting Section 2.
The canonical first digit remains 1 even when the repeated block
begins at the root.

It follows that after at most `n-M` canonical digits the path is
inside `Q_tail`. Let the integer represented by this prefix be
`x`, and suppose the reached state is `f_r`. Comparing sufficiently
long appended words shows

```text
x = r mod b.
```

Indeed, on sufficiently large resulting integers the original
sequence agrees with `v`, whereas the state `f_r` gives the shifted
values of `v`; choose a suffix length containing a full period of
such arguments and use minimality of `p`, just as in Section 2.
If `n-M=0`, the prefix is empty and `x=0`; in that case choose
suffix values past the onset spanning a full period. The same
argument applies.

After at least `a` more digits, the difference `x-r` is multiplied
by a multiple of `2^a`. It was already divisible by `b`, so the
full residues modulo `p` now agree. The output is exactly the
pure periodic extension `v`.

Thus every canonical positive input whose digit length is at least

```text
n-M+a <= n-b <= N-1
```

already agrees with `v`. In particular every `n_integer>=2^N`
does. Its period divides `P`, proving necessity in Section 1.
Sufficiency is the definition of eventual periodicity. QED.

Both the period proof and the onset proof were reviewed independently.
They use the actual MSB residuals and never construct reversed states.

**Sharper optional corollary (U).** The same proof permits

```text
H_sharp = 2^max(0,N-2),
P_sharp = 2^(N-1) * lcm(odd positive integers <=N).
```

For `N>=2`, every integer at least `2^(N-2)` has at least `N-1`
canonical digits, so Section 4 applies. A one-state automaton is
constant. Section 3 gives the period divisor directly. The sharper
constants for observable sizes 4 through 8 are:

| States | H_sharp | P_sharp |
|---:|---:|---:|
| 4 | 4 | 24 |
| 5 | 8 | 240 |
| 6 | 16 | 480 |
| 7 | 32 | 6,720 |
| 8 | 64 | 13,440 |

The separate off-by-one audit passes. An independent regression,
`msb_period_sharp_audit.py`, classifies the same 738 small MSB
machines by reversing them and invoking the prior LSD theorem,
then checks the sharper equality by an independent exact addition
product. Every eventually periodic machine passes; the sharp products
inspect 8, 78, and 3,780 states for sizes 1, 2, and 3 respectively.
The main direct checker below retains the conservative constants to
preserve its issued certificates. Neither pair of bounds is claimed
optimal.

## 5. Exact MSB addition product

The implementation also avoids reversal when checking the equality.
It reads padded binary expansions of `n`, `n+P`, and the constant
`P` from left to right. Before the fixed digits of `P`, it permits
arbitrarily many leading zeros. At each digit it retains the carry
`c_out` into the already-read higher position and guesses the carry
`c_in` from the next lower position. The local equation is

```text
n_bit + P_bit + c_in = shifted_bit + 2*c_out.
```

The initial high carry and final low carry must both be zero. These
equations, summed with their binary place values, are exactly
`shifted_n=n+P`; no arithmetic approximation is used.

A product state retains the two original DFAO states, that carry,
the position in the fixed constant (or its leading-zero phase),
and the number of significant digits of `n` capped at `N+1`.
The last coordinate tests `n>=2^N` exactly. An accepting state has
consumed the constant, has zero carry, passes the threshold, and
has different output bits. Breadth-first search either supplies
an exact integer mismatch or exhausts the finite product.

The product has at most

```text
2*N^2*(bitlength(P)+1)*(N+2)
```

states. This is `O(N^3 log P)`, using the original observable
automaton directly. Scalar evaluation separately replays each
returned mismatch.

## 6. Independent finite regressions and Rule 90

All labelled reachable MSB automata of sizes 1 through 3 with a
leading-zero root self-loop were classified. For regression only,
each was also reversed and tested by the independently established
LSD checker. All classifications agree.

| States | Machines | Eventually periodic | Aperiodic | Direct product states visited |
|---:|---:|---:|---:|---:|
| 1 | 2 | 2 | 0 | 36 |
| 2 | 16 | 12 | 4 | 984 |
| 3 | 720 | 292 | 428 | 126,840 |

The scalar regression performs 20,016 additional comparisons. Four
named automata are checked against their formulas at 4,096 integers
each. The three-state MSB automaton for the Rule 90 lone-seed
neighbour has the exact aperiodicity witness

```text
N=3, H=8, P=48, n=31:
r(31)=1, r(79)=0.
```

Its formula `[n>0 and n=2^j-1]` is independently compared with
256 neighbour samples from the unchanged ladder Rule 90 engine,
using 66,048 scalar cell updates. Unchanged
`controls.rule90_control(6)` also passes all three cases.

The theorem correctly certifies aperiodic Rule 90 signals. It is a
generic observable test, not a Rule 30 proof. A proposed Rule 30
counterdiagram must still have its automatic local rule identities
verified at every coordinate before this observable test is useful.
Any added clocks, masks, coordinate restrictions, or subsequence
encodings require their own justified reachable-state count.

## 7. Reproduction and use

```sh
uv run python experiments/rule30/r1-isolated-column/msb_automatic_period_bound.py
uv run python experiments/rule30/r1-isolated-column/msb_period_sharp_audit.py
```

This verifies the saved
`experiments/rule30/r1-isolated-column/msb-automatic-period-bound.json`.
The callable `mismatch(delta, output, start=0)` accepts transitions
in MSB digit order, requires a leading-zero root self-loop, and
returns either an exact aperiodicity witness or an eventual-periodicity
verdict with the proved `H,P`. Its production path performs no
reversal. Finite regressions calibrate the implementation; they do
not establish the all-length theorem.

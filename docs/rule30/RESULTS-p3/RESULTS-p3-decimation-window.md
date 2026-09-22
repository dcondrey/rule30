# A nonlinear singleton decimation law has an exact collision

Date: 2026-09-13. **A specified shortcut class is refuted; P3 remains open.**
The new counterexample concerns the actual singleton center sequence, with
`c_0=1`. It does not use auxiliary reconstruction frontiers or arbitrary
initial rows.

Two independently recomputed indices refute every proposed rule of the form

\[
c_{2n+b}=F_b\bigl(\ell(n),n\bmod4,
                 c_{n-R},\ldots,c_{n+R}\bigr),\qquad b\in\{0,1\},\tag{1}
\]

valid at every `n>=R`, for every fixed `R<=8`. Here `ell(n)` is binary index
length. The functions `F_b` may be nonlinear, have arbitrarily large tables,
and depend arbitrarily on the supplied length. Each branch is separately
impossible. The functions receive only the displayed arguments; allowing the
remaining index digits as another unrestricted argument would change the
claim.

## 1. Exact singleton witness

| Half index `n` | Binary index | `ell(n)` | `n mod4` | `c_(n-8)..c_(n+8)` | `(c_(2n),c_(2n+1))` |
|---:|---|---:|---:|---|---|
| 1863 | `11101000111` | 11 | 3 | `00000010000101101` | `(1,0)` |
| 2011 | `11111011011` | 11 | 3 | `00000010000101101` | `(0,1)` |

The inputs of each `F_b` coincide, whereas its required outputs differ.
This is a complete counterexample to (1), not an extrapolation from a fit.
Every smaller centered window also agrees, proving the result for all
`R<=8`. The witness does not rule out a formula asserted only after an
unspecified later threshold, a larger radius, a richer index control, or
additional joint state.

The verifier also retains two shorter radius-four controls. Indices `200`
and `244` have common window `110110010` and different outputs in both
branches. Indices `220` and `228` have common window `101100011` and
different odd-branch outputs. In each pair the index lengths and residues
modulo four agree.

The older [binary-kernel probe](ARM6-binary-kernel.md) excluded small linear
representations and established finite lower bounds on kernel size. The
new collision does not assume linearity or a fixed finite state space. It
instead specifies what singleton information a proposed doubling law may
read. Neither result proves that the complete binary kernel is infinite.

## 2. Why a valid law of this form would supply a query algorithm

This paragraph is a **conditional construction**, not a discovered Rule 30
law. Suppose an explicit, correct law (1) with some fixed radius `R` were
given, together with its necessary fixed initial values. Define the larger
window

\[
Q_n=(c_{n-2R},\ldots,c_{n+2R}).\tag{2}
\]

To compute any entry `c_m` of `Q_n`, write `m=2k+b`. If
`h=floor(n/2)`, then `h-R<=k<=h+R`; consequently the entire radius-`R`
window needed by (1) lies inside `Q_h`. Thus **one recursive call computing
`Q_h` supplies every input needed to compute `Q_n`**. There is no branching
into independent smaller-index queries.

For a fixed small threshold, all entries of `Q_n` are supplied by a fixed
initial table. Above that threshold, the recursion just proved is valid;
negative indices are never passed to (1). The provided implementation uses
threshold `4R+2`, stores initial values through `6R+2`, and makes at most
`ell(n)+1` recursive calls. These constants are sufficient rather than
claimed optimal.

If each explicit `F_b` evaluation costs `A(ell(n))` bit operations, the
direct implementation costs

\[
O\!\left((R+1)\ell(n)A(\ell(n))
        +(R+1)^2\ell(n)+(R+1)\ell(n)^2\right),\tag{3}
\]

where the second term charges window copying and the third conservatively
charges integer arithmetic and index controls. This also covers `R=0`.
In particular, a uniformly supplied law with polynomial cost in
index length would give a polylogarithmic exact singleton query algorithm.
Fixed tables can be part of one finite program; constructing any
query-dependent table, or obtaining unproved values from a saved center
archive, must instead be charged. A finite fitted law has no certified
continuation and cannot serve as the premise of this construction.

This makes the failed hypothesis a concrete algorithm proposal: it would
close one shrinking-index recursion if true. The collision shows that its
seventeen observed center bits and two index controls do not close it.
No larger summary is supplied by this result.

## 3. Exact verifier and resource scope

- [Verifier](../../experiments/rule30/p3_decimation_window.py).
- [Saved artifact](../../experiments/rule30/p3-decimation-window.json).

The verifier independently evolves a literal eight-entry Rule 30 truth
table on growing rows and the maintained integer-row engine through time
`4023`. All 4,024 center bits agree; this bounded recomputation validates the
specific witness and is not a prefix extension or census. An existing
8,388,608-bit archive supplies an additional comparison with explicit
LSB-first decoding, zero payload offset, and SHA256 provenance. The
recomputed witnesses remain independently validated if that optional cache
is unavailable.

The conditional recursive algorithm is also implemented. Its positive
control is the exact Thue–Morse law `t_(2n+b)=t_n XOR b`, checked at four
window radii and eight directed indices, including `1,000,003`; those
control queries use the recursion, not cellular-automaton simulation.

Run with the approved local runner:

```sh
uv run --offline --no-project python experiments/rule30/p3_decimation_window.py
```

The saved run passed in approximately one second. No paid compute, large
kernel scan, or long-prefix regeneration was used. No conclusion about
eventual periodicity, an unrestricted computational lower bound, or a
working Rule 30 shortcut follows.

# Four-phase indexed restart for the endpoint Craig morph

Date: 2026-09-02

Status: **A NEW ALL-LENGTH SECTION, A FOUR-PHASE INDEXED RESTART LAW, AND
THE EXACT EXCEPTIONAL ZERO-CUT FIBER ARE PROVED.  TOGETHER THEY ELIMINATE
THE LAST POSSIBLE EQUALITY IN THE KNOWN GAP CONDITION, BUT DO NOT YET PROVE
THE RANK-ZERO SEPARATOR OR PERIOD-TWO EXCLUSION.**

The solver-free checker is `endpoint_restart_cocycle.py`.

## 1. Two exact sections of the endpoint morph

Let `I` be the inverse terminal cone, `T=I^(-1)`, `P` be Peel, and

```text
F = T o P o I.
```

The earlier Craig calculation proved the leading-`2` section.  The same
local square gives the complementary leading-`0` section:

```text
F(0e) = r_0(e_0) . F(e),    r_0=(2,3,1,0),
F(2e) = r_2(e_0) . F(e),    r_2=(1,0,2,3).            (1)
```

Here `e` is any nonempty four-state word; no hard-core or periodicity
hypothesis is used.

**Proof.**  Put `x_0=B(e_0)` and `a=phi(q,x_0)` for `q` equal to `0` or
`2`.  The endpoint-prefix grammar gives

```text
I(qe) = (B(q),a) . P(I(e)).                           (2)
```

For `r=r_q(e_0)`, the complete eight-row local check is

```text
B(r) = phi(B(q),a),
phi(r,s) = phi(a,s) for every s in {0,1,2,3}.          (3)
```

Equations (2)--(3) identify `P(I(qe))` with
`I(r . F(e))`, proving (1) by bijectivity of `I`.  This is a finite local
proof of an arbitrary-word identity, not bounded enumeration.  The checker
also verifies the resulting sections on every suffix through its requested
control length.

For reference, the first output symbol for every adjacent pair is

```text
q=0: 2 3 1 0
q=1: 0 1 3 2
q=2: 1 0 2 3
q=3: 3 2 0 1,                                        (4)
```

with columns indexed by the following endpoint symbol `0,1,2,3`.

## 2. Exact four-phase restart

Define

```text
p_0=12,  p_1=03,  p_2=10,  p_3=00.                  (5)
```

Equation (1), followed by one lookup in (4), proves the prefix transition

```text
F(2^m p_r v) begins 2^(m-1) p_(r+1 mod 4)            (6)
```

for every `m>=1`, every phase `r`, and every suffix `v`.  Induction gives
the indexed restart law

```text
F^t(2^k 12 v) begins 2^(k-t) p_(t mod 4),
                                      0 <= t <= k.    (7)
```

Thus the moving forbidden coordinate isolated by the Craig morph is not an
untyped defect.  It carries an exact mod-four phase:

```text
12 -> 03 -> 10 -> 00 -> 12.
```

After four applications of `F`, a hard-core prefix of the same form returns
with four fewer leading `2`s.  This is the requested indexed restart data;
it does not assert that the unshown suffix is hard-core.

## 3. Consequence for a hypothetical zero-tail endpoint

Suppose a hard-core endpoint `e` had

```text
x=I(e)=y 0^omega
```

with finite `y`.  For every sufficiently large `j`, the rotated-Peel
identity gives

```text
P^j(I(sigma^j e)) = sigma^(2j)x = 0^omega,
F^j(sigma^j e) = T(0^omega).                          (8)
```

The first symbol of `T(0^omega)` is `3`.  If `sigma^j e` began with at
least `j` copies of `2` before its next `1`, (7) would make the first symbol
of the left side of (8) either `2`, `0`, or `1`, never `3`.  Hence its next
`1` occurs at an offset strictly smaller than `j`.  The same argument rules
out an all-`2` suffix, so a hypothetical endpoint has infinitely many `1`s.

There is a phase refinement at the last possible offset.  If that offset is
`j-1`, one further application of `F` reads the pair `p_(j-1 mod 4)`.  By
(4), its first output can be `3` only when

```text
j-1 = 0 mod 4.                                       (9)
```

It remains to decide whether this one phase can actually attain equality.
It cannot; the obstruction is an exact fiber calculation rather than a
longer prefix search.

Put

```text
z = T(0^omega),       u_* = T(2^omega).
```

If `F(u)=z` and `u_0=1`, then injectivity of `T` gives
`P(I(u))=0^omega`, while `I(u)_0=B(1)=2`.  Every row of `phi` is a
permutation, so a Peel output and the first input symbol determine the
whole input from left to right.  The unique lift is therefore
`I(u)=2^omega`, or

```text
u = u_* = 1200320330210211... .                       (10)
```

Let `U_k` be the unique `k`-fold inverse branch of `u_*` whose first
symbol at every lift is `2`.  The leading-`2` section proves
`U_k=2^k W_k`.  More precisely, a fixed prefix of `W_k` evolves autonomously:
for a word `w` of length `L`, let `H_L(w)` be the unique word `v` of length
`L` satisfying

```text
v_0 = r_2^(-1)(w_0),       F(v)=sigma(w).              (11)
```

Then `W_(k+1)[0:L]=H_L(W_k[0:L])`.  Existence and uniqueness in (11) are
the same row-permutation calculation used above, so this is an exact finite
quotient of the infinite words, not a truncation assumption.

For `L=5`, the orbit starts at `T(2^5)=12003`, is purely periodic of period
32, and its eight states at indices `k=0 mod 4` are

```text
12003, 12321, 12111, 12211,
12012, 12332, 12103, 12203.                            (12)
```

Every word in (12) either contains `0` or `3`, or contains `11`; none is
hard-core.  Thus the only phase allowed by (9) is also impossible.  This
five-symbol calculation is an exhaustive traversal of a proved autonomous
quotient, so its period-32 return proves the statement for every `k`, not
only for 32 tested values.

Let `k_i<k_(i+1)` be successive positions of endpoint symbol `1`.  Taking
`j=k_i+1` in (8), hard-core legality supplies the intervening `2`-run.
Equations (7)--(12) now prove the uniform eventual bound

```text
k_(i+1) <= 2k_i.                                      (13)
```

This removes two units from the previous compact-influence consequence
`k_(i+1)<=2k_i+2`.  More importantly, the proof identifies and eliminates
the exact residual fiber carried by an extremal gap instead of treating
every covering interval alike.

## 4. Limit and next obligation

Equation (13) still permits infinite defect sets (for example, a doubling
sequence), so it is not the rank-zero contradiction.  The next useful step
is to generalize the autonomous tail quotient from the eliminated equality
fiber to a scale-sensitive band below equality.  Any proposed quotient must
reproduce (1), (6), (11), and the existing interior-queue closure
counterexamples.  Merely reusing the scalar gap bound discards the new
information.

## 5. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/endpoint_restart_cocycle.py
```

The printed arbitrary-word and prefix counts are regression controls.  The
all-length proof consists of the local-square calculation (2)--(3), the
induction (6)--(7), row-permutative uniqueness of the fiber (10), and the
complete return of the autonomous five-symbol quotient (11)--(12).

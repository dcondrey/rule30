# A source defect has an exact correction and a sufficient erasure length

Status: **all-length prefix identities, an exact ordered correction at every
depth, and a sharp padding theorem for uniform prefix erasure are proved**.
The full RW separator and period-two exclusion remain
open. These are identities for the exact endpoint morphism, including the
ordered suffix; no finite-state replacement for the whole suffix is made.

The first defect is confined to one endpoint symbol at `F^3` (§2).
Sections 5–6 give its ordered cocycle at every depth and the exact minimum
pure-`2` padding for erasure at the displayed-prefix cutoff. The simpler
bound in §1 supplies the synchronization induction used by that sharper
result.

Write `F=T P I`, `R_a(v)=F(av)`, and use the bijection
`J(v)=(v_0,F(v)_0,F²(v)_0,...)` and seven-state machine from the
[endpoint-section report](../../experiments/rule30/p1-period2-invariant/RESULTS-ENDPOINT-SECTION-MACHINE.md).
In `J` coordinates, `F` deletes one symbol and `R_1,R_2` act as the
invertible machine states `B,C`. For a prefix `w`, its exact suffix action
is defined by `J(wv)=J(w) M_w(J(v))`. Composition is leftmost after
rightmost.

## 1. A positive rule at every source depth

For every integer `k>=0` and every finite four-state suffix `v`,

\[
 F^{4k+3}(2^k1\,2^{3k+2}v)
   =F^{4k+3}(2^{4k+3}v).                         \tag{1}
\]

Thus the prefix `2^k1 2^(3k+2)` can be replaced by `2^(4k+3)` whenever
the RW source `W` begins with the displayed block and that block lies
entirely inside `W`. This does not authorize substitution after an
arbitrary left context. Every later
`F^n` image then agrees. The length and binary source alphabet are
preserved, the number of source `1`s decreases, and the hard-core suffix,
its junction, and terminal `12a` condition are unchanged. This applies to
both constant target tails and every residue `r`.

**Proof of (1).** The seven machine states form a closed set, each state
has section `C` after reading `222`, and `C` fixes the infinite all-`2`
word, with section `C` after `2`. Consequently any ordered composition of
`k` states has section `C^k` after `2^(3k)`.

For clarity, this last statement is an induction on composition length,
not an independence assertion. After the inner `k-1` states read the
first `3(k-1)` input symbols, their section is `C^(k-1)`. They therefore
output `222` on the next three input symbols and retain that section.
The outer state has reached some state of the same closed seven-state
set; reading these final three output symbols puts its section in `C`.
The composite section is exactly `C^k`.

The previously proved identity `J(122v)=130 C³(J(v))` gives

\[
 M_{2^k122}=T_k C^3,\qquad
 T_k=(C^k)|_{130},                              \tag{2}
\]

where `T_k` is a composition of exactly `k` states. Append `2^(3k)` to
this prefix. Its `J` image is still `2^(3k)`, and its suffix action is
`C^(3k)`. Applying the induction to `T_k` in (2) gives

\[
 M_{2^k122\,2^{3k}}=C^{k+3}C^{3k}=C^{4k+3}.
\]

This is also `M_(2^(4k+3))`. Deleting the entire prefix in `J` coordinates
proves (1). The argument has no upper bound on `k` or on the suffix length.

At depth `k=2`, a shorter exact rule is available:

\[
 F^7(2212222v)=F^7(2222222v).                    \tag{3}
\]

Indeed `M_22122=BC⁴`, while the sections of both `B` and `C` after `22`
are `C`. Hence `M_2212222=C⁷=M_2222222`.

Together with the [homogeneous-source exclusion](RESULTS-rw-homogeneous-source-exclusion.md),
(1) excludes every RW source of the form `W=2^k1 2^m` with
`m>=3k+2`. Formula (3) also excludes `W=2212^m` for `m>=4`.
These are sufficient run-length conditions, not a normalization theorem
for all sources. Shorter or interrupted runs can retain a nontrivial
ordered correction.

If an additional source restriction excludes `22222`, the general rule
for `k>=1` cannot apply because `3k+2>=5`. The shorter rule (3) does not
contain five consecutive `2`s. The all-length identities remain valid,
but their applicability must be checked against the actual source language.
Their replacement words do contain five consecutive `2`s: these reductions
preserve the stated RW guards, not the strengthened `22222` avoidance
restriction or actual-orbit ancestry.

## 2. The first short-run defect is a correction, not immediate erasure

For every suffix `v`, the exact identities are

\[
\begin{array}{lll}
 F^3(22122v)=02R_2^3(v), && F^3(22222v)=22R_2^3(v),\\
 F^4(22122v)=1R_2^4(v),  && F^4(22222v)=2R_2^4(v),\\
 F^5(22122v)=R_1R_2^4(v),&& F^5(22222v)=R_2^5(v).
\end{array}                                                   \tag{4}
\]

These follow from the finite symbolic section identities

`J(22122)=22101`, `M_22122=BC⁴`,
`J(22222)=22222`, `M_22222=C⁵`,
`J(02)=01`, `M_02=BC`, and `M_22=C²`.
The shared suffix in the first line is exact. Only the first endpoint
symbol differs at that time, from `2` to `0`; the common following `2`
is part of the correction's context. That correction cannot simply be
deleted.

For example, the common suffix `Q=1212121` preserves the hard-core
junction and terminal `121`, but

```
F^4(22122 Q)  = 11230303    F^4(22222 Q)  = 21230303
F^5(222122 Q) = 01333210    F^5(222222 Q) = 20333210.
```

These controls refute the corresponding shorter erasures. They do not
refute RW, since neither side is being asserted to meet a constant target.

## 3. No fixed later time erases the short defect for every arbitrary suffix

For every `h>=0`, there exists a finite four-state suffix `v_h` such that

\[
 F^{5+h}(22122v_h)\ne F^{5+h}(22222v_h).          \tag{5}
\]

At time five the two `J` words are `BC⁴(J(v))` and `C⁵(J(v))`.
For `h>=2`, choose `y=21 3^(h-2)0`. After reading `21`, the respective
`B,C` sections are `G,A`; both retain their own state on `3`, and their
outputs on `0` differ. Therefore their outputs at position `h` differ.
Set `v_h=J^-1 C^-4(y)`, which exists because both actions are bijective.
For `h=0,1`, use `y=0,20`, respectively. This proves (5) at all lengths.

The suffixes in this construction are arbitrary four-state words.
It does **not** establish a hard-core suffix with terminal `12a` for every
`h`. It is compatible with the positive guarded rules (1) and (3).
The particular infinite suffix `2^infinity` coalesces after seven steps;
its first five cut cells follow the exact orbit

```
12303 -> 11321 -> 20121 -> 31121 -> 22121 -> 02121 -> 32121 -> 12121.
```

## 4. Exact verification and remaining obligation

The maintained [verifier](../../experiments/rule30/rw_defect_cocycle.py)
and [artifact](../../experiments/rule30/rw-defect-cocycle.json) check the
seven local `222` sections, the symbolic correction identities, and the
distinguishing-state loop underlying (5). They also retain 17 symbolic
composition controls (`k=0..16`), 42 direct endpoint checks of (4),
21 direct checks of (3), seven explicit controls of (5), and the two
guarded examples above. The universal quantifiers in (1) and (5) come
from the stated inductions and fixed machine transitions, not these
bounded controls. No temporal or frontier census is run.

One precise candidate order is
`lambda(W)=(number of 1s in W, position of the leftmost 1)`, ordered
lexicographically, with positions counted from one and position zero
assigned to an all-`2` word. Every admitted prefix erasure strictly lowers
the first coordinate. The suffix `v` may contain additional `1`s, so these
rules also apply to some sources with several `1`s. What is not proved is
that a rule always remains applicable after the first erasure, or that a
guard-preserving move decreases the second coordinate otherwise.

The missing step is a guard-preserving reduction or separator for sources
whose short or interrupted runs evade these rules, including the sharper
criterion (9)–(10) below. A decreasing
number of source `1`s is a valid rank only when an applicable identity
preserves the full suffix action at the required time. Formula (4)
records the correction that such an argument must retain.

## 5. A periodic block formula for the full ordered correction

The exact orbit of the three-symbol point `130` under the action `C` is

```
130,002,101,020,132,001,103,023,
131,003,100,021,133,000,102,022,130.
```

Its period is sixteen. Write `g_i=C^i(130)` and `s_i=C|_(g_i)`. The
successive single-state sections are

```
C,B,A,D,B,E,E,B,E,A,B,G,A,C,C,C.
```

The ordered return section is therefore

\[
 L=s_{15}\cdots s_0=CCCAGBAEBEEBDABC.             \tag{6}
\]

With `T_0` the identity and `T_b=s_(b-1)...s_0`, the all-depth formula is

\[
 T_{16a+b}=T_b L^a,\qquad a\ge0,\quad 0\le b<16.\tag{7}
\]

**Proof.** The section law for composition is
`(gh)|x=(g|_(h(x)))(h|x)`. Since `C^16` fixes the entire point `130`,
its `a`-th power has section `L^a` there. Applying the final `C^b` gives
(7), with the order shown. This does not commute any of the machine
actions.

The relative defect after removing the initial `k+3` source symbols is

\[
 \Delta_k=T_kC^{-k},\qquad
 \Delta_{16a+b}=T_bL^a C^{-(16a+b)}.              \tag{8}
\]

Indeed the defect and homogeneous suffix actions are `T_kC³` and
`C^(k+3)` respectively, so the former is `Delta_k` applied to the latter.
Equivalently, `Delta_(k+1)=s_(k mod16) Delta_k C^-1`.
These are invertible ordered actions on the full suffix. A finite orbit
of the point `130` does not imply periodicity or bounded memory of the
residual action in (8).

## 6. Exact minimum padding for erasure at the full-prefix cutoff

Fix `k>=0`. Define `f(k)` to be the least integer `j>=0` for which

\[
 F^{k+3+j}(2^k122\,2^j v)
   =F^{k+3+j}(2^{k+3+j}v)
       \quad\text{for every finite four-state suffix }v. \tag{9}
\]

Both the displayed prefix and the cutoff in (9) include the extra
padding `j`. The exact answer is

\[
 f(0)=f(1)=0,\qquad f(2)=f(3)=2,\qquad
 f(k)=3k-8\quad(k\ge4).                         \tag{10}
\]

Thus the sufficient cutoff improves from `4k+3` in (1) to `4k-5` for
`k>=4`. The newly admitted short rule at `k=3` is

\[
 F^8(22212222v)=F^8(22222222v).                  \tag{11}
\]

These improvements are anchored source-prefix rules with the same RW
guard scope as §1. They exclude sources `W=2^k1 2^m` whenever
`m>=f(k)+2`, using the already proved homogeneous exclusion. They are
not arbitrary left-context substitutions.

**Reduction to a section.** Appending `2^j` to (2) gives

\[
 M_{2^k122\,2^j}=(T_k|_{2^j})C^{3+j}.
\]

The homogeneous suffix action is `C^(k+3+j)`. As these actions are
invertible, (9) is equivalent to

\[
 T_k|_{2^j}=C^k.                               \tag{12}
\]

**Upper bound.** The exact initial sections are `T_0=1`, `T_1=C`,
`T_2=BC`, `T_3=ABC`, and `T_4=DABC`. They give the paddings
`0,0,2,2,4` respectively. For `k>=4`, write `T_k=U T_4`, where `U`
is an ordered composition of `k-4` states. After four input `2`s,
`T_4` has section `C⁴`. The outer composition `U` has read a four-symbol
output prefix and reached another composition of `k-4` states in the
same closed machine. It therefore needs at most `3(k-4)` additional
input `2`s to reach section `C^(k-4)`, by the induction in §1.
This proves (12) with `j=4+3(k-4)=3k-8`.

**Lower bound: an exact advancing marker.** The notation `2^infinity`
below is a convenient way to describe finite-word actions on arbitrarily
long constant tails. Every distinction used has a finite witness.
Put `x_k=C^k(130 2^infinity)`. Direct finite section identities give

\[
 x_4=1320130\,2^\infty,
 \qquad C|_{1320}=A.                            \tag{13}
\]

Let `S={A,B,D,G}`. Consider the precise invariant class

\[
 x=P130\,2^\infty\quad\text{with }C|_P\in S.
\]

If `s=C|P`, the four machine identities are

\[
 s(130\,2^\infty)=H_s130\,2^\infty,
 \qquad H_A=310,\quad H_B=H_D=H_G=120.            \tag{14}
\]

Each finite prefix `130222` in (14) has output `H_s130` and section
`C`, which fixes the remaining constant tail. Consequently

\[
 C(x)=C(P)H_s130\,2^\infty.
\]

The new prefix is `P'=C(P)H_s`. To verify its required section, one must
retain `C|_(C(P))`, not infer it from `C|P`. It is some state `t` in the
closed seven-state set. The complete local table gives

\[
 t|_{310}\in\{A,G\}\subseteq S,\qquad
 t|_{120}\in\{A,B,D\}\subseteq S
       \quad\text{for every one of the seven states }t. \tag{15}
\]

These fourteen checks prove `C|P' in S` without any assumption about
`C|_(C(P))`. Thus the class is invariant. Its last non-`2` symbol is
the final `0` of the marker, and every iteration moves it exactly three
positions to the right. By (13), for every `k>=4`, that last non-`2`
symbol in `x_k` has zero-based position `3k-6`.

The first three symbols of `x_k` are `C^k(130)`, and the remaining
word is `T_k(2^infinity)`. Its last non-`2` symbol therefore has position
`3k-9`, so no `j<3k-8` can satisfy (12): the residual section still
produces a non-`2` on an all-`2` tail, whereas `C^k` fixes that tail.
For each such `j`, a finite witness to failure of (9) is
`v=2^(3k-8-j)`. This proves the lower bound at every `k>=4`.
For `k=2,3`, the root permutations of the sections at padding zero and
one differ from those of `C^k`; the verifier retains each distinguishing
input symbol. This completes (10).

In particular, taking one fewer padding cell than the minimum gives the
explicit one-cell witnesses, for every `k>=4`,

\[
 F^{4k-6}(2^k1\,2^{3k-6})=0,
 \qquad F^{4k-6}(2^{4k-5})=2.                   \tag{16}
\]

Here the last input `2` is the one-cell suffix in (9); the shortened
displayed prefix has length `4k-6`. Equality at a later cutoff for a
specific longer continuation is a different question.

**Scope of sharpness.** The minimum in (10) concerns equality for every
suffix at the full displayed-prefix cutoff `k+3+j`. It says neither
that a particular short guarded instance cannot coalesce later nor that
the same lower bound holds after restricting to actual RW continuations.
The all-`2` witnesses above do not assert the RW suffix length and terminal
`12a` constraints. Moreover an all-`2` replacement need not remain in a
strengthened source language forbidding `22222`.

The verifier now saves the entire sixteen-phase orbit and ordered block,
the exact small padding minima, the four identities (14), all fourteen
closure checks (15), and the finite base (13). Seventeen symbolic controls
also check the improved rule, but the all-`k` upper and lower bounds are
proved by the preceding inductions. No large enumeration is involved.

The [independent checker](../../experiments/rule30/rw_defect_cocycle_independent.py)
rederives the marker, closure, and synchronization identities from the raw
sixteen-state machine and checks directed finite controls against the older
endpoint engine. Its [saved audit](../../experiments/rule30/rw-defect-cocycle-independent.json)
passed. These local identities check the premises of the displayed
inductions; the finite controls alone do not establish the universal claims.

# A complete four-period central carry from one upstream period

Date: 2026-09-14. **Under a specified four-cycle monodromy, the complete
central carry over four periods can be computed by one scan of the
upstream period. No intermediate physical column or four replicated
histories need be constructed.** This is an all-length conditional
identity with an explicit constant-state evaluator. It applies to the
saved actual period8 driver and recovers its nonzero period32 correction.

The premise is an even upstream period and a quarter rotation on the
next physical digit. The conclusion concerns a complete four-period
block. The marked query is not assumed to end at such a complete
four-period block; this is not a sublinear P3 algorithm or a closure
of all period lifts.

## 1. Conventions and the period premise

Use the forward B zero orbit and the chronological carry convention in
the [Cartier report](RESULTS-p3-parity-string-cartier.md). For an upstream
digit z_t=p_t+2q_t, sampled at its UPDATED fine time t, put

```
c_t=p_t OR q_t,       d_t=1+q_t.
```

Bit sums are over F2. A first carry X=(U,V,W), initially000, obeys

```
U'=U+c,     V'=V+d,     W'=W+c*V.                (1)
```

Its physical digit is `(U,W+U+UV)`. If instead its initial physical
digit is(a,b), its physical value at time t is

```
(a+U_t, b+V_t*a+W_t+U_t+U_t*V_t).              (2)
```

The U,V,W on the right are the zero-initialized carry in(1). Formula(2)
follows by induction and is valid for every supplied driver history.

Suppose z_t has an even period P>=2, aligned so the period is
z_1,...,z_P. The assumption needed below is

```
U_P=V_P=1.                                      (3)
```

Its one-period physical action is consequently the quarter rotation

```
M(a,b)=(a+1,b+a+e),       e=W_P.                 (4)
```

Every starting digit visits all four digits under M. The period P may
be supplied rather than primitive; both periodicity and(3) must be
justified when using the theorem on the actual seed orbit. The evenness
of P ensures that the cuts into odd/even time pairs align in all four
copies. No new virtual origin is placed at a cut.

## 2. One-period signatures retain the chronological central term

At each even fine time, the next carry Y=(P2,V2,Q2) has the exact update

```
(P2,V2,Q2) -> (P2+g,V2+f,Q2+g*V2+E),           (5)
```

where, for the upstream digit(p,q) and current first physical digit(a,b),

```
c=p ORq,
g=c*(1+b+a*q),
f=c+a*(1+q),
E=a*b+c*(a ORb)+a*q.                            (6)
```

There is no hidden orientation or odd-time physical digit in(6).
The current a,b in(6) are the UPDATED digits, not their values at the
start of the period.

Holding the upstream period fixed, the complete action(5) over one
period can be written as a function of the first digit's INITIAL(a,b):

```
(P2,V2,Q2) -> (P2+G,V2+F,Q2+G*V2+H),
G=g0+ga*a+gb*b,       F=f0+fa*a,
H=h0+ha*a+hb*b+hab*a*b.                          (7)
```

Indeed(2) makes every paired g affine and every paired f affine with
no b coefficient. Composition preserves these two properties. The
central function H can be represented by its four Boolean coefficients.
Its ordered cross term is `g_later*f_earlier`, as required by(5).

**Four-cycle identity.** Four consecutive copies of(7), with the first
digit advanced by(4) between copies, return the first digit, P2 and V2.
They change Q2 by exactly

```
kappa = hab + fa*ga + e*fa*gb + f0*gb.          (8)
```

This holds for every initial first digit and every initial Y. The
constants g0,h0,ha,hb cancel. For example, starting the first digit at00,
its four values are `00,(1,e),01,(1,1+e)`. Summing H on these gives hab.
Substituting the corresponding G,F into
`sum_(s<r)G(M^r(00))*F(M^s(00))` gives the three remaining terms in(8).
Starting elsewhere cyclically rotates the same orbit. Since total G
and F are zero, this rotation does not change the central sum. The
verifier separately checks all32768 Boolean coefficient/initial-state
assignments, including the chronological order and phase e.

## 3. Every coefficient needed in(8) comes from the upstream drivers

All sums in this section run over EVEN times t=2,4,...,P. Define a
second, decimated carry directly from these upstream pairs(c_t,d_t):

```
C = sum_even c_t,
D = sum_even d_t,
Wdec = sum_(even s<t) c_t*d_s,
K = sum_even (1+c_t).                            (9)
```

There are also two chronological prefix sums, using the U_t,V_t of(1):

```
A = sum_even c_t*(V_t+1+d_t),
F0 = sum_even (c_t+d_t*U_t).                     (10)
```

Then the coefficients in(8) are exactly

```
gb=C,       fa=D,       ga=A,       f0=F0,
hab=K+Wdec,       e=W_P.                         (11)
```

Here is the coefficient argument, which avoids constructing the first
physical history in(2). Inserting(2) into the even-time g,f in(6) gives

```
[a]g_t=c_t*(V_t+q_t),   [b]g_t=c_t,
[1]f_t=c_t+d_t*U_t,     [a]f_t=d_t,   [b]f_t=0.
```

Since q_t=1+d_t, summing proves the first four equalities. The coefficient
of ab in E_t is1+c_t: the affine change in(2) has a coefficient1 on ab,
and all other terms of(6) are affine. The coefficient of ab in the
chronological cross term `g_t*sum_(earlier even s)f_s` is
`c_t*sum_(earlier even s)d_s`. This proves hab=K+Wdec, including its
ordering. Finally(2) and(3) give e=W_P.

Combining(8)-(11) gives the promised upstream-only evaluation:

```
kappa = K+Wdec + D*A + W_P*D*C + F0*C.          (12)
```

No value of W_t at an intermediate time is needed in(10); only its final
value W_P is needed. The ordinary first-carry low/orientation prefixes
U_t,V_t remain part of the computation and are charged.

There is a simpler trace identity for the explicit Cartier correction:

```
sum_(r=1..2P) E_(2r) = K
  = parity of zero upstream digits at even times in one period.       (13)
```

At each fixed even phase, four copies of the period give all four first
digits. Summing(6) over these digits leaves1+c_t. Similarly the total g
and f over four periods vanish. Equation(13) alone is insufficient for
the full central carry: (12) also retains the ordered area.

For reference, `A+F0=sum_even Delta(U_t*V_t)`. This identity does not
silently set A=F0 or C=D. A four-cycle alone does not force C=D: the
supplied period `0,1,1,2` satisfies(3) but has C=0,D=1. It is an
arbitrary driver control, not an asserted actual seed period.

## 4. Actual seed control and exact cost

The saved complete three-digit orbit certifies that actual driver
column1 has period8, with chronological digits

```
1,2,1,3,0,3,0,0.
```

Its next-digit monodromy satisfies(3), with e=1. The one-period scan gives

```
C=D=A=1,       F0=0,       hab=1,       K=1.
```

Thus(12) gives kappa=1. The even-phase upstream digits are2,3,3,0,
so(13) also gives K=1 immediately. This recovers the separately saved
actual period32 holonomy: the first carry returns000, the second returns
`(P2,V2,Q2)=(0,0,1)`, and the fourth physical digit of B^32(0) is2.
The actual driver and the fourth-digit certificate are reused; no
longer period or singleton prefix is generated.
This control is at time32 and digit3, outside the marked-query offsets
`time-digit` in{2,3}; it is not a direct diagonal speedup.

The [evaluator](../../experiments/rule30/p3_four_period_central_carry.py)
scans P upstream digits and performs P/2 decimated updates. It uses nine
running Boolean bits, a phase/counter, and O(P) Boolean work. Counter,
input construction and access costs remain charged. In contrast, its
independent control follows four complete driver copies; those extra
steps are validation work, not part of the new evaluator.

For each fixed input digit and phase, the nine-bit update is affine
over F2. The checker verifies all4096 such input/state assignments.
Consequently a supplied concat/Repeat grammar can be annotated by two
parity-indexed affine maps and its length parity. Concatenation composes
the maps in order; repetition uses ordinary binary powering, including
the alternation of starting phase for an odd-length repeated word.
This gives fixed-size aggregation of a supplied temporal grammar, with
grammar construction and exponent arithmetic still charged. The code
implements these small affine block operations: a block has two10-by-10
homogeneous Boolean maps, one for each starting phase, and a length
parity. Its concatenation chooses the second map at the phase left by
the first block. Each matrix column is a ten-bit integer;
no whole-history integer operation is hidden in those maps.

In fact the supplied-counter repeat exponent has a uniform reduction.
Partition the nine counters as

```
X=(U,V,C,D,K),       Y=(W,Wdec,A,F0).
```

For a fixed digit and phase, and hence for any fixed word and starting
phase, the action has the form

```
X'=X+r,       Y'=Y+L*X+s.                        (14)
```

The base counters are only translated; no upper counter enters the
increment of another upper counter. Two actions compose as
`(r+r',L+L',s+s'+L'*r)`. Squaring one action therefore leaves X fixed
and translates Y by Lr. Its fourth power is identity. Every even-length
word preserves the starting phase, so its full counter action has
fourth power identity. An odd-length word squared is even, so its eighth
power is identity. These bounds are sharp for the supplied words02
and1 respectively, as checked on the complete affine matrices.

The repeat helper verifies form(14), reduces an exponent modulo4 for
an even-length word or modulo8 for an odd-length word, and composes only
the bounded remainder. Reading and reducing the binary exponent remains
charged; this takes O(log r) bit work, while the subsequent fixed-size
matrix work is bounded independently of r. This exponent bound is for
the nine-counter annotation, not the B dynamics or the physical word.

The block contract checks400 starting-phase/basis cases, odd-length
repeat words, and the actual period8 split into lengths3 and5. As a
separate supplied-grammar control, word012 repeated2^80+123 times reduces
to its third power modulo the universal odd-word bound8. The helper
reads an81-bit exponent and uses two binary rounds and three block
compositions after reduction, without constructing the expanded stream.
This artificial odd-length repeated word is
an aggregation control, not an actual seed history or an application
of the even-period theorem. No procedure for constructing the actual
driver grammar from a marked query is claimed.

## 5. What this does and does not close

This replaces a complete four-period central calculation by one
upstream-period scan and eliminates the intermediate physical history.
It is valid at every period length satisfying the premises, including
the actual period8 example; it is not extrapolated from that example.

The exponent bound has a useful scope control on that same actual
example. The period8 word repeated four times has the identity action
on all nine summary counters, yet its direct second carry ends001.
The summary of the32-position word has U=V=0 and fails premise(3).
Thus the finite annotation is not a general-prefix central evaluator:
the quarter-rotation premise and the four-block readout in(12) matter.

The required summary closes under concatenation and repetition of a
SUPPLIED driver word. Obtaining the next column's period summary is a
different operation: it transduces that word, with its entering digit
states and ordered boundaries. In fact a homogeneous update of this
particular annotation is false even on actual seed ancestry. Let z_j
be the word at column j and times1 through32 of the saved orbit. Then

```
z_0=(1230)^8,       z_1=(12130300)^4.
```

Both have length32 and the same COMPLETE phase-indexed affine action:
the identity. The same column transducer, started at physical digit0,
sends z_0 to z_1 and z_1 to z_2. The annotation of z_1 is identity, but
that of z_2 sends the zero summary to `(0,0,1,0,0,0,0,0,0)`.
Therefore the input annotation, length, phase, and entering digit do
not determine the next annotation. The verifier checks both complete
input maps and both chronological transductions using only the saved
three-digit orbit. Column-dependent updates or richer profiles are
outside this witness.

A bound on the profiles required by
repeated such transductions has not been proved. Likewise (12) gives
a complete four-period result, not a prefix that stops inside one
period. The theorem supplies no evaluation for unmatched query prefixes.
No recursive complexity bound or new period census is claimed.

The [artifact](../../experiments/rule30/p3-four-period-central-carry.json)
records the formal32768-case contract,32 complete local coefficient
contexts, the affine update checks,
160 directed supplied-period/initial-state comparisons,400 affine block
controls, the actual period8 control, the actual column-annotation
collision, and source hashes. Nonzero alternative initial states
in the control are algebraic probes; only the explicitly marked zero
initialization has actual seed ancestry.

```
uv run --offline --no-project python experiments/rule30/p3_four_period_central_carry.py
```

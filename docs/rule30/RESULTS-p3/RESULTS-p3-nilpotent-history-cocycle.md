# Corrected inverse squaring and its neighboring-history correlation

Date: 2026-09-14. **Every inverse time block has an exact class-two
group signature. Squaring uses that signature on the actual transformed
history. Its ordered double sum telescopes to one explicit correlation
between neighboring temporal histories.** The remaining correlation
does occur on the actual B orbit; it is not an origin-only term.

This extends the one-composition law in the
[inverse temporal-squaring report](RESULTS-p3-bitplane-temporal-squaring.md)
to every block length, and specifies a shared evaluation and its cost.
It does not close repeated dyadic spatial blocking or prove a fast P3
query. The [verifier](../../experiments/rule30/p3_nilpotent_history_cocycle.py)
and [artifact](../../experiments/rule30/p3-nilpotent-history-cocycle.json)
check the finite local algebra and the corrected composition.

## 1. A fixed group, with a nonconstant history argument

Put L=B inverse. Write the current input digit as p+2q and its
previous input digit as u+2v. The inverse local rule is

```
p'=p+c,       q'=q+d*p+e,
c=u OR v,    d=1+v,    e=c.                        (1)
```

All additions and products in the bit formulas are over F2. The last
identity follows from the unsimplified e=v+(1+v)c and c=u ORv.
At the origin the previous digit is the fixed virtual1 at every
inverse iteration, so(c,d,e)=(1,1,1). No second virtual digit is added.

For arbitrary coefficients, denote the digit action in(1) by g=(c,d,e).
If g is applied first and h=(C,D,E) second, define

```
g star h = (c+C, d+D, e+E+D*c).                    (2)
```

These eight actions form UT3(F2), equivalently the dihedral group of
order8. Acting on(q,p,1), the matrix is

```
[[1,d,e], [0,1,c], [0,0,1]].
```

Chronological composition in(2) is ordinary multiplication of the
second matrix by the first. The commutator is central, with coefficient
(0,0,D*c+d*C); g squared=(0,0,d*c), and every g has fourth power
identity. These identities also hold pointwise for coefficients that
are functions of the preceding input history.

The fixed group does not make the history argument fixed. At inverse
time t the local generator is evaluated on the predecessor digit of
L^t(X), not repeatedly on the predecessor digit of X.

## 2. The complete time-block signature and exact doubling

Fix a site j and an input prefix X through j. Let(c_t,d_t,c_t) be
the local coefficients at this site on L^t(X), including the repeated
origin convention. Write the ordered block signature as
G_N(X)=(C_N,D_N,E_N). Then

```
C_N = sum_(0<=t<N) c_t,
D_N = sum_(0<=t<N) d_t,
E_N = C_N + sum_(0<=s<t<N) d_t*c_s.               (3)
```

This is proved by appending one factor using(2). It holds for every
N>=0, with empty signature(0,0,0), and for every input prefix.

Let U be pullback by L on history-dependent coefficient functions:
(Uf)(X)=f(L(X)). Applying two chronological blocks gives

```
C_(2N) = C_N + U^N C_N,
D_(2N) = D_N + U^N D_N,
E_(2N) = E_N + U^N E_N + (U^N D_N)*C_N.          (4)
```

All three pulled-back functions are evaluated on the **same** middle
prefix Y=L^N(X). They do not require independently reconstructed
histories for C,D,E or for the four possible current-digit inputs.
The preceding history is independent of that current digit, so one
signature represents all four probes simultaneously.
This varies only site j while holding its preceding prefix fixed;
changing an earlier digit requires reevaluating the relevant history.

For a precise comparison with squaring the same group element twice,
put Delta_N f=U^N f+f. Equation(4) is

```
C_(2N) = Delta_N C_N,
D_(2N) = Delta_N D_N,
E_(2N) = D_N*C_N + Delta_N E_N
                         +(Delta_N D_N)*C_N.     (5)
```

Only D_N*C_N is the same-history central square. The remaining terms
are explicit history differences. Nilpotence alone does not set them
to zero. Equation(5) is the corrected squaring law; it preserves the
ordered middle history rather than replacing it by a decimated or
fresh input.

## 3. The ordered area telescopes to one adjacent-history correlation

Let p_t,q_t be the current digit bits in L^t(X), and let v_t be the
high bit of its left neighbor at the same inverse time. At the origin
take v_t=0. The local low-bit equation gives

```
c_t=p_t+p_(t+1),
C_N=p_0+p_N,
D_N=(N mod2)+sum_(t<N) v_t.                       (6)
```

The inner sum in the ordered area of(3) is
sum_(s<t)c_s=p_0+p_t. Therefore

```
E_N = C_N + p_0*D_N + sum_(t<N)(1+v_t)*p_t,

q_N = q_0+p_0+p_N+sum_(t<N)p_t
                         +sum_(t<N)v_t*p_t.      (7)
```

Thus the nonlinear term remaining after the low-bit telescoping is
the single chronological correlation

```
R_N = sum_(t<N) v_t*p_t.                          (8)
```

It involves both neighboring histories at matching times. Replacing
either history by a newly completed trace would change this term.
For arbitrary block lengths N,M it concatenates exactly as

```
R_(N+M)(X)=R_N(X)+R_M(L^N(X)).                   (9)
```

In particular the second half uses the same middle prefix Y required
in(4). Formula(7) is a reduction of the original ordered double sum,
not an endpoint-only expression: the single-time sums still have to
be obtained from the actual histories.

There is a further exact decomposition that identifies the exceptional
events. Since v_t=1 implies c_t=1, a high neighbor forces the low bit
to flip. Let m_N be the ordinary integer count of low-bit flips,
m_N=sum_integer c_t, and put a_t=1[the left digit at time t is1].
Then c_t=v_t+a_t and

```
R_N = (floor((m_N+p_0)/2) mod2)
             + sum_(t<N) a_t*p_t.                (10)
```

The values of p_t immediately before successive flips alternate,
starting at p_0. Their parity sum is floor(m_N/2)+p_0*(m_N mod2),
equivalently floor((m_N+p_0)/2) modulo2.
Only the previous digit1 gives the residual event a_t. This is another
ordered correlation, not a reason to discard the history.

## 4. A retained actual-orbit control

The existing exact orbit certificate proves

```
B^8(0)=003(0332)^infinity,
L^4(B^8(0))=B^4(0)=(03)^infinity.
```

Use site j=4 and four inverse steps. The local histories are

```
p_t, t=0..4: 11010,
q_t, t=0..4: 10100,
v_t, t=0..3: 0110.
```

Their correlation R_4 is1. The expression in(7) without this term
would give q_4=1; the exact answer is0. The checker reads the saved
seven-digit seed-ray certificate and takes four local inverse steps;
it does not regenerate a singleton center prefix or extend an orbit
census. This control shows that the term is active on the actual
orbit. It does not prove that every compressed construction of it is
expensive.

The correlation is also nonzero beyond every finite origin prefix.
At site j, four inverse steps use only the five original digits
at positions j-4 through j. More specifically, at inverse time t<=3,
p_t depends only on positions j-t through j, and its neighboring
high bit v_t depends only on positions j-1-t through j-1. Their union
lies in that five-digit window. This follows by induction from the
radius-one local inverse, and proves locality of R_4 without inserting
an origin boundary inside the window.

The already certified period0332 therefore gives every recurring case:

| Five-digit window | First terminal site j | R_4 |
|---|---:|---:|
| 03320 | 7 | 0 |
| 33203 | 8 | 1 |
| 32033 | 9 | 0 |
| 20332 | 10 | 1 |

Each row recurs after every four spatial positions. For example R_4=1
at every j=8+4k, k>=0, so no finite origin strip contains the entire
correlation correction on this actual ray. The checker evaluates each
window independently by repeatedly applying the inverse to adjacent
digits and deleting its first site: lengths5,4,3,2,1. It never supplies
a virtual boundary for these local calculations. The periodicity comes
from the saved whole-ray certificate, not from extrapolating these four
calculations. The correction in this example is itself periodic and
may still be represented cheaply.

## 5. A shared doubling evaluator and its honest work recurrence

The executable `inverse_block` returns both L^N(X) and its coefficient
field for a supplied m-digit prefix X, when N is a power of two.
At each doubling node it obtains the first transformed prefix and
signature once, uses that exact prefix for the second child, and
composes the two fields with(2). There are two recursive histories,
not separate histories for each coefficient or each entering digit.

For this explicit construction on a nonempty m-digit prefix, with
Boolean-operation unit costs,

```
W(1,m)=O(m),
W(2N,m)=2W(N,m)+O(m),
W(N,m)=O(N*m).
```

It performs N*m local digit updates and (N-1)*m group compositions.
A depth-first implementation retains O(m*(1+log N)) bits of intermediate
fields for N>=1 in addition to counters; copying, allocation, and integer
metadata are charged separately. Balanced formula depth does not make
the second recursive history available in parallel with the first.
For an empty prefix the listed digit-operation counts are both zero,
but this implementation still makes2N-1 recursive calls; it does not
claim zero total work when m=0.

A supplied temporal history compressed as a concat/Repeat grammar can
instead be annotated by its group product. Every repeat power reduces
modulo4, and a bottom-up annotation uses O(s) group operations on an
s-node grammar, plus exponent arithmetic. This is the ordinary finite-
monoid aggregation mechanism already used by the
[repeat transducer](RESULTS-p3-itinerary-repeat-transduction.md); no
second generic compiler is introduced here. Obtaining that temporal
grammar from the growing singleton query is an additional task.

The new concrete requirement for a repeated blocking scheme is thus
to construct the adjacent-history correlation in(8), or equivalent
signature data, at both actual half-block histories with shared cost.
Neither(4) nor(7) supplies that construction at sublinear cost.

The saved verifier passed256 group-action checks,512 associativity
checks,16 complete local inverse cases,36 directed history/entering-digit
controls, and16 shared-block controls. The last controls check the
stated operation counts as well as the outputs. The actual correlation
control and four independent shrinking-window checks reuse the existing
seven-digit ray certificate.

```
uv run --offline --no-project python experiments/rule30/p3_nilpotent_history_cocycle.py
```

# A compact nonlinear normal form for balanced defect commutators

Date: 2026-09-14. **A proved nonlinear rewrite reduces an exponentially
expanded balanced commutator to one explicitly controlled bit flip.** Its
depth parameter is stored in binary. The full guard can be tested using
`O(d)` supplied low bits, while its zero-input marked query takes
`O(log(d+2)+log(k+2))` bit work.

This is a positive simplification of a particular group-expression family.
It does not simplify the entire ordered norm for `B_0^N(0)` or give a new
bound for the Rule 30 singleton query. Conjugating the simplified gate by
`A^j` still carries an unevaluated orbit computation; section 4 identifies
that computation exactly.

## 1. An arbitrary-guard commutator identity

Use original binary coordinates, ordinary composition, and
`[g,h]=g h g^(-1) h^(-1)`. Let

```text
A(x)=x XOR((x<<1) OR(x<<2)),
y_i=x_i+(x_(i-1) OR x_(i-2)),     x_-1=x_-2=0.
```

For `p>=0`, let `f` be any Boolean function of the first `p` input bits,
and let `T=T_(p,f)` toggle bit `p` by `f`, fixing all other bits. It is
an involution, since its guard does not inspect the bit it changes.
Then

```text
[A T A^(-1),T] = T_(p+2,h),
h(y) = f(y) f(A^(-1)y) (1+(A^(-1)y)_(p-1)).               (1)
```

At `p=0` the last inverse bit is defined as zero. The new guard depends
only on bits below `p`; the arguments of each `f` mean its required
`p`-bit prefix.

**Proof.** Write `x=A^(-1)y`, `a=f(x)`, `b=f(y)`, and
`gamma=A T A^(-1)`. Applying `T` to `x` changes only `x_p`, by `a`.
Consequently `gamma` changes exactly the following possible output bits:

```text
coordinate       p               p+1                    p+2
change           a          a*(1+x_(p-1))          a*(1+x_(p+1)).
```

Applying `T` instead to `y` leaves inverse bits below `p` unchanged,
changes inverse bit `p` by `b`, and changes inverse bit `p+1` by
`b*(1+x_(p-1))`. Thus `a` remains unchanged. Conversely, `gamma` fixes
all bits below `p`, so applying `T` after `gamma` still uses exactly
`b=f(y)`. Comparing these two orders, every coordinate agrees except
possibly `p+2`, whose difference is
`a*b*(1+x_(p-1))`. This proves
`gamma T = T_(p+2,h) T gamma`. Multiplying on the right by
`gamma T`, and using the two involutions, gives (1). The calculation
also proves all untouched higher coordinates, not just a truncated action.

## 2. The balanced family and its complete normal form

Define

```text
E_0=tau_0,              tau_i(x)=x XOR2^i,
E_(d+1)=[A E_d A^(-1),E_d].                              (2)
```

Then

```text
E_0=tau_0,   E_1=tau_2.
```

For every `d>=2`, the complete map `E_d` toggles **only bit `2d`**, and
does so exactly when

```text
the first 2d-4 input bits are all zero,
and input bits 2d-4 and 2d-3 are equal.                    (3)
```

Every other input is fixed. In particular, bits `2d-2` and `2d-1` are
unrestricted, as is the bit being toggled and the entire higher tail.
There are exactly eight eligible prefixes of length `2d`: two choices
for the equal pair and four choices for the remaining two bits. This
count includes `d=2`, where the initial zero run is empty.

**Proof.** Formula (1) applied to `E_0` first gives `E_1=tau_2`.
Applied to `E_1`, it gives a bit-four flip with guard
`1+(A^(-1)y)_1=1+y_1+y_0`, proving (3) at `d=2`.

Suppose (3) holds at depth `d>=2`, put `p=2d`, and let `L=p-4`.
The two old guards in (1) require both the `y` prefix and its inverse
prefix to have `L` zeros followed by an equal pair. Once the first
`L` bits are zero, the next pair `a,b` in `y` becomes `a,a+b` under
`A^(-1)`. The requirements

```text
a=b   and   a=a+b
```

are equivalent to `a=b=0`. Therefore the product of the two old guards
is exactly the condition that the first `p-2` bits of `y` are zero.
Under this condition,

```text
(A^(-1)y)_(p-1)=y_(p-1)+y_(p-2).
```

The final factor in (1) imposes equality of that next pair. Its new
flip is at `p+2`, giving (3) for depth `d+1`. This proves the normal
form for every depth and every infinite binary input.

### Every initial lower-bit guard eventually has the same form

The normal form is not restricted to starting with `tau_0`. Start with
any controlled flip `T_0=T_(p,f)` as in section 1, and define

```text
T_(d+1)=[A T_d A^(-1),T_d],
P=p+2d,    d_0=max(2,floor(p/2)+1).
```

For every `d>=d_0`, the complete action is identity if `f(0)=0`.
If `f(0)=1`, it flips only bit `P`, with the canonical guard

```text
bits0,...,P-5 are zero,     bit_(P-4)=bit_(P-3).          (3a)
```

Thus every initial guard reduces to its single value at zero. There
are again exactly eight eligible prefixes of length `P` in the
nonidentity case. This is a theorem about the indicated balanced
iteration, rather than arbitrary products of such gates.

**Proof of the reduction.** Put `x_t=A^(-t)y`. Repeated application
of (1) shows that the guard after `d` steps is the Boolean product

```text
product_(t=0,...,d) f(x_t)
  times product_(ell=0,...,d-1) product_(t=1,...,d-ell)
          (1+x_t[p+2ell-1]).                            (3b)
```

Bits with index `-1` are zero. Products are Boolean conjunctions:
repeated factors collapse by idempotence, not by cancellation in a
sum. Formula (3b) follows by multiplying the guard at `y` and at
`A^(-1)y`, then adding the new last factor from (1).

For `p>=1`, an active guard therefore requires `x_t[p-1]=0` for
`1<=t<=d`. The following elementary consecutive-zero fact forces
the whole lower prefix to vanish: if bit `k>=0` is zero for
`ceil(k/2)+1` consecutive inverse iterates, their first `k+1` bits
are all zero. For `k=0`, this is immediate because `A` preserves
bit zero. For `k=1`, two zero samples and

```text
x_t[k]=x_(t+1)[k]+(x_(t+1)[k-1] OR x_(t+1)[k-2])
```

force the lower bit to be zero too. For `k>=2`, every pair of
consecutive zero samples forces both bits `k-1,k-2` to be zero
at the later sample. Apply induction to the `k-2` column, whose
required sample count is one smaller, then include the already-zero
bits `k-1,k`. A zero prefix is preserved by `A` and its inverse, so
the conclusion holds at every time in the orbit, including `y`.

Taking `k=p-1` proves that at `d>=floor(p/2)+1`, every active
guard lies in the invariant cylinder `2^p Z_2`. On this cylinder,
`A(2^p z)=2^p A(z)`. The initial flip is identity if `f(0)=0`
and otherwise the shifted `tau_0`. Every subsequent commutator
therefore restricts to identity or the shifted `E_d`, respectively.
Section 2 supplies its canonical form for `d>=2`. For `p=0`, the
initial guard is already constant and this last argument applies
directly. This proves (3a). When `p>=1` and `f(0)=0`, vanishing
already holds at `d>=floor(p/2)+1`, without the extra `d>=2`.

For `p>=3`, the stated convergence time is sharp in general.
Choose `f` constantly one and `1<=d<=floor(p/2)`, and take
`y=A^d(1)`. Then `x_t=A^(d-t)(1)` has highest nonzero bit
`2(d-t)` for `1<=t<=d`. Every coordinate required to vanish in
(3b) is at least `p-1>2d-2`; hence the actual guard is active.
But `y` is odd, and the canonical guard (3a) requires bit zero
to vanish. This proves failure before the threshold without an
enumeration of guards or group elements.

The cost of obtaining `f(0)` must be charged. After that evaluation,
a zero-input marked query is just the comparison `k=p+2d`.
The implemented `collapsed_zero_marked` makes exactly one call to
the supplied guard and otherwise uses
`O(log(p+2)+log(d+2)+log(k+2))` bit work. On an arbitrary supplied
input, testing (3a) reads `O(p+d)` low bits; producing the full
output still charges its size. This theorem does not supply a cheap
evaluation of an arbitrary encoded initial guard, or a collection
algorithm for the actual ordered norm.

## 3. The reduction is substantial, and its costs are explicit

If (2) is expanded literally using the primitive symbols
`A,A^(-1),tau_0`, its word length obeys

```text
L_0=1,   L_(d+1)=4L_d+4,
L_d=(7*4^d-4)/3.                                         (4)
```

A shared expression already avoids storing all these letters; the
normal form goes further by removing their recursive evaluation for
this family. It stores `d` and uses the one guard (3).

For a supplied input prefix, evaluating the guard needs at most
`2d-2` input bits and `O(d)` Boolean work. Index arithmetic is charged
separately. Producing a complete output integer also charges its length;
in particular creating the bit `2d` from zero takes linear output space.
The normal form is not a constant-cost operation on an arbitrarily long
unread input.

On zero input, however, the guard is always true and

```text
E_d(0)=2^(2d),      bit_k(E_d(0))=1[k=2d].                 (5)
```

The implemented `zero_marked(d,k)` compares binary integers and costs
`O(log(d+2)+log(k+2))` bit work. It constructs neither `2^(2d)` nor an
enormous mask. The large-index control uses `d=10^1000` and checks the
three positions `2d-1,2d,2d+1` with those costs.

This explicit nonlinear gate family is consistent with the earlier
[faithful-matrix obstruction](RESULTS-p3-defect-derived-series.md).
That theorem concerns faithful representations of entire defect groups;
it does not forbid compact evaluation of particular group elements.

## 4. Exact connection to the ordered norm and the singleton query

Put `alpha_j=A^j tau_0 A^(-j)`. The ordered norm in the
[existing factorization](RESULTS-p3-conjugated-defects.md) is

```text
B_0^N=(alpha_0 alpha_1 ... alpha_(N-1)) A^N.
```

Equation (1) at `p=0,f=1` gives
`[A tau_0 A^(-1),tau_0]=tau_2`. Conjugating by `A^j` proves

```text
[alpha_(j+1),alpha_j]=A^j tau_2 A^(-j).                   (6)
```

Thus swapping two neighboring levels in the ordered norm introduces
exactly one conjugated bit-two flip. This is an explicit residual, not
permission to discard it or to commute it through other levels freely.

More generally, define balanced neighboring residuals

```text
D_(0,j)=alpha_j,
D_(d+1,j)=[D_(d,j+1),D_(d,j)].
```

Conjugation of (2) gives `D_(d,j)=A^j E_d A^(-j)`.
Since `A(4x)=4A(x)`, also `A^(-1)(4x)=4A^(-1)(x)`.
The cylinder of inputs divisible by `4^d` is invariant under both.
On that cylinder, (3) is satisfied and `E_d` acts as the shift of
`tau_0` by `2d` bits. Therefore the complete guarded identity is

```text
D_(d,j)(4^d x)=4^d alpha_j(x),             d,j>=0.         (7)
```

In particular, with the actual singleton row `A^j(1)`,

```text
D_(d,j)(0)=4^d A^j(1),
bit_(j+2d)(D_(d,j)(0))=c_j.                              (8)
```

Equations (7)-(8) preserve the actual zero input and full group action;
they use no fresh completion or arbitrary reconstructed ancestry.
They also show the remaining cost: the rewrite has **not decreased
`j`**. At zero, straightforward evaluation computes the singleton row
for `j` steps; on an arbitrary supplied prefix, direct conjugated
evaluation needs the inverse and forward `A^j` passes. Their scalar
cost is `O(jw)` for a supplied width-`w` prefix, plus the gate and
index costs. No cheap conjugator is assumed.

The balanced words in (2) and (8) are not asserted to appear without
cancellation in the particular norm for `B_0^N(0)`. The missing positive
step is a collection rule for that norm which both exposes usable
controlled gates and bounds their conjugator and observer costs. The
present family supplies a real nonlinear simplification, not that
complete collection algorithm or a P3 lower bound.

## 5. Adjacent cancellation does not permit arbitrary collection

For `d>=3`, every `A`-conjugate of `E_d` fixes every odd input: `A`
and its inverse preserve the lowest bit, while guard (3) requires it
to be zero. This useful cylinder simplification has a precise limit.

Put `F_i=A^i E_2 A^(-i)`. The adjacent commutators

```text
[F_(i+1),F_i]=A^i E_3 A^(-i)
```

all fix odd inputs. Nevertheless, on the saved actual singleton row
`y=A^8(1)=102849`, the nonadjacent commutator gives

```text
[F_3,F_1](y)=102465,
y XOR [F_3,F_1](y)=2^7+2^8.                              (9)
```

In particular it changes the actual time-eight center readout, bit
eight, from one to zero. The order in (9) is the ordinary composition
convention of section 1. This refutes extending adjacent cancellation
to arbitrary pairs even on this actual odd singleton input. It does
not assert that this commutator occurs uncancelled in the ordered norm.

Equation (9) is a complete-output control. `E_2` fixes all bits from
five onward. A changed input bit can propagate upward by at most two
positions per application of `A`; hence `F_i` fixes all bits from
`5+2i` onward. The commutator in (9) therefore fixes every bit from
eleven onward. Its exact eleven-bit action, computed by unreduced
forward and inverse Mealy words and reattached to the unchanged high
tail, proves the displayed full value. A twenty-bit replay checks the
seam independently. The initial row is read from the existing
[dyadic-section artifact](../../experiments/rule30/p3-dyadic-sections.json),
not regenerated by a new trajectory run.

## 6. An exact collection inside the actual ordered norm

The preceding witness concerns a particular commutator. The following
control instead retains an exact decomposition of the actual ordered
norm and tests a precisely identified omission.

For arbitrary invertible maps, ordinary composition gives

```text
L a b R = (L[a,b]L^(-1)) L b a R.                       (10)
```

Apply (10) to the stable even/odd shuffle of
`P_8=alpha_0 alpha_1 ... alpha_7`. With

```text
W=alpha_0 alpha_2 alpha_4 alpha_6 alpha_1 alpha_3 alpha_5 alpha_7,
P_8=C_1 C_2 C_3 C_4 C_5 C_6 W,
C_s=L_s [alpha_i,alpha_j] L_s^(-1),                     (11)
```

the exact six corrections are listed below. A prefix such as `0,2,1`
means the ordinary product `alpha_0 alpha_2 alpha_1`.

| Correction | Prefix `L_s` | Pair `(i,j)` | Output if only this correction is omitted | Time-13 readout | Time-14 readout |
|---|---|---|---:|---:|---:|
| none omitted | — | — | 25712 | 1 | 0 |
| `C_1` | `0` | `(1,2)` | 25716 | 1 | 0 |
| `C_2` | `0,2,1` | `(3,4)` | 25628 | 1 | 0 |
| `C_3` | `0,2` | `(1,4)` | 25676 | 1 | 0 |
| `C_4` | `0,2,4,1,3` | `(5,6)` | 25668 | 0 | 0 |
| `C_5` | `0,2,4,1` | `(3,6)` | 26540 | 1 | 1 |
| `C_6` | `0,2,4` | `(1,6)` | 28428 | 1 | 1 |

Every row evaluates on the same original zero input. In an omission
row, all other corrections retain their exact order in (11). The
true output is `P_8(0)=B_0^8(0)=25712`, since `A^8(0)=0`.
The altered outputs are not asserted to be other singleton trajectories.

For original binary coordinates put `H(x)=A(x)>>2`. By the
[proved actual B-query formula](RESULTS-p3-actual-b-query.md), the
readouts in this table are precisely

```text
time13: bit_1 H^5(x),       time14: bit_0 H^6(x).         (12)
```

Thus discarding just `C_5` or `C_6` changes the required time-fourteen
answer. The adjacent correction `C_4` also matters, changing the
time-thirteen answer. All these statements concern this specified
collection and observation, rather than every possible collection
algorithm. Each `alpha_i` fixes all bits from `2i+1` onward, so the
complete actions in this table fix every bit from fifteen onward.
Fifteen-bit evaluation plus the untouched high tail is exact; the
verifier also checks a wider prefix.

There is a positive distinction here: the discrepancy from omitting
`C_3` disappears completely before either observation. Starting from
the true and altered values `25712,25676`, their differences under
successive `H` updates are

```text
60, 25, 15, 12, 1, 0.
```

After five updates both complete integers are `28519`. Subsequent
equality follows from determinism. The complete local difference law
explains a valid erasure mechanism. If `y=x XOR delta`, then

```text
(Hx XOR Hy)_i = delta_(i+2)
                +(1+x_i)delta_(i+1)
                +(1+x_(i+1))delta_i
                +delta_i delta_(i+1).                  (13)
```

In particular, if `x,y` agree above position `j` and their common
bit `j+1` is one, their next images agree at every position at least
`j`. This follows by substituting the zero higher differences in
(13), and is valid for all input lengths and tails. Iterating it
requires the actual intervening common bits; those bits are not free
data. The `C_3` computation retains the entire paired history and
proves this particular erasure. It does not license the omissions
whose marked outputs differ in the table.

This particular erasure also holds for every common higher tail:

```text
H^5(25712+2^16 z)=H^5(25676+2^16 z),    z in Z_2.        (14)
```

Initially the pair agrees at every bit from six onward, and this
agreement persists because `H` uses only the current bit and the
next two higher bits. Its low six bits after five steps depend only
on the original low sixteen bits. Those outputs were already
checked equal, so the entire output agrees for every `z`.
Since all factors in (11) fix bits from fifteen onward, (14)
also proves equality after `H^5` of the original and omitted-`C_3`
norm actions on the cylinder of inputs divisible by `2^16`.
The other omissions in the table retain their stated failures.

The [collection helper](../../experiments/rule30/p3_dyadic_norm_collection.py)
retains the individual swap identities, omission controls, and all
64 local assignments in (13). The balanced-family verifier implements
the collection independently. There is no claimed compression of
the general correction sequence: a stable parity shuffle of `2m`
distinct ordered levels takes `m(m-1)/2` adjacent swaps by this direct
construction, with their action and observer costs still to be paid.

## 7. Exact verifier

The [source](../../experiments/rule30/p3_balanced_defect_normal_form.py) and
[artifact](../../experiments/rule30/p3-balanced-defect-normal-form.json) retain:

- all Boolean guards on zero, one, and two lower bits, with every input
  in their required local cones: 592 exact instances of (1);
- the complete four-pair seam used by the all-depth induction;
- the arbitrary-initial-guard convergence theorem, with selected
  guards at positions zero through six checked by both the exact
  recurrence and its expanded zero constraints, plus independently
  evaluated unreduced words and directed sharpness controls;
- directed unreduced-word checks through depth four, in both inverse
  orientations, including eligible and failing guards, both values of
  the target bit, and nonzero untouched high bits;
- the eight eligible prefixes at every retained depth, without a
  finite-group closure computation;
- adjacent-norm and zero-cylinder checks using independent raw Mealy
  forward/inverse actions;
- the complete nonadjacent commutator action on the saved actual
  time-eight row, including its changed center bit;
- an independent exact six-swap collection of `P_8`, every single
  correction omission, and the two actual marked observations;
- the large binary-index marked control and source/report hashes.

The recursive oracle does not assume `E_d` is an involution; it evaluates
inverse words explicitly. The all-length claims follow from (1) and the
guard induction, while these finite checks validate the implementation.
No old Rule 30 census, growing group enumeration, center-prefix
generation, GPU work, or paid computation is performed.

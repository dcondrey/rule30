# Exact closure and shared evaluation of parallel defect pairs

Date: 2026-09-14. **A balanced commutator of two parallel controlled bit flips
is again a parallel pair, shifted two positions.** The complete guard
recurrence is explicit. For any supplied input, all repeated guard calls
share a single inverse orbit, giving a triangular evaluator instead of an
exponential recursive call tree. On zero input its two coefficients have
a closed formula, permitting a logarithmic binary-index marked query.

These are exact simplifications of the specified group-expression family.
They do not assert that the complete ordered Rule 30 norm belongs to it,
or give a new P3 query-work bound.

## 1. The all-length pair identity

Work in original binary coordinates with ordinary composition,
`[g,h]=g h g^(-1) h^(-1)`, and

```text
A(x)=x XOR((x<<1) OR(x<<2)).
```

For `p>=0`, let the two Boolean functions `f,g` inspect only bits below
`p`. Define the parallel involution `G` by

```text
G(y)=y XOR(f(y)<<p) XOR(g(y)<<(p+1)).
```

Its two guards are evaluated on the same input prefix. Neither guard
inspects either bit being flipped. For the current input `y`, put

```text
x=A^(-1)y,       r=1+x_(p-1),     x_-1=0,
(a,b)=(f(x),g(x)),     (u,v)=(f(y),g(y)),
D=v+u*r,
H=b*u+a*D,
J=b*(D*(1+x_p+u+a)+u*x_(p+1)).                         (1)
```

Every addition and multiplication in the coefficients is in `F_2`.
Then the complete commutator is

```text
[A G A^(-1),G](y)=y XOR(H<<(p+2)) XOR(J<<(p+3)).        (2)
```

`H` depends only on input bits below `p`; `J` depends only on bits
below `p+2`. Therefore (2) is again a parallel involution, now at
position `p+2`. This proves closure for all lengths and all tails.
There is no dependence on either new target bit.

**Proof.** Set `gamma=A G A^(-1)`. In terms of `x=A^(-1)y`, its
possible changes at output positions `p,p+1,p+2,p+3` are respectively

```text
a,
b+a*r,
b*(1+x_p)+a*(1+x_(p+1))+a*b,
b*(1+x_(p+2)).
```

All higher bits are unchanged. Applying `G` to `y` instead changes
the corresponding inverse coordinates at `p,p+1,p+2` by

```text
u,    D,    F=D*(1+x_p)+u*(1+x_(p+1))+u*D.
```

Every lower guard remains fixed throughout these operations. Comparing
`gamma G` with `G gamma`, their first two possible changes cancel;
the remaining differences are `H` at `p+2` and `b*F` at `p+3`.
To express this correction as a map of the output of `G gamma`,
substitute the inverse-coordinate changes

```text
x_p -> x_p+u+a,    x_(p+1) -> x_(p+1)+D+b.
```

The expression `b*F` simplifies to `J` in (1). Thus
`gamma G = K G gamma`, where `K` is the right side of (2).
Multiplying on the right by `gamma G` proves the commutator identity.
This computation includes the entire unchanged higher tail.

If the second guard is identically zero, (1) becomes the earlier
[single-flip identity](RESULTS-p3-balanced-defect-normal-form.md):
`H=f(y)f(A^(-1)y)(1+x_(p-1))`, `J=0`.

## 2. Exact shared evaluation through any number of commutators

Starting with this `G_0`, define

```text
G_(d+1)=[A G_d A^(-1),G_d].
```

The target pair at depth `d` starts at `p+2d`. To compute its guard
on a supplied input `y`, only the first `w=p+2d` input bits are needed.
Construct the one actual inverse orbit

```text
x_t=A^(-t)y modulo2^w,     0<=t<=d.
```

Evaluate the original pair `(f(x_t),g(x_t))` once at each point.
Then fill a triangular table: the guard at `(ell+1,t)` is given by
(1) from the entries at `(ell,t)` and `(ell,t+1)`, using the actual
bits of `x_(t+1)` at positions `p+2ell-1,p+2ell,p+2ell+1`.
At the zero boundary, the negative bit is zero.

Induction in `ell` proves that every table entry is exactly the guard
of `G_ell` at `A^(-t)y`. Compatibility of `A^(-1)` with prefixes
justifies the common precision. No inverse orbit is restarted with a
fresh boundary or a guessed completion.

The construction uses exactly:

- `d+1` evaluations of the supplied initial guard pair;
- `d` inverse-prefix passes, each of `p+2d` bits;
- `d(d+1)/2` constant-size pair updates.

For `d>=1`, explicit bit arrays use `O(d*(p+d))` bit operations, plus
the initial-guard evaluation costs, input/index access, and requested
output construction. Storing the inverse orbit costs
`O((d+1)*(p+2d+1))` bits; two rolling guard rows suffice. Depth zero
directly evaluates the supplied initial gate. The Python
verifier uses big integers, so their shifting/allocation costs are
charged separately from its exact scalar-operation counters. A
conservative direct implementation bound for those scans is
`O(d*(p+2d)^2)` bit work, plus the other stated costs.

This is polynomial in the **value** of `d`, not its binary encoding
length. A literal signed word has `4^d` copies of its initial gate;
the triangular method eliminates that evaluation tree. It does not
establish uniformly small full guard circuits or an efficient
collection of the separate ordered norm.

## 3. Zero input has an exact marked-query shortcut

Let `(a_0,b_0)=(f(0),g(0))`. Substituting `x=y=0` in (1) gives
the zero-guard update

```text
(a,b) -> (a,b*(1+a)).                                  (3)
```

This update is idempotent. Thus for every `d>=1`,

```text
G_d(0)=a_0*2^(p+2d)+b_0*(1+a_0)*2^(p+2d+1).           (4)
```

At `d=0` use the original pair. The implemented `zero_marked`
makes one paid call to the initial guard at zero, then answers by
binary-index comparisons in
`O(log(p+2)+log(d+2)+log(k+2))` additional bit work. It constructs
neither the output integer nor a mask of its implied length.
The supplied guard may itself be expensive; that evaluation is not
made free by (4).

Formula (4) concerns zero input only. It does not imply that the
second gate vanishes from the complete action.

## 4. Directed controls for an initial XOR-three gate

Take `p=0` and `(f,g)=(1,1)`, so `G_0(x)=x XOR3`.
Its first commutator flips bit two unconditionally and flips bit
three precisely when `y_0+y_1=1`. Both follow directly from (1).
The independently evaluated signed words also give

| Depth | Input | Guard pair | Complete output |
|---:|---:|---|---:|
| 3 | 14 | `(0,1)` | 142 |
| 3 | 50 | `(0,1)` | 178 |
| 4 | 50 | `(0,1)` | 562 |
| 5 | 222 | `(0,0)` | 222 |

These are small exact controls, not a general convergence or
nonconvergence assertion. They show why the single-flip normal form
cannot simply be applied at depth three or four to this pair.
They also falsify the particular proposed propagation
`guard_d(A^(d-3)(14))=(0,1)` for all `d>=3`:
`A(14)=50`, `A(50)=222`, and the last row fails it at depth five.
No general guard-collapse law is inferred from this failure.

The parallel-pair closure also cannot be extended unchanged to a
three-bit band. For the named initial gate `G(x)=x XOR5`, put
`K=[A G A^(-1),G]`. Exact evaluation gives

```text
K(0)=28,     K(28)=16,     K^2(0)=16 !=0.
```

Thus `K` is not an involution. Every parallel-controlled band whose
guards avoid all its changed bits is an involution, so `K` cannot
belong to that class. The initial gate changes only bits zero and
two; its conjugate can change only bits zero through four. Their
commutator therefore fixes every bit from five onward. The complete
five-bit action proves the displayed full outputs, and the verifier
also replays twelve bits. This is a counterexample to that particular
extension; a larger class with internally dependent guards is open.

## 5. Verification and remaining task

The [source](../../experiments/rule30/p3_parallel_defect_pair.py) and
[artifact](../../experiments/rule30/p3-parallel-defect-pair.json) contain
the complete 1,024-case local coefficient certificate, directed raw
forward/inverse word controls, exact sharing counters, the displayed
XOR-three controls, the complete three-bit-band counterexample, all four
zero-guard cases, and a marked query with
thousand-digit indices. The raw word evaluator does not assume that
intermediate commutators are involutions. The proof above supplies
the all-length conclusions; the finite controls validate their code.

The remaining obstacle to applying this construction to P3 is concrete:
the actual ordered norm contains conjugated and nonadjacent correction
factors. No proved collection keeps all those factors in this one
parallel-pair family while also bounding their action contexts and
marked readouts. The closure and shared evaluator establish neither
that collection nor a sublinear singleton algorithm.

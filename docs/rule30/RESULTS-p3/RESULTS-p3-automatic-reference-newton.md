# A finite-cone automatic reference can have a nonautomatic Newton solution

Date: 2026-09-14. **The general automatic-reference closure claim is false.**
There is an explicit jointly 2-automatic reference with the correct singleton
initial row and support inside `0 <= j <= 2t` whose unique triangular linear
Newton solution is not jointly 2-automatic. Both the reference and its solution
retain that finite light cone. The reference has an explicit algebraic bivariate
series; the solution's bivariate series is not algebraic.

This is an all-length counterexample to a proposed general compiler. It does
not settle automaticity of the particular first Newton reference
`a_t=(1+X+X^2)^t`, its next Newton iterate, or any singleton query complexity.
The construction below is a prescribed reference, not a claimed actual Rule 30
trajectory or a member of the successive Newton orbit.

## 1. The finite-cone reference and the exact linear solve

Use the moving coordinates of the
[prefix Newton report](RESULTS-p3-prefix-newton-tail.md). All arithmetic is over
F_2, negative spatial indices are zero, and L=1+X+X^2. The Newton solve at a
reference a is

```
v_0=1,
v_(t+1,j)=v_(t,j)+(1+a_(t,j-2))*v_(t,j-1)
         +(1+a_(t,j-1))*v_(t,j-2)+a_(t,j-1)*a_(t,j-2).       (1)
```

This is the exact Boolean linearization of
`r'_j=r_j+(r_(j-1) OR r_(j-2))`, including its forcing term. Define

```
s_t=0  if t is a positive power of 2,
    1  otherwise,
a_t(X)=s_t*(1+X+...+X^(2t)).                                (2)
```

In particular s_0=1 and a_0=1. The predicate that t is a positive power of 2
has binary language `10*`; the relation `j <= 2t` is recognized by fixed binary
shift and comparison automata. Boolean combinations therefore give a finite
automaton for every coefficient of (2), reading padded pairs of binary digits.
No finite prefix is fitted to obtain this reference.

It also has an explicit algebraic description. Let
`Theta(Z)=sum_(r>=0) Z^(2^r)`, so `Theta(Z)^2+Theta(Z)=Z`. Then

```
A(T,X)=sum_t a_t(X) T^t
 = ([1/(1+T)+Theta(T)]
    +X*[1/(1+T X^2)+Theta(T X^2)])/(1+X).                   (3)
```

All denominators have constant term 1. Formula (3) follows by summing the
finite interval in each row, then removing the positive-power-of-two times.
Thus its use of an automatic environment is explicit at both the digit and
algebraic levels.

## 2. The Newton row update reduces to two exact operations

Write `B_K=X+X^2+...+X^K`. For every t, the solution of (1)-(2) has constant
coefficient 1, degree exactly 2t, and highest coefficient 1. Its update is

```
v_(t+1)=L*v_t            if s_t=0,
v_(t+1)=v_t+B_(2t+2)     if s_t=1.                         (4)
```

**Proof.** With a_t=0, (1) is multiplication by L. With a_t equal to the full
interval through 2t, the output at j=0 is unchanged; at j=1 it adds v_(t,0)=1;
at each 2<=j<=2t it adds 1 because both derivative coefficients vanish.
The two new high outputs at 2t+1 and 2t+2 are both 1: the first is the forcing
term and the second is the former highest coefficient. Entries beyond 2t+2
remain zero. This proves the second line of (4). The t=0 case is directly
`1 -> L` and satisfies the same formula. Both operations preserve the claimed
extreme coefficients and increase the degree by exactly 2, completing induction.

The high boundary is retained in (4). Replacing B_(2t+2) by an infinite tail
would be a different reference and is not used in the theorem.

## 3. Exact blocks between consecutive powers of 2

For m>=1 put

```
w_m=v_(2^m+1),       F_m=(1+X^2)*w_m+L.                     (5)
```

The initial block is `w_1=L^3`, hence `F_1=X^6 L`. Between times `2^m+1` and
`2^(m+1)-1` there are `2^m-1` successive additions in (4), an odd number.
The next step, at time `2^(m+1)`, multiplies by L. Consequently

```
F_(m+1)=L*F_m+E_m,
E_m=L*(1+X)*sum_(tau=2^m+1..2^(m+1)-1) X^(2tau+3).         (6)
```

To derive the cancellation, temporarily write `B=X/(1+X)` as a formal series.
For each finite K,

```
B_K=B+X^(K+1)/(1+X),       (1+X^2)*B=L+1.
```

The odd number of additions leaves one B term; its contribution cancels the
constant L added in (5). The remaining terms are precisely the finite
polynomial E_m in (6). Thus the infinite B is only an algebraic aid for an
identity of finite polynomials, not a replacement boundary.

The first term of E_m has exponent `2^(m+1)+5`, with coefficient 1. Therefore

```
ord_X(E_m)=2^(m+1)+5,
F_(m+1)=L F_m mod X^(2^(m+1)+5),
ord_X(F_m)=6  for every m>=1.                               (7)
```

The last assertion follows from F_1=X^6 L, the constant coefficient of L,
and the strictly higher valuations of all errors.

## 4. A finite automaton would impose one common exponent period

We use the following elementary consequence of a finite digit automaton.

**Lemma.** If a binary array f(t,j) is jointly 2-automatic, there is an integer
P>=1 such that, for every fixed cutoff K, there is m_0(K) satisfying

```
f(2^(m+P)+1,j)=f(2^m+1,j)
for all m>=m_0(K) and all 0<=j<K.                           (8)
```

The period P is independent of K. Only the starting threshold may depend on K.

**Proof.** Use a most-significant-digit finite automaton and choose a fixed
spatial digit length ell with K<=2^ell. For m>ell, each padded input pair
`(2^m+1,j)` first reads `(1,0)`, then `(0,0)` repeated `m-ell` times, then an
ell-symbol suffix encoding the remaining time and spatial digits. For each j
this suffix is fixed as m varies. Iterating the single transition `(0,0)` on
a finite state set is eventually periodic, with one period P for the state
reached after `(1,0)`. The same P works for every suffix and every ell. This
proves (8).

Suppose now that the Newton solution v in (1)-(2) were jointly 2-automatic.
The array

```
f(t,j)=v(t,j)+v(t,j-2)+[X^j]L
```

would also be automatic: bounded index shifts are recognized by finite carry
machines, and XOR uses a product automaton. Its row at `t=2^m+1` is F_m.
The lemma would give a single P with

```
F_(m+P)=F_m mod X^K                                      (9)
```

for all sufficiently large m, separately for each fixed K.

But for sufficiently large m, all P error terms from (6) have valuation at
least K. Thus the same rows satisfy

```
F_(m+P)=L^P F_m mod X^K.                                  (10)
```

For every P>=1, L^P+1 is nonzero and

```
ord_X(L^P+1)=2^v2(P).                                    (11)
```

Indeed write P=2^r q with q odd. The first nonconstant term of
`(1+X+X^2)^q` is X; applying Frobenius r times makes its exponent 2^r.
By (7), the difference `(L^P+1)F_m` therefore has valuation exactly
`6+2^v2(P)`. Choose `K=7+2^v2(P)`. Equations (9)-(10) demand that this
nonzero coefficient vanish, a contradiction. The solution is not jointly
2-automatic.

This is not an inference from growing numerical state counts or from a
finite failure of fitted sections. It excludes every finite automaton by the
same transition-period argument.

## 5. Algebraic scope and the particular first reference

Over a finite field, the multivariate Christol theorem equates algebraicity
with a finite joint section orbit, hence automatic coefficients. An effective
primary proof states this as Theorem B and Remark 1.1 in
[Adamczewski, Bostan and Caruso, *A sharper multivariate Christol's theorem*](https://adamczewski.perso.math.cnrs.fr/Effective_Christol.pdf).
Therefore the full series `sum_(t,j) v(t,j) T^t X^j` just constructed is not
algebraic over F_2(T,X), although its reference series (3) is algebraic.

Closure of algebraic series under a supplied Hadamard product does not imply
closure under the triangular Newton inverse. Likewise, fixed-rule linear-CA
results have stronger hypotheses: for example the rational-series argument in
[Rowland and Yassawi, Theorem 3.1](https://arxiv.org/pdf/1209.6008)
uses fixed Laurent-polynomial rule coefficients. The Newton operator here has
coefficients varying in both space and time.

The actual first reference `a_t=L^t` is more specific: its spacetime series is
rational, `1/(1+TL)`, and it has explicit Frobenius sections. This report does
not prove or disprove closure for that reference, for successive actual Newton
iterates, or for another restricted rational-reference class. It proves that
automaticity or algebraicity of a finite-cone reference alone is insufficient.
Nor does nonautomaticity supply a lower bound against other coefficient-query
algorithms, compressed expressions, or P3 algorithms.

## 6. Bounded exact controls

The [verifier](../../experiments/rule30/p3_automatic_reference_newton.py) and
[artifact](../../experiments/rule30/p3-automatic-reference-newton.json) check:

- All 64 local reference/current triples against literal truth-table differences.
- Both row kernels on 43 complete small rows with the proved extreme bits.
- A new linear-reference diagram through time 17, using 629 scalar Newton cells.
- Four dyadic rows, three complete error polynomials in (6), and directed
  characteristic-two valuation identities.

These are controls of the all-length derivation, not its replacement. No
additional actual Rule 30 trajectory, center-prefix schedule, or automatic-state
census is generated. The artifact records the exact source and report hashes.

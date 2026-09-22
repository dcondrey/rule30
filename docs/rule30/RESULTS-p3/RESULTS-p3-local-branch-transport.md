# Local cancellation of the first-return prefix observable

Date: 2026-09-14. **All four first-return powers of C squared on zero
have exact expressions using powers of B and local output operations.**
The inverse Gamma prefix recurrence cancels against an inverse generator;
alternatively, one further B action absorbs it. This supplies actual
query reductions, while preserving the changed exponent and requested
digits. It does not prove fast powering of B or a sublinear singleton
algorithm.

The [verifier](../../experiments/rule30/p3_local_branch_transport.py) and
[artifact](../../experiments/rule30/p3-local-branch-transport.json) save
complete local identities and an independent finite-state equality
certificate. There is no original-frontier census or long center scan.

## 1. A local expression for the conjugated binary shift

Use the [itinerary convention](RESULTS-p3-itinerary-conjugacy.md), and
write sigma for deletion of the first base-four digit. Define

```
J(z)_j = high(z_j)
         +2*(low(z_(j+1)) XOR 1[z_j!=0]).          (1)
```

**Theorem.** If D is deletion of the first original binary bit, then
`J=Phi composed with D composed with Phi inverse` on all 2-adic inputs.

Indeed, H commutes with D. If `z_j=H^j(x) mod4`, the first bit of
`H^j(Dx)` is `high(z_j)`. Its second bit is the bit at position2 of
`H^j(x)`, which the H equation gives as
`low(z_(j+1)) XOR(low(z_j) OR high(z_j))`. This is (1).

One digit of J needs the supplied current digit and only the low bit of
the next digit. A complete m-digit output uses at most2m+1 input bits
and linear bit-array work. Obtaining those input bits is a separate cost.

The square must not be confused with sigma. In original coordinates
`D^2 g_0=H` for each generator g in A,B,C, so

```
J^2 composed with g = sigma,
J^2 = sigma composed with g^(-1).                 (2)
```

There is also a direct local check: `J^2(z)_j` is the inverse-generator
digit computed from `z_j,z_(j+1)`. The inverse's initial-state choice is
discarded by sigma, so all three generators give the same expression.
For example `J^2(1)=3` whereas `sigma(1)=0`; (2) retains the inverse
action and is not an uncharged jump.

## 2. The Gamma inverse cancels locally

The [return-class embedding](RESULTS-p3-itinerary-return-classes.md)
satisfies `Gamma CA=B^2 Gamma`, with Gamma a bijection onto the even
component and `Gamma(0)=0`. Let `z=Gamma(y)` and write
`p_j=low(z_j), q_j=high(z_j)`. Its inverse is

```
a_(-1)=0,
a_j=low(y_j)=q_j XOR(a_(j-1) OR p_j),
high(y_j)=p_(j+1).                                (3)
```

Applying A inverse to y cancels the repeated term in (3). Its output
low bit is `a_j XOR(a_(j-1) OR p_j)=q_j`; its high bit is
`p_(j+1) XOR(p_j OR q_j)`. Therefore, on every even z,

```
A^(-1) Gamma^(-1)(z)=J(z).                       (4)
```

More generally `g^(-1) Gamma^(-1)(z)` equals J(z) at every digit j>=1.
At digit0 apply the following root correction to `J(z)_0`:

| g | Root correction |
|---|---|
| A | d |
| B | 3-d |
| C | d-1 modulo4 |

This follows because all inverse generators use the same local rule
after the first digit; only their initial permutation differs. The
virtual initial state is retained, rather than silently resetting it.

There is a second, useful identity on the same even domain:

```
Gamma^(-1)=J B.                                  (5)
```

For an all-length proof, the original-coordinate definition is
`Gamma=Phi L Phi^(-1)`, with `L(x)=2*A_0^(-1)(x)`. On an even input2u,
the original binary section of B gives `D B_0(2u)=A_0(u)=L^(-1)(2u)`.
Conjugating proves (5). A separate finite Mealy certificate checks
`J B Gamma=identity` on every input digit and every reachable state.
Since Gamma maps onto the even component, that certificate also proves
(5) without requiring an itinerary conversion algorithm.

Equation (5) trades a prefix observable at z for a local observable
after one additional B action. That action is useful when z is already
a known B power; its computation is still charged.

## 3. All four zero-input first returns become B queries

The first returns of C squared are CA, CB, BC, and AC. Combining
(4)-(5) with the previously proved guarded reductions gives, for all
k>=0,

| Return power on zero | Exact output ray |
|---|---|
| `(CA)^k(0)` | `J(B^(2k+1)(0))` |
| `(CB)^k(0)` | `4*J(B^(2k+1)(0))` |
| `(BC)^k(0)` | `B^(2k)(0)` |
| `(AC)^k(0)` | `J(B^(2k)(0))` |

For CA use `Gamma((CA)^k(0))=B^(2k)(0)` and (5). For AC use
`(AC)^k(0)=A^(-1)((CA)^k(0))` and (4). CB contributes its exact
leading zero digit, and BC uses its invariant even-input identity with
`B^(2k)`. Every line includes k=0.

In particular a low digit-bit of a J output is one high digit-bit of
the indicated B orbit. A high digit-bit is the next low digit-bit XOR
the OR of the two current digit-bits. Thus no line requires reconstructing
Gamma's entire inverse prefix. The B exponent has become2k or2k+1,
and the high-bit case still requests adjacent information. The theorem
does not close the return families generated recursively by B.

## 4. A guarded conjugacy preserving the exponent

There is also a useful all-input class behind the actual zero-orbit
relation. Let X contain exactly the itinerary inputs with first digit0
or3. Then X is invariant under C, and

```
J C^L(x)=B^L J(x),  for x in X and every L>=0.    (6)
```

The original binary C sections give `D C_0(x)=B_0 D(x)` on even x.
For odd x whose next bit is1 the identity also holds: its tail is odd,
and B_0 and C_0 agree there. This covers original root digits0 and3;
Phi preserves those root digits. C interchanges the two cylinders, so
the identity iterates without losing its guard.

J restricted to X is bijective onto all itinerary inputs. Given z,
recover the bits `a_j=low(x_j), b_j=high(x_j)` by

```
b_j=low(z_j),
a_0=b_0,
a_(j+1)=high(z_j) XOR(a_j OR b_j).                (7)
```

The initial equality puts x in X, and (1) proves both reconstruction
and uniqueness. Its inverse is explicit but contains a prefix recurrence;
(6) alone does not make all inverse observables local.

The guard is substantive: at input1, `JC(1)=(1)^infinity` but
`BJ(1)=(3)^infinity`. Indeed `C(1)=2(3)^infinity`, which J sends to the
constant1 ray, whereas `J(1)=2` and `B(2)=(3)^infinity`. The direct
relation on zero follows from (6), since zero belongs to X. Further
[actual singleton readouts](RESULTS-p3-actual-b-query.md) using the
following B exponent are derived separately; the present result supplies
their local transport identities.

## 5. Verification and remaining cost

The artifact checks16 local cancellation cases, all16 adjacent-digit
square identities, all initial root corrections, and the complete
`J B Gamma` finite-state certificate. Directed controls separately
compare the conjugated shift with Phi, verify32 guarded powers, and
check all four return formulas at five exponents through5 with an
independent arithmetic word engine. These are implementation controls;
the all-length proofs are the local equations, binary sections, and
closed finite-state identity.

The result removes a particular prefix reconstruction cost by changing
the query to a specified B power. Constructing that B power, obtaining
its digits, and combining dependent requests remain part of the algorithm.
No fixed small recursive B family, iterate jump, or sublinear center
algorithm is asserted.

```
uv run --offline --no-project python experiments/rule30/p3_local_branch_transport.py
```

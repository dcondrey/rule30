# The invertible local multiplicative transport is necessarily trivial

Date: 2026-09-14. **A specified local matrix-product route to block
evolution has no nontrivial invertible solution, in any dimension or
group.** The proof is five symbolic cancellations. All local tile types
needed by the proof occur on the actual B zero orbit, so restricting the
local equations to those visited tiles does not evade the result.

This is a restricted obstruction, not a complexity theorem for Rule30.
It leaves noninvertible representations, larger blocks, position-dependent
encodings, and other algorithms open. The investigation continues toward
the exact [B-power digit query](RESULTS-p3-actual-b-query.md).

## 1. The proposed block-transport mechanism

For each input digit d assign a group element M_d, and for each entering
state g in A,B,C assign a group element L_g. An input digit emits
e=P_g(d), and the next state is psi(e), with

```
P_A=(0,3,2,1), P_B=(1,2,3,0), P_C=(3,2,1,0),
psi=(A,B,C,C).
```

The precise proposed local identity is

```
L_g M_d = M_e L_psi(e).                           (1)
```

It would transport the entering state through a digit product. Repeating
(1) across a word d0...d_(m-1), with output e0...e_(m-1), gives

```
L_g M_d0 ... M_d(m-1)
  = M_e0 ... M_e(m-1) L_final.                    (2)
```

If the products retained a useful observable and the boundary actions
composed cheaply over time, this could be a route to bulk evaluation.
Those additional requirements are not assumed proved. Here the local
identity itself forces the proposed encoding to forget every input digit.

The theorem covers invertible matrices of any size over any field,
including matrices with rational-function entries or a spectral parameter:
all are group elements wherever the inverses are defined. It does not
assume commutativity or a particular matrix ansatz.

## 2. Complete classification in a group

**Theorem.** Every solution of (1) has

```
L_A=L_B=L_C=L,
M_0=M_1=M_2=M_3=M,
L M=M L.                                        (3)
```

Conversely, any commuting pair L,M gives such a solution.

**Proof.** The indicated input/state pairs give the following steps.

1. B3 and C3 both have right side M0 L_A. Thus
   `L_B M3=L_C M3`, and right cancellation gives L_B=L_C.
2. B0 and C0 have the same left side after step1. Their right sides
   are M1 L_B and M3 L_C. Therefore M1=M3.
3. B2 gives `L_B M2=M3 L_C=M1 L_B=L_B M0`, the last equality being
   B0. Thus M2=M0.
4. A0 and A2 now give
   `M0 L_A=L_A M0=L_A M2=M2 L_C=M0 L_C`.
   Left cancellation gives L_A=L_C.
5. Finally A0 and B0 give `M0 L_A=L_A M0=L_B M0=M1 L_B`.
   Right cancellation gives M0=M1.

All state elements and all digit elements have collapsed as claimed.
Substitution in any local equation leaves exactly L M=M L, which also
proves sufficiency. QED.

Thus the encoded product of any length-m input word is simply M^m.
It cannot distinguish two words of the same length, let alone encode a
specified interior digit. Computing a departing automaton state outside
this product would be a separate task, not information supplied by (2).

## 3. The actual orbit visits the required tiles

The local identity might be required only on tiles that genuinely occur
when constructing B^t(0). That restriction does not weaken this result:
the first seven digits through nine B updates visit all12 pairs (g,d).

Some of their first witnesses are particularly small:

| Tile | B update | Zero-based digit position | Actual input prefix |
|---|---:|---:|---|
| B0 | 1 | 0 | 0 |
| B2 | 3 | 0 | 2 |
| B3 | 4 | 0 | 3 |
| C3 | 4 | 2 | 313 |
| A0 | 5 | 2 | 030 |
| C0 | 6 | 1 | 10 |
| A2 | 9 | 6 | 0030332 |

These seven already supply the equations in the proof. The final witness
has B^8(0) prefix0030332 and B^9(0) prefix1100102, so its entering
state at position6 is A. A witness at an arbitrary current predecessor
is not substituted for this actual chronology.

Each row is independently checked by evolving the original integer B_0
from0 and then taking its seven-digit Phi prefix. Only63 local digit
transitions are used. This verifies tile reachability; it does not infer
an infinite property from a finite apparent pattern.

## 4. Exact verifier and limitations

The [verifier](../../experiments/rule30/p3_multiplicative_transport.py)
saves a symbolic proof certificate. Each deduction records a path of
the original local equations after earlier substitutions, followed by
one legal group cancellation. No enumeration of a small matrix group
is used to infer the theorem for arbitrary groups.
The [artifact](../../experiments/rule30/p3-multiplicative-transport.json)
also retains every actual tile witness and both implementations' checks.

Rank-deficient matrices need separate treatment because cancellation
is unavailable. Likewise, a state or digit encoding that depends on
position, time, a larger block, or additional carried data does not have
the form (1). None is ruled out merely by this theorem. The generic
existence of a local transport would also have required an exact
observable and a construction-cost proof before becoming a P3 algorithm.

```
uv run --offline --no-project python experiments/rule30/p3_multiplicative_transport.py
```

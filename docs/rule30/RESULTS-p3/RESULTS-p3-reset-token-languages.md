# Exact reset tokens and a failed four-pass return for K

Date: 2026-09-13. **Two K passes have an explicit bijective description
on every even-digit input stream. Their output is a simple constrained
language. Four passes do not return these streams to even digits, and
the actual eighth iterate escapes a natural decorated union of the two
languages.** These results identify a precise limitation of the proposed
reset-token renormalization. They do not exclude other finite token
families or prove a complexity bound for the singleton query.

The [verifier](../../experiments/rule30/p3_reset_token_languages.py) and
[artifact](../../experiments/rule30/p3-reset-token-languages.json) retain
complete finite automata, local induction checks, and actual infinite-tail
certificates. No growing-index census or long center prefix is generated.

## 1. The complete two-pass reset language

Use the [itinerary automaton](RESULTS-p3-itinerary-conjugacy.md), with
states A,B,C, digit permutations `(0,3,2,1)`, `(1,2,3,0)`, `(3,2,1,0)`,
and next state `psi(output)`, where `psi=(A,B,C,C)`.
Two passes retain the ordered pair of states. An input word is a
*universal two-pass reset* if its transition sends all nine entering
pairs to one pair. This does not mean merely resetting the first pass.

Start with the set of all nine pairs and apply each of the four input
digits to every element of the current set. This subset automaton closes
in exactly22 states. The saved transition table checks every edge by an
independent arithmetic implementation of the permutations. A word resets
exactly when its resulting subset is a singleton. The shortest reset is
`12`; all seven reachable singleton subsets have saved representatives.
Closure makes this an exact all-word language recognizer, not a test of
only words up to the length of its representatives.

The actual stream `K^4(0)=(02)^infinity` has no universal two-pass reset
anywhere. Its subset/phase path has transient4 and period2 and never
reaches a singleton. A resetting substring would force the complete
prefix ending there to be a singleton, so the certificate excludes
resetting substrings as well as resetting prefixes. The nonreset graph
contains unrestricted zero/two and zero/three corridors: neutral zeros
do not make a uniform reset-spacing argument possible.

Thus a complete reset-only decomposition already needs an exceptional
nonreset corridor for an actual singleton-derived itinerary. No claim
is made that actual later itineraries explore every word in a corridor.

## 2. An exact all-word image of the even-digit corridor

Let `E={0,2}^infinity`. Write an input as `d_t=2*b_t`, and set

```
r_(-1)=0,  r_t=r_(t-1) XOR b_t,
e_0=0,     e_(t+1)=(1-r_t)*(1-e_t).
```

**Theorem.** Starting both passes in C,

```
K^2(d)_t = e_t + 2*r_t.                            (1)
```

Proof. On even input digits the first pass stays in B or C, with state C
exactly when the prefix parity is zero. Its emitted digit is
`1+2*(1-r_t)`. For the second pass let `e_t` indicate that its entering
state is A. On input1 or3, its output low bit is `e_t`, and its high bit
is `r_t`. Its next state is A precisely when the emitted digit is zero,
giving the displayed recurrence. This proves (1) by induction for every
finite or infinite input word; the verifier checks all local induction
cases, including the two second-pass states represented by `e=0`.

Consequently `K^2(E)` is exactly the language R defined by

```
z_0 is even,
lowbit(z_(t+1)) = 1[z_t=0]  for every t>=0.         (2)
```

There is no additional hidden ancestry condition. Given a word satisfying
(2), take `r_t=highbit(z_t)` and recover
`b_t=r_t XOR r_(t-1)`. Its low bits then follow (1) from the specified
initial value. This proves both necessity and sufficiency.

Formula (1) is an explicit two-state construction once the input prefix
parities are retained. It takes linear digit work on a supplied stream.
It does not construct its input stream or jump through an unbounded
number of K iterates for free.

## 3. Four passes do not return the corridor to itself

The concrete closure candidate `K^4(E) subset E` is false. Its shortest
finite witness is

```
input200 -> output203.                            (3)
```

The four-pass automaton, started in `(C,C,C,C)` and restricted to even
input digits, has exactly17 reachable states. The verifier retains every
one of its34 transitions and a shortest representative for each state.
Breadth-first search certifies that the earliest odd output can occur
after three input digits and that (3) is a shortest witness.

There is also a complete actual-orbit certificate:

```
K^4(0) = (02)^infinity,
K^6(0) = 03(2012)^infinity,
K^8(0) = 00202(2013)^infinity.                     (4)
```

The last equality comes from the closed four-pass state/phase orbit on
the input `(02)^infinity`: transient5, period4. Its first odd output is
at digit7. A separate scalar-bit H computation checks the full orbit of
the finite core `C^8(0)=51424`, including the return edge, and agrees with
the same prefix and cycle. The two corresponding center readouts at
times14 and15 also agree with independent singleton evolution.

## 4. A natural decorated union still fails

Consider the union of E and R, allowing any fixed alphabet permutation
applied to every digit, any shift of the tail, and any finite prefix before
the tail.
This is a stronger family than just E and R with their stated initial
conditions. It is still not closed under two K passes: `K^6(0)` belongs
to R, but the eventual tail of `K^8(0)` belongs to none of these decorated
families.

Indeed, a periodic R tail satisfies the counting identity

```
number(1)+number(3) = number(0)                    (5)
```

over each digit period: sum (2) around the cycle. The period2013
contains every digit once. So does every fixed alphabet permutation of it,
and (5) would incorrectly require `2=1`. The tail cannot belong to a
relabeling of E either, since it uses four symbols. Phase shifts and
finite prefixes do not change either argument.

This refutes exactly this decorated two-language closure, not arbitrary
block codings, larger token alphabets, or repetition grammars. The
[repetition-node transducer](RESULTS-p3-itinerary-repeat-transduction.md)
remains an exact one-pass construction. A useful new renormalization
would have to retain a language beyond the two families above and prove
that its boundaries and descriptors can be constructed cheaply under
iteration. No such iterative closure is established here.

```
uv run --offline --no-project python experiments/rule30/p3_reset_token_languages.py
```

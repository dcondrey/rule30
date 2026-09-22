# A fixed finite autonomous profile cannot close the B seed orbit

Date: 2026-09-14. **No uniformly bounded finite state can advance the B
seed orbit for arbitrarily many iterations and recover the last digit at
every requested prefix length.** This remains true if the transition,
initial state, and readout depend on the prefix length. The conclusion
concerns autonomous summaries of successive **time iterates**; it is not
a bound on spatial transducers, general algorithms, or the singleton
query restricted to its coupled time and position.

This supplies an all-length limit on replacing a constructed digit
expression by a fixed finite profile before its next B action. The
[verifier](../../experiments/rule30/p3_autonomous_profile_bound.py) and
[artifact](../../experiments/rule30/p3-autonomous-profile-bound.json)
check its exact small controls. The theorem itself follows from the
leading-bit induction and finite-state periods below.

## 1. Unbounded periods with an explicit bound

Write B_0 for the original binary generator

```
B_0(x)=x XOR((x<<1) OR(x<<2)) XOR1,
```

and B=Phi B_0 Phi^(-1) for its
[itinerary conjugate](RESULTS-p3-itinerary-conjugacy.md). The seed is0
in both coordinates. For every positive time t,

```
highest_one(B_0^t(0))=2t-2.                       (1)
```

Indeed B_0(0)=1. For any positive integer with highest one at position d,
the term x<<2 supplies a one at d+2; neither x, x<<1, nor the final XOR1
can cancel it. This proves (1) by induction.

Let P_m be the primitive zero-orbit period of B modulo4^m, m>=1.
Every finite-prefix action is a permutation, so this orbit has no
transient. Binary-prefix compatibility implies that P_m is a power of
two: adjoining a binary coordinate preserves or doubles a cycle period.
The P_m also form a divisibility chain.

The itinerary map fixes0 and preserves the first differing binary bit.
Consequently B^P_m(0)=0 modulo4^m implies
B_0^P_m(0)=0 modulo2^(2m). The latter integer is positive by (1), so its
highest one must be at position at least2m. Thus

```
2P_m-2 >= 2m,  hence P_m >= m+1.                 (2)
```

In particular these actual seed periods are unbounded. No arbitrary
input or presumed random behavior is used. Equation (2) is only a lower
bound; it is not an asserted asymptotic growth law.

## 2. The exact summary model and its lower bound

For each prefix length j>=1, allow a finite set S_j, an initial state
s_j, an autonomous transition T_j:S_j->S_j, and a readout
d_j:S_j->{0,1,2,3}. Suppose they satisfy

```
d_j(T_j^t(s_j)) = digit_(j-1)(B^t(0))
                 for every t>=0.                (3)
```

The sets, transitions, initializers, and readouts may depend arbitrarily
on j. The hypothesis is exactness for every time with a time-independent
transition on that state's finite set. No cheap construction assumption
is imposed.

Let r_j be the primitive temporal period of the digit on the right of
(3). It divides P_j and therefore is a power of two. The primitive
period of the complete first m digits is the least common multiple of
their primitive coordinate periods. Hence

```
P_m=lcm(r_1,...,r_m)=max(r_1,...,r_m).            (4)
```

An orbit of T_j eventually enters a state cycle of length q_j<=|S_j|.
Its output is eventually periodic with period q_j. The target output
in (3) is purely periodic from time0, with primitive period r_j, so
r_j divides q_j. To justify the last step explicitly, any eventual
period of a purely periodic word is also a period of the entire word:
move a proposed comparison forward by enough multiples of r_j to put
both positions past the transient. The primitive period then divides it.

Choose j<=m attaining the maximum in (4). We obtain the all-length bound

```
max_(1<=j<=m)|S_j| >= P_m >= m+1.                 (5)
```

Therefore no uniform finite bound on all |S_j| is possible. A common
fixed finite profile closed under repeated B action, with the last-digit
readout at every prefix length, would give exactly such a family and is
excluded. The argument applies already to the actual seed orbit, without
extending a proposed summary to unrelated inputs.

## 3. Limits that matter for P3

Equation (5) counts possible states, not stored bits or computation
steps. Distinguishing m+1 states needs only logarithmically many bits.
It does not prove a linear space or time lower bound for an algorithm.

It also permits growing symbolic profiles, compressed transition
systems, and time-dependent procedures that read the binary index.
The three-state spatial B transducer is consistent with this theorem:
it scans a supplied digit word once, rather than storing a uniformly
bounded temporal summary of arbitrarily many B iterates.

Finally, (3) demands all times at each fixed depth. The singleton problem
asks one coupled time/position pair for each n. A procedure correct only
on those pairs need not realize (3). The bound therefore does not
establish an unrestricted P3 lower bound or exclude a sublinear
singleton algorithm. Its practical conclusion is confined to the
proposed fixed finite autonomous closure mechanism.

## 4. Independent exact controls

The verifier replays the already certified B zero orbit on three digits:
its primitive period is32. At every time through the return edge, a
separate original-integer B_0 evolution followed by Phi agrees with the
digit transducer. The three individual digit streams have primitive
periods4,8,32. Thus at these particular depths their autonomous summaries
would require at least4,8,32 states respectively.

The observed values are controls, not the basis for extending (2) or
(5) to all lengths. No larger automaton closure or growing query census
is performed.

```
uv run --offline --no-project python experiments/rule30/p3_autonomous_profile_bound.py
```

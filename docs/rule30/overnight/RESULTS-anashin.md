# RESULTS — arm "anashin": 2-adic ergodicity along the time direction

STATUS: KILLED — the Anashin route is retired, at three independent levels, any one of which
is fatal. Verified "holds" by adversarial verification and re-checked independently here.

This arm was launched at user direction on a lead I had endorsed. It is killed partly by
correcting my own reasoning, which is recorded below rather than quietly dropped.

## What I predicted, and what is actually true

I predicted the 1-Lipschitz property would FAIL, since Rule 30 has radius 1 on both sides so
new bit i depends on bit i+1 under either natural encoding. That prediction was WRONG in an
interesting way: a COMOVING frame at the light-cone edge restores it. Setting
x_j(t) = s(t, t-j) (right cone edge) gives
    x_j(t+1) = x_j(t) XOR (x_{j-1}(t) OR x_{j-2}(t)),  i.e.  y = x ^ ((x<<1) | (x<<2)),
a genuine 1-Lipschitz self-map of Z_2, computed by a 4-state Mealy automaton. The left-edge
frame gives y = (x<<2) ^ ((x<<1) | x), which is literally this repo's own shifted-frame
generator. So obstacle (A) is solved, and Anashin's automata-finiteness criterion is satisfied.

Prior-art note flagged by the verifier and upheld: the left-frame map is the repo's existing
generator, so its "discovery" here is not new and is attributed accordingly.

## Kill reason 1 — non-separating

Rule 90 has the identical structure: y = x ^ (x<<2) in the right-edge frame, also 1-Lipschitz,
also a 4-state Mealy automaton, also measure-preserving. VERIFIED here: both maps are bijective
mod 2^k for k = 1, 2, 3, 4, 8, 12, 16. Since Rule 90's single-seed center column is eventually
0, the mere existence of the Anashin object, its measure-preservation, and its automaton
finiteness are all non-separating and prove nothing.

## Kill reason 2 — Rule 30 is not Anashin-ergodic

Ergodicity in Anashin's sense requires transitivity, i.e. a single 2^k-cycle, for every k.
VERIFIED here by exhaustive cycle enumeration: Rule 30's comoving map is bijective but NOT a
single cycle at k = 1, 2, 3, 4, ..., 16. It fails immediately, at k = 1. (The agent additionally
reports failure at k = 2 on the specific coset carrying the single-seed orbit, checked to
k = 16.) The criterion therefore does not apply at all.

## Kill reason 3 — even transitivity would not have given P2

This is the correction to my own argument. I told the user that Anashin-transitivity escapes the
Rule 90 ensemble wall because a single cycle forces EVERY orbit to equidistribute, including the
seed's. The first half is right; the conclusion does not follow, and here is why.

Under this encoding the center column is the DIAGONAL digit: s(t,0) = bit_t(x_t). It is not a
fixed coordinate of the orbit, so equidistribution of the orbit sequence in Z_2 does not control
it. Counterexample, VERIFIED here: the odometer f(x) = x + 1 is maximally Anashin-ergodic (a
single cycle mod 2^k for every k), yet starting from x_0 = 0 gives x_t = t, whose diagonal digit
bit_t(t) is identically 0 for every t >= 0 — because t < 2^t. Maximal 2-adic ergodicity is
therefore compatible with a diagonal digit of density 0. My chain from transitivity to P2 was
invalid, independent of whether Rule 30 satisfies transitivity.

## Kill reason 4 — no bounded-index 1-Lipschitz encoding can exist unless P1 is false

Stronger than the above, and frame-independent. If there exist a 1-Lipschitz f : Z_2 -> Z_2, a
point x_0, a FINITE bit-index set S and a map phi with s(t,0) = phi(bits_S(x_t)) for all t,
then the center column is eventually periodic with eventual period a power of 2, at most
2^(max(S)+1). Proof: for 1-Lipschitz f the low bits form an autonomous system on 2^k states, so
every orbit is eventually periodic mod 2^k, and eventual periods double at most one level at a
time, hence are powers of 2. Converse: if the column were periodic with period 2^m, the
odometer with S = {0..m-1} realizes such an encoding.

So searching for ANY bounded-index 1-Lipschitz state object carrying the center column is
exactly as hard as refuting P1. This closes every reformulation the lead listed — other
encodings, quotients, van der Put coefficients, right-aligned rows, skew products over a
1-Lipschitz base — in one step, rather than one at a time.

## Corrections and attributions

- Citation: the measure-preserving/ergodic <=> bijective/transitive mod p^k criterion is
  Anashin, "Uniformly distributed sequences of p-adic integers", Mathematical Notes 55 (1994)
  109-133, DOI 10.1007/BF02113290 — NOT the 2012 van der Put paper (arXiv:1112.5089), which is
  the automata-finiteness criterion. The workflow initially attributed the former to the latter;
  corrected here.
- Frame asymmetry: only the RIGHT-edge frame is measure-preserving. The left-edge frame (the
  repo's own generator) is NOT: its image mod 2^8 has 101 of 256 elements, because y_j depends
  on x_j through an OR. That asymmetry is left-permutivity restated.
- Prior art: the eventual periodicity with power-of-two period of each fixed cone-edge column
  follows from 1-Lipschitzness alone and is adjacent to Rowland 2006 Lemma 2, already in the
  repo. Labelled validation, not discovery.

## Obstacle (B), settled frame-independently

The right half-line is not invariant (cell 0's update needs cell -1), so there is no self-map on
that object; the repo's own injectivity statement is a skew product over the trace. The comoving
frames evade this by moving with the light cone, which is why they work. But the comoving
frames are exactly what kill reasons 1-3 then dispose of.

## Honest assessment

Advances P1, P2, P3 by zero, and no repaired version looks viable: the three kill reasons are
independent, so patching any one leaves the others standing. The durable value is a permanent,
documented retirement of a route that looks attractive from the outside — 2-adic ergodicity is
the natural thing to reach for once one notices that ensemble ergodicity fails — together with
the odometer counterexample, which is a compact reason that NO 2-adic equidistribution statement
in this encoding can reach the center column.

## Reproduction

Comoving maps, bijectivity and cycle structure mod 2^k, and the odometer counterexample are all
short direct computations from the maps given below; no standalone script is checked in. Rule 30
right-edge frame: y = x ^ ((x<<1)|(x<<2)); Rule 90: y = x ^ (x<<2); odometer: x -> x+1 with
diagonal digit bit_t(x_t).

## Spending

Local CPU only. Modal $0.

# An exact history-preserving law for variable-length frontier episodes

Date: 2026-09-09. Based on commit `6f91a43`.

**A variable-length episode can be composed exactly from an autonomous
forward prefix and a terminal-driven backward suffix, joined by a two-bit
compatibility test at every update.** The suffix accumulated before a switch
must be carried through the switch. Resetting it gives a verified false
continuation.

History reconstruction also sharpens the previous constant-scalar bound:
an episode begun at active length r has

```
length <= r-1  for scalar 0,
length <= r    for scalar 1.
```

Both statements have uniform proofs below. They do not prove mortality,
period-two exclusion, P1 or P2. They supply an explicit episode interface
and a stronger bound on individual episodes.

## 1. Exact object, prior ingredients, and provenance

The state is a nonempty finite word w over `{0,1,2,3}`, with
`w_i=2*a_i+b_i` and `a_0=1`. It is the reversed zero-cost frontier, not a
spatial row of the original Rule 30 automaton. Its partial update Z scans
left to right from memory `(u,v,alpha)=(0,0,0)`:

```
v' = v XOR (alpha OR b_i),
u' = u XOR (v' OR a_i),
emit (u',v'),   next memory = (u',v',a_i).
```

The update succeeds precisely when its final u and v agree. Their common
value s is the terminal scalar. A successful update appends `(1,1 XOR s)`,
encoded as `3-s`, and increases the frontier length by one. The invariant
first coordinate remains `a_0=1`.

The scan, scalar-history reconstruction, and anchored one-step extensions
are prior work in `experiments/rule30/image-dfa/image_dfa.py:31,218`,
`experiments/rule30/panel/cert33.py:3,19`, and the panel transcripts. See
[the original frontier report](RESULTS-alt-trace-fiber.md) at its
reversed-coordinate and sector-reconstruction sections (lines 530 and 730).
Their reconstruction theorem is not claimed as a new discovery here.

The contribution here is the arbitrary-cut, all-times composition interface,
its exact intermediate matching condition, the episode implementation and
independent checks, and the sharper phase-specific bound in §5. The new
code imports the two frozen engines unchanged.

The surviving-episode and reset witnesses below are actual trajectories of
Z from specified legal frontiers; rejected formal tapes are identified as
such. No example is asserted to arise from the original lone-seed Rule 30
orbit. If a starting frontier has that provenance, the composition law
preserves its continuation; the law does not supply the provenance.

## 2. A factorization from both ends

Choose any spatial cut `w=P S`, where P is a nonempty prefix containing
site zero and S is a possibly empty suffix. Keep this cut fixed during
transport. Let B(P) be the emitted prefix obtained by scanning P from zero
memory, and let h(P) be the exit memory. B is total on legal prefixes,
whether or not the complete frontier survives.

For a proposed terminal scalar s, define a total suffix map R_s as follows.
If S is empty, put `R_s(S)=(3-s)`. Otherwise write its pairs as
`(a_i,b_i)`, `0<=i<m`. Set the last pre-append output pair to `(s,s)` and
solve backward, for `i=m-1,...,1`:

```
u_(i-1) = u_i XOR (v_i OR a_i),
v_(i-1) = v_i XOR (a_(i-1) OR b_i).
```

Append `(1,1 XOR s)`. This constructs all m+1 pairs of R_s(S) using only
S and s. No fresh prefix or exterior bits are selected.

Define the Boolean compatibility test C_s(P,S):

* If S is nonempty, scanning its first symbol from h(P) must emit the
  first symbol of R_s(S). This is equality of two bits.
* If S is empty, the u,v components of h(P) must equal `(s,s)`.

**One-step factorization.** Z(P S) exists and emits scalar s if and only if
C_s(P,S) holds. When it holds,

```
Z(P S) = B(P) R_s(S).                                      (1)
```

**Proof.** The backward formulas are exact rearrangements of the forward
scan. If S is nonempty, C_s matches its first output pair. The resulting
alpha is its first input high bit on both sides, so the complete three-bit
memory agrees immediately after that symbol. Determinism then makes every
following suffix output agree. The reconstructed last pair is `(s,s)`,
which supplies survival, and the appended symbol also agrees. Conversely,
every surviving forward scan satisfies the same backward equations, so it
has the reconstructed suffix and passes the test. The empty case is exactly
the original terminal test. This proves (1) for every cut and every length.

The prefix therefore governs compatibility; the suffix itself is transported
by the chronological terminal history. This separates construction from the
condition under which it belongs to the given starting frontier.

## 3. The history-preserving composition law

For a chronological scalar word `alpha=s_0...s_(n-1)`, define

```
R_alpha = R_(s_(n-1)) o ... o R_(s_0),
P_j = B^j(P),
S_j = R_(s_0...s_(j-1))(S),
K_alpha(P,S) = AND_(0<=j<n) C_(s_j)(P_j,S_j).
```

The empty word has identity transport and compatibility true. These formal
transports remain defined even after a failed test; such a path is accepted
only if **every** test passes.

**Composition theorem.** For arbitrary finite scalar words alpha and gamma,

```
R_(alpha gamma)(S) = R_gamma(R_alpha(S)),

K_(alpha gamma)(P,S)
  = K_alpha(P,S)
    AND K_gamma(B^|alpha|(P), R_alpha(S)).                 (2)
```

Moreover K_alpha is true if and only if the actual orbit of the same
frontier P S survives n updates with exactly that scalar word. In that case

```
Z^n(P S) = B^n(P) R_alpha(S).                             (3)
```

**Proof.** Apply (1) successively. The endpoint of the first segment is
precisely the starting pair in the second compatibility factor of (2).
Associativity of concatenating the prescribed scalar tape gives the first
identity; splitting the list of intermediate guards gives the second.
Induction supplies both directions of (3), including failure at the first
bad guard. No compactness or fresh completion is used.

This is more specific than the identity `Z^(n+m)=Z^m o Z^n`: it constructs
the entire transported suffix without replaying the prefix through it,
identifies the exact seam data, and supplies the complete domain test.
The fixed initial prefix can be evolved independently. Its complement
keeps every appended cell through episode boundaries.

A **constant-scalar episode** is a maximal block `s^ell` in the successful
scalar tape. At a switch, the first update of the new phase is not consumed
by the preceding episode. Apply (2) with alpha and gamma equal to successive
constant blocks, whose lengths are determined dynamically. No fixed episode
length or decrease at every update is assumed.

The implementation preserves both pieces at each return. It also records
every guard on proposed tapes: a later true guard never repairs a failed
past. For example, formal tape `0001` from frontier `2` has guard sequence
`false,false,false,true`. Testing only its endpoint would be unsound.

## 4. An episode seam where resetting history changes the answer

Start with frontier `3000002` and take P to be that entire initial word,
S empty. Its exact maximal episode itinerary is:

| Episode | Scalar | Successful updates | Prefix afterward | Suffix afterward | Next event |
|---:|---:|---:|---|---|---|
| 1 | 0 | 2 | `3030303` | `03` | switch |
| 2 | 1 | 1 | `3210321` | `032` | switch |
| 3 | 0 | 1 | `3031210` | `0303` | death |

At the second switch, the full frontier is `3210321032`. Carrying suffix
`032` gives one successful zero update and then death. Resetting that suffix
to empty instead creates the different frontier `3210321`, which admits a
zero episode of length two followed by a one. It falsely permits `00` as
the continuation of the original history.

The failed extra step can be located in the two-bit guard. The actual
prefix is then `3031210`, with exit memory `6=(1,1,0)`, and suffix `0303`.
R_0 of that suffix starts with symbol 3, while the forward seam emits 1.
The reset suffix at the corresponding step is merely `3`; its required
and actual first outputs are both zero, so the changed state passes.

Even keeping the same length and sector does not make episode metadata a
sufficient state. Frontiers `210123` and `201200` both have length 6 and
sector zero, both emit a first episode consisting of one scalar 1, and
both next enter a zero episode at length 7. Those next episodes have
lengths one and two respectively. Full states and continuations are
recorded in `verification.json`.

## 5. A stronger uniform bound on each episode

Consider L successful updates with constant scalar s, starting at active
length r. At time n within the episode, introduce depth measured inward
from the current terminal end:

```
A_d(n) = a_(r+n-1-d)(n),
B_d(n) = b_(r+n-1-d)(n).
```

For n>=1 the terminal data are

```
A_0=1, B_0=1 XOR s_(n-1), A_1=B_1=s_(n-1).
```

Rearranging the scan backward, for d>=2, gives

```
A_d(n) = A_(d-1)(n)
         XOR (B_(d-1)(n) OR A_(d-2)(n-1)),
B_d(n) = B_(d-1)(n)
         XOR (A_(d-1)(n-1) OR B_(d-2)(n-1)).            (4)
```

Let F_d(n),G_d(n) be the formal scalar-history fields with these boundary
data and recurrences. The existing reconstruction argument can be expressed
with the following separate depth thresholds:

```
A_d(n)=F_d(n)  whenever n >= 1+floor(d/2),
B_d(n)=G_d(n)  whenever n >= 1+ceil(d/2),              (5)
```

provided the physical site exists. These sufficient thresholds mean that
the required cells depend only on emissions since this episode began,
even though the frontier at its onset contains earlier history.

For completeness, simultaneous induction on n and then d proves (5).
The A recurrence needs A_(d-1), B_(d-1) at time n and A_(d-2) at n-1;
their three thresholds follow from the A threshold. The B recurrence
needs B_(d-1) at n and A_(d-1), B_(d-2) at n-1; the B threshold implies
all three. The terminal depths zero and one supply the bases. Thus the
argument is uniform in frontier length, not inferred from the census.

On a constant scalar history s, these fields satisfy

```
F_d(n) = G_d(n) = s XOR ((d-1) mod 2),   d>=1,          (6)
```

where each field is used within its reconstruction domain. Check depths
one and two directly. At greater depths each OR in (4)
joins complementary consecutive values, so it equals one and proves
(6) inductively.

If L>=r, set n=r. Site zero has depth `2r-1`, which is within A's
reconstruction domain. Its invariant value therefore forces `1=a_0=s`.
Consequently **s=0 implies L<=r-1**.

If L>=r+1, set n=r+1. Site zero now has depth `2r`, also reconstructed,
so `1=a_0=1 XOR s`. This contradicts the previous s=1. Consequently
**s=1 implies L<=r**. Both bounds include arbitrary episode onsets.

The old bound `2r-1` remains valid; this is a sharpening, not a repair of
a false statement. The extreme small cases occur: frontier `3` starts
with one scalar 1 at r=1, and frontier `32` emits one scalar 0 at r=2.
No optimality claim is made at every r.

If N successful updates occupy m constant runs, including a possibly
unfinished final run, their onset lengths satisfy
`r_(i+1) <= 2*r_i-1+s_i <= 2*r_i`. Hence

```
r+N <= 2^m*r,
m >= ceil(log2(1+N/r)).                                (7)
```

This quantifies the required switching. It is compatible with infinitely
many episodes and growing frontier lengths, so it is not a mortality proof.

## 6. Verification and reproduction

Code: `experiments/rule30/episode-composition/episodes.py` and `verify.py`.
The checker compares the new factorized transport against both unmodified
`cert33.direct_step` and `image_dfa.macro`.

| Check | Exact coverage |
|---|---:|
| Local reverse-scan identities | all 32 memory/symbol cases |
| Reverse suffix versus arbitrary entering memories, lengths 0–7 | 87,380 accepted scans, including four empty-suffix cases |
| Both proposed scalars at every spatial cut, legal lengths 1–7 | 145,636 cases |
| Every scalar tape of length 0–6 at every cut, legal starts of length 1–4 | 79,502 cases |
| Every temporal split of those tapes, including invalid histories | 481,394 composition checks |
| Complete initial-frontier census, lengths 1–9 | 174,762 starts; 173,478 successful updates |
| Phase-specific bound at every constant-run onset in that census | 133,546 episodes |

The complete episode engine also matches uninterrupted evolution on every
legal start of length at most seven, at cuts one and the initial length.
The two reset/metadata witnesses are independently replayed. There are
18,811 cases in the prescribed-tape census whose final guard is true but
whose history is rejected, reinforcing the need for all intermediate guards.

Run from the project directory:

```
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/episode-composition/verify.py
```

`verification.json` records counts, witnesses, the illustrated itinerary,
and SHA-256 hashes of the implementation and frozen engines. A computational
cap raises an inconclusive error, never a death verdict. The mathematical
arguments in §§2–5 provide the all-length statements; the finite checks
verify the implementation and their boundaries.

The next missing theorem is about **net progress across successive episodes**.
We now know exactly how to compose them and what history must cross a switch.
We have not found a seed-derived resource that cannot be replenished, or
proved that the successive episodes must end.

## Follow-up, 2026-09-09

The valid bounds above have been sharpened further: a frontier of length
R>=3 carrying the terminal pair of a preceding successful update admits at
most R-3 consecutive zeros; an arbitrary legal frontier of length R>=2
admits at most R-2 consecutive ones. The small-length exceptions are explicit.
The boundary credit does not accumulate with switches, and transported
suffixes can erase distinct accepted histories. The composition theorem
preserves a given continuation, not an injective record of its past.

See [RESULTS-episode-memory-and-repeat-budget.md](RESULTS-episode-memory-and-repeat-budget.md)
for the uniform proofs, exact inverse fibers, a finite repeat-budget test,
and the executed prescribed-tape preimage-language method. Mortality remains
open.
